---
title: 我做了一个自己的 Coding Agent CLI：nano-codin
date: 2026-03-22 19:41:00
tags:
---

# 我做了一个自己的 Coding Agent CLI：nano-codin

做 AI Coding 这件事，过去一段时间我一直更关心 workflow，而不是单次 demo。

我会长期看各种 agent、编排框架、CLI 工具，也会自己把它们接进真实开发流程里跑。但越用越明显的一点是：很多东西都能“演示会写代码”，却很难真正稳定地进入终端工作流。它们可能很聪明，也可能很炫，但一到持续修改、反复验证、上下文收敛、失败恢复这些工程细节上，就开始变得不可控。

所以我决定自己做一个。

这个项目叫 **nano-codin**。它不是为了证明 agent 能写代码，而是为了验证另一件更重要的事：**一个 Coding Agent，到底怎样才能真正进入工程工作流。**

## 为什么我要自己做 nano-codin

如果只是“让大模型帮我改几行代码”，其实市场上已经有很多选择了。

但我真正想要的，不是一个会表演的 agent，而是一个能长期待在 terminal 里的工程组件。它应该能理解 repo，先探索，再计划，再执行，再验证，最后给出结构化总结。更重要的是，它要能解释自己在做什么，为什么这么做，做错了怎么收回来。

换句话说，我想要的不是一个黑盒助手，而是一个 **可观察、可恢复、可约束、可扩展** 的最小化内核。

这也是 nano-codin 的出发点。

## 一句话介绍 nano-codin

**nano-codin 是一个基于 TypeScript、LangGraph 和 Ink 构建的 Coding Agent CLI。**

它的目标很直接：在终端里完成一条完整的 coding loop，包括代码理解、任务规划、文件修改、命令验证，以及最后的结果总结。

它不是一个 all-in-one 平台，也不是一个追求 feature list 的大而全产品。相反，我刻意把边界收得很窄，把核心做得更硬：

- 单代理 ReAct loop
- phase-aware workflow
- 显式 Tool Registry
- 分层上下文
- sandbox policy
- recovery / compression / checkpoint

我更愿意把它看成一个 **production-oriented minimal agent runtime**。

## 我想解决的，不只是“调用大模型写代码”

这类工具最容易被误解的一点，就是大家会把“会写代码”当作目标本身。

但在真实工程里，问题从来不只是生成代码。真正麻烦的是这些：

- 上下文不断膨胀，模型开始忘事
- 还没想清楚就直接改文件
- 改完以后没有验证，却直接宣布完成
- shell 命令和文件修改没有约束，任务很容易失控
- 中途报错后，整个执行轨迹无法恢复

所以我给 nano-codin 定的几条设计原则很简单：

- **small core**
- **explicit state**
- **safe execution**

比起“再接一个酷炫能力”，我更在意状态是不是显式的，动作是不是可审计的，失败之后能不能继续跑。

## nano-codin 的核心能力

从实现上看，nano-codin 现在已经具备了一条比较完整的最小闭环。

### 1. ReAct 单代理循环

核心执行模型仍然是经典的 ReAct：`Thought -> Action -> Observation`。但我没有把它停留在 prompt pattern，而是把它放进了 LangGraph 的状态图里，让 agent 的状态、步数、phase、recovery history 都有明确归属。

### 2. Phase-aware workflow

我把任务过程拆成了五个阶段：

`discover -> plan -> execute -> verify -> finalize`

这件事看起来很朴素，但它直接解决了很多“玩具 Agent”最常见的问题。尤其是 discover 和 execute 被明确分开之后，agent 不会刚看两眼 repo 就立刻开始乱改。

### 3. Tool Registry

工具层被收敛成一个显式 registry，目前分成四类：

- `fs`: `ls`、`tree`、`grep`、`repo_index_query`、`read_context`
- `edit`: `view`、`create`、`insert`、`str_replace`
- `shell`: `bash`
- `planning`: `todo`、`delegate`、`summarize_changes`

这很重要，因为 agent 的能力边界，不应该藏在 prompt 里，而应该体现在工具协议里。

### 4. Layered context

nano-codin 不是只喂聊天记录。它会从三个层级加载上下文：

- `AGENTS.md`
- `.nanocodin/context.md`
- `.nanocodin/memory.md`

前者更像 repo 级行为约束，后两者更像项目背景和持久记忆。这样做的好处是，context 不再只有“这一轮对话里说过什么”，而是开始有结构。

### 5. Repo index / compression / recovery / delegate

这是我觉得它逐渐脱离 demo 感的关键部分：

- `RepoIndexer` 会做增量索引，支持 `repo_index_query`
- `CompressionManager` 会在上下文压力过高时压缩历史轨迹，保留最近步骤并生成结构化 session memory
- `RecoveryEngine` 会对常见错误做单步恢复，比如 schema 错误、命令不存在、测试脚本缺失
- `delegate` 支持轻量级只读子任务，把探索工作局部外包，再把结果结构化带回主流程

这些都不是最显眼的 feature，但它们决定了一个 agent 是不是能连续工作。

### 6. Provider routing

模型接入层支持 OpenAI-compatible 和 Anthropic-compatible 路由，同时支持自定义 base URL。这个设计不花哨，但它让 nano-codin 更容易放进不同团队现有的 provider 体系里，而不是强绑定单一平台。

## 这项目最关键的设计取舍

很多选择不是“不会做”，而是“故意不先做”。

### 为什么先做单代理，而不是 multi-agent

我并不反对 multi-agent，但我对它的优先级判断一直比较保守。

因为在大多数 coding task 里，先把一个 agent 的状态管理、计划约束、验证闭环和恢复机制打磨清楚，比把三个 agent 同时拉起来更重要。单代理先跑稳，才能知道哪些能力真的需要 delegation，哪些只是把问题拆得更复杂。

所以 nano-codin 现在有 `delegate`，但它仍然是以单代理主循环为核心。这是有意为之。

### 为什么优先做 CLI，而不是 GUI

Coding Agent 最自然的落点，本来就应该是 terminal。

终端里已经有 repo、shell、git、test runner、package manager。CLI 不是妥协，而是最短路径。先把 agent 放进已有工作流，比先做一个更漂亮的外壳更重要。

这也是为什么我用了 Ink 做终端 UI，而不是先去做一层 web console。

### 为什么强调 plan gate / verify gate / sandbox policy

如果一个 agent 可以直接修改文件、执行命令、最后还自己宣布“完成了”，那它默认就是不安全的。

所以我把几个 gate 做成了一等公民：

- **plan gate**: 没有 todo 列表，没有 verification goal 和 command，就不允许执行 mutating action
- **verify gate**: 对“fix / bug / implement / refactor”这类任务，如果没有跑验证，不允许直接 `final`
- **sandbox policy**: shell 命令有 `allow / ask / deny` 策略，危险命令直接拦，写操作默认需要确认

这些机制不是为了保守，而是为了让 agent 的行为接近真实工程协作。

### 为什么 repo index、session memory、checkpoint 更重要

炫技 feature 很容易吸引注意力，但真正决定可用性的，往往是那些不起眼的系统细节。

比如：

- repo index 决定它理解代码库是不是足够快
- session memory 决定它压缩上下文之后会不会失忆
- checkpoint 决定任务被打断之后能不能 `continue`

如果这些东西没有，agent 就很难从一次性演示变成可持续使用的工具。

## 架构是怎么组织的

nano-codin 的目录不复杂，但边界切得比较清楚。

### 入口装配层：`src/index.ts`

这里负责 runtime 装配：加载 `.env`、解析 runtime config、读取 context sources、初始化 repo index、组装 Tool Registry、创建 `CodingAgentGraph`，最后挂到 Ink 控制台。

它不做复杂决策，只负责把依赖拼好。

### Agent 内核：`src/agent/`

这里是系统真正的心脏。

- `agentGraph.ts` 负责 LangGraph 状态机和 agent 主循环
- `reactLoop.ts` 负责 prompt 输入输出结构、response parse、execution state formatting

也就是说，`src/agent/` 处理的是“agent 如何思考和流转”，而不是“具体干什么活”。

### Tool 层：`src/tools/`

所有能力都通过 Tool Registry 暴露，schema 用 Zod 做约束。这样工具既有统一入口，也有明确的输入验证，不需要把行为隐藏在 prompt 约定里。

这是我很坚持的一点：**能力应该被注册，不应该被暗示。**

### 横切服务：`src/services/`

这一层承载的是工程性能力：

- `configLoader`
- `contextLoader`
- `repoIndexer`
- `compressionManager`
- `recoveryEngine`
- `sessionCheckpoint`
- `agentPolicy`
- `executionSummary`

这些文件单看都不“性感”，但它们基本决定了 nano-codin 不是一个脚本，而是一个 runtime。

### Prompt 层：`src/prompts/`

prompt 不只是 system text，还包括模板化渲染和 execution-state 注入。换句话说，prompt 在这里是显式资源，而不是散落在代码里的字符串。

### 终端 UI：`src/ui/`

UI 层负责把 agent 的运行状态实时展示出来，包括 thought、action、observation、phase、todo 状态、verification 状态和最新 snapshot。它不改变 agent 逻辑，只负责把执行过程变得可见。

这就是模块边界的核心原则：**agent 做决策，tool 做动作，service 做保障，UI 做可视化。**

## 一个典型任务是怎么跑起来的

如果把 nano-codin 的执行过程压缩成一条主线，大概是这样：

```text
User Task
  -> Build Prompt
  -> Model decides Thought / Action
  -> ToolRegistry validates and executes
  -> Observation returns to agent
  -> Phase gate checks plan / verify
  -> Final summary
```

再展开一点，会看到几个关键节点：

1. 用户在 terminal 里输入任务
2. agent 组装 system prompt、trajectory、execution state、project context
3. 模型输出 `Thought / Action / Action Input`
4. Tool Registry 做 schema 校验、权限判断和实际执行
5. observation 回流到 agent state
6. 如果动作不合法，会被 phase gate 拦回 `plan`
7. 如果验证缺失，会被 verify guard 拦回 `verify`
8. 最终输出带 execution summary 的结论

这个过程中，agent 不是一路向前冲，而是不断在“生成动作”和“被工程约束修正”之间来回校准。

## 我认为 nano-codin 和“玩具 Agent”真正拉开差距的地方

如果要说一个观点最集中的地方，我会放在这里。

我觉得一个 Agent 是否进入工程世界，不看它会不会调模型，也不看它能不能改文件，而看它有没有下面这些能力：

### 1. Phase budget，防止无限探索和无效循环

`discover`、`plan`、`execute + verify` 都有独立 budget。这样 agent 不能无限读 repo，也不能一直卡在规划阶段自我循环。

### 2. Verify guard，防止“没验证就宣布完成”

这一点非常关键。很多 agent 最不靠谱的地方，不是改错了，而是没验证就说自己改对了。nano-codin 会明确阻止这种行为。

### 3. Plan gate，防止直接乱改

没有 todo，没有 verification plan，就不允许进入 mutating path。这个约束会显著降低“先动手再想”的失控概率。

### 4. Recovery / compression / checkpoint，提升连续性

能否恢复、能否压缩、能否续跑，是我判断一个 agent 是否接近工程化的重要指标。nano-codin 现在虽然还是最小实现，但已经把这三个点都放进了核心流程里。

说得更直接一点：

**一个会调用模型的 CLI，不一定是 Coding Agent。**

**但一个有 phase、gate、memory、recovery、checkpoint 的 CLI，才开始像真正能进工作流的 agent runtime。**

## 当前还不完美的地方

当然，它现在离“完整产品”还很远。

首先，nano-codin 仍然是一个最小化 CLI。它有工程骨架，但还不是完整平台。插件生态、协作能力、扩展协议、长期 memory 策略，都还在很早期的阶段。

其次，复杂任务的效果仍然高度依赖模型质量和 prompt discipline。系统可以尽量约束 agent，但不能完全替代模型本身的推理质量。

另外，当前 delegation 还是轻量级只读子任务，不是完整 multi-agent orchestration。这个边界是刻意收敛出来的，但也意味着它暂时不会覆盖所有复杂协作场景。

我反而觉得，主动承认这些限制很重要。因为工程化不是“什么都能做”，而是“知道自己现阶段该做什么，不该做什么”。

## 为什么我会继续做这个项目

nano-codin 对我来说，不只是一个 side project。

它更像一个持续演进的实验场。很多我关心的问题，其实都可以在这个项目里验证：

- Coding Agent 的最小可靠内核应该长什么样
- workflow orchestration 应该在哪一层做，做到什么程度
- memory、planning、verification 之间怎样形成稳定闭环
- 一个 agent runtime 怎么从“自己能用”走向“团队可复用”

未来我会继续往几个方向推进：

- 更强的 delegation 机制
- 更稳定的 execution policy
- 更系统化的 memory 设计
- 更清晰的 workflow 抽象

但这些演进，都会建立在现有这个小内核之上，而不是重新堆一个更大的黑盒。

## 结尾

回到最开始那个问题：既然市面上已经有很多 AI Coding 工具了，为什么我还要自己做一个 Coding Agent？

我的答案其实很简单。

因为我想验证的，不是 agent 能不能写代码，而是 **AI Coding 能不能从“会用”推进到“可复用、可规模化、可工程落地”**。

nano-codin 就是在这个问题上的一次具体实践。

它还不大，也还不完美，但至少它已经不是一个只会演示的 demo 了。它开始长出 runtime、policy、memory、checkpoint 和 verification 这些真正属于工程系统的部分。

如果你也在关注 Coding Agent、terminal workflow 或 agent orchestration，欢迎看看这个项目：

- GitHub: `https://github.com/xcxyh/nanoCodin`

后面我也准备继续写这个系列，把里面一些关键设计单独展开，比如 phase-aware loop、plan gate、verify guard、context compression，以及为什么我对“先把单代理做好”这件事这么执着。

因为在我看来，这些看起来不那么热闹的工程细节，才是 AI Coding 真正开始落地的地方。
