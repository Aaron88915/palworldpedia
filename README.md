# Palworldpedia

> 幻兽帕鲁攻略站 — Palworld Guide & Tools
> palworldpedia.cc · 中英双语 · 静态站 · 靠 AdSense 变现

## 站点概况

- **域名**：palworldpedia.cc（GitHub Pages + Cloudflare DNS）
- **内容**：288 只帕鲁图鉴 + 587 个科技树 + 配种计算器 + 电力计算器 + 强度排行 + 5 篇长文 SEO 攻略（中英双语）
- **总页面**：1,784（885 ZH + 885 EN + 14 工具/通用）
- **目标受众**：Palworld 玩家，搜攻略和工具的搜索流量
- **变现**：Google AdSense（3 个广告位/页：top + inline + bottom）

## 技术栈

- **框架**：Astro 5.x（静态生成 + 零 JS 默认）
- **i18n**：自定义双语方案（`/pals/X/` = ZH，`/en/pals/X/` = EN），按浏览器/本地存储自动跳转
- **部署**：GitHub Pages + Actions（`main` 推 → 自动 build → 部署）
- **数据源**：pals.json / tech.json（合并自 paldb.cc + palworld.wiki.gg + beckerfelipee 配种矩阵）
- **推送**：HTTPS 经常被墙，自动 fallback 到 SSH `git@ssh.github.com:443`

## 核心页面

| 路径 | 功能 | SEO 价值 |
|---|---|---|
| `/pals/` | 288 只帕鲁图鉴 + 6 维筛选 | ⭐⭐⭐ |
| `/pals/<id>/` | 单帕鲁详情（属性 / 技能 / 词条 / 掉落 / 配种 CTA） | ⭐⭐⭐ |
| `/breeding/` | 配种计算器（正向 / 反向 / 最短路径 / Path Finder 4 模式） | ⭐⭐⭐ |
| `/tech-tree/` | 587 科技列表 + 详情页 | ⭐⭐⭐ |
| `/tier-list/` | 帕鲁强度排行 S/A/B/C/D（4 维评分） | ⭐⭐⭐ |
| `/calculator/power/` | 基地电力计算器 | ⭐⭐ |
| `/guides/` | 5 篇长文攻略（新手 / 配种 / 科技树 / BOSS / 基地） | ⭐⭐⭐ |
| `/guides/<slug>/` | 单篇攻略（ZH + EN） | ⭐⭐⭐ |
| `/about/`, `/contact/`, `/privacy/`, `/terms/` | 通用页 | ⭐ |

## 数据规模

```
src/data/
├── pals.json          288 帕鲁（含 7 DLC 变种）
├── tech.json          587 科技（结构 270 + 道具 317）
├── pal-tiers.json     287 帕鲁 S/A/B/C/D 评分
├── breeding-data.json 40,972 配种边
└── pals-data.json / skills-data.json  旧版（保留兼容）
```

## 本地开发

```bash
npm install
npm run dev          # 本地预览 http://localhost:4321
npm run build        # 产出 dist/（29s，1784 页）
npm run preview      # 预览构建结果
```

## 部署

```bash
# 改完代码后
git add -A
git commit -F COMMIT_MSG.txt
py scripts/ssh-push-*.py   # SSH 推送（自动 rebase + push）
```

GitHub Actions 自动跑 `npm run build` → 上传 `dist/` → 部署到 `palworldpedia.cc`。

## 数据 / 内容更新流程

1. 改数据：直接编辑 `src/data/*.json` 或跑 `scripts/*.py` 自动抓
2. 改文章：直接编辑 `src/pages/guides/*.astro` 或 `src/pages/en/guides/*.astro`
3. Build 验证：跑下面这套检测
4. SSH 推送

### 提交前必跑

```bash
py scripts/scan-all-404.py     # 扫全站内部链接 404
py scripts/verify-no-empty-a.py # 扫空 <a> 标签（无 href）
py scripts/audit-data-gaps.py  # 扫 biomes / description 缺口
```

## 目录结构

```
src/
├── data/                          # JSON 数据
│   ├── pals.json                 # 288 帕鲁
│   ├── tech.json                 # 587 科技
│   ├── pal-tiers.json            # tier 评分
│   ├── breeding-data.json        # 配种矩阵
│   └── types.ts                  # 数据类型契约
├── pages/                        # 路由
│   ├── index.astro              # ZH 首页
│   ├── tier-list.astro          # ZH 强度排行
│   ├── pals/                    # ZH 帕鲁图鉴
│   ├── breeding/                # 配种计算器
│   ├── tech-tree/               # 科技树
│   ├── calculator/power/        # 电力计算器
│   ├── guides/                  # ZH 5 篇攻略
│   └── en/                       # EN 镜像（全部 ZH 页面都有 EN 版）
├── layouts/
│   └── Layout.astro             # 基础布局（AdSense + Plausible + hreflang）
├── components/
│   ├── AdSlot.astro             # 广告位容器
│   ├── Header.astro / Footer.astro
│   └── PalImage.astro
├── i18n/
│   ├── strings.ts               # 双语字典
│   └── utils.ts                 # t() / switchLangPath() / hreflangsFor()
├── styles/
│   └── global.css               # 全局样式（深色主题）
└── scripts/                      # 100+ 工具脚本
    ├── ssh-push-*.py            # SSH 推送（443 端口 fallback）
    ├── scan-all-404.py          # 内部链接 404 扫描
    ├── verify-no-empty-a.py     # 空 <a> 标签扫描
    ├── fix-slug-case.py         # 修 slug 大小写
    ├── fix-empty-a-tags.py      # 删空 <a> 标签
    ├── audit-data-gaps.py       # 数据缺口审计
    └── fill-*.py                # 数据自动抓取 / 补全
```

## SEO 关键策略

- **每个帕鲁独立 URL**：`/pals/lifmunk/` 288 张 SEO 页面
- **每个科技独立 URL**：`/tech-tree/Battle_Cloth/` 587 张 SEO 页面
- **5 篇长文攻略**：每篇 1500-2500 字中文 + EN，H2 + 48+ 内部链接
- **结构化数据**：TechArticle / VideoGame / BreadcrumbList
- **hreflang 双语标注** + `x-default` 默认 zh
- **sitemap-index.xml + sitemap-0.xml** 自动生成（GSC 已提交）
- **移动端优先**：响应式布局，按钮 ≥44px

## 变现

- **AdSense**：3 个广告位/页（top + inline ×1-N + bottom），2 个在 404 页
- **Plausible Analytics**（待启用）：域名已绑定，但 Plausible.io 需注册付费 $9/mo
- **Cloudflare Web Analytics**（备选）：免费，但需域名解析在 CF

## 已知约束 / 历史踩坑

- **Tech URL 用 `slug`（CamelCase）不是 `id`（lowercase）**：详见 `agents/mavis/memory`
- **GitHub Pages 大小写敏感**：`/tech-tree/battle_cloth/` 404，必须 `/tech-tree/Battle_Cloth/`
- **Astro `slot` 是保留 prop 名**：AdSlot 用 `position` 不是 `slot`（[bug 历史](https://github.com)）
- **PowerShell GBK 编码坑**：所有 .ps1 文件用英文；中文 print 需 `$env:PYTHONIOENCODING='utf-8'`
- **HTTPS 推送被墙**：自动 fallback SSH `git@ssh.github.com:443`
- **Cloudflare 403 一些数据源**：Fandom Wiki / palworld.wiki.gg 国内 IP 抓不到；用 paldb.cc 兜底

## License

- **数据**：CC-BY-SA 4.0
- **代码**：MIT
- **声明**：本站为非官方攻略站，与 Pocketpair 无关联
