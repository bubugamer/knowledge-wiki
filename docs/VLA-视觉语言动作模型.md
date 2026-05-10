---
title: VLA（Vision-Language-Action Model）
created: 2026-04-16
last_updated: 2026-04-16
status: 草稿
confidence: 共识+专家观点
tags: [机器人, 具身智能, VLA, 基座模型, Gemini Robotics]
sources:
  - 02-Areas/LLM/121. 对DeepMind谭捷的访谈：机器人、跨本体、世界模型、Gemini Robotics 1.5和Google.md
---

> VLA = Vision-Language-Action Model。输入视觉和语言，输出机器人动作（低阶 joint/关节控制 或高阶 action token）。是当前"机器人基座模型"的主流架构范式——**本质是 VLM 的 action 版微调**。

## 核心结构

一个最小 VLA 由三部分组成：

1. **Vision Encoder**——吃相机图像，输出视觉表征
2. **Language 理解**——吃人类指令 / 任务描述
3. **Action Head**——把 fused 表征解码为机器人控制信号

<!-- confidence: 共识 -->

## 演进脉络

<!-- confidence: 共识 | 来源：谭捷 2026-01 访谈 -->

| 模型 | 出品 | 关键突破 |
|---|---|---|
| **RT-1** | Google 2022 | 首个大规模 Transformer 机器人模型，收集 13 万条 demo |
| **RT-2** | Google 2023 | 直接 fine-tune 预训练 VLM + action 数据，**继承互联网知识**（能识别 Taylor Swift） |
| **RT-X / Open X-Embodiment** | 跨机构联合 2023 | 22 种机器人本体的联合数据集，探索跨本体迁移 |
| **Gemini Robotics 1.5** | Google DeepMind 2025 | ER-VLA 分层架构 + Motion Transfer + Embodied Reasoning |

## ER-VLA 分层：快慢两个模型

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

Gemini Robotics 1.5 的关键架构创新——把一个大模型拆成两个：

| 模块 | 角色 | 频率 | 类比 LLM |
|---|---|---|---|
| **ER（Embodied Reasoner）** | 慢思考、做规划、可调工具（搜索 / 代码） | 秒级 | System 2 / CoT |
| **VLA** | 快速动作生成 | 10–30 Hz | System 1 |

**为什么非要拆**：机器人控制需要 0.5–1s 的 inference 延迟（不然动作卡顿），而 thinking 模型单步就要 20s 起。**单模型吃不下两个量级的时延预算**，所以目前只能分层。

**未来方向**：谭捷判断 E2E 是终态，分层是过渡——等算力/架构成熟后会合并。和自动驾驶的 planning/control 分离是反例。

## Action Space 的三种表示

<!-- confidence: 共识 -->

VLA 输出"动作"有多种编码方式，近年基本收敛到三类：

1. **Action Token**——把动作离散化成 token，沿用 LM 的自回归生成（RT-2 路线）
2. **Diffusion Policy**——用 diffusion 生成连续动作序列（π0 / Diffusion Policy）
3. **直接回归** joint/end-effector 目标

没有哪种天然胜出——和数据、任务、推理速度相关。

## VLA ≠ 独立研究方向

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

> "绝大多数做 VLA 的公司，其实还是在大语言模型或者多模态语言模型上做一些 fine tuning。"

谭捷的锐利观察：**VLA 目前不是一个独立的学科**，它是 VLM 的下游应用。这反驳了"机器人基座模型是独立赛道"的叙事——真正的 heavy lifting 仍在 VLM 预训练这一侧，只有极少数公司（Google/DeepMind）有能力从头预训练自己的 VLM。

推论：VLA 的进步=VLM 进步×机器人动作数据量。单靠机器人公司自己训基座，数据成本无法 justify。

## VLA 的下一步：VLV（Vision-Language-Vision）?

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

谭捷给出的架构演进猜想——下一代可能不直接输出 action，而是输出"下一帧图像"（V+L→V），把 world model 作为中间表征，action 从 world model 里规划出来。这就自然连到了 [[世界模型-WorldModel]] 和 [[JEPA-联合嵌入预测架构]] 的路线。

## 相关页面

- [[跨本体-CrossEmbodiment]] — Motion Transfer 是 VLA 跨机器人迁移的关键技术
- [[Sim-to-Real]] — VLA 的数据来源策略
- [[具身智能-EmbodiedAI]] — VLA 在具身智能栈里的位置
- [[世界模型-WorldModel]] — VLV / world model as backbone 的猜想
- [[LLM术语速查]] — RT-X / ALOHA / π0 等术语
