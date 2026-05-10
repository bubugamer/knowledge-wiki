---
title: SFT（有监督微调）
created: 2026-04-14
last_updated: 2026-04-14
status: 草稿
confidence: 共识
tags: [LLM, SFT, 微调]
sources:
  - 02-Areas/LLM/大型语言模型从0到1白皮书v2.md
---

> SFT 把"只会续写文本"的语言模型改造成"能听指令、按对话形式回答"的助理。它是人类第一次以逐条样本形式深度介入的阶段，核心工作是**写答案**。

## 核心目标：模仿"标准答案"

用"指令-回答"对（`Instruction-Response Pair`）数据集训练，目标函数是**最大化复现（模仿）数据集中给出的标准答案**。

## 人类介入：写答案而非判答案

这是理解 SFT 最重要的一句话：

> 在 SFT 阶段，人的工作是**"写答案"**，而不是"判答案"。

相比之下，[[Alignment-对齐]] 阶段人类才开始"判答案"（打偏好、排序、定安全边界）。

### 介入方式

- **方式一（人类撰写）**：标注员根据 Prompt 直接写"黄金标准答案"（Gold Response）。
- **方式二（人机协同）**：模型先生成草稿，人类标注员编辑、修订或重写。

### 相关角色

- 标注员（Annotator）
- 审校员（Reviewer）
- 领域专家（SME）

## 企业实践：几乎一定走 PEFT/LoRA

真实企业实践中，99% 的团队**不会做全参数微调**，而是用 [[PEFT-LoRA]]：

- **只训练新增的 LoRA/Adapter 参数**，基础模型权重冻结。
- **Tokenizer 和 Config 不变**。
- **交付物**不再是一个完整的新模型，而是一个轻量 Adapter 文件（如 `adapter_model.safetensors`）。

工程语义：基础模型是"能力地基"，SFT Adapter 是"说话方式"的插件。

## 相关页面

- [[LLM训练四阶段总览]] — SFT 在整条链路中的位置
- [[Alignment-对齐]] — SFT 之后的"价值观精雕"
- [[PEFT-LoRA]] — SFT 的主流落地形态
- [[LLM术语速查]] — SFT / Fine-tuning / Post-training 的精确区分
