'use strict';
/* =========================================================
<<<<<<< HEAD
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
=======
   실제 지도 (2026-11-12 K링크 2단계): MapLibre GL + OpenFreeMap(OSM) 타일, 키·요금 없음.
   Map2D 와 같은 함수(mount·showKorea·showWorld·showRegion·showRoute·refresh·focusOn·zoomBy·set3d)를 내놓는다.
   WebGL이 없거나 지도 스타일을 못 받으면 예전 SVG 지도(MapSVG)로 자동 전환한다.
   ========================================================= */
const MapGL = (() => {
  const STYLE = 'https://tiles.openfreemap.org/styles/liberty';
  const FONT = '"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR","Noto Sans CJK KR","PingFang SC","Hiragino Sans",sans-serif';
  const insts = new Map();
  let I = null, mode = null, ctx = {};
  const EMPTY = { type: 'FeatureCollection', features: [] };

  function create(el) {
    el.innerHTML = '';
    const map = new maplibregl.Map({ container: el, style: STYLE, center: [127.8, 36.2], zoom: 6, attributionControl: { compact: true },
      dragRotate: false, pitchWithRotate: false, localIdeographFontFamily: FONT, fadeDuration: 0, maxPitch: 65 });
    map.touchZoomRotate.disableRotation();
    const inst = { el, map, ready: false, queue: null, markers: [], lang: null, is3d: false };
    map.once('style.load', () => {
      inst.ready = true; addLayers(inst);
      const q = inst.queue; inst.queue = null; if (q) q();
    });
    map.on('error', e => { if (!inst.ready && e && e.error && /style|Failed to fetch|NetworkError/i.test(String(e.error.message || e.error))) glFail(); });
    map.on('click', e => { const t = e.originalEvent && e.originalEvent.target; if (t && t.closest && t.closest('.gm')) return; if (I === inst && ctx.onBg) ctx.onBg(); });
    map.on('zoom', () => { if (I === inst) labelVis(); });
    map.on('click', 'dist-fill', e => { if (I !== inst || mode !== 'region' || !ctx.onDistrict) return; const t = e.originalEvent && e.originalEvent.target; if (t && t.closest && t.closest('.gm')) return;
      const f = e.features && e.features[0]; if (f && f.properties.id !== ctx.district && map.getZoom() < 13) ctx.onDistrict(f.properties.id); });
    insts.set(el, inst);
    return inst;
  }
  function addLayers(inst) {
    const m = inst.map;
    m.addSource('dist', { type: 'geojson', data: EMPTY }); m.addSource('route', { type: 'geojson', data: EMPTY });
    m.addLayer({ id: 'dist-fill', type: 'fill', source: 'dist', paint: { 'fill-color': ['case', ['get', 'on'], '#2443E8', ['get', 'saved'], '#FF4F7B', '#2443E8'], 'fill-opacity': ['case', ['get', 'on'], 0.1, ['get', 'saved'], 0.06, 0.035] } });
    m.addLayer({ id: 'dist-line', type: 'line', source: 'dist', paint: { 'line-color': ['case', ['get', 'on'], '#2443E8', '#7F92EE'], 'line-width': ['case', ['get', 'on'], 2.2, 1.3], 'line-opacity': 0.7, 'line-dasharray': [3, 2] } });
    m.addLayer({ id: 'route-case', type: 'line', source: 'route', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': '#fff', 'line-width': 8, 'line-opacity': 0.9 } });
    m.addLayer({ id: 'route-line', type: 'line', source: 'route', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': ['get', 'c'], 'line-width': 4.5 } });
  }
  function setLabels(inst) {
    if (inst.lang === S.lang) return; inst.lang = S.lang;
    const L = S.lang, m = inst.map;
    for (const l of m.getStyle().layers) {
      if (l.type !== 'symbol' || !l.layout || !l.layout['text-field']) continue;
      if (!JSON.stringify(l.layout['text-field']).includes('name')) continue;
      try { m.setLayoutProperty(l.id, 'text-field', ['coalesce', ['get', 'name:' + L], ['get', 'name:' + (L === 'zh' ? 'zh-Hans' : L)], ['get', 'name']]); } catch (e) {}
    }
  }
  function glOK() {
    if (!window.maplibregl) return false;
    try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; }
  }
  function mount(el) {
    for (const [k, v] of insts) if (!k.isConnected) { try { v.map.remove(); } catch (e) {} insts.delete(k); }
    I = insts.get(el) || create(el);
    requestAnimationFrame(() => { if (I && I.el === el) I.map.resize(); });
  }
  const run = f => { const inst = I; if (inst.ready) { setLabels(inst); f(inst); } else inst.queue = () => { setLabels(inst); f(inst); }; };
  function clear(inst) { inst.markers.forEach(mk => mk.remove()); inst.markers = []; inst.map.getSource('dist').setData(EMPTY); inst.map.getSource('route').setData(EMPTY); }
  function marker(inst, lng, lat, el, anchor = 'center', offset) {
    const mk = new maplibregl.Marker({ element: el, anchor, offset }).setLngLat([lng, lat]).addTo(inst.map); inst.markers.push(mk); return mk;
  }
  const mkEl = (tag, cls, html, onClick) => { const el = document.createElement(tag); el.className = 'gm ' + cls; el.innerHTML = html;
    if (onClick) el.addEventListener('click', ev => { ev.stopPropagation(); onClick(); }); return el; };
  function pads() {
    const r = I.el.getBoundingClientRect(), desk = window.innerWidth >= 980;
    const sheet = desk || ctx.noSheet ? 0 : (parseFloat(getComputedStyle(document.getElementById('app')).getPropertyValue('--sheet-px')) || r.height * 0.38);
    const t = Math.min(desk ? 90 : 116, r.height * .25), b = Math.min(sheet + 24, Math.max(24, r.height - t - 120));
    return { top: ctx.top != null ? ctx.top + 20 : t, bottom: b, left: 28, right: desk ? 76 : 56 };
  }
  const bboxOf = pts => { const b = new maplibregl.LngLatBounds(); pts.forEach(p => b.extend([p[0], p[1]])); return b; };
  function fit(pts, maxZoom, dur = 600) { if (!pts.length) return; I.map.fitBounds(bboxOf(pts), { padding: pads(), maxZoom, duration: dur, pitch: I.is3d ? 55 : 0 }); }
  function labelVis() {
    if (!I) return; const z = I.map.getZoom(), mob = window.innerWidth < 980;
    I.el.classList.toggle('gl-lbl-off', mode === 'region' && !ctx.district && z < (mob ? 13.2 : 12.4));
    I.el.classList.toggle('gl-minor-off', mode === 'world' && z < 4.6);
    I.el.classList.toggle('gl-dist-off', mode === 'region' && z >= 13.6);
  }

  /* ---------- 한국 전체 ---------- */
  function showKorea(opts) {
    ctx = opts || {}; mode = 'korea';
    run(inst => { clear(inst); set3dRaw(inst, false);
      for (const r of KR_IDS) { const n = PLACES.filter(x => x.r === r).length, f = S.saved.filter(id => PBY[id].r === r).length;
        marker(inst, REGIONS[r].lng, REGIONS[r].lat, mkEl('button', 'g-reg', `<i></i><span>${esc(rn(r))}<small>${T.spots(n)}${f ? ` · <span class="hrt">♥${f}</span>` : ''}</small></span>`, () => ctx.onRegion(r)), 'left', [-9, 0]); }
      fit([[124.9, 33.1], [130.9, 38.4]], 7.2, 0); labelVis(); });
  }
  /* ---------- 해외 전체 ---------- */
  const OV_TOP = new Set(['tokyo', 'osaka', 'fukuoka', 'sapporo', 'okinawa', 'taipei', 'hongkong', 'shanghai', 'hanoi', 'danang', 'hochiminh', 'bangkok', 'singapore', 'kualalumpur', 'cebu', 'guam']);
  function showWorld(opts) {
    ctx = opts || {}; mode = 'world';
    run(inst => { clear(inst); set3dRaw(inst, false);
      for (const r of OV_IDS) { const f = S.saved.filter(id => PBY[id].r === r).length;
        marker(inst, REGIONS[r].lng, REGIONS[r].lat, mkEl('button', 'g-reg sm' + (OV_TOP.has(r) || f ? '' : ' minor'), `<i></i><span>${esc(rn(r))}${f ? `<small><span class="hrt">♥${f}</span></small>` : ''}</span>`, () => ctx.onRegion(r)), 'left', [-7, 0]); }
      fit(OV_IDS.map(r => [REGIONS[r].lng, REGIONS[r].lat]), 6, 0); labelVis(); });
  }
  /* ---------- 지역·구역 ---------- */
  const ringPts = g => g.flat(2);
  function showRegion(r, opts) {
    ctx = Object.assign({}, opts || {}, { r }); mode = 'region';
    run(inst => { draw(inst, r, true); });
  }
  function draw(inst, r, refit) {
    clear(inst);
    const reg = GEO.regions[r], fl = ctx.filter && ctx.filter !== 'all' ? ctx.filter : null;
    inst.map.getSource('dist').setData({ type: 'FeatureCollection', features: reg.districts.map(d => ({ type: 'Feature', properties: { id: d.id, on: d.id === ctx.district, saved: d.ids.some(isSaved) }, geometry: { type: 'MultiPolygon', coordinates: d.g } })) });
    // 구역 이름은 지도에 띄우지 않는다(핀과 겹침) — 패널의 '구역 둘러보기'와 점선 구역으로 고른다
>>>>>>> ad291fab (K링크 2단계: 실제 지도(MapLibre+OpenFreeMap, 3D 건물)로 전환하고 3D 거리 모형 제거, 시작 화면에서 여행 유형(국내 여행·해외 여행·한국 방문) 고르기, 국내 여행은 KTX역 출발·도착으로 일정)
    const list = PLACES.filter(p => p.r === r && (!fl || p.c === fl) && (!ctx.district || p.dist === ctx.district || isSaved(p.id) || p.id === ctx.sel))
      .sort((a, b) => ((a.id === ctx.sel) - (b.id === ctx.sel)) || (isSaved(a.id) - isSaved(b.id)));
    for (const p of list) {
      const sel = p.id === ctx.sel, sv = isSaved(p.id);
<<<<<<< HEAD
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
=======
      const el = mkEl('button', 'g-pin' + (sel ? ' on' : '') + (sv ? ' saved' : ''), `<span class="d" style="--c:${CATS[p.c].col}">${catIcon(p.c)}${sv ? '<em>♥</em>' : ''}</span><span class="lb">${esc(pn(p.id))}</span>`, () => ctx.onPlace && ctx.onPlace(p.id));
      el.setAttribute('aria-label', pn(p.id));
      const mk = marker(inst, p.lng, p.lat, el, 'top', [0, -15]); if (sel) mk.getElement().style.zIndex = 5; else if (sv) mk.getElement().style.zIndex = 3;
    }
    if (refit) {
      const focus = ctx.district && reg.districts.find(d => d.id === ctx.district);
      if (focus) fit(ringPts(focus.g), 15.5);
      else { let rp = PLACES.filter(p => p.r === r && !p.far); if (!rp.length) rp = PLACES.filter(p => p.r === r); fit(rp.map(p => [p.lng, p.lat]), 14); }
      if (ctx.sel && PBY[ctx.sel]) setTimeout(() => focusOn(PBY[ctx.sel].lat, PBY[ctx.sel].lng), 650);
    }
    labelVis();
  }
  function refresh(opts) { Object.assign(ctx, opts || {}); if (mode === 'region' && I) run(inst => draw(inst, ctx.r, false)); }

  /* ---------- 날짜별 동선 ---------- */
  function showRoute(plan, i, opts) {
    ctx = Object.assign({ noSheet: true }, opts || {}); mode = 'route';
    run(inst => { clear(inst);
      const day = plan.days[i], r = day.r, sc = scheduleDay(plan, i), stay = STAY_BY[plan.stays[r]], col = LINE[i % LINE.length];
      const pts = [{ k: 'stay', lat: stay.lat, lng: stay.lng }];
      sc.rows.forEach(o => { const id = o.e.id; if (id && PBY[id].r === r) pts.push({ k: o.e.k, id, n: o.num, lat: PBY[id].lat, lng: PBY[id].lng }); });
      inst.map.getSource('route').setData({ type: 'Feature', properties: { c: col }, geometry: { type: 'LineString', coordinates: [...pts, pts[0]].map(p => [p.lng, p.lat]) } });
      marker(inst, stay.lng, stay.lat, mkEl('div', 'g-stay', `${ICONS.house}<span class="lb">${esc(sn(stay.id))}</span>`), 'center');
      for (const p of pts.slice(1)) {
        const el = mkEl('button', 'g-num' + (p.k === 'meal' ? ' meal' : ''), `<b style="--c:${col}">${p.n || ''}</b><span class="lb">${esc(pn(p.id))}</span>`, () => selectPlace(p.id));
        marker(inst, p.lng, p.lat, el, 'center');
      }
      fit(pts.map(p => [p.lng, p.lat]), 15); labelVis(); });
  }

  /* ---------- 카메라 ---------- */
  function focusOn(lat, lng, k) { if (!I) return; const z = Math.max(I.map.getZoom(), k ? 12 + k : 14.2); I.map.easeTo({ center: [lng, lat], zoom: Math.min(z, 16.5), padding: pads(), duration: 600 }); }
  function zoomBy(f) { if (I) I.map.easeTo({ zoom: I.map.getZoom() + Math.log2(f), duration: 280 }); }
  function onResize() { if (I) I.map.resize(); }
  function set3dRaw(inst, on) {
    const m = inst.map; inst.is3d = on;
    if (on && !m.getLayer('bld3d')) {
      const src = Object.keys(m.getStyle().sources).find(s => m.getStyle().sources[s].type === 'vector');
      if (src) m.addLayer({ id: 'bld3d', type: 'fill-extrusion', source: src, 'source-layer': 'building', minzoom: 13,
        paint: { 'fill-extrusion-color': '#E3E7F0', 'fill-extrusion-height': ['coalesce', ['get', 'render_height'], 8], 'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0], 'fill-extrusion-opacity': 0.88 } }, 'dist-fill');
    }
    if (m.getLayer('bld3d')) m.setLayoutProperty('bld3d', 'visibility', on ? 'visible' : 'none');
  }
  function set3d(on) {
    if (!I) return; run(inst => { set3dRaw(inst, on);
      inst.map.easeTo({ pitch: on ? 55 : 0, zoom: on ? Math.max(inst.map.getZoom(), 15) : inst.map.getZoom(), padding: pads(), duration: 800 }); });
  }
  return { glOK, mount, showKorea, showWorld, showRegion, showRoute, refresh, focusOn, zoomBy, onResize, set3d, gl: true,
    get mode() { return mode; }, get host() { return I && I.el; } };
})();

// 지도 선택: 실제 지도를 쓰고, 안 되면 SVG 지도로. 둘 다 같은 함수 이름을 쓴다.
let USE_GL = MapGL.glOK();
function glFail() { if (!USE_GL) return; USE_GL = false; console.warn('K링크: 실제 지도를 불러오지 못해 기본 지도로 바꿉니다.'); try { stageKey = ''; renderStage(true); } catch (e) {} }
const Map2D = new Proxy({}, { get: (_, k) => k === 'thumb' ? MapSVG.thumb : k === 'gl' ? USE_GL : k === 'set3d' ? (USE_GL ? MapGL.set3d : () => {}) : (USE_GL ? MapGL : MapSVG)[k] });
>>>>>>> ad291fab (K링크 2단계: 실제 지도(MapLibre+OpenFreeMap, 3D 건물)로 전환하고 3D 거리 모형 제거, 시작 화면에서 여행 유형(국내 여행·해외 여행·한국 방문) 고르기, 국내 여행은 KTX역 출발·도착으로 일정)
