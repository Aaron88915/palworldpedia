#!/usr/bin/env python3
import re
raw = open('src/pages/breeding/index.astro', 'rb').read()
m = re.search(rb'<AdSlot slot="inline" />', raw)
if m:
    start = max(0, m.start() - 300)
    end = min(len(raw), m.end() + 300)
    snippet = raw[start:end]
    # 替换 \r\n 显式
    snippet_visible = snippet.replace(b'\r\n', b'<CRLF>\n')
    print('=== bytes around AdSlot (CRLF explicit) ===')
    print(snippet_visible.decode('utf-8', 'ignore'))
    print()
    print(f'AdSlot at byte {m.start()}, file is {len(raw)} bytes')
    print(f'CRLF count in file: {raw.count(b"\\r\\n")}')
    print(f'LF count in file: {raw.count(b"\\n")}')
