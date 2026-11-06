# Improvement log (research rounds; live rules unchanged unless stated)

## 2026-11-05 (UTC) - round: SPY market-fear filter on champion entries
Checked: stock sessions on 2026-11-04 all green (run 37 started 13:44 UTC, before the 14:30 UTC winter open; later runs success, several cancelled by self-chaining/concurrency, no errors). Report 2026-11-04: 0 errors, equity ~$100.06k, 4 open longs. Scorecard has only 1 closed (crypto) trade; no closed stock trades yet since the SPY>200d gate switch, so live win/PF cannot be compared to backtest (win ~66%, PF ~1.4) yet. Tests: 199 passed. challengers.md has only 2 weekly runs (no variant has 3 consecutive wins; none flagged PROMOTE-CANDIDATE).
Tested (lab_fear.py, 5 variants, multiple-comparison discount applies; same simulator as champion, bars cache data through 2026-10-29):
| Variant | n | Win % | PF | Ret % | MaxDD | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| skip if SPY 1d < -1% | 630 | 64.6 | 1.19 | 14.1 | 8.2 | 1.12 | worse every year |
| skip if SPY 1d < -2% | 728 | 65.0 | 1.32 | 29.0 | 6.5 | 1.40 | worse |
| skip if SPY 3d < -3% | 735 | 65.9 | 1.41 | 37.2 | 6.2 | 1.50 | ~same |
| skip if >3% below 5d high | 706 | 65.9 | 1.38 | 33.0 | 6.1 | 1.45 | mixed |
| ONLY if SPY 3d < -1% | 267 | 69.3 | 2.25 | 32.6 | 4.5 | 2.87 | 5.3/.07/.95/4.3/1.7/3.6 |
Result: a fear filter does NOT help; market weakness is where the mean-reversion edge is richest (skipping fear days cuts PF). The reverse (trade only after SPY dips) has much higher PF/Sharpe and lower drawdown, but 64% fewer trades, slightly lower total return, and 2023 PF 0.95 - so it fails the promotion bar (return, year consistency). Possible follow-up: use SPY-dip as a ranking/priority or size-up signal rather than a hard filter.
Decision: no change to live rules; not added to challenger.py (needs filter support; one-round evidence only).

## 2026-11-06 (UTC) - round: SPY-dip as a position-size tier (follow-up of the 11-05 fear-filter round)
Checked: stock sessions through 2026-11-05 all success (run 60-64 green; 53/55/56 cancelled by concurrency, no errors; 11-05 session run 37-era start was before the 14:30 UTC open). Report 2026-11-05: 0 errors, equity $99,265 (day -0.79%), 4 open longs, no entries/exits. Scorecard still has only 2 closed crypto trades and no closed stock trades, so live win/PF cannot yet be compared with the backtest (win ~66%, PF ~1.4). 11-06 session had not run yet at check time. Tests: 202 passed. Note: the sandbox checkout was a detached HEAD; checked out main before pulling. challengers.md has only 2 weekly runs (the two lab variants flagged PROMOTE-CANDIDATE have not won 3 consecutive runs).
Tested (lab_fearsize.py, 3 sizing variants + 1 control, post-hoc scaling of the champion's taken trades; multiple-comparison discount applies; cache data through 2026-10-29):
| Variant | Ret % | MaxDD | Sharpe | PF 21/22/23/24/25/26 |
|---|---|---|---|---|
| CHAMPION flat 10% | 36.8 | 6.2 | 1.05 | 1.82/.14/1.39/1.57/1.24/1.45 |
| 1.5x when SPY 3d<-1%, else 1x | 54.6 | 8.2 | 1.21 | 2.10/.13/1.29/1.76/1.34/1.60 |
| 1.5x dip, 0.75x else | 52.1 | 7.7 | 1.30 | 2.37/.11/1.23/1.94/1.42/1.74 |
| 1.3x dip only | 47.2 | 7.4 | 1.15 | 1.99/.13/1.33/1.69/1.31/1.55 |
Walk-forward split (1.5x/0.75x): 2021-23 return 8.8% -> 9.1% with maxDD 6.2 -> 7.7 and Sharpe 0.63 -> 0.59 (no gain); 2024-26 return 25.7% -> 39.3%, DD 5.9 -> 4.7, Sharpe 1.38 -> 1.94. 2023 PF falls in every variant.
Result: the gain comes entirely from the later years; the early (selection) period shows no improvement and a worse drawdown, so it does not pass walk-forward discipline. Also untested for capital/leverage limits (dip days stack up to 15% positions). Not promoted, not added to challenger.py (needs per-trade sizing support in the portfolio simulator).
Decision: no change to live rules.

## 2026-11-06 (manual, on Ori's explicit instruction) - promoted lab findings to the LIVE bot early
Ori told Claude to put the improvements live without waiting for the 3 consecutive weekly runs. Combined backtest (lab_combo.py, same simulator, data through 2026-10-29), champion entries A+E+F with SPY>200d:

| Variant | Trades | Win % | PF | Return % | MaxDD % | Sharpe | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|---|
| Old live setup | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.05 | 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| breadth>=10% filter | 605 | 68.6 | 1.79 | 52.3 | 5.6 | 1.75 | 2.59 | 2.04/.13/1.35/1.93/1.71/2.66 |
| rank weakest sector peers | 749 | 66.8 | 1.49 | 46.7 | 6.5 | 1.23 | 1.58 | 1.86/.14/1.42/1.76/1.39/1.49 |
| **filter + rank (now live)** | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |

Live changes: mr scan now (1) skips entries unless >= 10% of the ~125-stock universe has RSI2 < 10 (rules.yaml swing.mr.breadth_min), (2) ranks candidates weakest-sector-peers-first (3-day mean return of same-sector stocks), then rule rank. 2022 is still weak (PF 0.13); the SPY>200d gate stays. Caveats: dozens of variants were tried across lab runs, the universe is today's survivors, filter+rank was one extra combination tested. Watch live: trade count will drop (~20%), expect fewer but better entries. challenger.py's CHAMPION row still describes the OLD setup; the daily task should update the baseline to the new live setup (filter+rank) before judging future variants.
