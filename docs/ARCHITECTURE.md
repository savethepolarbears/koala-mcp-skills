# Architecture

## Deep modules, narrow interfaces

The pack separates model judgment from mechanical constraints. A skill selects the job and interprets evidence; the host owns authenticated native calls; the optional helper validates the exact local plan and records state. No second MCP server or speculative transport abstraction is introduced.

`catalog.py` owns the reviewed tool/input/cost model. `policy.py` owns scope, action semantics, budget estimates and exact-plan approvals. `ledger.py` owns transactional shared reservations, operation identities and append-only evidence history. `analytics.py` owns comparable periods and honest simple arithmetic. `cli.py` exposes those interfaces without network access. All are inside `koala-core` so global copies stay usable.

The reviewed catalogue is a conservative transcription, not a downloaded authoritative `tools/list` response. Beta contracts can change; `koala-schema-watch` handles input-shape review and semantic follow-up. The `amazon_product_details` schema was opaque in the exposed connector, which remains an explicit limitation.

## Skill portability

Each `skills/koala-*/SKILL.md` has Agent Skills frontmatter, own references, a declarative workflow contract and a report schema. References do not depend on parent repository paths. The local helper is optional; a shell-less host can use the instructions but must not claim transactional guards were used.

There are no automatic hooks or startup scripts. Tool access stays in the user’s existing remote OAuth MCP connection. The Python installer copies only skill directories, not client configurations or plugin marketplaces. Plugin installation is a separate deliberate path.

## Loop control

Every run starts with an objective, scope, evidence cutoff, item/attempt ceiling and spending envelope. Every iteration must produce a decision-relevant observation or a verifiable result. No more than two stagnant iterations; uncertainty and denial terminate the affected branch. The portfolio skill defaults to sequential work, a ten-brand ceiling and a shared account budget group.

A fixed plan is one execution phase. Dynamic values such as newly returned article IDs create a new frozen read phase; they never mutate an already-claimed plan. Stable operation keys survive run changes. Verification reads can follow a recorded write, while unrelated dependent work waits for verification.

The workflow JSON files document these states for orchestration/handoffs. They are not an executable scheduler, and the README does not claim otherwise.

## Test boundaries

Unit tests exercise public module interfaces and the installer against temporary homes. Repository validation checks discovery metadata, packaging paths, references and full tool coverage. The deterministic evaluation runner tests safety fixtures. The 52 host-agent scenarios are a separate, initially unrun benchmark corpus; model instruction-following requires a real host/model trial.
