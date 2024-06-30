---
title: Android Keyboard 高度监听实践
date: 2024-06-30 20:25:16
tags: Android
categories: Android 开发
---

最近遇到一个需求，需要输入框布局附着在软键盘上面，随着软键盘的上移下移动画而移动。要做到这一点，需要监听键盘的高度，而且最好是在键盘弹起的时候，每一帧都有一个高度的回调，这样，我们监听键盘高度的变化，对我们的输入框布局做transY动画 ，即可实现 输入框附着在键盘之上随之上下移动的动画效果了。

想要实现的效果：

![效果图](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202406302022019.gif)

但是，经过对android 键盘高度监听相关方法的了解，发现事情并没有那么简单。

Android 监听键盘高度 非常复杂。而且，有多种方式可以实现，并且对于不同的 Android 版本，其实现方式也各不相同。而且，由于Android 机型、版本众多，来自不同品牌、不同类型、不同版本的android  手机，相同的代码可能有不同的表现。

在很早之前，大家都是用 getViewTreeObserver().addOnGlobalLayoutListener  拿到Activity的ContentView，设置`contentView.getViewTreeObserver()                 .addOnGlobalLayoutListener(onGlobalLayoutListener);`

然后在监听内部再通过 `decorView.getWindowVisibleDisplayFrame`来获取显示的Rect，再通过 `decorView.getBottom() - outRect.bottom`的方式来获取高度。或者是 通过 添加一个宽度为0，高度撑满全屏的 PopupWindow 的骚操作来获取键盘的高度，让软键盘弹起的时候，计算PopopWindow移动了多少范围，从而计算软键盘的高度。而其中的关键就是当输入法弹出时， 它会把之前我们创建的那个看不见的弹窗往上挤， 这样我们创建的那个弹窗的位置就变化了，只要获取它底部高度的变化值就可以间接的获取输入法的高度了。

下面，简单介绍下，在 android 中 ，获取键盘高度的最新方式。在 Android R （Android 11 ，API 30）版本中，提供了 WindowInsets 相关API，新增了`WindowInsetsAnimation.Callback` 回调方法。 

什么是 Insets？

屏幕上除了开发者 app 绘制的内容还有系统的 Insets（嵌入物），Insets 区域负责描述屏幕的哪些部分会与系统 UI 相交。例如导航或状态栏。

常见的 Insets 有：

- `STATUS_BAR`，用于展示系统时间，电量，wifi 等信息
- `NAVIGATION_BAR`，虚拟导航栏（区别于实体的三大金刚键），形态有三大金刚键导航，手势导航两种。（有些设备形态如 TV 没有导航栏）
- `IME`，软键盘，用于输入文字

如果绘制的内容出现在了系统 UI 区域内，就可能出现视觉与手势的冲突。可以借助 Insets 把 view 从屏幕边缘向内移动到一个合适的位置。为了防止 App 内容区域与 `System bar`发生视觉冲突，官方提供了两种 API，`WidowInsets` 与  `fitsSystemWindows`。

**`WidowInsets`** 

**可以通过在自定义 View 中重写 `onApplyWindowInsets()` 方法或调用 `setOnApplyWindowInsetsListener()` 来监听 `WindowInsets` 的变化，通过对 View 添加 `margin` 或 `padding` 的方式处理解决冲突**。

```kotlin
editText.setOnApplyWindowInsetsListener(object : View.OnApplyWindowInsetsListener {
            override fun onApplyWindowInsets(v: View, insets: WindowInsets): WindowInsets {
                val statusBar = insets.getInsets(WindowInsets.Type.statusBars())
                val navBars = insets.getInsets(WindowInsets.Type.navigationBars())
                Log.i("MainActivity", "status bar: ${statusBar.bottom}, nav bar: ${navBars.bottom}")
                return insets
            }
        })
```

如何使用  window insets：( 版本 ≥ API 21 均可使用，windowInsetsCompat则为其兼容版本)

1. 使用 `ViewCompat.getRootWindowInsets(view)` 获取 `WindowInsets`
2. 通过 `WindowInsets#getInsets(type)` 获取 Insets
3. 通过 Insets.top 或 Insets.bottom 获取 `System bar` 高度

```kotlin
val windowInsetsCompat = ViewCompat.getRootWindowInsets(editText)
val ime = windowInsetsCompat?.getInsets(WindowInsetsCompat.Type.ime())
val height = ime?.bottom
```

**`fitsSystemWindows`**

**`SetFitsSystemWindows`** 是 View 中 API 14 后加入的方法，对应的 xml 属性是 **`android:fitsSystemWindows`**

```kotlin
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    **android:fitsSystemWindows="true"**
    tools:context=".MainActivity">
</androidx.constraintlayout.widget.ConstraintLayout>
```

**`FitsSystemWindows` 的默认行为是：通过 padding 为 `System bar` 预留出空间。**

关于 `fitsSystemWindows`：

- `fitsSystemWindows` 是深度优先（我们可以将视图树看成一个 N叉树）的，第一个设置 `fitsSystemWindows` 的 view 会去消费 insets 并影响视觉。
- 开发者在 xml 或 view 初始化设置的 padding 会被**覆盖。**
- [AppBarLayout](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.android.com%2Freference%2Fcom%2Fgoogle%2Fandroid%2Fmaterial%2Fappbar%2FAppBarLayout.html)，[CoordinatorLayout](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.android.com%2Freference%2Fandroidx%2Fcoordinatorlayout%2Fwidget%2FCoordinatorLayout.html)，[DrawerLayout](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.android.com%2Freference%2Fandroidx%2Fdrawerlayout%2Fwidget%2FDrawerLayout.html) 等 view 会自定义 `fitsSystemWindows` 的行为。

有了以上背景知识之后，我们来看如何使用 window insets 来监听键盘高度，首先，设置 setDecorFitsSystemWindows 为 false，来让内容区域全屏，然后去掉 android:fitsSystemWindows="true" （一定要去掉该属性）。设置完该属性后，发现下方内容都被系统的 nav bar 挡住了，出现了视觉冲突。可以使用以下代码来解决内容被系统bar 覆盖的问题。

首先设置 bar 为透明，然后，通过 setOnApplyWindowInsetsListener 来获取 window insets，获取系统bar 的高度之后，设置相应的padding。

**实现 边到边 (edge-to-edge) 沉浸式效果，并设置对应padding，不让系统bar 遮挡view内容。**

Android R 版本及以上的实现方式：

```kotlin
//1. 使内容区域全屏
window.setDecorFitsSystemWindows(false)
 // 2. 设置 System bar 透明
window.statusBarColor = Color.TRANSPARENT
window.navigationBarColor = Color.TRANSPARENT
val rootView = findViewById<View>(R.id.root_container)
rootView.setOnApplyWindowInsetsListener { v, insets ->
	val systemBars = insets.getInsets(WindowInsets.Type.systemBars())
  // 此处更改的 margin，也可设置 padding，视情况而定
  rootView.updateLayoutParams<ViewGroup.MarginLayoutParams> {
     topMargin = systemBars.top
     leftMargin = systemBars.left
     bottomMargin = systemBars.bottom
     rightMargin = systemBars.right
  }
  return@setOnApplyWindowInsetsListener insets
}
```

然后 设置 `WindowInsetsAnimation.Callback` 来监听 window insets 的高度变化。

```kotlin
 val editText = findViewById<EditText>(R.id.edit_text_view)
        val call = object : WindowInsetsAnimation.Callback(DISPATCH_MODE_CONTINUE_ON_SUBTREE) {
            @RequiresApi(Build.VERSION_CODES.R)
            override fun onProgress(
                insets: WindowInsets,
                runningAnimations: MutableList<WindowInsetsAnimation>
            ): WindowInsets {
                val navBar = insets.getInsets(WindowInsets.Type.navigationBars())
                val ime = insets.getInsets(WindowInsets.Type.ime())
                Log.i(
                    "MainActivity", "ime:" + ime.top +
                            " " + ime.bottom
                )
                val params = (editText.layoutParams as ViewGroup.MarginLayoutParams)
                params.bottomMargin = (ime.bottom - navBar.bottom).coerceAtLeast(0)
                editText.layoutParams = params
                return insets
            }
        }
```

在 onProgress 中，获取 ime 的 高度，并设置 输入框 view bottom margin 为 ime 高度 - nav bar高度，这样，输入框就会跟随键盘 弹起 和收起了。可以看到动画效果非常丝滑。

![录屏1](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202406302020246.gif)

<aside>
⛳ Android 提供了 WindowCompat 和 ViewCompat API 来对 小于 Android R 版本的 系统来进行兼容。具体实现代码如下所示，但是，经过我的实际测试，以下代码 无法在 低于 Android R 的设备上运行。
</aside>

原因分析： 我在 manifest xml 文件中设置了 
`android:windowSoftInputMode="stateAlwaysHidden|adjustNothing"` 属性，影响了低版本拿insets，此时获取到的 insets 为 null。在低版本上，各种SystemUiFlag都会影响到最终的显示效果。这里会有许多兼容性问题，不建议在 低版本机型上使用 windowinsets compat 的方式来监听键盘的高度。

```kotlin
// 1. 使内容区域全屏
WindowCompat.setDecorFitsSystemWindows(window, false)

// 2. 设置 System bar 透明
window.statusBarColor = Color.TRANSPARENT
window.navigationBarColor = Color.TRANSPARENT

// 3. 可能出现视觉冲突的 view 处理 insets
ViewCompat.setOnApplyWindowInsetsListener(view) { view, windowInsets ->
  val insets = windowInsets.getInsets(WindowInsetsCompat.Type.systemBars())
  // 此处更改的 margin，也可设置 padding，视情况而定
  view.updateLayoutParams<MarginLayoutParams> {
    	topMargin = insets.top
      leftMargin = insets.left
      bottomMargin = insets.bottom
      rightMargin = insets.right
  }
  WindowInsetsCompat.CONSUMED
}
val callback = object : WindowInsetsAnimationCompat.Callback(DISPATCH_MODE_CONTINUE_ON_SUBTREE) {

            override fun onPrepare(animation: WindowInsetsAnimationCompat) {
                super.onPrepare(animation)
            }

            override fun onStart(
                animation: WindowInsetsAnimationCompat,
                bounds: WindowInsetsAnimationCompat.BoundsCompat
            ): WindowInsetsAnimationCompat.BoundsCompat {
                return super.onStart(animation, bounds)
            }

            override fun onProgress(
                insets: WindowInsetsCompat,
                runningAnimations: MutableList<WindowInsetsAnimationCompat>
            ): WindowInsetsCompat {
                val navBar = insets.getInsets(WindowInsetsCompat.Type.navigationBars())
                val ime = insets.getInsets(WindowInsetsCompat.Type.ime())
                Log.i(
                    "MainActivity", "ime:" + ime.top +
                            " " + ime.bottom
                )
                val params = (editText.layoutParams as ViewGroup.MarginLayoutParams)
                params.bottomMargin = (ime.bottom - navBar.bottom).coerceAtLeast(0)
                editText.layoutParams = params
                return insets
            }

            override fun onEnd(animation: WindowInsetsAnimationCompat) {
                super.onEnd(animation)
            }
}
val editText = findViewById<EditText>(R.id.edit_text_view)
ViewCompat.setWindowInsetsAnimationCallback(editText, callback)
```

总结，针对键盘高度监听的问题，我们可以 根据 android 版本 和机型，做兼容性的处理，例如，判断 android 系统版本，在 Android R 及以上版本上，使用Window Insets Animation 的方式，以获得最佳的 键盘高度监听动画效果。在 Android R 以下版本 或者 类似 华为 三星等奇葩机型上，使用 addOnGlobalLayoutListener 结合 popup window 的方式监听键盘弹起时的高度变化。

参考：

[实现边到边的体验 | 让您的软键盘动起来 (一) - 掘金 (juejin.cn)](https://juejin.cn/post/6892118334762909709)

[Android：使用ViewCompat适配软键盘弹出，解决软键盘遮挡布局问题 - 掘金 (juejin.cn)](https://juejin.cn/post/7179128712141471802)

[处理视觉冲突 | 手势导航 (二) - 掘金 (juejin.cn)](https://juejin.cn/post/6844904006343458830)

[Android Detail：Window 篇—— WindowInsets 与 fitsSystemWindow - 掘金 (juejin.cn)](https://juejin.cn/post/7038422081528135687)