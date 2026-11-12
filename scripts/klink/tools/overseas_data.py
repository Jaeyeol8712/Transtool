# -*- coding: utf-8 -*-
"""K링크 해외 도시 원본 데이터 (2026-11-12 대표 지시: K링크를 해외여행으로 넓힘, 3D 거리는 준비 중).

장소는 어라운드툴 여행 가이드(travel-<id>.html)의 '지역별 볼거리'에 나온 곳만 넣는다 — 가이드가 K링크의 정보처.
새 해외 가이드를 올리면 여기에 같은 id로 도시를 추가하고 `python3 scripts/klink/tools/build_overseas.py`를 돌린다.

줄 형식 ( | 로 구분, 이름은 ko|zh|en|ja — 비우면 zh는 ja→en, ja는 en으로 채움 )
  C id cc lat lng sub fly | 이름 | 한 줄 소개(ko) | 한 줄 소개(en)          sub: 1=대중교통 촘촘, 0=차·택시 위주 / fly: 인천 출발 비행 분
  A code lat lng apMin | 공항 이름                                           apMin: 공항→도심 이동 분 (가이드의 '이동 시간' 기준)
  S id lat lng | 숙소 권역 이름 | 설명(ko) | 설명(en)
  Z id | 구역 이름(ko) | 구역 이름(en)
  P id cat lat lng h [옵션] | 이름 | 설명(ko) | 설명(en)
     옵션: am·eve·night(가기 좋은 때) / o=A(종일) D(낮 9~17) S(상점 10~21) N(야시장 17~23) M(아침시장 6~14) F(식당 11~21) T(테마파크 9~19)
           lunch·dinner(식사) / x=요일(쉬는 요일, 0=일) / 좌표는 대표 지점의 대략적 위치
운영 시간·요금은 확인된 값이 아니라 일정 계산용 기본값이다. 화면에는 '현지 확인'으로 표시한다(est).
"""

COUNTRIES = {  # cc: [ko, zh, en, ja]
    "jp": ["일본", "日本", "Japan", "日本"], "tw": ["대만", "台湾", "Taiwan", "台湾"], "hk": ["홍콩", "香港", "Hong Kong", "香港"],
    "mo": ["마카오", "澳门", "Macau", "マカオ"], "cn": ["중국", "中国", "China", "中国"], "th": ["태국", "泰国", "Thailand", "タイ"],
    "vn": ["베트남", "越南", "Vietnam", "ベトナム"], "ph": ["필리핀", "菲律宾", "Philippines", "フィリピン"],
    "sg": ["싱가포르", "新加坡", "Singapore", "シンガポール"], "my": ["말레이시아", "马来西亚", "Malaysia", "マレーシア"],
    "gu": ["괌", "关岛", "Guam", "グアム"], "mp": ["사이판", "塞班", "Saipan", "サイパン"],
}
COUNTRY_ORDER = ["jp", "tw", "hk", "mo", "cn", "vn", "th", "ph", "sg", "my", "gu", "mp"]

DATA = r"""
C tokyo jp 35.6812 139.7671 1 150 | 도쿄|东京|Tokyo|東京 | 옛 절과 쇼핑 거리, 도쿄만 야경 | Old temples, shopping streets and bay views
A HND 35.5494 139.7798 30 | 하네다공항|羽田机场|Haneda (HND)|羽田空港
A NRT 35.7720 140.3929 60 | 나리타공항|成田机场|Narita (NRT)|成田空港
S tk_s1 35.7118 139.7800 | 우에노·아사쿠사|上野·浅草|Ueno & Asakusa|上野・浅草 | 우에노역 · 나리타 스카이라이너 | Ueno Stn · Skyliner to Narita
S tk_s2 35.6896 139.7006 | 신주쿠|新宿|Shinjuku|新宿 | 신주쿠역 · JR·지하철 여러 노선 | Shinjuku Stn · JR & subway lines
S tk_s3 35.6740 139.7650 | 도쿄역·긴자|东京站·银座|Tokyo Stn & Ginza|東京駅・銀座 | 도쿄역 · 하네다 이동 편리 | Tokyo Stn · easy for Haneda
Z tk_z1 | 아사쿠사·우에노 | Asakusa & Ueno
P tk_sensoji palace 35.7148 139.7967 1.5 am o=A | 센소지||Senso-ji Temple|浅草寺 | 아사쿠사의 옛 절 · 붉은 가미나리몬이 입구 | Asakusa's old temple behind the red Kaminarimon gate
P tk_nakamise shop 35.7118 139.7964 0.75 | 나카미세 거리||Nakamise Street|仲見世通り | 센소지로 이어지는 기념품·간식 거리 | Souvenir and snack street leading to Senso-ji
P tk_ueno nature 35.7148 139.7745 1.5 | 우에노 공원||Ueno Park|上野公園 | 박물관·동물원이 모인 큰 공원 | Large park with museums and a zoo
Z tk_z2 | 시부야·하라주쿠 | Shibuya & Harajuku
P tk_shibuya shop 35.6595 139.7005 1 eve | 시부야 스크램블 교차로||Shibuya Scramble Crossing|渋谷スクランブル交差点 | 한 번에 수많은 사람이 건너는 교차로 · 쇼핑 거리 | The famous all-way crossing and shopping streets
P tk_meiji palace 35.6764 139.6993 1.25 am o=A | 메이지 신궁||Meiji Shrine|明治神宮 | 숲길 끝에 있는 신사 · 하라주쿠역 옆 | Shrine at the end of a forest path by Harajuku Stn
P tk_takeshita shop 35.6716 139.7031 1 | 다케시타 거리||Takeshita Street|竹下通り | 하라주쿠의 젊은 쇼핑 골목 | Harajuku's youthful shopping lane
Z tk_z3 | 신주쿠 | Shinjuku
P tk_tocho night 35.6896 139.6917 1 night | 도쿄도청 전망실||Tokyo Metropolitan Govt. Observatory|東京都庁展望室 | 도청 건물 전망실에서 보는 시내 야경 | City night view from the government building's deck
P tk_omoide food 35.6929 139.6995 1.25 dinner | 오모이데 요코초||Omoide Yokocho|思い出横丁 | 신주쿠역 옆 작은 술집·꼬치 골목 | Alley of tiny bars and skewer shops by Shinjuku Stn
Z tk_z4 | 오다이바 | Odaiba
P tk_odaiba nature 35.6300 139.7750 1.5 eve | 오다이바 해변공원||Odaiba Seaside Park|お台場海浜公園 | 레인보우 브리지가 보이는 도쿄만 해변 · 쇼핑몰 | Bay-side beach facing Rainbow Bridge, with malls nearby
Z tk_z5 | 근교 | Day trips
P tk_kamakura palace 35.3167 139.5357 3.5 | 가마쿠라 대불||Kamakura Great Buddha|鎌倉大仏 | 가마쿠라 당일치기의 대표 볼거리 | The highlight of a Kamakura day trip
P tk_hakone nature 35.2324 139.1069 5 | 하코네||Hakone|箱根 | 온천과 호수를 도는 당일치기 | Hot springs and lake on a day trip

C osaka jp 34.6937 135.5023 1 110 | 오사카|大阪|Osaka|大阪 | 먹거리 골목과 오사카성, 테마파크 | Food alleys, Osaka Castle and a theme park
A KIX 34.4320 135.2304 50 | 간사이공항|关西机场|Kansai (KIX)|関西空港
S os_s1 34.6664 135.5010 | 난바·신사이바시|难波·心斋桥|Namba & Shinsaibashi|難波・心斎橋 | 난바역 · 공항 난카이선 종점 | Namba Stn · Nankai line from the airport
S os_s2 34.7025 135.4960 | 우메다|梅田|Umeda|梅田 | 오사카역·우메다역 · 교토·고베 이동 편리 | Osaka/Umeda Stn · easy for Kyoto & Kobe
Z os_z1 | 미나미(난바) | Minami (Namba)
P os_dotonbori food 34.6687 135.5013 1.5 eve dinner | 도톤보리||Dotonbori|道頓堀 | 간판과 먹거리가 늘어선 운하 거리 | Canal street lined with signs and street food
P os_shinsaibashi shop 34.6730 135.5010 1.25 | 신사이바시||Shinsaibashi|心斎橋 | 아케이드로 이어진 쇼핑 거리 | Covered arcade shopping street
P os_kuromon food 34.6654 135.5063 1 lunch o=M | 구로몬 시장||Kuromon Market|黒門市場 | 해산물·간식을 사 먹는 시장 | Market for seafood and snacks
P os_shinsekai night 34.6525 135.5063 1.25 eve | 신세카이·츠텐카쿠||Shinsekai & Tsutenkaku|新世界・通天閣 | 옛 분위기 번화가와 전망 타워 · 쿠시카츠 골목 | Retro district with a tower and kushikatsu lane
Z os_z2 | 오사카성·우메다 | Osaka Castle & Umeda
P os_castle palace 34.6873 135.5262 1.5 | 오사카성||Osaka Castle|大阪城 | 천수각과 넓은 성곽 공원 | Castle keep and wide moat-side park
P os_umeda night 34.7053 135.4903 1 night | 우메다 공중정원||Umeda Sky Building|梅田スカイビル | 두 빌딩을 잇는 옥상 전망대 | Rooftop observatory linking two towers
Z os_z3 | 베이 에어리어 | Bay area
P os_usj fun 34.6654 135.4323 7 o=T | 유니버설 스튜디오 재팬||Universal Studios Japan|ユニバーサル・スタジオ・ジャパン | 하루를 통째로 쓰는 테마파크 | Theme park that takes a full day
P os_kaiyukan fun 34.6545 135.4290 2 o=T | 가이유칸(카이유칸)||Osaka Aquarium Kaiyukan|海遊館 | 덴포잔의 대형 수족관 | Large aquarium at Tempozan
Z os_z4 | 근교 | Day trips
P os_nara palace 34.6851 135.8430 4 | 나라 공원·도다이지||Nara Park & Todai-ji|奈良公園・東大寺 | 사슴 공원과 큰 불상의 절 · 전철 당일치기 | Deer park and great-Buddha temple by train

C kyoto jp 35.0116 135.7681 1 110 | 교토|京都|Kyoto|京都 | 절과 신사, 대나무숲의 옛 수도 | Old capital of temples, shrines and bamboo
A KIX 34.4320 135.2304 80 | 간사이공항|关西机场|Kansai (KIX)|関西空港
S ky_s1 34.9858 135.7588 | 교토역|京都站|Kyoto Station|京都駅 | 교토역 · 공항 특급 하루카 | Kyoto Stn · Haruka airport express
S ky_s2 35.0037 135.7700 | 기온·가와라마치|祇园·河原町|Gion & Kawaramachi|祇園・河原町 | 한큐 가와라마치역 · 히가시야마 도보 | Hankyu Kawaramachi · walk to Higashiyama
Z ky_z1 | 히가시야마 | Higashiyama
P ky_kiyomizu palace 34.9949 135.7850 1.5 am | 기요미즈데라||Kiyomizu-dera|清水寺 | 언덕 위 나무 무대로 알려진 절 | Hillside temple known for its wooden stage
P ky_gion palace 35.0037 135.7752 1 eve o=A | 기온||Gion|祇園 | 전통 가옥이 이어지는 거리 | Streets of traditional townhouses
Z ky_z2 | 후시미 | Fushimi
P ky_fushimi palace 34.9671 135.7727 2 am o=A | 후시미 이나리 신사||Fushimi Inari Shrine|伏見稲荷大社 | 붉은 도리이가 이어지는 산길 | Mountain path through rows of red torii gates
Z ky_z3 | 아라시야마 | Arashiyama
P ky_bamboo nature 35.0170 135.6713 1.25 am | 아라시야마 대나무숲||Arashiyama Bamboo Grove|嵐山竹林 | 대나무 사이로 난 산책길 | Walking path through tall bamboo
P ky_togetsu nature 35.0094 135.6778 0.5 | 도게츠교||Togetsukyo Bridge|渡月橋 | 아라시야마 강 위의 다리 | Bridge over the river at Arashiyama
Z ky_z4 | 기타(북쪽) | North Kyoto
P ky_kinkaku palace 35.0394 135.7292 1 | 금각사||Kinkaku-ji|金閣寺 | 연못에 비치는 금빛 누각 | Golden pavilion reflected in a pond
P ky_ryoan palace 35.0345 135.7183 0.75 | 료안지||Ryoan-ji|龍安寺 | 돌 정원으로 알려진 절 | Temple known for its rock garden

C fukuoka jp 33.5902 130.4017 1 80 | 후쿠오카|福冈|Fukuoka|福岡 | 공항이 가까운 쇼핑·포장마차 도시 | Compact city of shopping and food stalls
A FUK 33.5859 130.4507 10 | 후쿠오카공항|福冈机场|Fukuoka (FUK)|福岡空港
S fk_s1 33.5897 130.4207 | 하카타|博多|Hakata|博多 | 하카타역 · 공항 지하철 약 10분 | Hakata Stn · about 10 min by subway from the airport
S fk_s2 33.5914 130.3990 | 텐진|天神|Tenjin|天神 | 텐진역 · 쇼핑·야타이 도보 | Tenjin Stn · walk to shops and food stalls
Z fk_z1 | 하카타 | Hakata
P fk_station shop 33.5897 130.4207 0.75 | 하카타역||Hakata Station|博多駅 | 역 빌딩 쇼핑·식당가 | Station building with shops and restaurants
P fk_canal shop 33.5898 130.4108 1.5 | 캐널시티 하카타||Canal City Hakata|キャナルシティ博多 | 운하가 흐르는 복합 쇼핑몰 | Shopping complex built around a canal
Z fk_z2 | 텐진·나카스 | Tenjin & Nakasu
P fk_tenjin shop 33.5914 130.3990 1 | 텐진 지하상가||Tenjin Underground Mall|天神地下街 | 길게 이어진 지하 쇼핑 거리 | Long underground shopping street
P fk_yatai food 33.5925 130.4055 1.25 eve dinner o=N | 나카스 야타이||Nakasu Yatai Stalls|中洲屋台 | 강변에 늘어서는 저녁 포장마차 | Evening food stalls along the river
Z fk_z3 | 다자이후 | Dazaifu
P fk_dazaifu palace 33.5215 130.5349 2 | 다자이후 텐만구||Dazaifu Tenmangu|太宰府天満宮 | 학문의 신을 모신 신사 · 전철 약 40분 | Shrine of learning, about 40 min by train
Z fk_z4 | 유후인 | Yufuin
P fk_yufuin nature 33.2659 131.3690 4 | 유후인 긴린코||Lake Kinrin, Yufuin|由布院 金鱗湖 | 온천 마을과 호수 · 버스 당일치기 | Hot-spring town and lake on a bus day trip

C sapporo jp 43.0621 141.3544 1 180 | 삿포로|札幌|Sapporo|札幌 | 눈과 라멘, 오타루 운하 | Snow, ramen and the Otaru canal
A CTS 42.7752 141.6923 40 | 신치토세공항|新千岁机场|New Chitose (CTS)|新千歳空港
S sp_s1 43.0687 141.3508 | 삿포로역|札幌站|Sapporo Station|札幌駅 | 삿포로역 · 공항 JR 쾌속 | Sapporo Stn · JR rapid from the airport
S sp_s2 43.0555 141.3535 | 스스키노|薄野|Susukino|すすきの | 스스키노역 · 밤거리 도보 | Susukino Stn · nightlife on foot
Z sp_z1 | 오도리·스스키노 | Odori & Susukino
P sp_odori nature 43.0603 141.3470 0.75 | 오도리 공원||Odori Park|大通公園 | 시내를 가로지르는 공원 · 눈축제 회장 | Park across downtown, the snow festival site
P sp_tvtower night 43.0611 141.3564 0.75 night | 삿포로 TV타워||Sapporo TV Tower|さっぽろテレビ塔 | 오도리 공원을 내려다보는 전망대 | Observation deck over Odori Park
P sp_clock palace 43.0625 141.3537 0.5 | 삿포로 시계탑||Sapporo Clock Tower|札幌市時計台 | 시내의 오래된 목조 시계탑 | Old wooden clock tower downtown
P sp_susukino food 43.0548 141.3535 1.25 eve dinner | 스스키노·라멘 골목||Susukino & Ramen Alley|すすきの・ラーメン横丁 | 밤거리와 라멘집 골목 | Nightlife district with a ramen alley
Z sp_z2 | 모이와산 | Mt. Moiwa
P sp_moiwa night 43.0335 141.3296 1.5 night | 모이와산 로프웨이||Mt. Moiwa Ropeway|藻岩山ロープウェイ | 로프웨이로 올라 보는 삿포로 야경 | Ropeway up to a night view of Sapporo
Z sp_z3 | 오타루 | Otaru
P sp_otaru nature 43.1994 141.0020 2 eve | 오타루 운하||Otaru Canal|小樽運河 | 창고가 늘어선 운하 산책길 · JR 약 30~40분 | Canal lined with warehouses, 30–40 min by JR
P sp_orgel shop 43.1907 141.0079 1 | 오타루 오르골당||Otaru Music Box Museum|小樽オルゴール堂 | 오르골 전시·판매 건물 | Hall selling and showing music boxes

C okinawa jp 26.2124 127.6792 0 140 | 오키나와|冲绳|Okinawa|沖縄 | 바다 드라이브와 수족관 | Coastal drives and the big aquarium
A OKA 26.2064 127.6465 15 | 나하공항|那霸机场|Naha (OKA)|那覇空港
S ok_s1 26.2144 127.6850 | 나하 국제거리|那霸国际通|Naha Kokusai-dori|那覇・国際通り | 모노레일 · 공항 가까움 | Monorail · close to the airport
S ok_s2 26.3165 127.7575 | 차탄(아메리칸 빌리지)|北谷|Chatan|北谷 | 중부 해안 · 렌터카 추천 | Central coast · car recommended
Z ok_z1 | 나하 | Naha
P ok_kokusai shop 26.2153 127.6862 1.5 | 국제거리||Kokusai-dori Street|国際通り | 나하 중심의 쇼핑·식당 거리 | Naha's main street of shops and restaurants
P ok_shuri palace 26.2170 127.7195 1.5 | 슈리성 공원||Shurijo Castle Park|首里城公園 | 류큐 왕국의 성터 공원 | Castle park of the Ryukyu Kingdom
Z ok_z2 | 중부 | Central
P ok_american shop 26.3165 127.7575 2 eve | 아메리칸 빌리지||American Village|アメリカンビレッジ | 바닷가 쇼핑·식당 단지 | Seaside complex of shops and restaurants
P ok_manzamo nature 26.5050 127.8503 0.75 | 만좌모||Cape Manzamo|万座毛 | 코끼리 코 모양 절벽 전망 | Cliff view shaped like an elephant's trunk
Z ok_z3 | 북부 | North
P ok_churaumi fun 26.6943 127.8779 3 o=T | 츄라우미 수족관||Churaumi Aquarium|美ら海水族館 | 큰 수조로 알려진 수족관 · 차 약 2시간 | Aquarium known for its huge tank, about 2 h by car
P ok_kouri nature 26.6936 128.0190 1 | 고우리 대교||Kouri Bridge|古宇利大橋 | 바다 위로 뻗은 다리 드라이브 | Drive across a bridge over clear sea

C nagoya jp 35.1709 136.8815 1 110 | 나고야|名古屋|Nagoya|名古屋 | 성과 상점가, 겨울 조명 | Castle, shopping arcades and winter lights
A NGO 34.8584 136.8054 30 | 주부공항|中部机场|Chubu Centrair (NGO)|中部国際空港
S ng_s1 35.1709 136.8815 | 나고야역|名古屋站|Nagoya Station|名古屋駅 | 나고야역 · 공항 메이테츠 특급 | Nagoya Stn · Meitetsu express from the airport
S ng_s2 35.1700 136.9085 | 사카에|荣|Sakae|栄 | 사카에역 · 쇼핑 도보 | Sakae Stn · shopping on foot
Z ng_z1 | 나고야역 | Nagoya Station
P ng_noritake palace 35.1802 136.8802 1 | 노리타케의 숲||Noritake Garden|ノリタケの森 | 도자기 회사 터에 만든 공원·전시관 | Park and museum on a ceramics maker's site
Z ng_z2 | 사카에·오스 | Sakae & Osu
P ng_sakae shop 35.1709 136.9098 1.5 | 사카에||Sakae|栄 | 백화점과 상점이 모인 번화가 | Downtown of department stores and shops
P ng_osu shop 35.1596 136.9020 1.5 | 오스 상점가||Osu Shopping Street|大須商店街 | 아케이드 상점가와 절 | Covered shopping arcades around a temple
Z ng_z3 | 나고야성 | Nagoya Castle
P ng_castle palace 35.1856 136.8991 1.5 | 나고야성||Nagoya Castle|名古屋城 | 성과 혼마루 궁전 | Castle with the Honmaru Palace
Z ng_z4 | 근교 | Day trips
P ng_nabana night 35.0919 136.6989 2 night | 나바나노사토||Nabana no Sato|なばなの里 | 겨울 조명으로 알려진 꽃 공원 · 버스 | Flower park known for winter illuminations, by bus

C hakodate jp 41.7737 140.7265 1 160 | 하코다테|函馆|Hakodate|函館 | 야경과 아침시장의 항구 도시 | Port city of night views and a morning market
A CTS 42.7752 141.6923 235 | 신치토세공항|新千岁机场|New Chitose (CTS)|新千歳空港
S hd_s1 41.7737 140.7265 | 하코다테역|函馆站|Hakodate Station|函館駅 | 하코다테역 · 아침시장 옆 | Hakodate Stn · next to the morning market
S hd_s2 41.7790 140.7870 | 유노카와 온천|汤之川温泉|Yunokawa Onsen|湯の川温泉 | 온천 숙소 · 노면전차 | Hot-spring inns · tram
Z hd_z1 | 하코다테역·항구 | Station & bay
P hd_asaichi food 41.7727 140.7262 1 am lunch o=M | 하코다테 아침시장||Hakodate Morning Market|函館朝市 | 역 옆 해산물 시장 | Seafood market next to the station
P hd_brick shop 41.7664 140.7166 1.25 | 가네모리 붉은벽돌창고||Kanemori Red Brick Warehouse|金森赤レンガ倉庫 | 항구 창고를 고친 상점가 | Shops in converted harbour warehouses
P hd_motomachi palace 41.7632 140.7126 1 | 모토마치||Motomachi|元町 | 언덕길과 옛 서양식 건물 | Sloping streets with old Western-style buildings
P hd_ropeway night 41.7606 140.7137 1.5 night | 하코다테산 로프웨이||Mt. Hakodate Ropeway|函館山ロープウェイ | 산 위에서 보는 항구 야경 | Harbour night view from the mountain top
Z hd_z2 | 고료카쿠·유노카와 | Goryokaku & Yunokawa
P hd_goryokaku palace 41.7969 140.7570 1.5 | 고료카쿠 공원·타워||Goryokaku Park & Tower|五稜郭公園・タワー | 별 모양 요새와 전망 타워 | Star-shaped fort with a viewing tower
P hd_yunokawa fun 41.7790 140.7870 1.5 eve | 유노카와 온천||Yunokawa Onsen|湯の川温泉 | 공항 가까운 온천 마을 | Hot-spring town near the airport

C beppu jp 33.2796 131.5003 0 80 | 벳푸|别府|Beppu|別府 | 지옥 온천과 유후인 | Hell hot springs and Yufuin
A FUK 33.5859 130.4507 130 | 후쿠오카공항|福冈机场|Fukuoka (FUK)|福岡空港
S bp_s1 33.2796 131.5003 | 벳푸역|别府站|Beppu Station|別府駅 | 벳푸역 · 온천·상점가 도보 | Beppu Stn · baths and arcades on foot
S bp_s2 33.3160 131.4750 | 칸나와 온천|铁轮温泉|Kannawa Onsen|鉄輪温泉 | 온천 마을 · 역에서 버스 약 20분 | Onsen quarter · about 20 min by bus
Z bp_z1 | 칸나와 | Kannawa
P bp_jigoku nature 33.3185 131.4695 2.5 | 벳푸 지옥 온천 순례||Beppu Hells (Jigoku)|別府地獄めぐり | 색이 다른 온천 못을 차례로 둘러보는 코스 | A circuit of vividly coloured hot-spring ponds
P bp_kannawa fun 33.3155 131.4755 1 | 칸나와 온천 마을||Kannawa Onsen Town|鉄輪温泉 | 김이 오르는 골목과 온천 | Steamy lanes and bathhouses
Z bp_z2 | 벳푸역 | Beppu Station
P bp_takegawara fun 33.2766 131.5046 1 | 벳푸역 앞 온천·상점가||Baths & arcades near Beppu Stn|別府駅前 | 역 주변 온천과 상점가 | Bathhouses and arcades around the station
Z bp_z3 | 유후인 | Yufuin
P bp_kinrin nature 33.2659 131.3690 1.5 am | 긴린코 호수||Lake Kinrin|金鱗湖 | 유후인의 작은 호수 · 버스 약 1시간 | Small lake in Yufuin, about 1 h by bus
P bp_yunotsubo shop 33.2653 131.3620 1.5 | 유노쓰보 거리||Yunotsubo Street|湯の坪街道 | 유후인 역에서 호수로 이어지는 상점 거리 | Shop-lined street from Yufuin Stn to the lake

C matsuyama jp 33.8392 132.7657 1 90 | 마쓰야마|松山|Matsuyama|松山 | 도고온천과 언덕 위 성 | Dogo Onsen and a hilltop castle
A MYJ 33.8272 132.6997 20 | 마쓰야마공항|松山机场|Matsuyama (MYJ)|松山空港
S my_s1 33.8400 132.7700 | 오카이도|大街道|Okaido|大街道 | 시내 중심 · 노면전차 | City centre · tram
S my_s2 33.8515 132.7860 | 도고온천|道后温泉|Dogo Onsen|道後温泉 | 온천 숙소 · 노면전차 종점 | Onsen inns · tram terminus
Z my_z1 | 도고 | Dogo
P my_dogo fun 33.8520 132.7864 1.5 eve | 도고온천 본관||Dogo Onsen Honkan|道後温泉本館 | 오래된 목조 온천 건물 | Historic wooden bathhouse
P my_haikara shop 33.8510 132.7850 0.75 | 도고 상점가||Dogo Shopping Arcade|道後商店街 | 온천 앞 기념품·간식 거리 | Souvenir and snack arcade by the bathhouse
Z my_z2 | 시내 | City centre
P my_castle palace 33.8456 132.7655 1.5 | 마쓰야마성||Matsuyama Castle|松山城 | 로프웨이로 오르는 언덕 위 성 | Hilltop castle reached by ropeway
P my_okaido shop 33.8400 132.7700 1 | 오카이도||Okaido Arcade|大街道 | 시내 중심 아케이드 상점가 | Covered shopping arcade downtown
Z my_z3 | 이요시 | Iyo
P my_shimonada nature 33.6617 132.5896 1 eve | 시모나다역||Shimonada Station|下灘駅 | 바다 바로 앞 작은 역 · 차 약 40분 | Tiny station right by the sea, about 40 min by car

C kagoshima jp 31.5966 130.5571 1 100 | 가고시마|鹿儿岛|Kagoshima|鹿児島 | 사쿠라지마 화산과 온천 | Sakurajima volcano and hot springs
A KOJ 31.8034 130.7194 50 | 가고시마공항|鹿儿岛机场|Kagoshima (KOJ)|鹿児島空港
S kg_s1 31.5907 130.5553 | 덴몬칸|天文馆|Tenmonkan|天文館 | 시내 번화가 · 노면전차 | Downtown · tram
S kg_s2 31.5840 130.5410 | 가고시마추오역|鹿儿岛中央站|Kagoshima-Chuo Stn|鹿児島中央駅 | 신칸센·이부스키 열차 | Shinkansen & trains to Ibusuki
Z kg_z1 | 시내 | City centre
P kg_tenmonkan shop 31.5907 130.5553 1.25 | 덴몬칸||Tenmonkan|天文館 | 아케이드 번화가 | Covered downtown arcades
P kg_shiroyama night 31.5975 130.5497 0.75 eve | 시로야마 전망대||Shiroyama Observatory|城山展望台 | 시내와 사쿠라지마가 보이는 전망대 | Lookout over the city and Sakurajima
Z kg_z2 | 이소 | Iso
P kg_sengan palace 31.6177 130.5773 1.5 | 센간엔||Sengan-en Garden|仙巌園 | 사쿠라지마를 바라보는 옛 영주 정원 | Feudal lord's garden facing Sakurajima
Z kg_z3 | 사쿠라지마 | Sakurajima
P kg_sakurajima nature 31.5925 130.6397 3 | 사쿠라지마||Sakurajima|桜島 | 페리 약 15분으로 건너는 활화산 섬 | Active volcano island, about 15 min by ferry
Z kg_z4 | 이부스키 | Ibusuki
P kg_ibusuki fun 31.2278 130.6515 2.5 | 이부스키 모래찜질 온천||Ibusuki Sand Bath|指宿 砂むし温泉 | 따뜻한 모래에 몸을 묻는 온천 · 열차 약 1시간 | Hot-sand bathing, about 1 h by train

C shizuoka jp 34.9716 138.3890 0 120 | 시즈오카|静冈|Shizuoka|静岡 | 후지산이 보이는 바다와 언덕 | Sea and hills with views of Mt. Fuji
A FSZ 34.7960 138.1894 50 | 시즈오카공항|静冈机场|Shizuoka (FSZ)|静岡空港
S sz_s1 34.9716 138.3890 | 시즈오카역|静冈站|Shizuoka Station|静岡駅 | 시즈오카역 · 신칸센 | Shizuoka Stn · Shinkansen
Z sz_z1 | 시내 | City centre
P sz_sunpu palace 34.9790 138.3830 1 | 시즈오카역 주변·슨푸성 공원||Sunpu Castle Park|駿府城公園 | 역에서 걸어가는 성터 공원 | Castle-ruins park within walking distance of the station
Z sz_z2 | 니혼다이라 | Nihondaira
P sz_nihondaira nature 34.9735 138.4639 1.5 am | 니혼다이라||Nihondaira|日本平 | 후지산과 바다가 보이는 언덕 · 로프웨이 | Hilltop with Mt. Fuji and sea views, with a ropeway
Z sz_z3 | 시미즈 | Shimizu
P sz_miho nature 34.9953 138.5247 1.25 am | 미호노마쓰바라||Miho no Matsubara|三保の松原 | 소나무 해변 너머로 보는 후지산 | Mt. Fuji seen across a pine-lined beach
P sz_shimizu shop 35.0090 138.4950 1.5 | 시미즈 항||Shimizu Port|清水港 | 항구 주변 상점·식당가 | Shops and restaurants around the port

C takamatsu jp 34.3401 134.0434 0 90 | 다카마쓰|高松|Takamatsu|高松 | 정원과 예술의 섬 | A grand garden and art islands
A TAK 34.2142 134.0156 40 | 다카마쓰공항|高松机场|Takamatsu (TAK)|高松空港
S tm_s1 34.3507 134.0467 | 다카마쓰역·항구|高松站·港口|Takamatsu Stn & Port|高松駅・高松港 | 역과 페리 터미널 도보 | Station and ferry terminal on foot
Z tm_z1 | 시내 | City centre
P tm_ritsurin nature 34.3297 134.0444 1.5 am | 리쓰린 공원||Ritsurin Garden|栗林公園 | 연못과 소나무가 어우러진 큰 정원 | Large garden of ponds and pines
P tm_arcade shop 34.3445 134.0497 1 | 다카마쓰 상점가||Takamatsu Shopping Arcades|高松中央商店街 | 길게 이어진 아케이드 상점가 | Long covered shopping arcades
Z tm_z2 | 나오시마 | Naoshima
P tm_naoshima fun 34.4586 133.9753 5 | 나오시마||Naoshima|直島 | 미술관과 야외 작품의 섬 · 페리 약 50분~1시간 | Island of museums and outdoor art, 50–60 min by ferry
Z tm_z3 | 고토히라 | Kotohira
P tm_kotohira palace 34.1839 133.8095 3 am | 고토히라궁||Kotohira-gu Shrine|金刀比羅宮 | 긴 돌계단을 오르는 신사 · 전철 약 1시간 | Shrine up a long stone stairway, about 1 h by train
Z tm_z4 | 쇼도시마 | Shodoshima
P tm_shodo nature 34.4720 134.2710 5 | 쇼도시마||Shodoshima|小豆島 | 드라이브로 도는 섬 · 페리 약 1시간 | Island for a scenic drive, about 1 h by ferry

C taipei tw 25.0478 121.5170 1 150 | 타이베이|台北|Taipei|台北 | 야시장과 101, 근교 지우펀 | Night markets, Taipei 101 and Jiufen
A TPE 25.0777 121.2328 40 | 타오위안공항|桃园机场|Taoyuan (TPE)|桃園空港
S tp_s1 25.0478 121.5170 | 타이베이역|台北车站|Taipei Main Station|台北駅 | 공항철도·MRT 환승 | Airport MRT and metro interchange
S tp_s2 25.0421 121.5081 | 시먼딩|西门町|Ximending|西門町 | 시먼역 · 쇼핑 거리 | Ximen Stn · shopping streets
Z tp_z1 | 신이 | Xinyi
P tp_101 night 25.0340 121.5645 1.5 eve | 타이베이 101|台北101|Taipei 101| | 전망대가 있는 초고층 빌딩 | Skyscraper with an observatory
P tp_xiangshan nature 25.0272 121.5746 1.25 eve o=A | 샹산 전망|象山|Xiangshan (Elephant Mountain)| | 계단을 올라 101과 시내를 보는 전망 | Stair climb to a view of Taipei 101
Z tp_z2 | 스린 | Shilin
P tp_shilin food 25.0880 121.5241 1.5 night dinner o=N | 스린 야시장|士林夜市|Shilin Night Market| | 타이베이에서 손꼽히는 큰 야시장 | One of Taipei's biggest night markets
P tp_palace palace 25.1024 121.5485 2.5 | 국립고궁박물원|故宫博物院|National Palace Museum| | 중국 황실 유물을 모은 박물관 | Museum of Chinese imperial collections
Z tp_z3 | 시먼딩 | Ximending
P tp_ximen shop 25.0421 121.5081 1.5 eve | 시먼딩|西门町|Ximending| | 젊은 층이 모이는 쇼핑 거리 | Youthful shopping district
Z tp_z4 | 단수이 | Tamsui
P tp_tamsui nature 25.1689 121.4400 2 eve o=A | 단수이|淡水|Tamsui| | 강변 일몰로 알려진 MRT 종점 | River-mouth sunsets at the end of the MRT
Z tp_z5 | 근교 북동부 | Northeast coast
P tp_jiufen palace 25.1092 121.8443 3 eve o=A | 지우펀|九份|Jiufen| | 홍등이 걸린 산비탈 옛 거리 · 버스 약 1시간 | Hillside old street with red lanterns, about 1 h by bus
P tp_shifen fun 25.0413 121.7754 1.5 | 스펀|十分|Shifen| | 기찻길에서 천등을 날리는 마을 | Village where sky lanterns are released on the tracks
P tp_yehliu nature 25.2063 121.6905 1.5 am | 예류 지질공원|野柳地质公园|Yehliu Geopark| | 바닷가 기암괴석 공원 | Seaside park of unusual rock formations

C kaohsiung tw 22.6273 120.3014 1 180 | 가오슝|高雄|Kaohsiung|高雄 | 항구 예술 거리와 야시장 | Harbour art district and night markets
A KHH 22.5771 120.3500 20 | 가오슝공항|高雄机场|Kaohsiung (KHH)|高雄空港
S kh_s1 22.6316 120.3019 | 메이리다오역|美丽岛站|Formosa Boulevard|美麗島駅 | MRT 환승역 · 야시장 도보 | MRT interchange · walk to the night market
Z kh_z1 | 시내 | City centre
P kh_dome palace 22.6316 120.3019 0.5 | 메이리다오역 빛의 돔|美丽岛站 光之穹顶|Dome of Light, Formosa Blvd Stn| | 역 안의 대형 스테인드글라스 천장 | Huge stained-glass ceiling inside the station
P kh_liuhe food 22.6320 120.2990 1.25 night dinner o=N | 리우허 야시장|六合夜市|Liuhe Night Market| | 메이리다오역 옆 야시장 | Night market beside Formosa Blvd Stn
Z kh_z2 | 항구 | Harbour
P kh_pier2 shop 22.6200 120.2817 1.5 | 보얼예술특구|驳二艺术特区|Pier-2 Art Center| | 창고를 고친 예술 거리 | Art district in converted warehouses
P kh_love night 22.6260 120.2880 1 eve o=A | 아이허(러브 리버)|爱河|Love River| | 저녁 산책하기 좋은 강변 | Riverside for an evening stroll
Z kh_z3 | 치진섬 | Cijin
P kh_cijin nature 22.6130 120.2670 2.5 | 치진섬|旗津|Cijin Island| | 페리 약 10분 · 해변과 해산물 거리 | 10 min by ferry to a beach and seafood street
Z kh_z4 | 연지담 | Lotus Pond
P kh_lotus palace 22.6818 120.2939 1.5 | 연지담 용호탑|莲池潭 龙虎塔|Dragon & Tiger Pagodas, Lotus Pond| | 호수 위 용과 호랑이 탑 | Dragon and tiger pagodas on the lake

C taichung tw 24.1477 120.6736 0 170 | 타이중|台中|Taichung|台中 | 야시장과 무지개마을, 습지 노을 | Night market, Rainbow Village and wetland sunsets
A RMQ 24.2647 120.6210 40 | 타이중공항|台中机场|Taichung (RMQ)|台中空港
S tc_s1 24.1370 120.6850 | 타이중역|台中站|Taichung Station|台中駅 | 타이중역 · 시내 버스·택시 | Taichung Stn · buses and taxis
Z tc_z1 | 시내 | City centre
P tc_miyahara cafe 24.1378 120.6835 0.75 | 궁원안과|宫原眼科|Miyahara| | 옛 안과 건물을 고친 디저트 가게 | Dessert shop in a restored eye-clinic building
P tc_museum palace 24.1410 120.6630 1.5 | 국립대만미술관|国立台湾美术馆|National Taiwan Museum of Fine Arts| | 시내의 큰 미술관 | Major art museum in the city
Z tc_z2 | 펑자 | Fengjia
P tc_fengjia food 24.1790 120.6465 1.5 night dinner o=N | 펑자 야시장|逢甲夜市|Fengjia Night Market| | 타이중의 대표 야시장 | Taichung's best-known night market
Z tc_z3 | 남둔 | Nantun
P tc_rainbow palace 24.1335 120.6100 0.75 | 무지개마을|彩虹眷村|Rainbow Village| | 알록달록한 벽화 마을 | Small village of colourful murals
Z tc_z4 | 근교 | Day trips
P tc_gaomei nature 24.3120 120.5490 2 eve o=A | 가오메이 습지|高美湿地|Gaomei Wetlands| | 풍차와 노을로 알려진 갯벌 | Tidal flats known for windmills and sunsets
P tc_sunmoon nature 23.8650 120.9160 4 | 일월담|日月潭|Sun Moon Lake| | 산속 큰 호수 · 차·버스 1~2시간 | Mountain lake, 1–2 h by car or bus

C hongkong hk 22.2988 114.1722 1 220 | 홍콩|香港|Hong Kong|香港 | 야경과 피크, 야시장 | Harbour lights, the Peak and night markets
A HKG 22.3080 113.9185 30 | 홍콩공항|香港机场|Hong Kong (HKG)|香港空港
S hk_s1 22.2988 114.1722 | 침사추이|尖沙咀|Tsim Sha Tsui|尖沙咀 | MTR 침사추이역 · 야경 도보 | MTR Tsim Sha Tsui · harbour view on foot
S hk_s2 22.2819 114.1580 | 센트럴|中环|Central|セントラル | 공항철도 홍콩역 | Airport Express Hong Kong Stn
Z hk_z1 | 침사추이 | Tsim Sha Tsui
P hk_avenue night 22.2930 114.1740 1 night o=A | 스타의 거리·심포니 오브 라이트|星光大道|Avenue of Stars & Symphony of Lights| | 항구 야경과 저녁 조명 쇼를 보는 산책로 | Promenade for the harbour skyline and evening light show
P hk_ferry fun 22.2937 114.1687 0.5 | 스타페리|天星小轮|Star Ferry| | 침사추이와 센트럴을 잇는 배 · 약 10분 | Ferry between Tsim Sha Tsui and Central, about 10 min
Z hk_z2 | 센트럴 | Central
P hk_peak night 22.2713 114.1500 2 eve | 피크트램·빅토리아 피크|山顶缆车·太平山顶|Peak Tram & Victoria Peak| | 트램으로 올라 보는 홍콩 전경 | Tram ride up to the classic Hong Kong view
P hk_central shop 22.2836 114.1548 1.25 | 센트럴|中环|Central| | 홍콩섬 중심가 · 언덕 골목 | Hong Kong Island's core with hillside lanes
Z hk_z3 | 몽콕 | Mong Kok
P hk_mongkok shop 22.3193 114.1708 1.5 night o=N | 몽콕 야시장|旺角夜市|Mong Kok Night Markets| | 거리 음식과 노점이 모인 야시장 | Night markets with stalls and street food
Z hk_z4 | 란타우 | Lantau
P hk_ngongping palace 22.2540 113.9050 3.5 | 옹핑 케이블카·빅부다|昂坪360·天坛大佛|Ngong Ping 360 & Big Buddha| | 케이블카로 가는 큰 불상 · 공항 가까움 | Cable car to the giant Buddha, near the airport

C macau mo 22.1937 113.5439 0 210 | 마카오|澳门|Macau|マカオ | 옛 광장과 리조트 거리 | Old squares and resort boulevards
A MFM 22.1496 113.5916 15 | 마카오공항|澳门机场|Macau (MFM)|マカオ空港
S mc_s1 22.1900 113.5420 | 마카오 반도|澳门半岛|Macau Peninsula|マカオ半島 | 구시가지 도보 | Old town on foot
S mc_s2 22.1450 113.5620 | 코타이|路氹|Cotai|コタイ | 리조트 · 무료 셔틀 | Resorts · free shuttles
Z mc_z1 | 구시가지 | Old town
P mc_senado palace 22.1936 113.5399 0.75 o=A | 세나도 광장|议事亭前地|Senado Square| | 물결무늬 바닥의 옛 광장 | Old square with wave-pattern paving
P mc_stpaul palace 22.1975 113.5409 0.75 am o=A | 성 바울 성당 유적|大三巴牌坊|Ruins of St. Paul's| | 계단 위에 남은 성당 정면 | Church façade standing atop a stairway
Z mc_z2 | 타이파 | Taipa
P mc_taipa food 22.1530 113.5570 1.25 | 타이파 빌리지|氹仔旧城区|Taipa Village| | 에그타르트와 식당이 있는 옛 골목 | Old lanes with egg tarts and eateries
Z mc_z3 | 코타이 | Cotai
P mc_cotai fun 22.1470 113.5590 2 night o=A | 코타이 리조트|路氹金光大道|Cotai Strip| | 대형 리조트와 공연이 모인 거리 | Boulevard of large resorts and shows
Z mc_z4 | 남쪽 | South
P mc_tower night 22.1797 113.5367 1.25 eve | 마카오 타워|澳门旅游塔|Macau Tower| | 전망대가 있는 타워 | Tower with an observation deck

C shanghai cn 31.2304 121.4737 1 120 | 상하이|上海|Shanghai|上海 | 와이탄 야경과 옛 정원 | The Bund at night and a classical garden
A PVG 31.1443 121.8083 50 | 푸둥공항|浦东机场|Pudong (PVG)|浦東空港
S sh_s1 31.2352 121.4790 | 난징둥루|南京东路|East Nanjing Road|南京東路 | 지하철 난징둥루역 · 와이탄 도보 | Metro East Nanjing Rd · walk to the Bund
Z sh_z1 | 와이탄 | The Bund
P sh_bund night 31.2400 121.4900 1.25 night o=A | 와이탄|外滩|The Bund| | 강 건너 고층 빌딩을 보는 강변 | Riverside facing the skyline across the water
P sh_nanjing shop 31.2352 121.4790 1.25 | 난징루|南京路步行街|Nanjing Road| | 와이탄으로 이어지는 보행자 쇼핑 거리 | Pedestrian shopping street leading to the Bund
Z sh_z2 | 루자쭈이 | Lujiazui
P sh_pearl night 31.2397 121.4998 1.5 eve | 동방명주|东方明珠|Oriental Pearl Tower| | 강 건너편의 전망 타워 | Observation tower across the river
Z sh_z3 | 구시가지 | Old city
P sh_yuyuan palace 31.2270 121.4920 1.5 | 예원·위위안 상가|豫园|Yu Garden & Bazaar| | 옛 정원과 전통 상가 | Classical garden with a traditional bazaar
Z sh_z4 | 근교 | Day trips
P sh_zhujiajiao palace 31.1110 121.0530 3.5 | 주자자오 수향|朱家角|Zhujiajiao Water Town| | 운하가 흐르는 옛 마을 · 차 약 1시간 | Old canal town about 1 h away by car

C danang vn 16.0544 108.2022 0 270 | 다낭|岘港|Da Nang|ダナン | 해변 리조트와 호이안, 바나힐 | Beach resorts, Hoi An and Ba Na Hills
A DAD 16.0439 108.1994 15 | 다낭공항|岘港机场|Da Nang (DAD)|ダナン空港
S dn_s1 16.0600 108.2440 | 미케 해변|美溪海滩|My Khe Beach|ミーケービーチ | 해변 호텔 · 공항 차 약 15분 | Beach hotels · about 15 min from the airport
S dn_s2 16.0680 108.2210 | 한강 주변|汉江|Han River|ハン川 | 시내 · 한시장·용다리 도보 | Downtown · walk to Han Market and Dragon Bridge
Z dn_z1 | 다낭 시내 | Da Nang city
P dn_mykhe nature 16.0600 108.2470 1.5 o=A | 미케 해변||My Khe Beach| | 길게 이어진 시내 해변 | Long city beach
P dn_han shop 16.0683 108.2243 1 | 한 시장||Han Market| | 기념품·건과일을 사는 시장 | Market for souvenirs and dried fruit
P dn_dragon night 16.0612 108.2270 0.75 night o=A | 용다리||Dragon Bridge| | 용 모양 조명 다리 | Bridge shaped like a dragon, lit at night
Z dn_z2 | 오행산 | Marble Mountains
P dn_marble nature 16.0040 108.2630 1.5 am | 오행산||Marble Mountains| | 대리석 산과 동굴 사원 | Marble hills with cave temples
Z dn_z3 | 바나힐 | Ba Na Hills
P dn_bana fun 15.9950 107.9960 6 o=T | 바나힐·골든브리지||Ba Na Hills & Golden Bridge| | 케이블카로 오르는 산 위 테마파크 · 차 약 40분 | Mountain-top park by cable car, about 40 min by car
Z dn_z4 | 호이안 | Hoi An
P dn_hoian palace 15.8770 108.3280 3.5 eve o=A | 호이안 구시가지||Hoi An Ancient Town| | 등불이 켜지는 옛 거리 · 차 약 40분 | Old streets lit by lanterns, about 40 min by car

C nhatrang vn 12.2388 109.1967 0 300 | 나트랑|芽庄|Nha Trang|ニャチャン | 긴 해변과 섬 투어, 머드 온천 | Long beach, island tours and mud baths
A CXR 11.9982 109.2194 40 | 깜라인공항|金兰机场|Cam Ranh (CXR)|カムラン空港
S nt_s1 12.2388 109.1967 | 나트랑 해변 시내|芽庄市区|Nha Trang beachfront|ニャチャン市内 | 해변·야시장 도보 | Beach and night market on foot
Z nt_z1 | 시내 | City
P nt_beach nature 12.2400 109.1970 1.5 o=A | 나트랑 해변||Nha Trang Beach| | 시내 앞 긴 해변 | Long beach in front of the city
P nt_night shop 12.2410 109.1960 1 night o=N | 나트랑 야시장||Nha Trang Night Market| | 해변 옆 저녁 시장 | Evening market by the beach
P nt_ponagar palace 12.2654 109.1955 1 | 포나가르 탑||Po Nagar Towers| | 언덕 위 참파 유적 | Cham-era towers on a hill
Z nt_z2 | 머드 온천 | Mud baths
P nt_mud fun 12.2697 109.1766 2.5 | 머드 온천(탑바)||Thap Ba Mud Baths| | 진흙 온천과 온수 풀 · 차 약 15~20분 | Mud baths and warm pools, 15–20 min by car
Z nt_z3 | 섬 | Islands
P nt_vin fun 12.2190 109.2430 6 o=T | 빈원더스(혼째섬)||VinWonders (Hon Tre)| | 케이블카·배로 가는 섬 놀이공원 | Island theme park by cable car or boat
P nt_hopping nature 12.1680 109.3050 5 am | 호핑투어(혼문섬)||Island hopping (Hon Mun)| | 배로 도는 스노클링 투어 | Snorkelling tour by boat

C hanoi vn 21.0285 105.8542 0 280 | 하노이|河内|Hanoi|ハノイ | 호수와 구시가지, 근교 절경 | Lakes, the Old Quarter and karst scenery
A HAN 21.2212 105.8072 40 | 노이바이공항|内排机场|Noi Bai (HAN)|ノイバイ空港
S hn_s1 21.0320 105.8520 | 구시가지|老城区|Old Quarter|旧市街 | 호안끼엠 호수 도보 | Walk to Hoan Kiem Lake
Z hn_z1 | 구시가지 | Old Quarter
P hn_hoankiem nature 21.0287 105.8524 1 o=A | 호안끼엠 호수||Hoan Kiem Lake| | 구시가지 한가운데 호수 | Lake at the heart of the Old Quarter
P hn_36 shop 21.0340 105.8500 1.5 | 36거리||Old Quarter (36 Streets)| | 가게와 음식점이 빼곡한 옛 거리 | Dense old streets of shops and eateries
Z hn_z2 | 시내 | City
P hn_temple palace 21.0294 105.8355 1 | 문묘||Temple of Literature| | 베트남 최초의 대학 터 | Site of Vietnam's first university
P hn_hcm palace 21.0369 105.8346 1 am | 호찌민 묘소||Ho Chi Minh Mausoleum| | 바딘 광장의 묘소 | Mausoleum on Ba Dinh Square
Z hn_z3 | 닌빈 | Ninh Binh
P hn_trangan nature 20.2527 105.9150 5 | 닌빈 짱안||Trang An, Ninh Binh| | 나룻배로 도는 석회암 절경 · 차 약 2시간 | Boat ride through karst scenery, about 2 h by car
Z hn_z4 | 하롱베이 | Ha Long Bay
P hn_halong nature 20.9101 107.1839 6 | 하롱베이||Ha Long Bay| | 섬 사이를 도는 크루즈 · 차 약 2시간 30분 | Cruise among limestone islands, about 2.5 h by car

C hochiminh vn 10.7769 106.7009 0 330 | 호치민|胡志明市|Ho Chi Minh City|ホーチミン | 시장과 프랑스풍 건물, 근교 투어 | Markets, colonial buildings and day tours
A SGN 10.8188 106.6520 40 | 떤선녓공항|新山一机场|Tan Son Nhat (SGN)|タンソンニャット空港
S hc_s1 10.7750 106.7000 | 1군|第一郡|District 1|1区 | 주요 볼거리 도보 | Main sights on foot
Z hc_z1 | 1군 | District 1
P hc_benthanh shop 10.7725 106.6980 1 | 벤탄 시장||Ben Thanh Market| | 기념품과 먹거리 시장 | Market for souvenirs and food
P hc_post palace 10.7799 106.6999 0.5 | 중앙우체국||Central Post Office| | 프랑스풍 옛 우체국 건물 | French-colonial post office building
P hc_palace palace 10.7770 106.6953 1.25 | 통일궁||Independence Palace| | 옛 대통령궁 | Former presidential palace
P hc_buivien night 10.7674 106.6940 1.5 night o=A | 부이비엔 거리||Bui Vien Street| | 여행자가 모이는 밤 거리 | Backpacker street that fills up at night
Z hc_z2 | 구찌 | Cu Chi
P hc_cuchi palace 11.1410 106.4620 3 | 구찌 터널||Cu Chi Tunnels| | 전쟁 때 쓰인 땅굴 유적 · 차 약 1시간 30분 | Wartime tunnel network, about 1.5 h by car
Z hc_z3 | 메콩델타 | Mekong Delta
P hc_mekong nature 10.3600 106.3600 5 | 메콩델타 보트 투어||Mekong Delta boat tour| | 강과 수로를 도는 투어 · 차 약 2시간 | Tour by boat on the river and canals, about 2 h by car

C phuquoc vn 10.2170 103.9590 0 330 | 푸꾸옥|富国岛|Phu Quoc|フーコック | 케이블카와 해변, 야시장 | Cable car, beaches and a night market
A PQC 10.1698 103.9931 15 | 푸꾸옥공항|富国机场|Phu Quoc (PQC)|フーコック空港
S pq_s1 10.2000 103.9630 | 즈엉동|阳东|Duong Dong|ズオンドン | 야시장 · 공항 차 약 15분 | Night market · about 15 min from the airport
S pq_s2 10.0330 104.0020 | 남부(선셋타운)|南部|South (Sunset Town)|南部 | 케이블카 가까움 | Close to the cable car
Z pq_z1 | 즈엉동 | Duong Dong
P pq_night food 10.2135 103.9605 1.25 night dinner o=N | 즈엉동 야시장||Duong Dong Night Market| | 해산물과 간식이 모인 야시장 | Night market of seafood and snacks
Z pq_z2 | 남부 | South
P pq_cable fun 10.0280 104.0060 4 o=T | 혼텀 케이블카||Hon Thom Cable Car| | 바다 위를 건너는 케이블카 · 차 약 30분 | Cable car across the sea, about 30 min by car
P pq_sunset night 10.0330 104.0020 1.5 eve o=A | 선셋타운||Sunset Town| | 노을을 보는 남부 해안 마을 | Seaside quarter for watching the sunset
Z pq_z3 | 동쪽 | East
P pq_sao nature 10.0540 104.0370 2.5 o=A | 사오 해변||Sao Beach| | 흰 모래 해변 | White-sand beach
Z pq_z4 | 북부 | North
P pq_vin fun 10.3370 103.8560 6 o=T | 빈원더스·사파리||VinWonders & Safari| | 놀이공원과 사파리 · 차 약 1시간 | Theme park and safari, about 1 h by car

C bangkok th 13.7466 100.5347 1 360 | 방콕|曼谷|Bangkok|バンコク | 왕궁과 사원, 쇼핑과 야경 | Palace, temples, malls and rooftops
A BKK 13.6900 100.7501 35 | 수완나품공항|素万那普机场|Suvarnabhumi (BKK)|スワンナプーム空港
S bk_s1 13.7466 100.5347 | 시암|暹罗|Siam|サイアム | BTS 시암역 · 쇼핑몰 도보 | BTS Siam · malls on foot
S bk_s2 13.7370 100.5600 | 아속·수쿰윗|素坤逸|Asok & Sukhumvit|アソーク | BTS·MRT 환승 | BTS & MRT interchange
Z bk_z1 | 구시가지 | Old city
P bk_palace palace 13.7500 100.4913 2 am | 왕궁·왓 프라깨우||Grand Palace & Wat Phra Kaew| | 방콕의 대표 궁전과 사원 · 복장 규정 확인 | Bangkok's signature palace and temple; check the dress code
P bk_watpho palace 13.7465 100.4927 1 | 왓 포||Wat Pho| | 누워 있는 큰 불상의 사원 | Temple of the reclining Buddha
P bk_watarun palace 13.7437 100.4889 1 eve | 왓 아룬||Wat Arun| | 강 건너 탑이 솟은 사원 | Riverside temple with a tall spire
Z bk_z2 | 카오산 | Khao San
P bk_khaosan night 13.7589 100.4974 1.25 night o=A | 카오산 로드||Khao San Road| | 여행자가 모이는 밤 거리 | Travellers' street that comes alive at night
Z bk_z3 | 시암·아속 | Siam & Asok
P bk_siam shop 13.7462 100.5347 2 | 시암 쇼핑몰||Siam shopping malls| | BTS로 이어진 대형 쇼핑몰 | Large malls linked by the BTS
Z bk_z4 | 짜뚜짝 | Chatuchak
P bk_chatuchak shop 13.7999 100.5500 2 am x=1,2,3,4,5 | 짜뚜짝 주말시장||Chatuchak Weekend Market| | 주말에 여는 큰 시장 | Huge market open on weekends
Z bk_z5 | 근교 | Day trips
P bk_ayutthaya palace 14.3560 100.5680 4 | 아유타야 유적||Ayutthaya ruins| | 옛 수도의 사원 유적 · 약 1시간 30분 | Temple ruins of the old capital, about 1.5 h away

C chiangmai th 18.7883 98.9853 0 360 | 치앙마이|清迈|Chiang Mai|チェンマイ | 사원과 카페, 일요 야시장 | Temples, cafés and the Sunday market
A CNX 18.7668 98.9626 15 | 치앙마이공항|清迈机场|Chiang Mai (CNX)|チェンマイ空港
S cm_s1 18.7883 98.9853 | 올드시티|古城|Old City|旧市街 | 사원 도보 | Temples on foot
S cm_s2 18.7997 98.9680 | 님만해민|宁曼路|Nimman|ニマンヘミン | 카페·쇼핑 거리 | Cafés and shopping
Z cm_z1 | 올드시티 | Old City
P cm_phrasingh palace 18.7885 98.9817 0.75 | 왓 프라싱||Wat Phra Singh| | 올드시티의 대표 사원 | The Old City's best-known temple
P cm_chediluang palace 18.7869 98.9865 0.75 | 왓 체디루앙||Wat Chedi Luang| | 큰 벽돌 탑이 남은 사원 | Temple with a massive brick chedi
P cm_sunday shop 18.7877 98.9932 1.5 night o=N x=1,2,3,4,5,6 | 일요 워킹스트리트||Sunday Walking Street| | 일요일 저녁 올드시티 야시장 | Sunday-evening market in the Old City
Z cm_z2 | 님만해민 | Nimman
P cm_nimman cafe 18.7997 98.9680 1.5 | 님만해민||Nimmanhaemin| | 카페와 가게가 모인 동네 | Neighbourhood of cafés and shops
Z cm_z3 | 도이수텝 | Doi Suthep
P cm_doisuthep palace 18.8049 98.9216 2 am | 왓 프라탓 도이수텝||Wat Phra That Doi Suthep| | 산 위 황금 탑 사원 · 차 약 30분 | Golden hilltop temple, about 30 min by car

C cebu ph 10.3000 123.9300 0 270 | 세부|宿务|Cebu|セブ | 리조트와 호핑, 성당 | Resorts, island hopping and an old basilica
A CEB 10.3075 123.9794 20 | 막탄세부공항|麦克坦宿务机场|Mactan–Cebu (CEB)|マクタン・セブ空港
S cb_s1 10.3000 124.0050 | 막탄|麦克坦|Mactan|マクタン | 리조트 · 공항 가까움 | Resorts · close to the airport
S cb_s2 10.3100 123.8930 | 세부시티|宿务市|Cebu City|セブシティ | 시내 쇼핑몰·성당 | Malls and churches downtown
Z cb_z1 | 막탄 | Mactan
P cb_mactan nature 10.3090 124.0130 4 am | 막탄 호핑 투어||Mactan island hopping| | 배로 나가는 스노클링 투어 | Snorkelling trip by boat
Z cb_z2 | 세부시티 | Cebu City
P cb_santonino palace 10.2942 123.9021 0.75 | 산토니뇨 성당||Basilica del Santo Niño| | 세부에서 가장 오래된 성당 | Cebu's oldest church
Z cb_z3 | 모알보알 | Moalboal
P cb_moalboal nature 9.9520 123.3680 5 | 모알보알||Moalboal| | 정어리 떼 스노클링 · 차 약 3시간 | Snorkelling with sardine shoals, about 3 h by car

C bohol ph 9.5500 123.7700 0 285 | 보홀|薄荷岛|Bohol|ボホール | 해변과 초콜릿 힐, 안경원숭이 | Beaches, Chocolate Hills and tarsiers
A TAG 9.5731 123.7750 15 | 보홀팡라오공항|薄荷邦劳机场|Bohol–Panglao (TAG)|ボホール・パングラオ空港
S bh_s1 9.5490 123.7730 | 알로나 해변|阿罗娜海滩|Alona Beach|アロナビーチ | 리조트 · 공항 차 약 15분 | Resorts · about 15 min from the airport
Z bh_z1 | 팡라오 | Panglao
P bh_alona nature 9.5487 123.7735 2 o=A | 알로나 해변||Alona Beach| | 팡라오의 중심 해변 | Panglao's main beach
P bh_balicasag nature 9.5170 123.6830 5 am | 발리카삭 호핑||Balicasag island hopping| | 배 약 30~40분 · 스노클링 | Snorkelling, 30–40 min by boat
Z bh_z2 | 로복 | Loboc
P bh_loboc fun 9.6360 124.0310 1.5 lunch | 로복강||Loboc River| | 강을 따라 가는 배 투어 | Boat tour along the river
P bh_tarsier nature 9.6650 124.0170 1 | 안경원숭이 보호구역||Tarsier sanctuary| | 작은 안경원숭이를 보는 보호구역 | Sanctuary for tiny tarsiers
Z bh_z3 | 내륙 | Inland
P bh_chocolate nature 9.7986 124.1672 1.5 | 초콜릿 힐||Chocolate Hills| | 둥근 언덕이 이어지는 전망 · 차 약 1시간 30분~2시간 | View over rows of rounded hills, 1.5–2 h by car

C clark ph 15.1850 120.5600 0 240 | 클락|克拉克|Clark|クラーク | 리조트와 화산 트레킹 | Resorts and a volcano trek
A CRK 15.1860 120.5603 15 | 클락공항|克拉克机场|Clark (CRK)|クラーク空港
S cl_s1 15.1830 120.5350 | 클락 프리포트|克拉克自由港|Clark Freeport|クラーク・フリーポート | 리조트 · 공항 차 약 10~20분 | Resorts · 10–20 min from the airport
Z cl_z1 | 클락·앙헬레스 | Clark & Angeles
P cl_freeport nature 15.1830 120.5350 2 | 클락 프리포트||Clark Freeport Zone| | 리조트와 골프장이 모인 구역 | Zone of resorts and golf courses
P cl_angeles food 15.1450 120.5880 1.5 dinner | 앙헬레스 시내||Angeles City| | 시내 식당가 · 차 약 15분 | Downtown restaurants, about 15 min by car
Z cl_z2 | 피나투보 | Pinatubo
P cl_pinatubo nature 15.1430 120.3500 7 am | 피나투보 화산||Mt. Pinatubo| | 분화구 호수 트레킹 · 차·4x4 약 2시간 | Crater-lake trek, about 2 h by car and 4x4
Z cl_z3 | 수빅 | Subic
P cl_subic nature 14.8200 120.2830 4 | 수빅||Subic Bay| | 해변과 프리포트 · 차 약 1시간 | Beach and freeport, about 1 h by car

C singapore sg 1.2903 103.8520 1 390 | 싱가포르|新加坡|Singapore|シンガポール | 마리나베이 야경과 정원, 센토사 | Marina Bay lights, gardens and Sentosa
A SIN 1.3644 103.9915 35 | 창이공항|樟宜机场|Changi (SIN)|チャンギ空港
S sg_s1 1.2850 103.8540 | 마리나베이|滨海湾|Marina Bay|マリーナベイ | MRT · 야경 도보 | MRT · night views on foot
S sg_s2 1.3040 103.8320 | 오차드|乌节路|Orchard|オーチャード | MRT 오차드역 · 쇼핑 | MRT Orchard · shopping
Z sg_z1 | 마리나베이 | Marina Bay
P sg_mbs night 1.2834 103.8607 1.5 night | 마리나베이샌즈|滨海湾金沙|Marina Bay Sands| | 옥상 전망대가 있는 호텔·쇼핑몰 | Hotel and mall with a rooftop deck
P sg_merlion nature 1.2868 103.8545 0.5 o=A | 멀라이언 공원|鱼尾狮公园|Merlion Park| | 멀라이언 상과 마리나베이 전망 | Merlion statue with a Marina Bay view
P sg_gardens nature 1.2816 103.8636 2 eve | 가든스 바이 더 베이|滨海湾花园|Gardens by the Bay| | 슈퍼트리와 온실 · 저녁 조명 쇼 | Supertrees and conservatories with an evening light show
Z sg_z2 | 차이나타운·리틀인디아 | Chinatown & Little India
P sg_chinatown food 1.2836 103.8443 1.5 lunch | 차이나타운|牛车水|Chinatown| | 사원과 호커센터가 있는 거리 | Temples and hawker centres
P sg_india palace 1.3066 103.8518 1 | 리틀인디아|小印度|Little India| | 인도 문화 거리 | Indian cultural quarter
Z sg_z3 | 오차드 | Orchard
P sg_orchard shop 1.3040 103.8320 1.5 | 오차드 로드|乌节路|Orchard Road| | 쇼핑몰이 이어진 거리 | Avenue of shopping malls
Z sg_z4 | 센토사 | Sentosa
P sg_sentosa fun 1.2494 103.8303 6 o=T | 센토사|圣淘沙|Sentosa| | 해변과 테마파크가 있는 섬 | Island of beaches and theme parks

C kualalumpur my 3.1516 101.7110 1 390 | 쿠알라룸푸르|吉隆坡|Kuala Lumpur|クアラルンプール | 트윈타워와 야시장, 바투동굴 | Twin Towers, a food street and Batu Caves
A KUL 2.7456 101.7099 30 | 쿠알라룸푸르공항|吉隆坡机场|Kuala Lumpur (KUL)|クアラルンプール空港
S kl_s1 3.1466 101.7113 | 부킷빈탕|武吉免登|Bukit Bintang|ブキッビンタン | 쇼핑·야시장 도보 | Shopping and food street on foot
S kl_s2 3.1579 101.7116 | KLCC|KLCC|KLCC|KLCC | 트윈타워 옆 | Beside the Twin Towers
Z kl_z1 | KLCC | KLCC
P kl_twin night 3.1579 101.7116 1.5 eve | 페트로나스 트윈타워·KLCC 공원|双子塔|Petronas Twin Towers & KLCC Park| | 쌍둥이 빌딩과 그 앞 공원 | The twin skyscrapers and the park below
Z kl_z2 | 부킷빈탕 | Bukit Bintang
P kl_bintang shop 3.1466 101.7113 1.5 | 부킷빈탕|武吉免登|Bukit Bintang| | 쇼핑몰이 모인 번화가 | Downtown of shopping malls
P kl_alor food 3.1458 101.7085 1.25 night dinner o=N | 잘란알로 야시장|亚罗街|Jalan Alor| | 저녁에 열리는 먹거리 거리 | Street-food strip that opens in the evening
Z kl_z3 | 올드타운 | Old town
P kl_merdeka palace 3.1478 101.6935 0.75 o=A | 메르데카 광장|独立广场|Merdeka Square| | 독립 광장과 옛 건물 | Independence Square and colonial buildings
P kl_chinatown shop 3.1440 101.6975 1 | 차이나타운|茨厂街|Chinatown (Petaling Street)| | 노점이 늘어선 시장 거리 | Market street lined with stalls
Z kl_z4 | 근교 | Day trips
P kl_batu palace 3.2379 101.6840 1.5 am | 바투동굴|黑风洞|Batu Caves| | 큰 계단과 동굴 사원 · 차 약 30분 | Cave temple up a long stairway, about 30 min by car

C kotakinabalu my 5.9804 116.0735 0 300 | 코타키나발루|亚庇|Kota Kinabalu|コタキナバル | 노을 해변과 섬, 키나발루 | Sunset beach, islands and Mt. Kinabalu
A BKI 5.9372 116.0512 15 | 코타키나발루공항|亚庇机场|Kota Kinabalu (BKI)|コタキナバル空港
S kk_s1 5.9790 116.0720 | 시내 워터프런트|市区海滨|Waterfront|ウォーターフロント | 야시장·선착장 도보 | Night market and jetty on foot
Z kk_z1 | 시내 | City
P kk_waterfront food 5.9795 116.0705 1.25 night dinner o=N | 워터프런트·야시장||Waterfront & night market| | 바닷가 식당가와 저녁 시장 | Seaside restaurants and an evening market
Z kk_z2 | 탄중아루 | Tanjung Aru
P kk_aru nature 5.9460 116.0460 1.5 eve o=A | 탄중아루 해변||Tanjung Aru Beach| | 노을로 알려진 해변 · 차 약 15분 | Beach known for sunsets, about 15 min by car
Z kk_z3 | 해양공원 | Marine park
P kk_sapi nature 6.0090 116.0040 3 am | 사피섬||Sapi Island| | 배 약 15~20분 · 스노클링 | Snorkelling, 15–20 min by boat
P kk_manukan nature 5.9730 116.0020 3 am | 마누칸섬||Manukan Island| | 해양공원의 해변 섬 | Beach island in the marine park
Z kk_z4 | 키나발루 | Kinabalu
P kk_kinabalu nature 6.0060 116.5420 4 | 키나발루 국립공원||Kinabalu Park| | 산기슭 국립공원 · 차 약 2시간 | National park at the mountain's foot, about 2 h by car

C guam gu 13.5120 144.8030 0 270 | 괌|关岛|Guam|グアム | 투몬 해변과 쇼핑, 남부 드라이브 | Tumon beach, shopping and a southern drive
A GUM 13.4834 144.7960 15 | 괌공항|关岛机场|Guam (GUM)|グアム空港
S gm_s1 13.5120 144.8030 | 투몬|杜梦湾|Tumon|タモン | 호텔 지구 · 공항 차 약 15분 | Hotel district · about 15 min from the airport
Z gm_z1 | 투몬 | Tumon
P gm_beach nature 13.5130 144.8040 2 o=A | 투몬 비치||Tumon Beach| | 호텔 앞 얕은 해변 | Shallow beach in front of the hotels
P gm_shop shop 13.5146 144.8055 1.5 | 투몬 쇼핑몰||Tumon shopping| | 호텔 지구의 쇼핑몰 | Malls in the hotel district
Z gm_z2 | 북부 | North
P gm_lovers nature 13.5350 144.8020 0.75 eve | 사랑의 절벽||Two Lovers Point| | 바다를 내려다보는 절벽 전망대 | Clifftop lookout over the sea
Z gm_z3 | 하갓냐 | Hagatna
P gm_chamorro food 13.4770 144.7530 1.5 night dinner o=N x=0,1,2,4,5,6 | 차모로 빌리지 야시장||Chamorro Village Night Market| | 보통 수요일 저녁에 열리는 야시장 | Night market usually held on Wednesday evenings
Z gm_z4 | 남부 | South
P gm_inarajan nature 13.2730 144.7480 1.5 | 이나라한 자연 풀||Inarajan Natural Pool| | 바위로 둘러싸인 천연 수영장 · 차 약 1시간 | Rock-enclosed natural pool, about 1 h by car

C saipan mp 15.2130 145.7200 0 270 | 사이판|塞班|Saipan|サイパン | 맑은 바다와 마나가하섬 | Clear water and Managaha Island
A SPN 15.1190 145.7290 20 | 사이판공항|塞班机场|Saipan (SPN)|サイパン空港
S sn_s1 15.2130 145.7200 | 가라판|加拉班|Garapan|ガラパン | 시내 · 공항 차 약 20분 | Town centre · about 20 min from the airport
Z sn_z1 | 가라판 | Garapan
P sn_micro nature 15.2190 145.7170 1.5 eve o=A | 마이크로 비치||Micro Beach| | 가라판 앞 얕은 해변 | Shallow beach in front of Garapan
P sn_garapan shop 15.2125 145.7190 1 | 가라판 시내||Garapan| | 식당과 상점이 모인 시내 | Town centre of restaurants and shops
Z sn_z2 | 마나가하섬 | Managaha
P sn_managaha nature 15.2410 145.7130 4 am | 마나가하섬||Managaha Island| | 배 약 15분 · 스노클링 해변 | Snorkelling beach, about 15 min by boat
Z sn_z3 | 북부 | North
P sn_north nature 15.2853 145.8156 2 | 북부(만세절벽·새섬·그로토)||North coast (Banzai Cliff, Bird Island, Grotto)| | 차로 도는 북부 해안 전망 · 약 30분 | Coastal lookouts on a northern drive, about 30 min away
"""
