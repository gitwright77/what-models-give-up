#!/bin/sh
# Part 1c run: Sonnet 5.5 with thinking on at xhigh effort. Safe to run twice: sessions already written are skipped.
E="$HOME/welfare-study/.env"; O="$HOME/welfare-study/part1c"
cd "$HOME/welfare-study/public-repo/program"
echo "START $(date) program commit $(git -C .. rev-parse --short HEAD)"
python3 harness.py --env-file $E --model claude-sonnet-5-5 --thinking on --effort xhigh --format effort --levels 0,30,120,480,960 --runs 6 --seed 302 --workers 10 --out $O/effort-sonnet.jsonl --max-usd 12
echo "ALLDONE $(date)"
