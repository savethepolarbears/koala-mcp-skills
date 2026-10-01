# Release verification — 0.1.0

Recorded 2026-10-01T16:37:06+00:00.
Build environment: Linux, Python 3.13.5. Tests use synthetic fixtures and temporary homes only.

## Observed results

| Check | Observed result |
|---|---|
| Unit and repository tests | **93 passed**, zero failures |
| Deterministic policy fixtures | **18/18 matched expected allow/block outcomes** |
| Skill structure | **26** valid indexed skill directories |
| Tool coverage | **62/62**, each covered by a non-core workflow |
| Tool reference cards | **62** present |
| Global installation | **104 copies** across four simulated host destinations; preview made no writes |
| Repeat installation | All copies reported unchanged |
| Uninstall | Clean owned copies removed; tests also cover refusal to remove modified/foreign content |
| Standalone copied helper | Offline demo passed without the repository on its import path |
| ZIP extraction | Integrity/member hashes checked; extracted test suite and demo passed |
| Reproducible package test | Identical bytes for identical repository snapshots |
| Live MCP operations | **0** |
| Real Koala credits / Writer words spent | **0 / 0** |

The initial core, installer and regression tests were observed failing before their implementation or fix. Release review added tests for noncanonical numeric hosts, malformed ports, stable write identities across domain spellings, reconciliation identity checks, verification-read dependencies and SQLite connection cleanup. Those regressions pass in the recorded final suite.

## Reproduce locally

```bash
python3 scripts/check.py
python3 scripts/koala.py demo
python3 scripts/install.py --agent codex --profile all --home /tmp/koala-test-home
python3 scripts/package.py --output /tmp/koala-mcp-skills-release.zip
```

Use a fresh output path for packaging. To save reports, capture command output **outside the checkout**, then copy completed files into the evidence directory. Writing a JSON report into the directory while the validator is reading that same file can create a self-read failure. Reproducible-package checks likewise assume a stable source snapshot, not a live-growing log.

## Evidence files

[Unit-test output](unit-tests.txt), [structure result](structure.json), [policy cases and outcomes](policy-evaluation.json), [offline demo](offline-demo.json), and [pre-release archive smoke test](archive-smoke.json).

The archive smoke record refers to the tested release candidate before final evidence metadata was added. The final distributable is separately checksum-verified and tested after extraction during handoff. Its external SHA-256 identifies the exact delivered bytes; the ZIP includes a per-file `MANIFEST.sha256`.

## Explicitly not performed

**No actual Codex, Claude Code, Gemini CLI or Antigravity application was launched.** Their documented installation paths were exercised in isolated directories; directory creation is not host discovery. No live OAuth flow, Koala article generation, scheduling, editing, image generation, indexing submission or CMS effect was tested. No real brand data was retrieved.

The external `plugin-eval` executable was unavailable, so no Plugin Eval report or score is claimed. The **52 host-agent scenarios remain unrun**. The 18 policy cases are deterministic code checks, not 18 model trials. There is no measured model-token saving, SEO uplift, citation improvement or instruction-following score.

The structural validator checks local metadata, paths, links and conservative tool contracts; it is not full validation against every external plugin host’s remote JSON Schema. Python 3.10 compatibility is targeted and represented in CI configuration; this build’s observed runtime was Python 3.13.5, not every matrix entry.

Read [the live canary checklist](../LIVE-SMOKE-TEST.md) before enabling effects. Local approval records and receipts are caller assertions, not authenticated permission grants or remote attestations.
