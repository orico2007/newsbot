# Research (walk-forward, 3 periods) - 6y daily, 40 symbols

Signals: 70846. **A** (before 2024-01-26) = choose, **B** (2024-01-26 to 2025-06-17) = confirm, **C** (after 2025-06-17) = holdout: never used for choosing, so it is the honest estimate. Past results do not guarantee future results.

## Honest result: holdout period C (never used to choose anything)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| baseline longs | 4843 | 48.1 | 0.012 | 0.143 | 1.03 |
| baseline shorts | 6387 | 40.6 | -0.135 | -0.689 | 0.76 |
| + filters longs | 2395 | 47.8 | 0.017 | 0.17 | 1.04 |
| + filters shorts | 6387 | 40.6 | -0.135 | -0.689 | 0.76 |
| **FINAL: filters + validated patterns** | 706 | 44.5 | -0.058 | -0.191 | 0.88 |
| FINAL longs | 499 | 46.9 | -0.013 | 0.105 | 0.97 |
| FINAL shorts | 207 | 38.6 | -0.167 | -0.902 | 0.74 |

## Same sets on earlier periods (selection bias makes A and B look better than reality)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| FINAL on A (chosen on this) | 1446 | 55.6 | 0.19 | 0.965 | 1.51 |
| FINAL on B (confirmation) | 721 | 50.3 | 0.136 | 0.429 | 1.31 |

## Variants compared on the holdout (alpha = trade return minus what SPY did over the same days; positive = beats just holding the market)

| Variant | Trades | Win % | Avg R | Avg % | Alpha % | Profit factor |
|---|---|---|---|---|---|---|
| all longs | 4843 | 48.1 | 0.012 | 0.143 | -0.204 | 1.03 |
| all shorts | 6387 | 40.6 | -0.135 | -0.689 | -0.278 | 0.76 |
| longs, market not bearish | 4712 | 47.8 | 0.004 | 0.091 | -0.178 | 1.01 |
| longs, market bullish only | 3349 | 48.5 | 0.006 | 0.103 | -0.226 | 1.01 |
| longs minus blacklisted patterns | 4435 | 48.8 | 0.019 | 0.176 | -0.175 | 1.04 |
| longs minus blacklist, market not bearish | 4312 | 48.5 | 0.012 | 0.12 | -0.148 | 1.03 |
| longs, high-volume only (rvol>=1.26) | 1921 | 49.8 | 0.034 | 0.4 | -0.041 | 1.08 |
| whitelist (validated patterns) longs | 499 | 46.9 | -0.013 | 0.105 | -0.222 | 0.97 |

Blacklist (lost on both A and B): adx_pullback:short, avwap_reclaim:short, base_breakout:short, bb_lower_bounce:short, bb_upper_fade:short, bear_divergence:short, bear_flag:short, bearish_engulfing_top:short, blowoff_top:short, bollinger_squeeze:short, breakdown_support:short, breakout_retest:short, bullish_engulfing_support:short, bullish_harami_support:short, channel_bounce:short, cup_handle:short, death_cross:short, donchian20:short, donchian55:short, double_bottom:short, down_trendline_break:short, ema21_bounce:short, ema21_rejection:short, evening_star:short, gap_up_hold:short, golden_cross:short, higher_low_breakout:short, ibs_reversion:short, ichimoku_breakout:short, inside_bar_breakout:short, keltner_thrust:short, level_bounce:short, low52_breakdown:short, lower_low_breakdown:short, macd_bear_cross:short, morning_star:short, nr7_breakout:long, nr7_breakout:short, outside_day_reversal:short, oversold_atr_stretch:short, piercing_line:short, pullback_reversal_day:short, range_breakdown:short, rising_wedge:short, rsi2_overbought:short, rsi2_reversion:short, rsi_divergence:short, sma200_reclaim:short, sma50_bounce:long, sma50_bounce:short, sma50_rejection:short, spring_reversal:short, three_inside_up:short, three_line_strike_bull:short, tight_closes_breakout:short, trend_pullback:long, triple_bottom:short, ttm_squeeze:short, tweezer_bottom:short, upthrust:short

## Feature filters chosen (improve A and confirmed on B)

- long: ret5 >= -0.25
- short: none

## Validated patterns (15) - good on A and confirmed on B

| Pattern:side | A n | A PF | B n | B PF | B win % | B avg R | Regimes | Size x |
|---|---|---|---|---|---|---|---|---|
| breakout_retest:long | 93 | 1.6 | 35 | 2.02 | 65.7 | 0.367 | bull,bear | 1.25 |
| golden_cross:long | 34 | 2.16 | 15 | 3.61 | 66.7 | 0.361 | bull,neutral | 1.25 |
| pullback_reversal_day:long | 58 | 1.41 | 33 | 2.08 | 63.6 | 0.322 | bull,bear,neutral | 1.25 |
| down_trendline_break:long | 60 | 1.97 | 22 | 1.56 | 54.5 | 0.23 | bull,bear,neutral | 1.25 |
| channel_bounce:long | 80 | 1.33 | 33 | 1.42 | 48.5 | 0.199 | bull,neutral | 1.0 |
| keltner_thrust:long | 58 | 1.64 | 29 | 1.47 | 58.6 | 0.199 | bull,neutral | 1.0 |
| tight_closes_breakout:long | 188 | 1.17 | 107 | 1.43 | 49.5 | 0.168 | bull | 1.0 |
| momentum_burst:short | 112 | 1.16 | 83 | 1.3 | 44.6 | 0.158 | bull,bear,neutral | 1.0 |
| pocket_pivot:short | 192 | 1.24 | 68 | 1.22 | 44.1 | 0.114 | bull,bear,neutral | 1.0 |
| level_bounce:long | 77 | 1.62 | 38 | 1.19 | 55.3 | 0.106 | bull,bear,neutral | 0.75 |
| avwap_reclaim:long | 54 | 1.71 | 18 | 1.15 | 38.9 | 0.08 | bull,bear | 0.75 |
| stoch_oversold:long | 24 | 3.09 | 14 | 1.07 | 42.9 | 0.043 | bull | 0.75 |
| donchian55:long | 214 | 1.75 | 111 | 1.11 | 50.5 | 0.038 | bull,bear,neutral | 0.75 |
| base_breakout:long | 208 | 1.41 | 101 | 1.08 | 51.5 | 0.03 | bull,bear,neutral | 0.75 |
| stoch_overbought_cross:short | 173 | 1.32 | 96 | 1.05 | 44.8 | 0.029 | bear,neutral | 0.75 |

## Exit tuning

Best on A: stop=atr3.0, target=none, hold=10d, scale=off
- avg % per trade: A 1.135 | B 0.264 vs default 0.429 | holdout C 0.122 vs default -0.191
- adopted by the bot: no (did not beat the default exits on B and C)