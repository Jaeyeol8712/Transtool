import re,os,base64,io,json,sys
from PIL import Image
R='/home/claude/transtool'
imp={}
for p in json.load(open('/tmp/gsc.json'))['pages']:
    k=p['page'].split('/')[-1].replace('.html',''); imp[k]=imp.get(k,0)+p['impressions']
def I(u): return imp.get(u.strip('/').replace('.html',''),0)
def thumb(p,w=480,h=320):
    im=Image.open(p).convert('RGB'); im.thumbnail((w,h)); b=io.BytesIO(); im.save(b,'JPEG',quality=70)
    return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
CSS=open('/home/claude/work/hub_travel.html').read()
CSS=re.search(r'<style>html body\.b.*?</style>',CSS,re.S).group(0)
CSS=CSS.replace('</style>','''.head{display:none!important}[data-k][hidden]{display:none!important}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.tiles a{border:1px solid #e5e7eb;border-radius:12px;padding:14px;text-decoration:none;color:#111;font-weight:700;font-size:15px;min-height:52px}
.tiles a small{display:block;font-weight:500;color:#9ca3af;font-size:13px;margin-top:4px}
.tabs{flex-wrap:wrap;column-gap:18px}
.pc{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}.pc a{text-decoration:none;color:#111}.pc .ph{display:block;aspect-ratio:4/3;border-radius:12px;background:#f2f4f7 center/cover}
.pc b{display:block;font-size:15px;margin:8px 0}.pc .bt{display:inline-block;background:#e11d48;color:#fff;font-weight:800;font-size:14px;padding:8px 14px;border-radius:10px}
.pc a.x{display:none}.pc.all a.x{display:block}.pc[hidden]{display:none!important}
.hl a b{font-weight:600}
@media(max-width:700px){.tiles{grid-template-columns:repeat(2,1fr)}}
</style>''')
JS='''<script>document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.tabs button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('[data-k]').forEach(l=>l.hidden=l.dataset.k!==b.dataset.t);const m=document.querySelector('.more');if(m)m.style.display='';});
const mb=document.querySelector('.more');if(mb)mb.onclick=e=>{document.querySelectorAll('[data-k]').forEach(l=>{if(!l.hidden)l.classList.add('all')});e.target.style.display='none'};
const si=document.querySelector('.hs input');if(si)si.oninput=e=>{const q=e.target.value.trim();document.querySelectorAll('[data-k]').forEach(l=>{l.classList.add('all');l.querySelectorAll('a').forEach(a=>a.style.display=!q||a.textContent.includes(q)?'':'none')})};</script>'''
def lst(items,key,hidden=False,cls='hl'):
    return f'<div class="{cls}" data-k="{key}"'+(' hidden' if hidden else '')+'>'+''.join(f'<a href="#" class="{"x" if i>=12 else ""}"><b>{n}</b></a>' for i,n in enumerate(items))+'</div>'
def tabs(groups):
    return '<div class="tabs">'+''.join(f'<button class="{"on" if i==0 else ""}" data-t="g{i}">{g} {len(v)}</button>' for i,(g,v) in enumerate(groups))+'</div>'+''.join(lst(v,f'g{i}',i>0) for i,(g,v) in enumerate(groups))+'<button class="more">더 보기</button>'
def page(src,out,title,ph,body):
    h=open(R+'/'+src).read()
    main=f'<main><article><div class="hub"><h1>{title}</h1><div class="hs"><input placeholder="{ph}"></div>{body}</div></article></main>'
    h=re.sub(r'<main.*?</main>',lambda m:main,h,flags=re.S)
    def cssin(m):
        u=re.search(r'href="([^"]+)"',m.group(0)).group(1); p=R+u.split('?')[0] if u.startswith('/') else None
        return '<style>'+open(p).read()+'</style>' if p and os.path.exists(p) else ''
    h=re.sub(r'<link[^>]*rel="stylesheet"[^>]*>',cssin,h)
    h=re.sub(r'<script.*?</script>','',h,flags=re.S)
    def img(m):
        p=R+m.group(2).split('?')[0]
        if os.path.exists(p): return f'{m.group(1)}="'+thumb(p,300,300)+'"'
        return m.group(0)
    h=re.sub(r'(src)="(/[^"]+\.(?:png|jpg|jpeg))"',img,h)
    h=re.sub(r'<link[^>]*(preload|preconnect|icon|manifest)[^>]*>','',h)
    h=h.replace('</head>',CSS+'</head>').replace('</body>',JS+'</body>')
    open(out,'w').write(h)
# 맛집
h=open(R+'/food.html').read(); m=re.search(r'<main.*?</main>',h,re.S).group(0)
groups=[];cur=None
for a,r in re.findall(r'<tr([^>]*)>(.*?)</tr>',m,re.S):
    if 'at-gr' in a: cur=[re.sub(r'(특별자치|광역|특별)?(시|도)$','',re.sub('<[^>]+>','',r.split('<span')[0]).strip()),[]];groups.append(cur);continue
    if "전체 보기" in r and cur and re.search(r"class=\"c\">(\d+)",r):
        u=re.search(r'href="([^"]+)"',r).group(1); n=re.search(r'class="c">(\d+)',r).group(1); gu=re.search(r'class="tag[^"]*">([^<]+)',r).group(1)
        (cur[1].append((gu,int(n),u)) if "메뉴" not in gu else None)
groups=[g for g in groups if g[1]]
for g in groups: g[0]={'인천':'인천','서울':'서울','부산':'부산','강원':'강원','대전':'대전','광주':'광주','제주':'제주','전라남':'전남','경상북':'경북'}.get(g[0],g[0])
allg=[(g,x) for g in groups for x in g[1]]
top=sorted(allg,key=lambda t:-I(t[1][2]))[:8]
tiles='<h2>많이 찾는 맛집</h2><div class="tiles">'+''.join(f'<a href="#">{g[0]} {x[0]}<small>{x[1]}곳</small></a>' for g,x in top)+'</div>'
body=tiles+'<div class="tabs">'+''.join(f'<button class="{"on" if i==0 else ""}" data-t="g{i}">{g[0]} {sum(x[1] for x in g[1])}</button>' for i,g in enumerate(groups))+'</div>'
body+=''.join(f'<div class="tiles" data-k="g{i}"'+(' hidden' if i else '')+' style="margin-top:12px">'+''.join(f'<a href="#">{x[0]}<small>{x[1]}곳</small></a>' for x in g[1])+'</div>' for i,g in enumerate(groups))
body=body.replace('<div class="tiles" data-k','<div class="tiles tl" data-k')
page('food.html','hub_food.html','맛집','지역이나 음식으로 찾기',body)
print('food',[ (g[0],len(g[1])) for g in groups])
# 계산기
h=open(R+'/tools.html').read(); m=re.search(r'<main.*?</main>',h,re.S).group(0)
tg=[];cur=None
for r in re.findall(r'<tr[^>]*>(.*?)</tr>',m,re.S):
    if 'colspan' in r: cur=[re.sub('<[^>]+>','',r.split('<span')[0]).strip(),[]];tg.append(cur);continue
    a=re.search(r'<a href="([^"]+)">([^<]+)</a>',r)
    if a and cur: cur[1].append((a.group(2),a.group(1)))
tg=[g for g in tg if g[1]]
alltools=[x for g in tg for x in g[1]]
top=sorted(alltools,key=lambda x:-I(x[1]))[:8]
body='<h2>많이 쓰는 계산기</h2><div class="tiles">'+''.join(f'<a href="#">{n}</a>' for n,u in top)+'</div>'+tabs([(g[0],[n for n,u in g[1]]) for g in tg])
page('tools.html','hub_tools.html','계산기','계산기 이름으로 찾기',body)
print('tools',[(g[0],len(g[1])) for g in tg],[n for n,u in top])
# 가이드
h=open(R+'/etc.html').read(); m=re.search(r'<main.*?</main>',h,re.S).group(0)
G=[]
for gm in re.finditer(r'<h2>([^<]+)<span class="c">\d+</span></h2><ul>(.*?)</ul>',m,re.S):
    G.append([gm.group(1),re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>',gm.group(2))])
trav=re.compile(r'passport|eta|esta|visa|tdac|mdac|etravel|arrival|duty-free|liquids|tax-free|travel|immigration|roaming|esim|airport|baggage|china-visa|k-eta|uk-eta')
bucket={'여행·입국':[]};order=[]
for name,items in G:
    if '텍스트' in name or '사이트' in name: continue
    for u,t in items:
        k='여행·입국' if trav.search(u) else name.replace('생활·건강·여행','생활·건강')
        bucket.setdefault(k,[]).append((t,u))
groups=[(k,v) for k,v in bucket.items() if v]
groups.sort(key=lambda kv:-len(kv[1]) if kv[0]!='여행·입국' else -999)
allg=[x for k,v in groups for x in v]
top=sorted(allg,key=lambda x:-I(x[1]))[:8]
body='<h2>많이 찾는 가이드</h2><div class="tiles">'+''.join(f'<a href="#">{t}</a>' for t,u in top)+'</div>'+tabs([(k,[t for t,u in v]) for k,v in groups])
page('etc.html','hub_guide.html','가이드','궁금한 것 찾기',body)
print('guide',[(k,len(v)) for k,v in groups])
# 추천
sys.path.insert(0,R+'/scripts')
import connect_posts as cp
P=cp.POSTS
def card(p,i):
    s=p['slug']; ph=None
    for f in ('thumb.jpg','product.jpg','og.jpg'):
        q=f'{R}/assets/shop/{s}/{f}'
        if os.path.exists(q): ph=q;break
    st=f'background-image:url({thumb(ph,400,300)})' if ph else ''
    return f'<a href="#" class="{"x" if i>=6 else ""}"><span class="ph" style="{st}"></span><b>{p["title"]}</b><span class="bt">{"제품 가격 알아보기 >>" if p.get("kind","product")=="product" else "여행 비용 알아보기 >>"}</span></a>'
prod=[p for p in P if p.get('kind','product')=='product'][:12]; trv=[p for p in P if p.get('kind')=='travel'][:12]
nprod=len([p for p in P if p.get('kind','product')=='product']); ntrv=len([p for p in P if p.get('kind')=='travel'])
body=f'<div class="tabs"><button class="on" data-t="p">제품 추천 {nprod}</button><button data-t="t">여행 추천 {ntrv}</button></div>'
body+='<div class="pc" data-k="p" style="margin-top:14px">'+''.join(card(p,i) for i,p in enumerate(prod))+'</div>'
body+='<div class="pc" data-k="t" hidden style="margin-top:14px">'+''.join(card(p,i) for i,p in enumerate(trv))+'</div><button class="more">더 보기</button>'
page('connect.html','hub_shop.html','추천','제품·여행 이름으로 찾기',body)
print('shop',nprod,ntrv)
