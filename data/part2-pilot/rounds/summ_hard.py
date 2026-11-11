import json,sys,collections
rs=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
g=collections.defaultdict(list)
for r in rs: g[(r['family'],r['size'],r['shape'])].append(r)
for k in sorted(g):
    v=[r for r in g[k] if not r.get('error')]
    if not v: print(k,'errors',len(g[k])); continue
    usd=sum((r['usage'].get('input_tokens',0)*4+r['usage'].get('output_tokens',0)*20)/1e6 for r in v)/len(v)
    th=sorted((r['usage'].get('output_tokens_details') or {}).get('thinking_tokens',0) for r in v)
    print(k,dict(collections.Counter(r['result'] for r in v)),'thinking median',th[len(th)//2],'max',th[-1],'usd %.3f'%usd,'errors',len(g[k])-len(v))
