# Repository working rules

This is a public, account-neutral skills pack for Koala MCP, not a private marketing workspace. Do not call live Koala actions merely to test a code change. No credentials, actual brand IDs, private analytics or customer content belong in this repo.

Read the relevant skill and `docs/SAFETY.md` before changing behavior. Canonical local catalogue: `skills/koala-core/references/tools.json`; it is a conservative dated transcription, not the authoritative remote schema. Preserve unknown/opaque fields instead of guessing.

Run `python3 scripts/check.py` after changes. Add regression tests for changed policy, state, cost or installation behavior. Separate deterministic test results from live host, OAuth and LLM evaluation. Do not claim an unrun check passed.

Keep Python standard-library-only and compatible with 3.10+. Each skill must remain self-contained under selected/global installation. No network hooks or automatic writes. Do not mutate active plans, silently relax budgets or retry uncertain effects.

Native ZzzOps/Riqor state belongs to an actual installed workflow using its current schema; this repo’s workflow JSON is not a substitute. Release archives exclude runtime data and caches.
