# -*- coding: utf-8 -*-
"""kanazawa — 2026-11-27 새 해외 지역 '가나자와'(일본, K링크 region id kanazawa, 장소 id 접두어 kz_) 데이터. 확인일 2026-11-27.
장소: travel-kanazawa.html 에 나오는 시내 7곳(겐로쿠엔·가나자와성 공원·히가시차야가이·오미초 시장·21세기 미술관·나가마치 무사 저택 거리·
  가나자와역 쓰즈미몬). 나가마치·가나자와역은 글 본문에는 없고 지시에 따라 넣었어요. 글의 시라카와고는 가나자와 시 밖(기후현)이라 넣지 않았어요.
못 쓴 것: GUIDE·ARTICLES 없음(지시대로).
메모(출처): 겐로쿠엔·가나자와성은 이시카와현 공식(shiro-niwa.pref.ishikawa.lg.jp), 나머지는 가나자와시 관광 공식(visitkanazawa.jp)·
  21세기 미술관 공식(kanazawa21.jp)·JNTO(japan.travel)·이시카와현 관광(ishikawatravel.jp)으로 확인했어요.
메모(확인 못 한·애매한 숫자):
  - 21세기 미술관 전시 요금은 전시마다 달라 '방문 전 확인'. 공식 시간표 페이지는 2024~2025 전시 기준이라 시간만 썼어요.
    〈수영장〉(레안드로 에를리치) 관람 방식·예약 여부는 공식 확인 못 해 '공식 사이트 확인' 문구로만 씀.
  - 오미초 시장 시간: visitkanazawa 9:00~16:00(가게마다 다름), JNTO 9:00~약 17:00 -> '약'·'가게마다 다름'. 수·일요일 쉬는 가게가 많다는 건 JNTO.
  - 시내 버스 요금은 JNTO에 200엔으로 나오지만 오래된 값일 수 있어 쓰지 않았어요.
  - 노무라가 무사 저택 요금 550엔은 2027.4.1부터 750엔으로 오른다고 공식 공지(visitkanazawa).
  - 쓰즈미몬 완공 연도는 공식 출처에서 못 찾음(역 대개장 2005년만 확인) -> 쓰지 않음. 높이 13.7m는 visitkanazawa.
  - 가나자와성 건물(히시야구라 등) 연도, 교쿠센인마루 정원 야간 조명은 공식 페이지에 없어 쓰지 않음.
  - 좌표는 시설 대표 지점의 대략값(소수 4자리).
메모(도시 줄): 고마쓰공항(KMQ) 서울 노선은 이시카와현 관광 공식에 '연중 운항'으로만 나오고 항공사·횟수는 없어, fly 값은 travel-kanazawa.html
  기준(대한항공 매일, 약 1시간 45분) 105분. 공항→가나자와 버스 약 40분(이시카와현 관광 공식), 국내선 도착 10~15분 뒤 출발(고마쓰공항 FAQ).
  sub=1(가나자와역 동쪽 출구에서 루프 버스·노선버스가 촘촘). 도시 중심 좌표는 고린보 교차로 부근 36.5613 136.6562.
"""

CITY_LINES = """C kanazawa jp 36.5613 136.6562 1 105 | 가나자와|金泽|Kanazawa|金沢 | 겐로쿠엔과 찻집 거리, 오미초 시장의 '작은 교토' | Castle-town of a great garden, teahouse streets and a seafood market
A KMQ 36.3946 136.4069 40 | 고마쓰공항|小松机场|Komatsu (KMQ)|小松空港
S kz_stay_station 36.5780 136.6485 | 가나자와역 주변|金泽站周边|Around Kanazawa Stn|金沢駅周辺 | 공항버스·신칸센이 서는 역 앞, 오미초 시장까지 걸어서 약 15분 | Airport buses and Shinkansen at the door, Omicho about 15 min on foot
S kz_stay_korinbo 36.5600 136.6545 | 고린보·가타마치|香林坊·片町|Korinbo & Katamachi|香林坊・片町 | 겐로쿠엔·21세기 미술관·나가마치가 걸어서 닿는 번화가 | Downtown within walking distance of Kenrokuen, the museum and Nagamachi
Z kz_z1 | 가나자와역·오미초 | Kanazawa Stn & Omicho
P kz_station palace 36.5781 136.6480 0.5 eve o=A | 가나자와역 쓰즈미몬|金泽站鼓门|Kanazawa Stn Tsuzumi-mon Gate|金沢駅鼓門 | 북 모양 나무 문과 유리 돔이 있는 역 동쪽 출구 | Drum-shaped wooden gate and glass dome at the east exit
P kz_omicho food 36.5714 136.6563 1 lunch o=M | 가나자와 오미초 시장|金泽近江町市场|Omicho Market|近江町市場 | 170곳 넘는 가게가 모인 300년 해산물 시장 | 300-year-old market of 170+ shops and seafood
Z kz_z2 | 겐로쿠엔·고린보 | Kenrokuen & Korinbo
P kz_kenrokuen nature 36.5621 136.6627 1.5 am o=D | 겐로쿠엔|兼六园|Kenrokuen Garden|兼六園 | 일본 3대 정원, 고토지 석등과 겨울 유키즈리 | One of Japan's three great gardens, with snow-rope pines
P kz_castle palace 36.5650 136.6597 1 am o=D | 가나자와성 공원|金泽城公园|Kanazawa Castle Park|金沢城公園 | 겐로쿠엔과 다리로 이어진 무료 성터 공원 | Free castle park linked to Kenrokuen by a bridge
P kz_21museum fun 36.5609 136.6582 1.5 o=D x=1 | 가나자와 21세기 미술관|金泽21世纪美术馆|21st Century Museum of Contemporary Art|金沢21世紀美術館 | 둥근 유리 건물의 현대 미술관, 무료 구역 있음 | Round glass contemporary art museum with a free zone
P kz_nagamachi palace 36.5626 136.6489 1 am o=D | 나가마치 무사 저택 거리|长町武家宅邸遗迹|Nagamachi Samurai District|長町武家屋敷跡 | 흙담과 수로가 남은 옛 무사 마을 | Old samurai quarter of earthen walls and canals
Z kz_z3 | 히가시차야 | Higashi Chaya
P kz_higashichaya shop 36.5724 136.6667 1 o=A | 히가시차야가이|东茶屋街|Higashi Chaya District|ひがし茶屋街 | 1820년 생긴 찻집 거리, 금박 공예 가게 | Teahouse street from 1820 with gold-leaf craft shops"""

ARTICLES = []
COORDS = {}

PLACES = {
 "kz_station": dict(ko=("가나자와역 쓰즈미몬", "북 모양 나무 문과 유리 돔이 있는 역 동쪽 출구"), en=("Kanazawa Stn Tsuzumi-mon Gate", "Drum-shaped wooden gate and glass dome at the east exit"), zh=("金泽站鼓门", "车站东口的鼓形木门和玻璃穹顶"), ja=("金沢駅鼓門", "駅東口の鼓形の木の門とガラスのドーム"),
   lat=36.5781, lng=136.6480, o=[0, 24], cost=0, closed=[], best="eve", meal=None, h=0.5, cat="palace", st="1-1 Kinoshinbomachi, Kanazawa, Ishikawa (가나자와역 동쪽 출구)"),
 "kz_omicho": dict(ko=("가나자와 오미초 시장", "170곳 넘는 가게가 모인 300년 해산물 시장"), en=("Omicho Market", "300-year-old market of 170+ shops and seafood"), zh=("金泽近江町市场", "170多家店铺的300年海鲜市场"), ja=("近江町市場", "170以上の店が集まる300年の市場"),
   lat=36.5714, lng=136.6563, o=[9, 17], cost=0, closed=[], best="am", meal="any", h=1, cat="food", st="50-1 Kamiomicho, Kanazawa, Ishikawa"),
 "kz_kenrokuen": dict(ko=("겐로쿠엔", "일본 3대 정원, 고토지 석등과 겨울 유키즈리"), en=("Kenrokuen Garden", "One of Japan's three great gardens, with snow-rope pines"), zh=("兼六园", "日本三大名园之一，徽轸灯笼与冬季雪吊"), ja=("兼六園", "日本三名園のひとつ、徽軫灯籠と冬の雪吊り"),
   lat=36.5621, lng=136.6627, o=[8, 17], cost=0, closed=[], best="am", meal=None, h=1.5, cat="nature", st="Kenrokumachi, Kanazawa, Ishikawa"),
 "kz_castle": dict(ko=("가나자와성 공원", "겐로쿠엔과 다리로 이어진 무료 성터 공원"), en=("Kanazawa Castle Park", "Free castle park linked to Kenrokuen by a bridge"), zh=("金泽城公园", "与兼六园以桥相连的免费城址公园"), ja=("金沢城公園", "兼六園と橋でつながる無料の城跡公園"),
   lat=36.5650, lng=136.6597, o=[8, 17], cost=0, closed=[], best="am", meal=None, h=1, cat="palace", st="Marunouchi, Kanazawa, Ishikawa"),
 "kz_21museum": dict(ko=("가나자와 21세기 미술관", "둥근 유리 건물의 현대 미술관, 무료 구역 있음"), en=("21st Century Museum of Contemporary Art", "Round glass contemporary art museum with a free zone"), zh=("金泽21世纪美术馆", "圆形玻璃建筑的现代美术馆，设免费区"), ja=("金沢21世紀美術館", "円形ガラス建築の現代美術館、無料ゾーンあり"),
   lat=36.5609, lng=136.6582, o=[10, 18], cost=0, closed=[1], best="day", meal=None, h=1.5, cat="fun", st="1-2-1 Hirosaka, Kanazawa, Ishikawa"),
 "kz_nagamachi": dict(ko=("나가마치 무사 저택 거리", "흙담과 수로가 남은 옛 무사 마을"), en=("Nagamachi Samurai District", "Old samurai quarter of earthen walls and canals"), zh=("长町武家宅邸遗迹", "保留土墙和水渠的旧武士町"), ja=("長町武家屋敷跡", "土塀と用水が残る武家町"),
   lat=36.5626, lng=136.6489, o=[8.5, 16.5], cost=0, closed=[], best="am", meal=None, h=1, cat="palace", st="Nagamachi, Kanazawa, Ishikawa (노무라가 무사 저택 부근)"),
 "kz_higashichaya": dict(ko=("히가시차야가이", "1820년 생긴 찻집 거리, 금박 공예 가게"), en=("Higashi Chaya District", "Teahouse street from 1820 with gold-leaf craft shops"), zh=("东茶屋街", "1820年形成的茶屋街，金箔工艺店"), ja=("ひがし茶屋街", "1820年にできた茶屋街、金箔の店"),
   lat=36.5724, lng=136.6667, o=[0, 24], cost=0, closed=[], best="am", meal=None, h=1, cat="shop", st="Higashiyama 1-chome, Kanazawa, Ishikawa"),
}

STAYS = [
 ("kz_stay_station", 36.5780, 136.6485, ["가나자와역 주변", "金泽站周边", "Around Kanazawa Stn", "金沢駅周辺"],
  ["공항버스·신칸센이 서는 역 앞, 오미초 시장까지 걸어서 약 15분", "机场巴士和新干线就在站前，步行约15分钟到近江町市场", "Airport buses and Shinkansen at the door, Omicho about 15 min on foot", "空港バスと新幹線の駅前、近江町市場まで徒歩約15分"]),
 ("kz_stay_korinbo", 36.5600, 136.6545, ["고린보·가타마치", "香林坊·片町", "Korinbo & Katamachi", "香林坊・片町"],
  ["겐로쿠엔·21세기 미술관·나가마치가 걸어서 닿는 번화가", "步行可到兼六园、21世纪美术馆和长町的繁华区", "Downtown within walking distance of Kenrokuen, the museum and Nagamachi", "兼六園・21世紀美術館・長町へ歩ける繁華街"]),
]

_PREF_KEN = ("이시카와현 — 겐로쿠엔 이용 안내 (Kenrokuen Garden Info)", "https://shiro-niwa.pref.ishikawa.lg.jp/kenrokuen-garden/e/info.html")
_PREF_CASTLE = ("이시카와현 — 가나자와성 공원 이용 안내 (Kanazawa Castle Info)", "https://shiro-niwa.pref.ishikawa.lg.jp/english/info.html")
_JNTO_KEN = ("JNTO — Kenrokuen Garden", "https://www.japan.travel/en/spot/1399/")
_VK_OMI = ("가나자와시 관광 공식 — Omicho Market", "https://visitkanazawa.jp/en/attractions/detail_10030.html")
_JNTO_OMI = ("JNTO — Omicho Market", "https://www.japan.travel/en/spot/1398/")
_VK_HIGA = ("가나자와시 관광 공식 — Higashi Chaya District", "https://visitkanazawa.jp/en/attractions/detail_10212.html")
_VK_SHIMA = ("가나자와시 관광 공식 — 오차야 시마 (Ochaya SHIMA)", "https://visitkanazawa.jp/en/attractions/detail_10094.html")
_K21 = ("가나자와 21세기 미술관 공식 — Museum Hours", "https://kanazawa21.jp/data_list.php?d=5&g=7")
_VK_21 = ("가나자와시 관광 공식 — 21st Century Museum of Contemporary Art", "https://visitkanazawa.jp/en/attractions/detail_10066.html")
_JNTO_21 = ("JNTO — 21st Century Museum of Contemporary Art, Kanazawa", "https://www.japan.travel/en/spot/1407")
_VK_NOMURA = ("가나자와시 관광 공식 — 노무라가 무사 저택 (Nomura Samurai Residence)", "https://visitkanazawa.jp/en/attractions/detail_50073.html")
_JNTO_NAGA = ("JNTO — Nagamachi Samurai District", "https://www.japan.travel/en/spot/668/")
_VK_STN = ("가나자와시 관광 공식 — Kanazawa Station (Tsuzumi-mon Gate)", "https://visitkanazawa.jp/en/attractions/detail_10050.html")
_JNTO_STN = ("JNTO — Kanazawa Station", "https://www.japan.travel/en/spot/1401/")
_IT_STN = ("이시카와현 관광 — Kanazawa Station (Tsuzumimon Gate)", "https://www.ishikawatravel.jp/spots/kanazawa-station-tsuzumimon-gate/")

SPOTS = {
 "kz_kenrokuen": dict(
   one="가가번 마에다 가문이 1676년부터 가꾼 정원으로, 일본 3대 정원 가운데 하나예요. 1874년에 일반에 열렸고 가나자와성 공원과 바로 이어져요.",
   see=[("고토지 석등", "다리 두 개로 선 겐로쿠엔의 상징 석등"), ("가스미가이케 연못", "물 높이 차로 약 3.5m 솟는 분수"), ("유키즈리", "11월 1일부터 약 3월 15일까지 소나무를 받치는 눈 밧줄")],
   facts=dict(hours="3월 1일~10월 15일 07:00~18:00, 10월 16일~2월 말 08:00~17:00 (2026년 기준)", fee="성인 320엔·6~17세 100엔, 현금만 (2026년 기준)", stay="약 1시간 30분~2시간", when="이른 아침, 단풍철(가을)·유키즈리가 걸린 겨울", access="가나자와역 동쪽 출구에서 버스 약 15~20분, 가나자와성 공원 이시카와몬에서 다리 건너 바로"),
   tips=["11월~2월에는 06:00부터 렌치몬·즈이신자카 입구로 무료로 들어갈 수 있고, 정규 개원 15분 전까지 나와야 해요.",
         "입장료는 현금만 받아 동전과 천 엔짜리를 챙기고, 65세 이상 외국인은 여권을 보여 주면 무료예요.",
         "21세기 미술관 등 시 문화시설 한 곳을 더 묶은 '겐로쿠엔+1' 표(500엔)도 있어 동선에 맞춰 골라요."],
   src=[_PREF_KEN, _JNTO_KEN],
   checked="2026-11-27", photo=None),
 "kz_castle": dict(
   one="가가번 마에다 가문의 성이 있던 자리를 공원으로 꾸민 곳으로, 공원 입장은 무료예요. 이시카와몬 앞 다리를 건너면 겐로쿠엔이에요.",
   see=[("이시카와몬", "겐로쿠엔 쪽으로 난 성문"), ("히시야구라·고짓켄나가야", "안에 들어가 보는 복원 망루와 긴 창고"), ("하시즈메몬", "성 안쪽으로 이어지는 문")],
   facts=dict(hours="공원 3월 1일~10월 15일 07:00~18:00, 10월 16일~2월 말 08:00~17:00 / 건물 09:00~16:30(입장 16:00까지) (2026년 기준)", fee="공원 무료, 히시야구라·고짓켄나가야·하시즈메몬 성인 320엔·6~17세 100엔, 현금만 (2026년 기준)", stay="약 1시간", when="오전, 겐로쿠엔과 같은 날", access="겐로쿠엔에서 이시카와몬 다리 건너 바로, 나가마치까지 걸어서 약 10분"),
   tips=["공원은 무료지만 건물 안은 09:00~16:00 입장이라 건물까지 보려면 오후 4시 전에 들어가요.",
         "건물 입장료도 현금만 받아 겐로쿠엔 표와 함께 현금을 넉넉히 준비해요.",
         "겐로쿠엔을 본 뒤 이시카와몬으로 넘어와 성 공원을 지나 나가마치 무사 저택 거리까지 걸으면 되돌아가지 않는 동선이 돼요."],
   src=[_PREF_CASTLE, _JNTO_KEN, _JNTO_NAGA],
   checked="2026-11-27", photo=None),
 "kz_higashichaya": dict(
   one="1820년 가나자와의 찻집들을 모아 만든 세 찻집 거리 가운데 가장 큰 곳이에요. 옛 찻집 건물이 국가 문화재로 지정돼 있고, 지금은 카페·식당·금박 공예 가게가 많아요.",
   see=[("오차야 시마", "1820년 지은 찻집 건물을 그대로 공개하는 국가 중요문화재"), ("격자창 찻집 거리", "나무 격자가 이어지는 돌길"), ("아사노강", "거리에서 걸어서 약 3분인 강변")],
   facts=dict(hours="거리는 상시, 오차야 시마 09:30~17:30(12~2월 17:00까지) 연중무휴 (2026년 기준)", fee="거리 무료, 오차야 시마 성인 500엔·16세 이하 300엔(말차·과자 별도) (2026년 기준)", stay="약 1시간", when="오전, 가게가 여는 낮", access="루프 버스 하시바초 정류장에서 걸어서 약 5분, 가나자와역에서 차로 약 10분"),
   tips=["가나자와시 관광협회가 정해진 토요일에 게이샤 공연을 여니 일정이 맞으면 미리 확인해요.",
         "오차야 시마는 연중무휴지만 겨울(12~2월)에는 17:00에 닫아 늦은 오후에는 시마부터 들어가요.",
         "거리 사진은 가게가 문을 열기 전 이른 아침이 사람이 적어요."],
   src=[_VK_HIGA, _VK_SHIMA],
   checked="2026-11-27", photo=None),
 "kz_omicho": dict(
   one="에도 시대부터 300년 넘게 가나자와의 부엌 역할을 한 시장으로, 가게가 170곳 넘어요. 해산물 덮밥(가이센동)과 겨울 게를 먹으러 많이 가요.",
   see=[("해산물 덮밥 가게", "회를 올린 가이센동"), ("생선·건어물 가게", "노도구로·겨울 게·방어"), ("오미초 이치바칸", "인기 식당과 가게가 모인 새 건물")],
   facts=dict(hours="약 09:00~16:00·17:00 (가게마다 다름, 2026년 기준)", fee="무료 (먹거리 비용 별도)", stay="약 1시간", when="오전, 11월부터 겨울 게철(가장 붐빔)", access="가나자와역에서 걸어서 15~20분, 버스 무사시가쓰지·오미초 시장 정류장에서 걸어서 1분"),
   tips=["수요일·일요일에 쉬는 가게가 많아 그날 가려면 가고 싶은 가게 휴무를 먼저 확인해요.",
         "11월 게철에는 가장 붐비니 점심 줄을 피해 문 여는 오전 9시 무렵에 가요.",
         "새해 연휴에는 시장 전체가 쉬어요."],
   src=[_VK_OMI, _JNTO_OMI],
   checked="2026-11-27", photo=None),
 "kz_21museum": dict(
   one="2004년 문을 연 둥근 유리 건물의 현대 미술관으로, 세지마 가즈요·니시자와 류에(SANAA)가 설계했어요. 전시는 유료지만 건물 안 무료 구역과 일부 작품은 그냥 들어가 봐요.",
   see=[("〈수영장〉", "레안드로 에를리치, 물 아래에 선 듯 보이는 작품"), ("〈블루 플래닛 스카이〉", "제임스 터렐의 하늘을 보는 방"), ("둥근 유리 건물", "앞뒤 구분 없이 사방으로 드나드는 건물")],
   facts=dict(hours="전시 구역 10:00~18:00(금·토 20:00까지), 무료 구역 09:00~22:00 (2026년 기준)", fee="건물·무료 구역 무료, 전시 요금은 전시마다 다름(방문 전 확인)", stay="약 1~2시간", when="평일, 월요일 피하기", access="가나자와역 동쪽 출구 버스 약 10~20분, 히로사카·21세기 미술관 정류장에서 걸어서 1분, 겐로쿠엔과 걸어서 가까움"),
   tips=["전시 구역은 월요일(공휴일이면 다음 평일)에 쉬지만 무료 구역은 월요일에도 열어요.",
         "전시 표 판매는 닫기 30분 전에 끝나니 금·토 저녁 연장일이 아니면 17:30 전에 표를 사요.",
         "〈수영장〉 관람 방식은 시기에 따라 달라 공식 사이트(kanazawa21.jp)에서 먼저 확인해요."],
   src=[_K21, _VK_21, _JNTO_21],
   checked="2026-11-27", photo=None),
 "kz_nagamachi": dict(
   one="가나자와성 남서쪽, 흙담과 좁은 골목·수로가 남은 옛 무사 마을이에요. 노무라가 무사 저택에 들어가 방에서 정원을 볼 수 있어요.",
   see=[("노무라가 무사 저택", "400년 넘은 소귀나무와 물길이 있는 안뜰 정원"), ("흙담 골목", "겨울에는 담을 짚으로 덮는 풍경"), ("좁은 골목과 수로", "마을 사이로 흐르는 작은 물길")],
   facts=dict(hours="거리는 상시, 노무라가 08:30~17:30(10~3월 16:30까지) (2026년 기준)", fee="거리 무료, 노무라가 성인 550엔·고교생 400엔·초중생 250엔 (2027년 4월부터 성인 750엔 예정)", stay="약 1시간", when="오전, 짚 덮개가 걸리는 겨울", access="버스 고린보 정류장에서 걸어서 약 5분, 가나자와성 이시카와몬에서 걸어서 약 10분"),
   tips=["노무라가 무사 저택은 12월 26~27일과 1월 1~2일에 쉬어요.",
         "10~3월에는 노무라가가 16:30에 닫아 겨울에는 오후 3시 반 전에 들어가요.",
         "골목이 좁고 주민이 사는 곳이라 길 가운데에 서서 사진을 찍지 말고 한쪽으로 비켜요."],
   src=[_VK_NOMURA, _JNTO_NAGA],
   checked="2026-11-27", photo=None),
 "kz_station": dict(
   one="가나자와역 동쪽 출구의 북 모양 나무 문 쓰즈미몬(높이 13.7m)과 유리 돔 모테나시 돔이에요. 비와 눈이 많은 고장에서 우산을 건네는 마음을 담았다고 해요.",
   see=[("쓰즈미몬", "노가쿠의 북 '쓰즈미'를 본뜬 높이 13.7m 나무 문"), ("모테나시 돔", "동쪽 출구 광장을 덮은 유리 지붕"), ("저녁 조명", "해 진 뒤 매시 정각 2분 동안 가가 오채색 조명")],
   facts=dict(hours="상시, 조명은 해 질 녘~자정 매시 정각 약 2분 (2026년 기준)", fee="무료", stay="약 30분", when="저녁(조명), 도착·출발하는 날", access="가나자와역 동쪽 출구 바로 앞, 고마쓰공항 버스 약 40분"),
   tips=["평일은 요일마다 한 가지 색, 주말·공휴일은 다섯 색을 2분씩 비추니 조명을 보려면 주말 저녁 정각에 맞춰 가요.",
         "신칸센 개찰구 맞은편 관광 안내소에서 지도·버스 시간표를 받고, 자원봉사 가이드는 2주 전까지 신청해요.",
         "고마쓰공항에서 오는 버스는 국내선 도착 10~15분 뒤 1·2번 정류장에서 떠나고, 역에서 공항으로 갈 때는 비행기 시각에 맞춰 버스 시간표를 미리 확인해요."],
   src=[_VK_STN, _JNTO_STN, _IT_STN],
   checked="2026-11-27", photo=None),
}
