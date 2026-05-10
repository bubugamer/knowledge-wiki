---
title: Dify — 开源 LLM 应用开发平台
created: 2026-04-28
last_updated: 2026-04-28
status: 草稿
tags: [AI平台, LLMOps, 开源, RAG, Agent, Workflow]
sources:
  - 03-Resources/articles/Research/深度调研文档 from gpt/dify调研-整合版.md
  - 03-Resources/articles/Research/深度调研文档 from gpt/dify调研1.md
  - 03-Resources/articles/Research/深度调研文档 from gpt/dify调研2.md
---

> Dify 是一个开源全栈 LLM 应用开发平台，把可视化 Workflow、RAG、Agent、Plugin、MCP、LLMOps 打包成统一体验，目标是让团队从原型到生产部署一站完成。

## What It Is

Dify（由 LangGenius 运营）是一个面向企业和开发者的 AI 应用开发平台。它不是单点工具或底层框架，而是把"搭建 → 接模型 → 接知识 → 接工具 → 调试 → 观测 → 发布 → 企业部署"的完整路径做成统一产品。

- **GitHub**：`langgenius/dify`，139k stars，22k forks（2026-04-28）
- **许可**：Dify Open Source License（主仓库；早期为 Apache 2.0）
- **代码构成**：TypeScript 52.8% + Python 42.6%
- **Release**：161 releases，最新 v1.13.3（2026-03-27）

## How It Works

### 核心能力

| 模块 | 功能 |
|---|---|
| **Workflow** | 可视化拖拽编排数据源、模型调用和工具节点 |
| **RAG** | 文档上传、向量索引、多模式检索；支持 Notion 同步和网页爬取 |
| **Agent** | 多角色智能体，内置 50+ 工具 |
| **Plugin 体系** | v1.0.0 后 models/tools 全面 plugin 化；类型含 models、tools、agent strategies、extensions |
| **MCP 双向连接** | 接入外部 MCP server，也可将 Dify app 暴露为 MCP server |
| **LLMOps** | 应用性能跟踪、日志、标注，辅助优化 |
| **BaaS** | 所有功能可通过后端 API 调用 |

### 架构

三层结构：**数据层**（文档/知识库/向量存储）→ **模型层**（多模型管理，支持 OpenAI/Anthropic/Google/Cohere/Llama/Ollama 等）→ **应用层**（Workflow/Agent），辅以监控层。

### 产品线

| 产品 | 形态 | 价格 |
|---|---|---|
| Cloud Sandbox | SaaS | 免费（200 credits） |
| Cloud Professional | SaaS | $59/workspace/月 |
| Cloud Team | SaaS | $159/workspace/月 |
| Community Edition | 自部署 | 软件免费 |
| Enterprise | 私有化 | 定制报价 |
| AWS Premium | Marketplace | 商业报价 |

### 部署

支持 Docker Compose、Kubernetes（Helm/YAML）、Terraform（Azure/GCP）、AWS CDK（EKS/ECS）、Alibaba Cloud。

## Key Properties

- **定位一句话**："不是最底层的 framework，也不是最广义的 automation hub，而是强调可视化开发、生产部署、私有化主权和企业落地的一体化 AI 应用平台"
- **用户规模**：10,000+ 团队，150+ 国家，60+ 行业，1M+ Applications（官网口径）
- **具名客户**：Maersk、ETS、Anker Innovations、Novartis
- **融资**：2026-03 完成 3000 万美元 Pre-A（红杉中国领投），估值约 1.8 亿美元
- **竞争对位**：同时对位可视化自动化（n8n）、可视化 AI builder（FlowiseAI）、代码优先框架（LangChain/LangGraph）、数据/RAG 层（LlamaIndex）、云厂商 AI 底座
- **商业模式**：开源分发获客 → Cloud 自助订阅转化 → Enterprise 私有化放大利润 → Plugin/Template 生态留存

## 与 RAG 的关系

Dify 内置了完整的 RAG pipeline 作为核心模块之一。它不是单独的 RAG 框架，而是把 RAG 作为平台能力的一部分，与 Workflow/Agent/Plugin 协同工作。这使得 Dify 的 RAG 实现更偏"产品化"而非"框架化"——用户通过 UI 配置即可完成文档上传、索引、检索和回答生成。

<!-- status: 草稿 — 数据主要来自 GPT 生成的调研报告，核心数字需回源核验 -->

## Related Pages

- [[RAG-检索增强生成]] — Dify 的核心模块之一，内置完整 RAG pipeline
- [[Agent三阶段演变]] — Dify 的 Agent 模块对应 LLM+推理阶段
- [[LangGenius-Dify母公司]] — Dify 的运营主体与公司结构
- [[张路宇-Dify创始人]] — Dify 创始人兼 CEO
