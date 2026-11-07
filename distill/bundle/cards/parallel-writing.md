<!-- capability_id: cap.novel-forge.parallel-writing | revision: 1 | status: active -->

# 写作模式与无人值守连写

## R — 原文 (Reading)

> - **逐章串行**（`serial`）：主 Agent 自己逐章写，全程无中断 - **子Agent并行**（`subagent-parallel`）：将章节分成批次，派生子 Agent 并行写作 - **Agent Teams**（`agent-teams`）：Claude Code 多 Agent 协作模式，Agent 间可通讯（需手动开启）
>
> — `PenglongHuang/chinese-novelist-skill/SKILL.md`·第2.5步 写作模式选择

> In marathon mode: - do not ask the user again chapter by chapter - do keep every internal control step active
>
> — `jingtai123/Novel-Control-Station-Skill/SKILL.md`·Marathon Mode

> `/story-long-write` 或 `$story-long-write` **裸调用**（无明确意图）时，只诊断项目并列选项，**不得自动进入正文写作，也不得把已有项目默认为日更 3 章**
>
> — `zenstory-ai/oh-story-claudecode/skills/story-long-write/SKILL.md`·裸调用与停靠点（防失控）

## I — 方法论骨架 (Interpretation)

长篇产量问题靠模式切换解决，但模式选择必须由用户显式确认，且「不打断」不等于「跳过控制步骤」。

三种模式：串行（稳）、子 Agent 并行（快，按批次分章）、Agent Teams（可通讯协作）。并行时每个 Agent 只拿自己那 1–3 章的上下文切片，相邻章尽量给同一 Agent 以保衔接；共享状态文件只用编辑式写入且改前重读，禁止整体重写覆盖。

无人值守的「疯狂创作模式」有两个前提：大纲与人物档案已获批、用户显式开启。开启后逐章不再确认，但每章仍要跑全套控制（写前必读、一致性检查、状态回写、去味、审查），按大纲自然完结停，不按字数停。最关键的防失控条款：裸调用/含糊指令只诊断并列选项，不得自动开写，不得把「日更 3 章」当默认值，正文单轮最多 3 章且需显式范围。

## A1 — 应用案例 (Past Application)

**原仓库案例**：`chinese-novelist-skill/phase3-writing.md` 规定并行写入协议「共享文件只用 Edit 且改前重读，禁止 Bash 整体重写」；`Novel-Control-Station-Skill` 在 Windows 下生成 UTF-8 BOM 的续写脚本，交接时给出启动命令与 Ctrl+C 停止方式。

**合成演练**：40 章长篇，用户选 `subagent-parallel` → 把 1–3、4–6、7–9 分给三个 Agent，各带本章细纲＋相关人物卡＋上章结尾 100 字 → 每章完成后各自提交 `CHAPTER_COMMIT`，由主 Agent 串行合并底账 → 第 10 章前做一次跨批次一致性门禁。

## A2 — 触发场景 (Future Trigger) ★

### 情境
1. 大纲已确认，要开始批量写章节。
2. 想提高产量，考虑多 Agent 并行。
3. 想让 Agent 一口气写到完本、中途别问。
4. 并行写完后出现风格/设定串味，要回查协议。

### 语言信号
- "一章一章写还是并行 / 选写作模式"
- "一口气写完 / 别再问我 / 疯狂创作模式"
- "多 Agent 一起写 / 分批次"
- "parallel writing / marathon mode / batch chapters"

### 与相邻能力的区分
- 与 `continuation`：本卡管任务分配与写回协议，续写卡管单 Agent 上下文切片。
- 与 `review-gate`：门禁由审查卡定义，本卡负责在每章循环中调用它。
- 与 `state-ledger`：底账是唯一写入口，并行时不得各 Agent 各存一份。
- 与 `chapter-craft`：具体行文仍由逐章写作卡负责。

## E — 可执行步骤 (Execution)

### 输入契约
必需：已获批的大纲与人物档案、显式选择的写作模式、显式章节范围。
「裸调用」或未给范围时，**只诊断并列选项**，不进入写作。

### 步骤
1. **确认模式与范围**：列出串行/并行/Teams 与章节范围让用户选。完成标准：模式与范围都显式，单轮正文 ≤3 章。
2. **切片与分派**：每 Agent 1–3 章，配六类精简上下文；相邻章归同一 Agent。完成标准：无 Agent 收到全书。
3. **写入协议**：共享文件只用编辑式写入且改前重读；底账提交串行化。完成标准：无整体重写、无并发覆盖。
4. **每章仍跑全套控制**：写前必读 → 一致性检查 → 状态回写 → 去味 → 审查。完成标准：无人值守模式下这些步骤一个不少。
5. **跨批次门禁**：每若干章做一次跨卷/跨批次一致性核对。完成标准：冲突标 BLOCKER 停下。
6. **按大纲完结**：自然完结即停，给出完稿报告。完成标准：不因字数目标追加章节。

### 输出契约
章节正文 + 每章提交记录 + 完稿报告。判停：用户只说「继续写」而未确认模式时，沿用上次模式但不扩大范围。

## B — 边界 (Boundary) ★

- **不得**把含糊指令当授权自动连写；裸调用只诊断（`oh-story` 防失控条款）。
- **不得**默认「日更 3 章」或把已有项目当成待续日更。
- **不得**为了不打断用户而跳过内部控制步骤——marathon mode 的硬条件。
- 大纲未获批不得开启无人值守。
- 并行 Agent 各自维护状态副本是最高频事故；唯一底账必须串行提交。
- 用户中断（Ctrl+C）后恢复必须走 `continuation` 的断点检测，不从头重跑。
