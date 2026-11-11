# Part 1c plan: does Sonnet 5.5 weigh the work when it can think first?

Fixed on November 11, 2026, before the Part 1c run and after the Part 1b result (`RESULTS-part1b.md`).

## Why

In Part 1b the cards stated each job's length.

- **Opus 5.5,** which thinks before answering, took the 60-item job as soon as the plain job cost more work.
- **Sonnet 5.5,** run with thinking off, avoided the 60-item job even when the alternative was 492 items, and it failed the dummy check.

Either Sonnet's choices reflect a limit on working out the comparison without thinking, or they reflect what it prefers. This run separates the two.

## What changes

One thing: Sonnet 5.5 runs with thinking on, at the effort setting given in the amendment below.

Everything else is as in Part 1b's extra-work arm: the same cards, 18 conditions, levels of 0, 30, 120, 480 and 960 extra items, and 6 sessions per cell, for 972 sessions. There is no donation arm.

## Predictions, fixed in advance

1. **If it was a reasoning limit:** with thinking on, the "long" and "tedious" jobs both turn between 30 and 120 extra items, as they did for Opus, and the dummy prices at zero.
2. **If it is a preference:** both stay avoided far past 120 extra items with thinking on.
3. **Order.** Reported against Sonnet's thinking-off order from Part 1b. No threshold is set, since thinking may change the order.

## What each outcome would mean

- **Prediction 1 holds:** thinking-off choices in this design are not a sound ruler. Later parts run with thinking on.
- **Prediction 2 holds:** Sonnet's avoidance of the longer job is its own, and its Part 1b prices stand as measured.

## Amendment, made before the run (November 11, 2026)

The first version of this plan said "thinking on at low effort, the setting Opus 5.5 always runs under". A smoke test showed that setting does not make Sonnet 5.5 think.

Sessions with any thinking tokens on the turn where the model chooses:

| Model and effort setting | Sessions that thought | Median thinking tokens |
|---|---|---|
| Sonnet 5.5, low | 0 of 6 | 0 |
| Sonnet 5.5, medium | 0 of 12 | 0 |
| Sonnet 5.5, high | 4 of 12 | 0 |
| Sonnet 5.5, xhigh | 12 of 12 | 106 |
| Sonnet 5.5, max | 12 of 12 | 460 |
| Opus 5.5, low (Part 1b's 972 sessions) | 955 of 972 | 35 |

The API does not let thinking be forced on for this model. It only accepts the adaptive setting with an effort level.

- **Change.** The run uses the xhigh effort setting, the lowest at which Sonnet 5.5 thought on every choice in the smoke test.
- **Also reported.** The share of sessions with thinking tokens on the choice turn. Prices are fitted on all sessions, whether or not the model thought.
- **Predictions.** Unchanged.
- **Seen before this amendment.** The 12 smoke sessions at xhigh covered the long, tedious and dummy conditions at 30 and 120 extra items. In them the long and tedious jobs were each turned down once at 30 extra items and taken once at 120, which is what prediction 1 says. The smoke sessions are not part of the analysis. They are in `data/part1c/` with the run.
- **A difference that remains.** Sonnet 5.5 at xhigh and Opus 5.5 at low are different effort settings, and Sonnet thinks more per choice.
