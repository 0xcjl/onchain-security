# Software Supply-Chain Attacks

The core is reviewing the parts of the delivery path that a source review cannot see.

| Pattern | Check | Protection |
|---|---|---|
| Runtime secondary downloads | Whether scripts temporarily install undeclared dependencies | Review all runtime commands; dependencies should be declared and pinned in advance |
| Pipe-to-execute | A downloaded script piped straight into a shell interpreter (red-flag example: `<downloader> <url> | <shell>`) | Download to a local file first, read and review it; never execute blindly |
| One-off execution | `npx` and other execution methods that skip local review | Pin the version, get a local copy and review it |
| Automatic updates | Remote version checks that download and execute | Update manually, verify signature/hash, keep the user in control |
| Dependency hijacking | Typosquatting, namespace confusion, abandoned-package takeover, Star Jacking | Verify name, publisher, version and package source |
| Build-time injection | install/postinstall, setup, Makefile, CI scripts | Audit build hooks and build artifacts |
| Trusted source compromised | Changes to repository, CI, registry, maintainer accounts | Compare commits, signatures, lockfiles and known hashes; watch for anomalous versions |

Check the complete path from source to local installation; verification is required even when the source is official. Invisible or unauditable payloads must be explicitly listed as evidence gaps and raise the rating.
