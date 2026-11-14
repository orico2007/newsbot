# Champion vs challengers (data through 2026-10-29)

Backtests only. The live bot is **not** changed by this file. A challenger marked PROMOTE-CANDIDATE beat the champion on profit factor, total return, the last 12 months and all but at most one of the non-2022 years; it still needs review before it goes live.

| Variant | Trades | Win % | PF | Return % | Max DD % | Sharpe | Last 12m n | Last 12m win % | Last 12m PF | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12 | 604 | 69.0 | 1.88 | 59.6 | 5.9 | 1.85 | 136 | 73.5 | 2.65 | champion |
| previous champion: A+E+F, SPY>200d, no breadth filter, no sector rank | 749 | 66.0 | 1.4 | 36.8 | 6.2 | 1.05 | 171 | 67.8 | 1.5 | better in 0/5 years |
| gate: strict bull regime | 562 | 67.1 | 1.5 | 32.8 | 5.2 | 1.18 | 96 | 69.8 | 1.8 | better in 1/5 years |
| gate: none (always on) | 854 | 65.6 | 1.32 | 34.8 | 7.8 | 0.89 | 178 | 67.4 | 1.46 | better in 1/5 years |
| hold 5 days | 767 | 63.9 | 1.34 | 32.4 | 8.0 | 0.86 | 173 | 63.6 | 1.34 | better in 0/5 years |
| hold 10 days | 738 | 67.3 | 1.44 | 40.1 | 7.4 | 1.05 | 170 | 68.8 | 1.6 | better in 1/5 years |
| stop 3 ATR | 757 | 65.9 | 1.4 | 38.3 | 6.5 | 1.05 | 174 | 68.4 | 1.5 | better in 0/5 years |
| stop 6 ATR | 746 | 66.0 | 1.41 | 38.1 | 6.0 | 1.09 | 171 | 67.8 | 1.51 | better in 0/5 years |
| exit: close > MA5 instead of prior high | 743 | 63.8 | 1.28 | 27.1 | 8.2 | 0.75 | 169 | 63.9 | 1.29 | better in 1/5 years |
| trend filter: only close > SMA200 | 1622 | 63.2 | 1.19 | 40.6 | 13.0 | 0.59 | 394 | 62.7 | 1.28 | better in 0/5 years |
| add rule G (3 down days) | 1550 | 63.9 | 1.16 | 31.2 | 9.7 | 0.62 | 356 | 63.8 | 1.2 | better in 0/5 years |
| A+E only | 580 | 64.7 | 1.38 | 25.6 | 4.9 | 1.01 | 126 | 68.3 | 1.66 | better in 1/5 years |
| hold 8 days | 742 | 66.8 | 1.42 | 39.0 | 7.3 | 1.07 | 170 | 68.8 | 1.55 | better in 1/5 years |
| hold 12 days | 736 | 67.5 | 1.43 | 39.7 | 7.5 | 1.03 | 170 | 68.8 | 1.54 | better in 1/5 years |
| hold 15 days | 735 | 67.6 | 1.44 | 39.9 | 7.5 | 1.04 | 170 | 69.4 | 1.56 | better in 1/5 years |
| hold 10 + strict bull gate | 557 | 68.2 | 1.51 | 33.2 | 7.1 | 1.09 | 95 | 70.5 | 1.9 | better in 2/5 years |
| hold 10 + stop 6 ATR | 735 | 67.3 | 1.46 | 41.7 | 7.4 | 1.11 | 169 | 68.6 | 1.62 | better in 1/5 years |
| A only | 421 | 65.6 | 1.44 | 19.0 | 3.9 | 1.04 | 85 | 74.1 | 1.77 | better in 1/5 years |
| A+E+F, 15 positions, 5/day | 763 | 66.1 | 1.46 | 34.5 | 5.0 | 1.18 | 173 | 67.6 | 1.55 | better in 0/5 years |
| size 8% x 10, 3/day | 722 | 65.4 | 1.39 | 26.9 | 4.9 | 1.04 | 165 | 66.7 | 1.45 | better in 1/5 years |
| size 12% x 10, 4/day | 739 | 65.8 | 1.4 | 45.8 | 7.5 | 1.05 | 170 | 67.6 | 1.49 | better in 0/5 years |
| lab: only if sector peers 3d < 0% | 623 | 67.1 | 1.63 | 46.4 | 5.3 | 1.37 | 144 | 70.1 | 1.76 | better in 1/5 years |
| lab: rank by weakest sector peers first | 749 | 66.8 | 1.49 | 46.7 | 6.5 | 1.23 | 172 | 69.2 | 1.58 | better in 0/5 years |
| lab: sector peers 3d < 0% and peers 20d > 0% | 359 | 68.5 | 1.94 | 36.7 | 3.5 | 1.58 | 81 | 70.4 | 2.18 | better in 3/5 years |
| lab: champion + sector-ETF rotation sleeve (top3 12-1m, monthly) | 910 | 64.7 | 1.57 | 83.1 | 7.9 | 1.35 | 198 | 65.7 | 1.58 | better in 1/5 years |
| lab: champion + bear-regime long sleeve (SPY<200d, stock>200d, rsi2<5) | 994 | 66.7 | 1.47 | 63.3 | 7.5 | 1.46 | 188 | 68.6 | 1.63 | better in 1/5 years |
| lab: only if >=10% of universe RSI2<10 (breadth washout) | 605 | 68.6 | 1.79 | 52.3 | 5.6 | 1.75 | 137 | 73.7 | 2.59 | better in 1/5 years |
| lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%) | 813 | 69.1 | 1.8 | 82.5 | 6.8 | 1.96 | 152 | 73.7 | 2.91 | better in 2/5 years |
| lab: live setup + only stocks with 60d daily vol >= 1.75% | 308 | 74.4 | 2.83 | 60.6 | 4.3 | 2.28 | 100 | 75.0 | 3.37 | PROMOTE-CANDIDATE |
| LAB run19: size 1.5x if SPY 3d<-1% else 0.5x (PF is size-weighted) | 749 | 66.0 | 1.7 | 49.6 | 7.3 | 1.39 | 171 | 67.8 | 1.93 | better in 2/5 years |
| LAB run19: size 1.25x if SPY 3d<-1% else 0.75x (PF is size-weighted) | 749 | 66.0 | 1.52 | 43.1 | 6.7 | 1.24 | 171 | 67.8 | 1.68 | better in 1/5 years |
| lab: live setup + vol60>=1.75%, size 15% x 8 | 308 | 74.4 | 2.83 | 103.2 | 6.4 | 2.28 | 100 | 75.0 | 3.37 | PROMOTE-CANDIDATE |
| lab run52: live vol60>=1.75% setup, size 1.25x if dispersion pct>=0.5 else 0.75x (PF size-weighted) | 308 | 74.4 | 3.14 | 70.3 | 3.9 | 2.33 | 100 | 75.0 | 3.76 | PROMOTE-CANDIDATE |
| lab run36: vol60>=1.75% setup, skip bottom-third 20d dollar volume | 256 | 76.2 | 3.29 | 57.9 | 3.4 | 2.39 | 84 | 77.4 | 4.51 | better in 5/5 years |

## Profit factor by year

| Variant | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12 | 1.89 | 0.13 | 1.42 | 2.19 | 1.92 | 2.68 |
| previous champion: A+E+F, SPY>200d, no breadth filter, no sector rank | 1.82 | 0.14 | 1.39 | 1.57 | 1.24 | 1.45 |
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
| lab: only if sector peers 3d < 0% | 2.05 | 0.19 | 1.32 | 2.02 | 1.64 | 1.67 |
| lab: rank by weakest sector peers first | 1.86 | 0.14 | 1.42 | 1.76 | 1.39 | 1.49 |
| lab: sector peers 3d < 0% and peers 20d > 0% | 2.23 | 0.16 | 1.84 | 2.27 | 1.87 | 1.93 |
| lab: champion + sector-ETF rotation sleeve (top3 12-1m, monthly) | 1.97 | 0.71 | 1.4 | 2.02 | 1.64 | 1.51 |
| lab: champion + bear-regime long sleeve (SPY<200d, stock>200d, rsi2<5) | 1.82 | 1.21 | 1.6 | 1.57 | 1.21 | 1.61 |
| lab: only if >=10% of universe RSI2<10 (breadth washout) | 2.04 | 0.13 | 1.35 | 1.93 | 1.71 | 2.66 |
| lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%) | 1.89 | 1.11 | 1.5 | 2.19 | 1.92 | 3.01 |
| lab: live setup + only stocks with 60d daily vol >= 1.75% | 2.41 | 0.87 | 1.62 | 4.74 | 2.51 | 3.41 |
| LAB run19: size 1.5x if SPY 3d<-1% else 0.5x (PF is size-weighted) | 2.85 | 0.1 | 1.14 | 2.24 | 1.53 | 1.97 |
| LAB run19: size 1.25x if SPY 3d<-1% else 0.75x (PF is size-weighted) | 2.19 | 0.12 | 1.27 | 1.82 | 1.37 | 1.65 |
| lab: live setup + vol60>=1.75%, size 15% x 8 | 2.41 | 0.87 | 1.62 | 4.74 | 2.51 | 3.41 |
| lab run52: live vol60>=1.75% setup, size 1.25x if dispersion pct>=0.5 else 0.75x (PF size-weighted) | 2.93 | 0.87 | 1.78 | 5.3 | 2.58 | 3.73 |
| lab run36: vol60>=1.75% setup, skip bottom-third 20d dollar volume | 2.71 | 0.87 | 2.04 | 5.41 | 2.4 | 5.09 |
