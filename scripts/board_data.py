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
# 추천 모음 일간 보고서: 일별(최근 7일)·주별(최근 8주) — 추천 글 조회·버튼 클릭 + 사이트 전체 조회수
def ctr(c, v): return round(c / v * 100, 1) if v else None
if daily and daily.get("days7"):
    for d in daily["days7"]:
        rows.append({"id": f'rday-{d["key"]}', "section": "rday", "label": d["label"], "cur": d["views"], "prev": None, "alt": d["clicks"], "chg": None,
                     "viewers": d["viewers"], "clickers": d["clickers"], "ctr": ctr(d["clicks"], d["views"]), "site": d.get("site")})
    for d in daily.get("weeks8") or []:
        rows.append({"id": f'rweek-{d["key"]}', "section": "rweek", "label": d["label"], "cur": d["views"], "prev": None, "alt": d["clicks"], "chg": None,
                     "viewers": d["viewers"], "clickers": d["clickers"], "ctr": ctr(d["clicks"], d["views"]), "site": d.get("site")})
    for i, x in enumerate(daily.get("sources") or []):
        rows.append({"id": f"rsrc-{i}", "section": "rsrc", "label": x["name"], "cur": x["sessions"], "prev": None, "alt": x["users"], "chg": None})
    for i, x in enumerate(daily.get("clickSrc7") or []):
        rows.append({"id": f"rclk-{i}", "section": "rclk", "label": x["channel"], "cur": x["clicks"], "prev": None, "alt": x["keyword"], "chg": None})
    for i, x in enumerate(daily.get("keywords") or []):
        rows.append({"id": f"rkw-{i}", "section": "rkw", "label": x["query"], "cur": x["sessions"], "prev": None, "alt": x["engine"], "chg": None})
# 맨 위: 어제 하루(그제 대비) / 아래: 주별(월~일)
if kpi.get("yday"):
    yd, y0 = kpi["yday"], kpi["yday0"]
    for key, lab in (("users", "사용자"), ("sessions", "방문"), ("organic", "검색 유입 방문"), ("views", "조회")):
        add("yday", key, lab, yd[key], y0[key])
    def wlab(w): return f'{int(w["start"][5:7])}.{int(w["start"][8:])}~' + (f'{int(w["end"][5:7])}.{int(w["end"][8:])}' if w.get("done", w.get("complete", True)) else "(진행 중)")
    for w_ in kpi.get("weeks", []):
        rows.append({"id": f'wsite-{w_["key"]}', "section": "wsite", "label": wlab(w_), "cur": w_["users"], "prev": None, "alt": w_["sessions"], "chg": None,
                     "organic": w_["organic"], "views": w_["views"], "done": w_["done"]})
    done = [w_ for w_ in kpi.get("weeks", []) if w_["done"]]
    if len(done) >= 1:
        c_, p_ = done[-1], (done[-2] if len(done) >= 2 else None)
        for key, lab in (("users", "사용자"), ("sessions", "방문"), ("organic", "검색 유입 방문"), ("views", "조회")):
            add("week", key, lab, c_[key], p_[key] if p_ else None)
    lw = kpi.get("lastWeek") or {}
    for i, l in enumerate(lw.get("landing", [])): add("wland", i, l["page"], l["sessions"])
    chw = lw.get("channels") or {"cur": {}, "prev": {}}
    for i, (k, v) in enumerate(sorted(chw["cur"].items(), key=lambda x: -x[1])): add("wchan", i, k, v, chw["prev"].get(k, 0))
    gws = kpi.get("googleWeeks") or []
    for w_ in gws:
        rows.append({"id": f'gweek-{w_["key"]}', "section": "gweek", "label": wlab({**w_, "done": w_["complete"]}), "cur": w_["clicks"], "prev": None, "alt": w_["impressions"], "chg": None, "position": w_["position"]})
    gdone = [w_ for w_ in gws if w_["complete"]]
    if gdone:
        c_, p_ = gdone[-1], (gdone[-2] if len(gdone) >= 2 else None)
        add("gw", "clicks", "클릭", c_["clicks"], p_["clicks"] if p_ else None)
        add("gw", "impressions", "노출", c_["impressions"], p_["impressions"] if p_ else None)
        add("gw", "position", "평균 순위", c_["position"], p_["position"] if p_ else None)
        meta["gwRange"] = f'{c_["start"]} ~ {c_["end"]}'
    meta["yday"] = yd["date"]
    meta["weekRange"] = f'{done[-1]["start"]} ~ {done[-1]["end"]}' if done else ""
    meta["lwRange"] = lw.get("range", "")
# K링크 (2026-11-12 컨펌 i261112-09): kpi.json 'klink' — 7일·전주. 이벤트(i261112-14)가 생기면 숫자 키가 더 붙어도 그대로 표에 나온다.
kl = kpi.get("klink") or {}
if isinstance(kl.get("cur"), dict):
    kc, kp = kl["cur"], kl.get("prev") or {}
    KL = (("views", "K링크 조회"), ("users", "K링크 사용자"), ("fromSite", "사이트 글→K링크"), ("fromTravel", "여행 글→K링크"))
    for key, lab in KL:
        if isinstance(kc.get(key), (int, float)): add("klink", key, lab, kc[key], kp.get(key))
    EVL = {"klink_save": "장소 저장", "klink_course": "코스 담기", "klink_plan": "일정 만들기", "klink_prep": "준비 탭 클릭", "klink_out": "어라운드툴 글·계산기로 이동"}
    ec, ep = kc.get("events") or {}, kp.get("events") or {}
    for key, v in ec.items():
        if not isinstance(v, (int, float)): continue
        pv = ep.get(key)
        add("klinkev", key, EVL.get(key, key), v, pv if isinstance(pv, (int, float)) else None)
    meta["klink"] = "있음"
elif kl.get("error"):
    meta["klink"] = "오류: " + str(kl["error"])[:80]
m = meta
for k, lab in (("made","갱신"),("range","웹 기간"),("prevRange","비교 기간"),("googleRange","구글 기간"),("ctaDay","추천 모음 기준일"),("yday","어제"),("weekRange","지난주"),("lwRange","지난주 랜딩"),("gwRange","구글 주"),("klink","K링크 지표")):
    if k not in m: continue
    rows.append({"id": f"meta-{k}", "section": "meta", "label": m[k], "cur": None, "prev": None, "alt": lab, "chg": None})
json.dump(rows, open(os.path.join(out, "board.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("ok", len(rows), "rows")
