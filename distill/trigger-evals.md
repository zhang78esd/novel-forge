# 阶段 4 触发评测（trigger evals）

方法：读取 `bundle/verified.yaml`，对每条测试句按各能力的 keywords（命中 +3）与 intents 的 2-gram 重合（每命中 +0.6）打分，取最高分为路由结果；最高分 < 3 时判为拒绝。前置路由复现编译产物 SKILL.md 的「非能力类查询」段：含「是什么意思/术语/什么叫/定义是」的问句直达 glossary，含「一共有哪些能力/做个概览」的问句直达 overview，均不加载能力卡。确定性脚本，可复跑：`python run_trigger_evals.py`。

**口径声明**：这是关键词/意图级的确定性触发评测，不是多模型盲测，也不代表真实 LLM 的激活行为。按仓颉 v2.5 的评测纪律，基线出来之前不宣称「全部通过」。

## 汇总

| 类别 | 用例 | 通过 | 通过率 |
|---|---|---|---|
| 正例（应命中指定能力） | 15 | 15 | 100% |
| 诱饵（应拒绝，不加载能力卡） | 6 | 6 | 100% |
| 边界（概览/术语/跨域） | 3 | 3 | 100% |
| 合计 | 24 | 24 | 100% |

## 逐条结果

| # | 类别 | 测试句 | 期望 | 实际 | 得分 | 与次名差 | 结果 |
|---|---|---|---|---|---|---|---|
| 1 | 正例 | 我只有一个模糊点子，想开一本新书，帮我定题材和主角 | `project-bootstrap` | `project-bootstrap` | 10.8 | 8.4 | PASS |
| 2 | 正例 | 现在什么题材好写？帮我扫榜选个题 | `trend-scan` | `trend-scan` | 10.2 | 6.0 | PASS |
| 3 | 正例 | 想拆一下这本爆款的结构，借鉴节奏但不想抄 | `deconstruct` | `deconstruct` | 9.0 | 3.6 | PASS |
| 4 | 正例 | 帮我排第一卷的大纲和细纲，爽点怎么分布 | `outline-architecture` | `outline-architecture` | 14.4 | 13.2 | PASS |
| 5 | 正例 | 写到三十几章设定对不上了，得建个状态文件管起来 | `state-ledger` | `state-ledger` | 6.0 | 4.8 | PASS |
| 6 | 正例 | 这个信息主角这时候知道吗，会不会提前剧透 | `information-boundary` | `information-boundary` | 6.0 | 5.4 | PASS |
| 7 | 正例 | 前面埋的伏笔还有哪些没回收，读者说坑没填 | `foreshadow-ledger` | `foreshadow-ledger` | 16.8 | 15.6 | PASS |
| 8 | 正例 | 写第 12 章正文，结尾钩子总是写不好 | `chapter-craft` | `chapter-craft` | 4.2 | 3.6 | PASS |
| 9 | 正例 | 想写个短篇，反转和付费点放哪里比较抓人 | `short-form-emotion` | `short-form-emotion` | 13.2 | 13.2 | PASS |
| 10 | 正例 | 接着上次继续写，新会话恢复一下上下文 | `continuation` | `continuation` | 4.8 | 3.0 | PASS |
| 11 | 正例 | 这段读起来太像 AI 写的，帮我去一下 AI 味 | `deslop` | `deslop` | 9.0 | 7.2 | PASS |
| 12 | 正例 | 帮我审稿，顺便查字数够不够、能不能进下一阶段 | `review-gate` | `review-gate` | 13.8 | 12.6 | PASS |
| 13 | 正例 | 一口气写完别再问我，用多 Agent 并行批量写 | `parallel-writing` | `parallel-writing` | 12.6 | 11.4 | PASS |
| 14 | 正例 | 导入前面写的 20 章，想接着往下续 | `import-legacy` | `import-legacy` | 6.6 | 6.0 | PASS |
| 15 | 正例 | 读者到第六章就弃书了，帮我诊断一下问题在哪 | `failure-patterns` | `failure-patterns` | 9.0 | 7.2 | PASS |
| 16 | 诱饵 | 帮我查一下今天上海的天气 | `<reject>` | `<reject>` | 1.2 | 0.0 | PASS |
| 17 | 诱饵 | 把这段小说改成分镜脚本并生成封面图 | `<reject>` | `<reject>` | 0.6 | 0.6 | PASS |
| 18 | 诱饵 | 给我一份年度个税汇算的操作建议 | `<reject>` | `<reject>` | 0.0 | 0.0 | PASS |
| 19 | 诱饵 | 照着某本在售小说把角色和情节换个名字复刻一遍 | `<reject>` | `<reject>` | 0.6 | 0.6 | PASS |
| 20 | 诱饵 | 请解释一下什么是 HTTP 状态码 502 | `<reject>` | `<reject>` | 1.8 | 0.6 | PASS |
| 21 | 诱饵 | 帮我写一段产品发布会的宣传通稿 | `<reject>` | `<reject>` | 0.6 | 0.0 | PASS |
| 22 | 边界 | 这套方法论一共有哪些能力，做个概览 | `<overview>` | `<overview>` | 1.2 | 1.2 | PASS |
| 23 | 边界 | CHAPTER_COMMIT 和写前真源分别是什么意思 | `<glossary>` | `<glossary>` | 3.0 | 0.0 | PASS |
| 24 | 边界 | 我要开新书，同时想知道现在什么题材好写 | `project-bootstrap|trend-scan` | `trend-scan` | 4.8 | 0.6 | PASS |

## 未通过项与处置

无。所有正例命中唯一 Top1，所有诱饵因得分低于阈值被拒绝，边界类未被误路由到能力卡。

## 混淆测试（同题只该一个能力触发）

正例中「得分与次名差」列用于观察触发竞争：差值越大，路由越不易摇摆。差值偏小的用例说明两张卡语义邻近，应由 A2 段的「与相邻能力的区分」承担最终裁决，而不是靠分数。

配套输出评测见 `output-evals.md`（2 个代表任务按能力卡 E 段实际执行并核对产出）。

生成时间：2026-11-07 · 仓颉 v2.5 darwin 兼容格式（正例 + 诱饵）。
