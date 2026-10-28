# -*- coding: utf-8 -*-
"""
추천 모음 글을 카페 게시용으로: 제목(검색 많은 키워드 + 설명) / 본문 1,500자 이내 + 페이지 링크.
하루 5개씩 _cafe/shop-day-NN.txt 로 저장.  python3 scripts/cafe_shop_posts.py
카페 글에는 제휴 링크를 직접 넣지 않고 사이트 글 주소만 넣으며, 링크 페이지에 제휴 링크가 있다는 점을 밝힌다.
"""
import html, os, re, sys
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(__file__))
from connect_posts import POSTS  # noqa: E402

SITE = "https://www.aroundtool.com"
NOTE = "※ 제휴 안내: 링크한 페이지에는 네이버 쇼핑 커넥트 제휴 링크가 있으며, 그 링크로 구매가 이뤄지면 수수료를 받습니다."

# 슬러그: 카페 제목 (검색 많은 키워드를 맨 앞에)
TITLES = {
    "queens-collagen-rg3": "미백 주름 화장품 추천 — 기능성 표시부터 확인하는 고르는 법",
    "bespoke-ai-fridge-4door": "비스포크 냉장고 4도어 추천 — 용량·키친핏 고르기 전 체크할 것",
    "galaxy-s26-ultra": "갤럭시 S26 울트라 자급제 가격 — 512GB 살 때 확인할 것 정리",
    "danang-5days": "다낭 여행 추천 코스 — 4박5일·3박5일 일정과 비용 정리",
    "prael-thermashot-ultimate": "프라엘 써마샷 가격 — 고주파 뷰티 디바이스 사기 전 체크",
    "jbl-authentics-200": "블루투스 스피커 추천 JBL 어센틱 200 — 와이파이·레트로 디자인 정리",
    "bespoke-ai-steam-ultra": "로봇청소기 추천 비스포크 AI 스팀 울트라 — 일반형 vs 급배수형",
    "galaxy-tab-s12-ultra": "갤럭시탭 S12 울트라 가격 — 256GB WiFi 살 때 볼 것",
    "west-europe-3-10days": "서유럽 여행 코스 추천 — 3국 10일 스트라스부르·루체른·융프라우",
    "student-office-laptop": "대학생 노트북 추천 — 인강용·사무용 사양 기준 정리",
    "mung-bean-cleanser": "약산성 클렌징폼 추천 — 녹두 클렌저 pH·전성분 보는 법",
    "calf-foot-air-massager": "종아리 마사지기 추천 — 공기압 방식 고를 때 볼 4가지",
    "fukuoka-3days": "후쿠오카 여행 추천 코스 — 2박3일 일정 다자이후·유후인",
    "food-waste-disposer": "음식물처리기 추천 — 건조·분쇄·미생물 방식별 장단점",
    "wireless-gaming-keyboard": "무선 게이밍 키보드 추천 — 트리모드·스위치·배열 고르는 법",
    "neck-traction": "거북목 교정기 추천 — 목견인기 의료기기 여부부터 확인",
    "c-type-65w-charger": "C타입 고속 충전기 추천 — 65W 일체형 고를 때 볼 숫자 3개",
}


def txt(el):
    t = el.get_text("") if el else ""
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def block(b):
    """시각 블록 HTML → (종류, 카페용 텍스트)."""
    if not b.lstrip().startswith("<"):
        return "p", txt(BeautifulSoup(b, "html.parser"))
    s = BeautifulSoup(b, "html.parser")
    root = s.find(True)
    cls = " ".join(root.get("class", []))
    if "vx-hero" in cls:
        h = s.select_one(".vx-hero-h")
        for br in h.find_all("br"):
            br.replace_with(" ")
        return "hero", txt(h) + "\n" + txt(s.select_one(".vx-hero-s"))
    if "vx-callout" in cls:
        return "callout", "💡 " + txt(s.find("p"))
    title = txt(s.select_one(".vx-title"))
    if s.select(".vx-card"):
        nums = "①②③④⑤⑥"
        rows = [f"{nums[i]} {txt(c.select_one('.vx-card-t'))} — {txt(c.select_one('.vx-card-d'))}" for i, c in enumerate(s.select(".vx-card"))]
        return "cards", "[" + title + "]\n" + "\n".join(rows)
    if s.select(".vx-vs-col"):
        rows = []
        for c in s.select(".vx-vs-col"):
            rows.append(f"▶ {txt(c.select_one('.vx-vs-name'))}: " + " / ".join(txt(li) for li in c.find_all("li")))
        return "versus", "[" + title + "]\n" + "\n".join(rows)
    if "vx-check" in cls:
        rows = [f"✔ {txt(li.find('b'))} — {txt(li.find('span'))}" for li in s.find_all("li")]
        return "check", "[" + title + "]\n" + "\n".join(rows)
    if s.select(".vx-tags"):
        rows = []
        for g in s.select(".vx-tags"):
            rows.append(txt(g.select_one(".vx-tags-h")))
            rows += ["  " + txt(t) for t in g.select(".vx-tag")]
        return "tags", "\n".join(rows)
    if s.select(".vx-meter-row"):
        rows = [f"· {txt(r.select_one('.vx-meter-k'))} — {txt(r.select_one('.vx-meter-d'))}" for r in s.select(".vx-meter-row")]
        return "meter", "[" + title + "]\n" + "\n".join(rows)
    return "other", txt(s)


def post(p):
    url = f"{SITE}/shop-{p['slug']}.html?utm_source=naver_cafe&utm_medium=cafe&utm_campaign=cafe_{p['slug']}&utm_content=v1"
    parts = [block(b) for b in p["body"] if not re.fullmatch(r"\{[^}]*\}", b.strip())]
    paras = [t for k, t in parts if k == "p"]
    tail = "가격·구성은 판매처와 시점마다 달라서, 비교 그래픽과 현재 가격 확인 링크는 아래 페이지에 정리해 두었어요." \
        if p.get("kind") != "travel" else "코스 정리 그래픽과 현재 여행 상품 비용 확인 링크는 아래 페이지에 정리해 두었어요."
    # 길면 덜 중요한 블록부터 뺀다
    drop_order = [[], ["meter", "other"], ["meter", "other", "versus"], ["meter", "other", "versus", "tags"],
                  ["meter", "other", "versus", "tags", "callout"], ["meter", "other", "versus", "tags", "callout", "cards"]]
    for drop in drop_order:
        out = [NOTE]
        for i, (k, t) in enumerate(parts):
            if k in drop:
                continue
            if k == "p" and paras and t == paras[-1] and len(paras) > 1:
                continue  # 마지막 마무리 문단은 끝에 따로
            out.append(t)
        if len(paras) > 1:
            out.append(paras[-1])
        out += [tail, url]
        body = "\n\n".join(out).replace("\n\n\n", "\n\n")
        if len(body) <= 1500:
            return TITLES[p["slug"]], body
    return TITLES[p["slug"]], body[:1350] + "…\n\n" + url


def main():
    os.makedirs("_cafe", exist_ok=True)
    order = {x["slug"]: i for i, x in enumerate(POSTS)}
    items = sorted([x for x in POSTS if x.get("live", True)], key=lambda x: (x["date"], order[x["slug"]]), reverse=True)
    for i in range(0, len(items), 5):
        day = i // 5 + 1
        out = [f"[추천 모음 카페 게시용 {day}일차] — 하루 5개 이내, 게시판 성격에 맞는 곳에 올려 주세요\n"]
        for n, p in enumerate(items[i:i + 5], 1):
            t, b = post(p)
            out += ["=" * 40, t, "", b, ""]
        open(f"_cafe/shop-day-{day:02d}.txt", "w", encoding="utf-8").write("\n".join(out))
    print(f"{len(items)}개 → {(len(items) + 4) // 5}일치")


if __name__ == "__main__":
    main()
