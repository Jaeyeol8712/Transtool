# -*- coding: utf-8 -*-
"""phuket — 2026-11-21 매일 콘텐츠(새 지역 담당: 푸켓, region id phuket). 확인일 2026-11-21. 못 쓴 글: 없음
메모(장소 대체): 기존 가이드 travel-phuket.html 에 '왓 찰롱'과 '카론 뷰포인트'가 없어 대체했습니다.
  - pk_chalong(왓 찰롱) → pk_promthep(프롬텝 곶): 가이드 DAY 3 '올드타운 → 빅붓다 → 프롬텝 곶 노을' 동선 그대로.
  - pk_karon(카론 뷰포인트) → id 유지, 이름 '까론 비치'(가이드 표기 '까론·까따 해변'), 좌표 해변 쪽으로 변경.
메모(확인 애매): 라사다 항의 피피섬 노선은 2001년 개항 보도·2018년 주지사 방문 보도로 확인했고, 공식 시간표는 찾지 못했습니다(운항사 확인).
  피피섬 국립공원 요금 외국인 성인 400·어린이 200바트는 2022년 DNP 고시·2024년 공원장 발표 보도 기준.
  팡아만 국립공원 입장료, 프롬텝 곶 등대 운영 시간, 락 디(라트야이) 마켓 끝나는 시간은 공식 근거를 찾지 못해 '방문 전 확인'.
  빅 부다는 2024년 8월 산사태 뒤 닫혔다가 2026년 3월 3일 재개장(매일 09:00~18:00, 왓 까따 관리) 보도 기준."""
ARTICLES = [
 dict(
  kind="trip",
  slug="travel-phuket-phiphi",
  region="phuket",
  places=["pk_phiphi", "pk_phangnga"],
  kw=("피피섬", 2300),
  name="피피섬 투어",
  title="피피섬 — 라사다 항 출발·국립공원 입장료·마야 베이 규정·하루 투어 동선",
  desc="푸켓에서 피피섬 가는 법(라사다 항), 국립공원 입장료 외국인 400바트, 마야 베이 8~9월 휴식기와 수영 금지 규정, 하루 투어 동선과 팡아만 투어와의 차이를 정리했습니다.",
  intro="푸켓에서 배로 다녀오는 <b>피피섬</b>을 가는 법 · 입장료 · 마야 베이 규정 · 하루 동선 순서로 정리했어요.",
  first="먼저 알아둘 것: 피피섬은 크라비주 핫 놉파랏 타라–피피섬 국립공원 안에 있어 외국인 성인 <b>400바트</b>, 어린이 <b>200바트</b>를 따로 내요(2024년 기준). 마야 베이는 매년 <b>8월 1일~9월 30일</b> 문을 닫고, 열려 있을 때도 <b>수영은 금지</b>예요.",
  cards=[
   ("가는 법 (라사다 항)",
    "<p>푸켓에서 피피섬으로 가는 정기 여객선은 푸켓 타운 쪽 <b>라사다 항</b>에서 출발해요. 라사다 항은 푸켓 지방행정기구가 소유한 항구로, 2001년 개항 때부터 피피섬·코야오 노선이 다녔어요.</p>"
    "<ul><li>여객선: 라사다 항 → 피피 돈 섬, 시간표·요금은 운항사 확인</li><li>스피드보트 투어: 숙소 픽업 후 부두에서 출발, 약 1시간</li><li>파도가 높은 5~10월 우기에는 결항·투어 취소가 잦아요</li></ul>"),
   ("국립공원 입장료 (외국인 기준)",
    "<p>피피 돈·피피 레·대나무섬(코 마이 파이)은 국립공원청(DNP) 특별 서비스 요금 구역이에요.</p>"
    "<ul><li>외국인 성인 400바트, 어린이 200바트</li><li>태국인 성인 40바트, 어린이 20바트</li><li>투어 요금에 포함됐는지 예약 때 확인</li></ul>"
    "<p>2024년 공원장 발표 기준이고, 요금은 고시로 바뀔 수 있어 방문 전 확인이 필요해요.</p>"),
   ("마야 베이 (휴식기·규정)",
    "<p>피피 레 섬의 마야 베이는 해마다 <b>8월 1일~9월 30일</b> 로사마 만·로코 만과 함께 닫고 10월 1일 다시 열어요(2026년도 10월 1일 재개장).</p>"
    "<ul><li>수영 금지(산호 보호)</li><li>배는 로사마 만 선착장에 내려 주고 마야 베이 앞바다로 들어가지 않아요</li><li>1회 관람 1시간 이내, 하루 최대 4,125명(375명씩 11회)</li><li>관람 시간 07:00~18:00</li></ul>"),
   ("하루 투어 동선 (스피드보트 기준)",
    "<ol><li>오전: 부두 출발 → 피피 레(마야 베이·로사마 만)</li><li>점심: 피피 돈 섬</li><li>오후: 대나무섬 또는 스노클링 지점 → 푸켓 복귀</li></ol>"
    "<p>순서는 업체마다 달라요. 피피섬과 팡아만은 방향이 달라서 하루에 둘 다 보기보다 날을 나누는 편이 여유로워요. 팡아만은 카누·제임스본드섬 투어가 중심이고 피피섬은 바다·해변 위주예요.</p>"),
   ("팡아만과 함께 짤 때",
    "<p>팡아만은 푸켓 북동쪽 팡아주 아오 팡아 국립공원의 석회암 섬 바다예요. <a href=\"/travel-phuket.html\">푸켓 여행 코스</a>처럼 4박 5일이면 피피섬 하루, 5박 6일이면 팡아만 하루를 더하는 구성이 무난해요.</p>"
    "<p>팡아만 국립공원 입장료는 공식 고시를 찾지 못해 투어 포함 여부를 예약 때 확인해요.</p>"),
  ],
  table=(["항목", "내용"], [
   ["출발", "라사다 항 여객선 또는 스피드보트 투어"],
   ["입장료", "외국인 성인 400바트, 어린이 200바트"],
   ["마야 베이", "8~9월 휴식기, 수영 금지, 1시간 이내"],
   ["관람 시간", "07:00~18:00"],
   ["팡아만", "다른 날 카누·제임스본드섬 투어"],
  ]),
  tip="입장료는 현금이나 전자 티켓으로 받는데 피피 돈 섬 일부는 통신이 약해 전자 티켓 확인이 어렵다고 보도됐어요. 바트 현금을 조금 챙기면 편해요.",
  faq=[
   ("피피섬 입장료는 얼마예요?", "외국인 성인 400바트, 어린이 200바트예요(2024년 국립공원 발표 기준). 투어 요금에 포함됐는지 확인해요."),
   ("마야 베이에서 수영할 수 있어요?", "아니요. 산호 보호를 위해 수영이 금지돼 있고 해변에서 보기만 해요."),
   ("마야 베이는 언제 닫아요?", "매년 8월 1일~9월 30일이에요. 10월 1일에 다시 열어요."),
   ("푸켓에서 어디서 배를 타요?", "정기 여객선은 라사다 항에서 출발해요. 스피드보트 투어는 업체가 정한 부두에서 출발하니 픽업 안내를 확인해요."),
   ("피피섬과 팡아만을 하루에 볼 수 있어요?", "방향이 달라 보통 날을 나눠요. 피피섬은 바다·해변, 팡아만은 카누·석회암 섬 위주예요."),
  ],
  sources=[
   ("Bangkok Post — 핫 놉파랏 타라–피피섬 국립공원 입장 요금(공원장 발표) (확인 2026.11.21)", "https://www.bangkokpost.com/thailand/general/2747304/national-park-in-krabi-earns-over-b260m-in-entry-fees-in-4-months"),
   ("The Phuket News — DNP 고시, 피피섬 특별 서비스 요금(2022) (확인 2026.11.21)", "https://www.thephuketnews.com/phi-phi-islands-under-new-special-service-entry-fees-85785.php"),
   ("태국 정부 홍보국(PRD) — 마야 베이 8월 1일~9월 30일 휴식 (확인 2026.11.21)", "https://thailand.prd.go.th/en/content/category/detail/id/52/iid/311034"),
   ("Khaosod English — 마야 베이 재개장 규정(공원장 발표) (확인 2026.11.21)", "https://www.khaosodenglish.com/tourism/2024/09/30/maya-bay-reopens-strict-measures-in-place-for-sustainable-tourism/"),
   ("Time Out Bangkok — 마야 베이 2026년 10월 1일 재개장 (확인 2026.11.21)", "https://www.timeout.com/bangkok/news/thailand-famous-maya-bay-reopens-092926"),
   ("The Thaiger — 라사다 항 개항(푸켓 주지사) (확인 2026.11.21)", "https://thethaiger.com/news/phuket/Rassada-Port-officially-opened"),
  ],
 ),
 dict(
  kind="trip",
  slug="travel-phuket-oldtown",
  region="phuket",
  places=["pk_oldtown", "pk_bigbuddha", "pk_promthep"],
  kw=("푸켓올드타운", 1840),
  name="푸켓 올드타운",
  title="푸켓 올드타운 — 선데이 워킹스트리트·시노-포르투갈 거리·빅 부다 반나절 동선",
  desc="푸켓 올드타운 일요일 워킹스트리트(락 디·라트야이 마켓) 운영 요일과 시간, 탈랑·디북·끄라비 거리 시노-포르투갈 건물, 빅 부다·프롬텝 곶과 묶는 반나절 동선을 정리했습니다.",
  intro="<b>푸켓 올드타운</b>의 일요일 야시장과 옛 건물 거리를 보고, 남쪽 빅 부다·프롬텝 곶 노을로 이어지는 반나절 동선이에요.",
  first="먼저 알아둘 것: 일요일 워킹스트리트(라트야이 마켓)는 <b>매주 일요일 16:00부터</b> 탈랑 거리에서 열려요. 빅 부다는 2024년 산사태로 닫혔다가 <b>2026년 3월 3일</b> 다시 열었고, 매일 09:00~18:00예요.",
  cards=[
   ("선데이 워킹스트리트 (라트야이 마켓)",
    "<p>태국관광청은 '푸켓 워킹스트리트(라트야이)'를 <b>매주 일요일 16:00부터</b> 탈랑 거리에서 여는 시장으로 안내해요. 끝나는 시간은 공식 안내에 없어 방문 전 확인이 필요해요.</p>"
    "<ul><li>구역: 기념품·체험·먹거리·학생 구역</li><li>먹거리: 푸켓 향토 음식·디저트</li><li>무대 3곳: 마노라 춤, 민속 음악, 청소년 공연(주마다 바뀜)</li></ul>"
    "<p>한국에서 '락 디 마켓'으로 부르기도 하는데 현지 이름은 라트야이(หลาดใหญ่)예요.</p>"),
   ("시노-포르투갈 건물 거리",
    "<p>푸켓 올드타운은 19~20세기 초 주석 광산 무역으로 생긴 거리예요. 호키엔 중국인과 포르투갈 등 유럽 상인의 영향으로 시노-포르투갈 양식 상가 주택이 남았어요.</p>"
    "<ul><li>탈랑·디북·끄라비 거리, 소이 롬마니가 대표 거리</li><li>앞쪽 회랑으로 이어진 좁고 깊은 상가 주택</li><li>타이후아 박물관(끄라비 거리 옛 중국어 학교)</li></ul>"
    "<p>낮에는 거리 벽화와 박물관을 보고, 일요일이면 저녁 시장까지 이어 보면 좋아요.</p>"),
   ("빅 부다 (재개장·시간)",
    "<p>빅 부다는 찰롱과 까따 사이 언덕 위의 대형 불상이에요. 2024년 8월 27일 인근 산사태 뒤 닫혔고, 2026년 3월 3일 왓 까따 위원회가 관리하는 '왓 낏띠상카람'으로 다시 열었어요.</p>"
    "<ul><li>운영: 매일 09:00~18:00</li><li>입장료: 재개장 첫 달 무료, 이후는 방문 전 확인</li><li>사원 구역이라 어깨·무릎을 가리는 옷이 무난해요</li></ul>"),
   ("반나절 동선 (오후 출발)",
    "<ol><li>13:00 빅 부다(언덕 전망, 약 1시간)</li><li>15:00 푸켓 올드타운 거리 산책</li><li>16:00 이후 일요일이면 워킹스트리트</li></ol>"
    "<p>일요일이 아니면 순서를 바꿔 푸켓 올드타운 → 빅 부다 → 프롬텝 곶 노을로 마무리해요. 프롬텝 곶은 섬 최남단 곶으로 해 질 녘 풍경을 보러 많이 가요. 전체 일정은 <a href=\"/travel-phuket.html\">푸켓 여행 코스</a>를 참고하세요.</p>"),
  ],
  table=(["장소", "시간", "포인트"], [
   ["워킹스트리트", "일요일 16:00부터", "탈랑 거리, 먹거리·공연"],
   ["올드타운 거리", "상시(가게별 상이)", "탈랑·디북·끄라비 거리"],
   ["빅 부다", "매일 09:00~18:00", "2026년 3월 재개장"],
   ["프롬텝 곶", "해 질 녘", "섬 최남단 노을"],
  ]),
  tip="빅 부다는 언덕길을 차로 올라가요. 오후에 올라갔다가 내려와 푸켓 올드타운 일요일 시장으로 가면 동선이 자연스러워요.",
  faq=[
   ("푸켓 올드타운 일요일 시장은 몇 시에 열어요?", "매주 일요일 16:00부터 탈랑 거리에서 열려요. 끝나는 시간은 방문 전 확인해요."),
   ("락 디 마켓과 라트야이는 같은 곳이에요?", "네, 같은 일요일 워킹스트리트를 가리켜요. 현지 이름은 라트야이(หลาดใหญ่)예요."),
   ("빅 부다는 지금 갈 수 있어요?", "2026년 3월 3일 재개장했고 매일 09:00~18:00로 보도됐어요."),
   ("시노-포르투갈 건물은 어느 거리에 많아요?", "탈랑·디북·끄라비 거리와 소이 롬마니가 대표 거리예요."),
   ("빠통에서 올드타운까지 얼마나 걸려요?", "차로 약 30분이에요(교통 상황에 따라 달라요)."),
  ],
  sources=[
   ("태국관광청 — Phuket Walking Street (확인 2026.11.21)", "https://www.tourismthailand.org/Shop/phuket-walking-street"),
   ("태국관광청 TAT Newsroom — Old Phuket Town (확인 2026.11.21)", "https://www.tatnews.org/2015/11/old-phuket-town-is-a-casserole-of-cultures-with-a-very-thai-taste/"),
   ("태국관광청 — 10 Things to Do in Phuket (확인 2026.11.21)", "https://www.tourismthailand.org/Articles/10-things-to-do-in-phuket"),
   ("The Phuket News — 빅 부다 재개장(왓 까따 주지 발표) (확인 2026.11.21)", "https://www.thephuketnews.com/big-buddha-reopens-99432.php"),
   ("The Phuket News — 빅 부다 산림청 25개 조건 (확인 2026.11.21)", "https://www.thephuketnews.com/big-buddha-25-conditions-99464.php"),
  ],
 ),
]
# 명소 안내 (K링크 장소 상세 화면). 공식 출처로 확인한 것만. 확인 못 한 칸은 '방문 전 확인'.
SPOTS = {
 "pk_patong": dict(
   one="푸켓 서쪽의 넓은 만에 있는 대표 해변이에요. 해양 스포츠와 숙소·식당이 모여 있고 방라로드 밤거리와 이어져요.",
   see=[("빠통 해변", "넓은 만과 맑은 바다"), ("해양 스포츠", "해변에서 즐기는 물놀이 활동"), ("방라로드", "해변 옆 밤거리")],
   facts=dict(hours="상시", fee="무료", stay="약 3시간", when="11~4월 건기, 해 질 녘", access="푸켓 타운에서 약 15km, 공항에서 차로 약 1시간"),
   tips=["5~10월 우기에는 파도가 높아 안전 깃발을 확인하고 들어가요.", "푸켓 타운으로 넘어가는 길은 굽고 경사가 있어 운전에 주의해요."],
   src=[("태국관광청 — 10 Things to Do in Phuket", "https://www.tourismthailand.org/Articles/10-things-to-do-in-phuket")],
   checked="2026-11-21", photo=None),
 "pk_oldtown": dict(
   one="주석 무역으로 성장한 푸켓 타운의 옛 거리예요. 시노-포르투갈 상가 주택과 일요일 워킹스트리트(라트야이)가 유명해요.",
   see=[("탈랑 거리", "일요일 워킹스트리트가 열리는 중심 거리"), ("소이 롬마니", "색이 고운 상가 주택 골목"), ("타이후아 박물관", "끄라비 거리 옛 중국어 학교, 푸켓 역사 전시")],
   facts=dict(hours="거리 상시, 워킹스트리트는 일요일 16:00부터", fee="무료(박물관 별도)", stay="약 2시간", when="일요일 오후~저녁", access="빠통에서 차로 약 30분"),
   tips=["일요일에 맞추면 낮 산책과 저녁 시장을 한 번에 볼 수 있어요.", "벽화와 회랑 사진은 햇볕이 덜한 오전이나 늦은 오후가 편해요."],
   src=[("태국관광청 — Phuket Walking Street", "https://www.tourismthailand.org/Shop/phuket-walking-street"), ("TAT Newsroom — Old Phuket Town", "https://www.tatnews.org/2015/11/old-phuket-town-is-a-casserole-of-cultures-with-a-very-thai-taste/")],
   checked="2026-11-21", photo=None),
 "pk_bigbuddha": dict(
   one="찰롱과 까따 사이 언덕 위의 대형 불상이에요. 2024년 산사태 뒤 닫혔다가 2026년 3월 3일 다시 열었어요.",
   see=[("대형 불상", "언덕 위 흰 불상"), ("전망", "찰롱 만과 섬 남부 풍경"), ("사원 구역", "왓 까따가 관리하는 예불 공간")],
   facts=dict(hours="매일 09:00~18:00", fee="방문 전 확인 (재개장 첫 달 무료)", stay="약 1시간", when="오전 또는 늦은 오후", access="찰롱·까따 쪽 언덕길, 차량 이동"),
   tips=["사원 구역이라 어깨·무릎을 가리는 옷을 챙겨요.", "산림청 조건부 재개장이라 출입 구역이 제한될 수 있어요."],
   src=[("The Phuket News — Big Buddha reopens", "https://www.thephuketnews.com/big-buddha-reopens-99432.php"), ("The Phuket News — 25 conditions", "https://www.thephuketnews.com/big-buddha-25-conditions-99464.php")],
   checked="2026-11-21", photo=None),
 "pk_promthep": dict(
   one="푸켓 섬 최남단의 곶이에요. 노을과 사진 명소로 유명하고 등대 안에 전시가 있어요.",
   see=[("노을 전망", "섬 최남단에서 보는 해 질 녘 바다"), ("등대", "불빛이 약 39km까지 보이는 등대"), ("등대 전시", "등대 안 전시 공간")],
   facts=dict(hours="방문 전 확인", fee="무료", stay="약 1시간", when="해 질 녘", access="섬 남부 라와이 쪽, 차량 이동"),
   tips=["노을 시간대에는 붐벼서 30분쯤 일찍 도착하면 자리 잡기 편해요.", "빅 부다와 같은 남부라 오후에 묶기 좋아요."],
   src=[("태국관광청 — 10 Things to Do in Phuket", "https://www.tourismthailand.org/Articles/10-things-to-do-in-phuket")],
   checked="2026-11-21", photo=None),
 "pk_phiphi": dict(
   one="크라비주 핫 놉파랏 타라–피피섬 국립공원의 섬들이에요. 푸켓에서 배로 다녀오고 피피 레의 마야 베이가 유명해요.",
   see=[("마야 베이", "피피 레 섬, 수영 금지·1시간 이내 관람"), ("피피 돈", "숙소·식당이 모인 큰 섬"), ("대나무섬", "코 마이 파이, 특별 요금 구역")],
   facts=dict(hours="마야 베이 07:00~18:00 (8~9월 휴식)", fee="외국인 성인 400바트, 어린이 200바트", stay="하루", when="11~4월 건기", access="라사다 항 여객선 또는 스피드보트 투어(약 1시간)"),
   tips=["8월 1일~9월 30일에는 마야 베이·로사마 만이 닫혀요.", "입장료가 투어 요금에 포함됐는지 예약 때 확인해요.", "산호 보호를 위해 물고기 먹이 주기와 해양 생물 만지기는 금지예요."],
   src=[("Bangkok Post — 국립공원 입장 요금", "https://www.bangkokpost.com/thailand/general/2747304/national-park-in-krabi-earns-over-b260m-in-entry-fees-in-4-months"), ("Khaosod English — 마야 베이 규정", "https://www.khaosodenglish.com/tourism/2024/09/30/maya-bay-reopens-strict-measures-in-place-for-sustainable-tourism/"), ("태국 정부 홍보국 — 마야 베이 휴식", "https://thailand.prd.go.th/en/content/category/detail/id/52/iid/311034")],
   checked="2026-11-21", photo=None),
}
# (새 지역 담당만) K링크 좌표 확인 결과: 브리프 좌표에서 바꾼 것만.
COORDS = {
 "pk_karon": (7.8440, 98.2946),     # 카론 뷰포인트 → 까론 비치로 대체
 "pk_promthep": (7.7620, 98.3055),  # 왓 찰롱 대체(새 id)
}
PLACES = {
 "pk_patong": dict(ko=("빠통 비치", "푸켓 대표 해변·밤거리"), en=("Patong Beach", "Phuket's main beach and nightlife"), zh=("芭东海滩", "普吉岛主要海滩与夜生活"), ja=("パトンビーチ", "プーケット定番のビーチと夜の街"),
   lat=7.8960, lng=98.2960, o=[0, 24], cost=0, closed=[], best="eve", meal="any", h=3, cat="nature", st="Patong, Kathu, Phuket"),
 "pk_oldtown": dict(ko=("푸켓 올드타운", "시노-포르투갈 거리·일요 야시장"), en=("Phuket Old Town", "Sino-Portuguese streets, Sunday market"), zh=("普吉老城", "中葡建筑街区与周日夜市"), ja=("プーケット・オールドタウン", "中葡様式の街並みと日曜市"),
   lat=7.8840, lng=98.3880, o=[9, 22], cost=0, closed=[], best="eve", meal="any", h=2, cat="shop", st="Thalang Road, Phuket Town"),
 "pk_bigbuddha": dict(ko=("빅 부다", "언덕 위 대형 불상·전망"), en=("Big Buddha", "Hilltop Buddha statue with views"), zh=("普吉大佛", "山顶大佛与观景"), ja=("ビッグブッダ", "丘の上の大仏と眺望"),
   lat=7.8277, lng=98.3128, o=[9, 18], cost=0, closed=[], best="am", meal=None, h=1, cat="palace", st="Chalong–Kata hills, Phuket"),
 "pk_promthep": dict(ko=("프롬텝 곶", "섬 최남단 노을 명소"), en=("Promthep Cape", "Southernmost sunset point"), zh=("神仙半岛", "岛屿最南端的日落观景点"), ja=("プロムテープ岬", "島最南端の夕日スポット"),
   lat=7.7620, lng=98.3055, o=[0, 24], cost=0, closed=[], best="eve", meal=None, h=1, cat="nature", st="Rawai, Mueang Phuket"),
 "pk_karon": dict(ko=("까론 비치", "조용한 서해안 해변"), en=("Karon Beach", "Quieter west-coast beach"), zh=("卡伦海滩", "较安静的西海岸海滩"), ja=("カロンビーチ", "落ち着いた西海岸のビーチ"),
   lat=7.8440, lng=98.2946, o=[0, 24], cost=0, closed=[], best="day", meal=None, h=3, cat="nature", st="Karon, Mueang Phuket"),
 "pk_phiphi": dict(ko=("피피섬", "마야 베이·국립공원 섬 투어"), en=("Phi Phi Islands", "Maya Bay and national park islands"), zh=("皮皮岛", "玛雅湾与国家公园海岛游"), ja=("ピピ島", "マヤベイと国立公園の島巡り"),
   lat=7.7407, lng=98.7784, o=[7, 18], cost=0, closed=[], best="day", meal="any", h=8, cat="nature", st="Rassada Pier, Phuket Town (boat)"),
 "pk_phangnga": dict(ko=("팡아만", "석회암 섬·카누·제임스본드섬"), en=("Phang Nga Bay", "Limestone islets, canoeing, James Bond Island"), zh=("攀牙湾", "石灰岩岛屿、划艇与007岛"), ja=("パンガー湾", "石灰岩の島々とカヌー、ジェームズ・ボンド島"),
   lat=8.2750, lng=98.5010, o=[8, 17], cost=0, closed=[], best="day", meal="any", h=8, cat="nature", st="Ao Phang Nga National Park (boat tour)"),
}
