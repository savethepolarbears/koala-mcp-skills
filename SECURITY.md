# Security

Treat this as a local skills package with optional offline helpers, not a security boundary. Read [docs/SAFETY.md](docs/SAFETY.md) and [docs/LOCAL-GUARD.md](docs/LOCAL-GUARD.md) before enabling effects.

No network transport, credential collection, automatic hooks or background scheduler is included. The installer writes only selected skill directories after `--apply`. The helper stores private plans/receipts locally; filesystem permissions and ignored directories are not encryption.

OAuth and permissions belong to the host and Koala. Exact-plan approval records are self-declared, not authenticated signatures. Supplied receipts can be false. Calls outside the ledger bypass its checks. Local URL screening cannot replace the remote fetcher’s DNS/redirect security. Do not grant publication-capable tools to an untrusted or unattended agent solely because a skill asks it to behave safely.

Report a vulnerability through the repository’s private vulnerability-reporting facility when enabled. Do not post secrets, real account data or a working abuse demonstration against a third party in a public issue. There is no fabricated security contact address in this unpublished package.

Supported release: 0.1.x, with beta tool-contract review required before live use. New provider/client behavior may invalidate assumptions without changing this code.
