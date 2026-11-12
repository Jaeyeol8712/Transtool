'use strict';
/* =========================================================
   실제 지도 (MapLibre + OpenFreeMap) — 컨펌 i261112-15
   Map2DSvg(d3 그림 지도)와 같은 API를 낸다. 지도 라이브러리·WebGL을 못 쓰거나
   지도 스타일이 12초 안에 안 오면 Map2DSvg로 대신 그린다.
   국내 구역의 3D 거리(World3D)는 그대로 둔다(해외는 이 지도만).
   ========================================================= */
const MapGL = (() => {
  const STYLE = 'https://tiles.openfreemap.org/styles/liberty';
  const KR_BOX = [[124.6, 33.1], [130.95, 38.62]];
  let map = null, host = null, mode = null, ctx = {}, ready = false, queue = [], marks = [], pins = [], lang = null, gen = 0, minorZ = 0;
  const glOK = () => { try { const c = document.createElement('canvas'); return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl'))); } catch (e) { return false; } };
  const ok = !!window.maplibregl && glOK();

  /* ---------- 지도 만들기 ---------- */
  function mount(el) {
    if (host === el && map && el.contains(map.getContainer())) return;
    if (map) { try { map.remove(); } catch (e) {} }
    host = el; el.innerHTML = ''; ready = false; queue = []; marks = []; pins = []; mode = null; lang = null;
    const div = document.createElement('div'); div.className = 'glmap'; el.appendChild(div);
    map = new maplibregl.Map({
      container: div, style: STYLE, center: [127.8, 36.2], zoom: 5.5, attributionControl: false,
      dragRotate: false, pitchWithRotate: false, touchPitch: false, maxPitch: 0, renderWorldCopies: false, fadeDuration: 0,
      localIdeographFontFamily: '"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR","Noto Sans CJK KR","Noto Sans SC","Noto Sans JP",sans-serif'
    });
    map.touchZoomRotate.disableRotation();
    map.addControl(new maplibregl.AttributionControl({ compact: true }), 'bottom-left');
    const me = map;
    map.on('style.load', () => { if (me !== map) return; ready = true; layers(); setLabels(); const q = queue; queue = []; q.forEach(f => f()); });
    map.on('zoom', zoomClass);
    map.on('click', ev => {
      if (mode !== 'region') return;
      const f = map.getLayer('kl-area-fill') ? map.queryRenderedFeatures(ev.point, { layers: ['kl-area-fill'] }) : [];
      if (f.length && ctx.onDistrict && f[0].properties.id !== ctx.district) ctx.onDistrict(f[0].properties.id);
      else ctx.onBg && ctx.onBg();
    });
    setTimeout(() => { if (me === map && !ready) fallback(); }, 12000);
  }
  // 지도 스타일이 안 오면 그림 지도로 바꾼다
  function fallback() {
    if (Map2D !== MapGL) return;
    try { map && map.remove(); } catch (e) {}
    map = null; host = null; Map2D = Map2DSvg;
    try { renderPanel(); safeStage(); } catch (e) { console.error(e); }
  }
  const whenReady = f => { const g = gen; const run = () => { if (g === gen) f(); }; if (ready) run(); else queue.push(run); };
  function layers() {
    const empty = { type: 'FeatureCollection', features: [] };
    map.addSource('kl-area', { type: 'geojson', data: empty });
    map.addSource('kl-route', { type: 'geojson', data: empty });
    const before = map.getStyle().layers.find(l => l.type === 'symbol');   // 지명 글씨 아래에 깐다
    const b = before ? before.id : undefined;
    map.addLayer({ id: 'kl-area-fill', type: 'fill', source: 'kl-area', paint: { 'fill-color': ['case', ['get', 'on'], '#2443E8', ['get', 'saved'], '#FF4F7B', '#2443E8'], 'fill-opacity': ['case', ['get', 'on'], 0.12, ['get', 'saved'], 0.08, 0.05] } }, b);
    map.addLayer({ id: 'kl-area-line', type: 'line', source: 'kl-area', paint: { 'line-color': ['case', ['get', 'on'], '#2443E8', '#7F93EE'], 'line-width': ['case', ['get', 'on'], 2.2, 1.3], 'line-opacity': 0.8, 'line-dasharray': [3, 2] } }, b);
    map.addLayer({ id: 'kl-route-case', type: 'line', source: 'kl-route', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': '#fff', 'line-width': 8, 'line-opacity': 0.9 } });
    map.addLayer({ id: 'kl-route', type: 'line', source: 'kl-route', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': '#2443E8', 'line-width': 4.5 } });
  }
  function setLabels() {
    if (!ready || lang === S.lang) return; lang = S.lang;
    for (const l of map.getStyle().layers) {
      if (l.type !== 'symbol' || !l.layout || !l.layout['text-field']) continue;
      if (!JSON.stringify(l.layout['text-field']).includes('name')) continue;
      map.setLayoutProperty(l.id, 'text-field', ['coalesce', ['get', 'name:' + S.lang], ['get', 'name']]);
    }
  }
  const setData = (id, fc) => { const s = map.getSource(id); if (s) s.setData(fc); };
  const fcOf = feats => ({ type: 'FeatureCollection', features: feats });

  /* ---------- 화면 여백 (모바일은 아래 시트, PC는 왼쪽 목록) ---------- */
  function pads() {
    const r = host.getBoundingClientRect(), w = Math.max(200, r.width), h = Math.max(160, r.height), desk = window.innerWidth >= 980;
    const app = document.getElementById('app');
    const sheet = desk || ctx.noSheet ? 0 : (parseFloat(app ? getComputedStyle(app).getPropertyValue('--sheet-px') : 0) || h * 0.38);
    let t = ctx.noSheet ? (ctx.top || 20) + 16 : desk ? 90 : 116, b = (ctx.noSheet ? 20 : sheet + 20), l = 24, rr = desk && !ctx.noSheet ? 76 : ctx.noSheet ? 24 : 64;
    if (t + b > h - 80) { const k = (h - 80) / (t + b); t = Math.round(t * k); b = Math.round(b * k); }
    if (l + rr > w - 80) { l = 12; rr = 12; }
    return { top: t, bottom: b, left: l, right: rr, w, h };
  }
  function fit(box, maxZoom, extra = 0) {
    map.resize();
    const p = pads();
    try { map.fitBounds(box, { padding: { top: p.top + extra, bottom: p.bottom + extra, left: p.left + extra, right: p.right + extra }, maxZoom: maxZoom || 15, animate: false }); }
    catch (e) { map.fitBounds(box, { padding: 10, maxZoom: maxZoom || 15, animate: false }); }
  }
  function bbox(pts, minSpan = 0.01) {
    let a0 = 90, a1 = -90, o0 = 180, o1 = -180;
    for (const [lng, lat] of pts) { if (lat < a0) a0 = lat; if (lat > a1) a1 = lat; if (lng < o0) o0 = lng; if (lng > o1) o1 = lng; }
    if (a1 - a0 < minSpan) { const m = (a0 + a1) / 2; a0 = m - minSpan / 2; a1 = m + minSpan / 2; }
    if (o1 - o0 < minSpan) { const m = (o0 + o1) / 2; o0 = m - minSpan / 2; o1 = m + minSpan / 2; }
    return [[o0, a0], [o1, a1]];
  }
  const polysPts = polys => polys.flatMap(poly => poly[0] || []);
  function centroid(polys) {   // 가장 큰 고리의 면적 중심
    let best = null, ba = -1;
    for (const poly of polys) { const ring = poly[0]; if (!ring || ring.length < 3) continue; let a = 0, cx = 0, cy = 0;
      for (let k = 0, j = ring.length - 1; k < ring.length; j = k++) { const f = ring[j][0] * ring[k][1] - ring[k][0] * ring[j][1]; a += f; cx += (ring[j][0] + ring[k][0]) * f; cy += (ring[j][1] + ring[k][1]) * f; }
      if (Math.abs(a) > ba) { ba = Math.abs(a); best = a ? [cx / (3 * a), cy / (3 * a)] : ring[0]; } }
    return best;
  }

  /* ---------- 표시물 ---------- */
  function clear() { marks.forEach(m => m.remove()); marks = []; pins.forEach(m => m.remove()); pins = []; host.classList.remove('gl-world', 'gl-region', 'gl-route', 'gl-korea'); }
  function mk(lnglat, el, anchor = 'center', offset = [0, 0], list = marks) { const m = new maplibregl.Marker({ element: el, anchor, offset }).setLngLat(lnglat).addTo(map); list.push(m); return m; }
  function btn(cls, html, onClick) { const el = document.createElement('button'); el.type = 'button'; el.className = cls; el.innerHTML = html;
    el.addEventListener('click', ev => { ev.stopPropagation(); onClick && onClick(); }); return el; }
  function zoomClass() {
    if (!host || !map) return; const z = map.getZoom();
    host.classList.toggle('gl-lbl-off', mode === 'region' && !ctx.district && z < 12.6);
    host.classList.toggle('gl-minor-off', mode === 'world' && z < minorZ);
  }
  function regionBadge(r, html, minor, onClick) {
    const el = btn('glreg' + (minor ? ' minor' : ''), `<span class="m-label region">${html}</span><i class="rdot"></i>`, onClick);
    mk([REGIONS[r].lng, REGIONS[r].lat], el, 'bottom', [0, 9]);
  }
  function begin(m, opts, extra) { gen++; ctx = Object.assign({}, opts || {}, extra || {}); mode = m; clear(); host.classList.add('gl-' + m); setLabels(); }

  /* ---------- 한국 전체 ---------- */
  function showKorea(opts) {
    begin('korea', opts);
    for (const r of KR_IDS) {
      const n = PLACES.filter(x => x.r === r).length, f = S.saved.filter(id => PBY[id].r === r).length;
      regionBadge(r, `${esc(rn(r))}<small>${T.spots(n)}${f ? ` · <span class="hrt">♥${f}</span>` : ''}</small>`, false, () => ctx.onRegion(r));
    }
    whenReady(() => { setData('kl-area', fcOf([])); setData('kl-route', fcOf([])); });
    fit(KR_BOX, 8, 4); zoomClass();
  }

  /* ---------- 해외 전체 ---------- */
  const OV_TOP = new Set(['tokyo', 'osaka', 'fukuoka', 'sapporo', 'okinawa', 'taipei', 'hongkong', 'shanghai', 'hanoi', 'danang', 'hochiminh', 'bangkok', 'singapore', 'kualalumpur', 'cebu', 'guam']);
  function showWorld(opts) {
    begin('world', opts);
    for (const r of OV_IDS) {
      const f = S.saved.filter(id => PBY[id].r === r).length;
      regionBadge(r, `${esc(rn(r))}${f ? `<small><span class="hrt">♥${f}</span></small>` : ''}`, !OV_TOP.has(r) && !f, () => ctx.onRegion(r));
    }
    whenReady(() => { setData('kl-area', fcOf([])); setData('kl-route', fcOf([])); });
    fit(bbox(OV_IDS.map(r => [REGIONS[r].lng, REGIONS[r].lat])), 6, 6);
    minorZ = map.getZoom() + 0.7; zoomClass();
  }

  /* ---------- 지역 (구역 + 장소 핀) ---------- */
  function showRegion(r, opts) {
    begin('region', opts, { r });
    const reg = GEO.regions[r];
    let rp = PLACES.filter(p => p.r === r && !p.far); if (!rp.length) rp = PLACES.filter(p => p.r === r);
    const focus = ctx.district && reg.districts.find(d => d.id === ctx.district);
    // 구역 이름
    for (const d of reg.districts) {
      const c = centroid(d.g); if (!c || !isFinite(c[0])) continue; const sv2 = d.ids.filter(isSaved).length;
      mk(c, btn('m-label district gldist' + (d.id === ctx.district ? ' on' : ''), `${esc(tr4(d.n))}<small>${T.spots(d.ids.length)}${sv2 ? ` · <span class="hrt">♥${sv2}</span>` : ''}</small>`, () => ctx.onDistrict && ctx.onDistrict(d.id)), 'center');
    }
    drawPins();
    whenReady(() => { area(); setData('kl-route', fcOf([])); });
    if (focus) fit(bbox(polysPts(focus.g)), 16, 10);
    else fit(bbox(rp.map(p => [p.lng, p.lat]), 0.02), 14.5, 4);
    if (ctx.sel && PBY[ctx.sel]) { const p = PBY[ctx.sel]; if (!map.getBounds().contains([p.lng, p.lat])) focusOn(p.lat, p.lng); }
    zoomClass();
  }
  function area() {
    if (mode !== 'region') return;
    const reg = GEO.regions[ctx.r];
    setData('kl-area', fcOf(reg.districts.map(d => ({ type: 'Feature', properties: { id: d.id, on: d.id === ctx.district, saved: d.ids.some(isSaved) }, geometry: { type: 'MultiPolygon', coordinates: d.g } }))));
  }
  function drawPins() {
    pins.forEach(m => m.remove()); pins = [];
    const r = ctx.r, fl = ctx.filter && ctx.filter !== 'all' ? ctx.filter : null;
    const list = PLACES.filter(p => p.r === r && (!fl || p.c === fl) && (!ctx.district || p.dist === ctx.district || isSaved(p.id) || p.id === ctx.sel))
      .sort((a, b) => ((a.id === ctx.sel) - (b.id === ctx.sel)) || (isSaved(a.id) - isSaved(b.id)));
    for (const p of list) {
      const sel = p.id === ctx.sel, sv = isSaved(p.id);
      const el = btn('glpin' + (sel ? ' sel' : '') + (sv ? ' saved keep' : '') + (ctx.district ? ' keep' : ''),
        `<span class="dot" style="background:${CATS[p.c].col}">${catIcon(p.c)}</span>${sv ? '<span class="hb">♥</span>' : ''}<span class="lb">${esc(pn(p.id))}</span>`,
        () => ctx.onPlace && ctx.onPlace(p.id));
      el.setAttribute('aria-label', pn(p.id));
      mk([p.lng, p.lat], el, 'center', [0, 0], pins);
    }
  }
  function refresh(opts) { Object.assign(ctx, opts || {}); if (mode === 'region') { drawPins(); whenReady(area); zoomClass(); } }

  /* ---------- 하루 동선 ---------- */
  function showRoute(plan, i, opts) {
    begin('route', Object.assign({ noSheet: true }, opts || {}));
    const day = plan.days[i], r = day.r, sc = scheduleDay(plan, i), stay = STAY_BY[plan.stays[r]], col = LINE[i % LINE.length];
    const pts = [{ k: 'stay', lat: stay.lat, lng: stay.lng }];
    sc.rows.forEach(o => { const id = o.e.id; if (id && PBY[id].r === r) pts.push({ k: o.e.k, id, n: o.num, lat: PBY[id].lat, lng: PBY[id].lng }); });
    const line = [...pts.map(p => [p.lng, p.lat]), [stay.lng, stay.lat]];
    const wide = host.getBoundingClientRect().width >= 520;
    mk([stay.lng, stay.lat], btn('glstay', ICONS.house + (wide ? `<span class="lb">${esc(sn(stay.id))}</span>` : '')), 'center');
    pts.slice(1).forEach(p => { const el = btn('glnum' + (p.k === 'meal' ? ' meal' : ''), `${p.n || ''}${wide ? `<span class="lb">${esc(pn(p.id))}</span>` : ''}`, () => ctx.onPlace && ctx.onPlace(p.id));
      el.style.setProperty('--lc0', col); mk([p.lng, p.lat], el, 'center'); });
    whenReady(() => { setData('kl-area', fcOf([])); setData('kl-route', { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: line } }); map.setPaintProperty('kl-route', 'line-color', col); });
    fit(bbox(line, 0.012), 15, 8);
  }

  /* ---------- 카메라 ---------- */
  function focusOn(lat, lng, k) {
    if (!map) return; const p = pads();
    map.easeTo({ center: [lng, lat], zoom: Math.max(map.getZoom(), k ? 14.2 : 13.6), offset: [(p.left - p.right) / 2, (p.top - p.bottom) / 2], duration: 600 });
  }
  function zoomBy(f) { if (map) map.easeTo({ zoom: map.getZoom() + Math.log2(f), duration: 250 }); }
  function onResize() { if (map) map.resize(); }
  return { ok, thumb: r => Map2DSvg.thumb(r), mount, showKorea, showWorld, showRegion, showRoute, refresh, focusOn, zoomBy, onResize,
    get mode() { return mode; }, get host() { return host; }, get map() { return map; } };
})();
// 실제 지도를 쓸 수 있으면 MapGL, 아니면 그림 지도
let Map2D = MapGL.ok ? MapGL : Map2DSvg;
