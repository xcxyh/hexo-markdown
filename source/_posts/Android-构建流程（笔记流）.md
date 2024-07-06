---
title: Android 构建流程（笔记流）
date: 2024-07-06 21:17:01
tags: Android
categories: 笔记
---

Android的Apk构建流程主要包括资源的编译和代码的编译。梳理清楚打包构建过程能够帮助我们理解为什么编译耗时久以及如何去优化。我们可以从以下两个方面去理解Android的Apk打包构建的过程：

- Apk构建步骤
- Apk自动化构建中的Gradle Task

### Apk构建步骤

![APK构建](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407062110151.png)

![APK打包流程](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407062111331.png)

Apk的构建主要包括以下几个步骤：

1. 资源文件的编译，包括通过aapt工具编译（AndroidManifest.xml，res）等资源，通过AIDL工具处理AIDL文件生成Java文件。
2. Java & kotlin 源代码编译。
3. 代码混淆，以及利用dex 工具将 class 文件编译为 dex 文件。
4. 通过 apkbuilder / zipflinger 生成 apk文件。
5. 使用zipalign 对齐，提升 mmap 访问apk文件的速度。
6. 利用 apksigner 对apk文件进行签名。

**资源文件的编译**
可以分析一下一个Android工程中通常会包括哪些资源文件：

1. AndroidManifest.xml
2. res/ 文件夹下的文件
3. asset/ 文件夹下的文件

![app文件](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407062111418.png)

在编译资源文件时，除了 asset/ 文件夹下的文件会直接保留之外，xml 与 res/下的文件都会通过 aapt2 来编译为二进制文件。

`AAPT2`（`Android Asset Packaging Tool2`）是一种构建工具，`Android Studio` 和 `Android Gradle` 插件使用它来编译和打包应用的资源。`AAPT2` 会解析资源、为资源编制索引，并将资源编译为针对 `Android`平台进行过优化的二进制格式。Android Gradle 插件 3.0.0 及更高版本默认情况下会启用 AAPT2，因此通常不需要自行调用 `aapt2`。

其路径位于：`android_sdk/build-tools/version/`下

![aapt](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407062112525.png)

AAPT2 支持通过启用增量编译实现更快的资源编译。这是通过将资源处理拆分为两个步骤来实现的：

- [编译](https://developer.android.google.cn/studio/command-line/aapt2?hl=zh-cn#compile)：将资源文件编译为二进制格式。
- [链接](https://developer.android.google.cn/studio/command-line/aapt2?hl=zh-cn#link)：合并所有已编译的文件并将它们打包到一个软件包中。

这种拆分方式有助于提高增量编译的性能。例如，如果某个文件中有更改，只需要重新编译该文件。

编译过程：

1. 针对位于`res/values/`下的 xml资源文件，会被编译为以 `*.arsc.flat`作为扩展名的资源表。
2. 其他资源文件中，其他所有的xml文件都将转换为扩展名为 `*.flat` 的二进制 XML 文件。而对于png图片，则会被压缩，并采用 `*.png.flat` 作为扩展名。

```bash
aapt2 compile project_root/module_root/src/main/res/values-en/
strings.xml -o compiled/
aapt2 compile project_root/module_root/src/main/res/drawable
/myImage.png -o compiled/

# 生成文件 values-en_strings.arsc.flat 和 drawable_img.png.flat
```

链接过程：

AAPT2 输出的文件不是可执行文件，必须在链接阶段添加这些二进制文件作为输入来生成 APK，在链接阶段，AAPT2 会合并在编译阶段生成的所有中间文件（如资源表、二进制 XML 文件和处理过的 PNG 等 .flat文件），并将它们打包成一个 APK。而且，这个过程中还会生成 R.java文件、resources.arsc和ProGuard 规则文件，此时生成的apk 不含 Dex 等源码文件，无法安装到设备使用。

```bash
aapt2 link -o output.apk
 -I android_sdk/platforms/android_version/android.jar
    compiled/res/values_values.arsc.flat
    compiled/res/drawable_img.flat --manifest /path/to/AndroidManifest.xml -v
```

[R.java](http://R.java) 文件提供资源文件的id进行索引，而 resources.arsc 文件是资源索引表，供在程序运行时根据id索引到具体的资源路径。如下表所示， resources.arsc 保存了id 、name和路径的映射关系。

![resources文件](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407062112749.png)

resources.arsc 文件的格式：

文件头：描述整个文件的信息，数据结构为 Restable_header （[ResourceTypes.h](https://android.googlesource.com/platform/frameworks/base/+/56a2301/include/androidfw/ResourceTypes.h)）

全局字符常量池：存放所有的字符串，便于字符资源的复用。

资源包：多个资源包，系统资源应用资源等。

AIDL文件是一种用于进程间通信的接口文件，最终还是要生成为java文件，位于`android_sdk/build-tools/version/`的 aidl 工具 会将 aidl文件编译为java文件。

**Java & kotlin 源代码编译**

Javac 编译 所有Java代码，包括 AIDL生成的java文件，生成 .class文件。kotlinc 编译所有的kotin代码，生成 .class 文件。APT/KAPT生成的代码也是位于这个阶段，当注解被标记为 `AnnotationTarget.CLASS`时，相对应的注解处理器会在该阶段生成对应的java文件和class文件。

**代码混淆 D8**

在 `AGP 3.X`以后，`Google` 分别引入 `D8`编译器和 `R8`工具作为默认的 `DEX`编译器和混淆压缩工具。

`d8`是一种命令行工具，位于`android_sdk/build-tools/version/`，Android Studio 和 Android Gradle 插件使用该工具来将项目的.class字节码文件编译为在 Android 设备上运行的 DEX 字节码，即`dexing` 过程。

`R8`是 `ProGuard` 的替代工具，用于代码的压缩（`shrinking`）和混淆（`obfuscation`）。

在 `AGP3.4.0`版本中，`R8`把 `desugaring`、`shrinking`、`obfuscating`、`optimizing` 和 `dexing`都合并到一步进行执行。

脱糖（`desugaring`）即在编译阶段将在语法层面一些底层字节码不支持的特性转换为基础的字节码结构，(比如 `List` 上的泛型脱糖后在字节码层面实际为 `Object`)，新的语法可以在所有的设备上运行。

可以在 gradle.properties 中配置相关属性，来禁用D8、R8 和 desugaring等过程。

```bash
# Disables R8 for Android Library modules only.
android.enableR8.libraries = false
# Disables R8 for all modules.
android.enableR8 = false
# Disables desugaring
android.enableIncrementalDesugaring=false
android.enableDesugar=false
```

d8还可用于增量构建，`d8` 在执行增量构建时，会将一些额外的信息存储在 DEX 输出中。随后在完整构建应用时，`d8`会利用这些信息来正确处理 `--main-dex-list`选项以及合并 DEX 文件。

**apkbuilder / zipflinger 生成 apk**

将`manifest`文件、`resources`文件、`dex`文件、`assets`文件等等打包成一个压缩包，也就是`apk`文件。老版本使用 apkbuilder ，在`AGP3.6.0`之后，使用`zipflinger`作为默认打包工具来构建`APK`，以提高构建速度。

**zipalign 对齐**

`zipalign`是一种 zip 归档文件对齐工具，有助于确保归档文件中的所有未压缩文件相对于文件开头对齐。这样一来，您便可直接通过 mmap 访问这些文件，而无需在 RAM 中复制这些数据并减少了应用的内存用量。

<aside>
💡 注意：您必须在构建流程的特定时间点使用 `zipalign`。该时间点取决于您使用的应用签名工具：


- 如果您使用的是 [**`apksigner`**](https://developer.android.google.cn/studio/command-line/apksigner?hl=zh-cn)，则必须在为 APK 文件签名**之前**使用 **`zipalign`**。如果您在使用 **`apksigner`** 为 APK 签名之后对 APK 做出了进一步更改，签名便会失效。
- 如果您使用的是 [**`jarsigner`**](https://docs.oracle.com/javase/tutorial/deployment/jar/signing.html)，则必须在为 APK 文件签名**之后**使用 **`zipalign`**。
  </aside>

为了实现对齐，`zipalign`会更改 zip **本地文件标头**部分中 `"extra"`字段的大小。此过程还会更改 `"extra"`字段中的现有数据。

```bash
zipalign -p -f -v 4 infile.apk outfile.apk

-p 对齐 
-f 覆盖输出
-v 详细信息
4 4字节对齐
```

对齐的主要过程是将`APK`包中所有的资源文件距离文件起始偏移为4字节整数倍，对齐后就可以使用`mmap`函数读取文件，可以像读取内存一样对普通文件进行操作。

**apksigner 签名**

需要对apk文件进行签名，否则无法安装，实际项目中会有 debug 和release 两种不同的签名文件。`jarsigner`只能进行`v1`签名，而`apksigner`可以进行`v2`、`v3`、`v4`签名。

详细介绍：[Android开发应该知道的签名知识！ - 掘金 (juejin.cn)](https://juejin.cn/post/7111116047960244254)

消息摘要：对数据进行单向hash，得到固定hash值的过程。常见的摘要算法都有 MD5、SHA-1 和 SHA-256，满足 对相同内容多次hash结果一致，且很少发生hash碰撞。

非对称加密：非对称加密是使用公钥/私钥中的公钥来加密明文，然后使用对应的私钥/私钥来解密密文的过程。例如 https 通信过程中的非对称加密过程。

数字证书：由 CA机构颁发的证明公钥的身份的证书。

Android 中数字签名的生成和普通的数字签名并没有很大的区别。Android主要使用自签名的方式，不需要CA机构颁发的数字证书。

**v1 签名：**

利用`META-INFO`文件夹中以`MF`、`SF`和 `RSA`为扩展名的三个文件，将`apk`中除了`META-INFO`文件夹中的所有文件进行进行摘要写到 `META-INFO/MANIFEST.MF`；然后计算`MANIFEST.MF`文件的摘要写到`CERT.SF`；最后计算`CERT.SF`的摘要，使用私钥计算签名，将签名和开发者证书写到`CERT.RSA`。

v1签名的问题：

签名校验慢。

`META-INFO`文件夹不会被签名，存在一定安全隐患

**v2签名：**

Apk本质上为一个压缩包，而压缩包文件格式一般分为三块：文件数据区，中央目录，中央目录结束节。`V2`要做的就是，在文件中插入一个`APK Signing Block`，位于中央目录部分之前。

### Apk自动化构建中的Gradle Task

```bash
> Configure project :app
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:compileDebugAidl NO-SOURCE
> Task :app:compileDebugRenderscript NO-SOURCE
> Task :app:generateDebugBuildConfig UP-TO-DATE
> Task :app:checkDebugAarMetadata UP-TO-DATE
> Task :app:generateDebugResValues UP-TO-DATE
> Task :app:generateDebugResources UP-TO-DATE
> Task :app:mergeDebugResources UP-TO-DATE
> Task :app:packageDebugResources UP-TO-DATE
> Task :app:parseDebugLocalResources UP-TO-DATE
> Task :app:createDebugCompatibleScreenManifests UP-TO-DATE
> Task :app:extractDeepLinksDebug UP-TO-DATE
> Task :app:processDebugMainManifest UP-TO-DATE
> Task :app:processDebugManifest UP-TO-DATE
> Task :app:processDebugManifestForPackage UP-TO-DATE
> Task :app:processDebugResources UP-TO-DATE
> Task :app:compileDebugKotlin UP-TO-DATE
> Task :app:javaPreCompileDebug UP-TO-DATE
> Task :app:compileDebugJavaWithJavac UP-TO-DATE
> Task :app:mergeDebugShaders UP-TO-DATE
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:mergeDebugAssets UP-TO-DATE
> Task :app:compressDebugAssets UP-TO-DATE
> Task :app:processDebugJavaRes NO-SOURCE
> Task :app:mergeDebugJavaResource UP-TO-DATE
> Task :app:checkDebugDuplicateClasses UP-TO-DATE
> Task :app:desugarDebugFileDependencies UP-TO-DATE
> Task :app:mergeExtDexDebug UP-TO-DATE
> Task :app:mergeLibDexDebug UP-TO-DATE
> Task :app:dexBuilderDebug UP-TO-DATE
> Task :app:mergeProjectDexDebug UP-TO-DATE
> Task :app:mergeDebugJniLibFolders UP-TO-DATE
> Task :app:mergeDebugNativeLibs NO-SOURCE
> Task :app:stripDebugDebugSymbols NO-SOURCE
> Task :app:validateSigningDebug UP-TO-DATE
> Task :app:writeDebugAppMetadata UP-TO-DATE
> Task :app:writeDebugSigningConfigVersions UP-TO-DATE
> Task :app:packageDebug UP-TO-DATE
> Task :app:createDebugApkListingFileRedirect UP-TO-DATE
> Task :app:assembleDebug UP-TO-DATE

BUILD SUCCESSFUL in 571ms
31 actionable tasks: 31 up-to-date

Build Analyzer results available
```

```bash
:app:preBuild UP-TO-DATE    → 空task，锚点
:app:preDebugBuild  → 空task，锚点
:app:compileDebugAidl NO-SOURCE → 处理AIDL
:app:checkDebugManifest → 检查Manifest是否存在
:app:compileDebugRenderscript NO-SOURCE → 处理renderscript
:app:generateDebugBuildConfig   → 生成 BuildConfig.java
:app:mainApkListPersistenceDebug → 生成 app-list.gson
:app:generateDebugResValues → 生成resvalue，generated.xml
:app:generateDebugResources → 空task，锚点
:app:mergeDebugResources    → 合并资源文件
:app:createDebugCompatibleScreenManifests   → manifest文件中生成compatible-screens，指定屏幕适配
:app:processDebugManifest → 合并manifest.xml文件
:app:processDebugResources → aapt打包资源
:app:compileDebugKotlin → 编译Kotlin文件
:app:prepareLintJar UP-TO-DATE → 拷贝 lint jar包到指定位置
:app:generateDebugSources → 空task，锚点
:app:javaPreCompileDebug → 生成 annotationProcessors.json 文件
:app:compileDebugJavaWithJavac → 编译 java文件
:app:compileDebugNdk → 编译ndk
:app:compileDebugSources → 空task，锚点
:app:mergeDebugShaders → 合并 shader文件
:app:compileDebugShaders → 编译 shaders
:app:generateDebugAssets → 空task，锚点
:app:mergeDebugAssets → 合并 assests文件
:app:validateSigningDebug → 验证签名
:app:signingConfigWriterDebug → 编写SigningConfig信息
:app:checkDebugDuplicateClasses → 检查重复class
:app:transformClassesWithDexBuilderForDebug → class打包成dex
:app:transformDexArchiveWithExternalLibsDexMergerForDebug → 打包第三方库的dex
:app:transformDexArchiveWithDexMergerForDebug → 打包最终的dex
:app:mergeDebugJniLibFolders → 合并jni lib 文件
:app:transformNativeLibsWithMergeJniLibsForDebug → 合并jnilibs
:app:transformNativeLibsWithStripDebugSymbolForDebug → 去掉native lib里的debug符号
:app:processDebugJavaRes NO-SOURCE → 处理java res
:app:transformResourcesWithMergeJavaResForDebug → 合并java res
:app:packageDebug  → 打包apk
:app:assembleDebug → 空task，锚点
:app:extractProguardFiles → 生成混淆文件
```

Android Gradle Plugin源码阅读准备

[Gradle - renxhui的专栏 - 掘金 (juejin.cn)](https://juejin.cn/column/6963508988642230285)

Android gradle plugin 的源码的依赖：

```bash
implementation "com.android.tools.build:gradle:$VERSION"
```

在 gradle 7.0 之前，gradle 的版本和 agp 的版本号不一致，以下是对应关系：

![AGP版本对应](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407062112400.png)

安利查看 `AGP` 源码的一个方法，直接在项目依赖对应 `AGP` 版本即可，不需要手动下载源码

`implementation "com.android.tools.build:gradle:7.1.2"`

sync 完成之后，才可以看到AGP源码

![gradle](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407062113285.png)

全局搜索 AppPlugin.java 类，而不是 AppPlugin.kt 文件，可以看到 [com.android.application.properties](http://com.android.application.properties) 文件中记录的implementation-class对应的实现类。

```bash
implementation-class=com.android.build.gradle.AppPlugin
```

BasePlugin.java

![BasePlugin](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407062113274.png)

app 构建流程包括：

`configureProject`

`configureExtension`

`createTasks`

`createTasksBeforeEvaluate`

`createAndroidTasks`

经过代码跟踪，最终到`ApplicationTaskManager`类中完成了整个打包过程task 的构建。对于源码阅读，只需要在用到时查找某个功能的使用节点时在跟进代码，找到具体位置即可，例如想知道自定义的 tranform 是在哪个task 任务中被执行的，就可以从该入口进入进行查找：TaskManager#createPostCompilationTasks，关于这个方法的注释为：

`Creates the post-compilation tasks for the given Variant.
These tasks create the dex file from the .class files, plus optional intermediary steps like proguard and jacoco`

为给定变体创建编译后任务。
这些任务从.class文件创建 dex 文件，以及可选的中间步骤，如 proguard 和 jacoco

![tranform Task](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202407062114189.png)

agp 各个版本 api 变化较大，最新版本甚至都用kotlin 重写了整个流程，但是整个打包的主体流程是不变的。所以，我们只需要选择其中一个版本，分析它打包流程中所对应的各个task 的作用即可。



**参考资料：**

- 开发者官网：[Android 开发者  |  Android Developers (google.cn)](https://developer.android.google.cn/)
- AOSP官网：[Android 开源项目  |  Android Open Source Project (google.cn)](https://source.android.google.cn/?hl=zh-cn)
- 构建相关官方文档：[配置 build  |  Android 开发者  |  Android Developers (google.cn)](https://developer.android.google.cn/studio/build?hl=zh-cn)
- beesX：[Android安装包的打包流程 (yuque.com)](https://www.yuque.com/beesx/beesandroid/qqqbuh)
- 一些博客：[Android Apk 编译打包流程，了解一下~ - 掘金 (juejin.cn)](https://juejin.cn/post/7113713363900694565)