import urllib.request, json
r = urllib.request.urlopen('https://api.github.com/repos/Aaron88915/palworldpedia/actions/runs?per_page=2', timeout=15)
data = json.loads(r.read().decode('utf-8'))
for run in data.get('workflow_runs', []):
    print(f"SHA: {run.get('head_sha', '?')[:7]} | Status: {run.get('status')} | Conclusion: {run.get('conclusion')} | Created: {run.get('created_at')}")
