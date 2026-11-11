# K링크 소스

`/klink/index.html`은 이 폴더의 소스를 한 파일로 묶은 결과물입니다.

- `src/` 화면·일정 엔진 코드, `build/places.json` 장소 데이터, `build/geo.json` 지도 경계 데이터
- 묶기: `python3 scripts/klink/tools/build.py scripts/klink klink/index.html klink/around.json`
- `klink/around.json`은 `scripts/build.py`가 사이트를 빌드할 때 만듭니다(여행 가이드·맛집 기록 연결 데이터).
  새 여행 가이드(`travel-<지역>.html`)나 맛집 지역이 생기면 사이트 빌드만 다시 하면 K링크에 이어집니다.
- K링크에 새 지역을 넣을 때는 `scripts/build.py`의 `KLINK_REGIONS`에도 같은 id를 추가합니다.
