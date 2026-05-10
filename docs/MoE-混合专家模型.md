---
title: MoE（Mixture of Experts，混合专家模型）
created: 2026-05-09
last_updated: 2026-05-09
status: 草稿
confidence: 共识
tags: [MoE, 模型架构, 稀疏计算, DeepSeek]
sources: []
---

> 一种稀疏计算架构——模型拥有大量参数，但每次推理只激活少数几个"专家"，实现"总参数很大，实际计算量没那么大"。

## 定义

传统 Dense 模型的问题：参数越大，每次推理越贵，因为所有参数都参与计算。

MoE 的思路：把原本一个 FFN（Feed-Forward Network）拆成多个专家网络，由 Router 决定当前 token 该交给哪些专家处理。例如 DeepSeek-V3 总参数 671B，但每个 token 只激活 37B 参数。

## 工作原理

### Expert 不是完整模型

Expert 本质上通常只是 Transformer 里的 FFN 模块。MoE 不是把很多完整模型拼起来，而是把一个 FFN 拆成多个专家网络。

### Router 决定路由

Router 本身也是神经网络，学习"什么 token 更适合什么专家"。一般采用 **Top-K Routing**，只选得分最高的几个专家参与计算。

### 涌现式专业化（Emergent Specialization）

专家并不是人工定义的"数学专家""代码专家"。在长期训练中，某些专家因为持续处理特定类型的 token，自然形成专业化。这是训练过程中涌现出来的，不是预设的。

## 核心工程难题：负载均衡

如果所有 token 都偏好某几个专家，就会出现 **routing collapse（路由坍塌）**：强专家越来越强，弱专家几乎没有梯度更新。

| 方案 | 做法 | 代价 |
|---|---|---|
| 传统做法 | 增加 auxiliary loss（辅助损失）强行均衡负载 | 影响模型性能 |
| DeepSeek-V3 | Auxiliary-loss-free load balancing，用动态 bias 调节专家热度 | 避免了硬加辅助 loss 的性能损失 |

## DeepSeek 的 MoE 路线

DeepSeek 的核心策略不是"把模型做大"，而是**"如何更低成本地做更大模型"**。围绕这个目标，他们同时推进多个方向：

- **MoE** — 稀疏激活，降低推理计算量
- **MLA（Multi-head Latent Attention）** — 压缩注意力计算
- **KV Cache Compression** — 降低推理内存占用
- **FP8 训练** — 降低训练精度需求
- **通信优化** — 降低分布式训练开销

## MoE 与 RL Reasoning：行业两条并行主线

当前行业正在同时解决两个问题：

| 问题 | 解决方向 | 代表 |
|---|---|---|
| 继续扩大模型规模而不让推理成本爆炸 | MoE + 稀疏计算 | DeepSeek-V3 |
| 让模型真正具备 reasoning，不仅是语言续写 | RL + 自我演化 | DeepSeek-R1 |

DeepSeek-R1-Zero 在几乎没有 SFT 冷启动的情况下，仅通过 RL 让模型逐渐涌现出长链推理、自我反思、自我验证等行为——这说明 reasoning 不一定必须靠大量人工标注数据堆出来，可以通过 RL 逐渐自我演化。

## 常见误解

- "MoE 是新发明" — 概念来自 1991 年（Jacobs et al.），是近年工程突破（路由稳定性、负载均衡、通信优化）让它在超大规模成为可行
- "Expert 是完整的子模型" — Expert 通常只是 FFN 模块，不是独立的 Transformer
- "专家有明确分工" — 专业化是涌现的，不是预设的

## 相关页面

- [[模型架构-ModelArchitecture]] — MoE 在架构全景中的位置
- [[推理训练-CoT]] — RL reasoning 路线（DeepSeek-R1）的训练方法
- [[RLHF-vs-DPO]] — RL 在对齐和推理训练中的应用
- [[AI技术体系总览]] — 行业趋势：规模化与推理能力的双线并进
