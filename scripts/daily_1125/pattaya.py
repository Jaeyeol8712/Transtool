# -*- coding: utf-8 -*-
"""pattaya — 2026-11-25 새 해외 지역 '파타야'(K링크 region id pattaya, 장소 id 접두어 pt_) 데이터 + 코타키나발루 공항 가이드 1개. 확인일 2026-11-25.
장소: travel-pattaya.html 에 나오는 7곳(꼬란·진리의 성전·파타야 뷰포인트·워킹 스트리트·농눅 빌리지·좀티엔 해변·파타야 비치).
못 쓴 것: 없음.
메모(출처): 태국관광청(tourismthailand.org)은 이 환경에서 열리지 않았어요(프록시 차단·WebFetch 실패). 꼬란·프라탐낙 뷰포인트·농눅 TAT 페이지는
  검색으로 있는 것만 확인했고, 숫자는 시설 공식(sanctuaryoftruthmuseum.com, nongnoochpattaya.com)과 파타야 현지 언론 Pattaya Mail(시 발표·현장 보도)로 확인했어요.
메모(확인 못 한 숫자): 농눅 빌리지 외국인 입장료(공식 예약 페이지에 금액이 표시되지 않음) -> '방문 전 확인'. 꼬란 배 첫·막배 시각, 워킹 스트리트 차 없는 거리 시각,
  좀티엔·파타야 비치 썬베드 요금 -> 숫자 안 씀. 꼬란 공영 배 약 30바트·약 45분은 Pattaya Mail 2026년 8월 기사 기준.
메모(코타키나발루): Malaysia Airports KKIA 대중교통 페이지는 택시 쿠폰·시내버스 '타는 곳(도착층 1층)'만 있고 요금·노선이 없어 '방문 전 확인'.
  그랩 KKIA 승차 지점(문 번호)은 그랩 공식 안내를 찾지 못해 '앱의 지정 승차 구역(Pick Up Area)'으로만 적음. 공항~시내 km는 공식 숫자를 못 찾아 '차로 약 15분'만 씀.
  제셀톤 포인트 배는 공사로 임시로 코타키나발루 항 사우스 제티(South Jetty)에서 떠남(jesseltonpoint.com.my, 2026.11.25 확인).
"""

ARTICLES = []
COORDS = {}

PLACES = {
 "pt_kohlarn": dict(ko=("꼬란 (산호섬)", "발리하이 부두에서 배로 가는 섬"), en=("Koh Larn (Coral Island)", "Island reached by ferry from Bali Hai Pier"), zh=("格兰岛 (珊瑚岛)", "从巴厘海码头坐船上岛"), ja=("ラン島 (コーラル島)", "バリハイ桟橋から船で渡る島"),
   lat=12.9195, lng=100.7815, o=[7, 18], cost=0, closed=[], best="day", meal="any", h=6, cat="nature", st="Koh Larn, Na Kluea, Bang Lamung, Chon Buri (Bali Hai Pier 출발)"),
 "pt_sanctuary": dict(ko=("진리의 성전", "나무로만 지은 거대한 바닷가 성전"), en=("Sanctuary of Truth", "Seaside temple-museum carved entirely of wood"), zh=("真理寺", "全木雕刻的海边寺庙博物馆"), ja=("サンクチュアリー・オブ・トゥルース", "木彫りだけで造られた海辺の寺院"),
   lat=12.9726, lng=100.8890, o=[8, 18], cost=0, closed=[], best="am", meal=None, h=1.5, cat="palace", st="206/2 Moo 5, Pattaya-Naklua Rd (Soi Naklua 12), Bang Lamung, Chon Buri"),
 "pt_viewpoint": dict(ko=("파타야 뷰포인트 (프라탐낙 언덕)", "파타야 만과 꼬란이 보이는 언덕"), en=("Pattaya Viewpoint (Pratumnak Hill)", "Hilltop view over Pattaya Bay and Koh Larn"), zh=("芭提雅观景台 (帕塔纳克山)", "俯瞰芭提雅湾与格兰岛"), ja=("パタヤ・ビューポイント (プラタムナックの丘)", "パタヤ湾とラン島を望む丘"),
   lat=12.9198, lng=100.8678, o=[0, 24], cost=0, closed=[], best="eve", meal=None, h=0.7, cat="nature", st="Pratumnak Hill, Pattaya (사우스 파타야와 좀티엔 사이)"),
 "pt_walking": dict(ko=("파타야 워킹 스트리트", "해변로 남쪽 끝의 밤거리"), en=("Pattaya Walking Street", "Nightlife street at the south end of Beach Road"), zh=("芭提雅步行街", "海滩路南端的夜生活街"), ja=("パタヤ・ウォーキングストリート", "ビーチロード南端の夜の通り"),
   lat=12.9270, lng=100.8718, o=[18, 24], cost=0, closed=[], best="night", meal="any", h=1.5, cat="night", st="Walking Street, South Pattaya (Beach Rd 남쪽 끝~발리하이 부두)"),
 "pt_nongnooch": dict(ko=("농눅 빌리지 (농눅 트로피컬 가든)", "식물 1만 8천여 종의 대형 정원"), en=("Nong Nooch Tropical Garden", "Huge garden with 18,000+ plants and Thai shows"), zh=("东芭乐园 (农诺热带植物园)", "收集一万八千多种植物的大型花园"), ja=("ノンヌッチ・トロピカルガーデン", "1万8千種以上の植物が集まる大庭園"),
   lat=12.7646, lng=100.9349, o=[8, 18], cost=0, closed=[], best="day", meal="any", h=4, cat="nature", st="34/1 Moo 7, Na Jomtien, Sattahip, Chon Buri"),
 "pt_jomtien": dict(ko=("좀티엔 해변", "파타야 남쪽의 길고 조용한 해변"), en=("Jomtien Beach", "Long, quieter beach south of Pattaya"), zh=("宗甸海滩", "芭提雅南边安静的长海滩"), ja=("ジョムティエン・ビーチ", "パタヤ南側の長く静かな浜"),
   lat=12.8870, lng=100.8705, o=[0, 24], cost=0, closed=[], best="eve", meal=None, h=2, cat="nature", st="Jomtien Beach Rd, Na Jomtien, Bang Lamung, Chon Buri"),
 "pt_beach": dict(ko=("파타야 비치", "시내 중심 해변로를 따라 놓인 해변"), en=("Pattaya Beach", "City beach along Beach Road"), zh=("芭提雅海滩", "沿海滩路的市中心海滩"), ja=("パタヤ・ビーチ", "ビーチロード沿いの街なかの浜"),
   lat=12.9370, lng=100.8835, o=[0, 24], cost=0, closed=[], best="eve", meal=None, h=1.5, cat="nature", st="Pattaya Beach Rd, Bang Lamung, Chon Buri"),
}

STAYS = [
 ("pt_stay_beach", 12.9370, 100.8850, ["파타야 비치로드 주변", "芭提雅海滩路周边", "Pattaya Beach Road", "パタヤ・ビーチロード周辺"],
  ["워킹 스트리트·발리하이 부두 가깝고 썽태우 타기 쉬움", "近步行街和巴厘海码头，双条车方便", "Near Walking Street and Bali Hai Pier, easy baht buses", "ウォーキングストリートとバリハイ桟橋に近くソンテウも便利"]),
 ("pt_stay_jomtien", 12.8850, 100.8720, ["좀티엔 해변 주변", "宗甸海滩周边", "Jomtien Beach", "ジョムティエン・ビーチ周辺"],
  ["조용한 해변 숙소, 가족 여행과 농눅 빌리지 가기 좋음", "安静的海滩住宿，适合家庭和去东芭乐园", "Quieter beach stays, good for families and Nong Nooch", "静かな浜の宿、家族旅行やノンヌッチに便利"]),
]

SPOTS = {
 "pt_kohlarn": dict(
   one="파타야 앞바다의 섬으로, 발리하이 부두에서 배를 타고 가요. 따웬·티엔·누안·사메 해변이 섬에 흩어져 있어요.",
   see=[("따웬 해변", "가장 붐비고 시설이 많은 해변"), ("사메 해변", "모래사장이 넓고 노을이 보여요"), ("나반 부두", "공영 배가 닿는 섬의 마을")],
   facts=dict(hours="배는 낮 동안 수시 운항, 돌아오는 배는 대개 이른 저녁에 끝나요 (방문 전 부두에서 확인)", fee="공영 배 편도 약 30바트, 스피드보트 1인 약 150~300바트 (2026년 기준)", stay="반나절~하루", when="11~4월, 오전 출발", access="발리하이 부두(워킹 스트리트 끝)에서 공영 배 약 45분, 스피드보트 약 15~20분"),
   tips=["표는 발리하이 부두 매표소에서 사고 길거리 호객꾼에게 사지 않아요.", "섬 ATM은 붐빌 때 쓰기 어려워 썽태우·썬베드 값은 현금으로 챙겨 가요.", "5~10월은 파도가 높아 스피드보트가 멈출 수 있으니 공영 배 막배 시각을 먼저 확인해요."],
   src=[("Pattaya Mail — Pattaya to Koh Larn ferry times, prices and beach guide 2026", "https://www.pattayamail.com/latestnews/news/how-to-get-from-pattaya-to-koh-larn-ferry-times-prices-and-beach-guide-for-2026-561423"), ("태국관광청 — Ko Lan", "https://www.tourismthailand.org/Attraction/ko-lan")],
   checked="2026-11-25", photo=None),
 "pt_sanctuary": dict(
   one="나끄루아 바닷가에 못 없이 나무로만 지은 성전이에요. 지금도 조각 작업이 이어지고 있어요.",
   see=[("목조 성전 외관", "바다를 등진 높은 나무 건물"), ("목각 공방", "장인이 조각하는 모습을 볼 수 있어요"), ("타이 음악 공연", "식음료 홀에서 상시 공연")],
   facts=dict(hours="매일 낮 관람 08:00~18:00(표 판매 17:00까지), 야간 관람 18:20~20:30(표 판매 17:30~19:30)", fee="낮 성인 500바트, 키 110~140cm 어린이 250바트 / 야간 성인 700바트, 어린이 350바트, 110cm 미만 무료 (2026년 기준)", stay="약 1시간 30분", when="오전", access="파타야 시내 북쪽 나끄루아 소이 12, 시내에서 차로 약 15분"),
   tips=["안에서는 안전모를 써야 하고 노출 있는 옷이면 보증금 200바트를 내고 숄·사롱을 빌려요.", "한국어 오디오·가이드 투어 시간이 요일마다 달라 공식 사이트 시간표를 보고 맞춰 가요.", "드론 촬영·동영상 촬영과 음식·음료 반입은 안 돼요."],
   src=[("Sanctuary of Truth Museum 공식 — Visit Us", "https://sanctuaryoftruthmuseum.com/visit-us/"), ("Sanctuary of Truth Museum 공식 — Entrance Ticket", "https://sanctuaryoftruthmuseum.com/shop/sanctuary-of-truth-entrance-ticket/")],
   checked="2026-11-25", photo=None),
 "pt_viewpoint": dict(
   one="사우스 파타야와 좀티엔 사이 프라탐낙 언덕의 전망대예요. 위에 파타야 시 사인이 있고 무료로 24시간 열려 있어요.",
   see=[("파타야 만 전망", "파타야 비치가 한눈에 보여요"), ("꼬란과 발리하이 부두", "바다 건너 섬과 부두"), ("파타야 시 사인", "전망대 바로 위 글자 조형물")],
   facts=dict(hours="상시", fee="무료", stay="약 40분", when="해 질 녘 또는 이른 아침", access="워킹 스트리트·발리하이 부두에서 언덕길로 차·오토바이 택시"),
   tips=["노을 무렵에는 전망대가 붐벼 해 지기 30분 전쯤 도착해 자리를 잡아요.", "낮에는 그늘이 적고 더워 아침이나 저녁 시간을 골라요."],
   src=[("Pattaya Mail — Pattaya City Sign viewpoint (Pratumnak Hill)", "https://www.pattayamail.com/latestnews/news/above-and-beyond-pattaya-city-sign-delivers-breath-taking-views-of-the-beach-city-for-free-358254"), ("태국관광청 — Phra Tamnak Mountain Viewpoint", "https://www.tourismthailand.org/Attraction/phra-tamnak-mountain-viewpoint")],
   checked="2026-11-25", photo=None),
 "pt_walking": dict(
   one="파타야 비치로드 남쪽 끝에서 발리하이 부두 쪽으로 이어지는 밤거리예요. 밤에는 오토바이까지 차가 다니지 않아요.",
   see=[("3D LED 입구 사인", "2025년 새로 단 돌고래 캐릭터 화면"), ("밤거리 식당·바", "저녁부터 새벽까지 문 열어요"), ("발리하이 부두 쪽 끝", "꼬란 가는 배 타는 곳")],
   facts=dict(hours="저녁~새벽, 가게마다 다름 (입구 LED 16:00~04:00)", fee="무료 (가게 이용 비용 별도)", stay="약 1시간 30분", when="밤", access="파타야 비치로드 남쪽 끝, 썽태우로 비치로드를 따라 내려와요"),
   tips=["밤에 차가 다니지 않으니 썽태우·그랩은 비치로드 쪽 입구에서 내리고 타요.", "가게 앞 호객과 가격표 없는 메뉴는 주문 전에 값을 먼저 확인해요."],
   src=[("Pattaya Mail — New 3D LED Walking Street entrance (2025.8)", "https://www.pattayamail.com/latestnews/news/pattaya-unveils-new-3d-led-walking-street-with-adorable-dolphin-mascot-to-welcome-tourists-515667"), ("Pattaya Mail — Walking Street back to feet only", "https://www.pattayamail.com/latestnews/news/pattayas-walking-street-back-to-feet-only-399060")],
   checked="2026-11-25", photo=None),
 "pt_nongnooch": dict(
   one="파타야 남쪽 사타힙의 대형 열대 정원이에요. 식물 1만 8천여 종을 모았고 타이 전통 공연을 하루 네 번 해요.",
   see=[("뷰티풀 가든", "꽃과 조형으로 꾸민 대표 정원"), ("다이노서 밸리", "공룡 조형물이 있는 정원"), ("타이 전통 공연", "10:30·11:30·13:30·15:30")],
   facts=dict(hours="매일 08:00~18:00, 쉬는 날 없음", fee="방문 전 확인 (공식 예약 페이지·전화로 확인)", stay="약 4시간", when="오전~낮", access="사타힙군 나쫌티엔, 파타야에서 차로 남쪽 이동"),
   tips=["타이 전통 공연 시간(10:30·11:30·13:30·15:30)에 맞춰 정원 동선을 짜요.", "공식 사이트에서 예약한 표는 예약일부터 5일 동안 쓸 수 있어요.", "정원이 넓고 그늘이 적어 오전에 들어가 더운 낮에는 공연장에서 쉬어요."],
   src=[("Nong Nooch Tropical Garden 공식 — Beautiful Garden", "https://www.nongnoochpattaya.com/en/beautiful-garden"), ("Nong Nooch Tropical Garden 공식 — Thai Cultural Performances", "https://www.nongnoochpattaya.com/en/event/1"), ("태국관광청 — Nong Nooch Tropical", "https://www.tourismthailand.org/Attraction/nong-nooch-tropical")],
   checked="2026-11-25", photo=None),
 "pt_jomtien": dict(
   one="프라탐낙 언덕 남쪽으로 길게 이어진 해변이에요. 파타야 비치보다 조용해 가족 숙소가 많아요.",
   see=[("넓어진 모래사장", "1단계 복원으로 폭 약 50m"), ("해변 산책로", "해변을 따라 걷는 길"), ("해 질 녘 바다", "서쪽 바다로 지는 노을")],
   facts=dict(hours="상시", fee="무료", stay="약 2시간", when="오후~해 질 녘", access="사우스 파타야에서 썽태우로 갈아타 이동(직행 없으면 사우스 파타야에서 환승)"),
   tips=["좀티엔 소이 11~소이 10 구간은 2027년 7월까지 모래 복원 공사 중이라 다른 구간으로 들어가요.", "파타야 중심과 바로 잇는 썽태우가 드물어 사우스 파타야에서 한 번 갈아타는 것을 염두에 둬요."],
   src=[("Pattaya Mail — Jomtien Beach expansion (2026.11.19)", "https://www.pattayamail.com/news/jomtien-beach-expansion-reaches-lifeguard-zone-aims-for-50-metre-wide-shoreline-572433"), ("Pattaya Mail — Pattaya baht buses", "https://www.pattayamail.com/news/dont-look-confused-be-determined-pattaya-baht-buses-still-a-bargain-but-tourists-call-for-more-routes-fewer-rip-offs-504219")],
   checked="2026-11-25", photo=None),
 "pt_beach": dict(
   one="파타야 시내 비치로드를 따라 놓인 중심 해변이에요. 남쪽 끝이 워킹 스트리트, 그 너머가 발리하이 부두예요.",
   see=[("비치로드 산책", "야자수 따라 걷는 해변길"), ("서쪽 노을", "만 너머로 지는 해"), ("썽태우 노선", "비치로드를 도는 합승 트럭")],
   facts=dict(hours="상시", fee="무료", stay="약 1시간 30분", when="해 질 녘", access="비치로드·세컨드로드 썽태우 1회 10~20바트 (2025년 기준)"),
   tips=["썽태우는 손을 들어 타고 내릴 때 버저를 누른 뒤 요금을 내요. 처음부터 '전세'로 타면 값이 크게 올라가요.", "개인 돗자리·의자는 가져가도 되지만 텐트·야영·모닥불·큰 음악은 시가 금지해요(2026년 4월 단속)."],
   src=[("Pattaya Mail — Pattaya allows free beach use with personal gear (2026.4)", "https://www.pattayamail.com/news/pattaya-allows-free-beach-use-with-personal-gear-but-bans-tents-and-loud-music-546793"), ("Pattaya Mail — Pattaya baht buses", "https://www.pattayamail.com/news/dont-look-confused-be-determined-pattaya-baht-buses-still-a-bargain-but-tourists-call-for-more-routes-fewer-rip-offs-504219")],
   checked="2026-11-25", photo=None),
}

GUIDE = {
 "slug": "kota-kinabalu-airport-to-city", "name": "코타키나발루 공항에서 시내", "date": "2026-11-25",
 "title": "코타키나발루 공항에서 시내 — 그랩·택시 쿠폰·공항버스, 워터프런트·제셀톤 포인트까지",
 "desc": "코타키나발루 공항(KKIA)에서 시내까지 차로 약 15분, 그랩 승차와 도착층 택시 쿠폰 카운터, 시내버스 타는 곳, 워터프런트·야시장과 사피섬·마누칸섬 배 타는 제셀톤 포인트(임시 사우스 제티) 요금까지 정리했습니다.",
 "answer": "코타키나발루 공항(KKIA)에서 시내는 <b>차로 약 15분</b>이라 짐이 있으면 <b>그랩</b>이나 <b>쿠폰 택시</b>가 가장 편해요. 택시 쿠폰 카운터와 시내버스 타는 곳은 모두 <b>터미널 도착층(1층)</b>에 있고, 택시는 목적지별로 요금이 정해져 있어요. 사피섬·마누칸섬 배는 지금 <b>코타키나발루 항 사우스 제티</b>에서 떠나요(제셀톤 포인트 공사 중).",
 "body": [
  ("공항 도착 (KKIA 터미널)",
   "<p>코타키나발루 국제공항(KKIA, 공항 코드 BKI)은 시내 남서쪽 탄중아루 쪽에 있어요. Sabah Tourism은 시내까지 <b>차로 약 15분</b>으로 안내해요.</p>"
   "<p>도착하면 <b>1층(Level 1) 도착층</b>으로 나와요. 택시 쿠폰 카운터와 시내버스 타는 곳이 모두 이 층에 있어요. 1층에는 24시간 짐 보관 서비스도 있는데 현금·전자지갑만 받아요.</p>"
   "<p>말레이시아 입국 전에는 디지털 입국카드(MDAC)를 꼭 내야 해요. 방법은 <a href=\"/guide-malaysia-mdac.html\">말레이시아 MDAC 입국 준비</a>에 정리했어요.</p>"),
  ("그랩·택시 쿠폰 (시내 약 15분)",
   "<ul><li><b>그랩</b>: 앱에서 부르면 기사가 공항 대기 주차장에서 와요. 앱이 알려 주는 <b>지정 승차 구역(Pick Up Area)</b>에서 타요. Maxim·AirAsia Ride 같은 다른 호출 앱도 사바주에서 쓰여요.</li>"
   "<li><b>쿠폰 택시</b>: 도착층 1층 카운터에서 목적지를 말하고 쿠폰을 사요. 요금은 목적지별로 정해져 있고 금액은 방문 전 확인이에요.</li>"
   "<li><b>호객 차량은 타지 않아요</b>: 허가 없는 영업 차량(kereta sapu)은 경찰·도로교통국 단속 대상이에요.</li></ul>"
   "<p>시내 숙소가 워터프런트·야시장 근처라면 그랩이나 쿠폰 택시로 바로 가는 편이 갈아타기가 없어 편해요.</p>"),
  ("공항버스 (시내버스)",
   "<p>Malaysia Airports는 공항에서 시내로 가는 <b>시내버스</b>를 도착층 1층 도착 홀에서 탄다고 안내해요. 노선·요금·배차 간격은 공식 페이지에 나와 있지 않아 <b>방문 전 확인</b>이 필요해요.</p>"
   "<p>밤늦게 도착하거나 짐이 많으면 버스 시간에 맞추기보다 그랩·쿠폰 택시를 타는 편이 확실해요. 원화로 얼마인지는 아래 공항 교통비 비교 계산기와 환율 계산기로 맞춰 봐요.</p>"),
  ("시내에서 사피섬·마누칸섬 배 (제셀톤 포인트)",
   "<p>사피섬·마누칸섬이 있는 툰쿠 압둘 라만 해양공원 배는 제셀톤 포인트 터미널이 운영해요. 지금은 공사로 <b>코타키나발루 항 사우스 제티(Jalan Tun Fuad Stephens, JQ 센트럴 주차장 근처)</b>에서 떠나요. 공항에서 택시·그랩으로 약 15분, 시내 가야 거리에서 걸어서 약 15~20분이에요.</p>"
   "<ul><li>터미널 운영: 매일 07:30~17:00</li>"
   "<li>사피섬까지 배로 약 30분</li>"
   "<li>섬 1곳 성인 RM48·어린이 RM43, 섬 2곳 성인 RM58·어린이 RM53 (터미널 이용료 포함, 2026년 기준)</li>"
   "<li>해양공원 보호비 외국인 성인 RM25·어린이 RM20은 따로 안내돼 있어 표 살 때 확인</li></ul>"
   "<p>워터프런트·야시장은 사우스 제티와 같은 바닷가 시내 쪽이라 섬에서 돌아온 저녁에 걸어서 묶기 좋아요. 탄중아루 해변은 공항 쪽이라 마지막 날 노을을 보고 공항으로 가는 동선이 편해요.</p>"),
  ("구간별 정리",
   "<div class=\"at-table\"><table><thead><tr><th>구간</th><th>수단</th><th>시간(약)</th><th>요금</th></tr></thead><tbody>"
   "<tr><td>공항 → 시내</td><td>그랩</td><td>15분</td><td>앱에서 확인</td></tr>"
   "<tr><td>공항 → 시내</td><td>쿠폰 택시</td><td>15분</td><td>목적지별 고정, 방문 전 확인</td></tr>"
   "<tr><td>공항 → 시내</td><td>시내버스</td><td>도로 사정 따라 다름</td><td>방문 전 확인</td></tr>"
   "<tr><td>사우스 제티 → 사피섬</td><td>배</td><td>30분</td><td>섬 1곳 RM48, 2곳 RM58 (성인)</td></tr>"
   "<tr><td>해양공원 보호비</td><td>-</td><td>-</td><td>외국인 성인 RM25</td></tr>"
   "</tbody></table></div>"
   "<p>장소 위치는 <a href=\"/klink/#kk_waterfront\">K링크 지도에서 워터프런트·야시장 보기</a>로 확인하고, 사피섬·마누칸섬·탄중아루 해변을 묶은 일정은 <a href=\"/travel-kotakinabalu.html\">코타키나발루 여행 코스</a>에 있어요.</p>"
   "<div class=\"b-tip\"><p><b>실전 팁</b> 섬 배 터미널은 17:00에 닫아요. 첫날 오후에 도착하면 섬은 다음 날 오전으로 미루고, 첫 저녁은 숙소에서 가까운 워터프런트·야시장으로 가요.</p></div>"),
 ],
 "faq": [
  ("코타키나발루 공항에서 시내까지 얼마나 걸려요?", "차로 약 15분이에요(Sabah Tourism 안내). 그랩이나 쿠폰 택시가 가장 빨라요."),
  ("택시 쿠폰은 어디서 사요?", "터미널 도착층(1층)의 택시 쿠폰 카운터에서 사요. 요금은 목적지별로 정해져 있고 금액은 방문 전 확인이에요."),
  ("공항버스가 있나요?", "도착층 1층 도착 홀에서 시내버스를 타요. 노선·요금은 공식 안내에 없어 방문 전 확인이 필요해요."),
  ("사피섬·마누칸섬 배는 어디서 타요?", "제셀톤 포인트 공사로 지금은 코타키나발루 항 사우스 제티에서 타요. 섬 1곳 성인 RM48, 2곳 RM58이고 해양공원 보호비(외국인 성인 RM25)는 따로 확인해요."),
  ("입국 전에 준비할 서류가 있나요?", "말레이시아 디지털 입국카드(MDAC)를 도착 전에 무료로 내야 해요. 공식 사이트에서만 작성해요."),
 ],
 "tools": ["airport_transport_compare_calculator", "exchange_rate_calculator", "overseas_card_fee_calculator"],
 "sources": [
  ("Malaysia Airports — KKIA Public Transport (택시 쿠폰·시내버스) (확인 2026.11.25)", "https://airports.malaysiaairports.com.my/kota-kinabalu/getting-around/transport/public-transport"),
  ("Sabah Tourism — Getting Around (확인 2026.11.25)", "https://sabahtourism.com/essential/getting-around/"),
  ("Sabah Tourism — 7 helpful ways to fill time before your departure flight (확인 2026.11.25)", "https://sabahtourism.com/article/7-helpful-ways-to-fill-time-before-your-departure-flight/"),
  ("Grab — KKIA Queue Feature (확인 2026.11.25)", "https://www.grab.com/my/blog/driver/car/kkia-queue-feature/"),
  ("Jesselton Point Ferry Terminal 공식 (확인 2026.11.25)", "https://jesseltonpoint.com.my/"),
  ("Jesselton Point — Sapi Island 요금 (확인 2026.11.25)", "https://jesseltonpoint.com.my/islands/sapi/"),
  ("Sabah Tourism — Jesselton Point Waterfront (확인 2026.11.25)", "https://sabahtourism.com/destination/jesselton-point-waterfront/"),
  ("The Star — Visit Sabah 2027 앞두고 불법 영업 차량 단속 (확인 2026.11.25)", "https://thestar.com.my/news/nation/2026/11/24/on-ground-issues-being-tackled-ahead-of-visit-sabah-2027"),
 ],
}
