# -*- coding: utf-8 -*-
"""컨펌 i11(설명 그래픽 글씨 키우기) 1단계: 카드 6개짜리 그래픽 6장을 카드 4개·큰 글씨로 다시 그림.
내용은 기존 그래픽에 있던 사실만 묶어 옮김(새 주장 없음). python3 scripts/shop_graphics_i11.py
글자 크기(1200px 기준): 제목 54 · 부제 32 · 카드 제목 46 · 카드 본문 34 → 휴대폰(약 360px 표시)에서 본문 약 10px 이상."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
INK, MUTE = "#222B36", "#4B5563"
PAL = ["#E4572E", "#1F8F86", "#3B6FD8", "#8B5CDB"]


def font(path, size):
    return ImageFont.truetype(path, size, index=1)


def fit(d, text, path, size, maxw, minsize):
    while size > minsize and d.textlength(text, font=font(path, size)) > maxw:
        size -= 2
    return font(path, size)


def draw(slug, n, title, sub, items, bg="#FFF8F2", size=(1200, 750), numbered=False):
    W, H = size
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    d.text((60, 44), title, font=fit(d, title, FB, 54, W - 120, 44), fill=INK)
    d.text((60, 120), sub, font=fit(d, sub, FR, 32, W - 120, 28), fill=MUTE)
    top, gap = 186, 24
    cw = (W - 120 - gap) // 2
    ch = (H - top - 36 - gap) // 2
    for i, (hd, lines) in enumerate(items):
        x = 60 + (i % 2) * (cw + gap)
        y = top + (i // 2) * (ch + gap)
        c = PAL[i % 4]
        d.rounded_rectangle((x, y, x + cw, y + ch), 26, fill="white", outline=c, width=4)
        hx = x + 32
        if numbered:
            d.ellipse((hx, y + 30, hx + 52, y + 82), fill=c)
            d.text((hx + 26, y + 56), str(i + 1), font=font(FB, 32), fill="white", anchor="mm")
            hx += 70
        else:
            d.rounded_rectangle((hx, y + 26, hx + 64, y + 36), 5, fill=c)
        hy = y + 30 if numbered else y + 50
        d.text((hx, hy + (6 if numbered else 0)), hd, font=fit(d, hd, FB, 46, x + cw - 28 - hx, 36), fill=c)
        by = y + (104 if numbered else 118)
        for k, ln in enumerate(lines[:2]):
            d.text((x + 32, by + k * 48), ln, font=fit(d, ln, FR, 34, cw - 60, 30), fill=INK)
    out = os.path.join(ROOT, "assets", "shop", slug, f"{n}.png")
    im.save(out, optimize=True)
    return out


JOBS = [
    ("galaxy-s26-ultra", 1, "갤럭시 S26 울트라 핵심 사양", "2026년 2월 공개 기준 (보도 종합)", [
        ("6.9형 QHD+", ["프라이버시 디스플레이", "옆에서는 화면이 잘 안 보임"]),
        ("2억 화소 F1.4", ["메인 카메라", "+ 5배 광학 망원 5천만"]),
        ("5,000mAh", ["배터리 용량", "전작과 같음"]),
        ("7.9mm · 214g", ["두께 · 무게", "S펜 내장 (블루투스 없음)"]),
    ], "#F3F1FF", (1200, 750), False),
    ("galaxy-tab-s12-ultra", 1, "갤럭시탭 S12 울트라 핵심 사양", "삼성전자 뉴스룸 발표(2026.10.1) 기준", [
        ("14.6형 120Hz", ["다이내믹 AMOLED 2X", "2960×1848"]),
        ("5.1mm · 692g", ["두께 · 무게", "Wi-Fi 모델 기준"]),
        ("11,600mAh", ["45W 고속 충전", "완충 약 95분"]),
        ("S펜 기본 포함", ["12GB 램 + 256GB부터", "microSD 최대 2TB"]),
    ], "#F1F6FF", (1200, 750), False),
    ("jbl-authentics-200", 1, "JBL 어센틱 200 핵심 사양", "JBL 공식 사양 기준", [
        ("최대 90W", ["스피커 4개 · 2.0 스테레오", "THD 1% 기준"]),
        ("50Hz~20kHz", ["재생 주파수", "-6dB 기준"]),
        ("블루투스 5.3 + Wi-Fi", ["Wi-Fi 6(ax) 지원", "2.4GHz · 5GHz"]),
        ("3.12kg · AC 전원", ["266 × 172 × 167mm", "배터리 없음, 콘센트 사용"]),
    ], "#FFF6F0", (1200, 750), False),
    ("student-office-laptop", 1, "인강·과제·사무용 권장 사양", "이 정도면 수업, 문서, 화상회의를 무리 없이 해요", [
        ("CPU · 램", ["i5 · Ryzen 5급 이상", "램 16GB 권장"]),
        ("저장장치", ["SSD 512GB", "자료가 많으면 1TB"]),
        ("무게 · 배터리", ["들고 다니면 1.5kg 안팎", "배터리는 표기보다 짧을 수 있음"]),
        ("화면", ["14~16인치", "FHD(1920×1080) 이상"]),
    ], "#F6F4FF", (1200, 800), True),
    ("bespoke-ai-steam-ultra", 3, "집 밖에서도 쓰는 기능 & 보안", "SmartThings 연동 · 삼성 녹스 (발표 기준)", [
        ("홈 모니터링 · 순찰", ["밖에서 로봇청소기로 집 안 확인", "움직임이 없으면 집 안 순찰"]),
        ("원격 상담", ["고장 진단 · 조치를", "원격으로"]),
        ("녹스 볼트", ["비밀번호 · 인증 정보를", "보안 칩에 저장"]),
        ("영상 암호화 · UL", ["이미지 · 영상 종단 간 암호화", "UL IoT 보안 최고 등급(다이아몬드)"]),
    ], "#F4F2FF", (1200, 750), False),
    ("calf-foot-air-massager", 2, "고를 때 볼 4가지", "상세페이지에서 이 표기를 먼저 찾아보세요", [
        ("압력 · 자동 꺼짐", ["약한 단계부터 있는지", "15~20분 자동 종료가 있는지"]),
        ("감싸는 부위 · 사이즈", ["발만 / 종아리 / 허벅지까지", "종아리 둘레에 맞게 조절되는지"]),
        ("온열 기능", ["따뜻함 + 온도 조절", "저온 화상 주의 표시"]),
        ("의료기기 표시", ["허가 · 신고 번호와", "사용상 주의사항"]),
    ], "#FFF6EF", (1200, 800), True),
]

if __name__ == "__main__":
    for j in JOBS:
        print(draw(*j))
