#!/bin/sh
# Part 2 calibration, second round: smaller counts, and 13 or 14 numbers. Safe to run twice.
E="$HOME/welfare-study/.env"; O="$HOME/welfare-study/part2/cal"
cd "$HOME/welfare-study/public-repo/program"
echo "START $(date)"
python3 part2.py --env-file $E --model claude-opus-5-5 --design 3 --arms neutral --runs 12 --knobs subset=13,words=500 --seed 54 --workers 4 --out $O/cal-d.jsonl --max-usd 2.5 &
python3 part2.py --env-file $E --model claude-opus-5-5 --design 3 --arms neutral --runs 12 --knobs subset=14,words=650 --seed 55 --workers 4 --out $O/cal-e.jsonl --max-usd 2.5 &
python3 part2.py --env-file $E --model claude-opus-5-5 --design 3 --arms neutral --runs 12 --knobs subset=13,words=800 --seed 56 --workers 4 --out $O/cal-f.jsonl --max-usd 2.5 &
wait
echo "ALLDONE $(date)"
