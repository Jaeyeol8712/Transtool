import json, sys, os
root = sys.argv[1]; out = sys.argv[2]
src = lambda f: open(os.path.join(root, 'src', f), encoding='utf-8').read()
places = open(os.path.join(root, 'build', 'places.json'), encoding='utf-8').read()
geo = open(os.path.join(root, 'build', 'geo.json'), encoding='utf-8').read()
ovp = os.path.join(root, 'build', 'overseas.json')
ov = open(ovp, encoding='utf-8').read() if os.path.exists(ovp) else 'null'
ap = sys.argv[3] if len(sys.argv) > 3 else ''
around = open(ap, encoding='utf-8').read() if ap and os.path.exists(ap) else 'null'
js = ['icons.js', 'i18n.js', 'i18n_ov.js', 'core.js', 'planner.js', 'map2d.js', 'mapgl.js', 'world3d.js', 'ui_shell.js', 'ui_views.js', 'main.js']
import json as _j
_P = _j.loads(places); _R = {}
for _p in _P: _R.setdefault(_p['r'], []).append(_p['n']['ko'])
_ov = _j.loads(open(os.path.join(root, 'build', 'regions.json'), encoding='utf-8').read()) if os.path.exists(os.path.join(root, 'build', 'regions.json')) else []
_li = ''.join(f"<li><a href=\"#{r['id']}\">{r['name']}</a> — {' · '.join(_R.get(r['id'], [])[:6])}</li>" for r in _ov)
static = (f'<main id="seo"><h1>K링크 — 여행 일정 플래너</h1><p>지도에서 가고 싶은 관광지·맛집을 저장하면 거리와 운영 시간을 따져 날짜별 동선과 숙소 위치를 추천합니다. '
          f'국내 {sum(1 for r in _ov if not r.get("ov"))}곳은 3D 거리, 해외 {sum(1 for r in _ov if r.get("ov"))}개 도시는 지도로 고릅니다. 정보는 어라운드툴 여행 가이드·맛집 기록·명소 안내에서 옵니다.</p>'
          f'<h2>여행지</h2><ul>{_li}</ul><p><a href="/travel.html">어라운드툴 여행 가이드 전체</a></p></main>')
html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>K링크 — 여행 일정 플래너 (국내·해외 지도로 동선·숙소 추천) | 어라운드툴</title>
<meta name="description" content="K링크 — 국내·해외 지도에서 가고 싶은 곳을 저장하면 날짜별 동선과 숙소 위치를 추천하는 여행 일정 플래너. 어라운드툴의 여행 가이드·맛집 기록·계산기와 연결됩니다.">
<link rel="canonical" href="https://www.aroundtool.com/klink/">
<meta property="og:title" content="K링크 — 여행 일정 플래너 | 어라운드툴">
<meta property="og:description" content="가고 싶은 곳만 저장하면 날짜별 동선과 숙소 위치를 짜 드려요. 국내 7곳·해외 도시 지도.">
<meta property="og:url" content="https://www.aroundtool.com/klink/">
<meta property="og:image" content="https://www.aroundtool.com/assets/og/og-trip.png">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@500;600;700;800&family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{src('style.css')}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2LK65NYW74"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-2LK65NYW74');</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css">
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
</head>
<body>
{static}
<script>window.__PLACES__={places};window.__GEO__={geo};window.__OV__={ov};window.__AROUND__={around};</script>
''' + '\n'.join(f'<script>\n{src(f)}\n</script>' for f in js) + '\n</body>\n</html>\n'
open(out, 'w', encoding='utf-8').write(html)
print('bytes', len(html.encode('utf-8')))
