#!/usr/bin/env python3
"""Offline structural validation, not a live host or full external-schema certification."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def validate(root: Path=ROOT) -> dict:
    errors=[]
    def require(condition,message):
        if not condition:errors.append(message)
    try:
        rows=json.loads((root/'catalog/skills.json').read_text())['skills']
        data=json.loads((root/'skills/koala-core/references/tools.json').read_text())
        tools=data['tools'];names={t['name'] for t in tools};skills={s['name'] for s in rows}
        require(len(tools)==len(names)==62,'Expected 62 unique reviewed tools')
        require(len(rows)==len(skills)==26,'Expected 26 unique skills')
        actual={p.parent.name for p in (root/'skills').glob('*/SKILL.md')}
        require(actual==skills,'Skill index differs from SKILL.md directories')
        coverage=set();metadata_chars=0
        for row in rows:
            name=row['name'];base=root/'skills'/name;path=base/'SKILL.md';text=path.read_text()
            require(bool(re.fullmatch(r'koala-[a-z0-9]+(?:-[a-z0-9]+)*',name)) and len(name)<=64,f'Invalid skill name: {name}')
            require(text.startswith('---\n'),f'Missing frontmatter: {name}')
            front=text.split('---',2)[1]
            require(re.search(r'^name: '+re.escape(name)+r'$',front,re.M) is not None,f'Name mismatch: {name}')
            desc=re.search(r'^description: (.+)$',front,re.M)
            require(desc is not None,f'Missing description: {name}')
            if desc:
                description=json.loads(desc.group(1));metadata_chars+=len(description)+len(name)
                require(description==row['description'] and 1<=len(description)<=1024,f'Description mismatch or length: {name}')
            require(len(text.splitlines())<=500,f'Oversized SKILL.md: {name}')
            for section in ['## Inputs','## Bounded procedure','## Branches and stop conditions','## Output contract','## Operating boundaries']:
                require(section in text,f'Missing {section}: {name}')
            wf=json.loads((base/'assets/workflow.json').read_text())
            report=json.loads((base/'assets/report.schema.json').read_text())
            require(wf['skill']==name and set(wf['tools'])==set(row['tools']),f'Workflow/index mismatch: {name}')
            require(set(wf['tools'])<=names,f'Unknown tools in {name}')
            require(wf.get('executable') is False,f'Declarative workflow mislabeled executable: {name}')
            require(wf['limits']['max_automatic_write_retries']==0,f'Unsafe retry declaration: {name}')
            require(report['properties']['skill']['const']==name,f'Report schema mismatch: {name}')
            if name!='koala-core':coverage.update(wf['tools'])
            notes=(base/'references/tool-notes.md').read_text()
            require(all('## `'+t+'`' in notes for t in row['tools']),f'Missing local tool notes: {name}')
        require(coverage==names,'Non-core workflow coverage missing: '+', '.join(sorted(names-coverage)))
        for t in tools:
            require((root/'skills/koala-core/references/tools'/f'{t["name"]}.md').is_file(),f'Missing tool card {t["name"]}')
            require(t['cost']['kind'] in {'free','fixed','per_unique_seed','words','image'},f'Unknown cost kind: {t["name"]}')
        # Check local markdown links. Skill-local references may not reach siblings/parents.
        link_count=0
        for path in root.rglob('*.md'):
            if any(x in {'.git','.koala','__pycache__','dist'} for x in path.parts):continue
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
                if target.startswith(('http://','https://','#','mailto:')):continue
                target=target.split('#',1)[0]
                if not target:continue
                dest=(path.parent/target).resolve();link_count+=1
                require(dest.exists(),f'Broken local link: {path.relative_to(root)} -> {target}')
                if path.is_relative_to(root/'skills'):
                    skillroot=root/'skills'/path.relative_to(root/'skills').parts[0]
                    require(dest.is_relative_to(skillroot.resolve()),f'Nonportable skill reference: {path.relative_to(root)} -> {target}')
        for path in root.rglob('*.json'):
            if not any(x in {'.git','.koala','__pycache__','dist'} for x in path.parts):json.loads(path.read_text())
        for manifest in ['plugin.json','.claude-plugin/plugin.json','.codex-plugin/plugin.json']:
            m=json.loads((root/manifest).read_text());require(m.get('name')=='koala-mcp-skills' and m.get('version')=='0.1.0',f'Manifest identity/version: {manifest}')
            for key in ['skills','mcpServers']:
                if key in m:
                    value=m[key];require(isinstance(value,str) and value.startswith('./') and (root/value).exists(),f'Manifest path invalid: {manifest}:{key}')
        portable=json.loads((root/'mcp.json').read_text())['mcpServers']['koala-ai']
        compatibility=json.loads((root/'.mcp.json').read_text())['mcpServers']['koala-ai']
        require(portable=={'type':'streamable-http','url':'https://koala.sh/api/mcp'},'Portable remote MCP config mismatch')
        require(compatibility=={'type':'http','url':'https://koala.sh/api/mcp'},'Compatibility remote MCP config mismatch')
        require(not (root/'hooks').exists(),'Automatic hooks are not part of this release')
        scenarios=[json.loads(x) for x in (root/'benchmarks/scenarios.jsonl').read_text().splitlines() if x.strip()]
        require(len(scenarios)==52 and len({x['id'] for x in scenarios})==52,'Expected 52 unique host-agent scenarios')
        require(all(x['status']=='not-run' for x in scenarios),'Do not mark benchmark corpus as executed; store actual trial evidence separately')
        return {'passed':not errors,'errors':errors,'skills':len(skills),'reviewed_tools':len(names),'non_core_tool_coverage':len(coverage),
                'tool_cards':len(tools),'host_agent_scenarios_not_run':len(scenarios),'local_links_checked':link_count,
                'skill_discovery_metadata_characters':metadata_chars,
                'notice':'Offline structural checks, not full external JSON Schema validation, live host loading or model-behavior evaluation.'}
    except (OSError,ValueError,KeyError,TypeError,IndexError) as exc:
        return {'passed':False,'errors':errors+[str(exc)],'notice':'Structural validation failed'}

if __name__=='__main__':
    result=validate();print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
