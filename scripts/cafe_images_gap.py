# -*- coding: utf-8 -*-
"""빈 칸 보강: 슬롯마다 후보 6장을 받아 _cafeimg2/<day>/<n>/<c>.jpg 로 저장(사람 얼굴 없는 사물 위주 검색어)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from photos import search, search_commons, load_img, meta_of, ROOT
Q = json.load(open(os.path.join(ROOT, "scripts/cafe_images_gap.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "_cafeimg2"); rank = {"cc0": 0, "pdm": 0, "by": 1, "by-sa": 2}
credits, used = {}, set()
for slot, qs in Q.items():
    day, n = slot.split(":"); d = os.path.join(OUT, day, n); os.makedirs(d, exist_ok=True)
    pool = []
    for q in qs:
        try: pool += search(q, 15)
        except Exception as e: print("ov", q, e)
        if len([r for r in pool if r.get("license") in ("cc0", "pdm")]) >= 8: break
    if len(pool) < 6:
        for q in qs:
            try: pool += search_commons(q)
            except Exception as e: print("wc", q, e)
    pool.sort(key=lambda r: rank.get(r.get("license"), 9)); c = 0
    for r in pool:
        if c == 6: break
        if r["url"] in used: continue
        try: im = load_img(r["url"], 800)
        except Exception as e: print("skip", e); continue
        c += 1; used.add(r["url"]); im.save(os.path.join(d, f"{c}.jpg"), quality=78, optimize=True)
        credits[f"{day}/{n}/{c}"] = meta_of(r)
    print(slot, c)
json.dump(credits, open(os.path.join(OUT, "credits.json"), "w"), ensure_ascii=False, indent=1)
