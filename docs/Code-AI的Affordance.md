---
title: Affordance — 为什么 Code 是 AI 的"手"
created: 2026-04-15
last_updated: 2026-04-15
status: 草稿
confidence: 专家观点
tags: [Agent, Coding, 环境, Affordance, 概念]
sources:
  - 02-Areas/LLM/115. 对OpenAI姚顺雨3小时访谈：6年Agent研究、人与系统、吞噬的边界、既单极又多元的世界.md
visibility: public
---

> **Affordance**（可供性）= 环境提供给智能体的行动可能性（心理学 / HCI 概念）。姚顺雨把它借到 AI 领域——**code 是 AI 最重要的 affordance**，因为它是世界上唯一一种"为机器而非为人设计的接口"。

## 类比：手之于人

- 人的核心 affordance 是**手**，因为人能制造"手能用的工具"（锤子、笔、筷子）
- 物理世界几乎所有工具都为"手能抓握"而设计

类比数字世界：

> "对于 AI 或 digital agent 来说，最重要的 affordance 就是 code。其他 affordance（网页、小说、图像）都是给人定义的，只有 code 是自然给机器定义的。"

## 广义的 Code

不只是写 Python。任何**通过结构化接口与数字世界交互**的能力都算：

- 调 API（function calling）
- 写 SQL 查数据库
- 配置 K8s YAML
- 写 Terraform
- MCP / 工具调用

所以"Coding Agent" 的外延 ≈ "所有能通过 code-like 接口操作数字世界的 Agent"。

## API vs GUI：车与路之争

最终的 AGI 是基于 code/API 的，还是基于 GUI 的？姚顺雨的类比：

> "你想改造车能适应所有路，还是改造路去适应车？"

她的判断：**meet in the middle，但 mix**。
- 让一个 Agent 既会 code 又会 screenshot/frontend 不难
- 让世界为每个事情造 API 比让 Agent 学 GUI 更难
- 所以 code 永远重要，但 GUI Agent 也会出现

## 为什么 Code 天然好训

Code 满足 [[下半场-任务与Reward设计]] 的 Reward 三原则：

| 维度   | Code            | 自然语言/GUI       |
| ---- | --------------- | -------------- |
| 接口对象 | 机器              | 人              |
| 反馈机制 | 编译器 / 测试用例 — 客观 | 人评分 — 主观 noisy |
| 可验证性 | 通过测试 = 通过       | 见仁见智           |

这是为什么 math/coding 先成为 RL 训练成功的领域。

## 相关页面

- [[Agent三阶段演变]] — Code 是第三代 Agent 能 work 的环境
- [[下半场-任务与Reward设计]] — Code 天然满足 Reward 三原则
- [[REACT-推理与行动架构]] — ReAct 在 coding 环境效果最好
- [[RAG-检索增强生成]] — 另一种把外部环境暴露给模型的接口
