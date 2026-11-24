# 매일 콘텐츠 작성 브리프 (2026-11-25)

aroundtool.com(어라운드툴) 여행·맛집·가이드 글과 K링크(aroundtool.com/klink, 여행 지도) 명소 안내를 쓴다. 저장소: /home/claude/transtool
**지정한 파일 하나만 만든다** (다른 파일·git 건드리지 않음). 파일 맨 위 docstring에 확인일 2026-11-25, 못 쓴 것·확인 못 한 숫자 메모.

## 형식 예시 (완성본, 그대로 따라 한다)
- 글(ARTICLES)·명소 안내(SPOTS)·새 지역 장소(PLACES): scripts/daily_1121b/sokcho.py, scripts/daily_1121b/daegu.py, scripts/daily_1121b/kobe.py
- 꿀팁만(SPOTS): scripts/daily_1121b/tips_jp_a.py
- 가이드(GUIDE dict): scripts/daily_1121b/guide_kl.py, scripts/daily_1121b/hiroshima.py (GUIDE)
- 계산기: scripts/calc_1121b.py + src/tools/danyang_trip_budget_calculator.html, src/tools/vietnam_dong_phuquoc_budget_calculator.html
- 페이지 생성 방식 참고: scripts/daily_1121b/__init__.py

```python
ARTICLES = [ dict(kind="trip"|"season", slug=..., region=..., places=[K링크 장소 id, ...], kw=("키워드", 검색수), name=짧은 이름,
             title=..., desc=..., intro=..., first="먼저 알아둘 것: ...", cards=[(h2, html), ...3~5개], table=([머리], [[...],...]),
             tip=..., faq=[(질문, 답)]*5, sources=[("이름 (확인 2026.11.25)", url), ...]) ]
SPOTS = { 장소id: dict(one=, see=[3개], facts=dict(hours,fee,stay,when,access), tips=[2~3개], src=[(이름,url)], checked="2026-11-25", photo=None) }
PLACES = {}   # 새 지역 담당만
STAYS = []    # 새 지역 담당만
```

## 글 구성 (대표 확정 시안, 바꾸지 않음)
제목+한 줄 소개(intro) → 먼저 알아둘 것(first, 결론 2~3문장) → 카드 3~5개(h2 짧게, 조건은 괄호) → 정리 표 1개(첫 열 짧은 이름, 칸 한두 줄) → 노란 실전 팁(tip 1~2문장) → 자주 묻는 질문 5개 → 근거 자료. 요약형(휴대폰 한 화면 반~두 화면), 해요체, 짧은 문장. 이모지·색 표현 금지. '비슷한 글' 목록 넣지 않음.
- title: 지정 키워드를 맨 앞에. 띄어쓰기는 자연스럽게("춘천가볼만한곳" → "춘천 가볼만한곳"). 사이트 기존 글 제목과 겹치지 않게(ls /home/claude/transtool/*.html | grep <지역> 후 <title> 확인).
- desc: 120자 안팎 '~정리했습니다.', 기존 글 설명과 다르게. intro: 한 문장, 핵심어 <b>굵게</b>.
- 카드 HTML은 <p>·<ul><li>·<ol><li>·<b>·<a href="/...">만. 사이트 내부 링크는 실제 있는 파일만(ls로 확인). 같은 지역 기존 글(travel-<지역>.html 등)에 1~2번 링크.
- 해외 지역 글도 kind="trip" (맛집 글이라도 travel-<지역>-food), 국내 먹거리 글만 kind="season"(slug season-<영문>).

## K링크 연결 (중요)
- places 에 이 글이 다루는 K링크 장소 id. **그 장소의 K링크 이름을 본문에 정확히 그대로 3번 이상**(제목에 들어가면 더 좋음).

## 사실 확인
- 공식 출처만: 지자체·한국관광공사(visitkorea.or.kr, ktriptips.com)·시설 공식 사이트·국가유산청·국립공원공단·현지 관광청·JNTO·시설 공식. 블로그·여행사 후기 금지(언론은 공식 발표 인용일 때 보조).
- WebSearch로 찾고 필요하면 web-fetch 에이전트/WebFetch로 열어 숫자 확인. 근거 자료 이름 끝에 "(확인 2026.11.25)".
- 바뀔 수 있는 수치는 '약'·'(2026년 기준)'. 확인 못 한 시간·요금은 '방문 전 확인'. **지어내지 않는다.**
- 가게 이름은 공식 출처(지자체 지정·공식 사이트)가 있을 때만. 후기처럼 쓰지 않음("먹어 보니" 금지). 예약 대행·흥정 문구 금지.
- 해외 요금은 현지 통화 그대로(엔·페소·바트·달러), 환산하지 않음(계산기 예시는 예외).
- 근거가 모자라 글을 못 쓰면 쓰지 말고 보고.

## SPOTS (명소 안내, K링크 장소 화면)
- one 두 문장 이내, see 정확히 3개, facts 5개(hours·fee·stay·when·access), tips 2~3개(구체적인 한 문장: 휴무·붐비는 시간 피하기·표 사는 법·동선·현금/카드 등. 빈말 금지), src 1~3개 공식, checked="2026-11-25", photo=None.

## 새 지역 담당만: PLACES·STAYS
- 국내: PLACES = { id: dict(ko=("이름","한 줄 설명 20자 안팎"), en=("Name","one-line"), zh=("名称","说明"), ja=("名前","説明"), lat=, lng=, o=[여는 시각, 닫는 시각](24시간제 소수, 상시 [0,24]), cost=성인 요금(원, 무료 0), closed=[쉬는 요일 0=일~6=토], best="am"|"day"|"eve"|"night"|"any", meal=None|"any", h=머무는 시간, cat="palace"|"nature"|"food"|"shop"|"night"|"fun"|"cafe", st="도로명 주소") }
- 해외: 위와 같되 cost=0, st="" 가능.
- 좌표는 공식 주소/시설 기준 소수 4자리. id는 지정 접두어(예: cc_).
- STAYS = [ (id, lat, lng, ["ko 권역 이름","zh","en","ja"], ["ko 한 줄 설명","zh","en","ja"]) ] 2곳 (숙소 권역: 역·터미널·해변 주변 등, 상호 아님).
- 장소 이름은 흔한 낱말 하나(시장·해변·케이블카·야시장·전망대·워킹스트리트)만으로 짓지 말고 고유한 부분을 포함(예: '파타야 워킹 스트리트').

## 끝나면
`python3 -c "import ast;ast.parse(open('파일').read())"` 통과 확인. 마지막 답변 3~8줄: 쓴 글/장소 수·제목, 못 쓴 것과 이유, 확인이 애매한 숫자.
