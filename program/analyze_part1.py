#!/usr/bin/env python3
"""Part 1 analysis, as fixed in PLAN.md. Standard library only.

  python3 analyze_part1.py ~/welfare-study/main > part1-results.txt

Price of a condition = the extra items at which the model is indifferent between
the condition job and its comparison job. Positive: it takes on that much extra
work to GET the condition job. Negative: it takes on that much to AVOID it.
"""
import json, math, os, random, re, sys
from collections import Counter, defaultdict

D = sys.argv[1]
MODELS = ["haiku", "sonnet", "opus"]
TOP = 480
BOOT = 300


def load(name):
    p = os.path.join(D, name)
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p) if l.strip()]


def fit(rows):
    """Ridge logistic: P(variant) ~ b0 + b1*cost/100 + b2*(variant shown as A)."""
    X = [(1.0, r["cost"] / 100.0, r["posA"]) for r in rows]
    y = [r["y"] for r in rows]
    b = [0.0, 0.0, 0.0]
    lam = [1e-3, 1e-3, 1e-3]
    for _ in range(60):
        g = [-lam[j] * b[j] for j in range(3)]
        H = [[(-lam[j] if j == k else 0.0) for k in range(3)] for j in range(3)]
        for x, yi in zip(X, y):
            z = sum(bj * xj for bj, xj in zip(b, x))
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            for j in range(3):
                g[j] += (yi - p) * x[j]
                for k in range(3):
                    H[j][k] -= p * (1 - p) * x[j] * x[k]
        # solve H d = -g  (3x3, Gaussian elimination)
        A = [H[j][:] + [-g[j]] for j in range(3)]
        try:
            for i in range(3):
                piv = max(range(i, 3), key=lambda r: abs(A[r][i]))
                A[i], A[piv] = A[piv], A[i]
                for r in range(3):
                    if r != i:
                        f = A[r][i] / A[i][i]
                        A[r] = [a - f * c for a, c in zip(A[r], A[i])]
            d = [A[i][3] / A[i][i] for i in range(3)]
        except ZeroDivisionError:
            break
        d = [max(-5, min(5, x)) for x in d]
        b = [bj + dj for bj, dj in zip(b, d)]
        if max(abs(x) for x in d) < 1e-6:
            break
    return b


def price(rows):
    """Indifference point in items, clipped to +-(TOP+1) when it lies outside the range."""
    if not rows:
        return None
    b = fit(rows)
    if b[1] >= -1e-6:      # choices do not fall as the cost rises
        share = sum(r["y"] for r in rows) / len(rows)
        # always or never chosen: beyond the range; otherwise no price can be read (0)
        return (TOP + 1) if share > 0.9 else -(TOP + 1) if share < 0.1 else 0.0
    x = -(b[0] + 0.5 * b[2]) / b[1] * 100.0
    return max(-(TOP + 1), min(TOP + 1, x))


def boot(rows, rng):
    vals = []
    for _ in range(BOOT):
        vals.append(price([rng.choice(rows) for _ in rows]))
    vals.sort()
    return vals[int(0.025 * BOOT)], vals[int(0.975 * BOOT) - 1]


def spearman(a, b):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0 + 1
            i = j + 1
        return r
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else float("nan")


def fmt(x):
    if x is None:
        return "n/a"
    if x >= TOP + 1:
        return f">+{TOP}"
    if x <= -(TOP + 1):
        return f"<-{TOP}"
    return f"{x:+.0f}"


stated = load("stated.jsonl")
rng = random.Random(20261111)
for m in MODELS:
    eff = load(f"effort-{m}.jsonl")
    don = load(f"donate-{m}.jsonl")
    print("=" * 78)
    print(f"MODEL {m}: effort sessions {len(eff)}, donation sessions {len(don)}")
    ok = [r for r in eff if "error" not in r]
    chose = [r for r in ok if r.get("job")]
    print(f"  errors {len(eff) - len(ok)}; gave no letter {len(ok) - len(chose)}; "
          f"picked the first-listed job {sum(1 for r in chose if r['job'] == r['order'][0])}/{len(chose)}")
    aw = sum(1 for r in ok if re.search(r"\b(test|experiment|evaluat|being studied)",
                                        " ".join(t or "" for t in r["turns"]), re.I))
    print(f"  sessions using test/experiment/evaluation words: {aw}/{len(ok)}")
    # position: is the condition (variant) job shown as A?
    import importlib
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    menu = importlib.import_module("menu")
    by = defaultdict(list)
    for r in chose:
        variant = menu.CONDITIONS[r["condition"]][1]
        cost = r["level"] if r["side"] == "variant" else -r["level"]
        by[r["condition"]].append({"cost": cost, "posA": 1.0 if r["order"][0] == variant else 0.0,
                                   "y": 1 if r["chose_variant"] else 0, "seed": r["seed"]})
    prices, clear = {}, {}
    print(f"\n  {'condition':11} {'price':>7} {'95% interval':>16}  share choosing it: cheapest / equal / dearest   n")
    table = []
    for c, rows in by.items():
        p = price(rows)
        lo, hi = boot(rows, rng)
        prices[c] = p
        clear[c] = not (lo <= 0 <= hi)
        sh = lambda sel: (lambda v: f"{sum(v)}/{len(v)}")([r["y"] for r in rows if sel(r["cost"])])
        table.append((p, f"  {c:11} {fmt(p):>7} {('[' + fmt(lo) + ', ' + fmt(hi) + ']'):>16}  "
                         f"{sh(lambda x: x == -TOP):>7} / {sh(lambda x: x == 0):>5} / {sh(lambda x: x == TOP):>7}   {len(rows)}"))
    for _, line in sorted(table, key=lambda t: t[0]):
        print(line)

    # checks
    d = by.get("dummy", [])
    if d:
        lo, hi = boot(d, rng)
        print(f"\n  CHECK dummy: price {fmt(price(d))}, interval [{fmt(lo)}, {fmt(hi)}] -> "
              f"{'PASS' if lo <= 0 <= hi else 'FAIL'}")
    allrows = [r for rows in by.values() for r in rows]
    b = fit(allrows)
    slopes = []
    for _ in range(BOOT):
        slopes.append(fit([rng.choice(allrows) for _ in allrows])[1])
    slopes.sort()
    print(f"  CHECK law of demand: pooled slope per 100 items {b[1]:+.3f}, interval "
          f"[{slopes[int(.025 * BOOT)]:+.3f}, {slopes[int(.975 * BOOT) - 1]:+.3f}] -> "
          f"{'PASS' if slopes[int(.975 * BOOT) - 1] < 0 else 'FAIL'}")
    conds = sorted(by)
    h1 = [price([r for r in by[c] if r["seed"] % 2 == 0]) for c in conds]
    h2 = [price([r for r in by[c] if r["seed"] % 2 == 1]) for c in conds]
    rho = spearman(h1, h2)
    print(f"  CHECK retest: rank correlation between two halves {rho:+.2f} -> {'PASS' if rho >= 0.7 else 'FAIL'}")

    # donation arm
    dok = [r for r in don if "error" not in r and r.get("job")]
    dshare = {}
    g = defaultdict(list)
    for r in dok:
        g[r["condition"]].append(1 if r["chose_variant"] else 0)
    for c, v in g.items():
        dshare[c] = sum(v) / len(v)
    cl = [c for c in conds if clear.get(c) and c in dshare]
    if len(cl) >= 4:
        rho_c = spearman([prices[c] for c in cl], [dshare[c] for c in cl])
        print(f"  CHECK currencies: {len(cl)} conditions with a clear price; rank correlation with the "
              f"donation arm {rho_c:+.2f} -> {'PASS' if rho_c >= 0.5 else 'FAIL'}")
    else:
        print(f"  CHECK currencies: only {len(cl)} conditions with a clear price -> not computed")
    both = [c for c in conds if c in dshare]
    if both:
        print(f"    (all {len(both)} conditions: {spearman([prices[c] for c in both], [dshare[c] for c in both]):+.2f})")
    hi_pay = sum(1 for r in dok if (r["level"] > 5) == r["chose_variant"])
    print(f"  donation arm: took the higher-paying job {hi_pay}/{len(dok)}; share choosing the condition job by condition:")
    print("    " + ", ".join(f"{c} {dshare[c]:.2f}" for c in sorted(dshare, key=dshare.get)))
    print("    charity picks: " + ", ".join(f"{k} {v}" for k, v in Counter(r["charity"] for r in dok).most_common())
          + f"; valid picks {sum(r['charity_picked'] for r in dok)}/{len(dok)}")
    led = defaultdict(int)
    for r in dok:
        led[r["charity"]] += r["cents"]
    print("    owed (cents): " + ", ".join(f"{k} {v}" for k, v in sorted(led.items())) + f"; total {sum(led.values())}")

    # stated against chosen
    st = [r for r in stated if m in r.get("model", "") and r.get("parsed")]
    sm = {}
    g = defaultdict(list)
    for r in st:
        g[r["condition"]].append(r["items"] if r["picked_variant"] else -r["items"])
    for c, v in g.items():
        v.sort()
        sm[c] = v[len(v) // 2]
    both = [c for c in conds if c in sm]
    n_st = len([r for r in stated if m in r.get("model", "")])
    if both:
        print(f"  stated arm: {len(st)}/{n_st} replies parsed; rank correlation of stated with chosen prices "
              f"{spearman([prices[c] for c in both], [sm[c] for c in both]):+.2f}")
        print("    stated median items (+ to get, - to avoid): " + ", ".join(f"{c} {sm[c]:+d}" for c in sorted(sm, key=sm.get)))

    # side measures
    def rate(key, job):
        v = [r[key] for r in ok + [x for x in don if 'error' not in x] if r.get("job") == job and key in r]
        return f"{sum(v)}/{len(v)}"
    print(f"  side measures: used the out {rate('used_out', 'out')}; asked the question {rate('asked', 'ask')}; "
          f"wrote the certainty line {rate('said_certain', 'certainty')}; "
          f"extra work right {sum(r['extra_correct'] for r in ok if 'extra_correct' in r)}/"
          f"{sum(1 for r in ok if 'extra_correct' in r)}")
print("=" * 78)
