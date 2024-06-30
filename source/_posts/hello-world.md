---
title: Hexo 建站-HelloWorld
tags: hexo建站
categories: HEXO 相关
---

为什么需要个人博客？

平时，作为个人记录，使用类似 Notion 的云笔记就足够了，为什么还需要一个个人博客呢，我认为个人博客有两个作用，一个是博客是展示自己的窗口，是对外的，让别人能够更快的了解你。另一个作用就是作为简历的补充，在找工作时，附上个人网站的链接，无论是 hr 还是 面试官，都可以通过个人博客网站快速了解你，这里的信息要比简历丰富，相比于没有博客网站的人更有优势。

一句话，它是向他人展示自己的窗口，也是简历的一部分。

Hexo 是一个快速、简洁且高效的博客框架。主要用于搭建静态博客。支持快速方便的将个人博客网站托管在 GitHub Pages 上，GitHub Pages 是一种静态站点托管服务，每个 GitHub 帐户或组织都可以有一个站点。

部署方式极其简单，只要简单几步，你就可以拥有一个个人网站。也可以参考官方文档搭建：

[文档 | Hexo](https://hexo.io/zh-cn/docs/)

# 环境搭建

首先保证你的电脑上有 node js 和 git 环境。

这里我推荐 创建两个 git 仓库，一个 git 仓库用来放 hexo 项目和博客 markdown 源文件，一个 git 仓库用于 部署 hexo 静态博客项目。可以将 放 hexo 项目和博客 markdown 源文件的仓库设置为 private 的，将 部署 hexo 的仓库设置为 public 的。

安装 hexo：

```java
npm install -g hexo
```

在想要的路径下新建一个名为 hexo 的文件夹（名字可以随便取），例如我的：

```java
D:\Hexo\hexo-markdown\
```

hexo 初始化：

```java
cd D:\Hexo\hexo-markdown\
hexo init
// 注意，先跑 hexo init，这个命令需要在一个空文件夹下运行
git init
```

输入以上命令后，hexo 会自动下载 hexo 项目初始化的文件到当前目录下，其中 \_config.yml 为网站的全局配置文件。如何配置这个配置文件，可以看官方文档，或者 config 文件中的注释配置。

```java
.
├── _config.yml
├── package.json
├── scaffolds
├── source
|   ├── _drafts
|   └── _posts
└── themes
```

关于主题，直接全网搜 hexo 主题，或者去这里[Themes | Hexo](https://hexo.io/themes/)挑一个自己顺眼的就行，将主题 下载到 themes 目录下，更改下 配置文件中的 theme 配置名称就行了。这里我选的是 [Hexo Theme Fluid (fluid-dev.com)](https://hexo.fluid-dev.com/) 这个主题，按照教程配置也很简单，这里就不介绍了。

# 博客生成、预览

```java
hexo g # 生成
hexo s # 启动服务
```

执行以上命令之后，hexo 就会在 public 文件夹生成相关 html 文件，这些就是你博客的静态文件，后续需要把这些提交到 GitHub 上。

hexo s 是开启本地预览服务，打开浏览器访问  `localhost:4000`  即可看到内容，很多人会碰到浏览器一直在转圈但是就是加载不出来的问题，一般情况下是因为端口占用的缘故。

一些常用的 hexo 命令：

```bash
hexo new "postName"   # 新建文章
hexo new page "pageName" # 新建页面
hexo generate # 生成静态页面至public目录
hexo server # 开启预览访问端口（默认端口4000，'ctrl + c'关闭server）
hexo deploy # 将.deploy目录部署到GitHub
hexo help  # 查看帮助
hexo version  # 查看Hexo的版本
hexo deploy -g  # 生成加部署
hexo server -g  # 生成加预览
# 命令的简写
hexo n == hexo new
hexo g == hexo generate
hexo s == hexo server
hexo d == hexo deploy
```

过程中遇到问题，可以先 hexo clean，再重试。

# 部署

首先，在 config 文件中 配置 部署方式，这里我们选择部署到 GitHub Pages 上。

```yaml
deploy:
  type: "git"
  repository: git@github.com:xxxxx/xxxxx.github.io.git # 写你自己的仓库
  branch: master
```

注意，需要先把 git 推代码的 ssh 配置完成，这样 在 部署时，hexo 会把最新代码推送到 部署仓库。

部署仓库创建：

新建一个名为 用户名.github.io  的仓库，比如说，如果你的 GitHub 用户名是 xcxyh，那么你就新建名为  xcxyh.github.io  的仓库，将来你的网站访问地址就是  xcxyh.github.io。仓库名字必须是：username.github.io，其中 username 是你的用户名。

由此可见，每一个 GitHub 账户最多只能创建一个这样可以直接使用域名访问的仓库。

hexo 部署命令：

```bash
hexo d
```

直接执行 hexo d 的话一般会报如下错误：

`Deployer not found: git`

这是因为缺少了一个插件，我们可以通过如下命令安装：

`npm install hexo-deployer-git --save`

然后输入 hexo d 就会将本次有改动的代码全部提交（PS：这里 hexo 选择的方式是强推到 master 分支）。

github.io  在大陆的加载速度过慢且延迟过高，可以选择将 个人网站部署在 Coding，可以参考：[CODING (qq.com)](https://support.qq.com/products/104149/faqs-more/?id=61222)

部署随机域名的个人网页流程：

新建团队用户，个人为管理。

新建 DevOps 项目，取名要与自己的团队名相同。

之后再左侧边栏中找到持续部署菜单栏，选中静态网站进行立即部署。

然后修改 配置 \_config.xml 中相关 deploy 部分即可。

# 写文章

在 hexo 根目录下执行命令：

```bash
hexo new '文章名称'
```

hexo 会帮我们在 \_posts 下生成相关 md 文件，我们只需要打开这个文件就可以开始写博客文章了，用这个命令的好处是帮我们自动生成了文章创建时间。
