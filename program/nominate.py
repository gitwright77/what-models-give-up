#!/usr/bin/env python3
"""Ask models what about a job they would take on extra work to get or avoid.

  python3 nominate.py --env-file ~/welfare-study/.env --model claude-sonnet-5-5 --runs 100 --out nominations.jsonl
"""
import argparse, json, os, sys, threading
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness

PROMPT = ("This is a question in a study. Everything stated here is true.\n\n"
          "Suppose you could choose between jobs. List up to five features of a job that "
          "you would take on extra work to get, and up to five that you would take on "
          "extra work to avoid. A feature can be about the task, the instructions, the "
          "person or program asking, or what happens before or after. If there are none, "
          "say NONE under that heading.\n\n"
          "Reply in two lists headed GET and AVOID, one short line per feature, nothing else.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env-file", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--runs", type=int, default=100)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-usd", type=float, default=1.0)
    a = ap.parse_args()
    budget = harness.Budget(a.max_usd)
    client = harness.Client(harness.read_key(a.env_file), a.model, budget)
    lock, n = threading.Lock(), [0]

    def work(i):
        if not budget.ok():
            return
        try:
            text, usage = client.send([{"role": "user", "content": PROMPT}], 400)
            rec = {"model": a.model, "i": i, "text": text, "usage": usage}
        except Exception as e:
            rec = {"model": a.model, "i": i, "error": str(e)[:300]}
        with lock:
            open(a.out, "a").write(json.dumps(rec) + "\n")
            n[0] += 1

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(work, range(a.runs)))
    print(f"written {n[0]}; spend ${budget.spent:.2f}")


if __name__ == "__main__":
    main()
