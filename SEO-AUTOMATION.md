# 색인 자동화 설정 가이드

새 콘텐츠를 올릴 때마다 서치어드바이저와 서치콘솔에 손으로 넣는 일을 없애기 위한 설정입니다.

---

## 먼저 알아야 할 것: 구글은 자동화가 안 됩니다

이건 설정 문제가 아니라 **구글 정책**입니다. 기대치를 정확히 맞추고 시작하는 게 낫습니다.

| 검색엔진 | 자동 색인 요청 | 방법 |
|---|---|---|
| **네이버** | ✅ 가능 | IndexNow |
| **Bing** | ✅ 가능 | IndexNow |
| **Yandex · Seznam · Yep** | ✅ 가능 | IndexNow |
| **구글** | ❌ 불가 | sitemap + 내부 링크가 유일한 정식 경로 |

### 구글이 안 되는 이유

구글에 `Indexing API`가 있긴 합니다. 그런데 공식 문서에 이렇게 적혀 있습니다.

> Indexing API는 JobPosting 또는 VideoObject에 삽입된 BroadcastEvent가 포함된 페이지를 크롤링하는 데만 사용할 수 있습니다.

채용 공고와 실시간 스트리밍 전용입니다. 맛집 페이지나 계산기 페이지에는 **공식적으로 쓸 수 없습니다.**

기술적으로는 아무 URL이나 던져도 200이 돌아옵니다. 그래서 많은 플러그인과 대행사가 이걸 씁니다. 하지만 구글 개발자 존 뮬러가 2025년에 다시 못 박았습니다.

> 스패머들이 Indexing API를 이렇게 오용하는 걸 많이 봅니다. 문서에 적힌 지원 사례만 쓰시길 권합니다.

**페널티를 주지는 않지만 동작을 보장하지도 않습니다.** 이 시리즈가 "근거를 밝힌다"는 원칙으로 만들어진 만큼, 편법은 넣지 않았습니다.

### 그럼 구글은 어떻게 하나

구글에 쓸 수 있는 자동 신호는 **정확한 `lastmod`가 붙은 sitemap** 하나입니다. 그래서 이 설정에는 lastmod를 git 커밋 날짜로 자동 갱신하는 스크립트가 들어 있습니다. lastmod가 부정확하면 구글은 그 값을 아예 무시하기 때문에, 정확하게 유지하는 것 자체가 유일하게 남은 지렛대입니다.

새 지역을 공개한 직후처럼 급할 때만 서치콘솔에서 URL 검사 → 색인 요청을 손으로 하시면 됩니다. **매번이 아니라 지역 단위로 한 번씩**이면 충분합니다.

---

## 설치할 파일

| 파일 | 올릴 위치 | 역할 |
|---|---|---|
| `620d91837f946664dd06905d8202fe8b.txt` | 사이트 **루트** | IndexNow 소유권 증명 키 |
| `feed.xml` | 사이트 **루트** | 네이버 RSS 제출용 |
| `scripts/indexnow.mjs` | 리포 `scripts/` | 색인 요청 스크립트 |
| `scripts/update-sitemap.mjs` | 리포 `scripts/` | lastmod 자동 갱신 |
| `.github/workflows/seo.yml` | 리포 `.github/workflows/` | push 시 자동 실행 |

---

## 설정 순서

### 1. 키 파일 업로드

`620d91837f946664dd06905d8202fe8b.txt` 를 사이트 루트에 올립니다.

올린 뒤 브라우저에서 직접 확인하세요.

```
https://www.aroundtool.com/620d91837f946664dd06905d8202fe8b.txt
```

화면에 키 값만 보여야 합니다. **404가 뜨면 IndexNow가 403으로 거부합니다.**

> 파일 안에는 키 값만 있어야 하고 줄바꿈이나 공백이 없어야 합니다. 이미 그렇게 만들어 뒀습니다.

### 2. GitHub 시크릿 등록

리포지토리 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| 항목 | 값 |
|---|---|
| Name | `INDEXNOW_KEY` |
| Secret | `620d91837f946664dd06905d8202fe8b` |

도메인이 `www.aroundtool.com`이 아니라면 같은 화면의 **Variables** 탭에서 `SITE_HOST`도 등록하세요.

### 3. 스크립트와 워크플로 배치

```
저장소 루트/
├── .github/
│   └── workflows/
│       └── seo.yml
├── scripts/
│   ├── indexnow.mjs
│   └── update-sitemap.mjs
├── 620d91837f946664dd06905d8202fe8b.txt
├── feed.xml
├── sitemap.xml
└── (HTML 파일들)
```

### 4. 네이버 서치어드바이저에 RSS 등록

서치어드바이저 → 사이트 선택 → **요청** → **RSS 제출**

```
https://www.aroundtool.com/feed.xml
```

RSS는 IndexNow와 별개 경로입니다. 둘 다 걸어두면 누락 확률이 줄어듭니다.

### 5. robots.txt 확인

이미 `Sitemap:` 줄이 있습니다. 여기에 RSS도 추가하면 좋습니다.

```
Sitemap: https://www.aroundtool.com/sitemap.xml
Sitemap: https://www.aroundtool.com/feed.xml
```

---

## 이제 어떻게 되나

`main` 브랜치에 HTML을 올리면 자동으로 이렇게 흘러갑니다.

1. 변경된 HTML 파일을 git diff로 찾아냅니다
2. sitemap의 `lastmod`를 실제 커밋 날짜로 고칩니다
3. 바뀐 sitemap을 자동 커밋합니다
4. 네이버·Bing·Yandex·Seznam에 색인 요청을 보냅니다

**손댈 일이 없습니다.** 결과는 리포 **Actions** 탭에서 확인합니다.

### 손으로 돌려야 할 때

Actions 탭 → **SEO 자동화** → **Run workflow**

`sitemap 전체 URL 을 다시 보낼까요?`를 체크하면 77개 전부 다시 보냅니다. 도메인을 옮겼거나 대량으로 고쳤을 때만 쓰세요.

### 로컬에서 테스트

```bash
# 실제로 보내지 않고 대상만 확인
INDEXNOW_KEY=620d91837f946664dd06905d8202fe8b node scripts/indexnow.mjs --dry

# 전체 전송
INDEXNOW_KEY=620d91837f946664dd06905d8202fe8b node scripts/indexnow.mjs --all
```

---

## 응답 코드 읽는 법

| 코드 | 뜻 | 조치 |
|---|---|---|
| `200` / `202` | 접수됨 | 정상 |
| `403` | 키 파일을 못 찾음 | 키 파일 URL이 열리는지 확인 |
| `422` | URL이 host와 불일치 | `SITE_HOST` 값 확인 |
| `429` | 요청이 너무 잦음 | 잠시 후 재시도 |

---

## 오해하기 쉬운 것

**접수 ≠ 색인.** IndexNow가 200을 돌려줘도 그건 "크롤링 대기열에 넣었다"는 뜻이지 검색에 노출된다는 뜻이 아닙니다. 색인 여부는 검색엔진이 페이지를 보고 따로 판단합니다.

**매번 전체를 보내지 마세요.** 바뀌지 않은 URL을 반복 전송하면 신호가 희석되고 429가 뜹니다. 기본 동작인 "변경분만 전송"이 맞습니다.

**구글에 편법을 쓰지 마세요.** Indexing API로 일반 페이지를 밀어 넣는 도구가 많지만, 공식 지원 밖입니다. 정확한 sitemap과 내부 링크가 느려 보여도 정식 경로입니다.

---

## 새 지역을 추가할 때 할 일

앞으로는 이것만 하면 됩니다.

- [ ] 새 HTML 파일과 갱신된 `index.html`, `sitemap.xml`을 커밋 → **자동 색인 요청됨**
- [ ] `feed.xml`에 새 `<item>` 추가 (선택, 네이버 RSS 반영용)
- [ ] 급하면 서치콘솔에서 대표 페이지 1~2개만 손으로 색인 요청

세 번째만 사람 손이 필요하고, 그것도 지역당 한 번이면 충분합니다.
