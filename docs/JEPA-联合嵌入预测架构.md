---
title: JEPA（Joint Embedding Predictive Architecture）
created: 2026-04-16
last_updated: 2026-04-16
status: 草稿
confidence: 专家观点
tags: [LLM, JEPA, LeCun, 世界模型, 架构]
sources:
  - 02-Areas/LLM/133. 对谢赛宁的7小时马拉松访谈：世界模型、逃出硅谷、AMI Labs、两次拒绝Ilya、杨立昆、李飞飞和42.md
---

> JEPA = Yann LeCun 2022 年在 *A Path Towards Autonomous Intelligence* 中提出的架构。内核：**不在像素空间做生成，而在抽象表征空间做预测**。它是一套 Cognitive Architecture，不是单一算法。

## 核心思想

<!-- confidence: 专家观点 | 来源：LeCun 2022 position paper -->

> 你不能做 generative model，不能把所有东西都记住重建出来。你需要在一个抽象的表征空间里做预测。

传统生成模型（Autoregressive、Diffusion）都在 pixel/token 空间里硬算，JEPA 的做法：

1. 把输入（图像、视频 patch）编码到 embedding 空间
2. 在 embedding 空间直接预测另一部分 embedding
3. **不回到 pixel，不计算重建 loss**

回避了"为每个像素建模"的信息浪费——大量像素级细节（纹理、光照变化）对世界理解无关。

## 变体

| 名称 | 领域 |
|---|---|
| **I-JEPA** | Image JEPA |
| **V-JEPA** | Video JEPA |
| **TheJEPA** 系列论文 | 给出数学证明：若要学到 downstream-agnostic 的 representation，它必须是 isotropic Gaussian distribution |

## JEPA ≠ Self-Supervised Learning

<!-- confidence: 专家观点 | 来源：谢赛宁 2026-03 访谈 -->

谢赛宁对 JEPA 的三阶段认知：

1. **质疑**——以为 "yet another SSL algorithm"（像 MoCo、MAE 的延伸）
2. **理解**——发现 JEPA 背后有严格数学原理，走得比普通 SSL 更深
3. **成为**——JEPA 不是一个算法，是一整套 cognitive architecture，LM 只是其中一部分

这套架构应同时具备：world understanding、prediction、planning。LLM 可以作为其中的"语言模块"接入。

## 为什么 AMI Labs 押注 JEPA

<!-- confidence: 专家观点 | 来源：谢赛宁 2026-03 访谈 -->

- **一致性**——LeCun 从 2016 年起就提 SSL 优先论，路线从未变过
- **架构包容性**——JEPA 是"海洋"，上面可以跑多艘船（LM、video gen、robotics policy）
- **去中心化**——不依赖互联网 tokenize 的数据，天然需要多方合作（"World Model needs the World"）
- **可规模化**——在 representation 空间做预测，计算成本远低于像素空间

## 和 Bitter Lesson 的张力

JEPA 在抽象表征空间里做预测，表面上引入了"不做像素"的结构先验，有人因此说它 anti-bitter-lesson。但谢赛宁的反论点：**LLM 才是 anti-bitter-lesson**——语言本身就是人类几千年设计出的极强结构。JEPA 反而丢掉了这层人工结构，交给数据自己学。见 [[Bitter-Lesson]]。

## 相关页面

- [[世界模型-WorldModel]] — JEPA 是"抽象表征派"的具体架构
- [[表征学习-RepresentationLearning]] — JEPA 是第三条 SSL 路线
- [[Bitter-Lesson]] — 哪条路线更 bitter lesson 的争论
- [[多模态融合-生成理解割裂]] — 生成和理解为什么分家
