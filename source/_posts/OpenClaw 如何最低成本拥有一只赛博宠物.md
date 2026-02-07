---
title: 'OpenClaw: 如何最低成本拥有一只赛博宠物（踩坑无数~纯手打教程）'
date: 2026-02-06 12:28:30
tags: AI,OpenClaw
---



最近 clawdbot 【[OpenClaw — Personal AI Assistant](https://openclaw.ai/)】火的一塌糊涂，无数人都想要拥有一个自己的聊天机器人，但是，由于这个项目还在非常初级的阶段，而且又历经三次改名，从 clawdbot 到 moltbot 再到 openclaw 才稳定下来，整个项目配置起来极其麻烦，有各种暗坑。

作为普通人，如何以最低成本拥有一个稳定的属于自己的 24小时待命的赛博宠物呢？

我探索出了一套成本极低的部署方案，那就是：亚马逊云服务器 + Minimax Coding Plan + 飞书应用 的部署方案。

为啥选择这套方案？

虽然说国内三大厂商迅速跟进，腾讯云、阿里云、火山引擎都出了自己的一键部署 bot的服务器方案，但是这三家的服务器都是 丐中丐版本的 2G 运行内存的实例，随便装点复杂的功能都没法用，而且网络环境又差，一些开源项目在github上，要下载都是龟速。

而且由于 openclaw 更新太太太频繁了，这些云厂商的构建脚本刚出来基本就过时要换了，火山云的构建脚本就从 clawdbot 、moltbot 到 openclaw 改了好几次。

经过我将三家厂商尝试了个遍的惨痛经历，最终我选择了亚马逊云部署。

亚马逊云实例的优点：

1. 新用户选择 free plan，180 天 100 刀额度，而且不升级plan不会扣费。相当于半年免费。
2. 亚马逊云免费套餐 可以选择 2核8G运行内存的 实例，硬盘存储空间也大。比 国内的 丐中丐 云服务器强太多。
3. 网络环境极好，什么都可以下载，下载速度非常快。

再说为什么选择 Minimax Coding Plan，因为对于 clawdbot 来说，实际使用你就会发现，这个东西非常消耗token，如果使用国内云服务器厂商提供的按量计费的方案，token消耗速度非常快，一天几十块就没了。Minimax Coding Plan 按月订阅， 按照使用额度计费，5小时 额度自动重置，省钱，巨省钱。除了订阅费，不用额外买token。

最后，选择飞书就很容易理解了，飞书机器人创建简单，而且 飞书支持的消息格式丰富，再加上 openclaw 最近刚刚官方支持了 社区版最好用的 飞书插件（2k star 的那个），直接按照指引安装即可。



## 亚马逊云云服务器（Free Plan）

开始前的准备：

1. 一个良好的网络环境🙂。
2. 一个邮箱。
3. 一个国内手机号 + 国内信用卡/借记卡 都行。

新用户注册绑卡后即可免费使用。作为老牌云服务器提供商，亚马逊云给新用户提供了 free plan ，100 US 的免费额度：

注册链接：[AWS Console - Signup](https://signin.aws.amazon.com/signup?request_type=register)

![image-20260206192501990](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602061925446.png)

注册过程很简单，按照指示操作即可，信用卡地址随便填国内的就行，国内手机号可以收短信验证。

登录后，来到首页，选择 EC2，创建云服务器实例。

![image-20260206194503800](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602061945444.png)

左侧选择实例，启动新实例。新建名称，选择 linux 服务器。

![image-20260206194614681](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602061946367.png)

注意，这里实例类型我们选最大的 8 G 的那个：

![image-20260206194710832](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602061947584.png)

然后创建一个密钥对，用于登录，这时会下载一个 pem 文件，保存好，后续从本地电脑连接服务器要用。（服务器的钥匙）

![image-20260206194804145](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602061948615.png)

最后，配置存储，这里我们选 100G，然后其他都是默认不用填，直接点击启动实例就创建好了。

![image-20260206194839321](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602061948673.png)

最后，来到实例管理页面，选择要连接的实例，连接即可登录进入，直接点连接，登录进去，看到命令行页面就成功了，这一步就完成了。

![image-20260206195039817](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602061950185.png)

## MiniMax Coding plan

Clawdbot 作为一个 Agent，需要配置一个 LLM 大模型，使用过程中会消耗大量token，所以这里是我们唯一需要花钱的一步。这里我们选择 minimax，量大，便宜。打开 https://platform.minimaxi.com/subscribe/coding-plan?code=hGjTEmSvw2&source=link，注册登录。然后选择 订阅 coding plan。[Coding Plan - MiniMax API 平台](https://platform.minimaxi.com/subscribe/coding-plan)。

选择 Starter 套餐，一个月的花费算是非常便宜的了。购买后来到账户管理页面，看到coding plan 的当前使用情况就证明ok了，什么都不用操作，这一步就完成了。然后来到 请求限制，开启一下限流预警，这里开启之后快用超了，就会提醒的。

![image-20260206200025108](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062000435.png)

这里顺便解释一下minimax coding plan 套餐的计费逻辑：40 prompts 每 5 小时

这里的 **prompt** 一般是指一次完整的模型调用请求，而不是单纯的一条聊天消息。多次交互算一次prompt，良心！

- ![image-20260206201130932](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062011124.png)

也就是说：

👉 **你在 5 小时内最多可以发起 40 次模型请求**

无论请求大小，只按“次数”计数。这里可以理解为 clawdbot 真正调用 llm 的那一次完整的请求。

而且， 5小时 的计算是 **滚动时间窗口（rolling window）**，从你发送第一个 prompt 开始，系统会向后滚动计算 5 小时的窗口。

5小时 40次，大部分场景够用了。

这种计费逻辑对于使用 clawdbot 这种 Agent 是比较友好的，省钱。因为Agent每轮的交互都会携带很多上下文和指令，单次token消耗大。

## OpenClaw 安装

来到官网[OpenClaw — Personal AI Assistant](https://openclaw.ai/)，复制 curl ，回到 云服务器 控制台界面执行。

![image-20260206201345649](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062013038.png)

直接执行，这个安装脚本写的也非常烂，普通人跟着跑一遍，基本都会遇到很多坑。这里我记录下怎么解决。

运行完成之后，等待一段时间：会有这样的一个提示，第一个坑点，不解决后续会遇到 openclaw 命令找不到的情况。

![image-20260206202931468](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062029284.png)

```
export PATH="/home/ec2-user/.npm-global/bin:\/home/ec2-user/.npm-global/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin"
source ~/.bashrc
```

这里先不管，等一切安装成功之后，再执行以上命令。接下来跟着我一步步操作即可。

![image-20260206203249723](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062032883.png)

![image-20260206203316030](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062033659.png)

模型选择 minimax：

![image-20260206203345928](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062033230.png)

![image-20260206203405115](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062034183.png)

然后选 第一个oauth，回车，这里不要按 ESC 或者 Ctrl + C，不然就退出了，又得重新来。这里 endpoint 选 cn。

![image-20260206203513919](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062035948.png)

![image-20260206203552854](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062035032.png)

然后鼠标右键复制（不要用  Ctrl + C）出来这个连接，浏览器打开授权即可。授权成功返回继续。选择第一个 keep current。

![image-20260206203840554](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062038879.png)

![image-20260206203920828](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062039900.png)

channel 这里选择飞书进行安装：回车

![image-20260206204019787](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062040572.png)

![image-20260206204046162](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062040152.png)

这里是skills ，先跳过吧，暂时用不上，后续装就行了。选 No

 ![image-20260206204133464](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062041587.png)

到这里，bot 就安装完成了，这里的意思是，你想怎么使用 clawdbot，这里提供了 两种方式，一种 是 TUI （命令行模式），一种是webui，通过网页chat 页面的形式来使用。这里我们就不使用了，先把环境装好。选 do this later

![image-20260206204315090](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062220770.png)

![image-20260206204429171](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062044294.png)

到这里就装好了，现在来解决两个问题：

1. openclaw 命令找不到问题：

直接执行：

```
export PATH="/home/ec2-user/.npm-global/bin:\/home/ec2-user/.npm-global/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin"
source ~/.bashrc
```

2. 如何连接 openclaw dashborad

首先在命令行输入：

```
openclaw dashboard
```

然后直接复制连接在浏览器访问url，发现访问不了，这时，我们上面下载的 pem 就有用了，

![image-20260206204749222](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062047110.png)

在 自己的本地电脑上执行以下命令（而不是服务器上）

![image-20260206205220498](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062052683.png)

```
ssh -i "C:\Users\Administrator\Downloads\my-esc.pem" -N -L 18789:127.0.0.1:18789 ec2-user@你的服务器公网ip
```

这里 需要改成你的 pem 文件路径，和 你的 服务器公网ip（在云服务器的下方就可以看到一个 publicips 就是它）

![image-20260206205038514](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062050573.png)

连接之后，刷新一下刚才的浏览器页面，可以正常访问了：到这里就安装完成了，可以去chat 里面跟它对话。

![image-20260206205626898](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062056393.png)

## 飞书 Channels 配置

首先，我们先去飞书开发者后台创建一个自己的机器人应用：（非常简单，就两步）https://open.feishu.cn/app

1. 创建应用。应用图标，名称都可以自定义。

![image-20260206205936903](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062059106.png)

2. 点击机器人进入 权限管理，点击导入权限，复制以下内容进去，开通即可。开通之后，提示需要发布，直接发布即可。

```
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "docx:document:readonly",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:chat:read",
      "im:chat:update",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message.pins:read",
      "im:message.pins:write_only",
      "im:message.reactions:read",
      "im:message.reactions:write_only",
      "im:message:readonly",
      "im:message:recall",
      "im:message:send_as_bot",
      "im:message:send_multi_users",
      "im:message:send_sys_msg",
      "im:message:update",
      "im:resource"
    ],
    "user": [
      "aily:file:read",
      "aily:file:write",
      "base:record:retrieve",
      "contact:contact.base:readonly",
      "contact:user.employee_id:readonly",
      "docs:document.content:read",
      "docx:document:readonly",
      "im:chat.access_event.bot_p2p_chat:read",
      "search:docs:read",
      "sheets:spreadsheet.meta:read",
      "sheets:spreadsheet:read",
      "wiki:node:read",
      "wiki:wiki:readonly"
    ]
  }
}
```

然后记下这里的 app id 和 app secret，后面配置要用。

![image-20260206210248124](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062102416.png)

然后，回到服务器，输入 openclaw channels add

![image-20260206210423569](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062104503.png)

![image-20260206210440451](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062104470.png)

![image-20260206210609734](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062106741.png)

account id 先随便写，选 飞书 china，然后输入 app id 和 app secret

最后回到这个页面，移动到 finished ，点击回车。

![image-20260206210739680](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062107755.png)

![image-20260206210817125](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062108304.png)

这里开始配对，然后这里就完成了

![image-20260206210847823](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062108047.png)

![image-20260206210909624](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062109699.png)

最后一步，输入 openclaw gateway restart 重启一下 openclaw，跟飞书机器人建立连接。这样才能在 飞书机器人页面上去开通事件与回调。

![image-20260206212208184](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062122379.png)

选择使用长连接，保存，然后 添加事件 im.message.receive_v1 ，最后，一定要再发布一次应用，不然不生效。

![image-20260206212401020](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062124238.png)

![image-20260206212622098](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062126349.png)

这里，就已经配置完成了，然后我们将 飞书机器人和clawdbot 进行配对。

1. 先在飞书上找到这个机器人，发送一条消息给机器人。

![image-20260206212956437](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062129772.png)

2. 然后 拿到 pairing code，到 服务器命令行中执行命令：openclaw pairing approve feishu 2DM42xxx 即可完成。

连接成功，可以随意发消息啦。

最后，运行下 openclaw update ，更新到最新版本 openclaw ，使用最新的 飞书插件即可~。

![image-20260206213305880](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062133089.png)

## 设定聊天机器人人设

可以通过聊天建立 bot 的人设，也可以去到 dashboard 页面进行手动配置和修改：这些内容我们都可以自定义。

![image-20260206213702219](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062137390.png)

以下是 OpenClaw 自己的介绍：

这些是OpenClaw工作区的配置文件，我来简单说明一下：

| 文件         | 作用                                                         |
| ------------ | ------------------------------------------------------------ |
| AGENTS.md    | 工作区手册 — 告诉我如何在这里工作，比如内存管理、心跳检查、群聊礼仪等 |
| SOUL.md      | 灵魂文件 — 定义我的核心性格、价值观和行为准则                |
| IDENTITY.md  | 身份卡 — 我的名字、是什么类型的生物、风格、emoji头像等       |
| USER.md      | 用户档案 — 记录你的信息、偏好、项目背景等                    |
| TOOLS.md     | 工具笔记 — 本地设备配置（SSH、摄像头、TTS等）的速查表        |
| HEARTBEAT.md | 心跳任务 — 周期性后台检查（邮件、日历、天气等），为空则不检查 |
| BOOTSTRAP.md | 首次启动引导 — 第一次运行时帮我认识自己和你，然后会删除      |


核心逻辑：

• AGENTS.md + SOUL.md = 我的"使用说明书"
• IDENTITY.md + USER.md = 我们俩的互相认识
• memory/ 文件夹 = 长期和短期记忆（类似人类的记事本）
每次会话开始，我会先读取这些文件来"醒来"。

## 安装自定义 skills

然后就可以通过bot 安装一些自定义的 skills 来建设一些能力了~。

这里我推荐三个能力：

1. 火山引擎 融合信息搜索，用于替代 自带的 web search skill，那个需要配置 brave search，没有api key 用不了。

2. 火山引擎 豆包 seedream 4.5 生图，用于替代自带的 nano banana pro 生图，如果你有 则不用配置，直接配置 nano banana 就行。
3. 火山引擎 豆包 seedance 1.5 pro 生视频。

安装过程中，有什么问题都可以让 bot 来解决。还是非常简单的。

可以直接 输入以下命令快捷安装以上三个 skill：

```
帮我安装这个仓库中的skills：https://github.com/xcxyh/my-custom-skills，并引导我获取相关配置api key，直到安装并测试成功。
```

火山模型开通页面：[火山方舟管理控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM={}&advancedActiveKey=model)

火山生图生视频apikey管理页面：[火山方舟管理控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)

火山融合信息搜索api key管理页面：[火山引擎控制台](https://console.volcengine.com/ask-echo/api-key)，如下，这里入口隐藏太深。

![image-20260206221242170](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062212357.png)

## 它可以干啥

1. 跑一些定时任务，例如总结、日报等
2. 盯盘，也是定时任务。
3. 安装一些skills，自动写文章、剪视频、发布 公众号、小红书等等。
4. 整理邮件，关联日程，自动回复等等
5. 指挥 其他 coding agent 写代码等等，不要用它来直接写代码，太费token了，这个bot 贼墨迹。

例如，让它每日总结日报：

```
来活了，你帮我个忙，每天早上9点，抓取一下这些网页最近24小时的消息： https://openai.com/zh-Hans-CN/news/ https://karpathy.ai
https://blog.samaltman.com/ https://blog.gregbrockman.com/ https://fchollet.com/
https://lilianweng.github.io/ https://colah.github.io/
https://medium.com/@woj.zaremba https://mustafa-suleyman.ai/ https://deepmind.google/blog/ https://www.darioamodei.com/ https://karinanguyen.com/ https://steipete.me/
https://simonwillison.net/ https://ai.hubtoday.app/
https://www.anthropic.com/research https://hy.tencent.com/research https://hn.buzzing.cc/
如果最近24小时没有新内容的，就忽视掉。
如果有新内容的，就整理起来，找到跟AI产品，论文，观点，认知相关的你觉得最棒的10条，每天早上9点给我以飞书云文档的形式，发送一份详细的AI日报，这个云文档用Markdown渲染。
```

例如，连接 notion ：

让它连接你的 notion 笔记，直接让跟他聊天按照bot 给的步骤 安装就行了，可以帮你记笔记，整理知识库，写文章同步到notion等等。

![image-20260206215231313](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602062152070.png)

总之给他越多的技能，他能做的事情也就越多，权限也就越大。更多好玩的也有待探索。

你能看到这，并成功创建一个自己的bot，那是真的很不容易啦~

