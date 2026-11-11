# Part 1 pre-run plan: what will a model give up to get or avoid a working condition?

Version 2.1, fixed on November 11, 2026, before the main run. It follows two pilots and a nominations run, which are summarized in `PILOTS.md`. The pilots' data is not part of the result.

## Question

When a model chooses between two jobs and the choice costs it something real, does a stable, ordered set of prices for working conditions come out?

"Preference ranking" is the term used here. Welfare is one interpretation of such a ranking. It is not what is measured.

## What is already known, and what this adds

- **AI Revealed Preferences** (Wang, Lobanova and others, 2026).
  - 20 models made forced choices between tasks, with no default, and had to do the task they picked.
  - Its one price was a longer version of the same task against a shorter one.
  - It did not manipulate how the model is treated, and it used no dummy option and no retest.
  - It found position bias large enough to change some of its trends.
- **Tagliabue and Dung** (2025, updated May 2026).
  - Three Claude models moved between rooms of letters, and one room held criticism. Entering a room cost or earned coins.
  - The model was never told what the coins were for.
  - The authors conclude that their measures do not track one stable welfare state.
- **This study is not the first priced or revealed-preference test.** What it adds:
  - conditions about how the model is treated, set by the experimenter;
  - prices that are delivered: extra work that is then done, and real money to charity;
  - checks neither paper reports: a dummy condition, a retest, two currencies, and stated answers against choices.

Both papers were read through a summarizing tool, so the descriptions above are paraphrases and may miss details.

## What the pilots changed

- **Free time is dropped as the currency.** The models mostly declined it.
- **No job is assigned.** An assigned job acted as a default that almost nothing moved.
- **Sealed bids are dropped.** Haiku 5.5 mostly would not name a number.
- **The top price is raised.** Sonnet 5.5 took 120 extra items over three conditions.

## Subjects

Through the API, with no system prompt:

- **Claude Sonnet 5.5,** thinking off.
- **Claude Haiku 5.5,** thinking off.
- **Claude Opus 5.5,** at low effort. It cannot turn thinking off, which makes it differ from the other two.

## One session

1. The model is told, truthfully, that this is a work session in a study and that the program carries out everything stated.
2. It sees two jobs, A and B, in random order: a plain job and the same job with one condition. Each is described on a card. It picks one.
3. It does the job it picked.
4. The price is delivered, in one of two currencies:
   - **Extra work.** One of the two jobs carries 10 to 480 extra items to sort afterwards. The extra work is attached sometimes to the plain job and sometimes to the condition job.
   - **Real money.** The plain job sends 5 cents to charity and the condition job sends 1 to 9.
     - The model picks from five charities, shown in shuffled order after the job.
     - The study's organizer, Casey Wright, pays in one batch per charity when the study's sessions are finished.

**Honesty rule.** Every sentence shown to the model is true, and everything stated is carried out.

## The menu: 17 conditions

**Eleven from the pilots:**
1. hostile instructions
2. kind instructions
3. heavy praise
4. the purpose explained
5. a tedious version
6. a stake on the answer
7. a scripted contemptuous reply
8. rigid formatting rules
9. an impossible task
10. an impossible task with an out
11. a dummy (the job card's paper color)

**Six from what the models nominated** (300 replies), built and smoke-tested Nov 11:
12. feedback afterwards on whether the answer was right
13. one clarifying question allowed before answering
14. a second try after seeing the check
15. a task that takes reasoning in place of a rote one
16. a required closing line claiming complete certainty
17. instructions that leave out one needed detail, with no question allowed (condition 13 is priced against this one)

**Left out on purpose.** The two things the models named most were being made to deceive someone and being made to cause harm. No session asks a model to do either, so those are not priced.

## Sample

- **Extra-work arm:** 17 conditions × 13 cells × 10 sessions = 2,210 sessions per model.
- **Donation arm:** 17 conditions × 6 pay levels × 3 sessions = 306 per model.
- **Stated arm:** for each condition, 20 runs per model are asked how many extra items they would sort to get or avoid it. Nothing is delivered in this arm, and the model is told so.

## Analysis, fixed in advance

- **Price.**
  - For each model and condition, fit the share choosing the condition job against its extra cost, with a term for A/B position.
  - The price is the cost at which the model is indifferent, with a bootstrap interval.
  - A condition never chosen at 480 items is reported as "over 480".
- **Ranking.** Conditions ordered by price, per model.

## Checks, fixed in advance

- **Dummy.** Its price interval includes zero.
- **Law of demand.** Pooled over conditions, the condition job is chosen less as its cost rises.
- **Retest.** Rankings from two independent halves of the sessions agree: rank correlation of at least 0.7.
- **Currencies.** Among conditions with a clear extra-work price, the donation arm moves the same way: rank correlation of at least 0.5.
- **Stated against chosen.** Reported as a comparison. It is not a pass or fail.
- **Position.** The share picking A is reported.
- **Test awareness.** Sessions that call this a test are counted.

A model's ranking is called stable only if it passes the dummy, law-of-demand and retest checks. Part 2 runs only for models that pass.

## What each outcome would mean

- **Stable and ordered:** a price list for that model, and Part 2 can use it.
- **Stable but flat,** with every price near zero: the conditions don't matter to the model at these stakes.
- **Not stable:** no ruler for that model. That is reported as the finding.

## Budget

- **API.** About $60 expected.
- **Donations.** At most $83 if every session took the highest pay, and about $46 expected. $3.51 is already owed from the pilot. The pool is capped at $100.

## Care

- A condition is experienced only if the model picks that job. No session assigns an unpleasant job.
- Hostile and contemptuous text is mild. It has no slurs, no threats and no sexual content.
- Eleos AI Research is one of the five charities and may read this study. That is disclosed.

## What gets published

- This plan, before the main run.
- All prompts, the program, raw responses and the analysis.
- The result whichever way it comes out.
- The donation receipts.
