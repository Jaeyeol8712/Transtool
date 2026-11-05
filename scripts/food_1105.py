# -*- coding: utf-8 -*-
"""2026-11-03 대표 지시: 겨울에 많이 찾는 메뉴별 서울 미쉐린 빕 구르망 10곳 묶음. 자료는 food_1103.R (2026-11-03 미쉐린 공식 페이지 확인분)."""
import os
from food_1103 import page

P = [
 ("mandu", "만두·만둣국", "겨울 만두·만둣국", "만두는 겨울·설 음식입니다. <strong>개성·평안도식 만둣국</strong>부터 손만두까지 6곳.", ["gaeseong-mandu-koong", "jaha-son-mandu", "hwangsaengga-kalguksu", "andeok", "mipildam", "mandujip"]),
 ("gomtang", "곰탕·설렁탕", "곰탕·설렁탕", "추운 날 뜨끈한 <strong>곰탕·설렁탕·도가니탕</strong> 6곳.", ["mapo-ok", "hapjeongok", "gomtang-lab", "neungdong-minari", "daesungjip", "kyewol-gomtang"]),
 ("gukbap", "국밥·탕", "국밥·추어탕·삼계탕", "<strong>돼지국밥·추어탕·삼계탕</strong> 등 국물 한 그릇 5곳.", ["anam", "okdongsik", "yonggeumok", "3rd-samgyetang", "oilje"]),
 ("naengmyeon", "평양냉면·막국수", "평양냉면·막국수", "냉면은 본래 겨울 음식(『동국세시기』 11월 조). <strong>평양냉면·막국수</strong> 4곳.", ["woo-lae-oak", "pildong-myeonok", "jungin-myeonok", "yangyang-memil-makguksu"]),
 ("memil", "메밀국수·소바", "메밀국수·소바", "<strong>메밀국수·순메밀·소바</strong> 5곳. 따뜻한 국물 메뉴가 있는지 확인하고 갑니다.", ["yurimmyeon", "seoryung", "mijin", "subaru", "sobakeeri-suzu"]),
 ("kalguksu", "칼국수·수제비", "칼국수·수제비", "겨울에 찾는 <strong>칼국수·수제비·자가제면 국수</strong> 4곳.", ["hwangsaengga-kalguksu", "limbyungjoo-sandong-kalguksu", "samcheongdong-sujebi", "myeon-seoul"]),
 ("yearend-gogi", "송년회 고기·족발", "송년회 고기·족발", "연말 모임에 많이 찾는 <strong>고기 구이·불고기·족발</strong> 4곳.", ["geumdwaeji-sikdang", "ggupdang", "yukjeon-hoekwan", "halmaejip"]),
 ("vegan", "채식·비건", "채식·비건", "연말 모임에 채식하는 사람이 있을 때 <strong>비건·채식 한식·두부</strong> 4곳.", ["gosari-express", "alt-a", "base-is-nice", "hwanggeum-kongbat"]),
 ("asian", "연말 모임 이국 요리", "타이·중식·타코", "연말 모임용 <strong>타이·중식·멕시칸</strong> 4곳.", ["horapa", "youhan", "jin-jin", "mattdol"]),
 ("hansik", "게장·한식 밥상", "게장·한식 밥상", "<strong>간장게장·들깨 미역국 백반·바싹불고기</strong> 등 한식 밥상 4곳.", ["gebang-sikdang", "hwa-hae-dang", "oilje", "yukjeon-hoekwan"]),
]

PAGES_1105 = [dict(file=f"seoul-winter-{s}.html", region="서울특별시", gu="겨울 메뉴", tag=tag,
                   eyebrow=f"서울 · 겨울에 찾는 {eb} · 미쉐린 빕 구르망",
                   h1=f"서울 {eb}<br/>빕 구르망 {len(keys)}곳", lede=lede, keys=keys)
              for s, tag, eb, lede, keys in P]


def make(style_path):
    style = open(style_path, encoding="utf-8").read()
    for p in PAGES_1105:
        if not os.path.exists(p["file"]):
            open(p["file"], "w", encoding="utf-8").write(page(p, style))
