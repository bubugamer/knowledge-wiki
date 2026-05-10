---
title: AI 系统形态（System Architecture）
created: 2026-05-06
last_updated: 2026-05-06
status: 草稿
confidence: 共识
tags: [AI, 系统架构, Agent, RAG]
sources: []
---

> AI 系统"如何组织"——从简单 Chatbot 到 AI Operating System 的七种系统形态，复杂度和自主性递增。

## What It Is

系统形态描述的是 AI 能力如何被**工程化地组装和交付**给用户。同样的底层模型（如 GPT-4），可以被组装成完全不同的系统形态。

## 七种系统形态

按自主性和复杂度递增排列：

| 系统形态 | 本质 | 人类角色 | 典型产品 |
|---|---|---|---|
| **Chatbot** | 单轮/多轮对话 | 主导者 | ChatGPT 基础模式 |
| **Copilot** | 人机协同辅助 | 决策者，AI 建议 | GitHub Copilot、Cursor |
| **RAG** | 检索增强生成 | 提问者 | 企业知识问答系统 |
| **Workflow AI** | 预定义工作流编排 | 设计者 | Dify Workflow、n8n |
| **Agent** | 长链任务自主执行 | 委托者 | Claude Code、Devin |
| **Multi-Agent** | 多智能体协作 | 监督者 | CrewAI、AutoGen |
| **AI Operating System** | AI 任务调度系统 | 用户 | 尚无成熟产品 |

## 关键区分

**Copilot vs Agent**:
- Copilot：人在 loop 中，AI 辅助每一步决策
- Agent：人委托目标，AI 自主规划和执行步骤

**RAG vs 微调**:
- RAG：知识在外部，模型检索后回答（见 [[微调vs RAG-决策]]）
- 微调：知识/行为编码进模型权重

**Workflow vs Agent**:
- Workflow：路径预定义，确定性执行
- Agent：路径动态生成，模型决定下一步（见 [[REACT-推理与行动架构]]）

## 演化方向

系统形态的演化不是线性替代，而是**按场景选择**：

- 高确定性 + 低风险 → Workflow AI（可靠、可审计）
- 高不确定性 + 需探索 → Agent（灵活、但需要 guardrails）
- 需要专业知识 → RAG（准确、可溯源）
- 需要实时协作 → Copilot（人保持控制）

当前趋势是**混合形态**：一个产品中可能同时包含 RAG + Agent + Workflow 组件。

## Related Pages

- [[AI技术体系总览]] — 本页所属的九层框架
- [[RAG-检索增强生成]] — RAG 的六步流水线详解
- [[Agent三阶段演变]] — Agent 从符号主义到 LLM 的演进
- [[REACT-推理与行动架构]] — Agent 的核心执行循环
- [[Code-AI的Affordance]] — 为什么 code 是 Agent 的最佳 affordance
- [[Dify-开源LLM应用平台]] — Workflow AI 的开源实现
- [[微调vs RAG-决策]] — 知识进 RAG 还是进微调
