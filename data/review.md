# Weekly review

# Weekly Review — 2026-10-30

## 1. What worked / what didn't

**Live trading this week:** Only one daily report was provided (2026-10-30), showing **0 entries, 0 exits, 0 blocked ideas**. Equity moved -$116.03 (-0.12%) with no trades — that's mark-to-market drift on open positions, not a trading result. No scorecard was included in this review. **I have zero closed live trades to evaluate this week**, so no live performance claims can be made (per the <20-trade rule, this is far too small a sample).

**Backtest (3yr, 21,100 trades) — this is historical/simulated, not live, but N is large enough to trust the pattern:**
- Overall edge is negative: ALL trades PF 0.86, win 44.0%.
- The split is stark and consistent across every cut: **longs are profitable, shorts are not.**
  - ALL longs: 8,991 trades, PF 1.11, 49.5% win
  - ALL shorts: 12,109 trades, PF 0.72, 39.9% win
  - FULL RULE longs: 6,742 trades, PF 1.10
  - FULL RULE shorts: 5,352 trades, PF 0.69
  - Same pattern in the "3+ chart tools" and "ALIGNED" cuts — shorts are PF 0.70–0.71 in every single one.
- A handful of large-N patterns are reliably bad regardless of direction: `sma50_bounce` (595, PF 0.79), `stoch_oversold` (449, PF 0.76), `base_breakout` (373, PF 0.74), `ichimoku_breakout` (277, PF 0.77), `macd_bear_cross` (289, PF 0.77, pure short).
- A handful of decent-N patterns show real edge, mostly long-biased: `rsi_oversold_uptrend` (175, PF 1.46), `flag` (266, PF 1.17), `cup_handle` (109, PF 1.21), `falling_wedge` (87, PF 1.35), `pullback_reversal_day` (307, PF 1.08).

## 2. Suggested rules.yaml changes (backtest-supported; live data insufficient to confirm)

1. **`allow_shorts: false`** (or add a strong short-side penalty) — supported by 12,109 ALL-shorts, 7,624 3+tool-shorts, 5,352 FULL-RULE-shorts, 5,643 ALIGNED-shorts trades, every single bucket PF 0.69–0.72. This is the single biggest lever in the data.
2. **`pattern_blacklist: [sma50_bounce, stoch_oversold, base_breakout, ichimoku_breakout, macd_bear_cross, gap_and_crap]`** — combined ~2,000 trades, all PF 0.70–0.88, win rates 30–46%.
3. **`min_pattern_profit_factor: 1.15`** (gate which patterns can fire at all) — would retain `rsi_oversold_uptrend` (175, PF 1.46), `flag` (266, PF 1.17), `cup_handle` (109, PF 1.21), `falling_wedge` (87, PF 1.35), `gap_down_reclaim` (30, PF 1.72), `pead_pullback` (67, PF 1.19).
4. Treat `three_black_crows` (PF 4.69), `volume_climax_top` (PF 1.5), `oversold_bounce` (PF 1.16) as **watch-list only, not rule-active** — only 9–22 trades each, too small to size real capital against even though they look great.
5. If shorts are kept at all rather than disabled, require the existing "3+ chart tools" AND market/sector alignment filter as a hard gate on shorts specifically — FULL RULE/ALIGNED shorts (PF ~0.69–0.70) are still negative, so alignment alone doesn't fix it; shorts likely need an additional filter not yet tested in this data (e.g., stricter RSI/trend confirmation) rather than a parameter tweak.

## 3. Risks

- **Concentration in a negative-edge bucket:** shorts are 57% of all backtest trades (12,109/21,100) but are the losing side — if live trading mirrors this mix, more than half of capital/risk is going into the weaker edge.
- **Losing streaks:** shorts win only ~40% of the time; at that rate, streaks of 5+ consecutive losses are statistically unsurprising (roughly 1-in-13 per 5-trade run), which can be mistaken for a regime change rather than expected variance.
- **Slippage:** backtest already assumes 0.05%/side — fine for liquid large caps, but if any live symbols are thinner, real slippage could erode the already-thin long-side edge (PF ~1.1 is not a large cushion).
- **Live-data gap:** with 0 trades reported this week, there's no way to confirm these backtest-driven changes would hold up live. Recommend validating the short-disable change against the next 2–4 weeks of live fills before treating it as settled.

**Process fix:** future weekly reviews need the scorecard and multiple daily reports with actual entries/exits included — a single zero-trade day isn't enough to assess live performance.
