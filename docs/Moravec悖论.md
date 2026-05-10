---
title: Moravec 悖论（莫拉维克悖论）
created: 2026-04-16
last_updated: 2026-04-16
status: 草稿
confidence: 共识+专家观点
tags: [AI, 机器人, 认知, Moravec, 具身智能]
sources:
  - 02-Areas/LLM/133. 对谢赛宁的7小时马拉松访谈：世界模型、逃出硅谷、AMI Labs、两次拒绝Ilya、杨立昆、李飞飞和42.md
  - 02-Areas/LLM/121. 对DeepMind谭捷的访谈：机器人、跨本体、世界模型、Gemini Robotics 1.5和Google.md
---

> Hans Moravec 1980 年代提出：**人类觉得难的（下棋、证明定理），机器做得好；人类觉得简单的（抓杯子、识别物体、走路），机器做不了**。在 LLM 时代这个悖论反而更显性——越是"听起来炫技"的任务 AI 越先做到，越是"人人都会"的能力 AI 越差。

## 原始论述

<!-- confidence: 共识 | 来源：Moravec 1988《Mind Children》 -->

> "It is comparatively easy to make computers exhibit adult level performance on intelligence tests or playing checkers, and difficult or impossible to give them the skills of a one-year-old when it comes to perception and mobility."

进化论解释：感知运动能力是 **5.3 亿年**自然选择的产物，占据大脑绝大部分硬件；而下棋、数学、逻辑只是 **最近几千年**人类文明的薄薄一层 GUI。AI 容易搞定"新皮层能力"，难以搞定"古老小脑能力"。

## LLM 时代的再印证

<!-- confidence: 专家观点 | 来源：谢赛宁 2026-03 访谈 -->

| 任务 | 人类难度 | AI 难度 |
|---|---|---|
| IMO 金牌 / 下围棋 / 写代码 | 需要训练多年的人类专家 | 已突破 |
| 把杯子放到桌子边缘不掉 | 任何三岁小孩 | **仍未解决** |
| 理解"为什么四条腿的猫比三条腿的猫常见" | 人人都会 | **仍未解决** |

Moravec 悖论的本质：AI 容易搞定**已经被语言/符号压缩好的任务**，难以搞定**未经压缩的连续物理世界**。见 [[世界模型-WorldModel]]。

## "松鼠的智能"——Sutton 的锐评

<!-- confidence: 专家观点 | 来源：Richard Sutton -->

> "能打造出一只松鼠的智能才是难的问题。一旦你有了一只松鼠——它有 goal、intrinsic reward、知道饥饿、有 emotion、有社群活动——后面写 code、上火星都是再容易不过的事情。"

对 "LLM 拿 IMO 金牌已经很厉害" 叙事的反驳：

- IMO 金牌只在人类自大视角下算"难题"
- 站在 5.3 亿年演化尺度看，**重新造一只松鼠** >> **最后 8 秒里人类文明造出的所有东西**
- LLM 让这种"人类中心主义"的评估更具误导性——它在我们自认为困难的事情上一骑绝尘，但离真正的智能仍然很远

## 悖论在机器人内部还在分层

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

Moravec 悖论不仅在 "AI vs 人类" 之间成立，在**机器人内部**也继续分层：

| 子任务 | 人类难度 | 机器人难度 | 现状 |
|---|---|---|---|
| 跑、跳、走 | 幼儿即会 | 传统控制论需要 PhD 级数学 | **已解决**（[[Sim-to-Real]] + RL） |
| 抓起一个杯子放到桌边不掉 | 幼儿即会 | 需要接触物理 + 视觉 + 力反馈 | **未解决** |
| 叠衣服、拧瓶盖、插 USB | 任何大人 | 需要灵巧手 + 触觉 | **未解决** |

谭捷的观察：**locomotion 相对容易（刚体 + 简单接触），manipulation 是所有仿真难点的交集**——这是 Moravec 悖论的延续。机器人从 "不会跑" 到 "跑得比人快" 只用了 5 年；从 "不会叠衣服" 到 "能叠衣服" 可能还要 10 年。见 [[具身智能-EmbodiedAI]]。

## 为什么这个悖论在生成式 AI 时代更显性

- 互联网数据堆满了"难任务"的答案（数学题、代码、论文），方便 LLM 通过压缩拿到
- 但**物理世界的连续动力学**从未被大规模数字化记录过——没有"桌面上的杯子受力分析"被写下来
- 解法路径：**绕开语言**，直接从视频、多模态数据建模 P(X|Y)——见 [[Bitter-Lesson]] 和 [[JEPA-联合嵌入预测架构]]

## Related Pages

- [[世界模型-WorldModel]] — 松鼠智能所需的核心组件
- [[Bitter-Lesson]] — 为什么绕开语言才是 endgame
- [[多模态融合-生成理解割裂]] — 视觉为什么没有 GPT 时刻（Moravec 悖论的当代版）
- [[NTP的本质缺陷]] — 语言压缩的局限
- [[具身智能-EmbodiedAI]] — locomotion vs manipulation 的工程现状
- [[Sim-to-Real]] — locomotion 被 RL 打穿的路径
