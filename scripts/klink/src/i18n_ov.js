'use strict';
/* 해외여행 확장 문구 (2026-11-12). i18n.js 뒤에 붙는다. */
Object.assign(I18N.ko, {
  scopeKr: '국내', scopeKrSub: '3D 거리', scopeOv: '해외', scopeOvSub: n => `${n}개 도시`, citiesN: n => `${n}개 도시`,
  whereLead: '지역을 고르면 지도가 펼쳐져요. 국내는 구역을 누르면 3D 거리로 들어가고, 해외는 도시 지도에서 가고 싶은 곳을 저장해요.',
  whereLeadOv: '도시를 고르면 지도가 펼쳐져요. 가고 싶은 곳을 ♥로 저장하면 날짜별 동선과 숙소 위치를 짜 드려요.',
  ovNote: '해외 장소는 어라운드툴 여행 가이드에 나온 곳이에요. 위치는 대략적이고 운영 시간·요금은 현지에서 확인해 주세요. 해외 3D 거리는 준비 중이에요. 지도 경계 © OpenStreetMap 기여자.',
  regionLeadOv: '핀이나 구역을 눌러 가고 싶은 곳을 저장하세요.', soon3dShort: '3D 거리 준비 중', soon3d: '해외 3D 거리는 준비 중이에요. 지금은 지도로 볼 수 있어요.',
  far: '근교', localCheck: '현지 확인', openMap: '구글 지도에서 위치 보기', estNote: '위치는 대략적이에요. 운영 시간·요금·휴무일은 방문 전에 공식 안내를 확인해 주세요.',
  tripLeadOv: c => `${c} 여행이에요. 현지 공항 도착·출국 시각을 알려 주시면 그 시간에 맞춰 일정을 짜요.`,
  tab_prep: '준비', mRailOv: '기차·버스', mFlightOv: '항공편', mAirportOv: '공항 이동', mCarOv: '차량·투어',
  priceLocal: '숙소 요금은 예약 사이트에서 확인하세요', daySumOv: (n, mv) => `${n}곳 · 이동 ${mv}`,
  planNoteOv: '이동 시간은 거리로 계산한 예상치예요. 해외 장소의 운영 시간은 일반적인 기준으로 잡았으니 방문 전에 공식 안내를 확인해 주세요. 입장료·교통비는 현지 요금이라 합계에 넣지 않았어요.',
  toPrep: '여행 준비 보기', prepTitle: '여행 준비', prepLead: '떠나기 전에 필요한 계산과 확인할 것을 어라운드툴에서 모았어요.',
  prepTrip: '여행 가이드', prepTools: '계산기', prepGuides: '준비 가이드',
  introP: '지도를 둘러보며 가고 싶은 곳을 저장하세요. 국내는 3D 거리에서, 해외는 도시 지도에서 고르면 거리와 운영 시간을 따져 날짜별 동선과 숙소 위치를 추천해 드려요.',
  introStops: ['서울', '부산', '도쿄', '다낭'], introSteps: ['국내·해외에서 여행지 고르기', '지도에서 관광지·맛집 저장', '날짜별 동선과 숙소 위치 추천', '여행 준비 계산기·가이드 연결'],
  atBy: 'K링크의 여행·맛집·준비 정보는 어라운드툴(aroundtool.com)의 여행 가이드, 맛집 기록, 계산기와 연결돼요. 새 글이 올라오면 여기에도 이어져요.'
});
Object.assign(I18N.zh, {
  scopeKr: '韩国', scopeKrSub: '3D 街区', scopeOv: '海外', scopeOvSub: n => `${n} 个城市`, citiesN: n => `${n} 个城市`,
  whereLeadOv: '选择城市后会展开地图。用 ♥ 收藏想去的地方，我们会为你安排每天的路线和住宿区域。',
  ovNote: '海外地点来自 AroundTool 的旅行指南。位置为大致位置，营业时间和费用请在当地确认。海外 3D 街区正在准备中。地图边界 © OpenStreetMap 贡献者。',
  regionLeadOv: '点击图钉或区域，收藏想去的地方。', soon3dShort: '3D 街区准备中', soon3d: '海外 3D 街区正在准备中，目前可用地图查看。',
  far: '近郊', localCheck: '请在当地确认', openMap: '在 Google 地图中查看位置', estNote: '位置为大致位置。营业时间、费用和休息日请在出发前查看官方信息。',
  tripLeadOv: c => `${c}旅行。请告诉我们当地机场的到达和离境时间，我们会据此安排行程。`,
  tab_prep: '准备', mRailOv: '火车·巴士', mFlightOv: '航班', mAirportOv: '机场交通', mCarOv: '包车·跟团',
  priceLocal: '住宿价格请在预订网站确认', daySumOv: (n, mv) => `${n} 处 · 交通 ${mv}`,
  planNoteOv: '交通时间按距离估算。海外地点的营业时间按一般情况计算，请在出发前查看官方信息。门票和交通费为当地价格，未计入合计。',
  toPrep: '查看旅行准备', prepTitle: '旅行准备', prepLead: '出发前需要的计算和注意事项，来自 AroundTool。',
  prepTrip: '旅行指南', prepTools: '计算器', prepGuides: '准备指南',
  introP: '浏览地图，收藏想去的地方。韩国可以走进 3D 街区，海外在城市地图上选择，我们会根据距离和营业时间推荐每天的路线和住宿区域。',
  introStops: ['首尔', '釜山', '东京', '岘港'], introSteps: ['选择韩国或海外目的地', '在地图上收藏景点和美食', '推荐每日路线和住宿区域', '连接旅行准备计算器和指南']
});
Object.assign(I18N.en, {
  scopeKr: 'Korea', scopeKrSub: '3D streets', scopeOv: 'Overseas', scopeOvSub: n => `${n} cities`, citiesN: n => `${n} ${n === 1 ? 'city' : 'cities'}`,
  whereLeadOv: 'Pick a city to open its map. Save the places you like with ♥ and we will plan each day and suggest where to stay.',
  ovNote: 'Overseas places come from AroundTool travel guides. Pins are approximate; check hours and prices locally. 3D streets for overseas cities are coming soon. Map outlines © OpenStreetMap contributors.',
  regionLeadOv: 'Tap a pin or an area to save places you want to visit.', soon3dShort: '3D coming soon', soon3d: '3D streets for overseas cities are coming soon. Use the map for now.',
  far: 'Day trip', localCheck: 'Check locally', openMap: 'Open location in Google Maps', estNote: 'The pin is approximate. Please check official information for hours, prices and closing days before you go.',
  tripLeadOv: c => `Trip to ${c}. Tell us when you land at and leave from the local airport and we will plan around it.`,
  tab_prep: 'Prep', mRailOv: 'Train / bus', mFlightOv: 'Flight', mAirportOv: 'Airport transfer', mCarOv: 'Car / tour',
  priceLocal: 'Check room rates on a booking site', daySumOv: (n, mv) => `${n} places · ${mv} travel`,
  planNoteOv: 'Travel times are estimates based on distance. Opening hours for overseas places use typical values, so check official information before you go. Admission and transport are local prices and are not included in the total.',
  toPrep: 'See trip prep', prepTitle: 'Trip prep', prepLead: 'Calculators and checklists for before you leave, from AroundTool.',
  prepTrip: 'Travel guides', prepTools: 'Calculators', prepGuides: 'Prep guides',
  introP: 'Browse the map and save the places you like — 3D streets in Korea, city maps overseas. We check distances and opening hours to suggest the best route for each day and where to stay.',
  introStops: ['Seoul', 'Busan', 'Tokyo', 'Da Nang'], introSteps: ['Pick a destination in Korea or overseas', 'Save sights and food on the map', 'Get daily routes and where to stay', 'Trip-prep calculators and guides']
});
Object.assign(I18N.ja, {
  scopeKr: '韓国', scopeKrSub: '3Dストリート', scopeOv: '海外', scopeOvSub: n => `${n}都市`, citiesN: n => `${n}都市`,
  whereLeadOv: '都市を選ぶと地図が開きます。行きたい場所を♥で保存すると、日ごとのルートと宿泊エリアを提案します。',
  ovNote: '海外のスポットはAroundToolの旅行ガイドに掲載された場所です。位置はおおよそで、営業時間・料金は現地でご確認ください。海外の3Dストリートは準備中です。地図の境界 © OpenStreetMap contributors。',
  regionLeadOv: 'ピンやエリアをタップして、行きたい場所を保存してください。', soon3dShort: '3D準備中', soon3d: '海外の3Dストリートは準備中です。今は地図でご覧ください。',
  far: '近郊', localCheck: '現地で確認', openMap: 'Googleマップで場所を見る', estNote: '位置はおおよそです。営業時間・料金・定休日は出発前に公式情報をご確認ください。',
  tripLeadOv: c => `${c}旅行です。現地空港の到着・出国時刻を教えていただければ、それに合わせて日程を組みます。`,
  tab_prep: '準備', mRailOv: '電車・バス', mFlightOv: '航空便', mAirportOv: '空港アクセス', mCarOv: '車・ツアー',
  priceLocal: '宿泊料金は予約サイトでご確認ください', daySumOv: (n, mv) => `${n}か所 · 移動 ${mv}`,
  planNoteOv: '移動時間は距離から計算した目安です。海外スポットの営業時間は一般的な基準で計算しているため、出発前に公式情報をご確認ください。入場料・交通費は現地料金のため合計に含めていません。',
  toPrep: '旅の準備を見る', prepTitle: '旅の準備', prepLead: '出発前に必要な計算と確認事項をAroundToolからまとめました。',
  prepTrip: '旅行ガイド', prepTools: '計算ツール', prepGuides: '準備ガイド',
  introP: '地図を見ながら行きたい場所を保存しましょう。韓国は3Dストリート、海外は都市の地図で選ぶと、距離と営業時間から日ごとのルートと宿泊エリアを提案します。',
  introStops: ['ソウル', '釜山', '東京', 'ダナン'], introSteps: ['韓国・海外から行き先を選ぶ', '地図で観光地・グルメを保存', '日ごとのルートと宿泊エリアを提案', '旅の準備の計算ツール・ガイド']
});
/* 장소 상세 개편 (2026-11-12) */
Object.assign(I18N.ko, {
  fFee: '요금', fWhen: '가기 좋은 때', seeTitle: '이곳의 볼거리', tipsTitle: '알아 두면 좋아요', courseTitle: '어라운드툴 코스에서는', areaLbl: '권역',
  movesTitle: '이동 시간', faqTitle: '자주 묻는 질문', nearTitle: '가까운 곳', photoBy: '사진', spotFrom: '어라운드툴 명소 안내',
  checkedOn: d => `${d} 확인`, checkBefore: '운영 시간·요금은 바뀔 수 있어요', guideMore: '여행 가이드에서 자세히 보기',
  spotSoonH: '명소 안내 준비 중', spotSoon: '어라운드툴이 이곳의 운영 시간·요금·볼거리를 공식 안내로 확인해 정리하고 있어요.'
});
Object.assign(I18N.zh, {
  fFee: '费用', fWhen: '推荐时段', seeTitle: '看点', tipsTitle: '小贴士', courseTitle: 'AroundTool 路线中', areaLbl: '区域',
  movesTitle: '交通时间', faqTitle: '常见问题', nearTitle: '附近', photoBy: '照片', spotFrom: 'AroundTool 景点介绍',
  checkedOn: d => `${d} 核实`, checkBefore: '营业时间和费用可能变动', guideMore: '在旅行指南中查看详情',
  spotSoonH: '景点介绍准备中', spotSoon: 'AroundTool 正在根据官方信息整理这里的营业时间、费用和看点。'
});
Object.assign(I18N.en, {
  fFee: 'Price', fWhen: 'Best time', seeTitle: 'Highlights', tipsTitle: 'Good to know', courseTitle: 'In AroundTool routes', areaLbl: 'Area',
  movesTitle: 'Travel times', faqTitle: 'FAQ', nearTitle: 'Nearby', photoBy: 'Photo', spotFrom: 'AroundTool spot guide',
  checkedOn: d => `Checked ${d}`, checkBefore: 'Hours and prices may change', guideMore: 'Read more in the travel guide',
  spotSoonH: 'Spot guide coming soon', spotSoon: 'AroundTool is checking official sources for this place’s hours, prices and highlights.'
});
Object.assign(I18N.ja, {
  fFee: '料金', fWhen: 'おすすめの時間', seeTitle: '見どころ', tipsTitle: '知っておきたいこと', courseTitle: 'AroundToolのコースでは', areaLbl: 'エリア',
  movesTitle: '移動時間', faqTitle: 'よくある質問', nearTitle: '近くのスポット', photoBy: '写真', spotFrom: 'AroundTool スポット案内',
  checkedOn: d => `${d} 確認`, checkBefore: '営業時間・料金は変わることがあります', guideMore: '旅行ガイドで詳しく見る',
  spotSoonH: 'スポット案内は準備中', spotSoon: 'AroundToolがこの場所の営業時間・料金・見どころを公式情報で確認してまとめています。'
});
/* 2026-11-12 K링크 정리: 예약·결제 대행 대신 어라운드툴 콘텐츠(추천 코스·맛집 기록·준비 계산기)를 잇는다 */
Object.assign(I18N.ko, {
  planNote: '이동 시간은 거리로 계산한 예상치예요. 운영 시간·요금·휴무일은 방문 전에 공식 안내로 확인하세요.',
  slotAm: '오전', slotPm: '오후', slotEve: '저녁', totalPlaces: '일정에 넣은 곳',
  coursesTitle: '어라운드툴 추천 코스', coursesSub: '여행 가이드의 코스를 그대로 담아요', courseLoad: '이 코스 담기', courseOpen: '가이드 보기',
  courseLoaded: n => `코스의 ${n}곳을 담고 일정을 짰어요`, courseStops: n => `${n}곳`,
  tripsTitle: '이 장소가 나오는 여행 글', foodTitle: '어라운드툴 맛집·먹거리 기록', foodSub: '이 근처를 다룬 글'
});
Object.assign(I18N.zh, {
  planNote: '交通时间是按距离估算的。营业时间、费用和休息日请在出发前查看官方信息。',
  slotAm: '上午', slotPm: '下午', slotEve: '晚上', totalPlaces: '行程中的地点',
  coursesTitle: 'AroundTool 推荐路线', coursesSub: '直接载入旅行指南里的路线', courseLoad: '载入这条路线', courseOpen: '查看指南',
  courseLoaded: n => `已载入路线中的 ${n} 个地点并生成行程`, courseStops: n => `${n} 处`,
  tripsTitle: '提到这里的旅行文章', foodTitle: 'AroundTool 美食记录', foodSub: '介绍这一带的文章'
});
Object.assign(I18N.en, {
  planNote: 'Travel times are estimates based on distance. Check official information for hours, prices and closing days before you go.',
  slotAm: 'Morning', slotPm: 'Afternoon', slotEve: 'Evening', totalPlaces: 'Places in plan',
  coursesTitle: 'AroundTool routes', coursesSub: 'Load a route from our travel guides', courseLoad: 'Use this route', courseOpen: 'Read guide',
  courseLoaded: n => `Added ${n} places from the route and built your plan`, courseStops: n => `${n} stops`,
  tripsTitle: 'Also in these travel guides', foodTitle: 'AroundTool food notes', foodSub: 'Articles about this area'
});
Object.assign(I18N.ja, {
  planNote: '移動時間は距離からの目安です。営業時間・料金・定休日は出発前に公式情報でご確認ください。',
  slotAm: '午前', slotPm: '午後', slotEve: '夜', totalPlaces: '日程に入れた場所',
  coursesTitle: 'AroundTool おすすめコース', coursesSub: '旅行ガイドのコースをそのまま入れます', courseLoad: 'このコースを入れる', courseOpen: 'ガイドを見る',
  courseLoaded: n => `コースの${n}か所を入れて日程を作りました`, courseStops: n => `${n}か所`,
  tripsTitle: 'この場所が出てくる旅行記事', foodTitle: 'AroundTool グルメ記録', foodSub: 'この周辺を扱った記事'
});
