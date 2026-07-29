import json
with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)
desc = sum(1 for t in techs if t.get('description'))
mat = sum(1 for t in techs if t.get('materials'))
lv = sum(1 for t in techs if t.get('unlockLevel'))
print(f'Desc: {desc}/587 ({desc/587*100:.0f}%)')
print(f'Materials: {mat}/587 ({mat/587*100:.0f}%)')
print(f'UnlockLevel: {lv}/587 ({lv/587*100:.0f}%)')
for t in techs:
    if t.get('description') and 'Workbench' in t['name']:
        print()
        print(t['name'] + ':')
        print('  ' + t['description'][:200])
        if t.get('materials'):
            print('  Materials: ' + str(t['materials']))
        break
