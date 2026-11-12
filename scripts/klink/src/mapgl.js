'use strict';
/* =========================================================
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
  // 지도 글자: 고른 언어 이름이 있는 것만 보여 준다(외국어 글자가 잔뜩 깔리지 않게).
  // 한국 지도를 한국어로 볼 때는 원래 이름(한글)을 쓰고, 영어는 로마자 이름으로 채운다. 나라·도시 이름만 예외로 로마자를 보탠다.
  function setLabels(inst) {
    const L = S.lang, kr = mode === 'korea' || (ctx.r && REGIONS[ctx.r] && !isOv(ctx.r));
    const key = L + (kr ? ':kr' : ':ov'); if (inst.lang === key) return; inst.lang = key;
    const m = inst.map, nm = ['get', 'name:' + L], loose = L === 'en' || (L === 'ko' && kr);
    inst.filt = inst.filt || {};
    for (const l of m.getStyle().layers) {
      if (l.type !== 'symbol' || !l.layout || !l.layout['text-field']) continue;
      if (!JSON.stringify(l.layout['text-field']).includes('name')) continue;
      const city = /country|state|city|capital|continent|town/.test(l.id), poi = /poi|transit|airport|aerialway/.test(l.id);
      let tf;
      if (L === 'en') tf = ['coalesce', nm, ['get', 'name_en'], ['get', 'name:latin'], ['get', 'name']];
      else if (loose) tf = ['coalesce', nm, ['get', 'name']];
      else tf = city ? ['coalesce', nm, ['get', 'name:latin'], ['get', 'name']] : ['coalesce', nm, ''];
      try { m.setLayoutProperty(l.id, 'text-field', tf); } catch (e) {}
      if (poi) {   // 고른 언어 이름이 없는 가게·정류장은 아이콘째 숨긴다
        if (!(l.id in inst.filt)) inst.filt[l.id] = m.getFilter(l.id) || null;
        const base = inst.filt[l.id];
        try { m.setFilter(l.id, loose ? base : (base ? ['all', base, ['has', 'name:' + L]] : ['has', 'name:' + L])); } catch (e) {}
      }
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
    const list = PLACES.filter(p => p.r === r && (!fl || p.c === fl) && (!ctx.district || p.dist === ctx.district || isSaved(p.id) || p.id === ctx.sel))
      .sort((a, b) => ((a.id === ctx.sel) - (b.id === ctx.sel)) || (isSaved(a.id) - isSaved(b.id)));
    for (const p of list) {
      const sel = p.id === ctx.sel, sv = isSaved(p.id);
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
    ctx = Object.assign({ noSheet: true }, opts || {}, { r: plan.days[i].r }); mode = 'route';
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
