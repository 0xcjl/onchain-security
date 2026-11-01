# 链上安全审查报告模板

用于汇总 [onchain.md](../references/onchain.md) 的只读审查结果。报告仅描述已取得的证据与未知项，不提供签名、批准或广播操作指引。

```yaml
evidence_id: "[证据记录 ID]"
as_of: "[YYYY-MM-DDTHH:mm:ss+07:00，Asia/Bangkok]"
expires_at: "[YYYY-MM-DDTHH:mm:ss+07:00，Asia/Bangkok]"
data_status: "[complete|partial|missing]"
rating: "[🟢 LOW|🟡 MEDIUM|🔴 HIGH|⛔ REJECT]"
tradable: "[true|false|unknown]"
flags:
  - "[风险标记及其来源；无则写 none]"
unknowns:
  - "[尚未确认的信息；无则写 none]"

subject:
  address_or_token: "[地址、代币或合约标识]"
  chain: "[链名称及 chain ID]"
  subject_type: "[EOA|合约|代币|其他|unknown]"
  observed_labels: "[来源标签或 unknown]"
  symbol_name: "[名称/符号或 unknown]"

source_checks:
  goplus:
    status: "[complete|partial|missing]"
    evidence: "[检查结果摘要或缺失原因]"
  binance_audit:
    status: "[complete|partial|missing]"
    evidence: "[检查结果摘要或缺失原因]"
  contract:
    status: "[complete|partial|missing]"
    evidence: "[只读代码/代理/权限观察，或缺失原因]"
  address_poisoning:
    status: "[complete|partial|missing]"
    evidence: "[相似地址/投毒检查观察，或缺失原因]"
  security_flags:
    status: "[complete|partial|missing]"
    evidence: "[标记检查结果或缺失原因]"

observations:
  goplus_fields: "[例如 phishing、sanctioned、stealing、honeypot_related；保留来源原值]"
  binance_audit_fields: "[审计风险字段与原始值；没有结果则标记 unknown]"
  contract_fields: "[是否验证、代理情况、可观察的管理权限/危险函数；没有结果则标记 unknown]"
  address_poisoning_fields: "[匹配地址、相似度/上下文及证据；没有结果则标记 unknown]"
  security_flags_fields: "[命中项和证据；没有结果则标记 unknown]"
  activity_context: "[可核实的链上活动与时间范围；不可得则标记 unknown]"
```

## 填写约定

- `as_of` 与 `expires_at` 使用带 `+07:00` 时区偏移的 ISO 8601 时间，即 Asia/Bangkok 时间；过期时间应来自检查数据或适用的本地规则，不能臆造。
- `data_status` 表示整份数据：所有适用来源均有完整结果时为 `complete`；有部分结果时为 `partial`；没有可用结果时为 `missing`。每个 `source_checks` 项分别使用同一组状态。
- `evidence_id` 应对应可回查的证据记录。缺失或无法回查时写入 `unknowns`，不要编造 ID。
- `tradable` 只记录工具或既定数据对可交易状态的明确输出；没有明确结果时填写 `unknown`。它不是交易建议。
- 保留来源原始字段与证据。未检查、工具失败或来源不可用均应列为 `unknowns`；未知不代表安全。
- `flags` 记录实际命中的风险标记，并注明来源；没有命中时明确写 `none`。评级按证据和参考流程给出，不以缺失数据作为安全结论。
- 合约、权限、授权模式等只作为静态或链上只读观察记录；不得把报告变成签名、批准或广播交易的步骤。
