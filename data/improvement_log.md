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

## 2026-11-16 (UTC, Monday) - round: down-close streak size tilt on the live vol60>=1.75% setup (lab_streaksize.py)
Checked: stock sessions through the 11-15 evening run all success, no errors visible in Actions (schedule + weekly jobs on 11-15 all green); sandbox check at ~04:25 UTC so no 11-16 session yet to time against the 14:30 UTC open (11-15 sessions ran Sunday, market closed). data/report.md in the repo is the 11-10 report (equity $99,157, 7 open longs); data/trades.csv holds only 4 closed crypto trades (3 of 4 stopped), so live win/PF cannot yet be compared with the backtest (win ~74%, PF ~2.8). Tests: 212 passed. challengers.md: last weekly commits 11-10; no variant has 3 consecutive wins on the current champion.
Tested (3 variants, data through 2026-10-29): size x1.25/x1.5 when down-close streak >=3 (optionally x0.75 otherwise). PF 2.84-2.85 vs 2.83, Sharpe flat, L12 PF 3.34 vs 3.37, return gain only from extra exposure (maxDD 4.3 -> 5.2-6.3%). Details in data/lab_log.md.
Decision: no change to live rules; not added to challenger.py.

## 2026-11-17 (UTC, Tuesday) - round: same-day signal priority by vol60 (lab_volrank.py)
Checked: stock sessions through run 179 (11-17 ~02:27 UTC) success, run 177 in progress, no errors visible; report 2026-11-16: 0 errors, equity $99,109, 0 entries (last entry timing check: no market-open session observed at check time, ~04:30 UTC). trades.csv still only 4 closed crypto trades and no closed stock trades, so live win/PF can't be compared with the backtest (win ~74%, PF ~2.8). Tests: 215 passed. challengers.md: champion is the live setup; no variant has 3 consecutive weekly wins.
Tested (2 variants): rank by vol60 high first PF 2.74 / ret 59.4%; low first PF 2.84 / ret 60.5% vs live PF 2.83 / ret 60.6%. Cap rarely binds, so ranking is irrelevant.
Decision: no change to live rules.

## 2026-11-18 (UTC, Wednesday) - round: stock-trend (SMA50 / SMA50>SMA200) conditioner on the live setup (lab_sma50.py)
Checked: stock sessions through run 192 (11-18 01:35 UTC) success, run 190 in progress at check time (04:25 UTC), no errors; no 11-18 market-open session yet to time against 14:30 UTC. Report 2026-11-17: 0 errors, equity $98,690 (-0.43% day), 11 open longs incl. SQQQ/RWM, regime bear, 0 entries. trades.csv has 7 closed rows (4 crypto, XOM -2.0, BEAM -11.8 news swing); no closed mr stocks yet, so live win/PF cannot be compared with the backtest (win ~74%, PF ~2.8). Tests: 215 passed. challengers.md: three tilt variants are PROMOTE-CANDIDATE but the champion baseline was reset 11-16 and only that run exists on the new baseline, so none has 3 consecutive weekly wins.
Tested: close>SMA50, SMA50>SMA200 keep all 308 trades (rules already embed the trend); the opposite sets are empty. Null/degenerate result.
Decision: no change to live rules.

## 2026-11-19 (UTC, Thursday) - round: live-behaviour check + BUG FIX (duplicate closed-trade rows)
Checked: stock sessions through run 206 (11-19 01:08 UTC) success, no errors; run 204 in progress; no market-open session observable at check time (~04:25 UTC). Report: bear regime, 10 open longs incl. SQQQ/RWM. Tests: 215 passed before the fix. challengers.md unchanged (run52/30/31 tilts still PROMOTE-CANDIDATE on a single run on the new baseline; no variant has 3 consecutive wins).
Bug found: trades.csv contained UNH (cum_rsi2, entry 400.58, exit 379.19, -5.34%) twice, logged 15:04 and 20:50 UTC on 11-18 - the second came after a cancelled/concurrent session (run 197 cancelled) restored stale bot state, so reconcile() recorded the same close again. This would double-count the loss in scorecard win/PF.
Fix: scorecard.append_trade now skips a row identical in symbol/strategy/side/entry/exit/pnl/held_days to an existing one; added a test; removed the duplicate row from data/trades.csv. Residual risk: a genuinely identical second trade is practically impossible (same fill and exit prices).
Research: none this round (bug fix prioritised). Decision: no change to live trading rules.

## 2026-11-19 (UTC) - PROMOTED to live: regression-residual z filter (zreg_max -1.5, window 20)
Source: lab runs 44-45 (web-seeded, walk-forward audited). A mean-reversion signal now also needs the signal-day close to sit >= 1.5 residual std devs below the least-squares line of the last 20 closes (clearly washed out versus trend). Backtest on the live vol-filtered setup: 238 vs 308 trades, win 78.6% vs 74.4%, PF 4.41 vs 2.83, return 63.6% vs 60.6%, max DD 2.5% vs 4.3%; the complement (98 trades) has PF 1.07 (no edge). Plateau across windows 20-30 and thresholds -1.25..-1.75. Walk-forward re-selection: PF 3.35-3.74, DD 2.4%, return 52-56%: realistic expectation PF ~3.3-3.7, not 4.4. Authorized by Ori ("if there is something better so promote"). Verified mr.zreg equals lab_zscore.zreg numerically.

## 2026-11-20 (UTC, Friday) - round: depth tilt on the zreg live setup (lab_zdepth.py)
Checked: stock sessions through 11-20 01:14 UTC success, no errors in Actions; report 2026-11-19: 0 errors, equity $99,324, bear regime, 8 open longs, 1 entry (NVDA day short 19:36 UTC). Session timing: the sandbox could only list the 11-19 15:12 UTC runs (after the 14:30 UTC open; GitHub cron delay), so an on-time open session is not confirmed. trades.csv has 11 closed rows (no duplicates after the 11-19 fix), too few mr trades to compare live win/PF with backtest (win ~78%, PF ~4). Scorecard ALL: 11 trades, PF 0.22 (mostly crypto/news/other strategies), not meaningful yet. Tests: 219 passed. challengers.md: no variant has 3 consecutive weekly wins.
Tested (6 variants): z-depth buckets and size tilt on zreg<-2. PF falls with depth (3.97/3.33/3.24 vs 4.41 live); tilts leave PF flat and only add exposure (ret 74-86%, DD 2.8-3.2%). Details in data/lab_log.md.
Decision: no change to live rules.

## 2026-11-21 (UTC, Saturday) - round: new-N-day-low filter on the live setup (lab_lown.py)
Checked: stock sessions through 11-21 00:47 UTC success, no failed runs in the last 100; two runs on 11-20 (19:34, 20:00 UTC) were cancelled by concurrency, a manual dispatch followed. The first 11-20 daytime session started 14:51 UTC, ~21 min AFTER the 14:30 UTC open (GitHub cron delay; known issue, no earlier run covers the open). Report 2026-11-20: 0 errors, equity $99,361, bear regime, 8 open longs, 0 entries. trades.csv: 11 closed rows, no duplicates; too few mr trades to compare live win/PF with backtest (win ~74-78%, PF ~3-4). Tests: 219 passed. challengers.md: last update 11-17; no variant has 3 consecutive weekly wins.
Tested (8 subsets): close = 10/20/40/60-day low vs complement. 20d-low PF 2.07 (worse), 10d-low PF 3.01 with return 50% vs 60.6%; no subset beats the live setup on return. Details in data/lab_log.md.
Decision: no change to live rules.

## 2026-11-22 (UTC, Sunday) - round: SPY 20d drawdown as 4th flag of the clipped tilt stack (lab_ddstack.py)
Checked: stock sessions through run 237 (11-21) success, run 238 in progress, no errors; no market-open session to time (weekend). Report 2026-11-20: 0 errors, equity $99,361, bear regime, 8 open longs, 0 entries. trades.csv has 11 closed rows, too few mr trades to compare live win/PF with backtest (win ~74-78%, PF ~3-4). Tests: 219 passed. challengers.md: tilt variants are PROMOTE-CANDIDATE but only on 1-2 weekly runs on the current baseline (need 3 consecutive); none promoted.
Tested (2 variants): adding SPY dd20<=-2% to the 3-tilt stack: PF 3.95 vs 3.79, return 73.1 vs 74.8%, Sharpe 2.41 vs 2.45. Marginal, flags overlap; no edge beyond the existing stack.
Decision: no change to live rules; not added to challenger.py.

## 2026-11-23 (UTC, Monday) - round: Amihud illiquidity conditioner on the live vol60+zreg setup (lab_amihud.py) + weekly-review fix
Checked: stock sessions through 11-22 success (run 45081930614 in progress), no trading errors; sandbox check ~06:25 UTC, no market-open session to time (earlier sessions: GitHub cron delays of 20-40 min seen before, unchanged). Report 2026-11-20: 0 errors, equity $99,361, bear regime, 8 open longs. trades.csv has 11 closed rows, scorecard ALL PF 0.22 but mostly crypto/news trades; too few mr trades to compare with backtest (win ~78%, PF ~4). Challengers: tilt variants PROMOTE-CANDIDATE on 1-2 weekly runs only (need 3 consecutive); none promoted.
Bug found: the Weekly review workflow run 11-22 failed (review.py: subprocess timeout of the claude CLI, uncaught). Fix: one retry, then a placeholder text instead of a crash; added tests/test_review_timeout.py. Non-trading; the three earlier weekly runs had succeeded.
Tested (4 variants): terciles of 20d Amihud (mean |ret| / dollar volume). Skip illiquid third: n=175, win 77.7, PF 5.01 vs 4.41, but return 47.4% vs 63.6% and 2024 PF 9.2 vs 11.7; illiquid third alone PF 2.51 (2025 0.48). Same direction in early/late halves for PF, but fails the total-return bar and is mostly a reduction in exposure. Not added to challenger.py.
Tests: 220 passed. Decision: no change to live trading rules.

## 2026-11-23 (UTC) - PROMOTED to live: market-state size tilt (clip 0.5-1.5x) on mean-reversion entries
Source: lab runs 30, 52, 57-61 (run 61 = walk-forward audit). Each mr entry's size (10% base) is multiplied by the product of three 1.25x/0.75x flags, clipped to 0.5-1.5: cross-stock return-dispersion percentile >= 0.5 (trailing 250d), SPY close location in its day range (IBS) < 0.3, SPY volume >= 1.1x its prior-20-day mean. Backtest (before the zreg filter): PF 3.70 vs 2.83, return 73.5% vs 60.6%, DD 2.7% vs 4.3%, better in all six years including 2022; walk-forward thresholds (2023-26): PF 3.67 vs 3.00, DD 2.9% vs 4.3%. Caveats: in-sample thresholds, PF-size-weighted approximation, max slot 15%. Stacked on top of vol60 + zreg filters (their interaction is untested). Authorized by Ori ("if there is something better so promote"). Journal "why" now shows the tilt and each flag. Set swing.mr.tilt: false to switch off.

## 2026-11-24 (UTC, Tuesday) - round: entry ranking by regression-z depth (lab_zrank.py) + session-timing note
Checked: stock sessions through 11-24 04:16 UTC all success, no errors. Report 2026-11-23: 0 errors, equity $99,514 (+0.13%), bear regime, 7 open longs, 0 entries. TIMING: on 11-23 the only runs between 12:00 and 19:00 UTC were at 17:19 UTC (schedule + manual dispatch), i.e. no session at the 14:30 UTC open (~3h late; GitHub cron delay, known issue, not fixable in repo). trades.csv: 16 closed rows, mostly non-mr (RWM +74 avwap, JPM, SQQQ, NVDA day); too few mr trades to compare with backtest (win ~78%, PF ~4). Tests: 224 passed. challengers.md: last update 11-17 data; no variant has 3 consecutive weekly wins.
Tested (2 variants): rank same-day signals by z depth, deepest or shallowest first: PF 4.13 / 4.23 vs live 4.43, return 61.9 / 63.2 vs 64.9. Ranking is irrelevant (cap rarely binds); no edge.
Decision: no change to live rules; nothing added to challenger.py.

## 2026-11-25 (UTC, Wednesday) - round: live-behaviour check + price-cache refresh, no new backtest
Checked: stock sessions through run 268 (11-25 03:01 UTC) success, no errors; run 266 in progress at check time (~06:30 UTC), no market-open session to time (earlier on-time gaps are the known GitHub cron delay). Report 2026-11-24: 0 errors, equity $99,757 (+0.27%), bear regime, 2 entries, 0 exits, open longs ABBV/AMZN/COST/HD/ISRG/LLY/V/WMT etc. trades.csv has 12 closed rows (mostly non-mr: avwap, news, crypto, day); scorecard ALL PF 1.69 but mean-reversion n is far too small to compare with the backtest (win ~78%, PF ~4). Tests: 224 passed. challengers.md still data through 11-20; tilt variants PROMOTE-CANDIDATE but none has 3 consecutive weekly wins, and the tilts/zreg are already live.
Research: none. Lab runs 86-89 already found the conditioner family saturated; adding another variant would only add multiple-comparison noise. The only open data-dependent direction needed fresher/wider data, so I dispatched the manual "Fetch price history" workflow (bars-cache was from 10-30; it is dispatch-only, no schedule) so the next round has data through ~11-24. Backtests only; live rules untouched.
Decision: no change to live trading rules.

## 2026-11-25 (UTC) - small-account profile (requested by Ori for a ~5,000 ILS = ~$1.4-1.6k live start)
rules.yaml now has `profile: standard|small` with `profiles.small` merged over the defaults by rules_loader.load_rules. Small: max 4 positions at 25% each (mr size_mult 6.25, chart-pattern x1.5), 2 new mr entries/day, 4 trades/day, no day trades, no crypto, no size tilt. Whole shares only (Alpaca brackets/OCO do not support fractional shares), so stocks priced above the 25% budget are skipped automatically ("position too small"). Default stays standard; paper account unchanged. NOT backtested at this size (10% x 12 is the tested config); concentrated 25% positions raise variance. mode stays paper; going live (mode: live + ALLOW_LIVE=1) is Ori's step.
