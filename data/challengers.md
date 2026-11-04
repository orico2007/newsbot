# Champion vs challengers (data through 2026-10-29)

Backtests only. The live bot is **not** changed by this file. A challenger marked PROMOTE-CANDIDATE beat the champion on profit factor, total return and the last 12 months; it still needs review before it goes live.

| Variant | Trades | Win % | PF | Return % | Max DD % | Sharpe | Last 12m n | Last 12m win % | Last 12m PF | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, hold 7, stop 4 ATR, 10% x 12 | 749 | 66.0 | 1.4 | 36.8 | 6.2 | 1.05 | 171 | 67.8 | 1.5 | champion |
| gate: strict bull regime | 562 | 67.1 | 1.5 | 32.8 | 5.2 | 1.18 | 96 | 69.8 | 1.8 |  |
| gate: none (always on) | 854 | 65.6 | 1.32 | 34.8 | 7.8 | 0.89 | 178 | 67.4 | 1.46 |  |
| hold 5 days | 767 | 63.9 | 1.34 | 32.4 | 8.0 | 0.86 | 173 | 63.6 | 1.34 |  |
| hold 10 days | 738 | 67.3 | 1.44 | 40.1 | 7.4 | 1.05 | 170 | 68.8 | 1.6 |  |
| stop 3 ATR | 757 | 65.9 | 1.4 | 38.3 | 6.5 | 1.05 | 174 | 68.4 | 1.5 |  |
| stop 6 ATR | 746 | 66.0 | 1.41 | 38.1 | 6.0 | 1.09 | 171 | 67.8 | 1.51 |  |
| exit: close > MA5 instead of prior high | 743 | 63.8 | 1.28 | 27.1 | 8.2 | 0.75 | 169 | 63.9 | 1.29 |  |
| trend filter: only close > SMA200 | 1622 | 63.2 | 1.19 | 40.6 | 13.0 | 0.59 | 394 | 62.7 | 1.28 |  |
| add rule G (3 down days) | 1550 | 63.9 | 1.16 | 31.2 | 9.7 | 0.62 | 356 | 63.8 | 1.2 |  |
| A+E only | 580 | 64.7 | 1.38 | 25.6 | 4.9 | 1.01 | 126 | 68.3 | 1.66 |  |
| size 8% x 10, 3/day | 722 | 65.4 | 1.39 | 26.9 | 4.9 | 1.04 | 165 | 66.7 | 1.45 |  |
| size 12% x 10, 4/day | 739 | 65.8 | 1.4 | 45.8 | 7.5 | 1.05 | 170 | 67.6 | 1.49 |  |

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
| size 8% x 10, 3/day | 1.79 | 0.18 | 1.47 | 1.5 | 1.24 | 1.41 |
| size 12% x 10, 4/day | 1.84 | 0.14 | 1.38 | 1.59 | 1.24 | 1.45 |
