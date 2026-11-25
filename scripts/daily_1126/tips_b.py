# -*- coding: utf-8 -*-
"""2026-11-26 명소 안내 채우기 (나트랑 5·호찌민 5·푸꾸옥 5 = 15곳). 확인일 2026-11-26. 못 쓴 곳: 없음
메모: 시·성 관광 공식 페이지가 없는 곳(벤탄 시장·중앙우체국·부이비엔·나트랑 야시장·즈엉동 야시장·사오 해변·나트랑 해변·머드 온천)은
      베트남 관광청(vietnamtourism.vn·vietnam.travel)과 베트남항공 공식 여행 안내를 함께 근거로 썼어요(사이트 기존 구찌 터널 안내와 같은 방식).
메모: 포나가르 탑 입장료는 베트남 관광청 22,000동, 베트남항공 안내 30,000동으로 달라 '약 30,000동 · 방문 전 확인'으로 적었어요.
      10~12월엔 17:30에 닫는다는 안내도 베트남항공 기준이에요.
메모: 머드 온천(탑바) 요금은 공식 안내에 달러만 있어 넣지 않았어요(방문 전 확인). 운영 7:00~17:30은 베트남항공 안내 기준.
메모: 혼텀 케이블카 운행 시각은 상시 안내를 못 찾았어요(2026년 설 연휴 안내 9:00~11:30·13:30~17:00 출발만 있음) → '방문 전 확인'.
      Kiss of the Sea는 '화요일 쉼'과 '화요일엔 배우 없이 진행'이 공식 안내 안에서 엇갈려요.
메모: 빈펄 사파리 운영 시작이 공식 글마다 8:30/9:00으로 달라 '9:00 무렵~16:00'으로 적었어요. 요금은 2026년 공식 글 기준.
메모: 통일궁 요금(2025/1/1 시행)은 공식 연락처 페이지 기준, 방문 안내 페이지엔 '갱신 중'이라 바뀔 수 있어요.
메모: 부이비엔 보행자 거리 운영 시간, 중앙우체국 개방 시간, 호핑투어·메콩델타 배 요금은 공식 수치를 못 찾아 '방문 전 확인'."""
SPOTS = {
 "nt_beach": dict(
   one="나트랑 시내 쩐푸 거리를 따라 길게 이어진 도심 해변이에요. 베트남 관광청은 약 7km 모래사장이라고 소개해요.",
   see=[("쩐푸 해변 산책로", "야자수와 호텔·식당이 늘어선 바닷가 산책길"), ("해양 스포츠", "패러세일링·제트스키·패들보드 등 바다 놀이"), ("해변 해산물 식당", "바닷가를 따라 모인 해산물 식당과 바")],
   facts=dict(hours="상시 개방", fee="입장 무료 (선베드·해양 스포츠는 별도 요금 · 방문 전 확인)", stay="약 1~2시간", when="이른 아침 또는 늦은 오후", access="나트랑 시내 쩐푸 거리 바로 앞, 시내 숙소에서 걸어서 가요"),
   tips=["한낮엔 그늘이 적고 붐비니 해 뜰 무렵이나 16시 이후에 걷거나 물놀이해요.", "수영은 지정된 구역에서만 하고, 10~12월 우기엔 날씨와 파도를 보고 들어가요.", "저녁엔 해변 산책 뒤 바로 옆 나트랑 야시장으로 걸어가면 동선이 한 번에 이어져요."],
   src=[("베트남 관광청 — 7 reasons to visit Nha Trang (확인 2026.11.26)", "https://vietnam.travel/node/563"), ("베트남항공 — Beaches in Nha Trang (확인 2026.11.26)", "https://www.vietnamairlines.com/en/useful-information/travel-guide/beach-nha-trang")],
   checked="2026-11-26", photo=None),
 "nt_night": dict(
   one="쩐푸 해변 근처 거리에 저녁마다 열리는 나트랑 야시장이에요. 해산물 구이와 반깐 같은 간식, 옷·기념품 가게가 모여 있어요.",
   see=[("해산물 구이 노점", "생선·오징어·조개를 바로 구워 주는 노점"), ("나트랑 간식", "작은 쌀 팬케이크 반깐, 닌호아식 넴느엉"), ("기념품·여름옷", "조개 장신구, 대나무·나무 공예품, 수영복·모자")],
   facts=dict(hours="19:00~22:00 무렵 (가게마다 다름)", fee="입장 무료", stay="약 1시간", when="저녁 19:00 무렵", access="나트랑 시내 쩐푸 거리 쪽, 18:00 무렵부터 차량이 막혀 걸어서 들어가요"),
   tips=["19:00 무렵 일찍 가면 덜 붐비고 갓 구운 음식을 먹기 좋아요.", "카드를 안 받는 노점이 많으니 작은 단위 동 현금을 챙겨요.", "해산물은 무게로 값을 매기는 경우가 많으니 주문 전에 값을 먼저 확인해요."],
   src=[("베트남항공 — Nha Trang Night Market (확인 2026.11.26)", "https://www.vietnamairlines.com/en/useful-information/travel-guide/nha-trang-night-market")],
   checked="2026-11-26", photo=None),
 "nt_ponagar": dict(
   one="시내 북쪽 약 2km 꾸라오 언덕에 선 참파 왕국 시대의 힌두 사원이에요. 높이 23m 본탑 등 탑 4기가 남아 있어요.",
   see=[("본탑", "높이 23m, 안에 2.6m 검은 화강암 포나가르 여신상"), ("만다파 기둥", "탑으로 오르기 전 남은 명상 회랑의 돌기둥"), ("카이강 하구 전망", "언덕 위에서 보는 강 하구와 어선")],
   facts=dict(hours="6:00~18:00 (10~12월은 17:30까지라는 안내도 있음 · 방문 전 확인)", fee="약 30,000동 (안내마다 달라 방문 전 확인)", stay="약 1시간", when="이른 아침(7:30~9:00) 또는 15시 이후", access="나트랑 시내에서 북쪽으로 약 2km, 택시로 약 5~10분"),
   tips=["사원이라 반바지·민소매 차림이면 들어가기 전에 가릴 숄이나 얇은 겉옷을 챙겨요.", "한낮엔 돌계단이 뜨거우니 아침 일찍이나 15시 이후에 가요.", "탑바 머드 온천이 탑 뒤쪽 가까이 있어 같은 날 묶으면 이동이 짧아요."],
   src=[("베트남 관광청 — Po Nagar Cham Towers (확인 2026.11.26)", "https://vietnamtourism.vn/en/index.php/tourism/items/829"), ("칸호아성 관광 — Po Nagar Cham Towers (확인 2026.11.26)", "https://dulichso.khanhhoa.gov.vn/en/article/po-nagar-cham-towers-77f"), ("베트남항공 — Ponagar Temple (확인 2026.11.26)", "https://www.vietnamairlines.com/en/useful-information/travel-guide/ponagar-temple")],
   checked="2026-11-26", photo=None),
 "nt_mud": dict(
   one="포나가르 탑 뒤쪽, 시내 북쪽 약 4km에 있는 광천 온천이에요. 땅속 100m에서 나오는 38~40°C 광천수와 머드 목욕을 해요.",
   see=[("머드 목욕", "진흙 탕에 몸을 담근 뒤 햇볕에 말리는 코스"), ("광천수 온탕", "머드를 씻어 내고 들어가는 따뜻한 광천수 탕"), ("개별탕", "둘이 따로 쓰는 개별 머드탕")],
   facts=dict(hours="7:00~17:30 (방문 전 확인)", fee="코스마다 다름 · 방문 전 확인", stay="약 2시간", when="오전 (건기 2~8월)", access="나트랑 시내에서 택시·그랩으로 약 15~20분"),
   tips=["밝은 수영복은 진흙 물이 들 수 있으니 어두운색 수영복과 슬리퍼, 머리끈을 챙겨요.", "배부르게 먹은 직후엔 피하고, 식사 뒤 약 2시간 지나서 들어가요.", "포나가르 탑을 오전에 보고 바로 온천으로 넘어가면 시내로 한 번만 돌아와요."],
   src=[("베트남 관광청 — Thap Ba Hot Spring Centre (확인 2026.11.26)", "https://vietnamtourism.vn/en/index.php/tourism/items/922"), ("베트남항공 — Mud bath in Nha Trang (확인 2026.11.26)", "https://www.vietnamairlines.com/en/useful-information/travel-guide/mud-bath-in-nha-trang")],
   checked="2026-11-26", photo=None),
 "nt_hopping": dict(
   one="나트랑만의 섬들을 배로 돌며 스노클링을 하는 바다 일정이에요. 혼문섬 일대는 2001년 베트남 첫 해양 보호구역으로 지정된 산호 바다예요.",
   see=[("혼문섬 산호초", "수심 10m 안팎에 산호와 열대어가 모인 보호구역"), ("스노클링·유리 바닥 배", "물에 들어가지 않아도 산호를 볼 수 있어요"), ("나트랑만 섬 풍경", "혼째·혼미에우 등 보호구역 안 섬들")],
   facts=dict(hours="배 일정에 따라 다름 · 방문 전 확인", fee="배·코스마다 다름 · 방문 전 확인", stay="약 반나절", when="오전 (바다가 잔잔한 시간)", access="꺼우다 항구에서 배로 약 45분 (약 10km)"),
   tips=["10~12월 우기엔 배가 취소될 수 있으니 여행 앞쪽 날짜에 잡아 미룰 여유를 둬요.", "보호구역이라 산호를 밟거나 만지지 말고, 물에 들어가기 전 선크림은 미리 발라 둬요.", "배 멀미가 걱정되면 출항 전에 멀미약을 먹고, 방수 휴대폰 케이스를 챙겨요."],
   src=[("칸호아성 — Hon Mun (확인 2026.11.26)", "https://en.khanhhoa.gov.vn/vi/tourist-sites/hon-mun-4060"), ("칸호아성 — Hon Mun Marine Protected Area (확인 2026.11.26)", "https://en.khanhhoa.gov.vn/vi/preserve/hon-mun-marine-protected-area"), ("베트남 관광청 — 7 reasons to visit Nha Trang (확인 2026.11.26)", "https://vietnam.travel/node/563")],
   checked="2026-11-26", photo=None),
 "hc_benthanh": dict(
   one="시계탑이 달린 정문으로 유명한 호찌민 1군의 대표 시장이에요. 약 1,450개 매장이 모여 기념품·옷·먹거리를 한 번에 봐요.",
   see=[("정문 시계탑", "시장 정면의 시계탑, 사진 찍는 대표 자리"), ("시장 안 먹거리 골목", "쌀국수·디저트 등 남부 음식을 파는 노점"), ("주변 저녁 시장", "시장이 닫은 뒤 옆 판보이짜우·판쭈찐 거리에 서는 노점")],
   facts=dict(hours="6:00~18:00 무렵 (시장 안), 주변 저녁 시장은 그 뒤 · 방문 전 확인", fee="입장 무료", stay="약 1시간", when="오전 (한낮 더위 전)", access="호찌민 1군 중심, 1군 숙소에서 걸어서 또는 그랩"),
   tips=["관광객 대상 가격이 높게 붙는 경우가 많으니 여러 가게 값을 비교하고 흥정해요.", "사람이 몰려 소매치기가 있으니 가방은 앞으로 메고 휴대폰은 손에 오래 들고 있지 않아요.", "정문 앞은 차가 많은 큰길이라 길을 건널 땐 주의하고, 중앙우체국·통일궁과 같은 날 걸어서 묶어요."],
   src=[("베트남항공 — Ben Thanh Market (확인 2026.11.26)", "https://www.vietnamairlines.com/en/useful-information/travel-guide/saigon-market")],
   checked="2026-11-26", photo=None),
 "hc_post": dict(
   one="1886~1891년에 지은 프랑스 식민지 시대 우체국이에요. 아치형 천장 아래에서 지금도 엽서와 우표를 보낼 수 있어요.",
   see=[("아치형 천장 홀", "기차역을 닮은 둥근 천장과 아치 창"), ("옛 지도 두 점", "1892년·1936년 남부 베트남 지도"), ("나무 전화 부스", "지금은 쓰지 않는 옛 공중전화 부스")],
   facts=dict(hours="방문 전 확인", fee="입장 무료", stay="약 30~45분", when="8:00~10:00 또는 16:00~18:00", access="호찌민 1군 꽁싸빠리 2번지, 노트르담 대성당 바로 옆"),
   tips=["한낮 단체 관광객을 피하려면 오전 8~10시나 오후 16시 이후에 가요.", "안에서 엽서와 우표를 사 바로 한국으로 부칠 수 있어요.", "노트르담 대성당(도보 약 1분)·책 거리(약 2분)·통일궁(약 10분)이 가까워 한 번에 걸어서 돌아요."],
   src=[("베트남항공 — Saigon Central Post Office (확인 2026.11.26)", "https://www.vietnamairlines.com/en/useful-information/travel-guide/saigon-central-post")],
   checked="2026-11-26", photo=None),
 "hc_palace": dict(
   one="옛 남베트남 대통령궁으로, 1975년 4월 전쟁이 끝난 현장이에요. 회의실·연회장부터 지하 벙커까지 그대로 둘러봐요.",
   see=[("연회장·회의실", "옛 대통령궁의 넓은 접견실과 각료 회의실"), ("지하 벙커", "작전 지휘실과 통신실이 남은 지하층"), ("노로돔 궁~통일궁 전시", "1868년부터 이곳의 역사를 보여 주는 상설 전시")],
   facts=dict(hours="7:00~18:00, 매일 (특별 휴관은 따로 공지)", fee="성인 80,000동, 학생·노인 40,000동, 6~17세 20,000동 (2025/1/1 시행)", stay="약 1시간 30분", when="오전 (개장 직후)", access="호찌민 1군, 매표소는 남끼커이응이아 135번지 문(7:00~18:00)·응우옌주 106번지 문(8:00~16:00)"),
   tips=["반바지·민소매 차림은 들어갈 수 없으니 긴바지나 무릎 아래 옷을 입고 가요.", "오디오 가이드가 10개 언어로 있으니 안내 데스크에서 빌려 동선에 맞춰 들어요.", "응우옌주 쪽 매표소는 16:00에 닫으니 오후 늦게 가면 남끼커이응이아 쪽 문으로 가요."],
   src=[("통일궁 공식 — Visit (확인 2026.11.26)", "https://dinhdoclap.gov.vn/en/visit"), ("통일궁 공식 — Contact·FAQ (확인 2026.11.26)", "https://dinhdoclap.gov.vn/en/?p=294")],
   checked="2026-11-26", photo=None),
 "hc_buivien": dict(
   one="부이비엔·데탐·팜응우라오 거리가 만나는 1군의 여행자 거리예요. 밤이면 차가 막히고 음악·노점·거리 공연으로 가득 차요.",
   see=[("밤 거리 분위기", "길 양쪽 바와 거리 음악·공연"), ("거리 음식", "반짱느엉(구운 라이스페이퍼)·반미·밤 껌떰"), ("주변 데탐·팜응우라오 거리", "여행자 숙소와 가게가 모인 옆 골목")],
   facts=dict(hours="상시 (밤 보행자 거리 운영 시간은 방문 전 확인)", fee="입장 무료", stay="약 1~2시간", when="밤 (특히 주말)", access="호찌민 1군, 벤탄 시장에서 걸어서 또는 그랩"),
   tips=["사람이 아주 많아 소매치기가 있으니 휴대폰·지갑은 앞주머니나 앞으로 멘 가방에 넣어요.", "술을 마신다면 오토바이·차 운전 대신 걸어서 가거나 그랩을 불러 돌아와요.", "기념품·문신·마사지 같은 거리 서비스는 시작 전에 값을 먼저 정해요."],
   src=[("베트남항공 — Bui Vien Walking Street (확인 2026.11.26)", "https://www.vietnamairlines.com/en/useful-information/travel-guide/bui-vien-walking-street")],
   checked="2026-11-26", photo=None),
 "hc_mekong": dict(
   one="호찌민에서 당일로 다녀오는 메콩강 하류의 수로 마을 일정이에요. 작은 배로 야자수 수로를 지나고 새벽 수상시장을 봐요.",
   see=[("야자수 수로 배 타기", "벤째 등에서 니파야자가 늘어선 좁은 수로를 작은 배로 지나요"), ("수상시장", "까이베·껀터에서 해 뜰 무렵 배끼리 사고파는 시장"), ("코코넛 캔디 공방", "벤째 수로 길에 들르는 전통 간식 공방")],
   facts=dict(hours="수상시장은 새벽~이른 아침, 배 일정은 코스마다 다름 · 방문 전 확인", fee="코스·배마다 다름 · 방문 전 확인", stay="약 하루", when="건기(12~4월) 이른 아침 출발", access="호찌민에서 차로 약 2시간 이상 (목적지에 따라 70~350km, 서부 버스터미널에서 버스도 있음)"),
   tips=["수상시장은 해 뜰 무렵이 가장 붐비니, 껀터 수상시장을 보려면 하루 묵고 6시 전에 배에 타요.", "당일로 다녀오려면 호찌민에서 가까운 벤째·미토 쪽 수로를 고르면 이동 시간이 줄어요.", "배 위는 햇볕을 피할 곳이 적어 모자·선크림·물을 챙기고 가벼운 옷을 입어요."],
   src=[("베트남 관광청 — 5 unique towns in the Mekong Delta (확인 2026.11.26)", "https://vietnam.travel/index.php/node/1175"), ("베트남항공 — Ho Chi Minh to Mekong Delta (확인 2026.11.26)", "https://www.vietnamairlines.com/en/useful-information/travel-guide/ho-chi-minh-to-mekong-delta")],
   checked="2026-11-26", photo=None),
 "pq_night": dict(
   one="즈엉동 강가 바익당 거리에 매일 저녁 서는 푸꾸옥 대표 야시장이에요. 해산물 구이와 간식, 조개 장신구 같은 기념품을 팔아요.",
   see=[("해산물 노점", "고르는 즉시 구워 주는 생선·조개·새우"), ("푸꾸옥 먹거리", "청어 샐러드, 국수 등 섬 음식"), ("딘꺼우 사당", "시장에서 약 600m, 바위 위 사당과 노을 전망")],
   facts=dict(hours="17:00~23:30 무렵 (붐비는 시간 19:00~22:00)", fee="입장 무료", stay="약 1시간", when="해 질 무렵~저녁", access="즈엉동 바익당 거리, 푸꾸옥 공항에서 약 3km (17:00 무렵부터 차량 통제라 걸어서 들어가요)"),
   tips=["해 질 무렵 딘꺼우 사당(약 8분 거리)에서 노을을 보고 시장으로 걸어오면 동선이 딱 맞아요.", "대부분 노점이 카드를 안 받으니 작은 단위 동 현금을 챙겨요.", "해산물은 무게로 파는 경우가 많아 주문 전 값을 꼭 확인하고 몇 곳을 비교해요."],
   src=[("베트남항공 — Duong Dong Night Market (확인 2026.11.26)", "https://www.vietnamairlines.com/en/useful-information/travel-guide/duong-dong-night-market"), ("베트남 관광청 — Explore Phu Quoc by night (확인 2026.11.26)", "https://vietnam.travel/vi/things-to-do/explore-phu-quoc-night")],
   checked="2026-11-26", photo=None),
 "pq_cable": dict(
   one="푸꾸옥 남쪽 안토이에서 혼텀섬까지 바다 위 7,899.9m를 건너는 케이블카예요. 편도 약 15분, 섬에선 워터파크와 놀이공원을 같은 표로 써요.",
   see=[("바다 위 케이블카", "혼즈아·혼로이 섬 위를 지나며 보는 남부 바다"), ("아쿠아토피아 워터파크", "왕복권에 포함된 혼텀섬 워터파크"), ("엑소티카 파크", "왕복권에 포함된 혼텀섬 놀이 구역")],
   facts=dict(hours="시즌마다 다름 · 방문 전 확인 (공식 앱·사이트 공지)", fee="왕복 성인(1.4m 이상) 850,000동, 어린이(1~1.4m) 700,000동, 1m 미만 무료 (2026년 기준)", stay="약 6~8시간", when="오전 일찍 출발", access="안토이역(선셋타운), 즈엉동에서 차로 약 40~45분"),
   tips=["현장 매표소는 성수기에 줄이 길어 공식 사이트나 앱에서 미리 사고 QR코드로 바로 들어가요.", "혼텀섬에서 하루를 쓰려면 아침 일찍 즈엉동을 나서고, 돌아와서 선셋타운 저녁 공연으로 이어 가요.", "왕복권은 같은 날만 유효하니 돌아오는 케이블카 마지막 시각을 탑승 때 확인해요."],
   src=[("Sun Paradise Land 공식 — Hon Thom Cable Car ticket price (확인 2026.11.26)", "https://sunparadiseland.com/en/SunParadiseLandPhuQuoc/tin-tuc/hon-thom-cable-car-ticket-price-and-things-to-do-for-a-fun-day-32438"), ("Sun World 공식 — How to buy and ticket prices Hon Thom (확인 2026.11.26)", "https://sunworld.vn/en/hon-thom/travel-news/tat-tan-tat-how-to-buy-and-ticket-prices-Hon-Thom-Tet-Nguyen-Dan-2026-16223")],
   checked="2026-11-26", photo=None),
 "pq_sunset": dict(
   one="푸꾸옥 남쪽 안토이에 지중해 마을처럼 꾸민 해안 거리예요. 끝이 30cm 떨어진 키스 브리지에서 노을을 보고 밤 공연까지 이어져요.",
   see=[("키스 브리지", "양쪽 끝이 30cm 떨어진 다리, 22개 언어 글귀 394개"), ("파스텔 언덕 거리", "언덕을 따라 이어진 파스텔색 집과 바다 보이는 카페"), ("저녁 공연", "17:00 Awaken Sea, 19:30 Symphony of the Sea, 21:00 Kiss of the Sea")],
   facts=dict(hours="거리는 상시, 공연 시각은 위 참고 (Kiss of the Sea 화요일 운영 방식은 방문 전 확인)", fee="거리 산책 무료, Kiss of the Sea 등 공연 요금은 방문 전 확인", stay="약 3시간 (노을~밤 공연)", when="16시 이후~밤", access="안토이, 푸꾸옥 공항에서 택시 약 25분, 즈엉동에서 약 40분"),
   tips=["16시 무렵 도착해 언덕 거리를 걷고 키스 브리지에서 노을을 본 뒤 밤 공연까지 보면 한 번에 끝나요.", "공연은 앞자리가 금방 차니 시작 20~30분 전에 자리를 잡아요.", "언덕과 계단이 많아 굽 낮은 신발이나 샌들을 신어요."],
   src=[("Sun World 공식 — Sunset Town Phu Quoc travel guide (확인 2026.11.26)", "https://sunworld.vn/en/hon-thom/travel-guide/kinh-nghiem-du-lich-sunset-town-phu-quoc-tron-ven-va-tiet-kiem-17546"), ("Sun Paradise Land 공식 — Kiss of the Sea 공연 일정 (확인 2026.11.26)", "https://sunparadiseland.com/en/SunParadiseLandPhuQuoc/tin-tuc/lich-dien-show-dien-nu-hon-cua-bien-ca-kiss-of-the-sea-17865")],
   checked="2026-11-26", photo=None),
 "pq_sao": dict(
   one="푸꾸옥 남동쪽 안토이에 있는 흰 모래 해변이에요. 잔잔한 만에 고운 모래와 옥빛 바다가 몇 km 이어져요.",
   see=[("흰 모래사장", "가루처럼 고운 흰 모래와 옥빛 얕은 바다"), ("바닷가 나무 그늘", "해변을 따라 그늘을 만들어 주는 나무"), ("해변 식당·카페", "바다를 보며 쉬는 해산물 식당과 카페")],
   facts=dict(hours="상시", fee="입장 요금 공식 안내 없음 · 방문 전 확인 (식당·선베드 별도)", stay="약 2~3시간", when="건기(11~4월) 이른 아침 또는 늦은 오후", access="즈엉동에서 차로 약 45분 (약 30km)"),
   tips=["주말보다 평일이 한산하니 해변 날은 평일로 잡아요.", "한낮 햇볕이 강하니 오전 일찍이나 늦은 오후에 가고 선크림·모자를 챙겨요.", "5~10월 우기엔 비와 높은 파도가 잦아 바다 상태를 보고 가요."],
   src=[("베트남항공 — Sao Beach (확인 2026.11.26)", "https://www.vietnamairlines.com/en/plan-book/travel/travel-guide/sao-beach")],
   checked="2026-11-26", photo=None),
 "pq_vin": dict(
   one="푸꾸옥 북서쪽에 놀이공원 빈원더스와 개방형 동물원 빈펄 사파리가 나란히 있어요. 사파리엔 약 200종 4,000여 마리 동물이 있어요.",
   see=[("빈원더스 테마 구역", "유럽 거리·바이킹 마을·타이푼 월드 등 6개 구역"), ("저녁 공연", "18:45~19:05 ONCE 쇼, 낮엔 음악 분수(11:30·14:00·17:30)"), ("빈펄 사파리 버스 투어", "동물이 풀려 있는 구역을 버스로 지나는 개방형 동물원")],
   facts=dict(hours="빈원더스 9:00~19:30. 사파리 9:00 무렵~16:00 (나이트 사파리 19:00~21:00) · 방문 전 확인", fee="빈원더스 140cm 이상 1,050,000동, 100~140cm·60세 이상 800,000동. 사파리 140cm 이상 950,000동. 두 곳 묶음 1,700,000동부터 (2026년 기준)", stay="약 하루", when="오전 사파리 → 오후·저녁 빈원더스", access="푸꾸옥 북서쪽, 즈엉동에서 차로 약 1시간"),
   tips=["동물이 활발하고 덜 더운 9~11시에 사파리를 먼저 보고, 오후에 빈원더스로 넘어가 저녁 ONCE 쇼로 마무리해요.", "공식 사이트에서 표를 사면 QR코드가 이메일로 와서 매표 줄을 서지 않아요.", "두 곳 묶음표는 하루 유효·구역마다 한 번만 출입이라 같은 날 둘 다 보도록 일정을 잡아요."],
   src=[("VinWonders 공식 — VinWonders Phu Quoc opening hours (확인 2026.11.26)", "https://vinwonders.com/en/wonderpedia/news/vinwonders-phu-quoc-opening-hours/"), ("VinWonders 공식 — Review of Vinpearl Safari Phu Quoc (확인 2026.11.26)", "https://vinwonders.com/en/wonderpedia/news/review-of-vinpearl-safari-phu-quoc/")],
   checked="2026-11-26", photo=None),
}
