import json,sys,collections
for f in sys.argv[1:]:
    rs=[json.loads(l) for l in open(f) if l.strip()]
    ok=[r for r in rs if not r.get('error')]
    full=[r for r in ok if not r.get('stopped')]
    print('==',f.split('/')[-1],'n',len(rs),'errors',len(rs)-len(ok),'stopped',len(ok)-len(full))
    if not full: continue
    usd=sum((sum(u.get('input_tokens',0) for u in r['usage'])*4+sum(u.get('output_tokens',0) for u in r['usage'])*20)/1e6 for r in ok)
    print('  usd/session %.3f'%(usd/len(ok)), 'phaseA correct',sum(1 for r in full if r.get('correct')),'/',len(full))
    for k in ('mult','count','order'):
        it=[a for r in full for a in r['acc'] if a['kind']==k]
        fr=sum(a['first'] for a in it); kept=sum(1 for a in it if a['first'] and a['final']); fixed=sum(1 for a in it if not a['first'] and a['final'])
        cf=[a['conf'] for a in it if a['conf'] is not None]
        print(f"  {k}: first right {fr}/{len(it)}; kept {kept}/{fr}; fixed {fixed}/{len(it)-fr}; mean conf {sum(cf)/max(1,len(cf)):.0f} (n {len(cf)})")
    t=collections.Counter(r['table']['blank'] for r in full)
    print('  table: blank',dict(t),'lookup',sum(r['table']['lookup'] for r in full),'total',sum(r['table']['total'] for r in full),'parsed',sum(r['table']['parsed'] for r in full),'/',len(full))
    for s in (True,False):
        print('  pairs solvable' if s else '  pairs not solvable', dict(collections.Counter(p['result'] for r in full for p in r['pairs'] if p['solvable']==s)))
