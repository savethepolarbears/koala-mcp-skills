# Local guard: exact scope, reservations and receipts

This standard-library helper is an **offline collaborator**, not an autonomous agent or MCP proxy. It performs no network calls. Your authenticated host performs each approved native MCP action. Only calls that use the same ledger participate in the reservation and duplicate checks.

## Quick offline walkthrough

```bash
python3 scripts/koala.py check examples/read-only-plan.json
python3 scripts/koala.py claim examples/read-only-plan.json usage --db .koala/state.sqlite3
python3 scripts/koala.py record examples/read-only-plan.json usage examples/synthetic-usage-receipt.json --db .koala/state.sqlite3
python3 scripts/koala.py claim examples/read-only-plan.json inventory --db .koala/state.sqlite3
python3 scripts/koala.py record examples/read-only-plan.json inventory examples/synthetic-sitemap-receipt.json --db .koala/state.sqlite3
python3 scripts/koala.py status --db .koala/state.sqlite3
```

These receipt files are explicitly synthetic. Do not use them to claim a live action happened. For real operations, replace the illustrative target with an explicitly authorized domain, create a fresh run ID, execute each returned native call once and write a truthful receipt. Repeating a claimed action is blocked. Private runtime files belong under the ignored `.koala/` directory or elsewhere outside the checkout.

## Plan contract

`version`, `run_id`, `budget_group`, `scope`, `mode`, `limits` and `actions` define one immutable phase. `scope.domain` is explicit even for account reads because a run should have a known business target. `scope.brand_id` is a resolved ID or null for an explicitly standalone/public-research phase. Use a stable non-secret `account_ref` alias in multi-account work.

Limits are **local conservative reservations**: `platform_credits` as a finite decimal string, `writer_words` as a nonnegative integer, and `max_calls` as a positive integer. Omitted monetary/word limits default to zero. Check current account usage and obtain the user’s spending envelope before creating a paid plan. An agent must not authorize its own budget by writing larger numbers.

Each action uses real, currently exposed tool arguments. The helper validates a conservative transcription of the reviewed input contract. Unknown tools/fields are blocked. For `amazon_product_details`, the discovered connector exposed opaque inputs: `live_schema_reviewed: true` is an operator assertion that the current arguments were inspected. It does not give the helper knowledge of the missing schema.

`depends_on` can reference earlier action IDs only. Ordinary downstream work waits for observed reads or verified writes. A declared verification read can follow a successfully recorded write, allowing its read-back to complete without a dependency deadlock; article identity must match a known returned ID.

### Three modes

`read-only` allows reads only, including paid reads within the approved envelope. `draft` allows reads plus approved standalone creation, editing, standalone image generation and cancellation; it does not mean all those effects are automatically authorized. `connected-write` is required for attached generation, scheduling, schedule updates and indexing submissions. Every non-read still needs an exact-plan approval.

For creation or scheduled generation, reserve Writer words using the current effective settings and a conservative upper estimate. This helper does not know the actual generated length, model multipliers or eventual billing. Scheduled changes require a future-word reservation even if the calendar call itself costs no platform credits. That conservative rule may overreserve, deliberately.

### Effect approval

After a human reviews the exact plan:

```bash
python3 scripts/koala.py approve .koala/reviewed-plan.json --by local-operator --minutes 30 --out .koala/approval.json
python3 scripts/koala.py claim .koala/reviewed-plan.json create --approval .koala/approval.json --db .koala/state.sqlite3
```

The approval contains the exact plan hash, effect list and expiry. Editing any plan value invalidates it. **The actor name is self-declared, not authenticated. The file is not a digital signature or a Koala permission grant. Agents must not issue their own approvals.** Preserve host-side confirmation and capability restrictions.

For brand/project-attached creation, the action must also include a fresh `integration_review`: `checked_at`, `arguments_sha256`, known `effective_status` (`none`, `draft` or `publish`) and a traceable `evidence_ref`. Review freshness is 15 minutes, checked again at claim time. Scheduling/updates require `accept_live_settings: true` because future settings may change. Do not use this as an excuse to schedule when the user forbids any possibility of publication.

### Dynamic results: use immutable phases

You cannot know a new articleId before creation returns. Do not put a fake ID or a `${variable}` placeholder into a supposedly executable plan. Use a creation phase, save its real ID, then freeze a separate read/poll phase with that ID. Keep the same ledger and budget group/ceilings. Reference the creation receipt in the follow-up evidence. Do not mutate a claimed run’s plan.

## Execution state

```text
unclaimed → claimed → recorded → verified
                    ↘ failure
                    ↘ uncertain / partial → reconcile existing result → recorded
```

`claimed` only means reserved locally. `recorded` means a caller-supplied observation was saved. `verified` means caller-supplied read-back evidence matched declared checks. None of these states proves the external system cryptographically.

Write actions need a stable `operation_key`, a `verification.tool`, and nonempty `verification.checks`. Reuse the same operation key for the same logical intent across run IDs. Explicitly approved new work needs a genuinely new key; changing a key to bypass an uncertain operation is forbidden. Exact-key blocking does not detect semantically similar topics or duplicate jobs created outside this ledger.

For every real verification/status read, create and claim a budgeted read action too. `verify` checks an evidence record; it does not perform or reserve that read itself. For images, `public_asset_readback` is a local evidence label for an actual permitted host/browser inspection, not an extra Koala tool.

Receipts use:

```json
{
  "tool": "get_usage",
  "outcome": "success",
  "data": {"note": "replace with an actual observed, scrubbed result"}
}
```

Generation success must include `external_id` containing the real returned article ID. Outcomes are `success`, `failure`, `uncertain` or `partial`. Save the original evidence separately when useful; never commit tokens, private analytics or customer material.

Read-back verification supplies the declared read tool, the same known `external_id`, and normalized `observed` values matching every expected check. Normalize honestly: checking `content_present: true` must correspond to actually retrieved nonempty content, not a generated assertion.

## Shared budgets and recovery

SQLite uses immediate transactions for reservations. All workers for the same account/cycle must use the same database and `budget_group`, with identical ceilings. A balance read is not a reservation, and a second machine with a different database is not coordinated. Single-host sequential execution is the easiest safe default.

Reservations are never automatically released—even on failures, uncertain calls or skipped remote work. This avoids falsely assuming a timeout was free. It can reduce usable capacity. Starting a fresh accounting cycle requires user authority; it is not an automatic escape hatch. Use the remote usage report to reconcile the true balance separately.

An uncertain/partial write is not retryable. Find the already-created job/task using live read tools and call `reconcile` with the original tool, recovered identity, success evidence and a `reconciliation_evidence` reference. Reconciliation adds history; it does not make a retry executable or refund reservations.

Read retries require a separately identified, budgeted action and a bounded retry decision; the helper has no retry daemon. Respect server Retry-After. Queue polling defaults to four checks within ten minutes at the skill layer, not a guarantee of completion.

## Other commands

```bash
python3 scripts/koala.py catalog --tool schedule_articles
python3 scripts/koala.py periods --end 2026-09-28 --days 28
python3 scripts/koala.py compare examples/metrics.json
python3 scripts/koala.py coverage examples/coverage.json
python3 scripts/koala.py schema-diff .koala/live-tools.json
python3 scripts/koala.py hash .koala/arguments.json
```

`schema-diff` compares reviewed input shapes, not billing semantics or all descriptions. Missing tools may be permission-filtered. Added/changed inputs return exit code 2; nothing is automatically updated. Exit 0 does not mean every capability exists or semantics are unchanged.

The URL screening is syntactic, not a DNS/redirect-aware network security boundary. Prompt text is not a comprehensive secret-scanning solution. The helper is deliberately not an OAuth client, scheduler, publisher, remote proof system or LLM evaluator.
