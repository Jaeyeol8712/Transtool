#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
어라운드툴 사이트 빌드 스크립트
=================================

    python3 scripts/build.py

하는 일
  1. 모든 페이지에 공통 헤더·GNB·브레드크럼·게시판 탭·사이드바·푸터를 넣습니다.
  2. <head> 를 정리합니다: title / description / canonical / robots / OG / Twitter /
     검증 메타 / 아이콘 / 구조화 데이터(BreadcrumbList, WebPage, FAQPage …)
  3. 계산기(scripts/calc_content.py + src/tools/*.html)와 허브·홈·검색·404·사이트맵을 새로 만듭니다.
  4. sitemap.xml, feed.xml, llms.txt, assets/search-index.json 을 다시 씁니다.

여러 번 실행해도 결과가 같습니다(멱등). 기존 페이지 본문은 건드리지 않고
<!-- at:... --> 주석으로 표시된 공통 영역만 교체합니다.
"""
import html
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime

from bs4 import BeautifulSoup, Comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from calc_content import CALCS  # noqa: E402
from calc_extra import LEGACY_STEPS, LEGACY_NOTE  # noqa: E402
from shop_extra import SHOP_EXTRA, TRUST_NOTE, TRUST_NOTE_TRAVEL, SHOP_UPDATED  # noqa: E402
from connect_posts import POSTS, DISCLOSURE  # noqa: E402
from guides import GUIDES  # noqa: E402

SITE = "https://www.aroundtool.com"
NAME = "어라운드툴"
import hashlib as _hl
CSS_V = _hl.md5(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "site.css"), "rb").read()).hexdigest()[:8]

# ---------- 이미지 (크기·캡션·저작자 표기·구조화 데이터) ----------
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
try:
    PHOTOS = json.load(open(os.path.join(_ROOT, "scripts", "photos.json"), encoding="utf-8"))
except FileNotFoundError:
    PHOTOS = {}
LIC_NAME = {"cc0": "CC0", "pdm": "퍼블릭 도메인", "by": "CC BY", "by-sa": "CC BY-SA"}
_SIZE = {}


def img_size(src):
    """로컬 이미지의 (가로, 세로). width/height 를 넣어 화면 밀림(CLS)을 막습니다."""
    if src in _SIZE:
        return _SIZE[src]
    wh = None
    path = os.path.join(_ROOT, src.lstrip("/"))
    if src.startswith("/") and os.path.exists(path):
        try:
            from PIL import Image as _Im
            with _Im.open(path) as im:
                wh = im.size
        except Exception:
            wh = None
    _SIZE[src] = wh
    return wh


def photo_ok(name):
    return name in PHOTOS and os.path.exists(os.path.join(_ROOT, "assets", "photos", f"{name}.jpg"))


def photo_credit(m):
    lic = LIC_NAME.get(m.get("license"), (m.get("license") or "").upper())
    ver = f" {m['license_version']}" if m.get("license_version") and m.get("license") not in ("pdm",) else ""
    who = esc(m.get("creator") or "작가 미상")
    if m.get("creator_url"):
        who = f'<a href="{esc(m["creator_url"])}" rel="nofollow noopener" target="_blank">{who}</a>'
    lic_html = esc(lic + ver)
    if m.get("license_url"):
        lic_html = f'<a href="{esc(m["license_url"])}" rel="license nofollow noopener" target="_blank">{lic_html}</a>'
    src = f' · <a href="{esc(m["foreign_landing_url"])}" rel="nofollow noopener" target="_blank">원본</a>' if m.get("foreign_landing_url") else ""
    return f"사진: {who} · {lic_html}{src}"


def figure_html(src, alt, caption=None, credit=None, eager=False):
    wh = img_size(src)
    size = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    cap = ""
    if caption or credit:
        cap = "<figcaption>" + (f"<span>{esc(caption)}</span>" if caption else "") + \
              (f'<small class="at-credit">{credit}</small>' if credit else "") + "</figcaption>"
    return f'<figure class="at-fig"><img src="{esc(src)}" alt="{esc(alt)}"{size} {load} decoding="async">{cap}</figure>'


def photo_html(name, eager=False):
    if not photo_ok(name):
        return ""
    m = PHOTOS[name]
    return figure_html(f"/assets/photos/{name}.jpg", m["alt"], m.get("caption"), photo_credit(m), eager)


def image_ld(src, alt, photo=None, seller=None):
    """ImageObject — 구글 이미지 검색의 캡션·라이선스(이미지 메타데이터) 정보.
    photo: 무료 사진 메타(위키미디어·플리커), seller: 판매 페이지 이미지의 권리자 이름(브랜드)."""
    url = SITE + src if src.startswith("/") else src
    o = {"@type": "ImageObject", "contentUrl": url, "url": url, "caption": alt, "name": alt}
    wh = img_size(src) if src.startswith("/") else None
    if wh:
        o["width"], o["height"] = wh
    if photo:
        who = photo.get("creator") or "작가 미상"
        o["creditText"] = who
        o["creator"] = {"@type": "Person", "name": who}
        o["copyrightNotice"] = f"© {who} ({LIC_NAME.get(photo.get('license'), photo.get('license', ''))})"
        if photo.get("license_url"):
            o["license"] = photo["license_url"]
        o["acquireLicensePage"] = photo.get("foreign_landing_url") or photo.get("license_url") or SITE + "/terms.html#copyright"
    elif seller:
        o["creditText"] = f"{seller} 판매 페이지 이미지"
        o["creator"] = {"@type": "Organization", "name": seller}
        o["copyrightNotice"] = f"© {seller}"
        o["license"] = SITE + "/terms.html#copyright"
        o["acquireLicensePage"] = SITE + "/contact.html"
    else:
        o["creditText"] = "어라운드툴"
        o["creator"] = {"@type": "Organization", "name": "어라운드툴", "url": SITE + "/"}
        o["copyrightNotice"] = "© 어라운드툴 (aroundtool.com)"
        o["license"] = SITE + "/terms.html#copyright"
        o["acquireLicensePage"] = SITE + "/contact.html"
    return o

JS_V = _hl.md5(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "assets", "site.js"), "rb").read()).hexdigest()[:8]
TODAY = "2026-10-24"
CALC_DATE = "2026-10-23"
BASE_DATE = "2026-08-29"
KST = timezone(timedelta(hours=9))
GA_ID = "G-2LK65NYW74"
ADSENSE = "ca-pub-7089972708901760"
NAVER_VERIFY = "819ae10e3fae28782afbbbbc248f8423b816872b"

# ════════════════════════════════════════════════════════════════
# 1. 사이트 구조 데이터
# ════════════════════════════════════════════════════════════════

CAT = {
    "bapjip": "밥집", "gogi": "고기", "gukmul-myeon": "국물과 면", "iguk": "이국",
    "sul-anju": "술과 안주", "cafe": "카페·디저트",
}
CAT_ORDER = list(CAT)

# (지역 id, 지역명, 짧은 이름, [(파일 접두사, 구 이름)])
FOOD_AREAS = [
    ("incheon", "인천광역시", "인천", [("yeonsu", "연수구")]),
    ("seoul", "서울특별시", "서울", [("gangnam", "강남구"), ("yongsan", "용산구")]),
    ("busan", "부산광역시", "부산", [("haeundae", "해운대구")]),
    ("gangwon", "강원특별자치도", "강원", [("sokcho", "속초시")]),
    ("daejeon", "대전광역시", "대전", [("daejeon-donggu", "동구"), ("daejeon-junggu", "중구"),
                                      ("daejeon-seogu", "서구"), ("daejeon-yuseong", "유성구"),
                                      ("daejeon-daedeok", "대덕구")]),
    ("gwangju", "광주광역시", "광주", [("gwangju-donggu", "동구"), ("gwangju-seogu", "서구"),
                                      ("gwangju-namgu", "남구"), ("gwangju-bukgu", "북구"),
                                      ("gwangju-gwangsan", "광산구")]),
    ("jeju", "제주특별자치도", "제주", [("jeju-jejusi", "제주시"), ("jeju-seogwipo", "서귀포시")]),
    ("jeonnam", "전라남도", "전남", [("jeonnam-dongbu", "동부권"), ("jeonnam-jungbu", "중부권"),
                                    ("jeonnam-seobu", "서부권"), ("jeonnam-nambu", "남부권")]),
]
REGION_TRAVEL = {"jeju": "travel-jeju.html", "gangwon": "travel-sokcho.html", "busan": "travel-busan.html"}

TOOL_GROUPS = [
    ("money", "재테크·부동산", ["salary_calculator", "loan_calculator", "savings_calculator", "compound_calculator",
                              "freelancer_tax_calculator", "dsr_calculator", "ltv_calculator",
                              "acquisition_tax_calculator", "brokerage_fee_calculator",
                              "increase_decrease_calculator", "pension_age_calculator",
                              "prepayment_penalty_calculator", "interior_calculator"]),
    ("labor", "노동·구직", ["severance_calculator", "unemployment_benefit_calculator", "pto_calculator",
                           "holiday_pay_calculator", "parental_leave_calculator", "service_years_calculator",
                           "hourly_monthly_wage_calculator"]),
    ("life", "생활·건강", ["discount_calculator", "discount_rate_calculator", "percent_calculator",
                          "dutch_pay_calculator", "electricity_bill_calculator", "gas_bill_calculator",
                          "car_tax_calculator", "pyeong_calculator", "age_calculator", "date_calculator", "due_date_calculator",
                          "bmi_calculator", "bmr_calculator", "calorie_calculator", "tire_date_calculator",
                          "grave_weeding_calculator", "qr_generator", "lotto_generator", "job_fortune_teller"]),
    ("trip", "여행", ["fuel_economy_calculator", "exchange_rate_calculator", "japan_travel_calculator",
                     "camping_gear_calculator"]),
    ("text", "텍스트", ["character_counter", "spell_checker", "spacing_checker"]),
]
TOOL_NAMES = {  # 새 템플릿이 아닌 계산기의 짧은 이름
    "salary_calculator": "연봉 실수령액", "acquisition_tax_calculator": "부동산 취득세",
    "interior_calculator": "인테리어 가견적", "severance_calculator": "퇴직금",
    "unemployment_benefit_calculator": "실업급여", "pto_calculator": "연차",
    "holiday_pay_calculator": "주휴수당", "parental_leave_calculator": "육아휴직급여",
    "japan_travel_calculator": "일본 여행 경비", "camping_gear_calculator": "캠핑 장비 견적",
}
KEY_TOOLS = ["salary_calculator", "severance_calculator", "unemployment_benefit_calculator", "pto_calculator",
             "holiday_pay_calculator", "loan_calculator", "acquisition_tax_calculator", "brokerage_fee_calculator",
             "electricity_bill_calculator", "car_tax_calculator"]

TRIP_PAGES = [("travel-jeju", "제주도 여행", "국내"), ("travel-busan", "부산 해운대 여행", "국내"),
              ("travel-sokcho", "속초 여행", "국내"), ("travel-osaka", "오사카 여행", "해외")]
GUIDE_PAGES = [("guide_2026_wage", "2026 최저임금·노동법 변경"), ("guide_2026_tax", "2026 연말정산·종소세 가이드")]
Q_GUIDES = [("guide-" + g["slug"], g["name"]) for g in GUIDES]
INFO_PAGES = [("about", "사이트 소개"), ("editorial", "편집 방침"), ("contact", "문의하기"),
              ("privacy", "개인정보처리방침"), ("terms", "이용약관")]

LEGACY_REDIRECTS = {
    "bapjip.html": "yeonsu-bapjip.html", "gogi.html": "yeonsu-gogi.html",
    "gukmul-myeon.html": "yeonsu-gukmul-myeon.html", "iguk.html": "yeonsu-iguk.html",
    "sul-anju.html": "yeonsu-sul-anju.html", "cafe.html": "yeonsu-cafe.html",
    "hambak.html": "yeonsu-hambak.html", "daily_calorie_calculator.html": "calorie_calculator.html",
}
UNTOUCHED = {"portfolio.html", "Portfolio.dc.html", "stats.html", "categories-section.html"}

UPDATES = [  # (날짜, 말머리, 제목, 링크)
    ("2026-10-24", "맛집", "지역별 맛집 모아보기 21곳 공개 — 구·시 단위로 전체 가게 한눈에", "/haeundae.html"),
    ("2026-10-24", "생활툴", "계산기 퍼가기 기능 — 블로그·홈페이지에 계산기를 그대로 넣기", "/salary_calculator.html"),
    ("2026-10-23", "공지", "사이트 개편 — 게시판형 화면, 통합 검색, 계산기 33종 설명·FAQ 보강", "/about.html"),
    ("2026-10-23", "생활툴", "환율 계산기 개편 — 8개 통화, 최신 기준 환율 자동 반영", "/exchange_rate_calculator.html"),
    ("2026-10-23", "생활툴", "맞춤법·띄어쓰기 검사기 개편 — 자주 틀리는 표현 약 70개, 의존명사 띄어쓰기", "/spell_checker.html"),
    ("2026-10-23", "생활툴", "종합소득세 계산기 — 과세표준 8단계 전 구간 반영", "/freelancer_tax_calculator.html"),
    ("2026-08-29", "생활툴", "노동 계산기 5종 개편 — 연차·주휴수당·육아휴직급여 2026년 기준", "/parental_leave_calculator.html"),
    ("2026-08-29", "생활툴", "실업급여·퇴직금 계산기 개편 — 2026년 상한액 반영", "/unemployment_benefit_calculator.html"),
    ("2026-08-29", "생활툴", "연봉 실수령액 계산기 개편 — 2026년 4대보험 요율 반영", "/salary_calculator.html"),
    ("2026-08-29", "여행", "일본 여행 경비 계산기 공개 — 항공비·일자별 코스·맛집 예산", "/japan_travel_calculator.html"),
    ("2026-08-29", "생활툴", "캠핑 장비 견적 계산기 공개 — 텐트캠핑·차박 32개 품목", "/camping_gear_calculator.html"),
]

FAQ_HOME = [
    ("어라운드툴은 어떤 사이트인가요?",
     "연봉 실수령액·퇴직금·실업급여 같은 생활 계산기와, 광고·협찬을 배제하고 선정 근거를 밝힌 전국 지역 맛집 기록, 국내외 여행 코스·예산 가이드를 무료로 제공하는 사이트입니다. 회원가입 없이 모든 페이지를 이용할 수 있습니다."),
    ("계산 결과를 그대로 믿어도 되나요?",
     "계산기는 최신 법령과 요율을 반영하지만 결과는 참고용 추정치이며 법적 효력이 없습니다. 각 계산기 페이지에 계산 기준과 공식을 적어 두었으니, 급여명세서·고지서·금융기관 안내와 함께 확인하세요."),
    ("맛집은 어떤 기준으로 고르나요?",
     "리뷰 개수가 아니라 재방문 언급을 보고, 미쉐린 가이드·백년가게·지자체 지정처럼 광고비로 살 수 없는 근거와 교차 확인합니다. 협찬·체험단 표기가 있는 글은 근거에서 제외하고, 단점과 확인하지 못한 항목도 함께 적습니다."),
    ("입력한 값이 저장되거나 전송되나요?",
     "계산은 모두 사용하는 브라우저 안에서 이뤄지며 입력값을 서버로 보내거나 저장하지 않습니다."),
    ("잘못된 정보는 어디에 알리나요?",
     "문의하기 페이지의 이메일로 알려 주시면 확인 후 수정하고, 수정 사항은 최근 업데이트에 기록합니다."),
]

# ════════════════════════════════════════════════════════════════
# 2. 유틸
# ════════════════════════════════════════════════════════════════

def esc(s):
    return html.escape(str(s), quote=True)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    d = os.path.dirname(p)
    if d:
        os.makedirs(d, exist_ok=True)
    if p.endswith(".html"):
        s = focusable_tables(s)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


_TBL_RE = re.compile(r'<div class="(at-table|tablewrap)"(?![^>]*tabindex)([^>]*)>')


def focusable_tables(s):
    """가로로 밀리는 표 상자를 키보드로도 스크롤할 수 있게 (접근성: scrollable-region-focusable)."""
    return _TBL_RE.sub(lambda m: '<div class="%s"%s tabindex="0" role="region" aria-label="표 (좌우로 밀어서 보기)">'
                       % (m.group(1), m.group(2)), s)


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def short_date(d):
    return d[5:].replace("-", ".")


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def url_of(f):
    return SITE + "/" if f == "index.html" else f"{SITE}/{f}"


def clean_title(t):
    t = html.unescape(t).strip()
    t = re.split(r"\s+\|\s+", t)[0].strip()
    t = re.sub(r"\s+-\s+", " — ", t)
    t = re.sub(r"\s+—\s+(어라운드툴|생활 계산기 모음)$", "", t)
    return t


# ════════════════════════════════════════════════════════════════
# 3. 페이지 목록 만들기
# ════════════════════════════════════════════════════════════════

PAGES = {}   # 파일명 → 정보 dict


def head_info(f):
    s = read(f)
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s)
    return (html.unescape(t.group(1)).strip() if t else ""), (html.unescape(d.group(1)).strip() if d else "")


def count_places(f, title):
    s = read(f)
    m = re.search(r"(\d+)곳", title)
    if m:
        return int(m.group(1))
    n = len(re.findall(r'"@type"\s*:\s*"Restaurant"', s))
    if n:
        return n
    return len(re.findall(r'<article class="entry[ "]', s))


def register_food():
    for rid, rname, rshort, gus in FOOD_AREAS:
        for prefix, gu in gus:
            files = sorted(f for f in os.listdir(".") if f.startswith(prefix + "-") and f.endswith(".html"))
            # 대전·광주는 접두사가 겹치지 않도록 정확히 다음 토막만 허용
            for f in files:
                slug = f[len(prefix) + 1:-5]
                if any(f.startswith(p2 + "-") and len(p2) > len(prefix) for _, _, _, g2 in FOOD_AREAS for p2, _ in g2):
                    continue
                title, desc = head_info(f)
                main = clean_title(title)
                detail = main.split(" — ", 1)[1].strip() if " — " in main else ""
                research = bool(re.search(r"조사 중", main))
                if slug in CAT:
                    cat, special = CAT[slug], False
                else:
                    special = True
                    cat = main.split(" — ")[0]
                    for pre in (f"{rshort} {gu} ", f"{rname} {gu} ", f"{gu} ", "해운대 ", "속초 ", "용산 ", "강남 "):
                        if cat.startswith(pre) and len(cat) > len(pre) + 1:
                            cat = cat[len(pre):]
                    cat = cat.replace("남도음식거리 ", "남도음식거리 ").strip()
                    if cat.startswith("남도음식거리"):
                        cat = "남도음식거리"
                n = 0 if research else count_places(f, main)
                if re.fullmatch(r"(\d+곳|자료 조사 중|조사 중)", detail):
                    detail = ""
                detail = re.sub(r"\s*\d+곳$", "", detail).strip()
                area = f"{rshort} {gu}"
                PAGES[f] = dict(
                    file=f, section="food", region=rid, region_name=rname, region_short=rshort, gu=gu,
                    prefix=prefix, slug=slug, cat=cat, special=special, count=n, research=research,
                    detail=detail, desc=desc, old_title=title, date=BASE_DATE,
                    name=f"{area} {cat}", short=cat,
                )


def register_tools():
    for gid, gname, slugs in TOOL_GROUPS:
        for slug in slugs:
            f = slug + ".html"
            if slug in CALCS:
                c = CALCS[slug]
                PAGES[f] = dict(file=f, section="tools", group=gid, group_name=gname, name=c["name"],
                                short=c["name"], desc=c["desc"], date=CALC_DATE, calc=True,
                                title=c["title"])
            else:
                title, desc = head_info(f)
                PAGES[f] = dict(file=f, section="tools", group=gid, group_name=gname,
                                name=TOOL_NAMES.get(slug, clean_title(title)), short=TOOL_NAMES.get(slug, ""),
                                desc=desc, date=BASE_DATE, calc=False, old_title=title)


def register_misc():
    for slug, name, kind in TRIP_PAGES:
        f = slug + ".html"
        title, desc = head_info(f)
        PAGES[f] = dict(file=f, section="trip", name=name, short=name.replace(" 여행", ""), kind=kind,
                        desc=desc, date=BASE_DATE, old_title=title)
    for g in GUIDES:
        f = f"guide-{g['slug']}.html"
        PAGES[f] = dict(file=f, section="guide", name=g["name"], short=g["name"], title=g["title"], desc=g["desc"],
                        date=g["date"], guide=g)
    for slug, name in GUIDE_PAGES:
        f = slug + ".html"
        title, desc = head_info(f)
        PAGES[f] = dict(file=f, section="guide", name=name, short=name, desc=desc, date=BASE_DATE, old_title=title)
    for slug, name in INFO_PAGES:
        f = slug + ".html"
        title, desc = head_info(f)
        PAGES[f] = dict(file=f, section="info", name=name, short=name, desc=desc, date=BASE_DATE, old_title=title)
    hubs = [("index.html", "home", "홈"), ("food.html", "hub-food", "전국 맛집"), ("tools.html", "hub-tools", "생활툴"),
            ("travel.html", "hub-trip", "여행"), ("etc.html", "hub-guide", "가이드·텍스트"),
            ("connect.html", "hub-connect", "추천 모음"), ("sitemap.html", "info", "사이트맵"), ("search.html", "util", "검색"), ("404.html", "util", "페이지를 찾을 수 없음")]
    for f, sec, name in hubs:
        title, desc = head_info(f) if os.path.exists(f) else ("", "")
        PAGES[f] = dict(file=f, section=sec, name=name, short=name, desc=desc, date=TODAY, old_title=title)
    PAGES["sitemap.html"]["date"] = TODAY
    for post in POSTS:
        f = f"shop-{post['slug']}.html"
        PAGES[f] = dict(file=f, section="connect", name=post["product"], short=post.get("short") or post["product"],
                        title=post["title"], desc=post["desc"], date=post.get("date", TODAY),
                        draft=post.get("draft", False), post=post)


register_food()
register_tools()
register_misc()


def register_gu_hubs():
    for rid, rname, rshort, gus in FOOD_AREAS:
        for prefix, gu in gus:
            f = prefix + ".html"
            PAGES[f] = dict(file=f, section="gu", region=rid, region_name=rname, region_short=rshort, gu=gu,
                            prefix=prefix, name=f"{rshort} {gu} 맛집", short=f"{gu} 전체", date=TODAY, research=False)


register_gu_hubs()

FOOD = [p for p in PAGES.values() if p["section"] == "food"]
FOOD_OK = [p for p in FOOD if not p["research"]]
TOOLS = [p for p in PAGES.values() if p["section"] == "tools"]
_POST_ORDER = {post["slug"]: i for i, post in enumerate(POSTS)}
# 최신 올린 순서: 작성일이 같으면 나중에 추가한 글이 먼저
SHOP = sorted([p for p in PAGES.values() if p["section"] == "connect"],
              key=lambda p: (p["date"], _POST_ORDER.get(p["post"]["slug"], 0)), reverse=True)
SHOP_LIVE = [p for p in SHOP if not p.get("draft")]
KINDS = {"product": "제품 추천", "travel": "여행 추천"}


def kind_of(p):
    k = (p.get("post") or {}).get("kind", "product")
    return k if k in KINDS else "product"
N_TOOLS = len(TOOLS)
N_PLACES = sum(p["count"] for p in FOOD_OK)
N_GU = sum(len(g) for _, _, _, g in FOOD_AREAS)


def food_pages(prefix):
    ps = [p for p in FOOD if p["prefix"] == prefix]
    order = {c: i for i, c in enumerate(CAT_ORDER)}
    return sorted(ps, key=lambda p: (order.get(p["slug"], 50), p["file"]))


def gu_first(prefix):
    ps = [p for p in food_pages(prefix) if not p["research"]] or food_pages(prefix)
    return ps[0]["file"]


def gu_count(prefix):
    return sum(p["count"] for p in food_pages(prefix) if not p["research"])


def region_count(rid):
    return sum(gu_count(pre) for r, _, _, gus in FOOD_AREAS if r == rid for pre, _ in gus)


# 각 페이지의 최종 SEO 제목·설명
for p in PAGES.values():
    sec = p["section"]
    if sec == "food":
        area = f"{p['region_short']} {p['gu']}"
        if p["research"]:
            p["title"] = f"{area} {p['cat']} — 자료 조사 중"
        elif p["special"]:
            base = clean_title(p["old_title"])
            if not base.startswith(p["region_short"]) and p["gu"] not in base and p["region_short"] not in base:
                base = f"{area} {base}"
            p["title"] = base
        else:
            p["title"] = f"{area} {p['cat']} 맛집 {p['count']}곳" + (f" — {p['detail']}" if p["detail"] else "")
        if not p["desc"]:
            p["desc"] = f"{p['region_name']} {p['gu']} {p['cat']} 맛집 기록. 광고·협찬을 배제하고 선정 근거와 단점, 가격·영업시간 확인 여부를 함께 적었습니다."
    elif sec == "tools" and not p.get("calc"):
        p["title"] = clean_title(p["old_title"])
    elif "title" not in p:
        p["title"] = clean_title(p.get("old_title") or p["name"])

PAGES["index.html"]["title"] = "어라운드툴 — 생활 계산기·전국 맛집 기록·여행 가이드"
PAGES["index.html"]["desc"] = (f"연봉 실수령액·퇴직금·실업급여·대출 이자 등 무료 생활 계산기 {N_TOOLS}종, 대가 없이 근거를 밝힌 "
                               f"전국 {N_GU}개 시군구 맛집 {N_PLACES}곳 기록, 제주·부산·속초·오사카 여행 코스와 예산을 한곳에서.")
PAGES["food.html"]["title"] = f"전국 맛집 기록 — {len(FOOD_AREAS)}개 시도 {N_GU}개 지역 {N_PLACES}곳"
PAGES["food.html"]["desc"] = (f"인천 연수구, 서울 강남·용산, 부산 해운대, 속초, 대전, 광주, 제주, 전남까지 {N_GU}개 지역의 맛집 {N_PLACES}곳. "
                              "광고·협찬을 빼고 재방문 언급과 공식 지정 근거로 고르고, 단점까지 적은 지역별 맛집 게시판입니다.")
PAGES["tools.html"]["title"] = f"생활툴 — 무료 생활 계산기 {N_TOOLS}종 모음"
PAGES["tools.html"]["desc"] = (f"연봉 실수령액, 퇴직금, 실업급여, 주휴수당, 대출 이자, 취득세, 중개보수, 전기요금, BMI까지 생활 계산기 {N_TOOLS}종. "
                               "로그인 없이 무료이며 2026년 요율과 법령을 반영했습니다.")
# ── 서치콘솔 기회 검색어(평균 8~20위)에 맞춘 제목·설명 보강 (2026-10-25 보고서 기준) ──
SEO_FIX = {
    "japan_travel_calculator.html": ("일본 여행 경비 계산기 — 일본여행 비용 얼마? 항공·숙박·식비 예산",
        "일본 여행 비용이 얼마나 드는지 도쿄·오사카·후쿠오카·삿포로·오키나와·나고야 등 도시와 기간, 여행 스타일로 계산합니다. 항공권·숙박·식비·교통비 내역과 일자별 코스를 함께 보여 줍니다."),
    "loan_calculator.html": ("대출 이자 계산기 — 원리금균등·원금균등 상환 계산기, 월 상환금표",
        None),
    "exchange_rate_calculator.html": ("환율 계산기 — 달러·엔화·위안·유로 원화 환산 (오늘 기준 환율)", None),
    "character_counter.html": ("글자수 세기 — 공백 포함·제외 글자수 계산기 (자소서·블로그)", None),
    "spell_checker.html": ("맞춤법 검사기 — 오탈자 검사, 자주 틀리는 표현 약 70개 자동 표시", None),
    "spacing_checker.html": ("띄어쓰기 검사기 — 자소서·블로그 글 띄어쓰기 교정 (의존명사 ‘수·것·때·줄’)", None),
    "severance_calculator.html": ("퇴직금 계산기 — 근속연수·평균임금으로 퇴직금 얼마인지 계산 (상여금 반영)", None),
    "yeonsu-hambak.html": ("함박마을 맛집 — 인천 연수구 고려인 마을 중앙아시아 식당 기록",
        "인천 연수구 함박마을(국내 최대 고려인 마을)의 중앙아시아 식당 기록. 플롭·샤슬릭·삼사 같은 메뉴와 가게별 선정 근거, 단점까지 함께 정리했습니다."),
    "jeju-seogwipo-galchi.html": ("서귀포 갈치 맛집 2곳 — 갈치국·갈치조림 (호림식당·네거리식당)", None),
    "yongsan-bapjip.html": ("용산 생선구이·순대국 맛집 2곳 — 후암동 순대국과 용산동 노포 대원식당", None),
}
for _f, (_t, _d) in SEO_FIX.items():
    if _f in PAGES:
        PAGES[_f]["title"] = _t
        if _d:
            PAGES[_f]["desc"] = _d
PAGES["search.html"].update(title="사이트 검색", desc="어라운드툴의 계산기, 맛집, 여행, 가이드 페이지를 검색합니다.")
PAGES["404.html"].update(title="페이지를 찾을 수 없습니다", desc="요청한 주소의 페이지가 없거나 이동했습니다.")
PAGES["sitemap.html"].update(title="사이트맵 — 어라운드툴 전체 페이지 목록",
                             desc=f"어라운드툴의 생활 계산기 {N_TOOLS}종, 지역별 맛집, 여행·가이드, 사이트 안내 페이지 전체 목록입니다.")


def indexable(p):
    if p["section"] in ("util",):
        return False
    if p.get("research") or p.get("draft"):
        return False
    if p["section"] == "hub-connect" and not [q for q in PAGES.values() if q["section"] == "connect" and not q.get("draft")]:
        return False
    return True


# ════════════════════════════════════════════════════════════════
# 4. 공통 영역 HTML
# ════════════════════════════════════════════════════════════════

GNB = [("index.html", "홈", "g-home", "home"), ("food.html", "맛집", "g-food", "food"),
       ("tools.html", "생활툴", "g-tool", "tools"), ("travel.html", "여행", "g-trip", "trip"),
       ("etc.html", "가이드", "g-etc", "guide"), ("connect.html", "추천 모음", "g-shop", "connect")]


def gnb_key(p):
    s = p["section"]
    return {"home": "home", "food": "food", "hub-food": "food", "gu": "food", "tools": "tools", "hub-tools": "tools",
            "trip": "trip", "hub-trip": "trip", "guide": "guide", "hub-guide": "guide",
            "connect": "connect", "hub-connect": "connect"}.get(s, "")


def header_html(p):
    key = gnb_key(p)
    items = []
    for f, label, cls, k in GNB:
        on = k == key
        cur = ' aria-current="page"' if p["file"] == f else ""
        items.append(f'<li><a class="{cls}{" is-on" if on else ""}" href="/{"" if f == "index.html" else f}"{cur}>{label}</a></li>')
    return f"""<a class="at-skip" href="#at-main">본문 바로가기</a>
<div class="at-util"><div class="at-in">
  <p class="at-util-msg">무료 생활 계산기 · 대가 없이 근거를 밝힌 맛집 기록</p>
  <nav aria-label="사이트 안내"><a href="/about.html">사이트 소개</a><a href="/editorial.html">편집 방침</a><a href="/contact.html">문의하기</a><a href="/sitemap.html">사이트맵</a></nav>
</div></div>
<header class="at-header"><div class="at-in">
  <a class="at-logo" href="/" aria-label="{NAME} 홈"><span class="at-logo-mark" aria-hidden="true"></span>어라운드<b>툴</b></a>
  <form class="at-search" action="/search.html" method="get" role="search">
    <label class="at-sr" for="at-q">사이트 검색</label>
    <input id="at-q" type="search" name="q" placeholder="계산기, 지역, 음식 이름으로 검색" autocomplete="off">
    <button type="submit">검색</button>
  </form>
  <nav class="at-header-links" aria-label="바로가기"><a href="/salary_calculator.html">연봉 실수령액</a><a href="/severance_calculator.html">퇴직금</a><a href="/food.html">지역별 맛집</a></nav>
</div></header>
<nav class="at-gnb" aria-label="주 메뉴"><ul>{"".join(items)}</ul></nav>"""


def crumbs_for(p):
    f, s = p["file"], p["section"]
    c = [("홈", "/")]
    if s == "food":
        c += [("맛집", "/food.html"), (p["region_short"], f"/food.html#r-{p['region']}"),
              (p["gu"], f"/{p['prefix']}.html"), (p["cat"], None)]
    elif s == "gu":
        c += [("맛집", "/food.html"), (p["region_short"], f"/food.html#r-{p['region']}"), (p["gu"], None)]
    elif s == "tools":
        c += [("생활툴", "/tools.html"), (p["group_name"], f"/tools.html#g-{p['group']}"), (p["name"], None)]
    elif s == "trip":
        c += [("여행", "/travel.html"), (p["name"], None)]
    elif s == "guide":
        c += [("가이드", "/etc.html"), (p["name"], None)]
    elif s == "connect":
        k = kind_of(p)
        c += [("추천 모음", "/connect.html"), (KINDS[k], f"/connect.html#{k}"), (p["name"], None)]
    elif s in ("info",):
        c += [(p["name"], None)]
    elif s.startswith("hub-") or s == "util":
        c += [(p["name"], None)]
    return c


def crumb_html(p):
    c = crumbs_for(p)
    if len(c) <= 1:
        return ""
    li = []
    for i, (label, href) in enumerate(c):
        if href is None or i == len(c) - 1:
            li.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
        else:
            li.append(f'<li><a href="{href}">{esc(label)}</a></li>')
    return f'<nav class="at-crumb" aria-label="현재 위치"><ol>{"".join(li)}</ol></nav>'


def crumb_ld(p):
    c = crumbs_for(p)
    if len(c) <= 1:
        return None
    items = []
    for i, (label, href) in enumerate(c):
        u = url_of(p["file"]) if (href is None or i == len(c) - 1) else (SITE + href if href != "/" else SITE + "/")
        items.append({"@type": "ListItem", "position": i + 1, "name": label, "item": u})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def board_html(p):
    s = p["section"]
    if s in ("food", "gu"):
        area = next(a for a in FOOD_AREAS if a[0] == p["region"])
        cur0 = ' aria-current="page"' if s == "gu" else ""
        tabs = [f'<li><a href="/{p["prefix"]}.html"{cur0}>전체<span class="c">{gu_count(p["prefix"])}</span></a></li>']
        for q in food_pages(p["prefix"]):
            cur = ' aria-current="page"' if q["file"] == p["file"] else ""
            cnt = f'<span class="c">{q["count"]}</span>' if q["count"] else ('<span class="c">조사 중</span>' if q["research"] else "")
            tabs.append(f'<li><a href="/{q["file"]}"{cur}>{esc(q["short"])}{cnt}</a></li>')
        sub = ""
        if len(area[3]) > 1:
            links = []
            for pre, gu in area[3]:
                cur = ' aria-current="page"' if pre == p["prefix"] else ""
                links.append(f'<a href="/{pre}.html"{cur}>{esc(gu)}</a>')
            sub = f'<div class="at-board-sub"><span>{esc(area[2])} 다른 지역</span>{"".join(links)}</div>'
        return f"""<div class="at-board is-food">
  <div class="at-board-head"><p class="at-board-name"><a href="/{p['prefix']}.html">{esc(p['region_short'])} {esc(p['gu'])} 맛집</a></p><span class="at-board-meta">{gu_count(p['prefix'])}곳 수록 · 광고·협찬 제외</span></div>
  <ul class="at-board-tabs">{"".join(tabs)}</ul>{sub}
</div>"""
    if s == "tools":
        g = next(x for x in TOOL_GROUPS if x[0] == p["group"])
        tabs = []
        for slug in g[2]:
            q = PAGES[slug + ".html"]
            cur = ' aria-current="page"' if q["file"] == p["file"] else ""
            tabs.append(f'<li><a href="/{q["file"]}"{cur}>{esc(q["name"])}</a></li>')
        return f"""<div class="at-board is-tool">
  <div class="at-board-head"><p class="at-board-name"><a href="/tools.html#g-{g[0]}">생활툴 · {esc(g[1])}</a></p><span class="at-board-meta">{len(g[2])}종</span></div>
  <ul class="at-board-tabs">{"".join(tabs)}</ul>
</div>"""
    if s == "trip":
        tabs = []
        for slug, name, kind in TRIP_PAGES:
            cur = ' aria-current="page"' if slug + ".html" == p["file"] else ""
            tabs.append(f'<li><a href="/{slug}.html"{cur}>{esc(name.replace(" 여행", ""))}</a></li>')
        tabs.append('<li><a href="/japan_travel_calculator.html">일본 여행 경비 계산</a></li>')
        tabs.append('<li><a href="/exchange_rate_calculator.html">환율 계산</a></li>')
        return f"""<div class="at-board is-trip">
  <div class="at-board-head"><p class="at-board-name"><a href="/travel.html">여행 가이드</a></p><span class="at-board-meta">코스 · 일정 · 예산 · 교통 · 맛집</span></div>
  <ul class="at-board-tabs">{"".join(tabs)}</ul>
</div>"""
    if s == "connect":
        k = kind_of(p)
        tabs = []
        for q in [x for x in SHOP if kind_of(x) == k and (not x.get("draft") or x["file"] == p["file"])][:12]:
            cur = ' aria-current="page"' if q["file"] == p["file"] else ""
            tabs.append(f'<li><a href="/{q["file"]}"{cur}>{esc(q["short"])}</a></li>')
        sub = "".join(f'<a href="/connect.html#{kk}"{" aria-current=\"page\"" if kk == k else ""}>{esc(v)}</a>' for kk, v in KINDS.items())
        return f"""<div class="at-board is-shop">
  <div class="at-board-head"><p class="at-board-name"><a href="/connect.html#{k}">추천 모음 · {esc(KINDS[k])}</a></p><span class="at-board-meta">제휴 링크가 포함된 광고 게시판</span></div>
  <ul class="at-board-tabs">{"".join(tabs)}</ul>
  <div class="at-board-sub"><span>분류</span>{sub}</div>
</div>"""
    if s == "guide":
        tabs = []
        for slug, name in Q_GUIDES + GUIDE_PAGES:
            cur = ' aria-current="page"' if slug + ".html" == p["file"] else ""
            tabs.append(f'<li><a href="/{slug}.html"{cur}>{esc(name)}</a></li>')
        return f"""<div class="at-board">
  <div class="at-board-head"><p class="at-board-name"><a href="/etc.html">생활 가이드</a></p><span class="at-board-meta">질문에 바로 답하는 가이드</span></div>
  <ul class="at-board-tabs">{"".join(tabs)}</ul>
</div>"""
    return ""


def row(href, title, tag=None, tagcls="", cnt=None, cntcls="", date=None, new=False, extra=None):
    t = f'<span class="tag {tagcls}">{esc(tag)}</span>' if tag else ""
    c = f'<span class="cnt {cntcls}">[{cnt}]</span>' if cnt else ""
    n = '<span class="n" aria-label="새 글">N</span>' if new else ""
    d = f'<time class="d" datetime="{date}">{short_date(date)}</time>' if date else ""
    x = f'<span class="x">{esc(extra)}</span>' if extra else ""
    return f'<li><a href="{href}">{t}<span class="t">{esc(title)}{c}{n}{x}</span>{d}</a></li>'


def is_new(date):
    return date >= "2026-10-01"


GUIDE_LINKS = {  # 가이드 ↔ 계산기
    "guide_2026_wage.html": ["salary_calculator", "holiday_pay_calculator", "pto_calculator", "severance_calculator",
                             "unemployment_benefit_calculator", "parental_leave_calculator"],
    "guide_2026_tax.html": ["freelancer_tax_calculator", "salary_calculator", "acquisition_tax_calculator", "car_tax_calculator"],
}
TRIP_TOOLS = {"travel-osaka.html": ["japan_travel_calculator", "exchange_rate_calculator"],
              "travel-jeju.html": ["fuel_economy_calculator", "camping_gear_calculator"],
              "travel-busan.html": ["fuel_economy_calculator"], "travel-sokcho.html": ["fuel_economy_calculator", "camping_gear_calculator"]}


def cross_links(p):
    """다른 섹션으로 이어지는 관련 페이지 (중복 없이 최대 6개)."""
    f, s = p["file"], p["section"]
    out = []
    add = lambda x: out.append(x) if x in PAGES and x != f and x not in out and indexable(PAGES[x]) else None
    travel_of = {v: k for k, v in REGION_TRAVEL.items()}
    if s in ("food", "gu"):
        if s == "food":
            add(p["prefix"] + ".html")
        if p["region"] in REGION_TRAVEL:
            add(REGION_TRAVEL[p["region"]])
            for t in TRIP_TOOLS.get(REGION_TRAVEL[p["region"]], []):
                add(t + ".html")
        for q in SHOP_LIVE:
            if f in [r if r.endswith(".html") else r + ".html" for r in q["post"].get("related", [])]:
                add(q["file"])
    elif s == "trip":
        rid = travel_of.get(f)
        if rid:
            for _, _, _, gus in [a for a in FOOD_AREAS if a[0] == rid]:
                for pre, _ in gus:
                    add(pre + ".html")
        for t in TRIP_TOOLS.get(f, []):
            add(t + ".html")
        for q in SHOP_LIVE:
            if kind_of(q) == "travel":
                add(q["file"])
    elif s == "tools":
        for g, calcs in GUIDE_LINKS.items():
            if f[:-5] in calcs:
                add(g)
        for t, calcs in TRIP_TOOLS.items():
            if f[:-5] in calcs:
                add(t)
        for q in SHOP_LIVE:
            if f in [r if r.endswith(".html") else r + ".html" for r in q["post"].get("related", [])]:
                add(q["file"])
    elif s == "guide":
        for c in GUIDE_LINKS.get(f, []):
            add(c + ".html")
        for g in GUIDE_LINKS:
            add(g)
    elif s == "connect":
        if kind_of(p) == "travel":
            for t in TRIP_PAGES:
                add(t[0] + ".html")
    return out[:6]


def cross_tag(q):
    return {"food": ("맛집", "food"), "gu": ("맛집", "food"), "tools": ("생활툴", ""), "trip": ("여행", "trip"),
            "guide": ("가이드", "etc"), "connect": ("추천", "shop")}.get(q["section"], ("안내", "etc"))


def cross_html(p):
    items = cross_links(p)
    if not items:
        return ""
    rows = []
    for f in items:
        q = PAGES[f]
        tag, cls = cross_tag(q)
        title = q.get("title") if q["section"] in ("connect", "trip", "guide") else q["name"] + (" 계산기" if q["section"] == "tools" and "계산" not in q["name"] else "")
        rows.append(row("/" + f, title, tag, cls, None, "", None))
    return f"""<section class="at-related at-cross" aria-label="다른 섹션에서 함께 보기">
  <div class="at-box-head"><h2>함께 보면 좋은 글</h2></div>
  <div class="at-box-body"><ul class="at-list">{"".join(rows)}</ul></div>
</section>"""


def related_html(p):
    s = p["section"]
    rows, head, more = [], "", ""
    if s == "food":
        head = f"{p['region_short']} 다른 맛집 기록"
        more = f'<a class="more" href="/food.html#r-{p["region"]}">{esc(p["region_short"])} 전체</a>'
        same = [q for q in FOOD_OK if q["region"] == p["region"] and q["file"] != p["file"] and q["prefix"] != p["prefix"]]
        if len(same) < 4:
            same += [q for q in FOOD_OK if q["prefix"] == p["prefix"] and q["file"] != p["file"]]
        if len(same) < 4:
            same += [q for q in FOOD_OK if q["region"] != p["region"] and not q["special"] and q["slug"] == p["slug"]]
        seen = []
        for q in same:
            if q["file"] not in seen:
                seen.append(q["file"])
        for f in seen[:8]:
            q = PAGES[f]
            rows.append(row("/" + q["file"], q["name"], q["region_short"], "food", q["count"] or None, "", q["date"]))
        if p["region"] in REGION_TRAVEL:
            tp = PAGES[REGION_TRAVEL[p["region"]]]
            rows.insert(0, row("/" + tp["file"], tp["name"] + " — 코스·예산·교통", "여행", "trip", None, "", tp["date"]))
    elif s == "tools":
        head = "함께 쓰는 계산기"
        more = '<a class="more" href="/tools.html">전체 계산기</a>'
        rel = CALCS.get(p["file"][:-5], {}).get("related") or []
        g = next(x for x in TOOL_GROUPS if x[0] == p["group"])[2]
        pool = [r for r in rel] + [x for x in g if x not in rel]
        pool = [x for x in pool if x + ".html" != p["file"] and x + ".html" in PAGES][:8]
        for slug in pool:
            q = PAGES[slug + ".html"]
            rows.append(row("/" + q["file"], q["name"], q["group_name"].split("·")[0], "", None, "", q["date"], is_new(q["date"])))
    elif s == "trip":
        head = "여행지 맛집 기록"
        more = '<a class="more" href="/food.html">전국 맛집</a>'
        rid = {v: k for k, v in REGION_TRAVEL.items()}.get(p["file"])
        pool = [q for q in FOOD_OK if q["region"] == rid][:8] if rid else []
        if not pool:
            pool = [PAGES[x] for x in ("japan_travel_calculator.html", "exchange_rate_calculator.html", "fuel_economy_calculator.html")]
            head = "여행 계산기"
            more = '<a class="more" href="/tools.html#g-trip">여행 도구</a>'
        for q in pool:
            rows.append(row("/" + q["file"], q["name"], q.get("region_short") or "도구", "food" if q["section"] == "food" else "", q.get("count") or None, "", q["date"]))
    elif s == "guide":
        head = "관련 계산기"
        more = '<a class="more" href="/tools.html#g-labor">노동 계산기</a>'
        for slug in ("salary_calculator", "holiday_pay_calculator", "severance_calculator", "unemployment_benefit_calculator", "freelancer_tax_calculator", "pto_calculator"):
            q = PAGES[slug + ".html"]
            rows.append(row("/" + q["file"], q["name"], "생활툴", "", None, "", q["date"], is_new(q["date"])))
    elif s == "connect":
        k = kind_of(p)
        head = f"다른 {KINDS[k]} 글"
        more = f'<a class="more" href="/connect.html#{k}">전체 글</a>'
        for q in sorted([x for x in SHOP_LIVE if x["file"] != p["file"]], key=lambda x: kind_of(x) != k)[:6]:
            rows.append(row("/" + q["file"], q["title"], "광고", "shop", None, "", q["date"], is_new(q["date"])))
        for f in p["post"].get("related", []):
            f = f if f.endswith(".html") else f + ".html"
            if f in PAGES:
                q = PAGES[f]
                rows.append(row("/" + f, q["name"] + (" 계산기" if q["section"] == "tools" else ""), "생활툴" if q["section"] == "tools" else "관련", "", None, "", q["date"]))
        if not rows:
            return ""
    else:
        return ""
    note = ""
    if s == "food":
        note = ('<p class="at-note" style="margin:0 0 .75rem"><b>조사 기준</b> 2026년 8월 조사. 가격·영업시간·휴무는 바뀔 수 있으니 방문 전 확인하세요. '
                '협찬·체험단·원고료를 받은 콘텐츠는 검증 근거에서 제외했습니다. <a href="/editorial.html" style="color:var(--at-brand)">선정 기준 보기</a></p>')
    return f"""<section class="at-related" aria-label="{esc(head)}">
  <div class="at-box-head"><h2>{esc(head)}</h2>{more}</div>
  <div class="at-box-body">{note}<ul class="at-list">{"".join(rows)}</ul></div>
</section>"""


def side_html():
    key = "".join(row("/" + PAGES[s + ".html"]["file"], PAGES[s + ".html"]["name"], None, "", None, "", None) for s in KEY_TOOLS[:8])
    ups = "".join(row(u, t, None, "", None, "", d, is_new(d)) for d, tag, t, u in UPDATES[:5])
    shops = "".join(row("/" + q["file"], q["title"], KINDS[kind_of(q)][:2], "shop", None, "", q["date"], is_new(q["date"])) for q in SHOP_LIVE[:5])
    regions = "".join(f'<a href="/food.html#r-{rid}">{esc(rshort)} <span style="color:var(--at-faint)">{region_count(rid)}</span></a>'
                      for rid, _, rshort, _ in FOOD_AREAS)
    return f"""<aside class="at-side" aria-label="사이드바">
  <section class="at-box"><div class="at-stat">
    <div><b>{N_TOOLS}</b><span>생활 계산기</span></div>
    <div><b>{N_PLACES}</b><span>맛집 기록</span></div>
    <div><b>{N_GU}</b><span>수록 지역</span></div>
  </div>
  <div class="at-visitors" data-visitors hidden><span>오늘 <b data-v="today">-</b></span><span>어제 <b data-v="yesterday">-</b></span><span>전체 <b data-v="total">-</b></span></div></section>
  <section class="at-box is-tool"><div class="at-box-head"><p>주요 계산기</p><a class="more" href="/tools.html">전체</a></div>
    <div class="at-box-body"><ul class="at-list">{key}</ul></div></section>
  <section class="at-box is-food"><div class="at-box-head"><p>지역별 맛집</p><a class="more" href="/food.html">전체</a></div>
    <div class="at-regions">{regions}</div></section>
  <section class="at-box is-shop"><div class="at-box-head"><p>추천 모음 새 글</p><a class="more" href="/connect.html">전체</a></div>
    <div class="at-box-body"><ul class="at-list is-wrap">{shops}</ul></div></section>
  <section class="at-box"><div class="at-box-head"><p>최근 업데이트</p></div>
    <div class="at-box-body"><ul class="at-list is-wrap">{ups}</ul></div></section>
  <section class="at-box"><div class="at-box-head"><p>이 사이트의 원칙</p></div>
    <div class="at-promise"><p>계산기는 계산 기준과 공식을 화면에 밝힙니다. 맛집은 광고·협찬 글을 근거에서 빼고 단점도 적습니다.</p>
    <a href="/editorial.html">편집 방침 읽기</a></div></section>
</aside>"""


def footer_html():
    regions = "".join(f'<li><a href="/{gus[0][0]}.html">{esc(rshort)} {esc(gus[0][1])} 맛집</a></li>' for rid, _, rshort, gus in FOOD_AREAS[:6])
    groups = "".join(f'<li><a href="/tools.html#g-{gid}">{esc(gname)}</a></li>' for gid, gname, _ in TOOL_GROUPS)
    trips = "".join(f'<li><a href="/{slug}.html">{esc(name)}</a></li>' for slug, name, _ in TRIP_PAGES)
    shop_links = "".join(f'<li><a href="/{q["file"]}">{esc(q["post"]["keyword"])}</a></li>' for q in SHOP_LIVE[:5])
    return f"""<footer class="at-footer"><div class="at-in">
  <div class="at-footer-brand"><a class="at-logo" href="/"><span class="at-logo-mark" aria-hidden="true"></span>어라운드<b>툴</b></a>
    <p>무료 생활 계산기와 대가 없이 근거를 밝힌 지역 맛집 기록. 회원가입 없이 모든 페이지를 볼 수 있습니다.</p></div>
  <div class="at-footer-cols">
    <div><p>생활툴</p><ul>{groups}</ul></div>
    <div><p>맛집</p><ul>{regions}<li><a href="/food.html">전체 지역</a></li></ul></div>
    <div><p>여행</p><ul>{trips}</ul></div>
    <div><p>가이드</p><ul><li><a href="/guide_2026_wage.html">2026 노동법 변경</a></li><li><a href="/guide_2026_tax.html">2026 세금 가이드</a></li><li><a href="/etc.html">텍스트 도구</a></li><li><a href="/search.html">검색</a></li></ul></div>
    <div><p>추천 모음</p><ul>{shop_links}<li><a href="/connect.html">추천 모음 전체</a></li></ul></div>
  </div>
  <div class="at-footer-legal">
    <nav aria-label="정책"><a href="/privacy.html">개인정보처리방침</a><a href="/terms.html">이용약관</a><a href="/about.html">사이트 소개</a><a href="/editorial.html">편집 방침</a><a href="/contact.html">문의하기</a><a href="/sitemap.html">사이트맵</a></nav>
    <small class="at-foot-visitors" data-visitors hidden>방문자 오늘 <b data-v="today">-</b> · 전체 <b data-v="total">-</b></small>
    <small>© 2026 {NAME}. 계산 결과와 지역 정보는 참고용이며 법적 효력이 없습니다.</small>
  </div>
</div></footer>"""


# ── 추천 모음 홍보: 페이지 주제와 맞는 추천 글을 사이트 곳곳에 연결 ──
SHOP_TOPIC_BY_SLUG = {
    "electricity_bill_calculator": ["bespoke-ai-fridge-4door", "bespoke-ai-steam-ultra", "food-waste-disposer", "jbl-authentics-200"],
    "gas_bill_calculator": ["bespoke-ai-fridge-4door", "food-waste-disposer", "bespoke-ai-steam-ultra"],
    "interior_calculator": ["bespoke-ai-fridge-4door", "bespoke-ai-steam-ultra", "food-waste-disposer", "jbl-authentics-200"],
    "pyeong_calculator": ["bespoke-ai-fridge-4door", "bespoke-ai-steam-ultra", "food-waste-disposer"],
    "acquisition_tax_calculator": ["bespoke-ai-fridge-4door", "bespoke-ai-steam-ultra", "food-waste-disposer"],
    "brokerage_fee_calculator": ["bespoke-ai-fridge-4door", "bespoke-ai-steam-ultra", "food-waste-disposer"],
    "bmi_calculator": ["calf-foot-air-massager", "neck-traction", "mung-bean-cleanser", "queens-collagen-rg3"],
    "bmr_calculator": ["calf-foot-air-massager", "neck-traction", "queens-collagen-rg3"],
    "calorie_calculator": ["calf-foot-air-massager", "food-waste-disposer", "neck-traction"],
    "due_date_calculator": ["calf-foot-air-massager", "mung-bean-cleanser", "queens-collagen-rg3"],
    "age_calculator": ["queens-collagen-rg3", "prael-thermashot-ultimate", "calf-foot-air-massager"],
    "discount_calculator": ["galaxy-s26-ultra", "galaxy-tab-s12-ultra", "bespoke-ai-fridge-4door", "student-office-laptop"],
    "discount_rate_calculator": ["galaxy-s26-ultra", "galaxy-tab-s12-ultra", "bespoke-ai-steam-ultra", "student-office-laptop"],
    "percent_calculator": ["galaxy-s26-ultra", "student-office-laptop", "c-type-65w-charger"],
    "dutch_pay_calculator": ["fukuoka-3days", "danang-5days", "west-europe-3-10days"],
    "exchange_rate_calculator": ["fukuoka-3days", "danang-5days", "west-europe-3-10days"],
    "japan_travel_calculator": ["fukuoka-3days", "danang-5days", "west-europe-3-10days", "c-type-65w-charger"],
    "fuel_economy_calculator": ["fukuoka-3days", "danang-5days", "c-type-65w-charger"],
    "camping_gear_calculator": ["jbl-authentics-200", "c-type-65w-charger", "danang-5days"],
    "character_counter": ["student-office-laptop", "wireless-gaming-keyboard", "galaxy-tab-s12-ultra"],
    "spell_checker": ["student-office-laptop", "wireless-gaming-keyboard", "galaxy-tab-s12-ultra"],
    "spacing_checker": ["student-office-laptop", "wireless-gaming-keyboard", "galaxy-tab-s12-ultra"],
    "hourly_monthly_wage_calculator": ["student-office-laptop", "c-type-65w-charger", "galaxy-s26-ultra"],
    "job_fortune_teller": ["student-office-laptop", "wireless-gaming-keyboard", "c-type-65w-charger"],
    "qr_generator": ["c-type-65w-charger", "galaxy-s26-ultra", "student-office-laptop"],
    "travel-osaka.html": ["fukuoka-3days", "danang-5days", "west-europe-3-10days"],
}
SHOP_TOPIC_BY_GROUP = {
    "money": ["galaxy-s26-ultra", "bespoke-ai-fridge-4door", "galaxy-tab-s12-ultra", "student-office-laptop"],
    "labor": ["student-office-laptop", "neck-traction", "galaxy-s26-ultra", "c-type-65w-charger"],
    "life": ["food-waste-disposer", "c-type-65w-charger", "calf-foot-air-massager", "mung-bean-cleanser"],
    "trip": ["fukuoka-3days", "danang-5days", "west-europe-3-10days"],
    "text": ["student-office-laptop", "wireless-gaming-keyboard"],
}
SHOP_TOPIC_BY_SECTION = {
    "food": ["food-waste-disposer", "bespoke-ai-fridge-4door", "fukuoka-3days", "danang-5days"],
    "gu": ["food-waste-disposer", "bespoke-ai-fridge-4door", "fukuoka-3days", "danang-5days"],
    "hub-food": ["food-waste-disposer", "bespoke-ai-fridge-4door", "fukuoka-3days", "danang-5days"],
    "trip": ["fukuoka-3days", "danang-5days", "west-europe-3-10days", "c-type-65w-charger"],
    "hub-trip": ["fukuoka-3days", "danang-5days", "west-europe-3-10days", "c-type-65w-charger"],
    "guide": ["student-office-laptop", "neck-traction", "galaxy-s26-ultra", "galaxy-tab-s12-ultra"],
    "hub-guide": ["student-office-laptop", "neck-traction", "galaxy-s26-ultra", "galaxy-tab-s12-ultra"],
}
SHOP_PROMO_SKIP = {"connect", "hub-connect", "info", "util", "home"}


def shop_thumb(post):
    """추천 글 대표 사진의 작은 썸네일(가로 320px)을 만들어 주소를 돌려줍니다."""
    cp = post.get("cta_photo") or {}
    src = cp.get("src") or (post.get("images") or [("", "")])[0][0]
    if not src or not src.startswith("/"):
        return src, None
    full = src.lstrip("/")
    th = os.path.join(os.path.dirname(full), "thumb.jpg")
    try:
        if not os.path.exists(th) or os.path.getmtime(th) < os.path.getmtime(full):
            from PIL import Image
            im = Image.open(full).convert("RGB")
            w = 320
            im = im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)
            im.save(th, "JPEG", quality=72, optimize=True, progressive=True)
        from PIL import Image as _I
        with _I.open(th) as im2:
            return "/" + th, im2.size
    except Exception:
        return src, None


def shop_pick(p, n=4):
    by_slug = {q["post"]["slug"]: q for q in SHOP_LIVE}
    f = p["file"]
    want = SHOP_TOPIC_BY_SLUG.get(f[:-5]) or SHOP_TOPIC_BY_SLUG.get(f)
    if not want and p["section"] == "tools":
        want = SHOP_TOPIC_BY_GROUP.get(p.get("group"))
    if not want:
        want = SHOP_TOPIC_BY_SECTION.get(p["section"], [])
    out = [by_slug[s] for s in want if s in by_slug]
    for q in SHOP_LIVE:  # 최신 글로 채움
        if len(out) >= n:
            break
        if q not in out:
            out.append(q)
    return out[:n]


def shop_card(q, heading="h3"):
    post = q["post"]
    src, wh = shop_thumb(post)
    alt = (post.get("cta_photo") or {}).get("alt") or post["title"]
    size = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    img = f'<img src="{esc(src)}" alt="{esc(alt)}"{size} loading="lazy" decoding="async">' if src else ""
    return (f'<li><a class="at-sp-card" href="/{q["file"]}"><span class="at-sp-img">{img}</span>'
            f'<span class="at-sp-k">{esc(KINDS[kind_of(q)])}</span><{heading} class="at-sp-t">{esc(q["title"])}</{heading}>'
            f'<span class="at-sp-x">{esc(post["keyword"])}</span></a></li>')


def shop_promo_html(p, n=4, title="추천 모음에서 함께 보면 좋은 글"):
    if not SHOP_LIVE or p["section"] in SHOP_PROMO_SKIP or p["file"] in ("index.html", "search.html", "404.html", "connect.html",
                                                                        "privacy.html", "terms.html", "contact.html", "about.html", "editorial.html", "sitemap.html"):
        return ""
    cards = "".join(shop_card(q) for q in shop_pick(p, n))
    return (f'<section class="at-related at-shop-promo" aria-label="추천 모음">'
            f'<div class="at-box-head"><h2>{esc(title)}</h2><a class="more" href="/connect.html">추천 모음 전체</a></div>'
            f'<ul class="at-sp-grid">{cards}</ul>'
            f'</section>')


def top_block(p, board=True):
    return (f"<!-- at:top -->\n{header_html(p)}\n<div class=\"at-wrap\">\n{crumb_html(p)}\n"
            f"<div class=\"at-layout\">\n<div class=\"at-content\" id=\"at-main\" tabindex=\"-1\">\n"
            f"{board_html(p) if board else ''}\n<!-- /at:top -->")


def bottom_block(p):
    return (f"<!-- at:bottom -->\n{shop_promo_html(p)}\n{related_html(p)}\n{cross_html(p)}\n</div>\n{side_html()}\n</div>\n</div>\n{footer_html()}\n"
            f'<script src="/assets/site.js?v={JS_V}" defer></script>\n<!-- /at:bottom -->')


# ════════════════════════════════════════════════════════════════
# 5. <head>
# ════════════════════════════════════════════════════════════════

OG_IMG = {"food": "og-food.png", "hub-food": "og-food.png", "tools": "og-tools.png", "hub-tools": "og-tools.png",
          "trip": "og-trip.png", "hub-trip": "og-trip.png"}


def page_ld(p, extra=None):
    f = p["file"]
    u = url_of(f)
    graph = []
    typ = {"hub-food": "CollectionPage", "hub-tools": "CollectionPage", "hub-trip": "CollectionPage",
           "hub-guide": "CollectionPage", "hub-connect": "CollectionPage", "gu": "CollectionPage"}.get(p["section"], "WebPage")
    if f == "about.html":
        typ = "AboutPage"
    if f == "contact.html":
        typ = "ContactPage"
    if f == "search.html":
        typ = "SearchResultsPage"
    wp = {"@type": typ, "@id": u + "#webpage", "url": u, "name": p["title"], "description": p["desc"],
          "inLanguage": "ko-KR", "isPartOf": {"@id": SITE + "/#website"},
          "publisher": {"@id": SITE + "/#org"}, "dateModified": p["date"],
          "primaryImageOfPage": image_ld("/assets/og/og-default.png", "어라운드툴 대표 이미지")}
    bc = crumb_ld(p)
    if bc:
        wp["breadcrumb"] = {"@id": u + "#breadcrumb"}
        bc["@id"] = u + "#breadcrumb"
        graph.append(bc)
    graph.insert(0, wp)
    if extra:
        graph += extra
    return {"@context": "https://schema.org", "@graph": graph}


def head_block(p, robots=None):
    f = p["file"]
    u = url_of(f)
    title = p["title"] if f == "index.html" else f"{p['title']} | {NAME}"
    desc = p["desc"]
    img = f"{SITE}/assets/og/og-default.png"
    if robots is None:
        robots = "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" if indexable(p) else "noindex, follow"
    og_type = "article" if p["section"] in ("food", "trip", "guide", "connect") else "website"
    return f"""<!-- at:head -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{u}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0B6E5F">
<meta name="naver-site-verification" content="{NAVER_VERIFY}">
<meta name="google-adsense-account" content="{ADSENSE}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="ko_KR">
<meta property="og:url" content="{u}">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p['title'])}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">
<meta property="article:modified_time" content="{p['date']}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{NAME}" href="{SITE}/feed.xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<!-- /at:head -->"""


def assets_block(p, ld_obj, adsense=False):
    ads = (f'\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>'
           if adsense else "")
    return f"""<!-- at:assets -->
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
{ld(ld_obj)}
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>{ads}
<!-- /at:assets -->"""


def faq_ld(pairs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
        for q, a in pairs]}


# ════════════════════════════════════════════════════════════════
# 6. 기존 페이지 변환 (본문 보존 + 공통 영역 교체)
# ════════════════════════════════════════════════════════════════

FONT_FIX = [('"Gowun Batang",serif', 'var(--at-font)'), ("'Gowun Batang',serif", 'var(--at-font)'),
            ('"IBM Plex Sans KR"', '"Pretendard Variable",Pretendard'),
            ("'IBM Plex Sans KR'", '"Pretendard Variable",Pretendard')]


def split_jsonld(blocks):
    """기존 페이지 JSON-LD에서 BreadcrumbList·WebSite·Organization 을 걷어내고 나머지만 남김."""
    keep, has_faq = [], False
    for raw in blocks:
        try:
            data = json.loads(raw)
        except Exception:
            keep.append(raw)
            continue
        def ok(n):
            return isinstance(n, dict) and n.get("@type") not in ("BreadcrumbList", "WebSite", "Organization")
        if isinstance(data, dict) and "@graph" in data:
            data["@graph"] = [n for n in data["@graph"] if ok(n)]
            if not data["@graph"]:
                continue
            nodes = data["@graph"]
        elif isinstance(data, dict):
            if not ok(data):
                continue
            nodes = [data]
        else:
            nodes = data
        if any(isinstance(n, dict) and n.get("@type") == "FAQPage" for n in nodes):
            has_faq = True
        keep.append(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    return keep, has_faq


def html_faq_pairs(body):
    soup = BeautifulSoup(body, "html.parser")
    pairs = []
    for d in soup.find_all("details"):
        sm = d.find("summary")
        if not sm:
            continue
        q = sm.get_text(" ", strip=True)
        sm.extract()
        a = d.get_text(" ", strip=True)
        if q and a and len(a) > 10:
            pairs.append((q, a))
    return pairs


# 페이지별 사진: scripts/photo_map.json  {"파일.html": ["사진 이름", ...]}
#   기존 페이지(맛집·여행·가이드)는 1번째·3번째 <h2> 앞에, 계산기·지역 허브는 핵심 답변 아래에 들어갑니다.
try:
    PHOTO_MAP = json.load(open(os.path.join(_ROOT, "scripts", "photo_map.json"), encoding="utf-8"))
except FileNotFoundError:
    PHOTO_MAP = {}


def page_photo_block(f):
    names = [n for n in PHOTO_MAP.get(f, []) if photo_ok(n)]
    return "".join(photo_html(n) for n in names[:1]), [image_ld(f"/assets/photos/{n}.jpg", PHOTOS[n]["alt"], PHOTOS[n]) for n in names[:1]]


def inject_page_photos(f, body):
    """<!-- at:photo --> 블록을 지우고 다시 넣습니다(여러 번 빌드해도 같은 결과)."""
    body = re.sub(r"<!-- at:photo -->.*?<!-- /at:photo -->\n?", "", body, flags=re.S)
    names = [n for n in PHOTO_MAP.get(f, []) if photo_ok(n)]
    start = body.find("</h1>") + 1
    if PAGES.get(f, {}).get("section") == "tools":
        # 직접 만든 계산기 화면 안에도 <h2>가 있어서, '자주 묻는 질문' 앞에 넣습니다.
        spots = [m.start() for m in re.finditer(r"<h2[^>]*>\s*자주 묻는 질문", body)]
    else:
        spots = [m.start() for m in re.finditer(r"<h2[\s>]", body) if m.start() > start]
    placed = []
    for k, name in reversed(list(enumerate(names))):
        idx = k * 2
        if idx < len(spots):
            body = body[:spots[idx]] + f"<!-- at:photo -->{photo_html(name)}<!-- /at:photo -->\n" + body[spots[idx]:]
            placed.append(name)
    return body, [image_ld(f"/assets/photos/{n}.jpg", PHOTOS[n]["alt"], PHOTOS[n]) for n in reversed(placed)]


def transform_existing(p):
    f = p["file"]
    s = read(f)
    if "<!-- at:head -->" in s:
        # 이미 변환된 페이지: 보존 영역 추출
        preserved = re.search(r"<!-- /at:head -->(.*?)<!-- at:assets -->", s, re.S).group(1).strip()
        body = re.search(r"<!-- /at:top -->(.*?)<!-- at:bottom -->", s, re.S).group(1).strip()
        body_attr = re.search(r"<body([^>]*)>", s).group(1)
    else:
        head = re.search(r"<head[^>]*>(.*?)</head>", s, re.S).group(1)
        styles = re.findall(r"<style[^>]*>.*?</style>", head, re.S)
        links = [l for l in re.findall(r"<link[^>]+>", head) if 'rel="stylesheet"' in l and "fonts.googleapis" not in l]
        lds = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', head, re.S)
        keep_ld, _ = split_jsonld(lds)
        css = "\n".join(styles)
        for a, b in FONT_FIX:
            css = css.replace(a, b)
        links = [l.replace('href="style.css"', 'href="/style.css"') for l in links]
        preserved = "\n".join(links + [css] + [f'<script type="application/ld+json">{x}</script>' for x in keep_ld])
        m = re.search(r"<body([^>]*)>(.*)</body>", s, re.S)
        body_attr, body_html = m.group(1), m.group(2)
        soup = BeautifulSoup(body_html, "html.parser")
        tops = [c for c in soup.contents if getattr(c, "name", None)]
        # 첫 헤더(사이트 상단)와 마지막 푸터 제거
        if tops and (tops[0].name == "header" or "masthead" in (tops[0].get("class") or [])):
            tops[0].decompose()
        tops = [c for c in soup.contents if getattr(c, "name", None)]
        foot = [c for c in tops if c.name == "footer"]
        if foot:
            foot[-1].decompose()
        for sc in soup.find_all("script", src=re.compile("common_head")):
            sc.decompose()
        for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
            if "at:" in c:
                c.extract()
        body = str(soup).strip()
        for a, b in FONT_FIX:
            body = body.replace(a, b)
    body, photo_lds = inject_page_photos(f, body)
    # 직접 만든 계산기 페이지에도 '관련 가이드' 연결 (자주 묻는 질문 앞)
    body = re.sub(r"<!-- at:guides -->.*?<!-- /at:guides -->\n?", "", body, flags=re.S)
    # 직접 만든 계산기: 사용 방법 3~4단계 + 참고용·개인정보 안내 (+ HowTo 구조화 데이터)
    body = re.sub(r"<!-- at:howto -->.*?<!-- /at:howto -->\n?", "", body, flags=re.S)
    howto_ld = None
    if p.get("section") == "tools" and f[:-5] in LEGACY_STEPS:
        steps = LEGACY_STEPS[f[:-5]]
        lis = "".join(f"<li>{s}</li>" for s in steps)
        blk = (f'<!-- at:howto --><section class="at-prose" style="margin:1.5rem auto"><h2>이렇게 쓰세요</h2>'
               f'<ol class="at-steps">{lis}</ol><p class="at-note">{LEGACY_NOTE}</p></section><!-- /at:howto -->\n')
        m = re.search(r"<h2[^>]*>\s*(관련 가이드|자주 묻는 질문)", body)
        body = body[:m.start()] + blk + body[m.start():] if m else body + blk
        howto_ld = {"@type": "HowTo", "name": f"{p.get('name') or strip_tags(p.get('title', ''))} 사용 방법",
                    "step": [{"@type": "HowToStep", "position": i + 1, "text": strip_tags(s)} for i, s in enumerate(steps)]}
    if p.get("section") == "tools":
        gl = guide_links_for(f[:-5])
        if gl:
            blk = f'<!-- at:guides --><section class="at-prose" style="margin:1.5rem auto">{gl}</section><!-- /at:guides -->\n'
            m = re.search(r"<h2[^>]*>\s*자주 묻는 질문", body)
            body = body[:m.start()] + blk + body[m.start():] if m else body + blk
    # 맛집 게시판의 짧은 H1('밥집', '갈치')에 지역명을 붙여 검색어와 맞춥니다 (한 번만 적용).
    if p.get("section") == "food" and p.get("gu"):
        def _h1(m):
            x = m.group(1).strip()
            if p["gu"] in x or len(x) > 10:
                return m.group(0)
            tail = "" if x.endswith("집") else " 맛집"
            return f"<h1>{p['region_short']} {p['gu']} {x}{tail}</h1>"
        body = re.sub(r"<h1>([^<]{1,12})</h1>", _h1, body, count=1)
    # 맛집 게시판: 이 페이지에 실린 가게 목록·조사 기준·선정 기준을 묻는 질문 (본문에 이미 있는 사실만)
    body = re.sub(r"<!-- at:ffaq -->.*?<!-- /at:ffaq -->\n?", "", body, flags=re.S)
    if p.get("section") == "food" and "FAQPage" in preserved:
        # 페이지 고유 FAQ 구조화 데이터는 빼고, 아래에서 본문 질문 전체로 다시 만듭니다 (화면과 개수 일치).
        def _drop_faq(m):
            try:
                d = json.loads(m.group(1))
            except ValueError:
                return m.group(0)
            if isinstance(d, dict) and "@graph" in d:
                d["@graph"] = [o for o in d["@graph"] if not (isinstance(o, dict) and o.get("@type") == "FAQPage")]
                return f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>'
            if isinstance(d, dict) and d.get("@type") == "FAQPage":
                return ""
            return m.group(0)
        preserved = re.sub(r'<script type="application/ld\+json">(.*?)</script>', _drop_faq, preserved, flags=re.S)
    if p.get("section") == "food" and not p.get("research") and p.get("cat"):
        bs = BeautifulSoup(body, "html.parser")
        names = []
        for art_ in bs.select("article.entry, article[class*=entry]"):
            hd = art_.find(["h2", "h3"])
            if hd and hd.get_text(strip=True):
                names.append(re.sub(r"\s+", " ", hd.get_text(" ", strip=True)))
        if not names:
            names = re.findall(r'"@type"\s*:\s*"Restaurant"[^{}]*?"name"\s*:\s*"([^"]+)"', read(f))
        names = list(dict.fromkeys(names))[:8]
        area = f"{p['region_short']} {p['gu']}"
        qs = []
        if names:
            qs.append((f"{area} {p['cat']}{'' if p['cat'].endswith('집') else ' 맛집'}은 어디가 있나요?",
                       f"이 페이지에는 {', '.join(esc(n) for n in names)}{' 등' if len(names) >= 8 else ''} {len(names)}곳을 정리했습니다. "
                       "곳마다 대표 메뉴와 선정 근거, 아쉬운 점을 함께 적었습니다."))
        qs.append(("가격과 영업시간은 언제 기준인가요?",
                   f"{int(BASE_DATE[:4])}년 {int(BASE_DATE[5:7])}월 조사 기준입니다. 바뀌었을 수 있으니 방문 전 가게 공지나 지도 앱에서 확인하세요."))
        qs.append(("맛집은 어떤 기준으로 골랐나요?",
                   "리뷰 개수보다 재방문 언급을 보고, 다이닝코드 지역 랭킹·미쉐린 가이드·백년가게·지자체 지정처럼 광고비로 살 수 없는 근거와 "
                   "교차 확인했습니다. 협찬·체험단 글은 근거에서 뺐습니다. 자세한 기준은 <a href=\"/editorial.html\">편집 방침</a>에 있습니다."))
        have = body
        qs = [(q, a) for q, a in qs if q not in have]
        if qs:
            items = "".join(f"<details><summary>{q}</summary><div class=\"a\"><p>{a}</p></div></details>" for q, a in qs)
            blk = f'<!-- at:ffaq --><section class="at-prose" style="margin:1.5rem auto"><h2>자주 묻는 질문</h2><div class="at-faq">{items}</div></section><!-- /at:ffaq -->\n'
            m = re.search(r"<h2[^>]*>[^<]*(다른 맛집 기록|함께 보면|함께 보기)", body)
            if "<details" in body:
                # 이미 FAQ가 있으면 그 목록 끝에 덧붙임
                if 'class="ans"' in body:
                    items = "".join(f'<details><summary>{q}</summary>\n<div class="ans">{a}</div></details>' for q, a in qs)
                i = body.rfind("</details>") + len("</details>")
                body = body[:i] + "<!-- at:ffaq -->" + items + "<!-- /at:ffaq -->" + body[i:]
            else:
                body = body[:m.start()] + blk + body[m.start():] if m else body + blk
    # 구조화 데이터: 페이지 고유 JSON-LD 에 FAQ가 없으면 본문 <details>로 생성
    has_faq = "FAQPage" in preserved
    extra = list(photo_lds)
    if howto_ld and '"HowTo"' not in preserved:
        extra.append(howto_ld)
    if not has_faq:
        pairs = html_faq_pairs(body)
        if pairs:
            extra.append(faq_ld(pairs))
    body_attr = re.sub(r'\sclass="[^"]*"', "", body_attr)
    out = f"""<!DOCTYPE html>
<html lang="ko">
<head>
{head_block(p)}
{preserved}
{assets_block(p, page_ld(p, extra))}
</head>
<body{body_attr}>
{top_block(p)}
{body}
{bottom_block(p)}
</body>
</html>
"""
    write(f, out)


# ════════════════════════════════════════════════════════════════
# 7. 새로 만드는 페이지
# ════════════════════════════════════════════════════════════════

def page_shell(p, content, extra_ld=None, board=True, adsense=False, robots=None, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
{head_block(p, robots)}
{extra_head}
{assets_block(p, page_ld(p, extra_ld), adsense)}
</head>
<body>
{top_block(p, board)}
<main>
{content}
</main>
{bottom_block(p)}
</body>
</html>
"""


def faq_html(pairs, title="자주 묻는 질문"):
    items = "".join(f"<details><summary>{esc(q)}</summary><div class=\"a\"><p>{a}</p></div></details>" for q, a in pairs)
    return f'<h2 id="faq">{title}</h2><div class="at-faq">{items}</div>'


EMBED_H = {"character_counter": 620, "spell_checker": 720, "spacing_checker": 640, "percent_calculator": 420,
           "pyeong_calculator": 330, "exchange_rate_calculator": 640, "freelancer_tax_calculator": 760,
           "lotto_generator": 560, "qr_generator": 640, "loan_calculator": 720, "electricity_bill_calculator": 720}


def build_embed(slug, tool, head_css, ext_scripts):
    c = CALCS[slug]
    u = url_of(slug + ".html")
    write(f"embed/{slug}.html", f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(c['h1'])} | {NAME}</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{u}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
<style>body{{background:#fff!important}}.at-tool{{margin:0;max-width:none;border-radius:8px}}
.at-embed-credit{{margin:.6rem 0 0;font-size:.8125rem;color:var(--at-sub);text-align:right}}
.at-embed-credit a{{color:var(--at-ink);font-weight:700;text-decoration:none}}.at-embed-credit a:hover{{text-decoration:underline}}</style>
{head_css}
{chr(10).join(ext_scripts)}
</head>
<body style="padding:8px">
<section class="at-tool" aria-label="{esc(c['h1'])}">
<p style="margin:0 0 1rem;font-weight:800;font-size:1.0625rem">{esc(c['h1'])}</p>
{tool}
</section>
<p class="at-embed-credit">계산기 제공 <a href="{u}" target="_blank" rel="noopener">{NAME} {esc(c['h1'])}</a></p>
</body>
</html>
""")


def embed_box(slug):
    c = CALCS[slug]
    h = EMBED_H.get(slug, 560)
    code = (f'<iframe src="{SITE}/embed/{slug}.html" title="{c["h1"]}" width="100%" height="{h}" '
            f'style="border:0;max-width:640px" loading="lazy"></iframe>\n'
            f'<p style="font-size:13px">출처: <a href="{url_of(slug + ".html")}">{NAME} {c["h1"]}</a></p>')
    return f"""<h2 id="embed">이 계산기를 내 블로그·홈페이지에 넣기</h2>
<p>아래 코드를 복사해 HTML 편집 화면에 붙여 넣으면 계산기가 그대로 들어갑니다. 무료이며, 출처 링크만 지워지지 않게 두면 됩니다. 티스토리·워드프레스·개인 홈페이지에서 쓸 수 있고, 네이버 블로그는 외부 코드를 막아 두어 링크로 공유하는 편이 좋습니다.</p>
<div class="at-embed"><textarea id="embed-code" readonly rows="4" aria-label="퍼가기 코드">{esc(code)}</textarea>
<button type="button" class="at-copy" data-copy="embed-code">코드 복사</button></div>"""


def build_calc(slug):
    c = CALCS[slug]
    p = PAGES[slug + ".html"]
    tool = read(f"src/tools/{slug}.html")
    head_css = ""
    m = re.match(r"\s*(<style>.*?</style>)", tool, re.S)
    if m:
        head_css = m.group(1)
        tool = tool[m.end():]
    ext_scripts = re.findall(r'<script[^>]+src="[^"]+"[^>]*>\s*</script>', tool)
    for x in ext_scripts:
        tool = tool.replace(x, "")
    steps = "".join(f"<li>{s}</li>" for s in c["steps"])
    formula = f'<h2>계산 방법</h2><div class="at-formula">{c["formula"]}</div>' if c.get("formula") else ""
    related = "".join(f'<li><a href="/{r}.html">{esc(PAGES[r + ".html"]["name"])} 계산기</a> — {esc(PAGES[r + ".html"]["desc"][:60].rsplit(" ", 1)[0])}…</li>'
                      for r in c["related"] if r + ".html" in PAGES)
    g = p["group_name"]
    photo_blk, photo_ld = page_photo_block(p["file"])
    content = f"""<article itemscope itemtype="https://schema.org/WebApplication">
<header class="at-page-head">
  <h1 itemprop="name">{esc(c['h1'])}</h1>
  <p class="lede" itemprop="description">{esc(c['lede'])}</p>
  <p class="meta"><span>생활툴 · {esc(g)}</span><span>최종 수정 <time datetime="{p['date']}">{p['date'].replace('-', '.')}</time></span><span>로그인 없이 무료</span></p>
</header>
<div class="at-page">
<section class="at-tool" aria-label="{esc(c['h1'])}">
{tool.strip()}
</section>
<div class="at-prose">
<div class="at-answer"><p>{c['answer']}</p></div>
{photo_blk}
<h2>사용 방법</h2>
<ol class="at-steps">{steps}</ol>
{formula}
{c.get('body', '')}
{faq_html(c['faq'])}
{guide_links_for(slug)}
<h2>함께 보면 좋은 계산기</h2>
<ul>{related}</ul>
{embed_box(slug)}
<p class="at-note">계산 결과는 입력값과 일반적인 기준을 바탕으로 한 참고용 추정치이며 법적 효력이 없습니다. 입력값은 브라우저 안에서만 처리되고 저장·전송되지 않습니다. 오류를 발견하면 <a href="/contact.html">문의하기</a>로 알려 주세요.</p>
</div>
</div>
</article>"""
    app = {"@type": "WebApplication", "name": c["h1"], "url": url_of(p["file"]), "description": c["desc"],
           "applicationCategory": c["cat"], "operatingSystem": "All", "inLanguage": "ko-KR",
           "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"},
           "publisher": {"@id": SITE + "/#org"}}
    if photo_ld:
        app["image"] = photo_ld[0]
    howto = {"@type": "HowTo", "name": f"{c['h1']} 사용 방법",
             "step": [{"@type": "HowToStep", "position": i + 1, "text": strip_tags(s)} for i, s in enumerate(c["steps"])]}
    extra_head = head_css + "\n" + "\n".join(ext_scripts)
    build_embed(slug, tool.strip(), head_css, ext_scripts)
    write(p["file"], page_shell(p, content, [app, howto, faq_ld(c["faq"])], adsense=True, extra_head=extra_head))


def tag_for(p):
    s = p["section"]
    if s == "food":
        return p["region_short"], "food"
    if s == "tools":
        return "생활툴", ""
    if s == "trip":
        return "여행", "trip"
    if s == "guide":
        return "가이드", "etc"
    return "안내", "etc"


# ── 추천 모음 (브랜드 커넥트 · 쇼핑 커넥트) ──────────────────────

def disclosure_box(post, where="top"):
    text = DISCLOSURE.get(post.get("program", "shopping"), DISCLOSURE["shopping"])
    if where == "top":
        return f'<aside class="at-disclose" role="note" aria-label="광고 표시"><p>{esc(text)}</p></aside>'
    return f'<p class="at-disclose-sm"><b>광고</b> {esc(text)}</p>'


def buy_button(post, label=None):
    label = label or f"{post['product']} 판매 페이지 보기"
    return (f'<p class="at-buy"><a class="at-buy-btn" href="{esc(post.get("direct") or post["link"])}"{web_attr(post)} target="_blank" '
            f'rel="sponsored nofollow noopener">{esc(label)}</a>'
            f'<span>광고 링크 · 구매 시 사이트가 수수료를 받으며, 구매자가 내는 가격은 같습니다.</span></p>')


def cta_label(post):
    """버튼 문구: 제품은 '제품 가격 알아보기 >>', 여행은 '여행 비용 알아보기 >>'."""
    return "여행 비용 알아보기 >>" if post.get("kind") == "travel" else "제품 가격 알아보기 >>"


def link_card(post):
    """제휴 링크 버튼: 빨간 바탕·흰 글씨, 은은하게 깜빡이는 강조."""
    label = cta_label(post)
    return (f'<a class="at-cta" href="{esc(post.get("direct") or post["link"])}"{web_attr(post)} target="_blank" rel="sponsored nofollow noopener">'
            f'{esc(label)}</a>')


def popup_html(post):
    """6초 이상 읽으면 뜨는 '제품 가격 알아보기' 팝업 (assets/site.js 가 띄움)."""
    is_trip = post.get("kind") == "travel"
    head = "여행 코스가 궁금하다면?" if is_trip else "이 제품, 직접 확인해 볼까요?"
    sub = post.get("cta_hook") or ("일정·가격·포함 내역을 한 번에 볼 수 있어요." if is_trip else "현재 가격과 옵션, 상세 정보를 바로 볼 수 있어요.")
    label = cta_label(post)
    d = DISCLOSURE.get(post.get("program", "shopping"), DISCLOSURE["shopping"])
    cp = post.get("cta_photo")
    pop_visual = (f'<div class="at-pop-imgbox"><img class="at-pop-img" src="{esc(cp["src"])}" alt="{esc(cp["alt"])}" width="320" height="180" loading="lazy" decoding="async"></div>' if cp
                  else f'<p class="at-pop-emoji" aria-hidden="true">{"✈️" if is_trip else "🎁"}</p>')
    return f"""<div class="at-pop" data-at-popup="{esc(post['slug'])}" hidden>
  <div class="at-pop-back" data-pop-close></div>
  <div class="at-pop-box" role="dialog" aria-modal="true" aria-labelledby="at-pop-h">
    <button type="button" class="at-pop-x" data-pop-close aria-label="닫기">×</button>
    {pop_visual}
    <p class="at-pop-h" id="at-pop-h">{esc(head)}</p>
    <p class="at-pop-s">{esc(sub)}</p>
    <a class="at-cta" href="{esc(post.get('direct') or post['link'])}"{web_attr(post)} target="_blank" rel="sponsored nofollow noopener" data-pop-go>{esc(label)}</a>
    <button type="button" class="at-pop-later" data-pop-close>계속 읽을게요</button>
    <p class="at-pop-ad">광고 · {esc(d)}</p>
  </div>
</div>"""


def web_url(post):
    """브랜드 커넥트 연결 페이지의 '웹으로 보기'와 같은 주소(서버 리디렉트, 제휴 추적 포함).
    휴대폰에서 이 주소로 바로 이동하면 앱 선택창 없이 상품 페이지가 열립니다."""
    d = post.get("direct") or ""
    m = re.match(r"https://brandconnect\.naver\.com/affiliates/(\d+)\?channelProductNo=(\d+)", d)
    if m:
        return (f"https://gw-brandconnect.naver.com/affiliate/query/redirect/{m.group(1)}"
                f"?channelProductNo={m.group(2)}&originAccessLogChannel=UNKNOWN&ctid=&cid=")
    m = re.match(r"https://brandconnect\.naver\.com/connect/(\d+)", d)
    if m:
        return f"https://gw-brandconnect.naver.com/affiliate/query/connect-urls/{m.group(1)}/redirect"
    return ""


def web_attr(post):
    w = web_url(post)
    return f' data-web="{esc(w)}"' if w else ""


def top_photo(post):
    """대가성 문구 아래 첫 번째 버튼 바로 위 상품·여행 사진 (첫 화면이라 바로 불러옴)."""
    cp = post.get("cta_photo")
    if not cp:
        return ""
    wh = img_size(cp["src"])
    size = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    return (f'<figure class="vx-cta-photo vx-cta-top"><img src="{esc(cp["src"])}" alt="{esc(cp["alt"])}"{size} fetchpriority="high" decoding="async">'
            f'<figcaption>{esc(cp.get("caption", ""))}</figcaption></figure>')


def build_connect_blog(p):
    """블로그형 글: 소제목·표 없이 문단과 이미지 3장, 마무리 안내 + 구매 링크."""
    post = p["post"]
    imgs = post.get("images", [])
    parts, ld_imgs = [], []
    for para in post["body"]:
        m = re.fullmatch(r"\{img(\d)\}", para.strip())
        ph = re.fullmatch(r"\{photo:([\w-]+)\}", para.strip())
        if ph:
            name = ph.group(1)
            if photo_ok(name):
                parts.append(photo_html(name))
                ld_imgs.append(image_ld(f"/assets/photos/{name}.jpg", PHOTOS[name]["alt"], PHOTOS[name]))
        elif m:
            i = int(m.group(1)) - 1
            if i < len(imgs):
                src, alt = imgs[i]
                parts.append(figure_html(src, alt))
                ld_imgs.append(image_ld(src, alt))
        elif para.strip() == "{cta}":
            # 중간 버튼: 판매 페이지 사진은 넣지 않고, 무료 사진(mid_photo = photos.json 이름)이 있을 때만 넣음
            ph = ""
            mp = post.get("mid_photo")
            if mp and photo_ok(mp):
                ph = photo_html(mp).replace('class="at-fig"', 'class="at-fig vx-cta-photo"', 1)
                ld_imgs.append(image_ld(f"/assets/photos/{mp}.jpg", PHOTOS[mp]["alt"], PHOTOS[mp]))
            parts.append(f'<div class="vx-cta-mid">{ph}<p>{esc(post.get("cta_hook") or "가격과 옵션이 궁금하다면?")}</p>{link_card(post)}</div>')
        elif para.lstrip().startswith("<"):
            parts.append(para)
        else:
            parts.append(f"<p>{para}</p>")
    if post.get("cta_photo"):
        ld_imgs.insert(0, image_ld(post["cta_photo"]["src"], post["cta_photo"]["alt"], seller=post.get("brand") or "판매처"))
    closing = "".join(f"<p>{x}</p>" for x in post.get("closing", []))
    # 보강: 한눈에 보는 정리 표 + 자주 묻는 질문 + 이 글의 기준 (scripts/shop_extra.py)
    sx = SHOP_EXTRA.get(post["slug"], {})
    extra_html = ""
    if sx.get("summary"):
        st, head, rows = sx["summary"]
        th = "".join(f"<th>{esc(h)}</th>" for h in head)
        tr = "".join("<tr>" + f"<th>{esc(r[0])}</th>" + "".join(f"<td>{esc(c)}</td>" for c in r[1:]) + "</tr>" for r in rows)
        extra_html += f'<h2>{esc(st)}</h2><div class="at-table"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    if sx.get("faq"):
        extra_html += faq_html(sx["faq"])
    trust = TRUST_NOTE_TRAVEL if post.get("kind") == "travel" else TRUST_NOTE
    extra_html += f'<h2>이 글의 기준</h2><p class="at-note">{trust}</p>'
    content = f"""<article>
<header class="at-page-head">
  <h1>{esc(post['title'])}</h1>
  <p class="meta"><span>{esc(KINDS[kind_of(p)])} · 광고</span>{f"<span>{esc(post['brand'])}</span>" if post.get('brand') else ''}<span>작성 <time datetime="{p['date']}">{p['date'].replace('-', '.')}</time></span></p>
</header>
{disclosure_box(post)}
<div class="at-og-wrap">{top_photo(post)}{link_card(post)}</div>
<div class="at-page"><div class="at-prose at-blog">
{"".join(parts)}
{closing}
{extra_html}
{disclosure_box(post, 'bottom')}
{link_card(post)}
</div></div>
</article>
{popup_html(post)}"""
    art = {"@type": "BlogPosting", "headline": post["title"], "description": post["desc"], "inLanguage": "ko-KR",
           "datePublished": p["date"], "dateModified": max(post.get("updated", p["date"]), SHOP_UPDATED if post["slug"] in SHOP_EXTRA else ""), "author": {"@id": SITE + "/#org"},
           "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": url_of(p["file"]),
           "image": ld_imgs or [SITE + src if src.startswith("/") else src for src, _ in imgs],
           "keywords": ", ".join([post["keyword"]] + post.get("sub_keywords", []))}
    # Product 스키마는 가격·리뷰 없이 쓰면 구글에서 오류로 잡혀서, 글의 주제(about)로만 표시합니다.
    art["about"] = {"@type": "Thing", "name": post["product"]}
    extra = [art]
    if sx.get("faq"):
        extra.append(faq_ld(sx["faq"]))
    write(p["file"], page_shell(p, content, extra))


def guide_links_for(slug):
    """계산기 페이지에 붙일 '관련 가이드' 목록."""
    gs = [g for g in GUIDES if slug in g.get("tools", [])]
    if not gs:
        return ""
    li = "".join(f'<li><a href="/guide-{g["slug"]}.html">{esc(g["title"])}</a></li>' for g in gs)
    return f"<h2>관련 가이드</h2><ul>{li}</ul>"


def build_qguide(p):
    g = p["guide"]
    secs = "".join(f"<h2>{esc(h)}</h2>{html_}" for h, html_ in g["body"])
    tool_btns = "".join(
        f'<a class="at-guide-tool" href="/{s}.html"><b>{esc(PAGES[s + ".html"]["name"])}{"" if "계산" in PAGES[s + ".html"]["name"] or "검사" in PAGES[s + ".html"]["name"] else " 계산기"}</b>'
        f'<span>{esc(PAGES[s + ".html"]["desc"][:48].rsplit(" ", 1)[0])}…</span></a>'
        for s in g.get("tools", []) if s + ".html" in PAGES)
    src = "".join(f'<li><a href="{esc(u)}" rel="nofollow noopener" target="_blank">{esc(n)}</a></li>' for n, u in g.get("sources", []))
    others = "".join(f'<li><a href="/guide-{x["slug"]}.html">{esc(x["title"])}</a></li>' for x in GUIDES if x is not g)[:4000]
    content = f"""<article>
<header class="at-page-head">
  <h1>{esc(g['title'])}</h1>
  <p class="meta"><span>생활 가이드</span><span>작성 <time datetime="{p['date']}">{p['date'].replace('-', '.')}</time></span><span><a href="/editorial.html">편집 방침</a></span></p>
</header>
<div class="at-page"><div class="at-prose at-blog">
<div class="at-answer"><p>{g['answer']}</p></div>
{f'<div class="at-guide-tools">{tool_btns}</div>' if tool_btns else ''}
{secs}
{faq_html(g['faq']) if g.get('faq') else ''}
{f'<h2>근거 자료</h2><ul class="at-sources">{src}</ul>' if src else ''}
<h2>다른 생활 가이드</h2><ul>{others}</ul>
<p class="at-note">이 글은 작성일 기준 법령·공식 자료를 바탕으로 정리한 일반 안내이며, 개별 상황에 따라 다를 수 있습니다. 중요한 결정 전에는 관할 기관이나 전문가에게 확인하세요.</p>
</div></div>
</article>"""
    art = {"@type": "Article", "headline": g["title"], "description": g["desc"], "inLanguage": "ko-KR",
           "datePublished": p["date"], "dateModified": g.get("updated", p["date"]), "author": {"@id": SITE + "/#org"},
           "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": url_of(p["file"]),
           "image": image_ld("/assets/og/og-default.png", g["title"])}
    extra = [art] + ([faq_ld(g["faq"])] if g.get("faq") else [])
    write(p["file"], page_shell(p, content, extra))


def build_connect_post(p):
    post = p["post"]
    if post.get("body"):
        return build_connect_blog(p)
    price = ""
    if post.get("price"):
        pr = post["price"]
        price = f'<tr><th>판매가</th><td>{pr["value"]:,}원 <small>({pr["date"].replace("-", ".")} 확인, 할인·옵션에 따라 다름)</small></td></tr>'
    specs = "".join(f"<tr><th>{esc(k)}</th><td>{v}</td></tr>" for k, v in post.get("specs", []))
    sections = "".join(f"<h2>{esc(h)}</h2>{body}" for h, body in post.get("sections", []))
    fit = ""
    if post.get("fit_yes") or post.get("fit_no"):
        y = "".join(f"<li>{x}</li>" for x in post.get("fit_yes", []))
        n = "".join(f"<li>{x}</li>" for x in post.get("fit_no", []))
        fit = f'<h2>이런 분께 맞고, 이런 분께는 아닙니다</h2><div class="at-fit"><div><p>잘 맞는 경우</p><ul>{y}</ul></div><div><p>다시 생각해 볼 경우</p><ul>{n}</ul></div></div>'
    kind = "직접 사용해 본 기록" if post.get("hands_on") else "공식 상세페이지 정보를 정리한 글"
    content = f"""<article>
{disclosure_box(post)}
<header class="at-page-head">
  <h1>{esc(post['title'])}</h1>
  <p class="lede">{esc(post['lede'])}</p>
  <p class="meta"><span>{esc(KINDS[kind_of(p)])} · 광고</span><span>{esc(post['brand'])}</span><span>작성 <time datetime="{p['date']}">{p['date'].replace('-', '.')}</time></span><span>{kind}</span></p>
</header>
<div class="at-page"><div class="at-prose">
<div class="at-answer"><p>{post['answer']}</p></div>
<h2>{esc(post['product'])} 기본 정보</h2>
<div class="at-table"><table><tbody><tr><th>상품명</th><td>{esc(post['product'])}</td></tr><tr><th>브랜드</th><td>{esc(post['brand'])}</td></tr>{price}{specs}</tbody></table></div>
{buy_button(post)}
{sections}
{fit}
{faq_html(post.get('faq', [])) if post.get('faq') else ''}
{buy_button(post, '최신 가격과 옵션 확인하기')}
{disclosure_box(post, 'bottom')}
<p class="at-note">가격·구성·배송 조건은 판매처 사정에 따라 바뀔 수 있습니다. 구매 전 판매 페이지에서 최종 정보를 확인하세요. 이 글의 상품 정보는 작성일 기준 판매처 상세페이지를 바탕으로 정리했습니다.</p>
</div></div>
</article>"""
    art = {"@type": "Article", "headline": post["title"], "description": post["desc"], "inLanguage": "ko-KR",
           "datePublished": p["date"], "dateModified": p["date"], "author": {"@id": SITE + "/#org"},
           "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": url_of(p["file"]),
           "keywords": ", ".join([post["keyword"]] + post.get("sub_keywords", []))}
    prod = {"@type": "Product", "name": post["product"], "brand": {"@type": "Brand", "name": post["brand"]},
            "description": post["desc"]}
    if post.get("price"):
        prod["offers"] = {"@type": "Offer", "price": str(post["price"]["value"]), "priceCurrency": "KRW",
                          "url": post["link"], "availability": "https://schema.org/InStock"}
    extra = [art, prod] + ([faq_ld(post["faq"])] if post.get("faq") else [])
    write(p["file"], page_shell(p, content, extra))


CONNECT_FAQ = [
    ("직접 사용해 본 후기인가요?", "아닙니다. 제조사·판매처 공식 자료와 공개된 정보를 정리해 고르는 기준을 알려 드리는 글입니다."),
    ("가격은 어디서 확인하나요?", "각 글의 ‘제품 가격 알아보기’·‘여행 비용 알아보기’ 버튼을 누르면 판매 페이지에서 현재 가격을 볼 수 있습니다. 가격은 판매처와 시점마다 달라집니다."),
]


def build_connect_hub():
    p = PAGES["connect.html"]
    p["title"] = "추천 모음 — 제품 추천·여행 추천"
    p["desc"] = "제품을 고르는 기준과 여행 코스를 정리한 추천 글 모음입니다. 갤럭시·비스포크 가전·노트북·뷰티 디바이스부터 후쿠오카·다낭·서유럽 여행 코스까지, 공식 자료를 바탕으로 한눈에 정리했습니다."
    tabs, panes = [], []
    for i, (k, label) in enumerate(KINDS.items()):
        items = [q for q in SHOP_LIVE if kind_of(q) == k]
        sel = "true" if i == 0 else "false"
        tabs.append(f'<li role="presentation"><button type="button" role="tab" id="t-{k}" aria-controls="{k}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{esc(label)} <span class="c">{len(items)}</span></button></li>')
        def card(q):
            post = q["post"]
            cp = post.get("cta_photo") or {}
            thumb, twh = shop_thumb(post)
            tsz = f' width="{twh[0]}" height="{twh[1]}"' if twh else ""
            img = (f'<a class="at-shop-thumb" href="/{q["file"]}"><img src="{esc(thumb)}" alt="{esc(cp.get("alt") or post["title"])}"{tsz} loading="lazy" decoding="async"></a>'
                   if thumb else "")
            btn = (f'<a class="at-cta at-cta-sm" href="{esc(post.get("direct") or post["link"])}"{web_attr(post)} target="_blank" '
                   f'rel="sponsored nofollow noopener">{esc(cta_label(post))}</a>')
            return (f'<li class="at-shop-item">{img}<div class="at-shop-txt"><span class="tag shop">{esc(KINDS[kind_of(q)])}</span>'
                    f'<a class="t" href="/{q["file"]}">{esc(q["title"])}</a>'
                    f'<span class="x">{esc(post["keyword"])} · {short_date(q["date"])}</span>{btn}</div></li>')
        body = (f'<ul class="at-shop-list" data-paginate="5">{"".join(card(q) for q in items)}</ul>'
                if items else '<p class="at-empty">아직 올라온 글이 없습니다.</p>')
        panes.append(f'<section class="at-pane" role="tabpanel" id="{k}" aria-labelledby="t-{k}"{" hidden" if i else ""}>'
                     f'<h2 class="at-sr">{esc(label)}</h2>{body}</section>')
    content = f"""<header class="at-page-head">
  <h1>추천 모음</h1>
  <p class="lede">살 만한 제품을 고르는 기준과, 가 볼 만한 여행 코스를 정리했습니다. 직접 사용해 본 후기가 아니라, 제조사 공식 자료 등 공개된 정보를 정리한 글입니다.</p>
</header>
<aside class="at-disclose" role="note" aria-label="광고 표시"><p>이 게시판의 글은 네이버 커넥트 제휴 활동의 일환으로, 글 속 링크로 구매가 이뤄지면 일정액의 수수료를 제공받습니다.</p></aside>
<ul class="at-tabs at-tabs-lg" role="tablist" data-at-tabs aria-label="분류 선택">{"".join(tabs)}</ul>
{"".join(panes)}
<div class="at-prose" style="margin-top:1.5rem">{faq_html(CONNECT_FAQ)}</div>"""
    lst = {"@type": "ItemList", "name": "추천 모음 글", "numberOfItems": len(SHOP_LIVE), "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": q["title"], "url": url_of(q["file"])} for i, q in enumerate(SHOP_LIVE)]}
    write("connect.html", page_shell(p, content, [lst, faq_ld(CONNECT_FAQ)], board=False, robots=None if SHOP_LIVE else "noindex, follow"))


def build_home():
    p = PAGES["index.html"]
    notice = UPDATES[0]
    ups = "".join(row(u, t, tag, "notice" if tag == "공지" else ("trip" if tag == "여행" else ""), None, "", d, is_new(d))
                  for d, tag, t, u in UPDATES[:7])
    keytools = "".join(row("/" + PAGES[s + ".html"]["file"], PAGES[s + ".html"]["name"] + " 계산기", PAGES[s + ".html"]["group_name"].split("·")[0], "", None, "", None, False)
                       for s in KEY_TOOLS)
    # 지역 탭
    tabs, panes = [], []
    for i, (rid, rname, rshort, gus) in enumerate(FOOD_AREAS):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<li role="presentation"><button type="button" role="tab" id="t-{rid}" aria-controls="p-{rid}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{esc(rshort)}</button></li>')
        rows = []
        for pre, gu in gus:
            for q in food_pages(pre):
                if q["research"]:
                    continue
                rows.append(row("/" + q["file"], q["name"], gu, "food", q["count"] or None, "", None))
        hubs = " · ".join(f'<a href="/{pre}.html">{esc(gu)} 전체</a>' for pre, gu in gus)
        panes.append(f'<div class="at-pane" role="tabpanel" id="p-{rid}" aria-labelledby="t-{rid}"{" hidden" if i else ""}>'
                     f'<div class="at-box-body"><ul class="at-list">{"".join(rows[:8])}</ul>'
                     f'<p class="at-pane-more">{hubs}</p></div></div>')
    trips = "".join(f'<a href="/{slug}.html"><b>{esc(name)}</b><span>{esc(PAGES[slug + ".html"]["desc"][:44])}…</span></a>'
                    for slug, name, _ in TRIP_PAGES)
    trips += '<a href="/japan_travel_calculator.html"><b>일본 여행 경비</b><span>항공·숙박·식비 일자별 예산 계산</span></a>'
    trips += '<a href="/exchange_rate_calculator.html"><b>환율 계산</b><span>8개 통화 최신 기준 환율</span></a>'
    guides = "".join(row("/" + PAGES[s + ".html"]["file"], PAGES[s + ".html"]["name"], "가이드", "etc", None, "", PAGES[s + ".html"]["date"])
                     for s, _ in Q_GUIDES[:6] + GUIDE_PAGES)
    guides += "".join(row("/" + x + ".html", PAGES[x + ".html"]["name"], "텍스트", "", None, "", PAGES[x + ".html"]["date"], is_new(PAGES[x + ".html"]["date"]))
                      for x in ("character_counter", "spell_checker", "spacing_checker"))
    labor = "".join(row("/" + PAGES[s + ".html"]["file"], PAGES[s + ".html"]["name"], "노동", "", None, "", PAGES[s + ".html"]["date"])
                    for s in next(g for g in TOOL_GROUPS if g[0] == "labor")[2])
    faqs = "".join(f"<details><summary>{esc(q)}</summary><div class=\"a\"><p>{esc(a)}</p></div></details>" for q, a in FAQ_HOME)
    home_shop = "".join(shop_card(q) for q in SHOP_LIVE[:6])
    chips = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in [
        ("연봉 실수령액", "/salary_calculator.html"), ("퇴직금", "/severance_calculator.html"), ("실업급여", "/unemployment_benefit_calculator.html"),
        ("주휴수당", "/holiday_pay_calculator.html"), ("취득세", "/acquisition_tax_calculator.html"), ("해운대 맛집", "/haeundae-bapjip.html"),
        ("제주 맛집", "/jeju-jejusi-hyangto.html"), ("제주 여행 예산", "/travel-jeju.html")])
    content = f"""<div class="at-hello">
  <h1>생활 계산기와 지역 맛집 기록, 어라운드툴</h1>
  <p>계산기 {N_TOOLS}종은 계산 기준과 공식을 함께 보여주고, 맛집 {N_PLACES}곳은 광고·협찬을 빼고 근거와 단점을 적었습니다. 회원가입 없이 모두 무료입니다.</p>
  <ul class="at-chips" aria-label="자주 찾는 페이지">{chips}</ul>
</div>
<div class="at-notice"><b>공지</b><a href="{notice[3]}">{esc(notice[2])}</a><time datetime="{notice[0]}">{short_date(notice[0])}</time></div>
<section class="at-box"><div class="at-box-head"><h2>최근 업데이트</h2><a class="more" href="/sitemap.html">전체 페이지</a></div>
  <div class="at-box-body"><ul class="at-list">{ups}</ul></div></section>
<section class="at-box is-shop"><div class="at-box-head"><h2>추천 모음 — 제품 추천·여행 추천</h2><a class="more" href="/connect.html">추천 글 {len(SHOP_LIVE)}개 전체</a></div>
  <ul class="at-sp-grid at-sp-home">{home_shop}</ul>
</section>
<div class="at-two">
  <section class="at-box is-tool"><div class="at-box-head"><h2>주요 계산기</h2><a class="more" href="/tools.html">{N_TOOLS}종 전체</a></div>
    <div class="at-box-body"><ul class="at-list">{keytools}</ul></div></section>
  <section class="at-box is-food"><div class="at-box-head"><h2>지역별 맛집</h2><a class="more" href="/food.html">{N_GU}개 지역 전체</a></div>
    <ul class="at-tabs" role="tablist" data-at-tabs aria-label="지역 선택">{"".join(tabs)}</ul>{"".join(panes)}</section>
</div>
<section class="at-box is-trip"><div class="at-box-head"><h2>여행 가이드</h2><a class="more" href="/travel.html">여행 전체</a></div>
  <div class="at-grid-links">{trips}</div></section>
<div class="at-two">
  <section class="at-box is-tool"><div class="at-box-head"><h2>노동·구직 계산기</h2><a class="more" href="/tools.html#g-labor">더보기</a></div>
    <div class="at-box-body"><ul class="at-list">{labor}</ul></div></section>
  <section class="at-box is-etc"><div class="at-box-head"><h2>가이드·텍스트 도구</h2><a class="more" href="/etc.html">더보기</a></div>
    <div class="at-box-body"><ul class="at-list">{guides}</ul></div></section>
</div>
<section class="at-box"><div class="at-box-head"><h2>자주 묻는 질문</h2><a class="more" href="/about.html">사이트 소개</a></div>
  <div class="at-box-body pad"><div class="at-faq">{faqs}</div></div></section>"""
    website = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME, "alternateName": "AroundTool",
               "inLanguage": "ko-KR", "description": p["desc"], "publisher": {"@id": SITE + "/#org"},
               "potentialAction": {"@type": "SearchAction",
                                   "target": {"@type": "EntryPoint", "urlTemplate": SITE + "/search.html?q={search_term_string}"},
                                   "query-input": "required name=search_term_string"}}
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": NAME, "url": SITE + "/",
           "logo": image_ld("/assets/logo-512.png", "어라운드툴 로고"),
           "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "url": SITE + "/contact.html", "availableLanguage": ["Korean"]}}
    sections = {"@type": "ItemList", "name": "어라운드툴 주요 섹션", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "url": SITE + "/" + u} for i, (n, u) in
        enumerate([("전국 맛집", "food.html"), ("생활툴", "tools.html"), ("여행", "travel.html"), ("가이드", "etc.html"), ("추천 모음", "connect.html")])]}
    # 홈은 at-content 상자 없이 박스들을 직접 배치
    html_ = page_shell(p, content, [website, org, sections, faq_ld(FAQ_HOME)], board=False)
    html_ = html_.replace('<div class="at-content" id="at-main" tabindex="-1">', '<div class="at-home" id="at-main" tabindex="-1">', 1)
    write("index.html", html_)


def restaurants_in(f):
    """카테고리 글에서 가게 이름과 첫 줄 정보(주소·대표 메뉴 등)를 뽑습니다."""
    soup = BeautifulSoup(read(f), "html.parser")
    out = []
    for a in soup.select("article.entry"):
        h = a.find("h2")
        if not h:
            continue
        for r in h.select(".rom"):
            r.decompose()
        name = h.get_text(" ", strip=True)
        meta = a.select_one(".meta span")
        out.append((name, meta.get_text(" ", strip=True) if meta else ""))
    return out


def build_gu_hub(p):
    pages = [q for q in food_pages(p["prefix"]) if not q["research"]]
    total = gu_count(p["prefix"])
    area = f"{p['region_short']} {p['gu']}"
    p["title"] = f"{area} 맛집 {total}곳 — 카테고리별 전체 정리"
    blocks, names, ld_items = [], [], []
    for q in pages:
        rs = restaurants_in(q["file"])
        if rs:
            li = "".join(f'<li><a href="/{q["file"]}"><span class="t">{esc(n)}</span></a>' + (f'<span class="x">{esc(m)}</span>' if m else "") + "</li>" for n, m in rs)
            names.append(f"{q['cat']} {', '.join(n for n, _ in rs[:3])}")
            for n, _ in rs:
                ld_items.append({"@type": "ListItem", "position": len(ld_items) + 1,
                                 "item": {"@type": "Restaurant", "name": n, "url": url_of(q["file"]),
                                          "address": {"@type": "PostalAddress", "addressRegion": p["region_name"], "addressLocality": p["gu"], "addressCountry": "KR"}}})
        else:
            li = f'<li><a href="/{q["file"]}"><span class="t">{esc(q["title"])}</span></a></li>'
        desc = q["desc"][:90] + ("…" if len(q["desc"]) > 90 else "")
        cnt = f'<span class="c">{q["count"]}곳</span>' if q["count"] else ""
        blocks.append(f'<section class="at-gu-cat"><h2><a href="/{q["file"]}">{esc(q["cat"])}</a>{cnt}</h2>'
                      f'<p class="d">{esc(desc)}</p><ul class="at-gu-list">{li}</ul></section>')
    p["desc"] = (f"{p['region_name']} {p['gu']} 맛집 {total}곳을 카테고리별로 모았습니다. "
                 f"광고·협찬을 빼고 재방문 언급과 공식 지정 근거로 골랐고, 가게별 단점과 확인하지 못한 정보도 함께 적었습니다.")
    answer = f"{area}에서 이 사이트가 기록한 맛집은 <b>{total}곳</b>입니다. " + " · ".join(esc(x) for x in names[:6]) + (" 등입니다." if names else "")
    others = [g for r, _, _, gus in FOOD_AREAS if r == p["region"] for g in gus if g[0] != p["prefix"]]
    other_html = ""
    if others:
        other_html = "<p>" + esc(p["region_short"]) + "의 다른 지역: " + " · ".join(f'<a href="/{pre}.html">{esc(gu)} 맛집</a>' for pre, gu in others) + "</p>"
    travel = ""
    if p["region"] in REGION_TRAVEL:
        t = PAGES[REGION_TRAVEL[p["region"]]]
        travel = f'<p>여행 일정을 짜고 있다면 <a href="/{t["file"]}">{esc(t["name"])} 코스·예산·교통 정리</a>와 함께 보면 동선을 잡기 쉽습니다.</p>'
    photo_blk, photo_ld = page_photo_block(p["file"])
    content = f"""<header class="at-page-head">
  <h1>{esc(area)} 맛집 {total}곳</h1>
  <p class="lede">{esc(p['gu'])}에서 광고·협찬을 빼고 고른 가게를 카테고리별로 모았습니다. 가게 이름을 누르면 선정 근거와 단점, 가격과 영업시간 확인 여부를 볼 수 있습니다.</p>
  <p class="meta"><span>{len(pages)}개 카테고리</span><span>2026년 8월 조사</span><span><a href="/editorial.html">선정 기준</a></span></p>
</header>
<div class="at-page"><div class="at-prose" style="max-width:none">
<div class="at-answer"><p>{answer}</p></div>
{photo_blk}
{"".join(blocks)}
<h2>함께 보기</h2>
{travel}{other_html}
<p>전국 다른 지역은 <a href="/food.html">전국 맛집 기록</a>에서 볼 수 있습니다.</p>
</div></div>"""
    lst = {"@type": "ItemList", "name": f"{area} 맛집", "numberOfItems": len(ld_items), "itemListElement": ld_items}
    if photo_ld:
        lst["image"] = photo_ld[0]
    write(p["file"], page_shell(p, content, [lst]))


def build_food_hub():
    p = PAGES["food.html"]
    rows = []
    jump = []
    for rid, rname, rshort, gus in FOOD_AREAS:
        jump.append(f'<a href="#r-{rid}">{esc(rshort)} <span class="c">{region_count(rid)}</span></a>')
        rows.append(f'<tr class="at-gr" id="r-{rid}"><td colspan="4">{esc(rname)}<span>{region_count(rid)}곳</span></td></tr>')
        for pre, gu in gus:
            rows.append(f'<tr data-k="{esc(rname)} {esc(gu)}"><td class="k"><span class="tag food">{esc(gu)}</span></td>'
                        f'<td><a href="/{pre}.html"><b>{esc(rshort)} {esc(gu)} 맛집 전체 보기</b></a><span class="x">카테고리별 가게 목록을 한 페이지에</span></td>'
                        f'<td class="c">{gu_count(pre)}</td><td class="d">{short_date(TODAY)}</td></tr>')
            for q in food_pages(pre):
                dim = ' class="is-dim"' if q["research"] else ""
                cnt = q["count"] if q["count"] else "—"
                lab = esc(q["name"]) + (" (조사 중)" if q["research"] else "")
                rows.append(f'<tr{dim} data-k="{esc(rname)} {esc(q["cat"])}"><td class="k"><span class="tag food">{esc(gu)}</span></td>'
                            f'<td><a href="/{q["file"]}">{lab}</a><span class="x">{esc(q["desc"][:70])}{"…" if len(q["desc"]) > 70 else ""}</span></td>'
                            f'<td class="c">{cnt}</td><td class="d">{short_date(q["date"])}</td></tr>')
    content = f"""<header class="at-page-head">
  <h1>전국 맛집 기록</h1>
  <p class="lede">리뷰 수보다 재방문 언급을 보고, 미쉐린·백년가게·지자체 지정처럼 광고비로 살 수 없는 근거와 교차 확인했습니다. 협찬·체험단 글은 근거에서 빼고, 단점과 확인하지 못한 항목도 그대로 적습니다.</p>
  <p class="meta"><span>{len(FOOD_AREAS)}개 시도 · {N_GU}개 지역</span><span>맛집 {N_PLACES}곳</span><span>{len(FOOD_OK)}개 게시판</span></p>
</header>
<div class="at-board is-food"><ul class="at-board-tabs" aria-label="지역 바로가기">{"".join(f"<li>{j}</li>" for j in jump)}</ul></div>
<div class="at-filter"><label class="at-sr" for="ff">지역·음식으로 거르기</label><input id="ff" type="search" placeholder="지역이나 음식으로 거르기 (예: 국밥, 제주, 카페)" data-at-filter="food-table" data-at-empty="food-empty"></div>
<table class="at-btable" id="food-table"><thead><tr><th>지역</th><th>게시판</th><th class="c">수록</th><th class="d">갱신</th></tr></thead><tbody>{"".join(rows)}</tbody></table>
<p class="at-empty" id="food-empty" hidden>조건에 맞는 게시판이 없습니다.</p>
<div class="at-page"><div class="at-prose">
<h2>맛집을 고르는 방법</h2>
<ol class="at-steps"><li>지역 랭킹, 공공 자료, 미쉐린 가이드에서 후보를 모읍니다.</li>
<li>협찬·체험단·원고료 표기가 있는 글을 걸러내고, 서로 무관한 출처 3곳 이상에서 겹치는지 확인합니다.</li>
<li>주차, 웨이팅, 휴무, 플랫폼별 평점 차이 같은 단점을 함께 찾습니다.</li>
<li>확인하지 못한 항목은 ‘확인 필요’로 그대로 표시합니다.</li></ol>
<p>자세한 기준은 <a href="/editorial.html">편집 방침</a>에 정리했습니다.</p>
</div></div>"""
    lst = {"@type": "ItemList", "name": "지역별 맛집 게시판", "numberOfItems": len(FOOD_OK), "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": q["name"], "url": url_of(q["file"])} for i, q in enumerate(FOOD_OK)]}
    write("food.html", page_shell(p, content, [lst], board=False))


def build_tools_hub():
    p = PAGES["tools.html"]
    rows, jump = [], []
    for gid, gname, slugs in TOOL_GROUPS:
        jump.append(f'<a href="#g-{gid}">{esc(gname)} <span class="c">{len(slugs)}</span></a>')
        rows.append(f'<tr class="at-gr" id="g-{gid}"><td colspan="3">{esc(gname)}<span>{len(slugs)}종</span></td></tr>')
        for slug in slugs:
            q = PAGES[slug + ".html"]
            new = '<span class="n" style="display:inline-flex;align-items:center;justify-content:center;width:1rem;height:1rem;border-radius:3px;background:var(--at-new);color:#fff;font-size:.625rem;font-weight:800;margin-left:.3rem">N</span>' if is_new(q["date"]) else ""
            rows.append(f'<tr data-k="{esc(gname)}"><td class="k"><span class="tag">{esc(gname.split("·")[0])}</span></td>'
                        f'<td><a href="/{q["file"]}">{esc(q["name"])} 계산기</a>{new}<span class="x">{esc(q["desc"][:78])}{"…" if len(q["desc"]) > 78 else ""}</span></td>'
                        f'<td class="d">{short_date(q["date"])}</td></tr>')
    content = f"""<header class="at-page-head">
  <h1>생활툴 — 무료 생활 계산기 {N_TOOLS}종</h1>
  <p class="lede">연봉·퇴직금·세금·요금부터 여행 경비까지. 각 계산기에 계산 기준과 공식을 적어 두었고, 2026년 바뀐 요율과 법령을 반영했습니다. 입력값은 브라우저 밖으로 나가지 않습니다.</p>
  <p class="meta"><span>{len(TOOL_GROUPS)}개 분류</span><span>로그인 없이 무료</span><span>최종 갱신 {TODAY.replace('-', '.')}</span></p>
</header>
<div class="at-board is-tool"><ul class="at-board-tabs" aria-label="분류 바로가기">{"".join(f"<li>{j}</li>" for j in jump)}</ul></div>
<div class="at-filter"><label class="at-sr" for="tf">계산기 이름으로 찾기</label><input id="tf" type="search" placeholder="계산기 이름으로 찾기 (예: 퇴직금, 세금, 칼로리)" data-at-filter="tool-table" data-at-empty="tool-empty"></div>
<table class="at-btable" id="tool-table"><thead><tr><th>분류</th><th>계산기</th><th class="d">갱신</th></tr></thead><tbody>{"".join(rows)}</tbody></table>
<p class="at-empty" id="tool-empty" hidden>찾는 계산기가 없습니다. <a href="/contact.html">문의하기</a>로 필요한 계산기를 알려 주세요.</p>"""
    lst = {"@type": "ItemList", "name": "생활 계산기 목록", "numberOfItems": N_TOOLS, "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": q["name"], "url": url_of(q["file"])} for i, q in enumerate(TOOLS)]}
    write("tools.html", page_shell(p, content, [lst], board=False))


def build_search():
    p = PAGES["search.html"]
    content = """<header class="at-page-head">
  <h1>사이트 검색</h1>
  <form action="/search.html" method="get" role="search" class="at-filter" style="padding:1rem 0 0;border:0">
    <label class="at-sr" for="at-search-page-q">검색어</label>
    <input id="at-search-page-q" type="search" name="q" placeholder="예: 퇴직금, 해운대 국밥, 제주 여행">
  </form>
  <p class="meta" id="at-search-info" aria-live="polite"></p>
</header>
<div class="at-page"><ul class="at-results" id="at-search-results"></ul></div>"""
    write("search.html", page_shell(p, content, board=False, robots="noindex, follow"))


def build_404():
    p = PAGES["404.html"]
    links = "".join(row("/" + PAGES[s + ".html"]["file"], PAGES[s + ".html"]["name"] + " 계산기", "생활툴", "", None, "", None) for s in KEY_TOOLS[:6])
    content = f"""<header class="at-page-head">
  <h1>페이지를 찾을 수 없습니다</h1>
  <p class="lede">주소가 바뀌었거나 아직 공개하지 않은 페이지입니다. 검색하거나 아래 목록에서 찾아보세요.</p>
  <form action="/search.html" method="get" role="search" class="at-filter" style="padding:1rem 0 0;border:0">
    <label class="at-sr" for="nf-q">검색어</label><input id="nf-q" type="search" name="q" placeholder="계산기, 지역, 음식 이름으로 검색">
  </form>
</header>
<div class="at-page"><div class="at-prose"><h2>많이 찾는 페이지</h2></div><ul class="at-list">{links}
{row('/food.html', '전국 맛집 게시판', '맛집', 'food')}{row('/travel.html', '여행 가이드', '여행', 'trip')}{row('/sitemap.html', '전체 페이지 목록', '안내', 'etc')}</ul></div>"""
    html_ = page_shell(p, content, board=False, robots="noindex, follow")
    # 404 는 어느 경로에서든 열리므로 canonical·og:url 을 넣지 않음
    html_ = re.sub(r'<link rel="canonical"[^>]+>\n', "", html_)
    html_ = re.sub(r'<meta property="og:url"[^>]+>\n', "", html_)
    write("404.html", html_)


def build_sitemap_html():
    p = PAGES["sitemap.html"]
    secs = []
    for gid, gname, slugs in TOOL_GROUPS:
        items = "".join(f'<li><a href="/{s}.html">{esc(PAGES[s + ".html"]["name"])}</a></li>' for s in slugs)
        secs.append(f'<h2 class="at-sm-h">생활툴 · {esc(gname)} ({len(slugs)})</h2><ul class="at-cols">{items}</ul>')
    for rid, rname, rshort, gus in FOOD_AREAS:
        items = "".join(f'<li><a href="/{q["file"]}">{esc(q["name"])}</a>{" <small>(조사 중)</small>" if q["research"] else ""}</li>'
                        for pre, _ in gus for q in food_pages(pre))
        secs.append(f'<h2 class="at-sm-h">맛집 · {esc(rname)}</h2><ul class="at-cols">{items}</ul>')
    items = "".join(f'<li><a href="/{s}.html">{esc(n)}</a></li>' for s, n, _ in TRIP_PAGES)
    secs.append(f'<h2 class="at-sm-h">여행</h2><ul class="at-cols"><li><a href="/travel.html">여행 전체</a></li>{items}</ul>')
    items = "".join(f'<li><a href="/{s}.html">{esc(n)}</a></li>' for s, n in Q_GUIDES + GUIDE_PAGES)
    secs.append(f'<h2 class="at-sm-h">가이드</h2><ul class="at-cols"><li><a href="/etc.html">가이드·텍스트 도구</a></li>{items}</ul>')
    items = "".join(f'<li><a href="/{s}.html">{esc(n)}</a></li>' for s, n in INFO_PAGES)
    secs.append(f'<h2 class="at-sm-h">사이트 안내</h2><ul class="at-cols"><li><a href="/">홈</a></li><li><a href="/food.html">전국 맛집</a></li><li><a href="/tools.html">생활툴</a></li>{items}</ul>')
    n_idx = len([q for q in PAGES.values() if indexable(q)])
    content = f"""<header class="at-page-head"><h1>사이트맵</h1>
  <p class="lede">어라운드툴의 모든 페이지를 분류별로 모았습니다. 검색엔진용 목록은 <a href="/sitemap.xml">sitemap.xml</a>, AI 검색용 요약은 <a href="/llms.txt">llms.txt</a>에 있습니다.</p>
  <p class="meta"><span>계산기 {N_TOOLS}</span><span>맛집 게시판 {len(FOOD)}</span><span>공개 페이지 {n_idx}</span><span>갱신 {TODAY.replace('-', '.')}</span></p></header>
<div class="at-page"><div class="at-prose at-sitemap" style="max-width:none">{"".join(secs)}</div></div>
<style>.at-sitemap .at-cols{{columns:2 12rem;column-gap:1.5rem;padding-left:1.1rem}}.at-sitemap h3{{margin-top:1.75rem}}</style>"""
    write("sitemap.html", page_shell(p, content, board=False))


def build_redirects():
    for old, new in LEGACY_REDIRECTS.items():
        u = url_of(new)
        write(old, f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>페이지가 이동했습니다 | {NAME}</title>
<link rel="canonical" href="{u}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url=/{new}">
<script>location.replace('/{new}'+location.hash);</script>
</head>
<body>
<p>이 페이지는 <a href="/{new}">{u}</a>로 이동했습니다.</p>
</body>
</html>
""")


def mark_untouched_noindex():
    for f in ("Portfolio.dc.html", "categories-section.html"):
        if not os.path.exists(f):
            continue
        s = read(f)
        if 'name="robots"' not in s:
            s = re.sub(r"(<head[^>]*>)", r'\1\n<meta name="robots" content="noindex, nofollow">', s, count=1)
            write(f, s)


# ════════════════════════════════════════════════════════════════
# 8. sitemap.xml · feed.xml · llms.txt · 검색 색인
# ════════════════════════════════════════════════════════════════

def all_index_pages():
    order = ["index.html", "food.html", "tools.html", "travel.html", "etc.html"]
    ps = [PAGES[f] for f in order] + sorted([q for q in PAGES.values() if q["file"] not in order], key=lambda q: q["file"])
    return [q for q in ps if indexable(q)]


def git_date(f):
    import subprocess
    try:
        d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f], capture_output=True, text=True).stdout.strip()
        return d or None
    except Exception:
        return None


def sitemap_images(file):
    """본문(article)에 들어간 사진·설명 이미지를 이미지 사이트맵으로 알립니다."""
    path = os.path.join(_ROOT, file)
    if not os.path.exists(path):
        return ""
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    seen, out = set(), []
    for img in soup.select("article img, main figure img"):
        src = img.get("src") or ""
        if not src.startswith("/assets/") or src in seen or src.endswith(".svg"):
            continue
        seen.add(src)
        out.append(f"    <image:image><image:loc>{SITE}{html.escape(src)}</image:loc></image:image>\n")
    return "".join(out[:20])


def build_sitemap_xml():
    urls = []
    for q in all_index_pages():
        lm = max(filter(None, [git_date(q["file"]), q["date"]]))
        urls.append(f"  <url>\n    <loc>{url_of(q['file'])}</loc>\n    <lastmod>{lm}</lastmod>\n{sitemap_images(q['file'])}  </url>")
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- aroundtool.com · scripts/build.py 가 생성 · {TODAY} · {len(urls)} URL -->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{chr(10).join(urls)}
</urlset>
""")
    return len(urls)


def build_feed():
    items = []
    ps = sorted([q for q in all_index_pages() if q["section"] in ("food", "trip", "guide", "tools", "connect")],
                key=lambda q: (q["date"], q["file"]), reverse=True)
    for q in ps:
        d = datetime.strptime(q["date"], "%Y-%m-%d").replace(hour=9, tzinfo=KST)
        cat = {"food": "맛집", "trip": "여행", "guide": "가이드", "tools": "생활툴", "connect": "추천 모음"}[q["section"]]
        items.append(f"""    <item>
      <title>{esc(q['title'])}</title>
      <link>{url_of(q['file'])}</link>
      <guid isPermaLink="true">{url_of(q['file'])}</guid>
      <category>{cat}</category>
      <description>{esc(q['desc'])}</description>
      <pubDate>{format_datetime(d)}</pubDate>
    </item>""")
    now = datetime.strptime(TODAY, "%Y-%m-%d").replace(hour=9, tzinfo=KST)
    write("feed.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{NAME} — 생활 계산기·전국 맛집·여행 가이드</title>
    <link>{SITE}/</link>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>{esc(PAGES['index.html']['desc'])}</description>
    <language>ko</language>
    <lastBuildDate>{format_datetime(now)}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
""")


def build_llms():
    lines = [f"# {NAME} (aroundtool.com)", "",
             f"> 무료 생활 계산기 {N_TOOLS}종과, 광고·협찬을 배제하고 선정 근거를 밝힌 전국 {N_GU}개 지역 맛집 {N_PLACES}곳 기록, 국내외 여행 코스·예산 가이드를 제공하는 한국어 사이트입니다. 회원가입 없이 모든 페이지를 볼 수 있습니다.",
             "", f"- 최종 갱신: {TODAY}", f"- 전체 페이지 목록: {SITE}/sitemap.html", f"- 편집 방침: {SITE}/editorial.html", "",
             "## 인용 시 유의사항", "",
             "- 계산 결과는 **참고용 추정치**이며 법적 효력이 없습니다. 각 계산기 페이지에 계산식과 기준 연도가 적혀 있습니다.",
             "- 맛집 정보의 가격·영업시간·휴무는 2026년 8월 조사 기준이며 변동될 수 있습니다.",
             "- \"확인 필요\"로 표시된 항목은 검증되지 않은 정보입니다.", "",
             "## 맛집 선정 기준", "",
             "리뷰 개수가 아니라 재방문 언급을 봅니다. 다이닝코드 지역 랭킹, 미쉐린 가이드, 중소벤처기업부 백년가게, 지자체 공식 지정처럼 광고비로 살 수 없는 근거와 교차 확인합니다. 협찬·체험단·원고료 표기가 있는 글은 근거에서 제외하고, 단점도 함께 적습니다.", ""]
    lines += ["## 생활 계산기", ""]
    for gid, gname, slugs in TOOL_GROUPS:
        lines.append(f"### {gname}")
        for s in slugs:
            q = PAGES[s + ".html"]
            lines.append(f"- [{q['name']}]({url_of(q['file'])}): {q['desc']}")
        lines.append("")
    lines += ["## 지역별 맛집 모아보기", ""] + [f"- [{PAGES[pre + '.html']['title']}]({SITE}/{pre}.html)" for _, _, _, gus in FOOD_AREAS for pre, _ in gus] + [""]
    lines += ["## 지역별 맛집", ""]
    for rid, rname, rshort, gus in FOOD_AREAS:
        lines.append(f"### {rname}")
        for pre, gu in gus:
            for q in food_pages(pre):
                if not q["research"]:
                    lines.append(f"- [{q['name']}]({url_of(q['file'])})" + (f" — {q['count']}곳" if q["count"] else ""))
        lines.append("")
    lines += ["## 여행", ""] + [f"- [{n}]({SITE}/{s}.html): {PAGES[s + '.html']['desc']}" for s, n, _ in TRIP_PAGES] + [""]
    lines += ["## 가이드", ""] + [f"- [{PAGES[s + '.html'].get('title') or n}]({SITE}/{s}.html)" for s, n in Q_GUIDES + GUIDE_PAGES] + [""]
    if SHOP_LIVE:
        lines += ["## 추천 모음 — 제품 추천·여행 추천", ""]
        lines += [f"- [{q['title']}]({url_of(q['file'])})" for q in SHOP_LIVE] + [""]
    write("llms.txt", "\n".join(lines))


def build_search_index():
    items = []
    for q in all_index_pages():
        if q["file"] in ("sitemap.html",):
            continue
        k = " ".join(filter(None, [q.get("region_name"), q.get("gu"), q.get("cat"), q.get("group_name"), q.get("kind")]))
        sec = {"food": "맛집", "gu": "맛집", "tools": "생활툴", "trip": "여행", "guide": "가이드", "info": "사이트 안내", "connect": "추천 모음"}.get(q["section"], "안내")
        title = q["name"] + (" 계산기" if q["section"] == "tools" and "계산" not in q["name"] and "생성" not in q["name"] and "검사" not in q["name"] and "세기" not in q["name"] and "운세" not in q["name"] else "")
        if q["section"] in ("home",) or q["section"].startswith("hub"):
            title = q["title"]
        items.append({"t": title, "u": "/" + ("" if q["file"] == "index.html" else q["file"]), "d": q["desc"], "s": sec, "k": k})
    write("assets/search-index.json", json.dumps(items, ensure_ascii=False, separators=(",", ":")))
    return len(items)


# ════════════════════════════════════════════════════════════════
# 실행
# ════════════════════════════════════════════════════════════════

def main():
    for slug in CALCS:
        build_calc(slug)
    for q in SHOP:
        build_connect_post(q)
    build_connect_hub()
    for g in GUIDES:
        build_qguide(PAGES[f"guide-{g['slug']}.html"])
    for _, _, _, gus in FOOD_AREAS:
        for pre, _ in gus:
            build_gu_hub(PAGES[pre + ".html"])
    generated = {pre + ".html" for _, _, _, gus in FOOD_AREAS for pre, _ in gus} | {"index.html", "food.html", "tools.html", "search.html", "404.html", "sitemap.html", "connect.html"} | {s + ".html" for s in CALCS} | {q["file"] for q in SHOP} | {f"guide-{g['slug']}.html" for g in GUIDES}
    for f, p in PAGES.items():
        if f in generated or f in UNTOUCHED:
            continue
        transform_existing(p)
    build_home()
    build_food_hub()
    build_tools_hub()
    build_search()
    build_404()
    build_sitemap_html()
    build_redirects()
    mark_untouched_noindex()
    n = build_sitemap_xml()
    build_feed()
    build_llms()
    m = build_search_index()
    print(f"shop_posts={len(SHOP)} live={len(SHOP_LIVE)}")
    print(f"pages={len(PAGES)} tools={N_TOOLS} food_boards={len(FOOD)} places={N_PLACES} gu={N_GU} sitemap={n} search={m}")


if __name__ == "__main__":
    main()
