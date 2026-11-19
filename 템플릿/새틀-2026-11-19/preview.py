import re,sys
SRC='/home/claude/transtool/'
CSS='''<style>
body,main,.at-page,.at-page-head,.b-card,.at-tool{background:#fff!important;box-shadow:none!important}
.nt{color:#222}
.nt p{font-size:16px!important;line-height:1.6!important;margin:0 0 10px!important;color:#222}
.nt b,.nt strong{color:#111}
.nt h2.q{font-size:19px!important;font-weight:800;margin:24px 0 10px!important;padding:0;border:0;background:none;color:#14315c}
.nt .key{border:1px solid #e5e7eb;border-radius:14px;padding:16px;margin:6px 0 10px;background:#fff}
.nt .key p{margin:0!important}
.nt .key .big{font-size:21px!important;font-weight:800;line-height:1.35!important;margin:0 0 12px!important;color:#14315c}
.nt .key em{font-style:normal;color:#14315c}
.nt .key .s{font-size:13px!important;color:#6b7280;margin-top:10px!important}
.nt .nums{display:grid;grid-template-columns:repeat(3,1fr);gap:0}
.nt .nums div{padding:4px 2px;text-align:center;border-left:1px solid #e5e7eb}
.nt .nums div:first-child{border-left:0}
.nt .nums b{display:block;font-size:21px;color:#111;line-height:1.25}
.nt .nums span{font-size:12px;color:#6b7280}
.nt .yn{font-size:15px;line-height:1.7;margin:0 0 6px}
.nt .chips{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 0}
.nt .chips span{border:1px solid #d1d5db;border-radius:20px;padding:4px 11px;font-size:14px;font-weight:600;color:#222;background:#fff}
.nt .flow{display:grid;grid-template-columns:repeat(var(--n,5),1fr);gap:4px;text-align:center}
.nt .flow div{border:1px solid #e5e7eb;border-radius:10px;padding:8px 2px;font-size:12px;font-weight:600;color:#222;line-height:1.3}
.nt .flow i{display:block;font-style:normal;font-size:20px;margin-bottom:2px}
.nt .rows{border-top:1px solid #e5e7eb}
.nt .rows div{display:flex;gap:10px;padding:9px 0;border-bottom:1px solid #e5e7eb;font-size:15px;line-height:1.45}
.nt .rows b{flex:0 0 60px}
.nt .tip{border-top:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb;padding:10px 0;margin:14px 0}
.nt .tip p{margin:0!important;font-size:15px!important;line-height:1.75!important}
.nt .lab{font-size:13px;color:#6b7280;border:1px dashed #9ca3af;display:inline-block;padding:3px 8px;border-radius:6px;margin:0 0 10px}
.nt details{border:1px solid #e5e7eb;border-radius:10px;margin:8px 0;background:#fff}
.nt summary{padding:11px 14px;font-weight:600;font-size:15px;color:#222}
.nt .next{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 0}
.nt .next a{padding:7px 12px;border-radius:20px;border:1px solid #d1d5db;color:#222;font-weight:600;text-decoration:none;font-size:14px}
.nt .sim{margin:22px 0 0;border-top:1px solid #222;padding-top:12px}
.nt .sim b.t{display:block;font-size:16px;color:#14315c;margin:0 0 4px}
.nt .sim a{display:flex;justify-content:space-between;padding:9px 2px;border-bottom:1px solid #e5e7eb;color:#222;text-decoration:none;font-size:15px;font-weight:500}
.nt .sim a span{color:#9ca3af}
.nt .ad{font-size:12px!important;color:#6b7280;margin:0 0 8px!important}
.nt .prod{width:100%;border-radius:12px;display:block;margin:0 0 8px}
.nt .btn{display:block;text-align:center;background:#e11d48;color:#fff!important;font-weight:800;font-size:17px;padding:14px;border-radius:12px;text-decoration:none;margin:8px 0 14px}
.nt .ex{border:1px solid #e5e7eb;border-radius:12px;padding:12px 14px;font-size:15px;line-height:1.7}
.nt .at-answer,.nt mark{background:none}
.nt b,.nt strong,.nt mark{background:none!important;box-shadow:none!important;text-decoration:none!important;padding:0!important}
.nt .flow{counter-reset:f}
.nt .flow div{counter-increment:f}
.nt .flow i{font-size:15px!important;font-weight:800;color:#14315c}
.nt .flow i::before{content:counter(f)}
.nt .yn span.m{font-weight:700;color:#111;margin-right:4px}
</style>'''
def sim(items): return '<div class="sim"><b class="t">비슷한 글</b>'+''.join(f'<a href="#">{t} <span>›</span></a>' for t in items)+'</div>'
def nxt(items): return '<div class="next">'+''.join(f'<a href="#">{t}</a>' for t in items)+'</div>'
def head(title,meta): return f'<header class="at-page-head"><h1>{title}</h1><p class="meta">{meta}</p></header>'
def wrap(title,meta,inner,lab): return f'<main><article>{head(title,meta)}{CSS}<div class="at-page"><div class="at-prose at-blog nt"><p class="lab">{lab} — 미리보기(사이트 미반영)</p>{inner}</div></div></article></main>'
EMO=re.compile('[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]')
def clean(x):
    x=re.sub(r'<i>[^<]*</i>','<i></i>',x)
    x=x.replace('⭕','<span class="m">추천</span>').replace('❌','<span class="m">비추천</span>').replace('➕','<span class="m">+</span>')
    x=re.sub('(?:'+EMO.pattern+')+ ?','',x)
    return x
def write(src,out,main,keep_tool=False):
    main=clean(main)
    h=open(SRC+src).read()
    if keep_tool:
        m=re.search(r'(<main.*?)<div class="at-prose">.*?</main>',h,re.S)
        new=m.group(1).replace('<main>','<main>'+CSS)+main+'</div></main>'
        h=h[:m.start()]+new+h[m.end():]
    else:
        h=re.sub(r'<main.*?</main>',lambda m:main,h,flags=re.S)
    open(SRC+out,'w').write(h)
