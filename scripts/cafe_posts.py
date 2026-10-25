# -*- coding: utf-8 -*-
"""
카페 게시용 글 만들기: 페이지마다 '제목(검색 많은 키워드 + 설명) / 본문 1,500자 이내 + 링크'.
하루 5개씩 _cafe/day-NN.txt 로 나눠 저장합니다.  python3 scripts/cafe_posts.py
키워드 순서는 실제 검색량 데이터가 아니라 일반적으로 검색이 많은 생활 키워드 기준의 추정입니다.
"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from calc_content import CALCS  # noqa: E402
from guides import GUIDES  # noqa: E402

SITE = "https://www.aroundtool.com"
# (파일, 제목, 첫 문장)
QUEUE = [
    ("salary_calculator", "연봉 실수령액 계산기 — 2026년 4대보험 올라서 월급 얼마나 줄었는지 확인", "올해 월급 명세서 보고 실수령액이 줄어든 것 같아서 직접 계산해 봤어요."),
    ("severance_calculator", "퇴직금 계산기 — 평균임금·상여금까지 넣어서 내 퇴직금 바로 계산", "퇴사 앞두고 퇴직금이 얼마나 나올지 궁금하신 분들 많으시죠."),
    ("unemployment_benefit_calculator", "실업급여 계산기 — 2026년 상한액 68,100원 기준 하루·총액 계산", "실업급여 신청 전에 하루에 얼마, 며칠 받는지 먼저 계산해 보세요."),
    ("holiday_pay_calculator", "주휴수당 계산기 — 알바 주 15시간 이상이면 주휴수당 얼마?", "알바하시는 분들, 주휴수당 제대로 받고 계신지 한번 확인해 보세요."),
    ("guide-minimum-wage-2027", "2027년 최저임금 1만700원 — 월급 223만원, 주휴수당까지 정리", "내년 최저임금이 1만700원으로 확정됐어요. 월급으로 얼마인지 정리해 봤습니다."),
    ("loan_calculator", "대출 이자 계산기 — 원리금균등·원금균등 월 상환금 비교", "대출 받기 전에 상환 방식에 따라 이자가 얼마나 차이 나는지 비교해 보세요."),
    ("exchange_rate_calculator", "환율 계산기 — 달러·엔화·위안 원화로 바로 환산", "해외여행이나 직구할 때 환율 계산 번거로우셨죠."),
    ("character_counter", "글자수 세기 — 자소서 공백 포함·제외 글자수 바로 확인", "자소서 쓸 때 글자수 제한 맞추느라 고생하셨던 분들께 추천해요."),
    ("spell_checker", "맞춤법 검사기 — 자주 틀리는 표현 70개 자동으로 찾아줌", "보고서나 자소서 내기 전에 맞춤법 한 번 더 점검해 보세요."),
    ("age_calculator", "만 나이 계산기 — 생년월일 넣으면 오늘 기준 만 나이·띠", "만 나이 통일법 이후로 내 나이가 헷갈리시는 분들 많으시죠."),
    ("pto_calculator", "연차 계산기 — 입사일로 내 연차 개수·연차수당 계산", "올해 연차가 몇 개인지, 남은 연차 수당은 얼마인지 궁금하셨다면."),
    ("car_tax_calculator", "자동차세 계산기 — 배기량·연식으로 올해 자동차세 미리 계산", "6월·12월 자동차세 고지서 나오기 전에 미리 계산해 볼 수 있어요."),
    ("electricity_bill_calculator", "전기요금 계산기 — 누진제 구간별로 이번 달 전기세 계산", "에어컨·전기장판 쓰는 달엔 전기요금이 걱정되죠."),
    ("acquisition_tax_calculator", "부동산 취득세 계산기 — 생애최초·신생아 감면까지 반영", "집 사기 전에 취득세가 얼마인지 꼭 계산해 보셔야 해요."),
    ("brokerage_fee_calculator", "복비 계산기 — 매매·전월세 중개보수 법정 상한 계산", "이사 갈 때 부동산 중개수수료 얼마 내야 하는지 헷갈리시죠."),
    ("bmi_calculator", "BMI 계산기 — 키·몸무게로 비만도 판정 (한국 기준)", "건강검진 전에 내 BMI가 정상 범위인지 확인해 보세요."),
    ("bmr_calculator", "기초대사량 계산기 — 다이어트 전 내 BMR 먼저 확인", "다이어트 시작할 때 기초대사량부터 알면 계획 세우기 쉬워요."),
    ("calorie_calculator", "하루 권장 칼로리 계산기 — 감량 목표에 맞춰 섭취량 계산", "살 빼려면 하루에 얼마나 먹어야 할지 궁금하셨다면."),
    ("due_date_calculator", "출산예정일 계산기 — 마지막 생리일로 예정일·임신 주수", "임신 확인하고 출산예정일이 언제인지 궁금하신 분들께."),
    ("date_calculator", "날짜 계산기 — D-day·100일·두 날짜 사이 며칠인지", "기념일 100일이 언제인지, 시험까지 며칠 남았는지 바로 계산돼요."),
    ("japan_travel_calculator", "일본 여행 경비 계산기 — 오사카·도쿄 여행 비용 얼마?", "일본 여행 준비하면서 총 경비가 얼마나 들지 계산해 봤어요."),
    ("savings_calculator", "적금 이자 계산기 — 단리·월복리 세후 수령액 계산", "적금 만기 때 실제로 손에 쥐는 금액, 세금까지 빼고 계산해 보세요."),
    ("parental_leave_calculator", "육아휴직급여 계산기 — 2026년 바뀐 기준으로 월 수령액", "육아휴직 들어가기 전에 한 달에 얼마 받는지 계산해 보세요."),
    ("hourly_monthly_wage_calculator", "시급 월급 계산기 — 시급으로 월급·주급·연봉 환산 (주휴 포함)", "시급만 알고 월급이 얼마인지 헷갈릴 때 쓰기 좋아요."),
    ("service_years_calculator", "근속연수 계산기 — 입사일·퇴사일로 근속기간 년·월·일", "퇴직금이나 연차 계산하려면 근속기간부터 정확히 알아야 해요."),
    ("guide-severance-pay-conditions", "퇴직금 받는 조건 — 1년 미만·알바도 받나? 14일 이내 지급", "퇴직금 받을 수 있는지 헷갈리시는 분들 위해 조건만 정리했어요."),
    ("guide-unemployment-benefit-conditions", "실업급여 조건 — 자진퇴사도 받는 경우 정리", "자진퇴사하면 실업급여 못 받는 줄 아셨다면 꼭 보세요."),
    ("guide-annual-leave-rules", "연차 몇 개? 1년 미만 월 1개, 1년 15개, 최대 25개", "연차 개수 계산법을 표로 한 번에 정리했어요."),
    ("guide-weekly-holiday-pay-rules", "주휴수당 조건 — 주 15시간·개근이면 받는다", "주휴수당 받을 수 있는지 조건부터 확인해 보세요."),
    ("guide-year-end-tax-schedule", "연말정산 언제? 12월 전에 꼭 챙길 공제 정리", "연말정산 준비는 12월이 가기 전에 해야 해요."),
    ("guide-income-tax-filing-may", "종합소득세 신고 기간 5월 — 프리랜서 3.3% 환급", "프리랜서분들, 5월 종합소득세 신고로 환급받을 수 있어요."),
    ("guide-severance-pay-formula", "퇴직금 계산 방법 — 월급 300만원 5년이면 얼마?", "퇴직금 계산 공식을 예시로 쉽게 풀어 봤어요."),
    ("guide-korean-age-rules", "만 나이 계산법 — 생일 지났으면 연도 차이 그대로", "만 나이 계산이 헷갈리시는 분들 위해 정리했어요."),
    ("guide-bmi-normal-range", "BMI 정상 범위 18.5~22.9 — 키별 정상 체중표", "내 키에 정상 체중이 몇 kg인지 표로 정리했어요."),
    ("dsr_calculator", "DSR 계산기 — 대출 가능한지 DSR 40% 기준 확인", "주담대·신용대출 받기 전에 DSR부터 계산해 보세요."),
    ("ltv_calculator", "LTV 계산기 — 주택담보대출 한도 미리 계산", "집 살 때 대출이 얼마까지 나오는지 LTV로 먼저 확인해 보세요."),
    ("freelancer_tax_calculator", "프리랜서 종합소득세 계산기 — 3.3% 환급 예상액", "3.3% 떼인 프리랜서라면 환급받을 수 있는지 계산해 보세요."),
    ("gas_bill_calculator", "도시가스 요금 계산기 — 계량기 숫자로 가스비 계산", "겨울 난방비 걱정될 때 가스요금 미리 계산해 볼 수 있어요."),
    ("fuel_economy_calculator", "유류비 계산기 — 거리·연비로 주유비 계산", "장거리 운전 전에 기름값이 얼마나 들지 계산해 보세요."),
    ("pyeong_calculator", "평수 계산기 — 평↔㎡ 변환, 전용·공급면적 정리", "아파트 평수랑 제곱미터 헷갈릴 때 바로 변환돼요."),
    ("discount_calculator", "할인율 계산기 — 정가·할인율로 결제 금액 계산", "세일 기간에 얼마 할인되는지 바로 계산돼요."),
    ("percent_calculator", "퍼센트 계산기 — 몇 %인지, N%가 얼마인지", "퍼센트 계산 헷갈릴 때 쓰는 계산기예요."),
    ("dutch_pay_calculator", "더치페이 계산기 — 모임 비용 N분의 1 정산", "회식·여행 비용 나눌 때 편하게 쓰세요."),
    ("pension_age_calculator", "국민연금 수령 나이 계산기 — 출생연도별 수급 연령", "국민연금 몇 살부터 받는지 출생연도로 바로 확인돼요."),
    ("compound_calculator", "복리 계산기 — 원금·수익률·기간으로 미래 자산", "복리의 힘, 직접 숫자로 확인해 보세요."),
]


def clean(h):
    h = re.sub(r"<tr>\s*<th>(.*?)</th>(.*?)</tr>", lambda m: "· " + m.group(1) + ": " + re.sub(r"</td>\s*<td>", " / ", m.group(2)) + "\n", h, flags=re.S)
    h = re.sub(r"<li>\s*<b>(.*?)</b>\s*<span>(.*?)</span>\s*</li>", r"· \1 — \2\n", h, flags=re.S)
    h = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>|</table>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h))
    t = "\n".join(re.sub(r"[ \t]+", " ", ln).strip() for ln in t.splitlines())
    t = re.sub(r"(?<=[^\n])\n(?=[^\n·Q A0-9])", " ", t) if False else t
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def page_parts(f):
    slug = f
    if f.startswith("guide-"):
        g = next(x for x in GUIDES if "guide-" + x["slug"] == f)
        return clean(g["answer"]), [(q, a) for q, a in g["faq"]], [clean(b) for _, b in g["body"]][:2]
    if slug in CALCS:
        c = CALCS[slug]
        return clean(c["answer"]), [(q, a) for q, a in c["faq"]], ["이렇게 쓰면 돼요\n" + "\n".join(f"{i + 1}. {clean(s)}" for i, s in enumerate(c["steps"]))]
    h = open(f"{f}.html", encoding="utf-8").read()
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', h).group(1))
    faqs = re.findall(r"<summary>(.*?)</summary>\s*<div[^>]*>(.*?)</div>", h, re.S)
    return desc, [(clean(q), " ".join(clean(a).split())) for q, a in faqs], []


def post(f, title, hook):
    ans, faqs, extra = page_parts(f)
    url = f"{SITE}/{f}.html"
    def body(nf, ne):
        parts = [hook, "", ans, ""]
        for e in extra[:ne]:
            parts += [e, ""]
        if faqs[:nf]:
            parts += ["자주 묻는 질문"]
            for q, a in faqs[:nf]:
                parts += [f"Q. {q}", f"A. {a}", ""]
        parts += ["직접 숫자 넣어서 계산해 보시려면 아래 페이지에서 바로 확인하실 수 있어요. 로그인 없이 무료예요." if not f.startswith("guide-")
                  else "자세한 표와 관련 계산기는 아래 페이지에 정리해 두었어요.", url]
        return "\n".join(parts)
    for nf, ne in [(3, 2), (2, 2), (2, 1), (1, 1), (1, 0), (0, 0)]:
        b = body(nf, ne)
        for a_, b_ in [("위 계산기에서", "링크의 계산기에서"), ("위 표에서", "링크의 표에서"), ("아래 표", "링크의 표"), ("위 표", "링크의 표")]:
            b = b.replace(a_, b_)
        if len(b) <= 1500:
            return title, b
    return title, b[:1450] + "…\n" + url


def main():
    os.makedirs("_cafe", exist_ok=True)
    for i in range(0, len(QUEUE), 5):
        day = i // 5 + 1
        out = [f"[카페 게시용 {day}일차] — 하루 5개 이내, 게시판 성격에 맞는 곳에 올려 주세요\n"]
        for n, (f, title, hook) in enumerate(QUEUE[i:i + 5], 1):
            t, b = post(f, title, hook)
            out += ["=" * 40, f"#{n}  제목: {t}", f"(본문 {len(b)}자)", "-" * 40, b, ""]
        open(f"_cafe/day-{day:02d}.txt", "w", encoding="utf-8").write("\n".join(out))
    print(f"{len(QUEUE)}개 → {(len(QUEUE) + 4) // 5}일치")


if __name__ == "__main__":
    main()
