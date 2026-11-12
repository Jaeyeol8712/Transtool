# -*- coding: utf-8 -*-
"""K링크 해외 도시 데이터 빌드.

  python3 scripts/klink/tools/build_overseas.py [<earth-lands-250m map.geo.json>] [--keep-world]

- overseas_data.py 를 읽어 build/places.json(해외 장소 추가), build/overseas.json(지역·공항·숙소 권역),
  build/regions.json(사이트 빌드가 읽는 지역 목록)을 만든다.
- 땅 경계 파일(npm @geo-maps/earth-lands-250m 의 map.geo.json, 출처 OpenStreetMap · ODbL)을 주면 build/geo.json 에 해외 지도 경계와
  구역(zone)을 다시 만든다. 주지 않으면 geo.json 은 건드리지 않는다(장소만 바꿨을 때).
- 좌표 검사: 도시 중심에서 너무 멀거나 바다 위에 찍힌 장소를 알려 준다.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import overseas_data as OD  # noqa: E402

B = lambda f: os.path.join(ROOT, 'build', f)
KR = ['seoul', 'busan', 'jeju', 'gyeongju', 'gangneung', 'jeonju', 'yeosu']
KR_NAME = {'seoul': '서울', 'busan': '부산', 'jeju': '제주', 'gyeongju': '경주', 'gangneung': '강릉', 'jeonju': '전주', 'yeosu': '여수'}
CATS = {'palace', 'food', 'skin', 'shop', 'cafe', 'kpop', 'night', 'nature', 'fun'}
HOURS = {'A': [0, 24], 'D': [9, 17], 'S': [10, 21], 'N': [17, 23.5], 'M': [6, 14], 'F': [11, 21], 'T': [9, 19]}
CAT_O = {'palace': 'D', 'nature': 'A', 'food': 'F', 'cafe': 'S', 'shop': 'S', 'night': 'A', 'fun': 'T'}
FAR_KM = 25


def hav(a, b):
    R = 6371; t = math.pi / 180
    dla = (b[0] - a[0]) * t; dlo = (b[1] - a[1]) * t
    x = math.sin(dla / 2) ** 2 + math.cos(a[0] * t) * math.cos(b[0] * t) * math.sin(dlo / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def names4(s):
    """ko|zh|en|ja — zh 비면 ja→en, ja 비면 en."""
    a = [x.strip() for x in s.split('|')]
    a += [''] * (4 - len(a))
    ko, zh, en, ja = a[:4]
    en = en or ko
    return [ko, zh or ja or en, en, ja or en]


def two4(ko, en):
    return [ko.strip(), en.strip(), en.strip(), en.strip()]


def parse():
    cities, cur, zone = [], None, None
    for raw in OD.DATA.strip().splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        head, *rest = [x.strip() for x in line.split(' | ')]
        tok = head.split()
        k = tok[0]
        if k == 'C':
            cur = dict(id=tok[1], cc=tok[2], lat=float(tok[3]), lng=float(tok[4]), sub=tok[5] == '1', fly=int(tok[6]),
                       t=names4(rest[0]), tag=two4(rest[1], rest[2]), airports=[], stays=[], zones=[])
            cities.append(cur); zone = None
        elif k == 'A':
            cur['airports'].append(dict(code=tok[1], lat=float(tok[2]), lng=float(tok[3]), min=int(tok[4]), t=names4(rest[0])))
        elif k == 'S':
            cur['stays'].append(dict(id=tok[1], lat=float(tok[2]), lng=float(tok[3]), t=names4(rest[0]), st=two4(rest[1], rest[2])))
        elif k == 'Z':
            zone = dict(id=tok[1], n=two4(rest[0], rest[1]), places=[])
            cur['zones'].append(zone)
        elif k == 'P':
            pid, cat, lat, lng, h = tok[1], tok[2], float(tok[3]), float(tok[4]), float(tok[5])
            assert cat in CATS, (pid, cat)
            p = dict(id=pid, c=cat, r=cur['id'], cost=None, rsv=False, closed=[], prem=False, st='', est=1,
                     lat=lat, lng=lng, h=h, best='any', meal=None)
            okey = CAT_O[cat]
            for o in tok[6:]:
                if o in ('am', 'eve', 'night'): p['best'] = o
                elif o in ('lunch', 'dinner'): p['meal'] = o
                elif o.startswith('o='): okey = o[2:]
                elif o.startswith('x='): p['closed'] = [int(x) for x in o[2:].split(',')]
                else: raise SystemExit(f'unknown option {o} in {pid}')
            p['o'] = HOURS[okey]
            n = names4(rest[0]); p['n'] = dict(zip(['ko', 'zh', 'en', 'ja'], n))
            p['d'] = {'ko': rest[1], 'en': rest[2]}
            d = hav((cur['lat'], cur['lng']), (lat, lng))
            if d > FAR_KM: p['far'] = 1
            p['_km'] = d
            zone['places'].append(p)
        else:
            raise SystemExit('bad line: ' + line)
    return cities


def main():
    cities = parse()
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    land_path = args[0] if args else None
    ov_ids = [c['id'] for c in cities]
    # ---------- places ----------
    old = json.load(open(B('places.json'), encoding='utf-8'))
    dom = [p for p in old if p['r'] in KR]
    seen = {p['id'] for p in dom}
    new = []
    for c in cities:
        assert c['cc'] in OD.COUNTRIES, c['id']
        assert c['airports'] and c['stays'] and c['zones'], c['id']
        for z in c['zones']:
            for p in z['places']:
                assert p['id'] not in seen, 'duplicate id ' + p['id']
                seen.add(p['id'])
                if p['_km'] > 260: print('  ! far from centre', p['id'], round(p['_km']))
                q = {k: v for k, v in p.items() if not k.startswith('_')}
                new.append(q)
    json.dump(dom + new, open(B('places.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    # ---------- regions / airports / stays ----------
    regions, airports, stays = {}, {}, []
    for c in cities:
        a0 = c['airports'][0]
        regions[c['id']] = dict(lat=c['lat'], lng=c['lng'], sub=c['sub'], cc=c['cc'], air=a0['code'], fly=c['fly'], t=c['t'], tag=c['tag'])
        for a in c['airports']:
            ap = airports.setdefault(a['code'], dict(lat=a['lat'], lng=a['lng'], r=c['id'], cc=c['cc'], t=a['t'], to={}))
            ap['to'][c['id']] = a['min']
        for s in c['stays']:
            stays.append([s['id'], c['id'], s['lat'], s['lng'], s['t'], s['st']])
    ov = dict(countries=OD.COUNTRIES, order=OD.COUNTRY_ORDER, regions=regions, airports=airports, stays=stays)
    json.dump(ov, open(B('overseas.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    idx = [dict(id=r, name=KR_NAME[r], cc='kr', country='대한민국', ov=False) for r in KR]
    for cc in OD.COUNTRY_ORDER:
        idx += [dict(id=c['id'], name=c['t'][0], cc=cc, country=OD.COUNTRIES[cc][0], ov=True) for c in cities if c['cc'] == cc]
    json.dump(idx, open(B('regions.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('places', len(dom), '+', len(new), '| regions', len(cities), '| airports', len(airports), '| stays', len(stays))
    if not land_path:
        geo = json.load(open(B('geo.json'), encoding='utf-8'))
        miss = [p['id'] for p in new if p['id'] not in geo['pd']]
        if miss: print('  ! geo.json 에 구역이 없는 장소(땅 경계 파일을 주고 다시 돌리세요):', miss)
        return
    build_geo(cities, land_path)


def build_geo(cities, land_path):
    """해외 도시 지도 경계와 구역, 해외 전체 지도. land_path: @geo-maps/earth-lands-250m(권장) 또는 -1km 의 map.geo.json"""
    import pickle, time
    import numpy as np
    import shapely
    from shapely.geometry import Point, box, Polygon
    from shapely.ops import unary_union, transform
    import warnings; warnings.filterwarnings('ignore')
    t0 = time.time()
    WORLD = (70, -11, 165, 58)
    cache = land_path + '.asia2.pkl'   # 동아시아 부분만 잘라 둔 캐시 (다시 돌릴 때 빠르게)
    if os.path.exists(cache):
        raw = pickle.load(open(cache, 'rb'))
    else:
        g = json.load(open(land_path, encoding='utf-8'))
        geoms = g['geometries'] if g.get('type') == 'GeometryCollection' else [f['geometry'] for f in g['features']]
        raw = []
        for gm in geoms:
            for poly in (gm['coordinates'] if gm['type'] == 'MultiPolygon' else [gm['coordinates']]):
                ext = np.asarray(poly[0], dtype='f8')
                x0, y0 = ext.min(axis=0); x1, y1 = ext.max(axis=0)
                if x1 < WORLD[0] or x0 > WORLD[2] or y1 < WORLD[1] or y0 > WORLD[3]: continue
                raw.append(((x0, y0, x1, y1), ext, [np.asarray(h, dtype='f8') for h in poly[1:]]))
        del g, geoms
        pickle.dump(raw, open(cache, 'wb'), protocol=4)
    polys = [(bb, Polygon(ext, holes)) for bb, ext, holes in raw]
    del raw
    print('  land polygons', len(polys), 'loaded in', round(time.time() - t0), 's')

    def land_in(b, skip=None):   # b = (x0, y0, x1, y1). 사각형으로 빠르게 잘라 낸 땅
        parts = []
        for (x0, y0, x1, y1), poly in polys:
            if x1 < b[0] or x0 > b[2] or y1 < b[1] or y0 > b[3]: continue
            if skip and skip((x0, y0, x1, y1)): continue
            c = shapely.clip_by_rect(poly, *b)
            if c is not None and not c.is_empty: parts.append(c.buffer(0))
        return unary_union(parts) if parts else None
    def rings_of(geom, nd):
        out = []
        for p in ([geom] if geom.geom_type == 'Polygon' else list(getattr(geom, 'geoms', []))):
            if p.is_empty or p.geom_type != 'Polygon': continue
            out.append([[[round(x, nd), round(y, nd)] for x, y in r.coords] for r in [p.exterior] + list(p.interiors)])
        return out
    def tidy(geom, tol, keep_pts):
        """단순화 + 아주 작은 섬·호수 구멍 정리 (장소가 있는 작은 섬은 남긴다)."""
        out = []
        for p in ([geom] if geom.geom_type == 'Polygon' else list(getattr(geom, 'geoms', []))):
            if p.is_empty or p.geom_type != 'Polygon': continue
            if p.area < (tol * 5) ** 2 and not any(p.distance(k) < 0.012 for k in keep_pts): continue
            q = Polygon(p.exterior, [h for h in p.interiors if Polygon(h).area > 0.004]).simplify(tol, preserve_topology=True)   # 강·작은 호수 구멍은 지운다 (단순화하면 세모 조각으로 보임)
            if not q.is_empty: out.append(q)
        return unary_union(out) if out else None
    def proj_fn(lat0, lng0):
        kx = math.cos(math.radians(lat0)) * 111320.0; ky = 110574.0
        return (lambda x, y, z=None: ((x - lng0) * kx, (y - lat0) * ky)), (lambda x, y, z=None: (x / kx + lng0, y / ky + lat0))

    geo = json.load(open(B('geo.json'), encoding='utf-8'))
    for r in list(geo['regions']):
        if r not in KR: del geo['regions'][r]
    dom_ids = {i for r in KR for d in geo['regions'][r]['districts'] for i in d['ids']}
    geo['pd'] = {k: v for k, v in geo['pd'].items() if k in dom_ids}
    off = []
    for c in cities:
        pts = [p for z in c['zones'] for p in z['places']]
        la = [p['lat'] for p in pts] + [c['lat']]; lo = [p['lng'] for p in pts] + [c['lng']]
        a0, a1, o0, o1 = min(la), max(la), min(lo), max(lo)
        ma = max(0.07, (a1 - a0) * 0.4); mo = max(0.09, (o1 - o0) * 0.4)
        b = (o0 - mo, a0 - ma, o1 + mo, a1 + ma)
        land = land_in(b)
        span = max(b[2] - b[0], b[3] - b[1])
        reg = {'munis': [], 'neigh': [], 'districts': [], 'water': []}
        P = [Point(p['lng'], p['lat']) for p in pts]
        if land is not None:
            # 도심(근교 제외)은 촘촘하게, 근교까지 넓힌 바깥은 성기게 그린다
            core = [p for p in pts if not p.get('far')] or pts
            cb = box(min(p['lng'] for p in core) - 0.09, min(p['lat'] for p in core) - 0.07, max(p['lng'] for p in core) + 0.09, max(p['lat'] for p in core) + 0.07)
            cspan = max(cb.bounds[2] - cb.bounds[0], cb.bounds[3] - cb.bounds[1])
            fine = tidy(land.intersection(cb), max(0.0005, cspan / 500), P)
            shown = fine
            if span > cspan * 1.5:
                outer = tidy(land.difference(cb), max(0.0025, span / 260), P)
                shown = unary_union([g_ for g_ in (fine, outer) if g_ is not None]) if (fine is not None or outer is not None) else None
            if shown is not None: reg['munis'].append({'code': 'land', 'n': ['', '', '', ''], 'g': rings_of(shown, 4)})
            for p, pt in zip(pts, P):  # 바다 위에 찍힌 좌표 검사 (여유 약 400m)
                if land.distance(pt) > 0.004: off.append((p['id'], p['n']['ko'], round(land.distance(pt) * 111, 1)))
        for z in c['zones']:
            zp = z['places']
            lat0 = sum(p['lat'] for p in zp) / len(zp); lng0 = sum(p['lng'] for p in zp) / len(zp)
            fwd, inv = proj_fn(lat0, lng0)
            xy = [fwd(p['lng'], p['lat']) for p in zp]
            spread = max(math.hypot(x1 - x2, y1 - y2) for x1, y1 in xy for x2, y2 in xy)
            rad = 850 if spread < 9000 else 1400
            circles = [Point(x, y).buffer(rad) for x, y in xy]
            blob = unary_union(circles).convex_hull.buffer(250) if spread < 9000 else unary_union(circles)
            blob_ll = transform(inv, blob)
            if land is not None:
                cut = blob_ll.intersection(land.buffer(0.003))
                if not cut.is_empty and cut.area > blob_ll.area * 0.25: blob_ll = cut
            for p in zp: geo['pd'][p['id']] = z['id']
            reg['districts'].append({'id': z['id'], 'n': z['n'], 'ids': [p['id'] for p in zp], 'g': rings_of(blob_ll.simplify(0.0006), 4), 'kind': 'zone'})
        geo['regions'][c['id']] = reg
    print('  regions done', round(time.time() - t0), 's')
    # ---------- 해외 전체 지도 (동아시아·동남아·괌·사이판) ----------
    if '--keep-world' in sys.argv and geo.get('world'):   # 전체 지도는 그대로 두고 도시만 다시 만들 때 (전체 지도는 6~7분 걸림)
        s = json.dumps(geo, ensure_ascii=False, separators=(',', ':'))
        open(B('geo.json'), 'w', encoding='utf-8').write(s)
        print('geo bytes', len(s), '(world kept)')
        if off: print('  ! 바다 위로 보이는 좌표(확인 필요, km):', off)
        return
    cc = [(c['lng'], c['lat']) for c in cities]
    def tiny(bb):   # 작은 섬은 도시가 있는 곳만 남긴다 (자르기 전에 걸러 속도를 낸다)
        if (bb[2] - bb[0]) * (bb[3] - bb[1]) > 0.35: return False
        return not any(bb[0] - 0.25 < x < bb[2] + 0.25 and bb[1] - 0.25 < y < bb[3] + 0.25 for x, y in cc)
    world = land_in(WORLD, tiny)
    keep = []
    for p in (world.geoms if hasattr(world, 'geoms') else [world]):
        a = p.area
        if a < 0.0004: continue
        q = Polygon(p.exterior).simplify(0.16 if a > 2 else 0.07 if a > 0.2 else 0.015, preserve_topology=True)
        if not q.is_empty and q.geom_type == 'Polygon': keep.append(q)
    geo['world'] = [[[round(x, 2), round(y, 2)] for x, y in poly.exterior.coords] for poly in keep]
    s = json.dumps(geo, ensure_ascii=False, separators=(',', ':'))
    open(B('geo.json'), 'w', encoding='utf-8').write(s)
    print('geo bytes', len(s), '| world rings', len(geo['world']), '| world bytes', len(json.dumps(geo['world'])), '|', round(time.time() - t0), 's')
    big = sorted(((len(json.dumps(geo['regions'][c['id']])), c['id']) for c in cities), reverse=True)[:8]
    print('largest regions', big, '| overseas regions bytes', sum(len(json.dumps(geo['regions'][c['id']])) for c in cities))
    if off: print('  ! 바다 위로 보이는 좌표(확인 필요, km):', off)


if __name__ == '__main__':
    main()
