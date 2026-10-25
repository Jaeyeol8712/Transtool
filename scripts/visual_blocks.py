# -*- coding: utf-8 -*-
"""
추천 모음 글에 쓰는 시각 블록(컬러 카드·체크리스트·비교·태그 등).

connect_posts.py 의 "body" 목록에 이 함수들이 돌려주는 HTML 을 그대로 넣으면 됩니다.
"{cta}" 문자열을 넣으면 그 자리에 빨강·검정 '제품 가격 알아보기' 버튼이 들어갑니다.
색상 이름: coral · amber · teal · blue · violet · pink
"""
from html import escape as _e

COLORS = ["coral", "amber", "teal", "blue", "violet", "pink"]


def hero(emoji, headline, sub, chips=()):
    """글 첫 화면: 큰 질문/한 줄 결론 + 요약 칩."""
    c = "".join(f'<span class="vx-chip vx-{COLORS[i % 6]}">{x}</span>' for i, x in enumerate(chips))
    return (f'<div class="vx-hero"><div class="vx-hero-emoji" aria-hidden="true">{emoji}</div>'
            f'<p class="vx-hero-h">{headline}</p><p class="vx-hero-s">{sub}</p>'
            f'{f"<div class=vx-chips>{c}</div>" if c else ""}</div>')


def cards(title, items):
    """색상 카드 묶음. items = [(이모지, 제목, 설명)]"""
    out = "".join(
        f'<div class="vx-card vx-{COLORS[i % 6]}"><span class="vx-card-n">{i + 1}</span>'
        f'<span class="vx-card-e" aria-hidden="true">{e}</span><p class="vx-card-t">{t}</p><p class="vx-card-d">{d}</p></div>'
        for i, (e, t, d) in enumerate(items))
    return f'<section class="vx-sec"><p class="vx-title">{title}</p><div class="vx-cards">{out}</div></section>'


def check(title, items, color="teal"):
    """체크리스트. items = [(굵은 말, 설명)]"""
    li = "".join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in items)
    return f'<section class="vx-sec vx-check vx-{color}"><p class="vx-title">{title}</p><ul>{li}</ul></section>'


def versus(title, left, right):
    """둘 비교. left/right = (이름, 색상, [특징...])"""
    def col(x):
        name, color, pts = x
        return f'<div class="vx-vs-col vx-{color}"><p class="vx-vs-name">{name}</p><ul>' + "".join(f"<li>{p}</li>" for p in pts) + "</ul></div>"
    return f'<section class="vx-sec"><p class="vx-title">{title}</p><div class="vx-vs">{col(left)}<span class="vx-vs-mid">VS</span>{col(right)}</div></section>'


def meter(title, rows):
    """중요도 막대. rows = [(항목, 1~5, 한 줄 설명)]"""
    r = "".join(
        f'<div class="vx-meter-row"><span class="vx-meter-k">{k}</span>'
        f'<span class="vx-meter-bar vx-{COLORS[i % 6]}"><i style="width:{v * 20}%"></i></span>'
        f'<span class="vx-meter-d">{d}</span></div>' for i, (k, v, d) in enumerate(rows))
    return f'<section class="vx-sec vx-meter"><p class="vx-title">{title}</p>{r}</section>'


def tags(title, yes, no):
    """이런 분께 추천 / 다시 생각해 볼 분."""
    y = "".join(f'<span class="vx-tag vx-yes">✔ {t}</span>' for t in yes)
    n = "".join(f'<span class="vx-tag vx-no">✕ {t}</span>' for t in no)
    return (f'<section class="vx-sec"><p class="vx-title">{title}</p>'
            f'<div class="vx-tags"><p class="vx-tags-h vx-yes-h">이런 분께 잘 맞아요</p>{y}</div>'
            f'<div class="vx-tags"><p class="vx-tags-h vx-no-h">이런 분은 한 번 더 생각해 보세요</p>{n}</div></section>')


def callout(emoji, text, color="amber"):
    """강조 박스 한 줄."""
    return f'<div class="vx-callout vx-{color}"><span aria-hidden="true">{emoji}</span><p>{text}</p></div>'


def hl(text):
    """문장 속 형광펜 강조."""
    return f'<mark class="vx-hl">{text}</mark>'
