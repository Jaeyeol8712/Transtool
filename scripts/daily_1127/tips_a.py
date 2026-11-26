# -*- coding: utf-8 -*-
"""2026-11-27 명소 안내 채우기 (싱가포르 5·쿠알라룸푸르 6·코타키나발루 4 = 15곳). 확인일 2026-11-27. 못 쓴 곳: 없음
메모: visitsingapore.com 장소 페이지는 본문이 스크립트로 떠서 읽히지 않아, 같은 사이트의 PDF 안내서(리틀 인디아 안내서, MICE 지구 안내서, 한국어 탐험 가이드북 2018년 7월판)로 확인했어요. 2018년판 숫자(사원 시간·인디안 헤리티지 센터 요금)는 오래돼 넣지 않았고, 멀라이언 공원 상시 개방·래플스 플레이스역 B출구 도보 약 5분은 그 판 기준이에요.
메모: 센토사 공식 사이트도 스크립트 페이지라 2026년 4월 'Sentosa Discovery Guide' PDF로 확인(센토사 익스프레스 섬 입장 S$4, 케이블카 어른 S$33·어린이 S$22, 보드워크 걸어서 무료). 센토사 익스프레스 운행 시간, 섬 안 버스 요금은 못 찾아 '방문 전 확인'.
메모: 페트로나스 트윈타워 요금(외국인 어른 RM98)은 공식 사이트 'Admission + Ticketing'의 non-MyKad 요금이에요. 같은 페이지의 휴관 날짜가 2025년 것이라 최신 갱신인지 애매해요. 스카이브리지 41층 170m(관광청), 레이크 심포니 분수 20:00·21:00(관광청)도 방문 전 확인 권장.
메모: 페탈링 스트리트 시간은 관광청 페이지끼리 다름(매일 8:00~22:00 / 일~금 8:00~20:00·토 ~22:00). 센트럴 마켓도 10:00~21:30 / 10:00~20:00 두 가지라 시간은 '가게마다 다름'으로 적었어요.
메모: 바투동굴 운영 시간·입장료·복장 규정은 관광청·셀랑오르 관광청 페이지에 수치가 없어(셀랑오르 목록엔 24시간 표기) '방문 전 확인'. 메르데카 광장 국기 게양대 높이는 공식 수치를 못 찾아 넣지 않았어요.
메모: 섬 배 시간(8:00~16:00, 마지막 귀환 16:00)·요금(1섬 왕복 어른 RM48 등)과 '공사 중 KK 항 사우스 제티 임시 출발'은 제셀턴 포인트 터미널 사이트(jesseltonpoint.com.my, 운영사 Suria Bumiria 표기) 기준이라 정부 발표로는 확인 못 했어요. 해양공원 입장료(외국인 18세 이상 RM25)는 Sabah Parks 공식.
메모: 코타키나발루 워터프런트 야시장(필리피노 마켓 등)의 시간은 공식 출처에 없어 '방문 전 확인'. 사바관광청 일본어 사이트의 아피아피 야시장(가야 스트리트, 금·토 18:00~2:00)만 팁에 적었어요."""
SPOTS = {
 "sg_merlion": dict(
   one="사자 머리에 물고기 몸을 한 싱가포르의 상징 멀라이언이 마리나 베이를 바라보며 물을 뿜는 공원이에요. 1972년 싱가포르강 어귀에 세웠다가 1997년 에스플러네이드 다리가 생기며 지금 자리로 옮겼어요.",
   see=[("멀라이언상", "높이 8.6m·무게 70t, 입에서 물을 뿜는 대표 조각상"), ("작은 멀라이언", "큰 멀라이언 뒤편에 있는 작은 멀라이언상"), ("마리나 베이 전망", "풀러턴 호텔 앞에서 마리나 베이와 맞은편 스카이라인을 한눈에 봐요")],
   facts=dict(hours="상시 개방 (24시간)", fee="무료", stay="약 30분", when="이른 아침 또는 해 진 뒤", access="MRT 래플스 플레이스역(EW14/NS26) B 출구에서 걸어서 약 5분, 풀러턴 호텔 앞"),
   tips=["낮엔 단체 관광객이 몰리니 사진은 이른 아침이나 해 진 뒤에 찍으면 한결 여유로워요.", "멀라이언 앞 강변을 따라 싱가포르강 산책이나 범보트(작은 유람선)로 이어 가면 동선이 자연스러워요.", "그늘이 거의 없는 물가라 낮에 간다면 모자와 물을 챙겨요."],
   src=[("싱가포르관광청 — Merlion Park (확인 2026.11.27)", "https://www.visitsingapore.com/en_my/see-do-singapore/recreation-leisure/viewpoints/merlion-park/"), ("싱가포르관광청 — 싱가포르 탐험 여행 가이드북(한국어) (확인 2026.11.27)", "https://www.visitsingapore.com/content/dam/desktop/korea/downloadkit/explorer-guide-kr.pdf")],
   checked="2026-11-27", photo=None),
 "sg_chinatown": dict(
   one="중국계 이민자들의 터전이던 동네로, 파고다 스트리트를 중심으로 사원과 호커 센터, 숍하우스 골목이 모여 있어요. 해가 지면 홍등이 켜져 분위기가 달라져요.",
   see=[("불아사(Buddha Tooth Relic Temple)", "사우스 브리지 로드 288, 부처의 치아 사리를 모신 사원"), ("스리 마리암만 사원", "사우스 브리지 로드 244의 힌두 사원, 10월엔 불 위를 걷는 의식"), ("맥스웰·스미스 스트리트 먹거리", "맥스웰 푸드 센터와 차이나타운 푸드 스트리트(스미스 스트리트 7)의 호커 음식")],
   facts=dict(hours="거리 상시 (사원·가게마다 다름, 방문 전 확인)", fee="거리 무료", stay="약 1시간 30분~2시간", when="늦은 오후~해 진 뒤", access="MRT 차이나타운역(NE4/DT19) A 출구에서 파고다 스트리트까지 도보 약 1분, 또는 맥스웰역(TE18)·텔록 아이어역(DT18)"),
   tips=["불아사는 등이 파인 옷·어깨가 드러나는 옷·반바지·미니스커트로는 들어갈 수 없으니 긴 바지나 걸칠 옷을 챙겨요.", "불아사 안에는 고기 음식을 가지고 들어갈 수 없어, 호커 센터 식사는 사원을 본 뒤로 미뤄요.", "맥스웰 푸드 센터는 점심시간에 직장인으로 붐비니 점심 피크를 조금 비켜 가면 자리 잡기 쉬워요."],
   src=[("불아사 공식 — 오시는 길·방문 안내 (확인 2026.11.27)", "https://www.buddhatoothrelictemple.org.sg/lianxin/contact"), ("싱가포르관광청 — Essential Singapore 지구 안내서 (확인 2026.11.27)", "https://www.visitsingapore.com/content/dam/MICE/Global/downloads/bt_precinct_guide.pdf"), ("싱가포르관광청 — 싱가포르 탐험 여행 가이드북(한국어) (확인 2026.11.27)", "https://www.visitsingapore.com/content/dam/desktop/korea/downloadkit/explorer-guide-kr.pdf")],
   checked="2026-11-27", photo=None),
 "sg_india": dict(
   one="영국 식민지 시절 인도계 이주민이 자리 잡은 동네로, 세랑군 로드를 따라 힌두 사원과 향신료·사리 가게, 인도 식당이 이어져요.",
   see=[("스리 비라마칼리암만 사원", "세랑군 로드 141, 여신 칼리를 모신 남인도 타밀 양식 사원"), ("테카 센터", "1915년에 생겨 1982년 지금 자리로 옮긴 호커 센터 겸 시장, 마살라 도사·비리야니"), ("탄텡니아의 집", "커바우 로드 37, 리틀 인디아에 남은 마지막 중국식 빌라")],
   facts=dict(hours="거리 상시 (사원·가게마다 다름). 무스타파 센터 24시간", fee="거리 무료", stay="약 2시간", when="오전~점심 (디파발리·타이푸삼 축제 기간엔 행사)", access="MRT 리틀 인디아역(NE7/DT12) E 출구에서 세랑군 로드까지 도보 약 5분, 패러 파크·로쵸르·잘란 베사르역도 가까워요"),
   tips=["사원은 민소매·노출 있는 옷으로 들어갈 수 없으니 어깨와 무릎을 가리는 옷을 입고, 신발은 입구에서 벗어요.", "테카 센터에서는 마살라 도사를 오른손으로 먹는 게 전통이지만 숟가락·포크도 있으니 편한 대로 먹어요.", "기념품은 24시간 여는 무스타파 센터(시드 알위 로드 145)에서 밤늦게 사면 낮 일정을 아낄 수 있어요."],
   src=[("싱가포르관광청 — Little India 안내서 (확인 2026.11.27)", "https://www.visitsingapore.com/content/dam/visitsingapore/neighbourhoods/little-india/Little-India_Digital-Version_Final_(1)_(1).pdf"), ("싱가포르관광청 — Essential Singapore 지구 안내서 (확인 2026.11.27)", "https://www.visitsingapore.com/content/dam/MICE/Global/downloads/bt_precinct_guide.pdf"), ("싱가포르관광청 — 싱가포르 탐험 여행 가이드북(한국어) (확인 2026.11.27)", "https://www.visitsingapore.com/content/dam/desktop/korea/downloadkit/explorer-guide-kr.pdf")],
   checked="2026-11-27", photo=None),
 "sg_orchard": dict(
   one="약 2.2km 길이로 백화점과 쇼핑몰이 늘어선 싱가포르 대표 쇼핑 거리예요. 연말엔 거리 전체에 크리스마스 조명이 켜져요.",
   see=[("대형 쇼핑몰", "아이온 오차드·파라곤·탕스(Tang Plaza)·니안 시티 등"), ("에메랄드 힐", "서머셋역 맞은편, 옛 숍하우스를 고친 바가 모인 골목"), ("크리스마스 온 어 그레이트 스트리트", "2026.11.17~2027.1.3 거리 조명, 니안 시티·쇼 하우스 광장에 크리스마스 빌리지")],
   facts=dict(hours="거리 상시 (몰마다 다름, 방문 전 확인)", fee="무료", stay="약 2~3시간", when="저녁 (11월 중순~1월 초엔 조명)", access="MRT 남북선 오차드역(NS22)·서머셋역(NS23)·도비갓역(NS24/NE6/CC1)"),
   tips=["길이 약 2.2km라 오차드역에서 내려 도비갓역 쪽으로 걸어 내려오며 몰을 고르면 되돌아가지 않아요.", "2026년 크리스마스 조명은 11월 17일부터 2027년 1월 3일까지라, 이 기간엔 해 진 뒤 걸으며 조명과 니안 시티 크리스마스 빌리지를 함께 봐요.", "한낮 더위는 몰 안에서 피하고, 쇼핑 뒤 저녁엔 서머셋역 맞은편 에메랄드 힐로 옮겨 가요."],
   src=[("Orchard Road Business Association — Christmas on A Great Street 2026 (확인 2026.11.27)", "https://christmas.orchardroad.org"), ("싱가포르관광청 — Essential Singapore 지구 안내서 (확인 2026.11.27)", "https://www.visitsingapore.com/content/dam/MICE/Global/downloads/bt_precinct_guide.pdf")],
   checked="2026-11-27", photo=None),
 "sg_sentosa": dict(
   one="싱가포르 남쪽의 휴양 섬으로, 실로소·팔라완·탄종 해변과 리조트 월드 센토사, 실로소 요새 같은 볼거리가 모여 있어요. 본섬 비보시티에서 걸어서나 모노레일·케이블카로 건너가요.",
   see=[("팔라완 해변", "흔들다리를 건너 '아시아 대륙 최남단' 지점에 가는 해변"), ("실로소 해변·탄종 해변", "수상 스포츠와 비스트로가 모인 실로소, 바다 위 배가 보이는 한적한 탄종"), ("실로소 요새", "옛 영국 요새, 체험 구역 6곳과 11층 높이 스카이워크")],
   facts=dict(hours="시설마다 다름 · 방문 전 확인", fee="보드워크 걸어서 무료. 센토사 익스프레스 섬 입장 S$4, 케이블카(마운트 페이버 라인) 어른 S$33·어린이 S$22 (2026년 기준)", stay="약 반나절~하루", when="오전에 들어가 해 질 무렵까지", access="MRT 하버프런트역(CC29/NE1) → 비보시티. 센토사 익스프레스는 비보시티 L 로비 3층, 보드워크는 F 로비 1층에서 출발"),
   tips=["돈을 아끼려면 비보시티 F 로비 1층에서 센토사 보드워크로 걸어 들어가면 섬 입장료가 없어요.", "센토사 익스프레스는 EZ-Link 카드로 탈 수 있어, 따로 표를 사지 않고 카드를 찍고 들어가요.", "해변이 섬 남쪽에 길게 이어지니 북적이는 실로소에서 놀고, 쉬고 싶을 땐 탄종 해변으로 옮겨 가요."],
   src=[("센토사 공식 — Sentosa Discovery Guide 2026년 4월 (확인 2026.11.27)", "https://www.sentosa.com.sg/-/media/sentosa/discovery-guide/2026/sdg-apr-2026_en_r1-lr4.pdf?revision=6f1cd682-8bae-495b-9253-9011e5413217"), ("센토사 공식 — Sentosa Express (확인 2026.11.27)", "https://www.sentosa.com.sg/en/things-to-do/attractions/sentosa-express/")],
   checked="2026-11-27", photo=None),
 "kl_twin": dict(
   one="높이 약 452m의 쌍둥이 빌딩으로, 41·42층 스카이브리지가 두 탑을 잇고 86층에 전망대가 있어요. 아래 약 50에이커 KLCC 공원에선 밤마다 음악 분수 쇼가 열려요.",
   see=[("스카이브리지", "41층(약 170m)에서 두 탑을 잇는 다리"), ("86층 전망대", "쿠알라룸푸르 시내를 내려다보는 가장 높은 관람 층"), ("KLCC 공원 레이크 심포니", "빛·음악 분수 쇼 20:00·21:00, 빛만 켜는 쇼 19:30·20:30·21:30")],
   facts=dict(hours="스카이브리지·전망대 화~일·공휴일 9:00~21:00 (입장 20:30까지), 월요일은 둘째·넷째 주만 9:00~20:00. 공원 상시", fee="외국인(MyKad 없음) 어른 RM98, 3~12세·61세 이상 RM50, 2세 미만 무료 (2026년 기준). 공원 무료", stay="약 1시간 30분", when="해 질 무렵~저녁 분수 쇼", access="LRT 'KLCC'역, 탑 사이 수리아 KLCC 쇼핑몰"),
   tips=["24시간 안 방문 표는 온라인으로만 팔고 주말엔 빨리 매진되니 공식 e티켓 사이트에서 미리 사 두고 다운로드해 가요.", "입장 15분 전까지 도착해야 하고 늦으면 환불 없이 입장이 거절될 수 있어요.", "전망대를 해 질 무렵 시간대로 잡고 내려와 20:00·21:00 레이크 심포니 분수 쇼를 공원에서 이어 봐요."],
   src=[("페트로나스 트윈타워 공식 — Admission + Ticketing (확인 2026.11.27)", "https://www.petronastwintowers.com.my/plan-your-visit/admission-ticketing/"), ("말레이시아관광청 — Top Places to Visit in Kuala Lumpur (확인 2026.11.27)", "https://www.malaysia.travel/explore/top-places-to-visit-in-kuala-lumpur"), ("말레이시아관광청 — KL's Best Parks (확인 2026.11.27)", "https://www.malaysia.travel/explore/kl-s-best-parks-for-a-relaxing-day-out")],
   checked="2026-11-27", photo=None),
 "kl_bintang": dict(
   one="쿠알라룸푸르의 대표 쇼핑·유흥 거리예요. 명품부터 저렴한 옷, 전자제품까지 몰마다 성격이 다르고, 밤엔 창캇 부킷빈탕 바 거리가 붐벼요.",
   see=[("파빌리온 쿠알라룸푸르", "명품 브랜드와 영화관이 있는 대형 몰"), ("랏 10·숭가이 왕·로우 얏", "이세탄 재팬 스토어(랏 10), 저렴한 패션(숭가이 왕), 전자제품(로우 얏)"), ("창캇 부킷빈탕", "바와 클럽이 모인 밤거리")],
   facts=dict(hours="거리 상시 (몰·가게마다 다름, 방문 전 확인)", fee="무료", stay="약 2시간", when="오후~밤", access="KL 모노레일·MRT '부킷빈탕'역, GO KL 시티버스 초록·보라 노선"),
   tips=["외국인 여행자는 모노레일·LRT·MRT를 무제한 타는 'KL Travel Pass'를 쓰면 부킷빈탕~KLCC를 오가기 편해요.", "택시 요금은 출발지에 따라 들쭉날쭉하니 Grab 같은 앱 차량으로 요금을 미리 정하고 타요.", "저녁엔 걸어서 갈 수 있는 잘란알로 야시장으로 이어 가면 쇼핑과 저녁을 한 번에 끝내요."],
   src=[("말레이시아관광청 — Bukit Bintang (확인 2026.11.27)", "https://www.malaysia.travel/explore/bukit-bintang"), ("말레이시아관광청 — Jalan Alor (확인 2026.11.27)", "https://www.malaysia.travel/explore/jalan-alor-a-taste-of-malaysian-street-food")],
   checked="2026-11-27", photo=None),
 "kl_alor": dict(
   one="부킷빈탕 바로 옆, 해가 지면 길 양쪽에 노점과 식당 테이블이 깔리는 먹자골목이에요. 대부분 새벽까지 열어요.",
   see=[("꼬치·닭날개 구이", "숯불 닭날개와 사테"), ("면 요리", "커리 락사·아쌈 락사·완탄미·차퀘테우"), ("해산물", "칠리 크랩·굴전·매운 가오리 구이·솔티드 에그 오징어")],
   facts=dict(hours="저녁부터 새벽까지 (노점마다 다름)", fee="거리 무료 (음식값 별도)", stay="약 1시간~1시간 30분", when="해 진 뒤", access="KL 모노레일 '부킷빈탕'역에서 걸어서, 부킷빈탕 워크에서 도보 거리"),
   tips=["가게가 많으니 끝까지 한 바퀴 걸어 본 뒤 고르면 실패가 적어요.", "메뉴 대부분에 사진과 영어가 있고 물어보면 설명해 주니 처음 보는 요리도 부담 없이 시켜 봐요.", "한 번에 다 먹기 어려우니 여러 명이 여러 가게에서 한두 접시씩 나눠 시켜요."],
   src=[("말레이시아관광청 — Jalan Alor: A Taste of Malaysian Street Food (확인 2026.11.27)", "https://www.malaysia.travel/explore/jalan-alor-a-taste-of-malaysian-street-food")],
   checked="2026-11-27", photo=None),
 "kl_merdeka": dict(
   one="1957년 8월 31일 영국 국기를 내리고 말라야 국기를 처음 올린 독립 광장이에요. 맞은편 술탄 압둘 사마드 빌딩의 구리 돔과 시계탑이 상징이에요.",
   see=[("국기 게양대", "세계에서 손꼽히게 높은 게양대가 광장 한쪽에 서 있어요"), ("술탄 압둘 사마드 빌딩", "구리 돔과 시계탑의 옛 건물, 2026년 2월 보존 공사 뒤 다시 열고 안에 갤러리"), ("KL 시티 갤러리", "건물 안 유료 갤러리, 표는 온라인이나 1층 방문자 센터에서")],
   facts=dict(hours="광장 상시. 술탄 압둘 사마드 빌딩 매일 8:00~22:00", fee="광장·건물 입장 무료 (KL 시티 갤러리 유료, 요금 방문 전 확인)", stay="약 45분~1시간", when="이른 아침 또는 해 진 뒤", access="LRT '마스지드 자멕'역에서 걸어서 약 5~7분, RapidKL 버스 420·590번"),
   tips=["그늘 없는 넓은 광장이라 한낮을 피해 이른 아침이나 해 진 뒤 조명이 켜질 때 가요.", "앱 택시로 갈 땐 하차 지점을 'Bangunan Sultan Abdul Samad'로 찍으면 정문 가까이 내려요.", "걸어서 가까운 센트럴 마켓·페탈링 스트리트(차이나타운)와 묶으면 구시가 동선이 한 번에 끝나요."],
   src=[("말레이시아관광청 — Top Places to Visit in Kuala Lumpur (확인 2026.11.27)", "https://www.malaysia.travel/explore/top-places-to-visit-in-kuala-lumpur"), ("말레이시아관광청 — Sultan Abdul Samad Building (확인 2026.11.27)", "https://www.malaysia.travel/explore/sultan-abdul-samad-building")],
   checked="2026-11-27", photo=None),
 "kl_chinatown": dict(
   one="두 개의 큰 문으로 들어가는 페탈링 스트리트 시장과 주변 사원·골목을 아우르는 쿠알라룸푸르 차이나타운이에요. 저녁엔 옷·잡화 노점이 늘어선 야시장이 돼요.",
   see=[("페탈링 스트리트 시장", "옷·액세서리·기념품 노점과 호키엔미·아쌈 락사 같은 먹거리"), ("콰이차이홍 벽화 골목", "벽화마다 옆 QR 코드로 이야기를 볼 수 있는 뒷골목"), ("스리 마하 마리암만 사원", "1873년 세운 말레이시아에서 가장 오래된 힌두 사원 중 하나, 매일 6:30~20:30")],
   facts=dict(hours="가게마다 다름 (관광청 안내 대략 8:00~20:00, 토요일은 ~22:00)", fee="무료", stay="약 1시간 30분", when="늦은 오후~저녁", access="LRT 크라나자야선·MRT '파사르 세니'역에서 도보 약 3분, 모노레일 '마하라자렐라'역에서 도보 약 14분"),
   tips=["노점은 흥정이 기본이라 처음 부른 값보다 한참 낮게 시작해요.", "벽화 골목 콰이차이홍은 오후 햇빛이 사진에 가장 좋아요.", "스리 마하 마리암만 사원은 신발을 벗고 단정한 옷차림이어야 들어갈 수 있고, 돼지고기를 쓰는 노점이 많으니 할랄이 필요하면 인증 표시를 확인해요."],
   src=[("말레이시아관광청 — 5 Best Hotspots in Petaling Street (확인 2026.11.27)", "https://www.malaysia.travel/explore/5-best-hotspots-in-petaling-street-you-don-t-want-to-miss"), ("말레이시아관광청 — Top Places to Visit in Kuala Lumpur (확인 2026.11.27)", "https://www.malaysia.travel/explore/top-places-to-visit-in-kuala-lumpur")],
   checked="2026-11-27", photo=None),
 "kl_batu": dict(
   one="석회암 언덕 속 힌두 성지로, 140피트가 넘는 황금 무루간 신상 옆 272개 색색 계단을 올라 1920년 세운 템플 케이브에 들어가요. 타이푸삼 축제 때 수많은 순례자가 모여요.",
   see=[("무루간 신상과 272계단", "140피트가 넘는 황금 신상, 빨강·노랑·파랑·초록으로 칠한 계단"), ("템플 케이브", "계단 끝 큰 동굴 안의 1920년 사원"), ("다크 케이브·라마야나 동굴", "204번째 계단 쪽 2km가 넘는 동굴(가이드 투어), 힌두 신화 장면을 꾸민 라마야나 동굴")],
   facts=dict(hours="방문 전 확인. 다크 케이브 교육 투어(45분) 평일 10:00~17:00", fee="템플 케이브 입장료 공식 안내 없음 · 방문 전 확인. 주차 RM2", stay="약 1시간 30분", when="아침 8시 전", access="KTM 코뮤터 '바투 케이브'역에서 걸어서 약 5분, 또는 티티왕사 버스 터미널에서 U6 버스"),
   tips=["사람이 몰리기 전인 오전 8시 전에 도착하면 계단을 여유 있게 올라요.", "계단과 사원 주변에 원숭이가 많으니 음식과 비닐봉지는 가방 안에 넣고 올라가요.", "주차 공간이 좁아 공휴일엔 특히 KTM 코뮤터를 타고 가는 게 편해요."],
   src=[("말레이시아관광청 — Batu Caves (확인 2026.11.27)", "https://www.malaysia.travel/explore/batu-caves"), ("셀랑오르 관광청 — Batu Caves (확인 2026.11.27)", "https://selangor.travel/listing/batu-caves/")],
   checked="2026-11-27", photo=None),
 "kk_waterfront": dict(
   one="코타키나발루 시내 바닷가를 따라 식당·바가 모인 워터프런트와 센트럴 마켓, 제셀턴 포인트가 이어지는 곳이에요. 남중국해로 지는 노을을 보며 저녁을 먹어요.",
   see=[("더 워터프런트", "인도 요리부터 퓨전까지 식당이 모이고 해피 아워 바가 많은 노을 명소"), ("코타키나발루 센트럴 마켓", "바닷가의 생선·새우·열대 과일·건어물 시장"), ("제셀턴 포인트 워터프런트", "옛 페리 터미널, 빨간 영국식 공중전화와 옛 사진이 남은 산책길")],
   facts=dict(hours="거리 상시 (식당·시장·야시장 시간은 방문 전 확인)", fee="무료", stay="약 1시간~1시간 30분", when="해 질 무렵~저녁", access="코타키나발루 시내 중심 바닷가, 시내 어디서나 걸어서"),
   tips=["해 지기 전 워터프런트 해피 아워 시간에 자리를 잡으면 노을과 저녁을 함께 즐겨요.", "금·토요일이라면 가까운 가야 스트리트의 아피아피 야시장(18:00~새벽 2시)까지 걸어가 해산물 구이를 먹어요.", "일요일 아침엔 같은 가야 스트리트에서 선데이 마켓(6:00~12:00)이 열리니 섬 투어 전 들러요."],
   src=[("사바관광청 — The Waterfront (확인 2026.11.27)", "https://sabahtourism.com/destination/the-waterfront/"), ("사바관광청 — Jesselton Point Waterfront (확인 2026.11.27)", "https://sabahtourism.com/destination/jesselton-point-waterfront/"), ("사바관광청 일본어 — コタキナバルのナイトマーケット (확인 2026.11.27)", "https://japan.sabahtourism.com/2024/10/08/%E3%82%B3%E3%82%BF%E3%82%AD%E3%83%8A%E3%83%90%E3%83%AB%E3%81%AE%E3%83%8A%E3%82%A4%E3%83%88%E3%83%9E%E3%83%BC%E3%82%B1%E3%83%83%E3%83%88%E3%81%A7%E5%A4%9C%E3%81%AE%E5%86%92%E9%99%BA%E3%81%B8%E2%9D%A3")],
   checked="2026-11-27", photo=None),
 "kk_aru": dict(
   one="코타키나발루 시내에서 약 6km 남쪽, 서쪽을 향한 긴 모래 해변이라 노을 명소로 꼽혀요. 해 질 녘이면 현지인들이 소풍을 나와요.",
   see=[("해변 노을", "바다 수평선으로 해가 지며 하늘이 붉게 물들어요"), ("간식 노점", "노을을 보며 먹을 간식을 파는 작은 노점들"), ("프린스 필립 공원·페르다나 공원", "해변 옆 산책로와 공원")],
   facts=dict(hours="상시 (노점 시간은 방문 전 확인)", fee="무료", stay="약 1시간 30분", when="해 지기 약 1시간 전~노을", access="시내에서 약 6km, 잘란 툰쿠 압둘 라만 끝. 택시·앱 차량으로"),
   tips=["서쪽을 향한 해변이라 해 지기 약 1시간 전에 도착해 자리를 잡고 노을을 봐요.", "노점에서 간식을 사 해변에 앉아 먹는 게 현지식이니 작은 돈 현금을 챙겨요.", "조금 일찍 도착해 해변 옆 프린스 필립 공원·페르다나 공원을 먼저 걷고 노을 시간에 맞춰 해변으로 나가요."],
   src=[("사바관광청 — Tanjung Aru Beach (확인 2026.11.27)", "https://sabahtourism.com/destination/tanjung-aru-beach/"), ("사바관광청 — Why Tanjung Aru Is Kota Kinabalu's Most Popular Beach (확인 2026.11.27)", "https://sabahtourism.com/article/why-tanjung-aru-is-kota-kinabalus-most-popular-beach/")],
   checked="2026-11-27", photo=None),
 "kk_sapi": dict(
   one="툰구 압둘 라만 해양공원의 섬으로, 물살이 잔잔하고 얕은 산호초가 있어 아이와 스노클링 초보에게 좋아요. 썰물 땐 모래톱으로 가야섬까지 걸어서 건너요.",
   see=[("얕은 산호초 해변", "잔잔한 물살에서 즐기는 스노클링"), ("섬 숲길", "약 5km 이어지는 자연 산책로"), ("가야섬 모래톱", "썰물 때 드러나 걸어서 건너는 모래길")],
   facts=dict(hours="해양공원 매일 8:00~17:00. 배 8:00~16:00 (섬에서 마지막 귀환 16:00)", fee="해양공원 입장 외국인 18세 이상 RM25, 17세 이하·60세 이상 RM20. 배 왕복 1섬 어른 RM48·어린이 RM43 (2026년 기준)", stay="약 3~4시간", when="오전 일찍", access="코타키나발루 시내 선착장에서 배로 약 30분 (제셀턴 포인트 공사 중엔 KK 항 사우스 제티에서 출발)"),
   tips=["마지막 귀환 배가 16:00이고 늦은 배가 없으니 오전 첫 배로 들어가 시간을 넉넉히 써요.", "해양공원 입장료는 선착장의 Sabah Parks 창구에서 따로 내고 외국인은 여권이 필요하니 꼭 챙겨요.", "배는 현금·카드·Touch 'n Go로 낼 수 있고, 섬 2곳을 묶으면 왕복 RM58이라 마누칸섬과 함께 도는 게 좋아요."],
   src=[("Sabah Parks 공식 — Tunku Abdul Rahman Park (확인 2026.11.27)", "https://www.sabahparks.org.my/tunku-abdul-rahman-park"), ("사바관광청 — Tunku Abdul Rahman Park (확인 2026.11.27)", "https://sabahtourism.com/destination/tunku-abdul-rahman-park/"), ("제셀턴 포인트 터미널 — 배 시간·요금 (확인 2026.11.27)", "https://jesseltonpoint.com.my/schedule")],
   checked="2026-11-27", photo=None),
 "kk_manukan": dict(
   one="툰구 압둘 라만 해양공원에서 가장 잘 갖춰진 섬으로, 공원 본부와 해변 샬레가 있어요. 섬 동쪽 끝 해변이 스노클링하기 좋아요.",
   see=[("동쪽 끝 해변", "스노클링하기 좋은 맑은 바다"), ("자연 산책로", "섬 숲을 따라 걷는 길"), ("해변 샬레", "Sutera Sanctuary Lodges가 운영하는 숙박 시설")],
   facts=dict(hours="해양공원 매일 8:00~17:00. 배 8:00~16:00 (섬에서 마지막 귀환 16:00)", fee="해양공원 입장 외국인 18세 이상 RM25, 17세 이하·60세 이상 RM20. 배 왕복 1섬 어른 RM48·어린이 RM43 (2026년 기준)", stay="약 3~4시간 (숙박 가능)", when="오전 일찍", access="코타키나발루 시내 선착장에서 배로 약 30분 (제셀턴 포인트 공사 중엔 KK 항 사우스 제티에서 출발)"),
   tips=["공사로 출발 선착장이 KK 항 사우스 제티로 바뀌었다는 안내가 있으니 출발 전 터미널 사이트에서 타는 곳을 확인해요.", "Easybook으로 배를 미리 예약하면 선착장 매표 줄을 건너뛸 수 있어요.", "섬에서 하룻밤 묵으려면 운영사(Sutera Sanctuary Lodges)에 직접 예약해야 해요."],
   src=[("Sabah Parks 공식 — Tunku Abdul Rahman Park (확인 2026.11.27)", "https://www.sabahparks.org.my/tunku-abdul-rahman-park"), ("사바관광청 — Tunku Abdul Rahman Park (확인 2026.11.27)", "https://sabahtourism.com/destination/tunku-abdul-rahman-park/"), ("제셀턴 포인트 터미널 — 배 시간·요금 (확인 2026.11.27)", "https://jesseltonpoint.com.my/schedule")],
   checked="2026-11-27", photo=None),
}
