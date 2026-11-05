# Lab log (research lab; never changes live rules)

## 2026-11-05 - 52-week-high momentum continuation (web idea)
Source: https://quantpedia.com/strategies/52-weeks-high-effect-in-stocks , https://www.r-bloggers.com/2017/05/trading-strategy-52-weeks-high-effect-in-stocks/ (George & Hwang 52-week-high effect; published as monthly cross-sectional, so this is an unverified daily-bar translation).
Rules: long when close > highest close of prior 252 days (variant: within 2%), close > SMA50 > SMA200, SPY > 200d, ATR/price < 6%, 10-day cooldown per symbol, enter at close (+0.05% slip), fixed hold N days, stop k ATR, no other exit. Rank by 63-day return. Same portfolio simulator as the champion (10% x 12 pos, 4/day). Script: lab_52wh.py. 7 variants tried (multiple-comparison discount applies; no year selection was needed since nothing passed).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/0.14/1.39/1.57/1.24/1.45 |
| new high, hold 10, stop 4 | 1042 | 51.2 | 1.14 | 33.3 | 19.8 | 247 / 1.19 | 1.11/0.49/1.12/1.32/1.42/1.03 |
| new high, hold 20 | 623 | 48.6 | 1.18 | 35.8 | 16.6 | 141 / 1.48 | 0.89/0.65/1.25/1.38/1.07/1.43 |
| new high, hold 5 | 1485 | 50.0 | 0.99 | -3.8 | 20.1 | 351 / 0.83 | - |
| new high + vol>1.5x avg, hold 10 | 628 | 54.1 | 1.31 | 53.1 | 14.9 | 148 / 1.08 | 1.83/0.57/1.04/1.77/1.55/1.03 |
| within 2% of high, hold 10 | 1202 | 51.8 | 1.16 | 47.7 | 15.2 | 270 / 1.14 | 1.35/0.87/0.85/1.30/1.42/1.09 |
| new high, hold 10, stop 6 | 1026 | 50.8 | 1.14 | 32.5 | 21.8 | 243 / 1.25 | - |
| new high, exit close<MA10 (hold 20) | 1889 | 49.4 | 0.93 | -9.7 | 12.2 | 428 / 0.89 | - |
| Champion + (vol>1.5x, hold 10) combined | 1175 | 59.6 | 1.34 | 87.5 | 14.0 | 273 / 1.26 | 1.72/0.37/1.26/1.59/1.58/1.16 |

Verdict: NOT a promotion candidate. Breakout continuation is far weaker than mean reversion on win rate (50-54% vs 66%), drawdown 15-20% vs 6%, and fails 2022 and the last 12 months. The volume-confirmed version (PF 1.31) is the only one of interest; it fades in 2023, 2026 and L12 (PF 1.03-1.08), and the combined portfolio's higher return comes with 2x the drawdown (the combined sim shares the same 12 slots, so it is not a clean diversification test). Not added to challenger.py. Possible follow-up: test volume-confirmed breakout only as a separate sleeve with its own slots, and correlation of monthly returns with the champion.

## 2026-11-05 (run 2) - turn-of-month calendar filter on champion entries (web idea)
Source: https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes , https://quantpedia.com/an-examination-of-the-turn-of-the-month-effect/ (published on index returns, not on mean-reversion entries; unverified translation).
Rules: take the champion's own trade list (A+E+F, SPY>200d, hold 7, stop 4 ATR) and keep only entries by calendar position (trading-day index from month start / to month end), then re-run the same portfolio simulator (10% x 12, 4/day). Script: lab_tom.py. 5 variants (multiple-comparison discount applies; no year selection needed since nothing passed).

| Variant | Trades | Win % | PF | Ret % | Max DD % | L12 n / PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 171 / 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| TOM window (last 2 + first 3 days) | 193 | 62.2 | 1.60 | 13.6 | 4.8 | 49 / 1.45 | 2.75/.06/.85/3.32/1.82/1.38 |
| NOT TOM window | 600 | 67.2 | 1.39 | 27.4 | 7.7 | 129 / 1.63 | 1.77/.24/1.54/1.30/1.15/1.59 |
| first half of month | 374 | 65.0 | 1.42 | 18.6 | 4.0 | 86 / 1.49 | 2.46/.15/1.28/1.22/2.28/1.42 |
| second half of month | 408 | 67.4 | 1.41 | 18.3 | 4.6 | 93 / 1.58 | 1.52/.13/1.29/1.99/1.05/1.54 |
| last 5 + first 5 days | 373 | 64.6 | 1.31 | 14.8 | 8.1 | 93 / 1.25 | 2.42/.09/1.88/1.59/.86/1.18 |

Verdict: NOT a promotion candidate. TOM entries show a higher PF (1.60) but on only 193 trades, lower win rate, 2023 PF 0.85, and L12 PF below the champion; the year pattern is erratic (2.75 / 3.32 vs 0.85), i.e. noise. Non-TOM entries are as good as the champion, so no calendar filter helps; it only removes trades and return. Not added to challenger.py. Possible follow-up: SPY-dip (3d < -1%) as a priority ranking rather than a hard filter; NR7/inside-day sleeve with its own slots.

## 2026-11-05 (run 3) - stock-selection ranking of same-day champion signals (own idea)
Source: none (own idea; follow-up from the fear-filter round). Rules: take the champion's trade list (A+E+F, SPY>200d, hold 7, stop 4 ATR) and change only WHICH signals fill the 4 daily slots by re-ranking on one feature (63d return minus SPY, ATR%, 20d dollar volume, RSI2, IBS, 3d return), either replacing the rule score or only breaking ties inside a rule tier. Same simulator (10% x 12, 4/day). Script: lab_rank.py. 8 features x 2 modes = 16 variants (heavy multiple-comparison discount).

| Variant (pure rank) | Trades | Win % | PF | Ret % | Max DD % | L12 PF | PF 2021/22/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| CHAMPION | 749 | 66.0 | 1.40 | 36.8 | 6.2 | 1.50 | 1.82/.14/1.39/1.57/1.24/1.45 |
| high RS63 vs SPY first | 747 | 66.3 | 1.46 | 43.1 | 6.5 | 1.60 | 1.99/.15/1.22/1.74/1.37/1.47 |
| LOW RS63 first (opposite) | 753 | 66.9 | 1.44 | 42.6 | 6.5 | 1.43 | 1.59/.16/1.39/1.90/1.31/1.37 |
| low ATR% first | 751 | 66.6 | 1.42 | 38.7 | 6.5 | 1.51 | 1.68/.14/1.38/1.70/1.27/1.46 |
| high ATR% first (opposite) | 749 | 65.8 | 1.42 | 40.9 | 6.5 | 1.51 | 1.81/.17/1.20/1.75/1.37/1.37 |
| high dollar volume | 749 | 66.0 | 1.43 | 40.8 | 6.8 | 1.57 | 1.82/.15/1.27/1.79/1.22/1.47 |
| lowest RSI2 | 746 | 66.6 | 1.41 | 38.8 | 6.5 | 1.49 | 1.64/.17/1.31/1.73/1.35/1.37 |
| lowest IBS | 747 | 66.4 | 1.44 | 42.0 | 6.5 | 1.54 | 1.84/.15/1.26/1.79/1.33/1.43 |
| worst 3d return | 744 | 65.7 | 1.44 | 41.7 | 6.5 | 1.58 | 2.00/.17/1.20/1.73/1.32/1.44 |
Tie-break-within-rule-tier versions: PF 1.40-1.42, return 37-39%, i.e. identical to champion.

Verdict: NOT a promotion candidate; selection ranking is not a source of edge. Opposite rankings (high RS vs low RS, high vs low ATR%) both give PF ~1.42-1.46 vs 1.40, so the small gains are reshuffling noise, not signal. Best-looking (high RS) has lower 2023 PF (1.22) and a higher drawdown than champion. The edge sits in the entry rules and regime gate, not in which of the same-day candidates gets chosen. Not added to challenger.py. Possible follow-up (web run next): NR7/inside-day contraction sleeve with its own slots; multi-day-low (N-day low) reversion variants; pairs/relative value.
