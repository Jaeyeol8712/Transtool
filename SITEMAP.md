# 사이트 구조와 빌드 방법 (2026-10-23 개편)

## 한 번에 다시 만들기

```bash
pip install beautifulsoup4
python3 scripts/build.py
```

여러 번 실행해도 결과가 같습니다. 각 페이지의 본문은 그대로 두고 `<!-- at:... -->` 주석 사이의
공통 영역(헤더·GNB·브레드크럼·게시판 탭·사이드바·푸터·head 메타·구조화 데이터)만 다시 씁니다.

## 폴더

| 경로 | 역할 |
|---|---|
| `assets/site.css`, `assets/site.js` | 공통 레이아웃(커뮤니티형 헤더·GNB·사이드바·게시판 목록)과 검색·필터 스크립트 |
| `assets/og/` | 공유용 OG 이미지(섹션별 1200×630) |
| `assets/search-index.json` | 사이트 검색 색인 (빌드 시 생성) |
| `scripts/build.py` | 사이트 구조 데이터(지역·계산기 분류·여행·가이드)와 모든 생성 로직 |
| `scripts/calc_content.py` | 계산기 33종의 제목·설명·사용법·공식·FAQ 원고 |
| `src/tools/*.html` | 계산기 33종의 입력 폼과 계산 스크립트 |
| `.github/workflows/seo.yml` | sitemap lastmod 갱신 + IndexNow 전송 (이전엔 루트에 있어 동작하지 않았음) |

## 자주 하는 작업

- **맛집 페이지 추가**: `지역접두사-카테고리.html` 로 저장 후 빌드. 새 지역이면 `build.py` 의 `FOOD_AREAS` 에 추가.
- **계산기 설명 수정**: `scripts/calc_content.py` 수정 후 빌드.
- **새 계산기 추가**: `src/tools/<slug>.html` + `calc_content.py` 항목 + `TOOL_GROUPS` 에 slug 추가 후 빌드.
- **최근 업데이트·공지**: `build.py` 의 `UPDATES` 목록 맨 위에 추가.

빌드가 sitemap.xml, feed.xml, llms.txt, sitemap.html, 홈·허브의 숫자를 모두 자동으로 맞춥니다.

## 2026-10-24 추가

- **구·시 단위 맛집 모아보기** (`haeundae.html`, `jeju-jejusi.html` …): 빌드가 카테고리 글에서 가게 이름을 모아 자동 생성합니다.
- **섹션 간 연결**: 모든 페이지 아래 "함께 보면 좋은 글"이 맛집 ↔ 여행 ↔ 계산기 ↔ 가이드 ↔ 추천 글을 서로 잇습니다.
  규칙은 `build.py` 의 `cross_links()`, `GUIDE_LINKS`, `TRIP_TOOLS`, 추천 글의 `related` 에서 정합니다.
- **계산기 퍼가기** (`embed/<계산기>.html`): 검색 노출 제외(noindex), 출처 링크 포함. 계산기 페이지 아래에 복사 코드가 있습니다.

## 자동 색인

| 대상 | 방식 | 상태 |
|---|---|---|
| 네이버·Bing | IndexNow (`scripts/indexnow.mjs`) — main 에 올라간 바뀐 페이지만 전송 | 동작 중 (`INDEXNOW_KEY` 등록됨) |
| 구글 | 서치콘솔 API 로 sitemap.xml·feed.xml 제출 (`scripts/gsc-sitemap.mjs`) — 푸시마다 + 매주 월요일 | `GSC_SERVICE_ACCOUNT` 등록 시 동작 |

구글 설정 방법
1. Google Cloud Console → 새 프로젝트 → "Google Search Console API" 사용 설정
2. IAM → 서비스 계정 만들기 → 키 → JSON 키 다운로드
3. 서치콘솔 → 설정 → 사용자 및 권한 → 서비스 계정 이메일을 **소유자**로 추가
4. GitHub 저장소 → Settings → Secrets and variables → Actions
   - Secrets: `GSC_SERVICE_ACCOUNT` = JSON 파일 내용 전체
   - Variables: `GSC_SITE` = 서치콘솔 속성 주소 (URL 접두어면 `https://www.aroundtool.com/`, 도메인 속성이면 `sc-domain:aroundtool.com`)

## 방문자 수 표시 (오늘·어제·전체)

- `.github/workflows/visitors.yml` 이 매시간 GA4 에서 숫자를 가져와 `assets/visitors.json` 에 저장하고, 사이드바·푸터가 이 파일을 읽어 표시합니다.
- 기준: GA4 '사용자(활성 사용자)'. 전체는 2024-01-01부터 합계(`VISITORS_SINCE` 로 변경 가능).
- 설정: 구글 자동 제출용 서비스 계정을 그대로 쓰고, GA4 관리 → 속성 액세스 관리에 서비스 계정 이메일을 **뷰어**로 추가하면 됩니다.
- 숫자가 아직 없으면 방문자 줄은 자동으로 숨겨집니다.
