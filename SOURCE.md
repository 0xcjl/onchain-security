# Sources and Adaptation Notes

This directory is based on two MIT-licensed upstreams:

- [`slowmist-security-cc`](https://github.com/0xcjl/slowmist-security-cc), commit `d9c0a31`, a Chinese translation / Claude Code adaptation.
- [`slowmist-agent-security`](https://github.com/slowmist/slowmist-agent-security), commit `0718ece96b8acb121466874d111fe80d41971a57`, v0.1.2, by evilcos; this is the original English version.

Both license texts ship with this directory: `LICENSE` contains the SlowMist/0xcjl MIT copyright notice, and `LICENSE-slowmist-agent-security` preserves the MIT notice of the original English version. The adaptation does not imply upstream endorsement of the rules, tools or integrations added here.

Adaptations: the skill entry point and review reference documents were organized in Chinese (this repository root now carries an English translation; the Chinese version is preserved in `zh-CN/`), environment-specific and personal memory paths were replaced, and an append-only review log was set up; added an on-chain check script (scripts/security-check), a SkillSpector scanning step, a wallet self-protection checklist and a configurable example gating policy for agent roles. The on-chain self-protection checklist is also excerpted from the Blockchain Dark Forest Selfguard Handbook and Dark Handbook.

## Template translation and source decision

`templates/report-onchain.md`, `report-product.md`, `report-repo.md`, `report-skill.md` and `report-url.md` are translated and adapted from the templates of the same name in `slowmist-agent-security/templates/`. The on-chain template has been adapted to this skill's check-script fields, uses GoPlus address/token security fields and unknowns, and contains no paid MistTrack fields. All templates were rewritten for read-only review use.

`slowmist-agent-security` was adopted on 2026-11-01 after the package author reviewed it item by item, even though its SkillSpector result was 100/CRITICAL (58 documentation-example findings, no executable files). This source decision and scan result are recorded here; they are not presented as a SkillSpector pass or an upstream endorsement.


## Public release notes

The public version has removed personal names, bot names and local absolute paths; `references/gate-rules.md` was changed into a configurable example policy. The check scripts in `scripts/` are original to this package (MIT, Copyright (c) 2026 Jialin).
