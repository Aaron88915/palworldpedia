#!/usr/bin/env python3
import subprocess, os
os.chdir(r'D:\minamax\projects\palworldpedia')
env = os.environ.copy()
env['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=30'
env['PYTHONIOENCODING'] = 'utf-8'
for cmd in [['git','log','--oneline','origin/main','-5'], ['git','log','--oneline','-5']]:
    r = subprocess.run(cmd, capture_output=True, env=env)
    label = ' '.join(cmd[1:])
    print(f'=== {label} ===')
    print(r.stdout.decode('utf-8', 'replace'))
    if r.stderr:
        print('STDERR:', r.stderr.decode('utf-8', 'replace'))
