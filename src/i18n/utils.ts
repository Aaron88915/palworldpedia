/**
 * i18n 工具函数
 */
import { STRINGS, type Locale } from './strings';

export type { Locale };

/**
 * 从 URL 路径判断语言
 * - /en/... → 'en'
 * - 其他（默认） → 'zh'
 */
export function getLangFromUrl(url: URL | string): Locale {
  const path = typeof url === 'string' ? url : url.pathname;
  return path === '/en' || path.startsWith('/en/') ? 'en' : 'zh';
}

/**
 * 获取翻译字符串
 * 支持 'nav.home' / 'common.search' / 'home.title' 等点分路径
 * 找不到时返回 key 本身 + console.warn（开发期）
 */
export function t(key: string, lang: Locale): string {
  const parts = key.split('.');
  let cur: any = STRINGS;
  for (const p of parts) {
    if (cur == null) return key;
    cur = cur[p];
  }
  if (cur && typeof cur === 'object' && (cur.zh || cur.en)) {
    return cur[lang] || cur.zh || key;
  }
  if (typeof cur === 'string') {
    return cur; // 单语 fallback（不该发生）
  }
  return key;
}

/**
 * 创建当前 lang 的 t 函数（页面用）
 */
export function useTranslations(lang: Locale) {
  return (key: string) => t(key, lang);
}

/**
 * 切换语言路径
 * - 已在 /en/ 路径 → 去掉 /en 前缀（返回 /xxx）
 * - 其他 → 加 /en 前缀
 * 自动处理根路径
 */
export function switchLangPath(currentPath: string): string {
  const isEn = currentPath === '/en' || currentPath.startsWith('/en/');
  if (isEn) {
    const stripped = currentPath.replace(/^\/en/, '') || '/';
    return stripped.startsWith('/') ? stripped : '/' + stripped;
  }
  // zh → en
  if (currentPath === '/' || currentPath === '') return '/en/';
  return '/en' + (currentPath.startsWith('/') ? currentPath : '/' + currentPath);
}

/**
 * hreflang 链接
 * 给定当前页面路径 + 当前 lang，返回 zh/en 两条 alternate
 */
export function hreflangsFor(currentPath: string): { lang: string; href: string }[] {
  const isEn = currentPath === '/en' || currentPath.startsWith('/en/');
  if (isEn) {
    const zhPath = currentPath.replace(/^\/en/, '') || '/';
    return [
      { lang: 'en', href: currentPath },
      { lang: 'zh-CN', href: zhPath },
    ];
  }
  return [
    { lang: 'zh-CN', href: currentPath },
    { lang: 'en', href: switchLangPath(currentPath) },
  ];
}
