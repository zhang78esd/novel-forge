# novel-forge

中文小说 / 网文创作全流程 Agent Skill。用 [仓颉 skill](https://github.com/kangarooking/cangjie-skill) v2.5 的 RIA-TV++ 流水线，把 GitHub 上 9 个高星写小说 skill 蒸馏成 **1 个路由入口 + 15 张能力卡**。

## 为什么

同一主题下堆十几个 skill，会带来安装负担、理解成本和触发竞争：用户问一个问题，两三个 skill 都觉得自己该上。仓颉 v2.5 的实测里，19 个平铺技能光「名字 + 描述」的发现目录就要 3,897 tokens，收敛成 1 个路由入口后是 340 tokens。

所以这里不是把九份文档拼接，而是拆成互不重叠的能力卡，用一个路由表按意图**只加载 1 张**（跨域最多 2 张）。

## 来源

九个开源仓库（★ 与安装量为 2026-11-07 快照）：

| 仓库 | ★ | 主要贡献 |
|---|---|---|
| `zenstory-ai/oh-story-claudecode` | 8,369 | 全链路、去 AI 味 lint、逆向导入 |
| `lingfengQAQ/webnovel-writer` | 7,884 | 写前/写后真源、CHAPTER_COMMIT |
| `KKKKhazix/human-writing` | 4,450 | 翻案腔判定、中文语感硬规则 |
| `PenglongHuang/chinese-novelist-skill` | 4,670 | 三层问答、钩子十三式、四阶段流程 |
| `Tomsawyerhu/Chinese-WebNovel-Skill` | 979 | 每章四问、故事承诺 |
| `jingtai123/Novel-Control-Station-Skill` | 433 | 动态状态回写、疯狂创作模式 |
| `danjdewhurst/story-skills` | 394 | promises/payoffs 三态机 |
| `wordflowlab/novel-writer-skills` | 270 | 写前重读、遗忘阈值、警报格式 |
| `xindoo/sumeru` | 223 | 状态回证、阶段门禁、伏笔台账 |

跨源最强的共识：**长篇质量是事实管理问题，不是文笔问题**。四家独立实现「每章写后强制回写状态」，三家独立实现「作者真相 / 读者已知分离」，三家独立实现「去味不能靠加戏」。

## 安装

```bash
npx skills add zhang78esd/novel-forge
```

或把整个仓库目录放进 Agent 的 skills 目录。触发后直接说需求即可：

| 你说 | 加载的能力卡 |
|---|---|
| 我有个点子，想开本新书 | `project-bootstrap` |
| 写到第 30 章设定对不上了 | `state-ledger` |
| 这段太像 AI 写的 | `deslop` |
| 为什么没人追 | `failure-patterns` |
| 导入前面写的 20 章 | `import-legacy` |

## 15 张能力卡

`project-bootstrap` · `trend-scan` · `deconstruct` · `outline-architecture` · `state-ledger` · `information-boundary` · `foreshadow-ledger` · `chapter-craft` · `short-form-emotion` · `continuation` · `deslop` · `review-gate` · `parallel-writing` · `import-legacy` · `failure-patterns`

每张按 RIA++ 六段组织：R 原文出处（≤150 字）、I 方法论骨架、A1 案例、A2 触发场景与相邻能力区分、E 可执行步骤（含输入/输出契约与完成标准）、B 边界与失败模式。

## 目录结构

```
SKILL.md                     # 唯一路由入口：意图路由表 / 核心原则 / 加载规则 / 边界判停
references/
  capabilities/*.md          # 15 张能力卡
  capability-index.md        # 完整意图与关键词索引
  cheatsheet.md              # 决策规则速查
  overview.md                # 资料集概览（含对来源的批判与盲点）
  glossary.md                # 术语词典
```

## 验证

- 仓颉 `validate_skill_pack.py`：**0 errors / 0 warnings**（20 个 .md，1 个 SKILL.md）
- 触发评测：**24/24**（15 正例 + 6 诱饵 + 3 边界，关键词/意图级确定性匹配）
- 输出评测：2 个代表任务按 E 段实际执行，均 PASS
- 覆盖率：19 类关键任务全部有去向，9/9 来源至少贡献 1 张卡

## 边界

- 产物只提炼**方法论**，不含来源仓库的专有设定、角色、事件链或可执行脚本。
- 爽点密度、遗忘阈值等经验值标为诊断参数，不作硬配额；不承诺「过 AI 检测」。
- 拆文只迁移抽象机制：专名换功能位占位符，最长连续重合 ≤12 字。
- 触发评测不是多模型盲测，输出评测未覆盖全部 15 张卡，故不宣称全场景完整通过。
- 封面生图、短剧分镜、视频生成等改编环节不在范围内。

## 致谢与许可

方法论归功于上表九个开源项目及其作者，蒸馏工具为 `kangarooking/cangjie-skill`（MIT）。本仓库的编排与文字为原创整理，卡片 R 段为带出处的短引用，用于说明机制。

MIT License。商用前请自行核查各来源仓库的许可与版权边界。
