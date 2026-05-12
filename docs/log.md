# Wiki 活动日志

## [2026-05-12] ingest | GCA Variables 变量体系页

- 新建：GCA-Variables（变量分类与作用域、数据类型体系、系统预置变量、变量配置选项、关键 Action 中的变量行为、设计限制）
- 更新：Genesys-Cloud-Architect（变量体系章节改为简表+详情链接）
- 更新：CCaaS-平台与架构（新增 GCA Variables 条目）
- 更新：mkdocs.yml nav（新增 GCA Variables）
- 来源：SynologyDrive/archive/work-mx/02-Areas/gca调研/ 下的调研文档（变量体系结构.pdf、Variable Prefixes and Scopes.pdf、gca default data.md、genesys_architect_data.md）

## [2026-05-12] ingest | GCA Actions 组件详解页

- 新建：GCA-Actions（组件分类详解：用户交互、数据操作、路由转接、逻辑分支、动态查找、AI/NLU、流程管理、任务管理、表达式系统、管理配置）
- 更新：CCaaS-平台与架构（新增 GCA Actions 条目）
- 更新：mkdocs.yml nav（新增 GCA Actions）
- 来源：SynologyDrive/archive/work-mx/02-Areas/gca调研/ 下的调研文档

## [2026-05-12] ingest | GCA vs Dify Workflow 对比页

- 新建：GCA-vs-Dify-Workflow（组件映射、变量体系、多渠道策略、版本管理、结构性差异）
- 更新：Genesys-Cloud-Architect（移除所有 Dify 引用，GCA 作为独立知识页）
- 更新：CCaaS-平台与架构、mkdocs.yml（新增对比页条目）
- 来源：从 Genesys-Cloud-Architect 原有对比内容拆分独立

## [2026-05-12] ingest | GCA Flow Types

- 新建：GCA-Flow-Types（15 种流程类型详解：一览表、能力矩阵、协作模式图、设计哲学）
- 更新：Genesys-Cloud-Architect（Flow 类型章节改为简表+详情链接）
- 更新：CCaaS-平台与架构（新增 GCA Flow Types 条目）
- 更新：mkdocs.yml nav（新增 GCA Flow Types）
- 来源：用户提供的 Genesys flow types 调研报告（精简后约为原文 1/4 篇幅）

## [2026-05-12] maintenance | 首页改造为二级目录结构

- 重构：index.md 精简为只展示一级/二级主题，文章链接下沉到主题页
- 新建主题页（10 个）：AI-总览与框架、AI-训练阶段、AI-方法与对比、AI-应用架构、AI-多模态、AI-行业应用、AI-前沿议题、AI-术语与参考、AI产品与公司、CCaaS-平台与架构
- 新建一级分类：联络中心 / CCaaS
- 新建文章：Genesys-Cloud-Architect（含 Flow 类型、组件分类、变量体系、与 Dify Workflow 对比）
- 来源：Dify 面试准备行动计划 → 行动 1 双平台对齐表

## [2026-05-10] ingest | 量化交易中的 AI

- 新建：量化交易中的AI（行业应用页：学习范式选择、模型架构、训练流水线、与 LLM 的区别）
- 更新：index.md（新增"行业应用"大类，机器人与具身智能归入其下，新增量化交易子分组）
- 更新：mkdocs.yml nav 结构同步调整
- 来源：用户问答 + 用户提供的量化 AI 分析文本

## [2026-05-10] maintenance | 路径迁移

- wiki 源头统一为 `_wiki/docs/`，废弃 vault 级别的 `_wiki-index.md` 和 `_wiki-log.md`
- llm-wiki skill 路径全部更新指向 `docs/`

## [2026-05-09] ingest | MoE 混合专家模型

- 新建：MoE-混合专家模型（概念页：稀疏计算、Router、负载均衡、DeepSeek 路线、行业双线并进）
- 更新：模型架构-ModelArchitecture（MoE 相关段落增加详情链接）
- 更新：index.md（总览与框架小节新增 1 条）
- 来源：用户提供的 MoE 问答文本

## [2026-05-06] ingest | AI技术体系九层框架

- 新建：AI技术体系总览、学习范式-LearningParadigm、模型架构-ModelArchitecture、AI系统形态-SystemArchitecture
- 更新：index.md（总览与框架小节新增 4 条）
- 来源：用户提供的"当前 AI 主流技术体系（严格分层版）"文本

## [2026-05-06] query | 训练阶段 vs 学习范式区分

- 更新：学习范式-LearningParadigm（新增"易混淆：训练阶段 vs 学习范式"一节）
- 更新：LLM训练四阶段总览（新增"注意：阶段名 ≠ 学习范式"备注）
- 来源：对话中讨论"预训练是否等于自监督学习"收束后的结论

## [2026-05-06] query | SSL ≠ NTP 澄清

- 更新：学习范式-LearningParadigm（修正表格中 SSL 的典型用途描述，修正 LLM 训练范式组合中 Pre-training 的说明）
- 来源：对话中讨论"Self-supervised Learning 是否等于 Next Token Prediction"收束后的结论
