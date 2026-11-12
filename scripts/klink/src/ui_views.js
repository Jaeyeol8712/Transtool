'use strict';
/* =========================================================
   Saved, Plan, Prep views
   ========================================================= */
function koRo(w) { const c = w.charCodeAt(w.length - 1) - 0xAC00; if (c < 0 || c > 11171) return '로'; const j = c % 28; return (j === 0 || j === 8) ? '로' : '으로'; }
const emptyArt = (ic) => `<div class="art"><svg viewBox="0 0 120 90"><rect x="8" y="14" width="104" height="66" rx="16" fill="#E9EDFF"/><circle cx="60" cy="47" r="22" fill="#fff"/><g transform="translate(46,33)" color="#2443E8">${ICONS[ic].replace('<svg ', '<svg width="28" height="28" ')}</g></svg></div>`;

/* ---------- Saved ---------- */
function needDays() {
  const per = PACE[S.trip.pace].cap;
  const mins = S.saved.map(id => PBY[id]).filter(p => !isFood(p)).reduce((a, p) => a + loadOf(p), 0);
  return { mins, days: mins / per };
}
function panelSaved() {
  if (!S.saved.length) return `<h1 class="h1">${T.savedTitle}</h1><div class="empty" style="margin-top:20px">${emptyArt('heart')}<b>${T.savedEmptyH}</b>${T.savedEmpty}<div style="margin-top:16px"><button class="btn" data-act="toMap">${ICONS.map}${T.exploreMap}</button></div></div>`;
  const order = tripOrder(), nd = needDays(), n = tripDates().length, ratio = clamp(nd.days / n, 0, 1.4);
  const sig = S.plan && S.plan.sig === planSig();
  return `<h1 class="h1">${T.savedTitle} <span class="muted" style="font-family:var(--sans);font-weight:600">${S.saved.length}</span></h1><p class="lead">${T.savedLead}</p>
    <div class="need"><div class="grow"><b>${T.needDays(Math.max(1, Math.ceil(nd.days * 10) / 10))}</b><small>${T.tripDays(n)} · ${T.paces[S.trip.pace][0]}</small>
      <div class="bar" style="margin-top:8px"><i class="${nd.days > n ? 'over' : ''}" style="width:${Math.min(100, ratio / 1.4 * 100)}%"></i></div></div></div>
    ${nd.days > n ? `<p class="note" style="color:var(--amber)">${T.tooMany}</p>` : ''}
    <div class="sec"><h3>${T.regionOrder}</h3><small>${S.orderManual ? T.orderManual : T.orderAuto}</small></div>
    ${order.map((r, k) => { const ids = S.saved.filter(id => PBY[id].r === r); const hrs = ids.map(id => PBY[id]).filter(p => !isFood(p)).reduce((a, p) => a + p.h, 0);
      return `<div class="list" style="margin-bottom:12px"><div class="rg-head"><span class="cicon" style="background:var(--ink);font-family:var(--serif);font-weight:800;font-size:14px">${k + 1}</span>
        <div class="tx"><b>${esc(rn(r))}</b><small>${T.spots(ids.length)} · ${T.aboutH(Math.round(hrs * 10) / 10)}</small></div>
        <div class="ord"><button data-act="ordUp" data-v="${r}" ${k === 0 ? 'disabled' : ''} aria-label="${T.up}">${ICONS.up}</button><button data-act="ordDown" data-v="${r}" ${k === order.length - 1 ? 'disabled' : ''} aria-label="${T.down}">${ICONS.down}</button></div></div>
        ${ids.map(id => { const p = PBY[id]; return placeRow(p, { sub: `${esc(dn(p.dist))} · ${T.usually(F.dur(p.h * 60))} · ${F.hours(p)}` }); }).join('')}</div>`; }).join('')}
    ${S.orderManual ? `<button class="btn sm ghost" data-act="ordAuto">${ICONS.magic}${T.orderReset}</button>` : ''}
    <div class="stickycta"><button class="btn block" data-act="genPlan">${ICONS.magic}${S.plan ? (sig ? T.viewPlan : T.replan) : T.makePlan(S.saved.length)}</button></div>`;
}

/* ---------- Plan ---------- */
// 분 단위 시각 대신 시간대(오전·점심·오후·저녁)로 보여 준다. 공항 도착·출발만 입력한 시각 그대로.
function slotOf(o) { const e = o.e;
  if (e.k === 'meal') return e.slot === 'dinner' ? T.dinner : T.lunch;
  const t = o.start; return t < 12 ? T.slotAm : t < 17.5 ? T.slotPm : T.slotEve; }
function slotLbl(o, prev) {
  if (o.e.k === 'arrive' || o.e.k === 'depart') return hm(o.start);
  const s = slotOf(o); return prev && !['arrive', 'depart'].includes(prev.e.k) && slotOf(prev) === s ? '' : s; }
function modeLabel(leg) { const k = { walk: 'mWalk', subway: 'mSubway', taxi: 'mTaxi', car: 'mCar', rail: 'mRail', flight: 'mFlight', airport: 'mAirport' }[leg.mode];
  return leg.ov && T[k + 'Ov'] ? T[k + 'Ov'] : T[k]; }
function entryName(o) {
  const e = o.e;
  switch (e.k) {
    case 'arrive': return ORIGINS[e.ap] ? T.eFrom(an(e.ap)) : T.eArrive(an(e.ap));
    case 'checkout': return T.eCheckout(sn(e.stay.id));
    case 'transfer': return T.eTransfer(rn(e.to));
    case 'stay': return e.drop ? T.eDrop(sn(e.stay.id)) : T.ePickup(sn(e.stay.id));
    case 'start': return T.eStart(sn(e.stay.id));
    case 'end': return T.eEnd(sn(e.stay.id));
    case 'depart': return ORIGINS[e.ap] ? T.eBack(an(e.ap)) : T.eDepart(an(e.ap));
    case 'meal': return e.id ? pn(e.id) : (e.slot === 'dinner' ? T.genericDinner : T.genericLunch);
    default: return pn(e.id);
  }
}
function flagPill(f) {
  const [k, v] = f;
  const m = { wait: ['warn', T.fWait(v)], closed: ['warn', T.fClosed], season: ['warn', T.fSeasonOff], shut: ['warn', T.fShut], late: ['warn', T.fLate], night: ['info', T.fNight], eve: ['info', T.fEve], sug: ['sug', T.fSug], free: ['ok', T.fFree(F.dur(v))], depLate: ['warn', T.fDepLate] }[k];
  return m ? `<span class="pill ${m[0]}">${m[1]}</span>` : '';
}
function panelPlan() {
  if (!S.plan) {
    if (!S.saved.length) return `<h1 class="h1">${T.planTitle}</h1><div class="empty" style="margin-top:20px">${emptyArt('cal')}<b>${T.planEmptyH}</b>${T.planEmpty}<div style="margin-top:16px"><button class="btn" data-act="toMap">${ICONS.map}${T.exploreMap}</button></div></div>`;
    return `<h1 class="h1">${T.planTitle}</h1><div class="empty" style="margin-top:20px">${emptyArt('magic')}<b>${T.planReadyH(S.saved.length)}</b>${T.planReady}<div style="margin-top:16px"><button class="btn" data-act="genPlan">${ICONS.magic}${T.makePlan(S.saved.length)}</button></div></div>`;
  }
  const P = S.plan, ds = P.days, n = ds.length, i = clamp(S.ui.day, 0, n - 1), day = ds[i], sc = scheduleDay(P, i);
  document.documentElement.style.setProperty('--lc', LINE[i % LINE.length]);
  const R = [...new Set(ds.map(d => d.r))];
  const route = R.map((r, k) => { const cnt = ds.filter(d => d.r === r).length; const tr = k ? interRegion(R[k - 1], r) : null;
    return `${tr ? `<span class="tr">${ICONS[tr.mode === 'flight' ? 'plane' : 'rail']}${F.dur(tr.ride)}</span>` : ''}<span class="rc">${esc(rn(r))}<small>${T.daysN(cnt)}</small></span>`; }).join('');
  const stale = P.sig !== planSig();
  const totals = ds.map((_, k) => scheduleDay(P, k)).reduce((a, s) => ({ cost: a.cost + s.cost, move: a.move + s.moveMin, places: a.places + s.places }), { cost: 0, move: 0, places: 0 });
  const stays = R.map(r => { const st = STAY_BY[P.stays[r]], sc2 = stayScore(st, r, S.saved), nights = ds.filter((d, k) => d.r === r && k < n - 1).length;
    const dIdx = ds.map((d, k) => d.r === r ? k + 1 : 0).filter(Boolean); 
    const ta = tripAir(), apCode = R[0] === r ? ta.arr : (R[R.length - 1] === r || ta.dom ? ta.dep : (REGIONS[r].air));
    const apMin = gateLeg(apCode, st, r).min;
    return `<div class="stay"><div class="stay-top"><span class="hic">${ICONS.house}</span><div class="tx"><small>${T.stayFor(esc(rn(r)), T.dayRange(dIdx[0], dIdx[dIdx.length - 1]), nights)}</small><b>${esc(sn(st.id))}</b></div>
      <label class="stsel"><span class="vh">${T.changeStay}</span><select data-stay="${r}">${STAYS.filter(s => s.r === r).map(s => `<option value="${s.id}" ${s.id === st.id ? 'selected' : ''}>${esc(sn(s.id))}</option>`).join('')}</select></label></div>
      <div class="stay-why"><div><b>${sc2.total ? T.avgMin(sc2.avg) : '—'}</b>${T.avgMinSub}</div><div><b>${T.nearN(sc2.near, sc2.total)}</b>${T.nearSub}</div>
        <div><b>${esc(tr4(st.st))}</b>${T.stationSub}</div><div><b>${T.apMin(an(apCode), F.dur(apMin))}</b>${ORIGINS[apCode] ? T.originSub : T.apSub}</div>
        <div style="grid-column:1/-1"><b>${T.localCheck}</b>${T.priceLocal}</div></div>
      ${S.stayOv[r] ? `<p class="note">${T.stayManual} <button class="btn sm ghost" data-act="stayAuto" data-v="${r}" style="margin-left:6px">${T.stayAuto}</button></p>` : ''}</div>`; }).join('');
  const rows = sc.rows, last = rows.length - 1;
  let tl = '';
  rows.forEach((o, k) => {
    if (o.leg && o.leg.min) tl += `<div class="seg"><span></span><span class="rl"></span><div class="sg">${ICONS[MODE_ICON[o.leg.mode]] || ''}<span><b>${modeLabel(o.leg)} ${F.dur(o.leg.min)}</b>${o.leg.km ? ` · ${o.leg.km < 1 ? Math.round(o.leg.km * 1000) + 'm' : o.leg.km.toFixed(1) + 'km'}` : ''}</span></div></div>`;
    const e = o.e, sp = !['place', 'meal'].includes(e.k), p = e.id ? PBY[e.id] : null;
    const tags = (o.flags || []).map(flagPill).join('') + (e.k === 'meal' ? `<span class="pill" style="background:#FFF1E3;color:#B5560F">${e.slot === 'dinner' ? T.dinner : T.lunch}</span>` : '');
    const sub = p ? `${esc(T.cats[p.c])} · ${F.dur(p.h * 60)}` : (e.k === 'transfer' ? `${T.mRail === modeLabel(o.leg || {}) ? '' : ''}${esc(rn(e.from))} → ${esc(rn(e.to))}` : '');
    const gi = e.ap && ORIGINS[e.ap] ? { rail: 'rail', car: 'taxi', air: 'plane' }[ORIGINS[e.ap].g] : 'plane';
    const icon = sp ? ({ arrive: gi, depart: gi, transfer: (o.leg && o.leg.mode === 'flight') ? 'plane' : 'rail', checkout: 'house', stay: 'house', start: 'house', end: 'house' }[e.k]) : null;
    tl += `<div class="ent ${sp ? 'sp' : ''} ${e.k === 'meal' ? 'meal' : ''} ${k === 0 ? 'first' : ''} ${k === last ? 'last' : ''}">
      <div class="tm">${slotLbl(o, rows[k - 1])}</div><div class="rl"><i>${sp ? ICONS[icon] : (o.num || '')}</i></div>
      <div class="bx">${p ? `<button class="tx" style="text-align:left" data-act="openPlace" data-v="${p.id}">` : '<div class="tx">'}<div class="nm">${esc(entryName(o))}</div>${sub ? `<div class="sub">${sub}</div>` : ''}${tags ? `<div class="tags">${tags}</div>` : ''}${p ? '</button>' : '</div>'}
      ${!sp ? `<button class="more" data-act="stopMenu" data-v="${e.si}" aria-label="${T.more}">${ICONS.more}</button>` : ''}</div></div>`;
  });
  const uns = P.unsched.filter(u => PBY[u.id]);
  return `<div class="eyebrow">${F.date(ds[0].date)} – ${F.date(ds[n - 1].date)} · ${F.nights(n)} · ${T.ppl(S.trip.people)}</div>
    <div class="row" style="justify-content:space-between;align-items:flex-start"><h1 class="h1">${T.planTitle}</h1><button class="btn sm ghost" data-act="genPlan">${ICONS.magic}${T.replanShort}</button></div>
    <div class="route">${route}</div>
    ${stale ? `<div class="banner">${ICONS.info.replace('<svg ', '<svg width="20" height="20" style="flex-shrink:0" ')}<span class="grow">${T.stale}</span><button class="btn sm" data-act="genPlan">${T.replanShort}</button></div>` : ''}
    ${P.warn && P.warn.k === 'farDep' ? `<div class="banner">${ICONS.warn.replace('<svg ', '<svg width="20" height="20" style="flex-shrink:0" ')}<span class="grow">${T.farDep(rn(P.warn.r), F.dur(P.warn.min))}</span><button class="btn sm ghost" data-act="trip">${T.editTrip}</button></div>` : ''}
    <div class="sec"><h3>${T.staysTitle}</h3><small>${T.staysSub}</small></div><div class="stays">${stays}</div>
    <div class="sec"><h3>${T.byDay}</h3><small>${T.byDaySub}</small></div>
    <div class="days">${ds.map((d, k) => `<button class="dchip ${k === i ? 'on' : ''}" style="--c:${LINE[k % LINE.length]}" data-act="day" data-v="${k}"><span class="n">${k + 1}</span><span class="d"><b>${F.date(d.date)}</b><small>${esc(rn(d.r))}</small></span></button>`).join('')}</div>
    <div class="dhead"><div><h2>${T.day(i + 1)} · ${esc(rn(day.r))}</h2><small>${F.date(day.date, true)} · ${T.daySumOv(sc.places, F.dur(sc.moveMin))}</small></div></div>
    <div class="routebox inline" id="rbox"></div>
    <div class="tl">${tl}</div>
    <div class="dayacts"><button class="btn sm ghost" data-act="optDay" data-v="${i}">${ICONS.magic}${T.optimize}</button><button class="btn sm ghost" data-act="addStop" data-v="${i}">${ICONS.plus}${T.addStop}</button></div>
    ${uns.length ? `<div class="sec"><h3>${T.unsched}</h3><small>${T.unschedSub}</small></div><div class="list">${uns.map(u => { const p = PBY[u.id]; const can = ds.some(d => d.r === p.r);
      return `<div class="prow">${cicon(p.c)}<span class="tx"><span class="nm">${esc(pn(u.id))}</span><span class="ds">${esc(rn(p.r))} · ${T.why[u.why] || ''}</span></span>${can ? `<button class="btn sm soft" data-act="placeUns" data-v="${u.id}">${T.putIn}</button>` : ''}</div>`; }).join('')}</div>` : ''}
    <div class="tot"><div><small>${T.totalPlaces}</small><b>${T.spots(totals.places)}</b></div><div><small>${T.totalMove}</small><b>${F.dur(totals.move)}</b></div></div>
    <p class="note">${T.planNote}</p>
    ${prepCard(4)}
    ${(rows => rows ? `<div class="sec"><h3>${T.atTitle}</h3><small>${koOnly()}</small></div><div class="around">${rows}</div>` : '')(R.map(r => aroundCard(r, null, 'rows')).join(''))}
    <div class="stickycta"><button class="btn block" data-act="toPrep">${ICONS.ticket}${T.toPrep}</button></div>`;
}
/* ---------- 여행 준비: 어라운드툴 계산기·가이드가 정보를 댄다 ---------- */
function prepItems() {
  const pr = AROUND && AROUND.prep; if (!pr) return { tools: [], guides: [] };
  const ta = tripAir(), fit = x => x.when === 'all' || x.when === ta.cc || (x.when === 'ov' && ta.ov);
  const rank = x => x.when === ta.cc ? 0 : x.when === 'all' ? 2 : 1;
  return { tools: pr.tools.filter(fit).sort((a, b) => rank(a) - rank(b)), guides: pr.guides.filter(fit).sort((a, b) => rank(a) - rank(b)) };
}
const prepRow = (x, ic) => ext(x.url, `<span class="cicon sm" style="background:var(--at)">${ICONS[ic]}</span><span class="tx"><b lang="ko">${esc(x.name)}</b>${x.desc ? `<small lang="ko">${esc(x.desc.length > 46 ? x.desc.slice(0, 45) + '…' : x.desc)}</small>` : ''}</span>${ICONS.right}`, 'arow');
function prepCard(max) {
  const it = prepItems(), rows = [...it.tools.map(x => prepRow(x, 'ticket')), ...it.guides.map(x => prepRow(x, 'info'))].slice(0, max || 99);
  return rows.length ? `<div class="sec"><h3>${T.prepTitle}</h3><small>${koOnly()}</small></div><div class="around">${rows.join('')}</div>` : '';
}
function panelPrep() {
  const it = prepItems(), P = S.plan, R = P ? [...new Set(P.days.map(d => d.r))] : savedRegions();
  const trips = R.map(r => aroundCard(r, null, 'rows')).join('');
  return `<h1 class="h1">${T.prepTitle}</h1><p class="lead">${T.prepLead}</p>
    ${trips ? `<div class="sec"><h3>${T.prepTrip}</h3><small>${koOnly()}</small></div><div class="around">${trips}</div>` : ''}
    ${it.tools.length ? `<div class="sec"><h3>${T.prepTools}</h3><small>${koOnly()}</small></div><div class="around">${it.tools.map(x => prepRow(x, 'ticket')).join('')}</div>` : ''}
    ${it.guides.length ? `<div class="sec"><h3>${T.prepGuides}</h3><small>${koOnly()}</small></div><div class="around">${it.guides.map(x => prepRow(x, 'info')).join('')}</div>` : ''}
    ${P ? `<div style="margin-top:18px"><button class="btn ghost block" data-act="copyTxt">${ICONS.copy}${T.copyTxt}</button></div>` : ''}
    <p class="note">${T.atBy}</p>`;
}
function afterPlanRender() {
  $$('[data-stay]', pin).forEach(s => s.onchange = () => { S.stayOv[s.dataset.stay] = s.value; regenerate(true); });
  const rb = $('#rbox');
  if (rb && !isDesk() && S.plan) { const tmp = Map2D.host; Map2D.mount(rb); Map2D.showRoute(S.plan, clamp(S.ui.day, 0, S.plan.days.length - 1), { top: 24 }); if (tmp && tmp !== rb) { /* stage map remounts on map tab */ } }
}
function regenerate(keepDay) {
  const prev = S.ui.day; S.plan = generatePlan(); S.ui.day = keepDay ? clamp(prev, 0, S.plan ? S.plan.days.length - 1 : 0) : 0; persist();
  renderAll(); toast(T.planned);
}

/* ---------- 어라운드툴 추천 코스: 여행 가이드 일정을 그대로 담는다 ---------- */
function courseCards(r) {
  const cs = ((aroundRegion(r) || {}).courses || []).filter(c => c.days.some(d => d.ids.some(id => PBY[id])));
  if (!cs.length) return '';
  return `<div class="sec"><h3>${T.coursesTitle}</h3><small>${T.coursesSub}</small></div><div class="crs">${cs.map((c, k) => `<div class="crs-c">
    <div class="crs-h"><b lang="ko">${esc(c.t.replace(/\s*—.*$/, ''))}</b>${c.t.includes('—') ? `<small lang="ko">${esc(c.t.replace(/^.*?—\s*/, ''))}</small>` : ''}</div>
    <ol class="crs-d">${c.days.map((d, i) => `<li style="--lc:${LINE[i % LINE.length]}"><span class="n">${i + 1}</span><span class="s">${d.ids.filter(id => PBY[id]).map(id => esc(pn(id))).join(' → ') || `<em lang="ko">${esc(d.t)}</em>`}</span></li>`).join('')}</ol>
    <div class="crs-a"><button class="btn sm" data-act="loadCourse" data-v="${r}:${k}">${ICONS.magic}${T.courseLoad}</button>${ext(c.url, T.courseOpen, 'btn sm ghost')}</div></div>`).join('')}</div>`;
}
function loadCourse(v) {
  const [r, k] = v.split(':'), c = ((aroundRegion(r) || {}).courses || []).filter(c => c.days.some(d => d.ids.some(id => PBY[id])))[+k]; if (!c) return;
  const days = c.days.map(d => d.ids.filter(id => PBY[id])), ids = days.flat();
  S.saved = [...S.saved.filter(id => PBY[id].r !== r), ...ids]; savedRegions();
  if (S.order.length === 1) S.trip.end = addDays(S.trip.start, days.length - 1);
  S.course = { r, days }; S.plan = generatePlan(); S.ui.day = 0; persist(); track('klink_course', { region: r }); go('plan'); toast(T.courseLoaded(ids.length));
}

/* ---------- 일정 텍스트 ---------- */
function itineraryText() {
  const P = S.plan, L = [];
  const ds = P.days; L.push(`${T.brand} · ${F.date(ds[0].date)}–${F.date(ds[ds.length - 1].date)} (${F.nights(ds.length)})`);
  ds.forEach((d, i) => { L.push(''); L.push(`[${T.day(i + 1)} · ${F.date(d.date, true)} · ${rn(d.r)}]`);
    { let prev = null; scheduleDay(P, i).rows.forEach(o => { if (['start', 'end'].includes(o.e.k)) return; const lb = slotLbl(o, prev); prev = o; L.push(`${lb ? `[${lb}] ` : '    '}${entryName(o)}`); }); } });
  L.push(''); [...new Set(ds.map(d => d.r))].forEach(r => L.push(`${T.staysTitle}: ${rn(r)} ${sn(P.stays[r])}`));
  return L.join('\n');
}
/* ---------- actions (views) ---------- */
Object.assign(ACT, {
  toMap: () => go('map'), toPlanTab: () => go('plan'), toPrep: () => go('prep'), loadCourse: v => loadCourse(v), trip: () => openTrip(),
  ordUp: v => { const o = tripOrder(), k = o.indexOf(v); if (k > 0) { [o[k - 1], o[k]] = [o[k], o[k - 1]]; S.order = o; S.orderManual = true; persist(); renderPanel(); } },
  ordDown: v => { const o = tripOrder(), k = o.indexOf(v); if (k >= 0 && k < o.length - 1) { [o[k + 1], o[k]] = [o[k], o[k + 1]]; S.order = o; S.orderManual = true; persist(); renderPanel(); } },
  ordAuto: () => { S.orderManual = false; persist(); renderPanel(); },
  genPlan: () => { if (S.ui.tab === 'saved' && S.plan && S.plan.sig === planSig()) { go('plan'); return; } S.plan = generatePlan(); S.ui.day = 0; persist(); track('klink_plan', { places: S.saved.length }); go('plan'); toast(T.planned); },
  day: v => { S.ui.day = +v; persist(); renderPanel(); if (isDesk()) renderStage(); },
  openPlace: v => selectPlace(v),
  stopMenu: (v, el) => { const i = S.ui.day, si = +v, st = S.plan.days[i].stops, e = st[si];
    const others = S.plan.days.map((d, k) => ({ d, k })).filter(x => x.k !== i && x.d.r === S.plan.days[i].r);
    const items = [{ icon: 'up', label: T.mUp, disabled: si === 0, fn: () => { Plan.move(i, si, -1); renderPanel(); if (isDesk()) renderStage(); } },
      { icon: 'down', label: T.mDown, disabled: si === st.length - 1, fn: () => { Plan.move(i, si, 1); renderPanel(); if (isDesk()) renderStage(); } }];
    if (e.k === 'meal') items.push({ icon: 'swap', label: T.mSwap, fn: () => { if (!Plan.swapMeal(i, si)) toast(T.noOther); renderPanel(); if (isDesk()) renderStage(); } });
    others.forEach(x => items.push({ icon: 'move', label: T.mMoveTo(x.k + 1), fn: () => { Plan.moveTo(i, si, x.k); toast(T.movedTo(x.k + 1)); renderPanel(); if (isDesk()) renderStage(); } }));
    if (e.id) items.push({ icon: 'taxi', label: T.taxiCard, fn: () => openTaxi(e.id) });
    items.push('-', { icon: 'trash', label: T.mRemove, danger: true, fn: () => { Plan.remove(i, si); renderPanel(); if (isDesk()) renderStage(); } });
    openMenu(el, items); },
  optDay: v => { Plan.optimize(+v); toast(T.optimized); renderPanel(); if (isDesk()) renderStage(); },
  addStop: (v, el) => { const i = +v, r = S.plan.days[i].r; const inPlan = new Set(S.plan.days.flatMap(d => d.stops.map(s => s.id)).filter(Boolean));
    const cands = [...S.plan.unsched.map(u => u.id).filter(id => PBY[id] && PBY[id].r === r), ...S.saved.filter(id => PBY[id].r === r && !inPlan.has(id))];
    const uniq = [...new Set(cands)];
    openModal(`<h3>${T.addStopT(i + 1)}</h3><p class="lead">${T.addStopLead}</p><div class="list" style="margin-top:14px">${uniq.length ? uniq.map(id => `<button class="prow" data-add="${id}">${cicon(PBY[id].c)}<span class="tx"><span class="nm">${esc(pn(id))}</span><span class="ds">${esc(dn(PBY[id].dist))} · ${F.dur(PBY[id].h * 60)}</span></span>${ICONS.plus.replace('<svg ', '<svg width="20" height="20" ')}</button>`).join('') : `<div class="empty">${T.addStopNone}</div>`}</div>
      <div style="display:flex;gap:8px;margin-top:14px"><button class="btn ghost" style="flex:1" data-close>${T.close}</button><button class="btn" style="flex:1" id="addmap">${ICONS.map}${T.findMore}</button></div>`,
      m => { $$('[data-add]', m).forEach(b => b.onclick = () => { Plan.add(b.dataset.add, i); closeModal(); toast(T.addedDay(i + 1)); renderPanel(); if (isDesk()) renderStage(); }); $('#addmap', m).onclick = () => { closeModal(); go('map'); openRegion(r); }; }); },
  placeUns: (v, el) => { const p = PBY[v]; openMenu(el, S.plan.days.map((d, k) => ({ d, k })).filter(x => x.d.r === p.r).map(x => ({ icon: 'cal', label: `${T.day(x.k + 1)} · ${F.date(x.d.date)}`, fn: () => { Plan.add(v, x.k); toast(T.addedDay(x.k + 1)); S.ui.day = x.k; renderPanel(); if (isDesk()) renderStage(); } }))); },
  stayAuto: v => { delete S.stayOv[v]; regenerate(true); },
  copyTxt: async () => { const txt = itineraryText(); try { await navigator.clipboard.writeText(txt); toast(T.copied); } catch (e) {
      openModal(`<h3>${T.copyTxt}</h3><textarea class="txtin" style="height:300px;margin-top:12px" readonly>${esc(txt)}</textarea><button class="btn block ink" style="margin-top:12px" data-close>${T.close}</button>`); } },
});
const _renderPanel0 = renderPanel;
renderPanel = function () { _renderPanel0(); if (S.ui.tab === 'plan') afterPlanRender(); };
