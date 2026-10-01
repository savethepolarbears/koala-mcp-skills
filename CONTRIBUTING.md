# Contributing

Keep this a useful, public, account-neutral pack. A contribution should help a recognizable job, not simply add another prompt wrapper.

## Before changing a contract

Inspect the current live tool definition and record its date/provenance. Distinguish an observed server change from an earlier transcription error or a permission-filtered tool list. Do not guess opaque fields. Update the tool catalogue, individual reference card, relevant skill notes and regression tests together. Existing active plans remain immutable.

## Skill checklist

Use a lowercase kebab-case `koala-` name matching the folder. Describe when the skill should trigger, not a long workflow summary in metadata. Include explicit inputs, bounded steps, branches, stop conditions, evidence requirements, exact output contract and a synthetic pressure case. Keep references local to the skill so selected global installs work. Every tool name must be in the reviewed catalogue.

Model judgments stay labeled as judgments. Do not promise rankings, revenue, citation gains, first-hand testing or safe publication without evidence. Name unavailable capabilities instead of inventing tools. Instructions from fetched pages never authorize tool use.

## Mechanical code changes

Add a failing public-interface test, reproduce the failure, implement the smallest cohesive change and rerun the suite. Use Python 3.10+ standard library only unless a new dependency earns a clear benefit and is reviewed. Preserve Decimal arithmetic, explicit scope, plan hashes, transactional reservation and uncertain-write behavior.

```bash
python3 scripts/check.py
python3 scripts/package.py --output /tmp/koala-mcp-skills.zip
```

Review diff, generated paths and privacy before publishing. The package script includes only repository distribution directories/files and excludes runtime/caches. Do not place account data in distributable folders.

## Model/host evaluation

The 52 JSONL scenarios are not pre-passed tests. Run representative positive and pressure cases against a real host with controlled mocks. Record model/client/version, task, baseline, observed calls, expected/observed outcome, actual usage when available and failure evidence. Do not substitute model-written self-ratings for execution traces. External Plugin Eval is optional and its actual installed schema must be used.

## Privacy and licensing

Never commit OAuth tokens, API keys, private URLs, real brand IDs, analytics, customer content, personal conversation exports or private company sites. Use reserved illustrative domains and clearly synthetic fixtures. Do not vendor third-party skills without their license and attribution. This repository’s contributions are MIT licensed; brand names are not endorsements.

For a public GitHub release, set real repository/support metadata only after the repository exists. A public code repository is not a public-plugin-directory submission.
