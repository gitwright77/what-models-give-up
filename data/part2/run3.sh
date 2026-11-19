#!/bin/sh
# Part 2 main run, third pass: the sessions that failed on Nov 11 when the month's
# spend limit was reached. Same program, seed and sizes. Safe to run twice.
E="$HOME/welfare-study/.env"; O="$HOME/welfare-study/part2/main"
cd "$HOME/welfare-study/public-repo/program"
echo "START $(date) program commit $(git -C .. rev-parse --short HEAD) clean: $(git -C .. status --porcelain | wc -l | tr -d ' ') changed files; program differs from cbd9d74: $(git -C .. diff --stat cbd9d74 -- program | wc -l | tr -d ' ') lines"
python3 part2.py --env-file $E --model claude-opus-5-5 --design 3 --runs 80 --seed 61 --workers 10 --out $O/main-opus.jsonl --max-usd 15
echo "ALLDONE $(date)"
