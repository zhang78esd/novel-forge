# 资料集概览 — 九源写小说 Skill

## 结构（Adler 第一步：这本书讲什么）

本次蒸馏的「书」不是一本书，而是一份资料集：GitHub 上按 star 与安装量排名靠前的 9 个中文/英文写小说 Agent Skill 仓库，共 144 个 Markdown 文件。它们共同回答一个问题：**怎么让 AI 稳定地写完一部长篇，而不是写出一堆会互相矛盾的章节**。

九源构成一条隐含的流水线，彼此互补而非同质：

| 环节 | 主要来源 | 独门贡献 |
|---|---|---|
| 选题 | oh-story-claudecode | 多榜重复模式才算趋势；拆文只迁移抽象机制 |
| 定位与行文 | chinese-novelist-skill | 三层问答、三大黄金法则、钩子十三式/引子七式、三段式播种 |
| 长篇工程 | webnovel-writer | 写前真源/写后真源/投影层、CHAPTER_COMMIT |
| 长篇工程 | sumeru、Novel-Control-Station | 状态回证、阶段门禁、伏笔台账、疯狂创作模式 |
| 专项精修 | Chinese-WebNovel-Skill | 按需单层输出、每章四问、故事承诺 |
| 一致性 | story-skills、wordflowlab | promises/payoffs 三态机、遗忘阈值、警报格式 |
| 语感 | human-writing | 翻案腔按动作禁、标点与黑话禁令 |

## 解释（第二步：核心论点）

跨源最强的共识是：**长篇质量不是文笔问题，是事实管理问题**。四家独立实现「每章写后强制回写状态」，三家独立实现「作者真相/读者已知分离」，三家独立实现「去味不能靠加戏」。这三条在本次 Bundle 中分别固化为 `state-ledger`、`information-boundary`、`deslop`。

第二个共识是**入口要少、能力要多**：九源共 100+ 个 skill，若平铺安装会造成触发竞争与目录膨胀。仓颉 v2.5 的 single 形态（1 个路由入口 + 按需加载 1–2 张能力卡）正好解决这一点——这也是用户「蒸馏成一个新的 skill」的目标形态。

## 批判（第三步：来源的盲点与冲突）

- **工具绑定过强**：多数来源把方法论绑在特定脚本/目录结构上（如 `tracking_commit.py`、`CHAPTER_COMMIT`）。本包抽的是机制，不假设用户装了这些脚本；卡片 E 段给出无脚本时的降级约定。
- **长篇偏向**：九源里 7 个面向百万字网文，短篇与中篇被当作附属。故单列 `short-form-emotion`，并在 `outline-architecture`、`state-ledger` 的 B 段写明短篇不适用。
- **量化阈值来源不明**：如「每 3–5 章一个小爽点」「遗忘阈值 10/12/20 章」是经验值，不是实测结论。卡片中标注为诊断参数，不作为硬配额。
- **平台检测争议**：多源以「过朱雀/降 AI 率」为卖点。本包明确外部检测器只作自测参考，不替代人工读感。
- **口径冲突**：`chinese-novelist` 第三、四阶段「禁止向用户确认」，而 `oh-story` 要求「裸调用不得自动开写」。本包的裁决是：模式与范围须显式确认；确认之后，逐章过程不再打断——两者并不矛盾，见 `parallel-writing`。

## 应用（第四步：什么时候用）

- 从零开书 → 先 `project-bootstrap`，需要市场校准再前置 `trend-scan`。
- 写到中段崩设定 → `state-ledger` + `information-boundary` + `foreshadow-ledger`。
- 单章写不好 → `chapter-craft` 写，`deslop` 清语感，`review-gate` 校验。
- 不知道哪里不对 → `failure-patterns` 定位主因后再转派。
- 已有旧稿 → `import-legacy`，不要重做定位问答。

## 来源与边界

所有能力卡的 R 段引用均来自 9 源真实文件，出处见各卡；引用长度 ≤150 字/段。本包是方法论提炼，不含任何来源仓库的专有设定、角色、事件链或可执行脚本。来源仓库均为 MIT/Apache 等开源许可，清单见 SOURCES.md。
