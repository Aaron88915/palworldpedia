#!/usr/bin/env python3
import urllib.request, re

# 检查英文版
print('=== 英文版页面标题 ===')
for u in ['/en/', '/en/pals/', '/en/pals/lamball/', '/en/pals/cattiva/', '/en/tech-tree/', '/en/tech-tree/Workbench/', '/en/breeding/', '/en/about/', '/en/contact/']:
    try:
        req = urllib.request.Request(f'https://palworldpedia.cc{u}', headers={'User-Agent': 'Mozilla/5.0'})
        c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
        title_m = re.search(r'<title>([^<]+)</title>', c)
        title = title_m.group(1) if title_m else '(no title)'
        # 检查 lang switch 按钮
        has_zh_switch = '中文' in c or '/zh' in c
        has_en_switch = '/en/' in c and 'EN' in c
        # 自动检测脚本
        has_detect = 'navigator.language' in c
        ins = len(re.findall(r'<ins class="adsbygoogle"', c))
        print(f'  {u:<30} ins={ins}  lang-switch={"Y" if (has_zh_switch or has_en_switch) else "N"}  detect={"Y" if has_detect else "N"}')
        print(f'    title: {title[:80]}')
    except Exception as e:
        print(f'  {u}: {e}')

print('\n=== 现场 action: zh 用户访问 en 应被跳回 zh ===')
# 用 Accept-Language: zh-CN 请求 /en/
import urllib.request
req = urllib.request.Request('https://palworldpedia.cc/en/', headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'zh-CN,zh;q=0.9'})
try:
    r = urllib.request.urlopen(req, timeout=15)
    final_url = r.geturl()
    print(f'  Final URL after zh request: {final_url}')
except Exception as e:
    print(f'  Error: {e}')
