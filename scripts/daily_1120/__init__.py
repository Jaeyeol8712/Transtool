# -*- coding: utf-8 -*-
"""2026-11-20 매일 콘텐츠 (대표 지시 2026-11-19 21:00): K링크 새 지역 4곳(군산·목포·발리·칭다오) 글 10개 + 기존 지역 글 20개.

- 원고는 이 폴더의 gunsan·mokpo·overseas_new(새 지역), dom_a·dom_b(국내 기존), ov_a·ov_b(해외 기존).
- 구성은 2026-11-19 확정 시안: 제목+한 줄 소개 → 먼저 알아둘 것 → 카드 3~5 → 정리 표 → 노란 팁 → 자주 묻는 질문 5 → 근거 자료.
- trip 글은 travel-*.html(여행 목록·K링크 '이 장소가 나오는 여행 글'), season 글은 season-*.html(제철·시장, K링크 '맛집·먹거리 기록').
- make() 는 파일이 없을 때 한 번만 만든다(이후 build.py 가 공통 영역을 다시 씀).
"""
import html
import re
import json
import os

from . import gunsan, mokpo, overseas_new, dom_a, dom_b, ov_a, ov_b

D = "2026-11-20"
CHK = "2026년 11월 20일 확인"
MODS = [gunsan, mokpo, overseas_new, dom_a, dom_b, ov_a, ov_b]
ARTICLES = [a for m in MODS for a in m.ARTICLES]
SPOTS_1120 = {k: v for m in MODS for k, v in m.SPOTS.items()}

OVERSEAS = {"bali", "qingdao", "osaka", "kyoto", "fukuoka", "okinawa", "taipei", "hongkong", "singapore", "nhatrang", "hochiminh", "kaohsiung"}
RNAME = {"gunsan": "군산", "mokpo": "목포", "bali": "발리", "qingdao": "칭다오", "seoul": "서울", "gyeongju": "경주", "yeosu": "여수", "jeonju": "전주",
         "jeju": "제주", "gangneung": "강릉", "osaka": "오사카", "kyoto": "교토", "fukuoka": "후쿠오카", "okinawa": "오키나와", "taipei": "타이베이",
         "hongkong": "홍콩", "singapore": "싱가포르", "nhatrang": "나트랑", "hochiminh": "호치민", "kaohsiung": "가오슝"}


def kind_of(a):
    return "해외" if a["region"] in OVERSEAS else "국내"


TRIP_PAGES_1120 = [(a["slug"], a["name"], kind_of(a)) for a in ARTICLES if a["kind"] == "trip"]
FILES_1120 = [a["slug"] + ".html" for a in ARTICLES]


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
