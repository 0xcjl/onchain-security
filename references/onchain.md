# On-chain Address / Token / Contract / DApp Review

## Triggers

Any safety judgment about a token, address, contract or DApp, and before a swap, transfer, approval or other transaction action.

## Standard check tool

Run:

```sh
scripts/security-check --chain <4663|base|bsc|solana|eth> --address <addr> --mode light|full|trade --json
```

The toolchain uses GoPlus, Binance token audit, Blockscout/RPC contract reads, address-poisoning comparison and `security-flags`. Result fields include `rating`, `data_status`, `tradable`, `flags`, `evidence_id`, `expires_at`. Keep the key fields of the raw JSON as evidence; do not invent missing fields or interpret unknowns as safe.

Use the local free GoPlus address security check:

```sh
$ONCHAIN_SECURITY_HOME/bin/goplus address-security <chainid> <addr>
```

Check risk fields such as phishing, sanctioned, stealing, honeypot_related, and keep the output as evidence. MistTrack unavailable → record in unknowns and raise the risk by one level.

## Review points

- Verify the chain and full address, the official contract address, same-name token impersonation, labels, transaction history and known risk flags.
- Contracts: source verification, proxy and upgrade authority, owner/admin, mint/blacklist/pause/tax permissions, reentrancy, `delegatecall`, suspicious fund flows and liquidity control.
- **Signature / approval / Permit read-only checklist (inspect only; never sign, approve or submit)**: parse the actual method, parameters, recipient, spender, amount, nonce, expiry and asset diff; identify `eth_sign`, blind signing, EIP-712, `permit`/`permit2`, unlimited `approve`, `setApprovalForAll`, Safe multi-calls and `delegatecall`. When it cannot be decoded or fields are unclear, record unknowns and stop the workflow. Any product/workflow using "keys stored locally, agent signs" is ⛔ REJECT, applicable to all agents; the only exception is owner-confirmed trading agent execution (if your deployment enables that role), which must still pass every gate in [gate-rules.md](gate-rules.md). This exception does not authorize any other signing or approval.
- DApps: verify the domain, HTTPS certificate and official announcements; check for frontend/supply-chain/DNS hijacking, requested permissions and transaction preview. Stop interacting immediately on a certificate error or when the project officially reports a hijacked frontend.
- Address poisoning: compare the full address and context, not the first and last characters; confirm the recipient address comes from a trusted record.
- See [darkforest-checklist.md](darkforest-checklist.md) and [gate-rules.md](gate-rules.md).

## Rating and report

Use the main skill's LOW / MEDIUM / HIGH / REJECT. Confirmed labels such as Phishing, Scam, Sanctioned, Exploit are at least HIGH; confirmed malicious is REJECT. HIGH/REJECT must be handed to a human for decision. Unverified source code, partially missing data or expired results must be clearly labeled.

The report includes chain, full target address, check mode, rating, `data_status`, `tradable`, active flags, `evidence_id`, `expires_at`, specific findings and data gaps. Transaction actions must also satisfy `gate-rules.md`; the report does not replace the transaction gate.
