#!/usr/bin/env python3
"""Verify paragraph parity across all paper pages."""
import sys, os, glob

errors = []
for path in glob.glob('papers/*/index.html'):
    slug = os.path.dirname(path).split('/')[-1]
    with open(path) as f:
        c = f.read()
    try:
        ar = c.split('class="lang-content ar')[1].split('</div>')[0].split('<section')
        en = c.split('class="lang-content en')[1].split('</div>')[0].split('<section')
        if len(ar) != len(en):
            errors.append(f'{slug}: section count AR={len(ar)-1} EN={len(en)-1}')
            continue
        for i in range(1, len(ar)):
            ap = ar[i].count('<p>')
            ep = en[i].count('<p>')
            if ap != ep:
                errors.append(f'{slug}: Section {i} AR={ap} EN={ep}')
        print(f'  OK: {slug} ({len(ar)-1} sections)')
    except Exception as e:
        errors.append(f'{slug}: parse error - {e}')

if errors:
    print('\nFAILURES:')
    for e in errors:
        print(f'  {e}')
    sys.exit(1)
else:
    print('\nAll papers passed.')
