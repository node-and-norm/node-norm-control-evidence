"""Check repository-local Markdown navigation and expandable-section balance."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]


def without_fences(text):
    return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M|re.S)


def anchors(text):
    found=set();counts={}
    for title in re.findall(r'^#{1,6} (.+)$',without_fences(text),re.M):
        title=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',title).lower()
        base=re.sub(r'[^\w\s-]','',title).replace(' ','-')
        n=counts.get(base,0);counts[base]=n+1
        found.add(base+(f'-{n}' if n else ''))
    found.update(re.findall(r'(?:id|name)="([^"]+)"',text))
    return found


def check():
    errors=[]
    for path in ROOT.rglob('*.md'):
        if any(part in {'.git','.venv','private','build'} for part in path.relative_to(ROOT).parts): continue
        # Immutable source copies retain links relative to their original checkout.
        # Their exact contents are checked by the archived-run reproduction test.
        if any(path.is_relative_to(ROOT/f'experiments/jev-cec/execution-v2/{run}/source') for run in ('mock-001','live-001')): continue
        if any(path.is_relative_to(ROOT/f'experiments/jev-cec/instruction-comparison-001/{run}/source') for run in ('mock-001','live-001')): continue
        if any(path.is_relative_to(ROOT/f'experiments/jev-cec/packet-linkage-001/{run}/source') for run in ('mock-001','live-001')): continue
        if any(path.is_relative_to(ROOT/f'experiments/jev-cec/answer-execution-001/{run}/source') for run in ('mock-001','live-001')): continue
        text=path.read_text();body=without_fences(text)
        depth=0
        for token in re.findall(r'</?details\b[^>]*>',body):
            depth+=-1 if token.startswith('</') else 1
            if depth<0: errors.append(f'{path.relative_to(ROOT)}: unexpected details close')
        if depth: errors.append(f'{path.relative_to(ROOT)}: unbalanced details')
        links=re.findall(r'\]\(([^)]+)\)',body)+re.findall(r'href="([^"]+)"',body)
        for link in links:
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',link): continue
            dest,_,fragment=unquote(link).partition('#')
            target=(path.parent/dest).resolve() if dest else path
            if not target.is_relative_to(ROOT):
                errors.append(f'{path.relative_to(ROOT)}: link escapes repository: {link}');continue
            if not target.exists(): errors.append(f'{path.relative_to(ROOT)}: missing {link}');continue
            if fragment and target.suffix=='.md' and fragment not in anchors(target.read_text()):
                errors.append(f'{path.relative_to(ROOT)}: missing fragment {link}')
    return errors

if __name__=='__main__':
    errors=check()
    print('\n'.join(errors) if errors else 'Local Markdown links, fragments, and details sections pass.')
    sys.exit(bool(errors))
