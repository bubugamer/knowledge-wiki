---
title: Genesys Cloud Architect
created: 2026-05-12
last_updated: 2026-05-12
status: 草稿
tags: [联络中心, CCaaS, 流程编排, IVR]
sources:
  - Genesys Cloud 官方文档
visibility: public
---

> Genesys Cloud Architect 是 Genesys Cloud CX 平台的可视化流程编排工具，用于设计 IVR、语音机器人、数字渠道交互和工作流。

## 介绍

Architect 是 Genesys Cloud 的拖拽式流程设计器（Flow Designer），覆盖从来电接入到座席分配的全链路交互逻辑。管理员和流程开发者通过可视化画布编排业务流程，无需编写代码即可实现复杂的自助服务和路由策略。

## Flow 类型

Architect 支持 15 种 Flow 类型，按交互渠道和功能场景划分。详见 **[Flow Types 详解](GCA-Flow-Types.md)**。

简表：

| 类别 | Flow 类型 | 核心职责 |
|------|-----------|---------|
| 语音 | Inbound / Outbound Call | IVR 主流程、外呼自动化 |
| | In-Queue Call | 排队等待体验 |
| | Secure Call | 敏感数据采集（PCI 合规） |
| | Voicemail / Voice Survey | 留言、通话后满意度调查 |
| 数字 | Inbound Chat / Email / Message | 数字渠道路由与自动应答 |
| 机器人 | Bot Flow / Digital Bot Flow | NLU 多轮对话（语音+文本 / 纯文本） |
| 后台 | Common Module | 可复用子流程 |
| | Workflow | 事件驱动后台自动化 |
| | Workitem Flow | 工单生命周期管理 |
| | Survey Invite Flow | 调查邀请邮件发送 |

## 核心组件（Action）

Action 是流程的最小执行单元，不同 Flow 类型可用的 Action 集合不同。详见 **[GCA 组件详解](GCA-Actions.md)**。

按功能域分为六大类：

| 功能域 | 代表组件 | 说明 |
|--------|---------|------|
| 用户交互 | Ask for Intent / Slot, Communicate, Collect Input, Digital Menu | 面向客户的输入/输出，按渠道分语音系和数字系 |
| 数据操作 | Call Data Action, Data Table Lookup, Update Data, Set Participant Data | 后端数据查询、变量赋值、外部 API 调用 |
| 路由与转接 | Transfer to ACD / Number / User / Flow, Disconnect | 控制交互去向 |
| 逻辑与分支 | Decision, Switch, Loop, Evaluate Schedule | 流程控制 |
| 动态查找 | Find Queue / User / Skill / Language Skill / Schedule | 运行时按名称或 ID 查找平台对象 |
| AI / NLU | Intents, Slots, Knowledge, Intent Miner | Bot Flow 的对话 AI 配置 |

## 变量体系

详见 **[GCA 变量与表达式体系](GCA-Variables.md)**。

简表：

| 维度 | 说明 |
|------|------|
| 变量分类 | Flow 变量 / Task 变量 / Input-Output 变量 / 系统上下文变量 / Participant Data |
| 类型系统 | 原生类型（String, Integer, Boolean, DateTime, Duration 等）、复合类型（Collection, JSON, PhoneNumber, EmailAddress）、网络引用类型（User, Queue, Skill 等） |
| 传递方式 | Flow 内直接引用；跨 Flow 通过 Input/Output 参数；跨全会话通过 Participant Data |
| 系统变量 | 按渠道前缀：Call.* / Message.* / Chat.* / Email.* / Session.* / System.* |
| 安全变量 | Secure 标记，禁录音/日志，仅 Secure Call Flow 内有效 |

## 版本与发布

| 维度 | 说明 |
|------|------|
| 版本模型 | 每个 Flow 有独立版本号，支持多版本共存 |
| 发布机制 | 编辑 → 保存（草稿）→ 发布（Published）→ 生产生效 |
| 回滚 | 可切回任意历史已发布版本 |
| 灰度 | 不支持原生灰度发布，需通过路由规则或 Data Action 变通实现 |
| 协作 | 同一时间只有一个人可以编辑同一个 Flow（锁定机制） |
| Common Module 版本快照 | 被引用时锁定版本；主流程需重新发布才能取到模块新版 |

## 执行引擎

| 维度 | 说明 |
|------|------|
| 执行模式 | 同步（通话 Flow，毫秒级响应）/ 异步（Workflow，可长时间运行） |
| 超时处理 | 每个采集节点可设置 No Input Timeout、Max Attempts |
| 错误处理 | Failure Output 分支（类似 try-catch），Secure Flow 转接失败直接挂断 |
| 并发 | 每通电话/每个交互独立执行一个 Flow 实例，天然隔离 |
| 可观测性 | Flow 执行日志、Debug 模式（逐步执行、变量查看） |
| 执行时长上限 | Call Flow 短时运行；Email Flow 可达 8+ 小时；Workitem Flow 可能持续数天 |
| Action 执行上限 | 10,000 次/实例，Error Handler 额外 1,000 次，超出后 Silent Disconnect |

深入运行时行为（事件处理、错误恢复、超时、重试、可观测性、底层架构）详见 **[GCA 运行时执行架构](GCA-Runtime-Execution.md)**。

<!-- status: 草稿 — 组件分类基于公开文档和使用经验，部分细节待核验 -->

## Related Pages

- [[GCA-Actions]] — 组件（Action）分类详解：用户交互、数据操作、路由转接、逻辑分支
- [[GCA-Variables]] — 变量与表达式体系：分类、作用域、数据类型、系统变量、内置函数、运算符
- [[GCA-Flow-Types]] — Flow 类型详解：能力矩阵、协作模式、设计哲学
- [[GCA-Resources-Permissions]] — 资源类型与权限管理：Division 分区、RBAC、资源限额
- [[GCA-Routing-Admin]] — 路由配置与 ACD 策略：号码映射、日程、Bullseye、Predictive Routing
- [[GCA-Runtime-Execution]] — 运行时执行架构：事件处理、错误恢复、超时、重试、可观测性、底层架构
- [[GCA-Glossary]] — 术语表：核心概念快速解释与跳转索引
- [[GCA-vs-Dify-Workflow]] — 与 Dify Workflow 的结构性对比
- [[CCaaS-平台与架构]] — 所属主题页
