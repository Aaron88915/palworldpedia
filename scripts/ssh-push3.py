#!/usr/bin/env python3
"""Push via SSH (HTTPS unreliable from this machine)"""
import subprocess, os
os.chdir(r'D:\minamax\projects\palworldpedia')
env = os.environ.copy()
env['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=30'
env['PYTHONIOENCODING'] = 'utf-8'

# 确保 remote 是 SSH
subprocess.run(['git', 'remote', 'set-url', 'origin', 'git@ssh.github.com:Aaron88915/palworldpedia.git'])

# fetch + rebase + push
for cmd, label in [
    (['git', 'fetch', 'origin'], 'fetch'),
    (['git', 'pull', '--rebase', 'origin', 'main'], 'pull --rebase'),
    (['git', 'push', 'origin', 'main'], 'push'),
]:
    print(f'=== {label} ===')
    r = subprocess.run(cmd, capture_output=True, env=env, timeout=120)
    print('exit:', r.returncode)
    if r.stdout:
        print(r.stdout.decode('utf-8', 'replace'))
    if r.stderr:
        print(r.stderr.decode('utf-8', 'replace'))
    if r.returncode != 0 and label != 'push':
        break
