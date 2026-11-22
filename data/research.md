# Research (walk-forward, 3 periods) - 6y daily, 40 symbols

Signals: 70766. **A** (before 2024-02-09) = choose, **B** (2024-02-09 to 2025-07-02) = confirm, **C** (after 2025-07-02) = holdout: never used for choosing, so it is the honest estimate. Past results do not guarantee future results.

## Honest result: holdout period C (never used to choose anything)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| baseline longs | 4756 | 47.0 | -0.016 | 0.018 | 0.97 |
| baseline shorts | 6410 | 42.0 | -0.104 | -0.555 | 0.81 |
| + filters longs | 2292 | 47.2 | -0.003 | 0.071 | 0.99 |
| + filters shorts | 6410 | 42.0 | -0.104 | -0.555 | 0.81 |
| **FINAL: filters + validated patterns** | 681 | 44.2 | -0.044 | -0.101 | 0.91 |
| FINAL longs | 536 | 44.8 | -0.04 | -0.008 | 0.91 |
| FINAL shorts | 145 | 42.1 | -0.057 | -0.444 | 0.91 |

## Same sets on earlier periods (selection bias makes A and B look better than reality)

| Set | Trades | Win % | Avg R | Avg % | Profit factor |
|---|---|---|---|---|---|
| FINAL on A (chosen on this) | 1436 | 56.5 | 0.206 | 1.05 | 1.55 |
| FINAL on B (confirmation) | 708 | 50.3 | 0.128 | 0.426 | 1.31 |

## Variants compared on the holdout (alpha = trade return minus what SPY did over the same days; positive = beats just holding the market)

| Variant | Trades | Win % | Avg R | Avg % | Alpha % | Profit factor |
|---|---|---|---|---|---|---|
| all longs | 4756 | 47.0 | -0.016 | 0.018 | -0.174 | 0.97 |
| all shorts | 6410 | 42.0 | -0.104 | -0.555 | -0.269 | 0.81 |
| longs, market not bearish | 4610 | 46.7 | -0.023 | -0.029 | -0.154 | 0.95 |
| longs, market bullish only | 3172 | 47.3 | -0.02 | 0.014 | -0.211 | 0.96 |
| longs minus blacklisted patterns | 4404 | 47.5 | -0.014 | 0.024 | -0.163 | 0.97 |
| longs minus blacklist, market not bearish | 4265 | 47.2 | -0.02 | -0.023 | -0.142 | 0.96 |
| longs, high-volume only (rvol>=1.26) | 1871 | 49.3 | 0.026 | 0.342 | 0.015 | 1.06 |
| whitelist (validated patterns) longs | 536 | 44.8 | -0.04 | -0.008 | -0.208 | 0.91 |

Blacklist (lost on both A and B): adx_pullback:short, avwap_reclaim:short, base_breakout:short, bb_lower_bounce:short, bb_upper_fade:short, bear_divergence:short, bear_flag:short, bearish_engulfing_top:short, blowoff_top:short, bollinger_squeeze:short, breakdown_support:short, breakout_retest:short, bullish_engulfing_support:short, bullish_harami_support:short, channel_bounce:short, cup_handle:short, death_cross:short, donchian20:short, donchian55:short, double_bottom:short, down_trendline_break:short, ema21_bounce:short, ema21_rejection:short, fib_pullback:short, gap_up_hold:long, gap_up_hold:short, golden_cross:short, higher_low_breakout:short, ibs_reversion:short, ichimoku_breakout:short, inside_bar_breakout:short, keltner_thrust:short, level_bounce:short, low52_breakdown:short, lower_low_breakdown:short, macd_bear_cross:short, morning_star:short, nr7_breakout:short, outside_day_reversal:short, oversold_atr_stretch:short, piercing_line:short, pullback_reversal_day:short, range_breakdown:short, rising_wedge:short, rsi2_overbought:short, rsi2_reversion:short, rsi_divergence:short, rsi_oversold_uptrend:short, runaway_gap:short, sma200_reclaim:short, sma50_bounce:long, sma50_bounce:short, sma50_rejection:short, spring_reversal:short, three_inside_up:short, three_line_strike_bull:short, tight_closes_breakout:short, trend_pullback:long, triple_bottom:short, ttm_squeeze:short, tweezer_bottom:short, upthrust:short

## Feature filters chosen (improve A and confirmed on B)

- long: ret5 >= -0.216
- short: none

## Validated patterns (15) - good on A and confirmed on B

| Pattern:side | A n | A PF | B n | B PF | B win % | B avg R | Regimes | Size x |
|---|---|---|---|---|---|---|---|---|
| breakout_retest:long | 94 | 1.61 | 37 | 2.31 | 67.6 | 0.446 | bull,bear | 1.25 |
| pullback_reversal_day:long | 58 | 1.51 | 32 | 1.99 | 62.5 | 0.304 | bull,bear,neutral | 1.25 |
| golden_cross:long | 33 | 2.32 | 19 | 2.46 | 63.2 | 0.276 | bull,neutral | 1.25 |
| down_trendline_break:long | 61 | 2.0 | 21 | 1.5 | 52.4 | 0.214 | bull,bear,neutral | 1.25 |
| channel_bounce:long | 78 | 1.32 | 33 | 1.42 | 48.5 | 0.199 | bull,neutral | 1.0 |
| level_bounce:long | 75 | 1.7 | 39 | 1.39 | 56.4 | 0.19 | bull,bear,neutral | 1.0 |
| stoch_oversold:long | 21 | 3.77 | 15 | 1.31 | 46.7 | 0.188 | bull | 1.0 |
| fib_pullback:long | 46 | 1.68 | 37 | 1.39 | 59.5 | 0.15 | bull,bear,neutral | 1.0 |
| tight_closes_breakout:long | 191 | 1.26 | 101 | 1.35 | 48.5 | 0.139 | bull | 1.0 |
| avwap_reclaim:long | 52 | 1.58 | 19 | 1.16 | 42.1 | 0.081 | bull,bear | 0.75 |
| base_breakout:long | 207 | 1.35 | 104 | 1.18 | 52.9 | 0.06 | bull,bear,neutral | 0.75 |
| pocket_pivot:short | 193 | 1.25 | 72 | 1.1 | 41.7 | 0.055 | bull,bear,neutral | 0.75 |
| donchian55:long | 215 | 1.7 | 113 | 1.15 | 50.4 | 0.046 | bull,bear,neutral | 0.75 |
| stoch_overbought_cross:short | 173 | 1.32 | 96 | 1.05 | 44.8 | 0.029 | bear,neutral | 0.75 |
| momentum_burst:long | 115 | 1.44 | 52 | 1.05 | 38.5 | 0.028 | bull,bear,neutral | 0.75 |

## Exit tuning

Best on A: stop=atr3.0, target=none, hold=20d, scale=off
- avg % per trade: A 1.861 | B 0.665 vs default 0.426 | holdout C 0.259 vs default -0.101
- adopted by the bot: yes