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

# 합본: 보고판은 이 파일 하나만 읽는다(행마다 id·section·label·cur·prev·alt·chg)
rows = []
def chg(c, p): return None if not p else round((c - p) / p * 100)
def add(sec, key, label, cur, prev=None, alt=None):
    rows.append({"id": f"{sec}-{key}", "section": sec, "label": label, "cur": cur, "prev": prev, "alt": alt, "chg": chg(cur, prev) if prev is not None else None})
for r in json.load(open(os.path.join(out, "board-kpi.json"), encoding="utf-8")): add("kpi", {"사용자":"users","방문":"sessions","검색 유입 방문":"organic","조회":"views"}[r["metric"]], r["metric"], r["cur"], r["prev"])
for r in json.load(open(os.path.join(out, "board-daily.json"), encoding="utf-8")): add("daily", r["date"], r["date"], r["users"], None, r["sessions"])
for i, r in enumerate(json.load(open(os.path.join(out, "board-landing.json"), encoding="utf-8"))): add("landing", i, r["page"], r["sessions"])
for i, r in enumerate(json.load(open(os.path.join(out, "board-channels.json"), encoding="utf-8"))): add("channel", i, r["channel"], r["cur"], r["prev"])
for r in json.load(open(os.path.join(out, "board-google.json"), encoding="utf-8")): add("google", {"클릭":"clicks","노출":"impressions","평균 순위":"position"}[r["metric"]], r["metric"], r["cur"], r["prev"])
if os.path.exists(os.path.join(out, "board-cta.json")):
    for r in json.load(open(os.path.join(out, "board-cta.json"), encoding="utf-8")): add("cta", {"추천 글 조회":"views","추천 글 본 사람":"viewers","버튼 클릭":"clicks","버튼 누른 사람":"clickers"}[r["metric"]], r["metric"], r["cur"], r["prev"])
    for i, r in enumerate(json.load(open(os.path.join(out, "board-posts.json"), encoding="utf-8"))): add("post", i, r["post"], r["views"], None, r["clicks"])
m = meta
for k, lab in (("made","갱신"),("range","웹 기간"),("prevRange","비교 기간"),("googleRange","구글 기간"),("ctaDay","추천 모음 기준일")):
    rows.append({"id": f"meta-{k}", "section": "meta", "label": m[k], "cur": None, "prev": None, "alt": lab, "chg": None})
json.dump(rows, open(os.path.join(out, "board.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("ok", len(rows), "rows")
