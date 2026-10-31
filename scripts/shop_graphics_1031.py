# -*- coding: utf-8 -*-
"""2026-10-31 추천 글 9개의 설명 그래픽(1200x750) 생성. python3 scripts/shop_graphics_1031.py"""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def font(path, size): return ImageFont.truetype(path, size, index=1)
BG, INK, MUTE = "#FFF6F0", "#222B36", "#5B6572"
PAL = ["#E4572E", "#F6A945", "#17A398", "#3B82F6", "#8B5CDB", "#E0518D"]
W, H = 1200, 750

def fit(d, text, path, size, maxw, minsize=22):
    while size > minsize and d.textlength(text, font=font(path, size)) > maxw:
        size -= 2
    return font(path, size)

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=f) > maxw and cur:
            lines.append(cur); cur = ch.lstrip()
        else:
            cur += ch
    if cur: lines.append(cur)
    return lines

def head(d, title, sub):
    d.text((60, 52), title, font=fit(d, title, FB, 50, W - 120), fill=INK)
    d.text((60, 122), sub, font=fit(d, sub, FR, 28, W - 120), fill=MUTE)

def rows(path, title, sub, items):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im); head(d, title, sub)
    n = len(items); top = 178; gap = 16; rh = (H - top - 40 - gap * (n - 1)) // n
    for i, (tag, text) in enumerate(items):
        y = top + i * (rh + gap); c = PAL[i % 6]
        d.rounded_rectangle((60, y, W - 60, y + rh), 24, fill="white", outline=c, width=3)
        d.rounded_rectangle((60, y, 270, y + rh), 24, fill=c)
        d.rectangle((200, y, 270, y + rh), fill=c)
        tf = fit(d, tag, FB, 34, 180)
        d.text((165, y + rh / 2), tag, font=tf, fill="white", anchor="mm")
        xf = fit(d, text, FB, 36, W - 400)
        if d.textlength(text, font=xf) > W - 400:
            f2 = font(FB, 28); ls = wrap(d, text, f2, W - 400)[:2]
            for k, l in enumerate(ls):
                d.text((300, y + rh / 2 + (k - (len(ls) - 1) / 2) * 38), l, font=f2, fill=INK, anchor="lm")
        else:
            d.text((300, y + rh / 2), text, font=xf, fill=INK, anchor="lm")
    im.save(path)

def cards(path, title, sub, items):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im); head(d, title, sub)
    n = len(items); cols = 2; rws = (n + 1) // 2; top = 178; gap = 22
    cw = (W - 120 - gap) // 2; ch = (H - top - 40 - gap * (rws - 1)) // rws
    for i, (hd, body) in enumerate(items):
        x = 60 + (i % cols) * (cw + gap); y = top + (i // cols) * (ch + gap); c = PAL[i % 6]
        d.rounded_rectangle((x, y, x + cw, y + ch), 24, fill="white", outline=c, width=3)
        d.rounded_rectangle((x, y, x + cw, y + 18), 10, fill=c)
        d.text((x + 28, y + 40), hd, font=fit(d, hd, FB, 36, cw - 56), fill=c)
        f = font(FR, 28)
        for k, l in enumerate(wrap(d, body, f, cw - 56)[:4]):
            d.text((x + 28, y + 96 + k * 40), l, font=f, fill=INK)
    im.save(path)

def bars(path, title, sub, items, unit, note=""):
    """items = [(이름, 값, 보조설명)] 값은 대략치(약)."""
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im); head(d, title, sub)
    n = len(items); top = 190; gap = 18; rh = (H - top - 70 - gap * (n - 1)) // n
    mx = max(v for _, v, _ in items)
    bx, bw = 330, 560
    for i, (nm, v, ex) in enumerate(items):
        y = top + i * (rh + gap); c = PAL[i % 6]
        d.text((60, y + rh / 2), nm, font=fit(d, nm, FB, 32, 250), fill=INK, anchor="lm")
        d.rounded_rectangle((bx, y + 8, bx + bw, y + rh - 8), 18, fill="#F1E7DF")
        d.rounded_rectangle((bx, y + 8, bx + max(40, int(bw * v / mx)), y + rh - 8), 18, fill=c)
        d.text((bx + bw + 20, y + rh / 2), ex, font=fit(d, ex, FB, 30, W - bx - bw - 70), fill=INK, anchor="lm")
    if note: d.text((60, H - 44), note, font=font(FR, 24), fill=MUTE)
    im.save(path)

def out(slug, n):
    p = os.path.join(ROOT, "assets", "shop", slug); os.makedirs(p, exist_ok=True)
    return os.path.join(p, f"{n}.png")

def build_all():
    from posts_1031_graphics import SPECS
    for slug, specs in SPECS.items():
        for n, (kind, args) in enumerate(specs, 1):
            globals()[kind](out(slug, n), *args)
    print("graphics", sum(len(v) for v in SPECS.values()))

if __name__ == "__main__":
    import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); build_all()
