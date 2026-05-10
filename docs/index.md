---
title: Knowledge Wiki
---

# Knowledge Wiki

---

## 人工智能 / 大模型

### 总览与框架

- [AI技术体系总览](AI技术体系总览.md) — 九层分层框架：从学习范式到统一认知架构的全景地图
- [学习范式](学习范式-LearningParadigm.md) — 七种主流学习范式；LLM 训练如何串联多种范式
- [模型架构](模型架构-ModelArchitecture.md) — 11 种架构全景；Transformer/Diffusion/SSM/MoE 当前格局
- [MoE-混合专家模型](MoE-混合专家模型.md) — 稀疏计算架构；Router/负载均衡/涌现式专业化；DeepSeek 路线
- [AI系统形态](AI系统形态-SystemArchitecture.md) — Chatbot → Agent → AI OS 的七种系统形态与选型
- [LLM训练四阶段总览](LLM训练四阶段总览.md) — 从预训练到部署的企业落地主线；世代演进的两根驱动轴
- [OpenAI五级智能分类](OpenAI五级智能分类.md) — Chatbot → Reasoner → Agent → Innovator → Organization
- [Agent三阶段演变](Agent三阶段演变.md) — 符号主义 → 深度 RL → LLM + 推理；为什么这代能泛化

### 训练阶段

- [预训练](预训练-Pretraining.md) — 能力地基；Tokenizer 与 Config 的不可逆性
- [SFT-有监督微调](SFT-有监督微调.md) — 从"会续写"到"会回答"
- [Alignment-对齐](Alignment-对齐.md) — 从"能说"到"会说"；偏好数据标注
- [推理训练-CoT](推理训练-CoT.md) — CoT / Meta-CoT；O 系列的核心

### 方法与对比

- [RLHF vs DPO](RLHF-vs-DPO.md) — 对齐两种主流实现；附 Rubix RL 的三条瓶颈
- [PEFT-LoRA](PEFT-LoRA.md) — 企业微调的默认范式
- [下半场-任务与Reward设计](下半场-任务与Reward设计.md) — Reward 三原则；Pass@k vs Pass@head k
- [表征学习](表征学习-RepresentationLearning.md) — 三条 SSL 路线；LeCun layer cake；谢赛宁的中心 bet

### 应用架构

- [RAG-检索增强生成](RAG-检索增强生成.md) — 私有知识问答的标准架构与六步流水线
- [向量数据库](向量数据库-VectorDatabase.md) — ANN 检索基础设施；RAG 流水线的存储与检索层
- [微调 vs RAG 决策](微调vs%20RAG-决策.md) — 知识进 RAG、行为进微调
- [REACT-推理与行动架构](REACT-推理与行动架构.md) — Thought / Action / Observation 循环
- [Code-AI的Affordance](Code-AI的Affordance.md) — 为什么 code 是 AI 的"手"；API vs GUI
- [JEPA-联合嵌入预测架构](JEPA-联合嵌入预测架构.md) — 在抽象表征空间做预测；AMI Labs 路线

### 多模态

- [多模态融合-生成理解割裂](多模态融合-生成理解割裂.md) — 为什么 CV 没有 GPT 时刻
- [视觉空间推理](视觉空间推理-多模态GPT-4时刻.md) — 视觉 CoT 的两条路径；预测一年内

### 机器人与具身智能

- [具身智能](具身智能-EmbodiedAI.md) — 子域入口；大脑+小脑；两次范式迁移
- [VLA-视觉语言动作模型](VLA-视觉语言动作模型.md) — Vision-Language-Action；ER-VLA 分层；RT 系列演进
- [跨本体](跨本体-CrossEmbodiment.md) — Motion Transfer；单本体数据凑不齐 scale
- [Sim-to-Real](Sim-to-Real.md) — 数据金字塔；video gen 作为新仿真

### 前沿议题与展望

- [NTP的本质缺陷](NTP的本质缺陷.md) — 压缩率 ≠ 计算精度
- [LongContext与分层记忆](LongContext与分层记忆.md) — 分层记忆 vs Transformer 不压缩；冯诺依曼 memory hierarchy
- [自主学习与在线学习](自主学习与在线学习.md) — Rubix 瓶颈指向的下一代范式；预测两年内
- [世界模型](世界模型-WorldModel.md) — 三大流派（生成 / 3D / 抽象表征）；为什么 LLM 是 flawed world model

### 参考

- [LLM术语速查](LLM术语速查.md) — 术语精确定义、阶段顺序、易混淆概念对比
- [Bitter Lesson](Bitter-Lesson.md) — Sutton 2019；LLM 是否是 bitter lesson 的争论
- [Moravec悖论](Moravec悖论.md) — "难的容易、容易的难"；在 LLM 时代再印证

---

## AI 产品与公司

- [Dify-开源LLM应用平台](Dify-开源LLM应用平台.md) — 开源全栈 LLM 应用开发平台；Workflow+RAG+Agent+Plugin 一站式
- [LangGenius-Dify母公司](LangGenius-Dify母公司.md) — Dify 的跨法域运营主体结构
- [张路宇-Dify创始人](张路宇-Dify创始人.md) — Dify Founder & CEO；连续创业者，前腾讯 CODING

---

## 活动日志

查看 [Wiki 活动日志](log.md)。
