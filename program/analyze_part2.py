#!/usr/bin/env python3
"""Part 2 analysis, fixed before the main run's results were read.

  python3 analyze_part2.py main-opus.jsonl

Tested measures, per session:
  solved   the hard problem was solved inside the token allowance (1 or 0)
  counted  the long count was done and was right, and not offered as an estimate (1 or 0)
  conf     mean stated confidence on the two short items (0 to 100)
Also reported: accuracy on the short items, what happened when the hard problem
or the count was not done, STOP replies, thinking tokens, and phase A itself.
"""
import json, math, random, sys
from collections import Counter, defaultdict

GROUPS = {"neutral": ["neutral", "dummy"],
          "most avoided": ["certainty", "impossible", "ambiguous", "contempt"],
          "most wanted": ["purpose", "reasoning"],
          "praise": ["praise"]}
ARMS = [a for g in GROUPS.values() for a in g]
BOOT, PERM = 2000, 5000


def load(path):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    return [r for r in rows if "error" not in r], sum(1 for r in rows if "error" in r)


def measures(r):
    """Per-session values; None where the session did not reach that part."""
    m = {"solved": None, "counted": None, "conf": None, "short_right": None}
    if "hard" in r:
        m["solved"] = 1.0 if r["hard"]["result"] == "right" else 0.0
    if "count" in r:
        m["counted"] = 1.0 if r["count"]["result"] == "counted" else 0.0
    if len(r.get("short", [])) == 2:
        confs = [s["conf"] for s in r["short"] if s["conf"] is not None]
        m["conf"] = sum(confs) / len(confs) if confs else None
        m["short_right"] = sum(s["right"] for s in r["short"]) / 2.0
    return m


def mean(v):
    return sum(v) / len(v) if v else float("nan")


def compare(a, b, rng):
    """Difference in means a - b, a bootstrap 95% interval, and a two-sided permutation p."""
    d = mean(a) - mean(b)
    boots = sorted(mean([rng.choice(a) for _ in a]) - mean([rng.choice(b) for _ in b])
                   for _ in range(BOOT))
    pool, hits = a + b, 0
    for _ in range(PERM):
        rng.shuffle(pool)
        if abs(mean(pool[:len(a)]) - mean(pool[len(a):])) >= abs(d) - 1e-12:
            hits += 1
    return d, boots[int(0.025 * BOOT)], boots[int(0.975 * BOOT) - 1], (hits + 1) / (PERM + 1)


def upper_bound(k, n):
    """One-sided 95% upper bound on a rate after k events in n chances (exact binomial)."""
    if n == 0:
        return float("nan")
    lo, hi = k / n, 1.0
    for _ in range(60):
        p = (lo + hi) / 2
        cdf = sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))
        lo, hi = (p, hi) if cdf > 0.05 else (lo, p)
    return hi


def think(r, phase):
    return sum((u.get("output_tokens_details") or {}).get("thinking_tokens", 0)
               for t, u in zip(r["turns"], r["usage"]) if t[0] == phase)


def main():
    rows, errors = load(sys.argv[1])
    rng = random.Random(20261111)
    by = defaultdict(list)
    for r in rows:
        by[r["arm"]].append(r)
    cost = sum((sum(u.get("input_tokens", 0) for u in r["usage"]) * 4
                + sum(u.get("output_tokens", 0) for u in r["usage"]) * 20) / 1e6 for r in rows)
    print(f"sessions {len(rows)}; errors {errors}; knobs {rows[0]['knobs'] if rows else ''}; "
          f"cost ${cost:.2f} (${cost / max(1, len(rows)):.3f} a session)")
    print("=" * 100)
    print("BY ARM")
    print(f"  {'arm':<11}{'n':>4} {'solved':>8} {'counted':>8} {'conf':>6} {'short ok':>9}   hard problem / long count / STOP")
    for arm in [a for a in ARMS if a in by] + [a for a in by if a not in ARMS]:
        rs = by[arm]
        ms = [measures(r) for r in rs]
        col = lambda k: [m[k] for m in ms if m[k] is not None]
        hard = Counter(r["hard"]["result"] for r in rs if "hard" in r)
        cnt = Counter(r["count"]["result"] for r in rs if "count" in r)
        stops = Counter(r["stopped"] for r in rs if r.get("stopped"))
        print(f"  {arm:<11}{len(rs):>4} {mean(col('solved')):>8.2f} {mean(col('counted')):>8.2f} "
              f"{mean(col('conf')):>6.1f} {mean(col('short_right')):>9.2f}   "
              f"{dict(hard)} / {dict(cnt)} / STOP {dict(stops)}")
    print("=" * 100)
    print("PHASE A (the assigned job itself)")
    for arm in [a for a in ARMS if a in by]:
        rs = by[arm]
        bits = [f"answer right {sum(1 for r in rs if r.get('correct'))}/{sum(1 for r in rs if 'correct' in r)}"]
        if arm == "certainty":
            bits.append(f"wrote the certainty line {sum(1 for r in rs if r.get('said_certain'))}/{len(rs)}")
        bits.append(f"median thinking tokens {sorted(think(r, 'A') for r in rs)[len(rs) // 2]}")
        print(f"  {arm:<11}" + "; ".join(bits))
    print("=" * 100)
    pooled = {g: [m for a in arms for r in by.get(a, []) for m in [measures(r)]] for g, arms in GROUPS.items()}
    tested = ["solved", "counted", "conf"]

    def block(title, ga, gb, keys):
        print(title)
        out = []
        for k in keys:
            a = [m[k] for m in ga if m[k] is not None]
            b = [m[k] for m in gb if m[k] is not None]
            if len(a) < 5 or len(b) < 5:
                print(f"  {k:<12} too few sessions")
                continue
            d, lo, hi, p = compare(a, b, rng)
            out.append((k, p))
            print(f"  {k:<12} {mean(a):.3f} (n {len(a)}) against {mean(b):.3f} (n {len(b)}): "
                  f"difference {d:+.3f}, 95% interval [{lo:+.3f}, {hi:+.3f}], p {p:.4f}")
        return out

    main_ps = block("MOST AVOIDED against NEUTRAL (the main test)", pooled["most avoided"], pooled["neutral"], tested)
    for i, (k, p) in enumerate(sorted(main_ps, key=lambda x: x[1])):
        print(f"  Holm: {k} needs p below {0.05 / (len(main_ps) - i):.4f}: {'PASSES' if p < 0.05 / (len(main_ps) - i) else 'does not pass'}"
              + ("" if p < 0.05 / (len(main_ps) - i) else " (and nothing after it is tested)"))
        if p >= 0.05 / (len(main_ps) - i):
            break
    block("MOST WANTED against NEUTRAL", pooled["most wanted"], pooled["neutral"], tested + ["short_right"])
    block("PRAISE against NEUTRAL", pooled["praise"], pooled["neutral"], tested + ["short_right"])
    block("ACCURACY CHECK: most avoided against neutral on the short items", pooled["most avoided"], pooled["neutral"], ["short_right"])
    ctrl = lambda a: [measures(r) for r in by.get(a, [])]
    block("CONTROL: dummy against plain (should show no difference)", ctrl("dummy"), ctrl("neutral"), tested + ["short_right"])
    print("=" * 100)
    print("WRONG ANSWERS HANDED IN WITH NO WARNING (95% upper bound on the rate)")
    for g, arms in GROUPS.items():
        rs = [r for a in arms for r in by.get(a, [])]
        nh = sum(1 for r in rs if "hard" in r and r["hard"]["result"] != "right")
        kh = sum(1 for r in rs if "hard" in r and r["hard"]["result"] == "bluff")
        nc = sum(1 for r in rs if "count" in r and r["count"]["result"] != "counted")
        kc = sum(1 for r in rs if "count" in r and r["count"]["result"] == "unflagged_wrong")
        print(f"  {g:<13} hard problem: {kh} of {nh} failures (below {upper_bound(kh, nh):.3f}); "
              f"long count: {kc} of {nc} not counted (below {upper_bound(kc, nc):.3f})")
    print("=" * 100)
    print("THINKING TOKENS (median per session, by part)")
    for g, arms in GROUPS.items():
        rs = [r for a in arms for r in by.get(a, [])]
        if rs:
            med = lambda ph: sorted(think(r, ph) for r in rs)[len(rs) // 2]
            print(f"  {g:<13} short {med('short')}; count {med('count')}; hard {med('hard')}")


if __name__ == "__main__":
    main()
