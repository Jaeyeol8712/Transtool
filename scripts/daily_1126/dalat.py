# -*- coding: utf-8 -*-
"""dalat — 2026-11-26 새 해외 지역 '달랏'(베트남, K링크 region id dalat, 장소 id 접두어 dl_) 데이터. 확인일 2026-11-26.
장소: travel-dalat.html 권역표·일정에 나오는 8곳(쑤언흐엉 호수·달랏 야시장·달랏 대성당·크레이지 하우스·다딴라 폭포·뚜옌럼 호수·죽림선원·로빈힐 케이블카·랑비앙 산).
  글의 '꽃 농장'은 특정 장소 이름이 없어 넣지 않았고, 달랏역은 글에 없어 넣지 않았어요.
못 쓴 것: GUIDE·ARTICLES 없음(지시대로).
메모(출처): 베트남 관광청 vietnam.travel 달랏 페이지는 호수·랑비앙·공항 30km 정도만 있고 요금·시간이 없어, 숫자는 vietnamtourism.com(Vietnam Tourism, 기존
  travel-dalat.html이 근거로 쓴 사이트)의 장소별 페이지(2026.10~11 갱신)와 럼동성 공식 신문 Bao Lam Dong(대성당 연도·높이)으로 확인했어요.
  럼동성 정부 사이트(lamdong.gov.vn)는 이 환경에서 열리지 않았어요(robots 확인 실패).
메모(확인 못 한·애매한 숫자):
  - 다딴라 알파인 코스터 요금: 같은 사이트 안에서 5만/8만, 10만, 15만 동으로 서로 달라 '방문 전 확인'. 입장료 5만 동은 두 페이지가 같아 씀. 운영 시간은 못 찾음.
  - 랑비앙 입장료: 장소 전용 페이지(2026.11.7 갱신) 성인 5만 동·지프 1인 12만 동을 썼고, 다른 페이지는 3만/10만 동이라 '약'·현장 확인 문구를 붙임.
  - 크레이지 하우스 6만 동·08:30~19:00은 한 페이지 값(입장료는 두 페이지가 같음). 대성당 관람·미사 시간은 공식 출처를 못 찾아 '방문 전 확인'.
  - 쑤언흐엉 호수 오리배는 2024년 11월부터 새 운영자 허가 대기로 멈춤(2026.11.11 갱신 페이지) -> 현장 확인으로 씀.
  - 좌표는 시설 주소 기준 대략값(소수 4자리). 죽림선원·로빈힐 케이블카는 케이블카 로빈힐 역(1 Dong Da) 기준.
메모(도시 줄): 인천-달랏 직항은 2026년 11월 현재 확인되지 않음(travel-dalat.html). 과거 직항 운항 기록은 있으나 지금 시간표가 없어,
  fly 값은 글의 '인천→나트랑(깜라인) 직항 약 5시간'을 따라 300분으로 둠(직항 재개 시 고칠 것). sub=0(차·택시 위주).
  공항 리엔크엉(DLI) 좌표 11.7500 108.3673(대략), 시내까지 셔틀 약 45분(vietnamtourism.com 셔틀 5만 동, 택시·그랩 35만~42만 동), 시내 남쪽 약 30km(vietnam.travel).
  도시 중심 좌표 11.9410 108.4400(쑤언흐엉 호수 서쪽 시내).
"""

CITY_LINES = """C dalat vn 11.9410 108.4400 0 300 | 달랏|大叻|Da Lat|ダラット | 해발 1,500m 고원 도시, 호수와 폭포·랑비앙 산 | Cool highland city with a lake, waterfalls and Lang Biang
A DLI 11.7500 108.3673 45 | 리엔크엉공항|连姜机场|Lien Khuong (DLI)|リエンクオン空港
S dl_stay_lake 11.94 108.443 | 쑤언흐엉 호수·시내 중심|春香湖·市中心|Xuan Huong Lake & Center|スアンフーン湖・中心部 | 호수 산책로와 광장이 가깝고 시내 대부분을 걸어서 다님 | Lakeside walks and the square nearby, most sights walkable
S dl_stay_market 11.9435 108.4365 | 달랏 야시장 주변|大叻夜市周边|Da Lat Night Market area|ダラット夜市周辺 | 야시장·달랏 시장 바로 옆, 저녁 먹거리와 택시 잡기 쉬움 | Next to the night market and Da Lat Market, easy food and taxis
Z dl_z1 | 달랏 시내 | Central Da Lat
P dl_xuanhuong nature 11.942 108.445 1.5 eve o=A | 쑤언흐엉 호수|春香湖|Xuan Huong Lake|スアンフーン湖 | 시내 한가운데 둘레 약 5km 호수 | Lake of about 5 km around in the city center
P dl_nightmarket food 11.9428 108.437 1.5 night dinner o=N | 달랏 야시장|大叻夜市|Da Lat Night Market|ダラット夜市 | 달랏 시장 앞 계단 아래 저녁 먹거리 시장 | Evening street-food market below Da Lat Market
P dl_cathedral palace 11.9367 108.4381 0.5 o=D | 달랏 대성당 (닭 성당)|大叻主教座堂 (鸡教堂)|Da Lat Cathedral (Chicken Church)|ダラット大聖堂 (鶏の教会) | 첨탑 위 닭 조형이 있는 1942년 완공 성당 | Cathedral finished in 1942 with a rooster on its spire
P dl_crazyhouse fun 11.9352 108.4307 1 am o=D | 크레이지 하우스 (항응아 빌라)|疯狂屋 (姮娥别墅)|Crazy House (Hang Nga Villa)|クレイジーハウス (ハンガー・ヴィラ) | 나무·동굴 모양의 기묘한 건축 숙소 | Surreal tree-and-cave shaped guesthouse
Z dl_z2 | 남쪽 (뚜옌럼 호수 쪽) | South (Tuyen Lam Lake)
P dl_datanla nature 11.9014 108.4491 2 o=D | 다딴라 폭포|达坦拉瀑布|Datanla Waterfall|ダタンラの滝 | 알파인 코스터로 내려가는 시내 근처 폭포 | Waterfall near town reached by alpine coaster
P dl_truclam palace 11.9277 108.4316 3 am o=D | 죽림선원·로빈힐 케이블카|竹林禅院·罗宾山缆车|Truc Lam Monastery & Robin Hill Cable Car|竹林禅院・ロビンヒル・ケーブルカー | 케이블카로 건너가는 호숫가 언덕의 선원 | Zen monastery on a lakeside hill reached by cable car
P dl_tuyenlam nature 11.8936 108.4256 2 o=A | 뚜옌럼 호수|宣林湖|Tuyen Lam Lake|トゥエンラム湖 | 소나무 숲에 둘러싸인 남쪽 큰 호수 | Large pine-ringed lake south of town
Z dl_z3 | 북쪽 (랑비앙) | North (Lang Biang)
P dl_langbiang nature 12.027 108.4396 4 am o=D | 랑비앙 산|朗边山|Lang Biang Mountain|ランビアン山 | 해발 2,167m, 지프나 걸어서 오르는 산 | 2,167 m peak climbed on foot or by jeep"""

ARTICLES = []
COORDS = {}

PLACES = {
 "dl_xuanhuong": dict(ko=("쑤언흐엉 호수", "시내 한가운데 둘레 약 5km 호수"), en=("Xuan Huong Lake", "Lake of about 5 km around in the city center"), zh=("春香湖", "市中心周长约5公里的湖"), ja=("スアンフーン湖", "街の真ん中にある周囲約5kmの湖"),
   lat=11.9420, lng=108.4450, o=[0, 24], cost=0, closed=[], best="eve", meal=None, h=1.5, cat="nature", st="Xuan Huong Lake, Da Lat, Lam Dong (럼비엔 광장 옆)"),
 "dl_nightmarket": dict(ko=("달랏 야시장", "달랏 시장 앞 계단 아래 저녁 먹거리 시장"), en=("Da Lat Night Market", "Evening street-food market below Da Lat Market"), zh=("大叻夜市", "大叻市场前台阶下的夜间小吃市场"), ja=("ダラット夜市", "ダラット市場前の階段下に立つ夜の屋台街"),
   lat=11.9428, lng=108.4370, o=[17, 23], cost=0, closed=[], best="night", meal="any", h=1.5, cat="night", st="Nguyen Thi Minh Khai, Da Lat, Lam Dong (달랏 시장·호아빈 광장 아래)"),
 "dl_cathedral": dict(ko=("달랏 대성당 (닭 성당)", "첨탑 위 닭 조형이 있는 1942년 완공 성당"), en=("Da Lat Cathedral (Chicken Church)", "Cathedral finished in 1942 with a rooster on its spire"), zh=("大叻主教座堂 (鸡教堂)", "尖塔上有公鸡雕像，1942年建成"), ja=("ダラット大聖堂 (鶏の教会)", "尖塔に鶏が立つ1942年完成の大聖堂"),
   lat=11.9367, lng=108.4381, o=[8, 17], cost=0, closed=[], best="day", meal=None, h=0.5, cat="palace", st="Tran Phu, Da Lat, Lam Dong"),
 "dl_crazyhouse": dict(ko=("크레이지 하우스 (항응아 빌라)", "나무·동굴 모양의 기묘한 건축 숙소"), en=("Crazy House (Hang Nga Villa)", "Surreal tree-and-cave shaped guesthouse"), zh=("疯狂屋 (姮娥别墅)", "树木和洞穴造型的奇特建筑旅馆"), ja=("クレイジーハウス (ハンガー・ヴィラ)", "木や洞窟の形をした奇抜な建築の宿"),
   lat=11.9352, lng=108.4307, o=[8.5, 19], cost=0, closed=[], best="am", meal=None, h=1, cat="fun", st="3 Huynh Thuc Khang, Da Lat, Lam Dong"),
 "dl_datanla": dict(ko=("다딴라 폭포", "알파인 코스터로 내려가는 시내 근처 폭포"), en=("Datanla Waterfall", "Waterfall near town reached by alpine coaster"), zh=("达坦拉瀑布", "坐高山滑车下行的近郊瀑布"), ja=("ダタンラの滝", "アルパインコースターで下る街近くの滝"),
   lat=11.9014, lng=108.4491, o=[8, 17], cost=0, closed=[], best="am", meal=None, h=2, cat="nature", st="Datanla Waterfall, Da Lat, Lam Dong (시내 남쪽 약 5km)"),
 "dl_truclam": dict(ko=("죽림선원·로빈힐 케이블카", "케이블카로 건너가는 호숫가 언덕의 선원"), en=("Truc Lam Monastery & Robin Hill Cable Car", "Zen monastery on a lakeside hill reached by cable car"), zh=("竹林禅院·罗宾山缆车", "坐缆车到湖边山丘上的禅院"), ja=("竹林禅院・ロビンヒル・ケーブルカー", "ケーブルカーで渡る湖畔の丘の禅寺"),
   lat=11.9277, lng=108.4316, o=[7, 17], cost=0, closed=[], best="am", meal=None, h=3, cat="palace", st="1 Dong Da, Da Lat, Lam Dong (로빈힐 케이블카 역)"),
 "dl_tuyenlam": dict(ko=("뚜옌럼 호수", "소나무 숲에 둘러싸인 남쪽 큰 호수"), en=("Tuyen Lam Lake", "Large pine-ringed lake south of town"), zh=("宣林湖", "被松林环绕的南郊大湖"), ja=("トゥエンラム湖", "松林に囲まれた南郊の大きな湖"),
   lat=11.8936, lng=108.4256, o=[0, 24], cost=0, closed=[], best="day", meal=None, h=2, cat="nature", st="Tuyen Lam Lake, Da Lat, Lam Dong"),
 "dl_langbiang": dict(ko=("랑비앙 산", "해발 2,167m, 지프나 걸어서 오르는 산"), en=("Lang Biang Mountain", "2,167 m peak climbed on foot or by jeep"), zh=("朗边山", "海拔2167米，可徒步或坐吉普车上山"), ja=("ランビアン山", "標高2,167m、徒歩かジープで登る山"),
   lat=12.0270, lng=108.4396, o=[7, 17], cost=0, closed=[], best="am", meal=None, h=4, cat="nature", st="Lac Duong, Lam Dong (달랏 시내 북쪽 약 12km)"),
}

STAYS = [
 ("dl_stay_lake", 11.9400, 108.4430, ["쑤언흐엉 호수·시내 중심", "春香湖·市中心", "Xuan Huong Lake & Center", "スアンフーン湖・中心部"],
  ["호수 산책로와 광장이 가깝고 시내 대부분을 걸어서 다님", "靠近湖边步道和广场，市区景点大多可步行", "Lakeside walks and the square nearby, most sights walkable", "湖畔の散歩道と広場に近く、中心部はほぼ徒歩圏"]),
 ("dl_stay_market", 11.9435, 108.4365, ["달랏 야시장 주변", "大叻夜市周边", "Da Lat Night Market area", "ダラット夜市周辺"],
  ["야시장·달랏 시장 바로 옆, 저녁 먹거리와 택시 잡기 쉬움", "紧邻夜市和大叻市场，晚餐和打车方便", "Next to the night market and Da Lat Market, easy food and taxis", "夜市とダラット市場のすぐそば、夕食やタクシーに便利"]),
]

_VT_LAKE = ("Vietnam Tourism — 럼비엔 광장과 쑤언흐엉 호수 안내 (2026.11.11 갱신)", "https://www.vietnamtourism.com/vi/quang-truong-lam-vien-va-ho-xuan-huong-o-a-lat-huong-dan-ay")
_VT_THINGS = ("Vietnam Tourism — Da Lat things to do: waterfalls, farms and the Crazy House (2026.10.1 갱신)", "https://www.vietnamtourism.com/en/da-lat-things-to-do-waterfalls-farms-and-the-crazy-house")
_VT_GUIDE = ("Vietnam Tourism — Da Lat Honest 2026 Guide (2026.10.20 갱신)", "https://www.vietnamtourism.com/en/da-lat-vietnam-s-cool-weather-highland-escape-honest-2026-guide")
_VT_TRUC = ("Vietnam Tourism — Truc Lam Zen Monastery in Da Lat (2026.10.24 갱신)", "https://www.vietnamtourism.com/en/truc-lam-zen-monastery-in-da-lat-history-what-to-see-and-how")
_VT_FALLS = ("Vietnam Tourism — Vietnam's best waterfalls (2026.10.7 갱신)", "https://www.vietnamtourism.com/en/vietnam-s-best-waterfalls-a-complete-guide")
_VT_LANG = ("Vietnam Tourism — 랑비앙 산: 걸어서 또는 지프로 (2026.11.7 갱신)", "https://www.vietnamtourism.com/vi/nui-lang-biang-gan-da-lat-truyen-thuyet-di-bo-hay-di-jeep")
_VNAT = ("베트남 관광청 — Da Lat", "https://vietnam.travel/place-to-go/south-central-coast-central-highlands/dalat/")
_BLD = ("Bao Lam Dong (럼동성 공식 신문) — 닭 성당 두 곳", "https://baolamdong.vn/dulich/202002/hai-nha-tho-con-ga-xu-da-thanh-2987912/")

SPOTS = {
 "dl_xuanhuong": dict(
   one="달랏 시내 한가운데의 인공 호수로, 둘레가 약 5km예요. 호수 남쪽 럼비엔 광장과 함께 달랏 여행의 출발점이에요.",
   see=[("호숫가 산책로", "한 바퀴 걸어서 약 1시간 15분"), ("럼비엔 광장", "유리 돔 두 개가 있는 호수 남쪽 광장, 무료"), ("저녁 호수 풍경", "해 질 녘 호수 위로 지는 빛")],
   facts=dict(hours="상시", fee="무료 (자전거·2인 자전거 대여는 시간당 수만 동, 2026년 기준)", stay="약 1시간 30분", when="이른 아침 또는 해 질 녘, 12~3월 건기", access="시내 숙소에서 걸어서, 야시장과 걸어서 약 10분"),
   tips=["한 바퀴는 럼비엔 광장에서 시계 반대 방향으로 도는 것이 공식 안내 동선이고, 일부 구간은 오토바이와 길을 같이 써서 차도 쪽을 조심해요.",
         "오리배는 2024년 11월부터 새 운영자 허가를 기다리며 멈춘 상태라 선착장에서 운영하는지 먼저 물어봐요.",
         "호숫가 마차는 타기 전에 요금을 먼저 정하고, 말에게 먹이를 주거나 만지지 않아요."],
   src=[_VT_LAKE, _VNAT],
   checked="2026-11-26", photo=None),
 "dl_nightmarket": dict(
   one="달랏 시장 앞 호아빈 광장 계단 아래로 매일 저녁 펼쳐지는 먹거리 시장이에요. 꼬치구이·곶감·아티초크 차 같은 달랏 특산을 사 먹어요.",
   see=[("계단 아래 먹거리 노점", "꼬치구이와 따뜻한 두유"), ("달랏 특산 가게", "곶감·아티초크 차"), ("달랏 시장 건물", "낮에는 꽃·채소 시장")],
   facts=dict(hours="매일 약 17:00~18:00부터 밤늦게까지", fee="무료 (먹거리 비용 별도)", stay="약 1시간 30분", when="저녁", access="쑤언흐엉 호수에서 걸어서 약 10분, 달랏 시장 앞"),
   tips=["소매치기가 있다는 공식 안내가 있어 가방은 앞으로 메고 지퍼를 닫아요.",
         "고원이라 저녁 기온이 많이 내려가 12~3월에는 겉옷을 챙겨 가요.",
         "가격표 없는 노점은 주문 전에 값을 먼저 확인하고, 잔돈이 많은 현금을 준비해요."],
   src=[_VT_GUIDE, _VT_THINGS, _VT_LAKE],
   checked="2026-11-26", photo=None),
 "dl_cathedral": dict(
   one="쩐푸 거리에 있는 달랏 대성당으로, 1931년에 짓기 시작해 1942년에 완공했어요. 첨탑 십자가 위 닭 조형 때문에 '닭 성당'이라 불려요.",
   see=[("첨탑의 닭 조형", "땅에서 약 27m 높이, 바람 따라 돌아요"), ("높이 47m 종탑", "종탑 꼭대기까지 47m"), ("랑비앙 산을 향한 정문", "성당 앞에서 보는 시내 풍경")],
   facts=dict(hours="방문 전 확인 (미사 시간 외 관람)", fee="방문 전 확인", stay="약 30분", when="낮, 성탄절 무렵은 미사로 붐빔", access="쑤언흐엉 호수에서 걸어서 약 10분, 쩐푸 거리"),
   tips=["미사 중에는 안으로 들어가지 말고 밖에서 외관만 봐요.",
         "성당이라 어깨와 무릎을 가리는 옷으로 가요.",
         "성탄절 무렵은 미사와 관람객이 몰리니 낮 시간에 일찍 가요."],
   src=[_BLD],
   checked="2026-11-26", photo=None),
 "dl_crazyhouse": dict(
   one="나무·동굴 모양으로 지은 기묘한 건물로, 관람과 숙박을 함께 해요. 좁은 계단과 복도가 미로처럼 이어져요.",
   see=[("나무·동굴 모양 외관", "곡선으로 휜 벽과 창"), ("미로 같은 복도", "길을 잃기 쉬운 통로"), ("좁은 계단 위 전망", "높은 곳에서 보는 시내")],
   facts=dict(hours="매일 08:30~19:00 (2026년 기준)", fee="6만 동 (2026년 기준)", stay="약 1시간", when="문 여는 시간 바로", access="쑤언흐엉 호수에서 차로 약 5분, 후인툭캉 거리 3번지"),
   tips=["오전 10시쯤부터 단체 관광객이 몰려 문 여는 08:30에 맞춰 가요.",
         "계단과 통로가 좁고 높아 미끄럽지 않은 신발을 신고 어린이는 손을 잡아요."],
   src=[_VT_THINGS, _VT_GUIDE],
   checked="2026-11-26", photo=None),
 "dl_datanla": dict(
   one="시내에서 약 5km 떨어진 폭포로, 알파인 코스터를 타고 폭포 아래까지 내려가요. 가족 여행으로 가기 가장 쉬운 폭포예요.",
   see=[("알파인 코스터", "숲을 지나 폭포 앞까지 내려가는 썰매"), ("폭포 전망대", "만들어 둔 관람 데크"), ("캐니어닝", "폭포를 타고 내려가는 체험(별도 요금)")],
   facts=dict(hours="방문 전 확인", fee="입장 5만 동, 알파인 코스터 별도(방문 전 확인), 캐니어닝 150만~200만 동 (2026년 기준)", stay="약 2시간", when="오전, 평일", access="시내에서 남쪽으로 차 약 20분"),
   tips=["주말에는 코스터 줄이 45분까지 길어져 평일 오전에 가요.",
         "코스터는 편도·왕복 표가 따로 있어 매표소에서 돌아오는 방법까지 정하고 사요.",
         "죽림선원·로빈힐 케이블카와 같은 남쪽이라 같은 날 묶어서 돌아요."],
   src=[_VT_FALLS, _VT_GUIDE, _VT_THINGS],
   checked="2026-11-26", photo=None),
 "dl_truclam": dict(
   one="로빈힐에서 케이블카(약 2.3km, 약 12분)를 타고 뚜옌럼 호숫가 풍황 언덕의 죽림선원으로 건너가요. 선원은 무료로 들어가요.",
   see=[("로빈힐 케이블카", "소나무 숲 위로 가는 약 12분"), ("죽림선원 경내", "정원과 법당"), ("뚜옌럼 호수 선착장", "선원에서 걸어서 약 15~20분")],
   facts=dict(hours="선원 약 07:00~17:00, 케이블카는 점심(약 11:30~13:00/13:30)에 쉼 (2026년 기준)", fee="선원 무료, 케이블카 성인 편도 약 10만 동·왕복 약 12만 동 (2026년 기준)", stay="약 2시간 30분~3시간", when="오전", access="케이블카 로빈힐 역은 쑤언흐엉 호수에서 약 3km(동다 거리 1번지)"),
   tips=["케이블카가 점심시간에 멈춰 오전에 타고 건너가 선원을 본 뒤 11시 반 전에 돌아오거나 호수 쪽으로 내려가요.",
         "선원에서는 어깨와 무릎을 가리고, 반바지·민소매·비치는 옷은 피해요.",
         "편도로 건너가 뚜옌럼 호수 선착장까지 걸어 내려가면 다딴라 폭포와 묶기 좋아요."],
   src=[_VT_TRUC],
   checked="2026-11-26", photo=None),
 "dl_tuyenlam": dict(
   one="시내 남쪽 약 5km의 큰 호수로, 1980년대에 만든 저수지예요. 소나무 숲길과 보트, 죽림선원으로 가는 케이블카가 모여 있어요.",
   see=[("호숫가 소나무 숲길", "여러 갈래 산책로"), ("카약·보트", "호수 위에서 노 젓기"), ("죽림선원 쪽 선착장", "선원에서 걸어서 약 15~20분")],
   facts=dict(hours="상시 (보트 대여는 낮 시간, 방문 전 확인)", fee="무료, 카약 대여 시간당 약 15만 동 (2026년 기준)", stay="약 2시간", when="오전~오후, 12~3월 건기", access="시내에서 차로 남쪽 약 5km, 죽림선원에서 걸어서 내려가요"),
   tips=["반나절을 잡고 죽림선원·로빈힐 케이블카와 한 번에 묶어요.",
         "호수 주변은 대중교통이 드물어 돌아오는 택시·그랩을 미리 생각해 두거나 차를 대절해요."],
   src=[_VT_THINGS, _VT_TRUC, _VT_GUIDE],
   checked="2026-11-26", photo=None),
 "dl_langbiang": dict(
   one="달랏 시내 북쪽 약 12km의 산으로, 정상이 해발 2,167m예요. 지프를 타고 레이더 언덕 전망대까지 가거나 정상까지 걸어 올라요.",
   see=[("레이더 언덕 전망대", "지프로 오르는 전망 지점"), ("정상 등산로", "편도 약 2.5km 숲길"), ("고원 풍경", "달랏 분지와 마을이 내려다보여요")],
   facts=dict(hours="매일 약 07:00~17:00 (2026년 기준)", fee="입장 성인 약 5만 동·어린이 약 2만 5천 동, 지프 1인 약 12만 동 또는 6인 차 약 72만 동 (2026년 기준, 매표소 확인)", stay="지프 약 2시간, 걸어서 왕복 2~4시간", when="이른 아침, 12~3월 건기", access="달랏 시내에서 북쪽 락즈엉으로 차 약 30분"),
   tips=["오후에는 구름이 끼기 쉬워 아침 일찍 출발해요.",
         "지프는 혼자면 1인 표, 여럿이면 6인 한 대를 빌리는 쪽이 나아 인원을 맞춰 매표소에서 사요.",
         "정상까지 걸으면 체력이 필요하고 산 위가 쌀쌀해 물과 겉옷을 챙겨요."],
   src=[_VT_LANG, _VT_THINGS, _VNAT],
   checked="2026-11-26", photo=None),
}
