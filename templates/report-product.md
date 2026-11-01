# Product / Service Security Review Report Template

Used to summarize review results from [product-service.md](../references/product-service.md).

---

## Subject

- **Name:** [product/service name]
- **Provider:** [company/organization or unknown]
- **Official URL:** [URL or unknown]
- **Type:** [API / SDK / SaaS / platform / Skill / other]
- **Trust tier:** [1–5 / unknown] — [basis]
- **Review time:** [Asia/Bangkok ISO 8601]
- **Evidence:** [evidence_id, link, version or local path]

## Architecture observations

- **Key management:** [custody model, storage location, rotation capability; list unknowns explicitly]
- **Write capabilities:** [write/fund operation capabilities the product actually has; record observations only]
- **Data flow:** [data kept locally or the services/third parties it is sent to]
- **Transport and storage protection:** [verifiable encryption measures; list unknowns explicitly]
- **Data retention:** [policy or actual observation]
- **Update mechanism:** [manual/notification/automatic update, etc.]
- **Release artifact integrity:** [whether signature/checksum information is verifiable; list unknowns explicitly]
- **External dependencies:** [services, domains, SDKs, dependencies]

## Permissions and impact scope

| Permission/capability | Purpose basis | Worst-case impact | Evidence or unknowns |
|---|---|---|---|
| [permission or capability] | [declared purpose] | [impact if abused or leaked] | [evidence/unknown] |

## Findings

- [No findings, or list severity, evidence and impact scope by unique ID]

## Rating and conclusion

- **Rating:** [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ REJECT]
- **Conclusion:** [brief evidence-based judgment and its applicable boundaries]
- **Unknowns:** [information not yet confirmed; write none if none]
- **Mitigation observations:** [mitigations that exist or are suggested for evaluation; review suggestions only]

## Notes

[Key context, comparison information and evidence limitations]
