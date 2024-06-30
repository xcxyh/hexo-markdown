---
title: Hexo 博客中的图片怎么管理？
date: 2024-06-02 19:09:08
tags: hexo建站
categories: HEXO 相关
---

一般来讲，我们的博客中会有很多的图片，如果都提交到 Hexo 项目中进行发布的话，会导致我们的 Hexo 静态网站项目非常臃肿，极不推荐使用这种方式来管理博客中的图片。

如果是我们本地写 Markdown 笔记，图片一般会保存到本地目录，如果是在 Notion or 一些云笔记网站上写，图片会上传到它们的服务器进行保存。

对于 Hexo 博客，这里推荐使用 图床 的方式来进行管理。

首先，介绍一下 picgo，**PicGo 是一个用于快速上传图片并获取图片 URL 链接的工具。**

[PicGo is Here | PicGo](https://picgo.github.io/PicGo-Doc/zh/guide/)

PicGo 本体支持如下图床：

- `七牛图床` v1.0
- `腾讯云 COS v4\v5 版本` v1.1 & v1.5.0
- `又拍云` v1.2.0
- `GitHub` v1.5.0
- `SM.MS V2` v2.3.0-beta.0
- `阿里云 OSS` v1.6.0
- `Imgur` v1.6.0

我们可以结合使用 picgo + github，来管理博客中的图片。

我们选择直接复用 我们托管 Hexo 博客的 github 仓库，也就是 [xcxyh.github.io](http://xcxyh.github.io) 这个仓库，来新建个 image-save 的分支管理图片。

在 PicGo 中配置：

![Untitled](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202406021902888.png)

其中，git token 的生成方式 可以参考：[github 生成 token 的方法 - 南菜园 - 博客园 (cnblogs.com)](https://www.cnblogs.com/leon-2016/p/9284837.html)

设置完成之后，可以测试上传一张图片，在相册中 复制图片的链接，看是否可以访问。

![Untitled 1](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202406021902261.png)

结合 Typora 使用：

当我们成功搭建好图床之后，每次写 Markdown 文档时，都需要先截图，再保存，然后手动打开 Picgo 完成上传，最后将图片地址复制到 Markdown 文档中。

如何做到更加高效地上传图片到图床呢？

用 Typora 写笔记，只需要先截图，再粘贴到 Markdown 文档，根据提示直接上传图片，Typora 帮我们自动完成。

操作为：打开 Typora 的设置，点击图像，按照我给的图片进行设置，替换 PicGo 路径为你当前的安装路径。

![Untitled 2](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202406021902052.png)

可以点击验证图片上传，验证是否设置成功~~

之后，我们便可以愉快地用 Hexo 写图文并茂的博客啦~~~~
