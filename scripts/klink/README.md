# K링크 소스

`/klink/index.html`은 이 폴더의 소스를 한 파일로 묶은 결과물입니다.

- `src/` 화면·일정 엔진 코드, `build/places.json` 장소 데이터, `build/geo.json` 지도 경계 데이터
- 묶기: `python3 scripts/klink/tools/build.py scripts/klink klink/index.html klink/around.json`
- `klink/around.json`은 `scripts/build.py`가 사이트를 빌드할 때 만듭니다(여행 가이드·맛집 기록 연결 데이터).
  새 여행 가이드(`travel-<지역>.html`)나 맛집 지역이 생기면 사이트 빌드만 다시 하면 K링크에 이어집니다.
- K링크에 새 지역을 넣을 때는 `scripts/build.py`의 `KLINK_REGIONS`에도 같은 id를 추가합니다.

## 해외 도시 (2026-11-12 추가)

- 원본: `tools/overseas_data.py` — 어라운드툴 해외 여행 가이드(`travel-<id>.html`)의 '지역별 볼거리'에 나온 곳만 넣는다.
  새 해외 가이드를 올리면 같은 id로 도시를 추가한다(공항 A, 숙소 권역 S, 구역 Z, 장소 P).
- 빌드: `python3 scripts/klink/tools/build_overseas.py <earth-lands-250m map.geo.json> [--keep-world]`
  - 땅 경계: `npm i @geo-maps/earth-lands-250m` 의 `map.geo.json` (OpenStreetMap · ODbL, 화면에 출처 표기)
  - `--keep-world`: 해외 전체 지도는 그대로 두고 도시 지도만 다시 만든다(전체 지도는 6~7분 걸림)
  - 장소 문구만 바꿨다면 경계 파일 없이 돌려도 된다(places·overseas·regions만 갱신)
  - '바다 위로 보이는 좌표'가 나오면 섬·바다 투어처럼 원래 바다인 곳인지 확인한다
- 결과: `build/places.json`(해외 장소 추가), `build/overseas.json`(지역·공항·숙소), `build/regions.json`(사이트 빌드가 읽어 홈·여행 글의 K링크 연결에 씀), `build/geo.json`
- 해외 장소는 `est: 1` — 운영 시간·요금은 일정 계산용 기본값이라 화면에 '현지 확인'으로 보이고 비용 합계에 넣지 않는다.
- 해외 3D 거리는 준비 중(구역을 눌러도 2D 지도). 해외 '예약' 탭은 '준비' 탭(어라운드툴 계산기·가이드)으로 바뀐다.
- 그다음 사이트 빌드(`python3 scripts/build.py`) → K링크 묶기(위 명령) 순서로 돌린다.
