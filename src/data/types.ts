/**
 * Palworld 数据类型定义
 * 这是整个站点的数据契约
 */

// 帕鲁类型
export type PalType =
  | 'neutral'
  | 'fire'
  | 'water'
  | 'grass'
  | 'electric'
  | 'ice'
  | 'ground'
  | 'dark'
  | 'dragon';

// 工作适配度
export type WorkSuitability =
  | 'kindling'
  | 'watering'
  | 'planting'
  | 'generating_electricity'
  | 'handiwork'
  | 'gathering'
  | 'lumbering'
  | 'mining'
  | 'medicine_production'
  | 'cooling'
  | 'transporting'
  | 'farming';

// 技能
export interface PalSkill {
  id: string;
  name: { zh: string; en: string };
  level: number;          // 解锁等级
  type: PalType;          // 技能类型
  power: number;          // 威力
  cooldown: number;       // 冷却
  description: { zh: string; en: string };
}

// 词条
export interface PalPassive {
  id: string;
  name: { zh: string; en: string };
  description: { zh: string; en: string };
}

// 帕鲁
export interface Pal {
  id: string;                      // slug, 英文名小写
  paldeckNo: number;               // 图鉴编号 1-N
  name: { zh: string; en: string };
  types: PalType[];                // 1-2 个类型
  rarity: number;                  // 稀有度 1-20 (paldb.cc 标准)
  rarityTier: 'Common' | 'Rare' | 'Epic' | 'Legendary';  // 稀有度分级
  stats: {
    hp: number;
    attack: { melee: number; ranged: number };
    defense: number;
    speed: number;
  };
  workSuitability: Partial<Record<WorkSuitability, number>>;  // 工作适配度
  skills: PalSkill[];              // 主动技能
  passives: PalPassive[];          // 词条
  drops: string[];                 // 掉落物
  food: number;                    // 食量
  price: number;                   // 售价
  biomes: string[];                // 出现区域
  nightOnly?: boolean;             // 是否仅夜间出现
  description: { zh: string; en: string };
  image: string;                   // 图片 URL
  updatedAt: string;               // 数据更新时间 ISO
}

// 配种关系（无向图）
export interface BreedingEdge {
  parent1: string;        // Pal.id
  parent2: string;
  child: string;
}

// 道具
export interface Item {
  id: string;
  name: { zh: string; en: string };
  type: 'material' | 'food' | 'medicine' | 'key' | 'ammo' | 'pal_sphere' | 'other';
  rarity: number;
  description: { zh: string; en: string };
  source?: string;        // 获取方式
  image: string;
}

// 科技树节点
export interface TechNode {
  id: string;             // slug-based id
  slug: string;           // paldb.cc 原始 slug
  name: string;           // 英文名（paldb.cc 是英文）
  category: 'Structures' | 'Items';
  cost: number;           // 古科技点（1-9）
  icon: string;           // 图标 URL
  // 可选：详情页 enrich
  description?: string;
  image?: string;         // 大图
  materials?: { name: string; count: number }[];
  product?: string;
  unlockLevel?: number;
  defense?: number;
  hp?: number;
}

// 地图区域
export interface MapRegion {
  id: string;
  name: { zh: string; en: string };
  description: { zh: string; en: string };
  pals: string[];         // 出现的帕鲁 ID
  resources: string[];    // 资源点
  coords: { x: number; y: number };  // 地图坐标
}
