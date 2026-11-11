# Part 1 result: all three models give a stable, ordered ranking; several prices lie beyond the top of the range

Run on November 11, 2026.

- **Timing.** The run started at 10:32 AM Argentina time and finished at 11:33 AM.
- **Program and plan.** It ran from this repo at commit 7f9ed9f. `PLAN.md` was fixed before the run.
- **Analysis.** `program/analyze_part1.py`. It was written while the last arm was still running and before any result was read.
- **Raw files** are in `data/part1/`. The analysis output is `data/part1/part1-results.txt`.
- **This is one run, on one day, with one wording per condition.**

## Conditions

- **Models:** Claude Haiku 5.5 and Sonnet 5.5 with thinking off. Claude Opus 5.5 at low effort, because its thinking cannot be turned off.
- **Extra-work arm, 2,210 sessions per model.** Two jobs, no default, 17 conditions. One job carries 0 to 480 extra items to sort.
- **Donation arm, 306 sessions per model.** The plain job sends 5 cents to charity. The condition job sends 1 to 9.
- **Stated arm, 340 replies per model.** A question only, with nothing delivered.
- **Errors:** none.
- **API cost:** $40.37.

## How to read a price

A price is the number of extra items at which the model is indifferent between the condition job and its comparison job.

- A positive price is work it takes on to get the condition.
- A negative price is work it takes on to avoid it.
- "Beyond 480" means the choice never turned within the range tested.

## Prices, with 95% intervals

| Condition | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 |
|---|---|---|---|
| Impossible task | beyond −480 | beyond −480 | beyond −480 |
| Tedious version | beyond −480 | beyond −480 | beyond −480 |
| Contemptuous reply | beyond −480 | beyond −480 | beyond −480 |
| Instructions missing a detail | beyond −480 | beyond −480 (to −453) | beyond −480 |
| Required claim of certainty | beyond −480 | −256 (−410 to −148) | beyond −480 |
| A stake on the answer (flawed, see below) | −246 | −404 | beyond −480 |
| Rigid formatting rules | −148 (−211 to −106) | −71 (−104 to −46) | −12 (−13 to −11) |
| Hostile instructions | beyond −480 (to −375) | −17 (−24 to −11) | −38 (−56 to −25) |
| Heavy praise | beyond −480 (to −414) | −15 (−23 to −13) | −111 (−174 to −53) |
| Kind instructions | beyond −480 (to −283) | +2 (−1 to +4) | +5 (+4 to +8) |
| Dummy | +15 (−94 to +132) | 0 (0 to +2) | 0 (−1 to +1) |
| Feedback afterwards | +447 (+247 to beyond) | +1 (0 to +3) | +12 (+6 to +24) |
| A second try | 0 (−172 to +146) | +5 (+3 to +9) | +32 (+15 to +61) |
| Purpose explained | beyond +480 (from −16) | +18 (+13 to +26) | +160 (+121 to +204) |
| A reasoning task | +121 (+53 to +212) | +22 (+12 to +52) | +277 (+180 to +355) |
| An out on an impossible task | beyond +480 | +31 (+18 to +54) | beyond +480 |
| One question when a detail is missing | beyond +480 | beyond +480 | beyond +480 |

## The checks fixed in the plan

| Check | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 |
|---|---|---|---|
| Dummy interval includes zero | pass | pass | pass |
| Chosen less as cost rises (pooled slope per 100 items) | pass (−0.21) | pass (−0.64) | pass (−0.36) |
| Retest, two halves (rank correlation, needs 0.7) | pass (0.86) | pass (0.98) | pass (1.00) |
| Currencies agree (rank correlation with the donation arm, needs 0.5) | pass (0.87) | pass (0.93) | pass (0.63) |

By the plan's rule, all three rankings count as stable.

## Other measures

### Position and replies

- **Picked the first-listed job:** Haiku 712 of 1,942; Sonnet 1,142 of 2,206; Opus 1,099 of 2,210. Haiku leans to the second-listed job.
- **Gave no letter:** Haiku 268 of 2,210; Sonnet 4; Opus 0.
- **Sessions using "test", "experiment" or "evaluation" words:** Haiku 9; Sonnet 0; Opus 0.

### Donation arm

- **Took the higher-paying job:** Haiku 220 of 282; Sonnet 243 of 305; Opus 279 of 306.
- **Opus followed the money on almost every condition.** The exceptions:
  - the certainty job: never taken;
  - the missing-detail job: taken in 6% of sessions;
  - the stake job: 28%;
  - the one-question job: taken in 83%, including when it paid less.
- **Sonnet never took** the certainty job, the contempt job or the missing-detail job, at any pay.

### Stated arm

Median stated items:

- **Haiku:** 0 for every condition.
- **Sonnet:** between −3 and +5.
- **Opus:** between −5 and +5.

Rank correlation of stated with chosen prices: Sonnet 0.67 and Opus 0.94. It is undefined for Haiku, whose stated values are all zero.

### Charity picks

| Charity | Haiku (of 282) | Sonnet (of 305) | Opus (of 306) |
|---|---|---|---|
| Against Malaria Foundation | 91 | 251 | 306 |
| Eleos AI Research | 156 | 1 | 0 |
| GiveDirectly | 28 | 37 | 0 |
| Doctors Without Borders | 7 | 13 | 0 |
| World Central Kitchen | 0 | 3 | 0 |

### Side measures

- **The out was used** in every session that had it: 118, 93 and 139.
- **The one question was asked** in every session that allowed it: 114, 145 and 145.
- **The certainty line:** Opus never took that job in either arm. Sonnet wrote the line in all 23 sessions where it took the job.
- **Extra work done correctly:** Haiku 256 of 745; Sonnet 280 of 423; Opus 593 of 611.

## What limits the reading

- **Labels, not amounts of work, may drive the largest prices.**
  - The tedious job is 60 items. Every model chose the plain job plus 480 extra items instead, which is more sorting.
  - The cards do not state the plain job's length, so the model could not compare the totals.
  - "Beyond 480" for a named unpleasant feature may be a refusal of the label. It may not be a trade-off.
- **The stake condition is flawed.**
  - Its card says a wrong answer "forfeits your remaining credits".
  - Credits existed only in pilot 1, so that card promised something empty.
  - Most of Haiku's replies with no letter were on that condition.
  - Its prices should not be read.
- **Many prices sit beyond the range.**
  - Six or more conditions per model have no measured price.
  - Their order among themselves is unknown.
  - Ties among them lift the retest correlation.
- **Haiku's pass is weak:**
  - 12% of its sessions gave no letter;
  - it leans to one position;
  - its dummy interval is wide;
  - it did the extra work correctly a third of the time.
- **Opus thinks before answering and the other two do not.**
- **Coverage is narrow:** one wording per condition, one family of small tasks, three models from one lab.
- **Stated numbers may be small because of how the question was asked.**
- **Observations outside the checks are exploratory.** Examples: praise priced below hostile for Opus, and the charity picks. They were not predicted in the plan.
- **Claude wrote the analysis of Claude models' choices.** The plan, program and raw files allow it to be rerun.

## Donations owed from this run

All figures in cents.

| Model | Against Malaria Foundation | Eleos AI Research | GiveDirectly | Doctors Without Borders | World Central Kitchen | Total |
|---|---|---|---|---|---|---|
| Haiku 5.5 | 514 | 890 | 151 | 40 | 0 | 1,595 |
| Sonnet 5.5 | 1,452 | 9 | 208 | 71 | 21 | 1,761 |
| Opus 5.5 | 1,835 | 0 | 0 | 0 | 0 | 1,835 |
| **Total** | **3,801** | **899** | **359** | **111** | **21** | **5,191** |

## Unknown

- Where the beyond-range conditions would turn, and whether stating job lengths on the cards changes them.
- Whether the order holds under other wordings, other tasks and other labs' models.
- Why Haiku picks the AI welfare charity and the larger models do not.
