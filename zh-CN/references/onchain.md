# 链上地址 / 代币 / 合约 / DApp 审查

## 触发条件

任何代币、地址、合约、DApp 的安全判断，以及 swap、转账、授权或其他交易动作之前。

## 标准检查工具

运行：

```sh
../scripts/security-check --chain <4663|base|bsc|solana|eth> --address <addr> --mode light|full|trade --json
```

工具链使用 GoPlus、Binance token audit、Blockscout/RPC 合约读取、地址投毒对比和 `security-flags`。结果字段包括 `rating`、`data_status`、`tradable`、`flags`、`evidence_id`、`expires_at`。保留原始 JSON 关键字段作为证据；不要自行编造缺失字段或把未知解释为安全。

使用本机免费 GoPlus 地址安全检查：

```sh
$ONCHAIN_SECURITY_HOME/bin/goplus address-security <chainid> <addr>
```

检查 phishing、sanctioned、stealing、honeypot_related 等风险字段，并保留输出作为证据。MistTrack 不可用 → 记入 unknowns 并将风险上调一级。

## 审查要点

- 核实链与完整地址、官方合约地址、代币同名仿冒、标签、交易历史及已知风险标记。
- 合约：源码验证、代理与升级权限、owner/admin、增发/黑名单/暂停/税费权限、重入、`delegatecall`、可疑资金流及流动性控制。
- **签名 / 授权 / Permit 只读检查清单（仅检查，绝不签名、批准或提交）**：解析实际方法、参数、接收者、spender、金额、nonce、有效期和资产差异；识别 `eth_sign`、盲签、EIP-712、`permit`/`permit2`、无限 `approve`、`setApprovalForAll`、Safe 多调用及 `delegatecall`。无法解码或字段不明确时记为 unknowns 并停止流程。任何产品/流程采用“keys stored locally, agent signs”均为 ⛔ REJECT，适用于所有代理；唯一例外是所有者已确认的交易代理执行（若你的部署启用该角色），且仍须满足 [gate-rules.md](gate-rules.md) 的全部闸门。此例外不授权其他签名或审批。
- DApp：验证域名、HTTPS 证书和官方公告；检查前端/供应链/DNS 劫持、请求权限和交易预览。证书错误或官方报告前端被劫持时立即停止交互。
- 地址投毒：对照完整地址及上下文，不以首尾字符判断；确认收款地址来自可信记录。
- 参考 [darkforest-checklist.md](darkforest-checklist.md) 和 [gate-rules.md](gate-rules.md)。

## 评级与报告

使用主技能的 LOW / MEDIUM / HIGH / REJECT。Phishing、Scam、Sanctioned、Exploit 等确证标签至少 HIGH；确认恶意为 REJECT。高/拒绝必须交由人类决定。未验证源码、数据部分缺失或结果过期均须清楚标示。

报告包含链、完整目标地址、检查模式、评级、`data_status`、`tradable`、活跃 flags、`evidence_id`、`expires_at`、具体发现及数据缺口。交易动作还需满足 `gate-rules.md`；报告不能代替交易闸门。
