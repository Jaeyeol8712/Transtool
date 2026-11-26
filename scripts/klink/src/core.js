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
  yeosu:     { lat: 34.7300, lng: 127.7400, sub: false, air: 'ICN', fromSeoul: 180, t: ['여수', '丽水', 'Yeosu', '麗水'] },
  gunsan:    { lat: 35.9800, lng: 126.7200, sub: false, air: 'ICN', fromSeoul: 170, t: ['군산', '群山', 'Gunsan', '群山'] },
  mokpo:     { lat: 34.7950, lng: 126.3900, sub: false, air: 'ICN', fromSeoul: 150, t: ['목포', '木浦', 'Mokpo', '木浦'] },
  danyang:   { lat: 36.9850, lng: 128.3650, sub: false, air: 'ICN', fromSeoul: 120, t: ['단양', '丹阳', 'Danyang', '丹陽'] },
  pohang:    { lat: 36.0400, lng: 129.3700, sub: false, air: 'ICN', fromSeoul: 150, t: ['포항', '浦项', 'Pohang', '浦項'] },
  sokcho:    { lat: 38.2070, lng: 128.5918, sub: false, air: 'ICN', fromSeoul: 150, t: ['속초', '束草', 'Sokcho', '束草'] },
  daegu:     { lat: 35.8714, lng: 128.6014, sub: false, air: 'ICN', fromSeoul: 110, t: ['대구', '大邱', 'Daegu', '大邱'] },
  chuncheon: { lat: 37.8813, lng: 127.7298, sub: false, air: 'ICN', fromSeoul: 70, t: ['춘천', '春川', 'Chuncheon', '春川'] },
  tongyeong: { lat: 34.8420, lng: 128.4250, sub: false, air: 'ICN', fromSeoul: 240, t: ['통영', '统营', 'Tongyeong', '統営'] },
  ulsan:     { lat: 35.5384, lng: 129.3114, sub: false, air: 'ICN', fromSeoul: 140, t: ['울산', '蔚山', 'Ulsan', '蔚山'] },
  damyang:   { lat: 35.3200, lng: 126.9900, sub: false, air: 'ICN', fromSeoul: 210, t: ['담양', '潭阳', 'Damyang', '潭陽'] },
  gapyeong:  { lat: 37.7800, lng: 127.4600, sub: false, air: 'ICN', fromSeoul: 60, t: ['가평', '加平', 'Gapyeong', '加平'] },
  incheon:   { lat: 37.4500, lng: 126.6600, sub: true, air: 'ICN', fromSeoul: 60, t: ['인천', '仁川', 'Incheon', '仁川'] }
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
// 국내 여행(한국에 사는 사람): 공항 대신 집에서 가까운 KTX역에서 출발해 돌아온다 (home)
Object.assign(AIRPORTS, {
  SEL: { lat: 37.5547, lng: 126.9707, r: 'seoul', home: true, t: ['서울', '首尔', 'Seoul', 'ソウル'] },
  BSS: { lat: 35.1151, lng: 129.0422, r: 'busan', home: true, t: ['부산', '釜山', 'Busan', '釜山'] },
  DGU: { lat: 35.8794, lng: 128.6286, r: 'daegu', home: true, t: ['대구', '大邱', 'Daegu', '大邱'] },
  DJN: { lat: 36.3323, lng: 127.4342, r: null, home: true, t: ['대전', '大田', 'Daejeon', '大田'] },
  GJS: { lat: 35.1374, lng: 126.7930, r: null, home: true, t: ['광주', '光州', 'Gwangju', '光州'] },
  ICH: { lat: 37.4563, lng: 126.7052, r: 'incheon', home: true, t: ['인천', '仁川', 'Incheon', '仁川'] },
  SWN: { lat: 37.2659, lng: 127.0001, r: null, home: true, t: ['수원', '水原', 'Suwon', '水原'] },
  CAN: { lat: 36.7946, lng: 127.1046, r: null, home: true, t: ['천안·아산', '天安·牙山', 'Cheonan·Asan', '天安・牙山'] },
  CJJ: { lat: 36.6203, lng: 127.3271, r: null, home: true, t: ['청주·세종', '清州·世宗', 'Cheongju·Sejong', '清州・世宗'] },
  CCN: { lat: 37.8846, lng: 127.7168, r: 'chuncheon', home: true, t: ['춘천', '春川', 'Chuncheon', '春川'] },
  WJU: { lat: 37.3177, lng: 127.9198, r: null, home: true, t: ['원주', '原州', 'Wonju', '原州'] },
  GNH: { lat: 37.764, lng: 128.899, r: 'gangneung', home: true, t: ['강릉', '江陵', 'Gangneung', '江陵'] },
  JNH: { lat: 35.8497, lng: 127.1617, r: 'jeonju', home: true, t: ['전주', '全州', 'Jeonju', '全州'] },
  GSH: { lat: 35.9908, lng: 126.7117, r: 'gunsan', home: true, t: ['군산', '群山', 'Gunsan', '群山'] },
  MPH: { lat: 34.7915, lng: 126.3866, r: 'mokpo', home: true, t: ['목포', '木浦', 'Mokpo', '木浦'] },
  GPH: { lat: 37.8146, lng: 127.5106, r: 'gapyeong', home: true, t: ['가평', '加平', 'Gapyeong', '加平'] },
  DMH: { lat: 35.3210, lng: 126.9860, r: 'damyang', home: true, t: ['담양', '潭阳', 'Damyang', '潭陽'] },
  TYH: { lat: 34.8810, lng: 128.4140, r: 'tongyeong', home: true, t: ['통영', '统营', 'Tongyeong', '統営'] },
  SCB: { lat: 38.1898, lng: 128.6008, r: 'sokcho', home: true, t: ['속초', '束草', 'Sokcho', '束草'] },
  DYH: { lat: 36.9670, lng: 128.3420, r: 'danyang', home: true, t: ['단양', '丹阳', 'Danyang', '丹陽'] },
  YSH: { lat: 34.753, lng: 127.747, r: 'yeosu', home: true, t: ['여수', '丽水', 'Yeosu', '麗水'] },
  PHG: { lat: 36.0718, lng: 129.3418, r: 'pohang', home: true, t: ['포항', '浦项', 'Pohang', '浦項'] },
  GJH: { lat: 35.7983, lng: 129.1386, r: 'gyeongju', home: true, t: ['경주', '庆州', 'Gyeongju', '慶州'] },
  ULS: { lat: 35.5513, lng: 129.1384, r: 'ulsan', home: true, t: ['울산', '蔚山', 'Ulsan', '蔚山'] },
  CWN: { lat: 35.2335, lng: 128.6807, r: null, home: true, t: ['창원', '昌原', 'Changwon', '昌原'] },
  JJH: { lat: 33.4996, lng: 126.5312, r: 'jeju', home: true, t: ['제주', '济州', 'Jeju', '済州'] }
});
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
  ['ys_dolsan', 'yeosu', 34.7280, 127.7430, ['돌산', '突山', 'Dolsan', '突山'], ['오션뷰 호텔 · 케이블카 근처', '海景酒店 · 近缆车', 'Sea-view hotels · near cable car', 'オーシャンビュー · ケーブルカー近く']],
  ['gs_down', 'gunsan', 35.9870, 126.7120, ['군산 원도심', '群山旧城', 'Old Town Gunsan', '群山旧市街'], ['근대역사박물관 · 원도심 걸어서', '近代历史博物馆 · 步行游旧城', 'Walk the old town', '旧市街を徒歩で']],
  ['gs_island', 'gunsan', 35.8114, 126.4130, ['선유도', '仙游岛', 'Seonyudo', '仙遊島'], ['고군산군도 펜션 · 차 이동', '古群山民宿 · 需开车', 'Island stays · car needed', '島の宿 · 車が便利']],
  ['mp_station', 'mokpo', 34.7915, 126.3866, ['목포역·원도심', '木浦站·旧城', 'Mokpo Stn & Old Town', '木浦駅・旧市街'], ['KTX 목포역 · 원도심 걸어서', 'KTX 木浦站 · 步行到旧城', 'KTX Mokpo Stn · walk to old town', 'KTX木浦駅 · 旧市街へ徒歩']],
  ['mp_hadang', 'mokpo', 34.7950, 126.4320, ['하당·평화광장', '下塘·和平广场', 'Hadang & Peace Plaza', '下塘・平和広場'], ['바다분수 야경 · 택시 약 15분', '海上喷泉夜景 · 打车约 15 分钟', 'Fountain shows · about 15 min by taxi', '噴水の夜景 · タクシー約15分']],
  ['dy_town', 'danyang', 36.9846, 128.3654, ['단양읍 시내', '丹阳邑市区', 'Danyang Town', '丹陽邑市内'], ['구경시장·잔도 걸어서 · 단양역 택시 약 10분', '步行到市场与栈道 · 丹阳站打车约 10 分钟', 'Walk to the market and trail · about 10 min taxi from Danyang Stn', '市場・桟道へ徒歩 · 丹陽駅からタクシー約10分']],
  ['dy_station', 'danyang', 36.9670, 128.3420, ['단양역', '丹阳站', 'Danyang Stn', '丹陽駅'], ['KTX-이음 단양역 · 도담삼봉 차 약 10분', 'KTX-EUM 丹阳站 · 开车约 10 分钟到岛潭三峰', 'KTX-EUM Danyang Stn · about 10 min drive to Dodamsambong', 'KTX-イウム丹陽駅 · 島潭三峰へ車約10分']],
  ['ph_yeongil', 'pohang', 36.0560, 129.3790, ['영일대', '迎日台', 'Yeongildae', '迎日台'], ['해변 호텔 · 죽도시장 택시 약 10분', '海边酒店 · 打车约 10 分钟到竹岛市场', 'Beach hotels · about 10 min taxi to Jukdo Market', '海辺ホテル · 竹島市場へタクシー約10分']],
  ['ph_station', 'pohang', 36.0718, 129.3418, ['포항역', '浦项站', 'Pohang Stn', '浦項駅'], ['KTX 포항역 · 시내·호미곶은 차 이동', 'KTX 浦项站 · 市区和虎尾串需开车', 'KTX Pohang Stn · drive to town and Homigot', 'KTX浦項駅 · 市内・虎尾串へは車']],
  ['sc_stay_beach', 'sokcho', 38.1910, 128.6010, ['속초해수욕장·고속버스터미널 주변', '束草海水浴场·高速巴士站周边', 'Sokcho Beach & Express Bus Terminal area', '束草海水浴場・高速バスターミナル周辺'], ['버스 도착 후 바로 해변, 남쪽 대포항도 가까워요', '下车即到海滩，离南边大浦港也近', 'Steps from the beach and bus terminal, close to Daepo Port', 'ビーチとバスターミナルのすぐそば、大浦港にも近い']],
  ['sc_stay_central', 'sokcho', 38.2050, 128.5915, ['속초관광수산시장·중앙동 주변', '束草观光水产市场·中央洞周边', 'Fishery Market & Jungang-dong area', '束草観光水産市場・中央洞周辺'], ['시장·갯배·영금정을 걸어서 묶기 좋아요', '步行可到市场、渡船和灵琴亭', 'Walk to the market, Gaetbae ferry and Yeonggeumjeong', '市場・渡し船・霊琴亭へ歩いて回れる']],
  ['dg_stay_dongdaegu', 'daegu', 35.8797, 128.6286, ['동대구역 주변', '东大邱站周边', 'Around Dongdaegu Station', '東大邱駅周辺'], ['KTX 도착역 바로 앞, 팔공산·수성못 이동이 편해요', 'KTX到达站前，去八公山、寿城池方便', 'Right by the KTX station, easy to Palgongsan and Suseongmot', 'KTX駅前、八公山・寿城池へ便利']],
  ['dg_stay_dongseongno', 'daegu', 35.8690, 128.5950, ['동성로·반월당', '东城路·半月堂', 'Dongseong-ro & Banwoldang', '東城路・半月堂'], ['근대골목·서문시장·찜갈비 골목까지 걸어서 다녀요', '步行可到近代胡同、西门市场、炖排骨胡同', 'Walk to the modern alleys, Seomun Market and jjimgalbi alley', '近代路地・西門市場・チムカルビ路地へ徒歩圏']],
  ['cc_stay_station', 'chuncheon', 37.8846, 127.7168, ["춘천역 주변", "春川站周边", "Chuncheon Station area", "春川駅周辺"], ["ITX·전철 도착 후 바로, 소양강 스카이워크도 가까워요", "下车即到，离昭阳江天空步道也近", "Right by ITX/subway arrivals, near Soyanggang Skywalk", "ITX・電車ですぐ、昭陽江スカイウォークにも近い"]],
  ['cc_stay_myeongdong', 'chuncheon', 37.8805, 127.729, ["명동·중앙로 주변", "明洞·中央路周边", "Myeongdong & Jungang-ro area", "明洞・中央路周辺"], ["닭갈비골목·명동 거리·중앙시장을 걸어서 묶기 좋아요", "步行可到鸡排街、明洞街和中央市场", "Walk to Dakgalbi Street, Myeongdong and Jungang Market", "タッカルビ通り・明洞・中央市場へ歩いて回れる"]],
  ['ty_stay_ganguan', 'tongyeong', 34.8445, 128.4255, ["강구안·통영중앙시장 주변", "江口岸·统营中央市场周边", "Gangguan & Jungang Market area", "江口岸・統営中央市場周辺"], ["동피랑·통제영·디피랑을 걸어서 다녀요", "步行可到东皮郎、统制营和Dpirang", "Walk to Dongpirang, Tongjeyeong and Dpirang", "東ピラン・統制営・ディピランへ徒歩圏"]],
  ['ty_stay_donam', 'tongyeong', 34.827, 128.4215, ["도남동 관광단지 (케이블카·루지) 주변", "道南洞旅游区（缆车·滑车）周边", "Donam-dong resort area (cable car & luge)", "道南洞観光団地（ケーブルカー・リュージュ）周辺"], ["아침 일찍 케이블카·루지 타기 좋아요", "适合一早坐缆车、玩滑车", "Easy early start for the cable car and luge", "朝一番のケーブルカー・リュージュに便利"]],
  ['ul_stay_samsan', 'ulsan', 35.539, 129.337, ["태화강역·삼산동 주변", "太和江站·三山洞周边", "Taehwagang Station & Samsan-dong area", "太和江駅・三山洞周辺"], ["태화강 국가정원·장생포로 가기 편한 시내 중심", "去太和江国家庭园和长生浦都方便的市中心", "Central base for Taehwagang Garden and Jangsaengpo", "太和江国家庭園・長生浦へ行きやすい市中心"]],
  ['ul_stay_ilsan', 'ulsan', 35.4975, 129.43, ["일산해수욕장 주변", "日山海水浴场周边", "Ilsan Beach area", "日山海水浴場周辺"], ["대왕암공원·방어진 활어센터를 걸어서 묶기 좋아요", "步行可到大王岩公园和方鱼津活鱼中心", "Walk to Daewangam Park and Bangeojin fish market", "大王岩公園・方魚津活魚センターへ歩いて回れる"]],
  ['dm_stay_juknokwon', 'damyang', 35.3245, 126.989, ["담양읍 죽녹원·관방제림 주변", "潭阳邑竹绿苑·官防堤林周边", "Damyang-eup (Juknokwon & Gwanbangjerim)", "潭陽邑 竹緑苑・官防堤林周辺"], ["죽녹원·관방제림·담양 국수거리를 걸어서 묶기 좋아요", "步行可到竹绿苑、官防堤林和面条街", "Walk to Juknokwon, Gwanbangjerim and Noodle Street", "竹緑苑・官防堤林・ククス通りへ歩いて回れる"]],
  ['dm_stay_metaprovence', 'damyang', 35.3218, 126.9978, ["메타프로방스·메타세쿼이아길 주변", "Meta Provence·水杉林荫路周边", "Meta Provence & Metasequoia Road area", "メタプロバンス・メタセコイア並木道周辺"], ["아침 일찍 가로수길을 걷고 저녁엔 상점가를 둘러봐요", "清晨走林荫道，傍晚逛商街", "Early walks on the tree-lined road, evenings in the shops", "朝は並木道を歩き、夜は商店街を散策"]],
  ['gp_stay_station', 'gapyeong', 37.8146, 127.5106, ['가평역·가평읍 시내 주변', '加平站·加平邑市区周边', 'Gapyeong Station & town area', '加平駅・加平邑市街周辺'], ['남이섬·자라섬·레일바이크를 걸어서·버스로 묶기 좋아요', '步行或乘公交可去南怡岛、紫鳞岛和铁路自行车', 'Walk or bus to Nami, Jarasum and the rail bike', '南怡島・チャラ島・レールバイクへ徒歩やバスで']],
  ['gp_stay_cheongpyeong', 'gapyeong', 37.7353, 127.4265, ['청평역·청평호 주변', '清平站·清平湖周边', 'Cheongpyeong Station & lake area', '清平駅・清平湖周辺'], ['쁘띠프랑스·아침고요수목원으로 가기 편한 서쪽 거점', '去小法国村和晨静树木园都方便的西侧据点', 'Western base for Petite France and Morning Calm', 'プチフランス・朝の静かな樹木園へ行きやすい西側拠点']],
  ['ic_stay_dongincheon', 'incheon', 37.474, 126.625, ['인천역·동인천역 주변', '仁川站·东仁川站周边', 'Incheon & Dongincheon Station area', '仁川駅・東仁川駅周辺'], ['차이나타운·개항장·신포시장을 걸어서 묶기 좋아요', '步行可到中华街、开港场和新浦市场', 'Walk to Chinatown, the open port area and Sinpo Market', 'チャイナタウン・開港場・新浦市場へ歩いて回れる']],
  ['ic_stay_songdo', 'incheon', 37.3935, 126.64, ['송도 센트럴파크 주변', '松岛中央公园周边', 'Songdo Central Park area', '松島セントラルパーク周辺'], ['송도 센트럴파크 산책과 소래포구로 가기 편한 신도시', '方便散步松岛中央公园、去苏莱浦口的新城', 'New town base for Songdo Central Park and Sorae Port', '松島セントラルパーク散策と蘇莱浦口へ便利な新都市']]
].concat(OVD.stays).map(([id, r, lat, lng, t, st]) => ({ id, r, lat, lng, t, st }));
const STAY_BY = Object.fromEntries(STAYS.map(s => [s.id, s]));
const REGION_TAG = {
  seoul: ['궁궐과 쇼핑, K-뷰티의 중심', '宫殿、购物与韩式美容中心', 'Palaces, shopping and K-beauty', '宮殿とショッピング、Kビューティーの中心'],
  busan: ['바다와 시장, 야경의 도시', '大海、市场与夜景之城', 'Beaches, markets and night views', '海と市場、夜景の街'],
  jeju: ['화산섬 자연과 바다 카페', '火山岛自然与海边咖啡馆', 'Volcanic nature and seaside cafés', '火山島の自然と海辺カフェ'],
  gyeongju: ['천년 신라의 유적', '千年新罗古迹', 'A thousand years of Silla heritage', '千年の新羅の遺跡'],
  gangneung: ['커피 거리와 동해 바다', '咖啡街与东海', 'Coffee street and the East Sea', 'コーヒー通りと東海'],
  jeonju: ['한옥마을과 비빔밥', '韩屋村与拌饭', 'Hanok village and bibimbap', '韓屋村とビビンバ'],
  yeosu: ['밤바다와 섬 풍경', '夜海与海岛风光', 'Night sea and island views', '夜の海と島の風景'],
  gunsan: ['근대 거리와 고군산군도 바다', '近代街道与古群山群岛', 'Modern-era streets and the Gogunsan islands', '近代の街並みと古群山の海'],
  mokpo: ['해상케이블카와 유달산, 바다 분수', '海上缆车、儒达山与海上喷泉', 'Sea cable car, Yudalsan and fountain shows', '海上ケーブルカーと儒達山'],
  danyang: ['남한강 절벽과 동굴, 스카이워크', '南汉江悬崖、洞窟与天空步道', 'River cliffs, caves and a skywalk', '南漢江の断崖と洞窟、スカイウォーク'],
  pohang: ['동해 일출과 바다 위 걷는 조형물', '东海日出与海边步行雕塑', 'East Sea sunrise and a walkable sculpture', '東海の日の出と歩ける造形物'],
  sokcho: ['설악산과 동해 바다, 시장 먹거리를 함께 즐기는 강원 바닷가 도시', '雪岳山、东海与市场美食兼备的江原海滨城市', 'Gangwon seaside city of Seoraksan, the East Sea and market food', '雪岳山と東海、市場グルメがそろう江原の港町'],
  daegu: ['근대골목·시장·야경과 대구 10미를 함께 즐기는 도시', '近代胡同、市场、夜景与大邱十味', 'Modern alleys, markets, night views and Daegu\'s 10 signature dishes', '近代路地・市場・夜景と大邱十味の街'],
  chuncheon: ['호수와 강 위 스카이워크, 막국수·닭갈비의 도시', '湖泊与江上天空步道，荞麦冷面与铁板鸡之城', 'Lakes, a river skywalk, makguksu and dakgalbi', '湖と川のスカイウォーク、マックッス・タッカルビの街'],
  tongyeong: ['한려수도 바다와 케이블카, 벽화마을과 충무김밥', '闲丽水道海景、缆车、壁画村与忠武紫菜包饭', 'Hallyeo waterway views, a cable car, mural village and Chungmu gimbap', '閑麗水道の海とケーブルカー、壁画村と忠武キンパ'],
  ulsan: ["국가정원과 바다, 고래·언양불고기로 이름난 동해 산업 도시", "以国家庭园、大海、鲸鱼和彦阳烤牛肉闻名的东海岸工业城市", "East Sea industrial city of a national garden, whales and Eonyang bulgogi", "国家庭園と海、クジラと彦陽プルコギで知られる東海岸の産業都市"],
  damyang: ["대숲과 메타세쿼이아 가로수길, 떡갈비·대통밥의 남도 대나무 고장", "竹林与水杉林荫路、牛肉饼和竹筒饭的南道竹乡", "Southern bamboo town of forests, metasequoia roads, tteokgalbi and bamboo rice", "竹林とメタセコイア並木、トッカルビと竹筒ご飯の南道の竹の里"],
  gapyeong: ['북한강 섬과 정원, 닭갈비·잣으로 이름난 서울 근교 여행지', '以北汉江小岛、庭园、辣炒鸡排和松子闻名的首尔近郊', 'Riverside escape near Seoul of islands, gardens, dakgalbi and pine nuts', '北漢江の島と庭園、タッカルビと松の実で知られるソウル近郊'],
  incheon: ['개항장과 차이나타운, 짜장면과 월미도 바다로 이름난 서해 항구 도시', '以开港场、中华街、炸酱面和月尾岛海景闻名的西海港口城市', 'West Sea port city of the old open port, Chinatown, jajangmyeon and Wolmido', '開港場とチャイナタウン、ジャジャン麺と月尾島の海で知られる西海の港町']
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
  if (ap.home) {   // 집 근처 역 ↔ 여행지: 같은 도시면 시내 이동, 제주는 항공, 나머지는 KTX·기차 (시간만 어림)
    if (ap.r === r) { const L = legBetween(ap, pt, r); return Object.assign({}, L, { home: true }); }
    const last = legBetween(REGIONS[r], pt, r);
    if (REGIONS[r].fly || (ap.r && REGIONS[ap.r].fly)) return { mode: 'flight', min: 170 + last.min, km: 0, cost: 0, via: true, home: true };
    const ride = code === 'SEL' && REGIONS[r].fromSeoul ? REGIONS[r].fromSeoul : ap.r && REGIONS[ap.r] && r === 'seoul' && REGIONS[ap.r].fromSeoul ? REGIONS[ap.r].fromSeoul : Math.round((hav(ap, REGIONS[r]) * 0.6 + 25) / 5) * 5;
    return { mode: 'rail', min: ride + last.min, km: 0, cost: 0, via: true, home: true };
  }
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
  const key = S.saved.join(',') + '|' + S.trip.arr + '|' + S.trip.dep + '|' + (S.ui.r || '') + '|' + (S.ui.scope || '') + '|' + tripKind();
  if (key === _taKey) return _ta;
  const cnt = {}, rc = {};
  for (const id of S.saved) { const r = PBY[id].r, cc = REGIONS[r].cc; cnt[cc] = (cnt[cc] || 0) + 1; rc[r] = (rc[r] || 0) + 1; }
  const pick = AIRPORTS[S.trip.arr];   // 해외 여행인데 아직 도시를 안 골랐으면 고른 공항의 나라
  const cc = Object.keys(cnt).sort((a, b) => cnt[b] - cnt[a])[0] || (S.ui.r && REGIONS[S.ui.r] ? REGIONS[S.ui.r].cc : null)
    || (tripKind() === 'ov' && pick && pick.cc !== 'kr' ? pick.cc : 'kr');
  const home = cc === 'kr' && tripKind() === 'kr';   // 국내 여행: 역에서 출발
  const ok = c => AIRPORTS[c] && AIRPORTS[c].cc === cc && !!AIRPORTS[c].home === home;
  let def = home ? 'SEL' : 'ICN';
  if (cc !== 'kr') {
    const top = Object.keys(rc).filter(r => REGIONS[r].cc === cc).sort((a, b) => rc[b] - rc[a])[0] || (S.ui.r && REGIONS[S.ui.r] && REGIONS[S.ui.r].cc === cc ? S.ui.r : OV_IDS.find(r => REGIONS[r].cc === cc));
    def = REGIONS[top].air;
  }
  _taKey = key; _ta = { cc, ov: cc !== 'kr', home, arr: ok(S.trip.arr) ? S.trip.arr : def, dep: ok(S.trip.dep) ? S.trip.dep : def };
  return _ta;
}
// 여행 유형: kr 국내 여행(한국에 사는 사람) · ov 해외 여행 · visit 한국 방문(외국에서 오는 사람). 고르지 않았으면 언어로 정한다.
// 여행 유형을 바꿀 때 기본 시각: 국내 여행은 아침 8시 출발·밤 9시 도착, 비행기는 오전 도착·저녁 출국
function setKindTimes(t, k) { const H = k === 'kr'; if ((t.arrT === 9 || t.arrT === 8 || t.arrT === 10) && (t.depT === 19 || t.depT === 21)) { t.arrT = H ? 8 : 10; t.depT = H ? 21 : 19; } }
function tripKind() { return S.trip.kind || (S.lang === 'ko' ? 'kr' : 'visit'); }
// 공항·역에서 쓰는 여유 시간(시간): 입국 심사·출국 수속은 공항만
const arrBuf = () => tripAir().home ? 0 : 1, depBuf = () => tripAir().home ? 0.4 : 2.5;
function regionOfPoint(pt) { let best = 'seoul', bd = 1e9; for (const r of REGION_IDS) { const d = hav(REGIONS[r], pt); if (d < bd) { bd = d; best = r; } } return best; }

/* ---------- state & persistence ---------- */
const KEY = 'klink-v2';
const DEFAULT = () => ({
  v: 2, lang: null, seenIntro: false,
  trip: { start: '2026-11-14', end: '2026-11-17', people: 2, party: 1, budget: 1, pace: 1, interests: ['palace', 'food', 'night'], kind: null,
          arr: 'ICN', arrT: 9, dep: 'ICN', depT: 19 },
  saved: [], order: [], plan: null, stayOv: {},
  ui: { tab: 'map', lvl: 'korea', scope: 'kr', r: null, d: null, sel: null, filter: 'all', day: 0, mode3d: false }
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
function track(name, p) { try { if (typeof gtag === 'function') gtag('event', name, p || {}); } catch (e) {} try { if (typeof clarity === 'function') { clarity('event', name); clarity('set', 'klink_' + name.replace(/^klink_/, ''), 'yes'); } } catch (e) {} }   // 2026-11-25 클래리티: 행동별 녹화 필터
function toggleSave(id) {
  const i = S.saved.indexOf(id);
  if (i >= 0) S.saved.splice(i, 1); else S.saved.push(id);
  savedRegions(); persist();
  if (i < 0 && PBY[id]) track('klink_save', { region: PBY[id].r });
  return i < 0;
}
const isSaved = id => S.saved.includes(id);
function planSig() { const a = tripAir(); return JSON.stringify([S.saved.slice().sort(), S.order, S.trip.start, S.trip.end, S.trip.pace, a.arr, S.trip.arrT, a.dep, S.trip.depT, S.stayOv]); }
