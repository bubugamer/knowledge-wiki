---
title: 具身智能（Embodied AI / Embodied Intelligence）
created: 2026-04-16
last_updated: 2026-04-16
status: 草稿
confidence: 共识+专家观点
tags: [机器人, 具身智能, AGI, 总览]
sources:
  - 02-Areas/LLM/121. 对DeepMind谭捷的访谈：机器人、跨本体、世界模型、Gemini Robotics 1.5和Google.md
---

> 具身智能 = 把 AI 放进一个能感知、行动、和物理世界交互的身体里。它不是 "LLM + 机器人" 的简单合成，而是对"智能是否必须具身"这个 AGI 元问题的一条答案。本页是机器人/具身子域的入口。

## "大脑 + 小脑" 的分解

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

谭捷的工程性分解：

| 分层                | 角色             | 对应技术                                     |
| ----------------- | -------------- | ---------------------------------------- |
| **大脑**（cognition） | 理解任务、做计划、调工具   | LLM / VLM / ER（Embodied Reasoner）        |
| **小脑**（dexterity） | 控制关节、保持平衡、执行动作 | RL / [[VLA-视觉语言动作模型]] / Diffusion Policy |

两者并非天然割裂——Gemini Robotics 1.5 的 ER-VLA 分层正是这种工程折衷，但**终态 E2E**（见 VLA 页）。

## 两次 Paradigm Shift

<!-- confidence: 共识 | 来源：谭捷 2026-01 访谈 -->

谭捷总结机器人领域过去十年的两次范式迁移：

### 第一次（2015 前后）：RL + Graphics → 腿部运动解决

- 此前：控制论方案（MPC、手工步态生成），需要 PhD 级数学
- 之后：**[[Sim-to-Real]] 的 RL** 让任何四足/双足都能跑跳
- 结果：Atlas、ANYmal、Unitree 百花齐放

### 第二次（2022+）：LLM 到来 → 大脑打通

- 此前：任务规划靠手写 state machine
- 之后：VLM 带来**常识 + 语义理解 + 自然语言指令**
- 结果：RT-1 → RT-2 → Gemini Robotics 的基座模型线

**两次 shift 的共同点**：都是 general-purpose 方法（RL、LLM）**干掉**了手工特化方案——和 [[Bitter-Lesson]] 一致。

## 通用 vs 专用：当前最大的战略分歧

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

| 路线 | 代表 | 商业逻辑 | 风险 |
|---|---|---|---|
| **Generalist（通用）** | Google DeepMind / Figure | 一个模型干 100 种任务，押 AGI | 十年级长周期，现金流难 |
| **Specialist（专用）** | Dyna（折衣服）/ 各类工业垂类 | 单场景深耕、短期盈利 | 通用模型成熟后被降维打击 |

谭捷押通用——判断：**一旦 Generalist 真正成形，Specialist 很难生存**。

## 具身智能为什么还没 GPT 时刻

<!-- confidence: 专家观点 | 来源：谭捷 2026-01 访谈 -->

三大瓶颈：

1. **数据瓶颈**——真机数据不可 scale；仿真有 gap；video 有形态 gap。解法见 [[Sim-to-Real]] 的数据金字塔。
2. **跨本体瓶颈**——单本体数据永远凑不齐 scale。解法见 [[跨本体-CrossEmbodiment]]。
3. **推理延迟瓶颈**——机器人控制需要 10–30 Hz，thinking model 每步要 20s。解法见 [[VLA-视觉语言动作模型]] 的 ER-VLA 分层。

谭捷预测：**2-3 年内具身 AGI 会出现 "GPT 时刻"**（scaling law 被证实，资本涌入）；**5-10 年内真正大规模落地**（工厂/物流先行，家庭最后）。

## 和现有 AI 概念的关系

| 概念 | 具身智能的映射 |
|---|---|
| [[世界模型-WorldModel]] | 机器人的"内部模拟器"——Genie 型可交互视频生成是最前沿候选 |
| [[Moravec悖论]] | 直接体现：腿部已解决，手部还没——在机器人内部继续分层 |
| [[Bitter-Lesson]] | 两次范式迁移都印证：通用方法打败手工方案 |
| [[多模态融合-生成理解割裂]] | 具身智能必须打通感知→行动，不能停在 "看懂 ≠ 做对" |
| [[Code-AI的Affordance]] | 物理世界是机器人的 affordance，code 是数字 agent 的 affordance |

## 相关页面

- [[VLA-视觉语言动作模型]] — "小脑"的主流架构
- [[跨本体-CrossEmbodiment]] — scale 的关键约束
- [[Sim-to-Real]] — 数据金字塔与仿真策略
- [[世界模型-WorldModel]] — 具身智能的终态基础设施
- [[Moravec悖论]] — 为什么这件事难
- [[Bitter-Lesson]] — 为什么 general > specialist
