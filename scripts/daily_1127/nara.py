# -*- coding: utf-8 -*-
"""nara — 2026-11-27 새 해외 지역 '나라'(일본, K링크 region id nara, 장소 id 접두어 nr_) 데이터 + 가이드 1개. 확인일 2026-11-27.
못 쓴 글: 없음 (ARTICLES 비움, GUIDE 1개).
메모(총괄용):
- 장소 8곳: 기존 /travel-nara.html 본문에 나온 나라 공원, 도다이지, 고후쿠지, 가스가타이샤, 나라마치, 이스이엔(설명문) 6곳 +
  지시로 넣은 와카쿠사산, 나라 국립박물관 2곳(이 둘은 travel-nara.html 본문에 이름이 없음 — overseas_data.py 원칙과 다르니 총괄 판단).
- 오사카 블록(overseas_data.py)의 os_nara(나라 공원·도다이지 한 점)는 그대로 둠. 새 region nara 와 겹침.
- GUIDE slug: 생성기(scripts/build.py 511행)가 'guide-' + slug 로 파일을 만들어서 slug="nara-from-osaka" 로 씀
  -> guide-nara-from-osaka.html (지시의 'guide-nara-from-osaka' 그대로 넣으면 guide-guide-... 가 됨).
- 긴테쓰 오사카난바~긴테쓰나라 운임 680엔: 긴테쓰 운임·특급요금표 PDF + JR서일본 팩트시트(2025.4.1 현재)가 일치.
- 긴테쓰 특급권: 긴테쓰 여객영업규칙(40km까지 520엔)·요금표 PDF는 520엔인데, JR서일본 팩트시트 각주는 '통상기 620엔'이라 충돌.
  본문은 '520엔(긴테쓰 규칙 기준, 방문 전 확인)'으로 씀.
- JR 운임: JR서일본 2024.5.15 보도자료(2025.4.1 시행 특정 운임표)의 JR난바~나라 580엔, 팩트시트의 덴노지~나라 510엔(2025.4.1 현재)만 씀.
  JR 오사카역~나라 운임은 공식 숫자를 못 찾아 '방문 전 확인'. (다른 JR 별책 PDF는 JR난바~나라 560→570엔으로 적혀 있는데 2025.4 이전 개정분으로 보여 안 씀.)
- 간사이 에어리어 패스: JR서일본 공식 페이지에 '2026.9.30 판매 종료' 게시 → 본문에 판매 종료로 씀. 간사이 미니 패스(3일 3,000엔)는 종료 표시 없음.
- 특급 마호로바: 토·일·공휴일 운행, e5489 특급권 860엔(오사카·신오사카~나라). 소요 시간은 공식 텍스트에 없어 안 씀.
- 고후쿠지 오층탑 보수 공사(가림막 여부·공기)는 나라현 페이지 열람 승인 시간 초과로 확인 못 함 → '방문 전 확인'.
- 나라 국립박물관 공식(narahaku.go.jp)은 열리지 않아 나라시 관광협회 페이지로 확인(700엔, 월요일 휴관, 불교조각관 2026.9.14부터 보수 휴관).
- 좌표: 역·본당·입구 대표 지점의 대략값(소수 4자리). 간사이공항 이동 분(90)은 JR 덴노지 환승 기준 대략값.
"""

ARTICLES = []
COORDS = {}

# 도시 메타 (scripts/klink/tools/overseas_data.py 에 붙일 블록)
CITY_LINES = """C nara jp 34.6851 135.8400 1 110 | 나라|奈良|Nara|奈良 | 사슴이 노니는 공원과 대불, 천 년 넘은 절과 신사의 옛 수도 | Deer park, the Great Buddha and temples older than a thousand years
A KIX 34.4320 135.2304 90 | 간사이공항|关西机场|Kansai (KIX)|関西空港
S nr_s1 34.6844 135.8279 | 긴테쓰나라역 주변|近铁奈良站周边|Around Kintetsu-Nara Stn|近鉄奈良駅周辺 | 나라 공원까지 걸어서 약 5~8분, 난바 직통 | 5-8 min walk to Nara Park, direct trains to Namba
S nr_s2 34.6811 135.8197 | JR나라역 주변|JR奈良站周边|Around JR Nara Stn|JR奈良駅周辺 | JR 야마토지선·순환 버스 출발점 | JR Yamatoji Line and city loop bus hub
Z nr_z1 | 나라 공원·고후쿠지 | Nara Park & Kofuku-ji
P nr_park nature 34.6850 135.8432 1.5 o=A | 나라 공원|奈良公园|Nara Park|奈良公園 | 사슴 약 1,200마리가 사는 넓은 공원 | Vast park home to about 1,200 deer
P nr_kofukuji palace 34.6832 135.8316 1 am o=D | 고후쿠지|兴福寺|Kofuku-ji Temple|興福寺 | 오층탑과 국보관이 있는 역 앞 절 | Temple with a five-storied pagoda and treasure hall
P nr_museum palace 34.6834 135.8370 1.5 o=D x=1 | 나라 국립박물관|奈良国立博物馆|Nara National Museum|奈良国立博物館 | 불교 미술을 모은 공원 안 박물관 | Buddhist art museum inside the park
P nr_isuien nature 34.6858 135.8370 1 o=D x=2 | 이스이엔|依水园|Isui-en Garden|依水園 | 와카쿠사산을 빌려 온 일본 정원 | Japanese garden borrowing the hills as backdrop
Z nr_z2 | 도다이지·가스가타이샤 | Todai-ji & Kasuga Taisha
P nr_todaiji palace 34.6890 135.8398 1.5 am o=D | 도다이지|东大寺|Todai-ji Temple|東大寺 | 대불전의 큰 불상과 니가쓰도 | Great Buddha Hall and Nigatsu-do
P nr_kasuga palace 34.6812 135.8484 1.25 am o=D | 가스가타이샤|春日大社|Kasuga Taisha Shrine|春日大社 | 등롱 길이 이어지는 숲속 신사 | Forest shrine lined with stone lanterns
P nr_wakakusa nature 34.6866 135.8487 1.5 o=D | 와카쿠사산|若草山|Mt. Wakakusa|若草山 | 나라 시내가 내려다보이는 잔디 산 | Grassy hill overlooking the city
Z nr_z3 | 나라마치 | Naramachi
P nr_naramachi shop 34.6775 135.8310 1.5 o=S | 나라마치|奈良町|Naramachi|ならまち | 옛 상가가 남은 골목·카페 거리 | Old merchant-house lanes with cafes"""

# K링크 장소 데이터 (해외 cost=0). 좌표는 대표 지점의 대략값.
PLACES = {
 "nr_park": dict(
   ko=("나라 공원", "사슴 약 1,200마리가 사는 넓은 공원"), en=("Nara Park", "Vast park home to about 1,200 deer"),
   zh=("奈良公园", "约1200头鹿生活的大公园"), ja=("奈良公園", "約1,200頭の鹿が暮らす広い公園"),
   lat=34.6850, lng=135.8432, o=[0, 24], cost=0, closed=[], best="am", meal=None, h=1.5, cat="nature", st=""),
 "nr_todaiji": dict(
   ko=("도다이지", "대불전의 큰 불상과 니가쓰도"), en=("Todai-ji Temple", "Great Buddha Hall and Nigatsu-do"),
   zh=("东大寺", "大佛殿的大佛与二月堂"), ja=("東大寺", "大仏殿の大仏と二月堂"),
   lat=34.6890, lng=135.8398, o=[8, 17], cost=0, closed=[], best="am", meal=None, h=1.5, cat="palace", st=""),
 "nr_kasuga": dict(
   ko=("가스가타이샤", "등롱 길이 이어지는 숲속 신사"), en=("Kasuga Taisha Shrine", "Forest shrine lined with stone lanterns"),
   zh=("春日大社", "石灯笼参道延绵的森林神社"), ja=("春日大社", "灯籠の参道が続く森の神社"),
   lat=34.6812, lng=135.8484, o=[7, 17], cost=0, closed=[], best="am", meal=None, h=1.25, cat="palace", st=""),
 "nr_kofukuji": dict(
   ko=("고후쿠지", "오층탑과 국보관이 있는 역 앞 절"), en=("Kofuku-ji Temple", "Temple with a five-storied pagoda and treasure hall"),
   zh=("兴福寺", "有五重塔和国宝馆的寺院"), ja=("興福寺", "五重塔と国宝館のある寺"),
   lat=34.6832, lng=135.8316, o=[9, 17], cost=0, closed=[], best="am", meal=None, h=1, cat="palace", st=""),
 "nr_naramachi": dict(
   ko=("나라마치", "옛 상가가 남은 골목·카페 거리"), en=("Naramachi", "Old merchant-house lanes with cafes"),
   zh=("奈良町", "保留老町家的小巷与咖啡街"), ja=("ならまち", "町家が残る路地とカフェの町"),
   lat=34.6775, lng=135.8310, o=[10, 17], cost=0, closed=[], best="day", meal="any", h=1.5, cat="shop", st=""),
 "nr_isuien": dict(
   ko=("이스이엔", "산을 배경으로 빌려 온 일본 정원"), en=("Isui-en Garden", "Japanese garden borrowing the hills as backdrop"),
   zh=("依水园", "借景远山的日式庭园"), ja=("依水園", "山を借景にした日本庭園"),
   lat=34.6858, lng=135.8370, o=[9.5, 16.5], cost=0, closed=[2], best="day", meal=None, h=1, cat="nature", st=""),
 "nr_wakakusa": dict(
   ko=("와카쿠사산", "나라 시내가 내려다보이는 잔디 산"), en=("Mt. Wakakusa", "Grassy hill overlooking the city"),
   zh=("若草山", "可俯瞰奈良市区的草山"), ja=("若草山", "奈良の街を見渡す芝の山"),
   lat=34.6866, lng=135.8487, o=[9, 17], cost=0, closed=[], best="day", meal=None, h=1.5, cat="nature", st=""),
 "nr_museum": dict(
   ko=("나라 국립박물관", "불교 미술을 모은 공원 안 박물관"), en=("Nara National Museum", "Buddhist art museum inside the park"),
   zh=("奈良国立博物馆", "公园内的佛教美术博物馆"), ja=("奈良国立博物館", "公園内の仏教美術の博物館"),
   lat=34.6834, lng=135.8370, o=[9.5, 17], cost=0, closed=[1], best="day", meal=None, h=1.5, cat="palace", st=""),
}

# 숙소 권역 2곳 (상호 아님)
STAYS = [
 ("nr_s1", 34.6844, 135.8279,
  ["긴테쓰나라역 주변", "近铁奈良站周边", "Around Kintetsu-Nara Stn", "近鉄奈良駅周辺"],
  ["나라 공원까지 걸어서 약 5~8분, 난바 직통", "步行约5~8分钟到奈良公园，直达难波", "5-8 min walk to Nara Park, direct trains to Namba", "奈良公園まで徒歩約5~8分、難波へ直通"]),
 ("nr_s2", 34.6811, 135.8197,
  ["JR나라역 주변", "JR奈良站周边", "Around JR Nara Stn", "JR奈良駅周辺"],
  ["JR 야마토지선·순환 버스 출발점", "JR大和路线与循环巴士起点", "JR Yamatoji Line and city loop bus hub", "JR大和路線と循環バスの起点"]),
]

_NSK_PARK = ("나라시 관광협회 — Nara Park", "https://narashikanko.or.jp/en/spot/detail_10089.html")
_NSK_DEER = ("나라시 관광협회 — 나라 공원 사슴 특집", "https://narashikanko.or.jp/feature/deer")
_VN_PARK = ("나라현 관광 공식 Visit Nara — Nara Park", "https://www.visitnara.jp/venues/A00489/")
_TODAIJI = ("도다이지 공식 — Opening Hours / Admission Fees", "https://www.todaiji.or.jp/en/information/haikan/")
_NSK_TODAIJI = ("나라시 관광협회 — Todaiji Temple", "https://narashikanko.or.jp/en/spot/detail_10001.html")
_KASUGA = ("가스가타이샤 공식 — General Information", "https://www.kasugataisha.or.jp/en/about_en/basic/")
_KOFUKUJI = ("고후쿠지 공식 (영문)", "https://www.kohfukuji.com/english/")
_VN_MACHI = ("나라현 관광 공식 Visit Nara — Naramachi Area Guide", "https://www.visitnara.jp/destinations/area/naramachi/")
_ISUIEN = ("이스이엔 공식 — Access", "https://isuien.or.jp/en/access")
_NSK_WAKA = ("나라시 관광협회 — Mount Wakakusa", "https://narashikanko.or.jp/en/spot/detail_10108.html")
_NSK_MUSEUM = ("나라시 관광협회 — Nara National Museum", "https://narashikanko.or.jp/en/spot/detail_10043.html")

# 명소 안내 (K링크 장소 상세 화면). 공식 출처로 확인한 것만, 나머지는 '방문 전 확인'.
SPOTS = {
 "nr_park": dict(
   one="사슴 약 1,200마리가 자유롭게 다니는 넓은 공원이에요. 고후쿠지·도다이지·가스가타이샤가 모두 이 공원 안팎에 있어요.",
   see=[("사슴", "국가 천연기념물인 야생 사슴"), ("사슴 센베이", "10장 한 묶음 200엔"), ("공원 안 절·신사", "고후쿠지·도다이지·가스가타이샤")],
   facts=dict(hours="상시 개방 (연중무휴)", fee="무료", stay="약 1시간 30분", when="오전", access="긴테쓰나라역에서 걸어서 약 5~8분, JR나라역에서 약 15~20분"),
   tips=["사슴에게는 사슴 센베이만 주고, 센베이를 산 뒤 띠지(종이)를 먼저 떼고 망설이지 말고 빨리 줘야 깨물림을 피해요.", "센베이가 다 떨어지면 두 손바닥을 펴 보여 주고, 지도·비닐봉지는 사슴이 먹어 버릴 수 있어 가방에 넣어요.", "공원에 쓰레기통이 없어 쓰레기는 들고 나가고, 가을엔 수사슴이 예민해 가까이 가지 않아요."],
   src=[_NSK_PARK, _NSK_DEER, _VN_PARK],
   checked="2026-11-27", photo=None),
 "nr_todaiji": dict(
   one="세계 최대급 목조 건물인 대불전에 큰 불상(대불)이 앉아 있는 절이에요. 언덕 위 니가쓰도에서는 서쪽 노을이 좋아요.",
   see=[("대불전", "청동 대불이 있는 큰 목조 건물"), ("니가쓰도", "3월 슈니에 의식의 법당, 노을 전망"), ("도다이지 뮤지엄", "대불전과 묶음 표 1,200엔")],
   facts=dict(hours="대불전 11~3월 8:00~17:00, 4~10월 7:30~17:30 (2026년 기준)", fee="대불전 성인 800엔, 대불전+뮤지엄 1,200엔", stay="약 1시간 30분 (전체는 약 4시간)", when="오전 (개문 직후)", access="긴테쓰나라역에서 걸어서 약 15분, 순환 버스 '다이부쓰덴 가스가타이샤마에' 하차 걸어서 약 5분"),
   tips=["겨울(11~3월)엔 대불전이 17:00에 닫아 오후 늦게 도착하면 대불전부터 먼저 봐요.", "대불전+뮤지엄 묶음 표(1,200엔)는 대불전과 뮤지엄 매표소에서만 팔아요.", "시간이 없으면 대불전을 보고 니가쓰도로 올라가 노을을 보는 순서가 나라시 관광협회 추천 동선이에요."],
   src=[_TODAIJI, _NSK_TODAIJI],
   checked="2026-11-27", photo=None),
 "nr_kasuga": dict(
   one="나라 공원 동쪽 숲속에 있는 신사로, 참배길을 따라 돌등롱이 길게 이어져요. 붉은 회랑 안 본전은 특별 참배로 들어가요.",
   see=[("등롱 참배길", "숲길 양옆의 돌등롱"), ("본전 특별 참배", "회랑 안쪽, 700엔"), ("만요 식물원", "만요슈에 나오는 식물 정원")],
   facts=dict(hours="일반 참배 11~2월 7:00~17:00, 3~10월 6:30~17:30 / 특별 참배 9:00~16:00 (2026년 기준)", fee="경내 무료, 본전 특별 참배 700엔, 박물관 700엔", stay="약 1시간 15분", when="오전", access="긴테쓰나라역에서 걸어서 약 25분, 또는 '가스가타이샤 혼덴'행 버스"),
   tips=["본전 특별 참배는 16:00에 끝나 일반 참배 시간보다 일찍 닫으니 오후 일정이면 먼저 가요.", "만요 식물원은 6~3월 화요일(공휴일 제외)에 쉬어요.", "걸어서 25분이 부담되면 순환 버스(시계 방향) '가스가타이샤 오모테산도'에서 내려 식물원 쪽으로 약 10분 걸어요."],
   src=[_KASUGA],
   checked="2026-11-27", photo=None),
 "nr_kofukuji": dict(
   one="긴테쓰나라역에서 가장 가까운 절로, 높이 50.1m 오층탑이 상징이에요. 국보관에 아수라상 등 불상이 모여 있어요.",
   see=[("오층탑", "730년 처음 세운 50.1m 목탑"), ("국보관", "팔부중 등 국보 불상"), ("동금당·중금당", "국보관과 묶음 표")],
   facts=dict(hours="국보관·동금당·중금당 9:00~17:00 (입장 16:45까지)", fee="국보관 900엔, 동금당·중금당 각 500엔, 세 곳 묶음 1,600엔", stay="약 1시간", when="오전 (역에서 첫 코스)", access="긴테쓰나라역에서 노보리오지 길로 걸어서 약 5분"),
   tips=["입장료는 현금만 받아서 엔화 현금을 챙겨요.", "세 곳 묶음 표(1,600엔)는 16:00까지만 팔아 늦게 오면 따로 사야 해요.", "오층탑은 보수 공사 중이라 가림막이 있을 수 있어 방문 전 공식 안내를 확인해요."],
   src=[_KOFUKUJI],
   checked="2026-11-27", photo=None),
 "nr_naramachi": dict(
   one="나라 공원 남쪽에 옛 상가 건물이 남은 골목 동네예요. 화과자 가게·갤러리·카페가 모여 있고 걸어서 둘러보기 좋아요.",
   see=[("간고지", "아스카에서 옮겨 온 오래된 절"), ("사루사와 연못", "고후쿠지 오층탑이 비치는 연못"), ("하루시카 양조장", "사케 시음·가게")],
   facts=dict(hours="가게마다 다름, 방문 전 확인", fee="무료 (시설·시음 별도)", stay="약 1시간 30분", when="낮~이른 저녁", access="긴테쓰나라역에서 남쪽으로 걸어서 (JR나라역에서 약 20분)"),
   tips=["좁은 골목이 바둑판처럼 얽혀 있어 사루사와 연못 옆 나라 비지터 센터에서 지도를 받고 걸어요.", "비 오거나 추운 날엔 옛 상가 안 가게·카페가 쉬어 가기 좋아 나라 공원 다음 마지막 코스로 넣어요."],
   src=[_VN_MACHI],
   checked="2026-11-27", photo=None),
 "nr_isuien": dict(
   one="도다이지 남대문 지붕과 와카쿠사산을 배경으로 빌려 온 일본 정원이에요. 안에 네이라쿠 미술관이 있어요.",
   see=[("빌린 경치", "도다이지 남대문과 와카쿠사산"), ("앞뒤 두 정원", "연못을 도는 정원"), ("네이라쿠 미술관", "입장료에 포함")],
   facts=dict(hours="9:30~16:30 (입장 16:00까지)", fee="성인 1,200엔 (정원+미술관)", stay="약 1시간", when="낮", access="긴테쓰나라역에서 걸어서 약 15분"),
   tips=["화요일(공휴일이면 다음 날)에 쉬어 일정을 짤 때 요일을 먼저 봐요.", "12월 말~1월 중순과 9월 하순에도 정비로 쉬어요.", "주차장이 없어 걸어서 가거나 버스를 타요."],
   src=[_ISUIEN],
   checked="2026-11-27", photo=None),
 "nr_wakakusa": dict(
   one="나라 공원 동쪽의 해발 342m 잔디 산이에요. 정상에 오르면 나라 시내와 도다이지 대불전 지붕이 내려다보여요.",
   see=[("정상 전망", "나라 시내 파노라마"), ("잔디 비탈", "사슴이 풀을 뜯어요"), ("야마야키", "1월 넷째 토요일 산 태우기 행사")],
   facts=dict(hours="9:00~17:00, 3월 셋째 토요일~12월 둘째 일요일만 입산", fee="성인 150엔, 초등학생 80엔", stay="약 1시간 30분", when="낮 (맑은 날)", access="순환 버스 '다이부쓰덴 가스가타이샤마에' 하차 걸어서 약 12분"),
   tips=["12월 둘째 일요일 뒤부터 3월 셋째 토요일 전까지는 입산 기간이 아니라 올라갈 수 없어요(2026년은 12월 13일까지).", "가파른 잔디 비탈이라 미끄럽지 않은 신발을 신고, 도다이지와 묶어 오후에 올라요."],
   src=[_NSK_WAKA],
   checked="2026-11-27", photo=None),
 "nr_museum": dict(
   one="나라 공원 안에 있는 불교 미술 박물관이에요. 해마다 가을 특별전 등 특별 전시가 열려요.",
   see=[("명품 전시", "불교 회화·공예"), ("특별전", "기간마다 따로 열림"), ("공원 안 위치", "고후쿠지와 도다이지 사이")],
   facts=dict(hours="9:30~17:00 (입장 16:30까지)", fee="성인 700엔, 대학생 350엔, 고교생 이하 무료 (특별전 별도)", stay="약 1시간 30분", when="낮 (비 오는 날 좋음)", access="긴테쓰나라역에서 걸어서 약 15분, 순환 버스 '히무로진자·고쿠리쓰하쿠부쓰칸' 하차"),
   tips=["월요일(공휴일이면 다음 날)과 연말연시에 쉬어요.", "불교 조각관은 2026년 9월 14일부터 보수 공사로 닫아 2028년 봄쯤까지 볼 수 없어요.", "주차장이 없어 걸어서 가거나 순환 버스를 타요."],
   src=[_NSK_MUSEUM],
   checked="2026-11-27", photo=None),
}

GUIDE = {
 "slug": "nara-from-osaka",
 "name": "오사카에서 나라 가는 법",
 "date": "2026-11-27",
 "kw": ("나라사슴공원", 4320),
 "title": "나라 사슴공원 가는 법 — 오사카에서 긴테쓰·JR 요금과 시간, 패스, 나라 공원·도다이지 동선",
 "desc": "오사카에서 나라 가는 법을 긴테쓰 난바역~긴테쓰나라역(680엔·약 40분)과 JR 난바·오사카역~JR나라역 비교, 긴테쓰 레일 패스·간사이 미니 패스, 사슴 센베이 주의점과 나라 공원·도다이지 동선까지 공식 안내 기준으로 정리했습니다.",
 "answer": "오사카에서 나라는 <b>긴테쓰 오사카난바역 → 긴테쓰나라역</b>이 가장 편해요. 급행으로 <b>약 40분, 어른 680엔</b>(2026년 기준)이고 역에서 <b>나라 공원</b>까지 걸어서 약 5~8분이에요. 우메다(오사카역) 쪽 숙소라면 <b>JR 야마토지 쾌속</b>으로 JR나라역까지 약 50분이지만, 도다이지까지 더 걸어야 해요.",
 "body": [
  ("긴테쓰: 오사카난바 → 긴테쓰나라 (추천)",
   "<p>난바·신사이바시·도톤보리 쪽 숙소라면 긴테쓰 나라선이 갈아타기 없이 가요. 오사카메트로·한신 난바역과 이어진 <b>긴테쓰 오사카난바역</b>에서 타요.</p>"
   "<ul><li><b>시간</b>: 쾌속급행·급행 약 40분, 특급 약 35분</li>"
   "<li><b>어른 운임</b>: 680엔 (2025.4.1 기준, 어린이 반값)</li>"
   "<li><b>특급</b>: 운임 외에 특급권이 따로 들어요(긴테쓰 규칙상 40km까지 520엔, 방문 전 확인). 급행과 시간 차이가 크지 않아 보통은 급행으로 충분해요.</li>"
   "<li>관광 특급 <b>아오니요시</b>는 오사카난바·긴테쓰나라·교토를 잇는 별도 요금 열차예요.</li></ul>"
   "<p>긴테쓰나라역에서 <b>고후쿠지</b>까지 걸어서 약 5분, <b>나라 공원</b>까지 약 5~8분, <b>도다이지</b>까지 약 15분이라 걷는 거리가 가장 짧아요.</p>"),
  ("JR: 난바·덴노지·오사카역 → JR나라",
   "<ul><li><b>JR 난바 → 나라</b>: 야마토지 쾌속 약 49분, 어른 580엔 (2025.4.1 기준)</li>"
   "<li><b>덴노지 → 나라</b>: 약 36분, 어른 510엔 (2025.4.1 기준)</li>"
   "<li><b>오사카역 → 나라</b>: 야마토지 쾌속 직통 약 50분 (운임은 방문 전 확인)</li>"
   "<li><b>특급 마호로바</b>: 토·일·공휴일에 오사카·신오사카~나라를 달려요. e5489 예약 특급권 860엔(운임 별도)이에요.</li></ul>"
   "<p>JR나라역은 <b>나라 공원</b>까지 걸어서 약 15~20분이라 긴테쓰보다 멀어요. 역 앞에서 순환 버스를 타면 '겐초마에'까지 약 7분이에요. JR 패스를 가지고 있다면 JR 쪽이 추가 요금이 없어요(긴테쓰는 JR 패스로 못 타요).</p>"),
  ("패스: 긴테쓰 레일 패스·간사이 미니 패스",
   "<ul><li><b>긴테쓰 레일 패스 1day</b>: 어른 1,900엔, 어린이 950엔. 오사카난바~긴테쓰나라, 교토~ 등 지정 구간과 나라교통 버스(나라 공원·니시노쿄·호류지)를 하루 무제한. 온라인으로 사서 바로 써요. 2day는 3,700엔.</li>"
   "<li><b>간사이 미니 패스</b>(JR서일본): 3일 연속 어른 3,000엔, 어린이 1,500엔. 오사카·교토·고베·나라 JR 쾌속·보통 무제한. 해외 여행사에서 E티켓을 사서 일본에서 교환해요(단기 체류 외국인만).</li>"
   "<li><b>간사이 에어리어 패스</b>(JR서일본)는 2026년 9월 30일로 판매가 끝났어요. 그 전에 산 패스만 기간 안에 써요.</li></ul>"
   "<p>긴테쓰 왕복은 1,360엔이라 나라 안에서 버스를 여러 번 타거나 호류지까지 갈 때 레일 패스가 이득이에요. 두 패스 모두 특급은 별도예요. JR 패스 본전은 <a href=\"/jr_pass_value_calculator.html\">JR 패스 계산기</a>로 따져 봐요.</p>"),
  ("구간별 정리",
   "<div class=\"at-table\"><table><thead><tr><th>구간</th><th>시간(약)</th><th>어른 운임</th></tr></thead><tbody>"
   "<tr><td>긴테쓰 오사카난바 → 긴테쓰나라</td><td>40분 (특급 35분)</td><td>680엔 (특급권 별도)</td></tr>"
   "<tr><td>JR 난바 → JR나라</td><td>49분</td><td>580엔</td></tr>"
   "<tr><td>JR 덴노지 → JR나라</td><td>36분</td><td>510엔</td></tr>"
   "<tr><td>JR 오사카역 → JR나라</td><td>50분</td><td>방문 전 확인</td></tr>"
   "<tr><td>긴테쓰 레일 패스 1day</td><td>하루</td><td>1,900엔</td></tr>"
   "</tbody></table></div>"
   "<p>운임은 긴테쓰·JR서일본 공식 운임(2025.4.1 기준)이에요. 긴테쓰나라역이 나라 공원·고후쿠지에 더 가까워요.</p>"),
  ("도착 뒤 동선: 고후쿠지 → 나라 공원 → 도다이지",
   "<ol><li>긴테쓰나라역 → <b>고후쿠지</b> 오층탑 (걸어서 약 5분, 입장료 현금만)</li>"
   "<li><b>나라 공원</b>에서 사슴 센베이 주기</li>"
   "<li><b>도다이지</b> 대불전 (성인 800엔, 11~3월 8:00~17:00)</li>"
   "<li>시간이 있으면 <b>가스가타이샤</b> 등롱 길 → 남쪽 <b>나라마치</b> 골목</li></ol>"
   "<p>반나절이면 고후쿠지·나라 공원·도다이지까지, 하루면 가스가타이샤·나라마치까지 돌아요. 권역별 일정은 <a href=\"/travel-nara.html\">나라 여행 코스</a>에, 오사카 쪽 일정은 <a href=\"/travel-osaka.html\">오사카 여행 코스</a>에 있어요. 장소 위치는 <a href=\"/klink/#nr_park\">K링크 지도에서 나라 공원 보기</a>와 <a href=\"/klink/#nr_todaiji\">도다이지 보기</a>로 확인해요.</p>"),
  ("사슴 센베이·주의할 점",
   "<ul><li>사슴 센베이는 <b>10장 한 묶음 200엔</b>으로 공원 곳곳 노점·기념품 가게에서 팔아요. 저녁엔 가스가타이샤 쪽 자판기 2곳에서 사요.</li>"
   "<li>센베이 말고 다른 음식은 절대 주지 않아요. 산 뒤엔 띠지(종이)를 먼저 떼요.</li>"
   "<li>주는 척하며 놀리면 깨물 수 있어 망설이지 말고 빨리 줘요. 다 주면 두 손바닥을 펴 보여요.</li>"
   "<li>지도·팸플릿·비닐봉지를 먹어 버릴 수 있어 가방에 넣어요. 공원에 쓰레기통이 없어요.</li>"
   "<li>가을엔 수사슴이 예민하고, 5월 중순~7월엔 새끼를 지키는 어미 사슴이 예민해 가까이 가지 않아요.</li></ul>"
   "<div class=\"b-tip\"><p><b>실전 팁</b> 난바 쪽 숙소면 긴테쓰 급행, 우메다 쪽이면 JR 야마토지 쾌속이 갈아타기가 적어요. 고후쿠지 입장료는 현금만 받아 엔화 현금을 챙기고, 경비는 <a href=\"/japan_travel_calculator.html\">일본 여행 경비 계산기</a>와 <a href=\"/exchange_rate_calculator.html\">환율 계산기</a>로 맞춰 봐요.</p></div>"),
 ],
 "faq": [
  ("오사카에서 나라까지 얼마나 걸려요?", "긴테쓰 오사카난바역에서 긴테쓰나라역까지 급행으로 약 40분, JR 오사카역에서 JR나라역까지 야마토지 쾌속으로 약 50분이에요."),
  ("긴테쓰 요금은 얼마예요?", "오사카난바~긴테쓰나라 어른 편도 680엔이에요(2026년 기준). 특급을 타면 특급권이 따로 들어요(방문 전 확인)."),
  ("긴테쓰와 JR 중 뭐가 나아요?", "긴테쓰나라역이 나라 공원·도다이지와 가까워 걷는 거리가 짧아요. JR 패스가 있거나 우메다 쪽 숙소면 JR도 좋아요."),
  ("간사이 에어리어 패스로 갈 수 있어요?", "간사이 에어리어 패스는 2026년 9월 30일에 판매가 끝났어요. 지금은 긴테쓰 레일 패스 1day(1,900엔)나 간사이 미니 패스(3일 3,000엔)를 따져 봐요."),
  ("사슴에게 아무거나 줘도 돼요?", "아니요. 사슴 센베이(10장 200엔)만 줘요. 놀리면 깨물 수 있어 빨리 주고, 지도·비닐봉지는 가방에 넣어요."),
 ],
 "tools": ["jr_pass_value_calculator", "japan_travel_calculator", "exchange_rate_calculator"],
 "sources": [
  ("긴테쓰 — 운임·특급요금표 (오사카난바~긴테쓰나라) (확인 2026.11.27)", "https://www.kintetsu.co.jp/railway/Dia/pdf/price_limited_express_e.pdf"),
  ("긴테쓰 — 여객영업규칙 특별급행요금 (확인 2026.11.27)", "https://www.kintetsu.co.jp/gyoumu/kippu/pdf/16_kisoku_2-03-07.pdf"),
  ("긴테쓰 — KINTETSU RAIL PASS 1day (확인 2026.11.27)", "https://www.kintetsu.co.jp/foreign/english/ticket/krp_1day.html"),
  ("JR서일본 — 게이한신 운임 체계 재검토 (2025.4.1 시행 특정 운임) (확인 2026.11.27)", "https://www.westjr.co.jp/press/article/items/240515_00_press_keihanshin_unchin.pdf"),
  ("JR서일본 — 팩트시트 2025 사철 경쟁 구간 (운임 2025.4.1 현재) (확인 2026.11.27)", "https://www.westjr.co.jp/company/ir/library/fact/pdf/2025/fact09.pdf"),
  ("JR서일본 — 특급 마호로바 운행 정보 (확인 2026.11.27)", "https://www.jr-odekake.net/railroad/mahorobalimitedexpress/service.html"),
  ("JR서일본 — Kansai Mini Pass (확인 2026.11.27)", "https://www.westjr.co.jp/travel-information/en/tickets-passes/jrwest-rail-pass/kansaimini/"),
  ("JR서일본 — Kansai Area Pass (판매 종료 안내) (확인 2026.11.27)", "https://www.westjr.co.jp/travel-information/en/tickets-passes/jrwest-rail-pass/kansai/"),
  ("나라현 관광 공식 Visit Nara — Travel to Nara (확인 2026.11.27)", "https://www.visitnara.jp/travel-to-nara/"),
  ("나라시 관광협회 — Access (확인 2026.11.27)", "https://narashikanko.or.jp/en/access/index.html"),
  ("나라시 관광협회 — 나라 공원 사슴 특집 (확인 2026.11.27)", "https://narashikanko.or.jp/feature/deer"),
  ("도다이지 공식 — Opening Hours / Admission Fees (확인 2026.11.27)", "https://www.todaiji.or.jp/en/information/haikan/"),
  ("나라 사슴 애호회 — 5월 중순~7월 어미 사슴 주의 (확인 2026.11.27)", "http://naradeer.com/blog/2022/05/02/5%E6%9C%88%E4%B8%AD%E6%97%AC%EF%BD%9E7%E6%9C%88%E9%A0%83%E3%81%AF%E6%AF%8D%E5%AD%90%E9%B9%BF%E3%81%AB%E6%B3%A8%E6%84%8F%EF%BC%81/"),
 ],
}
