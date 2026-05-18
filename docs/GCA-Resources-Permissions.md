---
title: Genesys Cloud Architect — 资源类型与权限管理
created: 2026-05-13
last_updated: 2026-05-13
status: 草稿
tags: [联络中心, CCaaS, 流程编排, IVR, Genesys]
sources:
  - Genesys Cloud 官方文档
  - SynologyDrive/archive/work-mx/02-Areas/gca调研/ 下的调研文档
  - Genesys Cloud Resource Center (2026-02/03 Release Notes)
visibility: public
---

> Architect 的资源对象通过 Division（分区）实现访问隔离，通过 RBAC（基于角色的权限）实现操作粒度控制。理解资源—分区—权限的关系是平台治理的基础。

## 资源类型一览

| 资源类型 | 用途 | Division 感知 | 可删除 | 关键限额 |
|---------|------|:------------:|:-----:|---------|
| **Flow** | IVR / Bot / Workflow 等交互逻辑 | 是 | 是（未被引用时） | 无公开上限（软限） |
| **Common Module** | 跨 Flow 可复用子流程 | 是 | 否（被引用时） | 不可嵌套；容量上限低于普通 Flow |
| **Prompt（用户提示音）** | 自定义录音 / TTS 文本 | 否（全局） | 是 | 单文件 ≤ 25 MB；名称 ≤ 200 字符 |
| **Prompt（系统提示音）** | 平台预置的通用提示 | 否（全局） | 否（只能覆写音频） | — |
| **Data Table** | 键值查找存储（配置数据） | 是 | 否（被引用时） | 200 表 / 5,000 行 / 50 列 / Key ≤ 256 字符 |
| **Script（座席脚本）** | 座席端弹屏指导界面 | 是 | 是 | — |
| **Flow Outcome** | 自助服务结果指标 | 是 | **不可删除** | 100 个/组织 |
| **Flow Milestone** | Outcome 内的中间检查点 | 跟随 Outcome | 可删除 | 1,000 个/组织；每 Outcome 实例最多记录 20 个 |

---

## 各资源详解

### Flow

- 每个 Flow 属于一个 Division，仅对有该 Division 权限的用户可见
- 只有**已发布**的 Flow 才能被其他 Flow 转接调用（Transfer to Flow）
- 调用者需要目标 Flow 的 `View` + `Search` 权限
- Flow 名称 ≤ 200 字符；每次执行最多 10,000 个 Action（错误处理跳转额外 +1,000）

### Common Module

- 封装可复用逻辑，一次设计多处调用，减少重复
- 创建时指定兼容的 Flow 类型（如语音+聊天），Architect 自动限制可用 Action 为兼容类型的交集
- **版本快照**：主 Flow 发布时锁定引用的 Common Module 版本；模块更新后须重新发布主 Flow
- **不可嵌套**：Common Module 内不能调用另一个 Common Module
- **删除保护**：被已发布 Flow 引用时不可删除

### Prompt

- **用户提示音**：自定义录音 / TTS，全局可见（不区分 Division）
- **系统提示音**：平台预置，不可删除/重命名，可覆写音频（约 1 小时生效）
- 更新用户提示音后几分钟内生效，无需重新发布引用它的 Flow
- 权限只有 `Architect > User Prompt > Add/Edit/View`，无 Search → 不受 Division 控制

> TTS 变更提示：原生 Enhanced TTS（部分 Google/Microsoft 语音）将于 2026-08-05 下线，需迁移到 AppFoundry 集成。

### Data Table

- 轻量键值存储，查询延迟 ~20ms，适合配置数据（非实时搜索场景）
- 首列为唯一 Key，按 Key 精确匹配查询
- Division 感知：只有对表所在 Division 有权限的用户才能查看/使用
- 结构管理（Datatable Add/Edit）与数据维护（Datatable Row Add/Edit）权限分离
- 限额：200 表 / 5,000 行 / 50 列（可联系 Genesys 扩容）
- **删除保护**：被已发布 Flow 引用时不可删除

### Script（座席脚本）

- 座席接听时自动弹出的指导界面（话术、信息采集字段、操作按钮）
- 通过队列默认配置或 Architect 的 `Set Screen Pop` Action 动态指定
- Division 感知：管理/编辑受 Division 限制，但运行时弹出不检查座席权限
- 权限分离：`Scripter > Script > Edit`（创建编辑）vs `Scripter > Published Script > View`（引用使用）

### Flow Outcome

- 衡量自助服务成功率的指标（如"支付成功"、"身份验证通过"）
- 在 Flow 内通过 `Initialize Flow Outcome` 开始追踪，`Set Flow Outcome` 标记成功/失败
- **不可删除**（防止影响历史数据）→ 创建前须慎重规划
- **不跨 Flow 实例**：Transfer 到另一个 Flow 后，新 Flow 的 Outcome 是独立实例
- 数据接入 Performance Dashboard，统计启动次数、成功率、平均耗时
- 限额：100 个/组织

### Flow Milestone

- Outcome 的中间检查点，记录用户在完成 Outcome 过程中经过的关键步骤
- 帮助分析路径转化率、找出瓶颈和放弃点
- 每个 Milestone 属于一个 Outcome，可在该 Outcome 的任何 Flow 中使用
- 限额：1,000 个/组织；每 Outcome 实例报告最多 20 个；每 Flow 报告最多 100 个
- 可删除（不影响已记录的历史数据）

---

## Division（分区）机制

### 核心概念

Division 在同一组织内划分配置对象的可见范围，实现多业务线/多区域/多环境的资源隔离。

- 每个 Division 感知的对象**只能属于一个 Division**
- 用户通过角色被授予一个或多个 Division 的访问权限
- 无权限的 Division 中的对象完全不可见

### All Division 模式（2026 更新）

- 新引入的 Division 感知对象默认分配到 **"All"** Division（对所有用户可见）
- 原 Home Division 的对象已自动迁移到 All
- 管理员可将对象从 All 重新分配到具体 Division 以收紧权限
- **建议**：核心资源（Flow / Data Table）应明确划分到具体 Division，而非长期留在 All

### 各资源的 Division 行为

| 资源 | Division 感知 | 判断依据 |
|------|:------------:|---------|
| Flow | 是 | 有 Search 权限项 |
| Common Module | 是 | 同 Flow |
| Data Table | 是 | 有 Search 权限项 |
| Script | 是 | 有 Division 过滤 |
| Flow Outcome | 是 | 有 Search 权限项 |
| Prompt | **否** | 无 Search 权限项 → 全局可见 |

> 判断技巧：权限清单中有 `Search` 操作的资源类型是 Division 感知的；没有 `Search` 的是全局的。

---

## 权限模型

### RBAC 基础

Genesys Cloud 采用**角色 + 权限 + Division** 三层模型：

1. **权限**：按资源类型细分操作（Add / Edit / View / Search / Delete / Publish）
2. **角色**：权限的集合，分配给用户
3. **Division 作用域**：角色在哪些 Division 内生效

### 管理权限 vs 使用权限分离

| 资源 | 管理权限（创建/编辑） | 使用权限（引用/查看） |
|------|---------------------|---------------------|
| Flow | `Architect > Flow > Add/Edit/Publish` | `Architect > Flow > View/Search` |
| Data Table | `Architect > Datatable > Add/Edit` + `Datatable Row > Add/Edit` | `Architect > Datatable > View` + `Datatable Row > View` |
| Prompt | `Architect > User Prompt > Add/Edit` | `Architect > User Prompt > View` |
| Script | `Scripter > Script > Add/Edit` | `Scripter > Published Script > View` |
| Flow Outcome | `Architect > Flow Outcome > Add/Edit` | `Architect > Flow Outcome > View/Search` |
| Flow Milestone | `Architect > Flow Milestone > Add/Edit` | `Architect > Flow Milestone > View/Search` |

### ABAC 补充（2025 引入）

- **属性基访问控制**（Attribute-Based Access Control）作为 RBAC 的补充层
- 支持基于动态条件（如用户属性、时间、资源标签）的更细粒度权限判定
- 与现有 RBAC + Division 模型共存，不替代

### 运行时 vs 设计时

- **设计时**：所有资源引用须由有权限的用户配置（选择 Queue / Flow / Script 等须 View 权限）
- **运行时**：Flow 执行不检查权限——一旦发布并绑定到路由，系统自动执行所有操作
- **实践含义**：为 IVR 设计人员授予足够的 View/Search 权限（Queue / Flow / Prompt / Data Table / Script），同时通过 Division 隔离无关对象

---

## 治理建议

| 建议 | 说明 |
|------|------|
| 按业务域划分 Division | 如"北美"/"欧洲"，或"生产"/"测试"，实现配置隔离 |
| Prompt 用命名规范替代 Division | Prompt 不受 Division 控制，用前缀区分（如 `NA_Welcome`、`EU_Welcome`） |
| 慎重规划 Flow Outcome | 不可删除 + 上限 100 → 创建前明确业务目标和命名 |
| Common Module 更新后重新发布主 Flow | 否则主 Flow 仍使用旧版本快照 |
| 分离管理与使用角色 | 少数管理员拥有 Add/Edit，多数设计者仅需 View/Search |
| 检查设计者的跨模块权限 | Transfer 需 `Routing > Queue > View`；Data Action 需 `Integrations > Action > View`；Script 需 `Published Script > View` |

<!-- status: 草稿 — 内容基于 Genesys Cloud 官方文档和内部调研文档，部分限额可联系 Genesys 调整 -->

## Related Pages

- [[Genesys-Cloud-Architect]] — Architect 总览
- [[GCA-Actions]] — 组件（Action）分类详解
- [[GCA-Variables]] — 变量与表达式体系
- [[GCA-Routing-Admin]] — 路由配置与 ACD 策略
- [[CCaaS-平台与架构]] — 所属主题页
