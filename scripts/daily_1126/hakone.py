# -*- coding: utf-8 -*-
"""hakone — 2026-11-26 새 해외 지역 '하코네'(일본, K링크 region id hakone, 장소 id 접두어 ha_) 데이터 + 가이드 1개. 확인일 2026-11-26.
못 쓴 글: 없음 (ARTICLES 비움, GUIDE 1개).
메모(총괄용):
- 장소는 기존 /travel-hakone.html 본문에 나온 곳만: 하코네유모토 온천가, 하코네 등산열차, 하코네 등산 케이블카, 하코네 로프웨이,
  오와쿠다니, 아시노코 해적선(글에서는 '아시노코 유람선'), 하코네 신사 — 7곳. 조각의 숲 미술관·고라 공원·온시하코네 공원은 글에
  이름이 없어(‘고라 미술관’만 있음) 넣지 않았어요.
- 도쿄(overseas_data.py) 블록에 이미 tk_hakone(하코네 당일치기 한 점)이 있어요. 새 region hakone 과 겹치니 총괄이 정리 여부 판단.
- 프리패스 가격: hakonenavi.jp 공식 Freepass 페이지(2025.10.1 개정가) — 신주쿠 2일 7,100엔/3일 7,500엔, 오다와라 2일 6,000엔/3일 6,400엔
  (성인). 어린이 신주쿠 1,600/1,850엔, 오다와라 1,500/1,750엔. 2026.11.26 현재 같은 값으로 게시.
- 로망스카 특급권 1,200엔: hakonenavi 당일 코스 글(course/244)의 '신주쿠 출발 별도 1,200엔' 기준. 열차·구간에 따라 다를 수 있어 '약'·'방문 전 확인'.
- 로프웨이 2,000엔(소운잔~도겐다이 편도 단일 요금, 2025.10.1 개정) — hakonenavi 공지 PDF. 등산열차·케이블카·해적선·버스 단독 요금은 공식 숫자를 못 열어 '방문 전 확인'.
- odakyu-global.com(오다큐 공식 블로그·한국어 프리패스 페이지)은 열람 승인 시간 초과로 못 열었어요. 대신 hakonenavi.jp(오다큐 하코네 공식)로 확인.
- 하코네 신사 참배 시간·요금, 아시노코 해적선 첫·막배 시각, 케이블카 소요 시간은 공식 확인 못 함 → '방문 전 확인'·'약'.
- 좌표: 역·항구·신사 대표 지점의 대략값(소수 4자리). 공항 이동 분(HND 120, NRT 180)은 대략값.
"""

ARTICLES = []
COORDS = {}

# 도시 메타 (scripts/klink/tools/overseas_data.py 에 붙일 블록, 'C boracay' 형식)
CITY_LINES = """C hakone jp 35.2328 139.1067 1 150 | 하코네|箱根|Hakone|箱根 | 온천 료칸과 화산 계곡, 아시노코를 한 바퀴 도는 도쿄 근교 | Hot-spring inns, a volcanic valley and the Lake Ashi loop near Tokyo
A HND 35.5494 139.7798 120 | 하네다공항|羽田机场|Haneda (HND)|羽田空港
A NRT 35.7720 140.3929 180 | 나리타공항|成田机场|Narita (NRT)|成田空港
S ha_s1 35.2328 139.1067 | 하코네유모토역 주변|箱根汤本站周边|Around Hakone-Yumoto Stn|箱根湯本駅周辺 | 로망스카 도착역, 온천가·버스 출발점 | Romancecar terminus, onsen street and bus hub
S ha_s2 35.2497 139.0478 | 고라역 주변|强罗站周边|Around Gora Stn|強羅駅周辺 | 케이블카·로프웨이로 바로 오르는 산 위 거점 | Hillside base right by the cable car and ropeway
Z ha_z1 | 하코네유모토 | Hakone-Yumoto
P ha_yumoto shop 35.2323 139.1048 2 eve o=S | 하코네유모토 온천가|箱根汤本温泉街|Hakone-Yumoto Onsen Street|箱根湯本温泉街 | 로망스카 도착역 앞 온천·상점 거리 | Onsen and shopping street by the Romancecar terminus
P ha_tozan fun 35.2497 139.0478 1 am o=D | 하코네 등산열차|箱根登山电车|Hakone Tozan Train|箱根登山電車 | 스위치백으로 고라까지 오르는 산악 열차 | Switchback mountain train up to Gora
Z ha_z2 | 고라·소운잔·오와쿠다니 | Gora, Sounzan & Owakudani
P ha_cablecar fun 35.2551 139.0369 0.5 am o=D | 하코네 등산 케이블카|箱根登山缆车|Hakone Tozan Cable Car|箱根登山ケーブルカー | 고라에서 소운잔까지 오르는 케이블카 | Cable car from Gora up to Sounzan
P ha_ropeway fun 35.2551 139.0369 1 am o=D | 하코네 로프웨이|箱根空中缆车|Hakone Ropeway|箱根ロープウェイ | 소운잔~오와쿠다니~도겐다이 곤돌라 | Gondola from Sounzan over Owakudani to Togendai
P ha_owakudani nature 35.2440 139.0196 1.5 am o=D | 오와쿠다니|大涌谷|Owakudani|大涌谷 | 연기 오르는 화산 계곡과 검은 달걀 | Steaming volcanic valley and black eggs
Z ha_z3 | 아시노코·모토하코네 | Lake Ashi & Moto-Hakone
P ha_cruise fun 35.2027 139.0264 1 o=D | 아시노코 해적선|芦之湖海盗船|Lake Ashi Pirate Ship|芦ノ湖海賊船 | 도겐다이~모토하코네 호수 유람선 | Lake Ashi cruise from Togendai to Moto-Hakone
P ha_shrine palace 35.2058 139.0246 1 am o=D | 하코네 신사|箱根神社|Hakone Shrine|箱根神社 | 호수 위 붉은 평화의 도리이 | Lakeside shrine with the red Peace Torii"""

# K링크 장소 데이터 (해외 cost=0). 좌표는 역·항구·신사 대표 지점의 대략값.
PLACES = {
 "ha_yumoto": dict(
   ko=("하코네유모토 온천가", "로망스카 도착역 앞 온천·상점 거리"), en=("Hakone-Yumoto Onsen Street", "Onsen and shopping street by the Romancecar terminus"),
   zh=("箱根汤本温泉街", "浪漫特快终点站前的温泉商店街"), ja=("箱根湯本温泉街", "ロマンスカー終着駅前の温泉街"),
   lat=35.2323, lng=139.1048, o=[9, 21], cost=0, closed=[], best="eve", meal="any", h=2, cat="shop", st=""),
 "ha_tozan": dict(
   ko=("하코네 등산열차", "스위치백으로 고라까지 오르는 열차"), en=("Hakone Tozan Train", "Switchback mountain train up to Gora"),
   zh=("箱根登山电车", "之字形爬升至强罗的登山电车"), ja=("箱根登山電車", "スイッチバックで強羅へ登る電車"),
   lat=35.2497, lng=139.0478, o=[6, 23], cost=0, closed=[], best="am", meal=None, h=1, cat="fun", st=""),
 "ha_cablecar": dict(
   ko=("하코네 등산 케이블카", "고라에서 소운잔까지 오르는 케이블카"), en=("Hakone Tozan Cable Car", "Cable car from Gora up to Sounzan"),
   zh=("箱根登山缆车", "从强罗上到早云山的缆车"), ja=("箱根登山ケーブルカー", "強羅から早雲山へ登るケーブルカー"),
   lat=35.2551, lng=139.0369, o=[9, 17], cost=0, closed=[], best="am", meal=None, h=0.5, cat="fun", st=""),
 "ha_ropeway": dict(
   ko=("하코네 로프웨이", "소운잔~오와쿠다니~도겐다이 곤돌라"), en=("Hakone Ropeway", "Gondola from Sounzan over Owakudani to Togendai"),
   zh=("箱根空中缆车", "早云山~大涌谷~桃源台的空中缆车"), ja=("箱根ロープウェイ", "早雲山~大涌谷~桃源台のゴンドラ"),
   lat=35.2551, lng=139.0369, o=[9, 17], cost=0, closed=[], best="am", meal=None, h=1, cat="fun", st=""),
 "ha_owakudani": dict(
   ko=("오와쿠다니", "연기 오르는 화산 계곡과 검은 달걀"), en=("Owakudani", "Steaming volcanic valley and black eggs"),
   zh=("大涌谷", "冒着白烟的火山谷与黑鸡蛋"), ja=("大涌谷", "噴煙の上がる火山の谷と黒たまご"),
   lat=35.2440, lng=139.0196, o=[9, 16.5], cost=0, closed=[], best="am", meal="any", h=1.5, cat="nature", st=""),
 "ha_cruise": dict(
   ko=("아시노코 해적선", "도겐다이~모토하코네 호수 유람선"), en=("Lake Ashi Pirate Ship", "Lake Ashi cruise from Togendai to Moto-Hakone"),
   zh=("芦之湖海盗船", "桃源台~元箱根的湖上游船"), ja=("芦ノ湖海賊船", "桃源台~元箱根の遊覧船"),
   lat=35.2027, lng=139.0264, o=[9.5, 17], cost=0, closed=[], best="day", meal=None, h=1, cat="fun", st=""),
 "ha_shrine": dict(
   ko=("하코네 신사", "호수 위 붉은 평화의 도리이"), en=("Hakone Shrine", "Lakeside shrine with the red Peace Torii"),
   zh=("箱根神社", "湖上红色和平鸟居"), ja=("箱根神社", "湖上に立つ赤い平和の鳥居"),
   lat=35.2058, lng=139.0246, o=[9, 17], cost=0, closed=[], best="am", meal=None, h=1, cat="palace", st=""),
}

# 숙소 권역 2곳 (상호 아님)
STAYS = [
 ("ha_s1", 35.2328, 139.1067,
  ["하코네유모토역 주변", "箱根汤本站周边", "Around Hakone-Yumoto Stn", "箱根湯本駅周辺"],
  ["로망스카 도착역, 온천가·버스 출발점", "浪漫特快终点站，温泉街与巴士起点", "Romancecar terminus, onsen street and bus hub", "ロマンスカー終着駅、温泉街とバスの起点"]),
 ("ha_s2", 35.2497, 139.0478,
  ["고라역 주변", "强罗站周边", "Around Gora Stn", "強羅駅周辺"],
  ["케이블카·로프웨이로 바로 오르는 산 위 거점", "可直接换乘缆车和空中缆车", "Hillside base right by the cable car and ropeway", "ケーブルカー・ロープウェイにすぐ乗れる山の拠点"]),
]

_NAVI_COURSE = ("하코네 내비(오다큐) — 하코네 당일 코스", "https://www.hakonenavi.jp/international/en/course/244")
_NAVI_ROPEWAY = ("하코네 내비 — Hakone Ropeway", "https://www.hakonenavi.jp/international/en/transportation/hakone-ropeway")
_NAVI_CRUISE = ("하코네 내비 — Hakone Sightseeing Cruise", "https://www.hakonenavi.jp/international/en/transportation/hakone-kankosen")
_NAVI_FREEPASS = ("하코네 내비 — Hakone Freepass", "https://www.hakonenavi.jp/international/en/discount_passes/free_pass")
_NAVI_OWAKU = ("하코네 내비 — 오와쿠다니 새 역·어스 밸리", "https://www.hakonenavi.jp/international/en/article/4226")

# 명소 안내 (K링크 장소 상세 화면). 공식 출처로 확인한 것만, 나머지는 '방문 전 확인'.
SPOTS = {
 "ha_yumoto": dict(
   one="로망스카가 도착하는 하코네유모토역 앞 온천 마을이에요. 하코네 한 바퀴의 출발점이자 마지막에 기념품을 사는 곳이에요.",
   see=[("하코네유모토역", "로망스카·등산열차·버스가 모이는 입구"), ("역 앞 상점가", "온천 만주·어묵 등 기념품 가게"), ("당일 온천", "료칸·온천 시설에서 당일 입욕")],
   facts=dict(hours="가게마다 다름, 방문 전 확인", fee="무료 (온천·쇼핑 비용 별도)", stay="약 2시간", when="저녁 (한 바퀴 돈 뒤)", access="신주쿠에서 로망스카로 약 1시간 30분"),
   tips=["하코네유모토역 짐 보관은 900엔부터(세금 포함)이고 숙소로 짐을 보내는 서비스도 있어 짐을 맡기고 한 바퀴 돌면 편해요.", "역 안 기념품 매장은 21시까지 열어 돌아가는 로망스카에서 먹을 도시락을 마지막에 사요.", "모토하코네에서 돌아오는 저녁 버스는 길이 막혀 늦어지기 쉬워 돌아가는 로망스카는 여유 있게 잡아요."],
   src=[_NAVI_COURSE],
   checked="2026-11-26", photo=None),
 "ha_tozan": dict(
   one="오다와라에서 고라까지 산을 오르는 산악 열차예요. 가파른 비탈에서 앞뒤 방향을 바꾸는 스위치백으로 올라가요.",
   see=[("스위치백", "열차가 지그재그로 방향을 바꿔요"), ("해발 541m 고라", "오다와라(14m)에서 산 위까지"), ("창밖 산골 풍경", "계곡과 다리를 지나요")],
   facts=dict(hours="첫·막차 방문 전 확인", fee="하코네 프리패스로 탑승 (단독 요금 방문 전 확인)", stay="유모토~고라 약 40분", when="오전", access="하코네유모토역에서 바로 환승"),
   tips=["하코네 프리패스로 타고 내릴 수 있어 조각의 숲역 등 중간역에 내려 들렀다 가도 돼요.", "오전에 유모토에서 출발해야 케이블카·로프웨이·해적선까지 하루에 이어져요."],
   src=[_NAVI_COURSE, _NAVI_FREEPASS],
   checked="2026-11-26", photo=None),
 "ha_cablecar": dict(
   one="고라역에서 소운잔역까지 비탈을 곧게 오르는 케이블카예요. 소운잔에서 하코네 로프웨이로 갈아타요.",
   see=[("고라역", "등산열차에서 바로 갈아타요"), ("비탈길 오르막", "계단식 객차로 산을 올라요"), ("소운잔역", "로프웨이 환승역")],
   facts=dict(hours="방문 전 확인", fee="하코네 프리패스로 탑승 (단독 요금 방문 전 확인)", stay="약 10분 (대략)", when="오전", access="하코네 등산열차 고라역에서 환승"),
   tips=["주말 오전엔 고라역 환승 줄이 길어 이른 시간에 올라가면 기다림이 줄어요.", "하코네 프리패스 구간이라 따로 표를 사지 않아도 돼요."],
   src=[_NAVI_COURSE, _NAVI_FREEPASS],
   checked="2026-11-26", photo=None),
 "ha_ropeway": dict(
   one="소운잔에서 오와쿠다니를 지나 아시노코 도겐다이까지 가는 곤돌라예요. 맑은 날엔 후지산이 보여요.",
   see=[("오와쿠다니 위 구간", "연기 오르는 화산 계곡을 내려다봐요"), ("후지산 전망", "맑은 날 창밖으로 보여요"), ("도겐다이", "아시노코 해적선 타는 곳")],
   facts=dict(hours="2~11월 9:00~17:00, 12~1월 막 탑승 16:15 (2026년 기준)", fee="소운잔~도겐다이 편도 2,000엔 (2025.10 개정), 하코네 프리패스 포함", stay="구간마다 약 15분, 오와쿠다니에서 갈아탐", when="오전 (맑은 날)", access="하코네 등산 케이블카 소운잔역에서 환승"),
   tips=["정기 점검으로 오와쿠다니~소운잔은 2026.12.7~12.24, 도겐다이~오와쿠다니는 2027.1.12~2.26에 쉬고 대체 버스가 다녀요(프리패스로 탈 수 있음).", "풍속 30m/s 이상이나 악천후면 멈춰 출발 전 하코네 내비 운행 정보를 확인해요.", "후지산은 오전에 잘 보이는 날이 많아 아침 일찍 타는 쪽이 좋아요."],
   src=[_NAVI_ROPEWAY, ("하코네 내비 — 로프웨이 등 요금 개정 (2025.10.1)", "https://www.hakonenavi.jp/international/en/wp-content/uploads/sites/2/2025/09/re_price202510.pdf")],
   checked="2026-11-26", photo=None),
 "ha_owakudani": dict(
   one="약 3,000년 전 생긴 화산 계곡으로 지금도 연기가 올라요. 온천물에 삶아 껍데기가 검은 '검은 달걀'이 유명해요.",
   see=[("어스 밸리 전망대", "2025년 새로 연 분기구 위 유리 데크"), ("검은 달걀", "4개 500엔(세금 포함)"), ("하코네 지오뮤지엄", "화산 정보 무료 구역")],
   facts=dict(hours="구로타마고칸 2~11월 9:00~16:20, 12~1월 9:00~16:00 (2025년 기준)", fee="무료 (먹거리 별도)", stay="약 1시간 30분", when="오전", access="하코네 로프웨이 오와쿠다니역에서 바로"),
   tips=["가게가 16시 무렵 닫아 오전~이른 오후에 들러요.", "화산 활동·가스 상황에 따라 출입이 제한될 수 있어 당일 하코네 내비 운행 정보를 확인해요.", "역 2층 식당(10:30~16:30)에서 오와쿠다니 카레로 점심을 해결하면 동선이 짧아요."],
   src=[_NAVI_OWAKU, _NAVI_COURSE],
   checked="2026-11-26", photo=None),
 "ha_cruise": dict(
   one="아시노코를 건너는 하코네 관광선으로, 해적선 모양 배 3척이 다녀요. 도겐다이에서 하코네마치·모토하코네 항으로 가요.",
   see=[("해적선 디자인 배", "모양이 다른 3척"), ("아시노코 호수", "맑은 날 후지산"), ("모토하코네 항", "하코네 신사까지 걸어서 약 10분")],
   facts=dict(hours="첫·막배 방문 전 확인 (겨울 12.1~3.19 다이어 따로)", fee="하코네 프리패스로 일반실 무제한 (특별실 추가 요금)", stay="편도 약 25~35분", when="낮", access="하코네 로프웨이 도겐다이역 바로 앞 도겐다이 항"),
   tips=["승선은 출발 5~10분 전에 시작해 그 전에 항구에 와 있어요.", "짙은 안개·강풍엔 결항·변경될 수 있어 하코네 내비 운행 정보를 확인해요."],
   src=[_NAVI_CRUISE, _NAVI_FREEPASS],
   checked="2026-11-26", photo=None),
 "ha_shrine": dict(
   one="아시노코 호숫가에 있는 1,260년 넘은 신사예요. 호수 위에 선 붉은 '평화의 도리이'가 사진 명소예요.",
   see=[("평화의 도리이", "1952년 세운 호수 위 붉은 도리이"), ("본전", "1936년 다시 지은 건물"), ("구즈류 신사 신궁", "아시노코 수호신 구두룡")],
   facts=dict(hours="방문 전 확인", fee="경내 무료 (방문 전 확인)", stay="약 1시간", when="오전 (평화의 도리이 사진 줄이 짧음)", access="모토하코네 항에서 걸어서 약 10분"),
   tips=["평화의 도리이 앞 사진 줄은 낮에 길어지기 쉬워 이른 시간에 가요.", "모토하코네에서 하코네유모토로 돌아가는 버스(K·R·H 노선)로 약 40분이라 한 바퀴의 마지막에 넣어요."],
   src=[_NAVI_COURSE, ("일본 관광청 다국어 해설 — Hakone Shrine", "https://www.mlit.go.jp/tagengo-db/en/R1-01104.html")],
   checked="2026-11-26", photo=None),
}

GUIDE = {
 "slug": "hakone-freepass",
 "name": "하코네 프리패스",
 "date": "2026-11-26",
 "kw": ("하코네프리패스", 1200),
 "title": "하코네 프리패스 — 2026년 가격·포함 교통·사는 곳·본전 뽑는 순환 코스",
 "desc": "하코네 프리패스 2026년 가격(신주쿠·오다와라 출발 2일·3일), 등산열차·케이블카·로프웨이·해적선·버스 포함 범위, EMot 온라인·역 구매처, 로망스카 특급권 별도 요금, 본전 뽑는 한 바퀴 코스를 오다큐 공식 안내 기준으로 정리했습니다.",
 "answer": "하코네 프리패스는 출발역~오다와라 오다큐선 왕복과 하코네 안 <b>등산열차·케이블카·로프웨이·해적선·버스</b>를 2일 또는 3일 마음껏 타는 표예요. 성인 기준 <b>신주쿠 출발 2일 7,100엔·3일 7,500엔</b>, <b>오다와라 출발 2일 6,000엔·3일 6,400엔</b>이에요(2025.10.1 개정, 2026년 기준). <b>로망스카 특급권은 따로</b> 사야 해요.",
 "body": [
  ("가격 (2026년 기준)",
   "<div class=\"at-table\"><table><thead><tr><th>출발</th><th>2일</th><th>3일</th></tr></thead><tbody>"
   "<tr><td>신주쿠 (성인)</td><td>7,100엔</td><td>7,500엔</td></tr>"
   "<tr><td>신주쿠 (어린이)</td><td>1,600엔</td><td>1,850엔</td></tr>"
   "<tr><td>오다와라 (성인)</td><td>6,000엔</td><td>6,400엔</td></tr>"
   "<tr><td>오다와라 (어린이)</td><td>1,500엔</td><td>1,750엔</td></tr>"
   "</tbody></table></div>"
   "<p>2025년 10월 1일에 1,000엔 올랐어요(이전 신주쿠 2일 6,100엔). 도쿄역에서 신칸센으로 오다와라까지 간다면 <b>오다와라 출발</b>을 사요. 1일권은 없어 당일치기도 2일권을 써요.</p>"),
  ("포함 교통",
   "<ul><li><b>하코네 등산열차</b>: 오다와라·하코네유모토~고라</li>"
   "<li><b>하코네 등산 케이블카</b>: 고라~소운잔</li>"
   "<li><b>하코네 로프웨이</b>: 소운잔~오와쿠다니~도겐다이 (단독 편도 2,000엔)</li>"
   "<li><b>아시노코 해적선</b>: 하코네 관광선 일반실 (특별실은 추가 요금)</li>"
   "<li>하코네 등산버스·오다큐 하코네 고속버스·도카이버스(지정 구간), 관광시설 순환 버스</li>"
   "<li>오다큐선 출발역~오다와라 왕복 1회 (중간 승하차 가능)</li></ul>"
   "<p>이즈하코네버스는 못 타요. 지정 구간 밖은 요금을 따로 내고, 약 70곳 관광 시설 입장료 할인이 붙어요.</p>"),
  ("어디서 사요",
   "<ul><li><b>EMot 온라인 티켓</b>: 스마트폰으로 사고 QR로 타요</li>"
   "<li><b>오다큐선 역</b>(신주쿠~오다와라): 출발 1개월 전부터, 당일 표는 발매기에서도</li>"
   "<li>오다와라역 오다큐 발매기·오다큐 관광 서비스 센터, 하코네유모토·고라·소운잔역 발매기</li>"
   "<li>세븐일레븐(7-Ticket), 오다큐 여행 창구</li></ul>"
   "<p>마지막에 내리는 역에서 표를 회수해요. 악천후로 운휴하면 안 탄 교통만 마지막 역에서 환불해요.</p>"),
  ("본전 뽑는 순환 코스",
   "<ol><li>신주쿠 → 하코네유모토 (로망스카 약 1시간 30분)</li>"
   "<li><b>하코네 등산열차</b>로 고라 (약 40분)</li>"
   "<li><b>하코네 등산 케이블카</b>로 소운잔</li>"
   "<li><b>하코네 로프웨이</b>로 <b>오와쿠다니</b> (검은 달걀·점심) → 도겐다이</li>"
   "<li><b>아시노코 해적선</b>으로 모토하코네 (약 25~35분)</li>"
   "<li>걸어서 약 10분 <b>하코네 신사</b> 평화의 도리이</li>"
   "<li>버스로 <b>하코네유모토 온천가</b> (약 40분) → 신주쿠</li></ol>"
   "<p>로프웨이 편도만 2,000엔이라 이 한 바퀴를 돌면 오다큐선 왕복까지 합쳐 프리패스가 유리한 경우가 많아요(단독 요금 일부는 방문 전 확인). 당일·1박 2일 동선은 <a href=\"/travel-hakone.html\">하코네 여행 코스</a>에 정리했어요.</p>"
   "<p><b>로프웨이 점검 운휴</b>: 오와쿠다니~소운잔 2026.12.7~12.24, 도겐다이~오와쿠다니 2027.1.12~2.26에 대체 버스가 다니고, 프리패스로 탈 수 있어요.</p>"),
  ("로망스카 특급권은 별도",
   "<p>프리패스에는 오다큐선 <b>보통·급행 요금만</b> 들어 있어요. 신주쿠~하코네유모토 특급 <b>로망스카</b>를 타려면 특급권(약 1,200엔, 열차·구간에 따라 다름, 방문 전 확인)을 따로 사요. 지정석이라 주말엔 미리 예약하는 게 좋아요.</p>"
   "<p>예산은 <a href=\"/japan_travel_calculator.html\">일본 여행 경비 계산기</a>, 엔화 환전은 <a href=\"/exchange_rate_calculator.html\">환율 계산기</a>로 맞춰 보고, JR 패스와 비교하려면 <a href=\"/jr_pass_value_calculator.html\">JR 패스 계산기</a>를 써요. 도쿄 일정은 <a href=\"/travel-tokyo.html\">도쿄 여행 코스</a>에 있어요.</p>"
   "<div class=\"b-tip\"><p><b>실전 팁</b> 도쿄역 출발이면 신칸센으로 오다와라까지 가서 오다와라 출발 프리패스를 사요. 하코네 로프웨이는 아침에 후지산이 잘 보여 한 바퀴는 오전 일찍 시작해요.</p></div>"),
 ],
 "faq": [
  ("하코네 프리패스 가격은 얼마예요?", "성인 기준 신주쿠 출발 2일 7,100엔·3일 7,500엔, 오다와라 출발 2일 6,000엔·3일 6,400엔이에요(2025.10.1 개정, 2026년 기준)."),
  ("로망스카도 프리패스로 타요?", "아니요. 로망스카는 특급권(약 1,200엔, 방문 전 확인)을 따로 사야 해요. 오다큐선 보통·급행은 프리패스로 타요."),
  ("어떤 교통이 포함돼요?", "하코네 등산열차, 하코네 등산 케이블카, 하코네 로프웨이, 아시노코 해적선(일반실), 지정 구간 버스, 오다큐선 출발역~오다와라 왕복이에요. 이즈하코네버스는 안 돼요."),
  ("어디서 사요?", "EMot 온라인 티켓, 오다큐선 역(신주쿠~오다와라), 오다와라역, 하코네유모토·고라·소운잔역 발매기, 세븐일레븐에서 사요."),
  ("당일치기에도 이득이에요?", "하코네유모토에서 등산열차·케이블카·로프웨이·해적선·버스로 한 바퀴를 돌면 대체로 이득이에요. 로프웨이 편도만 2,000엔이에요."),
 ],
 "tools": ["japan_travel_calculator", "exchange_rate_calculator", "jr_pass_value_calculator"],
 "sources": [
  ("하코네 내비(오다큐 하코네 공식) — Hakone Freepass (가격·포함 교통·구매처) (확인 2026.11.26)", "https://www.hakonenavi.jp/international/en/discount_passes/free_pass"),
  ("하코네 내비 — 하코네 당일 코스 (로망스카 특급권 1,200엔·이동 순서) (확인 2026.11.26)", "https://www.hakonenavi.jp/international/en/course/244"),
  ("하코네 내비 — 로프웨이 등 요금 개정 (2025.10.1) (확인 2026.11.26)", "https://www.hakonenavi.jp/international/en/wp-content/uploads/sites/2/2025/09/re_price202510.pdf"),
  ("하코네 내비 — Hakone Ropeway 운행 시간 (확인 2026.11.26)", "https://www.hakonenavi.jp/international/en/transportation/hakone-ropeway"),
  ("하코네 내비 — Hakone Sightseeing Cruise (확인 2026.11.26)", "https://www.hakonenavi.jp/international/en/transportation/hakone-kankosen"),
 ],
}
