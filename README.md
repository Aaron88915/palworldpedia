# Palworldpedia

> 幻兽帕鲁攻略站 — Palworld Guide & Tools
> palworldpedia.cc · 中英双语 · 静态站 · 靠 AdSense 变现

## 站点概况

- **域名**：palworldpedia.cc（GitHub Pages + Cloudflare DNS）
- **内容**：288 只帕鲁图鉴 + 588 个科技树 + 80 个地图区域 + 配种计算器 + 电力计算器 + 强度排行 + 6 篇长文 SEO 攻略（中英双语）
- **总页面**：1,790（ZH + EN 全镜像 + 通用页）
- **数据版本**：Palworld **1.0**（2026-07-10 正式版，补丁 1.100.427），最新补丁 v1.0.5
- **目标受众**：Palworld 玩家，搜攻略和工具的搜索流量
- **变现**：Google AdSense（3 个广告位/页：top + inline + bottom）

## 技术栈

- **框架**：Astro 5.x（静态生成 + 零 JS 默认）
- **i18n**：自定义双语方案（`/pals/X/` = ZH，`/en/pals/X/` = EN），按浏览器/本地存储自动跳转
- **部署**：GitHub Pages + Actions（`main` 推 → 自动 build → 部署）
- **数据源**：pals.json / tech.json / regions.json（合并自 paldb.cc 权威数据 + palworld.wiki.gg + beckerfelipee 配种矩阵）
- **推送**：HTTPS 经常被墙，自动 fallback 到 SSH `git@ssh.github.com:443`

## 核心页面

| 路径 | 功能 | SEO 价值 |
|---|---|---|
| `/pals/` | 288 只帕鲁图鉴 + 6 维筛选 | ⭐⭐⭐ |
| `/pals/<id>/` | 单帕鲁详情（属性 / 技能 / 词条 / 掉落 / 配种 CTA） | ⭐⭐⭐ |
| `/breeding/` | 配种计算器（正向 / 反向 / 最短路径 / Path Finder 4 模式） | ⭐⭐⭐ |
| `/tech-tree/` | 588 科技列表（按真实解锁等级 Lv 1-80 筛选） | ⭐⭐⭐ |
| `/tech-tree/<slug>/` | 单科技详情（真实解锁等级 + 材料 + 描述） | ⭐⭐⭐ |
| `/regions/` | 80 个地图区域 × 9 大区 + 敌人等级区间 | ⭐⭐⭐ |
| `/tier-list/` | 帕鲁强度排行 S/A/B/C/D（4 维评分） | ⭐⭐⭐ |
| `/guides/palworld-1-0-guide/` | **Palworld 1.0 全内容攻略**（等级 80 / 新区域 / 变异 / 觉醒） | ⭐⭐⭐ |
| `/guides/boss-guide/` | 9 座塔主（普通 + 困难）打法 | ⭐⭐⭐ |
| `/guides/` | 6 篇长文攻略（1.0 / 新手 / 配种 / 科技树 / BOSS / 基地） | ⭐⭐⭐ |
| `/calculator/power/` | 基地电力计算器 | ⭐⭐ |
| `/about/`, `/contact/`, `/privacy/`, `/terms/` | 通用页 | ⭐ |

> 所有 ZH 页面都有 `/en/` 镜像，带 `hreflang` 三语标注（zh-CN / en / x-default）。

## 数据规模

```
src/data/
├── pals.json          288 帕鲁（含 1.0 变种），biomes 全部为英文官方区域名
├── tech.json          588 科技（结构 217 + 道具 371），每条含真实 unlockLevel（Lv 1-80）
├── regions.json       80 个 1.0 官方区域（名称 / 等级区间 / 所属大区）
├── pal-tiers.json     286 条 S/A/B/C/D 评分
├── breeding-data.json 40,972 配种边
└── types.ts           数据类型契约
```

## 本地开发

```bash
npm install
npm run dev          # 本地预览 http://localhost:4321
npm run build        # 产出 dist/（约 11s，1790 页）
npm run preview      # 预览构建结果
```

## 部署

```bash
# 改完代码后
git add -A
git commit -F COMMIT_MSG.txt   # pre-commit hook 会自动 build + 校验
py scripts/ssh-push-*.py      # SSH 推送（自动 rebase + push）
```

GitHub Actions 自动跑 `npm run build` → 上传 `dist/` → 部署到 `palworldpedia.cc`。

## 数据 / 内容更新流程

1. 改数据：直接编辑 `src/data/*.json`，或跑 `scripts/*.py` 从 paldb.cc 抓权威数据
2. 改文章：直接编辑 `src/pages/guides/*.astro` 与 `src/pages/en/guides/*.astro`
3. **提交前自动校验**（pre-commit hook）：build → 扫全站内部链接 → 扫空 `<a>`
4. SSH 推送

### 提交前必跑

```bash
py scripts/pre-commit-check.py             # build + 全部校验（= pre-commit hook 做的事）
py scripts/scan-all-404.py                 # 扫全站内部链接（所有路径，不只 pals/tech-tree）
py scripts/verify-no-empty-a.py            # 扫空 <a> 标签（无 href）
py scripts/audit-data-gaps.py              # 扫 biomes / description 缺口
py scripts/verify-1.0-release.py           # 1.0 内容自检（等级 / 塔主 / 区域）
```

### pre-commit hook

```bash
git config core.hooksPath .githooks   # 每个 clone 执行一次
```

hook 会跑一次完整 build（约 11s）再校验，坏链接 / 空 `<a>` 会直接挡下 commit。
临时绕过：`git commit --no-verify`。

## 目录结构

```
src/
├── data/                          # JSON 数据
│   ├── pals.json                 # 288 帕鲁
│   ├── tech.json                 # 588 科技（含 unlockLevel）
│   ├── regions.json              # 80 个区域
│   ├── pal-tiers.json            # tier 评分
│   ├── breeding-data.json        # 配种矩阵
│   └── types.ts                  # 数据类型契约
├── pages/                        # 路由
│   ├── index.astro              # ZH 首页
│   ├── tier-list.astro          # ZH 强度排行
│   ├── regions.astro            # ZH 区域全图鉴
│   ├── pals/                    # ZH 帕鲁图鉴
│   ├── breeding/                # 配种计算器
│   ├── tech-tree/               # 科技树
│   ├── calculator/power/        # 电力计算器
│   ├── guides/                  # ZH 6 篇攻略
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
└── styles/
    └── global.css               # 全局样式（深色主题）

scripts/                          # 工具脚本
├── _run.ps1 / _put.ps1 / _get.ps1   # 真项目 / 暂存区之间的文件搬运
├── pre-commit-check.py          # build + 校验（pre-commit hook 入口）
├── scan-all-404.py              # 全站内部链接扫描
├── verify-no-empty-a.py         # 空 <a> 标签扫描
├── audit-data-gaps.py           # 数据缺口审计
├── merge-tech.py                # 从 paldb.cc 合并权威科技树
├── rebuild-biomes.py            # 从 paldb.cc spawner 表重建帕鲁区域
├── fetch-all-pal-regions.py     # 抓 288 个帕鲁页的 Map 卡片
├── parse-towers.py              # 解析 9 座塔主名单
└── ssh-push-*.py                # SSH 推送（443 端口 fallback）
```

## 数据准确性原则

- **不猜数据**：帕鲁区域、科技解锁等级、塔主等级/血量一律来自 paldb.cc 权威数据
- 拿不到权威来源时，用**宽区域**（Palpagos Islands / Sakurajima / Sunreach / The World Tree …）而不是猜细粒度
- 关键字段语义：`tech.cost` = 古科技点价格（1-9），`tech.unlockLevel` = 玩家解锁等级（1-80）
- 帕鲁 `biomes` 必须是**英文官方区域名**（游戏内栖息地中文名不能进 EN 页）

## SEO 关键策略

- **每个帕鲁独立 URL**：`/pals/lifmunk/` 288 张 SEO 页面
- **每个科技独立 URL**：`/tech-tree/Battle_Cloth/` 588 张 SEO 页面
- **区域长尾**：`/regions/` 覆盖 "Palworld Sunreach / World Tree / area levels" 等搜索词
- **6 篇长文攻略**：每篇 1500-2500 字中文 + EN，H2 + 48+ 内部链接
- **结构化数据**：TechArticle / ItemList / VideoGame / BreadcrumbList
- **hreflang 双语标注** + `x-default` 默认 zh
- **sitemap-index.xml + sitemap-0.xml** 自动生成（1788 条 URL）
- **移动端优先**：响应式布局，按钮 ≥44px

## 变现

- **AdSense**：3 个广告位/页（top + inline ×1-N + bottom），全站 1790 页 100% 覆盖，client `ca-pub-6473783239192829`
- **Plausible Analytics**（待启用）：域名已绑定，但 Plausible.io 需注册付费 $9/mo
- **Cloudflare Web Analytics**（备选）：免费，需在 CF 后台开站并取 beacon token

## 已知约束 / 历史踩坑

- **Tech URL 用 `slug`（CamelCase）不是 `id`（lowercase）**：`/tech-tree/battle_cloth/` 404，必须 `/tech-tree/Battle_Cloth/`
- **Pal URL 用 `id`（lowercase）**：`/pals/lifmunk/`
- **GitHub Pages 大小写敏感**
- **Astro `slot` 是保留 prop 名**：AdSlot 用 `position` 不是 `slot`
- **PowerShell GBK 编码坑**：所有 .ps1 文件用英文；中文 print 需 `$env:PYTHONIOENCODING='utf-8'`
- **HTTPS 推送被墙**：自动 fallback SSH `git@ssh.github.com:443`
- **Cloudflare 403 一些数据源**：Fandom Wiki / palworld.wiki.gg 国内 IP 抓不到；用 paldb.cc 兜底
- **Python 脚本一律用相对路径**：绝对路径会命中暂存副本而不是真项目
- **`_get.ps1` 会覆盖暂存区**：打过补丁的文件别再 `_get.ps1` 一次
- **`[slug].astro` 的方括号是通配符**：文件搬运必须用 `Copy-Item -LiteralPath`

## License

- **数据**：CC-BY-SA 4.0
- **代码**：MIT
- **声明**：本站为非官方攻略站，与 Pocketpair 无关联
