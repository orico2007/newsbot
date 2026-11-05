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
