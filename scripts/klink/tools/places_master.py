# Real coordinates and visiting rules for every place.
# id: lat lng open close best meal duration_h
# open/close in 24h decimal hours (close > 24 means after midnight). best: am/day/eve/night/any. meal: -, any, lunch, dinner
TABLE = """
gbg 37.5796 126.9770 9 18 am - 2
bukchon 37.5826 126.9837 10 17 am - 1.5
cdg 37.5794 126.9910 9 18 am - 2
insa 37.5743 126.9853 10.5 20.5 day - 1.5
museum 37.5239 126.9804 10 18 day - 2
gwangjang 37.5701 126.9996 9 23 any any 1.5
samgyup 37.5663 126.9918 16 23 eve dinner 1.5
gejang 37.5196 127.0205 11 21 any any 1.5
mdfood 37.5638 126.9853 17 22.5 eve dinner 1
samgye 37.5779 126.9714 10 22 any any 1
kalguksu 37.5625 126.9857 10.5 21 any any 1
dakgalbi 37.5560 126.9235 11 23 any any 1
sbrunch 37.5443 127.0540 10 16 day lunch 1
hanwoo 37.5245 127.0410 18 22.5 eve dinner 2
skin1 37.5047 127.0250 10 19 day - 2
skin2 37.5610 126.9840 10 20 day - 1.5
spa 37.5570 126.9245 11 21 day - 1.5
oliveyoung 37.5640 126.9839 10 22.5 any - 1
garosu 37.5210 127.0230 11 21 day - 2
seongsu 37.5447 127.0560 11 21 day - 2
ddp 37.5665 127.0092 10 22 any - 2
hongdae 37.5563 126.9236 12 23 eve - 2
thehyundai 37.5259 126.9284 10.5 20 day - 2
scafe 37.5418 127.0565 10 22 day - 1.5
ikcafe 37.5743 126.9896 11 22 day - 1
ycafe 37.5626 126.9255 11 22 day - 1.5
hybe 37.5290 126.9640 9 20 day - 1
coex 37.5115 127.0595 10.5 22 any - 1.5
kstar 37.5265 127.0405 0 24 any - 0.5
namsan 37.5512 126.9882 10 23 night - 1.5
hangang 37.5284 126.9326 0 24 eve - 1.5
lotte 37.5125 127.1025 10.5 22 night - 1.5
cheong 37.5692 126.9779 0 24 night - 1
banpo 37.5103 126.9958 19.5 21 night - 1
seoulforest 37.5444 127.0374 0 24 day - 1.5
deoksugung 37.5658 126.9751 9 21 any - 1.5
namdaemun 37.5592 126.9775 9 18 day - 1.5
lotteworld 37.5111 127.0980 10 21 day - 4
naksan 37.5806 127.0074 0 24 night - 1
mangwon 37.5560 126.9056 10 21 any any 1
noryangjin 37.5133 126.9405 0 22 any any 1.5
bs_haeundae 35.1587 129.1604 0 24 any - 1.5
bs_gamcheon 35.0975 129.0106 9 18 day - 2
bs_jagalchi 35.0966 129.0306 8 22 any any 1.5
bs_gwangan 35.1532 129.1186 0 24 night - 1.5
bs_gukbap 35.1577 129.0596 0 24 any any 1
bs_yonggung 35.1884 129.2233 5 19 am - 1.5
bs_huinyeoul 35.0784 129.0450 10 20 day - 1.5
bs_centum 35.1690 129.1295 10.5 20 day - 2
bs_skin 35.1560 129.0590 10 19 day - 2
bs_gejang 35.1630 129.1630 11 22 any any 1.5
bs_blueline 35.1597 129.1690 9.5 19 day - 1.5
bs_taejongdae 35.0530 129.0870 4 24 day - 2
bs_gukje 35.0995 129.0280 9 20 day - 1.5
bs_songdo 35.0760 129.0170 9 21 eve - 1.5
jj_seongsan 33.4580 126.9425 7.5 19 am - 2
jj_halla 33.3463 126.4947 6 12 am - 4
jj_pork 33.5136 126.5330 11 22 any any 1.5
jj_dongmun 33.5117 126.5262 18 24 eve dinner 1
jj_aewol 33.4625 126.3105 9 21 day - 1.5
jj_jusang 33.2378 126.4250 9 18 day - 1
jj_dutyfree 33.4890 126.4880 9.5 19 day - 1.5
jj_sunset 33.4720 126.3420 0 24 eve - 1
jj_udo 33.5000 126.9530 8 17.5 day - 4
jj_hyeopjae 33.3940 126.2390 0 24 day - 1.5
jj_osulloc 33.3060 126.2895 9 18 day - 1.5
jj_cheonjiyeon 33.2470 126.5540 9 22 eve - 1
jj_seopji 33.4240 126.9300 0 24 day - 1
gj_bulguksa 35.7900 129.3320 9 18 am - 2
gj_seokguram 35.7950 129.3490 9 17.5 am - 1
gj_daereung 35.8365 129.2135 9 22 day - 1.5
gj_hwangni 35.8378 129.2095 10 21 day - 1.5
gj_wolji 35.8347 129.2266 9 22 night - 1.5
gj_ssambap 35.8395 129.2140 10 21 any any 1
gj_bomun 35.8426 129.2830 0 24 day - 1.5
gj_gyochon 35.8300 129.2150 9 18 day - 1
gn_anmok 37.7720 128.9470 9 22 day - 1.5
gn_gyeongpo 37.8020 128.9060 0 24 day - 1.5
gn_jumunjin 37.8930 128.8290 8 21 any any 1.5
gn_sundubu 37.7920 128.9150 7 19 am any 1
gn_ojukheon 37.7790 128.8786 9 18 day - 1
gn_bts 37.9090 128.8110 0 24 day - 0.5
gn_jungang 37.7540 128.8990 8 21 any any 1
jn_hanok 35.8150 127.1530 0 24 day - 2
jn_bibim 35.8172 127.1489 10 21 any any 1
jn_night 35.8130 127.1470 18 23 night dinner 1.5
jn_gyeonggi 35.8154 127.1497 9 18 day - 1
jn_tea 35.8145 127.1545 10 21 day - 1
jn_jeondong 35.8133 127.1490 9 18 day - 0.5
ys_cable 34.7330 127.7480 9.5 21.5 eve - 1.5
ys_night 34.7395 127.7395 18 26 night dinner 1.5
ys_gejang 34.7340 127.7300 9 21 any any 1
ys_odong 34.7440 127.7690 0 24 day - 1.5
ys_hyangil 34.5920 127.8020 0 24 am - 2
ys_aqua 34.7460 127.7480 9.5 18 day - 2
ys_dolsanpark 34.7317 127.7409 0 24 night - 1
"""

# Changes to existing places (Korean text, category, flags)
UPDATES = {
    "smt": None,  # replaced by "coex"
    "hybe": {"d": ["BTS 팬들이 찾는 하이브 사옥 주변", "BTS 粉丝常去的 HYBE 总部周边", "Outside HYBE HQ, a BTS fan stop", "BTSファンが訪れるHYBE社屋周辺"]},
    "banpo": {"season": [4, 10]},
    "jn_night": {"closed": [0, 1, 2, 3, 4]},
    "jj_halla": {"d": ["왕복 4시간 등산 · 정오 이후 입산 통제", "往返 4 小时登山 · 中午后禁止上山", "4-hr round-trip hike · no entry after noon", "往復4時間の登山 · 正午以降は入山不可"]},
    "bukchon": {"d": ["경복궁에서 걸어서 10분 · 17시 이후 관광 제한 구역 있음", "从景福宫步行 10 分钟 · 部分区域 17 点后限制游览", "10 min walk from Gyeongbokgung · some lanes closed to visitors after 5pm", "景福宮から徒歩10分 · 17時以降は観光制限の路地あり"]},
}

# New places: id, category, region, cost, flags, station/address, [ko n, ko d], [zh n, zh d], [en n, en d], [ja n, ja d]
NEW = [
    ("coex", "kpop", "seoul", 0, {}, "삼성역 6번 출구",
     ["코엑스 K-POP 광장·별마당도서관", "대형 전광판과 거대한 책장 도서관"],
     ["COEX K-POP 广场·星空图书馆", "巨型屏幕和超大书墙图书馆"],
     ["COEX K-POP Square & Starfield Library", "Giant media wall and towering bookshelves"],
     ["COEX K-POPスクエア・ピョルマダン図書館", "巨大スクリーンと巨大本棚の図書館"]),
    ("deoksugung", "palace", "seoul", 1000, {"closed": [1]}, "시청역 2번 출구",
     ["덕수궁", "돌담길 산책 · 밤 9시까지 개방"], ["德寿宫", "石墙路散步 · 开放到晚上 9 点"],
     ["Deoksugung Palace", "Stone-wall walk · open till 9pm"], ["徳寿宮", "石垣道の散歩 · 夜9時まで開放"]),
    ("namdaemun", "shop", "seoul", 0, {"closed": [0]}, "회현역 5번 출구",
     ["남대문시장", "갈치조림 골목·기념품 · 일요일 휴무 많음"], ["南大门市场", "带鱼炖锅巷·纪念品 · 周日多数休息"],
     ["Namdaemun Market", "Hairtail stew alley & souvenirs · many shops shut Sun"], ["南大門市場", "太刀魚煮込み路地・お土産 · 日曜休み多め"]),
    ("lotteworld", "fun", "seoul", 62000, {}, "잠실역 4번 출구",
     ["롯데월드", "실내외 테마파크 · 반나절"], ["乐天世界", "室内外主题乐园 · 约半天"],
     ["Lotte World", "Indoor-outdoor theme park · half a day"], ["ロッテワールド", "屋内外テーマパーク · 半日"]),
    ("naksan", "night", "seoul", 0, {}, "혜화역 2번 출구",
     ["낙산공원 성곽길", "한양도성 성곽 따라 보는 야경"], ["骆山公园城郭路", "沿着汉阳都城城墙看夜景"],
     ["Naksan Park wall trail", "Night views along the old city wall"], ["駱山公園の城郭道", "漢陽都城の城壁沿いの夜景"]),
    ("mangwon", "food", "seoul", 10000, {}, "망원역 2번 출구",
     ["망원시장", "현지인 시장 먹거리 · 예약 불필요"], ["望远市场", "本地人的市场小吃 · 无需预约"],
     ["Mangwon Market", "Local market snacks · no booking"], ["望遠市場", "地元の市場グルメ · 予約不要"]),
    ("noryangjin", "food", "seoul", 40000, {}, "노량진역 7번 출구",
     ["노량진수산시장", "1층에서 고르고 2층에서 먹는 회"], ["鹭梁津水产市场", "一楼挑海鲜，二楼现吃"],
     ["Noryangjin Fish Market", "Pick seafood downstairs, eat it upstairs"], ["鷺梁津水産市場", "1階で選んで2階で食べる刺身"]),
    ("bs_blueline", "fun", "busan", 7000, {}, "해운대구 달맞이길62번길 13",
     ["해운대 블루라인파크", "바다 옆을 달리는 해변열차·스카이캡슐"], ["海云台蓝线公园", "沿海行驶的海边列车·天空胶囊"],
     ["Haeundae Blueline Park", "Beach train and sky capsules along the coast"], ["海雲台ブルーラインパーク", "海沿いを走る海辺列車・スカイカプセル"]),
    ("bs_taejongdae", "nature", "busan", 0, {}, "영도구 전망로 24",
     ["태종대", "절벽 해안과 등대 · 다누비 열차"], ["太宗台", "悬崖海岸与灯塔 · Danubi 小火车"],
     ["Taejongdae", "Cliffs, lighthouse and the Danubi tram"], ["太宗台", "断崖の海岸と灯台 · ダヌビ列車"]),
    ("bs_gukje", "shop", "busan", 0, {}, "자갈치역 7번 출구",
     ["국제시장·BIFF광장", "국제시장 구경과 씨앗호떡"], ["国际市场·BIFF广场", "逛国际市场，吃坚果糖饼"],
     ["Gukje Market & BIFF Square", "Market browsing and seed hotteok"], ["国際市場・BIFF広場", "国際市場散策とシアッホットク"]),
    ("bs_songdo", "fun", "busan", 17000, {}, "서구 송도해변로 171",
     ["송도 해상케이블카", "바다 위를 지나는 케이블카"], ["松岛海上缆车", "从海面上空经过的缆车"],
     ["Songdo Marine Cable Car", "Cable car over the sea"], ["松島海上ケーブルカー", "海の上を渡るケーブルカー"]),
    ("jj_udo", "nature", "jeju", 10500, {}, "성산포항 종합여객터미널",
     ["우도", "배 타고 15분 · 땅콩 아이스크림"], ["牛岛", "坐船 15 分钟 · 花生冰淇淋"],
     ["Udo Island", "15-min ferry · peanut ice cream"], ["牛島", "船で15分 · ピーナッツアイス"]),
    ("jj_hyeopjae", "nature", "jeju", 0, {}, "제주시 한림읍 협재리",
     ["협재해변", "에메랄드빛 바다와 비양도 전망"], ["挟才海边", "翡翠色海水与飞扬岛景色"],
     ["Hyeopjae Beach", "Emerald water facing Biyangdo"], ["挟才ビーチ", "エメラルドの海と飛揚島の眺め"]),
    ("jj_osulloc", "cafe", "jeju", 9000, {}, "서귀포시 안덕면 신화역사로 15",
     ["오설록 티뮤지엄", "녹차밭 산책과 녹차 디저트"], ["O'sulloc 茶博物馆", "绿茶园散步和抹茶甜点"],
     ["O'sulloc Tea Museum", "Green tea fields and matcha desserts"], ["オソルロク ティーミュージアム", "緑茶畑の散歩と抹茶スイーツ"]),
    ("jj_cheonjiyeon", "nature", "jeju", 2000, {}, "서귀포시 남성중로 2-15",
     ["천지연폭포", "야간 조명이 예쁜 폭포 산책"], ["天地渊瀑布", "夜间灯光很美的瀑布步道"],
     ["Cheonjiyeon Falls", "Waterfall walk, lovely when lit at night"], ["天地淵瀑布", "夜のライトアップがきれいな滝の散歩道"]),
    ("jj_seopji", "nature", "jeju", 0, {}, "서귀포시 성산읍 섭지코지로 107",
     ["섭지코지", "성산일출봉이 보이는 해안 산책길"], ["涉地可支", "能看到城山日出峰的海岸步道"],
     ["Seopjikoji", "Coastal walk with Seongsan views"], ["渉地可支", "城山日出峰が見える海岸の散歩道"]),
    ("gj_seokguram", "palace", "gyeongju", 0, {}, "경주시 석굴로 238",
     ["석굴암", "토함산의 신라 석굴 불상"], ["石窟庵", "吐含山上的新罗石窟佛像"],
     ["Seokguram Grotto", "Silla stone Buddha on Tohamsan"], ["石窟庵", "吐含山の新羅石窟仏"]),
    ("gj_gyochon", "palace", "gyeongju", 0, {}, "경주시 교촌안길 27-40",
     ["교촌마을", "경주 최부자댁과 전통 한옥 골목"], ["校村村", "庆州崔富者宅与传统韩屋小巷"],
     ["Gyochon Hanok Village", "Choi family estate and hanok lanes"], ["校村マウル", "崔富者宅と伝統韓屋の路地"]),
    ("gn_jungang", "food", "gangneung", 10000, {}, "강릉시 금성로 21",
     ["강릉 중앙시장", "닭강정·감자전 시장 먹거리"], ["江陵中央市场", "炸鸡块·土豆煎饼市场小吃"],
     ["Gangneung Jungang Market", "Sweet fried chicken and potato pancakes"], ["江陵中央市場", "タッカンジョン・カムジャジョン"]),
    ("jn_jeondong", "palace", "jeonju", 0, {}, "전주시 완산구 태조로 51",
     ["전동성당", "1914년 지어진 로마네스크 성당"], ["殿洞圣堂", "1914 年建成的罗马式教堂"],
     ["Jeondong Cathedral", "Romanesque church built in 1914"], ["殿洞聖堂", "1914年建築のロマネスク様式の聖堂"]),
    ("ys_aqua", "fun", "yeosu", 33000, {}, "여수시 오동도로 61-11",
     ["아쿠아플라넷 여수", "벨루가가 있는 대형 아쿠아리움"], ["丽水 Aqua Planet", "有白鲸的大型水族馆"],
     ["Aqua Planet Yeosu", "Big aquarium with belugas"], ["アクアプラネット麗水", "ベルーガがいる大型水族館"]),
    ("ys_dolsanpark", "night", "yeosu", 0, {}, "여수시 돌산읍 돌산로 3600",
     ["돌산공원 야경", "돌산대교와 여수항 야경"], ["突山公园夜景", "突山大桥与丽水港夜景"],
     ["Dolsan Park night view", "Dolsan Bridge and harbor lights"], ["突山公園の夜景", "突山大橋と麗水港の夜景"]),
]
