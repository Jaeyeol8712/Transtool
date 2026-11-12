'use strict';
/* =========================================================
   2D maps (d3): Korea overview, region/district map with pins, day route map
   Planar projection: x = lng*cos(lat0), y = lat (no spherical winding issues)
   ========================================================= */
<<<<<<< HEAD
const Map2DSvg = (() => {
=======
const MapSVG = (() => {
>>>>>>> ad291fab (K링크 2단계: 실제 지도(MapLibre+OpenFreeMap, 3D 건물)로 전환하고 3D 거리 모형 제거, 시작 화면에서 여행 유형(국내 여행·해외 여행·한국 방문) 고르기, 국내 여행은 KTX역 출발·도착으로 일정)
  let host = null, svg, gW, gPins, layer, zoom, proj, lat0 = 36, mode = null, ctx = {}, T0 = null, pinData = [], labData = [];
  const K = () => Math.cos(lat0 * Math.PI / 180);
  const P = (lng, lat) => proj([lng * K(), lat]);
  const polyFeat = polys => ({ type: 'Feature', geometry: { type: 'MultiPolygon', coordinates: polys.map(poly => poly.map(ring => ring.map(([x, y]) => [x * K(), y]))) } });
  const ringsFeat = rings => polyFeat(rings.map(r => [r]));
  const path = () => d3.geoPath(proj);

  function mount(el) {
    if (host === el && svg) return;
    host = el; el.innerHTML = '';
    const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); s.setAttribute('class', 'mapsvg'); el.appendChild(s);
    layer = document.createElement('div'); layer.className = 'mlayer'; el.appendChild(layer);
    svg = d3.select(s);
    svg.append('rect').attr('class', 'sea').attr('x', -5000).attr('y', -5000).attr('width', 20000).attr('height', 20000).attr('fill', 'var(--sea)');
    gW = svg.append('g'); gPins = svg.append('g');
    zoom = d3.zoom().scaleExtent([1, 18]).on('zoom', ev => { T0 = ev.transform; gW.attr('transform', T0); place(); });
    svg.call(zoom).on('dblclick.zoom', null);
    svg.on('click', ev => { if (ev.target === s || ev.target.classList.contains('sea') || ev.target.classList.contains('land')) ctx.onBg && ctx.onBg(); });
  }
  function size() { const r = host.getBoundingClientRect(); return [Math.max(200, r.width), Math.max(200, r.height)]; }
  function pads() { const [w, h] = size(); const desk = window.innerWidth >= 980; const sheet = desk ? 0 : (parseFloat(getComputedStyle(document.getElementById('app')).getPropertyValue('--sheet-px')) || h * 0.38);
    return { t: desk ? 90 : 116, b: (ctx.noSheet ? 24 : sheet + 20), l: 24, r: desk ? 76 : 64, w, h }; }
  function fit(fc, extraPad = 0) {
    const p = pads();
    proj = d3.geoIdentity().reflectY(true).fitExtent([[p.l + extraPad, p.t + extraPad], [p.w - p.r - extraPad, Math.max(p.t + 120, p.h - p.b - extraPad)]], fc);
    T0 = d3.zoomIdentity; svg.call(zoom.transform, T0);
  }
  const fc = feats => ({ type: 'FeatureCollection', features: feats });
  const tp = xy => T0 ? T0.apply(xy) : xy;

  /* ---------- overlay positioning ---------- */
  function place() {
    if (!gPins) return;
    gPins.classed('pins-small', mode === 'region' && !ctx.district && (T0 ? T0.k : 1) < 2.4);
    gPins.selectAll('g.pin').attr('transform', d => { const [x, y] = tp(d.xy); return `translate(${x},${y})`; });
    gPins.selectAll('path.route').attr('d', d => d3.line()(d.map(tp)));
    // labels with collision
    const [w, h] = size(), shown = [];
    const k = T0 ? T0.k : 1;
    const arr = labData.slice().sort((a, b) => b.pri - a.pri);
    for (const L of arr) {
      const [x, y] = tp(L.xy); const vis = L.minK == null || k >= L.minK || L.pri >= 3;
      const bw = L.el.offsetWidth || 80, bh = L.el.offsetHeight || 26;
      const rx = x - bw / 2, ry = y - bh - (L.dy || 0);
      let ok = vis && x > -40 && x < w + 40 && y > 0 && y < h + 40;
      if (ok) for (const R of shown) if (rx < R.x + R.w + 4 && rx + bw + 4 > R.x && ry < R.y + R.h + 2 && ry + bh + 2 > R.y) { ok = false; break; }
      L.el.style.transform = `translate(${x}px,${y - (L.dy || 0)}px) translate(-50%,-100%)`;
      L.el.style.visibility = ok ? 'visible' : 'hidden';
      if (ok) shown.push({ x: rx, y: ry, w: bw, h: bh });
    }
  }
  function addLabel(xy, html, cls, pri, opts = {}) {
    const el = document.createElement(opts.button ? 'button' : 'div'); el.className = 'm-label ' + (cls || ''); el.innerHTML = html;
    el.style.left = '0'; el.style.top = '0'; el.style.transform = 'translate(-9999px,0)';
    if (opts.onClick) el.addEventListener('click', ev => { ev.stopPropagation(); opts.onClick(); });
    layer.appendChild(el); labData.push({ xy, el, pri, minK: opts.minK, dy: opts.dy });
  }
  function clearOverlay() { gW.selectAll('*').remove(); gPins.selectAll('*').remove(); layer.innerHTML = ''; labData = []; pinData = []; }

  function pinG(sel) {
    const g = sel.append('g').attr('class', d => 'pin' + (d.sel ? ' sel' : '') + (d.sel || d.saved ? ' keep' : '')).style('cursor', 'pointer');
    g.append('circle').attr('class', 'dot').attr('r', 5.5).attr('fill', d => d.col).attr('stroke', '#fff').attr('stroke-width', 1.8);
    const bg = g.append('g').attr('class', 'big');
    bg.append('circle').attr('r', d => d.sel ? 22 : 0).attr('fill', 'rgba(36,67,232,.16)');
    bg.append('circle').attr('r', d => d.sel ? 17 : 13).attr('fill', d => d.col).attr('stroke', '#fff').attr('stroke-width', 2.5)
      .style('filter', 'drop-shadow(0 2px 3px rgba(20,26,46,.3))');
    bg.each(function (d) { const s = d.sel ? 18 : 14; d3.select(this).append('g').attr('transform', `translate(${-s / 2},${-s / 2})`).html(d.icon.replace('<svg ', `<svg width="${s}" height="${s}" color="#fff" `)); });
    g.filter(d => d.saved).append('circle').attr('cx', d => d.sel ? 13 : 10).attr('cy', d => d.sel ? -13 : -10).attr('r', 7).attr('fill', '#FF4F7B').attr('stroke', '#fff').attr('stroke-width', 2);
    g.filter(d => d.saved).append('path').attr('d', 'M0 2.6s-3.2-2-3.2-4.3a1.8 1.8 0 0 1 3.2-1.1 1.8 1.8 0 0 1 3.2 1.1C3.2 .6 0 2.6 0 2.6Z')
      .attr('transform', d => `translate(${d.sel ? 13 : 10},${d.sel ? -12.5 : -9.5}) scale(.85)`).attr('fill', '#fff');
    g.on('click', (ev, d) => { ev.stopPropagation(); d.onClick && d.onClick(); });
    return g;
  }

  /* ---------- Korea ---------- */
  function showKorea(opts) {
    ctx = opts || {}; mode = 'korea'; lat0 = 36; clearOverlay(); zoom.scaleExtent([1, 18]);
    const land = ringsFeat(GEO.korea);
    fit(fc([land]), 8);
    gW.append('path').datum(land).attr('class', 'land').attr('d', path()).attr('fill', 'var(--land)').attr('stroke', '#D3DAE8').attr('stroke-width', 1).attr('vector-effect', 'non-scaling-stroke').attr('fill-rule', 'evenodd')
      .style('filter', 'drop-shadow(0 6px 0 #BCCAEA)');
    const pins = KR_IDS.map(r => ({ r, xy: P(REGIONS[r].lng, REGIONS[r].lat) }));
    const g = gPins.selectAll('g.pin').data(pins.map(p => Object.assign(p, { col: '#2443E8', icon: ICONS.pin, onClick: () => ctx.onRegion(p.r) }))).join(enter => {
      const gg = enter.append('g').attr('class', 'pin').style('cursor', 'pointer');
      gg.append('circle').attr('r', 16).attr('fill', 'rgba(36,67,232,.14)');
      gg.append('circle').attr('r', 8).attr('fill', '#2443E8').attr('stroke', '#fff').attr('stroke-width', 3);
      gg.on('click', (ev, d) => { ev.stopPropagation(); d.onClick(); }); return gg; });
    for (const p of pins) {
      const n = PLACES.filter(x => x.r === p.r).length, f = S.saved.filter(id => PBY[id].r === p.r).length;
      addLabel(p.xy, `${esc(rn(p.r))}<small>${T.spots(n)}${f ? ` · <span class="hrt">♥${f}</span>` : ''}</small>`, 'region', 2, { button: true, dy: 14, onClick: () => ctx.onRegion(p.r) });
    }
    place();
  }

  /* ---------- 해외 전체 (동아시아·동남아·괌·사이판) ---------- */
  const OV_TOP = new Set(['tokyo', 'osaka', 'fukuoka', 'sapporo', 'okinawa', 'taipei', 'hongkong', 'shanghai', 'hanoi', 'danang', 'hochiminh', 'bangkok', 'singapore', 'kualalumpur', 'cebu', 'guam']);
  function showWorld(opts) {
    ctx = opts || {}; mode = 'world'; lat0 = 24; clearOverlay(); zoom.scaleExtent([1, 18]);
    const land = ringsFeat(GEO.world || []);
    const la = OV_IDS.map(r => REGIONS[r].lat), lo = OV_IDS.map(r => REGIONS[r].lng);
    const a0 = Math.min(...la) - 2.5, a1 = Math.max(...la) + 2.5, o0 = Math.min(...lo) - 2.5, o1 = Math.max(...lo) + 2.5;
    fit(fc([polyFeat([[[[o0, a0], [o1, a0], [o1, a1], [o0, a1], [o0, a0]]]])]), 0);
    gW.append('path').datum(land).attr('class', 'land').attr('d', path()).attr('fill', 'var(--land)').attr('stroke', '#D3DAE8').attr('stroke-width', 1).attr('vector-effect', 'non-scaling-stroke').attr('fill-rule', 'evenodd');
    const pins = OV_IDS.map(r => ({ r, xy: P(REGIONS[r].lng, REGIONS[r].lat) }));
    gPins.selectAll('g.pin').data(pins.map(p => Object.assign(p, { onClick: () => ctx.onRegion(p.r) }))).join(enter => {
      const gg = enter.append('g').attr('class', 'pin').style('cursor', 'pointer');
      gg.append('circle').attr('r', 13).attr('fill', 'rgba(36,67,232,.14)');
      gg.append('circle').attr('r', 6.5).attr('fill', '#2443E8').attr('stroke', '#fff').attr('stroke-width', 2.5);
      gg.on('click', (ev, d) => { ev.stopPropagation(); d.onClick(); }); return gg; });
    for (const p of pins) {
      const f = S.saved.filter(id => PBY[id].r === p.r).length;
      addLabel(p.xy, `${esc(rn(p.r))}${f ? `<small><span class="hrt">♥${f}</span></small>` : ''}`, 'region', f ? 3 : OV_TOP.has(p.r) ? 2.2 : 1.6, { button: true, dy: 12, minK: OV_TOP.has(p.r) ? null : 1.5, onClick: () => ctx.onRegion(p.r) });
    }
    place();
  }

  /* ---------- region ---------- */
  function regionBase(r, faint) {
    const reg = GEO.regions[r];
    const neigh = polyFeat(reg.neigh), munis = reg.munis.map(m => Object.assign(polyFeat(m.g), { code: m.code }));
    gW.append('path').datum(neigh).attr('class', 'land').attr('d', path()).attr('fill', 'var(--land2)').attr('stroke', '#DCE2EC').attr('vector-effect', 'non-scaling-stroke').attr('fill-rule', 'evenodd');
    gW.selectAll('path.muni').data(munis).join('path').attr('class', 'land muni').attr('d', path()).attr('fill', faint ? '#F7F8FB' : 'var(--land)').attr('stroke', '#D5DCE9').attr('stroke-width', 1).attr('vector-effect', 'non-scaling-stroke').attr('fill-rule', 'evenodd');
    if (reg.water.length) gW.append('path').datum(polyFeat(reg.water)).attr('d', path()).attr('fill', 'var(--river)').attr('pointer-events', 'none');
    return { reg, munis };
  }
  function showRegion(r, opts) {
    ctx = Object.assign({}, opts || {}, { r }); mode = 'region'; lat0 = REGIONS[r].lat; clearOverlay();
    zoom.scaleExtent([PLACES.some(p => p.r === r && p.far) ? 0.08 : 1, 18]);   // 근교가 있는 도시는 더 멀리 축소할 수 있게
    const reg = GEO.regions[r];
    let rp = PLACES.filter(p => p.r === r && !p.far); if (!rp.length) rp = PLACES.filter(p => p.r === r);   // 근교(far)는 처음 화면 맞춤에서 뺀다
    const las = rp.map(p => p.lat), los = rp.map(p => p.lng);
    let a0 = Math.min(...las), a1 = Math.max(...las), o0 = Math.min(...los), o1 = Math.max(...los);
    const pa = Math.max(.012, (a1 - a0) * .16), po = Math.max(.015, (o1 - o0) * .16); a0 -= pa; a1 += pa; o0 -= po; o1 += po;
    const fitFeats = [polyFeat([[[[o0, a0], [o1, a0], [o1, a1], [o0, a1], [o0, a0]]]])];
    const focus = ctx.district && reg.districts.find(d => d.id === ctx.district);
    fit(fc(focus ? [polyFeat(focus.g)] : fitFeats), focus ? 20 : 4);
    regionBase(r, false);
    // districts
    const dfe = reg.districts.map(d => Object.assign(polyFeat(d.g), { d }));
    gW.selectAll('path.dist').data(dfe).join('path').attr('class', 'dist').attr('d', path())
      .attr('fill', f => f.d.id === ctx.district ? 'rgba(36,67,232,.12)' : (f.d.ids.some(isSaved) ? 'rgba(255,79,123,.07)' : 'rgba(36,67,232,.045)'))
      .attr('stroke', f => f.d.id === ctx.district ? '#2443E8' : '#9DAEF2').attr('stroke-width', f => f.d.id === ctx.district ? 2 : 1.2).attr('stroke-dasharray', f => f.d.kind === 'zone' ? '5 4' : null)
      .attr('vector-effect', 'non-scaling-stroke').style('cursor', 'pointer')
      .on('mouseenter', function () { d3.select(this).attr('fill', 'rgba(36,67,232,.13)'); })
      .on('mouseleave', function (ev, f) { d3.select(this).attr('fill', f.d.id === ctx.district ? 'rgba(36,67,232,.12)' : (f.d.ids.some(isSaved) ? 'rgba(255,79,123,.07)' : 'rgba(36,67,232,.045)')); })
      .on('click', (ev, f) => { ev.stopPropagation(); ctx.onDistrict && ctx.onDistrict(f.d.id); });
    // district labels
    for (const f of dfe) {
      const c = path().centroid(f); const sv2 = f.d.ids.filter(isSaved).length;
      addLabel(c, `${esc(tr4(f.d.n))}<small>${T.spots(f.d.ids.length)}${sv2 ? ` · <span class="hrt">♥${sv2}</span>` : ''}</small>`, 'district' + (f.d.id === ctx.district ? ' on' : ''), 2.1, { button: true, onClick: () => ctx.onDistrict && ctx.onDistrict(f.d.id) });
    }
    // muni names (faint) for orientation
    if (!focus) for (const m of reg.munis) { if (!m.n[0] || reg.districts.some(d => d.id === m.code)) continue; const c = path().centroid(polyFeat(m.g)); if (!isFinite(c[0])) continue;
      const el = document.createElement('div'); el.className = 'm-label'; el.style.cssText = 'background:none;box-shadow:none;color:#A3ABC0;font-weight:500;font-size:11px;pointer-events:none'; el.textContent = tr4(m.n);
      layer.appendChild(el); labData.push({ xy: c, el, pri: 0, minK: 1.6 }); }
    drawPins(r);
    place();
  }
  function drawPins(r) {
    gPins.selectAll('g.pin').remove(); labData = labData.filter(L => { if (L.pin) { L.el.remove(); return false; } return true; });
    const fl = ctx.filter && ctx.filter !== 'all' ? ctx.filter : null;
    const list = PLACES.filter(p => p.r === r && (!fl || p.c === fl) && (!ctx.district || p.dist === ctx.district || isSaved(p.id) || p.id === ctx.sel));
    const data = list.map(p => ({ id: p.id, xy: P(p.lng, p.lat), col: CATS[p.c].col, icon: catIcon(p.c), saved: isSaved(p.id), sel: p.id === ctx.sel, onClick: () => ctx.onPlace && ctx.onPlace(p.id) }))
      .sort((a, b) => (a.sel - b.sel) || (a.saved - b.saved));
    pinG(gPins.selectAll('g.pin').data(data).enter());
    for (const d of data) { addLabel(d.xy, `${esc(pn(d.id))}${d.saved ? ' <span class="hrt">♥</span>' : ''}`, d.sel ? 'district on' : '', d.sel ? 3 : d.saved ? 2 : 1.5, { minK: d.saved || ctx.district ? 1 : 2.4, dy: d.sel ? 24 : 18, button: true, onClick: d.onClick }); labData[labData.length - 1].pin = true; }
    place();
  }
  function refresh(opts) { Object.assign(ctx, opts || {}); if (mode === 'region') drawPins(ctx.r || currentRegion()); }
  const currentRegion = () => ctx.r;

  /* ---------- day route ---------- */
  function showRoute(plan, i, opts) {
    ctx = Object.assign({ noSheet: true }, opts || {}); mode = 'route'; const day = plan.days[i]; const r = day.r; lat0 = REGIONS[r].lat; clearOverlay(); zoom.scaleExtent([0.08, 18]);
    const sc = scheduleDay(plan, i), stay = STAY_BY[plan.stays[r]];
    const pts = [{ k: 'stay', lat: stay.lat, lng: stay.lng }];
    sc.rows.forEach(o => { const id = o.e.id; if (id && PBY[id].r === r) pts.push({ k: o.e.k, id, n: o.num, lat: PBY[id].lat, lng: PBY[id].lng }); });
    pts.push({ k: 'stay', lat: stay.lat, lng: stay.lng, end: true });
    const la = pts.map(p => p.lat), lo = pts.map(p => p.lng);
    let a0 = Math.min(...la), a1 = Math.max(...la), o0 = Math.min(...lo), o1 = Math.max(...lo);
    const minSpan = 0.012; if (a1 - a0 < minSpan) { const m = (a0 + a1) / 2; a0 = m - minSpan / 2; a1 = m + minSpan / 2; } if (o1 - o0 < minSpan) { const m = (o0 + o1) / 2; o0 = m - minSpan / 2; o1 = m + minSpan / 2; }
    const bboxF = polyFeat([[[[o0, a0], [o1, a0], [o1, a1], [o0, a1], [o0, a0]]]]);
    const p0 = pads(); ctx._pads = p0;
    proj = d3.geoIdentity().reflectY(true).fitExtent([[Math.min(95, p0.w * .2), (ctx.top || 40) + 24], [p0.w - Math.min(95, p0.w * .2), p0.h - 40]], fc([bboxF]));
    T0 = d3.zoomIdentity; svg.call(zoom.transform, T0);
    regionBase(r, true);
    const line = pts.map(p => P(p.lng, p.lat));
    gPins.append('path').datum(line).attr('class', 'route').attr('fill', 'none').attr('stroke', LINE[i % LINE.length]).attr('stroke-width', 5).attr('stroke-linejoin', 'round').attr('stroke-linecap', 'round').attr('opacity', .9);
    gPins.append('path').datum(line).attr('class', 'route').attr('fill', 'none').attr('stroke', '#fff').attr('stroke-width', 1.4).attr('stroke-dasharray', '1 7').attr('stroke-linecap', 'round');
    const data = pts.filter(p => !p.end).map(p => ({ ...p, xy: P(p.lng, p.lat) }));
    // nudge overlapping stops apart so every number stays readable
    for (let it = 0; it < 40; it++) for (let a = 0; a < data.length; a++) for (let c = a + 1; c < data.length; c++) {
      const A = data[a], B = data[c]; let dx = B.xy[0] - A.xy[0], dy = B.xy[1] - A.xy[1], d = Math.hypot(dx, dy); if (d >= 28) continue;
      if (d < .01) { dx = Math.cos(c * 2.4); dy = Math.sin(c * 2.4); d = 1; }
      const m = (28 - d) / 2, ux = dx / d, uy = dy / d; if (A.k !== 'stay') A.xy = [A.xy[0] - ux * m, A.xy[1] - uy * m]; B.xy = [B.xy[0] + ux * m * (A.k === 'stay' ? 2 : 1), B.xy[1] + uy * m * (A.k === 'stay' ? 2 : 1)];
    }
    const line2 = [...data.map(d => d.xy), data[0].xy];
    gPins.selectAll('path.route').datum(line2);
    const g = gPins.selectAll('g.pin').data(data).enter().append('g').attr('class', 'pin');
    g.filter(d => d.k === 'stay').each(function () { const s = d3.select(this); s.append('circle').attr('r', 14).attr('fill', '#141A2E').attr('stroke', '#fff').attr('stroke-width', 2.5); s.append('g').attr('transform', 'translate(-8,-8)').html(ICONS.house.replace('<svg ', '<svg width="16" height="16" color="#fff" ')); });
    g.filter(d => d.k !== 'stay').each(function (d) { const s = d3.select(this); s.append('circle').attr('r', 12).attr('fill', '#fff').attr('stroke', d.k === 'meal' ? '#EF7C1C' : LINE[i % LINE.length]).attr('stroke-width', 3.5).style('filter', 'drop-shadow(0 2px 3px rgba(20,26,46,.25))');
      s.append('text').attr('text-anchor', 'middle').attr('dy', 4).attr('font-size', 11).attr('font-weight', 800).attr('fill', '#141A2E').text(d.n); });
    const small = p0.w < 520;
    for (const d of data) if (d.id && !small) addLabel(d.xy, esc(pn(d.id)), '', 1, { dy: 16 });
    if (!small) addLabel(data[0].xy, `${esc(sn(stay.id))}`, 'district on', 2, { dy: 18 });
    place();
  }

  /* ---------- camera helpers ---------- */
  function focusOn(lat, lng, k) {
    if (!proj) return; const [x, y] = P(lng, lat), p = pads(); const cy = (p.t + p.h - p.b) / 2, cx = (p.l + p.w - p.r) / 2;
    const kk = k || Math.max(T0 ? T0.k : 1, 2.5);
    svg.transition().duration(650).call(zoom.transform, d3.zoomIdentity.translate(cx - x * kk, cy - y * kk).scale(kk));
  }
  function zoomBy(f) { svg.transition().duration(300).call(zoom.scaleBy, f); }
  function onResize() { if (!host) return; if (mode === 'korea') showKorea(ctx); else if (mode === 'world') showWorld(ctx); else if (mode === 'region') showRegion(ctx.r, ctx); }
  // tiny silhouette of a region for list cards
  const thumbs = {};
  function thumb(r) {
    if (thumbs[r]) return thumbs[r];
    if (isOv(r)) return (thumbs[r] = `<span class="cc">${REGIONS[r].cc.toUpperCase()}</span>`);   // 해외는 나라 코드 배지
    const k = Math.cos(REGIONS[r].lat * Math.PI / 180), rings = [];
    for (const m of GEO.regions[r].munis) for (const poly of m.g) rings.push(poly[0].map(([x, y]) => [x * k, -y]));
    const xs = rings.flat().map(q => q[0]), ys = rings.flat().map(q => q[1]);
    const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys), sc = 40 / Math.max(x1 - x0, y1 - y0);
    const ox = (48 - (x1 - x0) * sc) / 2, oy = (48 - (y1 - y0) * sc) / 2;
    const d = rings.map(rg => 'M' + rg.filter((_, i) => i % 2 === 0 || rg.length < 40).map(([x, y]) => `${((x - x0) * sc + ox).toFixed(1)} ${((y - y0) * sc + oy).toFixed(1)}`).join('L') + 'Z').join('');
    return (thumbs[r] = `<svg viewBox="0 0 48 48" width="44" height="44" aria-hidden="true"><path d="${d}" fill="currentColor" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>`);
  }
  return { thumb, mount, showKorea, showWorld, showRegion, showRoute, refresh, focusOn, zoomBy, onResize, get mode() { return mode; }, get host() { return host; } };
})();
