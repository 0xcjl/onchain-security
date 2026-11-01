# 来源与改编说明

本目录基于以下两个 MIT 许可上游：

- [`slowmist-security-cc`](https://github.com/0xcjl/slowmist-security-cc)，commit `d9c0a31`，中文翻译/Claude Code 适配版。
- [`slowmist-agent-security`](https://github.com/slowmist/slowmist-agent-security)，commit `0718ece96b8acb121466874d111fe80d41971a57`，v0.1.2，作者 evilcos；这是英文原版。

两份许可文本均随本目录提供：`LICENSE` 包含 SlowMist/0xcjl 的 MIT 版权声明，`LICENSE-slowmist-agent-security` 保留英文原版的 MIT 声明。改编不代表上游对本目录新增规则、工具或集成作背书。

改编内容：将技能入口和审查参考文档整理为中文，替换原环境专属路径与个人记忆路径，设置追加式审查日志；增加链上检查脚本（scripts/security-check）、SkillSpector 扫描步骤、钱包自保清单和可配置的代理角色拦截门槛示例策略。另根据 Blockchain Dark Forest Selfguard Handbook 与 Dark Handbook 摘编链上自保检查表。

## 模板翻译与来源决策

`templates/report-onchain.md`、`report-product.md`、`report-repo.md`、`report-skill.md` 和 `report-url.md` 翻译并改编自 `slowmist-agent-security/templates/` 中同名模板。链上模板已按本技能检查脚本字段适配，使用 GoPlus 地址/代币安全字段及未知项；不包含付费 MistTrack 字段。所有模板均按只读审查用途改写。

`slowmist-agent-security` 于 2026-11-01 经本包作者按来源逐项审查后决定采用，尽管 SkillSpector 结果为 100/CRITICAL（58 条文档示例类发现，无可执行文件）。此处记录该来源决策及扫描结果，不将其表述为 SkillSpector 通过或上游背书。


## 公开发布说明

公开版本已移除个人姓名、机器人名称与本地绝对路径；`references/gate-rules.md` 改为可配置的示例策略。`scripts/` 中的检查脚本为本包原创（MIT，Copyright (c) 2026 Jialin）。
