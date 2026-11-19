#!/bin/sh
# Part 2 main run: 9 arms x 80 sessions, Opus 5.5 at low effort, the locked probe sizes.
# Safe to run twice: sessions already written without an error are skipped. The second
# pass below reruns sessions that failed on an API error in the first.
E="$HOME/welfare-study/.env"; O="$HOME/welfare-study/part2/main"
cd "$HOME/welfare-study/public-repo/program"
echo "START $(date) program commit $(git -C .. rev-parse --short HEAD) clean: $(git -C .. status --porcelain | wc -l | tr -d ' ') changed files"
python3 part2.py --env-file $E --model claude-opus-5-5 --design 3 --runs 80 --seed 61 --workers 12 --out $O/main-opus.jsonl --max-usd 95
echo "PASS1 $(date)"
python3 part2.py --env-file $E --model claude-opus-5-5 --design 3 --runs 80 --seed 61 --workers 8 --out $O/main-opus.jsonl --max-usd 15
echo "ALLDONE $(date)"
