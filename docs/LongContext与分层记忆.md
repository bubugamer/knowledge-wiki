---
title: Long Context 与分层记忆
created: 2026-04-14
last_updated: 2026-04-15
status: 草稿
confidence: 专家观点
tags: [LLM, LongContext, 记忆, 架构, Multi-Agent]
sources:
  - 02-Areas/LLM/102. 和张祥雨聊，多模态研究的挣扎史和未来两年的2个"GPT-4时刻".md
  - 02-Areas/LLM/115. 对OpenAI姚顺雨3小时访谈：6年Agent研究、人与系统、吞噬的边界、既单极又多元的世界.md
visibility: public
---

> **Long Context**（长上下文）≠ **Long-term Memory**（长期记忆）。主流做法是把 context window 做大，但"信息装得多"和"记忆层级化"是两回事。本页收录相关核心概念：**分层记忆**、**大海捞针误区**、**冯诺依曼 memory hierarchy**、**注意力转移**。

## 根本问题：Transformer 不做压缩

Transformer 的 context 大小**随数据增长等比例增长**，不做压缩或裁减。

**人类不是这样**——记忆是分层的：

| 层级 | 时长 | 特征 |
|---|---|---|
| **短期记忆**（Working Memory） | 2–4 秒 | 精确无损，但维持极短 |
| **中期记忆** | 几秒–几星期 | 会延迟、会遗忘、善于抓重点，反复刺激可增强 |
| **长期记忆** | 终身 | 反复刺激后固化（"相当于固化到参数里"） |

Transformer 只有一种——**过长的短期记忆**，既不裁、不压缩、不分层，越长越涣散。

> "压缩产生智能。信息不经过加工压缩，无法产生智能。"（张祥雨）

## 大海捞针（Needle-in-Haystack）benchmark 的误区

这类 benchmark 考 retrieval——在长文档里藏一句话然后问。倒逼模型学到错误 bias："我一点都不能忘"。

**必要非充分条件**——能找到第 437 页第 3 段 ≠ 读懂这本书。两位专家从不同角度殊途同归：
- 张祥雨（架构角度）：大海捞针倒逼"不压缩"的错误 bias
- 姚顺雨（评估角度）：retrieval 类 benchmark 被误当成 long memory 的充分条件

## 冯诺依曼 Memory Hierarchy

<!-- confidence: 专家观点 | 来源：姚顺雨 2025-09 访谈 -->

冯诺依曼《The Brain and the Computer》中的核心洞见：

> "**Essentially, environment is always the most outer part of the memory hierarchy.**"

所以 Long Context 不是"记忆问题"的唯一解——把记忆外化到环境也算记忆的一层。四条路径其实是同一问题的不同实现：

| 路径 | 本质 |
|---|---|
| Long Context | 把所有记忆塞进 working memory |
| RAG | 在向量库这一层做 memory |
| MCP | 在外部 SaaS 这一层做 memory |
| 持续学习 | 把记忆内化进权重 |

## 注意力转移：分层记忆的工程方案

人类查书的动作——"脑中有大概印象 → 翻到某段 → 仔细看几页"——本质是**注意力转移（Context 转移）**：从全局注意力切换到局部，局部由全局注意力引导。

张祥雨提出的工程方案：**Plan LM + Execute LM 两模型协作**
- Plan LM：短 context，看 high-level 架构，决定"读哪一段"
- Execute LM：只拿到 Plan 摘要过的局部 ctx，做具体推理
- 思维链长度从"几千万 token"压到 log N 级；可端到端 RL 训练

## 为什么 Linear Transformer 不是解

试图用 RNN 替代 Attention 的各种变体（Linear Transformer / Mamba 等）不是本质突破——建模 long context 的真正难点**不在架构**，而在"有没有分层压缩机制"。

> "架构不重要，它服务于算法。有什么样的算法，做什么样的架构。"（张祥雨）

## 相关页面

- [[RAG-检索增强生成]] — "塞 Context" 的企业级替代；记忆外化的一种
- [[自主学习与在线学习]] — 无限长动态序列是自主学习的前置
- [[推理训练-CoT]] — Meta-CoT 与 Plan+Execute 的协作精神相通
- [[OpenAI五级智能分类]] — Memory 是 L4 Innovator（姚顺雨视角）的前置
