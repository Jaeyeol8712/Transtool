# 매일 콘텐츠 글 작성 브리프 (2026-11-21)

aroundtool.com 여행·시장 글을 쓴다. 글은 K링크(aroundtool.com/klink, 여행 지도)의 장소와 연결된다.
**꼭 먼저 볼 것:** /home/claude/transtool/scripts/daily_1120/gunsan.py (같은 형식의 완성 예시 — ARTICLES·SPOTS·COORDS), /home/claude/transtool/scripts/daily_1120/__init__.py (페이지 생성 방식).

## 출력
지정한 파일 하나만 만든다(다른 파일·git 건드리지 않음). 파일 맨 위 docstring에 확인일 2026-11-21, 못 쓴 글/확인 못 한 숫자 메모.
```python
ARTICLES = [ dict(kind="trip"|"season", slug=..., region=..., places=[K링크 장소 id, ...], kw=("키워드", 검색수), name=짧은 이름,
             title=..., desc=..., intro=..., first="먼저 알아둘 것: ...", cards=[(h2, html), ...3~5개], table=([머리], [[...],...]),
             tip=..., faq=[(질문, 답)]*5, sources=[(이름 (확인 2026.11.21), url), ...]) , ... ]
SPOTS = { 장소id: dict(one=, see=[3개], facts=dict(hours,fee,stay,when,access), tips=[2~3개], src=[(이름,url)], checked="2026-11-21", photo=None) }   # 지시한 경우만, 아니면 {}
COORDS = {}   # 새 지역 담당만: 장소id: (lat, lng) — 브리프 좌표가 공식 주소와 크게 다를 때만
PLACES = {}   # 새 지역 담당만 (아래 참고)
```

## 구성(대표 확정 시안, 바꾸지 않음)
제목+한 줄 소개(intro) → 먼저 알아둘 것(first, 결론 2~3문장) → 카드 3~5개(h2 짧게, 조건은 괄호) → 정리 표 1개(첫 열 짧은 이름, 칸 한두 줄) → 노란 실전 팁(tip 1~2문장) → 자주 묻는 질문 5개 → 근거 자료. 요약형(휴대폰 한 화면 반~두 화면 분량), 해요체, 짧은 문장. 이모지·색 표현 금지. '비슷한 글' 목록 넣지 않음(같은 지역 글 링크는 빌드가 문장으로 자동 추가).
- title: 지정한 키워드를 맨 앞에(예: "경주 황리단길 — 걷는 순서·주차·한옥 카페 거리 정리"). 띄어쓰기는 자연스럽게("경주황리단길" → "경주 황리단길").
- desc: 120자 안팎 '~정리했습니다.' / intro: 한 문장, 핵심어 <b>굵게</b>.
- 카드 HTML은 <p>·<ul><li>·<ol><li>·<b>·<a href="/...">만. 다른 사이트 글 링크는 실제 있는 파일만(ls로 확인, 예: /travel-gyeongju.html).

## K링크 연결 (중요)
- places 에 이 글이 다루는 K링크 장소 id를 넣고, **그 장소의 K링크 이름을 본문에 정확히 그대로 3번 이상** 쓴다(제목에 들어가면 더 좋음). 이름은 아래 각 담당 목록에 준다.
- slug: 여행 글은 `travel-<지역id>-<영문 세부>` (예: travel-gyeongju-hwangnidan), 시장·먹거리 글은 `season-<영문>`.
- 이미 있는 주제와 겹치지 않게: `ls /home/claude/transtool/*.html | grep <지역>` 과 `grep -l "<title>" ...`로 같은 지역 기존 글을 확인하고, 겹치면 각도를 바꾸고 보고.

## 사실 확인
- 공식 출처만: 지자체·관광공사(visitkorea.or.kr, ktriptips는 관광공사 운영)·시설 공식 사이트·국가유산청·현지 관광청·시설 공식 사이트. 블로그·여행사 후기 금지(언론은 공식 발표 인용일 때 보조로).
- WebSearch로 찾고 web-fetch 도구로 열어 숫자를 확인. 근거 자료 이름 끝에 "(확인 2026.11.21)".
- 바뀔 수 있는 수치는 '약'·'(2026년 기준)'. 확인 못 한 시간·요금은 '방문 전 확인'. 지어내지 않는다.
- 가게 이름은 공식 출처(지자체 지정·공식 사이트)가 있을 때만. 후기처럼 쓰지 않음("먹어 보니" 금지). 예약 대행·가격 흥정 문구 금지.
- 근거가 모자라 글을 못 쓰면 쓰지 말고 보고(개수 부족으로 보고해도 됨).

## 새 지역 담당만: PLACES (K링크 장소 데이터)
PLACES = { id: dict(ko=("이름","한 줄 설명 20자 안팎"), en=("Name","one-line"), zh=("名称","说明"), ja=("名前","説明"), lat=, lng=, o=[여는 시각, 닫는 시각] (24시간제 소수, 상시면 [0,24]), cost=성인 요금(국내는 원, 해외는 0), closed=[쉬는 요일 0=일~6=토], best="am"|"day"|"eve"|"night"|"any", meal=None|"any", h=머무는 시간(시간), cat="palace"|"nature"|"food"|"shop"|"night"|"fun"|"cafe", st="주소 또는 가까운 역") }
좌표는 공식 주소 기준 소수 4자리. 해외 장소는 cost=0.

## 끝나면
`python3 -c "import ast;ast.parse(open('파일').read())"` 통과 확인. 마지막 답변 3~8줄: 쓴 글 수·제목, 못 쓴 것과 이유, 확인이 애매한 숫자.
