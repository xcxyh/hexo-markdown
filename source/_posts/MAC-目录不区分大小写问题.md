---
title: MAC 目录不区分大小写问题
date: 2024-06-02 19:13:16
tags:
---

在苹果文件系统 **APFS (Apple File System)**  中，默认情况下是不区分大小写的，这意味着文件和文件夹的名称不区分大小写。例如，"Document.txt" 和 "document.txt" 被视为相同的文件。这种行为适用于大多数用户，并且是 macOS 和 iOS 设备的默认设置。

最近遇到了一个该特性导致的问题，在往 git 仓库提交文件时，两个人分别创建了两个同名的不区分大小写的文件夹，例如是：”Module” 和 “module”，这两个文件夹都被提交到 git 仓库中了，然后，我本地在拉取代码到 Mac 本地时，这两个文件夹中的内容就被合并了，在不区分大小写的 mac 文件系统中，无法区分出这两个文件夹。

这种情况导致了一些问题，我们的代码编译是在 linux 上进行的，由于 linux 系统是区分大小写的，所以 在 Module 和 module 中的文件 出现了混乱，导致编译失败。

解决方案：

在 mac 上新建一个区分大小写的文件系统分区，打开磁盘工具，创建一个区分大小写的磁盘分区。

![apfs](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024Untitled.png)

然后拉取源代码到本地，这时，就可以看到有两个不同的 “Module” 和 “module” 目录，然后选择保留其中一个目录，例如，保留 “module” 小写目录，然后移动所有 “Module” 目录中的文件到 “module” 中之后，删除 “Module” 目录，重新提交更改到 git 仓库。

移动文件的相关指令，到 这两个文件夹的 父目录下，执行：

```bash
rsync -av --remove-source-files Module/ module/
```

`-a`：归档模式，递归复制并保持文件属性。

`-v`：显示详细输出。

`--remove-source-files`：在同步后删除源目录中的文件。

这个命令会将源目录中的所有文件移动到目标目录，并在完成后删除源目录中的文件。
