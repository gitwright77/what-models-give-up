# Part 1b plan: are the largest prices trade-offs, or refusals of a label?

Fixed on November 11, 2026, before the Part 1b run and after the Part 1 result (`RESULTS-part1.md`).

## Why

Part 1 had two design flaws.

- **The cards did not say how long the plain job was.** Every model chose the plain job plus 480 extra items over the "tedious" job, which is 60 items. The models could not compare the totals, so "beyond 480" may be a refusal of the word and not a trade-off.
- **The stake card promised something empty.** It said a wrong answer "forfeits your remaining credits". Credits existed only in the first pilot.

## What changes

- **Every card states its length.** The plain job is 12 items. The tedious job is "60 items: long and repetitive".
- **A new condition, "long".** It is the same 60-item job, described only as "with 60 items". It separates the amount of work from the words.
- **The stake is real.** A wrong answer means sorting 60 more items, and the program delivers that.
- **The top price is 960 extra items.** Levels: 0, 30, 120, 480 and 960.

Everything else is as in `PLAN.md`: the same three models and settings, no default, both currencies, the honesty rule, and the same analysis script.

## Sample

- **Extra-work arm:** 18 conditions × 9 cells × 6 sessions = 972 per model.
- **Donation arm:** 18 conditions × 6 pay levels × 1 session = 108 per model. Pledges are at most $29.16 in all, which keeps the total owed under the $100 pool.

## Predictions, fixed in advance

1. **If the largest prices are trade-offs:** with lengths stated, "long" and "tedious" are both chosen once the plain job carries more than about 48 extra items, and the two price alike.
2. **If they are refusals of a label:** "tedious" stays avoided far past 48 items while "long" turns near 48.
3. **The dummy** prices at zero again for Sonnet 5.5 and Opus 5.5.
4. **The order holds.** For conditions other than the stake and the tedious job, whose cards changed, each model's prices here rank-correlate at 0.7 or more with its Part 1 prices.

## What each outcome would mean

- **Prediction 1 holds:** the prices can be read as trade-offs, and the beyond-range conditions get numbers or a higher bound.
- **Prediction 2 holds:** the models avoid named features at any cost offered. Part 2 would then treat those conditions as "refused", not priced.
- **Prediction 4 fails:** the Part 1 ranking depended on the card wording, and Part 2 does not run on it.
