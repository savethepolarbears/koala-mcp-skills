# Public Koala MCP Skills — v0.1.0 design

## Product outcome
A publisher, agency, ecommerce operator or local service business can install portable skills globally, choose a recognizable marketing job, and complete a bounded, evidence-backed Koala workflow without confusing research with authorization to publish.

## Scope
26 goal-oriented Agent Skills; coverage of all 62 supplied beta tools; individual tool cards; conservative input contracts transcribed from connector discovery on 2026-10-01; portable and Claude/Codex compatibility manifests; an offline Python standard-library policy and receipt ledger; test fixtures; global installer with uninstall safeguards; contribution and release guidance.

## Non-goals
No new MCP server, OAuth implementation, cloud deployment, live article creation, automatic CMS changes, background worker, billing-meter guarantee, search-ranking guarantee or replacement for Koala's own permissions. No private account, portfolio, company or personal material in distributable files. No copied third-party skill bodies. No fabricated native ZzzOps/Riqor configurations.

## Architecture choice
A prompt-only pack is portable but cannot make arithmetic, local deduplication or state transitions reliable. A new autonomous MCP proxy could enforce calls but duplicates authentication and broadens the security boundary. Choose portable skills plus an optional deterministic LOCAL policy/receipt helper. Native clients own authenticated tool calls. The helper never calls Koala and cannot police calls made outside its ledger. Inputs and receipts are operator/agent assertions, not cryptographic attestations from Koala.

## Invariants
Read-only and zero-credit budgets by default; bounded action lists; separate platform-credit and writer-word reservations; exact-payload approvals for effects; stable operation keys for writes; no reissue after uncertain writes; account-wide budget groups for coordinated workers; explicit brand and market; untrusted retrieved content; unknown is not zero; integration-aware creation; scheduled tasks inherit live settings and may publish; explicit submission permission; execution receipt and independent read-back before verified write completion. Monetary arithmetic uses Decimal; SQL reservations are transactional. Public runtime data is ignored by Git.

## Verification
Unit tests for budgets, arguments, approvals, URL/brand boundaries, reservations, duplicate claims, receipt transitions, metrics and installation; static coverage/link/manifests checks; adversarial policy evaluations; archive extraction and quickstart smoke test. Live OAuth and host loading remain explicitly unverified in this environment. LLM behavior evaluation must be reported separately from deterministic tests.
