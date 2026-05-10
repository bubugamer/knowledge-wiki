---
title: 表征学习（Representation Learning）
created: 2026-04-16
last_updated: 2026-04-16
status: 草稿
confidence: 共识+专家观点
tags: [LLM, 表征, 自监督, CV]
sources:
  - 02-Areas/LLM/133. 对谢赛宁的7小时马拉松访谈：世界模型、逃出硅谷、AMI Labs、两次拒绝Ilya、杨立昆、李飞飞和42.md
---

> 表征学习 = 把数据映射到一个具有"良好性质"的空间，使下游任务变得容易。谢赛宁的核心 bet：**表征是世界模型最重要的一部分**——有了足够好的表征，语言模型会退化成一个 communication interface。

## 定义

给定数据 $x$，学一个编码器 $f$ 使 $f(x)$ 满足：

- **层次化（Hierarchical）**——每一层都是对上一层的抽象
- **抽象化 = 泛化**——一只真狗、卡通狗、小孩画的狗在像素上完全不同，但表征空间里都应该是"狗"
- **良好的下游可用性**——分类、检索、生成、决策都能用

## 三条主流自监督路线

<!-- confidence: 共识 -->

不依赖外部 label 的表征学习（Self-Supervised Learning, SSL）主要有三条路：

| 路线 | 代表工作 | 原理 | 性质 |
|---|---|---|---|
| **对比学习（Contrastive）** | MoCo、SimCLR、DINO | 把相似样本拉近、不相似样本推远 | 学"对 augmentation 的不变性" |
| **掩码重建（Masked Autoencoder）** | MAE、BEiT | 遮挡输入的一部分，让模型重建 | 学"遮挡不变性" |
| **联合嵌入预测（JEPA 系）** | I-JEPA、V-JEPA | 在抽象表征空间做预测，不回到像素 | 见 [[JEPA-联合嵌入预测架构]] |

前两条在小模型上有效，一 scale up 就失效——因为**不变性是人工设计的**，不是数据驱动的，见 [[多模态融合-生成理解割裂]]。

## Yann LeCun 的 "Layer Cake" 比喻

<!-- confidence: 专家观点 | 来源：LeCun 早期公开演讲 -->

机器学习能量分布：

- **蛋糕主体** = 自监督学习（绝大部分 signal 来自数据本身）
- **糖霜** = 监督学习（少量标注 fine-tune）
- **樱桃** = 强化学习（最后的校准）

LeCun 从 2016 年起就押注这条路线——这也是 AMI Labs 的精神底色。

## "不要惧怕高维度"

<!-- confidence: 共识 -->

经典机器学习原则（Kernel Method → Transformer 的 upper projection layer 都遵循）：

- 低维空间里无解的问题，升维之后往往线性可分
- 高维表征有更好的 efficiency 与信息承载量

马毅老师的补充：不但不要害怕高维度，还要害怕**不敢跳出当前的 local optimum**——例如 VAE 的低维 latent space 就是一个 local optimum，表征学习需要有意识地跳出它。

## 谢赛宁的中心论点：表征是世界模型的基础

<!-- confidence: 专家观点 | 来源：谢赛宁 2026-03 访谈 -->

> "这个世界上只有一件事重要，就是怎么学习到这个表征。"

有了足够好的表征：

- LM 退化为 communication interface（不再承担 heavy lifting）
- 可以 decode 成 pixel → 视频生成
- 可以 decode 成 action → robotics / VLA

这是他"逃出硅谷"、两次拒绝 Ilya、和 LeCun 创业（[[JEPA-联合嵌入预测架构]]）的核心驱动。

## 反思：Neural Architecture Search 耽误了两年

<!-- confidence: 专家观点 | 来源：谢赛宁 2026-03 访谈 -->

NAS（Neural Architecture Search）的错误在于——把研究 energy 投入到"改架构"而不是"改表征目标函数"。架构只是服务于算法的载体。这与张祥雨 "架构不重要，它服务于算法" 的判断一致（见 [[LongContext与分层记忆]]）。

## 相关页面

- [[JEPA-联合嵌入预测架构]] — 第三条 SSL 路线
- [[世界模型-WorldModel]] — 表征是世界模型的基础
- [[多模态融合-生成理解割裂]] — 为什么 CV 的对比学习/MAE scale up 会失败
- [[Bitter-Lesson]] — NAS 等反例的哲学
- [[LLM术语速查]] — MoCo、MAE、SimCLR 等术语定义
