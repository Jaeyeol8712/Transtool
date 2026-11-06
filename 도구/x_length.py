"""X(트위터) 글자 수 세기 — twitter-text v3 기준.
한글·한자·가나·이모지 = 2, 영문·숫자·기본 기호 = 1, 링크(URL)는 길이와 상관없이 23. 한도 280.
사용: python3 도구/x_length.py 원고.txt  (또는 표준입력)
"""
import re, sys, unicodedata
URL = re.compile(r"https?://\S+|(?:www\.)?[a-z0-9-]+\.(?:com|net|kr|co\.kr|org|io|me)(?:/\S*)?", re.I)
LIGHT = [(0, 4351), (8192, 8205), (8208, 8223), (8242, 8247)]
def weight(ch):
    cp = ord(ch)
    return 1 if any(a <= cp <= b for a, b in LIGHT) else 2
def x_len(text):
    text = unicodedata.normalize("NFC", text)
    n = 0
    for m in URL.finditer(text):
        n += 23
    rest = URL.sub("", text)
    return n + sum(weight(c) for c in rest)
if __name__ == "__main__":
    t = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    n = x_len(t.rstrip("\n"))
    print(f"X 글자 수 {n}/280 · 쓰레드 {len(t.rstrip())}/500 · {'OK' if n <= 280 else f'{n-280} 초과'}")
