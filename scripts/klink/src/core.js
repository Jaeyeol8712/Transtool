'use strict';
/* =========================================================
   K-Link core: data, geography helpers, state, persistence
   ========================================================= */
const PLACES = window.__PLACES__, GEO = window.__GEO__;
// 해외 도시(어라운드툴 해외 여행 가이드에서 온 지역·공항·숙소 권역). tools/build_overseas.py 가 만든다.
const OVD = window.__OV__ || { countries: {}, order: [], regions: {}, airports: {}, stays: [] };
const PBY = Object.fromEntries(PLACES.map(p => [p.id, p]));
const LANG_IDX = { ko: 0, zh: 1, en: 2, ja: 3 };
const LANGS = [['ko', '한국어', 'KO'], ['zh', '中文', '中'], ['en', 'English', 'EN'], ['ja', '日本語', '日']];
const HTML_LANG = { ko: 'ko', zh: 'zh-CN', en: 'en', ja: 'ja' };

const CATS = {
  palace: { col: '#A0522D' }, food: { col: '#EF7C1C' }, skin: { col: '#E8457A' }, shop: { col: '#0E9A63' },
  cafe: { col: '#8C6A4B' }, kpop: { col: '#8E5BD8' }, night: { col: '#3B3FB6' }, nature: { col: '#0E9F8F' }, fun: { col: '#D99A00' }
};
const CAT_ORDER = ['palace', 'nature', 'food', 'cafe', 'shop', 'night', 'kpop', 'fun'];
const LINE = ['#2443E8', '#00A84D', '#EF7C1C', '#00A5DE', '#996CAC', '#CD7C2F', '#747F00', '#E6186C', '#8C7B5A', '#5E8E3E'];

const REGIONS = {
  seoul:     { lat: 37.5600, lng: 126.9850, sub: true,  air: 'ICN', fromSeoul: 0,   t: ['서울', '首尔', 'Seoul', 'ソウル'] },
  busan:     { lat: 35.1300, lng: 129.0800, sub: true,  air: 'PUS', fromSeoul: 160, t: ['부산', '釜山', 'Busan', '釜山'] },
  jeju:      { lat: 33.3900, lng: 126.5500, sub: false, air: 'CJU', fromSeoul: 70,  fly: true, t: ['제주', '济州', 'Jeju', '済州'] },
  gyeongju:  { lat: 35.8200, lng: 129.2600, sub: false, air: 'ICN', fromSeoul: 130, t: ['경주', '庆州', 'Gyeongju', '慶州'] },
  gangneung: { lat: 37.8000, lng: 128.8900, sub: false, air: 'ICN', fromSeoul: 115, t: ['강릉', '江陵', 'Gangneung', '江陵'] },
  jeonju:    { lat: 35.8150, lng: 127.1500, sub: false, air: 'ICN', fromSeoul: 105, t: ['전주', '全州', 'Jeonju', '全州'] },
  yeosu:     { lat: 34.7300, lng: 127.7400, sub: false, air: 'ICN', fromSeoul: 180, t: ['여수', '丽水', 'Yeosu', '麗水'] }
};
const KR_IDS = Object.keys(REGIONS);
for (const r of KR_IDS) REGIONS[r].cc = 'kr';
for (const [id, v] of Object.entries(OVD.regions)) REGIONS[id] = v;
const REGION_IDS = Object.keys(REGIONS);
const OV_IDS = REGION_IDS.filter(r => REGIONS[r].cc !== 'kr');
const isOv = r => !!(REGIONS[r] && REGIONS[r].cc !== 'kr');
const AIRPORTS = {
  ICN: { lat: 37.4602, lng: 126.4407, r: 'seoul', t: ['인천공항', '仁川机场', 'Incheon (ICN)', '仁川空港'] },
  GMP: { lat: 37.5583, lng: 126.7906, r: 'seoul', t: ['김포공항', '金浦机场', 'Gimpo (GMP)', '金浦空港'] },
  PUS: { lat: 35.1796, lng: 128.9382, r: 'busan', t: ['김해공항', '金海机场', 'Gimhae (PUS)', '金海空港'] },
  CJU: { lat: 33.5104, lng: 126.4914, r: 'jeju', t: ['제주공항', '济州机场', 'Jeju (CJU)', '済州空港'] }
};
for (const c of Object.keys(AIRPORTS)) AIRPORTS[c].cc = 'kr';
for (const [c, v] of Object.entries(OVD.airports)) AIRPORTS[c] = v;   // 해외 공항: to = { 지역: 공항→도심 분 }
// Where to stay: candidate neighbourhoods per region with station / access notes.
const STAYS = [
  ['myeongdong', 'seoul', 37.5609, 126.9863, ['명동', '明洞', 'Myeongdong', '明洞'], ['명동역 · 4호선', '明洞站 · 4号线', 'Myeong-dong Stn · Line 4', '明洞駅 · 4号線']],
  ['jongno', 'seoul', 37.5701, 126.9827, ['종로·광화문', '钟路·光化门', 'Jongno & Gwanghwamun', '鍾路・光化門'], ['종각역 · 1호선', '钟阁站 · 1号线', 'Jonggak Stn · Line 1', '鍾閣駅 · 1号線']],
  ['hongdae', 'seoul', 37.5572, 126.9245, ['홍대', '弘大', 'Hongdae', '弘大'], ['홍대입구역 · 2호선·공항철도', '弘大入口站 · 2号线·机场快线', 'Hongik Univ. Stn · Line 2 & AREX', '弘大入口駅 · 2号線・空港鉄道']],
  ['dongdaemun', 'seoul', 37.5665, 127.0092, ['동대문', '东大门', 'Dongdaemun', '東大門'], ['동대문역사문화공원역 · 2·4·5호선', '东大门历史文化公园站 · 2·4·5号线', 'DDP Stn · Lines 2, 4, 5', '東大門歴史文化公園駅 · 2・4・5号線']],
  ['seongsu', 'seoul', 37.5446, 127.0557, ['성수', '圣水', 'Seongsu', '聖水'], ['성수역 · 2호선', '圣水站 · 2号线', 'Seongsu Stn · Line 2', '聖水駅 · 2号線']],
  ['gangnam', 'seoul', 37.4979, 127.0276, ['강남', '江南', 'Gangnam', '江南'], ['강남역 · 2호선·신분당선', '江南站 · 2号线·新盆唐线', 'Gangnam Stn · Line 2 & Sinbundang', '江南駅 · 2号線・新盆唐線']],
  ['yeouido', 'seoul', 37.5216, 126.9243, ['여의도', '汝矣岛', 'Yeouido', '汝矣島'], ['여의도역 · 5·9호선', '汝矣岛站 · 5·9号线', 'Yeouido Stn · Lines 5, 9', '汝矣島駅 · 5・9号線']],
  ['jamsil', 'seoul', 37.5133, 127.1001, ['잠실', '蚕室', 'Jamsil', '蚕室'], ['잠실역 · 2·8호선', '蚕室站 · 2·8号线', 'Jamsil Stn · Lines 2, 8', '蚕室駅 · 2・8号線']],
  ['haeundae', 'busan', 35.1631, 129.1635, ['해운대', '海云台', 'Haeundae', '海雲台'], ['해운대역 · 2호선', '海云台站 · 2号线', 'Haeundae Stn · Line 2', '海雲台駅 · 2号線']],
  ['seomyeon', 'busan', 35.1577, 129.0596, ['서면', '西面', 'Seomyeon', '西面'], ['서면역 · 1·2호선', '西面站 · 1·2号线', 'Seomyeon Stn · Lines 1, 2', '西面駅 · 1・2号線']],
  ['nampo', 'busan', 35.0980, 129.0306, ['남포동', '南浦洞', 'Nampo-dong', '南浦洞'], ['남포역 · 1호선', '南浦站 · 1号线', 'Nampo Stn · Line 1', '南浦駅 · 1号線']],
  ['gwangalli', 'busan', 35.1532, 129.1186, ['광안리', '广安里', 'Gwangalli', '広安里'], ['광안역 · 2호선', '广安站 · 2号线', 'Gwangan Stn · Line 2', '広安駅 · 2号線']],
  ['jejucity', 'jeju', 33.4890, 126.4980, ['제주 시내', '济州市区', 'Jeju City', '済州市内'], ['제주공항 차로 10분', '距济州机场车程 10 分钟', '10 min drive from the airport', '済州空港から車で10分']],
  ['aewol', 'jeju', 33.4630, 126.3100, ['애월', '涯月', 'Aewol', '涯月'], ['해안도로 · 렌터카 추천', '海岸公路 · 建议租车', 'Coast road · car recommended', '海岸道路 · レンタカー推奨']],
  ['jungmun', 'jeju', 33.2490, 126.4120, ['중문', '中文', 'Jungmun', '中文'], ['리조트 단지 · 공항버스 600번', '度假区 · 机场巴士 600 路', 'Resort area · airport bus 600', 'リゾート地区 · 空港バス600番']],
  ['seogwipo', 'jeju', 33.2490, 126.5600, ['서귀포', '西归浦', 'Seogwipo', '西帰浦'], ['서귀포 시내 · 올레시장 근처', '西归浦市区 · 近每日偶来市场', 'Downtown Seogwipo · near Olle Market', '西帰浦市内 · オルレ市場の近く']],
  ['seongsan', 'jeju', 33.4580, 126.9300, ['성산', '城山', 'Seongsan', '城山'], ['성산항 · 우도 배편', '城山港 · 去牛岛的船', 'Seongsan port · Udo ferry', '城山港 · 牛島行きの船']],
  ['gj_down', 'gyeongju', 35.8380, 129.2100, ['경주 시내', '庆州市区', 'Downtown Gyeongju', '慶州市内'], ['황리단길 · 버스 터미널 근처', '皇理团路 · 近巴士客运站', 'Hwangnidan-gil · near bus terminal', '皇理団通り · バスターミナル近く']],
  ['gj_bomun', 'gyeongju', 35.8420, 129.2850, ['보문단지', '普门园区', 'Bomun Lake', '普門団地'], ['호수 리조트 · 택시 이동', '湖边度假区 · 打车', 'Lakeside resorts · taxi', '湖畔リゾート · タクシー']],
  ['gn_station', 'gangneung', 37.7640, 128.8990, ['강릉역', '江陵站', 'Gangneung Stn', '江陵駅'], ['KTX 강릉역', 'KTX 江陵站', 'KTX Gangneung Stn', 'KTX江陵駅']],
  ['gn_gyeongpo', 'gangneung', 37.7950, 128.9080, ['경포', '镜浦', 'Gyeongpo', '鏡浦'], ['해변 호텔 · 택시 10분', '海边酒店 · 打车 10 分钟', 'Beach hotels · 10 min taxi', '海辺ホテル · タクシー10分']],
  ['jn_hanok', 'jeonju', 35.8150, 127.1530, ['한옥마을', '韩屋村', 'Hanok Village', '韓屋村'], ['한옥 스테이 · 전주역 택시 15분', '韩屋民宿 · 全州站打车 15 分钟', 'Hanok stays · 15 min taxi from station', '韓屋ステイ · 全州駅からタクシー15分']],
  ['ys_expo', 'yeosu', 34.7530, 127.7470, ['여수엑스포역', '丽水世博站', 'Yeosu Expo Stn', '麗水エキスポ駅'], ['KTX 종착역 · 오동도 도보', 'KTX 终点站 · 步行到梧桐岛', 'KTX terminus · walk to Odongdo', 'KTX終点駅 · 梧桐島へ徒歩']],
  ['ys_dolsan', 'yeosu', 34.7280, 127.7430, ['돌산', '突山', 'Dolsan', '突山'], ['오션뷰 호텔 · 케이블카 근처', '海景酒店 · 近缆车', 'Sea-view hotels · near cable car', 'オーシャンビュー · ケーブルカー近く']]
].concat(OVD.stays).map(([id, r, lat, lng, t, st]) => ({ id, r, lat, lng, t, st }));
const STAY_BY = Object.fromEntries(STAYS.map(s => [s.id, s]));
const REGION_TAG = {
  seoul: ['궁궐과 쇼핑, K-뷰티의 중심', '宫殿、购物与韩式美容中心', 'Palaces, shopping and K-beauty', '宮殿とショッピング、Kビューティーの中心'],
  busan: ['바다와 시장, 야경의 도시', '大海、市场与夜景之城', 'Beaches, markets and night views', '海と市場、夜景の街'],
  jeju: ['화산섬 자연과 바다 카페', '火山岛自然与海边咖啡馆', 'Volcanic nature and seaside cafés', '火山島の自然と海辺カフェ'],
  gyeongju: ['천년 신라의 유적', '千年新罗古迹', 'A thousand years of Silla heritage', '千年の新羅の遺跡'],
  gangneung: ['커피 거리와 동해 바다', '咖啡街与东海', 'Coffee street and the East Sea', 'コーヒー通りと東海'],
  jeonju: ['한옥마을과 비빔밥', '韩屋村与拌饭', 'Hanok village and bibimbap', '韓屋村とビビンバ'],
  yeosu: ['밤바다와 섬 풍경', '夜海与海岛风光', 'Night sea and island views', '夜の海と島の風景']
};

for (const r of OV_IDS) REGION_TAG[r] = REGIONS[r].tag;
const countryName = cc => OVD.countries[cc] ? tr4(OVD.countries[cc]) : T.korea;

/* district lookup from geometry */
const DISTRICTS = {};
for (const [r, reg] of Object.entries(GEO.regions)) for (const d of reg.districts) DISTRICTS[d.id] = Object.assign({ r }, d);
for (const p of PLACES) p.dist = GEO.pd[p.id];

/* ---------- 어라운드툴 연결 데이터 ---------- */
// build.py가 만드는 /klink/around.json. 빌드 때 넣어 둔 사본으로 먼저 그리고, 사이트에서는 최신본을 다시 읽는다.
let AROUND = window.__AROUND__ || null;
const JEJU_SI = { jj_city: '제주시', jj_aewol: '제주시', jj_hallim: '제주시', jj_halla: '제주시', jj_andeok: '서귀포시', jj_jungmun: '서귀포시', jj_seogwipo: '서귀포시', jj_seongsan: '서귀포시' };
const aroundRegion = r => (AROUND && AROUND.regions && AROUND.regions[r]) || null;
function aroundGu(did) {
  const d = DISTRICTS[did], ar = d && aroundRegion(d.r); if (!ar || !ar.gus.length) return null;
  const name = JEJU_SI[did] || d.n[0];
  return ar.gus.find(g => g.gu === name) || (d.kind === 'zone' && ar.gus.length === 1 ? ar.gus[0] : null);
}
function loadAround(done) {
  if (!/^https?:$/.test(location.protocol) || !/aroundtool\.com$|^localhost$/.test(location.hostname)) return;
  fetch('around.json', { cache: 'no-cache' }).then(r => r.ok ? r.json() : null).then(j => { if (j && j.regions) { AROUND = j; done && done(); } }).catch(() => {});
}

/* ---------- small helpers ---------- */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const tr4 = arr => arr[LANG_IDX[S.lang]] ?? arr[0];
const pn = id => { const p = PBY[id]; return p ? (p.n[S.lang] || p.n.ko) : ''; };
const pd = id => { const p = PBY[id]; return p ? (p.d[S.lang] || (S.lang !== 'ko' && p.d.en) || p.d.ko) : ''; };
const rn = r => REGIONS[r] ? tr4(REGIONS[r].t) : r;
const dn = id => DISTRICTS[id] ? tr4(DISTRICTS[id].n) : '';
const sn = id => STAY_BY[id] ? tr4(STAY_BY[id].t) : '';
const an = code => AIRPORTS[code] ? tr4(AIRPORTS[code].t) : code;
function hav(a, b) { const R = 6371, t = Math.PI / 180; const dLa = (b.lat - a.lat) * t, dLo = (b.lng - a.lng) * t;
  const x = Math.sin(dLa / 2) ** 2 + Math.cos(a.lat * t) * Math.cos(b.lat * t) * Math.sin(dLo / 2) ** 2; return 2 * R * Math.asin(Math.sqrt(x)); }
const hm = v => { v = ((v % 24) + 24) % 24; const h = Math.floor(v + 1e-6), m = Math.round((v - h) * 60); return `${String(h + (m === 60 ? 1 : 0)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`; };
const toDate = s => new Date(s + 'T00:00:00');
const fmtD = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const addDays = (s, n) => { const d = toDate(s); d.setDate(d.getDate() + n); return fmtD(d); };
function tripDates() { const out = []; let d = S.trip.start; for (let i = 0; i < 14 && d <= S.trip.end; i++) { out.push(d); d = addDays(d, 1); } return out.length ? out : [S.trip.start]; }
function catIcon(c) { return ICONS['c_' + c] || ICONS.c_palace; }

/* ---------- travel model ---------- */
// mode: walk | subway | taxi | car | rail | flight | airport
function legBetween(a, b, r) {
  const L = legRaw(a, b, r);
  if (isOv(r)) { L.cost = 0; L.ov = true; }   // 해외 교통비는 계산하지 않는다 (현지 요금 확인)
  return L;
}
function legRaw(a, b, r) {
  const km = hav(a, b);
  if (km < 0.05) return { mode: 'walk', min: 0, km: 0, cost: 0 };
  if (km <= 0.9) return { mode: 'walk', min: Math.max(4, Math.round(km * 1.25 / 4.5 * 60)), km, cost: 0 };
  if (REGIONS[r] && REGIONS[r].sub && km < 30) return { mode: 'subway', min: Math.round(10 + km * 1.25 * 2.1), km, cost: 1500 };
  if (km < 22) return { mode: 'taxi', min: Math.round(6 + km * 1.3 * 1.9), km, cost: Math.round((4800 + Math.max(0, km * 1.3 - 1.6) * 760) / 100) * 100, group: true };
  return { mode: 'car', min: Math.round(10 + km * 1.3 * 1.25), km, cost: Math.round((4800 + km * 1.3 * 760) / 1000) * 1000, group: true };
}
function interRegion(a, b) {
  if (a === b) return null;
  const A = REGIONS[a], B = REGIONS[b];
  if (isOv(a) || isOv(b)) {   // 해외: 같은 나라 가까운 도시는 기차·버스, 멀거나 나라가 다르면 항공편 (시간만 어림, 요금은 계산 안 함)
    const km = hav(A, B);
    if (A.cc === B.cc && km < 320) { const ride = Math.round((km * 0.75 + 20) / 5) * 5; return { mode: 'rail', min: ride + 40, ride, cost: 0, ov: true }; }
    const ride = Math.round((km / 780 * 60 + 35) / 5) * 5;
    return { mode: 'flight', min: ride + (A.cc === B.cc ? 110 : 190), ride, cost: 0, ov: true };
  }
  if (A.fly || B.fly) return { mode: 'flight', min: 70 + 100, ride: 70, cost: 70000 };
  let ride;
  if (a === 'seoul') ride = B.fromSeoul; else if (b === 'seoul') ride = A.fromSeoul;
  else ride = Math.round((hav(A, B) * 0.6 + 25) / 5) * 5;
  return { mode: 'rail', min: ride + 40, ride, cost: Math.round(ride * 360 / 100) * 100 };
}
// airport <-> a point inside region r
function airportLeg(code, pt, r) {
  const ap = AIRPORTS[code];
  if (ap.to) {   // 해외 공항: 여행 가이드의 '공항 → 시내' 시간에 도심에서 떨어진 만큼 더한다
    if (ap.to[r] != null) return { mode: 'airport', min: Math.round(ap.to[r] + hav(REGIONS[r], pt) * 2.2), km: 0, cost: 0, ov: true };
    const mid = interRegion(ap.r, r), last = legBetween(REGIONS[r], pt, r);
    return { mode: mid.mode, min: ap.to[ap.r] + mid.min + last.min, km: 0, cost: 0, via: true, ov: true };
  }
  if (isOv(r)) { const mid = interRegion(ap.r, r), last = legBetween(REGIONS[r], pt, r); return { mode: 'flight', min: 60 + mid.min + last.min, km: 0, cost: 0, via: true, ov: true }; }
  if (ap.r === r) {
    const km = hav(ap, pt);
    if (code === 'ICN') return { mode: 'airport', min: Math.round(18 + km * 1.05), km, cost: 12000 };
    if (code === 'GMP' && r === 'seoul') return { mode: 'subway', min: Math.round(12 + km * 2.1), km, cost: 1800 };
    if (code === 'PUS') return { mode: 'airport', min: Math.round(15 + km * 2), km, cost: 3000 };
    return { mode: 'taxi', min: Math.round(6 + km * 1.3 * 1.9), km, cost: Math.round((4800 + km * 1.3 * 760) / 100) * 100, group: true };
  }
  const hub = REGIONS[ap.r], first = airportLeg(code, hub, ap.r), mid = interRegion(ap.r, r), last = legBetween(REGIONS[r], pt, r);
  return { mode: mid.mode, min: first.min + mid.min + last.min, km: 0, cost: first.cost + mid.cost, via: true };
}
/* ---------- 여행 나라와 공항 ---------- */
// 저장한 곳이 가장 많은 나라가 이번 여행 나라. 공항은 그 나라 공항 중에서 고른 것, 없으면 저장이 가장 많은 도시의 공항.
let _taKey = null, _ta = null;
function tripAir() {
  const key = S.saved.join(',') + '|' + S.trip.arr + '|' + S.trip.dep + '|' + (S.ui.r || '') + '|' + (S.ui.scope || '');
  if (key === _taKey) return _ta;
  const cnt = {}, rc = {};
  for (const id of S.saved) { const r = PBY[id].r, cc = REGIONS[r].cc; cnt[cc] = (cnt[cc] || 0) + 1; rc[r] = (rc[r] || 0) + 1; }
  const cc = Object.keys(cnt).sort((a, b) => cnt[b] - cnt[a])[0] || (S.ui.r && REGIONS[S.ui.r] ? REGIONS[S.ui.r].cc : 'kr');
  const ok = c => AIRPORTS[c] && AIRPORTS[c].cc === cc;
  let def = 'ICN';
  if (cc !== 'kr') {
    const top = Object.keys(rc).filter(r => REGIONS[r].cc === cc).sort((a, b) => rc[b] - rc[a])[0] || (S.ui.r && REGIONS[S.ui.r] && REGIONS[S.ui.r].cc === cc ? S.ui.r : OV_IDS.find(r => REGIONS[r].cc === cc));
    def = REGIONS[top].air;
  }
  _taKey = key; _ta = { cc, ov: cc !== 'kr', arr: ok(S.trip.arr) ? S.trip.arr : def, dep: ok(S.trip.dep) ? S.trip.dep : def };
  return _ta;
}
function regionOfPoint(pt) { let best = 'seoul', bd = 1e9; for (const r of REGION_IDS) { const d = hav(REGIONS[r], pt); if (d < bd) { bd = d; best = r; } } return best; }

/* ---------- state & persistence ---------- */
const KEY = 'klink-v2';
const DEFAULT = () => ({
  v: 2, lang: null, seenIntro: false,
  trip: { start: '2026-11-14', end: '2026-11-17', people: 2, party: 1, budget: 1, pace: 1, interests: ['palace', 'food', 'night'],
          arr: 'ICN', arrT: 10, dep: 'ICN', depT: 19 },
  saved: [], order: [], plan: null, stayOv: {},
  ui: { tab: 'map', lvl: 'korea', scope: 'kr', r: null, d: null, sel: null, filter: 'all', day: 0, mode3d: true }
});
let S = DEFAULT();
// Browser storage is off: state lives only in memory and resets on reload. Remove anything an earlier version stored.
try { localStorage.removeItem(KEY); } catch (e) {}
S.saved = S.saved.filter(id => PBY[id]);
let saveT = null;
function persist() { /* storage disabled on purpose */ }

function savedRegions() {
  const rs = [...new Set(S.saved.map(id => PBY[id].r))];
  S.order = S.order.filter(r => rs.includes(r));
  for (const r of rs) if (!S.order.includes(r)) S.order.push(r);
  return S.order.slice();
}
function toggleSave(id) {
  const i = S.saved.indexOf(id);
  if (i >= 0) S.saved.splice(i, 1); else S.saved.push(id);
  savedRegions(); persist();
  return i < 0;
}
const isSaved = id => S.saved.includes(id);
function planSig() { const a = tripAir(); return JSON.stringify([S.saved.slice().sort(), S.order, S.trip.start, S.trip.end, S.trip.pace, a.arr, S.trip.arrT, a.dep, S.trip.depT, S.stayOv]); }
