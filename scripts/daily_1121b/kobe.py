# -*- coding: utf-8 -*-
"""kobe — 2026-11-21(2차) 매일 콘텐츠 (새 해외 지역: 고베, K링크 지역 id kobe, cc jp). 확인일 2026-11-21. 못 쓴 글: 없음
메모: 장소는 기존 가이드 travel-kobe.html 에 나온 곳만 넣었습니다(난킨마치·상점가·기타노 이진칸·메리켄파크·포트타워·하버랜드·롯코산·아리마 온천). 누노비키 허브원은 가이드에 없어 넣지 않았습니다.
메모: 고베규 기준은 고베비프 유통추진협의회 정관(definition) 기준. 협의회 '기준' 페이지에는 육질 등급 조건이 빠져 있고 정관에는 '육질 4 이상'이 있어 정관을 따랐습니다. 도체 중량은 암소 270~499.9kg, 거세우 300~499.9kg.
메모: 가자미도리노야카타(기타노) 운영 시간이 효고현 관광 공식은 09:00~18:00(입장 마감 17:45), 이진칸 공식은 09:00~17:00로 달라 '방문 전 확인'을 붙였습니다. 휴관일도 두 출처가 다름(효고현: 2·6월 첫째 화요일 / 이진칸 공식: 셋째 화요일) — 효고현 관광 공식을 따름.
메모: 가게 이름은 효고현 관광 공식이 직접 적은 곳만(로쇼키 — 일본 첫 부타만 판매로 소개, 모로조프·후게쓰도·유하임 — 고베 양과자 노포). 고베규 가격은 공식 출처가 없어 쓰지 않았습니다.
메모: 아카시야키는 이웃 아카시시 향토 음식(농림수산성 향토 요리 페이지, 아카시 관광협회 제공). 산노미야→아카시 이동 시간은 공식 확인 못 해 적지 않았습니다.
메모: 좌표는 대표 지점 대략값(롯코산은 롯코 가든 테라스 부근). OVD o= 값은 일정 계산용 기본값."""

OVD = r"""
C kobe jp 34.6913 135.1830 1 110 | 고베|神户|Kobe|神戸 | 항구 야경과 이진칸 거리, 고베규·난킨마치 먹거리 | Harbour night views, old foreign houses, Kobe beef and Chinatown food
A KIX 34.4320 135.2304 70 | 간사이공항|关西机场|Kansai (KIX)|関西空港
S kb_s1 34.6946 135.1955 | 산노미야|三宫|Sannomiya|三宮 | 산노미야역 · 공항 버스·기타노 걸어서 | Sannomiya Stn · airport bus, walk to Kitano
S kb_s2 34.6890 135.1860 | 모토마치|元町|Motomachi|元町 | 모토마치역 · 난킨마치·메리켄파크 걸어서 | Motomachi Stn · walk to Chinatown and Meriken Park
Z kb_z1 | 산노미야·모토마치 | Sannomiya & Motomachi
P kb_nankinmachi food 34.6880 135.1880 1 lunch o=F | 난킨마치|南京町|Nankinmachi (Chinatown)|南京町 | 부타만·중국 음식점이 모인 고베 차이나타운 | Kobe's Chinatown of pork buns and Chinese eateries
P kb_motomachi shop 34.6890 135.1840 1 o=S | 모토마치 상점가|元町商店街|Motomachi Shopping Street|元町商店街 | 난킨마치 옆 1.2km 아케이드 상점가 | 1.2 km arcade next to Chinatown
Z kb_z2 | 기타노 | Kitano
P kb_ijinkan palace 34.7012 135.1906 1.5 am o=D | 기타노 이진칸|北野异人馆|Kitano Ijinkan|北野異人館 | 언덕 위 서양식 옛 주택 거리 · 가자미도리노야카타 | Hillside street of old foreign residences
Z kb_z3 | 하버랜드 | Harborland
P kb_meriken night 34.6826 135.1867 1 eve | 메리켄파크·포트타워|美利坚公园·神户港塔|Meriken Park & Port Tower|メリケンパーク・ポートタワー | 붉은 포트타워와 BE KOBE 조형물이 있는 항구 공원 | Harbour park with the red Port Tower and BE KOBE sign
P kb_harborland shop 34.6795 135.1830 1.5 eve dinner o=S | 하버랜드|神户港湾区|Kobe Harborland|神戸ハーバーランド | 대관람차와 umie MOSAIC 항구 쇼핑 거리 | Waterfront shopping with the Mosaic Ferris wheel
Z kb_z4 | 롯코산·아리마 | Mt. Rokko & Arima
P kb_rokko night 34.7700 135.2400 2 night | 롯코산|六甲山|Mt. Rokko|六甲山 | 케이블카로 오르는 산 위 야경 전망 | Mountain night views reached by cable car
P kb_arima nature 34.7968 135.2478 3 o=D | 아리마 온천|有马温泉|Arima Onsen|有馬温泉 | 붉은 금탕·맑은 은탕 온천 마을 | Hot-spring town of golden and silver waters
"""

ARTICLES = [
 dict(
  kind="trip",
  slug="travel-kobe-food",
  region="kobe",
  places=["kb_nankinmachi", "kb_motomachi", "kb_harborland"],
  kw=("고베맛집", 4450),
  name="고베 맛집",
  title="고베 맛집 — 고베규 인증 기준·난킨마치 부타만·모토마치 상점가 먹거리 동선",
  desc="고베 맛집을 고르기 전에 알아둘 것을 정리했습니다. 고베비프 유통추진협의회 공식 기준으로 본 고베규의 조건과 확인법, 난킨마치 먹거리, 모토마치 상점가와 양과자, 아카시야키·소바메시까지 담았습니다.",
  intro="<b>고베규</b>를 제대로 고르는 법과 <b>난킨마치·모토마치 상점가</b>에서 먹는 동선을 짧게 정리했어요.",
  first="먼저 알아둘 것: '고베규'는 효고현 다지마 소 가운데 협의회 기준을 통과한 고기에만 붙는 이름이에요. 가게에서는 <b>10자리 개체 번호</b>와 노지기쿠(들국화) 인증 표시로 확인해요. 길거리 음식은 난킨마치, 디저트와 빵은 바로 옆 모토마치 상점가에서 이어서 먹으면 걷는 거리가 짧아요.",
  cards=[
   ("고베규란 (협의회 공식 기준)",
    "<p>고베비프 유통추진협의회 정관에 따르면 고베규는 '다지마규(但馬牛)' 가운데 아래 조건을 모두 갖춘 고기만 가리켜요. KOBE BEEF·고베규·고베니쿠는 같은 말이에요.</p>"
    "<ul><li>효고현 지정 농가에서 태어난 다지마 소 혈통, 암소 또는 거세 수소</li>"
    "<li>효고현 도축장에서 처리</li>"
    "<li>마블링(BMS) 6 이상, 육질 등급 4 이상, 보류(수율) 등급 A·B</li>"
    "<li>도체 중량 499.9kg 이하(암소 270kg부터, 거세우 300kg부터)</li></ul>"
    "<p>협의회는 최소 28개월, 평균 32개월 이상 키워 출하한다고 안내해요.</p>"),
   ("진짜 고베규 확인법 (가게에서)",
    "<ul><li><b>10자리 개체 번호</b>: 인증 고기마다 붙고, 협의회 사이트의 다지마규 증명 시스템에서 혈통·출생지·사육지를 조회할 수 있어요.</li>"
    "<li><b>노지기쿠 인증 도장</b>: 고베규로 인증된 고기에만 찍히는 들국화 모양 표시예요.</li>"
    "<li><b>청동 소 조각상</b>: 고베규를 사고팔 수 있도록 협의회가 지정한 가게임을 나타내요.</li></ul>"
    "<p>스테이크 외에 샤부샤부·스키야키로도 먹어요. 지정 가게 목록은 협의회 공식 사이트의 '지정 등록점' 안내에서 확인해요.</p>"),
   ("난킨마치 먹거리 (부타만·샤오롱바오)",
    "<p>난킨마치는 1868년 고베항 개항 뒤 중국에서 온 사람들이 만든 거리로, 동서 약 270m·남북 약 110m 안에 중국 음식점과 잡화점이 약 100곳 모여 있어요.</p>"
    "<ul><li>부타만(돼지고기 찐빵): 효고현 관광 공식 안내는 난킨마치의 로쇼키(老祥記)를 일본에서 처음 부타만을 판 곳으로 소개해요.</li>"
    "<li>샤오롱바오·베이징 덕·샥스핀 수프도 대표 메뉴로 안내돼요.</li></ul>"
    "<p>효고현 관광 공식 안내는 난킨마치에서 걸으면서 먹지 말라고 당부해요. 가게 앞이나 중앙 광장 쪽에서 멈춰 먹어요.</p>"),
   ("산노미야·모토마치 먹거리 동선",
    "<ol><li>JR·한신 모토마치역에서 남쪽으로 걸어서 약 5분, 난킨마치에서 점심</li>"
    "<li>바로 옆 모토마치 상점가(길이 1.2km, 가게 약 300곳, 1874년 형성)에서 양과자·빵 구경</li>"
    "<li>남쪽으로 내려가 메리켄파크를 지나 하버랜드 umie MOSAIC에서 저녁</li></ol>"
    "<p>고베는 1868년 개항 뒤 양과자와 빵이 일찍 자리 잡았어요. 효고현 관광 공식 안내는 모로조프·후게쓰도·유하임을 오래된 양과자점으로 소개해요. 동네별 볼거리 동선은 <a href='/travel-kobe.html'>고베 여행 코스</a>에 있어요.</p>"),
   ("아카시야키·소바메시 (근교 향토 음식)",
    "<ul><li><b>아카시야키</b>: 고베 서쪽 이웃 도시 아카시의 향토 음식이에요. 달걀이 많이 든 부드러운 반죽에 문어를 넣어 구운 뒤 다시마·가쓰오 국물에 찍어 먹어요. 현지에서는 '다마고야키'라고 불러요.</li>"
    "<li><b>소바메시</b>: 고베 나가타구의 소울푸드예요. 철판에서 야키소바와 밥을 함께 볶고, 1950년대 후반~1960년대 초 손님이 도시락 밥을 같이 볶아 달라고 한 데서 시작됐다고 안내돼요.</li>"
    "<li><b>미소다레 교자</b>: 붉은 된장 소스에 찍어 먹는 고베식 만두예요.</li></ul>"),
  ],
  table=(["구분", "어디서·무엇", "확인 포인트"], [
   ["고베규", "스테이크·샤부샤부·스키야키", "10자리 개체 번호·노지기쿠 도장"],
   ["난킨마치", "부타만·샤오롱바오", "걸으면서 먹지 않기"],
   ["모토마치 상점가", "양과자·빵", "난킨마치 바로 옆"],
   ["하버랜드", "umie MOSAIC 저녁", "가게별 영업시간 확인"],
   ["아카시야키", "아카시시 향토 음식", "국물에 찍어 먹기"],
  ]),
  tip="고베규를 주문할 때 메뉴나 매장에 붙은 10자리 개체 번호를 물어보면 협의회 사이트에서 바로 조회할 수 있어요. 난킨마치는 점심에 들르고, 저녁은 하버랜드 야경과 묶으면 동선이 짧아요.",
  faq=[
   ("고베규와 와규는 같은 말이에요?", "아니에요. 고베규는 효고현 다지마 소 가운데 BMS 6 이상 등 협의회 기준을 통과한 고기만 가리켜요."),
   ("진짜 고베규인지 어떻게 알아요?", "10자리 개체 번호를 협의회의 다지마규 증명 시스템에서 조회하고, 노지기쿠 인증 도장과 지정점의 청동 소 조각상을 확인해요."),
   ("난킨마치에서 꼭 먹을 것은요?", "효고현 관광 공식 안내는 부타만·샤오롱바오·베이징 덕·샥스핀 수프를 대표 메뉴로 꼽아요."),
   ("난킨마치는 어떻게 가요?", "JR·한신 모토마치역에서 걸어서 약 5분, 지하철 가이간선 규쿄류치·다이마루마에역에서 약 2분이에요."),
   ("아카시야키는 고베에서도 먹어요?", "아카시야키는 이웃 도시 아카시의 향토 음식이에요. 고베 시내 판매 가게는 방문 전 확인하세요."),
  ],
  sources=[
   ("고베비프 유통추진협의회 — Definition of Kobe Beef (정관) (확인 2026.11.21)", "https://kobe-niku.jp/en/contents/about/definition.html"),
   ("고베비프 유통추진협의회 — Criteria (확인 2026.11.21)", "https://kobe-niku.jp/en/contents/about/criteria.html"),
   ("고베비프 유통추진협의회 — FAQ (확인 2026.11.21)", "https://kobe-niku.jp/en/contents/faq"),
   ("효고현 관광 공식 HYOGO! — Nankinmachi (확인 2026.11.21)", "https://www.hyogo-tourism.jp/world/spot/detail_1021.html"),
   ("난킨마치 상점가 진흥조합 — 가이드북 (확인 2026.11.21)", "https://www.nankinmachi.or.jp/common/img/guidemap/guide_book.pdf"),
   ("고베시 관광 공식 Feel KOBE — Motomachi shopping street (확인 2026.11.21)", "https://plus.feel-kobe.jp/en/facilities/detail/?id=5818"),
   ("효고현 관광 공식 HYOGO! — Gourmet (확인 2026.11.21)", "https://www.hyogo-tourism.jp/world/feature/gourmet"),
   ("효고현 관광 공식 HYOGO! — The Kobe area (확인 2026.11.21)", "https://www.hyogo-tourism.jp/world/feature/detail_22.html"),
   ("농림수산성 향토 요리 — Akashiyaki (아카시 관광협회 제공) (확인 2026.11.21)", "https://local-cuisine.maff.go.jp/en/recipe/775/"),
   ("일본정부관광국 JNTO — Nankinmachi (확인 2026.11.21)", "https://www.japan.travel/en/spot/1037/"),
  ],
 ),
]

# 명소 안내 (K링크 장소 상세 화면). 공식 출처로 확인한 것만. 확인 못 한 칸은 '방문 전 확인'.
SPOTS = {
 "kb_nankinmachi": dict(
   one="1868년 고베항 개항 뒤 생긴 일본 3대 차이나타운이에요. 부타만·샤오롱바오를 먹기 좋은 곳이에요.",
   see=[("장안문", "동쪽 입구의 중국식 문, 1985년 완공"), ("난킨마치 광장", "거리 한가운데 사진 명소"), ("부타만 가게", "로쇼키는 일본 첫 부타만 판매점으로 소개")],
   facts=dict(hours="가게마다 다름, 방문 전 확인", fee="무료", stay="약 1시간", when="점심", access="JR·한신 모토마치역에서 걸어서 약 5분, 지하철 규쿄류치·다이마루마에역에서 약 2분"),
   tips=["효고현 관광 공식 안내는 거리에서 걸으며 먹지 말라고 당부해요.", "음력 설 춘절제·중추절·12월 랜턴 행사 때는 매우 붐벼요.", "주차장이 없어 전철로 가는 편이 좋아요."],
   src=[("효고현 관광 공식 HYOGO! — Nankinmachi", "https://www.hyogo-tourism.jp/world/spot/detail_1021.html"), ("난킨마치 상점가 진흥조합 — 가이드북", "https://www.nankinmachi.or.jp/common/img/guidemap/guide_book.pdf")],
   checked="2026-11-21", photo=None),
 "kb_motomachi": dict(
   one="1874년에 생긴 길이 1.2km 아케이드 상점가예요. 가게가 약 300곳이고 난킨마치 바로 옆이에요.",
   see=[("라 루체 유리 게이트", "상점가 입구의 유리 아치"), ("100년 넘은 노포", "오래된 가게와 새 가게가 섞여 있어요"), ("양과자·빵 가게", "개항 뒤 자리 잡은 고베 양과자")],
   facts=dict(hours="가게마다 다름, 방문 전 확인", fee="무료", stay="약 1시간", when="낮", access="JR·한신 모토마치역 남쪽, 난킨마치 바로 옆"),
   tips=["아케이드라 비 오는 날에도 걷기 좋아요.", "난킨마치 점심 뒤 이어서 걷고 남쪽 메리켄파크로 내려가면 동선이 짧아요."],
   src=[("고베시 관광 공식 Feel KOBE — Motomachi shopping street", "https://plus.feel-kobe.jp/en/facilities/detail/?id=5818")],
   checked="2026-11-21", photo=None),
 "kb_ijinkan": dict(
   one="개항 뒤 외국인들이 살던 서양식 옛 주택이 모인 언덕 동네예요. 붉은 벽돌의 가자미도리노야카타가 상징이에요.",
   see=[("가자미도리노야카타", "1909년 독일 무역상 주택, 국가 중요문화재"), ("독일식 벽난로·스테인드글라스", "응접실·식당 내부 장식"), ("언덕 위 전망", "정원에서 고베 시내가 보여요")],
   facts=dict(hours="가자미도리노야카타 09:00~18:00 (입장 마감 17:45, 방문 전 확인)", fee="가자미도리노야카타 성인 500엔, 고교생 이하 무료 (모에기노야카타 공통권 650엔)", stay="약 1시간 30분", when="오전", access="산노미야역·신고베역에서 걸어서 약 15분"),
   tips=["가자미도리노야카타는 2월·6월 첫째 화요일 휴관이에요(공휴일이면 다음 날).", "비탈과 계단이 많아 편한 신발이 좋아요.", "주차장이 없어 걸어서 가요."],
   src=[("효고현 관광 공식 HYOGO! — Weathercock House", "https://www.hyogo-tourism.jp/world/spot/detail_1024.html"), ("고베 기타노 이진칸 공식 — Weathercock House", "https://kobeijinkan.com/en/?p=57")],
   checked="2026-11-21", photo=None),
 "kb_meriken": dict(
   one="붉은 장구 모양 포트타워와 BE KOBE 조형물이 있는 항구 공원이에요. 해 진 뒤 조명이 예뻐요.",
   see=[("고베 포트타워", "전망층·옥상 데크에서 항구 전망"), ("BE KOBE 조형물", "밤에 조명이 켜지는 사진 명소"), ("고베항 지진 메모리얼 파크", "한신·아와지 대지진 피해 보존")],
   facts=dict(hours="포트타워 09:00~23:00 (입장 마감 22:30), 연중무휴(점검일 제외)", fee="포트타워 성인 1,200엔 (전망층+옥상), 전망층만 1,000엔 / 공원 무료", stay="약 1시간", when="해 질 무렵~저녁", access="JR·한신 모토마치역에서 걸어서 약 10분, 지하철 미나토모토마치역에서 약 8분"),
   tips=["포트타워 옥상 데크는 비·강풍 때 예고 없이 닫힐 수 있어요.", "하버랜드와 산책로로 이어져 야경을 연달아 보기 좋아요."],
   src=[("고베 포트타워 공식 — Tickets and Fees", "https://www.kobe-port-tower.com/en/?p=188"), ("고베 포트타워 공식 — Opening Hours", "https://www.kobe-port-tower.com/en"), ("효고현 관광 공식 HYOGO! — Meriken Park", "https://www.hyogo-tourism.jp/world/spot/detail_1003.html")],
   checked="2026-11-21", photo=None),
 "kb_harborland": dict(
   one="대관람차와 umie MOSAIC 쇼핑가가 있는 항구 거리예요. 바다에 비치는 야경이 알려져 있어요.",
   see=[("umie MOSAIC", "바닷가 카페·식당·기념품 가게"), ("모자이크 대관람차", "하버랜드의 상징, 밤 조명"), ("고베 호빵맨 어린이 박물관", "가족 여행객용 시설")],
   facts=dict(hours="가게마다 다름, 방문 전 확인", fee="입장 무료 (시설별 요금 별도)", stay="약 1시간 30분", when="저녁", access="JR 고베역에서 걸어서 약 10분, 지하철 가이간선 하버랜드역"),
   tips=["저녁을 umie MOSAIC에서 먹고 바닷가 산책로로 메리켄파크 야경까지 이어 걸어요.", "대관람차·크루즈 운행 시간은 공식 사이트에서 확인해요."],
   src=[("효고현 관광 공식 HYOGO! — Kobe Harborland", "https://www.hyogo-tourism.jp/world/spot/detail_1007.html")],
   checked="2026-11-21", photo=None),
 "kb_rokko": dict(
   one="고베 시내 뒤쪽 산으로, 롯코 케이블카를 타고 올라 바다와 시가지 야경을 봐요.",
   see=[("롯코 케이블카", "약 1.7km, 약 10분, 고도차 493.3m"), ("롯코 가든 테라스", "전망 포인트·식당·상점이 모인 산 위 시설"), ("롯코 아리마 로프웨이", "아리마 온천까지 약 12분")],
   facts=dict(hours="케이블카 07:10~21:10 (약 20분 간격) / 가든 테라스 10:00~21:00 (입장 마감 20:30), 시기마다 다름", fee="케이블카 성인 편도 600엔, 왕복 1,100엔", stay="약 2시간", when="해 진 뒤", access="JR 롯코미치·한큐 롯코역에서 시영 버스 16번으로 롯코 케이블시타역"),
   tips=["롯코 가든 테라스는 목요일 휴무가 있어요(시기·가게마다 다름).", "케이블카는 악천후에 갑자기 멈출 수 있어 출발 전 운행 정보를 확인해요.", "아리마 온천과 로프웨이로 이어 하루 코스로 묶어도 돼요."],
   src=[("효고현 관광 공식 HYOGO! — Rokko Cable Car", "https://www.hyogo-tourism.jp/world/note/17"), ("롯코산 관광 공식 — Access", "https://www.rokkosan.com/top/access/?lang=en")],
   checked="2026-11-21", photo=None),
 "kb_arima": dict(
   one="롯코산 북쪽의 온천 마을이에요. 붉은 금탕과 맑은 은탕 두 가지 온천을 맛볼 수 있어요.",
   see=[("킨노유(금탕)", "철분이 섞인 붉은 갈색 온천"), ("긴노유(은탕)", "맑은 온천"), ("온천 마을 골목", "공중탕 사이 언덕길")],
   facts=dict(hours="킨노유(금탕) 08:00~22:00 (입장 마감 21:30)", fee="킨노유 성인 800엔 (평일 650엔), 금탕·은탕 2탕권 1,200엔", stay="약 3시간", when="낮", access="산노미야에서 버스·전철로 약 30~40분, 롯코산에서 로프웨이 약 12분"),
   tips=["킨노유는 매월 둘째·넷째 화요일과 1월 1일 휴관이에요(공휴일이면 다음 날).", "수건은 직접 챙기거나 사야 해요.", "두 곳 다 가려면 2탕권이 따로 사는 것보다 싸요."],
   src=[("아리마 온천 킨노유·긴노유 공식 — Opening hours", "https://arimaspa-kingin.jp/en-01.htm"), ("효고현 관광 공식 HYOGO! — The Kobe area", "https://www.hyogo-tourism.jp/world/feature/detail_22.html")],
   checked="2026-11-21", photo=None),
}

COORDS = {}
