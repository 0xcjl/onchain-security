# Product / Service / API / SDK Review

## Workflow

1. **Verify the provider**: official identity, incident history, privacy policy, terms of service, open-source and audit status. Third parties claiming partnerships with well-known brands are high risk.
2. **Assess the architecture**, focusing on key and signing boundaries: does the user hold the private key; does the agent only build unsigned transactions; do sensitive operations require human confirmation; are credentials encrypted, least-privilege and rotatable; are there silent automatic updates; where does data go; does failure degrade safely.
3. **Check permissions one by one**: API key scope, network domains, data read, writes, persistence, system modification. Each permission should map to a clear purpose; reject unrelated permissions.
4. **Rate using the main skill's trust tiers**. Tier only affects review intensity and is not a safety endorsement.

## Signature / approval / Permit read-only checklist

This section is for review only; never sign, approve or submit transactions. Check where keys are stored, who can invoke the signer, whether signing requests are human-readable, and the chain, contract, recipient, spender, amount, nonce, expiry and actual asset changes; cover `eth_sign`, blind signing, EIP-712, `permit`/`permit2`, `approve`, `setApprovalForAll` and batch calls. When it cannot be fully parsed, record unknowns and stop the workflow.

Any product/workflow that is "keys stored locally, agent signs" is ⛔ REJECT, applicable to all agents. The only exception is owner-confirmed trading agent execution (if your deployment enables that role); each execution must still pass every gate in [gate-rules.md](gate-rules.md). This exception does not authorize other agents or workflows to sign, approve or submit.

## Rating

- LOW: verifiable identity, minimal permissions, transparent architecture.
- MEDIUM: clear scope, with acceptable limitations or risks.
- HIGH: third-party custody of private keys, no human confirmation, remote automatic updates, unclear data boundaries; requires a human decision.
- REJECT: confirmed malicious, serious over-permissioning, or a third party impersonating a well-known brand while requesting sensitive permissions.

## Report fields

Provider/product, official or third-party source, Tier, key management, confirmation mechanism, credential storage, update mechanism, data boundaries, permissions, findings, evidence, rating and recommendations.
