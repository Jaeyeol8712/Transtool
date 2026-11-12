# -*- coding: utf-8 -*-
"""시안 B(카드형) 레이아웃을 글 페이지에 입힙니다.

- 본문을 소제목(h2) 단위 카드(.b-card)로 나누고 소제목에 번호를 붙입니다.
- 표의 각 칸에 머리글 이름(data-label)을 넣어, 휴대폰에서는 표를 카드처럼 보여 줍니다.
- PC 사이드바 끝에 따라 내려오는 목차(.b-toc)를 넣습니다.
- <body class="b"> 로 표시해 site.css 의 시안 B 스타일을 켭니다.
여러 번 돌려도 결과가 같습니다(이미 나눈 카드는 다시 나누지 않음).
"""
import html
import re
from bs4 import BeautifulSoup, NavigableString, Comment

TOP = "<!-- /at:top -->"
BOT = "<!-- at:bottom -->"
NO_NUM = ("자주 묻는 질문", "명소 안내", "다른 ", "이 글의 기준", "함께 보면", "관련", "출처", "참고 자료")


def _text(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()


def _label_tables(root):
    for t in root.find_all("table"):
        head = t.find("thead")
        if not head:
            continue
        hr = head.find("tr")
        if not hr:
            continue
        names = [_text(c) for c in hr.find_all(["th", "td"])]
        if len(names) < 2:
            continue
        cls = [c for c in (t.get("class") or []) if c not in ("b-stack", "b-stack2")]
        # 3열 이하는 일반 표(네이버식 격자), 4열 이상만 카드형으로 쌓음
        longest = max((len(_text(c)) for c in t.find_all(["td", "th"])), default=0)
        stack = len(names) >= 4 or longest > 16
        t["class"] = cls + ((["b-stack"] + (["b-stack2"] if len(names) == 2 else [])) if stack else [])
        if not t["class"]:
            del t["class"]
        for tr in (t.find("tbody") or t).find_all("tr", recursive=False):
            for i, c in enumerate(tr.find_all(["th", "td"], recursive=False)):
                if c.name == "td" and i < len(names) and names[i] and not c.get("data-label"):
                    c["data-label"] = names[i]


def _number(h2, n):
    if h2.find(class_="b-num"):
        return
    span = BeautifulSoup(f'<span class="b-num" aria-hidden="true">{n}</span>', "html.parser").span
    h2.insert(0, span)


def _group(soup, root, number=True):
    """root 바로 아래 자식들을 h2 기준으로 카드에 담습니다."""
    kids = [c for c in list(root.children) if not (isinstance(c, NavigableString) and not isinstance(c, Comment) and not c.strip())]
    cards, cur = [], None
    for c in kids:
        name = getattr(c, "name", None)
        # 요약 상자는 카드 밖에 따로 둡니다
        cls = (c.get("class") or []) if name else []
        if name and ("at-answer" in cls or "vx-hero" in cls):
            cards.append(("solo", c))
            cur = None
            continue
        if name == "section" and "vx-sec" in cls:
            t = c.find("p", class_="vx-title")
            if t is not None:
                t.name = "h2"
        starts = name == "h2" or (name == "section" and "vx-sec" in cls and c.find("h2", class_="vx-title") is not None)
        if starts or cur is None:
            cur = []
            cards.append(("card", cur))
        cur.append(c)
    for c in kids:
        c.extract()
    n = 0
    for kind, item in cards:
        if kind == "solo":
            item["class"] = (item.get("class") or []) + ["b-sum"]
            root.append(item)
            continue
        sec = soup.new_tag("section")
        sec["class"] = ["b-card"]
        if not any(getattr(x, "name", None) for x in item):
            for x in item:
                root.append(x)
            continue
        h2 = next((x for x in item if getattr(x, "name", None) == "h2"), None)
        if h2 is None:
            h2 = next((x.find("h2", class_="vx-title") for x in item if getattr(x, "name", None) == "section" and x.find("h2", class_="vx-title")), None)
        if h2 is not None:
            title = _text(h2)
            if number and not any(k in title for k in NO_NUM):
                n += 1
                _number(h2, n)
            sec["id"] = f"b-s{len(root.find_all('section', class_='b-card', recursive=False)) + 1}"
        for x in item:
            sec.append(x)
        root.append(sec)


def _mark_blocks(root):
    """이미 블록으로 나뉜 맛집 페이지: 바로 아래 블록에 카드 표시만."""
    i = 0
    for c in root.find_all(recursive=False):
        if c.name in ("div", "section", "article", "aside", "details", "figure"):
            cls = c.get("class") or []
            if "b-card" not in cls:
                c["class"] = cls + ["b-card"]
            if not c.get("id") and c.find("h2"):
                i += 1
                c["id"] = f"b-s{i}"


def _toc(root):
    out = []
    for sec in root.find_all(class_="b-card"):
        h2 = sec.find("h2")
        if not h2 or not sec.get("id"):
            continue
        ht = h2.find(class_="b-ht")
        if ht is not None:
            t = "".join(x for x in ht.find_all(string=True, recursive=False)).strip() or ht.get_text(" ", strip=True)
        else:
            t = h2.get_text(" ", strip=True)
            num = h2.find(class_="b-num")
            if num:
                t = t[len(num.get_text()):].strip()
        out.append((sec["id"], re.sub(r"\s+", " ", t)))
    return out


_HSPLIT = re.compile(r"^(.{4,}?)\s*(?:\(([^()]{2,})\)|\s[—–]\s(.{2,}))\s*$")
_OPS = re.compile(r"\s+([×÷+−\-])\s+")
_PAREN = re.compile(r"([가-힣%])\((?=[가-힣])")


def _tidy_heads(soup):
    """소제목: 괄호·줄표 뒤 설명은 작은 둘째 줄로, 번호 옆 글자는 한 덩어리로."""
    for h in soup.find_all("h2"):
        if h.find(class_="b-ht"):
            continue
        num = h.find(class_="b-num")
        if num is not None:
            num.extract()
        kids = list(h.contents)
        only_text = all(isinstance(k, NavigableString) for k in kids)
        span = soup.new_tag("span")
        span["class"] = ["b-ht"]
        text = re.sub(r"\s+", " ", h.get_text()).strip()
        m = _HSPLIT.match(text) if only_text else None
        for k in kids:
            k.extract()
        if m:
            span.append(m.group(1).strip())
            sub = soup.new_tag("span")
            sub["class"] = ["b-hsub"]
            sub.append((m.group(2) or m.group(3)).strip())
            span.append(sub)
        else:
            for k in kids:
                span.append(k)
        if num is not None:
            h.append(num)
        h.append(span)


def _tidy_formula(soup):
    """계산식: 줄마다 이름과 식을 나누고, 식은 연산자 앞뒤에서 줄이 바뀌지 않게."""
    for f in soup.find_all(class_="at-formula"):
        if f.find(class_="f-row"):
            continue
        lines, cur = [], []
        for k in list(f.contents):
            if getattr(k, "name", None) == "br":
                lines.append(cur)
                cur = []
            else:
                cur.append(k)
        lines.append(cur)
        for k in list(f.contents):
            k.extract()
        split = []
        for ln in lines:
            if ln and all(isinstance(k, NavigableString) for k in ln):
                txt = re.sub(r"\s+", " ", "".join(str(k) for k in ln)).strip()
                parts = [x for x in re.split(r"\s·\s", txt) if x]
                if len(parts) > 1 and all("=" in x for x in parts):
                    split.extend([[NavigableString(x)] for x in parts])
                    continue
            split.append(ln)
        lines = split
        for ln in lines:
            ln = [k for k in ln if not (isinstance(k, NavigableString) and not k.strip())]
            if not ln:
                continue
            row = soup.new_tag("div")
            row["class"] = ["f-row"]
            if getattr(ln[0], "name", None) == "small":
                row["class"] = ["f-row", "f-note"]
            label = None
            if getattr(ln[0], "name", None) == "b":
                label = ln.pop(0)
            elif all(isinstance(k, NavigableString) for k in ln):
                txt = re.sub(r"\s+", " ", "".join(str(k) for k in ln)).strip()
                if ":" in txt.split("=")[0]:
                    k_, v_ = txt.split(":", 1)
                elif "=" in txt:
                    k_, v_ = txt.split("=", 1)
                    v_ = "= " + v_.strip()
                else:
                    k_, v_ = "", txt
                ln = [NavigableString(v_.strip())]
                if k_.strip():
                    label = soup.new_tag("b")
                    label.append(k_.strip())
            if label is not None:
                ks = soup.new_tag("span")
                ks["class"] = ["f-k"]
                ks.append(label.get_text())
                row.append(ks)
            vs = soup.new_tag("span")
            vs["class"] = ["f-v"]
            for k in ln:
                if isinstance(k, NavigableString):
                    k = NavigableString(_OPS.sub(lambda m: "\u00a0" + m.group(1) + "\u00a0", str(k)).strip(" "))
                vs.append(k)
            row.append(vs)
            f.append(row)


_FIXES = [
    (_PAREN, r"\1 ("),                                   # 375,000원(이자만) → 375,000원 (이자만)
    (re.compile(r"(\d)박(\d)일"), r"\1박 \2일"),          # 2박3일 → 2박 3일
    (re.compile(r"(\d)(만|천|억)원"), r"\1\2 원"),          # 200만원 → 200만 원
    (re.compile(r"(\d)(만|억)(\d)"), r"\1\2 \3"),          # 1억5천 → 1억 5천
]


def _tidy_text(soup):
    """띄어쓰기 맞춤법: 괄호 앞, 'N박 N일', 'N만 원' 등."""
    for t in soup.find_all(string=True):
        if isinstance(t, Comment) or t.parent is None or t.parent.name in ("script", "style", "code", "textarea", "pre"):
            continue
        new = str(t)
        for rx, rep in _FIXES:
            new = rx.sub(rep, new)
        if new != str(t):
            t.replace_with(NavigableString(new))


def tidy_spacing(s):
    """모든 페이지 본문(상단·하단 공통 영역 제외)에 띄어쓰기 정리를 적용합니다."""
    if TOP not in s or BOT not in s:
        return s
    a = s.index(TOP) + len(TOP)
    b = s.index(BOT, a)
    region = s[a:b]
    if not any(rx.search(region) for rx, _ in _FIXES):
        return s
    soup = BeautifulSoup(region, "html.parser")
    _tidy_text(soup)
    return s[:a] + str(soup) + s[b:]


def apply(s):
    if TOP not in s or BOT not in s:
        return s
    a = s.index(TOP) + len(TOP)
    b = s.index(BOT, a)
    region = s[a:b]
    soup = BeautifulSoup(region, "html.parser")
    for sec in soup.find_all("section", class_="b-card"):
        if not sec.find(True):
            sec.unwrap()
    root = soup
    prose = soup.find(class_="at-prose")
    if prose is not None and not prose.find(class_="b-card", recursive=False):
        _group(soup, prose)
    for m in soup.find_all("main"):
        if m.find(class_="at-prose") is not None or m.find("main") is not None:
            continue
        if not m.find(class_="b-card"):
            if m.find("h2", recursive=False):
                _group(soup, m)
            else:
                _mark_blocks(m)
    _label_tables(soup)
    _tidy_heads(soup)
    _tidy_formula(soup)
    _tidy_text(soup)
    toc = _toc(root)
    region = str(soup)
    s = s[:a] + region + s[b:]
    # 사이드바 끝 목차 (PC)
    s = re.sub(r'\s*<section class="at-box b-toc".*?</section><!-- /b-toc -->', "", s, flags=re.S)
    if len(toc) >= 3:
        li = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in toc)
        box = f'<section class="at-box b-toc" aria-label="목차"><div class="at-box-head"><p>이 글의 목차</p></div><ol>{li}</ol></section><!-- /b-toc -->'
        k = s.find('<aside class="at-side"')
        if k >= 0:
            e = s.find("</aside>", k)
            s = s[:e] + box + "\n" + s[e:]
    if '<body class="b"' not in s:
        s = re.sub(r"<body(?![^>]*class=)([^>]*)>", r'<body class="b"\1>', s, count=1)
    return s
