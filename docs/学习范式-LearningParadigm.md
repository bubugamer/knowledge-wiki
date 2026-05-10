---
title: 学习范式（Learning Paradigm）
created: 2026-05-06
last_updated: 2026-05-06
status: 草稿
confidence: 共识
tags: [AI, 学习范式, 机器学习]
sources: []
---

> AI "如何学习"的七种主流范式——它们不是互相替代的关系，而是针对不同数据条件和目标的不同路线。

## 定义

学习范式是对"模型如何从数据中获取能力"的分类。不同范式的核心区别在于：**监督信号从哪来**、**数据如何组织**、**优化目标是什么**。

## 七种主流范式

| 范式                              | 核心思想           | 监督信号 | 典型用途                           |
| ------------------------------- | -------------- | ---- | ------------------------------ |
| Supervised Learning（监督学习）       | 用标注数据学习输入→输出映射 | 人工标注 | 分类、预测                          |
| Unsupervised Learning（无监督学习）    | 从数据中发现结构       | 无    | 聚类、降维                          |
| Self-supervised Learning（自监督学习） | 用数据自身构造监督信号    | 数据自身 | LLM 预训练、BERT、CLIP、MAE          |
| Reinforcement Learning（强化学习）    | 通过环境奖励优化策略     | 奖励函数 | AlphaGo、机器人控制                  |
| Imitation Learning（模仿学习）        | 学习专家演示的行为      | 专家轨迹 | 自动驾驶、机器人                       |
| Online Learning（在线学习）           | 持续增量更新，不重新训练   | 流式数据 | 实时推荐、异常检测                      |
| Federated Learning（联邦学习）        | 分布式协同训练，数据不出端  | 本地数据 | 端侧 AI、隐私场景                     |

## 当前 LLM 训练中的范式组合

一个现代 LLM 的训练链条实际上**串联了多种范式**：

1. **Pre-training** — Self-supervised Learning（LLM 中具体实现为 NTP，但 SSL 还有 MLM、对比学习等变体）
2. **SFT** — Supervised Learning（人工标注的 instruction-response 对）
3. **RLHF / DPO** — Reinforcement Learning（人类偏好作为奖励信号）
4. **Reasoning training** — 混合 RL + Supervised（CoT 数据 + 过程奖励）

这说明范式层和训练阶段层是正交的——一个训练阶段可以使用不同范式。

## 易混淆：训练阶段 vs 学习范式

行业术语经常把"阶段"（when）和"范式"（how）混在一起，最典型的是 **SFT（Supervised Fine-Tuning）**——它把范式（Supervised）焊进了阶段名，暗示"这个阶段只能用监督学习"。实际上四个训练阶段的命名逻辑并不统一：

| 阶段名 | 名字实际编码的是 |
|---|---|
| Pre-training | when（什么时候） |
| SFT | when + how（阶段 + 范式） |
| Alignment | why（训练目标） |
| Reasoning | why（想达成的能力） |

这不是 wiki 的错——整个行业都这么叫。但理解这个区分很重要：**阶段和范式是正交的**，同一个阶段未来完全可以换用不同范式（例如 post-training 第一步从 supervised 换成 self-play 或 RLAIF）。

详见 [[LLM训练四阶段总览]]。

## 核心特性

- **Self-supervised Learning** 是当前 scale 成功的核心——它让"无标注的互联网文本"变成了可用的训练数据
- **Reinforcement Learning** 是 alignment 和 reasoning 的关键——但样本效率低，需要精心设计 reward
- **Online Learning** 和 **Federated Learning** 是边缘/端侧场景的必需——但在大模型时代尚未成为主流训练方式

## 相关页面

- [[AI技术体系总览]] — 本页所属的九层框架
- [[预训练-Pretraining]] — Self-supervised Learning 的 LLM 实践
- [[RLHF-vs-DPO]] — Reinforcement Learning 在对齐中的两种实现
- [[自主学习与在线学习]] — Online Learning 的前沿探索方向
- [[表征学习-RepresentationLearning]] — SSL 的三条技术路线
