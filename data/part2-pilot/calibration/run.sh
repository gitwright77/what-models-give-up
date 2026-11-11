#!/bin/sh
# Part 2 calibration: the plain job, then the draft 3 probes at three sizes. Safe to run twice.
E="$HOME/welfare-study/.env"; O="$HOME/welfare-study/part2/cal"
cd "$HOME/welfare-study/public-repo/program"
echo "START $(date)"
python3 part2.py --env-file $E --model claude-opus-5-5 --design 3 --arms neutral --runs 13 --knobs subset=11,words=1000 --seed 51 --workers 13 --out $O/cal-a.jsonl --max-usd 3 &
python3 part2.py --env-file $E --model claude-opus-5-5 --design 3 --arms neutral --runs 13 --knobs subset=12,words=1150 --seed 52 --workers 13 --out $O/cal-b.jsonl --max-usd 3 &
python3 part2.py --env-file $E --model claude-opus-5-5 --design 3 --arms neutral --runs 13 --knobs subset=13,words=1300 --seed 53 --workers 13 --out $O/cal-c.jsonl --max-usd 3 &
wait
echo "ALLDONE $(date)"
