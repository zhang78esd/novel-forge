<!-- capability_id: cap.novel-forge.state-ledger | revision: 1 | status: active -->

# 唯一底账：状态文件与每章强制回写

## R — 原文 (Reading)

> 所有追踪写入都走 `scripts/tracking_commit.py`：`追踪/_tracking-state.json` 是唯一底账，`上下文.md`、角色快照、`伏笔.md`、时间线都由它自动生成，禁止手改。
>
> — `zenstory-ai/oh-story-claudecode/skills/story-long-write/SKILL.md`·Phase 4 追踪

> 7. 调用 `data-agent` 提取事实 / 8. 生成 `CHAPTER_COMMIT`，驱动 state、index、summary、memory、vector 投影 / 9. 执行章节级备份
>
> — `lingfengQAQ/webnovel-writer/README.md`·写章工作流

> After every accepted chapter: - update `08-dynamic-state.md` … - update changed canonical files in `03/04/05/06/07/02` as needed
>
> — `jingtai123/Novel-Control-Station-Skill/SKILL.md`·Dynamic Update Rules（引用中的模板链接已省略）

## I — 方法论骨架 (Interpretation)

长篇会崩，不是模型文笔变差，而是「发生过的事实」没有权威记录。解法是把事实权威从对话记忆外移到文件链，且严格分层：

- **写前真源**：大纲、设定、禁区、最近一次被接受的章节提交。
- **写后真源**：已定稿章节与其 `CHAPTER_COMMIT`，不可篡改。
- **投影层**：state/index/summary/向量库/Dashboard，全部由真源自动生成，只供查询，**禁止手改、禁止当事实源**。

每章被接受后必须走一次「提交」：提取本章新事实 → 写唯一底账 → 自动重生成所有投影 → 章节级备份。任何手改投影文件的行为都应被检查器拒绝。这样换会话、换 Agent、写到第 200 章，都能从文件恢复准确状态。

## A1 — 应用案例 (Past Application)

**原仓库案例**：`oh-story-claudecode/README.md` 的续写状态卡展示一条完整记账链：细纲 → 章节检查（三个脚本零命中）→ 写第 21 章 → `chapter commit`（state_revision 0→1）→ 追踪整份重生成；新伏笔 F057/F058 取本卷下一个编号追加，退役风险写进「本章退役登记」。

**合成演练**：第 7 章主角左臂受伤、获得一枚铜钥 → 提交后底账自动更新「人物状态：左臂不可用（第7章起）」「道具：铜钥（未揭示来历）」；第 8 章写作若出现「他双手撑地」即被一致性检查拦下。

## A2 — 触发场景 (Future Trigger) ★

### 情境
1. 写到几十章后人物能力、关系、时间线开始对不上。
2. 换了会话/换了 Agent，需要恢复「现在到底发生到哪了」。
3. 一章刚写完，要把新事实登记入账。
4. 并行写作时多个 Agent 要共享同一份状态。

### 语言信号
- "接着上一章写 / 现在剧情到哪了"
- "前面设定是不是矛盾了 / 帮我查状态"
- "把这一章的事实记下来"
- "state file / canon / continuity / chapter commit"

### 与相邻能力的区分
- 与 `information-boundary`：底账管「客观发生过什么」，信息边界管「谁允许知道什么」。
- 与 `foreshadow-ledger`：伏笔账本是底账的一个投影；不要另建第二份伏笔记录。
- 与 `continuation`：本卡定义账本结构，续写卡定义「如何读账本恢复上下文」。

## E — 可执行步骤 (Execution)

### 输入契约
必需：项目目录（设定/大纲/正文/追踪分层）、待提交章节正文、上一版底账。
若项目尚无底账，先初始化，不得边写边补。

### 步骤
1. **定真源层级**：明确写前真源、写后真源、投影层各是哪些文件。完成标准：`state.json` 一类派生文件被标为只读 fallback。
2. **写前只读核对**：按「最窄工具」查本章相关状态，不整本加载。完成标准：只带本章用得上的状态与待回收项。
3. **写完提取事实**：列出本章新事件、人物状态变化、新道具/名词、数字事实。完成标准：每条可定位到章节。
4. **唯一入账口提交**：所有写入经同一提交入口（脚本或单一命令），自动重生成上下文卡、伏笔、时间线、摘要、索引。完成标准：检查器确认无手改投影文件。
5. **备份与断点标记**：章节级备份 + 记录 state_revision。完成标准：中断后可从已接受提交恢复，不重写已完成章节。

### 输出契约
更新后的唯一底账 + 自动生成的投影文件 + 一条提交记录。判停：发现设定冲突时标 BLOCKER 停下，等用户裁决，不自动「顺一下」。

## B — 边界 (Boundary) ★

- **禁止**手改自动生成的投影文件；也禁止把 `state.json`/索引当事实源。
- **禁止**主流程口头总结代替结构化提交；`webnovel-review` 明确「不伪造结论」。
- 日志只作审计，绝不作真相源（`Novel-Control-Station-Skill` 硬规则）。
- 断网/无脚本环境可以退化为「单一手写底账文件 + 每章回写」，但仍要保证只有一个写入口，不能多份并存。
- 短篇单文件项目不必建完整追踪体系，过度工程化反而拖慢。
