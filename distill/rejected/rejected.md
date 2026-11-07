# 阶段 1.5 淘汰记录

被淘汰的候选不删除，留档供审计。判定理由详见 `verified.md`。

| 候选 | 来源 | 淘汰类型 | 原因 |
|---|---|---|---|
| 一键生成封面图 / story-cover | oh-story | rejected | 非文字创作；依赖外部图像模型，V2 无法在本包内核验 |
| 扫榜脚本实时采集榜单 | oh-story story-long-scan | 降级 | 依赖特定平台与脚本，产物不附带脚本；机制保留在 trend-scan，并要求无实时数据时声明局限 |
| 多 Agent 通讯 / Agent Teams 具体实现 | chinese-novelist / Novel-Control-Station | 降级 | 绑定特定宿主能力，抽象为 parallel-writing 的模式选择 |
| 仿写某本具体作品风格 | 多源 | rejected | 触及版权表达复刻，直接拒绝 |
| AI 生成声明合规 / 平台过稿规则 | 零散提及 | rejected | 平台政策随时间变化，V3 增益不可验证 |
| 字数统计脚本 / 时间线校验脚本本体 | chinese-novelist / sumeru / oh-story | 降级 | 只保留「必须由确定性脚本判定」规则，脚本本体不迁移 |
| RPG 式选择交互推进剧情 | mave99a/novel-skill（榜单但未入本次 9 源） | rejected | 仅 1 处提及且无完整机制，V1 不充分 |
| 小说改编成可玩游戏 / 短剧分镜 / 视频生成 | zenstory-ai 系列 | out_of_scope | 超出文字创作范围，写入 SKILL.md「不适用」段 |
| 爽点密度 3–5 / 10–15 / 30–50 章 | sumeru outline | needs_review（保留但降级） | 无实测基线；标为诊断参数，不作硬配额 |
| 遗忘阈值 10 / 12 / 20 章 | wordflowlab | needs_review（保留但降级） | 同上；标为「提醒阈值」并注明来源 |
| 「过朱雀 / 降 AI 率」效果承诺 | 多源 | needs_review | 无独立复现证据；改为「外部检测器仅作自测参考」 |
| 情绪强度 −9~+9 标度 | oh-story | needs_review | 标度定义依赖内部实现；只作相对诊断，不作跨作品比较 |
| 各仓库安装命令与宿主兼容清单 | 多源 | reference | 部署细节，非方法论，跨源冲突且易过时 |
| 平台榜单字段名 / 脚本参数 / JSON Schema 细节 | 多源 | reference | 工具绑定过强，改为机制描述 |
| 40+ 术语（黄金三章、金手指、OOC、写作 lint 等） | 多源 | reference | 概念支撑，并入 glossary.md，不编译为能力 |
| 场景结果四值 yes-but / no-and | story-skills | reference | 有价值但未形成独立可执行契约；并入 outline-architecture 的节奏诊断 |
| 幽默伪风格禁忌 | Novel-Control-Station | reference | 单一风格模块，归入 failure-patterns 的诊断维度，避免能力碎片化 |

## 处置原则

- `rejected` 项不进入 `verified.yaml`，不生成能力卡。
- `needs_review` 项可以作为**带标注的参数**出现在卡片里，但不得伪装成已验证的硬规则。
- `reference` 项必须映射到实际交付的 overview / glossary / 边界声明，不能只是「未通过」。
- 编译器只处理 `status: active` 的能力，上述三类均不出现在路由表中。
