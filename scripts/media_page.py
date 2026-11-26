# -*- coding: utf-8 -*-
"""매체별 유입 페이지(2026-11-26 대표 지시). 사용: python3 scripts/media_page.py <kpi.json> <출력 html>
최신 날짜·최신 달이 맨 위. 결과 html을 아티팩트 '어라운드툴 매체별 유입'(slug 2a871c0a-c37a-4987-8f8b-c0f6b3ca185b)에 올린다."""
import json, sys
k = json.load(open(sys.argv[1], encoding="utf-8")); m = k["media"]
K = [("google", "구글"), ("naver", "네이버"), ("daum", "다음"), ("bing", "빙"), ("ai", "AI"), ("direct", "직접"), ("other", "기타")]
C = {"google": "#4285F4", "naver": "#03C75A", "daum": "#F5A623", "bing": "#00809D", "ai": "#8B5CF6", "direct": "#9CA3AF", "other": "#D1D5DB"}
def table(rows, lab, labf):
    rows = list(reversed(rows)); mx = max([r["total"] for r in rows] or [1]) or 1
    h = '<table><thead><tr><th>' + lab + '</th>' + ''.join(f'<th><i style="background:{C[x]}"></i>{n}</th>' for x, n in K) + '<th>합계</th></tr></thead><tbody>'
    for r in rows:
        bar = ''.join(f'<span style="width:{r[x]/mx*100:.2f}%;background:{C[x]}"></span>' for x, _ in K)
        h += f'<tr><td class="l">{labf(r)}<div class="bar">{bar}</div></td>' + ''.join(f'<td>{r[x] or "·"}</td>' for x, _ in K) + f'<td class="t">{r["total"]}</td></tr>'
    return h + '</tbody></table>'
d = table(m["daily"], "날짜", lambda r: r["date"][5:].replace("-", "."))
mo = table(m["monthly"], "월", lambda r: f'{r["month"][:4]}년 {int(r["month"][5:])}월' + (" (진행 중)" if r["month"] == m["daily"][-1]["date"][:7] else ""))
made = k["made"][:16].replace("T", " ")
html = f'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>어라운드툴 매체별 유입</title>
<style>:root{{color-scheme:light}}body{{font-family:-apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;margin:0;background:#fff;color:#111}}.w{{max-width:960px;margin:0 auto;padding:20px 16px 40px}}h1{{font-size:22px;margin:0 0 4px}}h2{{font-size:17px;margin:28px 0 8px}}p.s{{color:#666;font-size:13px;margin:0}}
table{{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}}th,td{{padding:8px 6px;border-bottom:1px solid #eee;text-align:right;white-space:nowrap}}th{{font-size:12px;color:#555;font-weight:600}}th i{{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:4px}}td.l,th:first-child{{text-align:left}}td.t{{font-weight:700}}
.bar{{display:flex;height:6px;margin-top:4px;border-radius:3px;overflow:hidden;background:#f3f4f6;width:160px}}.bar span{{display:block;height:100%}}.wrap{{overflow-x:auto}}.note{{font-size:12px;color:#777;margin-top:10px;line-height:1.6}}</style></head><body><div class="w">
<h1>매체별 유입</h1><p class="s">구글 애널리틱스 방문(세션) 기준 · 최신이 맨 위 · 갱신 {made} UTC</p>
<h2>최근 7일 (일별)</h2><div class="wrap">{d}</div>
<h2>월별</h2><div class="wrap">{mo}</div>
<p class="note">구글·네이버·다음·빙 = 각 검색엔진에서 검색해 들어온 방문 · AI = ChatGPT·Perplexity 등 AI 답변에서 들어온 방문 · 직접 = 주소 입력·즐겨찾기 · 기타 = SNS·다른 사이트·광고.<br>어제 숫자는 구글 애널리틱스 집계가 끝나지 않아 다음 날 조금 늘 수 있습니다.</p></div></body></html>'''
open(sys.argv[2], "w", encoding="utf-8").write(html); print("ok")
