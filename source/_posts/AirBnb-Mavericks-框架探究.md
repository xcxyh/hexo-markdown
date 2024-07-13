---
title: AirBnb Mavericks 框架探究
date: 2024-07-13 19:05:28
tags: Mavericks
categories: Android 开发
---

Mavericks 是 Airbnb 的 Android MVI 框架，是一种响应式的 UI 框架。

Mavericks 建立在以下现有技术和概念之上：

- Kotlin 语言
- Android Architecture Components（Lifecycle、ViewModel 等）
- Kotlin Flow
- React (概念)

Mavericks 吸收了来自 React 的响应式思想，同时 Mavericks 依赖了 Kotlin、AAC（Android Architecture Components）、Flow 等技术，实现了一个 Android 原生的响应式 UI 框架。

指路->：[https://github.com/airbnb/mavericks](https://github.com/airbnb/mavericks)

This is what it looks like:

```kotlin
data class HelloWorldState(val title: String = "Hello World") : MavericksState

/**
 * Refer to the wiki for how to set up your base ViewModel.
 */
class HelloWorldViewModel(initialState: HelloWorldState) : MavericksViewModel<HelloWorldState>(initialState) {
    fun getMoreExcited() = setState { copy(title = "$title!") }
}

class HelloWorldFragment : Fragment(R.layout.hello_world_fragment), MavericksView {
    private val viewModel: HelloWorldViewModel by fragmentViewModel()

    override fun invalidate() = withState(viewModel) { state ->
        // Update your views with the latest state here.
        // This will get called any time your state changes and the viewLifecycleOwner is STARTED.
    }
}
```

依赖：

```kotlin
dependencies {
  implementation 'com.airbnb.android:mavericks:x.y.z'
}
```

官方文档网站：[Mavericks Docs (airbnb.io)](https://airbnb.io/mavericks/#/)

Mavericks 建立在  [Android Jetpack](https://developer.android.com/jetpack)  和  [Kotlin 协程](https://developer.android.com/kotlin/coroutines)之上，因此可以将其视为对 Google 标准库集的补充，而不是背离。

Mavericks 的 1.0 版本 MVRX 是建立在 Rxjava 的基础之上，但是，在如今大部分 APP 都切换到 kotlin 协程之后，很多 App 都不再有 RxJava 的依赖了，因此，AirBnb 使用 Kotlin Flow 重写了该框架，也就是 Mavericks 2.0。

为什么我们需要它？

1. 减少 50%到 75%代码，更简洁高效的开发
2. 真正的响应式，数据与 UI 解耦，更清晰的代码
3. 与 Kotlin、AAC 的结合与包容，更符合技术趋势
4. React 思想在安卓的最佳实践

单向数据流、响应式 UI 架构模式：

MVI（Model-View-Intent） 和 React 是两种常用的 UI 架构模式，分别用于 Android 和前端开发。MVI 和 React 都是现代 UI 架构模式，强调单向数据流和不可变状态。尽管它们应用于不同的平台，但它们在设计理念上有许多相似之处，特别是在单向数据流的概念上。

### MVI（Model-View-Intent）

MVI 是一种用于 Android 应用的架构模式，它强调单向数据流和不可变状态。MVI 由三个主要部分组成：

1. **Model**: 表示应用的状态。Model 通常是不可变的，这意味着每次状态变化都会创建一个新的 Model 实例。
2. **View**: 负责呈现 UI 并接收用户输入。View 将用户输入转换为 Intent。
3. **Intent**: 表示用户的意图或动作。Intent 被发送到 Model，Model 根据 Intent 更新状态。

![单向数据流](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407131912670.png)

#### 数据流

1. **用户交互**: 用户与 View 交互，触发一个 Intent。
2. **Intent 处理**: Intent 被发送到 Model，Model 处理 Intent 并更新状态。
3. **状态更新**: 更新后的状态通过单向数据流传递回 View，更新 UI。

```kotlin
data class ViewState(val count: Int)

sealed class ViewIntent {
    object Increment : ViewIntent()
    object Decrement : ViewIntent()
}

class MainViewModel : ViewModel() {
    private val _viewState = MutableStateFlow(ViewState(0))
    val viewState: StateFlow<ViewState> = _viewState

    fun processIntent(intent: ViewIntent) {
        when (intent) {
            is ViewIntent.Increment -> _viewState.value = _viewState.value.copy(count = _viewState.value.count + 1)
            is ViewIntent.Decrement -> _viewState.value = _viewState.value.copy(count = _viewState.value.count - 1)
        }
    }
}

@Composable
fun MainScreen(viewModel: MainViewModel) {
    val viewState by viewModel.viewState.collectAsState()
    Column {
        Text("Count: ${viewState.count}")
        Button(onClick = { viewModel.processIntent(ViewIntent.Increment) }) {
            Text("Increment")
        }
        Button(onClick = { viewModel.processIntent(ViewIntent.Decrement) }) {
            Text("Decrement")
        }
    }
}

```

### React + Redux

React 是一个用于构建用户界面的 JavaScript 库。React 也强调单向数据流和不可变状态。React 的核心概念包括：

1. **Component**: React 应用由组件组成。每个组件描述了 UI 的一部分。
2. **State**: 组件可以拥有状态。状态变化会触发组件重新渲染。
3. **Props**: 组件可以接收外部传入的数据，这些数据称为 Props。

Redux 是一个用于 JavaScript 应用的状态管理库，通常与 React 一起使用，但也可以与其他 JavaScript 框架或库一起使用。Redux 提供了一种可预测的方式来管理应用的状态，使得状态变化更加透明和可调试。

Redux 的设计基于几个核心概念：

1. **单一数据源（Single Source of Truth）**:
   - 应用的整个状态被存储在一个对象树中，这个对象树只存在于一个单一的 store 中。
2. **状态是只读的（State is Read-Only）**:
   - 唯一改变状态的方法是触发一个 action。这样可以确保状态的变化是可预测的和可追踪的。
3. **使用纯函数来执行修改（Changes are Made with Pure Functions）**:
   - 为了描述状态树如何通过 actions 转变成下一个状态，你需要编写纯函数（reducers）。

![Redux](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407131912371.png)

#### 数据流

1. **用户交互**: 用户与组件交互，触发状态变化。
2. **状态更新**: 状态变化会触发组件重新渲染。
3. **单向数据流**: 数据从父组件流向子组件，子组件接收事件更改状态，状态改变触发 UI 更新。

```jsx
import React from "react";
import ReactDOM from "react-dom";
import { Provider, useDispatch, useSelector } from "react-redux";
import { createStore } from "redux";

// Reducer
function counter(state = 0, action) {
  switch (action.type) {
    case "INCREMENT":
      return state + 1;
    case "DECREMENT":
      return state - 1;
    default:
      return state;
  }
}

// 创建 Store
const store = createStore(counter);

// React 组件
function Counter() {
  const count = useSelector((state) => state);
  const dispatch = useDispatch();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => dispatch({ type: "INCREMENT" })}>Increment</button>
      <button onClick={() => dispatch({ type: "DECREMENT" })}>Decrement</button>
    </div>
  );
}

// 渲染应用
ReactDOM.render(
  <Provider store={store}>
    <Counter />
  </Provider>,
  document.getElementById("root")
);
```

MVI 和 React + Redux 两者具有相同的响应式思想和架构模式：

1. **不可变状态**:
   - **MVI**: 状态是不可变的，每次状态变化都会创建一个新的状态对象。
   - **React + Redux**: Redux 强调使用不可变状态，每次状态变化都会创建一个新的状态对象。
2. **单向数据流**:
   - **MVI**: 数据流是单向的，从 Intent 到 Model，再从 Model 到 View。
   - **React + Redux**: 数据流也是单向的，从 Action 到 Reducer，再从 Store 到 View。
3. **纯函数**:
   - **MVI**: Model 更新是通过纯函数处理的，即 Reducer。
   - **React + Redux**: Redux 中的 Reducer 是纯函数，负责根据 Action 更新状态。

### Airbnb Mavericks 框架

而对于 Airbnb 的 Mavericks 来说，也是借鉴和继承了相同的响应式思想，下面我们可以来对比一下：

**状态不可变：**

MavericksState 的状态使用 `data class` 定义，是不可变的，要修改状态，必须用`data class` 的`clone`方法。每次状态变化，都需要重新创建一个新的对象。

```jsx
data class UserState(
    val score: Int = 0,
    val previousHighScore: Int = 150,
    val livesLeft: Int = 99,
) : MavericksState
```

**单向数据流：**

通过 kotlin flow 实现 数据 （state）的单向流动。

状态更新：Mavericks 通过 setState 方法，异步更新 state，由于 state 为 `data class` ，更新状态时直接使用 copy 方法获取新对象。

```jsx
protected fun setState(reducer: S.() -> S) {

}
// example:
setState { copy(yourProp = newValue) }

//状态发送：
private suspend fun flushQueuesOnce() {
        select<Unit> {
            setStateChannel.onReceive { reducer ->
                val newState = state.reducer()
                if (newState != state) {
                    state = newState
                    stateSharedFlow.emit(newState) // 发送状态
                }
            }
            withStateChannel.onReceive { block ->
                block(state)
            }
        }
    }
```

状态监听：最新的状态 通过 **stateSharedFlow** 发送，通过 onEach 监听 收集 flow 中的最新状态。

```jsx
// Invoked whenever propA changes only.
onEach(YourState::propA) { a ->
}
// Invoked whenever propA, propB, or propC changes only.
onEach(YourState::propA, YourState::propB, YourState::propC) { a, b, c ->
}
```

**纯函数：**

Mavericks 中的 setState { } 代码块函数，也就是 reducer: S.() -> S 这部分是纯函数。

纯函数（Pure Function）是函数式编程中的一个重要概念。一个函数要被认为是纯函数，需要满足以下两个条件：

1. **确定性**：对于相同的输入，函数总是返回相同的输出。
2. **无副作用**：函数的执行不会影响外部状态，也不会依赖于外部可变状态。

在 Mavericks，会对 reducer 函数执行两次， 进行纯函数检查：

```jsx
val firstState = this.reducer()
val secondState = this.reducer()

if (firstState != secondState) { }
```

例如，如下写法 reducer 就不是纯函数，对于相同的输入，两次执行结果不一致。

```jsx
setState { copy(time = System.currentTimeMillis()) }
```

### 怎么使用？

添加依赖：

```jsx
dependencies {
  implementation 'com.airbnb.android:mavericks:x.y.z'
}
```

初始化（在 Application onCreate 时初始化）：

```kotlin
class SampleApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        **Mavericks.initialize(this)**
    }
}
```

示例：

```jsx
data class HelloWorldState(val title: String = "Hello World") : MavericksState

/**
 * Refer to the wiki for how to set up your base ViewModel.
 */
class HelloWorldViewModel(initialState: HelloWorldState) : MavericksViewModel<HelloWorldState>(initialState) {
    fun getMoreExcited() = setState { copy(title = "$title!") }
}

class HelloWorldFragment : Fragment(R.layout.hello_world_fragment), MavericksView {
    private val viewModel: HelloWorldViewModel by fragmentViewModel()

    override fun invalidate() = withState(viewModel) { state ->
        // Update your views with the latest state here.
        // This will get called any time your state changes and the viewLifecycleOwner is STARTED.
    }

    fun initView() {
		    viewModel.onEach(HelloWorldState::title) { title ->
				    // Update views
				    text_view.text = title
		    }
    }
}
```

数据流的流转过程如下：

1. 通过 ViewModel 更新 State
2. ViewModel 接收数据
3. 通过 setState 更新 state
4. MavericksState 发生变化后回调 invalidate 方法
5. 通过 withState 获取 state，更新 UI
6. 可以通过 onEach 监听 state 中某一个或多个属性的变化。

### Mavericks 结合 Compose

```
💡 Mavericks + Compose == Redux/Mobx + React
```

使用 Compose 构建 UI，Mavericks 可用于业务逻辑、数据获取、对象依赖注入等，有点类似于 Redux 和 React 的关系，Redux 用于数据管理和业务逻辑，React 组件负责构建 UI。

结合 compose 使用需要添加依赖：

```kotlin
implementation 'com.airbnb.android:mavericks-compose:x.y.z'
```

新建状态 和 ViewModel：

```kotlin
data class CounterState(
    val count: Int = 0,
) : MavericksState

class CounterViewModel(initialState: CounterState) : MavericksViewModel<CounterState>(initialState) {
    fun incrementCount() = setState { copy(count = count + 1) }
}

```

只需要在 Composable 函数里调用  `mavericksViewModel()`  来获取 ViewModel 实例。其默认关联的 LifecycleOwner 为 `LocalLifecycleOwner`，意味着该  `LocalLifeyclerOwner`  下的所有 Composable 将获取到相同的 ViewModel 实例。一般为 当前 Fragment 的 LifecycleOwner。如果使用 mavericksActivityViewModel 则 当前 ViewModel 的 LifecycleOwner 为 当前 Fragment 所在的 Activity，对于同一个 Activity，mavericksActivityViewModel 拿到的 都是同一个 ViewModel 实例。

```kotlin
@Composable
    fun IncrementNavigationCountButton() {
        val navScopedViewModel: CounterViewModel = mavericksViewModel()
        Button(onClick = navScopedViewModel::incrementCount) {
            Text("Increment Navigation Scoped Count")
        }
    }
```

要订阅 ViewModel 里的状态变化，Mavericks 提供了  `ViewModel.collectAsState()`。

```kotlin
// This will get or create a ViewModel scoped to the closest LocalLifecycleOwner which, in this case, is the NavHost.
val navScopedViewModel: CounterViewModel = mavericksViewModel()
// This will get or create a ViewModel scoped to the Activity.
val activityScopedViewModel: CounterViewModel = mavericksActivityViewModel()

val navScopedCount by navScopedViewModel.collectAsState(CounterState::count)
val activityScopedCount by activityScopedViewModel.collectAsStateWithLifecycle(CounterState::count)
```

通过 属性委托的方式 ，获取到 State 中的状态和属性。要优化使用  `collectAsState()`，不同 Composable 访问不同的状态属性，在重组时候可以最大限度地减少状态更改时需要完成的工作。因此在 Composable 里订阅状态属性比订阅整个状态更理想。

### 核心源码探究

**怎么检查是否是纯函数？**

```kotlin
stateStore.set {
	val firstState = this.reducer()
	val secondState = this.reducer()

	if (firstState != secondState) { }

	firstState
}
```

在 Mavericks 调试模式中，当调用 setState 时，会对 reducer 函数执行两次， 进行纯函数检查，如果不是 纯函数， 会抛出 IllegalArgumentException（仅调试模式）。

**shared flow 还是 state flow？**

**`SharedFlow`**  在 Mavericks 中被用来处理事件流和状态更新。

```kotlin
private val stateSharedFlow = MutableSharedFlow<S>(
        replay = 1,
        extraBufferCapacity = SubscriberBufferSize,
        onBufferOverflow = BufferOverflow.SUSPEND,
).apply { tryEmit(initialState) }

 @InternalMavericksApi const val SubscriberBufferSize = 63
```

**`replay`**  参数指定了  **`SharedFlow`**  应该缓存多少个最新的值，并且在新的订阅者开始收集时重放这些值。这里设置为 1， 代表有新的订阅者时，会立即发送当前最新值，也就是这里的消息订阅是 “粘性的”。这减少了订阅者错过重要状态更新的风险。

**`extraBufferCapacity`**  参数指定了额外的缓冲区容量。`SubscriberBufferSize`是一个常量值 63，表示额外的缓冲区大小。这个缓冲区用于存储在订阅者还没有准备好处理新值时发送的值。这有助于避免丢失事件。是一个“背压”参数，背压（Backpressure）是指在处理数据流时，消费者无法跟上生产者的速度，从而导致数据积压的问题。当有慢速消费者时，这里会为其缓存状态。

**`BufferOverflow.SUSPEND`**  表示当缓冲区已满时，新的值将会被挂起，直到有空间可用。这确保了不会丢失任何事件，但可能会导致发送方挂起，直到缓冲区有空间。

sharedFlow 和 StateFlow 比较：

StateFlow 就是一个 replaySize=1 的 sharedFlow。同时它必须有一个初始值，此外，每次更新数据都会和旧数据做一次比较，只有不同时候才会更新数值。

StateFlow**重点在状态**，ui 永远有状态，所以 StateFlow 必须有初始值，同时对 ui 而言，过期的状态毫无意义，所以 stateFLow 永远更新最新的数据（和 liveData 相似），所以必须有粘滞度=1 的粘滞事件，让 ui 状态保持到最新。

SharedFlow**侧重在事件**，当某个事件触发，发送到队列之中，按照挂起或者非挂起、缓存策略等将事件发送到接受方，在具体使用时，SharedFlow 更适合通知 ui 界面的一些事件，比如 toast 等，也适合作为 viewModel 和 repository 之间的桥梁用作数据的传输。

结论：

这里 Mavericks 使用 SharedFlow 来 实现一个 StateFlow 用于 State 状态的 保存和更新。

**withstate 和 setstate 怎么保证时序？**

💡 viewModel 中的 withState 和 View 中的 withState 区别：

viewModel 中的 withState 是 异步的 block，通过 这个 withState 拿到的状态可以保证是最新的状态。View 中的 withState 是 同步的 block，直接执行 View 中的 withState 获取到的状态不能保证是最新的 state 状态。

我们应该尽量在 invalidate 或者 onEach、onAsync 环境中调用 View 中的 withState。
因为这三个方法都是在子线程中执行完 state 的变更后回调到主线程的，所以这里调 withState 获取到的肯定是最新的状态。

withState 队列 与 setState 队列

```kotlin
private val setStateChannel = Channel<S.() -> S>(capacity = Channel.UNLIMITED)
private val withStateChannel = Channel<(S) -> Unit>(capacity = Channel.UNLIMITED)

private suspend fun flushQueuesOnce() {
        select<Unit> {
            setStateChannel.onReceive { reducer ->
                val newState = state.reducer()
                if (newState != state) {
                    state = newState
                    stateSharedFlow.emit(newState)
                }
            }
            withStateChannel.onReceive { block ->
                block(state)
            }
        }
    }
```

**`select`**  是一个 Kotlin 协程中的多路复用选择器，它允许在多个挂起函数中选择一个首先完成的函数。它的作用类似于  **`select`**  语句在 Go 语言中的作用。

这样保证了所有**待处理**的  **`setState`** reducer 将在每一个  **`withState`** lambda 之前运行。

假设你有以下两个操作：

1. **`setState { ... }`**
2. **`withState { ... }`**

在调用  `flushQueuesOnce`  之前，`setState`  操作会被放入  `setStateChannel`  中，而  `withState`  操作会被放入  `withStateChannel`  中。`flushQueuesOnce`  函数会确保首先处理  `setStateChannel`  中的所有消息，然后再处理  `withStateChannel`  中的消息。这确保了在  `withState`  操作执行时，状态已经是最新的。

**invalidate 效率问题探究**

首先`invalidate`的思路本身没有问题，它和 React 中的`render`是保持一致的，但是 React 中是有 Virtual Dom 的 diff 算法来确定哪些节点需要真正更新的，如果没有这样的机制，就会造成效率问题。

在单纯 Mavericks 环境下，我们应该使用`invalidate()`吗？

我认为是不应该的，因为 Mavericks 没有这样的 diff 机制来保证局部刷新（可以通过 Airbnb 的 另一个框架 Epoxy 借助 Recyclerview 实现的 diff 机制来保证局部刷新，但是这又是另一回事了，在有了 Compose 之后，Epoxy 就显得有点鸡肋了）。所以我们在单纯 Mavericks 环境下应该尽量使用`onEach`来对指定的属性进行监听和订阅。

### State 中便捷更新 List/Map 的扩展方法

list：

```kotlin
// 增删
setState { copy(list = list - newList) }
setState { copy(list = list + newList) }
// 修改
fun <T> List<T>.update(newValue: (T) -> T, finder: (T) -> Boolean) =
    indexOfFirst(finder).let { index ->
        if (index >= 0) copy(index, newValue(get(index))) else this
    }

fun <T> List<T>.copy(i: Int, value: T): List<T> = toMutableList().apply { set(i, value) }

setState { copy(list = list.update({ it.copy(checked = true) }, { it.id == id })) }
```

map:

```kotlin
// 修改
fun <K, V> Map<K, V>.copy(vararg pairs: Pair<K, V>) =
    HashMap<K, V>(size + pairs.size).apply {
        putAll(this@copy)
        pairs.forEach { put(it.first, it.second) }
    }

// 删除
fun <K, V> Map<K, V>.delete(vararg keys: K) =
    HashMap<K, V>(size - keys.size).apply {
        this@delete.entries.asSequence()
            .filter { it.key !in keys }
            .forEach { put(it.key, it.value) }
        }
```

### 参考：

[Mavericks Docs (airbnb.io)](https://airbnb.io/mavericks/#/)

[Mavericks Meet Jetpack Compose - 掘金 (juejin.cn)](https://juejin.cn/post/7077226398854676493)
