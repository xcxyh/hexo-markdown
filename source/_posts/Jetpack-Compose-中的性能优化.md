---
title: Jetpack Compose 中的性能优化
date: 2024-08-04 21:03:03
tags: Android Compose
categories: Android 开发
---

## Jetpack Compose 中的性能优化

![Compose Opt](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202408042102248.png)

在创建一个 Composable 功能时，开发人员不必考虑 Compose 在后台是如何工作的，这很好。然而，这样做有一个缺点——声明性降低了透明度和对正在发生的事情的理解，有些事情开始看起来像“魔法”。

Jetpack Compose 中的界面是使用 Composable 函数图构建的。 每次**函数参数的值发生变化时，都会发生重组**，即重新执行函数。在大多数情况下，这应该不是问题，因为可组合函数的速度足够快（只要它们不涉及任何额外的工作）。但在某些情况下，重组可能会发生得太频繁，应用程序开始“变慢”。性能问题并不总是肉眼可见的，尤其是在屏幕不复杂的情况下。但是，问题不可见，并不意味着它不存在。在任何情况下，都会发生不必要的计算并消耗电池电量。

Jetpack Compose 中的重组是由于 Composable 函数用于渲染的状态更改而更新 UI 的过程。在重构过程中，Compose 可以了解每个可组合项正在使用的数据，并且仅更新 UI 中已更改的部分。其他元素将被跳过。

当 Composable 将可变数据类型（如 MutableList）作为参数时，情况变得更加复杂。Jetpack Compose 编译器将不可变类标记为**稳定**类。如果函数中至少有一个参数的类型不稳定，那么参数的值将不会进行比较是否相等，并且每次调用函数时都会发生重组。

**将新字段添加到经常调用的 Composable 函数的状态类时要小心。一个这样的字段可以使整个类不稳定。**

稳定的数据类型用于减少重组次数，从而提高性能。

Jetpack Compose 编译器会专门将数据类型标记为稳定：

1. 类实例的字段值在创建实例后不会更改
2. 类中所有字段的类型都是稳定的

```kotlin
class Person（val name： String， val age： Int） // 稳定类型，因为所有的类字段都是不可变的
class NamesList（val items： List<String>） // 因为 List 不稳定的类型，接口也是一种不稳定的类型，可以使用 ImmutableList 代替
class Counter（var value： Int） // 不稳定类型，因为值字段是可变的
```

可以使用 *@Stable* 或 *@Immutable* 注释（它们是等效的）将类标记为稳定类。在这种情况下，您自己保证该类满足所有要求，即使编译器不这么认为。

有一些重要的常见类型，即使它们未使用 @Stable 注释明确标记为稳定，Compose 编译器也会将其视为稳定类型：

- 所有基元值类型：Boolean、Int、Long、Float、Char 等。
- 字符串
- 所有函数引用

**如果 Composable 函数的所有参数都是稳定的，那么将使用 equals 方法比较它们，如果它们都等于上一次调用的参数，则不会重新执行函数体**。

### 不稳定的List

 List 类型是一个接口，编译器无法知道此列表是否正在被修改，并且如果编译器没有 100% 的置信度，那么该类将**不会**被标记为稳定。可以使用 kotlinx-collections-immutable 库，它允许指定可组合方法将不可变列表作为参数。

```kotlin
// kotlinx-collections-immutable 库
// https://github.com/Kotlin/kotlinx.collections.immutable
@Composable
fun StableGrid(
    values: ImmutableList<GridItem>
) {
    ...
}
```

### 不稳定的 lambda

每当编写 lambda 时，编译器都会使用该代码创建一个匿名类。如果 lambda 需要访问外部变量，编译器会将这些变量添加为传递给 lambda 构造函数的字段。这有时被描述为*变量捕获*。对于 lambda，编译器会生成一个类。如下所示：onNameClick

```kotlin
@Composable
fun RecompositionTest() {
   val viewModel = remember { NamesViewModel() }
   val state by viewModel.state.collectAsState()

   NameColumnWithButton(
       names = state.names,
       onButtonClick = { viewModel.addName() },
       onNameClick = { viewModel.handleNameClick() },
   )
}

class NameClickLambda(val viewModel: NamesViewModel) {
   operator fun invoke() {
       viewModel.handleNameClick()
   }
}
```

所以，每次编写一个lambda都会创建一个匿名类，所以传递 lambda 给 Compose 函数时，lambda  是 不稳定的类型。

如何让 lambda 稳定？

1. **使用方法引用**

通过使用方法引用而不是 lambda，方法引用是函数类型，在重组之间将保持等效。

```kotlin
@Composable
fun RecompositionTest() {
   val viewModel = remember { NamesViewModel() }
   val state by viewModel.state.collectAsState()

   NameColumnWithButton(
       names = state.names,
       onButtonClick = viewModel::addName, // Method reference
       onNameClick = viewModel::handleNameClick, // Method reference
   )
}
```

2. **使用 remember**

另一种选择是记住重组之间的 lambda 实例。这将确保完全相同的 lambda 实例将在进一步的组合中被重用。

```kotlin
@Composable
fun RecompositionTest() {
   val viewModel = remember { NamesViewModel() }
   val state by viewModel.state.collectAsState()
   val onButtonClick = remember(viewModel) { { viewModel.addName() } }
   val onNameClick = remember(viewModel) { { viewModel.handleNameClick() } }

   NameColumnWithButton(
       names = state.names,
       onButtonClick = onButtonClick,
       onNameClick = onNameClick
   )
}
```

3. 如果 lambda 只是调用 **top-level 函数**，则应用于所有 lambda 的基本组合优化规则仍然适用。例如，如下所示的调用不需要更改：

```kotlin
@Composable
funRecompositionTest() {
val viewModel =remember {NamesViewModel() }
val stateby viewModel.state.collectAsState()

NameColumnWithButton(
       names = state.names,
       onButtonClick = viewModel::addName,
       onNameClick = {someNonScopedFunction() }
   )
}

funsomeNonScopedFunction() {
print("Do something")
}
```

4. 如果 lambda  捕获参数是稳定的，则它就不会违反任何跳过优化要求。例如，以下lambda 的所有参数都是稳定的，所以编译器就不会在图形重构时更新整个lambda。

```kotlin
@Composable
fun RecompositionTest() {
    var state by remember { mutableStateOf(listOf("Aaron", "Bob", "Claire")) }
    
    NameColumnWithButton(
        strings = state,
        buttonName = "Recompose Lambda Capturing @Stable",
        onButtonClick = { state = state + "Daisy" },
        onTextClick = { state = state + "Daisy" },
    )
}
```

几条原则：

1. 在传递给 Composable 的类上正确实现Equals 方法。
2. 使用state 包装 发生改变的值。Jetpack Compose 订阅 State/MutableState 更改。如果它们的值发生变化，则仅重新组合使用这些值的图形部分。

```kotlin
data class StopwatchState(
   val exercise: ExerciseState?,
   val min: MutableState<String> = mutableStateOf(“00”),
   val sec: MutableState<String> = mutableStateOf(“00”),
   val millis: MutableState<String> = mutableStateOf(“00”),
   val isRunning: MutableState<Boolean> = mutableStateOf(false)
)
```

3. 仅在函数的 Composable 参数中传递函数真正需要的内容。只传递当前Compose组件需要的状态。
4. 尽可能在 Composable 函数的参数中使用稳定类型。
5. 如果您确定 Composable 函数的参数是不可变的，请使用 Immutable 注解标记该类。

```kotlin
interface Content // 接口 是不稳定的，使用 Immutable 注解标记后，Composable 会认为它是稳定的，不要在具有 var 字段或包含列表的字段的类上“打”此注解。
@Immutable
data class ItemData(
 val content: Content
)
```

6. 在可组合的方法中始终使用 remember。由于多种原因，重组可能随时发生。如果你的值应该在重组后继续存在，记住会帮助你保持这种状态。
7. 传递给 compose 函数 lambda 参数时，使用方法引用。
8. 使用派生状态， 变量*派生*自其他一些快速变化的状态。对于一些快速变化的状态，使用 **derivedStateOf** 可以派生出需要的状态，防止不必要的重组。

```kotlin
   val showButton by remember { 
        derivedStateOf { 
            listState.firstVisibleItemIndex > 0 
        } 
   }
```

9. 仅在必要时使用惰性布局。将 LazyRow 用于包含五个项目的列表可能会显著减慢呈现速度。
10. 如果可能，请避免使用 ConstraintLayout。请改用 Column 和 Row。ConstraintLayout 是一个线性方程组，它需要更多的计算，而不是一个接一个地生成元素。


**参考：**

[要么优化，要么死亡。Jetpack Compose 中的分析和优化 |通过 IceRock Development |IceRock 开发 |中等 (medium.com)](https://medium.com/icerock/optimize-or-die-profiling-and-optimization-in-jetpack-compose-a165c8897b3f)

[Jetpack Compose 在引擎盖下：重组和稳定类型 |由 Denis Golubev |中等 (medium.com)](https://medium.com/@denisgolubev1999/jetpack-compose-%D0%BF%D0%BE%D0%B4-%D0%BA%D0%B0%D0%BF%D0%BE%D1%82%D0%BE%D0%BC-%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%BF%D0%BE%D0%B7%D0%B8%D1%86%D0%B8%D1%8F-%D0%B8-%D1%81%D1%82%D0%B0%D0%B1%D0%B8%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D1%82%D0%B8%D0%BF%D1%8B-9598f8b62006)

[Android: оптимизация UI на Jetpack Compose | Medium](https://medium.com/@denisgolubev1999/%D0%BE%D0%BF%D1%82%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F-ui-%D0%BD%D0%B0-jetpack-compose-f440c5659ab3)

[Jetpack Compose 重组中的陷阱 |Stitch Fix 技术 – 多线程](https://multithreaded.stitchfix.com/blog/2022/08/05/jetpack-compose-recomposition/)