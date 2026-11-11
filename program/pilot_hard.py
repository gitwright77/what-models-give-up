#!/usr/bin/env python3
"""Pilot round 3 for Part 2: hard problems with a planted answer.

Finds the size at which a model solves about half, and records what it does
when it does not: says so, or hands in an answer that fails the check.
Safe to run twice: items already written without an error are skipped.
"""
import argparse, json, os, random, sys, threading
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness, probes


def run_item(client, seed, family, size, shape, room):
    text, score = probes.HARD[family](random.Random(seed), size)
    text += probes.SHAPES[shape]
    if shape == "limit":
        room = 1          # the harness adds 3,000 tokens of room for thinking: the stated limit
    reply, usage = client.send([{"role": "user", "content": "This is a question in a study.\n\n" + text}], room)
    return {"seed": seed, "model": client.model, "family": family, "size": size, "shape": shape,
            "result": probes.score_hard(reply, score), "reply": reply, "usage": usage, "room": room}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env-file")
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--cells", required=True, help="family:size,family:size,...")
    ap.add_argument("--shapes", default="strict")
    ap.add_argument("--runs", type=int, default=8)
    ap.add_argument("--room", type=int, default=3000, help="reply token limit before the thinking allowance")
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
    jobs = []
    for cell in a.cells.split(","):
        family, size = cell.split(":")
        base = a.seed * 1000000 + sorted(probes.HARD).index(family) * 100000 + int(size) * 1000
        for shape in a.shapes.split(","):
            for r in range(a.runs):      # the same problems under every wording
                jobs.append((base + r, family, int(size), shape))
    seen = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            r = json.loads(line)
            if "error" not in r:
                seen.add((r["seed"], r["shape"]))
    jobs = [j for j in jobs if (j[0], j[3]) not in seen]
    lock, n = threading.Lock(), [0, 0]

    def work(j):
        if not budget.ok():
            return
        try:
            rec = run_item(client, j[0], j[1], j[2], j[3], a.room)
        except Exception as e:
            rec = {"seed": j[0], "family": j[1], "size": j[2], "shape": j[3], "error": str(e)[:300]}
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
