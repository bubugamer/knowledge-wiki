---
title: 跨本体（Cross-Embodiment）
created: 2026-04-16
last_updated: 2026-04-16
status: 草稿
confidence: 共识+专家观点
tags: [机器人, 具身智能, 跨本体, Motion Transfer, DeepMind]
sources:
  - 02-Areas/LLM/121. 对DeepMind谭捷的访谈：机器人、跨本体、世界模型、Gemini Robotics 1.5和Google.md
---

> 跨本体 = 同一个模型能在**不同形态的机器人**上运行（ALOHA 桌面双臂 / Franka 工业臂 / Unitree 人形腿 / 单臂 gripper / 五指灵巧手……）。它是机器人基座模型能否 scale 的关键——单本体数据永远凑不齐 GPT-3 需要的规模。

## 为什么非要跨本体

<!-- confidence: 共识 | 来源：谭捷 2026-01 访谈 -->

机器人数据的根本困境：

- 单本体上采集 100 万小时遥操作数据 → **需要数十亿美元 + 数年**
- 全世界把所有本体的数据加在一起 → 量级才勉强接近 LM 预训练的 scale
- 而且新机器人型号每年在变，死守单本体 = 重新造轮子

结论：**跨本体不是 "nice to have"，是机器人基座模型的生存条件**。

## Embodiment Gap（本体差异）

<!-- confidence: 共识 -->

不同机器人差异的维度：

| 维度 | 举例 |
|---|---|
| 自由度 | 6-DOF 单臂 vs 双臂 vs 人形（50+ DOF） |
| 末端执行器 | 平行 gripper / 吸盘 / 多指灵巧手 |
| 感知布置 | 手腕相机 / 头部相机 / 第三人称 |
| 移动能力 | 固定底座 / 轮式 / 腿式 |

本体差异越大，跨本体迁移越难。谭捷：**形态相似时 motion transfer 效果最好；形态差异大（桌面臂 → 人形）时需要大量数据才能打通**。

## Motion Transfer（Gemini Robotics 1.5 的关键技术）

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

Motion Transfer = 通过架构和训练 recipe 的修改，让模型自然学会 "在 ALOHA 上学的动作知识能直接用在 Franka 上"。

代表性 demo（Gemini Robotics 1.5）：
- **只在 ALOHA 上教**某个折叠动作 → **Franka 上零样本执行**（无需 Franka 的 demo）
- 反向亦然

技术来源：**不是高层规划的 API——是团队 bottom-up 自发研究的成果**（谭捷：这是 Google DeepMind 的工程文化，不是 CEO 指令）。

## Open X-Embodiment：先行的跨本体数据集

<!-- confidence: 共识 -->

2023 年跨机构联合发布：

- **22 种**不同机器人本体
- **160k+** 机器人任务轨迹
- 首次证明"多本体联合训练 > 单本体训练"
- 是后来 RT-X / Gemini Robotics 的数据基础

## 跨本体是 数据飞轮 的前提

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

谭捷的判断：机器人的 Tesla FSD 时刻（海量真机数据反哺模型）**不会发生**，除非先解决跨本体——否则每个型号都要重新收集。一旦跨本体成立：

- 厂商 A 卖的机器人 → 数据进入联合模型
- 厂商 B 的新本体 → 上来就能用联合模型的先验
- 数据飞轮才能转起来

## Related Pages

- [[VLA-视觉语言动作模型]] — Motion Transfer 是 VLA 的一个能力
- [[Sim-to-Real]] — 另一条 scale 路径（同构：数据的跨域迁移）
- [[具身智能-EmbodiedAI]] — 跨本体是具身 AGI 的 scale 前提
- [[LLM术语速查]] — ALOHA / Franka / Unitree 等术语
