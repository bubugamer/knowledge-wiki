---
title: AI 技术体系总览
created: 2026-05-06
last_updated: 2026-05-06
status: 草稿
confidence: 共识
tags: [AI, 总览, 技术体系]
sources: []
---

> 当前 AI 主流技术的九层分层框架——从学习范式到系统工程，再到行业趋势，提供一张完整的技术地图。

## Overview

理解当前 AI 技术体系，需要把"一锅粥"分成清晰的层次。每一层回答一个不同的问题：

| 层 | 回答的问题 | Wiki 入口 |
|---|---|---|
| 1. 学习范式 | AI 如何学习？ | [[学习范式-LearningParadigm]] |
| 2. 模型架构 | 神经网络长什么样？ | [[模型架构-ModelArchitecture]] |
| 3. 训练与优化 | 模型怎么训练？ | [[LLM训练四阶段总览]]、[[RLHF-vs-DPO]]、[[PEFT-LoRA]] |
| 4. 能力层 | AI 会什么？ | 见下方 |
| 5. 应用能力方向 | 产业 AI 主要做什么？ | 见下方 |
| 6. 系统工程 | AI 系统如何组织？ | [[AI系统形态-SystemArchitecture]] |
| 7. 产品映射 | 主流产品背后是什么？ | 见下方 |
| 8. 行业趋势 | 方向是什么？ | 大融合（Convergence） |
| 9. 未来架构 | 终局是什么？ | 统一认知架构 |

## 四、能力层（Capability Layer）

AI "会什么"——从底层能力到高级认知：

- **基础能力**: Classification、Regression、Perception
- **生成能力**: Generation（文本/图像/视频/代码）
- **认知能力**: Reasoning、Planning、Search
- **交互能力**: Retrieval、Tool Use、Memory、Control
- **融合能力**: Multi-modal Understanding

## 五、应用能力方向（Application Intelligence）

当前产业 AI 的主要产品化方向：

| 方向 | 核心技术栈 |
|---|---|
| LLM | Transformer |
| VLM（Vision-Language Model） | Vision Encoder + Transformer |
| TTS / STT | Transformer / Conformer |
| Image Generation | Diffusion |
| Video Generation | Diffusion + Transformer |
| Recommendation AI | Embedding + Ranking |
| Search AI | Retrieval + Ranking |
| Autonomous Driving | CV + RL + Planning |
| Robotics AI | [[VLA-视觉语言动作模型]] + RL |
| Scientific AI | GNN + Foundation Model |

## 七、产品技术映射

| 产品 | 底层本质 |
|---|---|
| ChatGPT | Transformer + RLHF |
| Claude | Transformer + Constitutional AI |
| Midjourney | Diffusion |
| Sora | Diffusion + Transformer |
| AlphaGo | RL + MCTS |
| Tesla FSD | CV + RL + Planning |
| AutoGPT | LLM + Workflow |
| Devin | LLM + Tool Chain |

## 八、行业最大趋势：大融合（Convergence）

当前最先进系统正在融合多条技术路线，而非"一条路线取代另一条"：

| 能力 | 技术来源 |
|---|---|
| 生成 | LLM / Diffusion |
| 推理 | Search / RL |
| 长期记忆 | RAG / Memory |
| 行动 | Agent / Tool Use |
| 世界理解 | [[世界模型-WorldModel]] |
| 多模态 | VLM |
| 决策 | RL |

## 九、未来：统一认知架构（Unified Cognitive Architecture）

行业正朝着一个统一系统演化，融合：感知、生成、推理、规划、记忆、行动、世界建模。

当前的大模型是这个方向的早期阶段——它们擅长生成和部分推理，但在规划、长期记忆、持续学习、世界建模方面仍有结构性缺陷（见 [[NTP的本质缺陷]]、[[LongContext与分层记忆]]、[[自主学习与在线学习]]）。

## Related Pages

- [[学习范式-LearningParadigm]] — AI 如何学习
- [[模型架构-ModelArchitecture]] — 神经网络长什么样
- [[AI系统形态-SystemArchitecture]] — AI 系统如何组织
- [[LLM训练四阶段总览]] — 训练与优化的 LLM 实践视角
- [[世界模型-WorldModel]] — 融合趋势的核心方向之一
- [[Agent三阶段演变]] — 系统形态中 Agent 的演进
