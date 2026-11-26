# -*- coding: utf-8 -*-
"""2026-11-27 명소 안내 채우기 (코타키나발루 1·발리 4·푸껫 2·홍콩 5·마카오 2·상하이 1 = 15곳). 확인일 2026-11-27. 못 쓴 곳: 없음
메모: 스타페리 요금은 정부 발표(2023/4/3 시행) 성인 상한 평일 HK$5·주말·공휴일 HK$6.5 기준. 2027/1/25부터 평일 HK$6·주말 HK$8.3으로
      오른다는 보도(China Daily HK, 홍콩 정부 보도자료 인용)가 있어 '방문 전 확인'을 붙였어요. 위층·아래층 금액 차이는 공식 시간표(2017년판)에만 있어 숫자는 뺐어요.
메모: 몽콕 야시장(여인가·템플 스트리트) 운영 시간은 홍콩관광청에 숫자가 없어 '오후~자정 무렵(가게마다 다름) · 방문 전 확인'으로 썼어요.
메모: 빅부다 개방 시간·포린사 정보는 포린사 공식 사이트(plm.org.hk)를 열지 못해 '방문 전 확인'. 높이 34m·계단 268개는 홍콩관광청·옹핑360 공식 기준.
메모: 태국관광청 개별 명소 페이지(까론 해변·팡아만·제임스 본드 섬)가 열리지 않아 푸껫 주 페이지·팡아 주 페이지·TAT 뉴스룸으로 썼어요.
      팡아만 국립공원 입장료·운영 시간, 제임스 본드 섬 세부는 확인 못 해 넣지 않았어요(방문 전 확인). 일부 섬 8/1~9/30 휴장은 2024~2025 국립공원 계절 휴장표 기준.
메모: 켈링킹 해변 입장료(누사페니다 관광 요금)는 공식 수치를 못 찾아 '방문 전 확인'. 우붓 시장·짐바란·스미냑 운영 시간·요금도 공식 수치 없음.
메모: 마카오 코타이는 마카오관광청 페이지에 리조트별 상세가 없어 베네시안·스튜디오시티 공식 사이트, 마카오 경전철 공식 사이트로 썼어요.
메모: 난징루 지하철역·길이는 상하이 공식 페이지에 없어 넣지 않았어요."""
SPOTS = {
 "kk_kinabalu": dict(
   one="코타키나발루에서 약 92km 떨어진 키나발루산 기슭의 국립공원이에요. 해발 약 1,520m 공원 본부 주변에서 식물원과 숲길을 걸어요.",
   see=[("키나발루 식물원", "본부 옆 산지 식물을 모아 둔 정원, 해설 산책 있음"), ("공원 숲길 산책", "본부에서 시작하는 숲길, 11시 해설 산책"), ("포링 온천", "숲길과 온천탕·물놀이장이 있는 공원 안 다른 구역")],
   facts=dict(hours="8:00~17:00, 매일 (식물원 마지막 입장 15:00)", fee="외국인 보전료 18세 이상 RM 50, 17세 이하 RM 25 / 식물원 별도 RM 5·RM 3", stay="약 3~4시간", when="오전 (식물원 해설 9:00·12:00·15:00)", access="코타키나발루에서 동해안 고속도로로 약 92km, 차로 약 2시간"),
   tips=["식물원은 9:00·12:00·15:00 해설 산책에 맞춰 들어가면 꽃과 식물 설명을 함께 들을 수 있어요.", "본부가 해발 약 1,520m라 시내보다 서늘하니 얇은 겉옷과 비옷을 챙겨요.", "포링의 캐노피 워크웨이는 임시 휴장 중이라 포링에 가면 온천과 숲길 위주로 일정을 짜요."],
   src=[("Sabah Parks — Kinabalu Park (확인 2026.11.27)", "https://www.sabahparks.org.my/kinabalu-park")],
   checked="2026-11-27", photo=None),
 "bl_ubudmarket": dict(
   one="우붓 중심 잘란 라야 우붓 35번지에 있는 공예품 시장이에요. 조각상·연·손으로 짠 가방·라탄 바구니와 모자를 팔아요.",
   see=[("수공예품 가게", "목조각, 연, 손으로 짠 가방, 라탄 바구니·모자"), ("우붓 왕궁(푸리 사렌)", "시장 맞은편 왕실 거처, 일부 구역 공개"), ("왕궁 저녁 무용 공연", "왕궁 마당에서 매일 저녁 열리는 발리 전통 무용")],
   facts=dict(hours="방문 전 확인", fee="입장 무료", stay="약 1시간", when="이른 아침 또는 늦은 오후", access="우붓 중심 Jl. Raya Ubud No.35, 우붓 왕궁 맞은편"),
   tips=["처음 부른 값에 바로 사지 말고 몇 곳을 둘러본 뒤 흥정해요.", "한낮을 피해 아침 일찍이나 늦은 오후에 가면 덜 붐벼요.", "저녁에 왕궁 마당에서 전통 무용을 보려면 시장 구경을 늦은 오후로 잡아 바로 이어 가요."],
   src=[("인도네시아 관광부 — 7 Top Places to Go Shopping in Bali (확인 2026.11.27)", "https://www.indonesia.travel/us/en/destination/bali-nusa-tenggara/bali/7-top-places-to-go-shopping-in-bali"), ("인도네시아 관광부 — Istana Ubud (확인 2026.11.27)", "https://www.indonesia.travel/jp/en/destination/bali-nusa-tenggara/bali/istana-ubud")],
   checked="2026-11-27", photo=None),
 "bl_jimbaran": dict(
   one="발리 남쪽 짐바란만을 따라 약 4km 이어진 해변이에요. 산호초가 막아 물결이 잔잔하고, 해 질 녘 모래 위 해산물 저녁으로 알려져 있어요.",
   see=[("해 질 녘 노을", "모래사장 테이블에서 보는 바다 노을"), ("해변 해산물 구이", "그날 잡은 도미·조개·게·랍스터·오징어를 골라 굽는 저녁"), ("비행기 이착륙 풍경", "가까운 응우라라이 공항을 오가는 비행기")],
   facts=dict(hours="상시", fee="입장 무료 (식당 이용은 별도)", stay="약 1~2시간", when="해 질 녘 (17:30~18:30 무렵)", access="응우라라이 국제공항에서 차로 약 15~30분, 스미냑·사누르에서 약 20분"),
   tips=["노을이 17:30~18:30 무렵이라 17시 전후에 도착해 해변 자리를 먼저 잡아요.", "해산물은 고른 재료마다 값이 달라지니 주문 전에 무게와 값을 먼저 확인해요.", "공항에서 가까워 도착 첫날 저녁이나 출국 전날 저녁에 넣으면 이동이 짧아요."],
   src=[("인도네시아 관광부 — Jimbaran (확인 2026.11.27)", "https://www.indonesia.travel/au-en/destination/bali-nusa-tenggara/bali/jimbaran"), ("인도네시아 관광부 — Romantic Jimbaran Beach (확인 2026.11.27)", "https://www.indonesia.travel/au-en/destination/bali-nusa-tenggara/bali/bali---romantic-jimbaran-beach"), ("인도네시아 관광부 — 발리 노을 해변 (확인 2026.11.27)", "https://www.indonesia.travel/jp/en/travel-ideas/marine/pantai-bali")],
   checked="2026-11-27", photo=None),
 "bl_seminyak": dict(
   one="쿠타·르기안 바로 북쪽, 더블식스 거리부터 페티텡겟 사원까지 이어지는 해변이에요. 파도가 좋아 서핑을 많이 하고 해변 클럽과 노을로 알려져 있어요.",
   see=[("스미냑·페티텡겟 노을", "쿠타보다 한적한 해변에서 보는 노을"), ("해변 클럽·식당", "바다를 보며 쉬는 비치 클럽과 해변 식당"), ("잘란 락스마나 거리", "작은 부티크와 디자이너 가게가 모인 쇼핑 거리")],
   facts=dict(hours="상시", fee="입장 무료 (비치 클럽·선베드는 별도)", stay="약 1~2시간", when="해 질 녘 (17:30~18:30 무렵)", access="덴파사르에서 선셋 로드로 약 30~40분, 오토바이·앱 택시"),
   tips=["파도가 세서 서핑하기 좋은 해변이라 수영은 얕은 곳에서만 하고 깃발 안내를 따라요.", "노을 전 잘란 락스마나에서 가게를 둘러보고 해변으로 걸어 나가면 동선이 이어져요.", "발리는 외국인 관광세 Rp 150,000을 한 번 내야 하니 출발 전에 Love Bali에서 카드로 미리 내 둬요."],
   src=[("인도네시아 관광부 — Seminyak (확인 2026.11.27)", "https://www.indonesia.travel/au-en/destination/bali-nusa-tenggara/bali/seminyak-the-truly-best-experiences-on-the-enchanting-island-of-bali"), ("인도네시아 관광부 — 발리 노을 해변 (확인 2026.11.27)", "https://www.indonesia.travel/jp/en/travel-ideas/marine/pantai-bali"), ("발리 주정부 Love Bali — FAQ (확인 2026.11.27)", "https://lovebali.baliprov.go.id/faq")],
   checked="2026-11-27", photo=None),
 "bl_kelingking": dict(
   one="누사페니다섬 남서쪽 붕아메카르 마을의 절벽 해변이에요. 바다로 뻗은 절벽이 입 벌린 티라노사우루스를 닮아 유명해요.",
   see=[("티렉스 절벽 전망", "바로 옆 전망 지점에서 보는 공룡 모양 절벽"), ("절벽 아래 해변", "가파르고 위험한 내리막을 내려가야 닿는 흰 모래 해변"), ("브로큰 비치", "북서쪽 약 3km, 바위 아치와 옥빛 웅덩이")],
   facts=dict(hours="방문 전 확인", fee="방문 전 확인 (누사페니다 관광 요금)", stay="약 반나절~하루 (섬 이동 포함)", when="건기(4~10월) 오전", access="사누르·쿠삼바·파당바이에서 쾌속선 약 30~45분, 섬 안에선 차·오토바이를 빌려 이동"),
   tips=["해변까지 내려가는 길이 가파르고 위험하니 운동화를 신고, 자신 없으면 위 전망 지점에서만 봐요.", "연휴엔 쾌속선 표가 매진될 수 있어 미리 예약하고, 날씨에 따라 배 시간이 바뀌어요.", "섬 안쪽 길이 언덕이고 거칠어 기사 딸린 차를 빌리면 안전하고, 외딴 해변이라 현금을 넉넉히 챙겨요."],
   src=[("인도네시아 관광부 — Kelingking Beach (확인 2026.11.27)", "https://www.indonesia.travel/au-en/destination/bali-nusa-tenggara/bali/kelingking-beach-a-marvelous-wonder-in-the-southwest-of-nusa-penida"), ("인도네시아 관광부 — Nusa Penida (확인 2026.11.27)", "https://www.indonesia.travel/gb/en/travel-ideas/adventure/nusa-penida"), ("인도네시아 관광부 — 발리 해변 팁 (확인 2026.11.27)", "https://www.indonesia.travel/jp/en/travel-ideas/marine/pantai-bali")],
   checked="2026-11-27", photo=None),
 "pk_karon": dict(
   one="푸껫 서해안에서 빠통 남쪽, 까따 바로 북쪽에 있는 넓은 해변이에요. 다이빙·스노클링·윈드서핑·요트 강습과 장비를 갖춘 해변이에요.",
   see=[("까론 모래사장", "빠통보다 한적한 서해안의 긴 해변"), ("해양 스포츠", "다이빙·스노클링·윈드서핑·세일링 강습과 장비 대여"), ("까론 전망대(카오 쌈 핫)", "까따노이·까따·까론 세 해변을 한눈에 보는 노을 명소")],
   facts=dict(hours="상시", fee="입장 무료 (선베드·해양 스포츠 별도 · 방문 전 확인)", stay="약 2~3시간", when="오전 또는 해 질 녘", access="빠통에서 남쪽으로 차로 이동, 전망대는 까따노이 해변 남쪽 언덕 해안도로 옆"),
   tips=["물에 들어가기 전에 해변의 깃발을 보고 빨간 깃발이면 수영하지 않아요.", "해 질 녘엔 까따노이 남쪽 까론 전망대에 올라 세 해변 노을을 보고 내려와 저녁을 먹어요.", "스노클링 장비는 해변 가게에서 빌릴 수 있으니 무겁게 챙겨 오지 않아도 돼요."],
   src=[("태국관광청 — Phuket (확인 2026.11.27)", "https://www.tourismthailand.org/Destinations/Provinces/Phuket/350"), ("TAT 뉴스룸 — Phuket and Phang Nga viewpoints (확인 2026.11.27)", "https://www.tatnews.org/2021/03/phuket-and-phang-nga-viewpoints-are-among-the-worlds-best-for-good-reason/")],
   checked="2026-11-27", photo=None),
 "pk_phangnga": dict(
   one="푸껫 북동쪽 팡아주의 바다 국립공원으로, 바다에서 곧게 솟은 석회암 섬과 바다 동굴이 모여 있어요. 만이 잔잔해 카약으로 동굴과 섬 사이를 지나요.",
   see=[("바다 카약", "잔잔한 만에서 바다 동굴과 섬 사이를 카약으로 지나요"), ("석회암 섬 풍경", "바다에서 곧게 솟은 바위섬과 절벽"), ("사멧낭셰 전망대", "팡아만 섬들을 내려다보는 일출·별 보기 명소")],
   facts=dict(hours="배 일정에 따라 다름 · 방문 전 확인", fee="국립공원 입장료·투어 요금 방문 전 확인", stay="약 하루", when="건기 오전 (일부 섬은 8/1~9/30 휴장)", access="푸껫에서 배 투어로, 사멧낭셰 전망대는 빠통에서 차로 약 2시간(약 80km)"),
   tips=["사멧낭셰 전망대는 동쪽 일출이 가장 좋아서 해 뜨기 전에 도착하도록 새벽에 출발해요.", "카약으로 동굴 안까지 들어가니 젖어도 되는 옷과 방수 휴대폰 케이스를 챙겨요.", "8~9월엔 국립공원 일부 섬과 캠핑장이 계절 휴장하니 투어 코스를 미리 확인해요."],
   src=[("태국관광청 — Phang Nga (확인 2026.11.27)", "https://www.tourismthailand.org/Destinations/Provinces/Phang-Nga/348"), ("TAT 뉴스룸 — Phuket and Phang Nga viewpoints (확인 2026.11.27)", "https://www.tatnews.org/2021/03/phuket-and-phang-nga-viewpoints-are-among-the-worlds-best-for-good-reason/"), ("TAT — Thai National Parks Seasonal Closure 2024~2025 (확인 2026.11.27)", "https://www.tatnews.org/wp-content/uploads/2024/01/Thailand-National-Parks-Seasonal-Closure-of-Attractions_2024-2025-1.pdf")],
   checked="2026-11-27", photo=None),
 "hk_avenue": dict(
   one="침사추이 바닷가에 홍콩 영화인을 기리는 산책로예요. 매일 저녁 8시 빅토리아 항구 빌딩들이 빛과 음악으로 '심포니 오브 라이트' 쇼를 해요.",
   see=[("심포니 오브 라이트", "매일 20:00 항구 양쪽 빌딩이 함께하는 빛·음악 쇼"), ("스타의 거리 산책로", "홍콩 영화인을 기리는 항구 앞 산책길"), ("황금 용 조명 난간", "쇼 때 비늘 무늬 난간 조명이 황금 용으로 바뀌어요")],
   facts=dict(hours="산책로 상시, 쇼 매일 20:00", fee="무료", stay="약 1시간", when="저녁 19:30~20:30", access="침사추이 바닷가, 스타페리 침사추이 부두에서 걸어서"),
   tips=["쇼는 20:00 정각에 시작하니 19:30 무렵 문화센터 앞이나 스타의 거리 난간 쪽에 자리를 잡아요.", "쇼 당일 15:00 이후 태풍 3호 이상이나 적색·흑색 호우 경보가 나오면 그날 쇼는 취소돼요.", "배 위에서 보고 싶으면 스타페리 심포니 오브 라이트 크루즈(침사추이 19:55 출발)를 미리 사요."],
   src=[("스타의 거리 공식 — A Symphony of Lights (확인 2026.11.27)", "https://www.avenueofstars.com.hk/en/a-symphony-of-lights/"), ("홍콩관광청 — A Symphony of Lights (확인 2026.11.27)", "https://discoverhongkong.com/anz/explore/attractions/a-symphony-of-lights.html"), ("스타페리 공식 — Harbour Tour (확인 2026.11.27)", "https://starferry.com.hk/Fares")],
   checked="2026-11-27", photo=None),
 "hk_ferry": dict(
   one="침사추이와 센트럴 사이 빅토리아 항구를 약 9분에 건너는 배예요. 싼 요금으로 항구 양쪽 스카이라인을 가까이 봐요.",
   see=[("빅토리아 항구 횡단", "약 9분 동안 보는 홍콩섬·구룡 스카이라인"), ("위층·아래층 갑판", "층마다 요금이 다르고 위층이 전망이 트였어요"), ("하버 투어", "항구를 한 바퀴 도는 1시간 관광선 (별도 요금)")],
   facts=dict(hours="6:30~23:30, 매일 (약 6~12분 간격)", fee="성인 평일 HK$5·주말·공휴일 HK$6.5 이내, 65세 이상 무료 (2027/1/25부터 인상 예정 · 방문 전 확인)", stay="약 30분", when="저녁 (20:00 쇼 전후)", access="침사추이 스타페리 부두 ↔ 센트럴 7번 부두"),
   tips=["평일 요금이 주말·공휴일보다 싸니 같은 일정이면 평일에 타요.", "저녁 20:00 심포니 오브 라이트 시간에 맞춰 건너면 배 위에서 야경 쇼를 함께 봐요.", "출퇴근 시간대(평일 7:15~9:45)는 현지인이 많으니 구경 목적이면 그 시간을 피해요."],
   src=[("스타페리 공식 — 침사추이·센트럴 시간표·요금 (확인 2026.11.27)", "https://www.starferry.com.hk/sites/default/files/TST_C_Eng.pdf"), ("홍콩 정부 news.gov.hk — Star Ferry fare hikes approved (확인 2026.11.27)", "https://www.news.gov.hk/eng/2023/01/20230131/20230131_190508_383.html"), ("China Daily HK — 2027년 요금 인상 (정부 발표 인용, 확인 2026.11.27)", "https://www.chinadailyhk.com/article/641486")],
   checked="2026-11-27", photo=None),
 "hk_central": dict(
   one="홍콩섬의 중심가로, 고층 빌딩 뒤 언덕에 옛 골목이 이어져요. 약 800m 미드레벨 에스컬레이터를 타고 할리우드 로드와 만모 사원까지 올라가요.",
   see=[("미드레벨 에스컬레이터", "에스컬레이터 16개·무빙워크 3개로 이어진 약 800m 언덕길"), ("만모 사원", "1847~1862년에 지은 문·무의 신 사원, 천장 가득 나선형 향"), ("그레이엄 스트리트 시장", "노점이 빽빽한 옛 거리 시장, 영화 '중경삼림' 촬영지")],
   facts=dict(hours="에스컬레이터 내려가는 방향 6:00~10:00, 올라가는 방향 10:20~24:00", fee="에스컬레이터 무료, 거리 산책 무료", stay="약 1~2시간", when="10:20 이후 (에스컬레이터 오르막 운행)", access="퀸스 로드 센트럴에서 시작해 미드레벨까지 (센트럴 마켓 육교 쪽)"),
   tips=["에스컬레이터는 10:20부터 오르막이라 오전엔 걸어 올라가고, 오전 10시 이후에 타고 올라가며 골목을 봐요.", "올라갈 땐 에스컬레이터로, 내려올 땐 할리우드 로드를 따라 만모 사원·타이쿤 쪽으로 걸어 내려오면 동선이 짧아요.", "에스컬레이터는 피크까지 가지 않으니 빅토리아 피크는 따로 피크트램이나 버스로 가요."],
   src=[("홍콩관광청 — Central–Mid-Levels Escalator (확인 2026.11.27)", "https://www.discoverhongkong.com/anz/place-to-go/central-mid-levels-escalator.html"), ("홍콩관광청 — Old Town Signatures (확인 2026.11.27)", "https://www.discoverhongkong.com/eng/neighbourhoods/old-town-central/old-town-signature.html")],
   checked="2026-11-27", photo=None),
 "hk_mongkok": dict(
   one="몽콕 퉁초이 거리의 여인가와 조던 쪽 템플 스트리트 야시장이 대표적인 구룡의 노점 시장이에요. 옷·기념품부터 길거리 간식과 다이파이동까지 모여 있어요.",
   see=[("여인가(레이디스 마켓)", "퉁초이 거리의 옷·액세서리·축구 유니폼·홍콩 기념품 노점"), ("템플 스트리트 야시장", "다이파이동 노천 식당, 광둥 오페라 공연, 점집"), ("길거리 간식", "카레 어묵, 오징어 튀김, 에그와플, 완탕면")],
   facts=dict(hours="오후~자정 무렵 (가게마다 다름 · 방문 전 확인)", fee="입장 무료", stay="약 1~2시간", when="해 질 녘~밤", access="MTR 프린스 에드워드역에서 남쪽으로 걸어서 (템플 스트리트는 조던 쪽)"),
   tips=["흥정이 기본이라 처음 부른 값에 사지 말고 몇 집을 비교한 뒤 깎아요.", "노점 뒤쪽 상설 가게도 함께 보면 같은 물건을 더 고를 수 있어요.", "템플 스트리트는 해 질 녘 다이파이동 풍경, 밤늦게는 사람이 줄어 아치 사진 찍기가 좋아요."],
   src=[("홍콩관광청 — Ladies' Market (확인 2026.11.27)", "https://www.discoverhongkong.com/hk-eng/interactive-map/ladies-market.html"), ("홍콩관광청 — Temple Street Night Market (확인 2026.11.27)", "https://www.discoverhongkong.com/eng/interactive-map/temple-street-night-market.html"), ("홍콩관광청 — Iconic Street Markets (확인 2026.11.27)", "https://www.discoverhongkong.com/eng/explore/shopping/iconic-street-market.html")],
   checked="2026-11-27", photo=None),
 "hk_ngongping": dict(
   one="퉁청에서 옹핑까지 5.7km를 약 25분에 오르는 케이블카와, 옹핑 마을에서 걸어서 약 10분 거리의 큰 불상이에요. 빅부다는 받침까지 높이 34m예요.",
   see=[("옹핑 360 케이블카", "란타우섬 산과 바다, 공항 위를 지나는 5.7km 케이블카"), ("빅부다(톈탄 대불)", "1993년 완성, 계단 268개 위의 높이 34m 청동 불상"), ("포린사", "빅부다 바로 옆 사찰")],
   facts=dict(hours="케이블카·옹핑 마을 10:00~18:00 (정기 점검일엔 케이블카 운휴 · 방문 전 확인)", fee="왕복 스탠다드 성인 HK$295·어린이 HK$150, 크리스털 성인 HK$365·어린이 HK$220 (2026년 기준)", stay="약 3~4시간", when="평일 오전 개장 직후", access="MTR 퉁청역 B 출구 옆 퉁청 케이블카 역"),
   tips=["주말·공휴일엔 매표 줄이 길어 공식 사이트에서 최대 14일 전에 미리 예약해요.", "비·뇌우 때 운행이 멈출 수 있으니 당일 아침 공식 사이트나 (852) 3666 0606으로 운행 여부를 확인해요.", "빅부다까지 계단 268개를 오르니 편한 신발을 신고, 케이블카 하차 뒤 걸어서 약 10분 잡아요."],
   src=[("옹핑360 공식 — FAQs (확인 2026.11.27)", "https://www.np360.com.hk/en/visitor-information/faqs/"), ("옹핑360 공식 — Cable Car Tickets (확인 2026.11.27)", "https://np360.com.hk/en/tickets-promotions/tickets-tours/cable-car-tickets"), ("홍콩관광청 — Big Buddha and Po Lin Monastery (확인 2026.11.27)", "https://discoverhongkong.com/us/explore/culture/feel-the-calm-at-the-big-buddha-and-po-lin-monastery.html")],
   checked="2026-11-27", photo=None),
 "mc_cotai": dict(
   one="대형 리조트가 줄지어 선 마카오 코타이의 리조트 거리예요. 실내 운하 곤돌라, 건물 사이 대관람차 같은 볼거리가 리조트마다 있어요.",
   see=[("베네시안 곤돌라", "그랜드 커낼·마르코 폴로 실내 운하를 도는 배"), ("골든 릴(스튜디오 시티)", "스튜디오 시티 동관 3층에서 타는 높이 130m 관람차"), ("MGM 코타이 스펙터클", "축구장 길이의 4층 높이 유리 지붕 실내 광장")],
   facts=dict(hours="거리 상시. 곤돌라 11:30~19:30, 골든 릴 14:00~20:00 (매표 13:30~)", fee="곤돌라 성인 평일 MOP 165·주말 MOP 175·공휴일 MOP 195, 골든 릴 MOP 100 (2026년 기준)", stay="약 2~3시간", when="오후~밤", access="마카오 경전철 코타이 서역 일대, 페리 터미널·국경에서 리조트 무료 셔틀"),
   tips=["페리 터미널과 국경에서 리조트 무료 셔틀이 다니니 코타이로 갈 땐 셔틀을 먼저 확인해요.", "곤돌라는 한 배에 최대 6명이 함께 타고 평일이 가장 싸니 평일 오후에 타요.", "골든 릴은 14:00에 열어 20:00에 닫으니 곤돌라를 먼저 타고 해 질 무렵 골든 릴로 넘어가요."],
   src=[("베네시안 마카오 공식 — Gondola Rides (확인 2026.11.27)", "https://www.venetianmacao.com/hotel/amenities/gondola-rides.html"), ("스튜디오 시티 공식 — Golden Reel (확인 2026.11.27)", "https://www.studiocity-macau.com/en/attractions/golden-reel"), ("마카오관광청 — Other Attractions (확인 2026.11.27)", "https://www.macaotourism.gov.mo/en/sightseeing/other-attractions")],
   checked="2026-11-27", photo=None),
 "mc_tower": dict(
   one="2001년에 문을 연 높이 338m 타워로, 223m 높이 전망대에서 마카오와 주강 삼각주를 내려다봐요. 같은 높이에서 233m 번지점프와 스카이워크도 해요.",
   see=[("58층 전망 라운지", "223m 높이에서 보는 마카오 시내 전경"), ("61층 어드벤처 데크", "전망대 입장권에 포함된 위층 데크"), ("AJ 해켓 번지점프·스카이워크", "233m 높이 번지점프, 타워 바깥 둘레를 걷는 스카이워크")],
   facts=dict(hours="전망대 10:00~20:00 (번지점프·스카이워크는 겨울 18:00, 여름 19:30부터 저녁 운영)", fee="전망대 성인 MOP 208, 3~11세·65세 이상 MOP 138, 0~2세 무료 (현장 기준)", stay="약 1시간", when="해 질 녘", access="마카오 반도 남쪽 끝, 시내에서 버스·택시 (노선 방문 전 확인)"),
   tips=["해 지기 30분 전쯤 올라가면 낮 풍경과 야경을 한 번에 보고 20:00 마감 전에 내려와요.", "가짜 표 판매 사이트가 있다고 공식 안내하니 표는 현장이나 공식 채널에서만 사요.", "번지점프·스카이워크는 공식 운영사 사이트에서 미리 예약해야 하니 날짜를 정하면 바로 잡아요."],
   src=[("마카오타워 공식 — Observation Deck (확인 2026.11.27)", "https://www.macautower.com.mo/observation-deck/"), ("마카오타워 공식 — Adventure (확인 2026.11.27)", "https://www.macautower.com.mo/en/entertainment/adventure/"), ("마카오관광청 — Other Attractions (확인 2026.11.27)", "https://www.macaotourism.gov.mo/en/sightseeing/other-attractions")],
   checked="2026-11-27", photo=None),
 "sh_nanjing": dict(
   one="와이탄에서 시작해 서쪽으로 이어지는 상하이 대표 보행자 쇼핑 거리예요. 오래된 백화점과 노포 먹거리 가게, 최신 플래그십 매장이 함께 있어요.",
   see=[("노포 먹거리 가게", "타이캉 식품, 사오완성 같은 오래된 상하이 식품점"), ("플래그십 매장", "화웨이·나이키·레고·세포라 대형 매장"), ("거리 야경", "해 진 뒤 간판 불빛이 켜진 보행자 거리")],
   facts=dict(hours="상시 (24시간, 가게 영업시간은 가게마다 다름)", fee="입장 무료", stay="약 1~2시간", when="오후~저녁", access="상하이 황푸구, 와이탄에서 걸어서 이어져요"),
   tips=["오후에 노포 가게에서 간식을 사 먹고, 해 진 뒤 동쪽 끝 와이탄까지 걸어가 야경으로 마무리해요.", "주말·연휴 저녁엔 사람이 아주 많으니 쇼핑은 평일 낮에 몰아서 해요.", "오래된 식품점은 줄이 길 수 있으니 사고 싶은 간식은 처음 지날 때 바로 사요."],
   src=[("상하이시 정부 — Nanjing Road Pedestrian Street (확인 2026.11.27)", "https://english.shanghai.gov.cn/en-ScenicSpots/20231226/45172d56a204477195888159d4698ac8.html"), ("상하이 관광 공식 Meet in Shanghai — Nanjing Road (확인 2026.11.27)", "https://www.meet-in-shanghai.net/en/huangpu-district/nanjing-road-856210")],
   checked="2026-11-27", photo=None),
}
