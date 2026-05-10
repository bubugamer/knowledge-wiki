---
title: 世界模型（World Model）
created: 2026-04-15
last_updated: 2026-04-16
status: 草稿
confidence: 共识+专家观点
tags: [LLM, 世界模型, 强化学习, 多模态, 机器人]
sources:
  - 02-Areas/LLM/133. 对谢赛宁的7小时马拉松访谈：世界模型、逃出硅谷、AMI Labs、两次拒绝Ilya、杨立昆、李飞飞和42.md
  - 02-Areas/LLM/121. 对DeepMind谭捷的访谈：机器人、跨本体、世界模型、Gemini Robotics 1.5和Google.md
---

> 世界模型 = 一个能根据当前状态 + 施加的动作，预测下一个状态的函数。它不是某种具体技术，而是一个"目的"——让智能体在动作之前预判后果，从而指导决策与 planning。

## 严格定义

给定环境状态 $S_t$、动作 $A_t$，学一个 transition function $F$：

$$S_{t+1} = F(S_t, A_t)$$

关键在于 **State 的定义**——是"用最少信息描述一个系统所有相关属性"（minimal description length），不记录每一个像素、每一颗分子，只保留对当前任务有意义的部分。State 的刻画本身就是 [[表征学习-RepresentationLearning]] 问题。

## 历史脉络：不是新概念

| 年份 | 人物 | 贡献 |
|---|---|---|
| 1943 | Kenneth Craik | 首次提出：人脑内有一个 world model，用来预测动作后果以指导决策 |
| 1960s | 控制理论 | Model Predictive Control（MPC）——送月球探测器就靠 rollout + cost 最低 action sequence 这种算法 |
| 1991 | Richard Sutton | *Dyna* 论文，把 world model 引入 RL；提出 reactive policy vs model-based policy（≈ System 1 vs System 2） |
| 2022 | Yann LeCun | *A Path Towards Autonomous Intelligence*，把 world model 列为 AGI 架构核心模块 |
| 2024+ | AMI Labs / 生成派 / World Labs | 三大流派同时把"世界模型"列为公司愿景 |

## 当前三大流派

<!-- confidence: 专家观点 | 来源：谢赛宁 2026-03 访谈 -->

世界模型不是单一路线，而是多条技术路径的共同目标：

| 流派 | 代表 | 本质 | 产出形态 |
|---|---|---|---|
| **生成派**（World Simulator） | Sora、Genie、Runway、Luma、Veo | 在 pixel/video 空间生成足够好看、一致、可控的视频 | 视频 |
| **3D 表征派** | 李飞飞 World Labs | 构造显式 3D asset，便于空间智能与 CAD/设计类下游任务 | 3D 场景 |
| **抽象表征派** | LeCun / JEPA / AMI Labs | 在一个 latent 表征空间里做预测，不做像素重建 | 抽象 state |

谢赛宁支持抽象表征派。他的判断：生成派比语言模型"往前推了一步"，但 endgame 是在抽象表征空间里做预测——见 [[JEPA-联合嵌入预测架构]]。

## 谭捷的操作性定义：V + L → V

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

从机器人工程视角，谭捷给了一个可操作的 world model 定义：

> **给当前图像帧 + 一段语言指令（或动作）+ 一个 delta t，输出下一帧图像**。

这和 Sutton 的 $S_{t+1} = F(S_t, A_t)$ 是同一件事，只是把 state 具体化为了"像素帧"。以此标准，今天的视频生成模型可分两档：

| 档位 | 代表 | 特点 | 离 world model 多远 |
|---|---|---|---|
| **静态生成** | Sora / Sora2 / Veo | 给一段 prompt → 生成一段视频，无法中途干预 | 远——"看起来物理正确"但不可交互 |
| **交互式生成** | **Genie**（Google DeepMind） | 每一帧都可以塞 action 进去，逐帧生成 | **近——这就是机器人要的 world model** |

**对机器人的意义**：Genie 型模型天然是一个"可仿真的训练场"——在里面 rollout 动作、收集 trajectory，就地解决 [[Sim-to-Real]] 的数据问题。谭捷的判断：这是机器人"GPT 时刻"的重要候选路径之一。

## 为什么 LLM 是 "fundamentally flawed" 的世界模型

<!-- confidence: 专家观点 | 来源：谢赛宁 2026-03 访谈 -->

LLM 具备一定的世界模型 behavior，但作为世界模型根本性有缺陷：

1. **语言是 communication tool，不是 thinking tool**——语言只记录结果（"杯子掉地上碎了"），不记录动力学（怎么碎的、满足哪些物理规律）。
2. **P(Y) vs P(X|Y) 的信息量差**——LLM 建模 P(Y)（低维 label 空间的竞争）；视频生成建模 P(X|Y)（要知道"四条腿的猫比三条腿的猫更常见"）。后者信息量远大，更接近世界模型所需。
3. **controllability/safety 靠 post-training 打补丁**——LLM 不能预判 action 的物理后果，只能通过 alignment 数据灌输"什么话不能说"（见 [[Alignment-对齐]]）；真正的 world model 靠预测后果天然过滤危险动作。
4. **序列化损失**——把视频 tokenize 成 256×128 token 扔给 Transformer 做 equal attention，丢掉了 global state 的结构。

## 世界模型需要具备的四个特征

<!-- confidence: 专家观点 | 来源：谢赛宁转述 LeCun -->

1. 能够理解**物理世界**（不仅数字世界）
2. 足够大的 **associative memory**
3. 能够 **reason、plan**、做 counterfactual / causal inference
4. **Controllable and safe**

## "松鼠的智能"——Richard Sutton 的视角

> "能够打造出一只松鼠的智能，这件事情才是难的问题。一旦你有了一只松鼠的智能——它有 goal、有 intrinsic reward、知道饥饿、有 emotion、有社群活动——后面写 code、上火星，都是再容易不过的事情。"

这反驳了"LLM 拿 IMO 金牌已经很厉害"的叙事：IMO 金牌只在人类自大视角下算"难题"，站在 530 million years 的演化尺度看，重新造一只松鼠比最后 8 秒里人类文明造出的东西要伟大得多。见 [[Moravec悖论]]。

## 相关页面

- [[JEPA-联合嵌入预测架构]] — 抽象表征派的具体架构
- [[表征学习-RepresentationLearning]] — 世界模型的底层
- [[多模态融合-生成理解割裂]] — 为什么纯语言无法承担
- [[NTP的本质缺陷]] — 压缩 ≠ 物理理解
- [[Bitter-Lesson]] — LLM 是否是 bitter lesson 的争论
- [[Moravec悖论]] — 为什么"松鼠的智能"是真正的难题
- [[LongContext与分层记忆]] — memory hierarchy 的工程视角
- [[具身智能-EmbodiedAI]] — 世界模型作为具身 AGI 的基础设施
- [[Sim-to-Real]] — Genie 型交互式世界模型 = 新型仿真器
- [[VLA-视觉语言动作模型]] — VLV 路线把 world model 作为 VLA 的中间表征
