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
gs_museum 35.9895 126.7105 9 18 am - 1.5
gs_chowon 35.9858 126.7133 9 18 day - 0.5
gs_dongguksa 35.9836 126.7118 9 18 am - 0.5
gs_rail 35.981 126.736 0 24 day - 0.75
gs_eunpa 35.954 126.72 0 24 eve - 1.0
gs_market 35.9871 126.7205 9 18 any any 0.75
gs_seonyudo 35.8114 126.41 0 24 eve - 4.0
mp_cable 34.8027 126.3712 9 19 eve - 1.0
mp_gohado 34.779 126.3655 9 18 eve - 0.75
mp_yudal 34.792 126.373 0 24 am - 1.5
mp_modern 34.7887 126.3838 9 18 day - 1.25
mp_gatbawi 34.7957 126.431 5 23 night - 0.5
mp_peace 34.7935 126.4336 0 24 night - 1.0
mp_market 34.787 126.3895 7 18 any any 1.0
dy_dodam 36.9998 128.3446 9 18 am - 0.7
dy_manchunha 36.9886 128.3606 9 17 day - 1.5
dy_jando 36.9858 128.3577 0 24 day - 0.7
dy_gosu 36.9757 128.3878 9 18 any - 1
dy_market 36.9846 128.3654 9 18 day any 1
dy_sainam 36.8973 128.3423 0 24 day - 0.5
dy_ondal 37.0485 128.5446 9 18 day - 1.5
ph_spacewalk 36.0656 129.3925 10 17 day - 1
ph_homigot 36.0768 129.5679 0 24 am - 1.5
ph_yeongildae 36.056 129.379 0 24 eve - 1
ph_guryongpo 35.9886 129.558 0 24 day - 1
ph_jukdo 36.0352 129.367 8 22 am any 1.5
ph_igari 36.196 129.387 9 18 day - 0.5
ph_canal 36.0335 129.38 9 18 day - 1
sc_seorak_cable 38.1728 128.4899 9 17 am - 1.5
sc_youngkeum 38.2133 128.6006 0 24 am - 0.7
sc_beach 38.19 128.6038 0 24 eve - 1
sc_abai 38.203 128.594 5.5 22.5 day - 1
sc_market 38.2047 128.59 8 24 day any 1
sc_yeongnang 38.216 128.583 0 24 day - 1.5
sc_daepo 38.1752 128.6078 0 24 eve any 1
dg_eworld 35.8533 128.5652 10 21 eve - 3
dg_suseong 35.8287 128.6176 0 24 eve - 1
dg_kimkwangseok 35.8599 128.6067 0 24 day - 0.7
dg_modern 35.8668 128.5873 0 24 am - 1.5
dg_seomun 35.869 128.5812 9 18 day any 1.5
dg_dongseongno 35.8692 128.5962 0 24 eve any 1.5
dg_palgong 35.989 128.695 9.5 17 am - 1.5
dg_apsan 35.8284 128.5857 10.5 20 night - 1.5
cc_skywalk 37.8955 127.7251 10 17.5 eve - 0.7
cc_samak_cable 37.869 127.699 9 18 day - 1.5
cc_gongjicheon 37.8708 127.7135 0 24 day - 1
cc_dakgalbi 37.8805 127.728 11 21 eve any 1.5
cc_kimyujeong 37.816 127.716 9.5 17 day - 1
cc_soyang_dam 37.9452 127.814 0 24 day - 1
cc_makguksu 37.918 127.7505 10 17 am - 1
ty_cablecar 34.8266 128.4251 9.5 18 am - 1.5
ty_luge 34.8244 128.4242 10 18 day - 1.5
ty_dongpirang 34.8453 128.4276 0 24 day - 1
ty_jungang 34.8453 128.4246 8 20 day any 1
ty_tongjeyoung 34.8472 128.4235 9 18 day - 1
ty_dipirang 34.8421 128.4285 18.5 22 night - 1
ty_dala 34.7692 128.3993 0 24 eve - 0.7
ty_yisunsin 34.8438 128.4429 0 24 am - 1
ul_taehwagang 35.5497 129.2955 0 24 any - 1.5
ul_daewangam 35.4925 129.4365 0 24 am - 1.5
ul_ganjeolgot 35.3593 129.3606 0 24 am - 1
ul_jangsaengpo 35.5012 129.3838 9 18 day - 1.5
ul_bridge_view 35.5043 129.4042 9 21 night - 0.7
ul_alps 35.5627 129.0452 9 22 day - 1.5
ul_eonyang_bulgogi 35.566 129.1225 11 20.5 eve any 1.5
ul_bangeojin 35.4878 129.4262 7 20 eve any 1
dm_juknokwon 35.3263 126.9866 9 18 am - 1.5
dm_gwanbang 35.3275 126.99 0 24 day - 0.7
dm_noodle 35.3243 126.988 10 20 day any 1
dm_metasequoia 35.3244 126.995 9 18 day - 1
dm_metaprovence 35.3218 126.9978 10 20 eve any 1
dm_soswaewon 35.1866 127.0134 9 17 am - 1
dm_gasa 35.191 127.0075 9 17 day - 1
"""

# Changes to existing places (Korean text, category, flags)
UPDATES = {
    "smt": None,  # replaced by "coex"
    # 2026-11-12 근거 없는 시연용 장소 제거 (prune_places.py REMOVED 와 같게)
    "skin1": None,
    "skin2": None,
    "spa": None,
    "bs_skin": None,
    "samgyup": None,
    "gejang": None,
    "samgye": None,
    "kalguksu": None,
    "sbrunch": None,
    "hanwoo": None,
    "bs_gejang": None,
    "jn_bibim": None,
    "ys_gejang": None,
    "hybe": None,
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
    # 2026-11-20 매일 콘텐츠: K링크 새 지역 군산·목포
    ("gs_museum", "palace", "gunsan", 2000, {"closed": [1]}, "군산시 해망로 240",
     ["군산근대역사박물관", "개항기 군산 거리와 생활사 전시"], ["群山近代历史博物馆", "开港时期群山街景与生活史展"], ["Gunsan Modern History Museum", "Port-era streets and daily life exhibits"], ["群山近代歴史博物館", "開港期の群山の街と暮らしの展示"]),
    ("gs_chowon", "palace", "gunsan", 0, {}, "군산시 구영2길 12-1",
     ["초원사진관", "영화 촬영지로 알려진 원도심 사진관"], ["草原照相馆", "因电影取景闻名的旧城照相馆"], ["Chowon Photo Studio", "Old-town photo studio from a well-known film"], ["草原写真館", "映画のロケ地として知られる写真館"]),
    ("gs_dongguksa", "palace", "gunsan", 0, {}, "군산시 동국사길 16",
     ["동국사", "일제강점기 일본식 사찰 건축이 남은 절"], ["东国寺", "保留日式寺院建筑的寺庙"], ["Dongguksa Temple", "Temple with surviving Japanese-style architecture"], ["東国寺", "日本式の寺院建築が残る寺"]),
    ("gs_rail", "fun", "gunsan", 0, {}, "군산시 경촌4길 14",
     ["경암동 철길마을", "옛 철길 양옆으로 이어진 골목"], ["京岩洞铁路村", "旧铁轨两旁的小巷"], ["Gyeongam-dong Railroad Village", "Lanes along an old railway track"], ["京岩洞線路村", "古い線路沿いの路地"]),
    ("gs_eunpa", "nature", "gunsan", 0, {}, "군산시 은파순환길 9",
     ["은파호수공원", "호수 둘레길과 물빛다리 야경"], ["银波湖水公园", "环湖步道与水光桥夜景"], ["Eunpa Lake Park", "Lakeside trail and lit bridge at night"], ["銀波湖水公園", "湖畔の散歩道と橋の夜景"]),
    ("gs_market", "food", "gunsan", 10000, {}, "군산시 신금길 18",
     ["군산공설시장", "박대·건어물과 시장 먹거리"], ["群山公设市场", "干鱼与市场小吃"], ["Gunsan Public Market", "Dried fish and market snacks"], ["群山公設市場", "干物と市場グルメ"]),
    ("gs_seonyudo", "nature", "gunsan", 0, {}, "군산시 옥도면 선유도리",
     ["선유도", "고군산군도 해변과 망주봉 · 차로 다리 건너"], ["仙游岛", "古群山群岛海滩与望主峰"], ["Seonyudo Island", "Gogunsan beaches and Mangjubong, reached by bridge"], ["仙遊島", "古群山群島の浜辺と望主峰"]),
    ("mp_cable", "fun", "mokpo", 24000, {}, "목포해상케이블카 북항 스테이션",
     ["목포해상케이블카", "유달산을 넘어 바다 건너 고하도까지"], ["木浦海上缆车", "越过儒达山跨海到高下岛"], ["Mokpo Marine Cable Car", "Over Yudalsan and across the sea to Gohado"], ["木浦海上ケーブルカー", "儒達山を越えて海を渡る"]),
    ("mp_gohado", "nature", "mokpo", 0, {}, "목포시 고하도안길 234",
     ["고하도 전망대", "케이블카로 건너는 섬 전망대와 해안 데크"], ["高下岛展望台", "乘缆车到达的海岛展望台"], ["Gohado Observatory", "Island lookout and coastal deck by cable car"], ["高下島展望台", "ケーブルカーで渡る島の展望台"]),
    ("mp_yudal", "nature", "mokpo", 0, {}, "목포시 노적봉길 45",
     ["유달산", "목포 시내와 다도해가 보이는 바위산"], ["儒达山", "可眺望木浦市区与多岛海"], ["Yudalsan Mountain", "Rocky peak over the city and islands"], ["儒達山", "市内と多島海を望む岩山"]),
    ("mp_modern", "palace", "mokpo", 2000, {"closed": [1]}, "목포시 영산로29번길 6",
     ["목포근대역사관", "옛 영사관 건물의 근대 역사 전시"], ["木浦近代历史馆", "旧领事馆建筑里的近代史展"], ["Mokpo Modern History Museum", "Modern history in a former consulate"], ["木浦近代歴史館", "旧領事館の近代史展示"]),
    ("mp_gatbawi", "night", "mokpo", 0, {}, "목포시 남농로 166-1",
     ["갓바위", "해상보행교로 보는 삿갓 모양 바위"], ["笠岩", "从海上步道看斗笠形岩石"], ["Gatbawi Rocks", "Hat-shaped rocks seen from a sea boardwalk"], ["カッパウィ", "笠の形をした岩と海上遊歩道"]),
    ("mp_peace", "night", "mokpo", 0, {}, "목포시 평화로 64",
     ["평화광장", "바다 분수 공연과 해변 산책"], ["和平广场", "海上喷泉表演与海边散步"], ["Peace Plaza", "Sea fountain shows and a seaside walk"], ["平和広場", "海の噴水ショーと海辺の散歩"]),
    ("mp_market", "food", "mokpo", 20000, {}, "목포시 해안로 267",
     ["목포종합수산시장", "홍어·낙지·생선을 고르는 수산시장"], ["木浦综合水产市场", "挑选斑鳐、章鱼与鲜鱼"], ["Mokpo Fish Market", "Skate, octopus and fresh fish"], ["木浦総合水産市場", "エイ・タコ・鮮魚の市場"]),
    # 2026-11-21 매일 콘텐츠: K링크 새 지역 단양·포항
    ('dy_dodam', 'nature', 'danyang', 0, {}, '단양군 매포읍 삼봉로 644',
     ['도담삼봉', '남한강 위 세 봉우리'], ['岛潭三峰', '南汉江上的三座石峰'], ['Dodamsambong Peaks', 'Three rock peaks in the Namhangang River'], ['島潭三峰', '南漢江に浮かぶ三つの岩峰']),
    ('dy_manchunha', 'fun', 'danyang', 4000, {}, '단양군 적성면 옷바위길 10',
     ['만천하스카이워크', '남한강 절벽 위 유리 전망대'], ['万天下天空步道', '南汉江悬崖上的玻璃观景台'], ['Mancheonha Skywalk', 'Glass-floor observatory above the river'], ['万天下スカイウォーク', '南漢江の断崖上のガラス展望台']),
    ('dy_jando', 'nature', 'danyang', 0, {}, '단양군 적성면 애곡리 (상진철교 쪽)',
     ['단양강 잔도', '강 절벽 따라 걷는 1.2km 길'], ['丹阳江栈道', '沿江悬崖步道1.2公里'], ['Danyanggang Jando Trail', '1.2 km cliffside river walkway'], ['丹陽江桟道', '川沿いの崖を歩く1.2kmの道']),
    ('dy_gosu', 'nature', 'danyang', 11000, {}, '단양군 단양읍 고수동굴길 8',
     ['고수동굴', '천연기념물 석회암 동굴'], ['古薮洞窟', '天然纪念物石灰岩洞窟'], ['Gosudonggul Cave', 'Limestone cave, natural monument'], ['古藪洞窟', '天然記念物の鍾乳洞']),
    ('dy_market', 'food', 'danyang', 0, {}, '단양군 단양읍 (단양구경시장)',
     ['단양구경시장', '마늘 간식 모인 상설시장'], ['丹阳九景市场', '以大蒜小吃闻名的市场'], ['Danyang Gugyeong Market', 'Market known for garlic snacks'], ['丹陽九景市場', 'ニンニク料理が並ぶ市場']),
    ('dy_sainam', 'nature', 'danyang', 0, {}, '단양군 대강면 사인암2길 42',
     ['사인암', '단양팔경 70m 절벽'], ['舍人岩', '丹阳八景之一的70米绝壁'], ['Sainam Rock', "70 m cliff, one of Danyang's Eight Views"], ['舎人岩', '丹陽八景の高さ70mの絶壁']),
    ('dy_ondal', 'fun', 'danyang', 6000, {}, '단양군 영춘면 온달로 23',
     ['온달관광지', '온달동굴 있는 강변 관광지'], ['温达观光地', '设有温达洞窟的江边景区'], ['Ondal Tourist Park', 'Riverside park with Ondal Cave'], ['温達観光地', '温達洞窟がある川辺の観光地']),
    ('ph_spacewalk', 'fun', 'pohang', 0, {}, '포항시 북구 환호공원길 30',
     ['스페이스워크', '환호공원 언덕 위 걷는 철제 조형물'], ['太空漫步', '环湖公园山丘上的步行钢结构'], ['Space Walk', 'Walkable steel sculpture in Hwanho Park'], ['スペースウォーク', '環湖公園の歩ける鉄の造形物']),
    ('ph_homigot', 'nature', 'pohang', 0, {}, '포항시 남구 호미곶면 대보리',
     ['호미곶 해맞이광장', '상생의 손이 있는 일출 명소'], ['虎尾串迎日广场', '有相生之手的日出胜地'], ['Homigot Sunrise Plaza', 'Sunrise spot with the Hands of Harmony'], ['虎尾串日の出広場', '相生の手がある日の出の名所']),
    ('ph_yeongildae', 'nature', 'pohang', 0, {}, '포항시 북구 두호동',
     ['영일대해수욕장', '누각 영일대가 있는 도심 해변'], ['迎日台海水浴场', '有海上楼阁的市区海滩'], ['Yeongildae Beach', 'City beach with a sea pavilion'], ['迎日台海水浴場', '海上楼閣のある市街のビーチ']),
    ('ph_guryongpo', 'palace', 'pohang', 0, {}, '포항시 남구 구룡포읍 호미로 277',
     ['구룡포 일본인 가옥거리', '일본식 목조 가옥 47채 거리'], ['九龙浦日本人住宅街', '保留日式木屋的街道'], ['Guryongpo Japanese House Street', 'Street of old Japanese wooden houses'], ['九龍浦日本人家屋通り', '日本式木造家屋が残る通り']),
    ('ph_jukdo', 'food', 'pohang', 0, {}, '포항시 북구 죽도시장13길 13',
     ['죽도시장', '동해안 최대 규모 전통시장'], ['竹岛市场', '东海岸最大的传统市场'], ['Jukdo Market', 'Largest traditional market on the east coast'], ['竹島市場', '東海岸最大級の伝統市場']),
    ('ph_igari', 'nature', 'pohang', 0, {}, '포항시 북구 청하면 이가리',
     ['이가리 닻 전망대', '닻 모양 해안 전망대'], ['二佳里锚形展望台', '锚形海边观景台'], ['Igari Anchor Observatory', 'Anchor-shaped seaside observatory'], ['イガリ錨展望台', '錨の形の海辺の展望台']),
    ('ph_canal', 'fun', 'pohang', 0, {}, '포항시 남구 희망대로 1040 (포항운하관)',
     ['포항운하', '크루즈로 도는 도심 물길'], ['浦项运河', '可乘游船的市区水道'], ['Pohang Canal', 'City canal with cruise boats'], ['浦項運河', 'クルーズで巡る街なかの水路']),
    # 2026-11-21(2차) 매일 콘텐츠: K링크 새 지역 속초·대구
    ('sc_seorak_cable', 'nature', 'sokcho', 16000, {}, '속초시 설악산로 1085',
     ['설악산 케이블카', '권금성까지 10분 케이블카'], ['雪岳山缆车', '10分钟直达权金城'], ['Seorak Cable Car', '10-minute ride up to Gwongeumseong'], ['雪岳山ケーブルカー', '権金城まで約10分のケーブルカー']),
    ('sc_youngkeum', 'nature', 'sokcho', 0, {}, '속초시 영금정로 43',
     ['영금정', '파도 소리 들리는 바위 정자'], ['灵琴亭', '灯塔下的海边岩石与亭子'], ['Yeonggeumjeong', 'Seaside rocks and pavilion by the lighthouse'], ['霊琴亭', '灯台下の岩場と海上あずまや']),
    ('sc_beach', 'nature', 'sokcho', 0, {}, '속초시 해오름로 186',
     ['속초해수욕장', '터미널 옆 시내 해변'], ['束草海水浴场', '客运站旁的市区海滩'], ['Sokcho Beach', 'City beach near the bus terminal'], ['束草海水浴場', 'バスターミナル近くの市街地ビーチ']),
    ('sc_abai', 'fun', 'sokcho', 500, {}, '속초시 중앙부두길 51',
     ['아바이마을 갯배', '줄 당겨 건너는 수로 배'], ['阿爸村渡船', '拉绳渡过水道到阿爸村'], ['Abai Village Gaetbae Ferry', 'Pull-rope barge to Abai Village'], ['アバイ村ケッベ渡し船', 'ロープを引いて渡る渡し船']),
    ('sc_market', 'food', 'sokcho', 0, {}, '속초시 중앙로147번길 12',
     ['속초관광수산시장', '오징어순대·닭강정 시장'], ['束草观光水产市场', '鱿鱼米肠与炸鸡块市场'], ['Sokcho Tourist & Fishery Market', 'Seafood, squid sundae and fried chicken'], ['束草観光水産市場', 'イカスンデやタッカンジョンの市場']),
    ('sc_yeongnang', 'nature', 'sokcho', 0, {}, '속초시 영랑호반길 140',
     ['영랑호', '둘레 7.8km 자연 석호'], ['永郎湖', '周长7.8公里的天然潟湖'], ['Yeongnangho Lake', '7.8 km lagoon with lakeside trail'], ['永郎湖', '周囲7.8kmの天然潟湖']),
    ('sc_daepo', 'food', 'sokcho', 0, {}, '속초시 대포항희망길 55',
     ['대포항', '튀김골목·전망대 있는 항구'], ['大浦港', '有炸物街与观景台的港口'], ['Daepo Port', 'Harbor with fried-seafood alley and lookout'], ['大浦港', '揚げ物横丁と展望台がある港']),
    ('dg_eworld', 'fun', 'daegu', 49000, {}, '대구 달서구 두류공원로 200',
     ['이월드·83타워', '두류공원 테마파크와 전망 타워'], ['E-World·83塔', '头流公园主题乐园与观景塔'], ['E-World & 83 Tower', 'Theme park and observation tower'], ['イーワールド・83タワー', '頭流公園のテーマパークと展望タワー']),
    ('dg_suseong', 'nature', 'daegu', 0, {}, '대구 수성구 용학로 35-5',
     ['수성못', '둘레 2km 호수 산책·음악분수'], ['寿城池', '环湖散步与音乐喷泉'], ['Suseongmot Lake', 'Lakeside walk and music fountain'], ['寿城池', '湖畔散策と音楽噴水']),
    ('dg_kimkwangseok', 'fun', 'daegu', 0, {}, '대구 중구 달구벌대로 2238',
     ['김광석 다시그리기길', '방천시장 옆 350m 벽화 골목'], ['金光石街', '防川市场旁350米壁画小巷'], ['Kim Kwang-seok Street', '350 m mural alley by Bangcheon Market'], ['キム・グァンソク通り', '防川市場横の350m壁画路地']),
    ('dg_modern', 'palace', 'daegu', 0, {}, '대구 중구 달구벌대로 2029',
     ['근대골목·청라언덕', '선교사 주택과 90계단 근대 골목'], ['近代胡同·青萝山丘', '传教士住宅与90级台阶'], ['Modern History Alleys & Cheongna Hill', 'Missionary houses and the 90 steps'], ['近代路地・青蘿の丘', '宣教師住宅と90階段']),
    ('dg_seomun', 'shop', 'daegu', 0, {}, '대구 중구 큰장로26길 45',
     ['서문시장', '대구 대표 시장·금~일 야시장'], ['西门市场', '大邱代表市场·周五至周日夜市'], ['Seomun Market', "Daegu's main market, night market Fri-Sun"], ['西門市場', '大邱最大の市場・金~日夜市']),
    ('dg_dongseongno', 'shop', 'daegu', 0, {}, '대구 중구 동성로2길 27',
     ['동성로', '약 900m 대구 대표 번화가'], ['东城路', '约900米的大邱繁华街'], ['Dongseong-ro', "Daegu's main 900 m shopping street"], ['東城路', '約900mの大邱随一の繁華街']),
    ('dg_palgong', 'nature', 'daegu', 14000, {}, '대구 동구 팔공산로185길 51',
     ['팔공산 케이블카', '신림봉 정상까지 오르는 곤돌라'], ['八公山缆车', '登上新林峰顶的缆车'], ['Palgongsan Cable Car', 'Gondola to Sinnimbong Peak'], ['八公山ケーブルカー', '新林峰山頂へのゴンドラ']),
    ('dg_apsan', 'night', 'daegu', 14000, {}, '대구 남구 앞산순환로 574-114',
     ['앞산전망대', '케이블카로 오르는 시내 야경 명소'], ['前山展望台', '乘缆车看市区夜景'], ['Apsan Observatory', 'City night view by cable car'], ['前山展望台', 'ケーブルカーで上る夜景スポット']),
    # 2026-11-25 매일 콘텐츠: K링크 새 지역 춘천·통영
    ('cc_skywalk', 'nature', 'chuncheon', 2000, {}, '춘천시 영서로 2663',
     ['소양강 스카이워크', '강 위 유리 바닥 다리'], ['昭阳江天空步道', '江面上的玻璃地板步道'], ['Soyanggang Skywalk', 'Glass-floor walkway over the Soyang River'], ['昭陽江スカイウォーク', '川の上のガラス床の歩道']),
    ('cc_samak_cable', 'fun', 'chuncheon', 24000, {}, '춘천시 스포츠타운길 245',
     ['삼악산 호수케이블카', '의암호 건너는 3.61km 케이블카'], ['三岳山湖水缆车', '横跨衣岩湖的3.61公里缆车'], ['Samaksan Lake Cable Car', '3.61 km ride across Uiamho Lake'], ['三岳山湖水ケーブルカー', '衣岩湖を渡る3.61kmのケーブルカー']),
    ('cc_gongjicheon', 'nature', 'chuncheon', 0, {}, '춘천시 이디오피아길 25',
     ['공지천유원지', '의암호 옆 산책·조각공원'], ['孔之川游园地', '衣岩湖边的散步道与雕塑公园'], ['Gongjicheon Recreation Area', 'Riverside park and trails by Uiamho Lake'], ['孔之川遊園地', '衣岩湖そばの散策路と彫刻公園']),
    ('cc_dakgalbi', 'food', 'chuncheon', 0, {}, '춘천시 조양동 52',
     ['춘천 명동 닭갈비골목', '철판·숯불 닭갈비 골목'], ['春川明洞辣炒鸡排一条街', '铁板与炭烤鸡排胡同'], ['Chuncheon Myeongdong Dakgalbi Street', 'Alley of pan-fried and charcoal dakgalbi'], ['春川明洞タッカルビ通り', '鉄板・炭火タッカルビの路地']),
    ('cc_kimyujeong', 'palace', 'chuncheon', 2000, {}, '춘천시 신동면 김유정로 1430-14',
     ['김유정문학촌', '소설가 김유정 고향 문학관'], ['金裕贞文学村', '小说家金裕贞故乡文学馆'], ['Kim Yu-jeong Literary Village', "Novelist Kim Yu-jeong's hometown museum"], ['金裕貞文学村', '小説家金裕貞の故郷の文学館']),
    ('cc_soyang_dam', 'nature', 'chuncheon', 0, {}, '춘천시 신북읍 신샘밭로 1128',
     ['소양강댐', '정상길 걷는 소양호 댐'], ['昭阳江大坝', '可走坝顶步道的昭阳湖大坝'], ['Soyanggang Dam', 'Walk the dam crest over Soyangho Lake'], ['昭陽江ダム', '堤頂を歩ける昭陽湖のダム']),
    ('cc_makguksu', 'fun', 'chuncheon', 1000, {}, '춘천시 신북읍 신북로 264',
     ['춘천막국수체험박물관', '막국수 만들기 체험 박물관'], ['春川荞麦冷面体验博物馆', '亲手制作荞麦面的博物馆'], ['Chuncheon Makguksu Museum', 'Make your own buckwheat noodles'], ['春川マックッス体験博物館', 'そば麺づくり体験ができる博物館']),
    ('ty_cablecar', 'nature', 'tongyeong', 17000, {}, '통영시 발개로 205',
     ['통영케이블카', '미륵산 9분 케이블카'], ['统营缆车', '9分钟登弥勒山'], ['Tongyeong Cable Car', '9-minute ride up Mireuksan'], ['統営ケーブルカー', '弥勒山まで約9分のケーブルカー']),
    ('ty_luge', 'fun', 'tongyeong', 30000, {}, '통영시 발개로 178',
     ['스카이라인 루지 통영', '리프트 타고 루지로 하강'], ['统营天际线斜坡滑车', '坐缆椅上山、滑车下山'], ['Skyline Luge Tongyeong', 'Chairlift up, luge ride down'], ['スカイラインリュージュ統営', 'リフトで上がりリュージュで下る']),
    ('ty_dongpirang', 'fun', 'tongyeong', 0, {}, '통영시 동피랑1길 6-18',
     ['동피랑 벽화마을', '강구안 언덕 벽화 골목'], ['东皮郎壁画村', '江口岸山坡壁画小巷'], ['Dongpirang Mural Village', 'Hillside mural alleys above Gangguan'], ['東ピラン壁画村', '江口岸の丘の壁画路地']),
    ('ty_jungang', 'food', 'tongyeong', 0, {}, '통영시 중앙시장1길 14-16',
     ['통영중앙시장', '활어·꿀빵 강구안 시장'], ['统营中央市场', '港边活鱼与蜂蜜面包市场'], ['Tongyeong Jungang Market', 'Live fish and honey bread by the harbor'], ['統営中央市場', '港前の活魚とクルパンの市場']),
    ('ty_tongjeyoung', 'palace', 'tongyeong', 3000, {}, '통영시 세병로 27',
     ['통영 삼도수군통제영', '세병관 남은 수군 본진'], ['统营三道水军统制营', '保留洗兵馆的水军本营'], ['Samdo Sugun Tongjeyeong', 'Joseon naval HQ with Sebyeonggwan'], ['統営三道水軍統制営', '洗兵館が残る水軍本営']),
    ('ty_dipirang', 'night', 'tongyeong', 15000, {}, '통영시 남망공원길 29',
     ['디피랑', '남망산 야간 미디어아트'], ['Dpirang夜间公园', '南望山夜间媒体艺术步道'], ['Dpirang', 'Night media-art trail on Nammangsan'], ['ディピラン', '南望山の夜間メディアアート']),
    ('ty_dala', 'nature', 'tongyeong', 0, {}, '통영시 산양일주로 1115',
     ['달아공원', '한려수도 노을 전망 공원'], ['达牙公园', '眺望闲丽水道的日落公园'], ['Dala Park', 'Sunset viewpoint over Hallyeosudo'], ['ダラ公園', '閑麗水道の夕日展望公園']),
    ('ty_yisunsin', 'nature', 'tongyeong', 0, {}, '통영시 정량동 688-1',
     ['통영 이순신공원', '17.3m 동상 선 바닷가 공원'], ['统营李舜臣公园', '立有17.3米铜像的海边公园'], ['Yi Sun-sin Park Tongyeong', 'Seaside park with a 17.3 m statue'], ['統営李舜臣公園', '17.3mの銅像が立つ海辺の公園']),
    # 2026-11-26 매일 콘텐츠: K링크 새 지역 울산·담양
    ('ul_taehwagang', 'nature', 'ulsan', 0, {}, '울산 중구 샛강남길 5',
     ['태화강 국가정원', '십리대숲 있는 국가정원'], ['太和江国家庭园', '有十里竹林的国家庭园'], ['Taehwagang National Garden', 'National garden with the Simni Bamboo Grove'], ['太和江国家庭園', '十里竹林のある国家庭園']),
    ('ul_daewangam', 'nature', 'ulsan', 0, {}, '울산 동구 등대로 95',
     ['대왕암공원', '기암 바다와 303m 출렁다리'], ['大王岩公园', '海边奇岩与303米吊桥'], ['Daewangam Park', 'Seaside rocks and a 303 m suspension bridge'], ['大王岩公園', '海辺の奇岩と303mの吊り橋']),
    ('ul_ganjeolgot', 'nature', 'ulsan', 0, {}, '울산 울주군 서생면 간절곶1길 39-2',
     ['간절곶', '해 일찍 뜨는 해맞이 명소'], ['艮绝串', '早看日出的海岬与灯塔'], ['Ganjeolgot Cape', 'Early sunrise spot with a lighthouse'], ['艮絶串', '早く日が昇る岬と灯台']),
    ('ul_jangsaengpo', 'fun', 'ulsan', 3000, {'closed': [1]}, '울산 남구 장생포고래로 271-1',
     ['장생포 고래문화마을', '옛 고래잡이 마을 재현'], ['长生浦鲸鱼文化村', '重现昔日捕鲸村'], ['Jangsaengpo Whale Culture Village', 'Recreated old whaling village'], ['長生浦クジラ文化村', '昔の捕鯨村を再現']),
    ('ul_bridge_view', 'night', 'ulsan', 0, {}, '울산 동구 봉수로 155-1',
     ['울산대교 전망대', '화정산 63m 전망대'], ['蔚山大桥展望台', '华井山上63米展望台'], ['Ulsandaegyo Observatory', '63 m tower over Ulsan Bridge'], ['蔚山大橋展望台', '華井山の63m展望台']),
    ('ul_alps', 'fun', 'ulsan', 0, {'closed': [1]}, '울산 울주군 상북면 알프스온천5길 103-8',
     ['영남알프스 복합웰컴센터', '산자락 영화관·클라이밍장'], ['岭南阿尔卑斯综合迎宾中心', '山脚下的影院与攀岩馆'], ['Yeongnam Alps Complex Welcome Center', 'Cinema and climbing gym below the peaks'], ['嶺南アルプス複合ウェルカムセンター', '山麓の映画館とクライミング場']),
    ('ul_eonyang_bulgogi', 'food', 'ulsan', 0, {}, '울산 울주군 언양읍 헌양길 일대',
     ['언양불고기 특구', '석쇠 언양불고기 집 모인 곳'], ['彦阳烤牛肉特区', '炭烤彦阳烤牛肉餐馆聚集地'], ['Eonyang Bulgogi Special Zone', 'Cluster of grilled Eonyang bulgogi houses'], ['彦陽プルコギ特区', '網焼き彦陽プルコギ店が集まる所']),
    ('ul_bangeojin', 'food', 'ulsan', 0, {'closed': [1]}, '울산 동구 중진2길 5',
     ['방어진 활어센터', '방어진항 옆 활어 시장'], ['方鱼津活鱼中心', '方鱼津港旁的活鱼市场'], ['Bangeojin Live Fish Center', 'Live fish market by Bangeojin Port'], ['方魚津活魚センター', '方魚津港そばの活魚市場']),
    ('dm_juknokwon', 'nature', 'damyang', 3000, {}, '담양군 담양읍 죽녹원로 119',
     ['죽녹원', '8가지 산책로의 대나무숲 정원'], ['竹绿苑', '有八条主题步道的竹林园'], ['Juknokwon Bamboo Garden', 'Bamboo forest with eight themed trails'], ['竹緑苑', '8つのテーマ散策路がある竹林']),
    ('dm_gwanbang', 'nature', 'damyang', 0, {}, '담양군 담양읍 남사리 일원',
     ['관방제림', '300년 노거수 담양천 둑길'], ['官防堤林', '潭阳川堤岸的三百年古树林'], ['Gwanbangjerim Forest', '300-year-old trees along the Damyangcheon levee'], ['官防堤林', '潭陽川の堤防に続く樹齢300年の並木']),
    ('dm_noodle', 'food', 'damyang', 0, {}, '담양군 담양읍 객사3길 일대',
     ['담양 국수거리', '강변 국숫집 음식테마거리'], ['潭阳面条街', '江边的面馆一条街'], ['Damyang Noodle Street', 'Riverside row of noodle houses'], ['潭陽ククス通り', '川沿いに麺の店が並ぶ通り']),
    ('dm_metasequoia', 'nature', 'damyang', 2000, {}, '담양군 담양읍 메타세쿼이아로 12',
     ['담양 메타세쿼이아길', '1972년 심은 5km 가로수길'], ['潭阳水杉林荫路', '1972年种植的5公里林荫道'], ['Damyang Metasequoia-lined Road', '5 km tree-lined road planted in 1972'], ['潭陽メタセコイア並木道', '1972年に植えられた5kmの並木道']),
    ('dm_metaprovence', 'shop', 'damyang', 0, {}, '담양군 담양읍 깊은실길 2-17',
     ['담양 메타프로방스', '프로방스풍 상점·공방 단지'], ['潭阳Meta Provence', '普罗旺斯风格商街与工坊'], ['Damyang Meta Provence', 'Provence-style shops and workshops'], ['潭陽メタプロバンス', 'プロヴァンス風の店と工房の街']),
    ('dm_soswaewon', 'palace', 'damyang', 2000, {}, '담양군 가사문학면 소쇄원길 17',
     ['소쇄원', '조선 선비의 계곡 원림'], ['潇洒园', '朝鲜士人的溪谷园林'], ['Soswaewon Garden', "Joseon scholar's valley garden"], ['瀟灑園', '朝鮮時代の士人が造った渓谷の庭園']),
    ('dm_gasa', 'palace', 'damyang', 0, {}, '담양군 가사문학면 가사문학로 877',
     ['한국가사문학관', '송순·정철 가사문학 전시관'], ['韩国歌辞文学馆', '宋纯·郑澈歌辞文学展馆'], ['Korea Gasa Literature Museum', 'Gasa poetry of Song Sun and Jeong Cheol'], ['韓国歌辞文学館', '宋純・鄭澈の歌辞文学の展示館']),
]

# 장소 이름 별칭 (2026-11-13 컨펌 i261113-02) — 사이트 빌드(scripts/build.py link_keys)가 글↔장소 연결에 함께 쓴다.
# 규칙: 3글자 이상만(2글자 별칭 금지), 흔한 낱말 금지(build.py K_LINK_GENERIC), 별칭으로만 걸린 글은
#       그 장소 지역 이름이 본문·제목에 나오고 다른 K링크 지역의 여행 가이드가 아닐 때만 연결한다(동명 장소 방지).
# 국내·해외 장소 모두 여기 둔다(id는 places.json 과 같다). places.json 을 다시 만들 필요는 없다.
ALIASES = {
    # 서울
    "gbg": ["경복궁"], "bukchon": ["북촌한옥마을", "북촌 한옥"], "cdg": ["창덕궁"], "insa": ["인사동", "쌈지길"],
    "gwangjang": ["광장시장"], "mdfood": ["명동 길거리", "명동 노점"], "dakgalbi": ["닭갈비 골목"], "oliveyoung": ["올리브영 명동"],
    "garosu": ["가로수길"], "seongsu": ["성수동", "성수 편집숍"], "ddp": ["동대문디자인플라자", "동대문 패션"], "hongdae": ["홍대 거리", "홍대입구"],
    "thehyundai": ["더현대 서울", "더현대"], "scafe": ["성수동 카페"], "ikcafe": ["익선동"], "ycafe": ["연남동"], "kstar": ["K-스타로드", "케이스타로드"],
    "namsan": ["남산서울타워", "N서울타워", "남산타워"], "hangang": ["한강공원", "여의도 한강"], "lotte": ["롯데월드타워", "서울스카이"],
    "cheong": ["청계천"], "banpo": ["달빛무지개분수", "반포한강"], "seoulforest": ["서울숲"], "coex": ["코엑스", "별마당도서관"],
    "deoksugung": ["덕수궁"], "namdaemun": ["남대문시장"], "lotteworld": ["롯데월드 어드벤처"], "naksan": ["낙산공원"], "mangwon": ["망원시장"],
    "noryangjin": ["노량진수산시장", "노량진 수산"],
    # 부산
    "bs_haeundae": ["해운대해수욕장", "해운대 해변"], "bs_gamcheon": ["감천문화마을", "감천마을"], "bs_jagalchi": ["자갈치시장", "자갈치"],
    "bs_gwangan": ["광안대교", "광안리"], "bs_gukbap": ["돼지국밥 골목", "서면 국밥"], "bs_yonggung": ["해동용궁사", "용궁사"],
    "bs_huinyeoul": ["흰여울문화마을", "흰여울"], "bs_centum": ["센텀시티"], "bs_blueline": ["블루라인파크", "해변열차"],
    "bs_taejongdae": ["태종대"], "bs_gukje": ["국제시장", "BIFF광장"], "bs_songdo": ["송도해상케이블카", "송도 케이블카", "송도해수욕장"],
    # 제주
    "jj_seongsan": ["성산일출봉", "일출봉"], "jj_halla": ["한라산"], "jj_pork": ["흑돼지 거리", "흑돼지거리"], "jj_dongmun": ["동문시장"],
    "jj_aewol": ["애월 카페", "애월해안"], "jj_jusang": ["주상절리"], "jj_dutyfree": ["제주 면세점"], "jj_sunset": ["애월 해안도로", "애월 노을"],
    "jj_udo": ["우도 땅콩", "우도 도항선", "우도행", "우도 배시간"], "jj_hyeopjae": ["협재해변", "협재해수욕장"], "jj_osulloc": ["오설록"],
    "jj_cheonjiyeon": ["천지연폭포", "천지연"], "jj_seopji": ["섭지코지"],
    # 경주
    "gj_bulguksa": ["불국사"], "gj_daereung": ["대릉원", "첨성대"], "gj_hwangni": ["황리단길"], "gj_wolji": ["동궁과 월지", "안압지"],
    "gj_ssambap": ["쌈밥 거리", "쌈밥거리"], "gj_bomun": ["보문호", "보문관광단지"], "gj_seokguram": ["석굴암"], "gj_gyochon": ["교촌마을", "월정교"],
    # 강릉
    "gn_anmok": ["안목해변", "커피거리"], "gn_gyeongpo": ["경포해변", "경포대", "경포호"], "gn_jumunjin": ["주문진"], "gn_sundubu": ["초당순두부", "초당 순두부"],
    "gn_ojukheon": ["오죽헌"], "gn_bts": ["향호해변"], "gn_jungang": ["강릉중앙시장", "강릉 중앙시장"],
    # 전주
    "jn_hanok": ["전주한옥마을", "전주 한옥마을"], "jn_night": ["남부시장"], "jn_gyeonggi": ["경기전"], "jn_tea": ["전통 찻집"], "jn_jeondong": ["전동성당"],
    # 여수
    "ys_cable": ["여수해상케이블카", "여수 케이블카"], "ys_night": ["낭만포차"], "ys_odong": ["오동도"], "ys_hyangil": ["향일암"],
    "ys_aqua": ["아쿠아플라넷"], "ys_dolsanpark": ["돌산공원", "돌산대교"],
    # 일본
    "tk_sensoji": ["센소지", "아사쿠사"], "tk_nakamise": ["나카미세"], "tk_ueno": ["우에노"], "tk_shibuya": ["시부야"], "tk_meiji": ["메이지 신궁", "메이지신궁"],
    "tk_takeshita": ["다케시타", "하라주쿠"], "tk_tocho": ["도쿄도청"], "tk_omoide": ["오모이데 요코초", "오모이데요코초"], "tk_odaiba": ["오다이바"],
    "tk_kamakura": ["가마쿠라"], "tk_hakone": ["하코네"],
    "os_dotonbori": ["도톤보리"], "os_shinsaibashi": ["신사이바시"], "os_kuromon": ["구로몬"], "os_shinsekai": ["신세카이", "츠텐카쿠"],
    "os_castle": ["오사카성"], "os_umeda": ["우메다", "공중정원"], "os_usj": ["유니버설 스튜디오", "유니버설스튜디오"], "os_kaiyukan": ["가이유칸", "카이유칸"],
    "os_nara": ["나라 공원", "나라공원", "도다이지"],
    "ky_kiyomizu": ["기요미즈데라", "기요미즈"], "ky_bamboo": ["아라시야마"], "ky_togetsu": ["도게츠교"], "ky_kinkaku": ["금각사", "킨카쿠지"], "ky_ryoan": ["료안지"],
    "fk_station": ["하카타역"], "fk_canal": ["캐널시티"], "fk_yatai": ["야타이"], "fk_dazaifu": ["다자이후"],
    "sp_odori": ["오도리 공원", "오도리공원"], "sp_tvtower": ["TV타워"], "sp_clock": ["시계탑"], "sp_susukino": ["스스키노"], "sp_otaru": ["오타루"],
    "sp_orgel": ["오르골당"],
    "ok_kokusai": ["국제거리"], "ok_shuri": ["슈리성"], "ok_american": ["아메리칸 빌리지", "아메리칸빌리지"], "ok_manzamo": ["만좌모"],
    "ok_churaumi": ["츄라우미"], "ok_kouri": ["고우리"],
    "ng_noritake": ["노리타케"], "ng_sakae": ["사카에"], "ng_osu": ["오스 상점가", "오스칸논"], "ng_castle": ["나고야성"], "ng_nabana": ["나바나노사토"],
    "hd_asaichi": ["아침시장"], "hd_brick": ["붉은벽돌창고", "가네모리"], "hd_motomachi": ["모토마치"], "hd_ropeway": ["하코다테산"],
    "hd_goryokaku": ["고료카쿠"], "hd_yunokawa": ["유노카와"],
    "bp_jigoku": ["지옥 순례", "지옥 온천"], "bp_kannawa": ["칸나와"], "bp_kinrin": ["긴린코"], "bp_yunotsubo": ["유노쓰보"],
    "my_dogo": ["도고온천"], "my_haikara": ["도고 상점가"], "my_castle": ["마쓰야마성"], "my_okaido": ["오카이도"], "my_shimonada": ["시모나다"],
    "kg_tenmonkan": ["덴몬칸"], "kg_shiroyama": ["시로야마"], "kg_sengan": ["센간엔"], "kg_sakurajima": ["사쿠라지마"], "kg_ibusuki": ["이부스키"],
    "sz_sunpu": ["슨푸성"], "sz_nihondaira": ["니혼다이라"], "sz_miho": ["미호노마쓰바라"], "sz_shimizu": ["시미즈항", "시미즈 항"],
    "tm_ritsurin": ["리쓰린"], "tm_naoshima": ["나오시마"], "tm_kotohira": ["고토히라", "곤피라"], "tm_shodo": ["쇼도시마"],
    # 대만·홍콩·마카오·중국
    "tp_101": ["타이베이 101", "타이베이101"], "tp_shilin": ["스린 야시장", "스린야시장"], "tp_palace": ["고궁박물원"],
    "tp_ximen": ["시먼딩"], "tp_tamsui": ["단수이"], "tp_jiufen": ["지우펀"],
    "kh_dome": ["메이리다오", "빛의 돔"], "kh_liuhe": ["리우허"], "kh_pier2": ["보얼예술특구"], "kh_love": ["아이허", "러브 리버"],
    "kh_lotus": ["연지담", "용호탑"],
    "tc_miyahara": ["궁원안과", "미야하라"], "tc_museum": ["국립대만미술관"], "tc_rainbow": ["무지개마을"],
    "tc_gaomei": ["가오메이"], "tc_sunmoon": ["일월담"],
    "hk_avenue": ["스타의 거리", "심포니 오브 라이트"], "hk_ferry": ["스타페리"], "hk_peak": ["빅토리아 피크", "피크트램"], "hk_central": ["센트럴 미드레벨"],
    "hk_ngongping": ["빅부다"],
    "mc_senado": ["세나도"], "mc_stpaul": ["성 바울 성당"], "mc_taipa": ["타이파"], "mc_cotai": ["코타이"], "mc_tower": ["마카오 타워", "마카오타워"],
    "sh_bund": ["와이탄"], "sh_nanjing": ["난징루"], "sh_pearl": ["동방명주"], "sh_yuyuan": ["위위안"], "sh_zhujiajiao": ["주자자오"],
    # 동남아·괌·사이판
    "dn_mykhe": ["미케 해변", "미케비치"], "dn_han": ["한 시장"], "dn_dragon": ["용다리"], "dn_marble": ["오행산"], "dn_bana": ["바나힐", "골든브리지"],
    "dn_hoian": ["호이안"],
    "nt_beach": ["나트랑 해변"], "nt_ponagar": ["포나가르"], "nt_mud": ["머드 온천"], "nt_vin": ["혼째섬"], "nt_hopping": ["혼문섬"],
    "hn_hoankiem": ["호안끼엠"], "hn_36": ["36거리"], "hn_hcm": ["호찌민 묘소"], "hn_halong": ["하롱베이"],
    "hc_post": ["중앙우체국"], "hc_palace": ["통일궁"], "hc_buivien": ["부이비엔"], "hc_cuchi": ["구찌 터널", "구찌터널"],
    "hc_mekong": ["메콩델타", "메콩강"],
    "pq_night": ["즈엉동"], "pq_sunset": ["선셋타운"], "pq_sao": ["사오 해변", "사오비치"],
    "bk_palace": ["왓 프라깨우", "에메랄드 사원"], "bk_watarun": ["왓 아룬", "왓아룬", "새벽 사원"], "bk_khaosan": ["카오산"],
    "bk_siam": ["시암 파라곤", "시암파라곤"], "bk_chatuchak": ["짜뚜짝"], "bk_ayutthaya": ["아유타야"],
    "cm_phrasingh": ["왓 프라싱"], "cm_chediluang": ["체디루앙"], "cm_sunday": ["선데이 마켓", "워킹스트리트"], "cm_nimman": ["님만해민"],
    "cm_doisuthep": ["도이수텝"],
    "cb_santonino": ["산토니뇨"], "cb_moalboal": ["모알보알"],
    "bh_alona": ["알로나"], "bh_balicasag": ["발리카삭"], "bh_loboc": ["로복강"], "bh_tarsier": ["안경원숭이"], "bh_chocolate": ["초콜릿 힐", "초콜릿힐"],
    "cl_freeport": ["클락 프리포트"], "cl_angeles": ["앙헬레스"], "cl_pinatubo": ["피나투보"],
    "sg_mbs": ["마리나베이샌즈", "마리나 베이 샌즈"], "sg_merlion": ["멀라이언"], "sg_gardens": ["가든스 바이 더 베이", "슈퍼트리"],
    "sg_india": ["리틀인디아"], "sg_orchard": ["오차드"], "sg_sentosa": ["센토사"],
    "kl_twin": ["페트로나스", "KLCC"], "kl_bintang": ["부킷빈탕"], "kl_alor": ["잘란알로"], "kl_merdeka": ["메르데카"], "kl_batu": ["바투동굴", "바투 동굴"],
    "kk_aru": ["탄중아루"], "kk_sapi": ["사피섬"], "kk_manukan": ["마누칸"], "kk_kinabalu": ["키나발루산", "키나발루 국립공원"],
    "gm_beach": ["투몬 비치", "투몬비치"], "gm_lovers": ["사랑의 절벽"], "gm_chamorro": ["차모로 빌리지", "차모로빌리지"], "gm_inarajan": ["이나라한"],
    "sn_micro": ["마이크로 비치", "마이크로비치"], "sn_garapan": ["가라판"], "sn_managaha": ["마나가하"], "sn_north": ["만세절벽"],
    # 군산·목포 (2026-11-20)
    "gs_museum": ["근대역사박물관"], "gs_rail": ["철길마을"], "gs_eunpa": ["은파호수"], "gs_market": ["공설시장"], "gs_seonyudo": ["고군산군도", "선유도해수욕장"],
    "mp_cable": ["목포 케이블카", "해상케이블카"], "mp_gohado": ["고하도"], "mp_modern": ["근대역사관"], "mp_market": ["종합수산시장"],
    # 발리·칭다오 (2026-11-20)
    "bl_monkey": ["몽키포레스트"], "bl_tegallalang": ["뜨갈랄랑"], "bl_kelingking": ["누사페니다", "켈링킹"], "bl_uluwatu": ["울루와투"],
    "qd_beer": ["맥주 박물관", "맥주박물관"], "qd_badaguan": ["팔대관"], "qd_pichaiyuan": ["피차위안"], "qd_zhanqiao": ["잔교"], "qd_laoshan": ["라오산"],
    # 속초·대구·히로시마·고베 (2026-11-21 2차)
    "sc_seorak_cable": ["설악케이블카", "권금성"], "sc_abai": ["아바이마을"], "sc_market": ["관광수산시장"],
    "dg_eworld": ["이월드", "83타워"], "dg_kimkwangseok": ["김광석길"], "dg_modern": ["근대골목", "청라언덕"], "dg_palgong": ["팔공산"],
    "hs_peace": ["원폭 돔", "평화기념자료관"], "hs_itsukushima": ["이쓰쿠시마", "이쓰쿠시마신사"], "hs_misen": ["미센"],
    "kb_ijinkan": ["이진칸"], "kb_meriken": ["메리켄파크", "포트타워"], "kb_harborland": ["하버랜드"],
    # 춘천·통영·보라카이·파타야 (2026-11-25)
    "cc_skywalk": ["소양강스카이워크"], "cc_samak_cable": ["삼악산 케이블카", "삼악산케이블카", "호수케이블카"], "cc_dakgalbi": ["명동 닭갈비골목", "명동닭갈비골목"],
    "cc_kimyujeong": ["김유정 문학촌", "김유정역"], "cc_makguksu": ["막국수체험박물관", "막국수 체험박물관"], "cc_soyang_dam": ["소양댐"],
    "ty_cablecar": ["통영 케이블카", "미륵산 케이블카"], "ty_luge": ["통영 루지", "스카이라인 루지"], "ty_dongpirang": ["동피랑"], "ty_jungang": ["통영 중앙시장"],
    "ty_tongjeyoung": ["삼도수군통제영", "세병관"], "ty_yisunsin": ["이순신공원"],
    "br_whitebeach": ["화이트 비치", "화이트비치"], "br_dmall": ["디몰"], "br_puka": ["푸카 비치", "푸카셸 비치"], "br_luho": ["루호 산", "루호산"], "br_crystalcove": ["크리스탈 코브"],
    "pt_kohlarn": ["꼬란", "산호섬"], "pt_nongnooch": ["농눅 빌리지", "농눅빌리지"], "pt_walking": ["파타야 워킹스트리트"], "pt_viewpoint": ["파타야 뷰포인트"],
}
