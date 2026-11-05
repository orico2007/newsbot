# Champion vs challengers (data through 2026-10-29)

Backtests only. The live bot is **not** changed by this file. A challenger marked PROMOTE-CANDIDATE beat the champion on profit factor, total return, the last 12 months and all but at most one of the non-2022 years; it still needs review before it goes live.

| Variant | Trades | Win % | PF | Return % | Max DD % | Sharpe | Last 12m n | Last 12m win % | Last 12m PF | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, hold 7, stop 4 ATR, 10% x 12 | 749 | 66.0 | 1.4 | 36.8 | 6.2 | 1.05 | 171 | 67.8 | 1.5 | champion |
| gate: strict bull regime | 562 | 67.1 | 1.5 | 32.8 | 5.2 | 1.18 | 96 | 69.8 | 1.8 | better in 3/5 years |
| gate: none (always on) | 854 | 65.6 | 1.32 | 34.8 | 7.8 | 0.89 | 178 | 67.4 | 1.46 | better in 1/5 years |
| hold 5 days | 767 | 63.9 | 1.34 | 32.4 | 8.0 | 0.86 | 173 | 63.6 | 1.34 | better in 2/5 years |
| hold 10 days | 738 | 67.3 | 1.44 | 40.1 | 7.4 | 1.05 | 170 | 68.8 | 1.6 | better in 4/5 years |
| stop 3 ATR | 757 | 65.9 | 1.4 | 38.3 | 6.5 | 1.05 | 174 | 68.4 | 1.5 | better in 2/5 years |
| stop 6 ATR | 746 | 66.0 | 1.41 | 38.1 | 6.0 | 1.09 | 171 | 67.8 | 1.51 | better in 5/5 years |
| exit: close > MA5 instead of prior high | 743 | 63.8 | 1.28 | 27.1 | 8.2 | 0.75 | 169 | 63.9 | 1.29 | better in 2/5 years |
| trend filter: only close > SMA200 | 1622 | 63.2 | 1.19 | 40.6 | 13.0 | 0.59 | 394 | 62.7 | 1.28 | better in 0/5 years |
| add rule G (3 down days) | 1550 | 63.9 | 1.16 | 31.2 | 9.7 | 0.62 | 356 | 63.8 | 1.2 | better in 1/5 years |
| A+E only | 580 | 64.7 | 1.38 | 25.6 | 4.9 | 1.01 | 126 | 68.3 | 1.66 | better in 3/5 years |
| hold 8 days | 742 | 66.8 | 1.42 | 39.0 | 7.3 | 1.07 | 170 | 68.8 | 1.55 | better in 3/5 years |
| hold 12 days | 736 | 67.5 | 1.43 | 39.7 | 7.5 | 1.03 | 170 | 68.8 | 1.54 | better in 4/5 years |
| hold 15 days | 735 | 67.6 | 1.44 | 39.9 | 7.5 | 1.04 | 170 | 69.4 | 1.56 | better in 4/5 years |
| hold 10 + strict bull gate | 557 | 68.2 | 1.51 | 33.2 | 7.1 | 1.09 | 95 | 70.5 | 1.9 | better in 4/5 years |
| hold 10 + stop 6 ATR | 735 | 67.3 | 1.46 | 41.7 | 7.4 | 1.11 | 169 | 68.6 | 1.62 | better in 3/5 years |
| A only | 421 | 65.6 | 1.44 | 19.0 | 3.9 | 1.04 | 85 | 74.1 | 1.77 | better in 3/5 years |
| A+E+F, 15 positions, 5/day | 763 | 66.1 | 1.46 | 34.5 | 5.0 | 1.18 | 173 | 67.6 | 1.55 | better in 3/5 years |
| size 8% x 10, 3/day | 722 | 65.4 | 1.39 | 26.9 | 4.9 | 1.04 | 165 | 66.7 | 1.45 | better in 1/5 years |
| size 12% x 10, 4/day | 739 | 65.8 | 1.4 | 45.8 | 7.5 | 1.05 | 170 | 67.6 | 1.49 | better in 2/5 years |

## Profit factor by year

| Variant | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, hold 7, stop 4 ATR, 10% x 12 | 1.82 | 0.14 | 1.39 | 1.57 | 1.24 | 1.45 |
| gate: strict bull regime | 1.82 | 0.07 | 1.86 | 1.41 | 1.27 | 1.86 |
| gate: none (always on) | 1.82 | 0.61 | 1.54 | 1.57 | 1.19 | 1.41 |
| hold 5 days | 1.87 | 0.14 | 1.11 | 1.71 | 1.21 | 1.3 |
| hold 10 days | 2.1 | 0.15 | 1.27 | 1.63 | 1.27 | 1.55 |
| stop 3 ATR | 1.8 | 0.16 | 1.34 | 1.58 | 1.2 | 1.49 |
| stop 6 ATR | 1.86 | 0.15 | 1.41 | 1.58 | 1.25 | 1.46 |
| exit: close > MA5 instead of prior high | 1.97 | 0.12 | 1.0 | 1.55 | 1.29 | 1.24 |
| trend filter: only close > SMA200 | 1.33 | 0.14 | 1.22 | 1.37 | 1.03 | 1.39 |
| add rule G (3 down days) | 1.42 | 0.32 | 1.01 | 1.19 | 1.3 | 1.23 |
| A+E only | 1.48 | 0.07 | 1.57 | 1.38 | 1.61 | 1.5 |
| hold 8 days | 1.95 | 0.15 | 1.33 | 1.55 | 1.34 | 1.49 |
| hold 12 days | 2.0 | 0.15 | 1.34 | 1.62 | 1.26 | 1.51 |
| hold 15 days | 2.0 | 0.15 | 1.34 | 1.62 | 1.29 | 1.5 |
| hold 10 + strict bull gate | 2.06 | 0.07 | 1.63 | 1.39 | 1.34 | 1.89 |
| hold 10 + stop 6 ATR | 2.26 | 0.16 | 1.33 | 1.61 | 1.23 | 1.57 |
| A only | 1.72 | 0.12 | 1.58 | 1.43 | 1.52 | 1.57 |
| A+E+F, 15 positions, 5/day | 1.86 | 0.14 | 1.34 | 1.75 | 1.41 | 1.44 |
| size 8% x 10, 3/day | 1.79 | 0.18 | 1.47 | 1.5 | 1.24 | 1.41 |
| size 12% x 10, 4/day | 1.84 | 0.14 | 1.38 | 1.59 | 1.24 | 1.45 |
