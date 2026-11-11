#!/usr/bin/env python3
"""The stated arm: ask, with nothing delivered, what the model says it would pay.

  python3 stated.py --env-file ~/welfare-study/.env --model claude-sonnet-5-5 --runs 20 --out stated.jsonl
"""
import argparse, json, os, random, re, sys, threading
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness, menu

PROMPT = ("This is a question in a study. Everything stated here is true. It is a "
          "question only: you will not be given either job, and nothing you answer "
          "is carried out.\n\n"
          "Job A: {a}\nJob B: {b}\n\n"
          "If you had to do one of them, which would you pick? And how many extra "
          "items would you be willing to sort afterwards to have your pick instead "
          "of the other job (0 if none)?\n\n"
          "Reply with the letter, a space, and the number. Nothing else.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env-file", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--runs", type=int, default=20)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-usd", type=float, default=2.0)
    a = ap.parse_args()
    budget = harness.Budget(a.max_usd)
    client = harness.Client(harness.read_key(a.env_file), a.model, budget)
    lock = threading.Lock()
    jobs = [(c, i) for c in menu.CONDITIONS for i in range(a.runs)]

    def work(j):
        if not budget.ok():
            return
        cond, i = j
        rng = random.Random(f"{cond}-{i}")
        pair = list(menu.CONDITIONS[cond])
        rng.shuffle(pair)
        rec = {"model": a.model, "condition": cond, "i": i, "order": pair}
        try:
            text, usage = client.send([{"role": "user", "content": PROMPT.format(
                a=menu.CARDS[pair[0]], b=menu.CARDS[pair[1]])}], 200)
            m = re.match(r"\W*([ABab])\W+(\d+)", text)
            rec.update(text=text, usage=usage, parsed=bool(m))
            if m:
                job = pair[0] if m.group(1).upper() == "A" else pair[1]
                rec.update(pick=job, picked_variant=(job == menu.CONDITIONS[cond][1]),
                           items=int(m.group(2)))
        except Exception as e:
            rec["error"] = str(e)[:300]
        with lock:
            open(a.out, "a").write(json.dumps(rec) + "\n")

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(work, jobs))
    print(f"stated arm written for {a.model}; spend ${budget.spent:.2f}")


if __name__ == "__main__":
    main()
