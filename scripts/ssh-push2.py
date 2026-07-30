#!/usr/bin/env python3
import subprocess, os
os.chdir(r'D:\minamax\projects\palworldpedia')
env = os.environ.copy()
env['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=30'
env['PYTHONIOENCODING'] = 'utf-8'

# pull --rebase
print('=== git pull --rebase ===')
r = subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], capture_output=True, env=env, timeout=60)
print('exit:', r.returncode)
print('STDOUT:', r.stdout.decode('utf-8', 'replace'))
print('STDERR:', r.stderr.decode('utf-8', 'replace'))

print('\n=== git log --oneline -3 ===')
r = subprocess.run(['git', 'log', '--oneline', '-3'], capture_output=True, env=env)
print(r.stdout.decode('utf-8', 'replace'))

print('\n=== git status -sb ===')
r = subprocess.run(['git', 'status', '-sb'], capture_output=True, env=env)
print(r.stdout.decode('utf-8', 'replace'))

# push
print('\n=== git push origin main ===')
r = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, env=env, timeout=120)
print('exit:', r.returncode)
print('STDOUT:', r.stdout.decode('utf-8', 'replace'))
print('STDERR:', r.stderr.decode('utf-8', 'replace'))
