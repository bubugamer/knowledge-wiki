---
title: Genesys Cloud Architect — 变量与表达式体系
created: 2026-05-12
last_updated: 2026-05-13
status: 草稿
tags: [联络中心, CCaaS, 流程编排, IVR, Genesys]
sources:
  - Genesys Cloud 官方文档
  - SynologyDrive/archive/work-mx/02-Areas/gca调研/ 下的调研文档
---

> Architect 的变量与表达式体系定义了流程数据的作用域、类型、生命周期、跨流程传递方式，以及操作这些数据的函数和运算符。

## 变量分类与作用域

Architect 中的数据按来源和作用域分为五类，通过命名前缀区分：

| 类别 | 前缀 | 定义方式 | 作用域 | 生命周期 | 跨流程 |
|------|------|---------|--------|---------|--------|
| **Flow 变量** | `Flow.` | 设计时预定义或表达式中首次引用自动创建 | 整个 Flow（所有 Task 可见） | Flow 实例启动时初始化，结束时销毁 | 通过 Input/Output 参数传递给子流程 |
| **Task 变量** | `Task.` | Task 内 Update Data 创建或表达式中自动创建 | 当前 Task | 进入 Task 时创建，Task 结束时销毁 | 不可跨 Task / 不可跨 Flow |
| **Input/Output 变量** | `Flow.`（标记 Input/Output） | Flow 设置中声明 | 调用方 ↔ 被调用 Flow | 调用时传入，返回时传出，之后释放 | 专为跨 Flow 传递设计 |
| **系统上下文变量** | `Call.` / `Message.` / `Chat.` / `Email.` / `Session.` / `System.` / `Flow.` | 平台自动提供，只读 | 当前 Flow 实例 | 会话进入 Flow 时填充，离开时重置 | 部分跨 Flow 保持（如 ConversationID） |
| **Participant Data** | 自定义 key | `Set Participant Data` Action 写入 | 整个 Conversation | 会话开始到结束，跨 Flow 持久 | 会话级持久，任何 Flow 可读取 |

### Participant Data 特殊说明

Participant Data 不属于任何 Flow 的局部变量，而是附着在 Conversation 对象上的键值对：

- 通过 `Set Participant Data` 写入，`Get Participant Data` 读取
- 仅支持基础类型：String / Integer / Decimal / Boolean
- 跨 Flow 转接时自动携带（IVR → In-Queue → 座席脚本均可读取）
- 典型用途：在 IVR 中记录客户选择，转接后座席侧脚本读取

---

## 数据类型

### 原生基础类型

| 类型 | 说明 | 未赋值状态 | 关键函数 |
|------|------|-----------|---------|
| **String** | 文本，最常用 | NOT_SET | Append, Contains, Length, Substring, Left, Right, Upper, Lower |
| **Integer** | 长整数（±9.9999×10¹⁴） | NOT_SET | ToInt |
| **Decimal** | 高精度小数 | NOT_SET | ToDecimal |
| **Boolean** | True / False | NOT_SET | ToBoolean, ToAudioBoolean |
| **DateTime** | UTC 日期+时间 | NOT_SET | ToDateTime, MakeDateTime, Year/Month/Day/Hour/Minute/Second, AddDays |
| **Date** | 仅日期（1800-01-01 ~ 2200-12-31） | NOT_SET | ToDate, MakeDate |
| **Time** | 仅时间（00:00 ~ 23:59） | NOT_SET | ToTime |
| **Duration** | 持续时长（ISO 8601） | NOT_SET | ToDuration, MakeDuration, AddDuration |

### 复合与集合类型

| 类型 | 说明 | 关键限制 |
|------|------|---------|
| **Collection** | 同类型有序列表（数组） | 最大 2000 项；空集合 ≠ NOT_SET；用 `[]` 索引访问 |
| **JSON Object** | 通用对象结构 | JsonParse 解析后用 `.` 访问属性；格式错误触发运行时错误 |
| **EmailAddress** | 邮件地址对象 | MakeEmailAddress 构造；可提取 LocalPart / DomainPart |
| **PhoneNumber** | E.164 电话号码对象 | MakePhoneNumber / ToPhoneNumber 构造；含 .dialingCode 等属性 |
| **Prompt** | 提示音资源引用 | `Prompt.名称` 引用；含 .id / .name / .textToSpeech / .duration 属性 |
| **Enum** | 系统枚举常量 | System.Regions / System.Languages / System.Currencies / System.Conversation；只读 |

### 网络资源引用类型

这些类型引用 Genesys Cloud 组织内已配置的对象，**不能**从字符串直接转换：

| 类型 | 获取方式 | 典型用途 |
|------|---------|---------|
| **User** | Find User Action 或 FindUserById() | Transfer to User |
| **Queue** | Find Queue Action 或 FindQueueById() | Transfer to ACD |
| **Skill** | FindSkill() | 技能路由 |
| **Group** | FindGroup() / FindGroupById() | 按组路由 |
| **WrapupCode** | FindWrapUpCode() | 话后处理标记 |
| **Contact / ContactList** | 系统自动填充（外呼场景） | 外呼活动 |
| **Campaign** | 系统自动填充 | 外呼活动 |

> **关键限制**：Architect 没有 ToUser / ToQueue / ToSkill 等转换函数。动态确定这些对象必须通过 Find Action 或 FindById 函数获取。

---

## 系统预置变量

### 语音呼叫（Call.*）

| 变量 | 类型 | 读写 | 说明 |
|------|------|------|------|
| Call.Ani | String | 只读 | 主叫号码（ANI） |
| Call.CalledAddress | String | 只读 | 被叫号码（DNIS），转接后可能变更 |
| Call.CalledAddressOriginal | String | 只读 | 原始拨入号码，永不变更 |
| Call.ConversationID | String | 只读 | 通话唯一标识 |
| Call.Language | String | 读写 | 当前语言（IETF 代码） |
| Call.UUIData | String | 只读 | 用户到用户信息（自定义数据串） |
| Call.CurrentQueue | Queue | 读写 | 当前排队的队列对象（In-Queue Flow） |
| Call.PositionInQueue | Integer | 只读 | 队列中位置（1 = 首位） |
| Call.EstimatedWaitTime | Duration | 只读 | 预计剩余等待时长 |
| Call.ACDSkills | Collection\<Skill\> | 读写 | 当前请求技能集合 |
| Call.LanguageSkill | String | 读写 | 请求的语言技能名称 |
| Call.Campaign | Campaign | 只读 | 所属外呼活动（Outbound） |
| Call.Contact | Contact | 只读 | 当前联系人（Outbound） |
| Call.ContactList | ContactList | 只读 | 联络清单（Outbound） |

### 流程通用（Flow.*）

| 变量 | 类型 | 说明 |
|------|------|------|
| Flow.StartDateTimeUTC | DateTime | 流程启动 UTC 时间戳 |
| Flow.IsTest | Boolean | 是否在调试模式运行 |
| Flow.Version | String | 当前执行的流程版本号 |
| Flow.WrapupCode | WrapupCode | 流程结束码 |

### 数字消息（Message.*）

| 变量 | 类型 | 说明 |
|------|------|------|
| Message.ConversationID | String | 消息会话标识 |
| Message.Message.body | String | 消息正文 |
| Message.Message.bodyType | String | 正文类型（text / HTML） |
| Message.Message.attachments | Collection | 附件集合 |
| Message.Message.stickers | Collection | 贴图集合 |
| Message.Message.type | String | 消息类型（SMS / Facebook / Twitter 等） |
| Message.Message.senderAddressInfo.addressNormalized | String | 标准化发件人地址 |
| Message.Message.senderAddressInfo.name | String | 发件人显示名 |
| Message.IsAuthenticated | Boolean | 是否已通过身份验证 |
| Message.IsNewConversation | Boolean | 是否为新会话 |
| Message.Language | String | 当前语言 |
| Message.JourneyContext | Object | Predictive Engagement 旅程上下文 |

### Web 聊天（Chat.*）

| 变量 | 类型 | 说明 |
|------|------|------|
| Chat.ConversationID | String | 聊天会话 ID |
| Chat.Guest | Object | 访客对象（ID、姓名等） |
| Chat.Language | String | 当前语言 |
| Chat.JourneyContext | Object | 旅程上下文 |

### 邮件（Email.*）

| 变量 | 类型 | 说明 |
|------|------|------|
| Email.ConversationID | String | 邮件交互 ID |
| Email.Message.from | Object | 发件人（含 .id / .name） |
| Email.Message.to | Collection\<EmailAddress\> | 收件人列表 |
| Email.Message.cc / bcc | Collection\<EmailAddress\> | 抄送 / 密送列表 |
| Email.Message.subject | String | 邮件主题 |
| Email.Message.body | String | 纯文本正文 |
| Email.Message.htmlBody | String | HTML 正文 |
| Email.Message.attachments | Collection | 附件集合 |
| Email.Message.spam | Boolean | 是否垃圾邮件 |
| Email.Message.direction | String | 方向（Inbound / Outbound） |

### Bot 会话（Session.*）

| 变量 | 类型 | 说明 |
|------|------|------|
| Session.ConversationID | String | 触发 Bot 的会话 ID |
| Session.Language | String | Bot 会话当前语言 |
| Session.Source | String | 渠道类型："call" / "chat" / "messaging" |
| Session.LastCollectionConfidence | Decimal | 上次 ASR 识别置信度（语音 Bot） |
| Session.LastNLUCollectionConfidence | Decimal | 上次 NLU 识别置信度（数字 Bot） |
| Session.LastCollectionUtterance | String | 上次用户完整语句 |
| Session.LastCompletedIntent | String | 上一个完成的 Intent 名称 |
| Session.LastKnowledgeQuestion | String | 最近一次知识查询的问题 |
| Session.LastKnowledgeAnswer | String | 最近一次知识查询的答案 |

### 系统常量（System.*）

| 变量 | 说明 |
|------|------|
| System.MinDateTime / MaxDateTime | DateTime 类型范围常量 |
| System.MinInt / MaxInt | Integer 范围常量 |
| System.MinDate / MaxDate | Date 范围（1800-01-01 ~ 2200-12-31） |
| System.MinTime / MaxTime | Time 范围（00:00 ~ 23:59） |
| System.Regions.* | 国家/区域枚举（含 .dialingCode 等） |
| System.Languages.* | 语言枚举 |
| System.Currencies.* | 货币枚举 |
| System.Conversation | 会话介质类型枚举 |

### 菜单与输入（Menu.*）

| 变量 | 类型 | 说明 |
|------|------|------|
| Menu.LastCollectionNoInput | Boolean | 上一次菜单未收到输入 |
| Menu.LastCollectionNoMatch | Boolean | 上一次菜单收到无效输入 |

---

## 变量配置选项

### 作用域选择

- **Entire Flow**：全流程共享，所有 Task 可见
- **Task Only**：仅当前 Task 可见，避免跨 Task 意外冲突

### 初始值

- **Literal**：直接指定默认值
- **Use default**：NOT_SET 状态（建议布尔/数值变量尽量初始化，减少空值判断）

### 安全与传递选项

| 选项 | 适用环境 | 作用 |
|------|---------|------|
| **Content is secure** | Secure Call / Voice Bot Flow | 写入加密安全变量，禁止出现在日志和录音中；须通过 Extract Secure Data 读取 |
| **Input to flow** | Secure / Workflow 等 | 声明为输入参数，父流程可在调用时传值 |
| **Output from flow** | Workflow 等 | 声明为输出参数，流程结束后由调用方读取 |

> 注意：设置安全变量时，须先取消 Input/Output 勾选，再勾选 Content is secure 才会生效。

---

## 变量在关键 Action 中的行为

### Update Data

- 配置多条赋值语句，每条指定变量和值
- 引用不存在的变量名时自动创建（默认 Task 作用域；加 `Flow.` 前缀创建 Flow 级）
- 支持 JSON Literal Editor 直接编辑 JSON 结构赋值
- 类型须匹配：赋值表达式结果类型须与变量类型一致

### Call Data Action

- **输入映射**：按 Data Action 的 JSON Input Contract 逐一映射值，类型须严格匹配
- **输出映射**：指定 Flow/Task 变量接收返回值；复杂对象需映射到 Object 类型后用 JsonParse 处理
- 成功走 Success 路径（变量已赋值），失败走 Failure 路径
- 数组输出须映射到 Collection 类型变量

### Transfer Actions

- **Transfer to ACD**：目标须为 Queue 对象（不能传字符串）
- **Transfer to Number**：目标须为 PhoneNumber 类型（建议 `tel:+E164` 格式）
- **Transfer to User**：目标须为 User 对象（先通过 Find User 获取）

### Ask for Input / Collect Input

- 语音 IVR：未指定变量时默认存入 `Task.Input`；DTMF 结果为字符串
- Bot Flow：槽位结果类型取决于 Slot Type 定义（可为 String / Integer / Date / Boolean 等）
- 无输入 → Menu.LastCollectionNoInput = True；无效输入 → Menu.LastCollectionNoMatch = True

---

## 表达式系统

表达式是操作变量的核心工具，用于 Decision / Switch / Update Data / 任何需要动态值的地方。

### 内置函数

| 类别 | 函数 | 说明 |
|------|------|------|
| **类型转换** | ToString, ToInt, ToDecimal, ToBoolean, ToDateTime, ToDate, ToTime, ToDuration, ToPhoneNumber | 基础类型互转；无 ToUser / ToQueue 等网络类型转换 |
| **对象构造** | MakeEmailAddress, MakePhoneNumber, MakeDuration, MakeDateTime, MakeList | 创建复合类型实例 |
| **网络查找** | FindUserById, FindQueueById, FindSkill, FindGroup, FindGroupById, FindWrapUpCode | 按 GUID 或名称获取网络类型对象；未找到返回 NOT_SET |
| **集合操作** | Count, IsEmpty, GetAt, Find, FindFirst, AddItem, AddItemAt, RemoveItem, RemoveItemAt, RemoveDups, ReplaceItem, ReplaceItemAt | 有序列表的增删改查 |
| **字符串** | Append, Contains, Length, Substring, Left, Right, Upper, Lower, Trim, Replace | Append 可安全拼接 NOT_SET 值（跳过而非报错） |
| **日期时间** | GetCurrentDateTimeUtc, AddDays, AddHours, AddMinutes, AddSeconds, AddDuration, GetDayOfWeek, Year, Month, Day, Hour, Minute, Second | 日期运算与部分提取 |
| **JSON** | JsonParse, ToJson, ToJsonCollection | JSON 字符串 ↔ 对象互转 |
| **判断** | IsSet, IsNotSetOrEmpty, AreEqual, Not | 空值检查与相等比较 |
| **音频** | ToAudioBoolean, ToAudioPrompt, ToAudioBlank, ToCommunication, ToCommunicationTTS | 语音渠道专用，将值转为可播放的音频/通信对象 |

### 运算符（按优先级从高到低）

| 类别 | 运算符 | 示例 |
|------|--------|------|
| 访问 | `.`（属性）`[]`（集合索引） | `Flow.MyCurrency.Amount`、`Flow.List[0]` |
| 一元 | `-`（取反）`!`（逻辑非）`~`（位非） | `!IsNotSetOrEmpty(Call.Ani)` |
| 幂 | `^` | `2 ^ Flow.Power` |
| 算术 | `*` `/` `%` | `(Flow.WaitMs / 1000) % 60` |
| 加减 | `+` `-` | `Flow.AverageHandleTime + 5` |
| 比较 | `<` `<=` `>` `>=` | `Call.AbandonRate <= 0.05` |
| 等于 | `==` `!=` | `Flow.MemberTier == "Gold"` |
| 位运算 | `&` `\|` | `Flow.Flags & 4 == 4`（极少用，能用 Boolean 就别用位运算） |
| 逻辑 | `and` `or` | `IsSet(Flow.Email) and Flow.Email != ""` |

> **易混淆**：逻辑 `and` / `or` 对 Boolean 短路求值；位运算 `&` / `|` 对 Integer 按位操作。两者完全不同，混用是常见错误。

---

## 设计限制

| 限制 | 说明 |
|------|------|
| 无 ToUser / ToQueue / ToSkill 函数 | 网络类型对象只能通过 Find Action 或 FindById 函数获取 |
| 无字符串 Split 函数 | 需用 Contains + Substring 手工实现，或通过 Data Action 处理 |
| 无高级数学函数 | 无 sin/cos 等，需通过 Data Action 调外部计算 |
| 集合最大 2000 项 | — |
| Participant Data 仅支持基础类型 | String / Integer / Decimal / Boolean |
| NOT_SET 参与 `+` 运算会报错 | 字符串拼接建议用 Append()（自动跳过 NOT_SET） |
| 变量名区分大小写 | 不能与系统前缀冲突 |
| 安全变量限制 | 仅 Secure Call Flow / Voice Bot Flow 内有效；无法在日志中查看 |

<!-- status: 草稿 — 内容基于 Genesys Cloud 官方文档和内部调研文档，部分细节待核验 -->

## Related Pages

- [[Genesys-Cloud-Architect]] — Architect 总览
- [[GCA-Actions]] — 组件（Action）分类详解
- [[GCA-Flow-Types]] — 15 种 Flow 类型详解
- [[CCaaS-平台与架构]] — 所属主题页
