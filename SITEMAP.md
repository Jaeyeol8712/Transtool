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
