#!/usr/bin/env node
/**
 * 구글 서치콘솔에 sitemap.xml · feed.xml 을 자동 (재)제출합니다.
 * ─────────────────────────────────────────────
 * 구글은 IndexNow 를 지원하지 않고, 색인 요청 API(Indexing API)는 채용공고·라이브 방송 전용이라
 * 일반 페이지에 쓰면 정책 위반입니다. 공식적으로 허용된 자동화는 "사이트맵 제출" 이며,
 * 정확한 lastmod 와 함께 제출하면 구글이 바뀐 페이지를 더 빨리 다시 가져갑니다.
 *
 * 필요한 것 (한 번만 설정)
 *   GitHub Secrets  GSC_SERVICE_ACCOUNT  서비스 계정 JSON 키 전체 내용
 *   GitHub Variables GSC_SITE            서치콘솔 속성 (기본값 https://www.aroundtool.com/)
 *                                        도메인 속성이면 sc-domain:aroundtool.com
 *   서치콘솔 → 설정 → 사용자 및 권한 에 서비스 계정 이메일을 "소유자" 로 추가
 *
 * 설정이 없으면 아무것도 하지 않고 정상 종료합니다.
 */
import crypto from "node:crypto";

const raw = process.env.GSC_SERVICE_ACCOUNT;
if (!raw) {
  console.log("· GSC_SERVICE_ACCOUNT 가 없어 구글 사이트맵 제출을 건너뜁니다.");
  process.exit(0);
}
const sa = JSON.parse(raw);
const SITE = process.env.GSC_SITE || "https://www.aroundtool.com/";
const ORIGIN = "https://" + (process.env.SITE_HOST || "www.aroundtool.com");
const FEEDS = [`${ORIGIN}/sitemap.xml`, `${ORIGIN}/feed.xml`];

const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const now = Math.floor(Date.now() / 1000);
const unsigned = b64({ alg: "RS256", typ: "JWT" }) + "." + b64({
  iss: sa.client_email,
  scope: "https://www.googleapis.com/auth/webmasters",
  aud: "https://oauth2.googleapis.com/token",
  iat: now,
  exp: now + 3600,
});
const jwt = unsigned + "." + crypto.sign("RSA-SHA256", Buffer.from(unsigned), sa.private_key).toString("base64url");

process.on("unhandledRejection", (e) => { console.log(`✗ 요청 실패: ${e.message}`); process.exit(0); });

const tokRes = await fetch("https://oauth2.googleapis.com/token", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: jwt }),
});
if (!tokRes.ok) {
  console.log(`✗ 구글 인증 실패 (${tokRes.status}) — 서비스 계정 키를 확인하세요.`);
  process.exit(0);
}
const { access_token } = await tokRes.json();

for (const feed of FEEDS) {
  const url = `https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(SITE)}/sitemaps/${encodeURIComponent(feed)}`;
  const res = await fetch(url, { method: "PUT", headers: { Authorization: `Bearer ${access_token}` } });
  if (res.ok) console.log(`  ✓ 구글 서치콘솔 — ${feed} 제출됨`);
  else if (res.status === 403) console.log(`  ✗ 403 — 서치콘솔에서 ${sa.client_email} 를 소유자로 추가했는지, GSC_SITE(${SITE})가 맞는지 확인하세요.`);
  else console.log(`  ? ${res.status} ${await res.text()}`);
}
