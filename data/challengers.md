# Champion vs challengers (data through 2026-11-13)

Backtests only. The live bot is **not** changed by this file. A challenger marked PROMOTE-CANDIDATE beat the champion on profit factor, total return, the last 12 months and all but at most one of the non-2022 years; it still needs review before it goes live.

| Variant | Trades | Win % | PF | Return % | Max DD % | Sharpe | Last 12m n | Last 12m win % | Last 12m PF | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12 | 607 | 68.9 | 1.86 | 58.9 | 5.9 | 1.8 | 132 | 72.7 | 2.51 | champion |
| previous champion: A+E+F, SPY>200d, no breadth filter, no sector rank | 751 | 65.8 | 1.37 | 34.3 | 6.2 | 0.96 | 166 | 66.9 | 1.35 | better in 0/5 years |
| gate: strict bull regime | 562 | 66.9 | 1.46 | 30.5 | 5.2 | 1.08 | 89 | 68.5 | 1.51 | better in 1/5 years |
| gate: none (always on) | 857 | 65.5 | 1.28 | 30.9 | 8.7 | 0.78 | 173 | 66.5 | 1.32 | better in 1/5 years |
| hold 5 days | 769 | 63.7 | 1.31 | 29.8 | 8.0 | 0.79 | 168 | 62.5 | 1.21 | better in 0/5 years |
| hold 10 days | 740 | 67.2 | 1.41 | 37.4 | 7.4 | 0.97 | 165 | 67.9 | 1.43 | better in 1/5 years |
| stop 3 ATR | 759 | 65.7 | 1.36 | 34.9 | 6.5 | 0.94 | 169 | 67.5 | 1.36 | better in 0/5 years |
| stop 6 ATR | 748 | 65.8 | 1.4 | 36.9 | 6.0 | 1.05 | 166 | 66.9 | 1.42 | better in 0/5 years |
| exit: close > MA5 instead of prior high | 746 | 63.7 | 1.28 | 26.7 | 8.2 | 0.73 | 165 | 63.0 | 1.23 | better in 1/5 years |
| trend filter: only close > SMA200 | 1632 | 63.1 | 1.16 | 34.1 | 13.0 | 0.49 | 386 | 62.4 | 1.17 | better in 0/5 years |
| add rule G (3 down days) | 1555 | 64.0 | 1.15 | 29.6 | 9.7 | 0.59 | 347 | 64.8 | 1.16 | better in 0/5 years |
| A+E only | 583 | 64.5 | 1.37 | 25.1 | 4.9 | 0.99 | 128 | 68.0 | 1.62 | better in 1/5 years |
| hold 8 days | 744 | 66.7 | 1.39 | 36.3 | 7.3 | 0.99 | 165 | 67.9 | 1.4 | better in 1/5 years |
| hold 12 days | 738 | 67.3 | 1.4 | 37.0 | 7.5 | 0.95 | 165 | 67.9 | 1.39 | better in 1/5 years |
| hold 15 days | 737 | 67.4 | 1.4 | 37.3 | 7.5 | 0.96 | 165 | 67.9 | 1.39 | better in 1/5 years |
| hold 10 + strict bull gate | 557 | 68.0 | 1.46 | 30.8 | 7.1 | 1.0 | 88 | 69.3 | 1.58 | better in 2/5 years |
| hold 10 + stop 6 ATR | 737 | 67.2 | 1.45 | 40.4 | 7.4 | 1.06 | 164 | 67.7 | 1.51 | better in 1/5 years |
| A only | 421 | 65.6 | 1.44 | 19.1 | 3.9 | 1.05 | 84 | 75.0 | 1.78 | better in 1/5 years |
| A+E+F, 15 positions, 5/day | 765 | 65.9 | 1.43 | 32.5 | 5.0 | 1.09 | 168 | 66.7 | 1.4 | better in 0/5 years |
| size 8% x 10, 3/day | 724 | 65.2 | 1.36 | 25.1 | 4.9 | 0.95 | 160 | 65.6 | 1.3 | better in 1/5 years |
| size 12% x 10, 4/day | 741 | 65.6 | 1.37 | 42.6 | 7.5 | 0.96 | 165 | 66.7 | 1.35 | better in 0/5 years |
| lab: only if sector peers 3d < 0% | 626 | 66.9 | 1.62 | 45.8 | 5.3 | 1.34 | 142 | 69.7 | 1.7 | better in 1/5 years |
| lab: rank by weakest sector peers first | 751 | 66.6 | 1.46 | 44.0 | 6.5 | 1.14 | 167 | 68.3 | 1.42 | better in 0/5 years |
| lab: sector peers 3d < 0% and peers 20d > 0% | 360 | 68.3 | 1.93 | 36.2 | 3.5 | 1.55 | 78 | 70.5 | 2.11 | better in 3/5 years |
| lab: champion + sector-ETF rotation sleeve (top3 12-1m, monthly) | 915 | 64.6 | 1.53 | 79.1 | 7.9 | 1.28 | 193 | 65.3 | 1.45 | better in 1/5 years |
| lab: champion + bear-regime long sleeve (SPY<200d, stock>200d, rsi2<5) | 997 | 66.5 | 1.44 | 59.7 | 7.5 | 1.36 | 183 | 67.8 | 1.48 | better in 1/5 years |
| lab: only if >=10% of universe RSI2<10 (breadth washout) | 608 | 68.4 | 1.77 | 51.7 | 5.6 | 1.71 | 133 | 72.9 | 2.46 | better in 1/5 years |
| lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%) | 818 | 68.9 | 1.78 | 80.2 | 6.8 | 1.89 | 148 | 73.0 | 2.77 | better in 2/5 years |
| lab: live setup + only stocks with 60d daily vol >= 1.75% | 310 | 74.2 | 2.8 | 60.3 | 4.3 | 2.23 | 98 | 74.5 | 3.23 | PROMOTE-CANDIDATE |
| LAB run19: size 1.5x if SPY 3d<-1% else 0.5x (PF is size-weighted) | 751 | 65.8 | 1.67 | 48.2 | 7.3 | 1.33 | 166 | 66.9 | 1.79 | better in 2/5 years |
| LAB run19: size 1.25x if SPY 3d<-1% else 0.75x (PF is size-weighted) | 751 | 65.8 | 1.49 | 41.1 | 6.7 | 1.17 | 166 | 66.9 | 1.53 | better in 1/5 years |
| lab: live setup + vol60>=1.75%, size 15% x 8 | 310 | 74.2 | 2.8 | 102.4 | 6.4 | 2.23 | 98 | 74.5 | 3.23 | PROMOTE-CANDIDATE |
| lab run52: live vol60>=1.75% setup, size 1.25x if dispersion pct>=0.5 else 0.75x (PF size-weighted) | 310 | 74.2 | 3.1 | 69.8 | 3.9 | 2.27 | 98 | 74.5 | 3.6 | PROMOTE-CANDIDATE |
| lab run36: vol60>=1.75% setup, skip bottom-third 20d dollar volume | 257 | 75.9 | 3.25 | 57.4 | 3.4 | 2.34 | 81 | 76.5 | 4.28 | better in 5/5 years |

## Profit factor by year

| Variant | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12 | 1.89 | 0.13 | 1.42 | 2.19 | 1.92 | 2.55 |
| previous champion: A+E+F, SPY>200d, no breadth filter, no sector rank | 1.82 | 0.15 | 1.39 | 1.57 | 1.24 | 1.32 |
| gate: strict bull regime | 1.82 | 0.08 | 1.86 | 1.41 | 1.27 | 1.58 |
| gate: none (always on) | 1.82 | 0.55 | 1.54 | 1.57 | 1.19 | 1.29 |
| hold 5 days | 1.87 | 0.14 | 1.11 | 1.71 | 1.21 | 1.19 |
| hold 10 days | 2.1 | 0.15 | 1.27 | 1.63 | 1.27 | 1.4 |
| stop 3 ATR | 1.8 | 0.15 | 1.34 | 1.58 | 1.2 | 1.36 |
| stop 6 ATR | 1.86 | 0.15 | 1.41 | 1.58 | 1.25 | 1.39 |
| exit: close > MA5 instead of prior high | 1.97 | 0.12 | 1.0 | 1.55 | 1.29 | 1.22 |
| trend filter: only close > SMA200 | 1.32 | 0.14 | 1.22 | 1.37 | 1.03 | 1.24 |
| add rule G (3 down days) | 1.43 | 0.33 | 1.01 | 1.19 | 1.3 | 1.18 |
| A+E only | 1.48 | 0.07 | 1.57 | 1.38 | 1.61 | 1.45 |
| hold 8 days | 1.95 | 0.15 | 1.33 | 1.55 | 1.34 | 1.35 |
| hold 12 days | 2.0 | 0.15 | 1.34 | 1.62 | 1.26 | 1.37 |
| hold 15 days | 2.0 | 0.15 | 1.34 | 1.62 | 1.29 | 1.36 |
| hold 10 + strict bull gate | 2.06 | 0.07 | 1.63 | 1.39 | 1.34 | 1.6 |
| hold 10 + stop 6 ATR | 2.26 | 0.16 | 1.33 | 1.61 | 1.23 | 1.49 |
| A only | 1.72 | 0.12 | 1.58 | 1.43 | 1.52 | 1.57 |
| A+E+F, 15 positions, 5/day | 1.86 | 0.15 | 1.34 | 1.75 | 1.41 | 1.31 |
| size 8% x 10, 3/day | 1.79 | 0.18 | 1.47 | 1.5 | 1.24 | 1.28 |
| size 12% x 10, 4/day | 1.84 | 0.15 | 1.38 | 1.59 | 1.24 | 1.31 |
| lab: only if sector peers 3d < 0% | 2.05 | 0.19 | 1.32 | 2.02 | 1.64 | 1.62 |
| lab: rank by weakest sector peers first | 1.86 | 0.15 | 1.42 | 1.76 | 1.39 | 1.36 |
| lab: sector peers 3d < 0% and peers 20d > 0% | 2.23 | 0.16 | 1.84 | 2.27 | 1.87 | 1.87 |
| lab: champion + sector-ETF rotation sleeve (top3 12-1m, monthly) | 1.97 | 0.71 | 1.4 | 2.02 | 1.64 | 1.37 |
| lab: champion + bear-regime long sleeve (SPY<200d, stock>200d, rsi2<5) | 1.82 | 1.2 | 1.6 | 1.57 | 1.21 | 1.47 |
| lab: only if >=10% of universe RSI2<10 (breadth washout) | 2.04 | 0.13 | 1.35 | 1.93 | 1.71 | 2.53 |
| lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%) | 1.89 | 1.07 | 1.5 | 2.19 | 1.92 | 2.88 |
| lab: live setup + only stocks with 60d daily vol >= 1.75% | 2.41 | 0.87 | 1.62 | 4.74 | 2.51 | 3.26 |
| LAB run19: size 1.5x if SPY 3d<-1% else 0.5x (PF is size-weighted) | 2.85 | 0.1 | 1.14 | 2.24 | 1.53 | 1.82 |
| LAB run19: size 1.25x if SPY 3d<-1% else 0.75x (PF is size-weighted) | 2.19 | 0.12 | 1.27 | 1.82 | 1.37 | 1.51 |
| lab: live setup + vol60>=1.75%, size 15% x 8 | 2.41 | 0.87 | 1.62 | 4.74 | 2.51 | 3.26 |
| lab run52: live vol60>=1.75% setup, size 1.25x if dispersion pct>=0.5 else 0.75x (PF size-weighted) | 2.93 | 0.87 | 1.78 | 5.3 | 2.58 | 3.54 |
| lab run36: vol60>=1.75% setup, skip bottom-third 20d dollar volume | 2.71 | 0.87 | 2.04 | 5.41 | 2.4 | 4.71 |
