---
title: Bitter Lesson（苦涩的教训）
created: 2026-04-16
last_updated: 2026-04-16
status: 草稿
confidence: 共识+专家观点
tags: [AI, 哲学, Scaling, Sutton]
sources:
  - 02-Areas/LLM/133. 对谢赛宁的7小时马拉松访谈：世界模型、逃出硅谷、AMI Labs、两次拒绝Ilya、杨立昆、李飞飞和42.md
visibility: public
---

> Richard Sutton 2019 年的博文 *The Bitter Lesson*：70 年 AI 史反复证明，**依赖算力的通用方法（search + learning）终将超越依赖人类领域知识的方法**。"苦涩"之处在于——研究者总想把自己理解的东西塞进系统，但这条路反复失败。

## 原始论点

<!-- confidence: 共识 | 来源：Sutton 2019 -->

> "The two methods that seem to scale arbitrarily in this way are **search** and **learning**."

核心结论：**尽可能减少人类知识的注入，尽可能多地用 search 和 learning**。

## Sutton 列的历史证据

| 领域 | 基于人类知识的方法 | 被谁取代 |
|---|---|---|
| 计算机国际象棋 | 人类设计的开局库 + 评估函数 | Deep Blue 的 alpha-beta search |
| 计算机围棋 | 人类棋理 + Monte Carlo | AlphaGo 的 search + RL |
| 语音识别 | HMM + 音素 | End-to-end 深度学习 |
| 计算机视觉 | SIFT / HOG / 手工特征 | CNN + ImageNet |

## 大模型时代的争议：LLM 算不算 bitter lesson?

<!-- confidence: 专家观点 | 来源：谢赛宁 2026-03 访谈 -->

**主流叙事**：LLM = bitter lesson 的胜利（巨大 scale + 通用 Transformer，抛弃了过去所有 NLP 手工流水线）。

**谢赛宁的反方观点**："LLM 其实是 anti-bitter-lesson"——

- 语言是人类几千年文明演化、精雕细琢的产物
- 它有精巧的句法、逻辑结构、语义抽象——**全都是人类设计的 structure**
- 把语言当作"免费的自监督数据"，其实是把这层巨大的人工设计偷渡了进去
- 真正的 bitter lesson 应该绕开语言，直接建模 P(X) 而不是 P(Y)

## Video Generation 比 LLM "更 bitter lesson"

<!-- confidence: 专家观点 | 来源：谢赛宁 2026-03 访谈 -->

- LLM 建模 **P(Y)**——低维 label 空间的竞争（是猫不是狗）
- Video diffusion 建模 **P(X|Y)**——要知道 "为什么四条腿的猫比三条腿的猫更常见"，信息量大得多
- 再推一步：连像素都是人为定义的 regular grid。**更 bitter lesson 的终点是直接在 latent 表征空间里学**——即 [[JEPA-联合嵌入预测架构]] 的主张

## 常见引用场景

- 为 Scaling Law 正名（"数据与算力压倒精巧设计"）
- 批评 Neural Architecture Search、复杂 inductive bias（见 [[表征学习-RepresentationLearning]]）
- 辩论 LLM 是否是 endgame（谢赛宁 vs LLM 派）

## 相关页面

- [[世界模型-WorldModel]] — 不同流派对 bitter lesson 的理解分歧
- [[JEPA-联合嵌入预测架构]] — 谢赛宁认为更 bitter lesson 的路线
- [[表征学习-RepresentationLearning]] — NAS 等反例
- [[NTP的本质缺陷]] — 另一条批评 LLM 的路径
