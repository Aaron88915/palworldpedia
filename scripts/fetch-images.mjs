/**
 * Palworld 帕鲁图片下载脚本
 *
 * 数据源: Fandom Wiki (palworld.fandom.com)
 * 用途: 下载帕鲁缩略图到 public/images/pals/
 *
 * 使用:
 *   node scripts/fetch-images.mjs
 *
 * 输出: public/images/pals/{filename}
 */

import { readFile, writeFile, mkdir } from 'fs/promises';
import { existsSync, statSync, createWriteStream } from 'fs';
import { get } from 'https';
import { URL } from 'url';

const API = 'https://palworld.fandom.com/api.php';
const CDN = 'https://static.wikia.nocookie.net';
const USER_AGENT = 'Palworldpedia-Bot/1.0 (https://palworldpedia.cc) Node.js';
const CONCURRENCY = 6;
const RATE_LIMIT_MS = 150;
const PALS_PATH = 'src/data/pals.json';
const IMG_DIR = 'public/images/pals';
const PROGRESS_PATH = 'public/images/pals/.downloaded.json';
const MIN_SIZE = 1024; // 1KB 以下的文件视为损坏

/**
 * HTTP GET，返回 Buffer
 */
function httpGetBuffer(url, redirects = 5) {
  return new Promise((resolve, reject) => {
    if (redirects <= 0) return reject(new Error('Too many redirects'));
    const u = new URL(url);
    const req = get(u, {
      headers: { 'User-Agent': USER_AGENT, 'Accept': '*/*' },
    }, (res) => {
      // 重定向
      if ([301, 302, 303, 307, 308].includes(res.statusCode)) {
        const loc = res.headers.location;
        if (!loc) return reject(new Error('Redirect with no Location'));
        res.resume();
        return resolve(httpGetBuffer(loc, redirects - 1));
      }
      if (res.statusCode !== 200) {
        res.resume();
        return reject(new Error(`HTTP ${res.statusCode}`));
      }
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => resolve(Buffer.concat(chunks)));
      res.on('error', reject);
    });
    req.on('error', reject);
    req.setTimeout(30000, () => req.destroy(new Error('Timeout')));
  });
}

/**
 * Fandom API 调用
 */
async function apiFetch(params, retries = 2) {
  const u = new URL(API);
  for (const [k, v] of Object.entries(params)) u.searchParams.set(k, v);
  for (let i = 0; i <= retries; i++) {
    try {
      const res = await fetch(u, { headers: { 'User-Agent': USER_AGENT } });
      if (res.status === 429 || res.status === 503) {
        await new Promise((r) => setTimeout(r, 1500 * (i + 1)));
        continue;
      }
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      if (i === retries) throw e;
      await new Promise((r) => setTimeout(r, 800 * (i + 1)));
    }
  }
}

/**
 * 拿帕鲁图片的 CDN URL
 */
async function getImageCdnUrl(filename) {
  const data = await apiFetch({
    action: 'query',
    titles: `File:${filename}`,
    prop: 'imageinfo',
    iiprop: 'url',
    iiurlwidth: '400',
    format: 'json',
  });
  const page = Object.values(data.query?.pages || {})[0];
  if (!page || page.missing !== undefined) return null;
  const info = page.imageinfo?.[0];
  return info?.thumburl || info?.url || null;
}

/**
 * 主流程
 */
async function main() {
  console.log('🖼️  Palworld 帕鲁图片下载\n');

  // 加载进度
  let downloaded = {};
  if (existsSync(PROGRESS_PATH)) {
    downloaded = JSON.parse(await readFile(PROGRESS_PATH, 'utf-8'));
    console.log(`  📂 已有 ${Object.keys(downloaded).length} 个图片`);
  }

  // 加载帕鲁列表
  const pals = JSON.parse(await readFile(PALS_PATH, 'utf-8'));
  console.log(`  📋 共 ${pals.length} 只帕鲁\n`);

  // 创建目录
  if (!existsSync(IMG_DIR)) await mkdir(IMG_DIR, { recursive: true });

  // 任务队列（跳过已下载 + 无 image 字段的）
  const tasks = pals
    .filter((p) => p.image && p.image.includes('/'))
    .filter((p) => {
      const filename = p.image.split('/').pop();
      return !downloaded[filename];
    });

  console.log(`  🔄 待下载: ${tasks.length}（已下载 ${Object.keys(downloaded).length}）\n`);

  let ok = 0, fail = 0, lastLog = 0;

  // 并发
  const queue = [...tasks];
  const workers = Array(CONCURRENCY).fill(null).map(async () => {
    while (queue.length > 0) {
      const pal = queue.shift();
      if (!pal) break;
      const filename = pal.image.split('/').pop();
      const dest = `${IMG_DIR}/${filename}`;

      try {
        const url = await getImageCdnUrl(filename);
        if (!url) {
          downloaded[filename] = 'missing';
          fail++;
          continue;
        }
        const buf = await httpGetBuffer(url);
        if (buf.length < MIN_SIZE) {
          throw new Error(`Too small: ${buf.length} bytes`);
        }
        await writeFile(dest, buf);
        downloaded[filename] = 'ok';
        ok++;

        if (ok - lastLog >= 20) {
          lastLog = ok;
          // 增量保存进度
          await writeFile(PROGRESS_PATH, JSON.stringify(downloaded, null, 2));
          process.stdout.write(`  ✅ [${ok}/${tasks.length}]\n`);
        }
      } catch (e) {
        downloaded[filename] = `fail: ${e.message}`;
        fail++;
        process.stdout.write(`  ❌ ${pal.id} (${filename}): ${e.message}\n`);
      }

      await new Promise((r) => setTimeout(r, RATE_LIMIT_MS));
    }
  });

  await Promise.all(workers);

  // 最终保存
  await writeFile(PROGRESS_PATH, JSON.stringify(downloaded, null, 2));

  console.log(`\n🎉 完成！下载 ${ok} / 失败 ${fail}`);
  console.log(`   图片目录: ${IMG_DIR}/`);
}

main().catch((e) => { console.error('💥 失败:', e); process.exit(1); });
