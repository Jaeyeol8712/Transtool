#!/usr/bin/env node
/**
 * Bing 웹마스터 도구에 사이트맵 제출 (Bing Webmaster API — SubmitFeed)
 * ─────────────────────────────────────────────
 * Bing 은 예전의 익명 사이트맵 핑(bing.com/ping)을 더 받지 않아, API 키로 제출합니다.
 * 키가 없으면 안내만 출력하고 성공으로 끝납니다(다른 단계에 영향 없음).
 *
 * 환경변수
 *   BING_WEBMASTER_KEY  Bing 웹마스터 도구 → 설정 → API 액세스 → API 키
 *   SITE_HOST           기본값 www.aroundtool.com
 */
const HOST = process.env.SITE_HOST || "www.aroundtool.com";
const KEY = (process.env.BING_WEBMASTER_KEY || "").trim();
const SITE = `https://${HOST}/`;
const FEEDS = [`https://${HOST}/sitemap.xml`, `https://${HOST}/feed.xml`];

if (!KEY) {
  console.log("· Bing 사이트맵 제출: BING_WEBMASTER_KEY 가 없어 건너뜁니다.");
  console.log("  Bing 웹마스터 도구 → 설정(톱니) → API 액세스에서 키를 만들고 GitHub Secrets 에 BING_WEBMASTER_KEY 로 등록하세요.");
  process.exit(0);
}

let fail = 0;
for (const feedUrl of FEEDS) {
  try {
    const res = await fetch(`https://ssl.bing.com/webmaster/api.svc/json/SubmitFeed?apikey=${encodeURIComponent(KEY)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({ siteUrl: SITE, feedUrl }),
    });
    const text = await res.text();
    if (res.ok) console.log(`  ✓ Bing 웹마스터 — ${feedUrl} 제출됨`);
    else { fail++; console.log(`  ✗ Bing 웹마스터 — ${feedUrl} ${res.status} ${text.slice(0, 200)}`); }
  } catch (e) {
    fail++; console.log(`  ✗ Bing 웹마스터 — ${feedUrl} 요청 실패: ${e.message}`);
  }
}
if (fail) {
  console.log("  · 사이트가 Bing 웹마스터 도구에 등록·인증돼 있는지, siteUrl 이 등록한 주소와 같은지 확인하세요.");
  process.exit(1);
}
