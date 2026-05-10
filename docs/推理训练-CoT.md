---
title: 推理训练（CoT / Meta-CoT）
created: 2026-04-14
last_updated: 2026-04-15
status: 草稿
confidence: 共识+专家观点
tags: [LLM, 推理, CoT, Meta-CoT, O系列]
sources:
  - 02-Areas/LLM/大型语言模型从0到1白皮书v2.md
  - 02-Areas/LLM/102. 和张祥雨聊，多模态研究的挣扎史和未来两年的2个"GPT-4时刻".md
---

> 推理训练 = 通过显式的中间思考步骤降低回答方差。本页收录：**CoT**、**Meta-CoT**、**Outcome vs Process Supervision**、**动作空间压缩**、**Pattern is all you need**。

## CoT（Chain of Thought）

让模型显式生成中间思考步骤把复杂问题分解。关键认知：

> CoT 并非提升"智商上限"，而是**降低回答方差**——不是更聪明，而是更稳。

### 为什么必须有 CoT：NTP 的单步复杂度上限

Transformer 做一次前向推理的计算复杂度是 `O(n)`。复杂度高于 `O(n)` 的问题（大数乘法 `O(n log n)` 或 `O(n²)`）原理上就不可能在一个 token 内完成。

**CoT 的本质作用**：把单步超限的问题，拆成一串每步都在复杂度内的子步骤。详见 [[NTP的本质缺陷]]。

## Outcome Supervision vs Process Supervision

两种 CoT 训练数据的监督强度：

| 类型 | 做法 | 成本 | 适用 |
|---|---|---|---|
| **Outcome Supervision**（主流） | SFT 数据里加入 CoT 范例，让模型模仿分步格式 | 低 | 绝大多数企业场景 |
| **Process Supervision**（研究级） | 对每一步都人工标注和监督 | 极高 | 前沿研究、过程可靠性要求极高 |

## Meta-CoT（思维链的思维链）

<!-- confidence: 专家观点 | 来源：张祥雨 2025-06 访谈 -->

O 系列的核心突破。普通 CoT 是一条直线思路；Meta-CoT 允许模型在**多个 CoT 模式之间切换、回退、重试**。

### 为什么需要 Meta-CoT

即便做 Rubix RL，某些题目正确率卡在 60% 上不去。原因：在**关键决策点（Critical Decision）** 有两个分支，选哪条的复杂度**超过单 token 判断上限**。人类也无法"算出来前就知道哪条对"——但人可以试错回溯。

### 常见反思 pattern

O 系列通过**特定数据注入"反思 pattern"**扩展动作空间：
- 反思（wait / I realize...）
- 验算（alternative verification）
- 大循环（推翻前面从头来）
- 审题（反复比对题目要求）

### Pattern is all you need

> "做 O 系列或思考模型，本质就是 pattern is all you need。"

真正差别不在 RL 算法（PPO / GRPO / reinforce++ 差别不大），而在**思维链的组织模式**。

## Action Space Compression（动作空间压缩）

<!-- confidence: 专家观点 | 来源：张祥雨 2025-06 访谈 -->

解答一个数学题可能有几千 token，看似搜索空间是 `词表^几千`——传统 RL 无法处理。但：

- **预训练已把动作空间极度压缩**：4000 token 的解题过程里真正影响结果的关键决策点通常**不超过 10 个**
- 其他 token 几乎被前文"决定"，自动输出
- RL 的真实任务是：**把这 10 个关键 token 选对**

这解释了两个现象：
1. 语言模型上 Rubix RL 很早就见效（很多题随机通关率不低）
2. MCTS / PRM 在语言模型上效果不明显——搜索空间本来就不大

**反面**：反思 pattern **被预训练过度压缩**——语料里反思数据稀少，RL 自己很难激发，必须人工注入。

## 跨领域泛化：为什么 O 系列能"举一反三"

只在数学上做过 RL 的 O-like 模型，做古诗词格律也能激发同样的思考 pattern（打草稿 → 检查 → 替换 → 推翻重来）。原因：反思、验算这些 pattern 在预训练语料中**虽稀疏但广泛分布**（Stack Overflow 高赞答辩、学术讨论），RL 激发它们时顺带激活了各领域知识。

反例：纯数学 O-like 做不了博弈题（斗地主）——博弈需要 `minmax` pattern，纯数学语料中没有。

## 相关页面

- [[NTP的本质缺陷]] — 为什么必须用 CoT 绕开单步复杂度上限
- [[SFT-有监督微调]] — CoT 数据常以 SFT 形式注入
- [[RLHF-vs-DPO]] — 被 O 系列超越之前的对齐主流方法
- [[PEFT-LoRA]] — Reasoning Adapter 的工程载体
- [[视觉空间推理-多模态GPT-4时刻]] — 视觉领域还缺 CoT 这一环
- [[下半场-任务与Reward设计]] — Reward 三原则解释为什么 math/coding 先成功
