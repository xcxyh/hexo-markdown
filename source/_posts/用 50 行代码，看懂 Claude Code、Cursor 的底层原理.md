---
title: 用 50 行代码，看懂 Claude Code / Cursor 的底层原理
date: 2026-03-17 23:27:00
tags: AI Coding
---

# 用 50 行代码，看懂 Claude Code / Cursor 的底层原理

Claude Code、Cursor、Windsurf、Kode……

这些 AI Coding Agent，你一定用过，或者至少听说过。

它们看起来像“黑科技”：  
自动改代码、自动分析项目、甚至还能自己拆任务。

但如果你真的拆开它们的实现，会发现一个很反直觉的事实：

> **它们的核心，其实非常简单。**


最近看到一个开源项目：  
👉 https://github.com/shareAI-lab/learn-claude-code  

它做了一件很有意思的事情：

> 用 12 个渐进式课程，从 50 行代码开始，带你一步步实现一个 nano 版 Claude Code。


## 一句话结论

如果你只记住一句话，那就是：

> **Agent = 一个循环（Loop）+ 一组工具（Tools）**

甚至可以再简单一点：

> **一个 while 循环 + 一个 Bash 工具 = 一个可用 Agent**


# 一、Agent 的本质：一个“会思考的循环”

所有 AI Coding Agent，本质都是同一个执行模式：

```

用户输入 → messages（上下文） → LLM → 输出
↓
是否需要调用工具？
↓        ↓
是        否
↓         ↓
执行工具     返回结果
↓
写回 messages
↓
继续循环

```

用代码表达，大概就是这样：

```python
def agent_loop(messages):
    while True:
        response = llm(messages, tools)

        if response.stop_reason != "tool_use":
            return response

        for tool_call in response.content:
            result = execute_tool(tool_call)
            messages.append(result)
```

就这么简单。

## 关键点有三个

### 1️⃣ Agent 不是 Prompt，而是 Runtime

很多人把 Agent 当成“高级 Prompt”。

其实不是。

> Agent 本质是一个“持续运行的系统”。

LLM 只是大脑，而这个循环，才是“生命”。


### 2️⃣ LLM 不执行，它只决策

模型只负责：

* 下一步做什么
* 要不要调用工具

真正干活的是：

> **工具（Tools）**


### 3️⃣ 这个循环，其实是一个状态机

你可以把它理解成：

> 一个“AI 驱动的事件循环”


# 二、为什么说：Bash is All You Need

项目里有一句非常经典的话：

> **The model is 80%. Code is 20%.**

翻译一下就是：

* 模型已经很聪明了
* 你只需要给它“手”


## 为什么只给一个 Bash 工具就够？

因为 Bash 本质是一个“万能执行器”：

| 能力   | 示例                      |
| ---- | ----------------------- |
| 读文件  | `cat file.txt`          |
| 写文件  | `echo "xxx" > file.txt` |
| 搜索代码 | `grep -r "xxx"`         |
| 执行脚本 | `python main.py`        |
| 安装依赖 | `npm install`           |

也就是说：

> **一个 Bash = 所有工具**

模型会自己组合这些能力，完成复杂任务。


## 一个重要的转变

传统开发：

> 代码 = 逻辑

Agent 时代：

> 模型 = 逻辑
> 工具 = 能力
> 代码 = 边界


# 三、12 个 Session，其实是在搭一个“Agent 操作系统”

这个项目最厉害的地方，不是 demo，而是它的设计方式：

👉 **每一节课，只加一个能力**


## Phase 1：最小 Agent

| Session | 做了什么  |
| ------- | ----- |
| s01     | 写一个循环 |
| s02     | 加工具   |

👉 得到一个“能跑”的 Agent


## Phase 2：让 Agent 变聪明

| Session | 核心能力           |
| ------- | -------------- |
| s03     | 任务拆解（Todo）     |
| s04     | 子 Agent（隔离上下文） |
| s05     | 按需加载知识         |
| s06     | 上下文压缩          |

👉 解决一个核心问题：

> **上下文会爆炸**


## Phase 3：让 Agent 变成系统

| Session | 核心能力  |
| ------- | ----- |
| s07     | 任务持久化 |
| s08     | 后台执行  |

👉 从“函数调用”变成“系统”


## Phase 4：多 Agent 协作

| Session | 核心能力           |
| ------- | -------------- |
| s09     | 分工             |
| s10     | 通信协议           |
| s11     | 自主抢任务          |
| s12     | 目录隔离（Worktree） |

👉 最终形态：

> 一个“Agent 团队”


# 四、这个项目真正教你的 4 件事


## 1️⃣ Loop 才是核心

Agent ≠ Prompt
Agent = **运行时系统**


## 2️⃣ Tool 决定能力边界

你不是在写代码，而是在定义：

* 它能做什么
* 它怎么做


## 3️⃣ Context 是资源

不是越多越好，而是要管理：

* 压缩
* 分层
* 按需加载


## 4️⃣ Agent 本质是系统

当你走到 s07 以后，你会发现：

* 有任务
* 有状态
* 有调度

这已经不是函数了，而是：

> **一个轻量操作系统**


# 五、为什么这个项目值得看

很多人用 Claude Code / Cursor：

> 觉得很强，但不知道它在干嘛

这个项目做了一件很关键的事情：

> **把 Agent 从“黑盒”拆成“透明结构”**

你不需要读几万行源码，只需要：

* 50 行理解 Loop
* 每一节理解一个能力


# 总结

如果用一句话总结：

> **LLM 本身已经是 Agent，你只是给它一个身体。**

你要做的事情其实只有三件：

* 给它工具
* 给它循环
* 别挡它


# 项目地址

GitHub：
[https://github.com/shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)

在线学习：
[https://learn.shareai.run/zh/](https://learn.shareai.run/zh/)


> **Bash is all you need.
> The model is the agent.**

