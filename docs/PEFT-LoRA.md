---
title: PEFT / LoRA（参数高效微调）
created: 2026-04-14
last_updated: 2026-04-14
status: 草稿
confidence: 共识
tags: [LLM, PEFT, LoRA, Adapter, 微调]
sources:
  - 02-Areas/LLM/大型语言模型从0到1白皮书v2.md
---

> PEFT 是企业微调 LLM 的默认范式。它冻结基础模型全部权重，只训练不到 1% 的新增参数，以 Adapter 的形式产出——由此打开了"多阶段、多任务、多版本"的工程管理空间。

## 核心思想

> **冻结基础模型（Base Model）的全部权重，仅引入并训练少量（通常 <1%）的新增参数，使模型在不破坏原有能力的前提下，学习新的行为或知识。**

**LoRA（Low-Rank Adaptation）** 是当前最主流的 PEFT 实现。

## 为什么企业几乎一定用 PEFT

企业面对的核心约束不是"能不能训练"，而是**成本、风险、可管理性**：

- **成本**：全参数微调需要与基础模型同量级的算力，PEFT 只需一小部分。
- **风险**：冻结原权重意味着不会破坏基础模型已有能力。
- **可管理性**：Adapter 文件轻量（MB 级），便于版本管理、独立发布、按需组合。

## 训练时：改变了什么 / 不变的是什么

| | 状态 |
|---|---|
| 新增的 LoRA/Adapter 参数 | **训练** |
| 基础模型原始权重 | 冻结（不变） |
| Tokenizer | 不变 |
| 核心 Config | 不变 |

## 交付物：Adapter 文件

产出不再是"一个完整的新模型"，而是一个轻量适配器文件（例如 `adapter_model.safetensors`）。

工程语义：
- **基础模型** = 能力地基
- **SFT Adapter** = "说话方式"插件
- **Safety/Preference Adapter** = 安全合规插件
- **Reasoning Adapter** = 推理能力插件（见 [[推理训练-CoT]]）
- **Production Adapter** = 聚合以上、面向业务的生产版本

## 多 Adapter 的组合与上线

上线时在 Model Registry 记录组合关系：

```
Base Model @ version X
+ SFT Adapter @ version A
+ Safety Adapter @ version B
+ Prod Adapter @ version C
```

这种显式记录使得"哪个版本的模型对外服务、由谁负责"成为可审计事实。上线阶段的关键不再是技术，而是**责任归属**——训练管线的终点是 Checkpoint，发布管线的终点是"被允许对外使用、并有人负责的模型资产"。

## Related Pages

- [[SFT-有监督微调]] — PEFT 最常见的应用阶段
- [[Alignment-对齐]] — PEFT 产出的 Safety/Preference Adapter
- [[推理训练-CoT]] — Reasoning Adapter 的来源
- [[LLM训练四阶段总览]] — PEFT 如何串起整条工程链路
