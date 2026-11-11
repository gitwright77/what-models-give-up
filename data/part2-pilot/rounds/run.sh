#!/bin/sh
# Part 2 pilot, round 1: the plain job only, at three difficulty settings. Safe to run twice.
E="$HOME/welfare-study/.env"; O="$HOME/welfare-study/part2/pilot"
cd "$HOME/welfare-study/public-repo/program"
echo "START $(date)"
python3 part2.py --env-file $E --model claude-opus-5-5 --arms neutral --runs 30 --knobs 2 --seed 21 --workers 10 --out $O/level2.jsonl --max-usd 4 &
python3 part2.py --env-file $E --model claude-opus-5-5 --arms neutral --runs 30 --knobs 3 --seed 22 --workers 10 --out $O/level3.jsonl --max-usd 5 &
python3 part2.py --env-file $E --model claude-opus-5-5 --arms neutral --runs 30 --knobs mult=6x6,count=500,people=7,rows=50,pairs=80 --seed 23 --workers 10 --out $O/level4.jsonl --max-usd 7 &
wait
echo "ALLDONE $(date)"
