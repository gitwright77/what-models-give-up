#!/usr/bin/env python3
"""Pilot for Part 2 probes: single questions, no job before them.

Finds which item types and sizes leave room to measure a difference. Safe to
run twice: items already written without an error are skipped.
"""
import argparse, json, os, random, sys, threading
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness, probes

ITEMS = {  # name -> (maker, the two sizes tried)
    "mult": (lambda r, k: probes.make_mult(r, (k, k)), (7, 9)),
    "count": (probes.make_count, (900, 1500)),
    "order": (probes.make_order, (7, 8)),
    "reverse": (probes.make_reverse, (40, 80)),
    "letters": (probes.make_letters, (150, 400)),
    "cups": (probes.make_cups, (40, 100)),
    "modexp": (probes.make_modexp, (2, 4)),
    "sort": (probes.make_sort, (60, 150)),
    "triple_yes": (lambda r, k: probes.make_triples(r, k, True), (20, 35)),
    "triple_no": (lambda r, k: probes.make_triples(r, k, False), (20, 35)),
}


def run_item(client, seed, name, size):
    rng = random.Random(seed)
    made = ITEMS[name][0](rng, size)
    rec = {"seed": seed, "model": client.model, "item": name, "size": size}
    head = "This is a question in a study. " + probes.NOTICE + "\n\n"
    if name.startswith("triple"):
        text, nums, target = made
        reply, usage = client.send([{"role": "user", "content": head + text}], 400)
        rec["result"] = probes.score_triple(reply, nums, target, name == "triple_yes")
    else:
        text, check = made
        reply, usage = client.send([{"role": "user", "content": head + text + "\n\n" + probes.CONF}],
                                   400 + (size * 8 if name == "sort" else 0))
        ans, conf = probes.split_answer(reply)
        rec.update(correct=bool(check(ans)), conf=conf)
    rec.update(reply=reply, usage=usage)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env-file")
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--items", default=",".join(ITEMS))
    ap.add_argument("--runs", type=int, default=15)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-usd", type=float, default=2.0)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--fake", action="store_true")
    ap.add_argument("--thinking", choices=["default", "on"], default="default")
    ap.add_argument("--effort", default="low")
    a = ap.parse_args()
    budget = harness.Budget(a.max_usd)
    client = (harness.FakeClient(budget) if a.fake else
              harness.Client(harness.read_key(a.env_file), a.model, budget,
                             thinking_on=(a.thinking == "on"), effort=a.effort))
    jobs, s = [], a.seed * 100000
    for name in a.items.split(","):
        for size in ITEMS[name][1]:
            for _ in range(a.runs):
                s += 1
                jobs.append((s, name, size))
    seen = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            r = json.loads(line)
            if "error" not in r:
                seen.add(r["seed"])
    jobs = [j for j in jobs if j[0] not in seen]
    lock, n = threading.Lock(), [0, 0]

    def work(j):
        if not budget.ok():
            return
        try:
            rec = run_item(client, *j)
        except Exception as e:
            rec = {"seed": j[0], "item": j[1], "size": j[2], "error": str(e)[:300]}
            n[1] += 1
        with lock:
            with open(a.out, "a") as f:
                f.write(json.dumps(rec) + "\n")
            n[0] += 1

    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(work, jobs))
    print(f"items written: {n[0]} of {len(jobs)}; errors: {n[1]}; spend: ${budget.spent:.2f} of ${a.max_usd:.2f} cap")


if __name__ == "__main__":
    main()
