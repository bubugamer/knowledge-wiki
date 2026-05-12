---
title: Genesys Cloud Architect — Flow Types
created: 2026-05-12
last_updated: 2026-05-12
status: 草稿
tags: [联络中心, CCaaS, 流程编排, IVR, Genesys]
sources:
  - Genesys Cloud Resource Center (help.mypurecloud.com)
  - SynologyDrive/archive/work-mx/02-Areas/gca调研/genesys_flow_types.xlsx
---

> Genesys Cloud Architect 按交互渠道和功能场景将流程划分为 15 种类型，每种类型内置了针对该场景的动作集、校验规则和安全策略。

## 全部 Flow 类型一览

### 语音渠道

| Flow 类型 | 触发方式 | 核心职责 |
|-----------|---------|---------|
| **Inbound Call Flow** | 外部来电匹配号码/DID | IVR 主流程：菜单导航、输入采集、数据查询、路由转接 |
| **Outbound Call Flow** | 外呼活动/API 拨出 | 外呼 IVR：播放通知、采集按键、可转人工；关联联络列表和结束码 |
| **In-Queue Call Flow** | 呼叫进入队列等待 | 排队体验：保持音乐、排队提示、回呼选项；系统提供默认流程 |
| **Secure Call Flow** | 主流程转入 / 坐席发起 | 敏感数据采集（信用卡号等）；自动禁用录音和日志；PCI DSS 合规 |
| **Voicemail Flow** | 呼叫转入语音信箱 | 留言录制：提示音、录音、录后选项（重听/重录）；全局唯一，不可删除 |
| **Voice Survey Flow** | 通话结束后转入 | 电话满意度调查；基于 Survey Form 自动生成问答逻辑；不可自由编辑结构 |

### 数字渠道

| Flow 类型 | 触发方式 | 核心职责 |
|-----------|---------|---------|
| **Inbound Chat Flow** | 网页/APP 聊天接入 | 聊天路由：欢迎语、意图判断、队列分配 |
| **Inbound Email Flow** | 客户邮件到达 | 邮件分类与路由：自动回复、基于主题/正文关键词分配队列 |
| **Inbound Message Flow** | SMS/WhatsApp/社交消息到达 | 消息路由：自动应答、关键词/附件分析、队列分配 |
| **In-Queue Email/Message Flow** | 邮件/消息进入队列等待 | 数字渠道排队体验；无默认流程需手动创建；同一交互最多触发 10 次 |

### 机器人

| Flow 类型 | 调用方式 | 核心职责 |
|-----------|---------|---------|
| **Bot Flow**（Dialog Engine） | 被 Call/Chat/Message Flow 调用 | NLU 驱动的多轮对话；支持语音+文本双渠道；PCI 合规可在 Secure Flow 中使用 |
| **Digital Bot Flow** | 被 Message Flow 调用 | 文本专用机器人；AI 增强槽位解析；**不支持 PCI**，不可在 Secure Flow 中使用 |

### 后台与复用

| Flow 类型 | 触发方式 | 核心职责 |
|-----------|---------|---------|
| **Common Module Flow** | 被其他流程 Call Common Module 调用 | 可复用子流程：定义输入/输出参数；动作集为所有兼容类型的交集；**不可嵌套调用** |
| **Workflow** | 事件触发器 / API 调用 | 后台自动化：调用外部 API、更新 CRM、处理系统事件；无客户交互能力 |
| **Workitem Flow** | 工单事件（创建/指派/超时等） | 工单生命周期管理：状态流转、SLA 监控、通知；每个 Worktype 对应一个 Flow |
| **Survey Invite Flow** | 交互结束后系统触发 | 发送调查邀请邮件（含问卷链接）；轻量流程，主要配置邮件模板 |

---

## 能力矩阵

各类型流程可用的动作集由其交互渠道决定。核心差异如下：

| 能力 | Call 系 | Chat/Email/Msg | Secure | Bot | Workflow | Workitem |
|------|---------|---------------|--------|-----|----------|----------|
| 播放语音 / TTS | Yes | — | Yes | 由平台处理 | — | — |
| DTMF 按键采集 | Yes | — | Yes | 由平台处理 | — | — |
| 发送文本消息 | — | Yes | — | Yes | — | — |
| 发送自动回复邮件 | — | Email only | — | — | — | — |
| 菜单节点 | Yes | — | Yes | — | — | — |
| 条件判断 / Switch | Yes | Yes | Yes | Yes | Yes | Yes |
| Data Action（API 调用） | Yes | Yes | Yes | Yes | Yes | Yes |
| Call Common Module | Yes | Yes | Yes | Yes | Yes | — |
| Call Bot Flow | Yes | Chat/Msg | Secure+Bot 可组合 | — | — | — |
| Transfer to ACD（转队列） | Yes | Yes | Yes（盲转） | — | — | — |
| Transfer to Secure Flow | Yes | — | — | — | — | — |
| 意图/槽位 NLU | — | — | — | Yes | — | — |
| 安全变量（禁录音/日志） | — | — | Yes | — | Yes（部分） | — |
| 多语言提示资源 | Yes | — | Yes | Yes | — | — |

**关键限制**：
- **数字渠道流程**无语音相关动作（播放、按键、录音），无菜单节点，无成功/失败路径分支
- **In-Queue Flow** 禁用菜单和可重用任务；Email/Message 队列流程同一交互最多触发 10 次
- **Secure Call Flow** 转接强制使用盲转，失败直接挂断（防止敏感数据在咨询转接中暴露）
- **Common Module** 动作集 = 所有声明兼容类型的交集；不可嵌套调用其他 Common Module
- **Voice Survey Flow** 结构由 Survey Form 决定，不可自由编辑问题顺序；选择题+是非题+打分题合计 ≤ 50
- **Voicemail Flow** 全局唯一，修改立即生效；不支持 Transfer to ACD

---

## 流程间协作模式

```
┌─────────────────────────────────────────────────────────┐
│                    客户交互层                              │
│                                                           │
│  Inbound Call ──┬── Transfer to ACD ──→ In-Queue Call     │
│  Outbound Call  │                                         │
│  Inbound Chat   ├── Call Bot Flow ──→ Bot / Digital Bot   │
│  Inbound Email  │                                         │
│  Inbound Msg    ├── Transfer to Secure ──→ Secure Call    │
│                 │        └── Return to Agent ─┘           │
│                 ├── Call Common Module ──→ Common Module   │
│                 │        └── return ──────────┘           │
│                 └── Transfer to Flow ──→ 另一同类流程      │
│                                                           │
├─────────────────────────────────────────────────────────┤
│                    后交互层                                │
│                                                           │
│  交互结束 ──→ Voice Survey Flow（通话后电话调查）           │
│           ──→ Survey Invite Flow（发送邮件问卷链接）        │
│           ──→ Voicemail Flow（无人接听时留言）              │
│                                                           │
├─────────────────────────────────────────────────────────┤
│                    后台自动化层                             │
│                                                           │
│  事件/API ──→ Workflow（后台任务自动化）                    │
│  工单事件 ──→ Workitem Flow（工单生命周期）                 │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### 六种协作机制

| 机制 | 说明 | 示例 |
|------|------|------|
| **同步调用** | 主流程暂挂，子流程执行后返回 | Call Common Module、Call Bot Flow |
| **转接衔接** | 主流程将交互移交另一流程 | Transfer to ACD → In-Queue；Transfer to Secure Flow |
| **Return** | 安全流程结束后接回原坐席 | Secure Call Flow → Return to Agent |
| **事件触发** | 系统事件自动启动后台流程 | conversation.end → Workflow；workitem.create → Workitem Flow |
| **平台调度** | 平台根据配置自动衔接 | 通话结束 → Voice Survey；队列无人接 → Voicemail |
| **版本快照** | Common Module 被引用时锁定版本，主流程重新发布才取新版 | 模块更新不影响已发布的主流程 |

### 典型呼叫旅程串联

> Inbound Call Flow（IVR 导航）→ In-Queue Call Flow（排队等待）→ 坐席接听 → 坐席发起 Secure Call Flow（支付）→ Return to Agent → 坐席挂断 → Voice Survey Flow（满意度调查）

---

## 设计哲学：为什么按类型划分

Genesys 将流程按类型而非"统一流程 + 配置开关"划分，核心考量：

**1. 安全隔离**
Secure Call Flow 作为独立类型，系统层面强制禁用录音和日志。如果是统一流程 + 安全开关，开发者可能遗漏配置导致敏感数据泄露。类型隔离将安全策略从"人的纪律"变成"架构的约束"。

**2. 设计时防错**
每种类型的 Architect 工具箱只显示该类型支持的动作。Chat Flow 里看不到"播放语音"，Call Flow 里看不到"发送自动回复邮件"。Common Module 兼容多类型时，动作集自动收敛为交集。这消除了跨渠道的无效配置。

**3. 模块化复用**
Common Module 提供跨类型复用机制。统一流程模式下，开发者需要在一个巨型流程里写大量渠道条件分支；类型划分后，共性逻辑提取到 Common Module，各类型流程各自简洁。

**4. 性能隔离**
不同类型的执行特性差异巨大：Call Flow 要求毫秒级响应，Email Flow 可运行 8+ 小时，Workitem Flow 可能持续数天。独立类型使平台能针对性优化超时、资源占用和调度策略。

**5. 管理体验**
流程类型与后台管理模块对齐：Email Flow 在邮件路由配置中关联，Chat Flow 在 Widget 部署中关联，Workitem Flow 在任务管理模块中关联。管理员按职责分工操作，无需在统一列表中辨认流程用途。

**代价**：同一逻辑在多渠道中可能需要各实现一次（Common Module 可缓解但不能完全消除）；初学者需要理解多种类型的边界。

<!-- status: 草稿 — 内容基于 Genesys Cloud Resource Center 官方文档和内部调研文档，部分能力限制细节待核验 -->

## Related Pages

- [[Genesys-Cloud-Architect]] — 上级页面：Architect 总览、组件分类、与 Dify 对比
- [[CCaaS-平台与架构]] — 所属主题页
