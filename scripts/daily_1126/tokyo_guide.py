# -*- coding: utf-8 -*-
"""tokyo_guide — 2026-11-26 기존 지역 '도쿄' 가이드 1개: 스카이라이너(나리타공항에서 도쿄 시내). 확인일 2026-11-26.
키워드: ("스카이라이너", 13640) / 관련: 도쿄스카이라이너 15,970, 나리타공항에서도쿄 1,180.
slug: 생성기(scripts/build.py)가 'guide-' + slug 로 파일을 만들어서 slug="tokyo-skyliner" -> guide-tokyo-skyliner.html.
K링크 연결: tk_ueno '우에노 공원', tk_sensoji '센소지' (본문에 각각 3번 이상).
메모(요금 충돌): 게이세이 영문 'Fares from Major Stations' 페이지는 닛포리·우에노 2,470엔(IC 2,465엔)으로 옛 금액이 남아 있음.
  같은 사이트의 FAQ·How to Purchase(기본 운임 1,280엔 + 스카이라이너권 1,300엔 = 2,580엔, IC 기본 운임 1,267엔, 어린이 640엔+650엔),
  Tokyo City Pass 추가권(2,310엔 = 270엔 할인)과 Aviation Wire 2026.11.8 기사(현재 2,580엔)가 서로 맞아 2,580엔을 씀.
메모(요금 인상 예정): Aviation Wire 2026.11.8 — 게이세이가 국토교통성에 인가 신청, 2027.3.13 특급권 +200엔(합계 2,780엔), 2028년 3월 3,000엔. 인가 전이라 '예정'으로만 씀.
메모(확인 못 한 숫자): 스카이라이너 할인권(Skyliner Discount Ticket)·Skyliner & Tokyo Subway Ticket 금액(공식 페이지에 이미지로만 있음),
  액세스 특급 소요 시간, 리무진 버스 신주쿠까지 소요 시간, 긴자선 우에노~아사쿠사 요금 -> 숫자 안 쓰고 '방문 전 확인'.
  N'EX 왕복권(N'EX TOKYO Round Trip Ticket 5,200엔)은 외국인 전용 여부가 공식 페이지에 없어 '외국인 전용'이라고 쓰지 않음.
못 쓴 것: 없음.
"""

ARTICLES = []
SPOTS = {}
PLACES = {}
STAYS = []

GUIDE = {
 "slug": "tokyo-skyliner", "name": "스카이라이너 (나리타공항에서 도쿄)", "date": "2026-11-26",
 "title": "스카이라이너 — 나리타공항에서 도쿄 시내 요금·시간, 우에노 공원·센소지 가는 법",
 "desc": "게이세이 스카이라이너로 나리타공항에서 닛포리 최단 36분, 우에노 약 41분, 요금 2,580엔과 Suica로 타는 법, 액세스 특급·N'EX·리무진 버스 비교, 우에노 공원·센소지 동선까지 정리했습니다.",
 "answer": "나리타공항에서 도쿄 동쪽(우에노·아사쿠사)으로 간다면 <b>게이세이 스카이라이너</b>가 가장 빨라요. <b>닛포리까지 최단 36분, 게이세이 우에노까지 약 41분</b>, 어른 편도 <b>2,580엔</b>(2026년 기준)이에요. 우에노에서 내리면 <b>우에노 공원</b>이 바로 옆이고, <b>센소지</b>는 긴자선으로 세 정거장이에요.",
 "body": [
  ("스카이라이너 요금·시간 (닛포리·우에노)",
   "<p>스카이라이너는 나리타공항(제1터미널역·제2·3터미널역)과 <b>닛포리·게이세이 우에노</b> 사이를 달리는 전석 지정석 특급이에요. 시간당 약 3대 다녀요.</p>"
   "<ul><li><b>시간</b>: 닛포리까지 최단 36분, 게이세이 우에노까지 약 41분(제2·3터미널 기준)</li>"
   "<li><b>어른 편도</b>: 2,580엔 = 기본 운임 1,280엔 + 스카이라이너권 1,300엔</li>"
   "<li><b>어린이(6~11세)</b>: 기본 운임 640엔 + 스카이라이너권 650엔</li>"
   "<li>스카이라이너권 없이 타면 특급 요금에 어른 300엔, 어린이 150엔이 더 붙어요.</li></ul>"
   "<p>게이세이는 2027년 3월 13일부터 스카이라이너권을 200엔 올리는 요금 인상을 신청해 둔 상태예요(인가 전). 3월 이후 여행이면 출발 전에 다시 확인해요.</p>"),
  ("표 사는 법·Suica 조합 (공식 확인분)",
   "<ul><li><b>공항역 창구·발매기</b>: 제1터미널역·제2·3터미널역 스카이라이너 창구와 발매기에서 사요. 신용카드도 돼요. 출발 한 달 전부터 팔아요.</li>"
   "<li><b>Suica·PASMO</b>: 기본 운임은 교통 IC 카드로 개찰구에서 내고(어른 1,267엔), 스카이라이너권(1,300엔)만 따로 사서 타는 방식도 있어요.</li>"
   "<li><b>Welcome Suica</b>: 나리타공항 제1터미널역·제2·3터미널역의 전용 발매기와 JR 동일본 여행 서비스 센터에서 사요. 보증금이 없고 구입일부터 28일 동안 써요.</li></ul>"
   "<p>게이세이 공식 할인 상품으로 <b>스카이라이너 할인권</b>(온라인 예약)과 <b>Keisei Skyliner & Tokyo Subway Ticket</b>(스카이라이너 편도·왕복 + 도쿄 메트로·도에이 지하철 24·48·72시간권)이 있어요. 금액은 공식 예약 페이지에서 확인해요. 지하철 패스가 이득인지는 <a href=\"/tokyo_subway_ticket_calculator.html\">도쿄 지하철 패스 계산기</a>로 따져 봐요.</p>"),
  ("액세스 특급·N'EX·리무진 버스 (다른 선택지)",
   "<ul><li><b>게이세이 액세스 특급</b>: 지정석 요금 없이 일반 운임만 내요. 아사쿠사까지 1,290엔(아사쿠사선 직통), 닛포리·우에노는 1,240엔이에요. 스카이라이너보다 오래 걸려 시간은 시간표로 확인해요.</li>"
   "<li><b>JR N'EX(나리타 익스프레스)</b>: 도쿄역 최단 53분, 보통차 3,140엔. 시나가와·시부야·신주쿠는 3,330엔이에요. 14일 안에 쓰는 N'EX TOKYO 왕복권은 5,200엔(JR 동일본 온라인 예약)이에요.</li>"
   "<li><b>리무진 버스</b>: 신주쿠 방면 어른 3,600엔, 어린이 1,800엔. 호텔 앞까지 가는 노선이 많지만 시간은 도로 사정에 따라 달라요.</li>"
   "<li><b>저가 버스(LCB)</b>: 도쿄역·긴자역까지 1,500엔(심야·이른 아침 편은 다름).</li></ul>"
   "<p>교통비를 원화로 비교하려면 <a href=\"/airport_transport_compare_calculator.html\">공항 교통비 비교 계산기</a>를 써요.</p>"),
  ("우에노 도착 뒤 우에노 공원·센소지",
   "<p>게이세이 우에노역은 <b>우에노 공원</b> 바로 옆에 있어요. 우에노 공원은 05:00~23:00에 열고 입장은 무료라, 숙소 체크인 전에 짐을 맡기고 한 바퀴 돌기 좋아요. 공원 안 박물관·미술관은 대부분 월요일에 쉬어요.</p>"
   "<ol><li>게이세이 우에노 도착 → <b>우에노 공원</b> 산책(시노바즈 연못·박물관 쪽)</li>"
   "<li>도쿄 메트로 우에노역에서 <b>긴자선</b> 아사쿠사 방면 → 세 정거장 뒤 아사쿠사역</li>"
   "<li>아사쿠사역에서 걸어서 약 5분이면 <b>센소지</b> 가미나리몬이에요.</li></ol>"
   "<p>센소지는 해 진 뒤부터 밤 11시쯤까지 조명을 켜서 저녁에 도착해도 둘러볼 수 있어요. 액세스 특급을 타면 아사쿠사역까지 갈아타지 않고 바로 가요.</p>"),
  ("구간별 정리",
   "<div class=\"at-table\"><table><thead><tr><th>수단</th><th>도착</th><th>시간(약)</th><th>어른 요금</th></tr></thead><tbody>"
   "<tr><td>스카이라이너</td><td>닛포리·우에노</td><td>36~41분</td><td>2,580엔</td></tr>"
   "<tr><td>액세스 특급</td><td>아사쿠사</td><td>시간표 확인</td><td>1,290엔</td></tr>"
   "<tr><td>N'EX</td><td>도쿄역</td><td>최단 53분</td><td>3,140엔</td></tr>"
   "<tr><td>리무진 버스</td><td>신주쿠 방면</td><td>도로 사정 따라 다름</td><td>3,600엔</td></tr>"
   "<tr><td>저가 버스</td><td>도쿄역·긴자</td><td>도로 사정 따라 다름</td><td>1,500엔</td></tr>"
   "</tbody></table></div>"
   "<p>장소 위치는 <a href=\"/klink/#tk_ueno\">K링크 지도에서 우에노 공원 보기</a>와 <a href=\"/klink/#tk_sensoji\">센소지 보기</a>로 확인하고, 아사쿠사·우에노를 묶은 일정은 <a href=\"/travel-tokyo.html\">도쿄 여행 코스</a>에 있어요.</p>"
   "<div class=\"b-tip\"><p><b>실전 팁</b> 숙소가 우에노·아사쿠사 쪽이면 스카이라이너나 액세스 특급, 도쿄역·신주쿠 쪽이면 N'EX가 갈아타기가 적어요. 스카이라이너는 지정석이라 공항역에 내리면 먼저 다음 열차 표부터 사 둬요.</p></div>"),
 ],
 "faq": [
  ("스카이라이너 요금은 얼마예요?", "나리타공항에서 닛포리·게이세이 우에노까지 어른 편도 2,580엔(기본 운임 1,280엔 + 스카이라이너권 1,300엔)이에요(2026년 기준). 2027년 3월 인상이 신청돼 있어요."),
  ("나리타공항에서 우에노까지 얼마나 걸려요?", "스카이라이너로 약 41분, 닛포리까지는 최단 36분이에요."),
  ("Suica로 스카이라이너를 탈 수 있어요?", "기본 운임은 Suica·PASMO로 개찰구에서 내고, 지정석인 스카이라이너권(1,300엔)은 따로 사야 해요."),
  ("스카이라이너와 N'EX 중 뭐가 나아요?", "우에노·아사쿠사 쪽은 스카이라이너가 빠르고 싸요. 도쿄역·시부야·신주쿠로 바로 가려면 N'EX(도쿄역 3,140엔)가 갈아타기가 없어요."),
  ("우에노에서 센소지는 어떻게 가요?", "도쿄 메트로 긴자선으로 세 정거장 가서 아사쿠사역에서 내리고, 걸어서 약 5분이에요. 우에노 공원을 먼저 둘러보고 가도 좋아요."),
 ],
 "tools": ["airport_transport_compare_calculator", "tokyo_subway_ticket_calculator", "exchange_rate_calculator"],
 "sources": [
  ("게이세이 전철 — Skyliner Overview (확인 2026.11.26)", "https://www.keisei.co.jp/keisei/tetudou/skyliner/us/skyliner/index.php"),
  ("게이세이 전철 — How to Purchase Tickets (요금표) (확인 2026.11.26)", "https://www.keisei.co.jp/keisei/tetudou/skyliner/us/skyliner/purchase.php"),
  ("게이세이 전철 — Skyliner FAQ (확인 2026.11.26)", "https://www.keisei.co.jp/keisei/tetudou/skyliner/us/faq/index.php"),
  ("게이세이 전철 — Keisei Skyliner & Tokyo Subway Ticket (확인 2026.11.26)", "https://www.keisei.co.jp/keisei/tetudou/skyliner/us/tickets/subway.php"),
  ("게이세이 전철 — Access Express Fares (확인 2026.11.26)", "https://www.keisei.co.jp/keisei/tetudou/skyliner/us/traffic/express_fares.php"),
  ("JR 동일본 — N'EX Tickets (확인 2026.11.26)", "https://www.jreast.co.jp/en/multi/nex/tickets/"),
  ("JR 동일본 — Welcome Suica 구입 (확인 2026.11.26)", "https://www.jreast.co.jp/en/multi/welcomesuica/purchase.html"),
  ("나리타국제공항 — LCB (확인 2026.11.26)", "https://www.narita-airport.jp/en/access/bus/lcb/"),
  ("Airport Limousine — Shinjuku area (확인 2026.11.26)", "https://www.limousinebus.co.jp/en/line/detail/Narita-Shinjuku/"),
  ("JNTO — Sensoji Temple (확인 2026.11.26)", "https://www.japan.travel/en/spot/1691/"),
  ("GO TOKYO — Tokyo Metropolitan Ueno Park (확인 2026.11.26)", "https://www.gotokyo.org/en/spot/482/index.html"),
  ("Aviation Wire — 게이세이 스카이라이너 요금 인상 신청 (2026.11.8) (확인 2026.11.26)", "https://www.aviationwire.jp/?p=354063"),
 ],
}
