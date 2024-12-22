---
title: SharedTransitionObserver 内存泄漏问题
date: 2024-12-22 17:06:43
tags: Compose
categories: 开发问题记录
---

# SharedTransitionObserver 内存泄漏问题

问题背景：

项目中使用 SharedTransitionLayout 来完成 两个元素之间的共享元素动画，但是，在持有该共享元素组件的页面退出之后，发现有内存泄漏，GCROOT 指向的是 SharedTransitionObserver 单例对象 中的一个列表中的元素。

```kotlin
java.lang.Object[] array
│    Leaking: NO (SharedTransitionScopeKt↓ is not leaking)
│    ↓ Object[1722]
├─ androidx.compose.animation.SharedTransitionScopeKt class
│    Leaking: NO (a class is never leaking)
│    ↓ static SharedTransitionScopeKt.SharedTransitionObserver$delegate
│                                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
├─ kotlin.UnsafeLazyImpl instance
│    Leaking: UNKNOWN
│    Retaining 16 B in 1 objects
│    ↓ UnsafeLazyImpl._value
│                     ~~~~~~
├─ androidx.compose.runtime.snapshots.SnapshotStateObserver instance
│    Leaking: UNKNOWN
│    Retaining 401.3 kB in 9944 objects
│    ↓ SnapshotStateObserver.observedScopeMaps
│                            ~~~~~~~~~~~~~~~~~
├─ androidx.compose.runtime.collection.MutableVector instance
│    Leaking: UNKNOWN
│    Retaining 401.2 kB in 9940 objects
│    ↓ MutableVector.content
│                    ~~~~~~~
├─ androidx.compose.runtime.snapshots.SnapshotStateObserver$ObservedScopeMap[]
│  array
│    Leaking: UNKNOWN
│    Retaining 401.2 kB in 9939 objects
│    ↓ SnapshotStateObserver$ObservedScopeMap[0]
```

经过分析，在页面销毁之后，会从 单例对象 SharedTransitionObserver 中清除所有持有的观察者。

```kotlin
internal valSharedTransitionObserverbylazy(LazyThreadSafetyMode.NONE){SnapshotStateObserver{ it()}.also{ it.start()}}

```

![代码截图1](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221712196.png)

在 clear 方法中调用 remove 方法 清空 observedScopeMaps。

![代码截图2](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221712063.png)

但是，实际过程中发现，当页面销毁完之后，成功调用了 SharedTransitionObserver 的clear 方法，但是，在clear之后，还有 保存在 observedScopeMaps 列表里面的数据。推断是这里产生了泄漏。

怀疑 是 compose sdk 的 缺陷，所以 到 issuetracker 上搜索：

![issue tracker](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221713041.png)

果然发现有类似的反馈，并且和我们的相同。

最终找到了原因：[https://issuetracker.google.com/issues/347035242](https://issuetracker.google.com/issues/347035242)，

![issue tracker](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221713050.png)

最终的 修复版本为 1.8.0-alpha ，但是 我们的版本无法升级到 1.8.0-alpha。所以尝试通过反射，在页面销毁时，手动清理 observedScopeMaps。

```kotlin
private fun fixMemoryLeak() {
    kotlin.runCatching {
        // 使用反射访问 SnapshotStateObserver 单例对象
        // Step 1: 获取 top-level 属性所在的 Kotlin 文件类
        val myModuleClass = Class.forName("androidx.compose.animation.SharedTransitionScopeKt")
        // Step 2: 获取 SharedTransitionObserver 属性的 Field
        // 注意属性名称将被编译成顶层属性的名字加上 `INSTANCE`，即 `SharedTransitionObserver$delegate`
        val fieldName = "SharedTransitionObserver\$delegate"
        val field: Field = myModuleClass.getDeclaredField(fieldName)
        field.isAccessible = true
        // Step 3: 获取 lazy 代理的实例
        val lazyInstance = field.get(null)
        // Step 4: 使用 Kotlin 的 reflection API 来获取 Lazy 的 value 属性
        val sharedTransitionObserverInstance = (lazyInstance as? Lazy<*>)?.value
        Log.d(TAG, "SharedTransitionObserver 实例: $sharedTransitionObserverInstance")
        if (sharedTransitionObserverInstance != null) {
            // 使用反射访问 observedScopeMaps 成员变量
            val observedScopeMapsField =
                sharedTransitionObserverInstance::class.java.getDeclaredField("observedScopeMaps")
            observedScopeMapsField.isAccessible = true
            val observedScopeMapsValue =
                observedScopeMapsField.get(sharedTransitionObserverInstance)
            (observedScopeMapsValue as? MutableVector<*>)?.clear()
            Log.d(TAG, "fixMemoryLeak: $observedScopeMapsValue cleared")
        } else {
            Log.e(TAG, "fixMemoryLeak: can't find SnapshotStateObserver object")
        }
    }.onFailure {
        Log.e(TAG, "fixMemoryLeak: exception: ${it.getReportLog()}")
    }
}

```

通过测试，发现没有内存泄漏了。

问题产生原因：

DisposableEffect 确实按预期在 SharedTransitionScope 中被调用，随后从 SnapshotObserver 中移除了scope。但是当稍后移除共享元素状态时（这是每次转换结束时的常见用例），会调用一个代码路径，让scope再次开始观察。

官方修复方式：

```
Fix SharedTransitionObserver leaking scopes
   
    This change adds a diposed flag to the SharedTransitionScope
    to ensure after the scope is diposed, no observations can
    be made on the shared transition scope or on shared elements
    created in that scope. This prevents scopes from being
    added to the observer after the they are disposed, therefore
    preventing leaks.
    
修复 SharedTransitionObserver 泄漏作用域

		此更改为 SharedTransitionScope 添加了一个已处置标志，以确保在作用域被处置后，
		无法对共享过渡作用域或在该作用域内创建的共享元素进行观察。
		这防止了在作用域处置后将其添加到观察者中，从而防止了内存泄漏。
```

[https://android-review.googlesource.com/c/platform/frameworks/support/+/3132164/1/compose/animation/animation/src/commonMain/kotlin/androidx/compose/animation/SharedTransitionScope.kt#b671](https://android-review.googlesource.com/c/platform/frameworks/support/+/3132164/1/compose/animation/animation/src/commonMain/kotlin/androidx/compose/animation/SharedTransitionScope.kt#b671)

![bugfix code](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221713868.png)