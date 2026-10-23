#!/usr/bin/env node
/**
 * sitemap.xml lastmod 자동 갱신
 * ─────────────────────────────────────────────
 * 각 URL에 대응하는 HTML 파일의 마지막 git 커밋 날짜를 읽어
 * <lastmod> 값을 실제 수정일로 맞춥니다.
 *
 * 왜 필요한가
 *   구글은 IndexNow를 지원하지 않아 sitemap이 주된 발견 경로입니다.
 *   lastmod 가 부정확하면 구글이 그 값을 아예 무시합니다.
 *   정확한 lastmod 는 구글에 쓸 수 있는 몇 안 되는 자동 신호입니다.
 *
 * 사용법
 *   node scripts/update-sitemap.mjs
 */

import { execSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync } from "node:fs";

const HOST = process.env.SITE_HOST || "www.aroundtool.com";
const ORIGIN = `https://${HOST}`;
const FILE = "sitemap.xml";

if (!existsSync(FILE)) {
  console.error(`✗ ${FILE} 을 찾을 수 없습니다.`);
  process.exit(1);
}

/** 파일의 마지막 커밋 날짜 (YYYY-MM-DD). 커밋 이력이 없으면 null */
function lastCommitDate(path) {
  if (!existsSync(path)) return null;
  try {
    const out = execSync(`git log -1 --format=%cs -- "${path}"`, {
      encoding: "utf8",
    }).trim();
    return /^\d{4}-\d{2}-\d{2}$/.test(out) ? out : null;
  } catch {
    return null;
  }
}

let xml = readFileSync(FILE, "utf8");
let changed = 0;
let skipped = 0;

xml = xml.replace(
  /(<loc>\s*([^<\s]+)\s*<\/loc>\s*<lastmod>)([^<]*)(<\/lastmod>)/g,
  (whole, head, loc, oldDate, tail) => {
    // URL → 로컬 파일 경로
    let path = loc.replace(`${ORIGIN}/`, "");
    if (path === "" || path === "/") path = "index.html";

    const date = lastCommitDate(path);
    if (!date) {
      skipped++;
      return whole;
    }
    if (date !== oldDate.trim()) changed++;
    return head + date + tail;
  }
);

writeFileSync(FILE, xml, "utf8");
console.log(`· lastmod 갱신 ${changed}건 / 이력 없어 건너뜀 ${skipped}건`);
