'use strict';
/* =========================================================
   Shell, formatting, chrome, bottom sheet, map tab, modals
   ========================================================= */
let T = I18N.ko;
const isDesk = () => window.innerWidth >= 980;
let sample = null;
(async () => { try { sample = await (window.claude && window.claude.use ? window.claude.use('sample') : null); } catch (e) { sample = null; } })();

/* ---------- formatting ---------- */
const F = {
  date(s, long) { const d = toDate(s); return long ? T.dateLong(d) : T.dateShort(d); },
  wd(s) { return T.wd[toDate(s).getDay()]; },
  dur(min) { min = Math.round(min); const h = Math.floor(min / 60), m = min % 60; return T.dur(h, m); },
  hours(p) { if (p.est) return T.localCheck; if (p.o[0] === 0 && p.o[1] >= 24) return T.always; return `${hm(p.o[0])}–${p.o[1] > 24 ? hm(p.o[1] - 24) + T.nextDay : hm(p.o[1])}`; },
  closed(p) { return p.closed && p.closed.length ? T.closedOn(p.closed.map(d => T.wd[d]).join(T.listSep)) : T.openDaily; },
  money: n => T.won(Math.round(n)), full: n => T.full(Math.round(n)),
  nights(n) { return T.nights(n); }
};
function setLang(l) {
  S.lang = l; T = I18N[l]; document.documentElement.lang = HTML_LANG[l]; loadFonts(); persist();
  if (!setLang.t0) setLang.t0 = document.title;
  document.title = l === 'ko' ? setLang.t0 : T.brand;   // 한국어는 검색용 제목 유지
}
function loadFonts() {
  const want = { zh: 'Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@600;700;900', ja: 'Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@600;700;900' }[S.lang];
  if (!want || document.getElementById('f-' + S.lang)) return;
  const l = document.createElement('link'); l.id = 'f-' + S.lang; l.rel = 'stylesheet'; l.href = `https://fonts.googleapis.com/css2?family=${want}&display=swap`; document.head.appendChild(l);
}
function toast(msg) { $$('.toast').forEach(t => t.remove()); const el = document.createElement('div'); el.className = 'toast'; el.textContent = msg; document.body.appendChild(el); setTimeout(() => el.remove(), 2200); }
const cicon = (c, cls = '') => `<span class="cicon ${cls}" style="background:${CATS[c].col}">${catIcon(c)}</span>`;
const heartBtn = id => `<button class="heart ${isSaved(id) ? 'on' : ''}" data-save="${id}" aria-pressed="${isSaved(id)}" aria-label="${isSaved(id) ? T.unsave : T.save}">${isSaved(id) ? ICONS.heartF : ICONS.heart}</button>`;

/* ---------- shell ---------- */
let app, panel, pin, stage;
function buildShell() {
  document.body.innerHTML = `<div class="app" id="app">
    <header class="appbar"><div class="brand"><span class="mark">${ICONS.logo}</span><span id="brandt"></span></div><span class="sp"></span>
      <button class="tripbtn" id="tripbtn">${ICONS.cal}<span id="tript"></span></button><div class="langs" id="langs" role="radiogroup" aria-label="Language"></div></header>
    <div class="main"><section class="panel" id="panel"><div class="grab" id="grab" role="button" aria-label="sheet"><i></i></div><div class="tabtop" id="tabtop"></div><div class="panel-in" id="pin"></div></section>
      <section class="stage" id="stage"><div id="mapbox"></div><div id="worldbox" style="display:none"></div><div id="ovl"></div></section></div>
    <nav class="tabbar" id="tabbar"></nav></div>`;
  app = $('#app'); panel = $('#panel'); pin = $('#pin'); stage = $('#stage');
  $('#tripbtn').onclick = openTrip;
  setupSheet();
  document.addEventListener('click', onGlobalClick);
  let rt = 0, rDesk = isDesk(); window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { setSheet(S.ui.sheet || 'half', true);
    if (Map2D.gl && rDesk === isDesk()) Map2D.onResize(); else { rDesk = isDesk(); renderStage(true); } }, 150); });
}
function onGlobalClick(e) {
  const sv = e.target.closest('[data-save]');
  if (sv) { e.stopPropagation(); const id = sv.dataset.save; const added = toggleSave(id); toast(added ? T.saved1 : T.unsaved1); afterSaveChange(id); return; }
}
function afterSaveChange(id) {
  renderChrome();
  if (S.ui.tab === 'map') { renderPanel(); Map2D.refresh({ sel: S.ui.sel, filter: S.ui.filter, district: S.ui.lvl === 'district' ? S.ui.d : null }); }
  else renderPanel();
  if (isDesk() && S.ui.tab !== 'map') renderStage();
}
const TABS = [['map', 'map'], ['saved', 'heart'], ['plan', 'cal'], ['prep', 'ticket']];
function renderChrome() {
  $('#brandt').textContent = T.brand;
  const ds = tripDates();
  $('#tript').innerHTML = `${esc(T.mdShort(toDate(ds[0])))}–${esc(T.mdShort(toDate(ds[ds.length - 1])))}<span class="pp"> · ${esc(T.ppl(S.trip.people))}</span>`;
  $('#langs').innerHTML = LANGS.map(([k, , s]) => `<button role="radio" aria-checked="${k === S.lang}" class="${k === S.lang ? 'on' : ''}" data-lang="${k}" lang="${HTML_LANG[k]}">${s}</button>`).join('');
  $$('#langs [data-lang]').forEach(b => b.onclick = () => { if (b.dataset.lang !== S.lang) { setLang(b.dataset.lang); renderAll(true); } });
  const badge = n => n ? `<span class="badge">${n}</span>` : '';
  const items = TABS.map(([k, ic]) => ({ k, ic, label: T['tab_' + k], b: k === 'saved' ? badge(S.saved.length) : '' }));
  $('#tabbar').innerHTML = items.map(t => `<button class="${S.ui.tab === t.k ? 'on' : ''}" data-tab="${t.k}">${ICONS[t.ic]}<span>${t.label}</span>${t.b}</button>`).join('');
  $('#tabtop').innerHTML = items.map(t => `<button class="${S.ui.tab === t.k ? 'on' : ''}" data-tab="${t.k}">${ICONS[t.ic]}<span>${t.label}</span>${t.b}</button>`).join('');
  $$('[data-tab]').forEach(b => b.onclick = () => go(b.dataset.tab));
  app.classList.toggle('t-map', S.ui.tab === 'map');
}
function go(tab) {
  if (S.ui.tab === tab && tab === 'map' && S.ui.sel) { S.ui.sel = null; }
  S.ui.tab = tab; persist(); if (tab === 'prep') track('klink_prep'); renderAll();
  panel.scrollTop = 0; const inn = $('.panel-in'); if (inn) inn.scrollTop = 0;
}
function renderAll(keepStage) { renderChrome(); renderPanel(); renderStage(!keepStage ? false : true); }
function renderPanel() {
  const fn = { map: panelMap, saved: panelSaved, plan: panelPlan, prep: panelPrep }[S.ui.tab];
  pin.innerHTML = fn(); bindPanel();
}
function bindPanel() {
  $$('[data-act]', pin).forEach(el => { el.onclick = ev => { ev.stopPropagation(); ACT[el.dataset.act] && ACT[el.dataset.act](el.dataset.v, el, ev); }; });
}

/* ---------- bottom sheet (mobile, map tab) ---------- */
function sheetPx(state) { const h = $('.main').getBoundingClientRect().height || window.innerHeight * .8;
  return state === 'peek' ? 148 : state === 'full' ? Math.round(h - 64) : Math.round(h * .42); }
function setSheet(state, quiet) {
  S.ui.sheet = state; app.classList.toggle('sheet-full', state === 'full'); const px = isDesk() ? 0 : sheetPx(state);
  app.style.setProperty('--sheet-h', px + 'px'); app.style.setProperty('--sheet-px', px);
  if (!quiet && S.ui.tab === 'map' && Map2D.mode === 'region' && S.ui.sel) { const p = PBY[S.ui.sel]; setTimeout(() => Map2D.focusOn(p.lat, p.lng), 340); }
}
function setupSheet() {
  const g = $('#grab'); let y0 = 0, h0 = 0, drag = false;
  g.addEventListener('pointerdown', e => { if (isDesk()) return; drag = true; y0 = e.clientY; h0 = panel.getBoundingClientRect().height; panel.classList.add('drag'); g.setPointerCapture(e.pointerId); });
  g.addEventListener('pointermove', e => { if (!drag) return; const h = clamp(h0 + (y0 - e.clientY), 120, sheetPx('full')); app.style.setProperty('--sheet-h', h + 'px'); });
  const end = e => { if (!drag) return; drag = false; panel.classList.remove('drag'); const h = panel.getBoundingClientRect().height, moved = Math.abs(e.clientY - y0);
    if (moved < 5) { setSheet(S.ui.sheet === 'peek' ? 'half' : S.ui.sheet === 'half' ? 'full' : 'half'); return; }
    const c = [['peek', sheetPx('peek')], ['half', sheetPx('half')], ['full', sheetPx('full')]].sort((a, b) => Math.abs(a[1] - h) - Math.abs(b[1] - h))[0][0]; setSheet(c); };
  g.addEventListener('pointerup', end); g.addEventListener('pointercancel', end);
  setSheet(S.ui.sheet || 'half', true);
}

/* ---------- map tab: navigation ---------- */
function openKorea(scope) { S.ui.scope = scope || (S.ui.r && isOv(S.ui.r) ? 'ov' : S.ui.r ? 'kr' : (S.ui.scope || 'kr')); S.ui.lvl = 'korea'; S.ui.r = null; S.ui.d = null; S.ui.sel = null; persist(); setSheet('half'); renderChrome(); renderPanel(); renderStage(); }
function openRegion(r, keepSel) { S.ui.lvl = 'region'; S.ui.r = r; S.ui.scope = isOv(r) ? 'ov' : 'kr'; S.ui.d = null; if (!keepSel) S.ui.sel = null; S.ui.filter = 'all'; persist(); if (S.ui.sheet === 'full') setSheet('half', true); renderChrome(); renderPanel(); renderStage(); }
function openDistrict(did) { const d = DISTRICTS[did], ov = isOv(d.r); S.ui.lvl = 'district'; S.ui.r = d.r; S.ui.d = did; S.ui.sel = null; persist(); setSheet('half', true); renderPanel(); renderStage(); }   // 해외는 3D 거리 준비 중 → 2D 지도
function selectPlace(id, opt = {}) {
  const p = PBY[id]; if (!p) return;
  if (S.ui.tab !== 'map') { S.ui.tab = 'map'; renderChrome(); }
  if (S.ui.lvl === 'korea' || S.ui.r !== p.r) { S.ui.lvl = 'region'; S.ui.r = p.r; S.ui.scope = isOv(p.r) ? 'ov' : 'kr'; S.ui.d = null; }
  S.ui.sel = id; persist();
  if (!isDesk() && S.ui.sheet !== 'full') setSheet('half', true);
  renderPanel(); (pin.closest('.panel-in') || pin).scrollTop = 0; pin.scrollTop = 0;
  if (Map2D.gl && stageR === p.r + '|' + (S.ui.lvl === 'district' ? S.ui.d : '')) { Map2D.refresh({ sel: id }); Map2D.focusOn(p.lat, p.lng); }
  else { renderStage(); if (!Map2D.gl) setTimeout(() => Map2D.focusOn(p.lat, p.lng, 2.6), 60); }
}
function clearSel() { S.ui.sel = null; persist(); renderPanel(); Map2D.refresh({ sel: null }); }

/* ---------- stage ---------- */
let stageKey = '', stageR = '';
function renderStage(force) {
  const mapbox = $('#mapbox'), worldbox = $('#worldbox'), ovl = $('#ovl');
  if (worldbox) { worldbox.style.display = 'none'; worldbox.innerHTML = ''; }
  mapbox.style.display = 'block'; stageR = '';
  if (S.ui.tab !== 'map') {
    ovl.innerHTML = '';
    if (!isDesk()) { stageKey = ''; return; }
    Map2D.mount(mapbox);
    if ((S.ui.tab === 'plan' || S.ui.tab === 'prep') && S.plan) { const i = clamp(S.ui.day, 0, S.plan.days.length - 1); Map2D.showRoute(S.plan, i, { top: 30 }); stageKey = 'route' + i; }
    else if (S.ui.tab === 'saved' && S.saved.length) { const r = tripOrder()[0]; Map2D.showRegion(r, { onPlace: id => selectPlace(id), onDistrict: openDistrict, onBg() {} }); stageKey = 'saved'; }
    else if (tripAir().ov || S.ui.scope === 'ov') { Map2D.showWorld({ onRegion: r => { go('map'); openRegion(r); } }); stageKey = 'world'; }
    else { Map2D.showKorea({ onRegion: r => { go('map'); openRegion(r); } }); stageKey = 'korea'; }
    return;
  }
  const lvl = S.ui.lvl;
  Map2D.mount(mapbox);
  if (lvl === 'korea') (S.ui.scope === 'ov' ? Map2D.showWorld : Map2D.showKorea)({ onRegion: openRegion });
  else { Map2D.showRegion(S.ui.r, { district: lvl === 'district' ? S.ui.d : null, sel: S.ui.sel, filter: S.ui.filter, onPlace: id => selectPlace(id), onDistrict: openDistrict, onBg: () => { if (S.ui.sel) clearSel(); } });
    stageR = S.ui.r + '|' + (lvl === 'district' ? S.ui.d : ''); if (S.ui.mode3d) Map2D.set3d(true); }
  ovl.innerHTML = overlayHtml(); bindOverlay();
}
function overlayHtml() {
  const lvl = S.ui.lvl, in3d = lvl !== 'korea' && S.ui.mode3d && Map2D.gl;
  const crumbs = [];
  if (lvl !== 'korea') crumbs.push(`<button data-o="korea">${ICONS.left}${esc(isOv(S.ui.r) ? T.scopeOv : T.korea)}</button>`);
  if (lvl === 'district') crumbs.push(`<button data-o="region">${esc(rn(S.ui.r))}</button>`, `<span>${esc(dn(S.ui.d))}</span>`);
  else if (lvl === 'region') crumbs.push(`<span>${esc(rn(S.ui.r))}</span>`);
  const ctrl = `<button class="iconbtn" data-o="zin" aria-label="+">${ICONS.plus}</button><button class="iconbtn" data-o="zout" aria-label="−">${ICONS.minus}</button>`
    + (lvl !== 'korea' && Map2D.gl ? `<button class="iconbtn t3d ${in3d ? 'on' : ''}" data-o="mode" aria-label="${in3d ? T.view2d : T.view3d}" aria-pressed="${in3d}"><span>3D</span></button>` : '');
  return `<div class="ov-top"><label class="search">${ICONS.search}<input id="q" placeholder="${esc(T.searchPh)}" autocomplete="off" value="${esc(S.ui.q || '')}"><button class="clr" data-o="clr" aria-label="${T.close}" ${S.ui.q ? '' : 'hidden'}>${ICONS.x}</button></label>
    <div class="searchres" id="sres" hidden></div>${crumbs.length ? `<div class="crumbs">${crumbs.join('')}</div>` : ''}</div>
    <div class="ov-ctrl">${ctrl}</div>`;
}
function bindOverlay() {
  $$('#ovl [data-o]').forEach(b => b.onclick = e => { e.stopPropagation(); const o = b.dataset.o;
    if (o === 'korea') openKorea(); else if (o === 'region') openRegion(S.ui.r);
    else if (o === 'zin') Map2D.zoomBy(1.6); else if (o === 'zout') Map2D.zoomBy(1 / 1.6);
    else if (o === 'mode') { S.ui.mode3d = !S.ui.mode3d; persist(); Map2D.set3d(S.ui.mode3d); b.classList.toggle('on', S.ui.mode3d); b.setAttribute('aria-pressed', S.ui.mode3d); }
    else if (o === 'clr') { S.ui.q = ''; $('#q').value = ''; showSearch(''); } });
  const q = $('#q'); if (q) { q.oninput = () => { S.ui.q = q.value; showSearch(q.value); }; q.onfocus = () => showSearch(q.value); q.onkeydown = e => { if (e.key === 'Escape') { q.blur(); showSearch(''); } }; }
}
const norm = s => String(s).toLowerCase().replace(/[\s·・\-'’]/g, '');
function showSearch(v) {
  const box = $('#sres'), clr = $('[data-o="clr"]'); if (clr) clr.hidden = !v; if (!box) return;
  const q = norm(v.trim()); if (!q) { box.hidden = true; box.innerHTML = ''; return; }
  const hits = PLACES.map(p => { const hay = norm([...Object.values(p.n), ...REGIONS[p.r].t, ...(OVD.countries[REGIONS[p.r].cc] || []), DISTRICTS[p.dist] ? DISTRICTS[p.dist].n.join('') : '', ...Object.values(I18N).map(L => L.cats[p.c])].join('|'));
    const nm = norm(Object.values(p.n).join('|')); return { p, s: nm.includes(q) ? 2 : hay.includes(q) ? 1 : 0 }; }).filter(x => x.s).sort((a, b) => b.s - a.s).slice(0, 8);
  box.hidden = false;
  box.innerHTML = hits.length ? hits.map(({ p }) => `<button class="prow" data-hit="${p.id}">${cicon(p.c, 'sm')}<span class="tx"><span class="nm">${esc(pn(p.id))}</span><span class="ds">${esc(rn(p.r))} · ${esc(dn(p.dist))}</span></span></button>`).join('') : `<div class="empty" style="padding:16px">${esc(T.noResult(v.trim()))}</div>`;
  $$('[data-hit]', box).forEach(b => b.onclick = () => { const id = b.dataset.hit; S.ui.q = ''; box.hidden = true; selectPlace(id); });
}

/* ---------- map tab: panel ---------- */
function panelMap() {
  if (S.ui.sel) return placeDetail(S.ui.sel);
  const lvl = S.ui.lvl;
  if (lvl === 'korea') {
    const ov = S.ui.scope === 'ov';
    const card = r => { const L = PLACES.filter(p => p.r === r), f = L.filter(p => isSaved(p.id)).length;
      return `<button class="rcard" data-act="region" data-v="${r}"><span class="rmap">${Map2D.thumb(r)}</span><span class="tx"><b>${esc(rn(r))}</b><span>${esc(tr4(REGION_TAG[r]))}</span>
        <span class="cnt"><span>${T.spots(L.length)}</span><span>${T.districtsN(GEO.regions[r].districts.length)}</span>${f ? `<span class="hrt">♥ ${f}</span>` : ''}</span></span>${ICONS.right}</button>`; };
    const seg = `<div class="segc scope" role="tablist"><button role="tab" class="${ov ? '' : 'on'}" data-act="scope" data-v="kr">${T.scopeKr}<small>${T.scopeKrSub}</small></button><button role="tab" class="${ov ? 'on' : ''}" data-act="scope" data-v="ov">${T.scopeOv}<small>${T.scopeOvSub(OV_IDS.length)}</small></button></div>`;
    if (!ov) return `<h1 class="h1">${T.where}</h1><p class="lead">${T.whereLead}</p>${seg}
      <div class="rgrid" style="margin-top:14px">${KR_IDS.map(card).join('')}</div>${aroundMore()}`;
    return `<h1 class="h1">${T.where}</h1><p class="lead">${T.whereLeadOv}</p>${seg}
      ${OVD.order.map(cc => { const rs = OV_IDS.filter(r => REGIONS[r].cc === cc); return rs.length ? `<div class="sec"><h3>${esc(countryName(cc))}</h3><small>${T.citiesN(rs.length)}</small></div><div class="rgrid">${rs.map(card).join('')}</div>` : ''; }).join('')}
      <p class="note">${T.ovNote}</p>${aroundMore()}`;
  }
  const r = S.ui.r, inD = lvl === 'district', ds = GEO.regions[r].districts;
  const list = PLACES.filter(p => p.r === r && (!inD || p.dist === S.ui.d) && (S.ui.filter === 'all' || p.c === S.ui.filter));
  const cats = CAT_ORDER.filter(c => PLACES.some(p => p.r === r && (!inD || p.dist === S.ui.d) && p.c === c));
  const head = inD
    ? `<div class="eyebrow"><button data-act="region" data-v="${r}">${esc(rn(r))}</button><span class="sep">›</span><span>${esc(dn(S.ui.d))}</span></div><h1 class="h1">${esc(dn(S.ui.d))}</h1><p class="lead">${S.ui.mode3d ? T.distLead3d : T.distLead2d}</p>`
    : `<div class="eyebrow"><button data-act="korea">${esc(isOv(r) ? `${T.scopeOv} · ${countryName(REGIONS[r].cc)}` : T.korea)}</button><span class="sep">›</span><span>${esc(rn(r))}</span></div><h1 class="h1">${esc(rn(r))}</h1><p class="lead">${esc(tr4(REGION_TAG[r]))}</p>
       <div class="sec"><h3>${T.pickDistrict}</h3><small>${T.pickDistrictSub}</small></div>
       <div class="chips scroll">${ds.map(d => `<button class="chip" data-act="district" data-v="${d.id}">${ICONS.pin.replace('<svg ', '<svg width="16" height="16" ')}${esc(tr4(d.n))}<span class="muted" style="font-weight:500">${d.ids.length}</span></button>`).join('')}</div>`;
  return `${head}${inD ? '' : courseCards(r)}
    <div class="sec"><h3>${inD ? T.inDistrict : T.allPlaces}</h3><small>${T.spots(list.length)}</small></div>
    <div class="chips scroll" style="margin-bottom:12px"><button class="chip ${S.ui.filter === 'all' ? 'on' : ''}" data-act="filter" data-v="all">${T.all}</button>${cats.map(c => `<button class="chip ${S.ui.filter === c ? 'on' : ''}" data-act="filter" data-v="${c}"><span class="ci" style="background:${CATS[c].col}">${catIcon(c)}</span>${T.cats[c]}</button>`).join('')}</div>
    <div class="list">${list.map(p => placeRow(p)).join('') || `<div class="empty">${T.noneFilter}</div>`}</div>
    ${aroundCard(r, inD ? S.ui.d : null)}`;
}
/* ---------- 어라운드툴 연결 ---------- */
const ext = (url, inner, cls = '') => `<a class="${cls}" href="${esc(url)}" target="_blank" rel="noopener">${inner}</a>`;
const koOnly = () => S.lang === 'ko' ? '' : `<span class="pill sug">${T.atKo}</span>`;
function aroundCard(r, did, compact) {
  const ar = aroundRegion(r); if (!ar) return '';
  const gu = did ? aroundGu(did) : null, rows = [];
  if (ar.trip) rows.push(ext(ar.trip.url, `<span class="cicon sm" style="background:var(--at)">${ICONS.map}</span><span class="tx"><b>${esc(T.atTrip(rn(r)))}</b><small>${T.atTripSub}</small></span>${ICONS.right}`, 'arow'));
  const gus = gu ? [gu] : (compact ? [] : ar.gus);
  if (!gu && ar.food) rows.push(ext(ar.food.url, `<span class="cicon sm" style="background:var(--at)">${ICONS.food2}</span><span class="tx"><b>${esc(T.atFood(rn(r), ar.food.count))}</b><small>${T.atFoodSub}</small></span>${ICONS.right}`, 'arow'));
  if (gu) rows.push(ext(gu.url, `<span class="cicon sm" style="background:var(--at)">${ICONS.food2}</span><span class="tx"><b>${esc(T.atFood(S.lang === 'ko' ? gu.gu : `${rn(r)} ${gu.gu}`, gu.count))}</b><small>${T.atFoodSub}</small></span>${ICONS.right}`, 'arow'));
  if (!rows.length) return '';
  if (compact === 'rows') return rows.join('');
  const chips = gu ? gu.cats.map(c => ext(c.url, `<span lang="ko">${esc(c.cat)}</span><span class="muted">${c.count}</span>`, 'chip')).join('')
    : (!compact && gus.length > 1 ? gus.map(g => ext(g.url, `<span lang="ko">${esc(g.gu)}</span><span class="muted">${g.count}</span>`, 'chip')).join('') : '');
  return `<div class="sec"><h3>${T.atTitle}</h3><small>${koOnly()}</small></div><div class="around">${rows.join('')}${chips ? `<div class="chips achips">${chips}</div>` : ''}</div>`;
}
function aroundMore() {
  if (!AROUND) return '';
  const more = (AROUND.moreTrips || []).slice(0, 12);
  return `<div class="sec"><h3>${T.atMoreTitle}</h3><small>${koOnly()}</small></div>
    <div class="around">${ext(AROUND.travel, `<span class="cicon sm" style="background:var(--at)">${ICONS.map}</span><span class="tx"><b>${T.atAllTrips(AROUND.counts.trips)}</b><small>${T.atTripSub}</small></span>${ICONS.right}`, 'arow')}
      ${ext(AROUND.food, `<span class="cicon sm" style="background:var(--at)">${ICONS.food2}</span><span class="tx"><b>${T.atAllFood(AROUND.counts.gu, AROUND.counts.places)}</b><small>${T.atFoodSub}</small></span>${ICONS.right}`, 'arow')}
      ${more.length ? `<div class="chips achips">${more.map(m => ext(m.url, `<span lang="ko">${esc(m.name)}</span>`, 'chip')).join('')}</div>` : ''}</div>
    <p class="note">${T.atBy}</p>`;
}
function placeRow(p, opts = {}) {
  const tags = [];
  if (p.far) tags.push(`<span class="pill sug">${T.far}</span>`);
  return `<div class="prow ${S.ui.sel === p.id ? 'sel' : ''}"><button class="row grow" style="text-align:left;gap:12px" data-act="place" data-v="${p.id}">${cicon(p.c)}<span class="tx"><span class="nm">${esc(pn(p.id))}</span>
    <span class="ds">${opts.sub || esc(pd(p.id))}</span>${tags.length ? `<span class="mt">${tags.join('')}</span>` : ''}</span></button>${heartBtn(p.id)}</div>`;
}
function placeInPlan(id) { if (!S.plan) return -1; return S.plan.days.findIndex(d => d.stops.some(s => s.id === id)); }
/* ---------- 장소 상세: 어라운드툴 명소 안내 + 가이드 코스 (2026-11-12) ---------- */
const spotOf = id => (AROUND && AROUND.spots && AROUND.spots[id]) || {};
const hiRoute = (txt, keys) => { let h = esc(txt); for (const k of (keys || []).slice().sort((a, b) => b.length - a.length)) { const e = esc(k); if (e && h.includes(e)) { h = h.split(e).join(`<b>${e}</b>`); break; } } return h; };
const ic = (name, s = 18) => ICONS[name].replace('<svg ', `<svg width="${s}" height="${s}" `);
function placeDetail(id) {
  const p = PBY[id], di = placeInPlan(id), { s: sp, g } = spotOf(id), ko = S.lang !== 'ko' ? ` lang="ko"` : '';
  const col = CATS[p.c].col, best = { am: T.bestAmL, eve: T.bestEveL, night: T.bestNightL }[p.best];
  // 한눈에 보는 정보: 명소 안내가 있으면 그 내용(한국어), 없으면 K링크 기본값
  const F_ = sp ? sp.facts : null;
  const facts = F_ ? [['clock', T.fHours, F_.hours], ['ticket', T.fFee, F_.fee], ['walk', T.fStay, F_.stay], ['sun', T.fWhen, F_.when], ['pin', T.fWhere, F_.access, 1]]
      .filter(x => x[2]).map(([i, k, v, w]) => [i, k, `<span${ko}>${esc(v)}</span>`, w])
    : p.est ? [['clock', T.fHours, `${T.localCheck}${p.closed && p.closed.length ? `<small>${F.closed(p)}</small>` : ''}`], ['walk', T.fStay, T.usually(F.dur(p.h * 60))],
        ['ticket', T.fFee, T.localCheck], ['pin', T.fWhere, esc(`${rn(p.r)} · ${dn(p.dist)}`)]]
    : [['clock', T.fHours, T.localCheck], ['walk', T.fStay, T.usually(F.dur(p.h * 60))],
        ['pin', T.fWhere, `${esc(stationOf(p))}${S.lang !== 'ko' ? `<small lang="ko">${esc(p.st)}</small>` : ''}`, 1]];
  if (!F_ && best) facts.splice(2, 0, ['sun', T.fWhen, best]);
  if (p.season) facts.splice(1, 0, ['cal', T.fSeason, T.season(p.season[0], p.season[1]), 1]);
  { const half = facts.filter(f => !f[3]); if (half.length % 2) half[half.length - 1][3] = 1; }   // 두 칸씩 맞추고 남는 칸은 넓게
  const factsHtml = `<div class="pdx-facts">${facts.map(([i, k, v, w]) => `<div class="pdx-f ${w ? 'wide' : ''}"><span class="i" style="color:${col}">${ic(i)}</span><div><small>${k}</small><b>${v}</b></div></div>`).join('')}</div>`;
  const photo = sp && sp.photo ? `<figure class="pdx-ph"><img src="${esc(sp.photo.src)}" alt="${esc(sp.photo.alt)}" loading="lazy" decoding="async"><figcaption>${T.photoBy} ${sp.photo.link ? `<a href="${esc(sp.photo.link)}" target="_blank" rel="noopener nofollow">${esc(sp.photo.by)}</a>` : esc(sp.photo.by)} · ${esc(sp.photo.lic)}</figcaption></figure>`
    : '';   // 사진이 없으면 큰 색 상자 대신 바로 이름부터 (2026-11-12 배치 개선)
  const chips = [`<span class="pdx-cat" style="background:${col}">${catIcon(p.c).replace('<svg ', '<svg width="14" height="14" ')}${esc(T.cats[p.c])}</span>`,
    p.best === 'night' && p.c !== 'night' ? `<span class="pdx-chip">${T.bestNight}</span>` : p.best === 'am' ? `<span class="pdx-chip">${T.bestAm}</span>` : '',
    p.far ? `<span class="pdx-chip">${T.far}</span>` : ''].join('');
  const sec = (title, body, extra = '') => `<section class="pdx-sec"><h3>${title}${extra}</h3>${body}</section>`;
  const see = sp && sp.see && sp.see.length ? sec(T.seeTitle, `<ol class="pdx-see"${ko}>${sp.see.map(([a, b]) => `<li><b>${esc(a)}</b><span>${esc(b)}</span></li>`).join('')}</ol>`, koOnly()) : '';
  const tips = sp && sp.tips && sp.tips.length ? `<div class="pdx-tips"${ko}><h3>${T.tipsTitle}</h3><ul>${sp.tips.map(t => `<li>${ic('check', 16)}<span>${esc(t)}</span></li>`).join('')}</ul></div>` : '';
  const course = g && (g.days || g.area) ? sec(T.courseTitle, `${g.area ? `<div class="pdx-area"${ko}><small>${T.areaLbl}</small><b>${esc(g.area[0])}</b><span>${esc(g.area[1])}${g.area[2] ? ` · ${esc(g.area[2])}` : ''}</span></div>` : ''}
      ${(g.days || []).map(d => `<div class="pdx-day"${ko}><div class="lbl"><span>${esc(d[0].replace(/\s*—.*$/, ''))}</span><em>${esc(d[1])}</em>${d[2] ? `<b>${esc(d[2])}</b>` : ''}</div><p>${hiRoute(d[3], g.keys)}</p></div>`).join('')}`, koOnly()) : '';
  const moves = g && g.moves ? sec(T.movesTitle, `<div class="pdx-moves"${ko}>${g.moves.map(m => `<div><span>${esc(m[0])}</span><em>${esc(m[1])}</em><b>${esc(m[2])}</b></div>`).join('')}</div>`) : '';
  const faq = g && g.faq ? sec(T.faqTitle, `<div class="pdx-faq"${ko}>${g.faq.map(([q, a]) => `<details><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join('')}</div>`) : '';
  const lk = spotOf(id), linkRow = (url, icn, b, sm) => ext(url, `<span class="cicon sm" style="background:var(--at)">${ICONS[icn]}</span><span class="tx"><b lang="ko">${esc(b)}</b>${sm ? `<small lang="ko">${esc(sm)}</small>` : ''}</span>${ICONS.right}`, 'arow');
  const foodRows = [lk.gu ? linkRow(lk.gu.url, 'food2', T.atFood(S.lang === 'ko' ? lk.gu.gu : `${rn(p.r)} ${lk.gu.gu}`, lk.gu.count), lk.gu.cats.map(c => c.cat).join(' · ')) : '',
    ...(lk.f || []).map(x => linkRow(x.url, 'food2', x.name, x.desc))].join('');
  const food = foodRows ? sec(T.foodTitle, `<div class="around">${foodRows}</div>`, koOnly()) : '';
  const trips = lk.t && lk.t.length ? sec(T.tripsTitle, `<div class="around">${lk.t.map(x => linkRow(x.url, 'map', x.name)).join('')}</div>`, koOnly()) : '';
  const near = PLACES.filter(q => q.r === p.r && q.id !== id).map(q => [hav(p, q), q]).sort((a, b) => a[0] - b[0]).slice(0, 3)
    .map(([, q]) => { const L = legBetween(p, q, p.r); return `<div class="prow"><button class="row grow" style="text-align:left;gap:12px" data-act="place" data-v="${q.id}">${cicon(q.c, 'sm')}<span class="tx"><span class="nm">${esc(pn(q.id))}</span><span class="ds">${modeLabel(L)} ${F.dur(L.min)}</span></span></button>${heartBtn(q.id)}</div>`; }).join('');
  const srcRow = sp ? `<div class="pdx-src"><div class="who">${ic('check', 16)}<span>${T.spotFrom}<small>${T.checkedOn(sp.checked)} · ${T.checkBefore}</small></span></div>
      ${(sp.src || []).filter(x => !/aroundtool\.com/.test(x[1])).length ? `<div class="links">${sp.src.filter(x => !/aroundtool\.com/.test(x[1])).map(([n, u]) => ext(u, esc(n))).join('')}</div>` : ''}
      ${sp.url ? ext(sp.url, `${ic('map', 18)}${T.guideMore}`, 'btn ghost block') : ''}</div>`
    : `<div class="pdx-soon">${ic('info', 20)}<div><b>${T.spotSoonH}</b><span>${T.spotSoon}</span>${g ? ext(g.url, `${esc(g.title)} ›`, 'lnk') : ''}</div></div>`;
  return `<button class="back" data-act="unsel">${ICONS.left}${esc(S.ui.lvl === 'district' ? dn(S.ui.d) : rn(p.r))}</button>
    ${photo}
    <div class="pdx-head"><div class="grow"><div class="pdx-chips">${chips}</div><h2 class="pdx-name">${esc(pn(id))}</h2>
      ${S.lang !== 'ko' ? `<div class="pd-ko" lang="ko">${esc(p.n.ko)}</div>` : ''}<div class="pdx-where">${ic('pin', 14)}${esc(rn(p.r))} · ${esc(dn(p.dist))}</div></div>${heartBtn(id)}</div>
    <p class="pdx-one"${sp ? ko : ''}>${esc(sp ? sp.one : pd(id))}</p>
    ${di >= 0 ? `<div class="banner" style="background:var(--green-soft);color:var(--green)">${ic('check')}<span>${T.inPlanDay(di + 1)}</span><button class="btn sm soft" data-act="gotoDay" data-v="${di}">${T.viewPlan}</button></div>` : ''}
    ${factsHtml}
    <div class="pd-acts"><button class="btn ${isSaved(id) ? 'ghost' : ''}" data-save="${id}">${isSaved(id) ? ICONS.heartF : ICONS.heart}${isSaved(id) ? T.savedBtn : T.saveBtn}</button>
      ${S.plan && di < 0 && S.plan.days.some(d => d.r === p.r) ? `<button class="btn ghost" data-act="addToPlan" data-v="${id}">${ICONS.plus}${T.addToPlan}</button>` : ''}
      <button class="btn ghost taxi" data-act="taxi" data-v="${id}" style="flex:0 0 auto" aria-label="${esc(T.taxiCard)}">${ICONS.taxi}<span>${T.taxiShort}</span></button></div>
    ${p.est ? `${ext(mapUrl(p), `${ICONS.pin}${T.openMap}`, 'btn ghost block maplink')}${sp ? '' : `<p class="note">${T.estNote}</p>`}` : ''}
    ${see}${tips}${course}${food}${moves}${faq}${trips}
    ${near ? sec(T.nearTitle, `<div class="list">${near}</div>`) : ''}
    ${srcRow}
    ${aroundCard(p.r, p.dist, true)}`;
}
function stationOf(p) { return /역/.test(p.st) ? stationTr(p.st) : `${rn(p.r)} ${dn(p.dist)}`; }
const mapUrl = p => `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${p.n.en} ${REGIONS[p.r].t[2]}`)}`;
// 해외에서 기사님께 보여 줄 현지어 이름과 한마디
const LOCAL_LANG = { jp: 'ja', tw: 'zh', hk: 'zh', mo: 'zh', cn: 'zh' };
const LOCAL_SAY = { ja: n => `${n}までお願いします。`, zh: n => `请到${n}。`, en: n => `Please take me to ${n}.` };
const ST_NAMES = { '경복궁': ['景福宫', 'Gyeongbokgung', '景福宮'], '안국': ['安国', 'Anguk', '安国'], '이촌': ['二村', 'Ichon', '二村'], '종로5가': ['钟路5街', 'Jongno 5-ga', '鍾路5街'], '을지로3가': ['乙支路3街', 'Euljiro 3-ga', '乙支路3街'],
  '신사': ['新沙', 'Sinsa', '新沙'], '명동': ['明洞', 'Myeong-dong', '明洞'], '홍대입구': ['弘大入口', 'Hongik Univ.', '弘大入口'], '서울숲': ['首尔林', 'Seoul Forest', 'ソウルの森'], '압구정로데오': ['狎鸥亭罗德奥', 'Apgujeong Rodeo', '狎鴎亭ロデオ'],
  '신논현': ['新论岘', 'Sinnonhyeon', '新論峴'], '성수': ['圣水', 'Seongsu', '聖水'], '동대문역사문화공원': ['东大门历史文化公园', 'DDP', '東大門歴史文化公園'], '여의나루': ['汝矣渡口', 'Yeouinaru', '汝矣ナル'], '종로3가': ['钟路3街', 'Jongno 3-ga', '鍾路3街'],
  '신용산': ['新龙山', 'Sinyongsan', '新龍山'], '삼성': ['三成', 'Samseong', '三成'], '잠실': ['蚕室', 'Jamsil', '蚕室'], '광화문': ['光化门', 'Gwanghwamun', '光化門'], '고속터미널': ['高速巴士客运站', 'Express Bus Terminal', '高速ターミナル'],
  '해운대': ['海云台', 'Haeundae', '海雲台'], '토성': ['土城', 'Toseong', '土城'], '자갈치': ['札嘎其', 'Jagalchi', 'チャガルチ'], '광안': ['广安', 'Gwangan', '広安'], '서면': ['西面', 'Seomyeon', '西面'], '오시리아': ['奥西利亚', 'OSIRIA', 'オシリア'],
  '센텀시티': ['Centum City', 'Centum City', 'センタムシティ'], '시청': ['市厅', 'City Hall', '市庁'], '회현': ['会贤', 'Hoehyeon', '会賢'], '혜화': ['惠化', 'Hyehwa', '恵化'], '망원': ['望远', 'Mangwon', '望遠'], '노량진': ['鹭梁津', 'Noryangjin', '鷺梁津'] };
function stationTr(st) { const m = /^(.+?)역(?: (\S+)번 출구)?$/.exec(st); if (!m || S.lang === 'ko') return st; const nm = ST_NAMES[m[1]] ? ST_NAMES[m[1]][LANG_IDX[S.lang] - 1] : m[1]; return T.station(nm, m[2]); }

/* ---------- modals ---------- */
function openModal(html, onMount) {
  closeModal(); const sc = document.createElement('div'); sc.className = 'scrim'; sc.innerHTML = `<div class="modal" role="dialog" aria-modal="true"><div class="grab2"></div>${html}</div>`;
  sc.addEventListener('click', e => { if (e.target === sc) closeModal(); }); document.body.appendChild(sc);
  $$('[data-close]', sc).forEach(b => b.onclick = closeModal);
  if (onMount) onMount(sc.querySelector('.modal')); return sc;
}
function closeModal() { $$('.scrim').forEach(s => s.remove()); }
function openMenu(anchor, items) {
  $$('.menu').forEach(m => m.remove()); const m = document.createElement('div'); m.className = 'menu'; m.setAttribute('role', 'menu');
  m.innerHTML = items.map((it, k) => it === '-' ? '<hr>' : `<button role="menuitem" data-k="${k}" class="${it.danger ? 'danger' : ''}" ${it.disabled ? 'disabled style="opacity:.35"' : ''}>${ICONS[it.icon] || ''}<span>${it.label}</span></button>`).join('');
  document.body.appendChild(m);
  const r = anchor.getBoundingClientRect(), mw = m.offsetWidth, mh = m.offsetHeight;
  m.style.left = clamp(r.right - mw, 8, window.innerWidth - mw - 8) + 'px'; m.style.top = (r.bottom + mh + 8 > window.innerHeight ? Math.max(8, r.top - mh - 6) : r.bottom + 6) + 'px';
  $$('[data-k]', m).forEach(b => b.onclick = e => { e.stopPropagation(); m.remove(); const it = items[+b.dataset.k]; it.fn && it.fn(); });
  setTimeout(() => document.addEventListener('click', function h(e) { if (!m.contains(e.target)) { m.remove(); document.removeEventListener('click', h); } }), 0);
}
function openTaxi(id) {
  const p = PBY[id];
  if (isOv(p.r)) {
    const ll = LOCAL_LANG[REGIONS[p.r].cc] || 'en', nm = p.n[ll] || p.n.en;
    openModal(`<h3>${T.taxiCard}</h3><p class="lead">${T.taxiLead}</p>
      <div class="taxi"><div class="ko" lang="${HTML_LANG[ll]}">${esc(nm)}</div>${nm !== p.n.en ? `<div class="ad" lang="en">${esc(p.n.en)}</div>` : ''}<small>${esc(pn(id))} · ${esc(rn(p.r))}</small></div>
      <div class="taxi" style="background:var(--cobalt-soft)"><div class="ad" lang="${HTML_LANG[ll]}">${esc(LOCAL_SAY[ll](nm))}</div><small>${T.taxiSay}</small></div>
      <button class="btn block ink" style="margin-top:16px" data-close>${T.close}</button>`);
    return;
  }
  openModal(`<h3>${T.taxiCard}</h3><p class="lead">${T.taxiLead}</p>
    <div class="taxi"><div class="ko" lang="ko">${esc(p.n.ko)}</div><div class="ad" lang="ko">${esc(p.st)}</div>${S.lang !== 'ko' ? `<small>${esc(pn(id))} · ${esc(stationOf(p))}</small>` : ''}</div>
    <div class="taxi" style="background:var(--cobalt-soft)"><div class="ad" lang="ko">${esc(`${p.n.ko}${koRo(p.n.ko)} 가 주세요.`)}</div><small>${T.taxiSay}</small></div>
    <button class="btn block ink" style="margin-top:16px" data-close>${T.close}</button>`);
}

/* ---------- trip settings ---------- */
function openTrip() {
  const t = JSON.parse(JSON.stringify(S.trip)), ta = tripAir();
  t.arr = ta.arr; t.dep = ta.dep; t.kind = tripKind();   // 이번 여행 나라의 공항(국내 여행은 역)으로 맞춘다
  const homeNow = () => ta.cc === 'kr' && t.kind === 'kr';
  const fix = () => { const L = Object.keys(AIRPORTS).filter(c => AIRPORTS[c].cc === ta.cc && !!AIRPORTS[c].home === homeNow());
    if (!L.includes(t.arr)) t.arr = L[0]; if (!L.includes(t.dep)) t.dep = L[0]; };
  fix();
  const draw = m => {
    const ds = []; for (let d = t.start, k = 0; d <= t.end && k < 14; d = addDays(d, 1), k++) ds.push(d); const n = ds.length;
    const hrs = Array.from({ length: 19 }, (_, k) => 6 + k);
    const H = homeNow();
    const apOpts = (v) => Object.keys(AIRPORTS).filter(c => AIRPORTS[c].cc === ta.cc && !!AIRPORTS[c].home === H).map(c => `<option value="${c}" ${c === v ? 'selected' : ''}>${esc(an(c))}</option>`).join('');
    const hOpts = v => hrs.map(h => `<option value="${h}" ${h === v ? 'selected' : ''}>${hm(h)}</option>`).join('');
    m.innerHTML = `<div class="grab2"></div><h3>${T.tripTitle}</h3><p class="lead">${ta.ov ? T.tripLeadOv(countryName(ta.cc)) : H ? T.tripLeadHome : T.tripLead}</p>
      <div class="fld"><div class="lb">${T.kindTitle}</div><div class="segc kindseg">${['kr', 'ov', 'visit'].map(k => `<button class="${t.kind === k ? 'on' : ''}" data-kind="${k}">${T.kinds[k][0]}</button>`).join('')}</div></div>
      <div class="fld"><div class="lb">${T.dates}<small>${n > 0 ? F.nights(n) : ''}</small></div>
        <div class="dates"><label class="dbox"><small>${T.first}</small><b>${T.mdShort(toDate(t.start))}</b><span>${T.wdL[toDate(t.start).getDay()]}</span><input type="date" id="t-s" value="${t.start}"></label>
        <label class="dbox"><small>${T.last}</small><b>${T.mdShort(toDate(t.end))}</b><span>${T.wdL[toDate(t.end).getDay()]}</span><input type="date" id="t-e" value="${t.end}" min="${t.start}"></label></div>
        ${n >= 14 ? `<p class="note">${T.max14}</p>` : ''}</div>
      <div class="fld"><div class="lb">${H ? T.flightsHome : T.flights}<small>${H ? T.flightsHomeSub : T.flightsSub}</small></div>
        <div class="ftrow"><div class="sel"><small>${H ? T.fromSt : T.arrAp}</small><select id="t-aa">${apOpts(t.arr)}</select></div><div class="sel"><small>${H ? T.fromT : T.arrT}</small><select id="t-at">${hOpts(t.arrT)}</select></div>
        <div class="sel"><small>${H ? T.backSt : T.depAp}</small><select id="t-da">${apOpts(t.dep)}</select></div><div class="sel"><small>${H ? T.backT : T.depT}</small><select id="t-dt">${hOpts(t.depT)}</select></div></div></div>
      <div class="fld"><div class="lb">${T.who}</div><div class="ftrow"><div class="stepper"><button data-p="-1" aria-label="−">−</button><b>${T.ppl(t.people)}</b><button data-p="1" aria-label="+">+</button></div>
        <div class="segc" style="align-self:center;justify-content:space-between">${T.parties.map((p, i) => `<button class="${t.party === i ? 'on' : ''}" data-party="${i}">${p}</button>`).join('')}</div></div></div>
      <div class="fld"><div class="lb">${T.pace}</div><div class="tiles">${T.paces.map((b, i) => `<button class="tile ${t.pace === i ? 'on' : ''}" data-pace="${i}"><small>${b[1]}</small><b>${b[0]}</b></button>`).join('')}</div></div>
      <div class="fld" ${ta.ov ? 'hidden' : ''}><div class="lb">${T.interests}<small>${T.multi}</small></div><div class="chips">${CAT_ORDER.map(c => `<button class="chip ${t.interests.includes(c) ? 'on' : ''}" data-int="${c}"><span class="ci" style="background:${CATS[c].col}">${catIcon(c)}</span>${T.cats[c]}</button>`).join('')}</div></div>
      <div style="display:flex;gap:10px;margin-top:22px"><button class="btn ghost" data-close style="flex:.6">${T.cancel}</button><button class="btn" id="t-ok" style="flex:1">${T.saveTrip}</button></div>`;
    const re = () => { const y = m.scrollTop; draw(m); m.scrollTop = y; };
    $('#t-s', m).onchange = e => { t.start = e.target.value || t.start; if (t.end < t.start) t.end = t.start; if (addDays(t.start, 13) < t.end) t.end = addDays(t.start, 13); re(); };
    $('#t-e', m).onchange = e => { t.end = e.target.value || t.end; if (t.end < t.start) t.end = t.start; if (addDays(t.start, 13) < t.end) t.end = addDays(t.start, 13); re(); };
    $$('.dbox', m).forEach(b => b.onclick = e => { const i = b.querySelector('input'); if (e.target !== i) { try { i.showPicker(); } catch (er) { i.focus(); } } });
    $('#t-aa', m).onchange = e => t.arr = e.target.value; $('#t-da', m).onchange = e => t.dep = e.target.value;
    $('#t-at', m).onchange = e => t.arrT = +e.target.value; $('#t-dt', m).onchange = e => t.depT = +e.target.value;
    $$('[data-kind]', m).forEach(b => b.onclick = () => { t.kind = b.dataset.kind; setKindTimes(t, t.kind); fix(); re(); });
    $$('[data-p]', m).forEach(b => b.onclick = () => { t.people = clamp(t.people + +b.dataset.p, 1, 8); re(); });
    $$('[data-party]', m).forEach(b => b.onclick = () => { t.party = +b.dataset.party; re(); });
    $$('[data-pace]', m).forEach(b => b.onclick = () => { t.pace = +b.dataset.pace; re(); });
    $$('[data-int]', m).forEach(b => b.onclick = () => { const c = b.dataset.int, i = t.interests.indexOf(c); i < 0 ? t.interests.push(c) : t.interests.splice(i, 1); re(); });
    $$('[data-close]', m).forEach(b => b.onclick = closeModal);
    $('#t-ok', m).onclick = () => { const kc = S.trip.kind !== t.kind; S.trip = t; if (kc) { S.ui.scope = t.kind === 'ov' ? 'ov' : 'kr'; if (S.ui.lvl !== 'korea' && isOv(S.ui.r) !== (t.kind === 'ov')) { S.ui.lvl = 'korea'; S.ui.r = null; S.ui.d = null; S.ui.sel = null; } } persist(); closeModal(); toast(T.tripSaved); renderAll(true); if (S.ui.tab === 'plan' || isDesk()) renderStage(); };
  };
  openModal('', m => draw(m));
}

/* ---------- intro ---------- */
function showIntro() {
  const el = document.createElement('div'); el.className = 'intro';
  const draw = () => {
    el.innerHTML = `<div class="intro-in">
      <h1>${T.introH}</h1><p>${T.introP}</p>
      <div class="intro-map" aria-hidden="true"><svg viewBox="0 0 400 180"><path d="M128 14 V90 L286 14 M128 90 L292 166 M128 90 V166" class="pth"/>
        ${[[128, 14, .35, 112, 19, 'end'], [128, 90, .9, 112, 95, 'end'], [286, 14, 1.5, 302, 19, 'start'], [292, 166, 2.2, 308, 171, 'start']].map(([x, y, d, lx, ly, an], k) => `<g class="st" style="animation-delay:${d}s"><circle cx="${x}" cy="${y}" r="9" fill="#2443E8" stroke="#fff" stroke-width="5"/><text x="${lx}" y="${ly}" fill="#fff" font-size="14" font-weight="700" text-anchor="${an}">${esc(T.introStops[k])}</text></g>`).join('')}</svg></div>
      <div class="sp"></div><div class="kinds"><b><span class="stp">1</span>언어 · 语言 · Language · 言語</b>
        <div class="langseg">${LANGS.map(([k, n]) => `<button class="${k === S.lang ? 'on' : ''}" data-l="${k}" lang="${HTML_LANG[k]}" aria-pressed="${k === S.lang}">${n}</button>`).join('')}</div>
        <b><span class="stp">2</span>${T.kindTitle}</b>${['kr', 'ov', 'visit'].map(k => `<button class="kindbtn" data-k="${k}"><i>${ICONS[k === 'ov' ? 'plane' : k === 'kr' ? 'rail' : 'pin']}</i><span><b>${T.kinds[k][0]}</b><small>${T.kinds[k][1]}</small></span>${ICONS.right}</button>`).join('')}</div></div>`;
    $$('[data-l]', el).forEach(b => b.onclick = () => { setLang(b.dataset.l); draw(); renderAll(true); });
    $$('[data-k]', el).forEach(b => b.onclick = () => { const k = b.dataset.k; S.trip.kind = k; setKindTimes(S.trip, k); S.seenIntro = true;
      if (S.ui.lvl === 'korea') S.ui.scope = k === 'ov' ? 'ov' : 'kr'; persist(); el.remove(); renderAll(); openTrip(); });
  };
  draw(); document.body.appendChild(el);
}

/* ---------- actions ---------- */
const ACT = {
  region: v => openRegion(v), korea: () => openKorea(), district: v => openDistrict(v), scope: v => openKorea(v),
  filter: v => { S.ui.filter = v; persist(); renderPanel(); Map2D.refresh({ filter: v }); },
  place: v => selectPlace(v), unsel: () => clearSel(),
  taxi: v => openTaxi(v),
  gotoDay: v => { S.ui.day = +v; go('plan'); },
  addToPlan: (v, el) => { const p = PBY[v]; const days = S.plan.days.map((d, i) => ({ d, i })).filter(x => x.d.r === p.r);
    openMenu(el, days.map(({ d, i }) => ({ icon: 'cal', label: `${T.day(i + 1)} · ${F.date(d.date)}`, fn: () => { Plan.add(v, i); toast(T.addedDay(i + 1)); renderPanel(); } }))); }
};
