# 覆盖率审计：来源 → 候选 → 判定 → 交付去向

仓颉阶段 1 要求「覆盖率硬门」：对照全量扫描候选与阶段 0 的原书关键任务清单，重要任务须有候选及明确去向；有未解释遗漏时补读，不虚报零遗漏。

## A. 关键任务覆盖（面向使用者的 15 类真实请求）

| # | 关键任务 | 候选 | 判定 | 实际交付去向 |
|---|---|---|---|---|
| 1 | 从模糊点子开新书 | 三层问答、故事承诺、设定词典 | verified | `project-bootstrap` |
| 2 | 判断写什么题材有市场 | 扫榜五阶段、核心信念 | verified | `trend-scan` |
| 3 | 学一本爆款但不抄 | 拆文六阶段、抽象化占位符 | verified | `deconstruct` |
| 4 | 排大纲 / 分卷 / 细纲 | 跨卷一致性、结构化节点、爽点密度 | verified | `outline-architecture` |
| 5 | 节奏太慢 / 中段散 | 同上 + 悬念强度波浪递进 | verified | `outline-architecture` + `chapter-craft` |
| 6 | 写某一章正文 | 黄金法则、每章四问、钩子模板 | verified | `chapter-craft` |
| 7 | 开头/结尾抓不住人 | 引子七式、钩子十三式、三段式 | verified | `chapter-craft` |
| 8 | 写短篇 / 爽文 | 短篇四阶段、六种目标情绪 | verified | `short-form-emotion` |
| 9 | 写到几十章设定对不上 | 唯一底账、跨卷检查、六类底线 | verified | `state-ledger` + `review-gate` |
| 10 | 角色提前知道不该知道的 | 作者真相/读者已知、信息边界 | verified | `information-boundary` |
| 11 | 伏笔只埋不收 / 坑没填 | 伏笔台账、三态机、到期必兑 | verified | `foreshadow-ledger` |
| 12 | 换会话接着写 | 断点检测、分层上下文、写前必读 | verified | `continuation` |
| 13 | AI 味重 / 要改得像人写 | 确定性 lint、三层扫描、翻案腔 | verified | `deslop` |
| 14 | 审稿 / 字数 / 能不能进下一阶段 | 审查铁律、3 轮修复、阶段门禁 | verified | `review-gate` |
| 15 | 批量连写 / 别再问我 | 三种模式、marathon、防失控 | verified | `parallel-writing` |
| 16 | 已有前 20 章旧稿要续写 | 逆向导入五阶段 | verified | `import-legacy` |
| 17 | 「没人追」但说不清哪里 | 悬念禁忌、六类底线、常见无效开头 | verified | `failure-patterns` |
| 18 | 概览 / 术语解释 | 全源术语表 | reference | `references/overview.md`、`glossary.md` |
| 19 | 封面图 / 分镜 / 改游戏 | 多源附属能力 | out_of_scope | SKILL.md「不适用」段明确排除 |

**结论**：19 类关键任务全部有明确去向，无未解释遗漏。第 19 类为主动边界声明，不是遗漏。

## B. 来源覆盖（9 源 → 能力映射）

| 来源 | 被哪些能力引用 | 是否至少 1 张卡 |
|---|---|---|
| oh-story-claudecode | trend-scan, deconstruct, state-ledger, information-boundary, short-form-emotion, continuation, deslop, review-gate, parallel-writing, import-legacy | ✓ |
| chinese-novelist-skill | project-bootstrap, information-boundary, foreshadow-ledger, chapter-craft, continuation, review-gate, parallel-writing, failure-patterns | ✓ |
| webnovel-writer | outline-architecture, state-ledger, review-gate | ✓ |
| sumeru | deconstruct, outline-architecture, foreshadow-ledger, short-form-emotion, continuation, review-gate, failure-patterns | ✓ |
| Chinese-WebNovel-Skill | project-bootstrap, foreshadow-ledger, chapter-craft, deslop | ✓ |
| story-skills | information-boundary, foreshadow-ledger | ✓ |
| wordflowlab | state-ledger, foreshadow-ledger, continuation, review-gate | ✓ |
| Novel-Control-Station | state-ledger, deslop, parallel-writing, continuation | ✓ |
| human-writing | deslop | ✓ |

**结论**：9/9 来源都至少贡献 1 张卡的 R 段或硬规则，无「挂名来源」。

## C. 补读记录

- 首轮语料下载时 `story-skills`、`wordflowlab`、`Novel-Control-Station`、`human-writing` 四个仓库尚未到位，第三提取器如实报告「目录不存在，未编造」。
- 下载完成后派第四提取器补读这 4 目录共 55 个文件，据此新增/补强：`information-boundary`（reader-knowledge）、`foreshadow-ledger`（promises 三态）、`deslop`（翻案腔按动作禁）、`parallel-writing`（marathon mode）、`continuation`（9 项重读）、`review-gate`（一致性警报格式）。
- 原文引用抽查：对 10 条关键摘录在语料中做全文检索，9 条逐字命中；1 条为措辞差异（脚本字数校验条），已改用核对过的原句入卡。

## D. 未覆盖与已知缺口

- **实时榜单数据**：产物不含采集脚本，无实时数据时应声明局限（已写入 `trend-scan` 输入契约与 B 段）。
- **多模型盲测**：本次触发评测为关键词/意图级确定性匹配，非 LLM 盲测；输出评测只覆盖 2 个代表任务。见 `trigger-evals.md`、`output-evals.md`。
- **英文创作**：语料以中文网文为主，英文向机制（`story-skills`）已抽象但未经英文写作任务实测。
- **平台政策**：过稿规则、AI 声明合规等随平台变化，主动排除。

据此，本包按仓颉质量红线第 8 条交付为「明确标注范围的可用产物」，不宣称全场景完整通过。
