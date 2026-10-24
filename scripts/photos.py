# -*- coding: utf-8 -*-
"""
무료(상업적 이용 가능) 사진 가져오기 — GitHub Actions 에서 실행됩니다.

출처: Openverse (Wikimedia Commons · Flickr 등 CC 라이선스 사진 검색, API 키 불필요)
  · 상업적 이용 가능한 라이선스만: CC0 · 공개 도메인(PDM) · CC BY · CC BY-SA
  · CC BY 계열은 사진 아래에 작가·라이선스 표기가 필요 → build.py 가 자동으로 넣음

사용법
  python3 scripts/photos.py candidates   scripts/photo_queries.json 의 검색어로 후보를 받아
                                          _candidates/<key>.jpg (번호 붙은 모음 이미지)와 meta.json 생성
  고른 사진은 scripts/photos.json 에 메타데이터와 함께 적고
  python3 scripts/photos.py fetch        photos.json 의 사진을 assets/photos/<name>.jpg (가로 960px, 압축)로 저장
"""
import io, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw, ImageFont

UA = "aroundtool.com photo fetcher (https://www.aroundtool.com/contact.html)"
API = "https://api.openverse.org/v1/images/"
OK_LIC = {"cc0", "pdm", "by", "by-sa"}
ROOT = os.path.join(os.path.dirname(__file__), "..")


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def small_url(url, w=1280):
    """Wikimedia 원본은 수십 MB 라서 썸네일 주소로 바꿔 받습니다. 플리커는 작은 크기 접미사를 씁니다."""
    f = re.match(r"(https://(?:live|farm\d+)\.static\.?flickr\.com/.+/\d+_[0-9a-f]+)(?:_[a-z])?\.jpg$", url)
    if f and w <= 640:
        return f.group(1) + ("_n.jpg" if w <= 320 else "_z.jpg")
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/([0-9a-f])/([0-9a-f]{2})/(.+)$", url)
    if m and not url.lower().endswith(".svg"):
        a, b, name = m.groups()
        return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{a}/{b}/{name}/{w}px-{name}"
    return url


def search(q, n=12):
    for attempt in range(3):
        try:
            return _search(q, n)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("요청 한도 — 70초 대기"); time.sleep(70); continue
            raise
    return []


def _search(q, n=12):
    qs = urllib.parse.urlencode({"q": q, "license": ",".join(sorted(OK_LIC)), "license_type": "commercial",
                                 "page_size": n, "mature": "false", "extension": "jpg"})
    data = json.loads(get(API + "?" + qs))
    return [r for r in data.get("results", []) if r.get("license") in OK_LIC and (r.get("width") or 0) >= 900]


def meta_of(r):
    return {k: r.get(k) for k in ("id", "title", "url", "creator", "creator_url", "license", "license_version",
                                  "license_url", "foreign_landing_url", "source", "width", "height")}


def load_img(url, w):
    raw = get(small_url(url, max(w, 640)))
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    return im


def candidates():
    queries = json.load(open(os.path.join(ROOT, "scripts/photo_queries.json"), encoding="utf-8"))
    out = os.path.join(ROOT, "_candidates")
    os.makedirs(out, exist_ok=True)
    font = ImageFont.load_default()
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except Exception:
        pass
    for key, qlist in queries.items():
        seen, picks = set(), []
        for q in qlist:
            try:
                for r in search(q):
                    if r["id"] not in seen:
                        seen.add(r["id"]); picks.append(r)
            except Exception as e:
                print("검색 실패", key, q, e)
            time.sleep(2)
        picks = picks[:8]

        def dl(r):
            try:
                return load_img(r["url"], 320), meta_of(r)
            except Exception as e:
                print("다운로드 실패", r.get("url"), e)
                return None
        res = [x for x in ThreadPoolExecutor(8).map(dl, picks) if x]
        thumbs = [a for a, _ in res]; metas = [b for _, b in res]
        if not thumbs:
            continue
        cols, cw, ch = 4, 320, 240
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cw, rows * ch), "white")
        d = ImageDraw.Draw(sheet)
        for i, t in enumerate(thumbs):
            t = t.copy(); t.thumbnail((cw - 8, ch - 8))
            x, y = (i % cols) * cw + 4, (i // cols) * ch + 4
            sheet.paste(t, (x, y))
            d.rectangle((x, y, x + 46, y + 38), fill="black"); d.text((x + 8, y + 3), str(i + 1), font=font, fill="yellow")
        sheet.save(os.path.join(out, f"{key}.jpg"), quality=80)
        json.dump(metas, open(os.path.join(out, f"{key}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{key}: {len(thumbs)}장")


def fetch():
    photos = json.load(open(os.path.join(ROOT, "scripts/photos.json"), encoding="utf-8"))
    out = os.path.join(ROOT, "assets/photos")
    os.makedirs(out, exist_ok=True)
    for name, m in photos.items():
        path = os.path.join(out, f"{name}.jpg")
        if os.path.exists(path):
            continue
        try:
            im = load_img(m["url"], 960)
            im.save(path, quality=74, optimize=True, progressive=True)
            print("저장", name, im.size)
        except Exception as e:
            print("실패", name, e)
        time.sleep(1)


if __name__ == "__main__":
    {"candidates": candidates, "fetch": fetch}[sys.argv[1]]()
