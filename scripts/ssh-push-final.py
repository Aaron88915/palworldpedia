#!/usr/bin/env python3
"""SSH push helper (HTTPS is unreliable from this IP)."""
import os
import subprocess
import sys

os.environ['GIT_SSH_COMMAND'] = 'ssh -i C:/Users/31963/.ssh/id_ed25519 -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL'

# Ensure SSH remote
subprocess.run(['git', 'remote', 'set-url', 'origin', 'git@ssh.github.com:Aaron88915/palworldpedia.git'], check=False)

# Stage
r = subprocess.run(['git', 'add', '-A'])
print('git add:', r.returncode)

# Commit using file
r = subprocess.run(['git', 'commit', '-F', 'COMMIT_MSG.txt'])
print('git commit:', r.returncode)
if r.returncode != 0:
    print('No commit to make or commit failed')
    sys.exit(0)

# Fetch + rebase + push
r = subprocess.run(['git', 'fetch', 'origin'], env=os.environ)
print('git fetch:', r.returncode)
r = subprocess.run(['git', 'pull', '--rebase', '--autostash', 'origin', 'main'], env=os.environ)
print('git pull --rebase:', r.returncode)
r = subprocess.run(['git', 'push', 'origin', 'main'], env=os.environ)
print('git push:', r.returncode)

if r.returncode == 0:
    r2 = subprocess.run(['git', 'log', '--oneline', '-1'])
    print('Latest:', r2.stdout.decode().strip())
