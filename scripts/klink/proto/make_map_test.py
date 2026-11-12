# -*- coding: utf-8 -*-
"""K링크 실제 지도 시험판 (MapLibre + OpenFreeMap) — /klink/map-test.html
python3 scripts/klink/proto/make_map_test.py"""
import json, os
R = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(R); ROOT = os.path.dirname(os.path.dirname(K))
P = json.load(open(os.path.join(K, 'build', 'places.json'), encoding='utf-8'))
G = json.load(open(os.path.join(K, 'build', 'geo.json'), encoding='utf-8'))
A = json.load(open(os.path.join(ROOT, 'klink', 'around.json'), encoding='utf-8'))
icons = open(os.path.join(K, 'src', 'icons.js'), encoding='utf-8').read()
REG = {
  'gyeongju': dict(t=['경주', '庆州', 'Gyeongju', '慶州'], route=dict(label=['경주 1박 2일 · 1일차 (어라운드툴 코스)', '庆州 2天1夜 · 第1天', 'Gyeongju 2 days · Day 1', '慶州1泊2日・1日目'],
                   ids=['gj_daereung', 'gj_hwangni', 'gj_gyochon', 'gj_wolji'])),
  'osaka': dict(t=['오사카', '大阪', 'Osaka', '大阪'], route=dict(label=['오사카 2박 3일 · 2일차 (어라운드툴 코스)', '大阪 3天2夜 · 第2天', 'Osaka 3 days · Day 2', '大阪2泊3日・2日目'],
                   ids=['os_castle', 'os_umeda', 'os_shinsekai'])),
}
data = {}
for r, v in REG.items():
    pl = [p for p in P if p['r'] == r]
    zones = [{'id': d['id'], 'n': d['n'], 'g': d['g']} for d in G['regions'][r]['districts']]
    spots = {p['id']: A['spots'].get(p['id'], {}) for p in pl}
    data[r] = dict(t=v['t'], route=v['route'], zones=zones,
                   places=[dict(id=p['id'], c=p['c'], n=p['n'], d=p['d'], lat=p['lat'], lng=p['lng'], far=p.get('far', 0), dist=G['pd'].get(p['id'], ''),
                                one=(spots[p['id']].get('s') or {}).get('one'), photo=((spots[p['id']].get('s') or {}).get('photo') or {}).get('src')) for p in pl])
html = r'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>K링크 실제 지도 시험판</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css">
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
<style>
:root{--ink:#141A2E;--mute:#6B7390;--line:#E3E7F0;--cobalt:#2443E8;--soft:#F3F5FA;--sheet:208px}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;height:100%;overflow:hidden;font-family:system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;color:var(--ink);background:#fff}
#map{position:fixed;left:0;right:0;top:0;bottom:var(--sheet)}
/* 위: 한 줄짜리 작은 막대 */
.bar{position:fixed;top:calc(env(safe-area-inset-top,0px) + 10px);left:10px;right:10px;display:flex;gap:6px;align-items:center;z-index:5}
.chip{appearance:none;border:0;background:#fff;border-radius:999px;height:40px;padding:0 14px;font:700 14px inherit;color:var(--ink);box-shadow:0 2px 10px rgba(20,26,46,.16);display:inline-flex;align-items:center;gap:6px;cursor:pointer}
select.chip{padding-right:30px;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23141A2E' stroke-width='3'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E") no-repeat right 12px center}
.chip.sm{font-weight:600;color:var(--mute)}
.chip.on{background:var(--ink);color:#fff}
.sp{flex:1}
/* 아래: 시트 (모바일 기본) */
.sheet{position:fixed;left:0;right:0;bottom:0;height:var(--sheet);background:#fff;border-radius:20px 20px 0 0;box-shadow:0 -6px 24px rgba(20,26,46,.14);z-index:6;padding:8px 0 calc(env(safe-area-inset-bottom,0px) + 8px);display:flex;flex-direction:column}
.grab{width:40px;height:4px;border-radius:2px;background:#D5DAE6;margin:0 auto 8px}
.shd{display:flex;align-items:center;gap:8px;padding:0 16px 8px;font-size:13px}
.shd b{font-size:15px}
.shd .rt{margin-left:auto;color:var(--cobalt);font-weight:700;display:flex;align-items:center;gap:6px;white-space:nowrap}
.shd .rt i{display:inline-block;width:16px;height:4px;border-radius:2px;background:var(--cobalt)}
.rail{display:flex;gap:10px;overflow-x:auto;padding:2px 16px 4px;scroll-snap-type:x mandatory;scrollbar-width:none;flex:1}
.rail::-webkit-scrollbar{display:none}
.pc{flex:0 0 78%;max-width:300px;scroll-snap-align:center;display:flex;gap:10px;background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:10px;cursor:pointer;text-align:left;font:inherit;color:inherit}
.pc.on{border-color:var(--cobalt);box-shadow:0 0 0 3px rgba(36,67,232,.15)}
.pc .th{width:76px;height:100%;min-height:84px;border-radius:12px;flex-shrink:0;background-size:cover;background-position:center;display:grid;place-items:center}
.pc .th svg{width:30px;height:30px;color:#fff}
.pc .tx{min-width:0;display:flex;flex-direction:column}
.pc .k{font-size:11.5px;font-weight:700}
.pc .n{font-size:15.5px;font-weight:800;line-height:1.3;margin-top:2px}
.pc .d{font-size:12.5px;color:var(--mute);line-height:1.45;margin-top:3px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.pc .go{margin-top:auto;padding-top:6px;font-size:12.5px;font-weight:800;color:var(--cobalt)}
.pc .num{position:static;display:inline-grid;place-items:center;width:18px;height:18px;border:2px solid var(--cobalt);font-size:10px;line-height:1;margin-right:4px;box-shadow:none}
/* 지도 위 핀 */
.pin{display:flex;flex-direction:column;align-items:center;cursor:pointer}
.pin .dot{width:28px;height:28px;border-radius:50%;border:2.5px solid #fff;display:grid;place-items:center;box-shadow:0 2px 6px rgba(0,0,0,.3);transition:transform .15s}
.pin .dot svg{width:15px;height:15px;color:#fff}
.pin .lb{margin-top:3px;background:rgba(255,255,255,.95);border-radius:8px;padding:2px 7px;font-size:11.5px;font-weight:700;white-space:nowrap;box-shadow:0 1px 4px rgba(0,0,0,.15)}
.lbl-off .pin .lb{display:none}.lbl-off .pin.on .lb{display:block}
.pin.on{z-index:3}.pin.on .dot{transform:scale(1.3);box-shadow:0 0 0 5px rgba(36,67,232,.25),0 2px 6px rgba(0,0,0,.3)}
.num{width:22px;height:22px;border-radius:50%;background:#fff;border:3px solid var(--cobalt);font:800 11px/16px inherit;text-align:center;color:var(--ink);box-shadow:0 2px 5px rgba(0,0,0,.25)}
.maplibregl-ctrl-bottom-right{bottom:6px}
.maplibregl-ctrl-group button{width:36px;height:36px}
/* PC: 왼쪽 목록 + 오른쪽 지도 */
@media (min-width:900px){
  :root{--sheet:0px}
  #map{left:380px}
  .bar{left:396px}
  .sheet{top:0;bottom:0;left:0;right:auto;width:380px;height:auto;border-radius:0;box-shadow:1px 0 0 var(--line);padding:16px 0}
  .grab{display:none}
  .rail{flex-direction:column;overflow-y:auto;overflow-x:hidden;scroll-snap-type:none;gap:10px}
  .pc{flex:0 0 auto;max-width:none}
  .shd{flex-wrap:wrap}
}
</style></head><body>
<div id="map"></div>
<div class="bar">
  <select class="chip" id="reg" aria-label="여행지"></select>
  <span class="sp"></span>
  <button class="chip sm" id="mode" aria-pressed="false">3D</button>
  <select class="chip sm" id="lang" aria-label="Language"></select>
</div>
<section class="sheet" id="sheet"><div class="grab"></div><div class="shd" id="shd"></div><div class="rail" id="rail"></div></section>
<script>
__ICONS__
const DATA = __DATA__;
const CATC = {palace:'#A0522D',food:'#EF7C1C',skin:'#E8457A',shop:'#0E9A63',cafe:'#8C6A4B',kpop:'#8E5BD8',night:'#3B3FB6',nature:'#0E9F8F',fun:'#D99A00'};
const CATN = {palace:['역사·문화','历史文化','History','歴史・文化'],food:['맛집','美食','Food','グルメ'],cafe:['카페','咖啡','Café','カフェ'],shop:['쇼핑','购物','Shopping','ショッピング'],night:['야경','夜景','Night view','夜景'],nature:['자연·바다','自然','Nature','自然'],fun:['테마파크·체험','体验','Fun','体験'],skin:['뷰티','美容','Beauty','ビューティー'],kpop:['K-POP','K-POP','K-POP','K-POP']};
const TX = {places:['곳','处','places','か所'],more:['자세히 ›','详情 ›','Details ›','詳しく ›']};
const LANGS = [['ko','한국어'],['zh','中文'],['en','English'],['ja','日本語']], LI = {ko:0,zh:1,en:2,ja:3};
let R = location.hash.slice(1) in DATA ? location.hash.slice(1) : 'gyeongju', L = 'ko', markers = {}, nums = [], sel = null;
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const t4 = a => a[LI[L]] || a[0];
const isMob = () => innerWidth < 900;
const map = new maplibregl.Map({ container: 'map', style: 'https://tiles.openfreemap.org/styles/liberty', center: [129.22, 35.83], zoom: 12,
  attributionControl: { compact: true }, dragRotate: false, pitchWithRotate: false,
  localIdeographFontFamily: '"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR","Noto Sans CJK KR",sans-serif' });
map.touchZoomRotate.disableRotation();
map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right');
function setLabels() {
  for (const l of map.getStyle().layers) {
    if (l.type !== 'symbol' || !l.layout || !l.layout['text-field']) continue;
    if (!JSON.stringify(l.layout['text-field']).includes('name')) continue;
    map.setLayoutProperty(l.id, 'text-field', ['coalesce', ['get', 'name:' + L], ['get', 'name']]);
  }
}
const pname = p => p.n[L] || p.n.en || p.n.ko;
function drawMap() {
  const d = DATA[R];
  Object.values(markers).forEach(m => m.remove()); nums.forEach(m => m.remove()); markers = {}; nums = [];
  const zones = { type: 'FeatureCollection', features: d.zones.map(z => ({ type: 'Feature', properties: {}, geometry: { type: 'MultiPolygon', coordinates: z.g } })) };
  const route = { type: 'Feature', geometry: { type: 'LineString', coordinates: d.route.ids.map(id => { const p = d.places.find(x => x.id === id); return [p.lng, p.lat]; }) } };
  for (const [id, data] of [['zones', zones], ['route', route]]) { const s = map.getSource(id); if (s) s.setData(data); else map.addSource(id, { type: 'geojson', data }); }
  if (!map.getLayer('zones-fill')) {
    map.addLayer({ id: 'zones-fill', type: 'fill', source: 'zones', paint: { 'fill-color': '#2443E8', 'fill-opacity': 0.05 } });
    map.addLayer({ id: 'zones-line', type: 'line', source: 'zones', paint: { 'line-color': '#2443E8', 'line-width': 1.4, 'line-dasharray': [3, 2], 'line-opacity': 0.5 } });
    map.addLayer({ id: 'route-line', type: 'line', source: 'route', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': '#2443E8', 'line-width': 4.5, 'line-opacity': 0.85 } });
  }
  d.route.ids.forEach((id, i) => { const p = d.places.find(x => x.id === id); const el = document.createElement('div'); el.className = 'num'; el.textContent = i + 1;
    nums.push(new maplibregl.Marker({ element: el, offset: [15, -14] }).setLngLat([p.lng, p.lat]).addTo(map)); });
  for (const p of d.places) {
    const el = document.createElement('div'); el.className = 'pin';
    el.innerHTML = `<span class="dot" style="background:${CATC[p.c]}">${ICONS['c_' + p.c] || ''}</span><span class="lb">${esc(pname(p))}</span>`;
    el.onclick = e => { e.stopPropagation(); pick(p.id, true); };
    markers[p.id] = new maplibregl.Marker({ element: el, anchor: 'center' }).setLngLat([p.lng, p.lat]).addTo(map);
  }
  labels();
}
function labels() { document.body.classList.toggle('lbl-off', isMob() && map.getZoom() < 13.2); }
map.on('zoom', labels);
function drawSheet() {
  const d = DATA[R];
  document.getElementById('shd').innerHTML = `<b>${esc(t4(d.t))}</b><span style="color:var(--mute)">${d.places.length}${t4(TX.places)}</span><span class="rt"><i></i>${esc(t4(d.route.label))}</span>`;
  const order = [...d.route.ids, ...d.places.map(p => p.id).filter(id => !d.route.ids.includes(id))];
  document.getElementById('rail').innerHTML = order.map(id => { const p = d.places.find(x => x.id === id), k = d.route.ids.indexOf(id);
    return `<button class="pc ${sel === id ? 'on' : ''}" data-id="${id}"><span class="th" style="${p.photo ? `background-image:url('${esc(p.photo)}')` : `background:${CATC[p.c]}`}">${p.photo ? '' : (ICONS['c_' + p.c] || '')}</span>
      <span class="tx"><span class="k" style="color:${CATC[p.c]}">${k >= 0 ? `<span class="num">${k + 1}</span>` : ''}${esc(t4(CATN[p.c]))}</span><span class="n">${esc(pname(p))}</span>
      <span class="d">${esc(L === 'ko' && p.one ? p.one : (p.d[L] || p.d.en || p.d.ko))}</span><span class="go" data-go="${id}">${t4(TX.more)}</span></span></button>`; }).join('');
  document.querySelectorAll('.pc').forEach(b => b.onclick = e => { if (e.target.dataset.go) { location.href = '/klink/#' + e.target.dataset.go; return; } pick(b.dataset.id, false); });
}
function pick(id, fromMap) {
  sel = id; const p = DATA[R].places.find(x => x.id === id);
  Object.entries(markers).forEach(([k, m]) => m.getElement().classList.toggle('on', k === id));
  document.querySelectorAll('.pc').forEach(b => b.classList.toggle('on', b.dataset.id === id));
  if (fromMap) { const c = document.querySelector(`.pc[data-id="${id}"]`); c && c.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' }); }
  map.easeTo({ center: [p.lng, p.lat], zoom: Math.max(map.getZoom(), 13.5), duration: 500 });
  labels();
}
// 모바일: 카드를 옆으로 넘기면 그 장소로 지도 이동
let st = 0; document.getElementById('rail').addEventListener('scroll', e => { if (!isMob()) return; clearTimeout(st); st = setTimeout(() => {
  const r = e.target.getBoundingClientRect(), cx = r.left + r.width / 2; let best = null, bd = 1e9;
  e.target.querySelectorAll('.pc').forEach(b => { const q = b.getBoundingClientRect(), dd = Math.abs(q.left + q.width / 2 - cx); if (dd < bd) { bd = dd; best = b; } });
  if (best && best.dataset.id !== sel) pick(best.dataset.id, false); }, 140); });
function fit() {
  const b = new maplibregl.LngLatBounds(); DATA[R].places.filter(p => !p.far).forEach(p => b.extend([p.lng, p.lat]));
  map.fitBounds(b, { padding: { top: 70, bottom: 30, left: 30, right: 30 }, maxZoom: 14, duration: 700 });
}
function ui() {
  const reg = document.getElementById('reg'), lang = document.getElementById('lang');
  reg.innerHTML = Object.keys(DATA).map(r => `<option value="${r}" ${r === R ? 'selected' : ''}>${esc(t4(DATA[r].t))}</option>`).join('');
  lang.innerHTML = LANGS.map(([k, n]) => `<option value="${k}" ${k === L ? 'selected' : ''}>${n}</option>`).join('');
  reg.onchange = () => { R = reg.value; sel = null; ui(); drawMap(); drawSheet(); fit(); };
  lang.onchange = () => { L = lang.value; document.documentElement.lang = L; ui(); setLabels(); drawMap(); drawSheet(); };
}
document.getElementById('mode').onclick = function () {
  const on = this.getAttribute('aria-pressed') !== 'true'; this.setAttribute('aria-pressed', on); this.classList.toggle('on', on);
  if (on && !map.getLayer('bld3d')) {
    const src = Object.keys(map.getStyle().sources).find(s => map.getStyle().sources[s].type === 'vector');
    if (src) map.addLayer({ id: 'bld3d', type: 'fill-extrusion', source: src, 'source-layer': 'building', minzoom: 13,
      paint: { 'fill-extrusion-color': '#dfe3ec', 'fill-extrusion-height': ['coalesce', ['get', 'render_height'], 8], 'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0], 'fill-extrusion-opacity': 0.85 } }, 'zones-fill');
  }
  if (map.getLayer('bld3d')) map.setLayoutProperty('bld3d', 'visibility', on ? 'visible' : 'none');
  map.easeTo({ pitch: on ? 55 : 0, zoom: on ? Math.max(map.getZoom(), 15) : map.getZoom(), duration: 800 });
};
map.on('load', () => { map.resize(); setLabels(); ui(); drawMap(); drawSheet(); fit(); });
addEventListener('resize', () => { map.resize(); labels(); });
</script></body></html>'''
html = html.replace('__ICONS__', icons).replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
open(os.path.join(ROOT, 'klink', 'map-test.html'), 'w', encoding='utf-8').write(html)
print('bytes', len(html.encode()))
