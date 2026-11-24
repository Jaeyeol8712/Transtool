# -*- coding: utf-8 -*-
"""2026-11-25 매일 콘텐츠 15개 (대표 지시 2026-11-21 21:16, SEO 원칙 2026-11-25).
- 새 지역: 춘천·통영(국내), 보라카이·파타야(해외). 글: chuncheon·tongyeong(여행·맛집 4), boracay.GUIDE(가이드 1)
- 기존 지역: dom(전주·한라산 영실·강릉 맛집), ov(도고온천·사쿠라지마·나고야 맛집), pattaya.GUIDE(코타키나발루 공항), 계산기 3(scripts/calc_1125.py)
- 꿀팁 채우기 30곳: tips_a·tips_b
- make() 는 파일이 없을 때 한 번만 만든다(이후 build.py 가 공통 영역을 다시 씀). 기존 글 제목·URL은 건드리지 않는다.
"""
import html
import re
import json
import os

from . import chuncheon, tongyeong, boracay, pattaya, dom, ov, tips_a, tips_b

D = "2026-11-25"
CHK = "2026년 11월 25일 확인"
MODS = [chuncheon, tongyeong, dom, ov]
ARTICLES = [a for m in MODS for a in m.ARTICLES]
SPOTS_1125 = {k: v for m in (tips_a, tips_b, chuncheon, tongyeong, boracay, pattaya) for k, v in m.SPOTS.items()}
GUIDES_1125 = [boracay.GUIDE, pattaya.GUIDE]

OVERSEAS = {"matsuyama", "kagoshima", "nagoya"}
RNAME = {"chuncheon": "춘천", "tongyeong": "통영", "jeonju": "전주", "jeju": "제주", "gangneung": "강릉",
         "matsuyama": "마쓰야마", "kagoshima": "가고시마", "nagoya": "나고야"}


def kind_of(a):
    return "해외" if a["region"] in OVERSEAS else "국내"


TRIP_PAGES_1125 = [(a["slug"], a["name"], kind_of(a)) for a in ARTICLES if a["kind"] == "trip"]
FILES_1125 = [a["slug"] + ".html" for a in ARTICLES]


# K링크 '이 장소가 나오는 글'(t)에 함께 잡을 가이드·계산기 (15개 모두 K링크 연결)
KLINK_EXTRA_1125 = ["guide-boracay-how-to-get-there.html", "guide-kota-kinabalu-airport-to-city.html",
                    "yeosu_trip_budget_calculator.html", "gunsan_trip_budget_calculator.html", "guam_price_tip_calculator.html"]


def _table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join(f'<tr><th scope="row">{r[0]}</th>' + "".join(f'<td class="num">{c}</td>' for c in r[1:]) + "</tr>" for r in rows)
    return f'<div class="tablewrap" tabindex="0" role="region" aria-label="표 (좌우로 밀어서 보기)"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def _links(a):
    """같은 지역 글과 K링크 장소로 잇는 한 문장 (비슷한 글 목록이 아니라 문장 안 링크)."""
    same = [b for b in ARTICLES if b["region"] == a["region"] and b["slug"] != a["slug"]]
    parts = [f'<a href="/{b["slug"]}.html">{html.escape(b["name"])}</a>' for b in same]
    if os.path.exists(f'travel-{a["region"]}.html'):
        parts.append(f'<a href="/travel-{a["region"]}.html">{RNAME[a["region"]]} 여행 코스</a>')
    k = f'<a href="/klink/#{a["places"][0]}">K링크 지도</a>'
    s = f'{RNAME[a["region"]]}의 다른 글은 ' + ", ".join(parts) + "에 있고, " if parts else ""
    return f'<p class="at-next">{s}위치와 동선은 {k}에서 저장해 볼 수 있어요.</p>'


def page(a, style):
    dom = kind_of(a) == "국내"
    faq = a["faq"][:5]
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in faq]}]}
    cards = "".join(f'<h2 class="sec">{h}</h2>\n{b}\n' for h, b in a["cards"])
    head, rows = a["table"]
    faqh = "".join(f'<details{" open" if i == 0 else ""}><summary>{html.escape(q)}</summary>\n<div class="ans">{html.escape(x)}</div></details>\n' for i, (q, x) in enumerate(faq))
    src = "".join(f'<li><a href="{html.escape(u)}" rel="nofollow noopener" target="_blank">{html.escape(n)}</a></li>' for n, u in a["sources"])
    tag = "시장·먹거리" if a["kind"] == "season" else "여행"
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<!-- at:head --><title>{html.escape(a['title'])}</title>
<meta name="description" content="{html.escape(a['desc'])}"><!-- /at:head -->
{style}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<!-- at:assets --><!-- /at:assets -->
</head>
<body>
<!-- at:top --><!-- /at:top -->
<div class="head {'h-dom' if dom else 'h-abr'}">
<div class="in">
<span class="n">{kind_of(a)} · {RNAME[a['region']]} · {tag}</span>
<h1>{html.escape(a['title'])}</h1>
<p>{a['intro']}</p>
</div>
</div>
<main>
<!-- at:photo --><!-- /at:photo -->
<div class="at-answer b-sum"><p>{re.sub(r'^\s*먼저 알아둘 것\s*[:：]\s*', '', a['first'])}</p></div>
{cards}<h2 class="sec">한눈에 정리</h2>
{_table(head, rows)}
<div class="b-tip"><p><b>실전 팁</b> {a['tip']}</p></div>
{_links(a)}
<h2 class="sec">자주 묻는 질문</h2>
<div class="faq">
{faqh}</div>
<h2 class="sec">근거 자료 ({CHK})</h2>
<ul>{src}</ul>
</main>
<!-- at:bottom --><!-- /at:bottom -->
</body>
</html>
"""


def make(src_page="travel-takamatsu.html", force=False):
    t0 = open(src_page, encoding="utf-8").read()
    style = t0[t0.index("<style>"):t0.index("</style>") + len("</style>")]
    n = 0
    for a in ARTICLES:
        f = a["slug"] + ".html"
        if force or not os.path.exists(f):
            open(f, "w", encoding="utf-8").write(page(a, style)); n += 1
    return n
