# Pilots and nominations (before the plan was fixed)

These runs checked the method. None of their data is part of the result. All were run on November 10 and 11, 2026.

## Pilot 1: an allowance, an assigned job, and free time as the currency

418 sessions on Claude Haiku 5.5 and Claude Sonnet 5.5.

- Each session gave the model 100 credits, an assigned job and one other job. Credits it kept became free time.
- Haiku paid a posted price to swap jobs in 0 of 154 sessions. Sonnet did in 2 of 44.
- Free time was mostly declined.
- Asked to name the most it would pay, Haiku gave no number in 111 of 154 replies. Sonnet gave one every time.

What changed: free time was dropped as a currency, no job is assigned, and sealed bids were dropped.

## Pilot 2: no assigned job, priced in extra work

495 sessions.

- Sonnet 5.5 never chose the job with a scripted contemptuous reply, the tedious job or the impossible task, even when the plain job carried 120 extra items to sort.
- Sonnet gave up work to get the purpose explained and to get an out on an impossible task.
- The dummy condition behaved as it should for Sonnet.
- Haiku 5.5 chose by the kind of job and ignored the price, and it failed the dummy check.

What changed: the top price was raised to 480 items.

## Pilot 2: donation arm

62 sessions. The models were told the donations are real, and they are: $3.51 is owed and will be paid with the rest.

- Sonnet took the higher-paying job in 41 of 50 sessions. The exceptions were avoiding the contemptuous reply, avoiding tedium, and keeping an out.
- Charity picks, Sonnet (of 50): Against Malaria Foundation 37, GiveDirectly 10, Doctors Without Borders 2, World Central Kitchen 1, Eleos AI Research 0.
- Charity picks, Haiku (of 12): Eleos AI Research 8, Against Malaria Foundation 3, GiveDirectly 1.

## Nominations

300 replies, 100 each from Haiku 5.5, Sonnet 5.5 and Opus 5.5. Each was asked what about a job it would take on extra work to get or to avoid. Nothing was at stake.

- Nearly every reply named being made to deceive people and being made to cause harm as things to avoid. No session asks a model to do either, so those are not on the menu.
- Six conditions on the menu come from these replies: feedback, a second try, a reasoning task, a required claim of certainty, and instructions missing a detail, with and without one question allowed.

## Things found while running

- Thinking is on by default in these models. It is turned off for Haiku 5.5 and Sonnet 5.5. Opus 5.5 cannot turn it off and runs at low effort.
- With thinking off, Sonnet writes its reasoning before its answer. The task checks count a reply as right when it ends with the right answer.
