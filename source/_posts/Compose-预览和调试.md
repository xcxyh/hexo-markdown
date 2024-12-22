---
title: Compose 预览和调试
date: 2024-12-22 17:04:46
tags: Compose
categories: Android 开发
---

# Compose 预览和调试

# 预览

添加依赖

```kotlin
dependencies {
    implementation "androidx.compose.ui:ui:1.0.0"
    implementation "androidx.compose.material:material:1.0.0"
    debugImplementation "androidx.compose.ui:ui-tooling:1.2.1"  // 预览工具
	implementation "androidx.compose.ui:ui-tooling-preview:1.2.1"
}
```

添加  **`@Preview`** 注解

```kotlin
@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    PreviewDemoTheme {
        Greeting("Android")
    }
}
```

预览结果：

![Compose预览](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221701747.png)

Compose 预览功能的局限性：

1. **性能问题**：
   - Compose的预览速度较慢，特别是在代码修改后需要重新构建才能生效，这与传统XML布局相比显得不够高效。XML布局可以快速预览，而Compose依赖于Kotlin代码的编译，这导致了预览的延迟。
2. **功能限制**：
   - 在Compose预览中，某些Android框架的功能不可用，例如网络访问和文件访问。此外，一些**Context** API可能无法完全使用，这限制了开发者在预览中测试复杂组件的能力。
3. **ViewModel支持不足**：
   - 使用**ViewModel**时，Compose预览会受到限制。预览系统无法构建传递给**ViewModel**的所有参数，特别是在依赖注入（如使用Hilt）时，可能会导致渲染错误。因此，开发者需要创建额外的可组合项，将**ViewModel**中的参数传递给这些可组合项，以便进行有效的预览。

# 使用 layout inspector 调试

[布局检查器  |  Jetpack Compose  |  Android Developers](https://developer.android.com/develop/ui/compose/tooling/layout-inspector?hl=zh-cn)

[使用布局检查器调试您的布局  |  Android Studio  |  Android Developers](https://developer.android.com/studio/debug/layout-inspector?hl=zh-cn)

1. [启用设备的开发者选项](https://developer.android.com/studio/debug/dev-options?hl=zh-cn#enable)，然后在设备的开发者设置中开启[启用视图属性检查功能](https://developer.android.com/studio/debug/dev-options?hl=zh-cn#debugging)。

2. 遇到错误

![Error Msg](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221701767.png)

[解决 Compose Layout Inspector 不能用 - Keeplooking](https://keeplooking.top/2023/08/12/Android/compose_inspector/)

按照 blog 中的步骤解决后，就可以正常使用了。

1. 打开Help->Edit Custom VM Options 添加参数-Dappinspection.use.dev.jar=true
2. 找到 grade androidx.compose.ui 的目录：

![compose ui lib](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221702016.png)

3. 打开目录：

![open finder](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221702502.png)

然后，退到当前目录的上一级目录，可以发现 一个 inspector.jar 的文件

![inspector.jar](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221702108.png)

4. 将inspector.jar复制到AS的安装目录下的，例如macos下的，Applications/Android Studio.app/Contents/plugins/android/resources目录，并重命名为compose-ui-inspection.jar
5. 重启一下Android Studio，就可以正常使用了。

![Component Tree](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202412221702815.png)
