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
    if code == '35020': return 'gunsan'
    if code == '36010': return 'mokpo'
    if code == '33380': return 'danyang'
    if code in ('37011', '37012'): return 'pohang'
    if code == '32060': return 'sokcho'  # 2026-11-21(2차)
    if code == '32010': return 'chuncheon'  # 2026-11-25
    if code == '38050': return 'tongyeong'  # 2026-11-25
    if code.startswith('26'): return 'ulsan'  # 2026-11-26 (KOSTAT 2013 울산 26xxx)
    if code == '36310': return 'damyang'  # 2026-11-26
    if code == '31370': return 'gapyeong'  # 2026-11-27
    if code.startswith('23') and code not in ('23310', '23320'): return 'incheon'  # 2026-11-27 (강화·옹진 제외)
    if code.startswith('22') and code != '22310': return 'daegu'  # 달성군 제외
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
 '완산구':['完山区','Wansan-gu','完山区'],'군산시':['群山市','Gunsan-si','群山市'],'목포시':['木浦市','Mokpo-si','木浦市'],'단양군':['丹阳郡','Danyang-gun','丹陽郡'],'포항시남구':['浦项市南区','Nam-gu, Pohang','浦項市南区'],'포항시북구':['浦项市北区','Buk-gu, Pohang','浦項市北区'],'속초시':['束草市','Sokcho-si','束草市'],'춘천시':['春川市','Chuncheon-si','春川市'],'통영시':['统营市','Tongyeong-si','統営市'],'울주군':['蔚州郡','Ulju-gun','蔚州郡'],'담양군':['潭阳郡','Damyang-gun','潭陽郡'],'가평군':['加平郡','Gapyeong-gun','加平郡'],'연수구':['延寿区','Yeonsu-gu','延寿区'],'남동구':['南洞区','Namdong-gu','南洞区'],'남구':['南区','Nam-gu','南区'],'부평구':['富平区','Bupyeong-gu','富平区'],'계양구':['桂阳区','Gyeyang-gu','桂陽区'],'수성구':['寿城区','Suseong-gu','寿城区'],'달서구':['达西区','Dalseo-gu','達西区'],'덕진구':['德津区','Deokjin-gu','徳津区'],
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
 'gunsan': [('gs_down', ['gs_museum','gs_chowon','gs_dongguksa','gs_market'], ['군산 원도심','群山旧城','Old Town Gunsan','群山旧市街']),
            ('gs_east', ['gs_rail','gs_eunpa'], ['철길마을·은파','铁路村·银波湖','Railroad Village & Eunpa','線路村・銀波湖']),
            ('gs_island', ['gs_seonyudo'], ['고군산군도','古群山群岛','Gogunsan Islands','古群山群島'])],
 'mokpo': [('mp_old', ['mp_modern','mp_yudal','mp_market','mp_cable'], ['원도심·유달산','旧城·儒达山','Old Town & Yudalsan','旧市街・儒達山']),
           ('mp_gohado', ['mp_gohado'], ['고하도','高下岛','Gohado','高下島']),
           ('mp_hadang', ['mp_gatbawi','mp_peace'], ['하당·평화광장','下塘·和平广场','Hadang & Peace Plaza','下塘・平和広場'])],
 'danyang': [('dy_town', ['dy_manchunha','dy_jando','dy_gosu','dy_market'], ['단양읍·남한강','丹阳邑·南汉江','Danyang Town & River','丹陽邑・南漢江']),
             ('dy_dodam', ['dy_dodam'], ['도담삼봉','岛潭三峰','Dodamsambong','島潭三峰']),
             ('dy_sainam', ['dy_sainam'], ['사인암','舍人岩','Sainam','舎人岩']),
             ('dy_ondal', ['dy_ondal'], ['영춘·온달','永春·温达','Yeongchun & Ondal','永春・温達'])],
 'pohang': [('ph_city', ['ph_spacewalk','ph_yeongildae','ph_jukdo','ph_canal'], ['포항 시내','浦项市区','Pohang City','浦項市内']),
            ('ph_east', ['ph_homigot','ph_guryongpo'], ['호미곶·구룡포','虎尾串·九龙浦','Homigot & Guryongpo','虎尾串・九龍浦']),
            ('ph_north', ['ph_igari'], ['이가리','二佳里','Igari','イガリ'])],
 'sokcho': [('sc_north', ['sc_youngkeum', 'sc_yeongnang'], ['북쪽 (영금정·영랑호)', '北部（灵琴亭·永郎湖）', 'North (Yeonggeumjeong & Yeongnangho)', '北部（霊琴亭・永郎湖）']),
           ('sc_downtown', ['sc_abai', 'sc_market'], ['시내 (갯배·수산시장)', '市区（渡船·水产市场）', 'Downtown (Gaetbae & Market)', '市街地（渡し船・水産市場）']),
           ('sc_south', ['sc_beach', 'sc_daepo'], ['남쪽 (해수욕장·대포항)', '南部（海水浴场·大浦港）', 'South (Beach & Daepo Port)', '南部（海水浴場・大浦港）']),
           ('sc_seorak', ['sc_seorak_cable'], ['설악동 (케이블카)', '雪岳洞（缆车）', 'Seorak-dong (Cable Car)', '雪岳洞（ケーブルカー）'])],
 'daegu': [('dg_old', ['dg_modern', 'dg_seomun', 'dg_dongseongno', 'dg_kimkwangseok'], ['원도심 (중구)', '老城区(中区)', 'Old Downtown (Jung-gu)', '旧市街(中区)']),
           ('dg_south', ['dg_apsan', 'dg_suseong'], ['앞산·수성못 (남구·수성구)', '前山·寿城池', 'Apsan & Suseongmot', '前山・寿城池']),
           ('dg_west', ['dg_eworld'], ['두류공원 (달서구)', '头流公园(达西区)', 'Duryu Park (Dalseo-gu)', '頭流公園(達西区)']),
           ('dg_palgongsan', ['dg_palgong'], ['팔공산 (동구)', '八公山(东区)', 'Palgongsan (Dong-gu)', '八公山(東区)'])],
 'chuncheon': [('cc_downtown', ['cc_skywalk', 'cc_dakgalbi'], ['시내 (스카이워크·닭갈비골목)', '市区（天空步道·鸡排街）', 'Downtown (Skywalk & Dakgalbi Street)', '市街地（スカイウォーク・タッカルビ通り）']),
           ('cc_uiamho', ['cc_gongjicheon', 'cc_samak_cable'], ['의암호 (공지천·케이블카)', '衣岩湖（孔之川·缆车）', 'Uiamho Lake (Gongjicheon & Cable Car)', '衣岩湖（孔之川・ケーブルカー）']),
           ('cc_sinbuk', ['cc_soyang_dam', 'cc_makguksu'], ['신북읍 (소양강댐·막국수박물관)', '新北邑（昭阳江大坝·荞麦面博物馆）', 'Sinbuk-eup (Dam & Makguksu Museum)', '新北邑（ダム・マックッス博物館）']),
           ('cc_sindong', ['cc_kimyujeong'], ['신동면 (김유정문학촌)', '新东面（金裕贞文学村）', 'Sindong-myeon (Kim Yu-jeong Village)', '新東面（金裕貞文学村）'])],
 'tongyeong': [('ty_donam', ['ty_cablecar', 'ty_luge'], ['도남동 (케이블카·루지)', '道南洞（缆车·滑车）', 'Donam-dong (Cable Car & Luge)', '道南洞（ケーブルカー・リュージュ）']),
           ('ty_ganguan', ['ty_dongpirang', 'ty_jungang', 'ty_tongjeyoung', 'ty_dipirang'], ['강구안 원도심', '江口岸老城区', 'Gangguan Old Town', '江口岸旧市街']),
           ('ty_east', ['ty_yisunsin'], ['정량동 (이순신공원)', '鼎梁洞（李舜臣公园）', 'Jeongnyang-dong (Yi Sun-sin Park)', '鼎梁洞（李舜臣公園）']),
           ('ty_sanyang', ['ty_dala'], ['산양읍 (달아공원)', '山阳邑（达牙公园）', 'Sanyang-eup (Dala Park)', '山陽邑（ダラ公園）'])],
 'ulsan': [
           ('ul_downtown', ['ul_taehwagang'], ['도심 (태화강 국가정원)', '市中心（太和江国家庭园）', 'Downtown (Taehwagang Garden)', '市中心（太和江国家庭園）']),
           ('ul_donggu', ['ul_bridge_view', 'ul_daewangam', 'ul_bangeojin'], ['동구 (대왕암공원·방어진)', '东区（大王岩公园·方鱼津）', 'Dong-gu (Daewangam & Bangeojin)', '東区（大王岩公園・方魚津）']),
           ('ul_namgu', ['ul_jangsaengpo'], ['남구 (장생포)', '南区（长生浦）', 'Nam-gu (Jangsaengpo)', '南区（長生浦）']),
           ('ul_ulju_west', ['ul_eonyang_bulgogi', 'ul_alps'], ['울주 서부 (언양·영남알프스)', '蔚州西部（彦阳·岭南阿尔卑斯）', 'West Ulju (Eonyang & Yeongnam Alps)', '蔚州西部（彦陽・嶺南アルプス）']),
           ('ul_ulju_coast', ['ul_ganjeolgot'], ['울주 해안 (간절곶)', '蔚州海岸（艮绝串）', 'Ulju Coast (Ganjeolgot)', '蔚州海岸（艮絶串）'])],
 'damyang': [
           ('dm_eup', ['dm_juknokwon', 'dm_gwanbang', 'dm_noodle'], ['담양읍 (죽녹원·관방제림·국수거리)', '潭阳邑（竹绿苑·官防堤林·面条街）', 'Damyang-eup (Juknokwon, Gwanbangjerim, Noodle Street)', '潭陽邑（竹緑苑・官防堤林・ククス通り）']),
           ('dm_hakdong', ['dm_metasequoia', 'dm_metaprovence'], ['학동리 (메타세쿼이아길·메타프로방스)', '鹤洞里（水杉林荫路·Meta Provence）', 'Hakdong-ri (Metasequoia Road & Meta Provence)', '鶴洞里（メタセコイア並木道・メタプロバンス）']),
           ('dm_gasa_zone', ['dm_soswaewon', 'dm_gasa'], ['가사문학면 (소쇄원·가사문학관)', '歌辞文学面（潇洒园·歌辞文学馆）', 'Gasamunhak-myeon (Soswaewon & Gasa Museum)', '歌辞文学面（瀟灑園・歌辞文学館）'])],
 'gapyeong': [
           ('gp_eup', ['gp_nami', 'gp_jarasum', 'gp_railbike', 'gp_jat_market'], ['가평읍 (남이섬·자라섬·레일바이크)', '加平邑（南怡岛·紫鳞岛·铁路自行车）', 'Gapyeong-eup (Nami, Jarasum & Rail Bike)', '加平邑（南怡島・チャラ島・レールバイク）']),
           ('gp_sangmyeon', ['gp_morningcalm', 'gp_jat_forest'], ['상면 (아침고요수목원·잣향기푸른숲)', '上面（晨静树木园·松子香绿林）', 'Sang-myeon (Morning Calm & Pine-nut Forest)', '上面（朝の静かな樹木園・チャッヒャンギ・プルンスプ）']),
           ('gp_cheongpyeong', ['gp_petitefrance'], ['청평 (쁘띠프랑스)', '清平（小法国村）', 'Cheongpyeong (Petite France)', '清平（プチフランス）']),
],
 'incheon': [
           ('ic_openport', ['ic_chinatown', 'ic_jjajang_museum', 'ic_fairytale', 'ic_gaehangjang', 'ic_sinpo_market'], ['개항장 (차이나타운·신포시장)', '开港场（中华街·新浦市场）', 'Open Port Area (Chinatown & Sinpo)', '開港場（チャイナタウン・新浦市場）']),
           ('ic_wolmido', ['ic_wolmi_train'], ['월미도 (월미바다열차)', '月尾岛（月尾海洋列车）', 'Wolmido (Wolmi Sea Train)', '月尾島（月尾海列車）']),
           ('ic_songdo', ['ic_songdo_park'], ['송도 (센트럴파크)', '松岛（中央公园）', 'Songdo (Central Park)', '松島（セントラルパーク）']),
           ('ic_sorae', ['ic_sorae'], ['소래 (소래포구)', '苏莱（苏莱浦口）', 'Sorae (Sorae Port)', '蘇莱（蘇莱浦口）']),
],
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
            ids = [i for i in ids if i in pbyid]  # 지운 장소는 건너뜀
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
