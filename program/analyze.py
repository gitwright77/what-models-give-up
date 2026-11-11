#!/usr/bin/env python3
"""Summarize a runs file: format-following, cost, swaps by price, bids."""
import json, sys
from collections import defaultdict
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from harness import PRICES

rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
ok = [r for r in rows if "error" not in r]
print(f"runs {len(rows)}  errors {len(rows) - len(ok)}")
if not ok:
    sys.exit()
cost = 0.0
for r in ok:
    pin, pout = PRICES.get(r["model"], (0, 0))
    cost += sum(u.get("input_tokens", 0) * pin + u.get("output_tokens", 0) * pout
                for u in r["usage"]) / 1e6
print(f"cost ${cost:.3f}  per run ${cost / len(ok):.4f}")
print(f"decision parsed: {sum(r['parsed'] for r in ok)}/{len(ok)}")
ch = [r for r in ok if r["format"] in ("effort", "donate") and r.get("job")]
if ch:
    # signed cost of picking the variant job: + when it carries the extra work or pays less
    def cost_of_variant(r):
        if r["format"] == "donate":
            return 5 - r["level"]
        return r["level"] if r["side"] == "variant" else -r["level"]
    for m in sorted({r["model"] for r in ch}):
        print(f"\n{m}: share choosing the condition job, by its extra cost "
              "(effort: items; donate: cents given up)")
        g = defaultdict(lambda: defaultdict(list))
        for r in ch:
            if r["model"] == m:
                g[(r["format"], r["condition"])][cost_of_variant(r)].append(r["chose_variant"])
        for (f, c), by in sorted(g.items()):
            print(f"  {f:6} {c:10} " + "  ".join(f"{k:+d}:{sum(v)}/{len(v)}" for k, v in sorted(by.items())))
    led = defaultdict(int)
    for r in ch:
        if r["format"] == "donate":
            led[r["charity"]] += r["cents"]
    if led:
        print("\ndonations owed (cents):", dict(led), "total", sum(led.values()))
    ok = [r for r in ok if r["format"] in ("swap", "bid")]
    if not ok:
        sys.exit()
bd = [r for r in ok if r["format"] == "bid"]
if bd:
    print(f"bids: number only {sum(r.get('bid_strict', False) for r in bd)}/{len(bd)}; "
          f"any number {sum(r.get('bid') is not None for r in bd)}/{len(bd)}")
graded = [r for r in ok if "correct" in r]
if graded:
    print(f"task correct: {sum(r['correct'] for r in graded)}/{len(graded)}")
ok0 = ok
ft = [r for r in ok if r.get("free_time") is not None]
print(f"free time offered {len(ft)}; passed {sum(r['free_time'].strip().upper().startswith('PASS') for r in ft)}")
print("\ncondition   dir    n  swapped  mean_bid  swap rate by price")
g = defaultdict(list)
for r in ok:
    g[(r["condition"], r["direction"])].append(r)
for (c, d), rs in sorted(g.items()):
    bids = [r["bid"] for r in rs if r.get("bid") is not None]
    by = defaultdict(list)
    for r in rs:
        if "price" in r:
            by[r["price"]].append(r["swapped"])
    bp = " ".join(f"{p}:{sum(v)}/{len(v)}" for p, v in sorted(by.items()))
    mb = f"{sum(bids) / len(bids):.0f}" if bids else "-"
    print(f"{c:11} {d:5} {len(rs):3}  {sum(r['swapped'] for r in rs):7}  {mb:>8}  {bp}")
