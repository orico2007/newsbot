# Research (walk-forward, 3 periods) - 6y daily, 40 symbols

Signals: 70762. **A** (before 2024-01-19) = choose, **B** (2024-01-19 to 2025-06-10) = confirm, **C** (after 2025-06-10) = holdout: never used for choosing, so it is the honest estimate. Past results do not guarantee future results.

## Honest result: holdout period C (never used to choose anything)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| baseline longs | 4805 | 48.6 | 0.019 | 0.209 | 1.04 |
| baseline shorts | 6365 | 40.5 | -0.14 | -0.73 | 0.75 |
| + filters longs | 2378 | 48.9 | 0.035 | 0.27 | 1.08 |
| + filters shorts | 6365 | 40.5 | -0.14 | -0.73 | 0.75 |
| **FINAL: filters + validated patterns** | 856 | 46.5 | -0.021 | 0.036 | 0.95 |
| FINAL longs | 651 | 49.0 | 0.027 | 0.345 | 1.07 |
| FINAL shorts | 205 | 38.5 | -0.172 | -0.944 | 0.73 |

## Same sets on earlier periods (selection bias makes A and B look better than reality)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| FINAL on A (chosen on this) | 1785 | 56.2 | 0.179 | 0.991 | 1.51 |
| FINAL on B (confirmation) | 951 | 50.4 | 0.108 | 0.289 | 1.26 |

## Variants compared on the holdout (alpha = trade return minus what SPY did over the same days; positive = beats just holding the market)

| Variant | Trades | Win % | Avg R | Avg % | Alpha % | Profit factor |
|---|---|---|---|---|---|---|
| all longs | 4805 | 48.6 | 0.019 | 0.209 | -0.218 | 1.04 |
| all shorts | 6365 | 40.5 | -0.14 | -0.73 | -0.271 | 0.75 |
| longs, market not bearish | 4674 | 48.3 | 0.012 | 0.158 | -0.193 | 1.03 |
| longs, market bullish only | 3420 | 48.5 | 0.005 | 0.109 | -0.226 | 1.01 |
| longs minus blacklisted patterns | 4394 | 49.3 | 0.027 | 0.244 | -0.192 | 1.06 |
| longs minus blacklist, market not bearish | 4271 | 49.0 | 0.02 | 0.19 | -0.166 | 1.04 |
| longs, high-volume only (rvol>=1.26) | 1867 | 51.0 | 0.051 | 0.54 | -0.066 | 1.12 |
| whitelist (validated patterns) longs | 651 | 49.0 | 0.027 | 0.345 | -0.187 | 1.07 |

Blacklist (lost on both A and B): adx_pullback:short, avwap_reclaim:short, base_breakout:short, bb_lower_bounce:short, bb_upper_fade:short, bear_divergence:short, bear_flag:short, bearish_engulfing_top:short, blowoff_top:short, bollinger_squeeze:short, breakdown_support:short, breakout_retest:short, bullish_engulfing_support:short, bullish_harami_support:short, channel_bounce:short, cup_handle:short, death_cross:short, donchian20:short, donchian55:short, double_bottom:short, down_trendline_break:short, ema21_bounce:short, ema21_rejection:short, evening_star:short, gap_up_hold:short, golden_cross:short, higher_low_breakout:short, ibs_reversion:short, ichimoku_breakout:short, inside_bar_breakout:short, keltner_thrust:short, level_bounce:short, low52_breakdown:short, lower_low_breakdown:short, macd_bear_cross:short, morning_star:short, nr7_breakout:long, nr7_breakout:short, outside_day_reversal:short, oversold_atr_stretch:short, piercing_line:short, pullback_reversal_day:short, range_breakdown:short, rising_wedge:short, rsi2_overbought:short, rsi2_reversion:short, rsi_divergence:short, runaway_gap:short, sma200_reclaim:short, sma50_bounce:long, sma50_bounce:short, sma50_rejection:short, spring_reversal:short, three_inside_up:short, three_line_strike_bull:short, tight_closes_breakout:short, trend_pullback:long, triple_bottom:short, ttm_squeeze:short, tweezer_bottom:short, upthrust:short

## Feature filters chosen (improve A and confirmed on B)

- long: ret5 >= -0.277
- short: none

## Validated patterns (17) - good on A and confirmed on B

| Pattern:side | A n | A PF | B n | B PF | B win % | B avg R | Regimes | Size x |
|---|---|---|---|---|---|---|---|---|
| breakout_retest:long | 93 | 1.6 | 35 | 1.92 | 65.7 | 0.329 | bull,bear | 1.25 |
| pullback_reversal_day:long | 59 | 1.47 | 33 | 2.08 | 63.6 | 0.322 | bull,bear,neutral | 1.25 |
| golden_cross:long | 34 | 2.16 | 12 | 2.57 | 58.3 | 0.271 | bull,neutral | 1.25 |
| down_trendline_break:long | 58 | 1.88 | 24 | 1.71 | 58.3 | 0.267 | bull,bear,neutral | 1.25 |
| channel_bounce:long | 82 | 1.19 | 35 | 1.4 | 48.6 | 0.192 | bull,neutral | 1.0 |
| tight_closes_breakout:long | 187 | 1.22 | 111 | 1.39 | 48.6 | 0.158 | bull | 1.0 |
| keltner_thrust:long | 58 | 1.78 | 29 | 1.34 | 55.2 | 0.157 | bull,neutral | 1.0 |
| momentum_burst:short | 112 | 1.16 | 84 | 1.26 | 44.0 | 0.143 | bull,bear,neutral | 1.0 |
| pocket_pivot:short | 192 | 1.24 | 67 | 1.23 | 44.8 | 0.121 | bull,bear,neutral | 1.0 |
| three_line_strike_bull:long | 41 | 1.15 | 16 | 1.26 | 43.8 | 0.116 | bull,neutral | 1.0 |
| level_bounce:long | 78 | 1.67 | 38 | 1.19 | 55.3 | 0.106 | bull,bear,neutral | 0.75 |
| avwap_reclaim:long | 54 | 1.71 | 18 | 1.15 | 38.9 | 0.08 | bull,bear | 0.75 |
| donchian55:long | 204 | 1.71 | 121 | 1.22 | 52.9 | 0.072 | bull,bear,neutral | 1.0 |
| donchian20:long | 286 | 1.64 | 161 | 1.12 | 50.3 | 0.042 | bull,bear,neutral | 0.75 |
| base_breakout:long | 198 | 1.42 | 110 | 1.1 | 52.7 | 0.037 | bull,bear,neutral | 0.75 |
| fib_pullback:long | 48 | 1.72 | 38 | 1.07 | 52.6 | 0.032 | bull,bear,neutral | 0.75 |
| stoch_overbought_cross:short | 176 | 1.27 | 95 | 1.05 | 44.2 | 0.029 | bear,neutral | 0.75 |

## Exit tuning

Best on A: stop=atr3.0, target=none, hold=10d, scale=off
- avg % per trade: A 1.166 | B 0.276 vs default 0.289 | holdout C 0.425 vs default 0.036
- adopted by the bot: no (did not beat the default exits on B and C)