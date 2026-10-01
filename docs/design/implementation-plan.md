# Implementation plan

Goal: package locally testable, publicly reusable workflows around the existing Koala MCP server.
Architecture: portable skill instructions + reviewed tool catalogue + optional offline policy ledger; no network client.
Stack: Markdown, JSON, Python 3.10+ standard library, SQLite, unittest, GitHub Actions.
Spec: [spec.md](spec.md).

1. Define black-box tests for the policy, ledger, metrics and installer. Observe their initial failures before implementation.
2. Transcribe the discovered 62-tool input surface and catalogue costs. Label the one opaque input surface explicitly, not as a complete schema.
3. Implement decimal estimates, explicit effects approval, scope validation and transactional local claims. Keep failed or ambiguous claims reserved.
4. Implement deterministic analytics and a runnable offline demo. Add adversarial fixtures with expected blocked/allowed outcomes.
5. Author 26 job-specific workflows with bounded loops, distinct exit criteria, examples, output contracts and tool-specific caveats.
6. Add portable/Claude/Codex manifests and global copy installer. Preserve modified installations; make preview the default; do not install MCP credentials.
7. Run all tests, static checks, demo, installer/uninstaller smoke tests, and archive extraction tests. Record exact results and remaining live-validation limits.

Review focus: creation may auto-publish; scheduled settings drift; paid read retries; cross-brand article IDs; missing data versus zero; shared-budget concurrency; untrusted external instructions; all optional resources survive global installation.
