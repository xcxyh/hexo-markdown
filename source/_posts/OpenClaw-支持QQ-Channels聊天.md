---
title: OpenClaw 支持QQ Channels聊天
date: 2026-02-07 11:37:01
tags: AI,OpenClaw
---

今天发现了一个非常好用的让 OpenClaw 支持 QQ 聊天的插件，地址如下：

https://github.com/BytePioneer-AI/openclaw-china/blob/main/doc/guides/qqbot/configuration.md

需要在 QQ 开发平台创建一个个人机器人。支持 单聊，群聊@，频道等消息渠道。

安装方式非常简单，只需要执行：

```
openclaw plugins install @openclaw-china/channels
```

然后配置以下内容：

```
openclaw config set channels.qqbot.enabled true
openclaw config set channels.qqbot.appId your-app-id
openclaw config set channels.qqbot.clientSecret your-app-secret
openclaw config set channels.qqbot.markdownSupport false


# 下面这些不需要配置，默认即可
openclaw config set channels.qqbot.dmPolicy open
openclaw config set channels.qqbot.groupPolicy open
openclaw config set channels.qqbot.requireMention true
openclaw config set channels.qqbot.textChunkLimit 1500
openclaw config set channels.qqbot.replyFinalOnly false
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
```

配置完成之后，输入命令重启即可使用了：

```
openclaw gateway restart
```

单聊测试：

![image-20260207114347182](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602071143384.png)

群聊测试：

![image-20260207114421119](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602071144498.png)

快去试试吧~
