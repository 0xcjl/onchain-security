# Code Repository Review

## Workflow

1. **Metadata and source**: verify creation time, recent commits, contributors, Issues/PRs, license, fork origin and differences from upstream. Stars can be faked; high attention does not replace a code audit. Determine intensity with the main skill's Tier system.
2. **Review the code surface**: prioritize entry points/APIs, authentication and authorization, config, dependencies, CI workflows and install scripts. Check for `eval`/`exec` on user input, injection, permissive CORS, non-expiring tokens, hardcoded credentials, excessive permissions and unvalidated input.
3. **Check CI/CD**: tokens with excessive write permissions, `pull_request_target`, workflows triggered by external input, printing secrets, unknown third-party Actions, and fetching code from external repositories to execute are all risk points.
4. **Review architecture and dependencies**: authentication and least privilege, data flows and logs, key rotation, update method, dependency sources and exact versions. Check for typosquatting, abandoned-package takeover, install hooks and lockfiles.
5. **Review forks**: focus on changes relative to upstream, new files, new dependencies and recent upstream security incidents. When source is unreadable or key release artifacts cannot be verified, do not conclude there is no risk.

## Rating reference

- LOW: source and code are clear; no substantive risk found.
- MEDIUM: bounded risks or issues that need fixing.
- HIGH: funds, credentials, authentication, sensitive config or critical code cannot be sufficiently verified; hand to a human for decision.
- REJECT: confirmed vulnerability, malicious execution, credential leakage or unacceptable permission design.

## Report

Record repository/commit, Tier, license, recent maintenance, review scope, dependency/CI checks, findings and evidence, rating and recommendations. Conclusions should be bound to a specific commit; do not rely only on the README, star count or author claims.
