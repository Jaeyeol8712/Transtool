# -*- coding: utf-8 -*-
"""데이터 보고판용 JSON 만들기. 사용: python3 scripts/board_data.py <cta-report 체크아웃 폴더> <출력 폴더>
입력: kpi.json, today.json(일간 보고서 요약). 출력: board-*.json (행 배열)."""
import json, os, sys
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
kpi = json.load(open(os.path.join(src, "kpi.json"), encoding="utf-8"))
today = json.load(open(os.path.join(src, "today.json"), encoding="utf-8"))
def w(name, rows):
    json.dump(rows, open(os.path.join(out, name), "w", encoding="utf-8"), ensure_ascii=False)
c, p = kpi["cur"], kpi["prev"]
w("board-kpi.json", [
  {"metric": "사용자", "cur": c["users"], "prev": p["users"]},
  {"metric": "방문", "cur": c["sessions"], "prev": p["sessions"]},
  {"metric": "검색 유입 방문", "cur": kpi["organic"]["cur"], "prev": kpi["organic"]["prev"]},
  {"metric": "조회", "cur": c["views"], "prev": p["views"]},
])
w("board-daily.json", [{"date": f'{d["date"][:4]}-{d["date"][4:6]}-{d["date"][6:]}', "users": d["users"], "sessions": d["sessions"]} for d in kpi["daily"]])
w("board-landing.json", [{"page": l["page"], "sessions": l["sessions"]} for l in kpi["landing"]])
ch = kpi["channels"]
w("board-channels.json", [{"channel": k, "cur": v, "prev": ch["prev"].get(k, 0)} for k, v in sorted(ch["cur"].items(), key=lambda x: -x[1])])
g = kpi["google"]
w("board-google.json", [
  {"metric": "클릭", "cur": g["cur"]["clicks"], "prev": g["prev"]["clicks"]},
  {"metric": "노출", "cur": g["cur"]["impressions"], "prev": g["prev"]["impressions"]},
  {"metric": "평균 순위", "cur": round(g["cur"]["position"], 1), "prev": round(g["prev"]["position"], 1)},
])
daily = next((r for r in today["reports"] if r["type"] == "daily"), None)
if daily:
    k, pk = daily["kpi"], daily.get("prev") or {}
    w("board-cta.json", [
      {"metric": "추천 글 조회", "cur": k["views"], "prev": pk.get("views", 0)},
      {"metric": "추천 글 본 사람", "cur": k["viewers"], "prev": pk.get("viewers", 0)},
      {"metric": "버튼 클릭", "cur": k["clicks"], "prev": pk.get("clicks", 0)},
      {"metric": "버튼 누른 사람", "cur": k["clickers"], "prev": pk.get("clickers", 0)},
    ])
    w("board-posts.json", [{"post": x["post"], "views": x["views"], "clicks": x["clicks"]} for x in daily["topPosts"]])
meta = {"made": kpi["made"], "range": kpi["range"], "prevRange": kpi["prevRange"], "googleRange": g["range"], "ctaDay": daily["title"] if daily else ""}
w("board-meta.json", [meta])
print("ok", sorted(os.listdir(out)))
