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
    return 0
if __name__ == "__main__": sys.exit(main())
