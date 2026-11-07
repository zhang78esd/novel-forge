# 阶段 1 候选池 — 案例与反例

## 案例（A1 素材）

| # | 案例 | 来源 | 去向 |
|---|---|---|---|
| C1 | 续写状态卡：第 20 章状态 → 第 21 章正文 + 追踪 diff（F057/F058 编号追加） | oh-story README | state-ledger |
| C2 | 拆文报告「立人设强、给爽点零」，只迁移三项局部技法 | oh-story README | deconstruct / trend-scan |
| C3 | 去 AI 味 lint：8 处命中 / 7 blocking，改后零命中 | oh-story README | deslop |
| C4 | 结构化伏笔写回 JSON 样例（buried_chapter 第10章 / level 卷级） | webnovel-writer webnovel-plan | outline-architecture / foreshadow-ledger |
| C5 | 稀薄版 → 充实版场景扩充对照 | chinese-novelist content-expansion | review-gate / failure-patterns |
| C6 | 悬念钩子「突然揭示」示例与三段式播种—生长—收获演练 | chinese-novelist hook-techniques | chapter-craft |
| C7 | 跨章悬念弧 20 章编排示例 | chinese-novelist hook-techniques | chapter-craft |
| C8 | premise 正反例（「庞大世界」vs「献祭品送往河中」） | Chinese-WebNovel-Skill SKILL | project-bootstrap |
| C9 | 去 AI 味正反对照（五味杂陈 vs 杯子放回桌上） | Chinese-WebNovel-Skill SKILL | deslop / failure-patterns |
| C10 | 抽象化改写（角色→[主角][对手][导师]，情节→动作+结果+代价） | sumeru deconstruct | deconstruct |
| C11 | 一致性警报格式（问题/位置/参考行/当前文本/已建立特征） | wordflowlab consistency-checker | review-gate |
| C12 | 翻案腔坏/好两段对照（「真正让他下定决心的，不是…而是…」） | human-writing human-writing-lite | deslop |
| C13 | 情绪节点标注 N1「门口偷听到『私生子而已』·情绪{震惊}{−7}」 | oh-story README | short-form-emotion |

## 反例 / 失败模式（B 段素材）

| # | 反例 | 来源 | 去向 |
|---|---|---|---|
| N1 | 禁止用新微动作、粗话、证据或冲突制造「真人感」 | oh-story story-deslop | deslop |
| N2 | 拆文不得虚构、不得倒推成人物早有计划、只迁移抽象机制 | oh-story story-long-analyze | deconstruct |
| N3 | 不为达标注水、不机械替换、密度提示不是词频配额 | oh-story expression / story-short-write | deslop / short-form-emotion |
| N4 | 悬念五禁忌：虚假悬念 / 机械降神 / 过度留白 / 低风险钩子 / 同质悬念 | chinese-novelist hook-techniques | chapter-craft / failure-patterns |
| N5 | 常见无效开头：天气 / 日常流程 / 回顾上章 / 过度解释 | chinese-novelist chapter-guide | failure-patterns |
| N6 | 困惑 ≠ 留白（新名词首现管理） | chinese-novelist chapter-guide | information-boundary / failure-patterns |
| N7 | 防注水：无意义风景 / 凑字数回忆 / 重复已知信息 | chinese-novelist content-expansion | failure-patterns |
| N8 | 一章只能有一个结尾；禁止「（补）/（扩）/（新增）」内部标记 | chinese-novelist content-expansion | chapter-craft / failure-patterns |
| N9 | 常见无效开头 / 不要收在总结句、讲道理、情绪散尽、解释掉悬念 | Chinese-WebNovel-Skill SKILL | failure-patterns |
| N10 | 六类底线问题：时间线/设定/OOC/重复/信息泄露/伏笔死结 | sumeru review | review-gate / failure-patterns |
| N11 | 拆书禁忌：报告当大纲 / 换名角色关系图 / 改一字章节标题 | sumeru deconstruct | deconstruct |
| N12 | 不要做的事：空谈人物立体 / 只给世界观 / 默认慢热 / 模仿当照抄 | Chinese-WebNovel-Skill SKILL | project-bootstrap |
| N13 | 不要盲洗（blind flattening） | Novel-Control-Station SKILL | deslop |
| N14 | 幽默伪风格：段子投递 / 人人同一吐槽腔 / 笑点无后果 / 网络梗偷懒 | Novel-Control-Station humor core | failure-patterns（未单列，见 coverage-audit） |
| N15 | 禁止以「敏感」「不适」为由中断只读拆解流水线 | oh-story story-short-analyze | deconstruct B 段 |
| N16 | 裸调用不得自动连写、不得默认日更 3 章 | oh-story story-long-write | parallel-writing |
| N17 | 导入源不得登记为对标、不得复制进对标目录 | oh-story story-import | import-legacy |
