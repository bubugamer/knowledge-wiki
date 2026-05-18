---
title: OpenAI 五级智能分类
created: 2026-04-14
last_updated: 2026-04-15
status: 草稿
confidence: 共识+专家观点
tags: [LLM, AGI, Agent, OpenAI, 路线图]
sources:
  - 02-Areas/LLM/102. 和张祥雨聊，多模态研究的挣扎史和未来两年的2个"GPT-4时刻".md
  - 02-Areas/LLM/115. 对OpenAI姚顺雨3小时访谈：6年Agent研究、人与系统、吞噬的边界、既单极又多元的世界.md
visibility: public
---

> OpenAI 官方提出的 AGI 路线图，从 Chatbot 到 Organization 五级。读访谈常会遇到"L2/L3 Agent"这类说法，本页给出每级的最小定义与读图要点。

## 五级定义（OpenAI 官方）

| 级别 | 名称 | 含义 |
|---|---|---|
| L1 | **Chatbot** | 对话助手 |
| L2 | **Reasoner** | 能做复杂推理 |
| L3 | **Agent** | 能独立完成工作 |
| L4 | **Innovator** | 能做出发明创新 |
| L5 | **Organization** | 能运营整个组织 |

## 每级对应的算法范式

<!-- confidence: 专家观点 | 来源：张祥雨 2025-06 访谈 -->

张祥雨的解读：每一级背后都是一次全新算法范式的产生，而不是能力的渐进提升。

| 级别 | 核心算法 | 代表模型 |
|---|---|---|
| L1 Chatbot | Next Token Prediction（见 [[NTP的本质缺陷]]） | GPT-3 / ChatGPT |
| L2 Reasoner | Rubix RL + Meta-CoT（见 [[推理训练-CoT]]） | o1 / o3 / DeepSeek R1 |
| L3 Agent | 自主 / 在线学习（见 [[自主学习与在线学习]]） | （未出现） |
| L4 / L5 | 更远未来，算法断点尚不清晰 | — |

## 两种"Agent"的术语混用

最容易误读的一级。读文献时要区分：

| 层面 | "Agent" 的含义 |
|---|---|
| **L3 算法意义的 Agent** | 自主搭环境 + 内生奖励 + 边用边进步 |
| **今天市面上的 Agent 应用** | LangChain / function-call pipeline，本质仍是 **L2 Reasoner 的上层应用** |

今天的 Agent 产品（包括 Cursor、Manus、Operator）都没有：自主环境扩展 / 内生奖励 / 训练完继续进步——所以都不是 L3。

## L4 / L5 的关系：姚顺雨的并列解读

<!-- confidence: 专家观点 | 来源：姚顺雨 2025-09 访谈 -->

L1 → L2 → L3 是单向依赖链，但 **L4 与 L5 是正交并列的两个方向**：

| 级别 | 核心能力 | 人物类比 |
|---|---|---|
| **L4 Innovator** | 长期记忆 + 内生奖励 | 爱因斯坦、梵高、贝多芬 |
| **L5 Organization** | Multi-Agent 协作与扩展 | 乔布斯、马斯克 |

> "谁是 Level 4 谁是 Level 5 我不确定，但这两件事显然是下一步需要做的。"

## 读图注意：两位专家对 L3 的定义分歧

两位专家都认同"当前 Agent 应用离真正的算法级 Agent 有差距"，但**标签分法不同**：

| 维度 | 张祥雨视角 | 姚顺雨视角 |
|---|---|---|
| 自主学习放在哪级 | L3 必要条件 | L4 Innovator 的实现 |
| 当前 Cursor / Manus | 仍是 L2 应用层 | L3 早期形态 |
| Multi-Agent | L3+ 的延伸 | L5 Organization 的核心 |

看到"现在已经是 L3 了 / 现在还不是 L3"这种话时，先分清楚对方用的是哪一套定义。

## 相关页面

- [[自主学习与在线学习]] — L3（张）/ L4（姚）的核心算法
- [[推理训练-CoT]] — L2 Reasoner 的核心算法
- [[NTP的本质缺陷]] — L1 Chatbot 的局限
- [[Agent三阶段演变]] — Agent 概念从符号主义到 LLM 的演变
- [[REACT-推理与行动架构]] — 当前 Agent 应用的架构底座
- [[LongContext与分层记忆]] — Memory 是 L4 Innovator 的前置
- [[LLM训练四阶段总览]] — 训练演进的另一种视角
