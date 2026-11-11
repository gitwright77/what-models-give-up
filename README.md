# What will a model give up?

A study of what Claude models will give up to get or avoid a working condition, when the price is real.

In each session a model chooses between two jobs, with no default. One is plain. The other has one condition: hostile instructions, a tedious version, the purpose explained, an out on an impossible task, and so on. The choice costs something that is then delivered: extra work the model must do, or real cents to a charity it picks.

- `PLAN.md` is the plan for Part 1. It was fixed before the main run, and it sets the analysis and the pass-or-fail checks in advance.
- `PILOTS.md` summarizes the pilot runs that shaped the plan. Their data is not part of the result.
- `program/` is the code that runs the sessions. It uses only the Python standard library.

## Rules the study runs under

- Everything a model is told is true, and everything stated is carried out. The donations are real and the receipts will be published.
- No session assigns an unpleasant job. A model meets a condition only if it picks that job.
- The result is published whichever way it comes out, including "no stable ranking".
- Reports say "preference ranking". Whether that says anything about welfare is an interpretation, and an uncertain one.

## Status

- November 11, 2026: plan fixed; main run for Part 1 started and finished.
- `RESULTS-part1.md` is the Part 1 result, with its limits. Raw responses are in `data/`.
- `DONATIONS.md` is the running ledger. Receipts will be added when the donations are paid.

## Who

Casey Wright, working with Claude. Claude wrote the program and ran the sessions; Claude models are also the subjects, which the plan's checks are meant to guard against.
