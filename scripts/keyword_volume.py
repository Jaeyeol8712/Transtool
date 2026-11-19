# -*- coding: utf-8 -*-
"""네이버 검색광고 API(keywordstool)로 월간 검색수 조회 → _kw/result.json
입력: scripts/kw_queue.txt (한 줄에 키워드 하나, 띄어쓰기는 자동 제거)
비밀값: NAVER_AD_CUSTOMER_ID · NAVER_AD_API_KEY · NAVER_AD_SECRET (GitHub secrets, 저장소에 남기지 않음)"""
import re, base64, hashlib, hmac, json, os, time, urllib.error, urllib.parse, urllib.request

CID, KEY, SEC = ("".join(os.environ.get(k, "").split()) for k in ("NAVER_AD_CUSTOMER_ID", "NAVER_AD_API_KEY", "NAVER_AD_SECRET"))


def call(hints):
    ts = str(int(time.time() * 1000))
    sig = base64.b64encode(hmac.new(SEC.encode(), f"{ts}.GET./keywordstool".encode(), hashlib.sha256).digest()).decode()
    q = urllib.parse.urlencode({"hintKeywords": ",".join(hints), "showDetail": "1"})
    req = urllib.request.Request(f"https://api.searchad.naver.com/keywordstool?{q}",
                                 headers={"X-Timestamp": ts, "X-API-KEY": KEY, "X-Customer": CID, "X-Signature": sig})
    return json.load(urllib.request.urlopen(req, timeout=30)).get("keywordList", [])


def n(v):
    return 5 if isinstance(v, str) else int(v or 0)  # "< 10" → 5


def main():
    seeds = [l.strip().replace(" ", "") for l in open("scripts/kw_queue.txt", encoding="utf-8") if l.strip() and not l.startswith("#")]
    out = {"checked": time.strftime("%Y-%m-%d %H:%M"), "seeds": {},
           "secrets": {k: len(v) for k, v in (("customer_id", CID), ("api_key", KEY), ("secret", SEC))}, "cid_digits": CID.isdigit()}
    for i in range(0, len(seeds), 5):
        batch = seeds[i:i + 5]
        try:
            rows = call(batch)
        except urllib.error.HTTPError as e:
            out.setdefault("errors", []).append(f"{batch}: {e.code} {re.sub(r'api-key: [^,]+', 'api-key: (가림)', e.read()[:300].decode('utf-8','replace'))}")
            continue
        except Exception as e:  # noqa: BLE001
            out.setdefault("errors", []).append(f"{batch}: {e}")
            continue
        for s in batch:
            rel = [r for r in rows if s in r["relKeyword"] or r["relKeyword"] == s]
            rel = sorted(rel, key=lambda r: -(n(r["monthlyPcQcCnt"]) + n(r["monthlyMobileQcCnt"])))[:30]
            out["seeds"][s] = [{"kw": r["relKeyword"], "pc": n(r["monthlyPcQcCnt"]), "mo": n(r["monthlyMobileQcCnt"]),
                                "total": n(r["monthlyPcQcCnt"]) + n(r["monthlyMobileQcCnt"]), "comp": r.get("compIdx")} for r in rel]
        time.sleep(1)
    os.makedirs("_kw", exist_ok=True)
    json.dump(out, open("_kw/result.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out["seeds"]), "seeds", len(out.get("errors", [])), "errors")


if __name__ == "__main__":
    main()
