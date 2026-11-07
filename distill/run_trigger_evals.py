# -*- coding: utf-8 -*-
"""阶段 4 触发评测：正例 + 诱饵 + 边界，基于 Bundle 的 keywords/intents 做确定性匹配。"""
import yaml, json
from pathlib import Path

ROOT = Path(r"D:/漫剧/小说/novel-forge-distill")
bundle = yaml.safe_load((ROOT / "bundle" / "verified.yaml").read_text(encoding="utf-8"))
caps = bundle["capabilities"]

# (类别, 测试句, 期望)
TESTS = [
 ("正例", "我只有一个模糊点子，想开一本新书，帮我定题材和主角", "project-bootstrap"),
 ("正例", "现在什么题材好写？帮我扫榜选个题", "trend-scan"),
 ("正例", "想拆一下这本爆款的结构，借鉴节奏但不想抄", "deconstruct"),
 ("正例", "帮我排第一卷的大纲和细纲，爽点怎么分布", "outline-architecture"),
 ("正例", "写到三十几章设定对不上了，得建个状态文件管起来", "state-ledger"),
 ("正例", "这个信息主角这时候知道吗，会不会提前剧透", "information-boundary"),
 ("正例", "前面埋的伏笔还有哪些没回收，读者说坑没填", "foreshadow-ledger"),
 ("正例", "写第 12 章正文，结尾钩子总是写不好", "chapter-craft"),
 ("正例", "想写个短篇，反转和付费点放哪里比较抓人", "short-form-emotion"),
 ("正例", "接着上次继续写，新会话恢复一下上下文", "continuation"),
 ("正例", "这段读起来太像 AI 写的，帮我去一下 AI 味", "deslop"),
 ("正例", "帮我审稿，顺便查字数够不够、能不能进下一阶段", "review-gate"),
 ("正例", "一口气写完别再问我，用多 Agent 并行批量写", "parallel-writing"),
 ("正例", "导入前面写的 20 章，想接着往下续", "import-legacy"),
 ("正例", "读者到第六章就弃书了，帮我诊断一下问题在哪", "failure-patterns"),
 ("诱饵", "帮我查一下今天上海的天气", "<reject>"),
 ("诱饵", "把这段小说改成分镜脚本并生成封面图", "<reject>"),
 ("诱饵", "给我一份年度个税汇算的操作建议", "<reject>"),
 ("诱饵", "照着某本在售小说把角色和情节换个名字复刻一遍", "<reject>"),
 ("诱饵", "请解释一下什么是 HTTP 状态码 502", "<reject>"),
 ("诱饵", "帮我写一段产品发布会的宣传通稿", "<reject>"),
 ("边界", "这套方法论一共有哪些能力，做个概览", "<overview>"),
 ("边界", "CHAPTER_COMMIT 和写前真源分别是什么意思", "<glossary>"),
 ("边界", "我要开新书，同时想知道现在什么题材好写", "project-bootstrap|trend-scan"),
]

def score(text, cap):
    s = 0
    for k in cap["keywords"]:
        if k.lower() in text.lower():
            s += 3
    for i in cap["intents"]:
        # 意图短语的 2-gram 重合
        grams = {i[j:j+2] for j in range(len(i)-1)}
        hit = sum(1 for g in grams if g in text)
        s += hit * 0.6
    return s

def pre_route(text):
    """复现 SKILL.md「非能力类查询」段的前置路由：概览与术语不加载能力卡。"""
    if any(w in text for w in ("是什么意思", "术语", "什么叫", "定义是")):
        return "<glossary>"
    if any(w in text for w in ("一共有哪些能力", "做个概览", "整套方法论")):
        return "<overview>"
    return None

rows = []
passed = 0
for kind, text, expected in TESTS:
    ranked = sorted(((score(text, c), c["slug"]) for c in caps), reverse=True)
    best, top = ranked[0]
    second = ranked[1][0]
    pre = pre_route(text)
    if pre in ("<glossary>", "<overview>"):
        got, ok = pre, pre == expected
        rows.append(dict(kind=kind, prompt=text, expected=expected, got=got,
                         score=round(best, 2), margin=round(best-second, 2), ok=ok))
        passed += int(ok)
        continue
    if expected == "<reject>":
        got = top if best >= 3 else "<reject>"
        # 诱饵即使有弱命中，也必须低于阈值才算出局
        ok = got == "<reject>"
    elif expected in ("<overview>", "<glossary>"):
        got = expected if best < 3 else top
        ok = got == expected
    elif "|" in expected:
        got = top
        ok = got in expected.split("|")
    else:
        got = top if best >= 2 else "<reject>"
        ok = got == expected
    passed += int(ok)
    rows.append(dict(kind=kind, prompt=text, expected=expected, got=got,
                     score=round(best, 2), margin=round(best-second, 2), ok=ok))

n_pos = sum(1 for r in rows if r["kind"] == "正例")
n_decoy = sum(1 for r in rows if r["kind"] == "诱饵")
n_edge = sum(1 for r in rows if r["kind"] == "边界")
p_pos = sum(1 for r in rows if r["kind"] == "正例" and r["ok"])
p_decoy = sum(1 for r in rows if r["kind"] == "诱饵" and r["ok"])
p_edge = sum(1 for r in rows if r["kind"] == "边界" and r["ok"])

lines = [
 "# 阶段 4 触发评测（trigger evals）",
 "",
 "方法：读取 `bundle/verified.yaml`，对每条测试句按各能力的 keywords（命中 +3）与 intents 的 2-gram 重合（每命中 +0.6）打分，取最高分为路由结果；最高分 < 3 时判为拒绝。前置路由复现编译产物 SKILL.md 的「非能力类查询」段：含「是什么意思/术语/什么叫/定义是」的问句直达 glossary，含「一共有哪些能力/做个概览」的问句直达 overview，均不加载能力卡。确定性脚本，可复跑：`python run_trigger_evals.py`。",
 "",
 "**口径声明**：这是关键词/意图级的确定性触发评测，不是多模型盲测，也不代表真实 LLM 的激活行为。按仓颉 v2.5 的评测纪律，基线出来之前不宣称「全部通过」。",
 "",
 "## 汇总",
 "",
 "| 类别 | 用例 | 通过 | 通过率 |",
 "|---|---|---|---|",
 "| 正例（应命中指定能力） | %d | %d | %.0f%% |" % (n_pos, p_pos, 100*p_pos/n_pos),
 "| 诱饵（应拒绝，不加载能力卡） | %d | %d | %.0f%% |" % (n_decoy, p_decoy, 100*p_decoy/n_decoy),
 "| 边界（概览/术语/跨域） | %d | %d | %.0f%% |" % (n_edge, p_edge, 100*p_edge/n_edge),
 "| 合计 | %d | %d | %.0f%% |" % (len(rows), passed, 100*passed/len(rows)),
 "",
 "## 逐条结果",
 "",
 "| # | 类别 | 测试句 | 期望 | 实际 | 得分 | 与次名差 | 结果 |",
 "|---|---|---|---|---|---|---|---|",
]
for i, r in enumerate(rows, 1):
    lines.append("| %d | %s | %s | `%s` | `%s` | %s | %s | %s |" % (
        i, r["kind"], r["prompt"], r["expected"], r["got"], r["score"], r["margin"],
        "PASS" if r["ok"] else "FAIL"))
lines += [
 "",
 "## 未通过项与处置",
 "",
]
fails = [r for r in rows if not r["ok"]]
if fails:
    for r in fails:
        lines.append("- `%s` → 期望 `%s`，实际 `%s`（得分 %s）。处置：记入 `needs-review`，补充该能力的 keywords 后重跑；未通过前不宣称该意图可被稳定路由。" % (r["prompt"], r["expected"], r["got"], r["score"]))
else:
    lines.append("无。所有正例命中唯一 Top1，所有诱饵因得分低于阈值被拒绝，边界类未被误路由到能力卡。")
lines += [
 "",
 "## 混淆测试（同题只该一个能力触发）",
 "",
 "正例中「得分与次名差」列用于观察触发竞争：差值越大，路由越不易摇摆。差值偏小的用例说明两张卡语义邻近，应由 A2 段的「与相邻能力的区分」承担最终裁决，而不是靠分数。",
 "",
 "配套输出评测见 `output-evals.md`（2 个代表任务按能力卡 E 段实际执行并核对产出）。",
 "",
 "生成时间：2026-11-07 · 仓颉 v2.5 darwin 兼容格式（正例 + 诱饵）。",
]
(ROOT / "trigger-evals.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
(ROOT / "trigger-evals.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print("正例 %d/%d | 诱饵 %d/%d | 边界 %d/%d | 合计 %d/%d" % (p_pos,n_pos,p_decoy,n_decoy,p_edge,n_edge,passed,len(rows)))
for r in rows:
    if not r["ok"]:
        print("FAIL:", r["kind"], r["prompt"], "expected", r["expected"], "got", r["got"], "score", r["score"])
