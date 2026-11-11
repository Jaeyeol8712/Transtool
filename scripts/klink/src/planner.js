'use strict';
/* =========================================================
   Planner: days per region, stays, clustering, ordering, meals, schedule
   ========================================================= */
const PACE = [{ start: 10, end: 20, cap: 330 }, { start: 9.5, end: 21, cap: 420 }, { start: 9, end: 22, cap: 510 }];
const isFood = p => p.c === 'food';
const wd = date => toDate(date).getDay();
const monthOf = date => toDate(date).getMonth() + 1;
function inSeason(p, date) { if (!p.season) return true; const m = monthOf(date); return m >= p.season[0] && m <= p.season[1]; }
function openOn(p, date) { return !(p.closed || []).includes(wd(date)) && inSeason(p, date); }
function bucketOf(p) { if (p.best === 'night') return 3; if (p.best === 'eve') return 2; if (p.best === 'am' || p.o[1] <= 17.5) return 0; return 1; }
const loadOf = p => p.h * 60 + (REGIONS[p.r].sub ? 25 : 45);
const TOP = new Set(['gbg','bukchon','cdg','namsan','gwangjang','lotte','hongdae','seongsu','deoksugung','museum','bs_haeundae','bs_gamcheon','bs_gwangan','bs_jagalchi','bs_taejongdae','jj_seongsan','jj_udo','jj_halla','gj_bulguksa','gj_seokguram','gj_daereung','gj_wolji','gn_anmok','gn_gyeongpo','jn_hanok','ys_odong','ys_night','ys_cable']);
const ptOf = x => x && x.lat != null ? { lat: x.lat, lng: x.lng } : null;

/* ---------- stays ---------- */
function stayScore(s, r, ids) {
  const items = ids.map(id => PBY[id]).filter(p => p.r === r);
  const legs = items.map(p => ({ p, m: legBetween(s, p, r).min }));
  const core = legs.filter(x => !isFood(x.p));
  const base = core.length ? core : legs;
  const avg = base.length ? Math.round(base.reduce((a, x) => a + x.m, 0) / base.length) : 0;
  const near = base.filter(x => x.m <= 20).length;
  let score = legs.reduce((a, x) => a + x.m * (isFood(x.p) ? 0.6 : 1), 0);
  return { score, avg, near, total: base.length };
}
function bestStay(r, ids, isFirst, isLast) {
  const cands = STAYS.filter(s => s.r === r);
  let best = cands[0], bs = Infinity;
  for (const s of cands) {
    let sc = stayScore(s, r, ids).score;
    if (isFirst && AIRPORTS[S.trip.arr].r === r) sc += 0.35 * airportLeg(S.trip.arr, s, r).min;
    if (isLast && AIRPORTS[S.trip.dep].r === r) sc += 0.35 * airportLeg(S.trip.dep, s, r).min;
    if (sc < bs) { bs = sc; best = s; }
  }
  return best.id;
}

/* ---------- path ordering: nearest neighbour + 2-opt (open path, fixed start) ---------- */
function orderPath(ids, start) {
  if (ids.length <= 1) return ids.slice();
  const pts = ids.map(id => PBY[id]);
  const rest = pts.slice(), seq = []; let cur = start;
  while (rest.length) { let bi = 0, bd = 1e9; rest.forEach((p, i) => { const d = hav(cur, p); if (d < bd) { bd = d; bi = i; } }); cur = rest[bi]; seq.push(rest.splice(bi, 1)[0]); }
  const D = (a, b) => hav(a, b);
  let improved = true, guard = 0;
  while (improved && guard++ < 50) {
    improved = false;
    for (let i = 0; i < seq.length - 1; i++) for (let k = i + 1; k < seq.length; k++) {
      const a = i === 0 ? start : seq[i - 1], b = seq[i], c = seq[k], d = seq[k + 1];
      const before = D(a, b) + (d ? D(c, d) : 0), after = D(a, c) + (d ? D(b, d) : 0);
      if (after + 1e-6 < before) { const mid = seq.slice(i, k + 1).reverse(); seq.splice(i, k - i + 1, ...mid); improved = true; }
    }
  }
  return seq.map(p => p.id);
}
function earliest(p) { let e = p.o[0]; if (p.best === 'night') e = Math.max(e, 18); else if (p.best === 'eve') e = Math.max(e, 16); return e; }
function seqCost(seq, start, t0, r) {
  let t = t0, pos = start, cost = 0, lunch = false, dinner = false;
  for (const id of seq) {
    const p = PBY[id], m = legBetween(pos, p, r).min;
    let a = t + m / 60;
    if (!lunch && a >= 12) { a += 1; lunch = true; }
    if (!dinner && (a >= 18.5 || (bucketOf(p) === 3 && a >= 16))) { a += 1.25; dinner = true; }
    const bo = Math.max(a, p.o[0]), b = Math.max(bo, earliest(p));
    cost += m + (pos === start ? 0 : (bo - a) * 60 * 0.8) + (b - bo) * 60 * 0.15 + (bucketOf(p) === 0 && b > 13 ? 40 : 0);
    const end = b + p.h; if (b >= p.o[1]) cost += 300; else if (end > p.o[1] + 0.1) cost += (end - p.o[1]) * 180;
    t = end; pos = p;
  }
  return cost + Math.max(0, t - 22) * 120;
}
function orderDayPlaces(ids, stay, t0, r) {
  if (ids.length <= 1) return ids.slice();
  r = r || PBY[ids[0]].r; t0 = t0 == null ? PACE[S.trip.pace].start : t0;
  const b = [[], [], [], []]; ids.forEach(id => b[bucketOf(PBY[id])].push(id));
  let seq = []; let cur = stay;
  for (const grp of b) { const s2 = orderPath(grp, cur); seq.push(...s2); if (s2.length) cur = PBY[s2[s2.length - 1]]; }
  let best = seqCost(seq, stay, t0, r), improved = true, guard = 0;
  while (improved && guard++ < 40) {
    improved = false;
    for (let i = 0; i < seq.length - 1; i++) for (let k = i + 1; k < seq.length; k++) {
      const c1 = seq.slice(); const mid = c1.slice(i, k + 1).reverse(); c1.splice(i, k - i + 1, ...mid);
      const v1 = seqCost(c1, stay, t0, r); if (v1 + 0.5 < best) { seq = c1; best = v1; improved = true; }
    }
    for (let i = 0; i < seq.length; i++) for (let k = 0; k < seq.length; k++) { if (i === k) continue;
      const c2 = seq.slice(); const [x] = c2.splice(i, 1); c2.splice(k, 0, x);
      const v2 = seqCost(c2, stay, t0, r); if (v2 + 0.5 < best) { seq = c2; best = v2; improved = true; } }
  }
  return seq;
}

/* ---------- day windows ---------- */
function dayWindow(plan, i) {
  const day = plan.days[i], pace = PACE[S.trip.pace], stay = STAY_BY[plan.stays[day.r]];
  let start = pace.start, end = pace.end;
  if (day.first) start = Math.max(start, S.trip.arrT + 1 + airportLeg(S.trip.arr, stay, day.r).min / 60 + 0.35);
  else if (day.transfer) start = Math.max(start, 9 + interRegion(plan.days[i - 1].r, day.r).min / 60 + 0.6);
  if (day.last) end = Math.min(end, S.trip.depT - 2.5 - airportLeg(S.trip.dep, stay, day.r).min / 60 - 0.35);
  end = Math.max(end, start + 0.5);
  const meals = (start <= 13 && end >= 12.5 ? 60 : 0) + (start <= 18.5 && end >= 19 ? 75 : 0);
  return { start, end, cap: Math.max(30, (end - start) * 60 - meals) };
}

/* ---------- balanced k-means ---------- */
function clusterPlaces(P, k, start) {
  if (k <= 1) return [P.slice()];
  const pts = P.map(id => PBY[id]);
  let cen = []; let far = pts.reduce((b, p) => hav(start, p) > hav(start, b) ? p : b, pts[0]); cen.push({ lat: far.lat, lng: far.lng });
  while (cen.length < k) { let bp = pts[0], bd = -1; for (const p of pts) { const d = Math.min(...cen.map(c => hav(c, p))); if (d > bd) { bd = d; bp = p; } } cen.push({ lat: bp.lat + 1e-5 * cen.length, lng: bp.lng }); }
  const total = pts.reduce((a, p) => a + loadOf(p), 0), capC = total / k * 1.2 + 30;
  let asg = new Array(pts.length).fill(0);
  for (let it = 0; it < 12; it++) {
    const pairs = []; pts.forEach((p, i) => cen.forEach((c, j) => pairs.push([hav(p, c), i, j]))); pairs.sort((a, b) => a[0] - b[0]);
    const done = new Array(pts.length).fill(false), load = new Array(k).fill(0);
    for (const [, i, j] of pairs) { if (done[i]) continue; if (load[j] + loadOf(pts[i]) > capC && load.some((l, jj) => jj !== j && l + loadOf(pts[i]) <= capC)) continue; done[i] = true; asg[i] = j; load[j] += loadOf(pts[i]); }
    cen = cen.map((c, j) => { const m = pts.filter((_, i) => asg[i] === j); return m.length ? { lat: m.reduce((a, p) => a + p.lat, 0) / m.length, lng: m.reduce((a, p) => a + p.lng, 0) / m.length } : c; });
  }
  const out = Array.from({ length: k }, () => []); pts.forEach((p, i) => out[asg[i]].push(p.id)); return out;
}
function permutations(n) { if (n > 6) return null; const res = []; const a = [...Array(n).keys()];
  (function rec(i) { if (i === n) { res.push(a.slice()); return; } for (let j = i; j < n; j++) { [a[i], a[j]] = [a[j], a[i]]; rec(i + 1); [a[i], a[j]] = [a[j], a[i]]; } })(0); return res; }

/* ---------- meal insertion ---------- */
function simulate(plan, i, stops) {
  const day = plan.days[i], w = dayWindow(plan, i), stay = STAY_BY[plan.stays[day.r]];
  let t = w.start, pos = stay; const arr = [];
  for (const st of stops) {
    const p = st.id ? PBY[st.id] : null;
    const leg = p ? legBetween(pos, p, day.r) : { min: 0 };
    const a = t + leg.min / 60; const dur = p ? p.h : 1;
    const b = p ? Math.max(a, earliest(p)) : a; arr.push({ a, b, end: b + dur }); t = b + dur; if (p) pos = p;
  }
  return { arr, t, w };
}
function mealSlots(plan, i, stops) {
  const sim = simulate(plan, i, stops), w = sim.w, slots = [];
  const day = plan.days[i];
  // lunch
  if (w.start <= 13.5 && w.end >= 12.5) {
    let at = stops.length; for (let k = 0; k < stops.length; k++) if (sim.arr[k].a >= 11.75 || sim.arr[k].end > 13.5) { at = k; break; }
    slots.push({ slot: 'lunch', at });
  }
  // dinner
  if (!day.last && w.end >= 19 && w.start <= 18.5) {
    let at = stops.length;
    for (let k = 0; k < stops.length; k++) { const p = stops[k].id && PBY[stops[k].id]; if (p && bucketOf(p) === 3) { at = k; break; } if (sim.arr[k].a >= 17.75) { at = k; break; } }
    slots.push({ slot: 'dinner', at });
  }
  return slots;
}
function slotPoints(plan, i, stops, at) {
  const day = plan.days[i], stay = STAY_BY[plan.stays[day.r]];
  const prev = at > 0 ? PBY[stops[at - 1].id] || stay : stay, next = at < stops.length ? PBY[stops[at].id] || stay : stay;
  return { prev, next };
}
function mealFits(p, slot, date) {
  if (!openOn(p, date)) return false;
  if (p.meal === 'lunch' && slot !== 'lunch') return false;
  if (p.meal === 'dinner' && slot !== 'dinner') return false;
  const t = slot === 'lunch' ? 12.5 : 18.75; return p.o[0] <= t && p.o[1] >= t + 0.75;
}
function detour(prev, next, p, r) { return legBetween(prev, p, r).min + legBetween(p, next, r).min - legBetween(prev, next, r).min; }
function insertMeals(plan, idxs, foods, used) {
  const all = [];
  for (const i of idxs) {
    const stops = plan.days[i].stops.filter(s => s.k === 'place');
    plan.days[i].stops = stops;
    for (const sl of mealSlots(plan, i, stops)) all.push({ i, ...sl });
  }
  const r = plan.days[idxs[0]].r, pairs = [];
  all.forEach((sl, si) => { const { prev, next } = slotPoints(plan, sl.i, plan.days[sl.i].stops, sl.at);
    foods.forEach(id => { const p = PBY[id]; if (mealFits(p, sl.slot, plan.days[sl.i].date)) pairs.push([detour(prev, next, p, r), si, id]); }); });
  pairs.sort((a, b) => a[0] - b[0]);
  const taken = new Set(), filled = new Map();
  for (const [, si, id] of pairs) { if (filled.has(si) || taken.has(id)) continue; filled.set(si, id); taken.add(id); }
  const leftovers = foods.filter(id => !taken.has(id));
  // suggestions for empty slots
  all.forEach((sl, si) => {
    if (filled.has(si)) return;
    const { prev, next } = slotPoints(plan, sl.i, plan.days[sl.i].stops, sl.at);
    let best = null, bd = REGIONS[r].sub ? 28 : 55;
    for (const p of PLACES) { if (p.r !== r || !isFood(p) || used.has(p.id) || taken.has(p.id) || (p.prem && S.trip.budget < 2)) continue;
      if (!mealFits(p, sl.slot, plan.days[sl.i].date)) continue; const d = detour(prev, next, p, r) + (p.rsv ? 8 : 0); if (d < bd) { bd = d; best = p.id; } }
    if (best) { used.add(best); filled.set(si, '~' + best); }
  });
  // insert (descending index per day)
  const byDay = {};
  all.forEach((sl, si) => (byDay[sl.i] = byDay[sl.i] || []).push({ ...sl, id: filled.get(si) }));
  for (const [i, list] of Object.entries(byDay)) {
    list.sort((a, b) => b.at - a.at || (a.slot === 'dinner' ? -1 : 1));
    for (const sl of list) {
      const sug = typeof sl.id === 'string' && sl.id.startsWith('~'); const id = sl.id ? sl.id.replace('~', '') : null;
      plan.days[i].stops.splice(sl.at, 0, { k: 'meal', slot: sl.slot, id, sug });
    }
  }
  return leftovers;
}

/* ---------- region order ---------- */
function autoOrder(rs) {
  if (rs.length <= 1) return rs.slice();
  const near = (list, pt) => list.slice().sort((a, b) => hav(REGIONS[a], pt) - hav(REGIONS[b], pt))[0];
  const arrR = AIRPORTS[S.trip.arr].r, depR = AIRPORTS[S.trip.dep].r;
  const first = rs.includes(arrR) ? arrR : near(rs, AIRPORTS[S.trip.arr]);
  let rest = rs.filter(r => r !== first);
  const last = rest.includes(depR) ? depR : near(rest, AIRPORTS[S.trip.dep]);
  rest = rest.filter(r => r !== last);
  const seq = [first]; let cur = first;
  while (rest.length) { const nx = rest.slice().sort((a, b) => hav(REGIONS[cur], REGIONS[a]) - hav(REGIONS[cur], REGIONS[b]))[0]; seq.push(nx); rest = rest.filter(r => r !== nx); cur = nx; }
  seq.push(last); return seq;
}
function tripOrder() { const rs = savedRegions(); return S.orderManual ? rs : autoOrder(rs); }

/* ---------- main ---------- */
function generatePlan() {
  const dates = tripDates(), n = dates.length;
  const regsAll = tripOrder();
  if (!regsAll.length) return null;
  const unsched = [];
  let R = regsAll.slice();
  const need = r => { const k = R.indexOf(r), pc = PACE[S.trip.pace], hub = REGIONS[r];
    let loss = k <= 0 ? Math.max(0, S.trip.arrT + 1.35 + airportLeg(S.trip.arr, hub, r).min / 60 - pc.start) * 60 : interRegion(R[k - 1], r).min + 60;
    if (k === R.length - 1) loss += Math.max(0, pc.end - (S.trip.depT - 2.85 - airportLeg(S.trip.dep, hub, r).min / 60)) * 60;
    return S.saved.map(id => PBY[id]).filter(p => p.r === r && !isFood(p)).reduce((a, p) => a + loadOf(p), 0) + loss; };
  if (R.length > n) { const keep = R.slice().sort((a, b) => need(b) - need(a)).slice(0, n); R = R.filter(r => keep.includes(r));
    S.saved.forEach(id => { if (!R.includes(PBY[id].r)) unsched.push({ id, why: 'nodays' }); }); }
  const cap = PACE[S.trip.pace].cap, alloc = R.map(() => 1); let left = n - R.length;
  while (left-- > 0) { let bi = 0, bv = -1e9; R.forEach((r, i) => { const v = need(r) / cap - alloc[i]; const v2 = v > 0 ? v : -alloc[i] / (need(r) + 1) * 0.001; if (v2 > bv) { bv = v2; bi = i; } }); alloc[bi]++; }
  const dayR = []; R.forEach((r, i) => { for (let k = 0; k < alloc[i]; k++) dayR.push(r); });
  const plan = { sig: planSig(), created: Date.now(), stays: {}, unsched, days: dates.map((date, i) => ({ date, r: dayR[i], first: i === 0, last: i === n - 1, transfer: i > 0 && dayR[i - 1] !== dayR[i], stops: [] })) };
  R.forEach((r, k) => { plan.stays[r] = S.stayOv[r] && STAY_BY[S.stayOv[r]] && STAY_BY[S.stayOv[r]].r === r ? S.stayOv[r] : bestStay(r, S.saved, k === 0, k === R.length - 1); });
  const used = new Set(S.saved);
  for (const r of R) {
    const idx = plan.days.map((d, i) => d.r === r ? i : -1).filter(i => i >= 0), stay = STAY_BY[plan.stays[r]];
    const mine = S.saved.filter(id => PBY[id].r === r);
    const P = [], F = [];
    for (const id of mine) { const p = PBY[id];
      if (!idx.some(i => inSeason(p, plan.days[i].date))) { unsched.push({ id, why: 'season' }); continue; }
      if (!idx.some(i => openOn(p, plan.days[i].date))) { unsched.push({ id, why: 'closed' }); continue; }
      (isFood(p) ? F : P).push(id); }
    const W = idx.map(i => dayWindow(plan, i));
    let groups;
    if (idx.length === 1) groups = [P.slice()];
    else groups = clusterPlaces(P, idx.length, stay);
    // map groups to days
    const conflicts = (g, i) => g.filter(id => !openOn(PBY[id], plan.days[i].date) || (bucketOf(PBY[id]) === 3 && W[idx.indexOf(i)].end < 19.5)).length;
    const gl = g => g.reduce((a, id) => a + loadOf(PBY[id]), 0);
    let mapping = idx.map((_, j) => j);
    const perms = permutations(idx.length);
    if (perms) { let bs = Infinity; for (const pm of perms) { let s = 0; pm.forEach((g, j) => { s += conflicts(groups[g], idx[j]) * 1000 + Math.max(0, gl(groups[g]) - W[j].cap); }); if (s < bs) { bs = s; mapping = pm; } } }
    const dayIds = idx.map((_, j) => groups[mapping[j]].slice());
    // fix conflicts and overflow
    const loadD = j => dayIds[j].reduce((a, id) => a + loadOf(PBY[id]), 0);
    const homeless = [];
    dayIds.forEach((ids, j) => { for (const id of ids.slice()) if (conflicts([id], idx[j])) { ids.splice(ids.indexOf(id), 1); homeless.push(id); } });
    dayIds.forEach((ids, j) => { while (loadD(j) > W[j].cap + 20 && ids.length) { const c = { lat: ids.reduce((a, id) => a + PBY[id].lat, 0) / ids.length, lng: ids.reduce((a, id) => a + PBY[id].lng, 0) / ids.length };
      const far = ids.slice().sort((a, b) => (TOP.has(a) - TOP.has(b)) || (hav(c, PBY[b]) - hav(c, PBY[a])))[0]; ids.splice(ids.indexOf(far), 1); homeless.push(far); } });
    for (const id of homeless) { const p = PBY[id]; let bj = -1, bd = 1e9;
      dayIds.forEach((ids, j) => { if (conflicts([id], idx[j])) return; if (loadD(j) + loadOf(p) > W[j].cap + 20) return;
        const d = ids.length ? Math.min(...ids.map(x => hav(PBY[x], p))) : hav(stay, p); if (d < bd) { bd = d; bj = j; } });
      if (bj < 0) { // make room: move something flexible out of a day this place can use
        outer: for (let j = 0; j < dayIds.length; j++) { if (conflicts([id], idx[j])) continue;
          for (const other of dayIds[j].slice().sort((a, b) => (TOP.has(a) - TOP.has(b)) || (loadOf(PBY[b]) - loadOf(PBY[a])))) {
            if (loadD(j) - loadOf(PBY[other]) + loadOf(p) > W[j].cap + 20) continue;
            for (let k = 0; k < dayIds.length; k++) { if (k === j || conflicts([other], idx[k]) || loadD(k) + loadOf(PBY[other]) > W[k].cap + 20) continue;
              dayIds[j].splice(dayIds[j].indexOf(other), 1); dayIds[k].push(other); bj = j; break outer; } } } }
      if (bj >= 0) dayIds[bj].push(id); else unsched.push({ id, why: conflicts([id], idx[0]) && idx.every(i => conflicts([id], i)) ? 'closed' : 'full' }); }
    idx.forEach((i, j) => { plan.days[i].stops = orderDayPlaces(dayIds[j], stay, W[j].start, r).map(id => ({ k: 'place', id })); });
    insertMeals(plan, idx, F, new Set(used));
    fitRegion(plan, idx, unsched);
    idx.forEach((i, j) => { const ids = plan.days[i].stops.filter(x => x.k === 'place').map(x => x.id); plan.days[i].stops = orderDayPlaces(ids, stay, dayWindow(plan, i).start, r).map(id => ({ k: 'place', id })); });
    const left = insertMeals(plan, idx, F, used);
    fitRegion(plan, idx, unsched);
    left.forEach(id => unsched.push({ id, why: 'meals' }));
    // rescue: anything dropped for lack of room gets one more try on every day of this region
    for (const u of unsched.slice()) { const p = PBY[u.id]; if (p.r !== r || u.why !== 'full') continue;
      if (plan.days.some(d => d.stops.some(x => x.id === u.id))) { unsched.splice(unsched.indexOf(u), 1); continue; }
      for (const j of idx.slice().sort((a, b) => plan.days[a].stops.length - plan.days[b].stops.length)) {
        if (!openOn(p, plan.days[j].date)) continue;
        const at = bestInsertAt(plan, j, u.id); plan.days[j].stops.splice(at, 0, { k: isFood(p) ? 'meal' : 'place', id: u.id, slot: 'lunch' });
        const c = dayOver(plan, j); if (!c.over && !c.late.length) { unsched.splice(unsched.indexOf(u), 1); break; }
        plan.days[j].stops.splice(at, 1);
      } }
  }
  const inPlan = new Set(plan.days.flatMap(d => d.stops.map(x => x.id)).filter(Boolean)), seen = new Set();
  plan.unsched = unsched.filter(u => !inPlan.has(u.id) && !seen.has(u.id) && seen.add(u.id));
  const lastR = plan.days[n - 1].r, depLeg = airportLeg(S.trip.dep, STAY_BY[plan.stays[lastR]], lastR);
  plan.warn = depLeg.min > 150 ? { k: 'farDep', min: depLeg.min, r: lastR } : null;
  return plan;
}

function dayOver(plan, i) {
  const sc = scheduleDay(plan, i), w = dayWindow(plan, i), last = sc.rows[sc.rows.length - 1];
  const late = sc.rows.filter(o => (o.e.k === 'place' || o.e.k === 'meal') && o.flags.some(f => f[0] === 'late' || f[0] === 'shut' || f[0] === 'closed'));
  const over = plan.days[i].last ? last.start > S.trip.depT - 2.5 + 0.05 : last.start > w.end + 0.75;
  return { over, late, sc };
}
function fitRegion(plan, idx, unsched) {
  for (let pass = 0; pass < 16; pass++) {
    let changed = false;
    for (const i of idx) {
      const chk = dayOver(plan, i); if (!chk.over && !chk.late.length) continue;
      const st = plan.days[i].stops, stay = STAY_BY[plan.stays[plan.days[i].r]];
      const cand = st.map((x, si) => ({ x, si })).filter(o => o.x.k === 'place');
      if (!cand.length) continue;
      const lateIds = new Set(chk.late.map(o => o.e.id));
      const marg = o => { const prev = o.si > 0 ? (PBY[st[o.si - 1].id] || stay) : stay, next = o.si < st.length - 1 ? (PBY[st[o.si + 1].id] || stay) : stay; return detour(prev, next, PBY[o.x.id], plan.days[i].r) + PBY[o.x.id].h * 30; };
      cand.sort((a, b) => (lateIds.has(b.x.id) - lateIds.has(a.x.id)) || (TOP.has(a.x.id) - TOP.has(b.x.id)) || (marg(b) - marg(a)));
      const v = cand[0]; st.splice(v.si, 1);
      let placed = false;
      for (const j of idx.filter(j => j !== i).sort((a, b) => plan.days[a].stops.length - plan.days[b].stops.length)) {
        if (!openOn(PBY[v.x.id], plan.days[j].date)) continue;
        const at = bestInsertAt(plan, j, v.x.id); plan.days[j].stops.splice(at, 0, v.x);
        const c2 = dayOver(plan, j); if (!c2.over && !c2.late.some(o => o.e.id === v.x.id)) { placed = true; break; }
        plan.days[j].stops.splice(at, 1);
      }
      if (!placed) unsched.push({ id: v.x.id, why: 'full' });
      changed = true;
    }
    if (!changed) break;
  }
}

/* ---------- schedule for display ---------- */
function entriesOf(plan, i) {
  const day = plan.days[i], stay = STAY_BY[plan.stays[day.r]], L = [];
  if (day.first) { L.push({ k: 'arrive', ap: S.trip.arr }); L.push({ k: 'stay', stay, drop: true }); }
  else if (day.transfer) { const ps = STAY_BY[plan.stays[plan.days[i - 1].r]]; L.push({ k: 'checkout', stay: ps }); L.push({ k: 'transfer', from: plan.days[i - 1].r, to: day.r }); L.push({ k: 'stay', stay, drop: true }); }
  else L.push({ k: 'start', stay });
  day.stops.forEach((s, si) => L.push(Object.assign({ si }, s)));
  if (day.last) { L.push({ k: 'stay', stay, pickup: true }); L.push({ k: 'depart', ap: S.trip.dep }); }
  else L.push({ k: 'end', stay });
  return L;
}
function scheduleDay(plan, i) {
  const day = plan.days[i], r = day.r, pace = PACE[S.trip.pace], L = entriesOf(plan, i), out = [];
  let t, pos, n = 0, cost = 0, moveMin = 0;
  const people = Math.max(1, S.trip.people);
  for (let k = 0; k < L.length; k++) {
    const e = L[k], o = { e, flags: [] };
    if (k === 0) {
      if (e.k === 'arrive') { t = S.trip.arrT; o.start = t; o.end = t + 1; pos = AIRPORTS[e.ap]; }
      else if (e.k === 'checkout') { t = 9; o.start = t; o.end = t; pos = e.stay; }
      else { t = pace.start; o.start = t; o.end = t; pos = e.stay; }
      t = o.end; out.push(o); continue;
    }
    let leg = null;
    if (e.k === 'stay' && L[k - 1].k === 'arrive') leg = airportLeg(L[k - 1].ap, e.stay, r);
    else if (e.k === 'transfer') leg = interRegion(e.from, e.to);
    else if (e.k === 'stay' && L[k - 1].k === 'transfer') leg = { mode: REGIONS[r].sub ? 'subway' : 'taxi', min: 15, cost: REGIONS[r].sub ? 1500 : 6000, group: !REGIONS[r].sub };
    else if (e.k === 'depart') leg = airportLeg(e.ap, pos, r);
    else { const tgt = e.id ? PBY[e.id] : (e.stay || null); leg = tgt ? legBetween(pos, tgt, r) : null; }
    if (leg && leg.min) { o.leg = leg; moveMin += leg.min; cost += leg.group ? leg.cost / people : leg.cost; }
    const a = t + (leg ? leg.min / 60 : 0);
    if (e.k === 'place' || e.k === 'meal') {
      const p = e.id ? PBY[e.id] : null, dur = p ? p.h : 1;
      let b = a, soft = a;
      if (e.k === 'meal') soft = e.slot === 'dinner' ? (a >= 12 ? Math.max(a, 17.5) : a) : (a >= 9.5 ? Math.max(a, 11.5) : a);
      else if (p && p.best === 'night' && a >= 15) soft = Math.max(a, 18); else if (p && p.best === 'eve' && a >= 14) soft = Math.max(a, 16);
      if (soft - a > 0.75) o.flags.push(['free', Math.round((soft - a) * 60)]);
      b = soft;
      if (p) { if (p.o[0] > b) { const w0 = b; b = p.o[0];
          const prevRow = out[out.length - 1];
          if (prevRow && prevRow.e.k === 'start') { const sh = b - w0; prevRow.start += sh; prevRow.end += sh; }
          else if (b - w0 > 0.3) o.flags.push(['wait', Math.round((b - w0) * 60)]); }
        if (!inSeason(p, day.date)) o.flags.push(['season']); else if (!openOn(p, day.date)) o.flags.push(['closed']);
        else if (b >= p.o[1]) o.flags.push(['shut']); else if (b + dur > p.o[1] + 0.1) o.flags.push(['late']);
        if (p.best === 'night' && b < 17.5) o.flags.push(['night']); else if (p.best === 'eve' && b < 15.5) o.flags.push(['eve']);
        cost += p.cost || (e.k === 'meal' ? 12000 : 0); pos = p; }
      else cost += 12000;
      if (e.sug) o.flags.push(['sug']);
      o.start = b; o.end = b + dur; o.num = ++n;
    } else if (e.k === 'stay') { o.start = a; o.end = a + (e.drop ? 0.35 : 0.25); pos = e.stay; }
    else if (e.k === 'transfer') { o.start = t; o.end = a; pos = REGIONS[e.to]; }
    else if (e.k === 'depart') { o.start = a; o.end = a; if (a > S.trip.depT - 2.4) o.flags.push(['depLate']); }
    else { o.start = a; o.end = a; pos = e.stay; }
    t = o.end; out.push(o);
  }
  return { rows: out, cost: Math.round(cost / 100) * 100, moveMin, places: n };
}

/* ---------- editing ---------- */
function locAt(st, k, stay, dir) { for (let j = k; j >= 0 && j < st.length; j += dir) if (st[j].id) return PBY[st[j].id]; return stay; }
function bestInsertAt(plan, i, id) {
  const day = plan.days[i], stay = STAY_BY[plan.stays[day.r]], p = PBY[id], st = day.stops;
  let bi = st.length, bd = 1e9;
  for (let k = 0; k <= st.length; k++) { const prev = locAt(st, k - 1, stay, -1), next = locAt(st, k, stay, 1);
    let d = detour(prev, next, p, day.r); if (bucketOf(p) === 3 && k < st.length) d += 20; if (d < bd) { bd = d; bi = k; } }
  return bi;
}
const Plan = {
  move(i, si, dir) { const st = S.plan.days[i].stops, j = si + dir; if (j < 0 || j >= st.length) return; [st[si], st[j]] = [st[j], st[si]]; persist(); },
  remove(i, si) { const st = S.plan.days[i].stops, e = st[si]; st.splice(si, 1); if (e.id && isSaved(e.id) && e.k === 'place') S.plan.unsched.push({ id: e.id, why: 'removed' }); persist(); },
  moveTo(i, si, j) { const e = S.plan.days[i].stops.splice(si, 1)[0]; if (!e.id) { persist(); return; } const at = bestInsertAt(S.plan, j, e.id); S.plan.days[j].stops.splice(at, 0, e); persist(); },
  add(id, j) { S.plan.unsched = S.plan.unsched.filter(u => u.id !== id); const p = PBY[id]; const e = { k: isFood(p) ? 'meal' : 'place', id, slot: 'lunch' }; S.plan.days[j].stops.splice(bestInsertAt(S.plan, j, id), 0, e); persist(); },
  optimize(i) {
    const day = S.plan.days[i], stay = STAY_BY[S.plan.stays[day.r]];
    const places = day.stops.filter(s => s.k === 'place').map(s => s.id);
    const meals = day.stops.filter(s => s.k === 'meal' && s.id).map(s => s.id);
    day.stops = orderDayPlaces(places, stay, dayWindow(S.plan, i).start, day.r).map(id => ({ k: 'place', id }));
    const used = new Set([...S.saved, ...S.plan.days.flatMap(d => d.stops.map(s => s.id)).filter(Boolean)]);
    meals.forEach(id => used.delete(id));
    const left = insertMeals(S.plan, [i], meals.filter(id => isSaved(id)), used);
    left.forEach(id => S.plan.unsched.push({ id, why: 'meals' }));
    persist();
  },
  swapMeal(i, si) {
    const day = S.plan.days[i], e = day.stops[si], stay = STAY_BY[S.plan.stays[day.r]];
    const prev = si > 0 ? (PBY[day.stops[si - 1].id] || stay) : stay, next = si < day.stops.length - 1 ? (PBY[day.stops[si + 1].id] || stay) : stay;
    const inPlan = new Set(S.plan.days.flatMap(d => d.stops.map(s => s.id)).filter(Boolean));
    const c = PLACES.filter(p => p.r === day.r && isFood(p) && !(p.prem && S.trip.budget < 2) && mealFits(p, e.slot || 'lunch', day.date) && (!inPlan.has(p.id) || p.id === e.id))
      .map(p => [detour(prev, next, p, day.r), p.id]).sort((a, b) => a[0] - b[0]).slice(0, 6).map(x => x[1]);
    if (!c.length) return false;
    const k = c.indexOf(e.id); e.id = c[(k + 1) % c.length]; e.sug = !isSaved(e.id); persist(); return true;
  }
};
