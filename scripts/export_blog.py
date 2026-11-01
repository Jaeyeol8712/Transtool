#!/usr/bin/env python3
"""추천 모음 글을 네이버 블로그에 붙여 넣기 좋은 텍스트로 내보냅니다.
   python3 scripts/export_blog.py <slug> [<slug> ...]  →  blog-export/<slug>.txt"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from connect_posts import POSTS, DISCLOSURE

def to_text(block):
    t = block
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r'<p class="vx-title">(.*?)</p>', r"\n■ \1\n", t)
    t = re.sub(r'<span class="vx-card-n">(\d+)</span>', r"\n\1) ", t)
    t = re.sub(r'<p class="vx-card-t">(.*?)</p>', r"\1\n", t)
    t = re.sub(r'<p class="vx-vs-name">(.*?)</p>', r"\n[\1]\n", t)
    t = re.sub(r'<span class="vx-vs-mid">VS</span>', "\n  VS\n", t)
    t = re.sub(r"<li><b>(.*?)</b><span>(.*?)</span></li>", r"✔ \1 — \2\n", t)
    t = re.sub(r"<li>(.*?)</li>", r"· \1\n", t)
    t = re.sub(r'<span class="vx-chip[^"]*">(.*?)</span>', r"#\1 ", t)
    t = re.sub(r'<span class="vx-tag vx-(?:yes|no)">(.*?)</span>', r"\1\n", t)
    t = re.sub(r'<span class="vx-meter-k">(.*?)</span>.*?<span class="vx-meter-d">(.*?)</span>', r"· \1: \2\n", t)
    t = re.sub(r"</(p|div|section)>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(l.strip() for l in t.splitlines())).strip()

SITE = "https://www.aroundtool.com"

def export(slug):
    """블로그용: 대가성 문구 → 대표 사진 → 본문(그래픽 자리 표시) → 제휴 링크(브랜드 커넥트 발급 링크 그대로) → 사이트 정리 글 링크."""
    p = next(x for x in POSTS if x["slug"] == slug)
    d = DISCLOSURE[p.get("program", "shopping")]
    label = "👉 여행 비용 알아보기" if p.get("kind") == "travel" else "👉 제품 가격 알아보기"
    link = f"{label}\n{p['link']}"
    out = [p["title"], "", d, ""]
    if p.get("cta_photo"):
        out += ["[사진: 대표 사진]", ""]
    out += [link, ""]
    for b in p["body"]:
        if b.startswith("{img"):
            out += [f"[사진: 설명 그래픽 {b[4]}]", ""]
        elif b == "{cta}":
            out += [p.get("cta_hook", ""), link, ""]
        else:
            t = to_text(b)
            t = re.sub(r"^(\S+)\n", r"\1 ", t) if t[:1] and not t[:1].isalnum() and "\n" in t[:4] else t
            out += [t, ""]
    out += [c.replace("아래 버튼에서", "아래 링크에서") for c in p.get("closing", [])]
    out += ["", link, "", f"📌 표와 자주 묻는 질문까지 정리한 글: {SITE}/shop-{slug}.html", "", d]
    os.makedirs("blog-export", exist_ok=True)
    path = f"blog-export/{slug}.txt"
    open(path, "w", encoding="utf-8").write("\n".join(out).strip() + "\n")
    return path

if __name__ == "__main__":
    for s in sys.argv[1:]:
        print(export(s))
