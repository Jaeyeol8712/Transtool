#!/usr/bin/env node
/**
 * 추천 모음 성과 보고서 (시각형 HTML) — 일간·주간·월간·분기·연간
 *
 *   node scripts/ga4-report.mjs                 오늘(한국 날짜) 기준으로 보낼 보고서를 자동 판단
 *   node scripts/ga4-report.mjs --type weekly   특정 보고서만
 *   node scripts/ga4-report.mjs --mock          GA 없이 가짜 숫자로 화면 확인
 *
 * 자동 판단 (매일 08:13 실행)
 *   일간  매일      — 어제 + 최근 3일 비교 + 최근 7일 추이
 *   주간  수요일    — 지난주 월~일 + 최근 4주
 *   월간  매월 3일  — 지난달 1일~말일 + 최근 4주·최근 3개월 누적
 *   분기  1·4·7·10월 3일 — 지난 분기 + 직전 분기 비교
 *   연간  1월 3일   — 지난해 1~12월
 * 결과: _cta/reports/<종류>-<기간>.html, _cta/today.json (오늘 만든 보고서 목록), _cta/cta-latest.md (요약)
 *
 * 숫자 기준: GA4. '본 사람·누른 사람' = 같은 기기·브라우저를 한 사람으로 센 값, '중복' = 횟수 − 사람 수.
 * (GA4는 IP 주소를 제공하지 않습니다.) 버튼 클릭은 site.js 의 'cta_click' 이벤트(link_id = cta-<글>-top|mid|end|pop).
 */
import crypto from "node:crypto";
import { mkdirSync, writeFileSync, readFileSync, existsSync } from "node:fs";

const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const MOCK = args.includes("--mock");
const PROPERTY = process.env.GA4_PROPERTY_ID || "546783366";
const TITLES = existsSync("_cta/titles.json") ? JSON.parse(readFileSync("_cta/titles.json", "utf8")) : {};
const title = (slug) => TITLES[slug] || slug;

// ───────── 날짜 (한국 시간) ─────────
const kstToday = () => { const d = new Date(Date.now() + 9 * 3600e3); return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate())); };
const TODAY = opt("--date") ? new Date(opt("--date") + "T00:00:00Z") : kstToday();
const iso = (d) => d.toISOString().slice(0, 10);
const add = (d, n) => new Date(d.getTime() + n * 864e5);
const ymd = (d) => iso(d).replace(/-/g, "");
const md_ = (d) => `${d.getUTCMonth() + 1}.${d.getUTCDate()}`;
const DOW = ["일", "월", "화", "수", "목", "금", "토"];
const monthStart = (y, m) => new Date(Date.UTC(y, m, 1));
const monthEnd = (y, m) => new Date(Date.UTC(y, m + 1, 0));

// ───────── GA4 / 서치 콘솔 ─────────
let TOKEN = null;
const ERRORS = [];
async function token() {
  if (TOKEN) return TOKEN;
  if (process.env.GOOGLE_ACCESS_TOKEN) return (TOKEN = process.env.GOOGLE_ACCESS_TOKEN);
  const raw = process.env.GA_SERVICE_ACCOUNT || process.env.GSC_SERVICE_ACCOUNT;
  if (!raw) throw new Error("구글 인증 설정 없음");
  const sa = JSON.parse(raw);
  const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
  const now = Math.floor(Date.now() / 1000);
  const uns = b64({ alg: "RS256", typ: "JWT" }) + "." + b64({ iss: sa.client_email,
    scope: "https://www.googleapis.com/auth/analytics.readonly https://www.googleapis.com/auth/webmasters.readonly",
    aud: "https://oauth2.googleapis.com/token", iat: now, exp: now + 3600 });
  const jwt = uns + "." + crypto.sign("RSA-SHA256", Buffer.from(uns), sa.private_key).toString("base64url");
  const r = await fetch("https://oauth2.googleapis.com/token", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: jwt }) });
  return (TOKEN = (await r.json()).access_token);
}
async function ga(start, end, dims, mets, filter, limit = 5000) {
  const body = { dateRanges: [{ startDate: iso(start), endDate: iso(end) }], dimensions: dims.map((name) => ({ name })),
    metrics: mets.map((name) => ({ name })), limit };
  if (filter) body.dimensionFilter = filter;
  let r;
  for (let attempt = 0; attempt < 5; attempt++) {   // 동시 요청 한도(429)면 잠시 쉬었다 다시
    r = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${PROPERTY}:runReport`, {
      method: "POST", headers: { Authorization: `Bearer ${await token()}`, "Content-Type": "application/json" }, body: JSON.stringify(body) });
    if (r.status !== 429) break;
    await new Promise((ok) => setTimeout(ok, 1500 * (attempt + 1)));
  }
  if (!r.ok) throw new Error(`GA4 ${r.status} ${(await r.text()).slice(0, 160)}`);
  return ((await r.json()).rows || []).map((x) => ({ d: (x.dimensionValues || []).map((v) => v.value), m: (x.metricValues || []).map((v) => +v.value) }));
}
const F = {
  shop: { filter: { fieldName: "pagePath", stringFilter: { matchType: "BEGINS_WITH", value: "/shop-" } } },
  land: { filter: { fieldName: "landingPage", stringFilter: { matchType: "BEGINS_WITH", value: "/shop-" } } },
  cta: { andGroup: { expressions: [{ filter: { fieldName: "eventName", stringFilter: { value: "cta_click" } } },
    { filter: { fieldName: "linkId", stringFilter: { matchType: "BEGINS_WITH", value: "cta-" } } }] } },
  anyCta: { filter: { fieldName: "eventName", stringFilter: { value: "cta_click" } } },
};
const slugOf = (p) => p.replace(/^\/shop-|\.html$|\?.*$/g, "");

// 기간 하나의 숫자 모음
async function collect(start, end, bucket) {
  if (MOCK) return mock(start, end, bucket);
  const bdim = { day: "date", week: "isoYearIsoWeek", month: "yearMonth" }[bucket];
  const jobs = [
    () => ga(start, end, [], ["screenPageViews", "totalUsers"], F.shop),
    () => ga(start, end, [], ["eventCount", "totalUsers"], F.cta),
    () => ga(start, end, [bdim], ["screenPageViews", "totalUsers"], F.shop),
    () => ga(start, end, [bdim], ["eventCount", "totalUsers"], F.cta),
    () => ga(start, end, ["pagePath"], ["screenPageViews", "totalUsers"], F.shop),
    () => ga(start, end, ["linkId"], ["eventCount", "totalUsers"], F.anyCta),
    () => ga(start, end, ["sessionSourceMedium"], ["sessions", "totalUsers"], F.land, 50),
    () => ga(start, end, ["pageReferrer", "landingPage"], ["sessions"], { andGroup: { expressions: [F.land,
      { filter: { fieldName: "pageReferrer", stringFilter: { matchType: "PARTIAL_REGEXP", value: "search\\.naver\\.com|search\\.daum\\.net|search\\.zum\\.com" } } }] } }, 1000),
  ];
  const settled = [];
  for (const job of jobs) { try { settled.push({ status: "fulfilled", value: await job() }); } catch (e) { settled.push({ status: "rejected", reason: e }); } }
  try {
    const rows = await ga(start, end, ["sessionDefaultChannelGroup", "sessionSourceMedium", "searchTerm", "landingPage", "linkId"], ["eventCount", "totalUsers"], F.cta, 2000);
    var clickSrc = rows.map((r) => { const m = r.d[4].match(/^cta-(.+)-(top|mid|end|pop)$/) || [];
      return { channel: r.d[0], source: r.d[1], keyword: r.d[2], landing: r.d[3], post: m[1] || r.d[4], pos: m[2] || "", clicks: r.m[0], users: r.m[1] }; });
  } catch (e) { ERRORS.push(`버튼 누른 사람 유입: ${e.message}`); var clickSrc = []; }
  const NAMES = ["합계 조회", "합계 클릭", "기간별 조회", "기간별 클릭", "글별 조회", "버튼별 클릭", "유입 매체", "검색어"];
  const [tv, tc, sv, sc, pv, pc, src, ref] = settled.map((x, i) => { if (x.status === "fulfilled") return x.value; ERRORS.push(`${NAMES[i]}: ${x.reason.message}`); return []; });
  const tot = { views: tv[0]?.m[0] || 0, viewers: tv[0]?.m[1] || 0, clicks: tc[0]?.m[0] || 0, clickers: tc[0]?.m[1] || 0 };
  const series = {};
  for (const r of sv) (series[r.d[0]] ||= blank()).views = r.m[0], series[r.d[0]].viewers = r.m[1];
  for (const r of sc) (series[r.d[0]] ||= blank()).clicks = r.m[0], series[r.d[0]].clickers = r.m[1];
  const posts = {};
  for (const r of pv) { const p = (posts[slugOf(r.d[0])] ||= postBlank()); p.views += r.m[0]; p.viewers += r.m[1]; }
  for (const r of pc) {
    let m = r.d[0].match(/^cta-(.+)-(top|mid|end|pop)$/);
    if (m) { const p = (posts[m[1]] ||= postBlank()); p.clicks += r.m[0]; p.clickers += r.m[1]; p.pos[m[2]] += r.m[0]; continue; }
    m = r.d[0].match(/^(hub|promo)-(.+)$/);
    if (m) { const p = (posts[m[2]] ||= postBlank()); p.inbound[m[1]] += r.m[0]; }
  }
  const sources = src.map((r) => ({ name: r.d[0], sessions: r.m[0], users: r.m[1] }));
  const kw = {};
  for (const r of ref) {
    let q = "", eng = /naver/.test(r.d[0]) ? "네이버" : /daum/.test(r.d[0]) ? "다음" : "줌";
    try { const u = new URL(r.d[0]); q = u.searchParams.get("query") || u.searchParams.get("q") || ""; } catch {}
    const k = `${eng}\t${q || "(검색어 미전달)"}\t${slugOf(r.d[1])}`; kw[k] = (kw[k] || 0) + r.m[0];
  }
  const keywords = Object.entries(kw).map(([k, n]) => { const [engine, query, post] = k.split("\t"); return { engine, query, post, sessions: n }; })
    .sort((a, b) => b.sessions - a.sessions);
  return { tot, series, posts, sources, keywords, clickSrc, google: await gsc(start, end) };
}
async function seq(fns) { const out = []; for (const f of fns) out.push(await f()); return out; }
const blank = () => ({ views: 0, viewers: 0, clicks: 0, clickers: 0 });
const postBlank = () => ({ views: 0, viewers: 0, clicks: 0, clickers: 0, pos: { top: 0, mid: 0, end: 0, pop: 0 }, inbound: { hub: 0, promo: 0 } });

async function gsc(start, end) {
  try {
    const last = add(kstToday(), -3); if (start > last) return { rows: [], note: "구글 검색 데이터는 2~3일 늦게 들어와 이 기간은 아직 없습니다." };
    const e = end > last ? last : end;
    const t = await token();
    const sites = await (await fetch("https://www.googleapis.com/webmasters/v3/sites", { headers: { Authorization: `Bearer ${t}` } })).json();
    const site = (sites.siteEntry || []).map((x) => x.siteUrl).find((u) => /aroundtool\.com/.test(u));
    if (!site) return { rows: [], note: "서치 콘솔 접근 권한이 없습니다." };
    const r = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(site)}/searchAnalytics/query`, {
      method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" },
      body: JSON.stringify({ startDate: iso(start), endDate: iso(e), dimensions: ["query", "page"], rowLimit: 100,
        dimensionFilterGroups: [{ filters: [{ dimension: "page", operator: "contains", expression: "/shop-" }] }] }) });
    const rows = ((await r.json()).rows || []).map((x) => ({ query: x.keys[0], post: slugOf(new URL(x.keys[1]).pathname), clicks: x.clicks, impressions: x.impressions, position: x.position }));
    return { rows: rows.sort((a, b) => b.clicks - a.clicks || b.impressions - a.impressions), note: `${iso(start)} ~ ${iso(e)} 서치 콘솔 기준` };
  } catch (err) { return { rows: [], note: `구글 검색어 조회 실패: ${err.message}` }; }
}

// ───────── 가짜 데이터 (화면 확인용) ─────────
function mock(start, end, bucket) {
  const r = (n) => Math.floor(Math.random() * n);
  const series = {};
  for (let d = start; d <= end; d = add(d, 1)) {
    const k = bucket === "day" ? ymd(d) : bucket === "month" ? ymd(d).slice(0, 6) : `${d.getUTCFullYear()}${String(Math.ceil((d - Date.UTC(d.getUTCFullYear(), 0, 1)) / 864e5 / 7) + 1).padStart(2, "0")}`;
    const s = (series[k] ||= blank()); const v = 20 + r(60); s.views += v; s.viewers += Math.ceil(v * 0.4); s.clicks += r(8); s.clickers += r(5);
  }
  const posts = {};
  for (const k of Object.keys(TITLES).slice(0, 17)) { const v = r(80); posts[k] = { views: v, viewers: Math.ceil(v * 0.5), clicks: r(10), clickers: r(6), pos: { top: r(5), mid: r(3), end: r(2), pop: r(4) }, inbound: { hub: r(5), promo: r(5) } }; }
  const tot = Object.values(series).reduce((a, s) => ({ views: a.views + s.views, viewers: a.viewers + s.viewers, clicks: a.clicks + s.clicks, clickers: a.clickers + s.clickers }), blank());
  return { tot, series, posts, sources: [{ name: "naver / organic", sessions: 30, users: 22 }, { name: "daum / organic", sessions: 12, users: 10 }, { name: "(direct) / (none)", sessions: 9, users: 4 }, { name: "google / organic", sessions: 5, users: 5 }],
    keywords: [{ engine: "다음", query: "로봇청소기 추천", post: "bespoke-ai-steam-ultra", sessions: 3 }, { engine: "네이버", query: "(검색어 미전달)", post: "galaxy-s26-ultra", sessions: 6 }],
    clickSrc: [{ channel: "Organic Search", source: "naver / organic", keyword: "갤럭시 s26 울트라 자급제", landing: "/shop-galaxy-s26-ultra.html", post: "galaxy-s26-ultra", pos: "top", clicks: 4, users: 3 },
      { channel: "Organic Search", source: "daum / organic", keyword: "로봇청소기 추천", landing: "/shop-bespoke-ai-steam-ultra.html", post: "bespoke-ai-steam-ultra", pos: "pop", clicks: 2, users: 2 },
      { channel: "Organic Search", source: "google / organic", keyword: "(검색어 미전달)", landing: "/shop-c-type-65w-charger.html", post: "c-type-65w-charger", pos: "mid", clicks: 1, users: 1 },
      { channel: "Direct", source: "(direct) / (none)", keyword: "(직접·내부)", landing: "/index.html", post: "jbl-authentics-200", pos: "top", clicks: 2, users: 1 }],
    google: { rows: [{ query: "65w 충전기", post: "c-type-65w-charger", clicks: 2, impressions: 40, position: 8.2 }], note: "가짜 데이터" } };
}

// ───────── 그림 (SVG) ─────────
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const n = (x) => Math.round(x).toLocaleString("ko-KR");
const pct = (a, b) => (b ? `${(a / b * 100).toFixed(1)}%` : "–");
function niceMax(v) { if (v <= 5) return 5; const p = 10 ** Math.floor(Math.log10(v)); const m = v / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 5 ? 5 : 10) * p; }

/** 세로 막대 (사람 수 + 중복 쌓기). items: [{label, people, dup, tip}] */
function columns(items, cls, unit) {
  const W = 640, H = 220, L = 34, B = 30, T = 18, R = 6;
  const max = niceMax(Math.max(1, ...items.map((i) => i.people + i.dup)));
  const slot = (W - L - R) / items.length, bw = Math.min(24, slot * 0.6);
  const y = (v) => T + (H - T - B) * (1 - v / max);
  let g = "";
  for (let k = 0; k <= 4; k++) { const v = max * k / 4, yy = y(v); g += `<line x1="${L}" x2="${W - R}" y1="${yy}" y2="${yy}" class="grid"/><text x="${L - 6}" y="${yy + 4}" class="tick" text-anchor="end">${v >= 1000 ? (v / 1000).toFixed(v % 1000 ? 1 : 0) + "K" : n(v)}</text>`; }
  items.forEach((it, i) => {
    const cx = L + slot * i + slot / 2, x = cx - bw / 2, tot = it.people + it.dup;
    const yp = y(it.people), yt = y(tot);
    const tip = esc(it.tip || `${it.label}: ${n(tot)}${unit} (사람 ${n(it.people)}, 중복 ${n(it.dup)})`);
    if (it.people > 0) g += `<path class="${cls}" d="${bar(x, yp, bw, y(0) - yp, it.dup > 0 ? 0 : 4)}"/>`;
    if (it.dup > 0) g += `<path class="${cls} dup" d="${bar(x, yt, bw, Math.max(0, yp - yt - (it.people > 0 ? 2 : 0)), 4)}"/>`;
    g += `<rect x="${cx - slot / 2}" y="${T}" width="${slot}" height="${H - T - B}" fill="transparent" data-tip="${tip}"/>`;
    if (items.length <= 14 && tot > 0) g += `<text x="${cx}" y="${yt - 5}" class="val" text-anchor="middle">${n(tot)}</text>`;
    const every = items.length > 14 ? Math.ceil(items.length / 8) : 1;
    if (i % every === 0 || i === items.length - 1) g += `<text x="${cx}" y="${H - 10}" class="tick" text-anchor="middle">${esc(it.label)}</text>`;
  });
  return `<svg viewBox="0 0 ${W} ${H}" class="chart" role="img">${g}<line x1="${L}" x2="${W - R}" y1="${y(0)}" y2="${y(0)}" class="axis"/></svg>`;
}
function bar(x, y, w, h, r) {   // 위쪽만 둥근 막대
  if (h <= 0) return "";
  r = Math.min(r, w / 2, h);
  return `M${x},${y + h}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h}Z`;
}
/** 가로 막대 표. rows: [{label, value, note}] */
function hbars(rows, cls, unit = "") {
  const max = Math.max(1, ...rows.map((r) => r.value));
  return `<div class="hb">${rows.map((r) => `<div class="hb-row" data-tip="${esc(`${r.label}: ${n(r.value)}${unit}${r.note ? " · " + r.note : ""}`)}">
    <span class="hb-l">${esc(r.label)}</span><span class="hb-t"><i class="${cls}" style="width:${(r.value / max * 100).toFixed(1)}%"></i></span>
    <span class="hb-v">${n(r.value)}${unit}${r.note ? `<small>${esc(r.note)}</small>` : ""}</span></div>`).join("")}</div>`;
}
function delta(cur, prev) {
  if (prev === undefined || prev === null) return "";
  if (!prev && !cur) return `<span class="dl">변화 없음</span>`;
  if (!prev) return `<span class="dl up">▲ 새로 생김</span>`;
  const d = (cur - prev) / prev * 100;
  return `<span class="dl ${d > 0 ? "up" : d < 0 ? "down" : ""}">${d > 0 ? "▲" : d < 0 ? "▼" : "–"} ${Math.abs(d).toFixed(0)}% <small>(이전 ${n(prev)})</small></span>`;
}
function kpis(cur, prev) {
  const c = cur.tot, p = prev?.tot;
  const card = (lab, v, pv, sub) => `<div class="kpi"><p>${lab}</p><b>${v}</b>${sub ? `<em>${sub}</em>` : ""}${pv}</div>`;
  return `<div class="kpis">
    ${card("글 조회수", n(c.views), delta(c.views, p?.views), `본 사람 ${n(c.viewers)} · 중복 ${n(Math.max(0, c.views - c.viewers))}`)}
    ${card("브랜드커넥트 버튼 클릭", n(c.clicks), delta(c.clicks, p?.clicks), `누른 사람 ${n(c.clickers)} · 중복 ${n(Math.max(0, c.clicks - c.clickers))}`)}
    ${card("클릭률", pct(c.clicks, c.views), p ? `<span class="dl">이전 ${pct(p.clicks, p.views)}</span>` : "", "클릭 ÷ 조회수")}
    ${card("사람 기준 클릭률", pct(c.clickers, c.viewers), p ? `<span class="dl">이전 ${pct(p.clickers, p.viewers)}</span>` : "", "누른 사람 ÷ 본 사람")}
  </div>`;
}
function legend(cls) {
  return `<p class="lg"><span><i class="${cls}"></i>사람 수(중복 제외)</span><span><i class="${cls} dup"></i>중복(같은 사람의 반복)</span></p>`;
}
function trend(buckets, data, labelFn, titleTxt) {
  const v = buckets.map((k) => ({ label: labelFn(k), people: data.series[k]?.viewers || 0, dup: Math.max(0, (data.series[k]?.views || 0) - (data.series[k]?.viewers || 0)) }));
  const c = buckets.map((k) => ({ label: labelFn(k), people: data.series[k]?.clickers || 0, dup: Math.max(0, (data.series[k]?.clicks || 0) - (data.series[k]?.clickers || 0)) }));
  return `<section class="card"><h2>${titleTxt}</h2>
    <div class="two"><div><h3>글 조회수</h3>${legend("s1")}${columns(v, "s1", "회")}</div>
    <div><h3>브랜드커넥트 버튼 클릭</h3>${legend("s2")}${columns(c, "s2", "회")}</div></div>
    ${table(["기간", "조회수", "본 사람", "중복 조회", "BC 버튼 클릭", "누른 사람", "중복 클릭", "클릭률"], buckets.map((k) => {
      const s = data.series[k] || blank(); return [labelFn(k), n(s.views), n(s.viewers), n(Math.max(0, s.views - s.viewers)), n(s.clicks), n(s.clickers), n(Math.max(0, s.clicks - s.clickers)), pct(s.clicks, s.views)]; }), true)}
  </section>`;
}
function table(head, rows, numeric) {
  return `<div class="tw" tabindex="0"><table><thead><tr>${head.map((h) => `<th>${h}</th>`).join("")}</tr></thead><tbody>${rows.map((r) =>
    `<tr>${r.map((c, i) => `<td${numeric && i ? ' class="r"' : ""}>${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}
function postsSection(data, label) {
  const ps = Object.entries(data.posts).map(([k, p]) => ({ k, ...p })).sort((a, b) => b.clicks - a.clicks || b.views - a.views);
  const top = ps.filter((p) => p.views || p.clicks).slice(0, 12);
  const posTot = ps.reduce((a, p) => { for (const k in a) a[k] += p.pos[k]; return a; }, { top: 0, mid: 0, end: 0, pop: 0 });
  const POS = { top: "첫 버튼(사진 아래)", mid: "중간 버튼", end: "글 끝 버튼", pop: "3초 팝업" };
  return `<section class="card"><h2>글별 성과 · ${label}</h2>
    <div class="two"><div><h3>조회수 상위 (본 사람 기준 중복 표시)</h3>${hbars(top.slice().sort((a, b) => b.views - a.views).map((p) => ({ label: title(p.k), value: p.views, note: `본 사람 ${n(p.viewers)}${p.views > p.viewers ? ` · 중복 ${n(p.views - p.viewers)}` : ""}` })), "s1", "회")}</div>
    <div><h3>브랜드커넥트 버튼 클릭 상위</h3>${top.some((p) => p.clicks) ? hbars(top.filter((p) => p.clicks).map((p) => ({ label: title(p.k), value: p.clicks, note: `누른 사람 ${n(p.clickers)} · 클릭률 ${pct(p.clicks, p.views)}` })), "s2", "회") : `<p class="empty">아직 클릭이 없습니다.</p>`}
    <h3 style="margin-top:1.2rem">어느 버튼이 눌렸나</h3>${hbars(Object.entries(POS).map(([k, l]) => ({ label: l, value: posTot[k] })), "s2", "회")}</div></div>
    ${table(["글", "조회수", "본 사람", "중복", "BC 버튼 클릭", "누른 사람", "클릭률", "첫 버튼", "중간", "글 끝", "팝업", "목록·카드로 들어옴"],
      ps.filter((p) => p.views || p.clicks).map((p) => [esc(title(p.k)), n(p.views), n(p.viewers), n(Math.max(0, p.views - p.viewers)), n(p.clicks), n(p.clickers), pct(p.clicks, p.views), n(p.pos.top), n(p.pos.mid), n(p.pos.end), n(p.pos.pop), n(p.inbound.hub + p.inbound.promo)]), true)}
  </section>`;
}
const CH = { "Organic Search": "검색(오가닉)", "Direct": "직접 방문", "Referral": "다른 사이트 링크", "Organic Social": "SNS", "Paid Search": "검색 광고",
  "Paid Social": "SNS 광고", "Display": "배너 광고", "Unassigned": "분류 안 됨", "Email": "이메일", "Organic Shopping": "쇼핑 검색", "Organic Video": "동영상" };
const POSK = { top: "첫 버튼", mid: "중간", end: "글 끝", pop: "팝업" };
function clickersSection(data, label) {
  const rows = (data.clickSrc || []).filter((r) => r.clicks).sort((a, b) => b.clicks - a.clicks);
  if (!rows.length) return `<section class="card main"><h2>★ 브랜드커넥트 버튼을 누른 사람은 어디서 왔나 · ${label}</h2>
    <p class="empty">이 기간에는 브랜드커넥트 버튼 클릭이 없습니다. 클릭이 생기면 채널·검색어·들어온 글이 여기에 나옵니다.</p></section>`;
  const sum = (key) => { const o = {}; for (const r of rows) { const k = key(r); o[k] ||= { clicks: 0, users: 0 }; o[k].clicks += r.clicks; o[k].users += r.users; } return Object.entries(o).sort((a, b) => b[1].clicks - a[1].clicks); };
  const total = rows.reduce((a, r) => a + r.clicks, 0);
  const ch = sum((r) => CH[r.channel] || r.channel), src = sum((r) => r.source);
  const kw = sum((r) => `${r.keyword}\t${r.source}`).filter(([k]) => !/^\(직접·내부\)|^\(not set\)/.test(k));
  const gq = (post) => (data.google.rows || []).filter((g) => g.post === post).slice(0, 3).map((g) => g.query).join(", ");
  return `<section class="card main"><h2>★ 브랜드커넥트 버튼을 누른 사람은 어디서 왔나 · ${label}</h2>
    <p class="note" style="margin:0 0 .8rem">‘제품 가격 알아보기·여행 비용 알아보기’ 버튼(브랜드 커넥트로 이동)을 누른 방문이 처음에 어떤 채널·검색어로 사이트에 들어왔는지입니다. 총 ${n(total)}회.</p>
    <div class="two"><div><h3>채널</h3>${hbars(ch.map(([k, v]) => ({ label: k, value: v.clicks, note: `${pct(v.clicks, total)} · 누른 사람 ${n(v.users)}` })), "s2", "회")}
      <h3 style="margin-top:1rem">소스 / 매체</h3>${hbars(src.slice(0, 8).map(([k, v]) => ({ label: k, value: v.clicks, note: `누른 사람 ${n(v.users)}` })), "s2", "회")}</div>
    <div><h3>검색 키워드</h3>${kw.length ? hbars(kw.slice(0, 10).map(([k, v]) => { const [q, s2] = k.split("\t"); return { label: q, value: v.clicks, note: `${s2} · 누른 사람 ${n(v.users)}` }; }), "s2", "회") : `<p class="empty">검색으로 들어와 누른 클릭이 없습니다.</p>`}
      <p class="note">네이버는 검색어를 넘기지 않는 경우가 많아 ‘(검색어 미전달)’로, 구글은 검색어를 넘기지 않아 아래 표에 서치 콘솔의 그 글 검색어를 ‘구글 추정’으로 붙였습니다.</p></div></div>
    ${table(["채널", "소스 / 매체", "검색어", "처음 들어온 페이지", "누른 글", "버튼", "클릭", "누른 사람"], rows.slice(0, 40).map((r) => [
      esc(CH[r.channel] || r.channel), esc(r.source), esc(/google/.test(r.source) && /미전달/.test(r.keyword) && gq(r.post) ? `구글 추정: ${gq(r.post)}` : r.keyword),
      esc(r.landing.startsWith("/shop-") ? title(slugOf(r.landing)) : r.landing), esc(title(r.post)), POSK[r.pos] || r.pos, n(r.clicks), n(r.users)]), false)}
  </section>`;
}
function sourcesSection(data, label) {
  const total = data.sources.reduce((a, s) => a + s.sessions, 0);
  const g = data.google;
  return `<section class="card"><h2>글을 본 사람의 유입 매체 · ${label}</h2>
    ${data.sources.length ? hbars(data.sources.slice(0, 10).map((s) => ({ label: s.name, value: s.sessions, note: `${pct(s.sessions, total)} · 사람 ${n(s.users)}` })), "s1", "회") : `<p class="empty">추천 글로 들어온 방문이 없습니다.</p>`}
    <p class="note">방문 = 추천 글로 처음 들어온 방문(세션). organic = 검색, referral = 다른 사이트 링크, (direct) = 주소 직접 입력·앱 등.</p>
  </section>
  <section class="card"><h2>오가닉 유입 키워드 · ${label}</h2>
    <div class="two"><div><h3>네이버·다음 검색어</h3>${data.keywords.length ? table(["검색엔진", "검색어", "들어온 글", "방문"], data.keywords.slice(0, 25).map((k) => [k.engine, esc(k.query), esc(title(k.post)), n(k.sessions)]), false)
      : `<p class="empty">이 기간 네이버·다음 검색 유입이 없습니다.</p>`}
      <p class="note">네이버는 검색어를 보내지 않는 경우가 많아 '(검색어 미전달)'로 표시됩니다. 전체 검색어는 네이버 서치어드바이저 → 리포트 → 검색 유입에서 볼 수 있습니다.</p></div>
    <div><h3>구글 검색어</h3>${g.rows.length ? table(["검색어", "들어온 글", "클릭", "노출", "평균 순위"], g.rows.slice(0, 25).map((x) => [esc(x.query), esc(title(x.post)), n(x.clicks), n(x.impressions), x.position.toFixed(1)]), false)
      : `<p class="empty">이 기간 구글 검색 노출이 없습니다.</p>`}<p class="note">${esc(g.note || "")}</p></div></div>
  </section>`;
}

// ───────── 보고서 종류 ─────────
const days = (s, e) => { const a = []; for (let d = s; d <= e; d = add(d, 1)) a.push(d); return a; };
const dayLabel = (k) => { const d = new Date(`${k.slice(0, 4)}-${k.slice(4, 6)}-${k.slice(6)}T00:00:00Z`); return `${md_(d)}(${DOW[d.getUTCDay()]})`; };
const weekLabel = (k) => `${+k.slice(4)}주`;
const monLabel = (k) => `${+k.slice(4)}월`;
function isoWeekKey(d) { const t = new Date(d); const day = (t.getUTCDay() + 6) % 7; t.setUTCDate(t.getUTCDate() - day + 3);
  const y = t.getUTCFullYear(), w = 1 + Math.round(((t - Date.UTC(y, 0, 4)) / 864e5 - 3 + ((new Date(Date.UTC(y, 0, 4)).getUTCDay() + 6) % 7)) / 7); return `${y}${String(w).padStart(2, "0")}`; }

async function daily() {
  const y = add(TODAY, -1), s3 = add(y, -2), s7 = add(y, -6);
  const [d1, d0, d3, w7] = await seq([() => collect(y, y, "day"), () => collect(add(y, -1), add(y, -1), "day"), () => collect(s3, y, "day"), () => collect(s7, y, "day")]);
  const b3 = days(s3, y).map(ymd), b7 = days(s7, y).map(ymd);
  return { name: `daily-${iso(y)}`, title: `일간 보고서 · ${iso(y)}(${DOW[y.getUTCDay()]})`,
    sub: `어제 하루 결과와 최근 3일 비교, 최근 7일 흐름입니다. (${iso(TODAY)} 08시 기준)`,
    body: `<section class="card"><h2>어제 한눈에 (그제와 비교)</h2>${kpis(d1, d0)}</section>
      ${clickersSection(d3, "최근 3일")}
      ${trend(b3, d3, dayLabel, "최근 3일 비교")}
      ${trend(b7, w7, dayLabel, "최근 7일 흐름")}
      ${postsSection(d3, "최근 3일")}${sourcesSection(d3, "최근 3일")}`, kpi: d1.tot, prevKpi: d0.tot, data: d3 };
}
async function weekly() {
  const end = add(TODAY, -((TODAY.getUTCDay() + 6) % 7) - 1);   // 지난 일요일
  const start = add(end, -6), ps = add(start, -7), pe = add(start, -1), w4s = add(start, -21);
  const [cur, prev, w4] = await seq([() => collect(start, end, "day"), () => collect(ps, pe, "day"), () => collect(w4s, end, "week")]);
  const wk = [...new Set(days(w4s, end).map(isoWeekKey))];
  return { name: `weekly-${iso(start)}`, title: `주간 보고서 · ${md_(start)}(월) ~ ${md_(end)}(일)`,
    sub: `지난주 월~일 결과를 그 전 주와 비교하고, 최근 4주 흐름을 함께 봅니다.`,
    body: `<section class="card"><h2>지난주 한눈에 (전주 대비)</h2>${kpis(cur, prev)}</section>
      ${clickersSection(cur, "이 기간")}
      ${trend(days(start, end).map(ymd), cur, dayLabel, "요일별")}
      ${trend(wk, w4, (k) => { const m = days(w4s, end).find((d) => isoWeekKey(d) === k); return `${md_(m)}~`; }, "최근 4주 (주별 누적)")}
      ${postsSection(cur, "지난주")}${sourcesSection(cur, "지난주")}`, kpi: cur.tot, prevKpi: prev.tot, data: cur };
}
async function monthly() {
  const y = TODAY.getUTCFullYear(), m = TODAY.getUTCMonth() - 1;
  const start = monthStart(y, m), end = monthEnd(y, m), ps = monthStart(y, m - 1), pe = monthEnd(y, m - 1);
  const m3s = monthStart(y, m - 2), w4s = add(end, -27);
  const [cur, prev, m3, w4] = await seq([() => collect(start, end, "day"), () => collect(ps, pe, "day"), () => collect(m3s, end, "month"), () => collect(w4s, end, "week")]);
  const wk = [...new Set(days(w4s, end).map(isoWeekKey))];
  return { name: `monthly-${iso(start).slice(0, 7)}`, title: `월간 보고서 · ${start.getUTCFullYear()}년 ${start.getUTCMonth() + 1}월`,
    sub: `${iso(start)} ~ ${iso(end)} 결과를 전월과 비교하고, 최근 4주·최근 3개월 누적을 함께 봅니다.`,
    body: `<section class="card"><h2>지난달 한눈에 (전월 대비)</h2>${kpis(cur, prev)}</section>
      ${clickersSection(cur, "이 기간")}
      ${trend(days(start, end).map(ymd), cur, (k) => `${+k.slice(6)}일`, "일별")}
      ${trend(wk, w4, (k) => { const d = days(w4s, end).find((x) => isoWeekKey(x) === k); return `${md_(d)}~`; }, "최근 4주 (주별 누적)")}
      ${trend([0, 1, 2].map((i) => ymd(monthStart(y, m - 2 + i)).slice(0, 6)), m3, monLabel, "최근 3개월 (월별 누적)")}
      ${postsSection(cur, "지난달")}${sourcesSection(cur, "지난달")}`, kpi: cur.tot, prevKpi: prev.tot, data: cur };
}
async function quarterly() {
  const y0 = TODAY.getUTCFullYear(), qm = Math.floor(TODAY.getUTCMonth() / 3) * 3 - 3;
  const start = monthStart(y0, qm), end = monthEnd(y0, qm + 2), ps = monthStart(y0, qm - 3), pe = monthEnd(y0, qm - 1);
  const [cur, prev, six] = await seq([() => collect(start, end, "month"), () => collect(ps, pe, "month"), () => collect(ps, end, "month")]);
  const q = Math.floor(start.getUTCMonth() / 3) + 1;
  return { name: `quarterly-${start.getUTCFullYear()}-Q${q}`, title: `분기 보고서 · ${start.getUTCFullYear()}년 ${q}분기`,
    sub: `${iso(start)} ~ ${iso(end)} 결과를 직전 분기와 비교합니다.`,
    body: `<section class="card"><h2>분기 한눈에 (직전 분기 대비)</h2>${kpis(cur, prev)}</section>
      ${clickersSection(cur, "이 기간")}
      ${trend([0, 1, 2, 3, 4, 5].map((i) => ymd(monthStart(y0, qm - 3 + i)).slice(0, 6)), six, monLabel, "최근 6개월 (월별)")}
      ${postsSection(cur, `${q}분기`)}${sourcesSection(cur, `${q}분기`)}`, kpi: cur.tot, prevKpi: prev.tot, data: cur };
}
async function yearly() {
  const yy = TODAY.getUTCFullYear() - 1, start = monthStart(yy, 0), end = monthEnd(yy, 11);
  const [cur, prev] = await seq([() => collect(start, end, "month"), () => collect(monthStart(yy - 1, 0), monthEnd(yy - 1, 11), "month")]);
  return { name: `yearly-${yy}`, title: `연간 보고서 · ${yy}년`, sub: `${yy}년 1~12월 결과를 전년과 비교합니다.`,
    body: `<section class="card"><h2>한 해 한눈에 (전년 대비)</h2>${kpis(cur, prev)}</section>
      ${clickersSection(cur, "이 기간")}
      ${trend([...Array(12).keys()].map((i) => ymd(monthStart(yy, i)).slice(0, 6)), cur, monLabel, "월별")}
      ${postsSection(cur, `${yy}년`)}${sourcesSection(cur, `${yy}년`)}`, kpi: cur.tot, prevKpi: prev.tot, data: cur };
}

// ───────── HTML ─────────
function page(rep) {
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(rep.title)} — 어라운드툴 추천 모음</title><style>
:root{--bg:#f4f3ef;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--ink3:#76756f;--line:#e4e2dc;--s1:#2a78d6;--s2:#eb6834;--up:#0c7a43;--down:#b42318}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121211;--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--ink3:#9a998f;--line:#33332f;--s1:#3987e5;--s2:#d95926;--up:#4cc38a;--down:#f97066}}
:root[data-theme="dark"]{--bg:#121211;--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--ink3:#9a998f;--line:#33332f;--s1:#3987e5;--s2:#d95926;--up:#4cc38a;--down:#f97066}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 "Pretendard Variable",Pretendard,-apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:20px 16px 48px}header h1{font-size:1.45rem;margin:0 0 .25rem}header p{margin:0;color:var(--ink2)}
.card.main{border:2px solid var(--s2)}.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 18px 14px;margin-top:16px}
h2{font-size:1.08rem;margin:0 0 .8rem}h3{font-size:.9rem;margin:.2rem 0 .4rem;color:var(--ink2);font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}@media(min-width:760px){.kpis{grid-template-columns:repeat(4,1fr)}}
.kpi{border:1px solid var(--line);border-radius:12px;padding:12px}.kpi p{margin:0;color:var(--ink2);font-size:.82rem}.kpi b{display:block;font-size:1.7rem;line-height:1.2;margin:.2rem 0}
.kpi em{display:block;font-style:normal;font-size:.78rem;color:var(--ink3)}.dl{display:block;font-size:.8rem;margin-top:.3rem;color:var(--ink2)}.dl.up{color:var(--up)}.dl.down{color:var(--down)}.dl small{color:var(--ink3)}
.two{display:grid;gap:18px}.two>div{min-width:0}@media(min-width:760px){.two{grid-template-columns:1fr 1fr}}
.chart{width:100%;height:auto;display:block}.grid{stroke:var(--line);stroke-width:1}.axis{stroke:var(--ink3);stroke-width:1}.tick{fill:var(--ink3);font-size:11px}.val{fill:var(--ink2);font-size:11px;font-weight:600}
.s1{fill:var(--s1);background:var(--s1)}.s2{fill:var(--s2);background:var(--s2)}.dup{opacity:.38}
.lg{display:flex;gap:14px;flex-wrap:wrap;margin:0 0 .2rem;font-size:.76rem;color:var(--ink2)}.lg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.hb-row{display:grid;grid-template-columns:minmax(90px,38%) 1fr auto;gap:8px;align-items:center;padding:4px 0;font-size:.84rem}
.hb-l{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.hb-t{height:12px;background:transparent;border-radius:0 4px 4px 0}.hb-t i{display:block;height:12px;border-radius:0 4px 4px 0;min-width:2px}
.hb-v{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}.hb-v small{display:block;color:var(--ink3);font-size:.72rem}
.tw{overflow-x:auto;margin-top:12px}table{border-collapse:collapse;width:100%;font-size:.82rem}th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;white-space:nowrap}
th{color:var(--ink2);font-weight:600;background:var(--bg)}td.r{text-align:right;font-variant-numeric:tabular-nums}
.note{font-size:.76rem;color:var(--ink3);margin:.5rem 0 0}.empty{color:var(--ink3);font-size:.86rem;margin:.4rem 0}
.foot{font-size:.76rem;color:var(--ink3);margin-top:18px;line-height:1.7}
#tip{position:fixed;pointer-events:none;background:var(--ink);color:var(--surface);font-size:.78rem;padding:6px 9px;border-radius:8px;max-width:280px;display:none;z-index:9}
</style></head><body><div class="wrap">
<header><h1>${esc(rep.title)}</h1><p>${esc(rep.sub)}</p></header>
${rep.body}
${ERRORS.length ? `<p class="foot" style="color:var(--down)">일부 숫자를 불러오지 못했습니다: ${esc([...new Set(ERRORS)].join(" / "))}</p>` : ""}
<p class="foot">· 사람 수 = 같은 기기·브라우저를 한 사람으로 센 값(GA4). 중복 = 횟수 − 사람 수. GA4는 개인정보 보호로 IP 주소를 제공하지 않아 같은 와이파이의 다른 기기는 다른 사람으로 셉니다.<br>
· 브랜드커넥트(BC) 버튼 = 네이버 브랜드 커넥트(구매·예약 페이지)로 가는 '제품 가격 알아보기·여행 비용 알아보기' 버튼(첫 버튼·중간·글 끝·팝업). 실제 구매 수는 네이버 커넥트 관리 화면에서 확인하세요.<br>
· 만든 시각 ${new Date().toISOString().slice(0, 16).replace("T", " ")} UTC · GA4 속성 ${PROPERTY}</p></div>
<div id="tip" role="tooltip"></div>
<script>(function(){var t=document.getElementById('tip');document.addEventListener('mousemove',function(e){var el=e.target.closest&&e.target.closest('[data-tip]');if(!el){t.style.display='none';return}t.textContent=el.getAttribute('data-tip');t.style.display='block';t.style.left=Math.min(e.clientX+12,innerWidth-290)+'px';t.style.top=(e.clientY+14)+'px'});
document.addEventListener('click',function(e){var el=e.target.closest&&e.target.closest('[data-tip]');if(!el){t.style.display='none';return}var r=el.getBoundingClientRect();t.textContent=el.getAttribute('data-tip');t.style.display='block';t.style.left=Math.min(r.left,innerWidth-290)+'px';t.style.top=(r.top-36)+'px'})})();</script>
</body></html>`;
}


// ───────── 사이트 전체 유입 KPI (팀 회의·/jack/ 용) ─────────
async function siteKpi() {
  const y = add(TODAY, -1), s7 = add(y, -6), p7e = add(s7, -1), p7s = add(p7e, -6), s28 = add(y, -27);
  const tot = async (a, b) => { const r = await ga(a, b, [], ["totalUsers", "sessions", "screenPageViews"]); const m = r[0] ? r[0].m : [0, 0, 0]; return { users: m[0], sessions: m[1], views: m[2] }; };
  const org = async (a, b) => { const r = await ga(a, b, ["sessionDefaultChannelGroup"], ["sessions"]); const o = {}; for (const x of r) o[x.d[0]] = x.m[0]; return o; };
  const [cur, prev, chCur, chPrev, series, land] = await seq([() => tot(s7, y), () => tot(p7s, p7e), () => org(s7, y), () => org(p7s, p7e),
    () => ga(s28, y, ["date"], ["totalUsers", "sessions"]), () => ga(s7, y, ["landingPage"], ["sessions"], null, 10)]);
  const g = {};
  try {
    const last = add(kstToday(), -3), t = await token();
    const sites = await (await fetch("https://www.googleapis.com/webmasters/v3/sites", { headers: { Authorization: `Bearer ${t}` } })).json();
    const site = (sites.siteEntry || []).map((x) => x.siteUrl).find((u) => /aroundtool\.com/.test(u));
    const q = async (a, b) => { const r = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(site)}/searchAnalytics/query`, {
      method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ startDate: iso(a), endDate: iso(b) }) });
      const row = ((await r.json()).rows || [])[0] || {}; return { clicks: row.clicks || 0, impressions: row.impressions || 0, position: row.position || null }; };
    if (site) { g.range = `${iso(add(last, -6))} ~ ${iso(last)}`; g.cur = await q(add(last, -6), last); g.prev = await q(add(last, -13), add(last, -7)); }
  } catch (e) { g.error = e.message; }
  return { made: new Date().toISOString(), range: `${iso(s7)} ~ ${iso(y)}`, prevRange: `${iso(p7s)} ~ ${iso(p7e)}`, cur, prev,
    organic: { cur: chCur["Organic Search"] || 0, prev: chPrev["Organic Search"] || 0 }, channels: { cur: chCur, prev: chPrev },
    daily: series.map((x) => ({ date: x.d[0], users: x.m[0], sessions: x.m[1] })).sort((a, b) => a.date.localeCompare(b.date)),
    landing: land.map((x) => ({ page: x.d[0], sessions: x.m[0] })), google: g };
}

// ───────── 실행 ─────────
const want = opt("--type");
const dow = TODAY.getUTCDay(), dom = TODAY.getUTCDate(), mon = TODAY.getUTCMonth();
const plan = want ? [want] : ["daily", ...(dow === 3 ? ["weekly"] : []), ...(dom === 3 ? ["monthly"] : []),
  ...(dom === 3 && [0, 3, 6, 9].includes(mon) ? ["quarterly"] : []), ...(dom === 3 && mon === 0 ? ["yearly"] : [])];
const FN = { daily, weekly, monthly, quarterly, yearly };
mkdirSync("_cta/reports", { recursive: true });
const made = [];
for (const t of plan) {
  try {
    const rep = await FN[t]();
    writeFileSync(`_cta/reports/${rep.name}.html`, page(rep));
    made.push({ type: t, file: `reports/${rep.name}.html`, title: rep.title, kpi: rep.kpi, prev: rep.prevKpi,
      topPosts: Object.entries(rep.data.posts).sort((a, b) => b[1].clicks - a[1].clicks || b[1].views - a[1].views).slice(0, 3).map(([k, p]) => ({ post: title(k), views: p.views, clicks: p.clicks })),
      sources: rep.data.sources.slice(0, 5), keywords: rep.data.keywords.slice(0, 8), google: rep.data.google.rows.slice(0, 8) });
    console.log(`✓ ${rep.title}`);
  } catch (e) { console.log(`✗ ${t}: ${e.message}`); ERRORS.push(`${t}: ${e.stack || e.message}`); }
}
if (!MOCK) { try { writeFileSync("_cta/kpi.json", JSON.stringify(await siteKpi(), null, 1)); console.log("✓ 사이트 KPI"); } catch (e) { console.log(`✗ 사이트 KPI: ${e.message}`); ERRORS.push(`kpi: ${e.message}`); } }
writeFileSync("_cta/today.json", JSON.stringify({ date: iso(TODAY), reports: made, errors: [...new Set(ERRORS)] }, null, 1));
let md = `# 추천 모음 보고서 ${iso(TODAY)}\n\n> 전달 방법: 이 브랜치의 today.json 에 적힌 reports/*.html 파일을 그대로 사용자에게 보내고(그래프·표가 든 시각 보고서), 핵심 숫자·상위 글·유입 매체·검색어를 짧게 요약한다.\n\n`;
for (const r of made) md += `- ${r.title}: 조회 ${r.kpi.views}(사람 ${r.kpi.viewers}) · 브랜드커넥트 버튼 클릭 ${r.kpi.clicks}(사람 ${r.kpi.clickers}) → ${r.file}\n`;
writeFileSync("_cta/cta-latest.md", md);
