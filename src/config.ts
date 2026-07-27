/**
 * 站点全局配置
 */

export const SITE = {
  name: 'Palworldpedia',
  shortName: '帕鲁百科',
  description: '幻兽帕鲁最全攻略站 - 帕鲁图鉴 / 配种计算器 / 科技树 / 词条筛选 / 基地电力计算。最专业的 Palworld 工具与攻略。',
  shortDescription: '幻兽帕鲁攻略站 - Palworld Guide & Tools',
  url: 'https://palworldpedia.cc',
  defaultImage: '/og-image.png',
  locale: 'zh-CN',
  alternateLocale: 'en-US',

  // 社交
  twitter: '@palworldpedia',

  // AdSense（申请通过后填入）
  adsense: {
    enabled: false,
    client: '',
  },

  // 联系
  email: 'contact@palworldpedia.cc',

  // i18n
  defaultLocale: 'zh' as const,
  locales: ['zh', 'en'] as const,
};

export const NAV = {
  zh: [
    { label: '首页', href: '/' },
    { label: '帕鲁图鉴', href: '/pals/' },
    { label: '配种计算器', href: '/breeding/' },
    { label: '科技树', href: '/tech-tree/' },
    { label: '基地计算', href: '/calculator/power/' },
    { label: '攻略', href: '/guides/' },
  ],
  en: [
    { label: 'Home', href: '/en/' },
    { label: 'Paldex', href: '/en/pals/' },
    { label: 'Breeding', href: '/en/breeding/' },
    { label: 'Tech Tree', href: '/en/tech-tree/' },
    { label: 'Power Calc', href: '/en/calculator/power/' },
    { label: 'Guides', href: '/en/guides/' },
  ],
};

export const PAL_TYPES = [
  { id: 'neutral', zh: '普通', en: 'Neutral', color: '#a0a8b0' },
  { id: 'fire', zh: '火', en: 'Fire', color: '#f87171' },
  { id: 'water', zh: '水', en: 'Water', color: '#5eb3f5' },
  { id: 'grass', zh: '草', en: 'Grass', color: '#4ade80' },
  { id: 'electric', zh: '电', en: 'Electric', color: '#fbbf24' },
  { id: 'ice', zh: '冰', en: 'Ice', color: '#93c5fd' },
  { id: 'ground', zh: '地', en: 'Ground', color: '#d97706' },
  { id: 'dark', zh: '暗', en: 'Dark', color: '#6b7280' },
  { id: 'dragon', zh: '龙', en: 'Dragon', color: '#c084fc' },
] as const;

export const WORK_SUITABILITIES = [
  { id: 'kindling', zh: '生火', en: 'Kindling', icon: '🔥' },
  { id: 'watering', zh: '浇水', en: 'Watering', icon: '💧' },
  { id: 'planting', zh: '播种', en: 'Planting', icon: '🌱' },
  { id: 'generating_electricity', zh: '发电', en: 'Generating Electricity', icon: '⚡' },
  { id: 'handiwork', zh: '手工作业', en: 'Handiwork', icon: '🔨' },
  { id: 'gathering', zh: '采集', en: 'Gathering', icon: '🌿' },
  { id: 'lumbering', zh: '伐木', en: 'Lumbering', icon: '🪓' },
  { id: 'mining', zh: '采矿', en: 'Mining', icon: '⛏️' },
  { id: 'medicine_production', zh: '制药', en: 'Medicine Production', icon: '💊' },
  { id: 'cooling', zh: '冷藏', en: 'Cooling', icon: '❄️' },
  { id: 'transporting', zh: '搬运', en: 'Transporting', icon: '📦' },
  { id: 'farming', zh: '种田', en: 'Farming', icon: '🌾' },
] as const;
