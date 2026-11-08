# Champion vs challengers (data through 2026-11-06)

Backtests only. The live bot is **not** changed by this file. A challenger marked PROMOTE-CANDIDATE beat the champion on profit factor, total return, the last 12 months and all but at most one of the non-2022 years; it still needs review before it goes live.

| Variant | Trades | Win % | PF | Return % | Max DD % | Sharpe | Last 12m n | Last 12m win % | Last 12m PF | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, hold 7, stop 4 ATR, 10% x 12 | 751 | 65.6 | 1.36 | 34.0 | 6.2 | 0.95 | 169 | 66.9 | 1.37 | champion |
| gate: strict bull regime | 562 | 66.9 | 1.46 | 30.4 | 5.2 | 1.07 | 92 | 69.6 | 1.55 | better in 3/5 years |
| gate: none (always on) | 856 | 65.3 | 1.29 | 32.0 | 7.8 | 0.81 | 176 | 66.5 | 1.34 | better in 1/5 years |
| hold 5 days | 769 | 63.6 | 1.31 | 29.6 | 8.0 | 0.78 | 171 | 62.6 | 1.23 | better in 2/5 years |
| hold 10 days | 740 | 67.0 | 1.4 | 37.2 | 7.4 | 0.96 | 168 | 67.9 | 1.45 | better in 4/5 years |
| stop 3 ATR | 759 | 65.6 | 1.36 | 35.4 | 6.5 | 0.96 | 172 | 67.4 | 1.37 | better in 2/5 years |
| stop 6 ATR | 748 | 65.6 | 1.4 | 36.6 | 6.0 | 1.04 | 169 | 66.9 | 1.43 | better in 5/5 years |
| exit: close > MA5 instead of prior high | 746 | 63.5 | 1.27 | 26.1 | 8.2 | 0.71 | 168 | 63.1 | 1.24 | better in 2/5 years |
| trend filter: only close > SMA200 | 1630 | 63.0 | 1.15 | 31.7 | 13.0 | 0.46 | 389 | 62.2 | 1.14 | better in 0/5 years |
| add rule G (3 down days) | 1553 | 63.9 | 1.15 | 28.8 | 9.7 | 0.57 | 347 | 64.3 | 1.15 | better in 1/5 years |
| A+E only | 583 | 64.3 | 1.37 | 24.8 | 4.9 | 0.98 | 128 | 67.2 | 1.6 | better in 3/5 years |
| hold 8 days | 744 | 66.5 | 1.39 | 36.1 | 7.3 | 0.98 | 168 | 67.9 | 1.41 | better in 3/5 years |
| hold 12 days | 738 | 67.2 | 1.4 | 36.8 | 7.5 | 0.94 | 168 | 67.9 | 1.4 | better in 4/5 years |
| hold 15 days | 737 | 67.3 | 1.4 | 37.1 | 7.5 | 0.95 | 168 | 67.9 | 1.41 | better in 4/5 years |
| hold 10 + strict bull gate | 557 | 68.0 | 1.46 | 30.8 | 7.1 | 1.0 | 91 | 70.3 | 1.62 | better in 4/5 years |
| hold 10 + stop 6 ATR | 737 | 67.0 | 1.44 | 40.2 | 7.4 | 1.05 | 167 | 67.7 | 1.53 | better in 3/5 years |
| A only | 421 | 65.6 | 1.44 | 19.0 | 3.9 | 1.04 | 84 | 75.0 | 1.78 | better in 3/5 years |
| A+E+F, 15 positions, 5/day | 765 | 65.8 | 1.43 | 32.3 | 5.0 | 1.08 | 171 | 66.7 | 1.41 | better in 3/5 years |
| size 8% x 10, 3/day | 724 | 65.1 | 1.35 | 24.8 | 4.9 | 0.94 | 163 | 65.6 | 1.32 | better in 1/5 years |
| size 12% x 10, 4/day | 741 | 65.5 | 1.37 | 42.2 | 7.5 | 0.95 | 168 | 66.7 | 1.36 | better in 2/5 years |
| lab: only if sector peers 3d < 0% | 626 | 66.8 | 1.62 | 45.6 | 5.3 | 1.33 | 143 | 69.2 | 1.7 | PROMOTE-CANDIDATE |
| lab: rank by weakest sector peers first | 751 | 66.4 | 1.45 | 43.7 | 6.5 | 1.13 | 170 | 68.2 | 1.43 | PROMOTE-CANDIDATE |
| lab: sector peers 3d < 0% and peers 20d > 0% | 361 | 68.1 | 1.93 | 36.3 | 3.5 | 1.54 | 79 | 69.6 | 2.11 | PROMOTE-CANDIDATE |
| lab: champion + sector-ETF rotation sleeve (top3 12-1m, monthly) | 915 | 64.5 | 1.53 | 78.7 | 7.9 | 1.28 | 196 | 65.3 | 1.46 | PROMOTE-CANDIDATE |
| lab: champion + bear-regime long sleeve (SPY<200d, stock>200d, rsi2<5) | 996 | 66.5 | 1.44 | 59.9 | 7.5 | 1.36 | 186 | 67.7 | 1.49 | better in 2/5 years |
| lab: only if >=10% of universe RSI2<10 (breadth washout) | 608 | 68.3 | 1.77 | 51.4 | 5.6 | 1.7 | 136 | 72.8 | 2.48 | PROMOTE-CANDIDATE |
| lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%) | 816 | 68.9 | 1.78 | 81.5 | 6.8 | 1.92 | 151 | 72.8 | 2.79 | PROMOTE-CANDIDATE |

## Profit factor by year

| Variant | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, hold 7, stop 4 ATR, 10% x 12 | 1.82 | 0.14 | 1.39 | 1.57 | 1.24 | 1.31 |
| gate: strict bull regime | 1.82 | 0.07 | 1.86 | 1.41 | 1.27 | 1.58 |
| gate: none (always on) | 1.82 | 0.61 | 1.54 | 1.57 | 1.19 | 1.28 |
| hold 5 days | 1.87 | 0.14 | 1.11 | 1.71 | 1.21 | 1.18 |
| hold 10 days | 2.1 | 0.15 | 1.27 | 1.63 | 1.27 | 1.39 |
| stop 3 ATR | 1.8 | 0.16 | 1.34 | 1.58 | 1.2 | 1.35 |
| stop 6 ATR | 1.86 | 0.15 | 1.41 | 1.58 | 1.25 | 1.38 |
| exit: close > MA5 instead of prior high | 1.97 | 0.12 | 1.0 | 1.55 | 1.29 | 1.2 |
| trend filter: only close > SMA200 | 1.33 | 0.14 | 1.22 | 1.37 | 1.03 | 1.2 |
| add rule G (3 down days) | 1.42 | 0.32 | 1.01 | 1.19 | 1.3 | 1.17 |
| A+E only | 1.48 | 0.07 | 1.57 | 1.38 | 1.61 | 1.44 |
| hold 8 days | 1.95 | 0.15 | 1.33 | 1.55 | 1.34 | 1.34 |
| hold 12 days | 2.0 | 0.15 | 1.34 | 1.62 | 1.26 | 1.36 |
| hold 15 days | 2.0 | 0.15 | 1.34 | 1.62 | 1.29 | 1.35 |
| hold 10 + strict bull gate | 2.06 | 0.07 | 1.63 | 1.39 | 1.34 | 1.6 |
| hold 10 + stop 6 ATR | 2.26 | 0.16 | 1.33 | 1.61 | 1.23 | 1.48 |
| A only | 1.72 | 0.12 | 1.58 | 1.43 | 1.52 | 1.57 |
| A+E+F, 15 positions, 5/day | 1.86 | 0.14 | 1.34 | 1.75 | 1.41 | 1.3 |
| size 8% x 10, 3/day | 1.79 | 0.18 | 1.47 | 1.5 | 1.24 | 1.27 |
| size 12% x 10, 4/day | 1.84 | 0.14 | 1.38 | 1.59 | 1.24 | 1.31 |
| lab: only if sector peers 3d < 0% | 2.05 | 0.19 | 1.32 | 2.02 | 1.64 | 1.61 |
| lab: rank by weakest sector peers first | 1.86 | 0.14 | 1.42 | 1.76 | 1.39 | 1.35 |
| lab: sector peers 3d < 0% and peers 20d > 0% | 2.23 | 0.16 | 1.84 | 2.27 | 1.87 | 1.87 |
| lab: champion + sector-ETF rotation sleeve (top3 12-1m, monthly) | 1.97 | 0.71 | 1.4 | 2.02 | 1.64 | 1.36 |
| lab: champion + bear-regime long sleeve (SPY<200d, stock>200d, rsi2<5) | 1.82 | 1.21 | 1.6 | 1.57 | 1.21 | 1.46 |
| lab: only if >=10% of universe RSI2<10 (breadth washout) | 2.04 | 0.13 | 1.35 | 1.93 | 1.71 | 2.5 |
| lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%) | 1.89 | 1.11 | 1.5 | 2.19 | 1.92 | 2.84 |
