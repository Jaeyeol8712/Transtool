import json, sys, importlib.util
spec = importlib.util.spec_from_file_location('pm', sys.argv[1]); pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
old = json.load(open(sys.argv[2], encoding='utf-8'))
rows = {}
for line in pm.TABLE.strip().splitlines():
    i, la, lo, o1, o2, best, meal, h = line.split()
    rows[i] = dict(lat=float(la), lng=float(lo), o=[float(o1), float(o2)], best=best, meal=None if meal == '-' else meal, h=float(h))
L = ['zh', 'en', 'ja']
out = []
for p in old['PLACES']:
    pid = p['id']
    if pid in pm.UPDATES and pm.UPDATES[pid] is None: continue
    t = old['PL_T'].get(pid)
    q = dict(id=pid, c=p['c'], r=p['r'], cost=p['cost'], rsv=bool(p.get('rsv')), closed=p.get('closed', []), prem=bool(p.get('premium')), st=p['st'],
             n={'ko': p['n']}, d={'ko': p['d']})
    for k, l in enumerate(L):
        q['n'][l] = t[k*2]; q['d'][l] = t[k*2+1]
    out.append(q)
for (pid, c, r, cost, flags, st, ko, zh, en, ja) in pm.NEW:
    q = dict(id=pid, c=c, r=r, cost=cost, rsv=False, closed=[], prem=False, st=st, n={}, d={})
    for l, v in zip(['ko'] + L, [ko, zh, en, ja]): q['n'][l] = v[0]; q['d'][l] = v[1]
    q.update(flags); out.append(q)
for q in out:
    u = pm.UPDATES.get(q['id'])
    if u:
        u = dict(u)
        if 'd' in u: q['d'] = dict(zip(['ko'] + L, u.pop('d')))
        q.update(u)
    if q['id'] not in rows: raise SystemExit('missing coords ' + q['id'])
    q.update(rows[q['id']])
missing = set(rows) - {q['id'] for q in out}
if missing: raise SystemExit('extra rows ' + str(missing))
json.dump(out, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False)
from collections import Counter
print(len(out), Counter(q['r'] for q in out), Counter(q['c'] for q in out))
