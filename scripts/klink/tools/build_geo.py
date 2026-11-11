"""Build compact map geometry for the app from KOSTAT 2013 boundaries.
usage: python3 -I build_geo.py <kostat_json_dir> <places.json> <out.json>
"""
import json, math, sys
from shapely.geometry import shape, Point, Polygon, MultiPolygon, LineString, box, mapping
from shapely.ops import unary_union, transform
import warnings; warnings.filterwarnings('ignore')

KDIR, PLACES, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
places = json.load(open(PLACES, encoding='utf-8'))
prov = json.load(open(KDIR + '/skorea_provinces_geo_simple.json', encoding='utf-8'))
muni = json.load(open(KDIR + '/skorea_municipalities_geo_simple.json', encoding='utf-8'))

def rnd(v, n): return round(v, n)
def rings_of(geom, nd):
    polys = [geom] if geom.geom_type == 'Polygon' else list(getattr(geom, 'geoms', []))
    out = []
    for p in polys:
        if p.is_empty or p.geom_type != 'Polygon': continue
        rs = [p.exterior] + list(p.interiors)
        out.append([[[rnd(x, nd), rnd(y, nd)] for x, y in r.coords] for r in rs])
    return out

# ---------- 1. Korea (provinces) ----------
korea = []
for f in prov['features']:
    g = shape(f['geometry']).buffer(0)
    g = g.simplify(0.01, preserve_topology=True)
    polys = [g] if g.geom_type == 'Polygon' else list(g.geoms)
    polys = [p for p in polys if p.area > 0.004]
    for p in polys:
        korea.append([[rnd(x, 3), rnd(y, 3)] for x, y in p.exterior.coords])

# ---------- 2. Regions & municipalities ----------
def region_of_code(code, name):
    if code.startswith('11'): return 'seoul'
    if code.startswith('21'): return 'busan'
    if code.startswith('39'): return 'jeju'
    if code == '37020': return 'gyeongju'
    if code == '32030': return 'gangneung'
    if code == '36020': return 'yeosu'
    if code in ('35011', '35012'): return 'jeonju'
    return None
MF = [(f['properties']['code'], f['properties']['name'].replace('전주시', ''), shape(f['geometry']).buffer(0)) for f in muni['features']]
full = json.load(open(KDIR + '/skorea_municipalities_geo.json', encoding='utf-8'))
FULL = {f['properties']['code']: shape(f['geometry']).buffer(0) for f in full['features'] if region_of_code(f['properties']['code'], '')}
del full
REG = {}
for code, name, g in MF:
    r = region_of_code(code, name)
    if r: REG.setdefault(r, []).append((code, name, g))

GU_T = {
 '종로구':['钟路区','Jongno-gu','鍾路区'],'중구':['中区','Jung-gu','中区'],'용산구':['龙山区','Yongsan-gu','龍山区'],'성동구':['城东区','Seongdong-gu','城東区'],
 '광진구':['广津区','Gwangjin-gu','広津区'],'동대문구':['东大门区','Dongdaemun-gu','東大門区'],'중랑구':['中浪区','Jungnang-gu','中浪区'],'성북구':['城北区','Seongbuk-gu','城北区'],
 '강북구':['江北区','Gangbuk-gu','江北区'],'도봉구':['道峰区','Dobong-gu','道峰区'],'노원구':['芦原区','Nowon-gu','蘆原区'],'은평구':['恩平区','Eunpyeong-gu','恩平区'],
 '서대문구':['西大门区','Seodaemun-gu','西大門区'],'마포구':['麻浦区','Mapo-gu','麻浦区'],'양천구':['阳川区','Yangcheon-gu','陽川区'],'강서구':['江西区','Gangseo-gu','江西区'],
 '구로구':['九老区','Guro-gu','九老区'],'금천구':['衿川区','Geumcheon-gu','衿川区'],'영등포구':['永登浦区','Yeongdeungpo-gu','永登浦区'],'동작구':['铜雀区','Dongjak-gu','銅雀区'],
 '관악구':['冠岳区','Gwanak-gu','冠岳区'],'서초구':['瑞草区','Seocho-gu','瑞草区'],'강남구':['江南区','Gangnam-gu','江南区'],'송파구':['松坡区','Songpa-gu','松坡区'],
 '강동구':['江东区','Gangdong-gu','江東区'],'서구':['西区','Seo-gu','西区'],'동구':['东区','Dong-gu','東区'],'영도구':['影岛区','Yeongdo-gu','影島区'],
 '부산진구':['釜山镇区','Busanjin-gu','釜山鎮区'],'동래구':['东莱区','Dongnae-gu','東萊区'],'남구':['南区','Nam-gu','南区'],'북구':['北区','Buk-gu','北区'],
 '해운대구':['海云台区','Haeundae-gu','海雲台区'],'사하구':['沙下区','Saha-gu','沙下区'],'금정구':['金井区','Geumjeong-gu','金井区'],'연제구':['莲堤区','Yeonje-gu','蓮堤区'],
 '수영구':['水营区','Suyeong-gu','水営区'],'사상구':['沙上区','Sasang-gu','沙上区'],'기장군':['机张郡','Gijang-gun','機張郡'],'제주시':['济州市','Jeju-si','済州市'],
 '서귀포시':['西归浦市','Seogwipo-si','西帰浦市'],'경주시':['庆州市','Gyeongju-si','慶州市'],'강릉시':['江陵市','Gangneung-si','江陵市'],'여수시':['丽水市','Yeosu-si','麗水市'],
 '완산구':['完山区','Wansan-gu','完山区'],'덕진구':['德津区','Deokjin-gu','徳津区'],
}
ZONES = {
 'jeju': [('jj_city', ['jj_pork','jj_dongmun','jj_dutyfree'], ['제주 시내','济州市区','Jeju City','済州市内']),
          ('jj_aewol', ['jj_aewol','jj_sunset'], ['애월','涯月','Aewol','涯月']),
          ('jj_hallim', ['jj_hyeopjae'], ['한림·협재','翰林·挟才','Hallim & Hyeopjae','翰林・挟才']),
          ('jj_andeok', ['jj_osulloc'], ['안덕·오설록','安德·O\'sulloc','Andeok & O\'sulloc','安徳・オソルロク']),
          ('jj_halla', ['jj_halla'], ['한라산','汉拿山','Hallasan','漢拏山']),
          ('jj_jungmun', ['jj_jusang'], ['중문','中文','Jungmun','中文']),
          ('jj_seogwipo', ['jj_cheonjiyeon'], ['서귀포 시내','西归浦市区','Seogwipo City','西帰浦市内']),
          ('jj_seongsan', ['jj_seongsan','jj_seopji','jj_udo'], ['성산·우도','城山·牛岛','Seongsan & Udo','城山・牛島'])],
 'gyeongju': [('gj_down', ['gj_daereung','gj_hwangni','gj_wolji','gj_ssambap','gj_gyochon'], ['경주 시내·황리단길','庆州市区·皇理团路','Downtown & Hwangnidan-gil','慶州市内・皇理団通り']),
              ('gj_bomun', ['gj_bomun'], ['보문관광단지','普门旅游区','Bomun Resort','普門観光団地']),
              ('gj_bulguk', ['gj_bulguksa','gj_seokguram'], ['불국사·석굴암','佛国寺·石窟庵','Bulguksa & Seokguram','仏国寺・石窟庵'])],
 'gangneung': [('gn_down', ['gn_ojukheon','gn_jungang'], ['강릉 시내','江陵市区','Downtown Gangneung','江陵市内']),
               ('gn_gyeongpo', ['gn_gyeongpo','gn_sundubu'], ['경포·초당','镜浦·草堂','Gyeongpo & Chodang','鏡浦・草堂']),
               ('gn_anmok', ['gn_anmok'], ['안목해변','安木海边','Anmok Beach','安木ビーチ']),
               ('gn_jumunjin', ['gn_jumunjin','gn_bts'], ['주문진','注文津','Jumunjin','注文津'])],
 'jeonju': [('jn_hanok', ['jn_hanok','jn_bibim','jn_night','jn_gyeonggi','jn_tea','jn_jeondong'], ['한옥마을 일대','韩屋村一带','Hanok Village area','韓屋村一帯'])],
 'yeosu': [('ys_down', ['ys_night','ys_gejang','ys_odong','ys_aqua','ys_cable','ys_dolsanpark'], ['여수 시내·오동도','丽水市区·梧桐岛','Downtown & Odongdo','麗水市内・梧桐島']),
           ('ys_hyangil', ['ys_hyangil'], ['향일암','向日庵','Hyangiram','向日庵'])],
}
HAN = [(37.598,126.808),(37.582,126.826),(37.570,126.860),(37.553,126.893),(37.5435,126.905),(37.536,126.925),(37.534,126.940),(37.527,126.950),
       (37.517,126.959),(37.510,126.980),(37.513,126.996),(37.527,127.012),(37.536,127.018),(37.537,127.035),(37.534,127.059),(37.525,127.065),
       (37.524,127.092),(37.534,127.105),(37.542,127.120),(37.555,127.140),(37.565,127.165)]

def proj_fn(lat0, lng0):
    kx = math.cos(math.radians(lat0)) * 111320.0; ky = 110574.0
    fwd = lambda x, y, z=None: ((x - lng0) * kx, (y - lat0) * ky)
    inv = lambda x, y, z=None: (x / kx + lng0, y / ky + lat0)
    return fwd, inv

pbyid = {p['id']: p for p in places}
regions_out = {}
diorama = {}
place_district = {}
for r, items in REG.items():
    land_r = unary_union([g for _, _, g in items])
    minx, miny, maxx, maxy = land_r.bounds
    ex = max(maxx - minx, maxy - miny) * 0.35
    ctx = box(minx - ex, miny - ex, maxx + ex, maxy + ex)
    neigh = [g for code, name, g in MF if g.intersects(ctx) and (code, name) not in {(c, n) for c, n, _ in items}]
    reg = {'munis': [], 'neigh': [], 'districts': [], 'water': []}
    for code, name, g in items:
        reg['munis'].append({'code': code, 'n': [name] + GU_T.get(name, [name] * 3), 'g': rings_of(g.simplify(0.0012, preserve_topology=True), 4)})
    for g in neigh:
        gg = g.intersection(ctx).simplify(0.003, preserve_topology=True)
        if not gg.is_empty: reg['neigh'] += rings_of(gg, 3)
    # river
    river = None
    if r == 'seoul':
        lat0, lng0 = 37.55, 126.98
        fwd, inv = proj_fn(lat0, lng0)
        line = transform(fwd, LineString([(lo, la) for la, lo in HAN]))
        river_m = line.buffer(430, cap_style=1, join_style=1)
        river = transform(inv, river_m)
        reg['water'] = rings_of(river.simplify(0.0008), 4)
    # districts
    rp = [p for p in places if p['r'] == r]
    if r in ('seoul', 'busan'):
        for p in rp:
            pt = Point(p['lng'], p['lat'])
            best = min(items, key=lambda it: FULL[it[0]].distance(pt))
            place_district[p['id']] = best[0]
        dist_codes = sorted({place_district[p['id']] for p in rp})
        for code in dist_codes:
            code_, name, g = next(it for it in items if it[0] == code)
            ids = [p['id'] for p in rp if place_district[p['id']] == code]
            reg['districts'].append({'id': code, 'n': [name] + GU_T.get(name, [name] * 3), 'ids': ids, 'g': rings_of(g.simplify(0.0008, preserve_topology=True), 4), 'kind': 'gu'})
    else:
        for zid, ids, names in ZONES[r]:
            pts = [pbyid[i] for i in ids]
            lat0 = sum(p['lat'] for p in pts) / len(pts); lng0 = sum(p['lng'] for p in pts) / len(pts)
            fwd, inv = proj_fn(lat0, lng0)
            blob = unary_union([Point(fwd(p['lng'], p['lat'])).buffer(850) for p in pts]).convex_hull.buffer(250)
            blob_ll = transform(inv, blob).intersection(land_r.buffer(0.0005))
            if blob_ll.is_empty: blob_ll = transform(inv, blob)
            for i in ids: place_district[i] = zid
            reg['districts'].append({'id': zid, 'n': names, 'ids': ids, 'g': rings_of(blob_ll.simplify(0.0006), 4), 'kind': 'zone'})
    regions_out[r] = reg
    # dioramas
    land_all = unary_union([g for _, _, g in items] + neigh)
    for d in reg['districts']:
        pts = [pbyid[i] for i in d['ids']]
        la = [p['lat'] for p in pts]; lo = [p['lng'] for p in pts]
        lat0 = (min(la) + max(la)) / 2; lng0 = (min(lo) + max(lo)) / 2
        fwd, inv = proj_fn(lat0, lng0)
        xy = [fwd(p['lng'], p['lat']) for p in pts]
        w = max(x for x, _ in xy) - min(x for x, _ in xy); h = max(y for _, y in xy) - min(y for _, y in xy)
        side = min(max(max(w, h) + 2200, 2400), 9000)
        sq = box(-side / 2, -side / 2, side / 2, side / 2)
        land_m = transform(fwd, land_all.intersection(transform(inv, sq).buffer(0.01))).intersection(sq)
        if d['kind'] == 'gu':
            focus_src = next(g for c, n, g in items if c == d['id'])
        else:
            focus_src = transform(inv, unary_union([Point(x, y).buffer(700) for x, y in xy]).convex_hull.buffer(300))
        focus_m = transform(fwd, focus_src).intersection(sq).intersection(land_m.buffer(1))
        water_m = transform(fwd, river).intersection(sq) if river is not None else Polygon()
        tol = side / 900
        diorama[d['id']] = {
            'c': [rnd(lat0, 5), rnd(lng0, 5)], 's': round(side),
            'land': rings_of(land_m.simplify(tol), 0), 'focus': rings_of(focus_m.simplify(tol), 0), 'water': rings_of(water_m.simplify(tol), 0),
        }

# integer-ize dioramas
for d in diorama.values():
    for k in ('land', 'focus', 'water'):
        d[k] = [[[[int(x), int(y)] for x, y in ring] for ring in poly] for poly in d[k]]

out = {'korea': korea, 'regions': regions_out, 'diorama': diorama, 'pd': place_district}
s = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
open(OUT, 'w', encoding='utf-8').write(s)
print('bytes', len(s), 'korea rings', len(korea))
for r, reg in regions_out.items():
    print(r, 'munis', len(reg['munis']), 'districts', [(d['id'], d['n'][0], len(d['ids'])) for d in reg['districts']])
print('diorama sizes', {k: (v['s'], len(json.dumps(v))) for k, v in list(diorama.items())[:6]})
