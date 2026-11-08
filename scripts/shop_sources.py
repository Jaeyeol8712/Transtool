# -*- coding: utf-8 -*-
"""컨펌 i08: 추천 글 '근거 자료' 목록. 글 slug → [(출처 이름, 공식 url)].
공식 페이지에서 글의 수치와 같은지 확인한 것만 넣는다(확인한 날짜를 주석에). 추천 글 안(이 글의 기준 위)에만 나온다."""

SHOP_SOURCES = {
    # 2026-11-07 확인: 14.6형 2960×1848 120Hz, 5.1mm, 692g(Wi-Fi), 11,600mAh, 45W 약 95분, S펜 포함, 12GB+256GB~, microSD 2TB
    "galaxy-tab-s12-ultra": [
        ("삼성전자 뉴스룸 — 갤럭시 탭 S12 시리즈 공개 (2026.10.1)", "https://news.samsung.com/kr/삼성전자-갤럭시-탭-s12-시리즈-공개"),
    ],
    # 2026-11-07 확인: 90W(THD 1%), 25mm 트위터 2·5인치 우퍼·6인치 패시브, 50Hz~20kHz(-6dB), BT 5.3, Wi-Fi 802.11ax 2.4/5GHz, 3.12kg, AC 전원
    "jbl-authentics-200": [
        ("JBL 공식 지원 페이지 — Authentics 200 사양", "https://support.jbl.com/speakers/speakers-voice-assisted/AUTHENTICS-200.html"),
    ],
}
