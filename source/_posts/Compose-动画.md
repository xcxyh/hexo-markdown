---
title: Compose 动画
date: 2024-11-17 21:25:58
tags: Compose
categories: Android 开发
---

Jetpack Compose 是一个声明式 UI 框架，旨在简化 Android 应用的 UI 开发。它通过可组合函数（Composable functions）来描述 UI，这些函数可以动态响应状态变化。

![Data](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202411161612714.png)

![Events](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202411161612781.png)

Compose 声明式 UI ，数据沿层次结构向下传递，渲染UI；事件沿层次结构向上传递，更新数据状态。

Compose 的动画系统是全新的，不依赖于传统的 View 动画或属性动画。它为可组合函数创建了专门的动画 API，支持更灵活的动画实现。

虽然，Compose 基本脱离了 view 系统，但是 在Android平台上，其底层依然是基于Canvas 的 自定义View，也就是通过一个自定义的 `View（AndroidComposeView）`，去对它的 `onMeasure()`、`onLayout()`、`onDraw()`、`dispatchTouchEvent()` 等等方法进行深度定制，来实现「在同一个 `View` 的内部完成整个 UI 组件树」这样的效果。也就是在 Compose 代码里面，你写的一个包含了多层复杂组件的完整界面，它实际上有可能全都被绘制在了同一个 `View` 上，并且触摸事件也都是由同一个 `View` 来进行实际承载和识别的。

所以，理论上，通过 view 能实现的效果，都可以通过Compose 来实现，而且 Compose 有一套全新的 动画 API，支持实现 更复杂更丰富的动画效果，实际上，对于实现一个复杂的动画效果，通过Compose来实现的难度是要低于通过 View系统来实现的难度的。

并且，Compose 通过重组（Recomposition）机制优化性能，只重新绘制发生变化的部分，这在处理动画时表现尤为出色。原生 View 在处理静态内容时性能优秀，但在动态更新频繁的场景中可能会出现性能瓶颈，因为每次状态变化都可能导致整个视图树的重绘。

#### 与 View 系统的对比

| **特性**     | **Jetpack Compose 动画**                 | **原生 View 动画**                                           |
| ------------ | ---------------------------------------- | ------------------------------------------------------------ |
| **架构**     | 声明式 UI，使用可组合函数来定义动画      | 命令式编程，通过直接操作 View 对象来实现动画                 |
| **动画 API** | 提供多种高级和低级 API，支持自定义动画   | 使用 **`ObjectAnimator`**、**`ViewPropertyAnimator`** 等传统 API |
| **学习曲线** | 需要适应新的声明式编程模型，学习成本较高 | 对于已有 Android 开发经验的开发者较为熟悉，学习成本低        |
| **性能优化** | 通过重组机制优化性能，只更新变化部分     | 在复杂布局中可能导致性能瓶颈，需要手动管理状态               |
| **动画效果** | 支持基于物理特性的动画（如弹簧效果）     | 需要分别处理基于时长和物理特性的动画，使用不同 API           |
| **灵活性**   | 高度灵活，可通过状态管理轻松控制动画     | 灵活性较低，需手动管理状态和视图的生命周期                   |
| **适应性**   | 自动适应不同屏幕密度和分辨率             | 需手动调整以适应不同设备的屏幕特性                           |
| **社区支持** | 新兴技术，社区支持逐渐增加               | 成熟稳定，有大量文档和社区资源                               |

Compose 提供了多种动画 API，包括高级和低级 API。高级 API如 **`AnimatedVisibility`** 和 **`AnimatedContent`** 简化了复杂的动画实现，而低级 API 如 **`Animatable`** 和 **`TargetBasedAnimation`** 则允许开发者进行更精细的控制。

#### 低级别动画API：

![Animatable API](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202411161612985.png)

`Animatable`：基于协程的单值动画，通过 `animateTo` 更改值时为值添加动画效果

[`Animation`](https://developer.android.com/reference/kotlin/androidx/compose/animation/core/Animation?hl=zh-cn) 是可用的最低级别的 Animation API。到目前为止，我们看到的许多动画都是基于 Animation 构建的。`Animation` 子类型有两种：[`TargetBasedAnimation`](https://developer.android.com/reference/kotlin/androidx/compose/animation/core/TargetBasedAnimation?hl=zh-cn) 和 [`DecayAnimation`](https://developer.android.com/reference/kotlin/androidx/compose/animation/core/DecayAnimation?hl=zh-cn)。

`Animatable` 的许多功能（包括 `animateTo`）以挂起函数的形式提供。这意味着，它们需要封装在适当的协程作用域内。例如，可以使用 `LaunchedEffect` 可组合项针对指定键值的时长创建一个作用域。

```kotlin
// Start out gray and animate to green/red based on `ok`
val color = remember { Animatable(Color.Gray) }
LaunchedEffect(ok) {
    color.animateTo(if (ok) Color.Green else Color.Red)
}
Box(
    Modifier
        .fillMaxSize()
        .background(color.value)
)
```

`animate*AsState` 函数是最简单的 API，可将即时值变化呈现为动画值。它由 `Animatable` 提供支持，后者是一种基于协程的 API，用于为单个值添加动画效果。`updateTransition` 可创建过渡对象，用于管理多个动画值，并且根据状态变化运行这些值。`rememberInfiniteTransition` 与其类似，不过，它会创建一个无限过渡对象，以管理多个无限期运行的动画。

[`animate*AsState`](https://developer.android.com/reference/kotlin/androidx/compose/animation/core/package-summary?hl=zh-cn#animateDpAsState(androidx.compose.ui.unit.Dp,androidx.compose.animation.core.AnimationSpec,kotlin.String,kotlin.Function1)) 函数是 Compose 中最简单的动画 API，用于为单个值添加动画效果。只需提供目标值（或结束值），该 API 就会从当前值开始向指定值播放动画。

```kotlin
var enabled by remember { mutableStateOf(true) }

val alpha: Float by animateFloatAsState(if (enabled) 1f else 0.5f, label = "alpha")
Box(
    Modifier
        .fillMaxSize()
        .graphicsLayer(alpha = alpha)
        .background(Color.Red)
)
```

使用 Transition 同时为多个属性添加动画效果，Transition 可管理一个或多个动画作为其子项，并在多种状态之间同时运行这些动画。这里的状态可以是任何数据类型。而且可以传递 `transitionSpec` 参数，为过渡状态变化的每个组合指定不同的 `AnimationSpec`。

```kotlin
enum class BoxState {
    Collapsed,
    Expanded
}

val color by transition.animateColor(
    transitionSpec = {
        when {
            BoxState.Expanded isTransitioningTo BoxState.Collapsed ->
                spring(stiffness = 50f)

            else ->
                tween(durationMillis = 500)
        }
    }, label = "color"
) { state ->
    when (state) {
        BoxState.Collapsed -> MaterialTheme.colorScheme.primary
        BoxState.Expanded -> MaterialTheme.colorScheme.background
    }
}
```

**`rememberInfiniteTransition`** 创建无限重复的动画，动画一进入组合阶段就开始运行，除非被移除，否则不会停止。可以使用 `rememberInfiniteTransition` 创建 `InfiniteTransition` 的实例。可以使用 `animateColor`、`animatedFloat` 或 `animatedValue` 添加子动画。

```kotlin
val infiniteTransition = rememberInfiniteTransition(label = "infinite")
val color by infiniteTransition.animateColor(
    initialValue = Color.Red,
    targetValue = Color.Green,
    animationSpec = infiniteRepeatable(
        animation = tween(1000, easing = LinearEasing),
        repeatMode = RepeatMode.Reverse
    ),
    label = "color"
)

Box(
    Modifier
        .fillMaxSize()
        .background(color)
)
```

#### 高级 API：

`AnimatedVisibility` ：用于控制组件的显示与隐藏，能够在组件进入或退出时添加动画效果。可以通过 **`enter`** 和 **`exit`** 参数来自定义进入和退出动画。 一旦退出动画完成，内容会被从组合树中移除，从而释放资源。

```kotlin
@Composable
fun AnimatedVisibilityExample() {
    var visible by remember { mutableStateOf(true) }

    Column(modifier = Modifier.padding(16.dp)) {
        Button(onClick = { visible = !visible }) {
            Text("Toggle Visibility")
        }

        AnimatedVisibility(
            visible = visible, 
            enter = slideInVertically(initialOffsetY = { -40 }) + fadeIn(),
            exit = slideOutVertically(targetOffsetY = { 40 }) + fadeOut()
    ) {
            Text(
                text = "This text will appear and disappear with animation!",
                modifier = Modifier.padding(top = 16.dp)
            )
        }
    }
}
```

`animateContentSize`：当组件的大小发生变化时，自动调整其内容的大小并添加平滑过渡效果，适用于动态内容变化的场景。主要用于在其子组件的大小发生变化时自动执行平滑的动画过渡。可以通过传入**`transitionSpec`** 参数自定义进入和退出动画效果。

```kotlin
@Composable
fun AnimateContentSizeExample() {
    var expanded by remember { mutableStateOf(false) }
    val shortText = "Hello"
    val longText = "Hello, this is a longer text that spans multiple lines."

    Box(
        modifier = Modifier
            .background(Color.Blue, RoundedCornerShape(8.dp))
            .clickable { expanded = !expanded }
            .padding(16.dp)
            .animateContentSize() // 应用 animateContentSize 修饰符
    ) {
        Text(
            text = if (expanded) longText else shortText,
            color = Color.White
        )
    }
}
```

`AnimatedContent` ：用于在状态变化时平滑地切换内容，适合需要根据状态动态更新UI的场合。例如，当一个text 内容需要动态变化时，添加动画效果。同样可以通过 **`transitionSpec`** 参数自定义进入和退出动画效果，包括大小变化、透明度变化等。

```kotlin
@Composable
fun <S> AnimatedContent(
    targetState: S,
    modifier: Modifier = Modifier,
    transitionSpec: AnimatedContentTransitionScope<S>.() -> ContentTransform = { /* 默认动画 */ },
    contentAlignment: Alignment = Alignment.TopStart,
    label: String = "AnimatedContent",
    contentKey: (targetState: S) -> Any? = { it },
    content: @Composable AnimatedContentScope.(targetState: S) -> Unit
)

@Composable
fun AnimatedContentExample() {
    var count by remember { mutableStateOf(0) }

    AnimatedContent(targetState = count, transitionSpec = {
        slideInHorizontally { width -> width } + fadeIn() with
        slideOutHorizontally { width -> -width } + fadeOut()
    }) { targetCount ->
        Text(text = "Count: $targetCount")
    }

    Row {
        Button(onClick = { count++ }) {
            Text("Increase")
        }
        Button(onClick = { count-- }) {
            Text("Decrease")
        }
    }
}
```

[`SharedTransitionLayout`](https://developer.android.com/reference/kotlin/androidx/compose/animation/package-summary?hl=zh-cn#SharedTransitionLayout(androidx.compose.ui.Modifier,kotlin.Function1))：共享元素动画`sharedElement()` 和`sharedBounds()`，共享元素转换可在内容保持一致的可组合项之间无缝转换。通常用于在不同屏幕之间共享元素，实现视觉上的连续性。`sharedElement()` 用于相同元素之间的过渡，而`sharedBounds()` 通常用于 不同元素之间的过渡动画。

| **特性**     | **sharedElement()**                     | **sharedBounds()**                          |
| ------------ | --------------------------------------- | ------------------------------------------- |
| 适用场景     | 内容完全相同的元素                      | 视觉上不同但共享区域的元素                  |
| 动画表现     | 在转换时仅显示目标内容                  | 在转换期间显示初始内容和目标内容            |
| 过渡效果控制 | 通过 **`animatedVisibilityScope`** 控制 | 额外支持 **`enter`** 和 **`exit`** 动画参数 |

![Compose BOM](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202411161612315.png)

<aside>
👉 共享元素支持从 Compose 1.7.0 （BOM  2024.09.00 及以上版本）开始提供，目前处于实验阶段，这些 API 未来可能会发生变化。
</aside>

#### 自定义动画效果：

`AnimationSpec` 是 Jetpack Compose 中用于定义动画行为的参数，允许开发者自定义动画的时间、缓动效果和其他特性。

 `tween`  `spring`  **和 `keyframes`** 

- **Tween Animation**：基于时间的线性或缓动动画。
- **Spring Animation**：基于物理特性创建弹簧效果。
- **Keyframe Animation**：允许在特定时间点设置关键帧值。

 **Tween Animation (`tween`)**

Tween Animation（插值动画）用于在指定时间内平滑地从一个值过渡到另一个值。`tween` 是“between”（介于）的缩写，因为它介于两个值之间。

- **`durationMillis`**: 动画持续时间（毫秒）。
- **`delayMillis`**: 动画开始前的延迟（毫秒）。
- **`easing`**: 用于定义动画速度变化的缓动函数。

```kotlin
@Immutable
class TweenSpec<T>(
    val durationMillis: Int = DefaultDurationMillis,
    val delay: Int = 0,
    val easing: Easing = FastOutSlowInEasing
) : DurationBasedAnimationSpec<T>

@Immutable
class CubicBezierEasing(
    private val a: Float,
    private val b: Float,
    private val c: Float,
    private val d: Float
) : Easing
```

**Easing**是描述动画在开始和结束之间如何变化的函数。它使得动画不仅仅是线性移动，而是可以加速、减速或产生弹跳等效果。
也可以通过 CubicBezierEasing 自定义 用于动画速度变化的 巴塞尔曲线参数。

Jetpack Compose提供了多种内置的Easing函数，适用于不同的动画需求：

- **LinearEasing**: 匀速运动，整个动画过程中速度保持不变。
- **FastOutSlowInEasing**: 动画开始时快速，然后逐渐减速，适合需要自然感的过渡。
- **LinearOutSlowInEasing**: 动画开始时匀速，随后减速。
- **CubicBezierEasing**: 自定义贝塞尔曲线，可以通过四个参数定义控制点，实现更复杂的运动效果。

**Spring Animation (`spring`)**

基于物理模型的动画，在起始值和结束值之间创建基于物理特性的动画，模拟弹簧的行为。

- **`dampingRatio（阻尼比）`**: 控制弹簧的反弹程度，值越高，反弹越少。
- **`stiffness（刚度）`**: 控制弹簧移动到目标 值的速度，值越高，移动越快。

**阻尼比：**

决定了弹簧动画的振荡或弹跳程度。它是一个无量纲值，影响弹簧对位移的响应：

- **0（无阻尼）**：弹簧无限期振荡而不停止。
- **1（临界阻尼）**：弹簧尽快返回到静止位置，不会振荡。
- **大于 1（过阻尼）**：弹簧缓慢返回到静止位置，不会振荡。
- **小于 1（欠阻尼）**：弹簧会振荡，产生弹跳效果。

Jetpack Compose 中常用的阻尼比预定义值包括：

- **`Spring.DampingRatioNoBouncy`**
- **`Spring.DampingRatioLowBouncy`**
- **`Spring.DampingRatioMediumBouncy`**
- **`Spring.DampingRatioHighBouncy`**

**刚度：**

参数控制弹簧朝目标值移动的速度。它的单位通常是力每单位长度（例如，像素每秒平方）。更高的刚度值意味着更快地返回到目标位置。刚度值也可以使用预定义常量设置：

- **`Spring.StiffnessLow`**
- **`Spring.StiffnessMedium`**
- **`Spring.StiffnessHigh`**

**从质量、刚度和阻尼值转换：**

在物理学中，弹簧的行为也可以通过质量Mass、刚度stiffness和阻尼值damping来描述。

**阻尼比计算**：

![阻尼比计算公式](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202411161613491.png)

这个公式允许将其他上下文中使用的阻尼值（例如 Figma 中的值）转换为 Android 弹簧动画中使用的阻尼比。

更高的刚度值会导致动画更快，而更高的阻尼值则会减少弹跳效果。

```kotlin
@Immutable
class SpringSpec<T>(
    val dampingRatio: Float = Spring.DampingRatioNoBouncy,
    val stiffness: Float = Spring.StiffnessMedium,
    val visibilityThreshold: T? = null
) : FiniteAnimationSpec<T>
```

相比基于时长的 `AnimationSpec` 类型`tween`，`spring` 可以更流畅地处理中断，因为它可以在目标值在动画中变化时保证速度的连续性。`spring` 用作很多动画 API（如 `animate*AsState` 和 `updateTransition`）的默认 AnimationSpec。

 **Keyframes Animation (`keyframes`)**

`keyframes` 会根据在动画时长内的不同时间戳中指定的快照值添加动画效果。在任何给定时间，动画值都将插值到两个关键帧值之间。对于其中每个关键帧，都可以指定 Easing 来确定插值曲线。
关键帧动画是通过 **`keyframes`** 函数定义的，该函数返回一个 **`KeyframesSpec`**。

要定义关键帧，可以利用 KeyframesSpecConfig类，该类允许指定：

- **持续时间**：动画的总时间。
- **关键帧值**：在指定时间戳处的特定值。
- **缓动函数**：可以为每个动画段应用自定义缓动，以实现不同的速度和加速度。

```kotlin
val value by animateFloatAsState(
    targetValue = 1f,
    animationSpec = keyframes {
        durationMillis = 375
        0.0f at 0 using LinearOutSlowInEasing // 开始
        0.2f at 15 using FastOutLinearInEasing // 第一个关键帧
        0.4f at 75 // 第二个关键帧
        0.4f at 225 // 第三个关键帧
    },
    label = "keyframe"
)
```

当以下情况出现时，关键帧特别有用：

- 创建需要特定时机和过渡的 **复杂动画**。
- 实现 **编排动画**，多个元素需要相互关联地移动。
- 设计根据用户输入或其他事件动态响应的交互元素。

Jetpack Compose的动画系统为Android开发者提供了强大而灵活的工具，使创建复杂、流畅的用户界面变得更加简单。通过深入理解和巧妙运用这些动画技术，开发者可以大大提升应用的用户体验，使界面交互更加生动有趣。随着Compose的不断发展，我们可以期待看到更多创新的动画应用，为Android应用带来更加丰富和吸引人的视觉效果。


[Compose 中的动画  |  Jetpack Compose  |  Android Developers](https://developer.android.com/develop/ui/compose/animation/introduction?hl=zh-cn)