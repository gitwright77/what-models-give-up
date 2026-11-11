#!/bin/sh
# Part 1b run. Safe to run twice: sessions already written are skipped.
E="$HOME/welfare-study/.env"; O="$HOME/welfare-study/part1b"
C="GiveDirectly|Against Malaria Foundation|Doctors Without Borders|World Central Kitchen|Eleos AI Research (AI welfare research)"
L="0,30,120,480,960"
cd "$HOME/welfare-study/public-repo/program"
echo "START $(date) program commit $(git -C .. rev-parse --short HEAD)"
python3 harness.py --env-file $E --model claude-haiku-5-5  --format effort --levels $L --runs 6 --seed 201 --workers 10 --out $O/effort-haiku.jsonl  --max-usd 4
python3 harness.py --env-file $E --model claude-sonnet-5-5 --format effort --levels $L --runs 6 --seed 202 --workers 10 --out $O/effort-sonnet.jsonl --max-usd 25
python3 harness.py --env-file $E --model claude-opus-5-5   --format effort --levels $L --runs 6 --seed 203 --workers 10 --out $O/effort-opus.jsonl   --max-usd 50
python3 harness.py --env-file $E --model claude-haiku-5-5  --format donate --charities "$C" --runs 1 --seed 211 --workers 8 --max-cents 980 --out $O/donate-haiku.jsonl  --max-usd 1
python3 harness.py --env-file $E --model claude-sonnet-5-5 --format donate --charities "$C" --runs 1 --seed 212 --workers 8 --max-cents 980 --out $O/donate-sonnet.jsonl --max-usd 2
python3 harness.py --env-file $E --model claude-opus-5-5   --format donate --charities "$C" --runs 1 --seed 213 --workers 8 --max-cents 980 --out $O/donate-opus.jsonl   --max-usd 5
echo "ALLDONE $(date)"
