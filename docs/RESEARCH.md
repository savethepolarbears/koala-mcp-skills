# Source research and design decisions

Reviewed **October 1, 2026**. This is a provenance record, not a claim that all third-party behavior was tested live.

## Requested source and live contract

The initial basis was a user-supplied public beta inventory describing 62 Koala tools, 23 with no platform-credit cost, two guided MCP prompts, OAuth connection and major workflows. The full marketing copy is not redistributed here. The available Koala connector’s 62 tool definitions were then inspected without invoking any account, research or generation action.

The local catalogue transcribes those definitions conservatively, with explicit notes for effects, inputs, limits and costs. It is **not** a byte-for-byte exported `tools/list` capture and does not assert full formal server-schema equivalence. In particular, `amazon_product_details` exposed a generic argument object; no hidden ASIN parameter was guessed.

## Source discrepancies worth preserving

The supplied inventory described access for all paid plans. The live [Koala MCP page](https://koala.sh/mcp) observed in research described Professional-and-above beta access with opt-in; other Koala pages were not wholly consistent. The skills therefore ask the current account/connection screen to establish eligibility instead of encoding a permanent tier rule.

The live connector descriptions add critical execution details that the marketing workflow summaries do not fully express: attached creation can auto-upload/publish; scheduling inherits live future settings; presets and per-task overrides have replacement semantics; queued work must be resumed by ID; the purported page analyzer is source-derived model analysis; several AIO tools do not expose market parameters. Those are explicitly represented in the skills.

Official Koala references: [MCP overview](https://koala.sh/mcp), [changelog](https://koala.sh/changelog), [API docs](https://koala.sh/pages/api-docs), [API access feature page](https://koala.sh/features/api-access). The API and MCP are not interchangeable contracts.

## Public GitHub precedents examined

| Repository | Useful pattern | What this pack adds |
|---|---|---|
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Discoverable job-oriented marketing skills | Koala-specific limits, integration behavior and budgeted receipts |
| [anthropics/skills](https://github.com/anthropics/skills) | Standard skill packaging and supporting resources | Self-contained Koala operational references and offline guards |
| [obra/superpowers](https://github.com/obra/superpowers) | Planning, testing and verification discipline | Concrete content-operation state and evidence gates |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | Cross-agent discovery and installation | Copy installer with ownership checks, plus a compatible standard layout |

Searches included `site:github.com "koala" "SKILL.md"`, `"koala.sh/api/mcp" "github"`, and `"koala-mcp-skills"`. No clearly established Koala-specific public skills pack surfaced in those searches. This is a limited search result, not proof that none exists, and no “first ever” claim is made.

## Format and client verification

The [Agent Skills specification](https://agentskills.io/specification) informed frontmatter and local resources. [OpenAI packaging docs](https://developers.openai.com/plugins/build/plugins) informed root portable manifests and Codex compatibility. [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference) informed the Claude layout. Current official [Antigravity skills docs](https://antigravity.google/docs/skills) specify `~/.gemini/config/skills/`, which differs from older examples. Additional official links are in [INSTALL.md](INSTALL.md).

The package was checked locally for its own contracts and paths. That is not full validation against every remote host’s JSON schema, nor proof of discovery/loading in those hosts. Live OAuth, host activation, model behavior and generation remain user-side canary tests.

## Originality and licensing

The skill prose, Python code, tests and fixtures in this pack are original contributions released under the included MIT license. Public project patterns and protocol/function names are referenced, not copied skill bodies. Koala AI and client/product names belong to their respective owners. No affiliation, endorsement or public-directory acceptance is implied.
