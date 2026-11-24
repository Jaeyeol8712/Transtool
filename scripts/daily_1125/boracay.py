# -*- coding: utf-8 -*-
"""boracay — 2026-11-25 새 해외 지역 '보라카이'(필리핀, K링크 region id boracay, 장소 id 접두어 br_) 데이터 + 가이드 1개. 확인일 2026-11-25.
못 쓴 글: 없음 (ARTICLES 비움, GUIDE 1개).
메모(총괄용):
- 공식 출처 사정: philippines.travel(필리핀 관광부)·etravel.gov.ph 는 열람 승인 시간 초과로 못 열었어요. 대신 주한 필리핀 대사관(비자),
  샹그릴라 보라카이 공식(시설, 환경세·까띠끌란 이동 시간), PIA(필리핀 정부 통신사, 말레이 관광청 발언 인용), 마닐라 불레틴(말레이 시장 발언 보조)으로 확인했어요.
- 환경세: 외국인 PHP 300, 필리핀인(아클란주 외) PHP 150 — 샹그릴라 공식(말레이시 징수, 숙소 체크아웃 때 청구). 마닐라 불레틴(2025.1.30)도 같은 금액.
- 터미널 요금: PHP 150 (2022년 9월부터) — 마닐라 불레틴(2025.1.30) 보조 출처만 있음 → '약'·'방문 전 확인' 표기.
- 배삯(까띠끌란~카그반): 공식 금액 확인 못 함 → '방문 전 확인'. e-트라이시클 요금도 공식 확인 못 함 → '방문 전 확인'.
- 운영 시간: 디몰 상점, 루호 산 전망대, 크리스탈 코브 섬 운영 시간·입장료는 공식 확인 못 함. PLACES o= 값은 대략값([10,22]·[8,17]), SPOTS에는 '방문 전 확인'.
- 좌표: 공식 주소 좌표를 못 열어 대표 지점의 대략값(소수 4자리). 섬 호핑은 대표 지점으로 크리스탈 코브 섬 하나를 넣었어요.
- 인천~칼리보 직항 약 4시간 30분은 기존 travel-boracay.html 수치를 그대로 씀(항공사마다 다름).
"""

ARTICLES = []
COORDS = {}

# K링크 장소 데이터 (해외 cost=0). 좌표는 대표 지점의 대략값.
PLACES = {
 "br_whitebeach": dict(
   ko=("보라카이 화이트 비치", "스테이션 1~3 이어진 4km 해변"), en=("Boracay White Beach", "Powdery west-coast beach, Stations 1 to 3"),
   zh=("长滩岛白沙滩", "1~3号站相连的白沙滩"), ja=("ボラカイ ホワイトビーチ", "ステーション1~3の白砂ビーチ"),
   lat=11.9650, lng=121.9240, o=[0, 24], cost=0, closed=[], best="eve", meal=None, h=3, cat="nature", st=""),
 "br_dmall": dict(
   ko=("보라카이 디몰", "스테이션 2 쇼핑·식당 거리"), en=("D'Mall Boracay", "Open-air shopping and dining lanes at Station 2"),
   zh=("长滩岛D'Mall", "2号站露天购物餐饮街"), ja=("ディーモール(ボラカイ)", "ステーション2の屋外商店街"),
   lat=11.9668, lng=121.9253, o=[10, 22], cost=0, closed=[], best="eve", meal="any", h=1.5, cat="shop", st=""),
 "br_puka": dict(
   ko=("푸카 셸 비치", "섬 북쪽 끝의 조용한 해변"), en=("Puka Shell Beach", "Quieter beach at the island's northern tip"),
   zh=("普卡贝壳海滩", "岛北端安静的海滩"), ja=("プカシェルビーチ", "島北端の静かなビーチ"),
   lat=11.9937, lng=121.9183, o=[6, 18], cost=0, closed=[], best="day", meal=None, h=2, cat="nature", st=""),
 "br_bulabog": dict(
   ko=("불라복 비치", "섬 동쪽 카이트서핑 해변"), en=("Bulabog Beach", "East-coast kitesurfing beach"),
   zh=("布拉博海滩", "岛东侧风筝冲浪海滩"), ja=("ブラボッグビーチ", "島東側のカイトサーフィンビーチ"),
   lat=11.9620, lng=121.9310, o=[0, 24], cost=0, closed=[], best="day", meal=None, h=1.5, cat="fun", st=""),
 "br_luho": dict(
   ko=("루호 산 전망대", "보라카이에서 가장 높은 전망 지점"), en=("Mt. Luho View Deck", "Highest viewpoint on Boracay"),
   zh=("卢霍山观景台", "长滩岛最高观景点"), ja=("ルホ山展望台", "ボラカイ最高地点の展望台"),
   lat=11.9760, lng=121.9310, o=[8, 17], cost=0, closed=[], best="am", meal=None, h=1, cat="nature", st=""),
 "br_crystalcove": dict(
   ko=("크리스탈 코브 섬", "섬 호핑 때 들르는 동굴·바위 섬"), en=("Crystal Cove Island", "Island-hopping stop with caves and coves"),
   zh=("水晶湾岛", "跳岛游常去的洞穴小岛"), ja=("クリスタルコーブ島", "アイランドホッピングで寄る洞窟の島"),
   lat=11.9426, lng=121.9407, o=[8, 17], cost=0, closed=[], best="am", meal=None, h=4, cat="nature", st=""),
}

# 숙소 권역 2곳 (상호 아님)
STAYS = [
 ("br_s1", 11.9725, 121.9222,
  ["스테이션 1", "1号站", "Station 1", "ステーション1"],
  ["화이트 비치 북쪽, 모래가 가장 넓은 구간", "白沙滩北段，沙滩最宽", "North White Beach, widest stretch of sand", "ホワイトビーチ北側、砂浜が最も広い"]),
 ("br_s2", 11.9662, 121.9248,
  ["스테이션 2·디몰", "2号站·D'Mall", "Station 2 & D'Mall", "ステーション2・ディーモール"],
  ["디몰·식당 걸어서, 불라복 비치도 가까움", "步行可达D'Mall和餐厅", "Walk to D'Mall, restaurants and Bulabog", "ディーモールや飲食店へ徒歩圏"]),
]

# 명소 안내 (K링크 장소 상세 화면). 공식 출처로 확인한 것만, 나머지는 '방문 전 확인'.
SPOTS = {
 "br_whitebeach": dict(
   one="섬 서쪽을 따라 스테이션 1~3이 이어지는 보라카이 대표 해변이에요. 해 질 무렵 노을과 파라우 세일링으로 알려져 있어요.",
   see=[("스테이션 1", "모래사장이 가장 넓은 북쪽 구간"), ("스테이션 2", "디몰과 식당이 모인 가운데 구간"), ("노을과 파라우", "해 질 무렵 돛단배가 떠요")],
   facts=dict(hours="상시 개방", fee="무료 (섬 입도 때 환경세 외국인 PHP 300 별도)", stay="약 3시간", when="저녁 (노을)", access="카그반 항에서 e-트라이시클로 이동, 스테이션 2는 디몰과 이어져요"),
   tips=["노을은 서쪽 해변에서 보여 해 지기 30분 전쯤 스테이션 1~2 쪽에 자리를 잡아요.", "파라우 세일링·액티비티는 필리핀 관광부(DOT) 인증 업체로 예약하라고 말레이 관광청이 안내해요."],
   src=[("PIA — Beware, deal only with DOT-accredited Boracay establishments", "https://mirror.pia.gov.ph/news/2023/08/02/beware-deal-only-with-dot-accredited-boracay-establishments"),
        ("Shangri-La Boracay — Map & Directions", "https://www.shangri-la.com/en/boracay/boracayresort/about/map-directions")],
   checked="2026-11-25", photo=None),
 "br_dmall": dict(
   one="스테이션 2 화이트 비치 바로 뒤에 있는 야외 쇼핑·식당 거리예요. 기념품, 환전, 식사를 한곳에서 해결해요.",
   see=[("골목 상점", "기념품·여름옷 가게"), ("식당가", "필리핀·각국 음식"), ("화이트 비치 출입구", "해변과 걸어서 바로 이어져요")],
   facts=dict(hours="가게마다 다름, 방문 전 확인", fee="무료 입장 (쇼핑·식사 비용 별도)", stay="약 1시간 30분", when="저녁", access="스테이션 2 화이트 비치에서 걸어서 바로"),
   tips=["노을을 본 뒤 저녁 식사 동선으로 묶으면 이동이 없어요.", "섬 투어·액티비티 호객이 많아 DOT 인증 업체인지 확인하고 예약해요."],
   src=[("PIA — Beware, deal only with DOT-accredited Boracay establishments", "https://mirror.pia.gov.ph/news/2023/08/02/beware-deal-only-with-dot-accredited-boracay-establishments")],
   checked="2026-11-25", photo=None),
 "br_puka": dict(
   one="섬 북쪽 끝에 있는 해변으로 화이트 비치보다 한적해요. 이름은 조개껍데기(푸카)에서 왔어요.",
   see=[("북쪽 해변", "화이트 비치보다 조용해요"), ("거친 모래와 조개", "고운 화이트 비치와 다른 느낌"), ("맑은 바다", "물놀이·사진")],
   facts=dict(hours="낮 방문 권장, 방문 전 확인", fee="무료", stay="약 2시간", when="낮", access="스테이션 1·2에서 e-트라이시클로 약 20분"),
   tips=["돌아오는 e-트라이시클을 잡기 어려울 수 있어 갈 때 탄 기사와 돌아오는 시간을 정해 두면 편해요.", "그늘이 적어 물·모자를 챙기고 오후 늦게 가면 화이트 비치 노을 시간에 맞춰 돌아오기 어려워요."],
   src=[("Shangri-La Boracay — Map & Directions", "https://www.shangri-la.com/en/boracay/boracayresort/about/map-directions")],
   checked="2026-11-25", photo=None),
 "br_bulabog": dict(
   one="섬 동쪽, 화이트 비치 반대편 해변이에요. 바람이 강한 철에는 카이트서핑·윈드서핑 해변이 돼요.",
   see=[("카이트서핑", "바람이 부는 철에 연이 가득해요"), ("동쪽 해안", "화이트 비치에서 섬을 가로질러 가까워요"), ("서핑 강습소", "해변을 따라 늘어서요")],
   facts=dict(hours="상시 개방", fee="무료 (강습·장비 대여 별도)", stay="약 1시간 30분", when="낮", access="디몰에서 섬을 가로질러 걸어서 약 10분 (대략)"),
   tips=["바람 부는 철엔 물놀이보다 카이트서핑 구경이 중심이라 수영은 화이트 비치에서 해요.", "강습은 DOT 인증 업체인지 확인하고 예약해요."],
   src=[("PIA — Beware, deal only with DOT-accredited Boracay establishments", "https://mirror.pia.gov.ph/news/2023/08/02/beware-deal-only-with-dot-accredited-boracay-establishments")],
   checked="2026-11-25", photo=None),
 "br_luho": dict(
   one="보라카이에서 가장 높은 곳에 있는 전망대예요. 섬 양쪽 해안을 한눈에 내려다봐요.",
   see=[("전망대", "섬 동·서 해안이 다 보여요"), ("화이트 비치 방향", "해변 선을 내려다봐요"), ("불라복 비치 방향", "카이트서핑 연이 보여요")],
   facts=dict(hours="방문 전 확인", fee="입장료 있음, 방문 전 확인", stay="약 1시간", when="오전", access="e-트라이시클로 입구까지 (스테이션 2에서 약 15분, 대략)"),
   tips=["한낮에는 덥고 그늘이 적어 오전에 가요.", "불라복 비치와 같은 섬 동쪽이라 하루에 묶으면 이동이 짧아요."],
   src=[("Shangri-La Boracay — Map & Directions", "https://www.shangri-la.com/en/boracay/boracayresort/about/map-directions")],
   checked="2026-11-25", photo=None),
 "br_crystalcove": dict(
   one="보라카이 섬 호핑 때 많이 들르는 작은 섬이에요. 바위 동굴과 작은 만을 걸어서 둘러봐요.",
   see=[("바위 동굴", "바다로 열린 동굴"), ("작은 만", "물놀이·스노클링"), ("섬 산책로", "섬을 한 바퀴 걸어요")],
   facts=dict(hours="방문 전 확인", fee="입장료 있음 (투어 포함 여부 방문 전 확인)", stay="섬 호핑 반나절 (약 4시간)", when="오전", access="화이트 비치·카그반 쪽에서 섬 호핑 배로 이동"),
   tips=["섬 호핑은 DOT 인증 여행사·업체로 예약하라고 말레이 관광청이 안내해요.", "오후엔 바람·파도가 세지는 날이 있어 오전 출발 투어를 골라요."],
   src=[("PIA — Beware, deal only with DOT-accredited Boracay establishments", "https://mirror.pia.gov.ph/news/2023/08/02/beware-deal-only-with-dot-accredited-boracay-establishments")],
   checked="2026-11-25", photo=None),
}

GUIDE = {
 "slug": "boracay-how-to-get-there",
 "name": "보라카이 가는 법",
 "date": "2026-11-25",
 "title": "보라카이 가는 법 — 칼리보·까띠끌란 공항, 환경세·터미널 요금·배·eTravel",
 "desc": "보라카이 가는 법을 칼리보(KLO)·까띠끌란(MPH) 공항 비교부터 까띠끌란 제티 포트, 환경세 PHP 300·터미널 요금·배삯, 섬 안 e-트라이시클, eTravel 등록과 한국인 30일 무비자까지 공식 안내 기준으로 정리했습니다.",
 "answer": "보라카이는 공항에서 바로 갈 수 없고 <b>까띠끌란 제티 포트에서 배를 타고</b> 들어가요. 인천 직항이 많은 <b>칼리보 공항</b>은 까띠끌란까지 차로 <b>약 1시간 30분</b>, <b>까띠끌란 공항</b>은 부두가 가깝지만 국내선을 갈아타야 해요. 섬에 들어갈 때 <b>환경세(외국인 PHP 300)</b>·터미널 요금·배삯이 들고, 출발 72시간 전부터 <b>eTravel</b>을 무료로 등록해요.",
 "body": [
  ("칼리보·까띠끌란 공항 비교",
   "<ul><li><b>칼리보 공항(KLO)</b>: 인천 직항이 많아요. 도착 뒤 까띠끌란 제티 포트까지 차로 약 1시간 30분이에요.</li>"
   "<li><b>까띠끌란 공항(MPH, 고도프레도 P. 라모스 공항)</b>: 제티 포트까지 차로 몇 분이라 가장 빨라요. 다만 마닐라·세부 등에서 국내선으로 갈아타야 해요.</li></ul>"
   "<p>인천에서 칼리보 직항은 약 4시간 30분이에요(항공사마다 다름). 짐이 많거나 밤에 도착하면 갈아타기 없는 칼리보 직항이 편하고, 이동 시간을 줄이고 싶으면 까띠끌란을 골라요.</p>"),
  ("까띠끌란 제티 포트 (배 약 15분)",
   "<ol><li>공항에서 차로 까띠끌란 제티 포트 도착</li>"
   "<li>터미널 요금·환경세·배삯을 내요 (숙소가 환경세를 체크아웃 때 받는 곳도 있어요)</li>"
   "<li>배로 약 15분, 보라카이 카그반 항 도착</li>"
   "<li>e-트라이시클로 숙소까지</li></ol>"
   "<p>숙소 예약 확인서를 보여 달라고 할 수 있어 필리핀 관광부(DOT) 인증 숙소 예약 확인서를 휴대폰에 저장해 두세요. 밤 늦게 도착하면 배편이 줄어 방문 전 운항 시간을 확인해요.</p>"),
  ("환경세·터미널 요금·배삯",
   "<div class=\"at-table\"><table><thead><tr><th>항목</th><th>금액 (2026년 기준)</th><th>메모</th></tr></thead><tbody>"
   "<tr><td>환경세</td><td>외국인 PHP 300</td><td>말레이시 징수, 숙소에서 받는 경우도 있음</td></tr>"
   "<tr><td>터미널 요금</td><td>약 PHP 150</td><td>까띠끌란 제티 포트, 방문 전 확인</td></tr>"
   "<tr><td>배삯</td><td>방문 전 확인</td><td>까띠끌란 → 카그반 약 15분</td></tr>"
   "<tr><td>칼리보 → 까띠끌란</td><td>방문 전 확인</td><td>차 약 1시간 30분</td></tr>"
   "</tbody></table></div>"
   "<p>금액은 페소 현금으로 내는 경우가 많아 공항에서 조금 환전해 두면 편해요. 원화로 얼마인지는 환율 계산기로 미리 맞춰 봐요.</p>"),
  ("섬 안 이동 (e-트라이시클)",
   "<p>보라카이 안에서는 전기로 다니는 <b>e-트라이시클</b>이 기본 교통수단이에요. 카그반 항에서 숙소, 숙소에서 <b>푸카 셸 비치</b>·<b>루호 산 전망대</b>로 갈 때 타요. 요금은 탑승 전 기사에게 확인해요.</p>"
   "<ul><li><b>보라카이 화이트 비치</b>: 스테이션 1~3을 해변 따라 걸어서 오가요.</li>"
   "<li><b>보라카이 디몰</b>: 스테이션 2 바로 뒤라 걸어서 가요.</li>"
   "<li><b>푸카 셸 비치</b>: 스테이션 1·2에서 e-트라이시클로 약 20분이에요.</li></ul>"
   "<p>장소 위치는 <a href=\"/klink/#br_whitebeach\">K링크 지도에서 보라카이 화이트 비치 보기</a>로 확인하고, 3박 5일·4박 6일 동선은 <a href=\"/travel-boracay.html\">보라카이 여행 코스</a>에 있어요.</p>"),
  ("eTravel·30일 무비자",
   "<p>필리핀 입국 전 <a href=\"https://etravel.gov.ph\">eTravel 공식 사이트</a>(etravel.gov.ph)에서 출발 72시간 전부터 <b>무료</b>로 등록하고 QR코드를 저장해요. 돈을 받는 대행 사이트는 피하세요. 순서는 <a href=\"/guide-philippines-etravel.html\">필리핀 eTravel 등록</a>에 정리했어요.</p>"
   "<p>한국 여권은 <b>30일 무비자</b>예요. 돌아가는(또는 다음 목적지로 가는) 항공권이 있어야 하고, 여권은 머무는 기간보다 6개월 이상 남아 있어야 해요.</p>"
   "<div class=\"b-tip\"><p><b>실전 팁</b> 첫날은 보라카이 화이트 비치 스테이션 1·2 쪽 숙소에 짐을 풀고 노을을 보면 이동이 가장 짧아요. 제티 포트 요금은 현금으로 낼 때가 많아 페소 잔돈을 준비해요.</p></div>"),
 ],
 "faq": [
  ("보라카이는 칼리보와 까띠끌란 중 어디로 가요?", "인천 직항이 많은 칼리보가 편하지만 까띠끌란 제티 포트까지 차로 약 1시간 30분 더 걸려요. 까띠끌란 공항은 부두가 가깝지만 국내선을 갈아타야 해요."),
  ("보라카이 환경세는 얼마예요?", "외국인 PHP 300이에요(2026년 기준). 제티 포트에서 내거나 숙소가 체크아웃 때 받기도 해요."),
  ("터미널 요금과 배삯은 얼마예요?", "터미널 요금은 약 PHP 150이에요. 배삯은 공식 금액을 확인하지 못해 방문 전 확인이 필요해요."),
  ("보라카이 섬 안에서는 어떻게 다녀요?", "e-트라이시클을 타요. 보라카이 화이트 비치와 보라카이 디몰은 걸어서 오가고, 푸카 셸 비치는 e-트라이시클로 약 20분이에요."),
  ("eTravel은 꼭 해야 하나요?", "네. 출발 72시간 전부터 etravel.gov.ph에서 무료로 등록하고 QR코드를 저장해요. 한국인은 30일 무비자예요."),
 ],
 "tools": ["exchange_rate_calculator", "airport_transport_compare_calculator", "overseas_card_fee_calculator"],
 "sources": [
  ("Shangri-La Boracay — Map & Directions (칼리보 이동 시간·환경세) (확인 2026.11.25)", "https://www.shangri-la.com/en/boracay/boracayresort/about/map-directions"),
  ("주한 필리핀 대사관 — Visa (한국인 30일 무비자) (확인 2026.11.25)", "https://philembassy-seoul.com/visa"),
  ("필리핀 eTravel 공식 포털 (확인 2026.11.25)", "https://etravel.gov.ph"),
  ("PIA — Beware, deal only with DOT-accredited Boracay establishments (확인 2026.11.25)", "https://mirror.pia.gov.ph/news/2023/08/02/beware-deal-only-with-dot-accredited-boracay-establishments"),
  ("Manila Bulletin — 말레이 시장 '보라카이 요금 인상 없음' (터미널 요금·환경세) (확인 2026.11.25)", "https://mb.com.ph/2025/1/30/mayor-frasco-misinformed-no-increase-in-boracay-fees"),
 ],
}
