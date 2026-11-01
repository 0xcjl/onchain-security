# Skill / MCP Security Review Report Template

Used to summarize review results from [skill-mcp.md](../references/skill-mcp.md).

---

## Subject information

- **Name:** [Skill/MCP name]
- **Version:** [version or unknown]
- **Source:** [ClawHub / GitHub / npm / URL / other]
- **Author:** [name/organization or unknown]
- **Trust tier:** [1–5 / unknown] — [basis]
- **Published / Updated:** [date / date, or unknown]
- **Review time:** [Asia/Bangkok ISO 8601]
- **Evidence:** [version, commit, evidence_id, link or path]

## File scan

- **Total:** [n]; **Executable files:** [n]; **Documentation/data files:** [n]
- **High-risk files:** [path and type; write none if none]
- **Scan scope limitations and unknowns:** [content]

## Risk signals

- [No findings, or record each signal with severity, file location, evidence and impact]

## Permission and capability observations

| Category | Declared/observed access scope | Purpose and evidence | Unknowns |
|---|---|---|---|
| Read | [files/directories or none] | [purpose] | [unknown] |
| Write | [files/directories or none] | [purpose] | [unknown] |
| Network | [domains/endpoints or none] | [purpose] | [unknown] |
| System commands | [commands or none] | [purpose] | [unknown] |
| Environment variables | [variable names or none] | [purpose] | [unknown] |

## Architecture observations

- **Credential handling:** [observation or unknown]
- **Human control points:** [describe only the controls and automatic behaviors present in the workflow]
- **Automatic updates:** [observation or unknown]
- **Data boundary:** [local / where it is sent; evidence]
- **Failure behavior:** [observation or unknown]

## Rating and conclusion

- **Rating:** [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ REJECT]
- **Conclusion:** [brief evidence-based judgment]
- **Unknowns:** [information not yet confirmed; write none if none]

## Notes

[Cite relevant categories from references/red-flags.md; explain false-positive interpretations, evidence limitations and suggested mitigations]
