# -*- coding: utf-8 -*-
"""按仓颉 skill v2.5 的 RIA-TV++ 流水线，从已验证候选构造 Capability Bundle 与审计文件。"""
import json, os, yaml
from pathlib import Path

ROOT = Path(r"D:/漫剧/小说/novel-forge-distill")
BUNDLE = ROOT / "bundle"
CARDS = BUNDLE / "cards"
BOOK = BUNDLE / "book"
for d in (CARDS, BOOK, ROOT / "candidates", ROOT / "rejected"):
    d.mkdir(parents=True, exist_ok=True)

# slug -> (title, importance, rationale, one_liner, intents, keywords, also_read, sources, fm_desc, tags)
CAPS = [
 dict(slug="project-bootstrap", title="开书定位与创作合同", importance="critical",
  rationale="9 源中 3 源把「先签合同再动笔」列为起点；缺定位/承诺/词典会直接导致后续所有状态与伏笔能力失效，覆盖审计中「开书」关键任务无替代去向。",
  one_liner="先三层问答定定位，再固化四类故事承诺，最后建设定与事实词典；没有词典不许动笔。",
  intents=["我有个点子，想开一本新书", "帮我定题材、主角和核心冲突", "开写前要建项目与设定词典"],
  keywords=["开书","定位","题材","premise","story bible","创作合同"],
  also_read=["outline-architecture","information-boundary"],
  sources=[("src-chinese-novelist","SKILL.md 第一阶段·三层递进式问答"),("src-webnovel-skill","outline_template 故事承诺"),("src-chinese-novelist","outline-template 设定与事实词典·登记规则")],
  fm_desc="当用户只有模糊点子要开新书、需要确定题材/主角/核心冲突、建立故事承诺与设定词典时调用。产出定位卡、承诺卡、词典三份写前真源。不适用于已有旧稿续写（走 import-legacy）、市场选题（走 trend-scan）或已定定位后的章节排布。Triggers: 开书/新书/定题材/premise/story bible/start a novel",
  tags=["planning","contract","premise"]),
 dict(slug="trend-scan", title="扫榜选材：找重复模式，不追单本爆款", importance="high",
  rationale="oh-story 把「单本排名只是线索」写成核心信念，是其全链路五步的第 1 步；覆盖「市场验证」关键任务，其余 8 源均无对应能力。",
  one_liner="单本爆款只是线索，多榜多作品的近期重复模式才支持趋势判断；只迁移抽象机制。",
  intents=["现在什么题材好写，帮我扫榜选题", "这个点子有没有市场", "拆一下这类爆款为什么火"],
  keywords=["扫榜","选题","趋势","爆款","trending","market"],
  also_read=["deconstruct","project-bootstrap"],
  sources=[("src-oh-story","skills/story-long-scan/SKILL.md 导语·核心信念"),("src-oh-story","skills/story-long-analyze/SKILL.md 分析边界")],
  fm_desc="当用户要选题、扫榜、验证点子是否有市场，或要解释某类爆款为什么成立时调用。输出选题决策与重复模式表。注意：单本排名不是趋势；无实时榜单数据时须声明局限，不编数据。不适用于单本书的纵向机制拆解（走 deconstruct）或已定题材后的定位收敛。Triggers: 扫榜/选题/什么题材好写/trending/market",
  tags=["research","selection"]),
 dict(slug="deconstruct", title="拆文：只迁移抽象机制，不复刻表达", importance="high",
  rationale="oh-story 与 sumeru 都把拆文设为独立管道，且有明确的工程约束（不重读）与衍生约束（专名占位符化）；是 trend-scan 与 outline-architecture 之间的必经环节。",
  one_liner="建索引→逐块只读一次→抽象成功能位与「动作+结果+代价」；专名零命中、连续重合 ≤12 字。",
  intents=["拆一下这本爆款的结构", "想借鉴这个节奏但不想抄", "把对标书拆成可迁移技法"],
  keywords=["拆文","拆书","对标","抽象迁移","reverse-engineer","structure"],
  also_read=["trend-scan","import-legacy"],
  sources=[("src-oh-story","skills/story-long-analyze/SKILL.md 导语·核心原则/分析边界"),("src-sumeru","skills/sumeru-deconstruct/SKILL.md 拆书禁忌/抽象化改写")],
  fm_desc="当用户要拆解单本作品、提炼结构或节奏、把对标书变成可迁移技法时调用。产出结构模板、节奏参数、功能位。硬约束：不凭记忆拆书、不复刻专名与原句、区分四条时间线。不适用于多书横向趋势（走 trend-scan）或将自己的旧稿迁移成项目（走 import-legacy）。Triggers: 拆文/拆书/借鉴结构/reverse-engineer",
  tags=["analysis","abstraction","copyright"]),
 dict(slug="outline-architecture", title="大纲与节奏：卷纲、细纲、爽点密度", importance="critical",
  rationale="webnovel-writer、sumeru、chinese-novelist 三源共同覆盖；跨卷一致性与节奏排布是长篇能否连载的决定项，覆盖审计中「排大纲」「接下一卷」两个关键任务。",
  one_liner="先查上一卷三条承接项，再按小 3–5 / 中 10–15 / 大 30–50 章布爽点，金手指必写来源·限制·成长空间。",
  intents=["帮我排大纲、分卷和细纲", "节奏太慢，重排爽点", "下一卷怎么接上一卷的伏笔"],
  keywords=["大纲","卷纲","细纲","爽点","节奏","outline","pacing"],
  also_read=["project-bootstrap","foreshadow-ledger","state-ledger"],
  sources=[("src-sumeru","skills/sumeru-outline/SKILL.md 节奏参数"),("src-webnovel-writer","webnovel-plan/SKILL.md Step 6 跨卷一致性检查")],
  fm_desc="当定位已定、要铺卷纲与章级细纲，或中段节奏发散、要开新卷承接上一卷、要补金手指限制时调用。产出卷纲、细纲表、爽点排布、伏笔写回。冲突标 BLOCKER 停下等裁决，不擅自取舍。不适用于具体行文（走 chapter-craft）与短篇（走 short-form-emotion）。Triggers: 大纲/分卷/细纲/爽点/节奏/outline/pacing",
  tags=["planning","structure","pacing"]),
 dict(slug="state-ledger", title="唯一底账：状态文件与每章强制回写", importance="critical",
  rationale="oh-story、webnovel-writer、Novel-Control-Station、wordflowlab 四源都以不同术语实现同一机制，是本次蒸馏中跨源佐证最强的一条；直接解决长篇「遗忘与幻觉」这一核心痛点。",
  one_liner="写前真源/写后真源/投影层三层分开，所有写入经唯一提交口，投影文件禁止手改。",
  intents=["写到几十章设定开始对不上", "新会话要恢复现在发生到哪了", "这一章写完要把新事实入账"],
  keywords=["状态文件","底账","一致性","回写","CHAPTER_COMMIT","canon","state"],
  also_read=["continuation","information-boundary","foreshadow-ledger"],
  sources=[("src-oh-story","skills/story-long-write/SKILL.md Phase 4 追踪"),("src-webnovel-writer","README 写章工作流"),("src-control-station","SKILL.md Dynamic Update Rules")],
  fm_desc="当长篇出现设定漂移、换会话要恢复状态、一章写完要登记新事实、或多 Agent 共享状态时调用。建立唯一底账并强制每章提交回写。硬约束：投影层只读、日志不作真相源、冲突标 BLOCKER。不适用于信息边界判定（走 information-boundary）与短篇单文件项目。Triggers: 状态/底账/接着写/前面矛盾/state/canon/continuity",
  tags=["continuity","state","engineering"]),
 dict(slug="information-boundary", title="信息边界：作者真相与读者已知分离", importance="critical",
  rationale="四栏词典在 chinese-novelist、oh-story、story-skills 三源独立出现（跨域验证通过）；「角色提前知道答案」是长篇最高频穿帮，且无其他能力可替代。",
  one_liner="维护客观发生与文本披露两条时间线，正文只能用「读者已知」栏，角色只能用自己已知的信息。",
  intents=["他这时候知道这件事吗", "读者反馈剧透或角色未卜先知", "计划揭示章到了要检查兑现"],
  keywords=["作者真相","读者已知","剧透","信息边界","POV","reader-knowledge"],
  also_read=["state-ledger","foreshadow-ledger"],
  sources=[("src-oh-story","README 续写状态卡·为什么连载几百章不崩盘"),("src-chinese-novelist","outline-template 设定与事实词典"),("src-story-skills","skills/chapter-writing/SKILL.md Knowledge filtering")],
  fm_desc="当拿不准某信息角色/读者此刻能否知道、出现剧透或未卜先知、或到了计划揭示章要兑现时调用。产出本章知识边界表与词典更新。关键判据：困惑不等于留白，新名词首现必须给类别与可感知特征。不适用于伏笔排期（走 foreshadow-ledger）。Triggers: 剧透/读者已知/作者真相/他这时候知道吗/POV leak",
  tags=["continuity","pov","knowledge"]),
 dict(slug="foreshadow-ledger", title="伏笔账本与承诺兑现", importance="high",
  rationale="sumeru 的伏笔台账、story-skills 的 promises/payoffs 三态机、chinese-novelist 的到期必兑在语义上收敛为同一机制；覆盖「坑没填」这一高频读者投诉。",
  one_liner="每个 setup 只许有一条记录，按 planned→planted→paid-off 推进；到期必兑，弃用要标弃用。",
  intents=["前面埋的伏笔还有哪些没回收", "读者说坑没填", "新卷怎么接上一卷未回收项"],
  keywords=["伏笔","承诺","回收","未结项","open loops","payoff"],
  also_read=["outline-architecture","information-boundary","state-ledger"],
  sources=[("src-sumeru","skills/sumeru-deconstruct/SKILL.md 伏笔台账"),("src-story-skills","skills/plot-structure/SKILL.md Setup and Payoff Records"),("src-chinese-novelist","outline-template 登记规则·到期必兑")],
  fm_desc="当要列未回收伏笔、规划新卷承接、读者反馈只埋不收、或安排一次回收时调用。产出唯一台账与未结项清单，含角色 10 章/情节线 12 章/伏笔 20 章的遗忘阈值提醒。禁止复制同一 setup 到多处、禁止从自由文本推断伏笔。Triggers: 伏笔/坑/回收/未结项/open loops/payoff",
  tags=["continuity","foreshadowing"]),
 dict(slug="chapter-craft", title="逐章写作：黄金法则、四问与悬念钩子", importance="critical",
  rationale="chinese-novelist 的三大黄金法则/钩子十三式/三段式与 Chinese-WebNovel-Skill 的每章四件事构成最完整的可执行行文方法；是「写正文」关键任务的唯一去向。",
  one_liner="写前答四问，钩子从前 20% 播种、末 10% 收获，短中长三条悬念弧并行，停在变化那一拍。",
  intents=["写第 X 章正文", "开头或结尾写不出抓手感", "这章是不是水了"],
  keywords=["写章节","章末钩子","章首引子","黄金三章","chapter","hook"],
  also_read=["continuation","deslop","failure-patterns"],
  sources=[("src-chinese-novelist","SKILL.md 三大黄金法则"),("src-webnovel-skill","SKILL.md 每章必须回答四件事"),("src-chinese-novelist","hook-techniques 三段式设计法/跨章悬念弧")],
  fm_desc="当细纲已定、要写某一章正文，或章节平淡、开头结尾缺抓手感时调用。产出正文、章节摘要与四问表。禁止虚假悬念、机械降神、注水、章末追加第二个结尾。不适用于写前上下文恢复（走 continuation）与写后去 AI 味（走 deslop）。Triggers: 写第X章/章末/钩子/开头抓人/chapter/hook",
  tags=["writing","hooks","pacing"]),
 dict(slug="short-form-emotion", title="短篇与爽文：情绪驱动单支点", importance="medium",
  rationale="oh-story 明确把短篇线与长篇线分开，并给出「所有内容为情绪服务」的独立执行规则；若不单列，短篇任务会被误路由到长篇大纲与逐章流程。",
  one_liner="短篇只有一个支点：要交付的那一种情绪；按情绪节点推进，场景完成职责就收，不加戏凑长度。",
  intents=["写一个短篇或爽文单篇", "反转和付费点怎么安排", "读完没感觉，情绪不够"],
  keywords=["短篇","爽文","情绪曲线","反转","付费点","short story","twist"],
  also_read=["trend-scan","deslop"],
  sources=[("src-oh-story","skills/story-short-write/SKILL.md 导语·执行规则/小节完整性流程"),("src-oh-story","README 拆文报告·短篇情绪节点")],
  fm_desc="当要写短篇/盐选短故事/爽文单篇、排情绪曲线与付费点、或诊断短篇情绪不足时调用。产出故事核、情绪节点表（−9~+9）、成稿。不套长篇卷纲、黄金三章与多弧并行；不为凑字数加戏。Triggers: 短篇/爽文/情绪/反转/付费点/short story/twist",
  tags=["writing","short-form","emotion"]),
 dict(slug="continuation", title="断点续写与分层上下文组装", importance="high",
  rationale="chinese-novelist 的中断续写、sumeru 的分层上下文、oh-story 的写前必读、wordflowlab 的 9 项重读清单四源交叉印证；解决「换会话就忘」这一工程问题。",
  one_liner="新会话先扫断点，按当前时刻整份重读该读的文件，只投喂本章相关的六类切片，绝不整本加载。",
  intents=["接着上次继续写", "写到后面老忘设定", "上下文快满，需要精简投喂"],
  keywords=["断点续写","接着写","上下文切片","写前必读","resume","context slice"],
  also_read=["state-ledger","parallel-writing","chapter-craft"],
  sources=[("src-sumeru","skills/sumeru-write/SKILL.md 子agent输入上下文"),("src-chinese-novelist","phase0-initialization 中断续写检测"),("src-oh-story","skills/story-long-write/SKILL.md 写前必读（强制）")],
  fm_desc="当新会话要接着写、中段开始忘设定、上下文需要精简、或给子 Agent 组装章节材料时调用。产出上下文切片清单与更新后的状态文件。硬约束：rg 检索或摘读不算写前重读、投影层不作事实源。不适用于旧稿导入（走 import-legacy）。Triggers: 接着写/断点续写/恢复上下文/resume/context",
  tags=["continuity","context","engineering"]),
 dict(slug="deslop", title="去 AI 味：确定性预检 + 三层诊断", importance="high",
  rationale="oh-story 的分层 lint、human-writing 的翻案腔规则、Chinese-WebNovel-Skill 的正反对照、Novel-Control-Station 的「不要盲洗」四源互补，构成「确定性 + 语义」双层而非二选一。",
  one_liner="确定性规则只负责定位硬伤，三层扫描负责读感；零命中不等于没问题，不许靠加戏制造真人感。",
  intents=["这段太像 AI 写的，帮我改", "编辑说 AI 味重 / 要过检测", "全稿收尾前统一清语感"],
  keywords=["去AI味","机器腔","翻案腔","humanize","de-AI","语感"],
  also_read=["chapter-craft","failure-patterns","review-gate"],
  sources=[("src-oh-story","skills/story-deslop/SKILL.md Phase 1/执行边界"),("src-human-writing","dist/human-writing-lite.md 规则二 翻案腔"),("src-control-station","SKILL.md Hard Rules 不要盲洗")],
  fm_desc="当正文读起来像 AI、编辑反馈 AI 味重、或全稿收尾要统一语感时调用。先确定性预检（行号+命中片段+blocking/advisory），再表达/用笔/故事三层诊断，改后复扫。禁止用微动作粗话制造真人感、禁止盲洗掉时代质地与人物声音。Triggers: 去AI味/机器腔/太假/humanize/de-AI",
  tags=["revision","style","lint"]),
 dict(slug="review-gate", title="审查、字数校验与阶段门禁", importance="high",
  rationale="oh-story 的审查铁律、chinese-novelist 的脚本字数校验与最多 3 轮、sumeru 的阶段门禁、wordflowlab 的一致性警报格式四源合并；覆盖「交付前质量」关键任务。",
  one_liner="审查是找问题不是背书；字数必须脚本判定；阶段交接必须过可执行校验，失败只重跑失败阶段。",
  intents=["帮我审稿、查这章有没有硬伤", "字数够不够 / 全稿校验", "能不能进入下一阶段"],
  keywords=["审稿","校验","字数","门禁","一致性","review","QA","gate"],
  also_read=["state-ledger","failure-patterns","foreshadow-ledger"],
  sources=[("src-oh-story","skills/story-review/SKILL.md 导语·执行铁律"),("src-chinese-novelist","phase4-validation 自动修复/shared-infrastructure 字数脚本"),("src-sumeru","CLAUDE.md 阶段门禁规则")],
  fm_desc="当一章或全稿写完要查完成度、一致性、字数，或阶段交接前要确认门禁时调用。产出 Findings 报告、校验日志与门禁结论。硬约束：不伪造结论、字数不用模型估算、最多 3 轮修复、只读检查器不自动修复。不适用于语感改写（走 deslop）。Triggers: 审稿/校验/字数/门禁/review/QA",
  tags=["qa","validation","gate"]),
 dict(slug="parallel-writing", title="写作模式与无人值守连写", importance="medium",
  rationale="chinese-novelist 的三种写作模式、Novel-Control-Station 的 marathon mode、oh-story 的裸调用防失控三条共同定义「何时可以不打断用户」，缺任一条都会导致误连写。",
  one_liner="模式与章节范围必须显式确认；无人值守不打断用户，但每章内部控制步骤一个都不能少。",
  intents=["一口气写完别再问我", "用多 Agent 并行批量写", "选哪种写作模式"],
  keywords=["并行写作","疯狂创作","日更","marathon","parallel","batch"],
  also_read=["continuation","state-ledger","review-gate"],
  sources=[("src-chinese-novelist","SKILL.md 第2.5步 写作模式选择"),("src-control-station","SKILL.md Marathon Mode"),("src-oh-story","skills/story-long-write/SKILL.md 裸调用与停靠点（防失控）")],
  fm_desc="当大纲获批后要批量写章节、选串行/并行/Teams 模式、或开启无人值守连写时调用。产出章节正文、每章提交记录与完稿报告。硬约束：裸调用只诊断不开写、不默认日更 3 章、单轮正文 ≤3 章、共享文件改前重读。Triggers: 一口气写完/并行写/疯狂创作/marathon/parallel",
  tags=["orchestration","workflow"]),
 dict(slug="import-legacy", title="逆向导入：把旧稿变成可续写工程", importance="medium",
  rationale="oh-story 的 story-import 是 9 源中唯一处理「已有旧稿」的管道，且其「导入源与对标硬隔离」为独门约束；覆盖审计中「已有前 20 章」这一独立任务。",
  one_liner="先拆文再迁移成项目结构，长篇才初始化底账；导入源绝不能登记成对标书。",
  intents=["导入前面写的 20 章接着写", "把旧稿反向解析成设定", "从别的工具迁移项目"],
  keywords=["逆向导入","旧稿","残稿","迁移","import","manuscript"],
  also_read=["deconstruct","continuation","state-ledger"],
  sources=[("src-oh-story","skills/story-import/SKILL.md 导语/名词与目录边界/Phase 4")],
  fm_desc="当已有若干章旧稿要接着写、要把半成品迁成标准项目结构、或旧项目缺追踪文件时调用。产出项目结构与导入报告。硬约束：导入源与对标硬隔离、不重做定位问答、不虚构未写章节、短篇不建追踪。Triggers: 导入/旧稿/接着前面写的/迁移项目/import",
  tags=["migration","engineering"]),
 dict(slug="failure-patterns", title="失败模式诊断：为什么读者不追", importance="high",
  rationale="把 4 源分散的「禁忌/反例/底线问题」收敛为一个症状驱动的入口；仓颉 A2 要求「不适用于什么」可识别，单列此卡可避免诊断类请求被误路由到改写类能力。",
  one_liner="把「不好看」拆成追读故障/阅读噪音/注水拼接/长篇崩坏四类，给主因与唯一修复去向。",
  intents=["为什么没人追 / 数据掉了", "开头劝退、看不懂设定", "帮我诊断一下别直接改"],
  keywords=["诊断","弃书","劝退","注水","机械降神","diagnose","drop-off"],
  also_read=["chapter-craft","deslop","review-gate"],
  sources=[("src-chinese-novelist","hook-techniques 悬念设置禁忌/chapter-guide 新名词首现/content-expansion 两条铁律"),("src-sumeru","skills/sumeru-review/SKILL.md 六类底线问题")],
  fm_desc="当读者/编辑反馈「不追了」「看不懂」「太水」但没指出具体位置，或要一份问题清单而非直接改稿时调用。产出问题清单（位置/类别/依据/修复去向）、主因结论与可检验验收判据。主因最多一个、次因最多两个；不编平台数据。Triggers: 诊断/为什么没人追/弃书/劝退/diagnose",
  tags=["diagnosis","qa","routing"]),
]

caps = []
for c in CAPS:
    caps.append({
        "capability_id": "cap.novel-forge." + c["slug"],
        "revision": 1,
        "status": "active",
        "aliases": [], "supersedes": [], "merged_into": None, "split_into": [],
        "slug": c["slug"],
        "title": c["title"],
        "importance": c["importance"],
        "importance_rationale": c["rationale"],
        "one_liner": c["one_liner"],
        "intents": c["intents"],
        "keywords": c["keywords"],
        "also_read": c["also_read"],
        "card": "cards/%s.md" % c["slug"],
        "frontmatter": {"description": c["fm_desc"], "tags": c["tags"]},
        "source_evidence": [{"source_id": s, "location": loc} for s, loc in c["sources"]],
        "promotion": {
            "destination": "router",
            "gate": {"independent_intent": False, "independent_contract": True,
                     "independent_run": False, "independent_reuse": True,
                     "independent_eval": True},
            "notes": "用户明确要求蒸馏成 1 个 skill；按 single-first 原则全部留在来源路由入口内，不晋级独立 Skill。五条判据中独立意图/独立运行不成立：写小说各能力高度依赖同一项目文件链，用户几乎不会脱离创作流程单独请求单一能力。",
        },
    })

bundle = {
    "schema_version": 1,
    "bundle_id": "bundle.novel-forge",
    "book": {
        "title": "中文小说创作能力合集：GitHub 写小说 Skill 榜单九源蒸馏",
        "author": "zenstory-ai / PenglongHuang / lingfengQAQ / xindoo / Tomsawyerhu / danjdewhurst / wordflowlab / jingtai123 / KKKKhazix（开源项目方法论）",
        "source_pack": "novel-forge-distill",
        "baseline_tag": "baseline-novel-forge-20261107",
    },
    "entry": {
        "name": "novel-forge",
        "description": (
            "中文小说/网文创作全流程能力入口。当用户要开新书、选题扫榜、拆解对标、排大纲与爽点、"
            "写章节、写短篇、断点续写、维护设定与伏笔、去 AI 味、审稿校验、并行连写、导入旧稿或诊断弃书原因时调用。"
            "按意图路由表加载 1 张能力卡，跨域任务最多 2 张。"
            "不适用于：非创作类事实问答、抄袭或复刻受版权保护作品的专有设定与表达、法律医疗金融建议、"
            "敏感有害内容。Triggers: 写小说/网文/开书/大纲/写章节/伏笔/去AI味/审稿/续写/novel/webnovel/writing"
        ),
        "core_principles": [
            "先有写前真源（定位、故事承诺、设定与事实词典），再动笔；没有词典不许现场编数字。",
            "发生过的事实只记在一个底账里：写前真源 / 写后真源 / 投影层分开，投影文件禁止手改。",
            "作者真相与读者已知分离；正文只能用读者已知，角色只能用自己已知。",
            "一章 = 一次局面变化 + 一个翻页理由；钩子从前 20% 播种、末 10% 收获，短中长三条悬念弧并行。",
            "去 AI 味是「确定性规则定位硬伤 + 三层语义诊断」两层，既不机械替换也不靠加戏制造真人感。",
            "审查是找问题不是背书；字数与阶段交接必须由可执行校验判定，不靠模型估算。",
            "含糊指令不等于授权连写；模式与章节范围显式确认，无人值守也不许跳过内部控制步骤。",
        ],
        "out_of_scope": [
            "非创作类事实问答、实时资讯、百科查询",
            "抄袭或复刻他人作品的专有设定、角色组合、关键事件链与原句；拆文只迁移抽象机制",
            "法律、医疗、金融等专业建议",
            "封面生图、短剧分镜、视频生成等改编与制作环节（本包聚焦文字创作）",
        ],
        "stop_conditions": [
            "意图在路由表与能力索引中均无法命中 → 明确告知超出范围，不硬套写作框架。",
            "没有正文/文本却要求拆文或导入 → 停下来要材料，不凭记忆蒸馏。",
            "发现总纲与设定冲突 → 标 BLOCKER 停下等用户裁决，不擅自取舍、不自动顺稿。",
            "用户只要求概览/术语解释 → 用核心原则与 overview/glossary 回答后即停，不加载能力卡。",
            "涉及权利不明的版权文本或有害内容 → 停止改写，说明边界。",
        ],
    },
    "router_entry": {
        "name": "novel-forge",
        "description": (
            "中文小说与网文创作的来源路由入口。处理所有未被独立晋级的能力：开书定位、扫榜选题、拆文、"
            "大纲节奏、状态底账、信息边界、伏笔账本、逐章写作、短篇情绪、断点续写、去 AI 味、审查门禁、"
            "并行连写、逆向导入、失败模式诊断。Triggers: 写小说/网文/大纲/伏笔/去AI味/审稿/novel/writing"
        ),
    },
    "promotion_budget": 8,
    "capabilities": caps,
}

with open(BUNDLE / "verified.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(bundle, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=200)

with open(BUNDLE / "destinations.json", "w", encoding="utf-8") as f:
    json.dump({"bundle_id": "bundle.novel-forge",
               "destinations": {c["capability_id"]: {"served_by": "novel-forge"} for c in caps}},
              f, ensure_ascii=False, indent=2)

(BOOK / "overview.md").write_text("""# 资料集概览 — 九源写小说 Skill

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
""", encoding="utf-8")

(BOOK / "glossary.md").write_text("""# 术语词典

| 术语 | 含义 | 主要来源 |
|---|---|---|
| 写前真源 / 写后真源 / 投影层 | 大纲设定与最近被接受的章节提交是真源；state、索引、摘要、向量库是自动生成的只读视图 | webnovel-writer |
| 唯一底账 / `CHAPTER_COMMIT` | 一章写完后新事实的唯一入账口，驱动所有投影重生成 | oh-story、webnovel-writer |
| 作者真相 / 读者已知 | 完整设定与文本已披露信息分开记录，防剧透与角色未卜先知 | oh-story、chinese-novelist、story-skills |
| 信息边界 | 角色言行只能使用该角色已知的信息 | chinese-novelist、story-skills |
| 设定与事实词典 | 名词/事实、首现章节、读者已知、完整真相、计划揭示 四至五栏 | chinese-novelist |
| 故事承诺 / promises / payoffs | 开书时向读者承诺的爽点、情绪点、反转点、长线期待，及其兑现 | Chinese-WebNovel-Skill、story-skills |
| 三态台账 | `planned → planted → paid-off`，每个 setup 只许有一条记录 | story-skills、sumeru |
| 遗忘阈值 | 角色 10 章 / 情节线 12 章 / 伏笔 20 章未动即提醒 | wordflowlab |
| BLOCKER | 总纲与设定冲突时阻断更新、等用户裁决的标记 | webnovel-writer |
| 阶段门禁 | 阶段交接必须通过可执行校验，失败只重跑失败阶段 | sumeru |
| 三层递进式问答 | 核心定位 → 深度定制 → 标题生成 | chinese-novelist |
| 三大黄金法则 | 展示而非讲述 / 冲突驱动剧情 / 悬念承上启下 | chinese-novelist |
| 每章四问 | 主角想做什么、谁阻止、局面变成什么、为什么还往下看 | Chinese-WebNovel-Skill |
| 悬念钩子十三式 / 章首引子七式 | 章末 13 类钩子与章首 50–150 字 7 类引子模板 | chinese-novelist |
| 三段式（播种-生长-收获） | 前 20% 埋种子、中段偶尔冒头、末 10% 兑现成钩子 | chinese-novelist |
| 跨章悬念弧 | 短弧 2–3 章 / 中弧 5–8 章 / 长弧全书，三线并行 | chinese-novelist |
| 黄金三章 | 前三章必须建立追读理由，不是固定模板 | Chinese-WebNovel-Skill、oh-story |
| 黄金爽点密度 | 小 3–5 章 / 中 10–15 章 / 大 30–50 章，经验参数非硬配额 | sumeru |
| 金手指三字段 | 来源、限制、成长空间 | sumeru |
| 分层上下文 / 检索切片 | 每 Agent 只拿本章相关的 1–3 章细纲、精简人物卡、本章术语、上章结尾 | sumeru、Novel-Control-Station |
| 写前必读 / 9 项重读清单 | 写前整份重读规定文件；检索或摘读不算 | oh-story、wordflowlab |
| blocking / advisory | 确定性句式硬命中（须清零或白名单）与语义层提示（回语境判断） | oh-story |
| 三层扫描 | 表达层 / 用笔层 / 故事层 | oh-story |
| 翻案腔 | 先立读者并没有的误解再推翻抬价，如「不是A，而是B」 | human-writing |
| 去 AI 味 / deslop / 写作 lint | 逐条匹配已知句式模板给出行号与改写方向 | oh-story |
| 防注水判据 | 「删掉这段，故事是否变差？」 | chinese-novelist |
| 六类底线问题 | 时间线矛盾 / 设定崩坏 / 人物 OOC / 重复情节 / 信息泄露 / 伏笔死结 | sumeru |
| Findings Schema | 严重度 S1–S4 + evidence + fix 的统一审查结论格式 | oh-story |
| 逆向导入 | 把旧稿反向解析成可续写的项目结构 | oh-story |
| 疯狂创作模式 / marathon | 不再逐章确认，但每章内部控制步骤一个不少 | Novel-Control-Station |
| 裸调用防失控 | 含糊指令只诊断并列选项，不得自动连写 | oh-story |
| 单一入口 / 能力卡 | 1 个路由 SKILL.md + 按需加载 1–2 张卡，避免触发竞争 | 仓颉 skill v2.5 |
""", encoding="utf-8")

print("Bundle generated:", len(caps), "capabilities")
print("cards present:", len(list(CARDS.glob('*.md'))))
for c in caps:
    assert (CARDS / (c["slug"] + ".md")).exists(), "missing card " + c["slug"]
print("all cards verified")
