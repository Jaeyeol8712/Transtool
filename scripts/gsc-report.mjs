#!/usr/bin/env node
/**
 * 구글 서치콘솔 주간 보고서 (최근 28일)
 * ─────────────────────────────────────────────
 * Search Analytics API 로 검색어·페이지별 노출/클릭/평균 순위를 받아
 * _report/gsc-latest.json, _report/gsc-latest.md 로 저장합니다. (seo-report 브랜치에 올라감)
 *
 * 특히 "기회 검색어" = 노출은 있는데 평균 순위 8~20위 인 검색어를 뽑아,
 * 어떤 페이지의 제목·첫 답변·FAQ 를 보강하면 1페이지로 올라올지 알려 줍니다.
 */
import { mkdirSync, writeFileSync } from "node:fs";

const TOKEN = process.env.GOOGLE_ACCESS_TOKEN;
if (!TOKEN) { console.log("· 구글 인증 토큰이 없어 보고서를 건너뜁니다."); process.exit(0); }
const H = { Authorization: `Bearer ${TOKEN}`, "Content-Type": "application/json" };

const sites = await (await fetch("https://www.googleapis.com/webmasters/v3/sites", { headers: H })).json();
const site = (sites.siteEntry || []).map((e) => e.siteUrl).find((u) => /aroundtool\.com/.test(u));
if (!site) { console.log("✗ 서치콘솔 속성을 찾지 못했습니다."); process.exit(1); }

const day = (d) => new Date(Date.now() - d * 864e5).toISOString().slice(0, 10);
const range = { startDate: day(30), endDate: day(2) };   // 최근 데이터는 2~3일 늦게 확정됩니다

async function q(dimensions, rowLimit = 1000) {
  const r = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(site)}/searchAnalytics/query`, {
    method: "POST", headers: H, body: JSON.stringify({ ...range, dimensions, rowLimit, dataState: "all" }),
  });
  if (!r.ok) { console.log(`✗ ${dimensions} ${r.status} ${await r.text()}`); return []; }
  return (await r.json()).rows || [];
}

const [byQuery, byPage, byQP, byDate] = await Promise.all([q(["query"]), q(["page"]), q(["query", "page"], 5000), q(["date"])]);
const pick = (r) => ({ clicks: r.clicks, impressions: r.impressions, ctr: +(r.ctr * 100).toFixed(1), position: +r.position.toFixed(1) });
const rows = {
  site, range,
  total: byDate.reduce((a, r) => ({ clicks: a.clicks + r.clicks, impressions: a.impressions + r.impressions }), { clicks: 0, impressions: 0 }),
  daily: byDate.map((r) => ({ date: r.keys[0], ...pick(r) })),
  queries: byQuery.map((r) => ({ query: r.keys[0], ...pick(r) })),
  pages: byPage.map((r) => ({ page: r.keys[0], ...pick(r) })),
  queryPages: byQP.map((r) => ({ query: r.keys[0], page: r.keys[1], ...pick(r) })),
};
rows.opportunities = rows.queryPages.filter((r) => r.position >= 7.5 && r.position <= 20.5 && r.impressions >= 3)
  .sort((a, b) => b.impressions - a.impressions).slice(0, 50);

mkdirSync("_report", { recursive: true });
writeFileSync("_report/gsc-latest.json", JSON.stringify(rows, null, 1));
const t = (list, cols) => ["| " + cols.join(" | ") + " |", "|" + cols.map(() => "---").join("|") + "|",
  ...list.map((r) => "| " + cols.map((c) => String(r[c] ?? "").replace(/\|/g, "/").replace("https://www.aroundtool.com", "")).join(" | ") + " |")].join("\n");
const md = [`# 서치콘솔 보고서 (${range.startDate} ~ ${range.endDate})`, ``,
  `속성: ${site} · 총 노출 ${rows.total.impressions} · 클릭 ${rows.total.clicks}`, ``,
  `## 기회 검색어 (평균 순위 8~20위)`, t(rows.opportunities.slice(0, 30), ["query", "page", "impressions", "clicks", "position"]), ``,
  `## 노출 상위 검색어`, t(rows.queries.slice(0, 40), ["query", "impressions", "clicks", "ctr", "position"]), ``,
  `## 노출 상위 페이지`, t(rows.pages.slice(0, 40), ["page", "impressions", "clicks", "ctr", "position"])].join("\n");
writeFileSync("_report/gsc-latest.md", md);
console.log(`✓ 보고서: 노출 ${rows.total.impressions}, 클릭 ${rows.total.clicks}, 검색어 ${rows.queries.length}개, 기회 검색어 ${rows.opportunities.length}개`);
