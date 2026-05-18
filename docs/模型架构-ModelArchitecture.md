---
title: 模型架构（Model Architecture）
created: 2026-05-06
last_updated: 2026-05-06
status: 草稿
confidence: 共识
tags: [AI, 模型架构, 神经网络]
sources: []
visibility: public
---

> 神经网络"长什么样"——当前主流的 11 种模型架构，从经典 MLP 到前沿 SSM 和 MoE。

## 定义

模型架构定义了神经网络的**计算图结构**——数据如何流动、信息如何聚合、参数如何组织。架构选择决定了模型擅长处理什么类型的数据和任务。

## 架构全景

| 架构                           | 核心机制           | 主流应用领域            | 时代定位                  |
| ---------------------------- | -------------- | ----------------- | --------------------- |
| MLP                          | 全连接前馈          | 小模型、特征处理子模块       | 基础构件                  |
| CNN                          | 卷积 + 局部感受野     | 图像视觉、早期 NLP       | 2012–2020 CV 主流       |
| RNN                          | 序列递归           | 早期 NLP、时序         | 已被 Transformer 替代     |
| LSTM / GRU                   | 门控长序列记忆        | 语音、早期 NLP         | 已被 Transformer 替代     |
| **Transformer**              | Self-Attention | LLM、多模态、几乎所有前沿    | 当前绝对主流                |
| **Diffusion Model**          | 逐步去噪生成         | 图像 / 视频生成         | 生成领域主流                |
| GAN                          | 对抗生成（G vs D）   | 图像生成、数据增强         | 被 Diffusion 逐步替代      |
| VAE                          | 潜变量编码-解码       | 表征学习、生成           | 仍在 latent space 设计中活跃 |
| GNN                          | 图结构消息传递        | 知识图谱、分子、社交网络      | 图数据专用                 |
| **State Space Model (SSM)**  | 线性递推 + 选择性机制   | 长序列建模（Mamba 等）    | 新兴挑战者                 |
| **Mixture of Experts (MoE)** | 稀疏激活 + 路由      | 超大规模模型（Mixtral 等） | 规模化主流方案               |

## 核心公式

**Transformer Attention**:

$$\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

核心洞察：通过 Q/K 点积计算 token 间的相关度，加权聚合 V。复杂度 O(n²)，这是长序列的瓶颈。

**Diffusion 前向过程**:

$$x_t = \sqrt{1-\beta_t} \cdot x_{t-1} + \sqrt{\beta_t} \cdot \epsilon$$

核心洞察：逐步加噪破坏数据，然后训练网络学习逆向去噪。生成质量高但推理慢。

## 当前格局

- **Transformer 是绝对中心**：LLM、VLM、甚至图像（ViT）、视频、音频都在用
- **Diffusion 是生成王者**：图像（Stable Diffusion/DALL-E）、视频（Sora）
- **SSM 是效率挑战者**：Mamba 等模型在长序列上有 O(n) 优势，但尚未撼动 Transformer 在 LLM 上的地位
- **MoE 是规模化方案**：不增加推理成本的情况下扩大模型容量（GPT-4、Mixtral、DeepSeek-V3）——详见 [[MoE-混合专家模型]]

## 常见误解

- "Transformer 会被 SSM 替代" — 目前更可能的结局是混合架构（Transformer + SSM），而非完全替代
- "Diffusion 只能做图像" — 已扩展到视频、3D、音频、蛋白质结构等
- "MoE 是新发明" — 概念来自 1991 年，是近年工程突破（路由稳定性、负载均衡）让它在超大规模成为可行。详见 [[MoE-混合专家模型]]

## 相关页面

- [[AI技术体系总览]] — 本页所属的九层框架
- [[表征学习-RepresentationLearning]] — VAE 和 SSL 路线的深入探讨
- [[JEPA-联合嵌入预测架构]] — 在表征空间做预测的新架构思路
- [[NTP的本质缺陷]] — Transformer + NTP 的固有限制
- [[多模态融合-生成理解割裂]] — 为什么 Diffusion 和 Transformer 还没真正统一
