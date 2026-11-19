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
    case 'arrive': return tripAir().home ? T.eFrom(an(e.ap)) : T.eArrive(an(e.ap));
    case 'checkout': return T.eCheckout(sn(e.stay.id));
    case 'transfer': return T.eTransfer(rn(e.to));
    case 'stay': return e.drop ? T.eDrop(sn(e.stay.id)) : T.ePickup(sn(e.stay.id));
    case 'start': return T.eStart(sn(e.stay.id));
    case 'end': return T.eEnd(sn(e.stay.id));
    case 'depart': return tripAir().home ? T.eBack(an(e.ap)) : T.eDepart(an(e.ap));
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
    const ta = tripAir(), apCode = R[0] === r ? ta.arr : (R[R.length - 1] === r ? ta.dep : (REGIONS[r].air));
    const apMin = airportLeg(apCode, st, r).min;
    return `<details class="k-stay"><summary><b>${esc(rn(r))}</b><span class="nm">${esc(sn(st.id))}</span><span class="mt">${esc(tr4(st.st))}${sc2.total ? ` · 평균 ${sc2.avg}분` : ''}</span></summary>
      <div class="k-stay-in"><label class="stsel"><span>숙소 위치 바꾸기</span><select data-stay="${r}">${STAYS.filter(s => s.r === r).map(s => `<option value="${s.id}" ${s.id === st.id ? 'selected' : ''}>${esc(sn(s.id))}</option>`).join('')}</select></label>
      <p>${T.dayRange(dIdx[0], dIdx[dIdx.length - 1])}${nights ? ` · ${nights}박` : ''} · ${T.nearN(sc2.near, sc2.total)} ${T.nearSub} · ${esc(an(apCode))}까지 ${F.dur(apMin)}</p>
      ${S.stayOv[r] ? `<p>${T.stayManual} <button class="btn sm ghost" data-act="stayAuto" data-v="${r}">${T.stayAuto}</button></p>` : ''}</div></details>`; }).join('');
  const rows = sc.rows, last = rows.length - 1;
  let tl = '';
  rows.forEach((o, k) => {
    if (o.leg && o.leg.min) tl += `<div class="seg"><span></span><span class="rl"></span><div class="sg">${ICONS[MODE_ICON[o.leg.mode]] || ''}<span><b>${modeLabel(o.leg)} ${F.dur(o.leg.min)}</b>${o.leg.km ? ` · ${o.leg.km < 1 ? Math.round(o.leg.km * 1000) + 'm' : o.leg.km.toFixed(1) + 'km'}` : ''}</span></div></div>`;
    const e = o.e, sp = !['place', 'meal'].includes(e.k), p = e.id ? PBY[e.id] : null;
    const tags = (o.flags || []).map(flagPill).join('') + (e.k === 'meal' ? `<span class="pill" style="background:#FFF1E3;color:#B5560F">${e.slot === 'dinner' ? T.dinner : T.lunch}</span>` : '');
    const sub = p ? `${esc(T.cats[p.c])} · ${F.dur(p.h * 60)}` : (e.k === 'transfer' ? `${T.mRail === modeLabel(o.leg || {}) ? '' : ''}${esc(rn(e.from))} → ${esc(rn(e.to))}` : '');
    const icon = sp ? ({ arrive: tripAir().home ? 'rail' : 'plane', depart: tripAir().home ? 'rail' : 'plane', transfer: (o.leg && o.leg.mode === 'flight') ? 'plane' : 'rail', checkout: 'house', stay: 'house', start: 'house', end: 'house' }[e.k]) : null;
    tl += `<div class="ent ${sp ? 'sp' : ''} ${e.k === 'meal' ? 'meal' : ''} ${k === 0 ? 'first' : ''} ${k === last ? 'last' : ''}">
      <div class="tm">${slotLbl(o, rows[k - 1])}</div><div class="rl"><i>${sp ? ICONS[icon] : (o.num || '')}</i></div>
      <div class="bx">${p ? `<button class="tx" style="text-align:left" data-act="openPlace" data-v="${p.id}">` : '<div class="tx">'}<div class="nm">${esc(entryName(o))}</div>${sub ? `<div class="sub">${sub}</div>` : ''}${tags ? `<div class="tags">${tags}</div>` : ''}${p ? '</button>' : '</div>'}
      ${!sp ? `<button class="more" data-act="stopMenu" data-v="${e.si}" aria-label="${T.more}">${ICONS.more}</button>` : ''}</div></div>`;
  });
  const uns = P.unsched.filter(u => PBY[u.id]);
  return `<div class="eyebrow">${F.date(ds[0].date)} – ${F.date(ds[n - 1].date)} · ${F.nights(n)}</div>
    <div class="row" style="justify-content:space-between;align-items:flex-start"><h1 class="h1">${T.planTitle}</h1><button class="btn sm ghost" data-act="genPlan">${ICONS.magic}${T.replanShort}</button></div>
    <div class="route">${route}</div>
    ${stale ? `<div class="banner">${ICONS.info.replace('<svg ', '<svg width="20" height="20" style="flex-shrink:0" ')}<span class="grow">${T.stale}</span><button class="btn sm" data-act="genPlan">${T.replanShort}</button></div>` : ''}
    ${P.warn && P.warn.k === 'farDep' ? `<div class="banner">${ICONS.warn.replace('<svg ', '<svg width="20" height="20" style="flex-shrink:0" ')}<span class="grow">${T.farDep(rn(P.warn.r), F.dur(P.warn.min))}</span><button class="btn sm ghost" data-act="trip">${T.editTrip}</button></div>` : ''}
    ${(() => { const ta = tripAir(), st0 = STAY_BY[P.stays[R[0]]], stN = STAY_BY[P.stays[R[R.length - 1]]];
      const lk = m => m === 'rail' ? ['https://www.letskorail.com/', '코레일'] : m === 'flight' ? null : (ta.arr === 'ICN' || ta.dep === 'ICN') && m !== 'walk' ? ['https://www.arex.or.kr/', '공항철도'] : null;
      const row = (k, from, to, L) => { const l = lk(L.mode); const body = `<span class="k">${k}</span><span class="tx"><b>${esc(from)} → ${esc(to)}</b><small>${esc(modeLabel(L))} · 약 ${F.dur(L.min)}</small></span>${l ? `<span class="go">${l[1]} ›</span>` : ''}`;
        return l ? `<a class="k-tr" href="${l[0]}" target="_blank" rel="noopener">${body}</a>` : `<div class="k-tr">${body}</div>`; };
      const MAIN = { seoul: '서울역', busan: '부산역', gyeongju: '경주역', gangneung: '강릉역', jeonju: '전주역', yeosu: '여수엑스포역', gunsan: '군산역', mokpo: '목포역', jeju: '제주공항' };
      const RAIL = { busan: ['서울역', 'KTX 경부선'], gyeongju: ['서울역', 'KTX 경부선'], gangneung: ['서울역·청량리역', 'KTX 강릉선'], jeonju: ['용산역', 'KTX 전라선'], yeosu: ['용산역', 'KTX 전라선'], gunsan: ['용산역', '장항선 열차'], mokpo: ['용산역', 'KTX 호남선'] };
      const stTx = s => (s && s.st && s.st[0]) || '';
      const last = (r, s) => { if (!s) return []; const t = stTx(s), nm = sn(s.id);
        if (r === 'seoul' || r === 'busan') return [`지하철로 ${t.replace(' · ', '(') + (t.includes(' · ') ? ')' : '')}`];
        if (r === 'jeju') return [`렌터카 또는 택시·버스로 ${nm}`];
        if (t.startsWith('KTX') || nm === MAIN[r]) return [`${MAIN[r]} 앞 숙소`];
        return [`${MAIN[r]}에서 택시·시내버스로 ${nm}`]; };
      const fromSeoul = (r, rev) => { if (r === 'jeju') return rev ? ['제주공항 → 김포공항 항공편', '김포공항에서 지하철 5·9호선·공항철도로 시내'] : ['지하철 5·9호선·공항철도로 김포공항', '김포공항 → 제주공항 항공편'];
        const x = RAIL[r]; if (!x) return null; return rev ? [`${MAIN[r]}에서 ${x[1]}`, `${x[0].split('·')[0]} 도착`] : [`${x[0]}에서 ${x[1]}`, `${MAIN[r]} 도착`]; };
      const between = (a, b, sb) => { if (a === 'seoul') return (b === 'jeju' ? [] : [`숙소에서 지하철로 ${RAIL[b] ? RAIL[b][0].replace('·', ' 또는 ') : '역'}`]).concat(fromSeoul(b) || [], last(b, sb)); if (b === 'seoul') return [`숙소에서 ${MAIN[a]}`].concat(fromSeoul(a, true), last('seoul', sb));
        if (a === 'jeju' || b === 'jeju') return [`${MAIN[a]} → ${MAIN[b]} 항공편 (직항 여부는 예매에서 확인)`].concat(last(b, sb));
        return [`${MAIN[a]}에서 KTX·고속버스로 ${MAIN[b]} (직통이 없으면 서울·대전·동대구 환승)`].concat(last(b, sb)); };
      const toSeoulHub = (code, r) => { const need = RAIL[r] && RAIL[r][0];
        if (code === 'ICN') { if (r === 'seoul') return ['공항철도 타고 서울역' + (/홍대/.test(sn(st0.id)) ? '·홍대입구역' : '')];
          return ['공항철도 타고 서울역'].concat(need === '용산역' ? ['서울역에서 지하철 1호선으로 용산역'] : need === '서울역·청량리역' ? [] : []); }
        if (code === 'GMP') return ['지하철 5·9호선 또는 공항철도로 시내' + (r === 'seoul' ? '' : (need === '용산역' ? '(용산역)' : '(서울역)'))];
        return null; };
      const arrSteps = (code, r, s) => { const ap = AIRPORTS[code] || {};
        if (ap.cc !== 'kr') return null;
        if (code === 'CJU') return r === 'jeju' ? last('jeju', s) : null;
        if (code === 'PUS') return r === 'busan' ? ['김해경전철 타고 사상역', '사상역에서 지하철 2호선 환승'].concat(last('busan', s).map(x => x.replace('지하철로', '숙소 역:'))) : null;
        if (ap.home) { const hr = ap.r; if (hr === r) return last(r, s); if (hr === 'seoul') return fromSeoul(r).concat(last(r, s));
          if (hr) return between(hr, r, s); return [`${an(code)}에서 KTX로 ${MAIN[r] || rn(r)} (노선은 코레일에서 확인)`].concat(last(r, s)); }
        const h = toSeoulHub(code, r); if (!h) return null; if (r === 'seoul') return h.concat(last('seoul', s)); return h.concat(fromSeoul(r) || [], last(r, s)); };
      const depSteps = (code, r, s) => { const a = arrSteps(code, r, s); if (!a) return null;
        const ap = AIRPORTS[code] || {}; if (code === 'CJU' && r === 'jeju') return [`${sn(s.id)}에서 렌터카 또는 택시·버스로 제주공항`];
        if (r === 'seoul' && code === 'ICN') return ['숙소 근처 역에서 지하철로 서울역', '서울역에서 공항철도로 인천공항'];
        if (r === 'seoul' && code === 'GMP') return ['지하철 5·9호선 또는 공항철도로 김포공항'];
        if (ap.home && ap.r === r) return [`숙소에서 ${an(code)}`];
        const out = [`숙소에서 ${MAIN[r] || '역'}까지 이동`];
        if (ap.home) return out.concat(ap.r === 'seoul' ? fromSeoul(r, true).concat(code === 'SEL' && RAIL[r] && RAIL[r][0] === '용산역' ? ['용산역에서 지하철 1호선으로 서울역'] : []) : [`KTX로 ${an(code)}`]);
        if (code === 'PUS') return r === 'busan' ? ['지하철 2호선으로 사상역', '김해경전철로 김해공항'] : null;
        const back = r === 'seoul' ? [] : (fromSeoul(r, true) || []);
        const fin = code === 'ICN' ? ['서울역에서 공항철도로 인천공항'] : ['지하철 5·9호선 또는 공항철도로 김포공항'];
        if (r === 'jeju') return out.slice(0, 0).concat([`${sn(s.id)}에서 제주공항`, `제주공항 → 김포공항 항공편`], code === 'ICN' ? ['김포공항에서 공항철도로 인천공항'] : []);
        return out.concat(back, RAIL[r] && RAIL[r][0] === '용산역' ? ['용산역에서 지하철 1호선으로 서울역'] : [], fin); };
      const rows = [];
      const row2 = (k, from, to, L, steps) => { if (!steps || !steps.length) return row(k, from, to, L);
        const l = lk(L.mode); return `<div class="k-tr k-tr2"><span class="k">${k}</span><span class="tx"><b>${esc(from)} → ${esc(to)}</b><ol class="k-st">${steps.map(x => `<li>${esc(x)}</li>`).join('')}</ol><small>약 ${F.dur(L.min)}${l ? ` · <a href="${l[0]}" target="_blank" rel="noopener">${l[1]} 예매 ›</a>` : ''}</small></span></div>`; };
      try { rows.push(row2('도착', an(ta.arr), `${rn(R[0])} 숙소 ${sn(st0.id)}`, airportLeg(ta.arr, st0, R[0]), arrSteps(ta.arr, R[0], st0))); } catch (e) {}
      R.forEach((r, k) => { if (k) { const t = interRegion(R[k - 1], r); if (t) rows.push(row2('이동', rn(R[k - 1]), rn(r), Object.assign({}, t, { min: t.ride || t.min }), isOv(r) || isOv(R[k - 1]) ? null : between(R[k - 1], r, STAY_BY[P.stays[r]]))); } });
      try { rows.push(row2(ta.home ? '귀가' : '출국', `${rn(R[R.length - 1])} 숙소 ${sn(stN.id)}`, an(ta.dep), airportLeg(ta.dep, stN, R[R.length - 1]), depSteps(ta.dep, R[R.length - 1], stN))); } catch (e) {}
      return rows.length ? `<div class="sec"><h3>교통편</h3><small>시간은 약, 요금은 예매 사이트 확인</small></div><div class="k-trs">${rows.join('')}</div>` : ''; })()}
    <div class="sec"><h3>${T.byDay}</h3></div>
    <div class="days">${ds.map((d, k) => `<button class="dchip ${k === i ? 'on' : ''}" style="--c:${LINE[k % LINE.length]}" data-act="day" data-v="${k}"><span class="n">${k + 1}</span><span class="d"><b>${F.date(d.date)}</b><small>${esc(rn(d.r))}</small></span></button>`).join('')}</div>
    <div class="dhead"><div><h2>${T.day(i + 1)} · ${esc(rn(day.r))}</h2><small>${F.date(day.date, true)} · ${T.daySumOv(sc.places, F.dur(sc.moveMin))}</small></div></div>
    <div class="routebox inline" id="rbox"></div>
    <div class="tl">${tl}</div>
    <div class="dayacts"><button class="btn sm ghost" data-act="optDay" data-v="${i}">${ICONS.magic}${T.optimize}</button><button class="btn sm ghost" data-act="addStop" data-v="${i}">${ICONS.plus}${T.addStop}</button></div>
    ${uns.length ? `<div class="sec"><h3>${T.unsched}</h3><small>${T.unschedSub}</small></div><div class="list">${uns.map(u => { const p = PBY[u.id]; const can = ds.some(d => d.r === p.r);
      return `<div class="prow">${cicon(p.c)}<span class="tx"><span class="nm">${esc(pn(u.id))}</span><span class="ds">${esc(rn(p.r))} · ${T.why[u.why] || ''}</span></span>${can ? `<button class="btn sm soft" data-act="placeUns" data-v="${u.id}">${T.putIn}</button>` : ''}</div>`; }).join('')}</div>` : ''}
    <div class="sec"><h3>숙소</h3><small>누르면 자세히</small></div><div class="k-stays">${stays}</div>
    <p class="k-tot">전체 ${T.spots(totals.places)} · 이동 ${F.dur(totals.move)}</p>
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
  const keys = tripAir().ov ? ['환율', '여권', '입국', '면세'] : ['KTX', '호텔', '주유', '통행료'];
  const sc = x => { const k = keys.findIndex(w => x.name.includes(w)); return k < 0 ? 99 : k; };
  const tools = it.tools.slice().sort((a, b) => sc(a) - sc(b)), top = tools.slice(0, 3), restT = tools.slice(3);
  const tile = x => ext(x.url, `<b lang="ko">${esc(x.name)}</b>`, 'k-ptile');
  const line = (u, t) => `<a class="k-pl" href="${esc(u)}" target="_blank" rel="noopener" lang="ko">${esc(t)}</a>`;
  const mine = R.map(r => { const ar = aroundRegion(r); if (!ar) return ''; return `<div class="k-prow"><b>${esc(rn(r))}</b>${ar.trip ? line(ar.trip.url, '여행 가이드') : ''}${ar.food ? line(ar.food.url, `맛집 ${ar.food.count}곳`) : ''}</div>`; }).join('');
  return `<h1 class="h1">${T.prepTitle}</h1>
    ${top.length ? `<div class="sec"><h3>꼭 확인할 것</h3></div><div class="k-ptiles">${top.map(tile).join('')}</div>` : ''}
    ${mine ? `<div class="sec"><h3>내 여행지</h3></div><div class="k-prows">${mine}</div>` : ''}
    ${restT.length ? `<details class="k-pmore"><summary>계산기 ${restT.length}개 더 보기</summary><div>${restT.map(x => line(x.url, x.name)).join('')}</div></details>` : ''}
    ${it.guides.length ? `<details class="k-pmore"><summary>가이드 ${it.guides.length}개 더 보기</summary><div>${it.guides.map(x => line(x.url, x.name)).join('')}</div></details>` : ''}
    ${P ? `<div style="margin-top:18px"><button class="btn ghost block" data-act="copyTxt">${ICONS.copy}${T.copyTxt}</button></div>` : ''}`;
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
