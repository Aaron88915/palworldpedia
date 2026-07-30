# Palworldpedia

> 幻兽帕鲁攻略站 — Palworld Guide & Tools

## 站点定位

- **域名**：palworldpedia.cc
- **目标**：Palworld 玩家的核心攻略站，吃搜索流量 + 工具型停留

## 技术栈

- **框架**：Astro 5.x（静态生成 + 群岛架构）
- **i18n**：中文（默认）/ English
- **部署**：GitHub Pages + Actions 自动部署
- **数据驱动**：JSON 数据源 + 自动生成静态页

## 核心功能

- 🥇 帕鲁图鉴（400+ 帕鲁，自动生成 SEO 页面）
- 🥇 配种计算器（核心差异化工具）
- 🥈 科技树可视化
- 🥈 词条 / 性格 / 体型筛选器
- 🥉 基地电力计算器
- 🥉 BOSS 攻略合集

## 本地开发

```bash
npm install
npm run dev          # http://localhost:4321
npm run build        # 构建静态站
npm run preview      # 预览构建结果
```

## 目录结构

```
src/
├── data/             # JSON 数据源（pals / breeding / items / map）
├── pages/            # 页面路由
│   ├── index.astro       # 中文首页
│   ├── pals/             # 帕鲁图鉴
│   ├── breeding/         # 配种工具
│   ├── calculator/       # 各类计算器
│   ├── tech-tree/        # 科技树
│   └── en/               # 英文镜像
├── layouts/          # 布局组件
├── components/       # UI 组件
├── content/          # MDX 攻略文章
│   ├── guides/
│   └── bosses/
└── styles/           # 全局样式
```

## 数据更新流程

1. 游戏版本更新 → 重新跑 `scripts/fetch-data.mjs`（待实现）
2. 数据写入 `src/data/*.json`
3. 自动 diff 校验
4. Git 提交 → 触发自动构建

## SEO 关键策略

- 每个帕鲁独立 URL（`/pals/lamball`）
- schema.org 结构化数据（VideoGame + ItemList + FAQPage）
- hreflang 标签（zh-CN / en-US）
- sitemap.xml 自动生成
- 移动端优先 + Core Web Vitals < 2.5s LCP

## License

- 数据：CC-BY-SA 4.0
- 代码：MIT
