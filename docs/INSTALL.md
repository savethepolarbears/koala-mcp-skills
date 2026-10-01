# Installation and local testing

## Pick one installation path

Use copied global skills for the simplest first test, especially when Koala is already connected. Use a plugin package when you want the skills and remote MCP connection bundled together. Do not install the same pack globally and as a plugin in the same host: duplicate skill discovery or duplicate MCP connections can confuse routing and permissions.

### Global copied skills

From the extracted repository root:

```bash
python3 scripts/install.py --agent codex --profile starter
python3 scripts/install.py --agent codex --profile starter --apply
```

Repeat `--agent` to target more hosts. The three profiles are `starter` (8), `research` (19) and `all` (26). The research profile includes recovery and QA instructions, not additional write permissions.

```bash
python3 scripts/install.py --agent claude-code --skill koala-content-decay --skill koala-ai-visibility --apply
```

Selected installations also include `koala-core`. Each workflow nevertheless has its own references and can be read independently. The core helper works from its copied location, without the original repository.

| Host | Target Flag | Global destination, reviewed October 1, 2026 |
|---|---|---|
| Codex (Universal Root) | `--agent codex` | `~/.agents/skills/` |
| Claude Code | `--agent claude-code` | `~/.claude/skills/` |
| Gemini CLI | `--agent gemini-cli` | `~/.gemini/skills/` |
| Antigravity (Global Config) | `--agent antigravity` | `~/.gemini/config/skills/` |
| Antigravity (App Store) | `--agent antigravity-app` | `~/.gemini/antigravity/skills/` |
| Codex (Store) | `--agent codex-store` | `~/.codex/skills/` |
| Cursor | `--agent cursor` | `~/.cursor/skills/` |

To install across all agent hubs simultaneously in a single command:

```bash
python3 scripts/install.py --all-hubs --profile all --apply
```

Antigravity’s official docs use `~/.gemini/config/skills/` for global discovery and `~/.gemini/antigravity/skills/` for the app store. Check the documentation for the product/version you actually use. `--home /path/to/isolated-home` safely redirects the installer for testing. No shell startup files are changed. Do not run with sudo.

The installer refuses symlink paths, foreign skill directories, modified tracked files and added non-generated files. It previews by default, checks the whole selection first and uses per-directory staged swaps with rollback on exceptions. It is not a hardened defense against a malicious process concurrently rewriting your filesystem. Harmless Python bytecode/cache files are ignored when checking installed content.

### Update and uninstall

Rerun the same installer command from a new release. Clean owned copies are updated; local modifications stop the operation. Preserve customized skills under a different name/location before installing over them.

```bash
# Preview removing this pack’s clean owned copies; then add --apply.
python3 scripts/install.py --agent codex --profile all --uninstall
python3 scripts/install.py --agent codex --profile all --uninstall --apply
```

Uninstalling selected `--skill` entries does not automatically remove the core. Uninstall does not delete private ledgers, user records, OAuth grants or an existing MCP connection. A Vercel Skills CLI installation must be managed with that CLI, not this installer.

### Vercel Skills CLI alternative

```bash
npx skills add . --list
npx skills add . --global --agent codex claude-code --skill '*' --copy
```

The command is documented by the upstream CLI; it was not executed in the build environment. It can download a package. After publishing a public GitHub fork, replace `.` with the actual repository URL or `owner/repo`. No nonexistent public repository is advertised here.

## Claude Code plugin path

For a temporary local test, from the repo root:

```bash
claude --plugin-dir .
```

Use `/mcp` to inspect and authorize the bundled connection. Review permissions before running a skill. For a persistent local marketplace, use Claude’s `/plugin marketplace add` with this repository’s absolute path, then install `koala-mcp-skills@koala-mcp-skills` through `/plugin`. Current command syntax can be checked in your client help. The marketplace points to this repo root, not a nonexistent remote repository.

The Claude compatibility manifest is `.claude-plugin/plugin.json`; `.mcp.json` uses the client’s `http` transport label. No hooks or agents that auto-run on startup are included.

## Codex / portable plugin path

The root `plugin.json` and `mcp.json` use Agent Plugins schemas. The root MCP transport is `streamable-http`. `.codex-plugin/plugin.json` supplies a compatibility layout, and `.agents/plugins/marketplace.json` defines a local marketplace entry whose source path is relative to the marketplace root.

For hosts with local marketplace support, add this repository root through the host’s plugin-marketplace flow. The current documented CLI entry is:

```bash
codex plugin marketplace add .
```

Then select this plugin in the host’s available-plugin UI/flow. Availability differs by client surface; this package has not been submitted to the public OpenAI directory. No technical app ID or cloud registration is fabricated. Prefer global copied skills when your host does not expose local marketplace installation.

## Connect the actual MCP server

Do not reconnect if the selected host already exposes Koala. Otherwise:

### Codex CLI
```bash
codex mcp add koala-ai --url https://koala.sh/api/mcp
codex mcp login koala-ai
```

### Claude Code
```bash
claude mcp add --transport http koala-ai --scope user https://koala.sh/api/mcp
```
Run `/mcp` in an active session to authorize via OAuth.

### Google Antigravity & Gemini CLI
Add to `~/.gemini/antigravity/mcp_config.json` (or use the repository's `.agents/mcp_config.json`):
```json
{
  "mcpServers": {
    "koala-ai": {
      "serverUrl": "https://koala.sh/api/mcp"
    }
  }
}
```

### Cursor IDE
Add to `.cursor/mcp.json` (already pre-configured in this repository):
```json
{
  "mcpServers": {
    "koala-ai": {
      "url": "https://koala.sh/api/mcp"
    }
  }
}
```

Use the client’s browser OAuth flow, not pasted API keys or bearer tokens. Other clients must support the remote HTTP MCP and OAuth flow. Verify their current documentation before changing settings. The optional Python helper deliberately implements no OAuth or HTTP transport.

Start with `get_usage`, then only the brand and research capabilities required for your task. Brand DNA and a connected Google property are separate prerequisites for brand/Google workflows. Standalone article reading and creation do not require Brand DNA, although creation has its own action permission.

### Beta eligibility discrepancy

The supplied beta inventory says MCP is included in all paid plans. The live Koala MCP landing page observed during the review instead described Professional-and-above beta access with beta opt-in; other Koala pages were not fully consistent. Do not treat either wording as a permanent entitlement. Check the current Koala account/connection screen and current official help. The skills fail closed on missing capabilities and do not encode a universal plan-tier gate.

## Acceptance checklist

Run the offline suite; install into a temporary home; check skill discovery in a restarted real host; authorize a least-privilege connection; call `get_usage`; run one read-only skill with an explicit ceiling. Only after those pass, consider a separately approved standalone generation canary. See [LIVE-SMOKE-TEST.md](LIVE-SMOKE-TEST.md).

## Official references

[Agent Skills specification](https://agentskills.io/specification), [Claude skills](https://code.claude.com/docs/en/skills), [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference), [Claude MCP](https://code.claude.com/docs/en/mcp), [Codex skills](https://developers.openai.com/codex/skills), [Codex MCP](https://developers.openai.com/codex/mcp), [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins), [Gemini skills](https://geminicli.com/docs/cli/using-agent-skills/), [Antigravity skills](https://antigravity.google/docs/skills), [Vercel Skills CLI](https://github.com/vercel-labs/skills), [Koala MCP](https://koala.sh/mcp).
