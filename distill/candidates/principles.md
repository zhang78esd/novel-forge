# 阶段 1 候选池 — 原则 / 硬规则 / 清单

| # | 候选原则 | 来源 | 最终去向 |
|---|---|---|---|
| P1 | 去 AI 味 = 三层诊断 + 确定性预检，零命中不代替三层扫描 | oh-story story-deslop | deslop |
| P2 | 写前必读清单（整份读，检索/摘读不算） | oh-story story-long-write | continuation |
| P3 | 追踪唯一底账，投影文件禁止手改 | oh-story story-long-write | state-ledger |
| P4 | 作者真相与读者已知分开记录 | oh-story README | information-boundary |
| P5 | 审查是找问题，不是验证正确性 | oh-story story-review | review-gate |
| P6 | 导入源与对标硬隔离 | oh-story story-import | import-legacy |
| P7 | 三大黄金法则（展示/冲突/钩子） | chinese-novelist SKILL | chapter-craft |
| P8 | 冲突先阻断再裁决 + 优先级链 | webnovel-writer webnovel-plan | outline-architecture |
| P9 | 不伪造结论 / 只读边界 | webnovel-writer webnovel-review | review-gate |
| P10 | 先登记后动笔 / 到期必兑 | chinese-novelist outline-template | project-bootstrap / foreshadow-ledger |
| P11 | 字数校验必须由脚本完成，禁止模型估算 | chinese-novelist shared-infrastructure | review-gate |
| P12 | 每章必须回答四件事 | Chinese-WebNovel-Skill SKILL | chapter-craft |
| P13 | 每章强制回答四件事 + 连载一致性清单 | Chinese-WebNovel-Skill quality-checklist | chapter-craft / foreshadow-ledger |
| P14 | 去 AI 味硬规则五条（能用动作不用总结等） | Chinese-WebNovel-Skill SKILL | deslop |
| P15 | 章节状态动态回写（chapter-meta / character-state） | sumeru write | state-ledger |
| P16 | 确定性工具优先（统计/校验/导出走脚本） | sumeru CLAUDE | review-gate |
| P17 | 风格模块按需加载 | sumeru outline | chapter-craft / overview |
| P18 | 承诺三态 planned→planted→paid-off | story-skills plot-structure | foreshadow-ledger |
| P19 | reader-knowledge 过滤 | story-skills chapter-writing | information-boundary |
| P20 | 每章强制状态回写（Dynamic Update Rules） | Novel-Control-Station SKILL | state-ledger |
| P21 | 9 项写前强制重读 | wordflowlab pre-write-checklist | continuation |
| P22 | 遗忘阈值 10/12/20 章 | wordflowlab forgotten-elements | foreshadow-ledger（标为经验参数） |
| P23 | 翻案腔按动作禁（含 6 类变形） | human-writing human-writing-lite | deslop |
| P24 | 标点与黑话硬禁令 | human-writing revision | deslop |
| P25 | 不要盲洗：保留题材语域/时代质地/人物声音 | Novel-Control-Station SKILL | deslop |
| P26 | 悬念钩子十三式 / 章首引子七式 | chinese-novelist hook-techniques | chapter-craft |
| P27 | 悬念强度等级 1–5 波浪递进 | chinese-novelist hook-techniques | chapter-craft / outline-architecture |
| P28 | 黄金爽点密度 3–5 / 10–15 / 30–50 章 | sumeru outline | outline-architecture（标为诊断参数） |
| P29 | 金手指三字段：来源/限制/成长空间 | sumeru outline | outline-architecture |
| P30 | 一章只能有一个结尾 | chinese-novelist content-expansion | chapter-craft / failure-patterns |
| P31 | 防注水判据「删掉这段，故事是否变差？」 | chinese-novelist content-expansion | failure-patterns |
| P32 | 新名词首现给类别 + 可感知特征 | chinese-novelist chapter-guide | information-boundary |
| P33 | 场景结果四值 yes-but / no-and 等 | story-skills plot-structure | outline-architecture（未单列，见 coverage-audit） |
| P34 | 并行写入协议：共享文件只用 Edit 且改前重读 | chinese-novelist phase3 | parallel-writing |
