---
name: novel-forge
description: |
  中文小说/网文创作全流程能力入口。当用户要开新书、选题扫榜、拆解对标、排大纲与爽点、写章节、写短篇、断点续写、维护设定与伏笔、去 AI 味、审稿校验、并行连写、导入旧稿或诊断弃书原因时调用。按意图路由表加载 1 张能力卡，跨域任务最多 2 张。不适用于：非创作类事实问答、抄袭或复刻受版权保护作品的专有设定与表达、法律医疗金融建议、敏感有害内容。Triggers: 写小说/网文/开书/大纲/写章节/伏笔/去AI味/审稿/续写/novel/webnovel/writing
metadata:
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: single
  cangjie.bundle-id: bundle.novel-forge
  cangjie.capability-count: 15
  cangjie.entrypoint-count: 1
---
# 中文小说创作能力合集：GitHub 写小说 Skill 榜单九源蒸馏 — 全书能力入口

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- 非创作类事实问答、实时资讯、百科查询
- 抄袭或复刻他人作品的专有设定、角色组合、关键事件链与原句；拆文只迁移抽象机制
- 法律、医疗、金融等专业建议
- 封面生图、短剧分镜、视频生成等改编与制作环节（本包聚焦文字创作）

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. 先有写前真源（定位、故事承诺、设定与事实词典），再动笔；没有词典不许现场编数字。
2. 发生过的事实只记在一个底账里：写前真源 / 写后真源 / 投影层分开，投影文件禁止手改。
3. 作者真相与读者已知分离；正文只能用读者已知，角色只能用自己已知。
4. 一章 = 一次局面变化 + 一个翻页理由；钩子从前 20% 播种、末 10% 收获，短中长三条悬念弧并行。
5. 去 AI 味是「确定性规则定位硬伤 + 三层语义诊断」两层，既不机械替换也不靠加戏制造真人感。
6. 审查是找问题不是背书；字数与阶段交接必须由可执行校验判定，不靠模型估算。
7. 含糊指令不等于授权连写；模式与章节范围显式确认，无人值守也不许跳过内部控制步骤。

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 我有个点子，想开一本新书；帮我定题材、主角和核心冲突；开写前要建项目与设定词典 | references/capabilities/project-bootstrap.md | references/capabilities/outline-architecture.md、references/capabilities/information-boundary.md |
| 现在什么题材好写，帮我扫榜选题；这个点子有没有市场；拆一下这类爆款为什么火 | references/capabilities/trend-scan.md | references/capabilities/deconstruct.md、references/capabilities/project-bootstrap.md |
| 拆一下这本爆款的结构；想借鉴这个节奏但不想抄；把对标书拆成可迁移技法 | references/capabilities/deconstruct.md | references/capabilities/trend-scan.md、references/capabilities/import-legacy.md |
| 帮我排大纲、分卷和细纲；节奏太慢，重排爽点；下一卷怎么接上一卷的伏笔 | references/capabilities/outline-architecture.md | references/capabilities/project-bootstrap.md、references/capabilities/foreshadow-ledger.md、references/capabilities/state-ledger.md |
| 写到几十章设定开始对不上；新会话要恢复现在发生到哪了；这一章写完要把新事实入账 | references/capabilities/state-ledger.md | references/capabilities/continuation.md、references/capabilities/information-boundary.md、references/capabilities/foreshadow-ledger.md |
| 他这时候知道这件事吗；读者反馈剧透或角色未卜先知；计划揭示章到了要检查兑现 | references/capabilities/information-boundary.md | references/capabilities/state-ledger.md、references/capabilities/foreshadow-ledger.md |
| 前面埋的伏笔还有哪些没回收；读者说坑没填；新卷怎么接上一卷未回收项 | references/capabilities/foreshadow-ledger.md | references/capabilities/outline-architecture.md、references/capabilities/information-boundary.md、references/capabilities/state-ledger.md |
| 写第 X 章正文；开头或结尾写不出抓手感；这章是不是水了 | references/capabilities/chapter-craft.md | references/capabilities/continuation.md、references/capabilities/deslop.md、references/capabilities/failure-patterns.md |
| 写一个短篇或爽文单篇；反转和付费点怎么安排；读完没感觉，情绪不够 | references/capabilities/short-form-emotion.md | references/capabilities/trend-scan.md、references/capabilities/deslop.md |
| 接着上次继续写；写到后面老忘设定；上下文快满，需要精简投喂 | references/capabilities/continuation.md | references/capabilities/state-ledger.md、references/capabilities/parallel-writing.md、references/capabilities/chapter-craft.md |
| 这段太像 AI 写的，帮我改；编辑说 AI 味重 / 要过检测；全稿收尾前统一清语感 | references/capabilities/deslop.md | references/capabilities/chapter-craft.md、references/capabilities/failure-patterns.md、references/capabilities/review-gate.md |
| 帮我审稿、查这章有没有硬伤；字数够不够 / 全稿校验；能不能进入下一阶段 | references/capabilities/review-gate.md | references/capabilities/state-ledger.md、references/capabilities/failure-patterns.md、references/capabilities/foreshadow-ledger.md |
| 一口气写完别再问我；用多 Agent 并行批量写；选哪种写作模式 | references/capabilities/parallel-writing.md | references/capabilities/continuation.md、references/capabilities/state-ledger.md、references/capabilities/review-gate.md |
| 导入前面写的 20 章接着写；把旧稿反向解析成设定；从别的工具迁移项目 | references/capabilities/import-legacy.md | references/capabilities/deconstruct.md、references/capabilities/continuation.md、references/capabilities/state-ledger.md |
| 为什么没人追 / 数据掉了；开头劝退、看不懂设定；帮我诊断一下别直接改 | references/capabilities/failure-patterns.md | references/capabilities/chapter-craft.md、references/capabilities/deslop.md、references/capabilities/review-gate.md |

**非能力类查询**：
- 书名/作者/章节/整书概览 → references/overview.md
- 术语解释 → references/glossary.md
- 决策规则速查（不需要原文依据时） → references/cheatsheet.md
- 完整意图与关键词索引（本表未覆盖的意图先查这里） → references/capability-index.md

## 加载规则

- 每次任务先读本文件，再按路由表加载 **1** 张能力卡；任务明确跨域时最多加载 2 张。
- 概览/书名类问题不加载能力卡，用「核心原则」与 overview.md 回答。
- 路由表与 capability-index.md 都无法命中的意图，明确告知超出本书范围，不要硬套。

## 边界与判停

- 意图在路由表与能力索引中均无法命中 → 明确告知超出范围，不硬套写作框架。
- 没有正文/文本却要求拆文或导入 → 停下来要材料，不凭记忆蒸馏。
- 发现总纲与设定冲突 → 标 BLOCKER 停下等用户裁决，不擅自取舍、不自动顺稿。
- 用户只要求概览/术语解释 → 用核心原则与 overview/glossary 回答后即停，不加载能力卡。
- 涉及权利不明的版权文本或有害内容 → 停止改写，说明边界。
