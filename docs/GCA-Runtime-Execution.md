---
title: Genesys Cloud Architect — 运行时执行架构
created: 2026-05-14
last_updated: 2026-05-14
status: 草稿
tags: [联络中心, CCaaS, 流程编排, IVR, Genesys, 运行时]
sources:
  - Genesys Cloud 官方文档 (help.mypurecloud.com)
  - Genesys Cloud Developer Center (developer.genesys.cloud)
  - Genesys Cloud 架构白皮书 (genesys.com/capabilities/cloud-architecture)
  - SynologyDrive/archive/work-mx/02-Areas/gca调研/ 下的调研文档
---

> 本文聚焦 Architect Flow 发布后在生产环境中的运行时行为：事件处理、错误恢复、超时机制、执行限制、重试模式、可观测性，以及底层平台架构。

## 1. 事件处理机制 (Event Handling)

### 事件类型

Architect 在运行时可响应以下事件类型（**确认来源：官方文档**）：

| 事件                            | 触发条件                      | 可用 Flow 类型                          |
| ----------------------------- | ------------------------- | ----------------------------------- |
| **Error Event**               | 未捕获的运行时错误、超出 Action 上限    | 所有类型                                |
| **Disconnect Event**          | 客户/系统侧断开连接                | Call Flow、In-Queue Call、Secure Call |
| **Recognition Failure Event** | Bot 无法识别客户回复（NLU 置信度不足）   | Bot Flow、Digital Bot Flow           |
| **Agent Escalation Event**    | 系统检测到客户希望转人工（无需显式 Intent） | Bot Flow、Digital Bot Flow           |
| **No Input Timeout**          | 采集节点等待超时，客户未输入            | Call Flow、Bot Flow                  |
| **No Match**                  | DTMF/语音输入不匹配任何选项          | Call Flow（Menu 节点）                  |

**不支持自定义事件**——事件类型由平台预定义，流程作者只能配置各事件的处理方式（Handling），不能创建新的事件类型。

### 事件处理层级

事件处理遵循二级层级（**确认来源：官方文档**）：

1. **Flow 级（全局默认）**：在 Settings > Event Handling 中配置，作为整个 Flow 的兜底策略。
2. **Task / Menu 级（局部覆盖）**：个别 Task 或 Menu 可覆盖全局设定，例如在特定 Task 中将 Error Event 路由到不同队列。

处理动作（Handling）选项：
- **Disconnect**（默认）
- **Transfer to ACD**（转至指定队列）
- **Jump to Menu**（跳转菜单，启动额外 1,000 Action 配额）
- **Jump to Reusable Task**（跳转可复用任务，同样启动额外配额）

### 跨 Flow 类型差异

- **Bot Flow / Digital Bot Flow**：额外拥有 Recognition Failure Event 和 Agent Escalation Event，这两个事件在 Call Flow 中不存在。
- **Workflow（后台）**：无 Disconnect Event（无实时交互连接），仅有 Error Event。
- **Secure Call Flow**：转接相关的 Failure 路径被平台强制覆盖——转接失败时直接 Disconnect，忽略开发者定义的失败分支。

## 2. 错误处理与恢复 (Error Handling & Recovery)

### Failure Output 分支

许多 Action 提供 Success / Failure / Timeout 三条输出分支（**确认来源：官方文档**）：

- **Call Data Action**：有明确的 Success、Failure、Timeout 三路分支。
- **Transfer 类 Action**：有 Failure 分支（但 Secure Flow 中被平台覆盖为 Disconnect）。
- **Find 类 Action**（Find Queue / User 等）：有 Not Found 分支。
- **简单逻辑 Action**（Decision、Update Data 等）：通常无独立的 Failure 分支。

### 错误信息获取

Failure 分支上可用的错误信息有限。Data Action 的 Failure 路径不会自动暴露 HTTP 状态码或详细错误消息到 Flow 变量中（**确认来源：社区论坛反馈**）。开发者通常需要通过 Participant Data 手动记录故障路径信息来辅助排查。系统层面可在交互记录的 Disconnect Type 和 Error Code 字段查看错误码（如 `error.ininedgecontrol.connection.noAvailableLines`）。

### 未处理错误的行为

当发生未被 Failure 分支捕获的错误时，Flow 进入 Flow 级 Error Event Handler。如果 Error Event Handler 也未配置或自身失败，默认行为是 **Disconnect**（挂断通话）。

### Secure Flow 特殊行为

**确认来源：官方文档**——在 Secure Call Flow 中，所有 Transfer Action（Transfer to ACD / User / Number / Group / Flow / Voicemail）的自定义 Failure 路径被平台覆盖，失败时直接断开。原因：Secure Flow 中使用 Blind Transfer 而非 Consultation Transfer，以避免 VXML 安全问题。

## 3. 超时机制 (Timeout Mechanisms)

| 超时场景                    | 默认值         | 可配置                                  | 说明                                                   |
| ----------------------- | ----------- | ------------------------------------ | ---------------------------------------------------- |
| **No Input Timeout**    | 因 Flow 类型而异 | 是，每个采集节点独立设置                         | 等待客户输入的超时时间                                          |
| **No Match 最大重试**       | 通常 3 次      | 是                                    | 达到上限后进入 Error Event Handling                         |
| **Data Action Timeout** | 60 秒        | 通过 Timeout 分支处理（**推断：超时值本身是否可改待确认**） | 走 Timeout 输出分支                                       |
| **Flow 级执行时长**          | 无统一硬限制      | N/A                                  | Call Flow 短时运行；Email Flow 可达 8h+；Workitem Flow 可持续数天 |
| **Action 上限**           | 10,000 次    | 不可调                                  | 超出后进入 Error Event Handler                            |

Bot Flow 的 No Input Timeout 支持通过 Archy CLI 工具配置（Digital Bot Flow 同样支持）。

## 4. 执行模型 (Execution Model)

### 实例隔离

每个交互（通话/聊天/邮件/工单）独立执行一个 Flow 实例。实例之间天然隔离，无共享状态（**确认来源：官方文档**）。

### Action 执行限制

**确认来源：官方文档**：

- 正常执行上限：**10,000 个 Action**（每个可执行节点计数一次，包括所有 Action 类型，不仅限于 Data Action）。
- Error Handler 额外配额：当正常执行达到 10,000 上限后，如果 Event Handling 配置为 Jump to Menu 或 Jump to Reusable Task，额外获得 **1,000 个 Action** 的执行配额。
- 绝对上限后：执行 **Silent Disconnect**（无提示直接挂断）。
- 注意：进入 Task 不算一个 Action，但进入 Menu 不算。

### 内存与数据限制

- Flow 执行历史中，JSON / String / Collection 类型变量超过存储上限时显示 "ValueTooLarge"。
- Common Module 的大小计入主 Flow 的总大小，可能导致超出 Flow 大小限制（**确认来源：社区论坛**）。
- 具体变量数量上限和单值大小上限未在公开文档中明确标注（**推断：存在限制但无公开数值**）。

### 并发与 Data Action 限速

**确认来源：官方文档**：

- 每个 Org 的 Data Action 并发上限：**50 个同时执行**。
- Data Action 执行速率上限：**2,500 次/分钟**（Org 级）。
- 如果 Data Action 调用 Genesys Cloud 自身 API，额外受 OAuth2 Token 的 **300 次请求** 限制。

## 5. 重试模式 (Retry Patterns)

### Data Action 重试

**无内置自动重试**（**确认来源：官方博客**）。必须在 Flow 中手动实现重试逻辑，通常使用 Loop Action + 计数器变量。Genesys 官方强调**必须设置重试上限**，防止无限循环耗尽 Action 配额或导致 Edge 服务器 CPU 飙升。

推荐模式：
1. 使用 Loop + 计数器变量包裹 Call Data Action。
2. Failure/Timeout 分支中递增计数器。
3. 达到上限后走降级路径（Transfer to ACD 或播放错误提示）。
4. 调用前验证输入变量有效性，避免可预见的失败。
5. 考虑使用 Data Table 做响应缓存，减少重复调用。

### ASR/NLU 重试

Bot Flow 在低置信度时自动重新提示（re-prompt），达到 Max Retry 次数后触发 Recognition Failure Event，进入 Event Handler。

### Transfer 重试

Transfer Action 的 Failure 分支可以跳回重试逻辑（仅限非 Secure Flow）。Secure Flow 中转接失败直接断开，无法重试。

## 6. 可观测性与调试 (Observability & Debugging)

### Debug 模式

**确认来源：官方文档**：

- 使用方式：Architect 中选择 Debug（而非 Publish），拨打 `YourCallFlow-debug@localhost` 触发。
- 提供 Action 执行顺序、Decision 结果、变量值等额外信息。
- 限制：仅支持英文语言 Flow；运行独立的调试版本（不影响生产已发布版本）。
- 本质是用真实通话测试未发布的 Flow 版本。

### Flow 执行历史 (Historical Execution Data)

**确认来源：官方文档**——默认关闭，需手动启用。四个数据级别：

| 级别 | 内容 |
|------|------|
| **Base** | 高层级用户旅程：Action 路径、菜单导航、错误、事件 |
| **Notes** | + 变量值（用于优化） |
| **Verbose Notes** | + 通信内容（对话文本） |
| **All** | + Action 输入/输出值（完整调试） |

注意事项：
- 执行数据计入 Org 存储配额（Fair Use Policy）。
- 加密变量（Secure 变量）通常显示 "ValueTooLarge"。
- 通过 Replay Mode 可在 Architect UI 中回放执行过程，支持断点和变量追踪。

### 分析功能

- **Flow Outcomes**：通过 Initialize Flow Outcome Action 追踪自助服务成功/失败率。上限 100 个 Outcome / Org。
- **Flow Milestones**：Outcome 内的细粒度里程碑。上限 1,000 个 / Org，报告层面每 Outcome 最多 20 个。
- **Query Builder**：按 Flow 启动/结束方式、个别 Action 执行条件查询执行数据。
- **跨 Flow 追踪**：可在 IVR Flow 中初始化 Outcome，在后续 Secure/Triggered Flow 中记录结果（**确认来源：社区讨论**）。

### 告警

无内置的 Flow 错误告警机制。可通过 Event Bridge 集成（如 AWS EventBridge）将 Flow Instance Execution Error Event 推送到外部监控系统（**确认来源：开发者事件目录**）。

## 7. 底层运行时架构 (Runtime Architecture)

### 平台架构

**确认来源：官方架构页面**：

- **微服务 + API-first**：Genesys Cloud 采用微服务架构，服务间通过 API 通信。
- **弹性伸缩**：使用 AWS ELB + Auto Scaling Groups (ASG)，按服务级策略自动扩缩容。
- **Serverless 混合**：较新的服务采用 Serverless 技术，按需响应负载变化。IVR/Media 处理是否为 Serverless 未明确说明（**推断：Media Tier 可能仍为容器/VM 模型，因为涉及实时音频处理**）。
- **自愈能力**：ELB 健康检查检测到不健康实例后自动摘除并替换。

### 地理分布

- **Core Region**：每个 Org 绑定一个 AWS Region（跨 3 个 AZ，Active/Active/Active 模式）。
- **Satellite Media Region**：通过 Global Media Fabric 将语音/视频媒体路由到离用户最近的区域，降低延迟。
- Flow 逻辑执行在 Core Region，媒体流走 Satellite Region（**推断**）。

### SLA

官方承诺高可用 SLA，最高可达 **100% 信用担保**。具体数值取决于合同等级。

### 冷启动 / 延迟特征

Media Tier 发布说明中提到过改进 "VXML Engine 启动时加载内置语法" 的可靠性，暗示存在引擎初始化过程。具体的冷启动延迟数值未公开（**推断：由于常驻服务+预热池，生产环境下冷启动影响极小**）。

---

**标注说明**：
- "确认来源：官方文档" = 来自 help.mypurecloud.com 或 developer.genesys.cloud 的明确描述
- "确认来源：社区论坛/博客" = 来自 Genesys 官方论坛或开发者博客
- "推断" = 基于已有信息和架构常识的合理推断，未被官方文档明确证实

<!-- status: 草稿 — 部分超时默认值和内存限制的精确数值待核验 -->

## Related Pages

- [[Genesys-Cloud-Architect]] — Architect 总览
- [[GCA-Actions]] — 组件（Action）分类详解
- [[GCA-Variables]] — 变量与表达式体系
- [[GCA-Flow-Types]] — Flow 类型详解
- [[GCA-Resources-Permissions]] — 资源类型与权限管理
- [[CCaaS-平台与架构]] — 所属主题页
