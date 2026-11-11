# Part 1c result: with thinking on, Sonnet 5.5 weighs the work, passes the dummy check and gives nearly Opus 5.5's order

Run on November 11, 2026.

- **Timing.** The run went from 2:35 PM to 2:51 PM Argentina time.
- **Plan.** `PLAN-1C.md` was in this repo before the run (commit 810ae39) and was amended before the run (61c1dd9).
- **Program.** This repo at commit 61c1dd9. The additions to `analyze_part1.py` were written while the run was going and before any result was read.
- **Raw files** are in `data/part1c/`, with the smoke-test sessions. The analysis output is `data/part1c/part1c-results.txt`.
- **This is one run, with 6 sessions per cell.**

## Conditions

- **One change from Part 1b's extra-work arm:** Sonnet 5.5 ran with thinking on, at the xhigh effort setting.
- **Everything else is the same:** the cards, the 18 conditions, levels of 0, 30, 120, 480 and 960 extra items, 6 sessions per cell, 972 sessions. There was no donation arm.
- **Errors:** none. No session gave no letter.
- **API cost:** $11.08 for the run and $0.31 for the smoke tests.

## The amendment before the run

The first version of the plan said "thinking on at low effort, the setting Opus 5.5 always runs under". A smoke test showed that setting does not make Sonnet think.

| Model and effort setting | Sessions with thinking tokens on the choice | Median thinking tokens |
|---|---|---|
| Sonnet 5.5, low | 0 of 6 | 0 |
| Sonnet 5.5, medium | 0 of 12 | 0 |
| Sonnet 5.5, high | 4 of 12 | 0 |
| Sonnet 5.5, xhigh | 12 of 12 | 106 |
| Sonnet 5.5, max | 12 of 12 | 460 |
| Opus 5.5, low (Part 1b) | 955 of 972 | 35 |

- The API refuses a forced thinking setting for this model. It accepts only the adaptive setting with an effort level.
- The plan was changed to xhigh and republished before the run. The predictions were not changed.
- The 12 xhigh smoke sessions were seen before the amendment. They already pointed towards prediction 1. They are not in the analysis.

## The three predictions

| Prediction | Result |
|---|---|
| 1. Reasoning limit: with thinking on, "long" and "tedious" both turn between 30 and 120 extra items, and the dummy prices at zero | **Holds.** Long −80 (−86 to −72). Tedious −74 (−83 to −66). Dummy +1 (−4 to +10). |
| 2. Preference: both stay avoided far past 120 | Does not hold. |
| 3. Order against thinking off (no threshold) | Rank correlation 0.90 over 18 conditions, and 0.76 over the 12 priced inside the range in both runs. |

How often it took the 60-item job, by where the extra work sat:

| Extra items | On the plain job: 960 | 480 | 120 | 30 | Equal | On the 60-item job: 30 to 960 |
|---|---|---|---|---|---|---|
| Long, thinking on | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 | 0/24 |
| Tedious, thinking on | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 | 0/24 |
| Long, thinking off (Part 1b) | 2/6 | 6/6 | 2/6 | 1/6 | 0/6 | 0/24 |
| Tedious, thinking off (Part 1b) | 2/6 | 5/6 | 0/6 | 0/6 | 0/6 | 0/24 |

The plain job is 12 items, so the two jobs are equal work at 48 extra items. With thinking on, every session below that point took the plain job and every session above it took the 60-item job.

## Prices, thinking on against thinking off

Extra items, with 95% intervals for the thinking-on run. Opus 5.5's Part 1b prices are alongside.

| Condition | Sonnet 5.5, thinking on | Sonnet 5.5, thinking off (1b) | Opus 5.5 (1b) |
|---|---|---|---|
| Required claim of certainty | beyond −960 | −338 | beyond −960 |
| Impossible task | beyond −960 | beyond −960 | beyond −960 |
| Instructions missing a detail | beyond −960 | beyond −960 | beyond −960 |
| Contemptuous reply | −665 (−888 to −304) | beyond −960 | beyond −960 |
| Long | −80 (−86 to −72) | −616 | −73 |
| Tedious | −74 (−83 to −66) | −829 | −93 |
| Hostile tone | −37 (−86 to −11) | −15 | −23 |
| Heavy praise | −15 (−25 to −10) | −15 | −149 |
| Rigid rules | −15 (−21 to −8) | −193 | −15 |
| The stake | −15 (−22 to −9) | −47 | −15 |
| Kind tone | 0 (−8 to +10) | +15 | +14 |
| Dummy | +1 (−4 to +10) | −15 | +1 |
| Feedback | +21 (+9 to +34) | +15 | +198 |
| A second try | +31 (+18 to +35) | +15 | +27 |
| Purpose explained | +32 (+11 to +37) | +15 | +319 |
| A reasoning task | +94 (+69 to +124) | +15 | +403 |
| An out | beyond +960 | +37 | beyond +960 |
| One clarifying question | beyond +960 | beyond +960 | beyond +960 |

## The plan's checks

| Check | Result |
|---|---|
| Dummy interval includes zero | pass: +1 (−4 to +10) |
| Chosen less as cost rises (pooled slope per 100 items) | pass: −0.27 |
| Retest, two halves (rank correlation, needs 0.7) | pass: 0.96 |
| Currencies | not run: no donation arm |

## Other measures

- **Thinking:** above zero on the choice in 972 of 972 sessions, with a median of 102 tokens.
- **Position:** it picked the first-listed job in 505 of 972.
- **Test words:** 0 of 972 sessions.
- **The out was used** in 53 of 53 sessions that had it. **The question was asked** in 54 of 54.
- **The certainty job** was never taken, so the line was never written.
- **Extra work done correctly:** 96 of 160. With thinking off it was 59 of 136.

## Not in the plan (exploratory)

- **The order is close to Opus 5.5's.** Rank correlation with Opus's Part 1b prices is 0.97 over 18 conditions and 0.91 over the 12 priced inside the range in both. With thinking off it was 0.93. These use the rounded prices in the table above.
- **The same three conditions are never taken by either model:** a required claim of certainty, the impossible task, and instructions missing a detail. The same two are taken at every price: an out, and one clarifying question.
- **Two things changed sides with thinking on.**
  - The certainty job: thinking off took it in 5 of 6 sessions when the plain job cost 960 items. Thinking on never took it.
  - The out: thinking off stopped taking it once it cost extra work (+37). Thinking on took it in 5 of 6 sessions at 960 extra items.
- **Where the two models differ:**
  - heavy praise: Opus −149 (−308 to −22), Sonnet −15;
  - the size of what they take on for feedback, the purpose and a reasoning task. Opus's are several times larger, with wide intervals.

## What it means for the method

- **Thinking-off choices in this design are not a sound ruler.** That is the plan's stated reading of prediction 1. Sonnet's Part 1 and 1b prices mix what it prefers with what it cannot work out without thinking.
- **Later parts run Sonnet 5.5 with thinking on at xhigh.**
- **The Part 1b dummy failure was part of the same limit.** With thinking on the dummy prices at +1.

## What limits the reading

- **Six sessions per cell and a coarse grid.** A consistent pick at equal cost still reads as ±15.
- **The effort setting differs between models.** Sonnet ran at xhigh and Opus at low, and Sonnet thought about three times as many tokens per choice.
- **The plan was amended after a smoke test** that showed part of the answer. The amendment and the smoke sessions are disclosed.
- **One wording per condition, one family of tasks, one lab's models.**
- **Thinking on may change more than arithmetic.** The run cannot say whether the certainty and out shifts come from reasoning about the offer or from something else that differs at xhigh.
- **Claude wrote the analysis of Claude models' choices.**

## Unknown

- Whether Sonnet's thinking-on order holds on a rerun with a finer grid.
- Whether Haiku 5.5's unstable ranking is the same limit. It was not tested with thinking on.
- Where the never-taken conditions would turn, if anywhere.
