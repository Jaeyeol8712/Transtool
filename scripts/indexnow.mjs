#!/usr/bin/env node
/**
 * IndexNow 색인 요청 스크립트
 * ─────────────────────────────────────────────
 * 네이버 · Bing · Yandex · Seznam · Yep 에 변경된 URL을 알립니다.
 * 구글은 IndexNow를 지원하지 않습니다 (SEO-AUTOMATION.md 참고).
 *
 * 사용법
 *   node scripts/indexnow.mjs            변경된 HTML만 전송 (git diff 기반)
 *   node scripts/indexnow.mjs --all      sitemap.xml의 모든 URL 전송
 *   node scripts/indexnow.mjs --dry      실제 전송 없이 대상만 출력
 *
 * 환경변수
 *   INDEXNOW_KEY   필수. 루트에 올린 키 파일명과 같아야 합니다.
 *   SITE_HOST      선택. 기본값 www.aroundtool.com
 */

import { execSync } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";

const HOST = process.env.SITE_HOST || "www.aroundtool.com";
const KEY = process.env.INDEXNOW_KEY;
const ORIGIN = `https://${HOST}`;

const ALL = process.argv.includes("--all");
const DRY = process.argv.includes("--dry");

// IndexNow 참여 검색엔진. 한 곳에 보내면 나머지에도 전파되지만,
// 네이버는 국내 반영 속도를 위해 직접 함께 호출합니다.
const ENDPOINTS = [
  "https://api.indexnow.org/indexnow",
  "https://searchadvisor.naver.com/indexnow",
];

if (!KEY) {
  console.error("✗ INDEXNOW_KEY 환경변수가 없습니다.");
  console.error("  GitHub → Settings → Secrets and variables → Actions 에 등록하세요.");
  process.exit(1);
}

/** sitemap.xml 에서 전체 URL 추출 */
function urlsFromSitemap() {
  if (!existsSync("sitemap.xml")) {
    console.error("✗ sitemap.xml 을 찾을 수 없습니다.");
    process.exit(1);
  }
  const xml = readFileSync("sitemap.xml", "utf8");
  return [...xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map((m) => m[1]);
}

/** 직전 커밋 대비 변경·추가된 HTML 파일 → URL */
function urlsFromGitDiff() {
  let out = "";
  try {
    // 첫 커밋이면 HEAD^ 가 없으므로 전체 목록으로 대체
    execSync("git rev-parse HEAD^", { stdio: "ignore" });
    out = execSync("git diff --name-only --diff-filter=AM HEAD^ HEAD", {
      encoding: "utf8",
    });
  } catch {
    console.log("· 이전 커밋이 없어 sitemap 전체를 대상으로 전환합니다.");
    return urlsFromSitemap();
  }

  const files = out
    .split("\n")
    .map((s) => s.trim())
    .filter((f) => f.endsWith(".html") && !f.includes("/"));

  return files.map((f) =>
    f === "index.html" ? `${ORIGIN}/` : `${ORIGIN}/${f}`
  );
}

async function submit(endpoint, urlList) {
  const body = {
    host: HOST,
    key: KEY,
    keyLocation: `${ORIGIN}/${KEY}.txt`,
    urlList,
  };

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify(body),
    });

    const label = new URL(endpoint).hostname;
    if (res.status === 200 || res.status === 202) {
      console.log(`  ✓ ${label} — ${res.status} 접수됨`);
    } else if (res.status === 403) {
      console.log(`  ✗ ${label} — 403 키 파일을 찾을 수 없습니다`);
      console.log(`     ${ORIGIN}/${KEY}.txt 가 실제로 열리는지 확인하세요.`);
    } else if (res.status === 422) {
      console.log(`  ✗ ${label} — 422 URL이 host와 맞지 않습니다`);
    } else if (res.status === 429) {
      console.log(`  ! ${label} — 429 요청이 너무 잦습니다. 잠시 후 재시도하세요`);
    } else {
      console.log(`  ? ${label} — ${res.status} ${res.statusText}`);
    }
  } catch (e) {
    console.log(`  ✗ ${new URL(endpoint).hostname} — 요청 실패: ${e.message}`);
  }
}

const urls = ALL ? urlsFromSitemap() : urlsFromGitDiff();

if (urls.length === 0) {
  console.log("· 전송할 URL이 없습니다. 변경된 HTML이 없습니다.");
  process.exit(0);
}

console.log(`· 대상 ${urls.length}개`);
urls.slice(0, 20).forEach((u) => console.log(`  ${u}`));
if (urls.length > 20) console.log(`  … 외 ${urls.length - 20}개`);

if (DRY) {
  console.log("\n· --dry 모드입니다. 실제로 전송하지 않았습니다.");
  process.exit(0);
}

console.log("");
for (const ep of ENDPOINTS) {
  await submit(ep, urls);
}

console.log("\n· 접수는 색인 확정이 아닙니다. 크롤링 우선순위가 올라갈 뿐입니다.");
