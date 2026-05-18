---
title: ReAct — 推理与行动统一的 Agent 架构
created: 2026-04-15
last_updated: 2026-04-15
status: 草稿
confidence: 共识
tags: [Agent, ReAct, 架构, Tool Use]
sources:
  - 02-Areas/LLM/115. 对OpenAI姚顺雨3小时访谈：6年Agent研究、人与系统、吞噬的边界、既单极又多元的世界.md
visibility: public
---

> ReAct（**Rea**soning + **Act**ing）= 让模型**交替产生"思考"和"动作"**的 Agent 架构。姚顺雨 2022 年提出。今天主流 Agent（OpenAI function calling、Anthropic tool use、Cursor、Devin）几乎都是 ReAct 变体。

## 最小定义

```
循环 {
   Thought:      模型用自然语言推理"我应该做什么"
   Action:       模型选一个工具并给参数
   Observation:  环境返回结果 → 喂回下一轮
}
```

只是一个 prompt loop——没有精巧的 graph、规划器、子模型协作。

## 它解决了什么

### 纯推理 vs 纯行动 都不够

ReAct 之前做语言 Agent 有两种思路，都失败：

| 路线                  | 问题                                   |
| ------------------- | ------------------------------------ |
| **纯推理（CoT）**        | 模型自己想但不能调工具 → 需要查事实时就编造（hallucinate） |
| **纯行动**（直接从语言映射到动作） | 没有中间思考 → 遇到新环境直接懵                    |

ReAct 的关键是把两者**交织**：思考决定调什么工具，工具结果又修正下一步思考。

### 自由动作空间

BERT 时代把语言任务建模成"选择题"。但 Agent 的动作空间是开放的——不是"上/下/左/右"，而是"用金色钥匙打开第三个房间"。只有 GPT 这种生成式模型才能产出自由动作。

## 为什么看起来太简单但没被取代

- **模型越强 ReAct 越能干** — 工具调用的"选择能力"和"思考质量"都是模型能力的副产品
- **可端到端 RL 训练** — 现代 function calling 用 RL 训练"何时调哪个工具"，但 outer loop 仍是 ReAct
- 更花哨的 Multi-Agent / Workflow 架构在特定任务更好，**最通用**的仍是 ReAct

## 与"Agent 应用"的代际

| 代际      | 工具调用机制                | 代表                                  |
| ------- | --------------------- | ----------------------------------- |
| 第一代     | Prompt engineering 激发 | LangChain 时代                        |
| 第二代     | RL 训练调用时机             | OpenAI / Anthropic function calling |
| 第三代（未来） | 自主学习                  | L3 Agent                            |

前两代都是 ReAct 结构，区别在工具调用是 prompt 还是 RL 训出。

## 相关页面

- [[Agent三阶段演变]] — ReAct 是第三代 Agent 的起点
- [[推理训练-CoT]] — ReAct 的"Thought"那一步与 CoT 是同一思想
- [[Code-AI的Affordance]] — ReAct 的"Action"需要好的动作空间，code 是最好的
- [[OpenAI五级智能分类]] — ReAct 支撑的是 L2 Reasoner 级应用
