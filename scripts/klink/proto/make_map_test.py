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
:root{--ink:#141A2E;--mute:#6B7390;--line:#E3E7F0;--cobalt:#2443E8;--soft:#F3F5FA}
*{box-sizing:border-box}html,body{margin:0;height:100%;font-family:system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;color:var(--ink);background:#fff}
#map{position:fixed;inset:0}
.top{position:fixed;top:12px;left:12px;right:12px;display:flex;flex-wrap:wrap;gap:8px;z-index:5;pointer-events:none}
.top>*{pointer-events:auto}
.seg{display:flex;background:#fff;border-radius:999px;padding:4px;box-shadow:0 2px 10px rgba(20,26,46,.15)}
.seg button{border:0;background:none;font:600 14px inherit;padding:8px 14px;border-radius:999px;cursor:pointer;color:var(--mute)}
.seg button.on{background:var(--ink);color:#fff}
.badge{background:#fff;border-radius:999px;padding:8px 12px;font-size:12.5px;box-shadow:0 2px 10px rgba(20,26,46,.15);color:var(--mute)}
.badge a{color:var(--cobalt);font-weight:700;text-decoration:none}
.pin{display:flex;flex-direction:column;align-items:center;cursor:pointer;transform:translateY(-6px)}
.pin .dot{width:30px;height:30px;border-radius:50%;border:2.5px solid #fff;display:grid;place-items:center;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.pin .dot svg{width:16px;height:16px;color:#fff}
.pin .lb{margin-top:3px;background:rgba(255,255,255,.95);border-radius:8px;padding:2px 7px;font-size:12px;font-weight:700;white-space:nowrap;box-shadow:0 1px 4px rgba(0,0,0,.15)}
.pin.on .dot{width:38px;height:38px;outline:4px solid rgba(36,67,232,.25)}
.num{width:24px;height:24px;border-radius:50%;background:#fff;border:3px solid var(--cobalt);font:800 12px/18px inherit;text-align:center;color:var(--ink);box-shadow:0 2px 5px rgba(0,0,0,.25)}
.card{position:fixed;left:12px;right:12px;bottom:12px;max-width:440px;background:#fff;border-radius:18px;box-shadow:0 8px 30px rgba(20,26,46,.25);overflow:hidden;z-index:6;display:none}
.card.show{display:block}
.card img{display:block;width:100%;height:150px;object-fit:cover}
.card .b{padding:14px 16px 16px}
.card .k{font-size:12px;font-weight:700;color:#fff;border-radius:999px;padding:3px 9px;display:inline-block}
.card h3{margin:8px 0 4px;font-size:19px}
.card p{margin:0;color:#3A4160;font-size:14px;line-height:1.55}
.card .act{display:flex;gap:8px;margin-top:12px}
.card .act a,.card .act button{flex:1;text-align:center;border-radius:12px;padding:11px;font:700 14px inherit;text-decoration:none;border:0;cursor:pointer}
.card .go{background:var(--cobalt);color:#fff}.card .x{background:var(--soft);color:var(--ink)}
.route{position:fixed;left:12px;bottom:12px;background:#fff;border-radius:14px;padding:10px 14px;font-size:13px;font-weight:700;box-shadow:0 2px 10px rgba(20,26,46,.15);z-index:4}
.route i{display:inline-block;width:18px;height:4px;background:var(--cobalt);border-radius:2px;vertical-align:middle;margin-right:6px}
@media (min-width:700px){.card{left:auto;right:16px;bottom:16px;width:380px}}
</style></head><body>
<div id="map"></div>
<div class="top">
  <div class="seg" id="reg"></div>
  <div class="seg" id="lang"></div>
  <div class="seg" id="mode"><button data-m="2d" class="on">2D</button><button data-m="3d">3D 건물</button></div>
  <div class="badge">실제 지도 시험판 · <a href="/klink/">지금 K링크와 비교</a></div>
</div>
<div class="route" id="route"></div>
<div class="card" id="card"></div>
<script>
__ICONS__
const DATA = __DATA__;
const CATC = {palace:'#A0522D',food:'#EF7C1C',skin:'#E8457A',shop:'#0E9A63',cafe:'#8C6A4B',kpop:'#8E5BD8',night:'#3B3FB6',nature:'#0E9F8F',fun:'#D99A00'};
const CATN = {palace:['역사·문화','历史文化','History','歴史・文化'],food:['맛집','美食','Food','グルメ'],cafe:['카페','咖啡','Café','カフェ'],shop:['쇼핑','购物','Shopping','ショッピング'],night:['야경','夜景','Night view','夜景'],nature:['자연·바다','自然','Nature','自然'],fun:['테마파크·체험','体验','Fun','体験'],skin:['뷰티','美容','Beauty','ビューティー'],kpop:['K-POP','K-POP','K-POP','K-POP']};
const LANGS = [['ko','한국어'],['zh','中文'],['en','EN'],['ja','日本語']], LI = {ko:0,zh:1,en:2,ja:3};
let R = location.hash.slice(1) in DATA ? location.hash.slice(1) : 'gyeongju', L = 'ko', markers = [], sel = null;
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const t4 = a => a[LI[L]] || a[0];
const map = new maplibregl.Map({ container: 'map', style: 'https://tiles.openfreemap.org/styles/liberty', center: [129.22, 35.83], zoom: 12,
  attributionControl: { compact: true }, localIdeographFontFamily: '"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR","Noto Sans CJK KR",sans-serif' });
map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'bottom-right');
function setLabels() {   // 지명을 보는 사람 언어로 (없으면 현지 이름)
  for (const l of map.getStyle().layers) {
    if (l.type !== 'symbol' || !l.layout || !l.layout['text-field']) continue;
    if (!JSON.stringify(l.layout['text-field']).includes('name')) continue;
    map.setLayoutProperty(l.id, 'text-field', ['coalesce', ['get', 'name:' + L], ['get', 'name']]);
  }
}
function feat(r) {
  const d = DATA[r];
  return { zones: { type: 'FeatureCollection', features: d.zones.map(z => ({ type: 'Feature', properties: { n: t4(z.n) }, geometry: { type: 'MultiPolygon', coordinates: z.g } })) },
    route: { type: 'Feature', geometry: { type: 'LineString', coordinates: d.route.ids.map(id => { const p = d.places.find(x => x.id === id); return [p.lng, p.lat]; }) } } };
}
function draw() {
  const d = DATA[R], f = feat(R);
  for (const m of markers) m.remove(); markers = [];
  for (const [id, data] of [['zones', f.zones], ['route', f.route]]) { const s = map.getSource(id); if (s) s.setData(data); else map.addSource(id, { type: 'geojson', data }); }
  if (!map.getLayer('zones-fill')) {
    map.addLayer({ id: 'zones-fill', type: 'fill', source: 'zones', paint: { 'fill-color': '#2443E8', 'fill-opacity': 0.06 } });
    map.addLayer({ id: 'zones-line', type: 'line', source: 'zones', paint: { 'line-color': '#2443E8', 'line-width': 1.6, 'line-dasharray': [3, 2], 'line-opacity': 0.6 } });
    map.addLayer({ id: 'route-line', type: 'line', source: 'route', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': '#2443E8', 'line-width': 5, 'line-opacity': 0.85 } });
  }
  d.route.ids.forEach((id, i) => { const p = d.places.find(x => x.id === id); const el = document.createElement('div'); el.className = 'num'; el.textContent = i + 1;
    markers.push(new maplibregl.Marker({ element: el, offset: [16, -26] }).setLngLat([p.lng, p.lat]).addTo(map)); });
  for (const p of d.places) {
    const el = document.createElement('div'); el.className = 'pin' + (sel === p.id ? ' on' : '');
    el.innerHTML = `<span class="dot" style="background:${CATC[p.c]}">${ICONS['c_' + p.c] || ''}</span><span class="lb">${esc(p.n[L] || p.n.en || p.n.ko)}</span>`;
    el.onclick = e => { e.stopPropagation(); open(p.id); };
    markers.push(new maplibregl.Marker({ element: el, anchor: 'top' }).setLngLat([p.lng, p.lat]).addTo(map));
  }
  document.getElementById('route').innerHTML = `<i></i>${esc(t4(d.route.label))}`;
}
function fit() {
  const pts = DATA[R].places.filter(p => !p.far), b = new maplibregl.LngLatBounds();
  pts.forEach(p => b.extend([p.lng, p.lat]));
  map.fitBounds(b, { padding: { top: 90, bottom: 90, left: 40, right: 40 }, maxZoom: 14.5, duration: 800 });
}
function open(id) {
  sel = id; const p = DATA[R].places.find(x => x.id === id), c = document.getElementById('card');
  c.innerHTML = `${p.photo ? `<img src="${esc(p.photo)}" alt="">` : ''}<div class="b"><span class="k" style="background:${CATC[p.c]}">${esc(t4(CATN[p.c]))}</span>
    <h3>${esc(p.n[L] || p.n.en || p.n.ko)}</h3><p>${esc(L === 'ko' && p.one ? p.one : (p.d[L] || p.d.en || p.d.ko))}</p>
    <div class="act"><a class="go" href="/klink/#${p.id}">K링크에서 자세히</a><button class="x" id="cx">닫기</button></div></div>`;
  c.classList.add('show'); document.getElementById('cx').onclick = () => { c.classList.remove('show'); sel = null; draw(); };
  map.easeTo({ center: [p.lng, p.lat], zoom: Math.max(map.getZoom(), 14), duration: 600, padding: innerWidth < 700 ? { bottom: Math.min(380, innerHeight * .5) } : { right: 400 } }); draw();
}
function ui() {
  document.getElementById('reg').innerHTML = Object.keys(DATA).map(r => `<button data-r="${r}" class="${r === R ? 'on' : ''}">${esc(t4(DATA[r].t))}</button>`).join('');
  document.getElementById('lang').innerHTML = LANGS.map(([k, n]) => `<button data-l="${k}" class="${k === L ? 'on' : ''}">${n}</button>`).join('');
  document.querySelectorAll('[data-r]').forEach(b => b.onclick = () => { R = b.dataset.r; sel = null; document.getElementById('card').classList.remove('show'); ui(); draw(); fit(); });
  document.querySelectorAll('[data-l]').forEach(b => b.onclick = () => { L = b.dataset.l; ui(); setLabels(); draw(); });
}
document.querySelectorAll('[data-m]').forEach(b => b.onclick = () => {
  document.querySelectorAll('[data-m]').forEach(x => x.classList.toggle('on', x === b));
  const on = b.dataset.m === '3d';
  if (on && !map.getLayer('bld3d')) {
    const src = Object.keys(map.getStyle().sources).find(s => map.getStyle().sources[s].type === 'vector');
    map.addLayer({ id: 'bld3d', type: 'fill-extrusion', source: src, 'source-layer': 'building', minzoom: 13,
      paint: { 'fill-extrusion-color': '#dfe3ec', 'fill-extrusion-height': ['coalesce', ['get', 'render_height'], 8], 'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0], 'fill-extrusion-opacity': 0.85 } }, 'zones-fill');
  }
  if (map.getLayer('bld3d')) map.setLayoutProperty('bld3d', 'visibility', on ? 'visible' : 'none');
  map.easeTo({ pitch: on ? 58 : 0, bearing: on ? -20 : 0, zoom: on ? Math.max(map.getZoom(), 15) : map.getZoom(), duration: 900 });
});
map.on('click', () => { document.getElementById('card').classList.remove('show'); if (sel) { sel = null; draw(); } });
map.on('load', () => { setLabels(); ui(); draw(); fit(); });
</script></body></html>'''
html = html.replace('__ICONS__', icons).replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
open(os.path.join(ROOT, 'klink', 'map-test.html'), 'w', encoding='utf-8').write(html)
print('bytes', len(html.encode()))
