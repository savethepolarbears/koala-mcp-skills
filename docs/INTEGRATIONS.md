# Compose with existing engineering and agent systems

This repository does not vendor or require ZzzOps, Superpowers, Riqor, Matt Pocock’s curated skills, Plugin Eval or Plugin Creator. Their installed workflows informed the design, but no third-party skill text, private configuration or invented native state format is copied here.

## ZzzOps: durable goal ownership

Keep one canonical product/content outcome in the user’s existing ZzzOps workspace. Create it only through the installed version’s supported workflow. Attach a bounded Koala phase as a subordinate task: explicit brand, goal, read/write authority, budget group, maximum iterations, evidence outputs and completion condition. Link receipts and unresolved blockers back to that goal. Do not treat this repository’s `workflow.json` as ZzzOps’s canonical goal schema.

Example handoff, in ordinary prose:

> Assess five existing-page opportunities for the selected brand. Read-only, ten-credit ceiling, no Writer words. Complete when each page has measured evidence, a refresh/new/hold decision and a reviewable brief. Stop on missing GSC access or exhausted budget. Return receipt references, not just a narrative.

## Superpowers: plan, test, verify

Use the installed planning workflow for changes to this repository. For a live Koala job, keep the process proportionate: define the outcome, inspect evidence, plan the bounded actions, obtain effect approval, execute, then verify. Tests pin mechanical rules; editorial pressure cases test how an agent reacts to uncertainty. A passing unit suite is not proof that a model will follow every instruction.

## Riqor: delegated specialists and evidence gates

A controller can delegate a single Koala outcome skill to a research or content specialist. Supply a scope packet and require evidence plus terminal status. Keep one controller responsible for the shared spending envelope and write approval. Read the installed Riqor version’s actual specialist/configuration schema before integrating; this pack defines no fake native-agent names or runtime configurations.

## Matt-style codebase design

Prefer deep modules over a wrapper for every tool. Cost/argument rules live in the catalogue/policy; state transitions live in the ledger. Test those public interfaces. Do not duplicate OAuth or build generic adapters for hypothetical transports. When a rule is mechanical and valuable, put it in code and a regression test rather than repeating more prose.

## Plugin Eval: independent analysis and host-agent benchmarking

When its CLI is actually installed, from this repository root:

```bash
plugin-eval start . --request "Evaluate this plugin." --format markdown
plugin-eval analyze . --format markdown
plugin-eval init-benchmark .
plugin-eval benchmark . --dry-run
```

Read its “Fix First” section, then adapt the generated benchmark setup using the installed version’s schema. The included `benchmarks/scenarios.jsonl` is a transparent generic corpus, **not** a claim to be Plugin Eval’s native config format. Keep raw outputs and actual host/model/usage details. Baseline and skill-enabled trials must use comparable mocks/tasks; report policy failures separately from style.

These Plugin Eval commands were not run while building this release because that executable was not installed. The repo’s own deterministic evaluation is not a substitute or a fabricated Plugin Eval score.

## Plugin Creator: local package before publication

The portable and compatibility manifests are already included. A local test does not need a fabricated cloud app ID. The user may later ask Plugin Creator to register or publish a plugin using the actual current tool contract and their chosen ownership metadata. Public GitHub distribution is separate from a public OpenAI-directory submission; review trademark, support, privacy and submission requirements before that later action.

## MCP server prompts

The live `koala-ai` MCP server provides 6 pre-configured workflow prompts discovered via `prompts/list`:

| Prompt Name | Description | Key Arguments |
|---|---|---|
| `research_topic` | Comprehensive topic research combining SERP data, questions, and topics. | `topic` (required), `brand` (optional) |
| `analyze_competitors` | Analyze competitor content strategy, rankings, and opportunities. | `competitors` (required), `topic` (required), `brand` (optional) |
| `plan_content` | Create a comprehensive content brief and outline based on research and brand guidelines. | `topic` (required), `content_type` (optional), `target_word_count` (optional), `brand` (optional) |
| `keyword_research` | Discover keywords, search intent, and ranking opportunities around a seed topic. | `seed_keyword` (required), `brand` (optional) |
| `ai_search_visibility` | Audit brand presence and citation share across AI search engines. | `brand` (optional), `domain` (optional) |
| `audit_page` | Comprehensive single-page audit for content quality, SEO, and competitive gaps. | `url` (required), `brand` (optional) |

Hosts that expose MCP prompts (such as Claude Code, Cursor, and Antigravity) can load them after inspecting current prompt arguments. Prompt loading is a conversational starter, not an extra Koala research tool or permission to execute unapproved write actions. Apply the selected skill’s scope, budget, and approval rules to any prompted tool calls.
