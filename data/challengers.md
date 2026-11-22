# Champion vs challengers (data through 2026-11-20)

Backtests only. The live bot is **not** changed by this file. A challenger marked PROMOTE-CANDIDATE beat the champion on profit factor, total return, the last 12 months and all but at most one of the non-2022 years; it still needs review before it goes live.

| Variant | Trades | Win % | PF | Return % | Max DD % | Sharpe | Last 12m n | Last 12m win % | Last 12m PF | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12 | 313 | 73.5 | 2.64 | 57.6 | 4.3 | 2.09 | 94 | 74.5 | 3.21 | champion |
| previous champion: live setup without the volatility filter | 610 | 68.5 | 1.81 | 56.6 | 5.9 | 1.71 | 127 | 73.2 | 2.53 | better in 0/5 years |
| previous champion: A+E+F, SPY>200d, no breadth filter, no sector rank | 754 | 65.5 | 1.34 | 32.1 | 6.2 | 0.89 | 161 | 67.1 | 1.33 | better in 0/5 years |
| gate: strict bull regime | 562 | 66.9 | 1.46 | 30.5 | 5.2 | 1.08 | 87 | 70.1 | 1.54 | better in 1/5 years |
| gate: none (always on) | 862 | 65.2 | 1.25 | 28.0 | 8.7 | 0.7 | 170 | 66.5 | 1.27 | better in 0/5 years |
| hold 5 days | 772 | 63.5 | 1.29 | 27.7 | 8.0 | 0.72 | 163 | 62.6 | 1.2 | better in 0/5 years |
| hold 10 days | 743 | 66.9 | 1.38 | 35.1 | 7.4 | 0.9 | 160 | 68.1 | 1.42 | better in 0/5 years |
| stop 3 ATR | 762 | 65.5 | 1.33 | 32.7 | 6.5 | 0.87 | 164 | 67.7 | 1.35 | better in 0/5 years |
| stop 6 ATR | 751 | 65.5 | 1.37 | 34.6 | 6.0 | 0.98 | 161 | 67.1 | 1.39 | better in 0/5 years |
| exit: close > MA5 instead of prior high | 749 | 63.4 | 1.26 | 24.6 | 8.2 | 0.67 | 160 | 63.1 | 1.21 | better in 0/5 years |
| trend filter: only close > SMA200 | 1640 | 62.8 | 1.13 | 27.9 | 13.0 | 0.4 | 383 | 62.4 | 1.14 | better in 0/5 years |
| add rule G (3 down days) | 1560 | 63.7 | 1.13 | 24.9 | 9.7 | 0.49 | 338 | 64.5 | 1.12 | better in 0/5 years |
| A+E only | 584 | 64.4 | 1.36 | 24.4 | 4.9 | 0.96 | 123 | 68.3 | 1.55 | better in 0/5 years |
| hold 8 days | 747 | 66.4 | 1.36 | 34.1 | 7.3 | 0.91 | 160 | 68.1 | 1.38 | better in 0/5 years |
| hold 12 days | 741 | 67.1 | 1.37 | 34.7 | 7.5 | 0.88 | 160 | 68.1 | 1.39 | better in 0/5 years |
| hold 15 days | 740 | 67.2 | 1.37 | 35.0 | 7.5 | 0.89 | 160 | 68.1 | 1.39 | better in 0/5 years |
| hold 10 + strict bull gate | 557 | 68.0 | 1.46 | 30.8 | 7.1 | 1.0 | 86 | 70.9 | 1.62 | better in 1/5 years |
| hold 10 + stop 6 ATR | 740 | 66.9 | 1.41 | 38.1 | 7.4 | 0.99 | 159 | 67.9 | 1.5 | better in 0/5 years |
| A only | 422 | 65.4 | 1.42 | 18.4 | 3.9 | 1.0 | 82 | 74.4 | 1.6 | better in 0/5 years |
| A+E+F, 15 positions, 5/day | 768 | 65.6 | 1.4 | 30.8 | 5.0 | 1.02 | 163 | 66.9 | 1.38 | better in 0/5 years |
| size 8% x 10, 3/day | 727 | 64.9 | 1.33 | 23.4 | 4.9 | 0.87 | 155 | 65.8 | 1.28 | better in 0/5 years |
| size 12% x 10, 4/day | 744 | 65.3 | 1.34 | 39.7 | 7.5 | 0.89 | 160 | 66.9 | 1.32 | better in 0/5 years |
| lab: only if sector peers 3d < 0% | 629 | 66.6 | 1.58 | 43.4 | 5.3 | 1.26 | 137 | 70.1 | 1.67 | better in 0/5 years |
| lab: rank by weakest sector peers first | 754 | 66.3 | 1.43 | 41.9 | 6.5 | 1.08 | 162 | 68.5 | 1.41 | better in 0/5 years |
| lab: sector peers 3d < 0% and peers 20d > 0% | 364 | 67.9 | 1.84 | 34.3 | 3.5 | 1.43 | 79 | 70.9 | 1.92 | better in 1/5 years |
| lab: champion + sector-ETF rotation sleeve (top3 12-1m, monthly) | 918 | 64.4 | 1.51 | 76.2 | 7.9 | 1.23 | 188 | 65.4 | 1.44 | better in 0/5 years |
| lab: champion + bear-regime long sleeve (SPY<200d, stock>200d, rsi2<5) | 1004 | 66.2 | 1.41 | 55.8 | 7.5 | 1.24 | 182 | 67.6 | 1.41 | better in 0/5 years |
| lab: only if >=10% of universe RSI2<10 (breadth washout) | 611 | 68.1 | 1.72 | 49.2 | 5.6 | 1.6 | 128 | 73.4 | 2.43 | better in 0/5 years |
| lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%) | 825 | 68.5 | 1.72 | 75.8 | 6.8 | 1.76 | 147 | 72.1 | 2.58 | better in 0/5 years |
| LAB run19: size 1.5x if SPY 3d<-1% else 0.5x (PF is size-weighted) | 754 | 65.5 | 1.6 | 44.6 | 7.3 | 1.21 | 161 | 67.1 | 1.74 | better in 1/5 years |
| LAB run19: size 1.25x if SPY 3d<-1% else 0.75x (PF is size-weighted) | 754 | 65.5 | 1.45 | 38.2 | 6.7 | 1.07 | 161 | 67.1 | 1.5 | better in 0/5 years |
| lab: live setup + vol60>=1.75%, size 15% x 8 | 313 | 73.5 | 2.64 | 97.4 | 6.4 | 2.09 | 94 | 74.5 | 3.21 | better in 0/5 years |
| lab run52: live vol60>=1.75% setup, size 1.25x if dispersion pct>=0.5 else 0.75x (PF size-weighted) | 313 | 73.5 | 2.92 | 67.2 | 3.9 | 2.15 | 94 | 74.5 | 3.51 | PROMOTE-CANDIDATE |
| lab run30: live vol60>=1.75% setup, size 1.25x if SPY day IBS<0.3 else 0.75x (PF size-weighted) | 313 | 73.5 | 3.02 | 64.6 | 3.3 | 2.18 | 94 | 74.5 | 3.5 | PROMOTE-CANDIDATE |
| lab run57: live vol60>=1.75% setup, size 1.25x if SPY day volume >=1.1x its 20d avg else 0.75x (PF size-weighted) | 313 | 73.5 | 2.87 | 62.3 | 3.6 | 2.16 | 94 | 74.5 | 3.14 | better in 4/5 years |
| lab run58: live vol60>=1.75% setup, STACKED 3 tilts (disp pct>=0.5, SPY IBS<0.3, SPY vol ratio>=1.1; each 1.25x/0.75x, multiplied; PF size-weighted) | 313 | 73.5 | 3.65 | 83.7 | 2.8 | 2.14 | 94 | 74.5 | 3.84 | PROMOTE-CANDIDATE |
| lab run59: live vol60>=1.75% setup, STACKED 3 tilts with multiplier CLIPPED to 0.5-1.5x (PF size-weighted) | 313 | 73.5 | 3.38 | 70.2 | 2.7 | 2.22 | 94 | 74.5 | 3.7 | PROMOTE-CANDIDATE |
| lab run31: live vol60>=1.75% setup, STACKED tilts (disp pct>=0.5 and SPY IBS<0.3, each 1.25x/0.75x, multiplied; PF size-weighted) | 313 | 73.5 | 3.36 | 76.0 | 3.0 | 2.19 | 94 | 74.5 | 3.86 | PROMOTE-CANDIDATE |
| lab run36: vol60>=1.75% setup, skip bottom-third 20d dollar volume | 258 | 75.6 | 3.16 | 56.5 | 3.4 | 2.28 | 75 | 78.7 | 5.34 | better in 4/5 years |
| lab run44: vol60>=1.75% setup, 20d regression-residual z < -1.5 | 243 | 77.4 | 3.89 | 60.5 | 2.5 | 2.45 | 75 | 74.7 | 3.72 | PROMOTE-CANDIDATE |
| lab run52b: live vol60>=1.75% setup + contraction D20 breakout sleeve (r10<=0.8*r60, vol>1.5x, hold 10) | 434 | 68.4 | 2.23 | 89.4 | 4.4 | 2.08 | 119 | 68.1 | 2.28 | better in 1/5 years |

## Profit factor by year

| Variant | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|
| CHAMPION (live): A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, vol60>=1.75%, hold 7, stop 4 ATR, 10% x 12 | 2.41 | 0.87 | 1.62 | 4.74 | 2.51 | 2.58 |
| previous champion: live setup without the volatility filter | 1.89 | 0.13 | 1.42 | 2.19 | 1.92 | 2.21 |
| previous champion: A+E+F, SPY>200d, no breadth filter, no sector rank | 1.82 | 0.15 | 1.39 | 1.57 | 1.24 | 1.22 |
| gate: strict bull regime | 1.82 | 0.08 | 1.86 | 1.41 | 1.27 | 1.58 |
| gate: none (always on) | 1.82 | 0.55 | 1.54 | 1.57 | 1.19 | 1.17 |
| hold 5 days | 1.87 | 0.14 | 1.11 | 1.71 | 1.21 | 1.1 |
| hold 10 days | 2.1 | 0.15 | 1.27 | 1.63 | 1.27 | 1.29 |
| stop 3 ATR | 1.8 | 0.15 | 1.34 | 1.58 | 1.2 | 1.26 |
| stop 6 ATR | 1.86 | 0.15 | 1.41 | 1.58 | 1.25 | 1.29 |
| exit: close > MA5 instead of prior high | 1.97 | 0.12 | 1.0 | 1.55 | 1.29 | 1.13 |
| trend filter: only close > SMA200 | 1.33 | 0.14 | 1.22 | 1.37 | 1.03 | 1.12 |
| add rule G (3 down days) | 1.42 | 0.33 | 1.01 | 1.19 | 1.3 | 1.08 |
| A+E only | 1.48 | 0.07 | 1.57 | 1.38 | 1.61 | 1.39 |
| hold 8 days | 1.95 | 0.15 | 1.33 | 1.55 | 1.34 | 1.25 |
| hold 12 days | 2.0 | 0.15 | 1.34 | 1.62 | 1.26 | 1.26 |
| hold 15 days | 2.0 | 0.15 | 1.34 | 1.62 | 1.29 | 1.26 |
| hold 10 + strict bull gate | 2.06 | 0.07 | 1.63 | 1.39 | 1.34 | 1.6 |
| hold 10 + stop 6 ATR | 2.26 | 0.16 | 1.33 | 1.61 | 1.23 | 1.37 |
| A only | 1.72 | 0.12 | 1.58 | 1.43 | 1.52 | 1.45 |
| A+E+F, 15 positions, 5/day | 1.86 | 0.15 | 1.34 | 1.75 | 1.41 | 1.21 |
| size 8% x 10, 3/day | 1.79 | 0.18 | 1.47 | 1.5 | 1.24 | 1.19 |
| size 12% x 10, 4/day | 1.84 | 0.15 | 1.38 | 1.59 | 1.24 | 1.22 |
| lab: only if sector peers 3d < 0% | 2.05 | 0.19 | 1.32 | 2.02 | 1.64 | 1.46 |
| lab: rank by weakest sector peers first | 1.86 | 0.15 | 1.42 | 1.76 | 1.39 | 1.27 |
| lab: sector peers 3d < 0% and peers 20d > 0% | 2.23 | 0.16 | 1.84 | 2.27 | 1.87 | 1.58 |
| lab: champion + sector-ETF rotation sleeve (top3 12-1m, monthly) | 1.97 | 0.71 | 1.4 | 2.02 | 1.64 | 1.3 |
| lab: champion + bear-regime long sleeve (SPY<200d, stock>200d, rsi2<5) | 1.82 | 1.2 | 1.6 | 1.57 | 1.21 | 1.32 |
| lab: only if >=10% of universe RSI2<10 (breadth washout) | 2.04 | 0.13 | 1.35 | 1.93 | 1.71 | 2.16 |
| lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%) | 1.89 | 1.07 | 1.5 | 2.19 | 1.92 | 2.3 |
| LAB run19: size 1.5x if SPY 3d<-1% else 0.5x (PF is size-weighted) | 2.85 | 0.1 | 1.14 | 2.24 | 1.53 | 1.53 |
| LAB run19: size 1.25x if SPY 3d<-1% else 0.75x (PF is size-weighted) | 2.19 | 0.12 | 1.27 | 1.82 | 1.37 | 1.35 |
| lab: live setup + vol60>=1.75%, size 15% x 8 | 2.41 | 0.87 | 1.62 | 4.74 | 2.51 | 2.58 |
| lab run52: live vol60>=1.75% setup, size 1.25x if dispersion pct>=0.5 else 0.75x (PF size-weighted) | 2.93 | 0.87 | 1.78 | 5.3 | 2.58 | 2.86 |
| lab run30: live vol60>=1.75% setup, size 1.25x if SPY day IBS<0.3 else 0.75x (PF size-weighted) | 2.96 | 0.95 | 2.18 | 5.2 | 2.87 | 2.66 |
| lab run57: live vol60>=1.75% setup, size 1.25x if SPY day volume >=1.1x its 20d avg else 0.75x (PF size-weighted) | 2.95 | 1.37 | 1.98 | 5.03 | 2.74 | 2.51 |
| lab run58: live vol60>=1.75% setup, STACKED 3 tilts (disp pct>=0.5, SPY IBS<0.3, SPY vol ratio>=1.1; each 1.25x/0.75x, multiplied; PF size-weighted) | 4.37 | 1.45 | 3.08 | 6.24 | 3.05 | 2.98 |
| lab run59: live vol60>=1.75% setup, STACKED 3 tilts with multiplier CLIPPED to 0.5-1.5x (PF size-weighted) | 3.79 | 1.45 | 2.53 | 5.69 | 3.05 | 2.88 |
| lab run31: live vol60>=1.75% setup, STACKED tilts (disp pct>=0.5 and SPY IBS<0.3, each 1.25x/0.75x, multiplied; PF size-weighted) | 3.74 | 0.95 | 2.44 | 5.85 | 2.9 | 3.0 |
| lab run36: vol60>=1.75% setup, skip bottom-third 20d dollar volume | 2.71 | 0.87 | 2.04 | 5.41 | 2.4 | 4.1 |
| lab run44: vol60>=1.75% setup, 20d regression-residual z < -1.5 | 4.11 | 0.12 | 2.7 | 11.74 | 3.1 | 3.13 |
| lab run52b: live vol60>=1.75% setup + contraction D20 breakout sleeve (r10<=0.8*r60, vol>1.5x, hold 10) | 2.33 | 1.27 | 2.08 | 2.8 | 2.31 | 2.01 |
