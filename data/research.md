# Research (walk-forward, 3 periods) - 6y daily, 126 symbols

Signals: 142832. **A** (before 2023-02-08) = choose, **B** (2023-02-08 to 2024-01-10) = confirm, **C** (after 2024-01-10) = holdout: never used for choosing, so it is the honest estimate. Past results do not guarantee future results.

## Honest result: holdout period C (never used to choose anything)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| baseline longs | 9543 | 52.9 | 0.085 | 0.277 | 1.2 |
| baseline shorts | 10002 | 36.8 | -0.209 | -0.683 | 0.65 |
| + filters longs | 2701 | 51.8 | 0.064 | 0.119 | 1.16 |
| + filters shorts | 10002 | 36.8 | -0.209 | -0.683 | 0.65 |
| **FINAL: filters + validated patterns** | 520 | 50.6 | 0.069 | 0.058 | 1.17 |
| FINAL longs | 514 | 50.2 | 0.065 | 0.047 | 1.16 |
| FINAL shorts | 6 | 83.3 | 0.45 | 0.986 | 12.04 |

## Same sets on earlier periods (selection bias makes A and B look better than reality)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| FINAL on A (chosen on this) | 899 | 53.6 | 0.134 | 0.694 | 1.37 |
| FINAL on B (confirmation) | 639 | 56.2 | 0.124 | 0.716 | 1.38 |

## Feature filters chosen (improve A and confirmed on B)

- long: ret5 >= -0.177, rvol >= 1.261
- short: none

## Validated patterns (11) - good on A and confirmed on B

| Pattern:side | A n | A PF | B n | B PF | B win % | B avg R | Regimes | Size x |
|---|---|---|---|---|---|---|---|---|
| macd_pullback:long | 26 | 1.44 | 14 | 4.21 | 64.3 | 0.404 | bear | 1.25 |
| level_bounce:long | 28 | 1.41 | 16 | 1.77 | 56.2 | 0.332 | bull,bear | 1.25 |
| three_line_strike_bull:long | 27 | 2.39 | 14 | 2.08 | 50.0 | 0.32 | bull | 1.25 |
| three_inside_up:long | 20 | 1.29 | 9 | 1.69 | 55.6 | 0.255 | bull | 1.25 |
| outside_day_reversal:long | 25 | 2.21 | 12 | 1.89 | 66.7 | 0.243 | bull,neutral | 1.25 |
| keltner_thrust:long | 81 | 1.81 | 60 | 1.66 | 58.3 | 0.174 | bull,bear,neutral | 1.25 |
| momentum_burst:long | 161 | 1.31 | 119 | 1.33 | 51.3 | 0.124 | bull,bear,neutral | 1.0 |
| bollinger_squeeze:long | 136 | 1.24 | 107 | 1.24 | 51.4 | 0.095 | bull,bear | 1.0 |
| down_trendline_break:long | 86 | 1.76 | 63 | 1.24 | 54.0 | 0.091 | bull,bear,neutral | 1.0 |
| volume_climax_top:short | 23 | 1.7 | 17 | 1.18 | 52.9 | 0.068 | bull | 0.75 |
| base_breakout:long | 386 | 1.18 | 258 | 1.17 | 57.8 | 0.054 | bull,bear,neutral | 0.75 |

## Exit tuning

Best on A: stop=atr3.0, target=r2.0, hold=10d, scale=off
- avg % per trade: A 0.958 | B 0.935 vs default 0.716 | holdout C -0.234 vs default 0.058
- adopted by the bot: no (did not beat the default exits on B and C)