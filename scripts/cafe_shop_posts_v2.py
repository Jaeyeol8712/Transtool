# -*- coding: utf-8 -*-
"""
추천 모음 카페 글 2차: 같은 페이지를 다른 검색 키워드(세부 키워드)와 질문·답 형식으로.
1차(cafe_shop_posts.py)와 제목·첫머리·구성이 다르게 나오도록 씁니다.
_cafe/shop2-day-NN.txt   python3 scripts/cafe_shop_posts_v2.py
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from connect_posts import POSTS  # noqa: E402
from cafe_shop_posts import block, NOTE, SITE  # noqa: E402

# 슬러그: (제목, 첫머리 2~3문장)  — 사실 주장 없이 상황·질문으로만 연다
V2 = {
    "queens-collagen-rg3": ("미백 주름 기능성 크림 고르는 법 — 식약처 기능성 표시 확인하기",
        "미백 크림, 주름 크림 종류가 너무 많아서 뭘 기준으로 골라야 할지 모르겠다는 얘기 자주 보여요. 광고 문구보다 먼저 볼 건 상자에 적힌 ‘기능성화장품’ 표시예요. 질문 형식으로 정리해 봤어요."),
    "bespoke-ai-fridge-4door": ("4도어 냉장고 추천 받기 전에 — 용량·키친핏·소비전력 체크",
        "냉장고 바꿀 때가 되면 4도어로 갈지, 몇 L가 맞을지부터 고민되죠. 매장 가기 전에 줄자로 잴 곳과 비교할 숫자를 먼저 정리해 두면 훨씬 수월해요."),
    "galaxy-s26-ultra": ("갤럭시 S26 울트라 256GB vs 512GB — 자급제로 살 때 비교",
        "S26 울트라 자급제로 넘어갈까 고민 중이라면 용량부터 정해야 가격 비교가 쉬워요. 출고가 기준으로 두 용량 차이와 결제 전에 볼 것을 정리했어요."),
    "danang-5days": ("다낭 4박5일 vs 3박5일 — 일정·우기·상품 포함 내역 비교",
        "다낭 여행 상품 보다 보면 3박 5일, 4박 5일이 섞여 있어서 헷갈리죠. 어느 쪽이 나한테 맞는지, 결제 전에 포함 내역에서 뭘 봐야 하는지 질문별로 정리했어요."),
    "prael-thermashot-ultimate": ("고주파 뷰티 디바이스 추천 전 체크 — 프라엘 써마샷 얼티밋 기능 정리",
        "집에서 쓰는 고주파 기기, 피부과 시술이랑 뭐가 다른지 궁금하셨던 분들 많을 거예요. 제조사 발표 내용을 기준으로 기능과 주의할 점을 정리했어요."),
    "jbl-authentics-200": ("레트로 블루투스 스피커 찾는다면 — JBL 어센틱 200 와이파이 기능 정리",
        "거실에 두고 인테리어 소품처럼 쓸 스피커를 찾다 보면 레트로 디자인 모델이 눈에 들어오죠. 블루투스만 되는지, 와이파이 스트리밍도 되는지부터 확인해 보세요."),
    "bespoke-ai-steam-ultra": ("스팀 로봇청소기 추천 전에 — 일반형·자동 급배수형 차이",
        "물걸레 로봇청소기는 걸레 냄새랑 물통 관리가 제일 귀찮다고들 하죠. 스팀 세척 모델을 볼 때 설치 방식부터 확인해야 하는 이유를 정리했어요."),
    "galaxy-tab-s12-ultra": ("갤럭시탭 S12 울트라 WiFi 256GB — 필기·인강용으로 볼 것",
        "큰 화면 태블릿으로 필기하고 인강 보려는 분들이 울트라 모델을 많이 찾으시죠. 와이파이 256GB 구성이 나한테 충분한지 질문별로 정리했어요."),
    "west-europe-3-10days": ("스위스 여행 코스 추천 — 루체른·융프라우 넣은 서유럽 10일 일정",
        "서유럽 패키지 고를 때 스위스가 며칠 들어가는지, 융프라우까지 올라가는지가 제일 궁금하죠. 프랑스·스위스·이탈리아 10일 일정에서 볼 것을 정리했어요."),
    "student-office-laptop": ("인강용 노트북 추천 사양 — 램·저장공간·무게 기준 정리",
        "새 학기 앞두고 노트북 사려는데 사양표만 보면 다 비슷해 보이죠. 인강·과제·사무용으로 쓸 때 어디서 후회가 많이 나는지 기준만 정리했어요."),
    "mung-bean-cleanser": ("녹두 클렌징폼 고르는 법 — 약산성 pH·전성분 확인하기",
        "약산성 클렌저로 바꿔 보려는 분들 많으시죠. ‘약산성’이라고 적혀 있어도 pH 표기가 있는지, 전성분은 어떻게 보는지 정리했어요."),
    "calf-foot-air-massager": ("공기압 마사지기 추천 받기 전 — 압력 단계·사이즈·타이머 체크",
        "부모님 선물이나 퇴근 후 쓰려고 종아리 마사지기 알아보시는 분들 많아요. 공기압 방식은 사이즈와 압력 단계가 맞는지가 제일 중요해서 그 기준만 정리했어요."),
    "fukuoka-3days": ("후쿠오카 2박3일 코스 — 다자이후·유후인 하루씩 넣는 일정",
        "가깝고 짧게 다녀오기 좋은 후쿠오카, 2박 3일이면 어디까지 갈 수 있을지 궁금하시죠. 시내·다자이후·유후인을 나누는 일정을 정리했어요."),
    "food-waste-disposer": ("가정용 음식물처리기 방식 비교 — 건조식·분쇄식·미생물식",
        "음식물 쓰레기 버리러 나가는 게 일이라 처리기 들일까 고민하시는 분들 많죠. 방식마다 소음·전기·관리가 달라서 먼저 방식부터 고르는 게 좋아요."),
    "wireless-gaming-keyboard": ("기계식 무선 키보드 추천 전 — 트리모드·스위치·배열 정리",
        "게임용 키보드는 유선이 정답이라는 말, 요즘은 꼭 그렇지 않아요. 무선 게이밍 키보드를 고를 때 연결 방식부터 스위치까지 순서대로 정리했어요."),
    "neck-traction": ("목견인기 고르기 전에 — 의료기기 표시와 진료가 먼저인 증상",
        "오래 앉아 일하다 보면 목이 앞으로 빠지는 게 신경 쓰이죠. 목견인기를 알아보기 전에 의료기기인지 확인하는 법과, 기구보다 진료가 먼저인 경우를 정리했어요."),
    "c-type-65w-charger": ("65W 충전기 고르는 법 — PD·PPS·케이블 전류까지 확인",
        "노트북이랑 휴대폰을 충전기 하나로 쓰고 싶어서 65W를 찾는 분들 많으시죠. 같은 65W라도 규격과 케이블에 따라 달라지는 부분을 질문으로 정리했어요."),
}

Q = {"cards": "Q. 핵심만 먼저 알려 주세요", "versus": "Q. 둘 중 뭐가 나을까요?", "check": "Q. 결제 전에 뭘 확인하면 되나요?",
     "tags": "Q. 저한테 맞을까요?", "callout": "Q. 꼭 알아 둘 점은요?", "meter": "Q. 기준이 있나요?"}


def post(p):
    title, opener = V2[p["slug"]]
    url = f"{SITE}/shop-{p['slug']}.html"
    parts = [block(b) for b in p["body"] if not re.fullmatch(r"\{[^}]*\}", b.strip())]
    paras = [t for k, t in parts if k == "p"]
    sec = {}
    for k, t in parts:
        if k in Q and k not in sec:
            sec[k] = re.sub(r"^\[[^\]]*\]\n", "", t) if k != "callout" else t.replace("💡 ", "")
    tail = ("가격과 구성은 판매처·시점마다 달라요. 그림으로 정리한 비교표와 현재 가격 확인 링크는 아래 페이지에 있어요."
            if p.get("kind") != "travel" else "일정 그림과 현재 여행 상품 비용 확인 링크는 아래 페이지에 있어요.")
    # 1차와 다른 순서: 체크리스트 → 비교 → 주의점 → 핵심 → 대상
    order = ["check", "versus", "callout", "cards", "tags", "meter"]
    for drop in [[], ["meter"], ["meter", "tags"], ["meter", "tags", "cards"], ["meter", "tags", "cards", "versus"]]:
        out = [opener]
        for k in order:
            if k in sec and k not in drop:
                out.append(Q[k] + "\n" + sec[k])
        if paras:
            out.append(paras[-1])
        out += [tail, url, NOTE]
        body = "\n\n".join(out)
        if len(body) <= 1500:
            return title, body
    return title, body[:1400] + "…\n\n" + url + "\n\n" + NOTE


def main():
    os.makedirs("_cafe", exist_ok=True)
    order = {x["slug"]: i for i, x in enumerate(POSTS)}
    items = sorted([x for x in POSTS if x.get("live", True)], key=lambda x: (x["date"], order[x["slug"]]))
    for i in range(0, len(items), 5):
        day = i // 5 + 1
        out = [f"[추천 모음 카페 게시용 2차 {day}일차] — 1차와 다른 제목·구성, 하루 5개 이내로 올려 주세요\n"]
        for p in items[i:i + 5]:
            t, b = post(p)
            out += ["=" * 40, t, "", b, ""]
        open(f"_cafe/shop2-day-{day:02d}.txt", "w", encoding="utf-8").write("\n".join(out))
    print(f"{len(items)}개 → {(len(items) + 4) // 5}일치")


if __name__ == "__main__":
    main()
