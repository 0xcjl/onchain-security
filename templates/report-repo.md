# Code Repository Security Review Report Template

Used to summarize repository review results from [repository.md](../references/repository.md).

---

## Repository information

- **Repository:** [owner/repo]
- **URL:** [repository URL]
- **Stars / Forks:** [count / count, or unknown]
- **Created / Last commit:** [date / date, or unknown]
- **Contributors:** [count, or unknown]
- **License:** [license or unknown]
- **Trust tier:** [1–5 / unknown] — [basis]
- **Review time:** [Asia/Bangkok ISO 8601]
- **Version/commit:** [tag or full commit]

## Review scope

- **Primary language:** [language]
- **Project purpose:** [actual purpose of the project]
- **Files checked:** [checked / total]
- **Focus paths:** [entry points, authentication, API handlers, install scripts, dependencies, etc.]
- **Scope limitations and unknowns:** [what was not checked and why; write none if none]

## Security findings

| ID | Severity | Title | Evidence (file:line) | Impact |
|---|---|---|---|---|
| [REPO-01] | [CRITICAL/HIGH/MEDIUM/LOW/INFO] | [title] | [location/link] | [impact] |

[When there are no findings, state "nothing found within the checked scope" and keep the scope limitations.]

## Architecture observations

- **Authentication:** [observation or unknown]
- **Authorization:** [observation or unknown]
- **Data flow:** [observation or unknown]
- **Secret handling:** [observation or unknown]
- **Dependencies:** [total, version pinning, known-vulnerability evidence or unknown]
- **Update mechanism:** [observation or unknown]
- **Build and release:** [release artifacts, checksums or supply-chain evidence]

## Rating and conclusion

- **Rating:** [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ REJECT]
- **Conclusion:** [recommendation and basis]
- **Unknowns:** [information not yet confirmed; write none if none]

## Notes

[Key context, comparison of alternatives and evidence limitations]
