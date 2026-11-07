# 术语词典

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
