"""K링크에서 근거 없는 장소를 뺀다 (2026-11-12 대표 지시: 부자연스러운 것·가상 장소는 빼고, 어라운드툴 콘텐츠가 정보를 대게).

빼는 것
- 실제 기관이 아닌 '피부과·스파' 예시 장소 (예약·통역 대행을 전제로 만든 시연용)
- 가게 이름 없이 만든 '○○ 맛집' 예시 (공식 출처가 없는 가게)
- 운영 여부를 확인하지 못한 곳
build/places.json 과 build/geo.json(구역 목록·장소→구역)에서 함께 지운다. 여러 번 돌려도 결과는 같다.
usage: python3 scripts/klink/tools/prune_places.py
"""
import json
import os

B = lambda f: os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build', f)

REMOVED = {
    # 시연용 의료·뷰티 예약
    'skin1', 'skin2', 'spa', 'bs_skin',
    # 출처 없는 가게·예시 맛집
    'samgyup', 'gejang', 'samgye', 'kalguksu', 'sbrunch', 'hanwoo', 'bs_gejang', 'jn_bibim', 'ys_gejang',
    # 운영 여부 확인 못 함
    'hybe',
}
# 남는 장소 중 근거 없는 표현을 고친다 (ko, zh, en, ja)
DESC = {
    'gwangjang': ['빈대떡·육회·김밥 등 시장 먹거리', '绿豆煎饼、生拌牛肉、紫菜包饭等市场小吃', 'Market food: mung bean pancakes, yukhoe, gimbap', 'ピンデトック・ユッケ・キンパなど市場グルメ'],
    'mdfood': ['저녁이면 노점이 늘어나는 먹거리 골목', '傍晚小吃摊变多的美食街', 'Street food stalls that fill up in the evening', '夕方から屋台が増える食べ歩き通り'],
    'dakgalbi': ['홍대 앞 닭갈비 가게들이 모인 골목', '弘大前辣炒鸡排店聚集的胡同', 'A lane of dakgalbi restaurants near Hongdae', '弘大前のタッカルビ店が集まる路地'],
    'bs_jagalchi': ['부산 대표 수산시장 · 회와 해산물', '釜山代表性水产市场 · 生鱼片与海鲜', "Busan's best-known fish market · raw fish and seafood", '釜山を代表する水産市場 · 刺身と海鮮'],
    'bs_gukbap': ['돼지국밥 가게가 모인 서면 골목', '西面猪肉汤饭店聚集的胡同', 'A Seomyeon lane of pork gukbap restaurants', '西面のテジクッパ店が集まる路地'],
    'jj_pork': ['제주 흑돼지 구이 가게들이 모인 거리', '济州黑猪烤肉店聚集的街道', 'A street of Jeju black pork BBQ restaurants', '済州黒豚焼肉店が集まる通り'],
    'gj_ssambap': ['쌈밥 가게들이 모인 대릉원 옆 거리', '大陵苑旁包饭店聚集的街道', 'A street of ssambap restaurants by Daereungwon', '大陵苑そばのサムパプ店が集まる通り'],
    'gn_jumunjin': ['동해 해산물을 사고 먹는 수산시장', '购买和品尝东海海鲜的水产市场', 'Fish market for East Sea seafood', '東海の海鮮を買って食べる水産市場'],
    'ys_night': ['여수 바닷가 포장마차 거리 야경', '丽水海边大排档街夜景', 'Seaside pojangmacha street at night', '麗水の海辺の屋台通りの夜景'],
}


def main():
    P = json.load(open(B('places.json'), encoding='utf-8'))
    keep = [p for p in P if p['id'] not in REMOVED]
    for p in keep:
        if p['id'] in DESC:
            p['d'] = dict(zip(['ko', 'zh', 'en', 'ja'], DESC[p['id']]))
        p['rsv'] = False      # '예약 필요' 표시는 근거가 없어 쓰지 않는다
        p['prem'] = False
    json.dump(keep, open(B('places.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    G = json.load(open(B('geo.json'), encoding='utf-8'))
    for reg in G['regions'].values():
        for d in reg['districts']:
            d['ids'] = [i for i in d['ids'] if i not in REMOVED]
    G['pd'] = {k: v for k, v in G['pd'].items() if k not in REMOVED}
    json.dump(G, open(B('geo.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('places', len(P), '->', len(keep))


if __name__ == '__main__':
    main()
