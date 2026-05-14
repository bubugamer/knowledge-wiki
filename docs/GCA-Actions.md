---
title: Genesys Cloud Architect — Actions（组件）
created: 2026-05-12
last_updated: 2026-05-12
status: 草稿
tags: [联络中心, CCaaS, 流程编排, IVR, Genesys]
sources:
  - Genesys Cloud 官方文档
  - SynologyDrive/archive/work-mx/02-Areas/gca调研/ 下的调研文档
---

> Architect 的组件（Action）是流程的最小执行单元。不同 Flow 类型可用的 Action 集合不同，由渠道特性和安全策略决定。

## 用户交互

面向客户的输入/输出组件，按渠道分为语音系和数字系。

| Action | 适用 Flow 类型 | 功能 | 关键限制 |
|--------|--------------|------|---------|
| **Ask for Intent** | Dialog Bot Flow | 开放式提问，NLU 引擎将回答分类到已配置的 Intent | Digital Bot Flow 不可用（用 Digital Menu / Wait for Input 替代） |
| **Ask for Yes/No** | Dialog + Digital Bot | 二元确认问题（是/否） | 需预先定义 yes/no Intent |
| **Ask for Slot** | Dialog + Digital Bot | 采集特定数据（账号、日期、电话等），按 Slot Type 校验 | 未识别输入触发重问；配合 Clear Slot + Loop 实现重试 |
| **Digital Menu** | Digital Bot Flow | 聊天/消息渠道的按钮菜单，每个选项对应一个分支 | 仅数字渠道，语音不可用 |
| **Wait for Input** | Digital Bot Flow | 等待用户自由文本输入，不做 NLU 分类 | 仅数字渠道；返回原始文本 |
| **Communicate** | 所有 Flow 类型 | 单向输出（TTS/录音/文本），不等待回复 | 仅输出，不采集输入 |
| **Collect Input (DTMF)** | 语音 Flow | 按键采集（含超时、最大尝试次数配置） | 仅语音渠道 |
| **Play Audio / Play TTS** | 语音 Flow | 播放预录语音文件 / 文本转语音 | 仅语音渠道 |
| **Send Response** | Chat / Message Flow | 向聊天/消息会话发送文本回复 | 仅数字渠道 |
| **Send Auto Reply** | Email Flow | 发送自动回复邮件 | 仅邮件 Flow |

---

## 数据操作

后端数据查询、变量赋值、外部 API 调用。

| Action | 适用 Flow 类型 | 功能 | 关键限制 |
|--------|--------------|------|---------|
| **Call Data Action** | 所有 | 调用已配置的 Data Action（REST API、CRM 查询、Lambda 等）；映射输入/输出参数；有 Success/Failure 分支 | 默认超时 60s；仅支持 JSON（不支持 XML）；不能控制交互状态（不能转接/挂断） |
| **Call Secure Data Action** | Secure 语音 Flow | 同上，但在 PCI 安全模式下执行 | 仅 Secure Flow 内可用；Data Action 须标记为 PCI 合规 |
| **Data Table Lookup** | 所有 | 按 Key 查询 Genesys 内置数据表，返回匹配行 | 单表最大 50K 行 × 100 列；精确匹配查询；~20ms 延迟 |
| **Update Data** | 所有 | 变量赋值（支持多条赋值语句，可自动创建变量） | 纯赋值，无分支 |
| **Extract Secure Data** | Secure 语音 Flow | 将加密安全变量值复制到非安全变量 | 仅 Secure Flow；会暴露敏感数据，慎用 |
| **Get Response** | Email / Message Flow | 从 Response Library 获取预设回复模板 | 仅邮件/消息 Flow；模板不存在走 Failure 分支 |
| **Set Participant Data** | 语音 / 数字 Flow | 向会话对象附加键值对，跨 Flow 转接时持久化 | 仅支持基础类型（string/int/decimal/boolean） |
| **Get Participant Data** | 语音 / 数字 Flow | 读取会话上已设置的 Participant Data | Key 不存在返回 NOT_SET |

### Data Action 集成类型

Call Data Action 的后端连接器，决定了能调用什么外部系统：

| 集成类型 | 预置 Action | 自定义 Action | 典型用途 |
|---------|-----------|-------------|---------|
| **Genesys Cloud API** | Get Estimated Wait Time / User Presence / Routing Status | 可调用任意平台 REST API | 内部数据查询 |
| **Genesys Cloud Function** | — | 上传自定义代码（Genesys 托管 Lambda） | 不需要自有 AWS 账号；适合 SOAP/SDK 服务 |
| **AWS Lambda** | — | 调用客户自有 Lambda | 需客户 AWS IAM 配置 |
| **Google Cloud** | — | Google Cloud APIs / Cloud Functions | Google 生态集成 |
| **Salesforce** | 6 个（按电话/邮件/ID 查 Account/Contact/Case） | 支持 | CRM 查询 |
| **Microsoft Dynamics 365** | 10 个（Account/Contact/Case 多维查询） | 支持 | CRM 查询 |
| **Zendesk** | 9 个（Ticket/User/Organization 查询） | 支持 | 工单系统 |
| **Web Services** | 4 个模板（天气/日历示例） | 任意 REST/JSON 端点 | 通用 HTTP；支持 Basic Auth / OAuth 2.0 / API Key / mTLS |

---

## 路由与转接

控制交互去向的组件。

| Action | 适用 Flow 类型 | 功能 | 关键限制 |
|--------|--------------|------|---------|
| **Transfer to ACD** | 所有交互 Flow | 转座席队列；可设转接前音频、覆盖 In-Queue Flow | 参数须为 Queue 对象（不支持字符串）；执行后当前 Flow 结束 |
| **Transfer to Number** | 语音 Flow | 转外部电话号码 | 须 E.164 格式 PhoneNumber 类型 |
| **Transfer to User** | 语音 Flow | 转指定 Genesys 用户/坐席 | 须先通过 Find User 获取 User 对象 |
| **Transfer to Flow** | 语音 / 数字 Flow | 转接到另一个已发布的 Architect Flow | 目标须已发布；调用者需 view 权限 |
| **Transfer to Secure Flow** | 语音 Flow | 转入 PCI 安全流程 | 用于支付/敏感数据采集 |
| **Return to Agent** | Secure Call Flow | 安全流程结束后接回原坐席 | 仅坐席发起的 Secure Flow 可用 |
| **Disconnect** | 语音 Flow | 挂断；可设挂断前音频 | 仅语音 |
| **Exit Bot Flow** | Bot Flow | 终止机器人对话，将控制权交回主流程 | 执行后无后续 Action |

---

## 逻辑与分支

流程控制组件。

| Action | 适用 Flow 类型 | 功能 | 关键限制 |
|--------|--------------|------|---------|
| **Decision** | 所有 | 布尔条件分支（Yes / No） | 仅支持单个布尔表达式 |
| **Switch** | 所有 | 多路分支匹配（类似 switch-case） | 最大 64 个 case；类型须一致 |
| **Evaluate Schedule** | 所有 | 判断当前时间是否在预定义日程内（Active / Inactive） | 须预配置 Schedule 对象 |
| **Evaluate Schedule Group** | 所有 | 判断日程组状态（Open / Closed）；优先级：紧急 > 假日 > 营业 > 关闭 | 须预配置 Schedule Group |
| **Loop / Loop Until** | 所有 | 按次数、集合遍历或条件循环 | 用 Exit Loop / Next Loop 控制流 |
| **Anything Else? Loop** | Dialog Bot Flow | 询问用户"还有其他问题吗"，决定继续或退出 | 仅 Dialog Bot（Digital Bot 不可用） |

---

## 动态资源查找（Find）

在运行时按名称或 ID 查找 Genesys 平台对象，返回 Found / Not Found 分支。

| Action | 查找对象 | 备注 |
|--------|---------|------|
| **Find Queue / Find Queue by ID** | ACD 队列 | — |
| **Find User / Find User by ID** | 平台用户 | Find Users by ID 支持批量（最多 50 个） |
| **Find Skill** | ACD 技能 | — |
| **Find Language Skill** | 语言技能 | 用于多语言路由 |
| **Find Schedule / Find Schedule Group** | 日程 / 日程组 | — |
| **Find Emergency Group** | 紧急组 | 不区分大小写；单 Flow 最多 100 次动态查找 |
| **Find Grammar / Find Grammar by ID** | ASR 语法资源 | 仅语音 Flow；名称区分大小写 |
| **Find System Prompt / Find User Prompt** | 提示音资源 | — |
| **Find Utilization Label** | 利用率标签 | 用于坐席工作量管理 |

---

## AI / NLU（Bot Flow 专属）

Bot Flow 的对话 AI 配置组件，非运行时 Action，而是设计时配置。

| 组件 | 功能 | 关键限制 |
|------|------|---------|
| **Intents** | 定义用户意图；每个 Intent 配训练语料（建议 15-30 条） | 单 Bot 最多 100 个 Intent；保留名 "None" / "Knowledge" 不可用 |
| **Slots** | 从用户输入中提取关键数据（日期、数字、姓名等） | 每个 Slot 须映射至少一个 Slot Type 值 |
| **Slot Types** | 定义数据格式：内置（date/time/number）、自定义列表、动态列表、正则 | 内置类型 NLU 支持最好；正则 NLU 支持有限 |
| **Knowledge** | 关联已发布的知识库，实现 FAQ 式问答 | 可能与 Intent 冲突；需通过响应优先级配置管理 |
| **Intent Miner** | 分析历史坐席对话，自动提取 Intent 和训练语料 | 需要足够的历史对话数据 |
| **Intent Health** | 评估训练质量；标记混淆/重复/离群语料 | 每 Intent 至少 2 条语料才可用 |
| **NLU Test Tool** | 用任意输入测试 Intent 识别，查看置信度分布 | 需先训练模型 |
| **Set Intent** | 运行时预设 Intent，下次 Ask for Intent 跳过用户输入 | 仅 Dialog Bot Flow；用于测试或上下文驱动场景 |
| **Clear Slot** | 重置已采集的 Slot 值为 NOT_SET | 配合 Loop 实现重试 |

---

## 流程管理与分析

| Action | 适用 Flow 类型 | 功能 | 关键限制 |
|--------|--------------|------|---------|
| **Set Language** | 所有 | 切换会话语言（IETF 代码） | 语音 Flow 在当前 Task 结束后生效；消息/邮件立即生效 |
| **Initialize Flow Outcome** | 所有 | 开始追踪自助服务结果指标 | 单组织最多 100 个 Outcome；创建后不可删除 |
| **Set Flow Outcome** | 所有 | 标记 Outcome 为成功/失败 | 须先 Initialize；跨 Flow 转接后不保留 |
| **Add Flow Milestone** | 所有 | 记录 Outcome 中的中间检查点 | 单实例最多 20 个；单组织最多 1000 个 |
| **Set Screen Pop** | 语音 Flow | 坐席接听时弹屏脚本，可传变量 | 须已发布 Script + view 权限 |
| **Set / Clear Utilization Label** | 所有 | 标记会话用于坐席容量管理 | 无会话上下文时可能失败 |

---

## 任务管理（Flow 内部结构）

| 概念 | 说明 |
|------|------|
| **Task** | Flow 内的命名子过程，将相关 Action 分组 |
| **Call Task** | 调用同 Flow 内另一个 Task，执行完返回调用点 |
| **Jump to Reusable Task** | 跳转到全局共享的可重用 Task，**不返回**调用点 |
| **End Task** | 以命名输出路径结束当前 Task（仅 Email/Message Flow） |
| **Call Common Module** | 调用跨 Flow 的可复用子流程；动作集为所有兼容类型的交集；**不可嵌套**；被引用时锁定版本快照 |

<!-- status: 草稿 — 内容基于 Genesys Cloud 官方文档和内部调研文档，部分细节待核验 -->

## Related Pages

- [[Genesys-Cloud-Architect]] — Architect 总览
- [[GCA-Flow-Types]] — 15 种 Flow 类型详解
- [[CCaaS-平台与架构]] — 所属主题页
