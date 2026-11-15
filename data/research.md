# Research (walk-forward, 3 periods) - 6y daily, 40 symbols

Signals: 70840. **A** (before 2024-02-02) = choose, **B** (2024-02-02 to 2025-06-25) = confirm, **C** (after 2025-06-25) = holdout: never used for choosing, so it is the honest estimate. Past results do not guarantee future results.

## Honest result: holdout period C (never used to choose anything)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| baseline longs | 4785 | 47.7 | -0.001 | 0.107 | 1.0 |
| baseline shorts | 6408 | 40.6 | -0.132 | -0.698 | 0.77 |
| + filters longs | 2306 | 49.7 | 0.043 | 0.199 | 1.1 |
| + filters shorts | 6408 | 40.6 | -0.132 | -0.698 | 0.77 |
| **FINAL: filters + validated patterns** | 569 | 46.9 | -0.011 | -0.054 | 0.98 |
| FINAL longs | 424 | 49.1 | 0.016 | 0.156 | 1.04 |
| FINAL shorts | 145 | 40.7 | -0.089 | -0.668 | 0.86 |

## Same sets on earlier periods (selection bias makes A and B look better than reality)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| FINAL on A (chosen on this) | 1245 | 56.5 | 0.179 | 1.008 | 1.49 |
| FINAL on B (confirmation) | 596 | 50.0 | 0.096 | 0.17 | 1.23 |

## Variants compared on the holdout (alpha = trade return minus what SPY did over the same days; positive = beats just holding the market)

| Variant | Trades | Win % | Avg R | Avg % | Alpha % | Profit factor |
|---|---|---|---|---|---|---|
| all longs | 4785 | 47.7 | -0.001 | 0.107 | -0.222 | 1.0 |
| all shorts | 6408 | 40.6 | -0.132 | -0.698 | -0.264 | 0.77 |
| longs, market not bearish | 4654 | 47.3 | -0.009 | 0.053 | -0.196 | 0.98 |
| longs, market bullish only | 3245 | 47.3 | -0.02 | 0.01 | -0.244 | 0.96 |
| longs minus blacklisted patterns | 4379 | 48.4 | 0.007 | 0.143 | -0.191 | 1.02 |
| longs minus blacklist, market not bearish | 4256 | 48.0 | -0.0 | 0.087 | -0.165 | 1.0 |
| longs, high-volume only (rvol>=1.26) | 1894 | 50.0 | 0.036 | 0.418 | -0.047 | 1.08 |
| whitelist (validated patterns) longs | 424 | 49.1 | 0.016 | 0.156 | -0.181 | 1.04 |

Blacklist (lost on both A and B): adx_pullback:short, avwap_reclaim:short, base_breakout:short, bb_lower_bounce:short, bb_upper_fade:short, bear_divergence:short, bear_flag:short, bearish_engulfing_top:short, blowoff_top:short, bollinger_squeeze:short, breakdown_support:short, breakout_retest:short, bullish_engulfing_support:short, bullish_harami_support:short, channel_bounce:short, cup_handle:short, death_cross:short, donchian20:short, donchian55:short, double_bottom:short, down_trendline_break:short, ema21_rejection:short, evening_star:short, fib_pullback:short, gap_up_hold:short, golden_cross:short, higher_low_breakout:short, ibs_reversion:short, ichimoku_breakout:short, inside_bar_breakout:short, keltner_thrust:short, level_bounce:short, low52_breakdown:short, lower_low_breakdown:short, macd_bear_cross:short, morning_star:short, nr7_breakout:long, nr7_breakout:short, outside_day_reversal:short, oversold_atr_stretch:short, piercing_line:short, pullback_reversal_day:short, range_breakdown:short, rising_wedge:short, rsi2_overbought:short, rsi2_reversion:short, rsi_divergence:short, rsi_oversold_uptrend:short, runaway_gap:short, sma200_reclaim:short, sma50_bounce:long, sma50_bounce:short, sma50_rejection:short, spring_reversal:short, three_inside_up:short, three_line_strike_bull:short, tight_closes_breakout:short, trend_pullback:long, triple_bottom:short, ttm_squeeze:short, tweezer_bottom:short, upthrust:short

## Feature filters chosen (improve A and confirmed on B)

- long: pos20 >= 0.59
- short: none

## Validated patterns (13) - good on A and confirmed on B

| Pattern:side | A n | A PF | B n | B PF | B win % | B avg R | Regimes | Size x |
|---|---|---|---|---|---|---|---|---|
| breakout_retest:long | 92 | 1.32 | 35 | 2.25 | 65.7 | 0.421 | bull,neutral | 1.25 |
| golden_cross:long | 32 | 1.75 | 17 | 2.95 | 64.7 | 0.357 | bull,neutral | 1.25 |
| keltner_thrust:long | 59 | 1.4 | 30 | 1.51 | 60.0 | 0.205 | bull,neutral | 1.25 |
| tight_closes_breakout:long | 192 | 1.22 | 104 | 1.38 | 49.0 | 0.149 | bull | 1.0 |
| three_line_strike_bull:long | 42 | 1.46 | 14 | 1.32 | 42.9 | 0.139 | bull | 1.0 |
| channel_bounce:long | 79 | 1.36 | 36 | 1.25 | 47.2 | 0.128 | bull,neutral | 1.0 |
| pocket_pivot:short | 194 | 1.23 | 70 | 1.15 | 42.9 | 0.082 | bull,bear,neutral | 0.75 |
| fib_pullback:long | 37 | 1.44 | 27 | 1.19 | 59.3 | 0.076 | bull,neutral | 0.75 |
| donchian55:long | 215 | 1.8 | 111 | 1.11 | 50.5 | 0.039 | bull,bear,neutral | 0.75 |
| avwap_reclaim:long | 39 | 1.5 | 16 | 1.06 | 43.8 | 0.03 | bull,bear | 0.75 |
| stoch_overbought_cross:short | 173 | 1.32 | 96 | 1.05 | 44.8 | 0.029 | bear,neutral | 0.75 |
| base_breakout:long | 208 | 1.43 | 102 | 1.08 | 52.0 | 0.028 | bull,bear,neutral | 0.75 |
| down_trendline_break:long | 38 | 3.26 | 17 | 1.06 | 52.9 | 0.026 | bull,neutral | 0.75 |

## Exit tuning

Best on A: stop=atr3.0, target=none, hold=20d, scale=off
- avg % per trade: A 1.628 | B 0.568 vs default 0.17 | holdout C 0.5 vs default -0.054
- adopted by the bot: yes