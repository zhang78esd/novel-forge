# 阶段 1 候选池 — 框架 / 流程

四个提取器（含 1 个补漏提取器）从 9 源 144 个文件中提取。本文件为审计留档，只记候选与来源，不含最终判定（判定见 `verified.md`）。

| # | 候选框架 | 来源 | 最终去向 |
|---|---|---|---|
| F1 | 扫榜→拆文→大纲→写作→去AI味→封面 全链路五步，长/短双线 | oh-story README | trend-scan / deconstruct / chapter-craft |
| F2 | 主入口路由与裸调用停靠 | oh-story story | SKILL.md 路由入口与防失控条款 |
| F3 | 扫榜五阶段（多榜重复模式） | oh-story story-long-scan | trend-scan |
| F4 | 拆文六阶段管道与断点续跑 | oh-story story-long-analyze | deconstruct |
| F5 | 长篇写作场景路由与防失控 | oh-story story-long-write | parallel-writing |
| F6 | 短篇四阶段（情绪驱动） | oh-story story-short-write | short-form-emotion |
| F7 | 逆向导入五阶段 | oh-story story-import | import-legacy |
| F8 | 三层真源：写前合同 / 写后提交 / 投影视图 | webnovel-writer webnovel-query | state-ledger |
| F9 | 每章写后强制回写（9 步流水线） | webnovel-writer README | state-ledger |
| F10 | 跨卷一致性检查（伏笔/关系/境界） | webnovel-writer webnovel-plan | outline-architecture |
| F11 | 三层递进式问答 | chinese-novelist SKILL | project-bootstrap |
| F12 | 四阶段 + 三种写作模式 | chinese-novelist SKILL | parallel-writing |
| F13 | 自动校验最多 3 轮 | chinese-novelist phase4 | review-gate |
| F14 | 中断续写检测 | chinese-novelist phase0 | continuation |
| F15 | 逐章 A-D 单一事实源 + 阶段 D 回写 | chinese-novelist chapter-checklist | state-ledger |
| F16 | 专项按需精修（11 层只输出当前 1 层） | Chinese-WebNovel-Skill SKILL | SKILL.md 加载规则 |
| F17 | 八模块流水线（选题→大纲→写作→审查→润色→完稿） | sumeru worldbuilder | outline-architecture / review-gate |
| F18 | 阶段门禁（可执行校验） | sumeru CLAUDE | review-gate |
| F19 | 状态回证（结构化时间线） | sumeru timeline-schema | state-ledger |
| F20 | 伏笔台账（埋设/回收/跨度/方式） | sumeru deconstruct | foreshadow-ledger |
| F21 | 分层上下文组装（每 Agent 只拿 6 类切片） | sumeru write | continuation |
| F22 | 承诺—回收单一记录归属表 | story-skills plot-structure | foreshadow-ledger |
| F23 | 每章强制状态回写 | Novel-Control-Station SKILL | state-ledger |
| F24 | 疯狂创作模式（不逐章问，但控制步骤全保留） | Novel-Control-Station SKILL | parallel-writing |
| F25 | 风格模块按需加载（最多 2 主 1 辅） | Novel-Control-Station style-modules | chapter-craft（B 段提及）/ overview |
| F26 | 项目文件格式：真值层 + 生成式注册表 | story-skills story-init | state-ledger |
| F27 | 写作前 9 项强制重读清单 | wordflowlab pre-write-checklist | continuation |
| F28 | 一致性警报输入→输出格式 | wordflowlab consistency-checker | review-gate |
| F29 | 去 AI 味三层诊断 + 确定性预检 | oh-story story-deslop | deslop |
| F30 | 审查铁律 + full/lean/solo 三模式 | oh-story story-review | review-gate |
| F31 | 三段式播种—生长—收获 | chinese-novelist hook-techniques | chapter-craft |
| F32 | 跨章悬念弧（短/中/长） | chinese-novelist hook-techniques | chapter-craft |
