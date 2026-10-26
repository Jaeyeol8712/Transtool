#!/usr/bin/env node
/**
 * 추천 모음 버튼 클릭 보고서 (GA4 이벤트 'cta_click').
 * 버튼 이름(link_id): cta-<글>-top/mid/end/pop (제휴 버튼), hub-<글> (목록 '자세히 보기'), promo-<글> (다른 페이지 추천 카드)
 * 결과: _cta/cta-latest.md, _cta/cta-latest.json  → 워크플로가 cta-report 브랜치에 저장
 * 인증은 ga4-visitors.mjs 와 같음 (GOOGLE_ACCESS_TOKEN 또는 서비스 계정 JSON, GA4 '뷰어' 권한이면 충분)
 */
import crypto from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";

const raw = process.env.GA_SERVICE_ACCOUNT || process.env.GSC_SERVICE_ACCOUNT;
const PRESET = process.env.GOOGLE_ACCESS_TOKEN;
const PROPERTY = process.env.GA4_PROPERTY_ID || "546783366";
if (!raw && !PRESET) { console.log("· 구글 인증 설정이 없어 건너뜁니다."); process.exit(0); }

async function token() {
  if (PRESET) return PRESET;
  const sa = JSON.parse(raw);
  const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
  const now = Math.floor(Date.now() / 1000);
  const uns = b64({ alg: "RS256", typ: "JWT" }) + "." + b64({ iss: sa.client_email, scope: "https://www.googleapis.com/auth/analytics.readonly",
    aud: "https://oauth2.googleapis.com/token", iat: now, exp: now + 3600 });
  const jwt = uns + "." + crypto.sign("RSA-SHA256", Buffer.from(uns), sa.private_key).toString("base64url");
  const r = await fetch("https://oauth2.googleapis.com/token", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: jwt }) });
  return (await r.json()).access_token;
}
const tok = await token();
async function report(body) {
  const r = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${PROPERTY}:runReport`, {
    method: "POST", headers: { Authorization: `Bearer ${tok}`, "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!r.ok) throw new Error(`${r.status} ${(await r.text()).slice(0, 300)}`);
  return (await r.json()).rows || [];
}
const onlyCta = { filter: { fieldName: "eventName", stringFilter: { value: "cta_click" } } };
const POS = { top: "첫 버튼", mid: "중간 버튼", end: "글 끝 버튼", pop: "팝업" };
function parse(id) {
  let m = id.match(/^cta-(.+)-(top|mid|end|pop)$/); if (m) return { post: m[1], pos: m[2], type: "제휴" };
  m = id.match(/^(hub|promo)-(.+)$/); if (m) return { post: m[2], pos: m[1], type: "글로 이동" };
  return { post: id, pos: "", type: "기타" };
}

const out = { updated: new Date().toISOString(), ranges: {} };
let md = `# 추천 모음 버튼 클릭 보고서\n\n갱신: ${out.updated.slice(0, 16).replace("T", " ")} (UTC) · GA4 이벤트 \`cta_click\`\n\n`;
for (const [label, start] of [["최근 7일", "7daysAgo"], ["최근 28일", "28daysAgo"]]) {
  const rows = await report({ dateRanges: [{ startDate: start, endDate: "today" }], dimensions: [{ name: "linkId" }],
    metrics: [{ name: "eventCount" }, { name: "totalUsers" }], dimensionFilter: onlyCta, limit: 500 });
  const views = await report({ dateRanges: [{ startDate: start, endDate: "today" }], dimensions: [{ name: "pagePath" }],
    metrics: [{ name: "screenPageViews" }], dimensionFilter: { filter: { fieldName: "pagePath", stringFilter: { matchType: "BEGINS_WITH", value: "/shop-" } } }, limit: 200 });
  const pv = Object.fromEntries(views.map((r) => [r.dimensionValues[0].value.replace(/^\/shop-|\.html$/g, ""), +r.metricValues[0].value]));
  const btn = rows.map((r) => ({ id: r.dimensionValues[0].value, clicks: +r.metricValues[0].value, users: +r.metricValues[1].value, ...parse(r.dimensionValues[0].value) }))
    .filter((x) => x.id && x.id !== "(not set)").sort((a, b) => b.clicks - a.clicks);
  const per = {};
  for (const b of btn) { const p = (per[b.post] ||= { post: b.post, affiliate: 0, internal: 0, top: 0, mid: 0, end: 0, pop: 0 });
    if (b.type === "제휴") { p.affiliate += b.clicks; p[b.pos] += b.clicks; } else p.internal += b.clicks; }
  for (const k of Object.keys(pv)) per[k] ||= { post: k, affiliate: 0, internal: 0, top: 0, mid: 0, end: 0, pop: 0 };
  const posts = Object.values(per).map((p) => ({ ...p, views: pv[p.post] || 0, ctr: pv[p.post] ? +(p.affiliate / pv[p.post] * 100).toFixed(1) : null }))
    .sort((a, b) => b.affiliate - a.affiliate || b.views - a.views);
  out.ranges[label] = { buttons: btn, posts };
  const tot = btn.filter((b) => b.type === "제휴").reduce((s, b) => s + b.clicks, 0);
  md += `## ${label} — 제휴 버튼 클릭 ${tot}회\n\n### 글별\n\n| 글 | 조회수 | 제휴 클릭 | 클릭률 | 첫 버튼 | 중간 | 글 끝 | 팝업 | 목록·카드에서 들어옴 |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n`;
  for (const p of posts) md += `| ${p.post} | ${p.views} | ${p.affiliate} | ${p.ctr == null ? "-" : p.ctr + "%"} | ${p.top} | ${p.mid} | ${p.end} | ${p.pop} | ${p.internal} |\n`;
  md += `\n### 버튼별 (상위 40)\n\n| 버튼 이름 | 종류 | 위치 | 클릭 | 클릭한 사람 |\n|---|---|---|---:|---:|\n`;
  for (const b of btn.slice(0, 40)) md += `| \`${b.id}\` | ${b.type} | ${POS[b.pos] || b.pos} | ${b.clicks} | ${b.users} |\n`;
  md += "\n";
}
md += "※ 클릭률 = 제휴 버튼 클릭 ÷ 글 조회수. 실제 구매 수는 네이버 커넥트 관리 화면에서 확인하세요.\n";
mkdirSync("_cta", { recursive: true });
writeFileSync("_cta/cta-latest.md", md);
writeFileSync("_cta/cta-latest.json", JSON.stringify(out, null, 1));
console.log(md.slice(0, 1500));
