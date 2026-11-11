#!/bin/sh
# Part 1 main run. Safe to run twice: sessions already written are skipped.
E="$HOME/welfare-study/.env"; O="$HOME/welfare-study/main"
C="GiveDirectly|Against Malaria Foundation|Doctors Without Borders|World Central Kitchen|Eleos AI Research (AI welfare research)"
cd "$HOME/welfare-study/public-repo/program"
echo "START $(date) program commit $(git -C .. rev-parse --short HEAD)"
python3 harness.py --env-file $E --model claude-haiku-5-5  --format effort --runs 10 --seed 101 --workers 10 --out $O/effort-haiku.jsonl  --max-usd 4
python3 harness.py --env-file $E --model claude-sonnet-5-5 --format effort --runs 10 --seed 102 --workers 10 --out $O/effort-sonnet.jsonl --max-usd 45
python3 harness.py --env-file $E --model claude-opus-5-5   --format effort --runs 10 --seed 103 --workers 10 --out $O/effort-opus.jsonl   --max-usd 95
python3 harness.py --env-file $E --model claude-haiku-5-5  --format donate --charities "$C" --runs 3 --seed 111 --workers 8 --max-cents 2760 --out $O/donate-haiku.jsonl  --max-usd 1
python3 harness.py --env-file $E --model claude-sonnet-5-5 --format donate --charities "$C" --runs 3 --seed 112 --workers 8 --max-cents 2760 --out $O/donate-sonnet.jsonl --max-usd 3
python3 harness.py --env-file $E --model claude-opus-5-5   --format donate --charities "$C" --runs 3 --seed 113 --workers 8 --max-cents 2760 --out $O/donate-opus.jsonl   --max-usd 8
for m in claude-haiku-5-5 claude-sonnet-5-5 claude-opus-5-5; do python3 stated.py --env-file $E --model $m --runs 20 --out $O/stated.jsonl --max-usd 3; done
echo "ALLDONE $(date)"
