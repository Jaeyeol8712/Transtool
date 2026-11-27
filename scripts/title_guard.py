"""2026-11-25 제목·주소 보호: 이미 있던 글의 <title>이 빌드로 바뀌었거나 글 파일이 사라졌으면 경고합니다.
검색 유입이 있는 글은 제목·URL을 바꾸지 않는 것이 원칙(결정기록 2026-11-25). 바꿔야 하면 서치콘솔 숫자를 먼저 보고 한 번에 몇 개만."""
import re, subprocess, sys
def old(path):
    try: return subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True).stdout
    except Exception: return ""
def title(h):
    m = re.search(r"<title>(.*?)</title>", h or "", re.S); return m.group(1).strip() if m else None
def main():
    out = subprocess.run(["git", "diff", "--name-status", "HEAD", "--", "*.html"], capture_output=True, text=True).stdout.splitlines()
    changed, gone = [], []
    for line in out:
        st, *f = line.split("\t"); f = f[-1]
        if f.startswith(("klink/", "jack/", "_")): continue
        if st.startswith("D"): gone.append(f); continue
        a, b = title(old(f)), title(open(f, encoding="utf-8").read())
        if a and b and a != b: changed.append((f, a, b))
    for f, a, b in changed: print(f"⚠ 제목 변경: {f}\n   전: {a}\n   후: {b}")
    for f in gone: print(f"⚠ 글 삭제: {f} (retire.json으로 noindex → 색인 제외 확인 → 삭제 순서를 지켰는지 확인)")
    if not changed and not gone: print("제목·주소 보호: 바뀐 제목·삭제된 글 없음")
    seo_check()
    return 0
def seo_check():
    """2026-11-28 S7: 색인 대상 페이지의 제목·설명 중복, 설명·canonical·이미지 alt 누락을 셉니다(자동 수정 없음)."""
    import glob, collections
    skip = ("scripts/", "node_modules/", "templates/", "src/")
    t, d = collections.defaultdict(list), collections.defaultdict(list)
    nodesc, nocan, noalt, n = [], [], [], 0
    for f in glob.glob("**/*.html", recursive=True):
        if f.startswith(skip): continue
        h = open(f, encoding="utf-8", errors="ignore").read()
        if "noindex" in h: continue
        n += 1
        a = title(h)
        if a: t[a].append(f)
        m = re.search(r'<meta name="description" content="(.*?)"', h)
        if m: d[m.group(1).strip()].append(f)
        else: nodesc.append(f)
        if 'rel="canonical"' not in h: nocan.append(f)
        if any(not re.search(r'\balt="[^"]+', im) for im in re.findall(r"<img\b[^>]*>", h)): noalt.append(f)
    dt = [v for v in t.values() if len(v) > 1]; dd = [v for v in d.values() if len(v) > 1]
    probs = [("제목 중복", dt), ("설명 중복", dd), ("설명 누락", nodesc), ("canonical 누락", nocan), ("alt 누락 이미지가 있는 글", noalt)]
    bad = [(k, v) for k, v in probs if v]
    for k, v in bad: print(f"⚠ {k} {len(v)}건: {v[:5]}")
    if not bad: print(f"테크니컬 SEO 점검: 색인 대상 {n}쪽, 제목·설명 중복·설명·canonical·alt 누락 0건")
if __name__ == "__main__": sys.exit(main())
