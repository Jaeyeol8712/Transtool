# -*- coding: utf-8 -*-
"""카페 원고용 무료 이미지 — 원고 1개당 3장. GitHub Actions에서 실행.
CC0·공개 도메인 우선(출처 표기 불필요), 모자라면 CC BY/BY-SA(출처 한 줄 필요).
결과: _cafeimg/<day>/<n>-<k>.jpg (가로 960) + _cafeimg/credits.json → cafe-images 브랜치."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from photos import search, search_commons, load_img, meta_of, ROOT

Q = json.load(open(os.path.join(ROOT, "scripts/cafe_image_queries.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "_cafeimg")
rank = {"cc0": 0, "pdm": 0, "by": 1, "by-sa": 2}
credits, used = {}, set()
for day, posts in Q.items():
    os.makedirs(os.path.join(OUT, day), exist_ok=True)
    for n, qs in enumerate(posts, 1):
        pool = []
        for q in qs:
            try: pool += search(q, 20)
            except Exception as e: print("openverse", q, e)
            if len([r for r in pool if r.get("license") in ("cc0", "pdm")]) >= 6: break
        if len(pool) < 6:
            for q in qs:
                try: pool += search_commons(q)
                except Exception as e: print("commons", q, e)
        pool.sort(key=lambda r: rank.get(r.get("license"), 9))
        k = 0
        for r in pool:
            if k == 3: break
            if r["url"] in used: continue
            try:
                im = load_img(r["url"], 960)
            except Exception as e:
                print("skip", r["url"], e); continue
            k += 1; used.add(r["url"])
            name = f"{n}-{k}.jpg"
            im.save(os.path.join(OUT, day, name), quality=80, optimize=True)
            credits[f"{day}/{name}"] = meta_of(r)
        print(day, n, k)
json.dump(credits, open(os.path.join(OUT, "credits.json"), "w"), ensure_ascii=False, indent=1)
