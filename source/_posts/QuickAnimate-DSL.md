---
title: QuickAnimate DSL
date: 2024-07-13 19:05:02
tags: Android
categories: Android 开发
---

一句话描述：

使用 Kotlin DSL （Domain-Specific Language，领域特定语言）和 ValueAnimator 实现一个动画框架，以 DSL 的方式来方便、快速的实现对 view 的各种属性动画。


通过 Kotlin DSL 的方式来组合针对 view 的多个属性的动画，用于快速、简单的实现复杂的组合动画效果。简单又好用------使用示例：

```kotlin
fun animateTest(view: View) {
    val controller: Animators.Controller = quickAnimate {
        together {
            play {
                targets = listOf(view)
                duration = 300L
                interpolator = LinearInterpolator()
                translationX(0f, 100f)
            }
            play {
                targets = listOf(view)
                duration = 300L
                interpolator = LinearInterpolator()
                translationY(0f, 100f)
            }
        }
        onStart = {}
        onEnd = {}
    }
    // 开始动画
    controller.start()
}
```

Animators 类： quickAnimate { } 代码块中的 receiver 实现类。通过 封装 Controller 的方式对外提供控制动画的接口。

```kotlin
fun quickAnimate(init: Animators.() -> Unit): Animators.Controller
```

SingleAnimator 类： 具体的 动画动作  封装类 ，也就是 play { } 代码块中的receiver 实现类。负责完成单个属性动画。

```kotlin
fun play(anim: SingleAnimator.() -> Unit)
```

同时也支持多个动画的组合动画，通过 together 包裹的 动画会同时执行。否则，默认所有动画都是 串行执行。

```kotlin
fun together(init: Animators.() -> Unit)
```

最后，提供一个控制类 Animators.Controller ，用于 控制 动画的 开始 、取消，暂停 等操作。

API 接口设计如下：

```kotlin
fun quickAnimate(init: Animators.() -> Unit): Animators.Controller

class Animators {

	class Controller {
		fun start()
				
		fun cancel()
				
		fun pause()
				
		fun resume()
				
		fun isRunning(): Boolean
	}
		
	fun play(anim: SingleAnimator.() -> Unit)
		
	fun together(init: Animators.() -> Unit)
		
	class SingleAnimator {
		
	}
}
```

对于 具体的View 的属性动画，主要利用以下API 来实现：

```kotlin
public static <T> ObjectAnimator ofFloat(T target, Property<T, Float> property, float... values)
```

`ObjectAnimator` 是 Android 动画框架中的一个类，专门用于执行属性动画。`ObjectAnimator` 可以对目标对象的某个属性执行动画，例如透明度、旋转角度、位置等。

**`Property<T, Float> property`**: 目标对象的属性。`Property` 是一个属性的抽象表示，这里可以传入以下属性：

```kotlin
View.ALPHA
View.ROTATION
View.TRANSLATION_X
View.TRANSLATION_Y
......
```

**`float... values`**:  动画的关键帧值序列。可以传入多个值，动画将依次在这些值之间进行插值。

对于单个动画，可以提供以下配置属性，用于配置动画的 view对象、动画时长、插值器、repeatMode 等参数。

```kotlin
var duration: Long = 0L
var targets: List<View?> = emptyList()
var interpolator: TimeInterpolator? = null
var repeatMode: Int = ValueAnimator.RESTART
var repeatCount: Int = 0
```

单个动画使用示例：

```kotlin
play {
	targets = listOf(view)
	duration = 300L
	interpolator = LinearInterpolator()
	repeatMode = ValueAnimator.RESTART
	repeatCount = 0
	translationY(0f, 100f)
}
```

注意：这里只是完成了动画的配置，并没有真正开始动画，需要通过 Animators.Controller 来统一来控制动画的 开始 、暂停、继续、取消等。

完整源码：

```kotlin
package com.example.helloworld

import android.animation.*
import android.util.Log
import android.util.Property
import android.view.View
import android.view.animation.LinearInterpolator

fun quickAnimate(init: Animators.() -> Unit): Animators.Controller {
    val animators = Animators().apply(init)
    val animSet = AnimatorSet()
    animSet.addListener(object : Animator.AnimatorListener {
        override fun onAnimationStart(animation: Animator?) {
            animators.onStart?.invoke()
        }
        override fun onAnimationEnd(animation: Animator?) {
            animators.onEnd?.invoke()
        }
        override fun onAnimationCancel(animation: Animator?) {
        }
        override fun onAnimationRepeat(animation: Animator?) {
        }
    })
    Log.i("xcc", "quick anim: ${animators.getAnimatorList()}")
    animSet.playSequentially(animators.getAnimatorList())
    return Animators.Controller(animSet)
}

class Animators {

    var onStart: (() -> Unit)? = null

    var onEnd: (() -> Unit)? = null

    private val anims: MutableList<Animator> = mutableListOf()

    fun getAnimatorList() = anims.toList()

    fun play(anim: SingleAnimator.() -> Unit) {
        val animator = SingleAnimator().apply(anim).createAnimator()
        Log.i("xcc", "add anim: $animator")
        anims.add(animator)

    }

    fun together(init: Animators.() -> Unit) {
        val animSet = Animators().apply(init).createAnimator()
        Log.i("xcc", "add animSet: $animSet")
        anims.add(animSet)
    }

    private fun createAnimator(): Animator {
        val animSet = AnimatorSet()
        animSet.addListener(object : Animator.AnimatorListener {
            override fun onAnimationStart(animation: Animator?) {
                onStart?.invoke()
            }
            override fun onAnimationEnd(animation: Animator?) {
                onEnd?.invoke()
            }
            override fun onAnimationCancel(animation: Animator?) {
            }
            override fun onAnimationRepeat(animation: Animator?) {
            }
        })
        animSet.playTogether(anims.toList())
        return animSet
    }

    class Controller(private val animator: Animator) {
        fun start() {
            animator.start()
        }

        fun cancel(){
            animator.cancel()
        }

        fun pause() {
            animator.pause()
        }

        fun resume() {
            animator.resume()
        }

        fun isRunning(): Boolean {
            return animator.isRunning
        }

    }

    class SingleAnimator {

        var duration: Long = 0L
        var targets: List<View?> = emptyList()
        var interpolator: TimeInterpolator? = null
        var repeatMode: Int = ValueAnimator.RESTART
        var repeatCount: Int = 0

        private val animList: MutableList<Animator> = mutableListOf()

        fun createAnimator(): Animator {
            val animSet = AnimatorSet()
            animSet.duration = this.duration
            animSet.interpolator = this.interpolator
            animSet.playSequentially(animList.toList())
            return animSet
        }

        fun translationY(
            vararg values: Float,
            onUpdate: ((animation: ValueAnimator) -> Unit)? = null
        ) {
            anim(property = View.TRANSLATION_Y, values = values, onUpdate = onUpdate)
        }

        fun translationX(
            vararg values: Float,
            onUpdate: ((animation: ValueAnimator) -> Unit)? = null
        ) {
            anim(property = View.TRANSLATION_X, values = values, onUpdate = onUpdate)
        }

        fun alpha(
            vararg values: Float,
            onUpdate: ((animation: ValueAnimator) -> Unit)? = null
        ) {
            anim(property = View.ALPHA, values = values, onUpdate = onUpdate)
        }

        fun rotate(
            vararg values: Float,
            onUpdate: ((animation: ValueAnimator) -> Unit)? = null
        ) {
            anim(property = View.ROTATION, values = values, onUpdate = onUpdate)
        }

        // add more view property here...

        private fun anim(
            property: Property<View, Float>,
            vararg values: Float,
            onUpdate: ((animation: ValueAnimator) -> Unit)? = null
        ) {
            targets.forEach {
                if (it == null) {
                    return@forEach
                }
                val anim = ObjectAnimator.ofFloat(it, property, *values)
                anim.addUpdateListener { animation ->
                    onUpdate?.invoke(animation)
                }
                anim.duration = this.duration
                anim.interpolator = this.interpolator
                anim.repeatMode = this.repeatMode
                anim.repeatCount = this.repeatCount
                animList.add(anim)
            }
        }

    }
}

var controller: Animators.Controller? = null

fun animateTest(view: View) {
    controller = quickAnimate {
        together {
            play {
                targets = listOf(view)
                duration = 300L
                interpolator = LinearInterpolator()
                translationX(view.translationX, view.translationX + 100f)
            }
            play {
                targets = listOf(view)
                duration = 300L
                interpolator = LinearInterpolator()
                translationY(view.translationY, view.translationY + 100f) {
                    Log.i("xcc", "on update: ${it.animatedValue}")
                }
            }
        }
        play {
            targets = listOf(view)
            duration = 300L
            interpolator = LinearInterpolator()
            alpha(0f, 1f)
        }
        play {
            targets = listOf(view)
            duration = 300L
            interpolator = LinearInterpolator()
            rotate(0f, 360f)
        }
        onStart = {
            Log.i("xcc", "onStart")
        }
        onEnd = {
            Log.i("xcc", "onEnd")
        }
    }
    controller?.start()
}
```
