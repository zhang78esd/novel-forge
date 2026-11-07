<!-- capability_id: cap.novel-forge.foreshadow-ledger | revision: 1 | status: active -->

# 伏笔账本与承诺兑现

## R — 原文 (Reading)

> 6. **伏笔台账**：埋设章 / 回收章 / 跨度 / 回收方式
>
> — `xindoo/sumeru/skills/sumeru-deconstruct/SKILL.md`·拆书报告结构

> Each setup has exactly one record. Pick it by use, update only that record, and never copy a setup into a second place.
>
> — `danjdewhurst/story-skills/skills/plot-structure/SKILL.md`·Setup and Payoff Records

> 到期必兑：登记了「计划揭示」的条目，写到该章必须兑现并在收尾时更新「读者已知」栏
>
> — `PenglongHuang/chinese-novelist-skill/references/guides/outline-template.md`·登记规则

## I — 方法论骨架 (Interpretation)

伏笔烂尾的根因是「记录多处、状态不明」。解法是给每个承诺/线索/疑问建立**唯一一条记录**，按用途归到不同目录（线索、承诺、疑问、弧内暗示），状态机只有三态：`planned → planted → paid-off`。每章只更新被触动的那一条，不许复制出第二份。

账本字段最少四个：埋设章、回收章、跨度、回收方式；再加「层数」（卷级/全书级）与「当前状态」。规划阶段显式写回（不要从自由文本里推断），写作阶段按章推进，收尾用清单核对「伏笔有推进，不是只埋不收」。故事承诺（爽点/情绪点/反转点/长线期待）也进同一台账，因为它同样是「向读者欠下的债」。

## A1 — 应用案例 (Past Application)

**原仓库案例**：`webnovel-plan/SKILL.md` 的 `foreshadow_writeback` 数组逐条显式列出「本卷规划明确新增的伏笔｜buried_chapter: 第10章｜payoff_chapter: 空｜level: 卷级」，并要求经总纲同步、清掉占位符后才允许写章。`story-skills` 的 `story next` 会统计未结承诺并打包进当章上下文。

**合成演练**：F012（铜钥来历，第 7 章埋，计划第 22 章收，卷级）→ 第 12 章出现一次「偶尔冒头」但不改状态 → 第 22 章兑现并标 paid-off → 收尾清单核对未结项仅剩 F015/F019，且都在推进中。

## A2 — 触发场景 (Future Trigger) ★

### 情境
1. 长篇写到中段，忘了前面埋过什么。
2. 规划新卷，要把上一卷未回收项接上。
3. 读者说「坑没填」「伏笔只埋不收」。
4. 想在某章安排一次回收，检查铺垫够不够。

### 语言信号
- "前面埋的伏笔还有哪些 / 帮我列未回收项"
- "这个坑怎么填 / 什么时候揭晓"
- "故事承诺有没有兑现"
- "open loops / setup payoff / plant and pay off"

### 与相邻能力的区分
- 与 `outline-architecture`：大纲负责排「何时埋、何时收」，本卡负责「逐章推进状态与不漏收」。
- 与 `information-boundary`：本卡管排期，信息边界管披露前能写什么。
- 与 `state-ledger`：伏笔台账是底账的一部分，禁止另建第二份记录。

## E — 可执行步骤 (Execution)

### 输入契约
必需：伏笔台账（或空账本）、当前章号、本章细纲。
台账与正文词表出现同一伏笔的两份描述时，先合并成唯一记录再继续。

### 步骤
1. **唯一归户**：按用途给每条线索/承诺/疑问分配唯一记录。完成标准：同名伏笔在台账中恰好一条。
2. **补齐四字段**：埋设章、回收章、跨度、回收方式。完成标准：无空字段；未定回收章写「待定」并列入未结项，不留空白。
3. **按章推进状态**：`planned → planted → paid-off`。完成标准：本章只改被触动的记录。
4. **到期必兑**：写到计划揭示章时执行回收并更新「读者已知」。完成标准：状态与正文同步。
5. **收尾核对**：没忘掉前文承诺、伏笔有推进、当前剧情仍服务故事引擎。完成标准：任一项不过则回改本章。
6. **遗忘阈值提醒**：角色 10 章、情节线 12 章、伏笔 20 章未动即主动提醒（阈值来自 `wordflowlab/novel-writer-skills` 遗忘元素检查）。

### 输出契约
更新后的台账 + 一张未结项清单（含逾期项）。判停：用户只问「某个伏笔是什么」时直接答，不启动全量核对。

## B — 边界 (Boundary) ★

- **不要**复制同一 setup 到多处；`story-skills` 把这条写成了硬规则。
- **不要**从自由文本里「推断」伏笔写回，只写规划中显式列出的条目。
- **不要**为兑现而机械降神：解决方案必须前文埋过（`hook-techniques.md` 禁忌）。
- 弃用伏笔要标「弃用」并说明，不要静默删除。
- 短篇通常只有 1–2 条核心伏笔，不必建完整三态台账。
