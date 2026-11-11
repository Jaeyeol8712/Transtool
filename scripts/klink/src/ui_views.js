'use strict';
/* =========================================================
   Saved, Plan, Book views
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
function modeLabel(leg) { const k = { walk: 'mWalk', subway: 'mSubway', taxi: 'mTaxi', car: 'mCar', rail: 'mRail', flight: 'mFlight', airport: 'mAirport' }[leg.mode]; return T[k]; }
function entryName(o) {
  const e = o.e;
  switch (e.k) {
    case 'arrive': return T.eArrive(an(e.ap));
    case 'checkout': return T.eCheckout(sn(e.stay.id));
    case 'transfer': return T.eTransfer(rn(e.to));
    case 'stay': return e.drop ? T.eDrop(sn(e.stay.id)) : T.ePickup(sn(e.stay.id));
    case 'start': return T.eStart(sn(e.stay.id));
    case 'end': return T.eEnd(sn(e.stay.id));
    case 'depart': return T.eDepart(an(e.ap));
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
    const dIdx = ds.map((d, k) => d.r === r ? k + 1 : 0).filter(Boolean); const band = (PRICE[r] || PRICE.other)[S.trip.budget];
    const apCode = (R[0] === r && AIRPORTS[S.trip.arr].r === r) ? S.trip.arr : (R[R.length - 1] === r ? S.trip.dep : (REGIONS[r].air));
    const apMin = airportLeg(apCode, st, r).min;
    return `<div class="stay"><div class="stay-top"><span class="hic">${ICONS.house}</span><div class="tx"><small>${T.stayFor(esc(rn(r)), T.dayRange(dIdx[0], dIdx[dIdx.length - 1]), nights)}</small><b>${esc(sn(st.id))}</b></div>
      <label class="stsel"><span class="vh">${T.changeStay}</span><select data-stay="${r}">${STAYS.filter(s => s.r === r).map(s => `<option value="${s.id}" ${s.id === st.id ? 'selected' : ''}>${esc(sn(s.id))}</option>`).join('')}</select></label></div>
      <div class="stay-why"><div><b>${sc2.total ? T.avgMin(sc2.avg) : '—'}</b>${T.avgMinSub}</div><div><b>${T.nearN(sc2.near, sc2.total)}</b>${T.nearSub}</div>
        <div><b>${esc(tr4(st.st))}</b>${T.stationSub}</div><div><b>${T.apMin(an(apCode), F.dur(apMin))}</b>${T.apSub}</div>
        <div style="grid-column:1/-1"><b>${T.priceBand(band[0], band[1])}</b>${T.priceSub(T.budgets[S.trip.budget][0])}</div></div>
      ${S.stayOv[r] ? `<p class="note">${T.stayManual} <button class="btn sm ghost" data-act="stayAuto" data-v="${r}" style="margin-left:6px">${T.stayAuto}</button></p>` : ''}</div>`; }).join('');
  const rows = sc.rows, last = rows.length - 1;
  let tl = '';
  rows.forEach((o, k) => {
    if (o.leg && o.leg.min) tl += `<div class="seg"><span></span><span class="rl"></span><div class="sg">${ICONS[MODE_ICON[o.leg.mode]] || ''}<span><b>${modeLabel(o.leg)} ${F.dur(o.leg.min)}</b>${o.leg.km ? ` · ${o.leg.km < 1 ? Math.round(o.leg.km * 1000) + 'm' : o.leg.km.toFixed(1) + 'km'}` : ''}${o.leg.cost ? ` · ${o.leg.group ? T.perGroup(F.money(o.leg.cost)) : T.perPerson(F.money(o.leg.cost))}` : ''}</span></div></div>`;
    const e = o.e, sp = !['place', 'meal'].includes(e.k), p = e.id ? PBY[e.id] : null;
    const tags = (o.flags || []).map(flagPill).join('') + (p && p.rsv ? `<span class="pill rsv">${T.needRsv}</span>` : '') + (e.k === 'meal' ? `<span class="pill" style="background:#FFF1E3;color:#B5560F">${e.slot === 'dinner' ? T.dinner : T.lunch}</span>` : '');
    const sub = p ? `${esc(T.cats[p.c])} · ${F.dur(p.h * 60)}${p.cost ? ` · ${T.perPerson(F.money(p.cost))}` : ''}` : (e.k === 'transfer' ? `${T.mRail === modeLabel(o.leg || {}) ? '' : ''}${esc(rn(e.from))} → ${esc(rn(e.to))}` : '');
    const icon = sp ? ({ arrive: 'plane', depart: 'plane', transfer: (o.leg && o.leg.mode === 'flight') ? 'plane' : 'rail', checkout: 'house', stay: 'house', start: 'house', end: 'house' }[e.k]) : null;
    tl += `<div class="ent ${sp ? 'sp' : ''} ${e.k === 'meal' ? 'meal' : ''} ${k === 0 ? 'first' : ''} ${k === last ? 'last' : ''}">
      <div class="tm">${hm(o.start)}${!sp && o.end ? `<small>~${hm(o.end)}</small>` : ''}</div><div class="rl"><i>${sp ? ICONS[icon] : (o.num || '')}</i></div>
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
    <div class="dhead"><div><h2>${T.day(i + 1)} · ${esc(rn(day.r))}</h2><small>${F.date(day.date, true)} · ${T.daySum(sc.places, F.dur(sc.moveMin), F.money(sc.cost))}</small></div></div>
    <div class="routebox inline" id="rbox"></div>
    <div class="tl">${tl}</div>
    <div class="dayacts"><button class="btn sm ghost" data-act="optDay" data-v="${i}">${ICONS.magic}${T.optimize}</button><button class="btn sm ghost" data-act="addStop" data-v="${i}">${ICONS.plus}${T.addStop}</button></div>
    ${uns.length ? `<div class="sec"><h3>${T.unsched}</h3><small>${T.unschedSub}</small></div><div class="list">${uns.map(u => { const p = PBY[u.id]; const can = ds.some(d => d.r === p.r);
      return `<div class="prow">${cicon(p.c)}<span class="tx"><span class="nm">${esc(pn(u.id))}</span><span class="ds">${esc(rn(p.r))} · ${T.why[u.why] || ''}</span></span>${can ? `<button class="btn sm soft" data-act="placeUns" data-v="${u.id}">${T.putIn}</button>` : ''}</div>`; }).join('')}</div>` : ''}
    <div class="tot"><div><small>${T.totalPP}</small><b>${F.money(totals.cost)}</b></div><div><small>${T.totalMove}</small><b>${F.dur(totals.move)}</b></div></div>
    <p class="note">${T.planNote}</p>
    ${(rows => rows ? `<div class="sec"><h3>${T.atTitle}</h3><small>${koOnly()}</small></div><div class="around">${rows}</div>` : '')(R.map(r => aroundCard(r, null, 'rows')).join(''))}
    <div class="stickycta"><button class="btn block" data-act="toBook">${ICONS.ticket}${T.toBook}</button></div>`;
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

/* ---------- Book ---------- */
function bookItems() {
  if (!S.plan) return { rsv: [], stays: [], days: [] };
  const rsv = [];
  S.plan.days.forEach((d, i) => { const sc = scheduleDay(S.plan, i); sc.rows.forEach(o => { const p = o.e.id && PBY[o.e.id]; if (p && p.rsv) rsv.push({ key: `${i}:${p.id}`, p, i, t: o.start, price: p.c === 'skin' ? 90000 : p.c === 'food' ? 5000 : 0, kind: p.c === 'skin' ? 'clinic' : p.c === 'food' ? 'table' : 'ticket' }); }); });
  const R = [...new Set(S.plan.days.map(d => d.r))], n = S.plan.days.length;
  const stays = R.map(r => ({ r, st: STAY_BY[S.plan.stays[r]], nights: S.plan.days.filter((d, k) => d.r === r && k < n - 1).length })).filter(x => x.nights > 0);
  return { rsv, stays, days: S.plan.days };
}
const GUIDE = { half: 160000, full: 300000 };
function bookTotal() { const b = bookItems(); let sum = 0, cnt = 0;
  b.rsv.forEach(x => { if (S.book.rsv[x.key] !== false) { sum += x.price; cnt++; } });
  b.stays.forEach(x => { if (S.book.stay[x.r] !== false) cnt++; });
  Object.values(S.book.guide).forEach(g => { if (GUIDE[g]) { sum += GUIDE[g]; cnt++; } });
  return { sum, cnt }; }
function panelBook() {
  if (!S.plan) return `<h1 class="h1">${T.bookTitle}</h1><div class="empty" style="margin-top:20px">${emptyArt('ticket')}<b>${T.bookEmptyH}</b>${T.bookEmpty}<div style="margin-top:16px"><button class="btn" data-act="toPlanTab">${ICONS.cal}${T.planTitle}</button></div></div>`;
  if (S.paid) return paidView();
  const b = bookItems(), tot = bookTotal();
  const sw = on => `<span class="sw"></span>`;
  return `<h1 class="h1">${T.bookTitle}</h1><p class="lead">${T.bookLead}</p>
    <div class="sec"><h3>${T.bRsv}</h3><small>${T.spots(b.rsv.length)}</small></div>
    <div class="list">${b.rsv.length ? b.rsv.map(x => `<button class="bitem ${S.book.rsv[x.key] !== false ? 'on' : ''}" data-act="tglRsv" data-v="${x.key}">${cicon(x.p.c)}<span class="tx"><span class="nm">${esc(pn(x.p.id))}</span>
      <span class="sub">${T.day(x.i + 1)} ${hm(x.t)} · ${T.bKind[x.kind]}</span></span><span class="pr ${x.price ? '' : 'free'}">${x.price ? F.full(x.price) : T.free}</span>${sw()}</button>`).join('') : `<div class="empty" style="padding:18px">${T.bNoRsv}</div>`}</div>
    <div class="sec"><h3>${T.bStay}</h3><small>${T.bStaySub}</small></div>
    <div class="list">${b.stays.map(x => { const band = (PRICE[x.r] || PRICE.other)[S.trip.budget];
      return `<button class="bitem ${S.book.stay[x.r] !== false ? 'on' : ''}" data-act="tglStay" data-v="${x.r}"><span class="cicon" style="background:var(--ink)">${ICONS.house}</span><span class="tx"><span class="nm">${esc(rn(x.r))} · ${esc(sn(x.st.id))}</span>
      <span class="sub">${T.nightsOnly(x.nights)} · ${T.priceBand(band[0], band[1])}</span></span><span class="pr free">${T.freeAgency}</span>${sw()}</button>`; }).join('') || `<div class="empty" style="padding:18px">${T.bNoStay}</div>`}</div>
    <div class="sec"><h3>${T.bGuide}</h3><small>${T.bGuideSub}</small></div>
    <div class="list">${b.days.map((d, i) => { const g = S.book.guide[i] || 'none';
      return `<div class="bitem"><span class="cicon" style="background:${LINE[i % LINE.length]};font-family:var(--serif);font-weight:800">${i + 1}</span><span class="tx"><span class="nm">${T.day(i + 1)} · ${esc(rn(d.r))}</span><span class="sub">${F.date(d.date)}</span></span>
        <span class="segc">${['none', 'half', 'full'].map(k => `<button class="${g === k ? 'on' : ''}" data-act="guide" data-v="${i}:${k}">${T.gOpt[k]}</button>`).join('')}</span></div>`; }).join('')}</div>
    <p class="note">${T.guideNote}</p>
    <div class="paybar"><div class="t"><small>${T.selN(tot.cnt)}</small><b>${F.full(tot.sum)}${tot.sum ? `<em>≈ ¥${Math.round(tot.sum / 195).toLocaleString()}</em>` : ''}</b></div>
      <button class="btn wechat block" data-act="pay">${tot.sum ? T.payBtn : T.sendBtn}</button></div>`;
}
function itineraryText() {
  const P = S.plan, L = [];
  const ds = P.days; L.push(`${T.brand} · ${F.date(ds[0].date)}–${F.date(ds[ds.length - 1].date)} (${F.nights(ds.length)})`);
  ds.forEach((d, i) => { L.push(''); L.push(`[${T.day(i + 1)} · ${F.date(d.date, true)} · ${rn(d.r)}]`);
    scheduleDay(P, i).rows.forEach(o => { if (['start', 'end'].includes(o.e.k)) return; L.push(`${hm(o.start)}  ${entryName(o)}`); }); });
  L.push(''); [...new Set(ds.map(d => d.r))].forEach(r => L.push(`${T.staysTitle}: ${rn(r)} ${sn(P.stays[r])}`));
  return L.join('\n');
}
function paidView() {
  const P = S.plan, ds = P.days, name = (S.trip.name || '').trim() || T.guest;
  const days = ds.map((d, i) => `<div class="dy" style="--lc:${LINE[i % LINE.length]}"><b>${T.day(i + 1)} · ${F.date(d.date)} · ${esc(rn(d.r))}</b>${scheduleDay(P, i).rows.filter(o => ['place', 'meal', 'transfer', 'arrive', 'depart'].includes(o.e.k)).map(o => `<div><span>${hm(o.start)}</span>${esc(entryName(o))}</div>`).join('')}</div>`).join('');
  return `<div class="eyebrow" style="color:var(--green)">${ICONS.check.replace('<svg ', '<svg width="16" height="16" ')}${T.paidEyebrow}</div><h1 class="h1">${T.paidH}</h1><p class="lead">${T.paidLead}</p>
    <div class="wcard"><div class="wmsg"><span class="av">${ICONS.logo}</span><span class="bub">${esc(T.wMsg(name))}</span></div>
      <div class="wmsg"><span class="av">${ICONS.logo}</span><div class="wsched"><div class="hd"><small>${T.brand} · ${F.nights(ds.length)}</small><b>${F.date(ds[0].date)} – ${F.date(ds[ds.length - 1].date)}</b></div>${days}</div></div>
      <div id="chatlog">${S.chat.map(m => `<div class="wmsg ${m.me ? 'me' : ''}"><span class="av">${m.me ? esc([...name][0]) : ICONS.logo}</span><span class="bub">${esc(m.t)}</span></div>`).join('')}</div>
      <div class="chatin"><input id="chatq" placeholder="${esc(T.chatPh)}"><button class="btn sm wechat" data-act="chatSend">${T.send}</button></div></div>
    <div style="display:flex;gap:8px;margin-top:14px"><button class="btn ghost" style="flex:1" data-act="copyTxt">${ICONS.copy}${T.copyTxt}</button><button class="btn ghost" style="flex:1" data-act="unpay">${T.editBook}</button></div>
    <p class="note">${T.demoNote}</p>`;
}
async function chatSend() {
  const q = $('#chatq'); const t = q.value.trim(); if (!t) return; q.value = '';
  const log = $('#chatlog'), name = (S.trip.name || '').trim() || T.guest;
  S.chat.push({ me: true, t }); log.insertAdjacentHTML('beforeend', `<div class="wmsg me"><span class="av">${esc([...name][0])}</span><span class="bub">${esc(t)}</span></div>`);
  log.insertAdjacentHTML('beforeend', `<div class="wmsg" id="typing"><span class="av">${ICONS.logo}</span><span class="bub">…</span></div>`);
  let reply = null;
  if (sample) { try { const r = await sample(`You are a K-Link travel concierge on WeChat. Reply in the same language as the customer (default ${LANGS.find(l => l[0] === S.lang)[1]}), 2-3 friendly sentences. Never claim a booking is confirmed unless listed as booked.\nTrip:\n${itineraryText()}\nCustomer: ${t}`, { modelTier: 'quick', cache: false }); reply = (r.text || '').trim(); } catch (e) { if (e && e.code === 'not_granted') sample = null; } }
  if (!reply) reply = /谢|고마|감사|thank|ありがと/i.test(t) ? T.thanks : T.autoReply;
  $('#typing') && $('#typing').remove(); S.chat.push({ me: false, t: reply }); persist();
  log.insertAdjacentHTML('beforeend', `<div class="wmsg"><span class="av">${ICONS.logo}</span><span class="bub">${esc(reply)}</span></div>`);
}

/* ---------- actions (views) ---------- */
Object.assign(ACT, {
  toMap: () => go('map'), toPlanTab: () => go('plan'), toBook: () => go('book'), trip: () => openTrip(),
  ordUp: v => { const o = tripOrder(), k = o.indexOf(v); if (k > 0) { [o[k - 1], o[k]] = [o[k], o[k - 1]]; S.order = o; S.orderManual = true; persist(); renderPanel(); } },
  ordDown: v => { const o = tripOrder(), k = o.indexOf(v); if (k >= 0 && k < o.length - 1) { [o[k + 1], o[k]] = [o[k], o[k + 1]]; S.order = o; S.orderManual = true; persist(); renderPanel(); } },
  ordAuto: () => { S.orderManual = false; persist(); renderPanel(); },
  genPlan: () => { if (S.ui.tab === 'saved' && S.plan && S.plan.sig === planSig()) { go('plan'); return; } S.plan = generatePlan(); S.ui.day = 0; S.paid = false; persist(); go('plan'); toast(T.planned); },
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
  tglRsv: v => { S.book.rsv[v] = S.book.rsv[v] === false; persist(); renderPanel(); },
  tglStay: v => { S.book.stay[v] = S.book.stay[v] === false; persist(); renderPanel(); },
  guide: v => { const [i, k] = v.split(':'); if (k === 'none') delete S.book.guide[i]; else S.book.guide[i] = k; persist(); renderPanel(); },
  pay: () => { const t = bookTotal(); if (!t.sum) { S.paid = true; persist(); renderPanel(); return; }
    openModal(`<h3>${T.payT}</h3><p class="lead">${T.demoNote}</p><div class="list" style="margin-top:14px">${bookItems().rsv.filter(x => S.book.rsv[x.key] !== false && x.price).map(x => `<div class="bitem"><span class="tx"><span class="nm">${esc(pn(x.p.id))}</span><span class="sub">${T.bKind[x.kind]}</span></span><span class="pr">${F.full(x.price)}</span></div>`).join('')}
      ${Object.entries(S.book.guide).filter(([, g]) => GUIDE[g]).map(([i, g]) => `<div class="bitem"><span class="tx"><span class="nm">${T.day(+i + 1)} · ${T.gOpt[g]}</span><span class="sub">${T.bGuide}</span></span><span class="pr">${F.full(GUIDE[g])}</span></div>`).join('')}</div>
      <div class="tot" style="grid-template-columns:1fr"><div><small>${T.total}</small><b>${F.full(t.sum)} · ≈ ¥${Math.round(t.sum / 195).toLocaleString()}</b></div></div>
      <div style="display:flex;gap:8px;margin-top:16px"><button class="btn ghost" style="flex:.7" data-close>${T.cancel}</button><button class="btn wechat" style="flex:1" id="payok">${T.payNow}</button></div>`,
      m => { $('#payok', m).onclick = () => { S.paid = true; persist(); closeModal(); renderPanel(); toast(T.paidToast); }; }); },
  unpay: () => { S.paid = false; persist(); renderPanel(); },
  copyTxt: async () => { const txt = itineraryText(); try { await navigator.clipboard.writeText(txt); toast(T.copied); } catch (e) {
      openModal(`<h3>${T.copyTxt}</h3><textarea class="txtin" style="height:300px;margin-top:12px" readonly>${esc(txt)}</textarea><button class="btn block ink" style="margin-top:12px" data-close>${T.close}</button>`); } },
  chatSend: () => chatSend()
});
const _renderPanel0 = renderPanel;
renderPanel = function () { _renderPanel0(); if (S.ui.tab === 'plan') afterPlanRender(); if (S.ui.tab === 'book' && S.paid) { const q = $('#chatq'); if (q) q.onkeydown = e => { if (e.key === 'Enter' && !e.isComposing) chatSend(); }; } };
