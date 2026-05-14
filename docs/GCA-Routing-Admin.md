---
title: Genesys Cloud Architect — 路由配置与 ACD 策略
created: 2026-05-13
last_updated: 2026-05-13
status: 草稿
tags: [联络中心, CCaaS, 流程编排, IVR, Genesys, 路由]
sources:
  - Genesys Cloud 官方文档
  - Genesys Cloud Resource Center (Release Notes 2025-08 ~ 2026-03)
  - SynologyDrive/archive/work-mx/02-Areas/gca调研/ 下的调研文档
---

> Admin > Routing 是 Genesys Cloud 中决定"交互何时、去哪、给谁"的统一控制面板。它将号码/地址绑定到 Architect Flow，并通过日程、紧急覆盖、ACD 策略控制交互的完整路由路径。

## 总览

Admin > Routing 包含 10 个子页面：

| # | 菜单项 | 作用 | 许可依赖 |
|---|--------|------|---------|
| 1 | Interaction Routing (ACD) | 概念文档入口，无可配置参数 | — |
| 2 | Work Automation | 管理 Work-item 任务流 | Work Automation 附加许可 |
| 3 | Schedules | 营业时间 / 假日时间段定义 | 基础 |
| 4 | Schedule Groups | 多日程打包复用 | 基础 |
| 5 | Call Routing | 号码 → Inbound Call Flow 映射 | 基础 |
| 6 | Message Routing | 消息地址 → Inbound Message Flow | 基础 |
| 7 | Direct Routing | 直连指定坐席，绕过队列 | Direct Routing 功能开关 |
| 8 | Emergencies | 紧急组开关，覆盖正常路由 | 基础 |
| 9 | Data Tables | IVR 本地数据表 | 基础 |
| 10 | Flow Outcomes & Milestones | 自助流程分析指标 | 基础 |

> Data Tables 和 Flow Outcomes/Milestones 的详细说明见 [[GCA-Resources-Permissions]]。

---

## Call Routing（号码→流程映射）

**路径**：Admin > Routing > Call Routing

每条 Call Route 将一个或多个 DID / 免费号码映射到 Architect Inbound Call Flow。

### 路由模式

| 模式 | 行为 |
|------|------|
| **Always** | 所有来电固定路由到一个 Flow，忽略日程 |
| **Schedule-based** | 关联 Schedule Group，按时段选择 Open Flow / Closed Flow |

### 关键配置字段

| 字段 | 说明 |
|------|------|
| Name | 路由名称 |
| Addresses | DID / 免费号码（支持多个） |
| Division | 所属分区 |
| Schedule Group | 关联的日程组（Schedule-based 模式） |
| Open Flow | 营业时间执行的 Flow |
| Closed Flow | 非营业时间执行的 Flow |
| Emergency Group | 关联的紧急组 |
| Emergency Flow | 紧急启用时执行的 Flow |

### 路由优先级

```
Emergency Group 激活？ ──是──→ Emergency Flow
       │否
Schedule Group 匹配 Holiday？ ──是──→ Holiday Flow（如已配置）
       │否
当前时间在 Open Schedule 内？ ──是──→ Open Flow
       │否
       └──→ Closed Flow
```

---

## Message Routing（消息地址→流程映射）

**路径**：Admin > Routing > Message Routing

将消息渠道地址映射到 Inbound Message Flow，结构与 Call Routing 类似。

### 支持的渠道

| 渠道 | 地址类型 |
|------|---------|
| WhatsApp | Business 号码（支持嵌入式注册，分钟级开通） |
| SMS | 长码 / 免费号码 |
| Facebook Messenger | Facebook 页面 |
| Instagram DM | Instagram 业务账户 |
| Apple Messages for Business | Apple Business ID |
| X (Twitter) DM | X 账户 |
| LINE | 通过 Open Messaging 集成 |
| Web Messaging | Genesys Messenger Widget |

消息 Flow 内可调用 Digital Bot Flow 实现自助服务，再 Transfer to ACD 进入队列。

---

## Email Routing

邮件路由可直接指向队列，也可路由到 **Inbound Email Flow**。

- Email Flow 内通过 `Evaluate Schedule` 判断工作时间
- 支持自定义发件人名称和域名（`mypurecloud.com` 或自有域名）
- 邮件 Flow 可运行数小时（非实时渠道），适合复杂分拣逻辑

---

## Schedules & Schedule Groups

### Schedule（日程）

- 命名时间块，包含时区、日期范围、循环规则
- 属于一个 Division
- 可被 Call Route / Message Route / Architect Flow（`Evaluate Schedule`）引用

### Schedule Group（日程组）

- 将多个日程捆绑为一个对象，按类型标记：
  - **Open**：营业时间
  - **Closed**：非营业时间（默认兜底）
  - **Holiday**：假日覆盖
- 支持时区和夏令时自动调整
- 优先级逻辑：**Emergency > Holiday > Open > Closed**

---

## Emergency Groups

**路径**：Admin > Routing > Emergencies

- 简单的**开/关切换**，激活后覆盖关联 Call Route 的正常路由
- 每条 Call Route 可关联独立的紧急组（不同站点可独立激活）
- 激活/停用即时生效（Emergencies 页面点击 Activate/Deactivate + Save）
- **典型场景**：自然灾害、系统故障、建筑关闭、恶劣天气

---

## Direct Routing

- 将交互**直接路由到指定坐席**，完全绕过队列等待
- 支持渠道：语音、邮件、聊天、消息、语音信箱、回拨
- 不支持：外呼活动（除座席预览记录）、预约回拨
- 通过 Architect 的 `Transfer to ACD` Action 配置坐席/分数对（默认最多 20 对，可扩展到 100）
- **与 Preferred Agent 的区别**：Direct Routing 完全跳过队列；Preferred Agent 先尝试偏好坐席，失败后回落到队列

---

## ACD 路由策略

路由策略在**队列级别**配置（Admin > Contact Center > Queues > Routing 标签页）。

### 路由方法

| 方法 | 机制 | 适用场景 |
|------|------|---------|
| **Standard** | 按技能匹配，分配第一个可用坐席 | 通用场景 |
| **Bullseye** | 最多 6 层同心环，从最严格技能匹配逐层放宽 | 先找专家，找不到再扩大范围 |
| **Preferred Agent** | 优先路由到评分最高的偏好坐席（最多 6 层），偏好坐席可跳过技能要求 | VIP 客户、续单场景 |
| **Conditional Group Routing (CGR)** | 根据实时条件（如近 30 分钟 SL%）路由到特定坐席组 | 动态调度 |
| **Predictive Routing** | AI/ML 驱动，详见下文 | 优化 KPI |

### 技能评估方法

| 方法 | 行为 |
|------|------|
| **All Skills Matching** | 坐席须拥有所有请求技能 |
| **Best Available Skills** | 评估前 100 名坐席，选择平均技能熟练度最高者 |
| **Disregard Skills, Next Agent** | 忽略技能，分配第一个可用坐席 |

语言技能独立于 ACD 技能，拥有请求语言的坐席自动优先。

### Bullseye Routing 展开机制

```
Ring 1（最严格）: 精确匹配所有技能 + 最高熟练度
  ↓ 超时
Ring 2: 放宽部分技能要求 或 加入更多坐席组
  ↓ 超时
Ring 3~6: 继续放宽，直到匹配到坐席
```

每层可独立配置：增加坐席组 或 放宽技能要求。

### Conditional Group Activation（2025-08 新增）

- CGR 的增强：根据队列实时指标（如 SL%、等待人数）动态**激活/停用坐席组**
- 无需人工干预，系统自动响应流量变化

### Predictive Routing（AI 路由）

| 维度 | 说明 |
|------|------|
| 状态 | GA（已全面可用） |
| 支持渠道 | 语音、邮件、异步消息 |
| 配置单位 | 每队列，每队列选择一个 KPI（AHT / 下次联络回避 / 转接率等） |
| 激活流程 | 效益评估 → A/B 对比测试 → 激活（80/20 渐进 → 全量） |
| 模型训练 | 每周自动重训，使用 90 天滚动数据 |
| 透明度 | 白盒模型，不使用 PII |

---

## 2025–2026 路由相关新特性

| 时间 | 特性 | 说明 |
|------|------|------|
| 2025-08 | Conditional Group Activation | 基于队列实时指标动态切换坐席组 |
| 2025-12 | 队列级转录方言 | 可在队列而非仅 Flow 中设置 ASR 方言 |
| 2026-01 | Set Post Flow Action | 挂断后触发后续 Flow（调查/CRM 更新） |
| 2026-01 | Customer Intent Taxonomy | 平台级归一化意图信号，可用于路由上下文 |
| 2026-02 | Predictive Routing 仪表盘增强 | 队列级 KPI/流量汇总视图 |
| 2026-02 | Get Assigned Customer Intents | Bot Flow 中获取最近意图，实现上下文路由 |
| 2026-02 | WhatsApp List Picker | 数字 Bot Flow 中支持交互式列表选择 |
| 2026-03 | Bot Transcription Connector | 接入第三方 ASR 引擎 |

<!-- status: 草稿 — 内容基于 Genesys Cloud 官方文档和 Web 调研，部分细节随版本迭代可能更新 -->

## Related Pages

- [[Genesys-Cloud-Architect]] — Architect 总览
- [[GCA-Actions]] — 组件（Action）分类详解
- [[GCA-Flow-Types]] — Flow 类型详解
- [[GCA-Resources-Permissions]] — 资源类型与权限管理
- [[CCaaS-平台与架构]] — 所属主题页
