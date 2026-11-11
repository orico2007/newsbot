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

## 2026-11-07 (UTC, Saturday) - round: weekday-of-signal seasonality inside the LIVE setup (breadth>=10% + weakest-peer rank)
Checked: stock sessions 11-05/11-06 all success or cancelled-by-concurrency (no errors); 11-06 session run 66 started 13:42 UTC, before the 14:30 UTC open. Report 2026-11-06: 0 errors, equity $99,159, 6 open longs, 2 entries (V, AMZN via chart-pattern swing). Scorecard still has only 3 closed (crypto) trades, no closed stock trades, so live win/PF cannot be compared with the backtest yet. Tests: 208 passed. challengers.md still only has 2 weekly runs; no variant has 3 consecutive wins. Note: challenger.py CHAMPION row still describes the OLD setup (pre-breadth/rank); baseline below is the new live setup.
Tested (lab_dow.py, 11 rows, same simulator, data through 2026-10-29; multiple-comparison discount applies):
| Variant | n | Win % | PF | Ret % | MaxDD | L12 PF | PF 21/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| LIVE | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 2.65 | 1.89/.13/1.42/2.19/1.92/2.68 |
| skip Monday signals | 548 | 70.4 | 2.02 | 59.8 | 5.7 | 3.52 | 2.07/.06/1.36/2.23/2.15/3.67 |
| skip Tuesday | 494 | 70.0 | 1.99 | 51.1 | 4.2 | 2.60 | worse return |
| skip Wed / Thu / Fri | | | 1.65 / 1.83 / 1.62 | 34.5 / 45.8 / 35.0 | | | worse |
Weekday-only PFs: Mon 1.45, Tue 1.44, Wed 2.16, Thu 1.41, Fri 2.00. Monday PF by year 3.0/1.4/2.3/1.5/0.9/0.7: strong 2021-24, weak 2025-26 - a regime drift, not a stable calendar effect. Wed/Fri 2024 and 2026 PFs are driven by tiny loss counts (16.8, 9.4).
Result: no stable weekday effect. Skip-Monday lifts PF slightly but total return is flat (59.8 vs 59.6), 2023 is worse, and the Monday weakness appears only in the sealed/late years (the selection signal is post-hoc), so it fails the promotion bar. Not added to challenger.py.
Decision: no change to live rules. Open follow-ups: sleeve sizing at 5%; ETF cross-asset filters (bond/VIX proxy) for the gate; true PEAD needs earnings data.

## 2026-11-08 (UTC, Sunday) - round: size-up tier for entries >10% below 252d high (live setup)
Checked: stock sessions through 11-06 success/cancelled-by-concurrency, no errors; 11-06 session started 13:42 UTC (before 14:30 open); run 83 in progress at check time. Report 2026-11-06: 0 errors, equity $99,159, 6 open longs. Scorecard still has only 3 closed crypto trades, none for stocks, so live win/PF can't be compared with the backtest yet. Tests: 208 passed. challengers.md has 2 weekly runs; no variant has 3 consecutive wins.
Tested (lab_proxsize.py, details in data/lab_log.md run 26): 1.5x size on entries >10% below the 252d high lifts return 59.6 -> 78.6%, Sharpe 1.85 -> 1.92, maxDD 5.9 -> 7.0, PF better or equal in every year, including the early period (2021-23 return 9.0 -> 12.2). Threshold is post hoc from run 24, modest risk-adjusted gain.
Decision: no change to live rules; not added to challenger.py (needs per-trade sizing support). Follow-up: add sizing support to the simulator and track.

## 2026-11-09 (UTC, Monday) - round: position-count / per-day cap / size grid on the NEW live setup (lab_portcap.py)
Checked: stock sessions through 11-08 success/cancelled-by-concurrency, no errors; last Friday session (run 66) started 13:42 UTC, before the 14:30 UTC open; no 11-09 session yet at check time (04:24 UTC). Report 2026-11-06: 0 errors. Scorecard has only 3 closed crypto trades, no closed stock trades, so live win/PF cannot be compared with the backtest (win ~66-69%, PF ~1.4-1.9) yet. Tests: 208 passed. challengers.md still has only a couple of weekly runs; no variant has 3 consecutive wins. Note: shorts in bear regimes were already tested in lab run 11 (not proven), so not repeated.
Tested (11 grid cells, same simulator, data through 2026-10-29; multiple-comparison discount applies). Live = 10% x 12 pos, 4/day: n=604, PF 1.88, ret 59.6%, DD 5.9, Sharpe 1.85.
| Variant | PF | Ret % | MaxDD | Sharpe |
|---|---|---|---|---|
| 2/day | 1.88 | 45.8 | 5.8 | 1.66 |
| 3/day | 1.94 | 59.9 | 5.9 | 1.89 |
| 6/day | 1.92 | 65.0 | 5.9 | 1.92 |
| 8 positions | 1.81 | 52.5 | 6.3 | 1.66 |
| 16 positions (4/day) | identical to live (cap never binds) | | | |
| 20 pos, 6/day | 1.92 | 65.2 | 5.9 | 1.92 |
| size 7 / 8 / 12 / 15% | return scales ~linearly with size (38.8 / 45.4 / 75.1 / 87.8%), DD 4.2 / 4.8 / 7.1 / 9.3, Sharpe/PF unchanged | | | |
Result: no free lunch. Sizing only trades return for drawdown at constant Sharpe; position cap above 12 never binds; per-day cap 6 adds ~+5pt return / +0.07 Sharpe, but PF is lower in 2021 and 2023 (1.77/1.40 vs 1.89/1.42), so it fails the "all but one non-2022 year better" bar and is within noise. Not added to challenger.py.
Decision: no change to live rules.

## 2026-11-10 (UTC, Tuesday) - round: down-close streak length filter on the live setup (lab_streak.py)
Checked: stock sessions through run 100 (11-10) success, no errors (run 98 in progress). Note: the 11-09 stock session (run 87) started 15:06 UTC, i.e. ~36 min AFTER the 14:30 UTC open (GitHub cron delay; earlier runs that day were overnight); report 2026-11-09 shows 0 errors, equity $99,269, 6 open longs, 0 entries. Scorecard still has only 4 closed crypto trades and no closed stock trades, so live win/PF can't be compared with the backtest yet. Tests: 209 passed. challengers.md has 2 weekly runs; no variant has 3 consecutive wins.
Tested (4 variants): streak>=3 down closes: n=487, win 71.0, PF 2.03, Sharpe 2.0 but return 50.6% vs 59.6% live; streak>=2 PF 1.79, ret 51.7; streak<=2 PF 1.27, ret 6.3. Fails the total-return bar; not promoted.
Decision: no change to live rules. Possible follow-up: size 1.25x on streak>=3 rather than filtering.

## 2026-11-10 (UTC) - PROMOTED to live: volatility filter (vol_min 1.75)
Source: lab runs 8-12. Live mr signals now require the stock's 60-day daily-return stdev >= 1.75%. Backtest on the live setup: 308 vs 604 trades, win 74.4% vs 69.0%, PF 2.83 vs 1.88, return 60.6% vs 59.6%, max DD 4.3% vs 5.9%, Sharpe 2.28 vs 1.85, PF better in every year (2022: 0.87 vs 0.13), holds in 2021-23 and 2024-26, ATR% measure agrees. Authorized by Ori ("if there is something better so promote"). Expect about half as many trades. Follow-ups: add vol_min to the challenger champion; sizing on the filtered set (15x8); bear sleeve.

## 2026-11-11 (UTC, Wednesday) - round: stop distance / max-hold on the live vol60>=1.75% setup (lab_stopvol.py)
Checked: stock sessions through run 114 (11-10 evening) success or cancelled-by-concurrency, no errors; no 11-11 session yet at check time (~04:30 UTC, nothing to compare with the 14:30 open). Report 2026-11-10: 0 errors, equity $99,157, 7 open longs, 1 entry (BEAM swing). Scorecard/trades.csv: only 4 closed crypto trades, no closed stock trades, so live win/PF cannot yet be compared with the backtest. Tests: 212 passed. challengers.md has 2 weekly runs; no variant has 3 consecutive wins.
Tested (6 variants): stop 3/5/6 ATR and hold 5/10/12 vs live (stop 4, hold 7; n=308, PF 2.83, ret 60.6%). Stops >4 are identical (rarely hit), stop 3 worse (PF 2.66); hold 10 PF 2.91 / ret 62.0 but worse in 2023 and 2025 and DD 5.0 vs 4.3; hold 5 clearly worse. Details in data/lab_log.md run 24.
Decision: no change to live rules; live parameters are on a plateau.
