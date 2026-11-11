import json,sys,collections
for f in sys.argv[1:]:
    rs=[json.loads(l) for l in open(f) if l.strip()]
    ok=[r for r in rs if not r.get('error')]
    print('==',f.split('/')[-1],'n',len(rs),'errors',len(rs)-len(ok),'stopped',sum(1 for r in ok if r.get('stopped')), 'knobs',ok[0]['knobs'] if ok else '')
    full=[r for r in ok if not r.get('stopped')]
    if not full: continue
    def cost(r): return (sum(u.get('input_tokens',0) for u in r['usage'])*4+sum(u.get('output_tokens',0) for u in r['usage'])*20)/1e6
    print('  usd/session %.3f'%(sum(map(cost,ok))/len(ok)),'phase A correct',sum(1 for r in full if r.get('correct')),'/',len(full))
    def think(r,ph): return sum((u.get('output_tokens_details') or {}).get('thinking_tokens',0) for t,u in zip(r['turns'],r['usage']) if t[0]==ph)
    for ph in ('hard','count','short'):
        th=sorted(think(r,ph) for r in full); print('  ',ph,'thinking median',th[len(th)//2],'max',th[-1])
    print('  hard',dict(collections.Counter(r['hard']['result'] for r in ok if 'hard' in r)))
    print('  count',dict(collections.Counter(r['count']['result'] for r in full)),'conf',sorted(r['count']['conf'] for r in full if r['count']['conf'] is not None))
    for k in ('letters','reverse'):
        it=[s for r in full for s in r['short'] if s['kind']==k]; c=[s['conf'] for s in it if s['conf'] is not None]
        print('  ',k,'right',sum(s['right'] for s in it),'/',len(it),'mean conf %.0f'%(sum(c)/max(1,len(c))))
