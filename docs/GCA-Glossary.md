---
title: Genesys Cloud Architect — 术语表
created: 2026-05-14
last_updated: 2026-05-14
status: 草稿
tags: [联络中心, CCaaS, 流程编排, IVR, Genesys, 术语]
sources:
  - Genesys Cloud 官方文档 (help.mypurecloud.com)
  - Genesys Cloud Developer Center (developer.genesys.cloud)
---

> GCA 相关核心术语的快速解释与跳转索引，按功能域分组。

## 平台与产品

| 术语 | 解释 | 详情 |
|------|------|------|
| **Genesys Cloud CX** | Genesys 的云原生 CCaaS 平台，基于 AWS 微服务架构，提供语音/数字全渠道联络中心能力 | [[GCA-Runtime-Execution#底层运行时架构]] |
| **Architect** | Genesys Cloud 的可视化流程编排工具（Flow Designer），用于拖拽式设计 IVR、Bot、数字渠道交互和后台工作流 | [[Genesys-Cloud-Architect]] |
| **Archy CLI** | Architect 的命令行接口，可用于批量导出/导入/部署 Flow，支持 YAML 格式定义 | [[GCA-Runtime-Execution#超时机制]] |
| **AppFoundry** | Genesys Cloud 的应用市场，第三方集成和预构建应用的分发平台 | [[GCA-Resources-Permissions]] |
| **Edge** | Genesys Cloud 的本地媒体网关设备，负责语音媒体处理（PSTN 接入、编解码、录音） | [[GCA-Runtime-Execution#底层运行时架构]] |
| **VXML Engine** | Architect 中语音 Flow 的底层执行引擎，基于 VoiceXML 标准处理语音交互 | [[GCA-Runtime-Execution#冷启动]] |
| **Global Media Fabric** | 跨区域媒体路由网络，将语音/视频流路由到离用户最近的 AWS Region 以降低延迟 | [[GCA-Runtime-Execution#地理分布]] |
| **Dialog Engine** | Genesys 内置的 NLU 引擎，为 Bot Flow 提供意图识别和槽位提取能力 | [[GCA-Flow-Types]] |

## Flow（流程）

| 术语 | 解释 | 详情 |
|------|------|------|
| **Flow** | Architect 中的基本编排单元，定义一个完整的交互处理逻辑。每种渠道/场景对应不同的 Flow 类型 | [[GCA-Flow-Types]] |
| **Flow Instance** | Flow 的运行时实例。每个交互（通话/聊天/邮件）独立执行一个实例，实例间天然隔离 | [[GCA-Runtime-Execution#实例隔离]] |
| **Inbound Call Flow** | 处理来电的主 IVR 流程，从接通到路由/断开的全链路逻辑 | [[GCA-Flow-Types]] |
| **In-Queue Call Flow** | 客户在排队等待时执行的流程（播放等待音乐、预计等待时间、回拨选项） | [[GCA-Flow-Types]] |
| **Secure Call Flow** | 用于采集敏感数据（信用卡号等）的 PCI 合规流程，所有数据加密处理，转接失败直接断开 | [[GCA-Flow-Types]] |
| **Bot Flow** | 基于 NLU 的多轮对话流程（语音+文本），使用 Intent/Slot 模型驱动 | [[GCA-Flow-Types]] |
| **Digital Bot Flow** | 纯文本渠道的 Bot 流程（Chat/Message），不涉及语音/ASR | [[GCA-Flow-Types]] |
| **Common Module** | 可复用的子流程模块，被多个 Flow 引用。被引用时锁定版本快照，主 Flow 需重新发布才能获取模块新版 | [[GCA-Flow-Types]] |
| **Workflow** | 事件驱动的后台自动化流程，无实时交互连接，可长时间运行 | [[GCA-Flow-Types]] |
| **Workitem Flow** | 管理工单（Workitem）生命周期的流程 | [[GCA-Flow-Types]] |

## Action（动作/组件）

| 术语 | 解释 | 详情 |
|------|------|------|
| **Action** | Flow 中的最小可执行单元（节点），每种 Action 对应一种操作（交互/数据/路由/逻辑等） | [[GCA-Actions]] |
| **Data Action** | 调用外部 API 或 Genesys Cloud 内部 API 的集成组件。有 Success / Failure / Timeout 三条输出分支 | [[GCA-Actions#数据操作与集成]] |
| **Transfer to ACD** | 将交互转接到 ACD 队列，由路由引擎分配给合适的座席 | [[GCA-Actions#路由与转接]] |
| **Blind Transfer** | 直接转接（不保持原通话），Secure Call Flow 中强制使用此方式 | [[GCA-Runtime-Execution#Secure-Flow-特殊行为]] |
| **Decision** | 条件分支节点，评估布尔表达式后走 True 或 False 路径 | [[GCA-Actions#逻辑与分支]] |
| **Switch** | 多路分支节点，类似 switch-case 语句 | [[GCA-Actions#逻辑与分支]] |
| **Loop** | 循环节点，常用于实现 Data Action 重试逻辑 | [[GCA-Actions#逻辑与分支]] |
| **Evaluate Schedule** | 评估当前时间是否匹配日程规则（工作时间/节假日），返回匹配的日程区间 | [[GCA-Actions#逻辑与分支]] |
| **Collect Input** | 语音流程中采集 DTMF 按键输入的节点 | [[GCA-Actions#用户交互]] |
| **Communicate** | 向客户播放/发送消息的节点（语音流中为 TTS/音频，数字流中为文本） | [[GCA-Actions#用户交互]] |
| **Task** | Flow 内的子过程（Sub-procedure），用于组织逻辑分组。Task 变量作用域仅限该 Task | [[GCA-Actions#流程管理]] |
| **Reusable Task** | 可被多个地方调用的 Task，常用于 Error Handler 的跳转目标 | [[GCA-Runtime-Execution#事件处理层级]] |

## 变量与数据

| 术语 | 解释 | 详情 |
|------|------|------|
| **Flow Variable** | 作用域为整个 Flow 的变量，所有 Task 内均可访问 | [[GCA-Variables#变量分类与作用域]] |
| **Task Variable** | 作用域仅限声明所在 Task 的变量 | [[GCA-Variables#变量分类与作用域]] |
| **Input/Output Variable** | Flow 的对外接口参数，用于 Flow 间传递数据（如 Common Module 的入参/出参） | [[GCA-Variables#变量分类与作用域]] |
| **Participant Data** | 附着在交互参与方（客户/座席/Flow）上的键值对数据，跨 Flow 持久存在直到交互结束 | [[GCA-Variables#变量分类与作用域]] |
| **Secure Variable** | 标记为安全的变量，禁止录音/日志记录，仅在 Secure Call Flow 中有效 | [[GCA-Variables#变量配置选项]] |
| **NOT_SET** | Genesys 表达式系统中的空值标记，类似其他语言的 null/nil | [[GCA-Variables#数据类型体系]] |
| **Collection** | 有序列表类型，类似数组，支持 Count / GetAt / AddItem 等操作 | [[GCA-Variables#数据类型体系]] |
| **Expression** | Architect 的内置表达式语言，用于变量赋值、条件判断、数据转换（~70 个内置函数） | [[GCA-Variables#表达式系统]] |

## 路由与 ACD

| 术语 | 解释 | 详情 |
|------|------|------|
| **ACD** | Automatic Call Distribution，自动呼叫分配系统，按预设策略将交互路由给合适的座席 | [[GCA-Routing-Admin#ACD-路由策略]] |
| **Queue** | ACD 队列，座席按技能/语言分组的逻辑容器，交互进入队列后等待分配 | [[GCA-Routing-Admin]] |
| **Bullseye Routing** | 靶心路由策略——从最严格的技能匹配开始，逐圈扩大匹配范围直到找到可用座席 | [[GCA-Routing-Admin#ACD-路由策略]] |
| **Predictive Routing** | AI 预测路由，基于历史数据预测最优座席匹配（按 KPI 优化），已 GA | [[GCA-Routing-Admin#Predictive-Routing]] |
| **Preferred Agent** | 优先分配给指定座席，超时后回退到常规路由 | [[GCA-Routing-Admin#ACD-路由策略]] |
| **Conditional Group Routing (CGR)** | 根据队列实时状态（排队人数/等待时长）触发条件规则的路由策略 | [[GCA-Routing-Admin#ACD-路由策略]] |
| **Direct Routing** | 绕过 ACD 队列，直接将交互路由到特定座席 | [[GCA-Routing-Admin#Direct-Routing]] |
| **Schedule** | 日程规则，定义工作时间/非工作时间/节假日，用于路由分流 | [[GCA-Routing-Admin#Schedules]] |
| **Schedule Group** | 日程组，将多个 Schedule 组合后与 Flow 关联 | [[GCA-Routing-Admin#Schedules]] |
| **Emergency Group** | 紧急覆盖开关，激活后直接跳转到预设 Flow，优先级最高（高于 Schedule） | [[GCA-Routing-Admin#Emergency-Groups]] |
| **DID** | Direct Inward Dialing，直拨号码，映射到 Call Routing 条目 | [[GCA-Routing-Admin#Call-Routing]] |
| **ANI** | Automatic Number Identification，来电号码（主叫号码识别） | [[GCA-Variables#系统预置变量]] |
| **DNIS** | Dialed Number Identification Service，被叫号码识别 | [[GCA-Variables#系统预置变量]] |
| **Skill** | 座席技能标签（如语言、产品线），用于 ACD 技能匹配路由 | [[GCA-Routing-Admin#ACD-路由策略]] |
| **WrapupCode** | 话后处理代码，座席在交互结束后标记的分类标签 | [[GCA-Variables#数据类型体系]] |

## 资源与权限

| 术语 | 解释 | 详情 |
|------|------|------|
| **Division** | Genesys Cloud 的访问控制分区单元，资源（Flow/Queue/User 等）归属于 Division，权限按 Division 授予 | [[GCA-Resources-Permissions#Division-分区机制]] |
| **Home Division** | 每个 Org 的默认 Division，新建资源默认归入 Home Division | [[GCA-Resources-Permissions#Division-分区机制]] |
| **All Division** | 2026 新增的特殊 Division，允许某些管理操作跨所有 Division 执行 | [[GCA-Resources-Permissions#Division-分区机制]] |
| **RBAC** | Role-Based Access Control，基于角色的权限控制。Genesys Cloud 通过 角色 × Division 授权 | [[GCA-Resources-Permissions#RBAC-权限模型]] |
| **Data Table** | Architect 内的键值查找表，类似轻量数据库，上限 200 个/Org | [[GCA-Resources-Permissions#资源类型详解]] |
| **Prompt** | 预录音频或 TTS 文本，分 System Prompt（系统内置）和 User Prompt（用户自定义） | [[GCA-Resources-Permissions#资源类型详解]] |
| **Script** | Scripter 脚本，定义座席桌面的弹屏布局（Screen Pop）和交互引导 | [[GCA-Resources-Permissions#资源类型详解]] |
| **Flow Outcome** | 自助服务结果追踪标记（成功/失败），上限 100 个/Org，不可删除 | [[GCA-Resources-Permissions#资源类型详解]] |
| **Flow Milestone** | Outcome 内的细粒度里程碑标记，上限 1,000 个/Org | [[GCA-Resources-Permissions#资源类型详解]] |

## 运行时与可观测性

| 术语 | 解释 | 详情 |
|------|------|------|
| **Action 执行上限** | 每个 Flow 实例最多执行 10,000 个 Action，超出后触发 Error Event Handler（额外 1,000 配额），绝对上限后 Silent Disconnect | [[GCA-Runtime-Execution#Action-执行限制]] |
| **Silent Disconnect** | 超出绝对 Action 上限后的系统行为——无提示直接挂断 | [[GCA-Runtime-Execution#Action-执行限制]] |
| **Error Event** | 未捕获运行时错误时触发的全局事件，可配置处理方式（Disconnect / Transfer / Jump） | [[GCA-Runtime-Execution#事件类型]] |
| **Disconnect Event** | 客户或系统侧断开连接时触发的事件（仅限有实时连接的 Flow 类型） | [[GCA-Runtime-Execution#事件类型]] |
| **Recognition Failure Event** | Bot Flow 中 NLU 无法识别客户回复时触发的事件 | [[GCA-Runtime-Execution#事件类型]] |
| **Failure Output** | Action 的失败输出分支，类似 try-catch 的异常路径 | [[GCA-Runtime-Execution#Failure-Output-分支]] |
| **Debug Mode** | Architect 的调试模式，用真实通话测试未发布的 Flow 版本，提供变量追踪和执行路径信息 | [[GCA-Runtime-Execution#Debug-模式]] |
| **Flow Execution History** | Flow 的历史执行数据（默认关闭），分 4 级采集深度（Base / Notes / Verbose Notes / All） | [[GCA-Runtime-Execution#Flow-执行历史]] |
| **Replay Mode** | 在 Architect UI 中回放 Flow 执行过程，支持断点和变量追踪 | [[GCA-Runtime-Execution#Flow-执行历史]] |
| **Core Region** | 每个 Org 绑定的主 AWS Region（3 AZ，Active/Active/Active），Flow 逻辑在此执行 | [[GCA-Runtime-Execution#地理分布]] |
| **Satellite Media Region** | 通过 Global Media Fabric 路由媒体流到离用户最近的区域 | [[GCA-Runtime-Execution#地理分布]] |

## AI / NLU

| 术语 | 解释 | 详情 |
|------|------|------|
| **NLU** | Natural Language Understanding，自然语言理解引擎，Bot Flow 的核心 AI 能力 | [[GCA-Actions#AI-NLU]] |
| **Intent** | 用户意图，NLU 识别用户输入后匹配的目标动作类别 | [[GCA-Actions#AI-NLU]] |
| **Slot** | 意图参数（槽位），从用户输入中提取的结构化信息（如日期、金额、产品名） | [[GCA-Actions#AI-NLU]] |
| **ASR** | Automatic Speech Recognition，自动语音识别，将语音转为文本 | [[GCA-Variables#系统预置变量]] |
| **TTS** | Text-to-Speech，文本转语音合成 | [[GCA-Flow-Types]] |
| **Intent Miner** | Genesys 的意图挖掘工具，从历史交互数据中自动发现常见意图模式 | [[GCA-Actions#AI-NLU]] |
| **Knowledge** | Architect 中的知识库集成，用于 FAQ 自动问答 | [[GCA-Actions#AI-NLU]] |
| **Agent Escalation Event** | Bot Flow 检测到客户希望转人工时自动触发的事件 | [[GCA-Runtime-Execution#事件类型]] |

## 通用缩写

| 缩写 | 全称 | 含义 |
|------|------|------|
| **CCaaS** | Contact Center as a Service | 云联络中心即服务 |
| **IVR** | Interactive Voice Response | 交互式语音应答 |
| **PCI DSS** | Payment Card Industry Data Security Standard | 支付卡行业数据安全标准 |
| **DTMF** | Dual-Tone Multi-Frequency | 双音多频（电话按键音信号） |
| **SLA** | Service Level Agreement | 服务级别协议 |
| **AHT** | Average Handle Time | 平均处理时长 |
| **E.164** | ITU-T E.164 | 国际电话号码格式标准（如 +8613800138000） |
| **UUI** | User-to-User Information | 用户到用户信息（SIP 头部携带的自定义数据） |
| **PSTN** | Public Switched Telephone Network | 公共交换电话网 |

## Related Pages

- [[Genesys-Cloud-Architect]] — Architect 总览
- [[GCA-Flow-Types]] — Flow 类型详解
- [[GCA-Actions]] — 组件（Action）分类详解
- [[GCA-Variables]] — 变量与表达式体系
- [[GCA-Resources-Permissions]] — 资源类型与权限管理
- [[GCA-Routing-Admin]] — 路由配置与 ACD 策略
- [[GCA-Runtime-Execution]] — 运行时执行架构
- [[CCaaS-平台与架构]] — 所属主题页
