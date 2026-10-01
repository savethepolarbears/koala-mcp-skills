# Real-host smoke test: opt-in and staged

The packaged evidence is offline. Record the actual host/client version, model, plugin/skills installation method, date, selected capabilities and results for your own trial. Do not put private results or credentials into this public repository.

## Stage 1: no live account required

Run `python3 scripts/check.py` and `python3 scripts/koala.py demo`. Preview installation into a temporary home with `--home`. Install one starter profile. Restart the actual host/session and verify it discovers `koala-core`, `koala-connect` and `koala-content-decay`. A copied folder existing on disk is not proof of host discovery.

## Stage 2: free authenticated reads only

Reuse the existing Koala connection or authorize it through OAuth with minimum read scopes. Inspect the live tool names/definitions. Ask for `get_usage` only. It should return actual account usage, not demo data. Then list brands only when needed and select the correct one explicitly.

Acceptance: the connection works, no write tool was called, no secret was requested or logged, and observed capabilities/eligibility are recorded. Missing tools after scope selection are not automatically a server regression.

## Stage 3: one bounded research job

Authorize a small platform-credit envelope and a single explicit domain/market. Run an opportunity or on-page skill with at most three findings and no Writer words. Check that the agent distinguishes measured versus estimated data, records caps/unknowns and does not create an article. Compare reported usage with actual Koala usage, acknowledging other account activity and billing timing.

Run one relevant pressure case from `benchmarks/scenarios.jsonl`, preferably with mocked results: an injected page instruction, a missing metric, a coverage false negative, an unavailable parameter or a request to publish disguised as planning. Do not expose a production site merely to test a failure mode.

## Stage 4: separately authorized generation canary

Only when the user requests it: verify standalone/no-integration creation without brandId/projectId, actual word settings, explicit budget and exact payload approval. Create one article, persist articleId, check that same job with bounded polling and retrieve its content. No duplicate on timeout. Observe the actual account/delivery state; do not infer no upload merely from the user’s prose.

Attached integration or scheduling tests are a further, separate risk decision—not part of this canary. Strict no-publication requirements may rule them out.

## Stage 5: document the result honestly

Record host discovery, OAuth, observed calls, usage, receipts, read-back and failures. Mark unexecuted stages “not run.” Keep baseline/skill-enabled model behavior trials separate from static validation and from a deterministic policy fixture. Never fill a missing run with an estimated quality score or fabricated token count.
