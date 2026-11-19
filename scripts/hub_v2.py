"""카테고리 첫 화면(허브) 새 틀 — 2026-11-19 대표 확정.

build.py가 travel/food/tools/connect/etc.html을 만든 뒤 실행해 본문을 바꾼다.
원칙: 설명 없이 제목 → 검색 → 많이 찾는 것 → 분류 탭 → 이름 목록(12개 + 더 보기).
사이드바는 추천 모음 새 글만, 배경 흰색, 푸터 링크 묶음 제거.
'많이 찾는 것'은 scripts/hub_popular.json(서치 콘솔 페이지별 노출)로 고른다.
"""
import html as H
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = '<!-- hub-v2 -->'

CSS = """<style id="hub2-css">
body.hub2,body.hub2 main,body.hub2 .at-page{background:#fff!important}
body.hub2 .at-content>.head,body.hub2 a.at-klink,body.hub2 .at-related,body.hub2 .at-footer-brand,body.hub2 .at-footer-cols{display:none!important}
body.hub2 .at-side>*:not(.is-shop){display:none!important}
.hub{padding:8px 0 30px;color:#111}.hub h1{font-size:28px;font-weight:800;margin:6px 0 14px;color:#111}
.hub h2{font-size:18px;font-weight:800;margin:24px 0 10px;color:#111}
.hub-q{width:100%;box-sizing:border-box;border:1px solid #e5e7eb;border-radius:12px;padding:12px 14px;font:inherit;font-size:15px;background:#fff}
.hub-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.hub-cards a{text-decoration:none;color:#111}.hub-cards .ph{display:block;aspect-ratio:3/2;border-radius:12px;background:#f2f4f7 center/cover}
.hub-cards b{display:block;font-size:15px;margin-top:6px}
.hub-tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.hub-tiles a{border:1px solid #e5e7eb;border-radius:12px;padding:14px;text-decoration:none;color:#111;font-weight:700;font-size:15px;line-height:1.4}
.hub-tiles a small{display:block;font-weight:500;color:#9ca3af;font-size:13px;margin-top:4px}
.hub-tabs{display:flex;flex-wrap:wrap;column-gap:18px;border-bottom:1px solid #e5e7eb;margin:28px 0 4px}
.hub-tabs button{font:inherit;font-size:16px;font-weight:700;color:#9ca3af;background:none;border:0;padding:10px 0;border-bottom:2px solid transparent;cursor:pointer}
.hub-tabs button.on{color:#111;border-color:#111}
.hub-list{display:grid;grid-template-columns:repeat(3,1fr);column-gap:20px}
.hub-list a{display:block;padding:12px 0;border-bottom:1px solid #eef0f3;text-decoration:none;color:#111;font-size:15px;font-weight:600}
.hub-g[hidden]{display:none!important}.hub-g.all a.nm,.hub-g a.nm{display:none!important}.hub-g .x{display:none!important}.hub-g.all .x{display:block!important}
.hub-tiles.hub-g{margin-top:12px}.hub-tiles.hub-g.all .x{display:block!important}
.hub-shop{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:14px}
.hub-shop a{text-decoration:none;color:#111}.hub-shop .ph{display:block;aspect-ratio:4/3;border-radius:12px;background:#f2f4f7 center/cover}
.hub-shop b{display:block;font-size:15px;margin:8px 0}.hub-shop .bt{display:inline-block;background:#e11d48;color:#fff;font-weight:800;font-size:14px;padding:8px 14px;border-radius:10px}
.hub-more{display:block;margin:16px auto 0;font:inherit;font-size:14px;font-weight:700;border:1px solid #e5e7eb;background:#fff;color:#111;border-radius:20px;padding:8px 20px;cursor:pointer}
@media(max-width:700px){.hub-cards{grid-template-columns:repeat(2,1fr)}.hub-tiles{grid-template-columns:repeat(2,1fr)}.hub-list{grid-template-columns:1fr}.hub-shop{grid-template-columns:1fr}}
</style>"""

JS = """<script id="hub2-js">(function(){var tb=document.querySelectorAll('.hub-tabs button'),gs=document.querySelectorAll('.hub-g'),mb=document.querySelector('.hub-more');
function more(){var g=document.querySelector('.hub-g:not([hidden])');if(mb)mb.style.display=g&&g.querySelector('.x')&&!g.classList.contains('all')?'':'none';}
tb.forEach(function(b){b.addEventListener('click',function(){tb.forEach(function(x){x.classList.toggle('on',x===b)});gs.forEach(function(g){g.hidden=g.getAttribute('data-k')!==b.getAttribute('data-t')});more();});});
if(mb)mb.addEventListener('click',function(){var g=document.querySelector('.hub-g:not([hidden])');if(g)g.classList.add('all');more();});
var q=document.querySelector('.hub-q');if(q)q.addEventListener('input',function(){var v=q.value.trim();gs.forEach(function(g){g.hidden=false;g.classList.toggle('all',!!v);g.querySelectorAll('a').forEach(function(a){a.classList.toggle('nm',!!v&&a.textContent.indexOf(v)<0)})});if(!v){tb.forEach(function(x,i){x.classList.toggle('on',i===0)});gs.forEach(function(g,i){g.hidden=i>0;g.classList.remove('all')});}if(mb)mb.style.display=v?'none':'';if(!v)more();});
var hh=location.hash.slice(1);if(hh){tb.forEach(function(b){if(b.getAttribute('data-h')===hh)b.click()})}more();})();</script>"""

POP = {}


def imp(url):
    k = re.sub(r'^https?://[^/]+', '', url).strip('/').replace('.html', '') or 'index'
    return POP.get(k, 0)


def e(s):
    return H.escape(s, quote=True)


def a_list(items, key, hidden, cls='hub-list'):
    """items: [(이름, url, 보조)]"""
    out = []
    for i, (n, u, sub) in enumerate(items):
        out.append(f'<a href="{e(u)}" class="{"x" if i >= 12 else ""}">{e(n)}' + (f'<small>{e(sub)}</small>' if sub else '') + '</a>')
    return f'<div class="{cls} hub-g" data-k="{key}"' + (' hidden' if hidden else '') + '>' + ''.join(out) + '</div>'


def tabs(groups, cls='hub-list'):
    t = '<div class="hub-tabs" role="tablist">' + ''.join(
        f'<button type="button" class="{"on" if i == 0 else ""}" data-t="g{i}">{e(g)} {len(v)}</button>' for i, (g, v) in enumerate(groups)) + '</div>'
    return t + ''.join(a_list(v, f'g{i}', i > 0, cls) for i, (g, v) in enumerate(groups)) + '<button type="button" class="hub-more">더 보기</button>'


def tiles(title, items):
    return f'<h2>{e(title)}</h2><div class="hub-tiles">' + ''.join(
        f'<a href="{e(u)}">{e(n)}' + (f'<small>{e(s)}</small>' if s else '') + '</a>' for n, u, s in items) + '</div>'


def main_of(h):
    m = re.search(r'<main.*?</main>', h, re.S)
    return m.group(0) if m else ''


def put(path, h, title, ph, body):
    main = f'<main>{MARK}<article><div class="hub"><h1>{e(title)}</h1><input class="hub-q" type="search" placeholder="{e(ph)}" aria-label="{e(ph)}">{body}</div></article></main>'
    h = re.sub(r'<main.*?</main>', lambda m: main, h, count=1, flags=re.S)
    # 화면에서 뺀 자주 묻는 질문의 구조화 데이터도 함께 뺀다(보이지 않는 FAQ 금지)
    h = re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*"FAQPage"(?:(?!</script>).)*</script>\s*', '', h, flags=re.S)
    h = re.sub(r'<style id="hub2-css">.*?</style>\s*', '', h, flags=re.S)
    h = re.sub(r'<script id="hub2-js">.*?</script>\s*', '', h, flags=re.S)
    h = re.sub(r'<body([^>]*)class="([^"]*)"', lambda m: f'<body{m.group(1)}class="{m.group(2)} hub2"' if 'hub2' not in m.group(2) else m.group(0), h, count=1)
    if 'hub2' not in h.split('<body', 1)[1][:300]:
        h = h.replace('<body', '<body class="hub2"', 1)
    h = h.replace('</head>', CSS + '\n</head>', 1).replace('</body>', JS + '\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(h)


def photo_for(url, pm):
    f = url.strip('/').split('/')[-1]
    f = f if f.endswith('.html') else f + '.html'
    slug = f[:-5].replace('travel-', '')
    for n in pm.get(f) or []:
        for ext in ('jpg', 'png'):
            if os.path.exists(os.path.join(ROOT, 'assets/photos', f'{n}.{ext}')):
                return f'/assets/photos/{n}.{ext}'
    for p in ('d', 't', 'k'):
        if os.path.exists(os.path.join(ROOT, 'assets/photos', f'{p}-{slug}.jpg')):
            return f'/assets/photos/{p}-{slug}.jpg'
    return None


DATA = {}


def travel(h):
    if DATA.get('trips'):
        groups = [(k, [(n, u, None) for n, u, kd in DATA['trips'] if kd == k]) for k in ('국내', '해외')]
        groups = [g for g in groups if g[1]]
        return travel_body(groups)
    m = main_of(h)
    parts = re.split(r'<h2 class="sec">', m)
    groups = []
    for p in parts[1:]:
        name = re.sub(r'<[^>]+>', ' ', p.split('</h2>')[0]).split()[0]
        if name not in ('국내', '해외'):
            continue
        items, seen = [], set()
        for u, t in re.findall(r'<a[^>]*href="(/?travel-[^"#]+)"[^>]*>(.*?)</a>', p, re.S):
            u = '/' + u.lstrip('/')
            if u in seen:
                continue
            seen.add(u)
            parts_t = [x.strip() for x in re.sub(r'<[^>]+>', '|', t).split('|') if x.strip()]
            items.append((H.unescape(parts_t[0]), u, None))
        groups.append((name, items))
    return travel_body(groups)


def travel_body(groups):
    pm = json.load(open(os.path.join(ROOT, 'scripts/photo_map.json'), encoding='utf-8'))
    pool = [x for _, v in groups for x in v if photo_for(x[1], pm)]
    top = sorted(pool, key=lambda x: -imp(x[1]))[:6]
    cards = '<h2>많이 찾는 여행</h2><div class="hub-cards">' + ''.join(
        f'<a href="{e(u)}"><span class="ph" style="background-image:url({e(photo_for(u, pm))})" role="img" aria-label="{e(n)}"></span><b>{e(n)}</b></a>' for n, u, _ in top) + '</div>'
    return cards + tabs(groups)


def food(h):
    m = main_of(h)
    short = {'인천광역시': '인천', '서울특별시': '서울', '부산광역시': '부산', '강원특별자치도': '강원', '대전광역시': '대전', '광주광역시': '광주',
             '제주특별자치도': '제주', '전라남도': '전남', '경상북도': '경북', '대구광역시': '대구', '울산광역시': '울산', '경기도': '경기'}
    groups, cur = [], None
    for attr, r in re.findall(r'<tr([^>]*)>(.*?)</tr>', m, re.S):
        if 'at-gr' in attr:
            nm = re.sub(r'<[^>]+>', '', r.split('<span')[0]).strip()
            hid = re.search(r'id="([^"]+)"', attr)
            cur = [short.get(nm, nm), [], hid.group(1) if hid else '']
            groups.append(cur)
            continue
        c = re.search(r'class="c">(\d+)', r)
        if cur is None or '전체 보기' not in r or not c:
            continue
        gu = re.search(r'class="tag[^"]*">([^<]+)', r).group(1)
        if '메뉴' in gu:
            continue
        cur[1].append((gu, re.search(r'href="([^"]+)"', r).group(1), f'{c.group(1)}곳'))
    groups = [g for g in groups if g[1]]
    allg = [(g[0], x) for g in groups for x in g[1]]
    top = sorted(allg, key=lambda t: -imp(t[1][1]))[:8]
    body = tiles('많이 찾는 맛집', [(f'{a} {x[0]}', x[1], x[2]) for a, x in top])
    body += '<div class="hub-tabs" role="tablist">' + ''.join(
        f'<button type="button" class="{"on" if i == 0 else ""}" data-t="g{i}" data-h="{e(g[2])}">{e(g[0])} {sum(int(x[2][:-1]) for x in g[1])}</button>' for i, g in enumerate(groups)) + '</div>'
    body += ''.join(f'<div class="hub-tiles hub-g" data-k="g{i}"' + (' hidden' if i else '') + '>' + ''.join(
        f'<a href="{e(u)}">{e(n)}<small>{e(s)}</small></a>' for n, u, s in g[1]) + '</div>' for i, g in enumerate(groups))
    return body


def tools(h):
    m = main_of(h)
    groups, cur = [], None
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', m, re.S):
        if 'colspan' in r:
            cur = [re.sub(r'<[^>]+>', '', r.split('<span')[0]).strip(), []]
            groups.append(cur)
            continue
        a = re.search(r'<a href="([^"]+)">([^<]+)</a>', r)
        if a and cur is not None:
            cur[1].append((H.unescape(a.group(2)), a.group(1), None))
    groups = [g for g in groups if g[1]]
    top = sorted([x for _, v in groups for x in v], key=lambda x: -imp(x[1]))[:8]
    return tiles('많이 쓰는 계산기', top) + tabs(groups)


TRAVEL_GUIDE = re.compile(r'passport|-eta|esta|visa|tdac|mdac|etravel|arrival|duty-free|liquids|tax-free|travel|immigration|roaming|esim|airport|baggage')


def guide(h):
    bucket = {'여행·입국': []}
    if DATA.get('guides'):
        for t, u, name in DATA['guides']:
            k = '여행·입국' if TRAVEL_GUIDE.search(u) else name.replace('생활·건강·여행', '생활·건강')
            bucket.setdefault(k, []).append((t, u, None))
        pass  # 텍스트 도구는 계산기 첫 화면에 있음
    m = '' if DATA.get('guides') else main_of(h)
    for gm in re.finditer(r'<h2>([^<]+)<span class="c">\d+</span></h2><ul>(.*?)</ul>', m, re.S):
        name = gm.group(1).strip()
        if '사이트' in name:
            continue
        for u, t in re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', gm.group(2)):
            if '텍스트' in name:
                k = '텍스트 도구'
            elif TRAVEL_GUIDE.search(u):
                k = '여행·입국'
            else:
                k = name.replace('생활·건강·여행', '생활·건강')
            bucket.setdefault(k, []).append((H.unescape(t), u, None))
    groups = [(k, v) for k, v in bucket.items() if v]
    first = [g for g in groups if g[0] == '여행·입국']
    rest = sorted([g for g in groups if g[0] not in ('여행·입국', '텍스트 도구')], key=lambda g: -len(g[1]))
    last = [g for g in groups if g[0] == '텍스트 도구']
    groups = first + rest + last
    top = sorted([x for k, v in groups if k != '텍스트 도구' for x in v], key=lambda x: -imp(x[1]))[:8]
    return tiles('많이 찾는 가이드', top) + tabs(groups)


def shop():
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    import connect_posts as cp
    live = [p for p in cp.POSTS if os.path.exists(os.path.join(ROOT, f"shop-{p['slug']}.html"))]

    def card(p, i):
        s = p['slug']
        ph = next((f'/assets/shop/{s}/{f}' for f in ('thumb.jpg', 'product.jpg', 'og.jpg') if os.path.exists(os.path.join(ROOT, f'assets/shop/{s}/{f}'))), None)
        bt = '여행 비용 알아보기 >>' if p.get('kind') == 'travel' else '제품 가격 알아보기 >>'
        st = f' style="background-image:url({e(ph)})"' if ph else ''
        return f'<a href="/shop-{e(s)}.html" class="{"x" if i >= 6 else ""}"><span class="ph"{st} role="img" aria-label="{e(p.get("product") or p["title"])}"></span><b>{e(p["title"])}</b><span class="bt">{bt}</span></a>'
    prod = [p for p in live if p.get('kind', 'product') != 'travel']
    trv = [p for p in live if p.get('kind') == 'travel']
    body = '<div class="hub-tabs" role="tablist">' + f'<button type="button" class="on" data-t="g0">제품 추천 {len(prod)}</button><button type="button" data-t="g1">여행 추천 {len(trv)}</button></div>'
    body += '<div class="hub-shop hub-g" data-k="g0">' + ''.join(card(p, i) for i, p in enumerate(prod)) + '</div>'
    body += '<div class="hub-shop hub-g" data-k="g1" hidden>' + ''.join(card(p, i) for i, p in enumerate(trv)) + '</div><button type="button" class="hub-more">더 보기</button>'
    return body


PAGES = [('travel.html', '여행', '도시·지역 이름으로 찾기', travel), ('food.html', '맛집', '지역이나 음식으로 찾기', food),
         ('tools.html', '계산기', '계산기 이름으로 찾기', tools), ('etc.html', '가이드', '궁금한 것 찾기', guide),
         ('connect.html', '추천', '제품·여행 이름으로 찾기', None)]


def run(root=None, data=None):
    global ROOT, POP, DATA
    if root:
        ROOT = root
    DATA = data or {}
    pp = os.path.join(ROOT, 'scripts/hub_popular.json')
    POP = json.load(open(pp, encoding='utf-8'))['impressions'] if os.path.exists(pp) else {}
    done = []
    for f, title, ph, fn in PAGES:
        path = os.path.join(ROOT, f)
        if not os.path.exists(path):
            continue
        h = open(path, encoding='utf-8').read()
        if MARK in h and not (f in ('travel.html', 'etc.html') and DATA):
            continue
        body = shop() if fn is None else fn(h)
        put(path, h, title, ph, body)
        done.append(f)
    # 기존 글 새 구성 보강(2026-11-19): '먼저 알아둘 것'이 없으면 설명문으로 넣고, 자주 묻는 질문은 5개까지
    import glob
    n_fix = 0
    SKIP = {'index.html', '404.html', 'search.html', 'sitemap.html', 'about.html', 'privacy.html', 'terms.html', 'editorial.html', 'contact.html',
            'connect.html', 'food.html', 'tools.html', 'travel.html', 'etc.html', 'season.html', 'guide_2026_tax.html', 'guide_2026_wage.html'}
    for path in glob.glob(os.path.join(ROOT, '*.html')):
        bn = os.path.basename(path)
        if bn in SKIP or bn.startswith('shop-'):
            continue
        h = open(path, encoding='utf-8').read(); o = h
        m = re.search(r'<main.*?</main>', h, re.S)
        if not m:
            continue
        main = m.group(0)
        if 'at-answer' not in main and '먼저 알아둘 것' not in main and 'vx-hero' not in main:
            d = re.search(r'<meta name="description" content="([^"]+)"', h)
            if d:
                box = f'<div class="at-answer b-sum"><p>{d.group(1)}</p></div>'
                k = min([x for x in (main.find('<section class="b-card"'), main.find('<section class="compare b-card"'), main.find('<section class="'), ) if x > 0] or [-1])
                if k > 0:
                    main = main[:k] + box + main[k:]
        # 본문 카드 정리: '함께 보기'류 목록 카드는 빼고, 핵심 카드가 5개를 넘으면 6번째부터 접기
        secs = list(re.finditer(r'<section class="[^"]*b-card[^"]*"[^>]*>.*?</section>', main, re.S))
        core = []
        for x in secs:
            hm = re.search(r'<h2[^>]*>(.*?)</h2>', x.group(0), re.S)
            t = re.sub(r'<[^>]+>', '', hm.group(1)) if hm else ''
            if re.search(r'관련 가이드|함께 보면 좋은|함께 보기|다른 계산기', t):
                main = main.replace(x.group(0), '', 1); continue
            if hm and not re.search(r'자주 묻는|근거|출처|이 글의 기준|블로그|홈페이지에 넣기', t):
                core.append((x.group(0), re.sub(r'^\d+', '', t).strip()))
        for sec, t in core[5:]:
            if 'b-more' in sec:
                continue
            main = main.replace(sec, f'<details class="b-more"><summary>{t}</summary>{sec}</details>', 1)
        fq = re.search(r'(<div class="(?:at-faq|faq)[^"]*">)(.*?)(</div>\s*</section>|</div>\s*</div>)', main, re.S)
        if fq:
            dets = list(re.finditer(r'<details[^>]*>.*?</details>', fq.group(2), re.S))
            if len(dets) > 5:
                inner = fq.group(2)[:dets[5].start()]
                main = main[:fq.start(2)] + inner + main[fq.end(2):]
        h = h[:m.start()] + main + h[m.end():]
        def trim_ld(mm):
            try:
                j = json.loads(mm.group(1))
            except Exception:
                return mm.group(0)
            if isinstance(j, dict) and j.get('@type') == 'FAQPage' and len(j.get('mainEntity', [])) > 5:
                j['mainEntity'] = j['mainEntity'][:5]
                return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + '</script>'
            return mm.group(0)
        h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', trim_ld, h, flags=re.S)
        if h != o:
            open(path, 'w', encoding='utf-8').write(h); n_fix += 1
    if n_fix:
        done.append(f'글 {n_fix}개 구성 보강')
    # 메인 페이지: 푸터의 브랜드 소개·링크 묶음 제거(2026-11-19 대표). 법적 링크 줄은 유지.
    ip = os.path.join(ROOT, 'index.html')
    if os.path.exists(ip):
        h = open(ip, encoding='utf-8').read()
        h2 = re.sub(r'\s*<div class="at-footer-brand">.*?</p></div>', '', h, count=1, flags=re.S)
        h2 = re.sub(r'\s*<div class="at-footer-cols">(?:\s*<div><p>[^<]*</p><ul>.*?</ul></div>)+\s*</div>', '', h2, count=1, flags=re.S)
        if h2 != h:
            open(ip, 'w', encoding='utf-8').write(h2)
            done.append('index.html(푸터)')
    print('hub_v2:', ', '.join(done) or '변경 없음')


if __name__ == '__main__':
    run()
