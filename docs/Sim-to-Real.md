---
title: Sim-to-Real（仿真到现实迁移）
created: 2026-04-16
last_updated: 2026-04-16
status: 草稿
confidence: 共识+专家观点
tags: [机器人, 仿真, 数据, Sim2Real, Diffusion]
sources:
  - 02-Areas/LLM/121. 对DeepMind谭捷的访谈：机器人、跨本体、世界模型、Gemini Robotics 1.5和Google.md
---

> Sim-to-Real = 在物理仿真器里训练策略，然后部署到真实机器人。**解决了过去十年机器人"腿部运动"（locomotion）的所有事**（Atlas 跑跳、四足机器人走路）——但对"操纵"（manipulation）至今没完全搞定。

## 为什么需要 Sim

<!-- confidence: 共识 -->

真机数据的根本问题：

| 维度 | 真机数据 | 仿真数据 |
|---|---|---|
| 单位成本 | 人工遥操作，$10–50/小时 | 电费，$0.01/小时 |
| 安全 | 机器人摔坏 → 几万美元 | 无 |
| 并行度 | 1 台机器 = 1 条数据 | 1 台 GPU = 10000 个并行 env |
| 可控性 | 真实世界无法 replay | 完全可复现 |
| **保真度** | **完美（就是真实）** | **有 sim-to-real gap** |

结论：真机数据质量高但不可 scale；仿真数据可 scale 但有 gap。

## Sim-to-Real Gap

<!-- confidence: 共识 -->

仿真器和真实世界的差异来源：

1. **物理引擎近似**——接触力、摩擦、软体、流体仿真都不够准
2. **视觉渲染差异**——光照、纹理、材质 domain gap
3. **传感器噪声**——真实相机噪声、IMU 漂移、时延难仿
4. **执行器动力学**——电机延迟、齿轮间隙、磨损

**谭捷的判断**：gap 永远存在，但"**用算力把量级堆到海量，可以把 gap 用平均效应抹平**"。这是 domain randomization 路线背后的逻辑。

## Domain Randomization：经典解法

<!-- confidence: 共识 -->

> 训练时随机化光照 / 纹理 / 物理参数 / 传感器噪声，让策略学到 **对 randomize 出来的分布都 robust** 的能力——真实世界只是这个分布里的一个样本。

代表工作：OpenAI Dactyl（2019，单手转魔方）、ANYmal 四足。适用于 locomotion 很好；manipulation 里碰到接触动力学差异大时效果打折。

## 数据金字塔（谭捷的数据策略框架）

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

机器人训练数据按"量级 vs 保真度"分四层：

```
            真机遥操作数据        ← 保真度 100%，量级最小（万级 demo）
               ↑
           仿真器数据            ← 保真度中，量级大（亿级步）
               ↑
          人类 ego-centric 视频   ← 形态 gap 大，量级非常大（YouTube 几十亿小时）
               ↑
           互联网多模态数据       ← 无 action，量级天文（VLM 预训练用）
```

**关键**：每一层各有用处，任何单一层都不够——金字塔越底越便宜、越广，越顶越准、越贵。Gemini Robotics 的数据配方是"四层混训"。

## 视频生成作为"新仿真"

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

谭捷：**Sora2 / Veo 正在重新定义"仿真"这个词**——如果一段生成视频的物理看起来是对的，它就是一种新意义上的仿真。

对比：

| 传统仿真器 | 视频生成模型 |
|---|---|
| 显式物理方程 | 隐式从数据学物理 |
| 任意交互 | 目前**条件生成**，交互性弱 |
| 保真度有限（软体、接触难仿） | 视觉保真度极高 |
| 已成熟十年 | 刚出现 |

**缺的是交互性**。[[世界模型-WorldModel]] 一节的 Genie 是"可交互的视频仿真"——这才是真正的 world model as simulator。谭捷：**V-JEPA / Genie 这类 interactive generation 是 sim-to-real 的下一步**。

## Manipulation 为什么还没 Sim-to-Real 成功

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

- Locomotion：刚体 + 关节 + 地面接触——物理仿真准
- Manipulation：柔软物体 + 多指接触 + 摩擦 + 视觉依赖——**所有仿真难点的交集**
- 谭捷预测：2-3 年内随 video gen + 真机数据混训，manipulation 会突破——详见 [[具身智能-EmbodiedAI]]

## Related Pages

- [[VLA-视觉语言动作模型]] — 使用 sim 数据训练的主流方式
- [[跨本体-CrossEmbodiment]] — 另一条 scale 路径
- [[世界模型-WorldModel]] — Genie / video gen 作为 interactive simulator
- [[具身智能-EmbodiedAI]] — locomotion 已解决 vs manipulation 未解决
- [[LLM术语速查]] — domain randomization / Genie / Sora2 等术语
