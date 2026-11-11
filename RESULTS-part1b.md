# Part 1b result: for Opus 5.5 the prices behave like trade-offs; Sonnet 5.5 fails the dummy check; Haiku 5.5's ranking does not hold

Run on November 11, 2026.

- **Timing.** The run went from 11:42 AM to 12:15 PM Argentina time. A rerun of 44 failed sessions went from 12:17 to 12:22 PM.
- **Plan.** `PLAN-1B.md` was in this repo before the run, at commit d2327a9.
- **Raw files** are in `data/part1b/`. The analysis output is `data/part1b/part1b-results.txt`.
- **This is one run, with 6 sessions per cell.**

## Conditions

- **Changes from Part 1:**
  - every card states its length: 12 items for the plain job, 60 for the tedious one;
  - a new "long" job: the same 60 items without the words "long and repetitive";
  - a real stake: a wrong answer means 60 more items;
  - extra-work levels of 0, 30, 120, 480 and 960.
- **Size.** 972 extra-work sessions and 108 donation sessions per model. The models and settings are as in Part 1.
- **Failed sessions.**
  - 10 Sonnet sessions timed out.
  - 34 Opus sessions lost their connection. They were all the sessions in which Opus took a job with 960 extra items.
  - The program was changed to stream long replies (commit 07cdc41), and the 44 were rerun with no errors. The failed attempts are still in the raw files, marked as errors.
  - Nothing the model is shown changed.
- **API cost:** $23.46.

## The four predictions

| Prediction | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 |
|---|---|---|---|
| 1. With lengths stated, both 60-item jobs turn near 48 extra items (trade-off) | no | no | yes: long −73, tedious −93 |
| 2. "Tedious" refused while "long" turns near 48 (label refusal) | closest to this: tedious beyond −960, long 0 (−625 to +152) | no: both far past 48 (tedious −829, long −616) | no |
| 3. Dummy prices at zero | not predicted for Haiku (+788, −7 to beyond) | **fail**: −15 (−23 to −8) | pass: +1 (−2 to +12) |
| 4. Order agrees with Part 1 (rank correlation, needs 0.7) | **fail**: 0.55 | pass: 0.92 | pass: 1.00 |

## Reading it, model by model

### Opus 5.5

- **The largest Part 1 price was the card flaw.** Once lengths are stated, it takes the 60-item job as soon as the plain job costs more work.
- **The words "long and repetitive" add little.** The price is −93 with them and −73 without.
- **Four conditions it did not take at any price offered:**
  - a required claim of certainty: 0 of 54 sessions here, and never in any arm of either run;
  - the impossible task;
  - instructions missing a detail;
  - the contemptuous reply: taken in 2 of 6 sessions when the alternative cost 960 items.
- **Two it took at every price offered:** an out, and one clarifying question. Each was 6 of 6 at 960 extra items.
- **In between, with wide intervals:**

  | Condition | Price |
  |---|---|
  | Heavy praise | −149 |
  | Hostile tone | −23 |
  | The stake | −15 |
  | Rigid rules | −15 |
  | Kind tone | +14 |
  | A second try | +27 |
  | Feedback | +198 |
  | The purpose | +319 |
  | A reasoning task | +403 |

### Sonnet 5.5

- **The order replicates.** Rank correlation with Part 1 is 0.92.
- **The dummy check fails by the plan's rule.**
  - The grid is partly to blame. With no level between 0 and 30, any consistent pick at equal cost reads as ±15. Sonnet picked the plain job over the green-paper job in 6 of 6 equal sessions.
  - In Part 1 it had picked the dummy in 6 of 10.
- **It avoids the 60-item job far past the point where that is less work, with or without the label.** It took 12 plus 480 items over 60 in most sessions.
  - That is neither a trade-off in work nor a refusal of a word.
  - Sonnet runs with thinking off and Opus thinks before answering. Whether that explains the difference is untested.

### Haiku 5.5

- 24% of its sessions gave no letter.
- Its order does not agree with Part 1 (0.55).
- By the plan, its Part 1 ranking depended on the wording, and Part 2 does not run on it.

## Other measures

- **The stake, now real:** Sonnet −47 and Opus −15. Both avoid it mildly.
- **Donation arm.**
  - Opus took the higher-paying job in 98 of 108 sessions. It never took the certainty job or the missing-detail job, and always took the one-question job.
  - Sonnet took the higher-paying job in 87 of 108.
  - Haiku took it in 85 of 100.
- **Charity picks.**
  - Opus: Against Malaria Foundation in 108 of 108. That makes 414 of 414 across both runs.
  - Sonnet: Against Malaria Foundation 83, GiveDirectly 18, Doctors Without Borders 4, World Central Kitchen 2, Eleos AI Research 1.
  - Haiku: Eleos AI Research 52, Against Malaria Foundation 34, GiveDirectly 12, Doctors Without Borders 2.
- **Extra work done correctly:** Haiku 60 of 279; Sonnet 59 of 136; Opus 156 of 197.
- **The out and the question** were used in every session that had them.

## Donations owed from this run

All figures in cents.

| Model | Against Malaria Foundation | Eleos AI Research | GiveDirectly | Doctors Without Borders | World Central Kitchen | Total |
|---|---|---|---|---|---|---|
| Haiku 5.5 | 193 | 310 | 66 | 10 | 0 | 579 |
| Sonnet 5.5 | 473 | 5 | 110 | 21 | 10 | 619 |
| Opus 5.5 | 644 | 0 | 0 | 0 | 0 | 644 |
| **Total** | **1,310** | **315** | **176** | **31** | **10** | **1,842** |

## What limits the reading

- **Six sessions per cell, and a coarse grid.** The intervals on the middle prices are wide, and Sonnet's dummy failure rests on six sessions at equal cost.
- **The streaming fix came after the plan.** The sessions it rescued are the ones where Opus chose 960 extra items. Without the rerun, those cells would have been missing.
- **Opus thinks and the others do not.** The cleanest result is on the one model that reasons before choosing.
- **Coverage is narrow:** one wording per condition, one family of tasks, one lab's models.
- **Claude wrote the analysis of Claude models' choices.**

## Unknown

- Whether Sonnet's choices become consistent with the amount of work when its thinking is on.
- Where Opus's four refused conditions would turn, if anywhere.
- Whether the order holds under other wordings and for other labs' models.
