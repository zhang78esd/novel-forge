# 流水线状态

- 项目：bundle.novel-forge
- 方法：仓颉 skill v2.5.0（RIA-TV++ / ADR-002 Capability Bundle）
- 当前阶段：**阶段 5 完成，已交付**
- 输出模式：single（用户显式指定，策略 single-first-v1）
- 最后更新：2026-11-07 14:45

| 阶段 | 状态 | 产出 |
|---|---|---|
| 0 整书理解 | ✓ | `BOOK_OVERVIEW.md`、`bundle/book/overview.md` |
| 1 五维并行提取 | ✓ | 4 个提取器（框架/原则/案例/反例/术语），`candidates/` |
| 1.5 三重验证 | ✓ | `verified.md`、`rejected/`、`coverage-audit.md` |
| 1.6 晋级门 | ✓ | `verified.yaml` 的 `promotion.destination` 全部 router、`destinations.json` |
| 2 RIA++ 能力卡 | ✓ | `bundle/cards/*.md`（15 张，六段齐全） |
| 3 Zettelkasten 链接 | ✓ | `also_read`、`bundle/book/glossary.md`、编译器生成索引 |
| 4 压力测试 | ✓（限定范围） | `trigger-evals.md`、`trigger-evals.json`、`output-evals.md` |
| 5 编译与交付 | ✓ | `novel-forge/`、`DIGEST.md`、`SOURCES.md` |

## 产物路径

- 可安装 Skill：`D:/漫剧/小说/novel-forge/`（20 个文件，156 KB）
- 编译事实源：`D:/漫剧/小说/novel-forge-distill/bundle/verified.yaml`
- 能力卡：`D:/漫剧/小说/novel-forge-distill/bundle/cards/`
- 语料（临时，不随产物交付）：`C:/Users/lenovo/AppData/Local/Temp/novel-distill/corpus/`

## 校验记录

- 编译器 staging 校验：首次因能力卡内残留来源仓库相对链接报 1 error，已修复；第二次 0 errors / 0 warnings，原子发布成功。
- 独立格式校验：`validate_skill_pack.py novel-forge/` → 0 errors, 0 warnings，扫描 20 个 .md / 1 个 SKILL.md。
- 编译 run id：`run-20261107-144454-14679c`。

## 断点续跑 / 增量更新

1. 修改 `bundle/cards/*.md` 与 `bundle/verified.yaml`（文案润色只加 revision；语义拆分才换 capability_id）。
2. 重跑 `python build_bundle.py` 会覆盖 `verified.yaml` 与 `destinations.json`（**不会覆盖 cards 与 book**）。
3. 重跑 `python run_trigger_evals.py` 刷新触发评测。
4. 重新编译需加 `--force-overwrite`（编译器检测到已发布目录中的本地手改时不会静默覆盖）。

## 已知限制

- 触发评测为关键词/意图级确定性匹配，非多模型盲测。
- 输出评测仅覆盖 2 个代表任务，未做全 15 卡回归。
- 实时榜单采集脚本、原仓库脚本本体未随产物交付。
- 英文创作场景未经实测。
