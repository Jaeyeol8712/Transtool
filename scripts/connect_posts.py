# -*- coding: utf-8 -*-
"""
쇼핑 추천(브랜드 커넥트 · 쇼핑 커넥트) 글 원고.

글 하나 = POSTS 에 dict 하나. 저장 후 `python3 scripts/build.py` 를 실행하면
shop-<slug>.html 이 만들어지고 메뉴·사이트맵·피드·검색에 자동으로 들어갑니다.

[대가성 표시 — 공정위 「추천·보증 등에 관한 표시·광고 심사지침」 기준으로 자동 처리]
  · 제목 바로 아래(본문 첫 화면)에 경제적 이해관계 문구를 크게 표시
  · 구매 링크 버튼마다 '광고 링크' 표기 + 링크 직전 안내 문구
  · 글 끝에 한 번 더 표시
  · 링크에는 rel="sponsored nofollow noopener" 를 붙여 검색엔진 정책도 지킴
  문구는 DISCLOSURE 에서 프로그램별로 바꿀 수 있습니다.

[필드]
  slug        파일 이름. shop-<slug>.html
  program     "shopping" | "brand"  → DISCLOSURE 문구 선택
  draft       True 면 noindex, 사이트맵·목록에서 제외 (검토용)
  hands_on    실제로 써 본 제품이면 True. False 면 '사용 후기' 표현을 쓰지 않고
              공식 정보 정리 글로 씁니다. (써 보지 않은 제품을 써 본 것처럼 쓰면
              그 자체로 기만 광고가 됩니다)
  keyword     핵심 키워드 1개 (제목·H1·첫 문단·메타 설명에 들어감)
  sub_keywords 보조 키워드 3~6개 (소제목·FAQ에 자연스럽게 분산)
  product     정확한 상품명,  brand  브랜드명
  link        커넥트에서 발급받은 링크 (naver.me 단축 링크 그대로)
  price       {"value": 29900, "date": "2026-10-23"} 또는 None (가격은 변동되므로 확인 날짜 필수)
  title, desc, lede, answer   제목 / 메타 설명 / 한 줄 요약 / 핵심 답변 문단
  specs       [(항목, 값)]   공식 상세페이지에서 확인한 것만
  sections    [(소제목, HTML)]
  fit_yes, fit_no  추천하는 경우 / 맞지 않는 경우
  faq         [(질문, 답변)]
  related     관련 계산기·글 파일명
"""

DISCLOSURE = {
    "shopping": "이 포스팅은 네이버 쇼핑 커넥트 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.",
    "brand": "이 포스팅은 네이버 브랜드 커넥트 활동의 일환으로, 판매 발생 시 수수료를 제공받습니다.",
}

POSTS = [
    # 예시 글은 상품 정보를 받은 뒤 여기에 추가합니다.
]
