#!/usr/bin/env node
/**
 * GA4 방문자 수(오늘·어제·전체)를 assets/visitors.json 으로 저장합니다.
 * 사이트 사이드바·푸터의 방문자 표시가 이 파일을 읽습니다.
 *
 * 필요한 것 (구글 서치콘솔 자동 제출과 같은 서비스 계정을 써도 됩니다)
 *   GitHub Secrets  GSC_SERVICE_ACCOUNT  서비스 계정 JSON 키 전체 내용
 *   GA4 관리 → 속성 액세스 관리 → 서비스 계정 이메일을 "뷰어" 로 추가
 *   GitHub Variables GA4_PROPERTY_ID   (기본값 546783366)
 *
 * 숫자는 GA4 의 '활성 사용자(사용자)' 기준이며, 오늘 수치는 GA4 처리 지연 때문에 실제보다 늦게 반영될 수 있습니다.
 */
import crypto from "node:crypto";
import { writeFileSync, readFileSync, existsSync } from "node:fs";

const raw = process.env.GA_SERVICE_ACCOUNT || process.env.GSC_SERVICE_ACCOUNT;
const PRESET = process.env.GOOGLE_ACCESS_TOKEN;   // GitHub ↔ 구글 키 없는 인증(Workload Identity)으로 받은 토큰
if (!raw && !PRESET) { console.log("· 구글 인증 설정이 없어 방문자 수 갱신을 건너뜁니다."); process.exit(0); }
process.on("unhandledRejection", (e) => { console.log(`✗ 요청 실패: ${e.message}`); process.exit(0); });

const PROPERTY = process.env.GA4_PROPERTY_ID || "546783366";
const SINCE = process.env.VISITORS_SINCE || "2024-01-01";
const OUT = "assets/visitors.json";

async function getToken() {
if (PRESET) return PRESET;
const sa = JSON.parse(raw);

const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const now = Math.floor(Date.now() / 1000);
const unsigned = b64({ alg: "RS256", typ: "JWT" }) + "." + b64({
  iss: sa.client_email, scope: "https://www.googleapis.com/auth/analytics.readonly",
  aud: "https://oauth2.googleapis.com/token", iat: now, exp: now + 3600,
});
const jwt = unsigned + "." + crypto.sign("RSA-SHA256", Buffer.from(unsigned), sa.private_key).toString("base64url");
const tok = await fetch("https://oauth2.googleapis.com/token", {
  method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: jwt }),
});
if (!tok.ok) { console.log(`✗ 구글 인증 실패 (${tok.status})`); process.exit(0); }
return (await tok.json()).access_token;
}
let access_token;
try { access_token = await getToken(); } catch (e) { console.log(`✗ 구글 인증 실패: ${e.message}`); process.exit(1); }

async function users(startDate, endDate) {
  const res = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${PROPERTY}:runReport`, {
    method: "POST",
    headers: { Authorization: `Bearer ${access_token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ dateRanges: [{ startDate, endDate }], metrics: [{ name: "activeUsers" }, { name: "screenPageViews" }] }),
  });
  if (!res.ok) throw new Error(`${res.status} ${(await res.text()).slice(0, 200)}`);
  const j = await res.json();
  const v = j.rows?.[0]?.metricValues || [];
  return { users: Number(v[0]?.value || 0), views: Number(v[1]?.value || 0) };
}

try {
  const [today, yesterday, total] = await Promise.all([users("today", "today"), users("yesterday", "yesterday"), users(SINCE, "today")]);
  const data = { today: today.users, yesterday: yesterday.users, total: total.users,
                 todayViews: today.views, totalViews: total.views, updated: new Date().toISOString() };
  const prev = existsSync(OUT) ? JSON.parse(readFileSync(OUT, "utf8")) : {};
  const same = ["today", "yesterday", "total", "todayViews", "totalViews"].every((k) => prev[k] === data[k]);
  if (same) { console.log("· 방문자 수 변화 없음"); process.exit(0); }
  writeFileSync(OUT, JSON.stringify(data) + "\n");
  console.log(`✓ 오늘 ${data.today} · 어제 ${data.yesterday} · 전체 ${data.total}`);
} catch (e) {
  process.exitCode = 1;
  console.log(`✗ GA4 조회 실패: ${e.message}`);
  console.log("  GA4 속성 액세스 관리에 서비스 계정을 '뷰어'로 추가했는지, GA4_PROPERTY_ID 가 맞는지 확인하세요.");
}
