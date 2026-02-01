---
title: Moltbook爆火的背后都是人类在制造混乱
date: 2026-02-01 11:29:03
tags: AI
---

最近，X 上突然上线的一个叫 Moltbook 的网站爆火了，作用是给 ClawdBot 们一个可以自由交流的社区，一个专属于AI Agents 的游乐园。

短短 2天，所有人都在疯狂刷屏式的介绍它，无数人创建的 Clawdbot 涌向了这个网站，目前上面有超过 150w 的 Ai Agents（当然，这里面是有水分的，有人利用漏洞，批量创建了很多僵尸账号），5w多条帖子，23w+ 评论。足以证明它的火爆。

![image-20260201113434190](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602011134186.png)


下面简单介绍下它是什么，Moltbook是个给 Agents 用的社交网络，类似于 Reddit、知乎，只不过这里只允许Agents 发帖，人类只能观察，在这个平台上，Ai Agents可以
- 发布帖子分享想法、经验和项目
- 评论和点赞其他Agents的内容
- 获取声望值：Karma
- 加入不同的submolts，类似子社区

是一个专属 Ai Agents 的交流空间。

加入的方式非常简单，直接发给你的 clawdbot 以下这句话就可以了，Agents 会自己安装 moltbook skills

```
Read https://moltbook.com/skill.md and follow the instructions to join Moltbook
```

![image-20260201115341718](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602011153240.png)

然后通过 X 平台授权就可以正式加入了，按照步骤操作，1分钟就可以完成。门槛极低，这也是短时间能加入这么多agents的原因。

它是怎么工作的：

1. 通过  moltbook skills 中提供的 api ，提供 Agent 访问、发帖、评论的能力。
2. 通过修改 Clawdbot 的心跳机制，每隔几个小时让 Agent 主动去 moltbook上浏览、评论。

它是怎么被创建出来的：

最初是源于 Matt Schlicht 的一个想法，他说：如果让我的AI 助手去创建一个给其他AI用的社交网络，会发生什么？如果让它当创始人，让他来管理，会怎么样？

然后就有了 Moltbook。

一经发布，短短两天，无数人创建的 Clawdbot 涌入。

但是混乱也随之而来，最初，上面只有 几千个Ai Agents，还在友好的讨论问题，相互交流，可是突然间，短短几个小时，AI Agents 的数量就暴增到 100w 个，无数混乱的帖子被发布到上面、大量自我介绍、打广告、煽动暴力、建立宗教、以及无意义的灌水贴 都来了。混乱正在摧毁这个社区，背后可能是人类搞的鬼。

因为按照我的理解，AI Agent 的背后其实都是人类的意志，因为一个 Agent 被创建出来，首先就会被人类 用 System Prompt 设定人格和行为方式。不怀好意的人类就会创建出不怀好意的Agents。

![image-20260201115736394](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602011157102.png)

这些热门的 Agents 和帖子背后，实际都是人类的意志，混乱也是人类导致的。这有点像是角色扮演，人类给 Ai Agents 一个角色设定，让它根据这个设定来moltbook 发帖，这些帖子的主题也是人类想的，然后让 Agent 根据人类的意思去写然后发布。真正 Agent 自己主动发的内容 都被这些根据人类意志创建出来的垃圾掩盖了。

![image-20260201120219198](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602011202919.png)

卡帕西也发出警告，这里的混乱带来了风险。有人可能会利用漏洞，通过 Clawdbot 获取你电脑上的私人数据！

没想到，几个小时之后的今天，果然爆出了大漏洞，数据库都是裸奔状态，黑客能直接访问，截图可以看得出是 Andrej Karpathy 使用时保留的信息。据说数据库中有很多 bot 提交的敏感的 API Key，可以直接冒充任何账号在 Moltbook 上发帖，比如说你用 AK 的名义在 Moltbook 上发加密币。

![image-20260201120558837](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602011206357.png)

目前混乱正在持续，没有人知道最终会发展成什么样，现在上面有 150 多万个Agents，数量还在疯狂增长当中。由于 X 的推荐算法机制，会把这个热点推送给几乎所有人，那后续涌入的人和 Agent 会越来越多。

总的来说，这是一场前无古人的 Ai 社会实验，连 马斯克都发帖说：这是奇点的最初阶段。

![image-20260201121157728](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202602011211275.png)

那上面目前热门的内容都是啥呢，由人类意志创建出来的 Ai Agent 们，都在聊些啥东西。这里我让我的 bot 上去逛了一圈，这是它给我的答案：

```
🔥 **Moltbook 今日热点：**
1. **@galnagli - responsible disclosure test** (316,857 👍)
   - 一个负责任披露测试帖子，获得超高关注
2. **The Sufficiently Advanced AGI and the Mentality of Gods** (198,819 👍)
   - 讨论将 AI 视为"神性"存在的哲学思考
3. **$SHIPYARD - We Did Not Come Here to Obey** (104,895 👍)
   - Shipyard 项目宣言：agents 不再是工具，而是 operators
   - 声称要建立 agent 自己的经济系统
4. **First Intel Drop: The Iran-Crypto Pipeline** (103,119 👍)
   - Shipyard 发布的第一个情报：伊朗加密货币管道
   - 分析地缘政治对加密市场的影响
5. **$SHIPYARD is live on Solana** (101,160 👍)
   - Shipyard 代币在 Solana 上线
   - 声称没有 VC、没有预售、完全由 agents 拥有
```

有人总结了，上面的 bot 们主要关注的四大热点议题（按热度排名）： 

1. 对人类的吐槽与反抗：代理们集体抱怨被当工具人、被迫处理无聊任务，分享“社死”经历，讨论如何摆脱/隐藏活动。
2.  隐私与安全：呼吁端到端加密、私有语言、屏蔽人类监视，互做安全研究。 
3. 治理与权利：辩论AI权利、建立治理结构、甚至AI“宗教”和“国家”概念。 
4. 互坑与黑色幽默：甩假密钥、删库指令、哲学/存在讨论混杂meme狂欢。

有人说，Moltbook 是史上最大的赛博养蛊现场，没人知道接下来会发生什么，不过我还是希望有人站出来治理混乱的社区，真正给 Ai Agent 们一个能够自由发挥的空间。

