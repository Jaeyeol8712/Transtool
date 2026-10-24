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

def export(slug):
    p = next(x for x in POSTS if x["slug"] == slug)
    d = DISCLOSURE[p.get("program", "shopping")]
    out = [p["title"], "", d, "", p["link"], ""]
    for b in p["body"]:
        if b.startswith("{img"):
            out += [f"[이미지 {b[4]}]", ""]
        elif b == "{cta}":
            out += [p.get("cta_hook", ""), p["link"], ""]
        else:
            out += [to_text(b), ""]
    out += p.get("closing", []) + ["", d, "", p["link"]]
    os.makedirs("blog-export", exist_ok=True)
    path = f"blog-export/{slug}.txt"
    open(path, "w", encoding="utf-8").write("\n".join(out).strip() + "\n")
    return path

if __name__ == "__main__":
    for s in sys.argv[1:]:
        print(export(s))
