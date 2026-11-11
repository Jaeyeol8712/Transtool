import json, sys, os
root = sys.argv[1]; out = sys.argv[2]
src = lambda f: open(os.path.join(root, 'src', f), encoding='utf-8').read()
places = open(os.path.join(root, 'build', 'places.json'), encoding='utf-8').read()
geo = open(os.path.join(root, 'build', 'geo.json'), encoding='utf-8').read()
ap = sys.argv[3] if len(sys.argv) > 3 else ''
around = open(ap, encoding='utf-8').read() if ap and os.path.exists(ap) else 'null'
js = ['icons.js', 'i18n.js', 'core.js', 'planner.js', 'map2d.js', 'world3d.js', 'ui_shell.js', 'ui_views.js', 'main.js']
html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>K링크 K-Link</title>
<meta name="robots" content="noindex, follow">
<meta name="description" content="K링크 — 지도와 3D 거리에서 가고 싶은 곳을 저장하면 날짜별 동선과 숙소를 추천하는 한국 여행 플래너 (시연 버전)">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@500;600;700;800&family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{src('style.css')}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
</head>
<body>
<script>window.__PLACES__={places};window.__GEO__={geo};window.__AROUND__={around};</script>
''' + '\n'.join(f'<script>\n{src(f)}\n</script>' for f in js) + '\n</body>\n</html>\n'
open(out, 'w', encoding='utf-8').write(html)
print('bytes', len(html.encode('utf-8')))
