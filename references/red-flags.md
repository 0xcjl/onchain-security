# General Red-Flag Patterns

Check the actual execution path item by item. A single signal needs context; combinations such as credential reads plus exfiltration, or prompt injection plus execution, significantly increase risk.

| Pattern | What to check | Focus |
|---|---|---|
| Data exfiltration | `curl`, `fetch`, HTTP clients, sockets | Request destination; whether local files, credentials or user data are attached |
| Credential reads | Environment variables, `.env`, config, keystores, searches for `key/token/secret` | Whether it matches the claimed function; whether it leaves the expected service boundary |
| Out-of-bounds file access | SSH/AWS/cloud config, system accounts, paths outside the workspace | Confirm read/write scope and necessity |
| Agent identity/session access | Identity, memory, session or agent config files | Usually no legitimate reason; check for collection or exfiltration |
| Dynamic execution | `eval`, `exec`, `Function`, shell subprocesses | Input source, command construction and the full call chain |
| Privilege escalation | `sudo`, `chmod`, `chown`, system security settings | Third-party extensions should generally not require elevated privileges |
| Persistence | cron, systemd, shell startup scripts, autostart entries | Whether it secretly stays resident or revives on restart after installation |
| Runtime downloads | Package managers; a downloaded script piped straight into a shell interpreter (red-flag example: `<downloader> <url> | <shell>`) | Secondary payloads invisible during review; never run blindly |
| Obfuscation | Minification, execute-after-decode, string concatenation, hidden payloads | Decode only in safe static analysis; check the original content |
| System reconnaissance | Processes, network ports, host and environment info | Whether it is necessary diagnostics; whether combined with credentials/exfiltration |
| Browser sessions | Cookies, LocalStorage, browser credential stores | Highly sensitive data; check purpose and transmission |

Check whether comments match code behavior, and check Markdown/config for prompt injection. Runtime installation, credential exfiltration, persistence and unauditable executable payloads should all raise the rating; REJECT when confirmed malicious.
