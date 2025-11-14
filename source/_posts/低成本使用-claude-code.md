---
title: 低成本使用 claude code
date: 2025-11-14 22:42:24
tags: ai coding
---

# 低成本使用Cluade code

Claude Code 是由 Anthropic 推出的一个“agentic coding 工具”——也就是说，它不仅仅是一个简单的代码补全工具，而是能够“理解你的代码库、执行常见任务、做多文件修改、解释代码、甚至做 git 操作”的终端/IDE 工具。

![image-20251114232908619](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142329027.png)

它通常以 CLI（命令行界面）方式运行，也可以在 IDE 插件中进行集成。你在终端里输入自然语言，比如 “请分析这个模块的依赖”／“帮我重构这些类”之类，它就能够理解并执行。它可以**理解整个代码库上下文**，而不仅仅局限于当前文件。比如它可以扫描项目目录、理解结构、理解依赖关系。

但是，在中国，想要正常使用 Claude code 确并不容易，即使通过一些手段解决了订阅问题。也不时会担心遭到 禁用、封号。

环境要求：node js 版本 >= 20 

```
nvm install latest
nvm use latest
npm install -g @anthropic-ai/claude-code
npm install -g @musistudio/claude-code-router
```

claude-code-router 全局配置(推荐，没有该文件就创建一个)：

```
C:\Users\<你的用户名>\.claude-code-router\config.json
```

Router 会在启动时自动扫描用户目录下的配置文件。

当然，也可以有项目级配置(适合放到当前项目下目录下启动)：

```
D:\Projects\claude-code-router\config.json

ccr --config config.json
```

在 claude-code-router.config.json 中加入以下配置：（这里使用火山引擎的api，便宜模型还多）

api key 获取页面：[API Key 管理--火山方舟大模型服务平台-火山引擎](https://www.volcengine.com/docs/82379/1361424)

模型开通页面：[开通管理--火山方舟大模型服务平台-火山引擎](https://www.volcengine.com/docs/82379/1159200)

```
{
    "LOG": true,
    "Providers": [
      {
        "name": "volcengine",
        "api_base_url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        "api_key": "你的火山 api key",
        "models": [
          "kimi-k2-250711",
          "doubao-seed-1-6-250615",
          "doubao-seed-1-6-thinking-250615"
        ]
      }
    ],
    "Router": {
      "default": "volcengine,kimi-k2-250711",
      "background": "volcengine,kimi-k2-250711",
      "think": "volcengine,doubao-seed-1-6-thinking-250715",
      "longContext": "volcengine,kimi-k2-250711"
    }
  }
```

配置完毕之后，直接新建一个项目目录，然后进入到项目目录下，cmd，然后输入以下命令启动。

```bash
# 启动 claude code
ccr code
# 如果报错可以重启重新加载一下配置 
ccr restart
```

如果你遇到了一些登录认证相关的问题，也可以配置以下环境变量，禁用 prompt caching 功能。

```
DISABLE_PROMPT_CACHING = 1
```

![image-20251114232846470](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142328471.png)

输入命令后，可以看到如下页面就是配置成功：

![image-20251114235755013](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142357248.png)









