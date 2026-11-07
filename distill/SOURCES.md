# 蒸馏语料来源清单

采集时间：2026-11-07。语料存放于临时目录 `C:/Users/lenovo/AppData/Local/Temp/novel-distill/corpus/`（144 个 Markdown 文件，约 1 MB），不随产物交付。

| # | 仓库 | GitHub ★ | skills.sh 安装量 | 本次取用文件 | 主要贡献 |
|---|---|---|---|---|---|
| 1 | `zenstory-ai/oh-story-claudecode` | 8,369 | 229.7K | 37 | 扫榜/拆文/长写/短写/去味/导入/审查，14 个 SKILL.md + README |
| 2 | `PenglongHuang/chinese-novelist-skill` | 4,670 | 6.7K | 22（完整 clone） | 三层问答、三大黄金法则、钩子十三式、引子七式、四阶段流程 |
| 3 | `lingfengQAQ/webnovel-writer` | 7,884 | 5.3K | 13 | 写前/写后真源、CHAPTER_COMMIT、跨卷一致性、BLOCKER |
| 4 | `xindoo/sumeru` | 223 | 6.1K | 16 | 状态回证、阶段门禁、伏笔台账、分层上下文、爽点密度 |
| 5 | `Tomsawyerhu/Chinese-WebNovel-Skill` | 979 | 382 | 6 | 按需单层输出、每章四问、故事承诺、去 AI 味正反对照 |
| 6 | `danjdewhurst/story-skills` | 394 | 11.9K | 16 | promises/payoffs 三态、项目文件格式、reader-knowledge 过滤 |
| 7 | `wordflowlab/novel-writer-skills` | 270 | 7.5K | 16 | 9 项写前重读、一致性警报格式、遗忘阈值 |
| 8 | `jingtai123/Novel-Control-Station-Skill` | 433 | 100 | 16 | 每章动态状态回写、疯狂创作模式、风格模块按需加载、不要盲洗 |
| 9 | `KKKKhazix/human-writing` | 4,450 | 824 | 8 | 翻案腔按动作禁、标点与黑话禁令、翻案腔坏/好对照 |

★ 与安装量为 2026-11-07 通过 GitHub REST API 与 skills.sh 实时抓取；口径说明见上一轮排名答复。安装量是仓库内所有 skill 安装次数之和，不等于独立用户数。

## 元信息映射（仓颉阶段 0 要求）

| 字段 | 本次取值 |
|---|---|
| 内容类型 | 资料集（9 个开源仓库的 SKILL.md / README / references / guides） |
| 「书名」 | 中文小说创作能力合集：GitHub 写小说 Skill 榜单九源蒸馏 |
| 「作者」 | 九个开源项目作者（见上表） |
| 「出版时间」 | 各仓库 2025–2026 年持续更新；本次采集快照 2026-11-07 |
| 「章节」 | 映射为各仓库的相对文件路径，用于卡片 R 段定位 |
| 使用目的 | workflow（接入日常创作工作流）→ 用户显式指定 single 形态 |
| 是否首次试点 | 是，一次性蒸馏 1 份资料集，未批量 |

## 版权与合规

- 所有来源均为 GitHub 公开开源仓库（MIT / Apache-2.0 等许可），仅做**方法论提炼**。
- 卡片 R 段引用均为 ≤150 字的短摘录，标注出处，用于说明机制，不复制完整文档。
- 产物不含任何来源仓库的专有设定、角色、事件链、原句模板或可执行脚本。
- 原仓库中的脚本名仅作为机制说明出现，产物不附带、不执行这些脚本。
- 蒸馏遵循「法律保护表达、不保护思想方法」的边界；商用前请自行核查各来源许可。
