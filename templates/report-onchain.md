# On-chain Security Review Report Template

Used to summarize read-only review results from [onchain.md](../references/onchain.md). The report describes only the evidence obtained and the unknowns; it provides no guidance for signing, approving or broadcasting.

```yaml
evidence_id: "[evidence record ID]"
as_of: "[YYYY-MM-DDTHH:mm:ss+07:00, Asia/Bangkok]"
expires_at: "[YYYY-MM-DDTHH:mm:ss+07:00, Asia/Bangkok]"
data_status: "[complete|partial|missing]"
rating: "[🟢 LOW|🟡 MEDIUM|🔴 HIGH|⛔ REJECT]"
tradable: "[true|false|unknown]"
flags:
  - "[risk flag and its source; write none if none]"
unknowns:
  - "[information not yet confirmed; write none if none]"

subject:
  address_or_token: "[address, token or contract identifier]"
  chain: "[chain name and chain ID]"
  subject_type: "[EOA|contract|token|other|unknown]"
  observed_labels: "[source labels or unknown]"
  symbol_name: "[name/symbol or unknown]"

source_checks:
  goplus:
    status: "[complete|partial|missing]"
    evidence: "[check result summary or reason missing]"
  binance_audit:
    status: "[complete|partial|missing]"
    evidence: "[check result summary or reason missing]"
  contract:
    status: "[complete|partial|missing]"
    evidence: "[read-only code/proxy/permission observations, or reason missing]"
  address_poisoning:
    status: "[complete|partial|missing]"
    evidence: "[look-alike address/poisoning check observations, or reason missing]"
  security_flags:
    status: "[complete|partial|missing]"
    evidence: "[flag check result or reason missing]"

observations:
  goplus_fields: "[e.g. phishing, sanctioned, stealing, honeypot_related; keep the source's raw values]"
  binance_audit_fields: "[audit risk fields and raw values; mark unknown if no result]"
  contract_fields: "[verified or not, proxy status, observable admin permissions/dangerous functions; mark unknown if no result]"
  address_poisoning_fields: "[matched addresses, similarity/context and evidence; mark unknown if no result]"
  security_flags_fields: "[hits and evidence; mark unknown if no result]"
  activity_context: "[verifiable on-chain activity and time range; mark unknown if unavailable]"
```

## Filling conventions

- `as_of` and `expires_at` use ISO 8601 times with a `+07:00` offset, i.e. Asia/Bangkok time; the expiry should come from the check data or the applicable local rule and must not be made up.
- `data_status` describes the data as a whole: `complete` when every applicable source has a complete result; `partial` when there are partial results; `missing` when no usable result exists. Each `source_checks` entry uses the same set of statuses.
- `evidence_id` should correspond to a retrievable evidence record. When missing or not retrievable, add it to `unknowns`; do not fabricate an ID.
- `tradable` records only an explicit tradability output from the tool or established data; fill `unknown` when there is no explicit result. It is not trading advice.
- Keep the sources' raw fields and evidence. Unchecked items, tool failures or unavailable sources must all be listed as `unknowns`; unknown does not mean safe.
- `flags` records risk flags actually hit, noting the source; when there are none, write `none` explicitly. The rating follows the evidence and reference workflow; missing data must not be used as a safety conclusion.
- Contracts, permissions, approval patterns and the like are recorded only as static or on-chain read-only observations; never turn the report into steps for signing, approving or broadcasting transactions.
