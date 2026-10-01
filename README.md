# Koala MCP Skills

**Go from “what should we do?” to one verified content action—not another unbounded agent loop.**

26 portable skills covering all 62 reviewed Koala MCP tools. Built for publishers, agencies, ecommerce teams and local businesses. Includes an optional, dependency-free Python helper for exact budget arithmetic, plan approvals, local duplicate prevention and execution receipts.

**Community project. Not an official Koala AI product.** Version 0.1.0 targets the beta tool definitions reviewed on October 1, 2026. Live tool definitions and account permissions always take precedence.

[Choose a skill](docs/SKILLS.md) · [All 62 tools](docs/TOOLS.md) · [Install](docs/INSTALL.md) · [Safety](docs/SAFETY.md) · [Verification](docs/evidence/verification.md)

## Try it locally

No account, network access or dependencies are needed for the offline checks. Python **3.10+** is required only for the helper, installer and tests; the skills themselves are Markdown.

```bash
cd koala-mcp-skills
python3 scripts/check.py
python3 scripts/koala.py demo
```

The demo uses synthetic data, makes zero network calls and spends no Koala credits or Writer words. It demonstrates a reserved read loop, receipts, duplicate blocking, a period comparison and an exact-intent duplicate check. It is not a live Koala or model-behavior test.

## Install globally

Preview the default eight-skill starter profile:

```bash
python3 scripts/install.py --agent codex --agent claude-code
```

Install all 26 skills for Codex, Claude Code and Antigravity:

```bash
python3 scripts/install.py --agent codex --agent claude-code --agent antigravity --profile all --apply
```

Or install to all agent stores (Codex, Claude Code, Gemini CLI, Antigravity, and Cursor) at once:

```bash
python3 scripts/install.py --all-hubs --profile all --apply
```

The installer copies self-contained directories. It will not overwrite foreign or locally modified skills, change MCP settings, add hooks, fetch packages or collect credentials. Restart the host/session afterward. Use `--agent cursor` for Cursor or `--agent gemini-cli` for Gemini CLI. Pick `--profile research` or repeated `--skill` options for a smaller installation.

An alternative for users already using the Vercel Skills CLI:

```bash
npx skills add . --global --agent codex claude-code --skill '*' --copy
```

This alternative can download the third-party CLI. Use one installation method per destination; its ownership/uninstall records are separate from this repository’s installer. No GitHub owner or repository URL is hard-coded, so the same layout works after you publish your fork.

## Connect Koala separately

Reuse an existing authenticated connection. Otherwise add the remote server in the client’s supported OAuth flow:

```bash
# Codex CLI
codex mcp add koala-ai --url https://koala.sh/api/mcp
codex mcp login koala-ai

# Claude Code: run /mcp in a session to authorize after adding
claude mcp add --transport http koala-ai --scope user https://koala.sh/api/mcp

# Google Antigravity & Gemini CLI: configure via .agents/mcp_config.json
# Cursor IDE: configure via .cursor/mcp.json (pre-configured)
```

Verify current CLI help and account eligibility. Begin with read permissions and only the research categories needed for your first task. Installation is not authorization to generate, edit, schedule or publish. The [installation guide](docs/INSTALL.md) covers plugin packages, client paths and beta eligibility differences.

## Three useful first prompts

**Recover value from existing pages**

> Use koala-content-decay for the brand I select. Compare two complete 28-day GSC periods, inspect the five largest meaningful declines, and propose refresh briefs. Read-only, at most 10 platform credits, no Writer words. Separate measured losses from hypotheses about why they happened.

**Find topics without creating duplicates**

> Use koala-opportunity-research for example.com in the UK, English. Find five worthwhile topics, check existing coverage and scheduled work, and classify each as refresh, new candidate, investigate or skip. Maximum 8 platform credits. Do not generate or schedule anything.

**Recover a dropped writing connection**

> Use koala-queue-operations to recover my existing article job. Reuse its article ID, or identify it from recent articles. Do not create a replacement. Return its observed state and the next safe action.

`example.com` is an illustrative domain. Supply your own site and resolve the correct brand before live research.

## What is in the pack?

| Job family | Skills |
|---|---|
| Start safely | Core/router, connection, budgets, brand audit, beta-schema review |
| Choose the work | Opportunities, content plans, decay diagnosis, competitor analysis, seasonal demand, prospect audits |
| Produce and recover | Article production, page refresh, editorial QA, queue recovery, approved calendar operations |
| Improve discovery | On-page audits, internal links, Google AI Overview visibility, link prospecting, indexing |
| Expand formats | Affiliate product research, video-to-article, image briefs and approved generation |
| Close the loop | Measured performance review, bounded multi-brand operations |

Each skill has a narrow trigger, concrete inputs, decision branches, stop conditions, a report schema, a declarative workflow contract, relevant tool notes and a synthetic pressure example. Full references load only when needed. All tools map to at least one non-core workflow; this is not a list of 62 one-tool wrappers.

## What “deterministic” means here

The optional helper deterministically checks known input contracts, fractional credit estimates, Writer reservations, explicit brand scope, exact-plan approval hashes, bounded action lists and local state transitions. SQLite transactions coordinate reservations across workers that use the **same ledger**. It blocks a repeated stable write operation key and preserves uncertain outcomes for reconciliation.

The model’s reasoning, search data, text generation and keyword intent judgments are **not deterministic**. The helper does not call MCP, authenticate approval identities, enforce Koala billing, validate the truth of supplied receipts, or intercept calls made outside it. Host permissions remain the real access boundary. See [the local guard guide](docs/LOCAL-GUARD.md).

```text
scope → inspect → propose → approve effects → reserve → native MCP call
                                                ↓
                                  record → read back → decide
                                     ↘ uncertain: reconcile, never blindly retry
```

## The publishing trap this pack handles

A KoalaWriter creation request can automatically upload or publish when its brand or project has an integration. “Write a draft” in article instructions is not a publishing switch. Presets can replace defaults, and scheduled tasks inherit settings that are live when they run.

These skills check the effective settings, explain the effects and require explicit authorization. Unknown delivery behavior stops generation. The conservative local helper refuses attached creation in `draft` mode; it requires `connected-write` plus fresh, argument-bound integration evidence. For strict no-upload work, use verified standalone creation without a brand/project or keep the brief local.

## Repository map

```text
skills/                   26 self-contained Agent Skills
  koala-core/scripts/     Optional standard-library policy and receipt helper
  koala-core/references/  62-tool catalogue and individual reference cards
catalog/                  Machine-readable skill/tool index
examples/                 Synthetic plans and normalized evidence formats
benchmarks/               52 host-agent scenarios, explicitly not yet run
scripts/                  Installer, checks, deterministic evaluation, ZIP builder
docs/                    Contracts, safety, source research and verification
.claude-plugin/           Claude compatibility manifest and local marketplace
.codex-plugin/            Codex compatibility manifest
.agents/                  Local Codex marketplace and Antigravity/Gemini mcp_config.json
.cursor/                  Cursor IDE MCP configuration
plugin.json, mcp.json      Portable Agent Plugins package
```

## Testing and contributing

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_repo.py
python3 scripts/evaluate.py
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) before adding a tool or changing effects. The [verification report](docs/evidence/verification.md) separates observed local tests from unperformed live-client, OAuth and LLM tests. No “production-proven” or model-quality score is inferred from static validation.

Plugin loading and authenticated Koala execution still need a local canary in your actual host. A [read-only smoke-test checklist](docs/LIVE-SMOKE-TEST.md) is included. [Research and precedents](docs/RESEARCH.md) explain the public repositories and official formats examined.

MIT licensed. No private accounts, portfolio domains or credentials are bundled.
