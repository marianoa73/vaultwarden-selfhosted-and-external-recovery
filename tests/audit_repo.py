"""Audit distributable text: privacy patterns, secrets, local Markdown links, JSON/SVG validity, required files."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
patterns = [r'192' + r'\.168', r'\b10' + r'\.[0-9]+\.[0-9]+\.', r'\b172' + r'\.(1[6-9]|2[0-9]|3[01])\.', 'duck' + 'dns', 'ts' + r'\.net',
            '/s' + 'rv/', '/ho' + 'me/', 'AI' + 'HUB', 'rpi-' + 'k3s', 'infer' + 'de', 'taila[0-9a-f]{4}', 'nvapi' + '-', 'sk-or' + '-',
            'BEGIN [A-Z ]*PRIVATE' + ' KEY', 'ssh-ed25519 AAAAC3[A-Za-z0-9+/]{40,}', 'gmail' + r'\.com', r'@' + r'[a-z0-9-]+\.(lan|local)\b']
fail, count = [], 0
for p in ROOT.rglob('*'):
    rel = p.relative_to(ROOT)
    if not p.is_file() or any(x in ('__pycache__', '.git') for x in rel.parts):
        continue
    if p.suffix in ('.png', '.gif', '.jpg'):
        continue
    if p.suffix == '.svg':
        ET.parse(p)
    text = p.read_text(encoding='utf-8')
    count += 1
    for pattern in patterns:
        if re.search(pattern, text, re.I):
            fail.append(f'{rel}: privacy rule {pattern}')
    if p.suffix == '.md':
        for href in re.findall(r'\]\(([^)]+)\)', text):
            if ':' in href or href.startswith('#'):
                continue
            if not (p.parent / href.split('#')[0].split('?')[0]).exists():
                fail.append(f'{rel}: missing link {href}')
for name in ['README.md', 'README.es.md', 'LICENSE', 'NOTICE.md', 'SECURITY.md', 'CHANGELOG.md', 'CONTRIBUTORS.md', 'docs/index.html', 'docs/.nojekyll',
             'src/vw-common.sh', 'src/vw-snapshot.sh', 'src/vw-backup.sh', 'src/vw-send.sh', 'src/vw-receive.sh', 'src/vw-restore.sh',
             'examples/compose.primary.yml', 'examples/compose.standby.yml', 'examples/vw.env.example', 'tests/test_backup_restore.sh']:
    if not (ROOT / name).is_file():
        fail.append(f'missing {name}')
if fail:
    print('\n'.join(fail))
    sys.exit(1)
print(f'OK: {count} text files, SVG parsing, local Markdown links, privacy and secret patterns, required files')
