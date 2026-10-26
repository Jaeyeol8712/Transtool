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
  const uns = b64({ alg: "RS256", typ: "JWT" }) + "." + b64({ iss: sa.client_email, scope: "https://www.googleapis.com/auth/analytics.readonly https://www.googleapis.com/auth/webmasters.readonly",
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
// ── 일별 (최근 7일) — 중복 = 같은 사람(같은 기기·브라우저)이 여러 번 본·누른 횟수 ──
try {
  const shopPage = { filter: { fieldName: "pagePath", stringFilter: { matchType: "BEGINS_WITH", value: "/shop-" } } };
  const dr = [{ startDate: "6daysAgo", endDate: "today" }];
  const pv = await report({ dateRanges: dr, dimensions: [{ name: "date" }], metrics: [{ name: "screenPageViews" }, { name: "totalUsers" }], dimensionFilter: shopPage, limit: 20 });
  const ck = await report({ dateRanges: dr, dimensions: [{ name: "date" }, { name: "linkId" }], metrics: [{ name: "eventCount" }, { name: "totalUsers" }], dimensionFilter: onlyCta, limit: 2000 });
  const ckDay = await report({ dateRanges: dr, dimensions: [{ name: "date" }], metrics: [{ name: "eventCount" }, { name: "totalUsers" }],
    dimensionFilter: { andGroup: { expressions: [onlyCta, { filter: { fieldName: "linkId", stringFilter: { matchType: "BEGINS_WITH", value: "cta-" } } }] } }, limit: 20 });
  const days = [];
  for (let i = 6; i >= 0; i--) { const d = new Date(Date.now() + 9 * 3600e3 - i * 864e5); days.push(d.toISOString().slice(0, 10).replace(/-/g, "")); }
  const g = (rows, d) => { const r = rows.find((x) => x.dimensionValues[0].value === d); return r ? r.metricValues.map((m) => +m.value) : [0, 0]; };
  const fmt = (d) => `${d.slice(4, 6)}.${d.slice(6)}`;
  out.daily = days.map((d) => { const [v, vu] = g(pv, d), [c, cu] = g(ckDay, d); return { date: d, views: v, viewers: vu, viewDup: Math.max(0, v - vu), clicks: c, clickers: cu, clickDup: Math.max(0, c - cu) }; });
  md += `## 일별 (최근 7일, 추천 모음 글 전체)\n\n| 날짜 | 조회수 | 본 사람 | 중복 조회 | 제휴 클릭 | 누른 사람 | 중복 클릭 |\n|---|---:|---:|---:|---:|---:|---:|\n`;
  for (const x of out.daily) md += `| ${fmt(x.date)} | ${x.views} | ${x.viewers} | ${x.viewDup} | ${x.clicks} | ${x.clickers} | ${x.clickDup} |\n`;
  const sum = (k) => out.daily.reduce((a, x) => a + x[k], 0);
  md += `| **합계** | **${sum("views")}** | ${sum("viewers")}* | ${sum("viewDup")} | **${sum("clicks")}** | ${sum("clickers")}* | ${sum("clickDup")} |\n\n`;
  // 글별 일별 제휴 클릭 (중복 포함 클릭 / 누른 사람)
  const per = {};
  for (const r of ck) { const [d, id] = r.dimensionValues.map((x) => x.value); const m = id.match(/^cta-(.+)-(top|mid|end|pop)$/); if (!m) continue;
    const o = ((per[m[1]] ||= {})[d] ||= [0, 0]); o[0] += +r.metricValues[0].value; o[1] += +r.metricValues[1].value; }
  const pvPost = await report({ dateRanges: dr, dimensions: [{ name: "date" }, { name: "pagePath" }], metrics: [{ name: "screenPageViews" }, { name: "totalUsers" }], dimensionFilter: shopPage, limit: 2000 });
  const vper = {};
  for (const r of pvPost) { const [d, pth] = r.dimensionValues.map((x) => x.value); const k = pth.replace(/^\/shop-|\.html$/g, "");
    const o = ((vper[k] ||= {})[d] ||= [0, 0]); o[0] += +r.metricValues[0].value; o[1] += +r.metricValues[1].value; }
  const posts = [...new Set([...Object.keys(vper), ...Object.keys(per)])].sort((a, b) =>
    Object.values(per[b] || {}).reduce((s, x) => s + x[0], 0) - Object.values(per[a] || {}).reduce((s, x) => s + x[0], 0) ||
    Object.values(vper[b] || {}).reduce((s, x) => s + x[0], 0) - Object.values(vper[a] || {}).reduce((s, x) => s + x[0], 0));
  out.dailyPosts = posts.map((k) => ({ post: k, days: days.map((d) => ({ date: d, views: (vper[k]?.[d] || [0, 0])[0], viewers: (vper[k]?.[d] || [0, 0])[1], clicks: (per[k]?.[d] || [0, 0])[0], clickers: (per[k]?.[d] || [0, 0])[1] })) }));
  md += `### 글별 일별 — 조회(본 사람) / 제휴 클릭(누른 사람)\n\n| 글 | ${days.map(fmt).join(" | ")} |\n|---|${days.map(() => "---:").join("|")}|\n`;
  const cell = (v, u) => (v ? (v > u ? `${v}(${u})` : `${v}`) : "·");
  for (const p of out.dailyPosts) md += `| ${p.post} | ${p.days.map((x) => `${cell(x.views, x.viewers)} / ${cell(x.clicks, x.clickers)}`).join(" | ")} |\n`;
  md += `\n중복 = 같은 사람이 여러 번 본·누른 횟수(횟수 − 사람 수). 괄호 안 숫자는 중복을 뺀 사람 수이며, 괄호가 없으면 중복이 없습니다.\n`;
  md += `*합계의 사람 수는 날짜별 합이라, 여러 날 들어온 같은 사람은 날마다 따로 셉니다.\n\n`;
} catch (e) { md += `## 일별\n\n조회 실패: ${e.message}\n\n`; }

// ── 유입 매체와 오가닉 유입 키워드 (추천 모음 글, 최근 7일) ──
const shopLanding = { filter: { fieldName: "landingPage", stringFilter: { matchType: "BEGINS_WITH", value: "/shop-" } } };
try {
  const src = await report({ dateRanges: [{ startDate: "7daysAgo", endDate: "today" }], dimensions: [{ name: "sessionSourceMedium" }],
    metrics: [{ name: "sessions" }, { name: "engagedSessions" }], dimensionFilter: shopLanding, limit: 50,
    orderBys: [{ metric: { metricName: "sessions" }, desc: true }] });
  out.sources = src.map((r) => ({ source: r.dimensionValues[0].value, sessions: +r.metricValues[0].value, engaged: +r.metricValues[1].value }));
  md += `## 유입 매체 (최근 7일, 추천 모음 글로 들어온 방문)\n\n| 매체 (소스 / 매체) | 방문 | 참여 방문 |\n|---|---:|---:|\n`;
  for (const x of out.sources) md += `| ${x.source} | ${x.sessions} | ${x.engaged} |\n`;
  if (!out.sources.length) md += `| (아직 없음) | 0 | 0 |\n`;
  md += "\n";
} catch (e) { md += `## 유입 매체\n\n조회 실패: ${e.message}\n\n`; }

// 네이버·다음 검색어: 검색 결과 페이지 주소(리퍼러)에 남는 query/q 값
md += `## 오가닉 유입 키워드\n\n`;
try {
  const ref = await report({ dateRanges: [{ startDate: "7daysAgo", endDate: "today" }], dimensions: [{ name: "pageReferrer" }, { name: "landingPage" }],
    metrics: [{ name: "sessions" }], dimensionFilter: { andGroup: { expressions: [shopLanding,
      { filter: { fieldName: "pageReferrer", stringFilter: { matchType: "PARTIAL_REGEXP", value: "search\\.naver\\.com|search\\.daum\\.net|search\\.zum\\.com" } } }] } }, limit: 500 });
  const kw = {};
  for (const r of ref) {
    const [u, lp] = r.dimensionValues.map((d) => d.value); const n = +r.metricValues[0].value;
    let q = ""; let eng = /naver/.test(u) ? "네이버" : /daum/.test(u) ? "다음" : "줌";
    try { const x = new URL(u); q = x.searchParams.get("query") || x.searchParams.get("q") || ""; } catch {}
    const key = `${eng}\t${q || "(검색어 미전달)"}\t${lp.replace(/^\/shop-|\.html$/g, "")}`; kw[key] = (kw[key] || 0) + n;
  }
  out.naverKeywords = Object.entries(kw).map(([k, n]) => { const [eng, q, post] = k.split("\t"); return { engine: eng, query: q, post, sessions: n }; }).sort((a, b) => b.sessions - a.sessions);
  md += `### 네이버·다음 (최근 7일, GA4 리퍼러 기준)\n\n| 검색엔진 | 검색어 | 들어온 글 | 방문 |\n|---|---|---|---:|\n`;
  for (const x of out.naverKeywords.slice(0, 40)) md += `| ${x.engine} | ${x.query} | ${x.post} | ${x.sessions} |\n`;
  if (!out.naverKeywords.length) md += `| - | (아직 없음) | - | 0 |\n`;
  md += "\n";
} catch (e) { md += `네이버·다음 검색어 조회 실패: ${e.message}\n\n`; }

// 구글 검색어: 서치 콘솔 (2~3일 늦게 반영)
try {
  const gtok = process.env.GSC_ACCESS_TOKEN || tok;
  const sites = await (await fetch("https://www.googleapis.com/webmasters/v3/sites", { headers: { Authorization: `Bearer ${gtok}` } })).json();
  const site = (sites.siteEntry || []).map((e) => e.siteUrl).find((u) => /aroundtool\.com/.test(u));
  if (!site) throw new Error("서치 콘솔 속성 접근 권한 없음");
  const end = new Date(Date.now() - 2 * 864e5).toISOString().slice(0, 10), start = new Date(Date.now() - 30 * 864e5).toISOString().slice(0, 10);
  const r = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(site)}/searchAnalytics/query`, {
    method: "POST", headers: { Authorization: `Bearer ${gtok}`, "Content-Type": "application/json" },
    body: JSON.stringify({ startDate: start, endDate: end, dimensions: ["query", "page"], rowLimit: 200,
      dimensionFilterGroups: [{ filters: [{ dimension: "page", operator: "contains", expression: "/shop-" }] }] }) });
  if (!r.ok) throw new Error(`${r.status} ${(await r.text()).slice(0, 200)}`);
  const rows = (await r.json()).rows || [];
  out.googleKeywords = rows.map((x) => ({ query: x.keys[0], post: x.keys[1].replace(/^.*\/shop-|\.html$/g, ""), clicks: x.clicks, impressions: x.impressions, position: +x.position.toFixed(1) }))
    .sort((a, b) => b.clicks - a.clicks || b.impressions - a.impressions);
  md += `### 구글 (${start} ~ ${end}, 서치 콘솔 · 2~3일 늦게 반영)\n\n| 검색어 | 들어온 글 | 클릭 | 노출 | 평균 순위 |\n|---|---|---:|---:|---:|\n`;
  for (const x of out.googleKeywords.slice(0, 40)) md += `| ${x.query} | ${x.post} | ${x.clicks} | ${x.impressions} | ${x.position} |\n`;
  if (!out.googleKeywords.length) md += `| (아직 없음) | - | 0 | 0 | - |\n`;
  md += "\n";
} catch (e) { md += `구글 검색어 조회 실패: ${e.message}\n\n`; }

md += "※ 클릭률 = 제휴 버튼 클릭 ÷ 글 조회수. 실제 구매 수는 네이버 커넥트 관리 화면에서 확인하세요.\n";
md += "※ 중복 판단: GA4는 개인정보 보호로 IP 주소를 저장·제공하지 않아, 같은 기기·브라우저(GA 사용자 식별값)를 같은 사람으로 봅니다. 같은 IP의 다른 기기는 다른 사람으로, 쿠키를 지운 같은 사람은 새 사람으로 셀 수 있습니다.\n";
md += "※ 네이버 검색어는 검색 결과 페이지 주소가 함께 전달될 때만 잡힙니다. 전달되지 않은 방문은 '(검색어 미전달)'로 표시되며, 전체 검색어는 네이버 서치어드바이저 → 리포트 → 검색 유입에서 볼 수 있습니다.\n";
mkdirSync("_cta", { recursive: true });
writeFileSync("_cta/cta-latest.md", md);
writeFileSync("_cta/cta-latest.json", JSON.stringify(out, null, 1));
console.log(md.slice(0, 1500));
