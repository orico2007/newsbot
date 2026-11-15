# Weekly review

# Weekly Review — 2026-11-09 to 2026-11-13

## 1. What worked / what didn't

**Live paper sample is small — 6 closed trades total.** That's below the 20-trade threshold needed for confident conclusions, so treat the numbers below as directional, not statistically solid.

- **Aggregate:** 6 trades, 16.7% win rate, avg P&L −5.625%, profit factor 0.08, avg R −0.64. Losses are dominating: avg loss −7.33% vs avg win +2.92%.
- **By strategy:** crypto (4 trades) is the less-bad bucket — 25% win, avg P&L −4.97%, PF 0.13. swing (2 trades) is 0% win, avg P&L −6.93%, PF 0.0.
- **By signal:** every pattern with >1 trade (`news`, n=2) lost both times, avg −9.8%, with entry slippage of 0.624% — roughly double the swing baseline of 0.3%. The single `cum_rsi2` trade won (+2.92%); everything else (`mr_E`, `spring_reversal`, `trend_pullback`) lost on n=1 each.
- **Account curve:** equity drifted from $99,269 (11/09) to $99,046 (11/13), a net −$222.93 (−0.22%) for the week, including a −$370.65 (−0.37%) day on 11/12.
- **Blocked ideas:** most-blocked reasons all week were "shorts disabled" and "price < $5" — the strategy layer is generating a lot of candidates the risk layer immediately throws out (not a loss, but wasted signal-generation effort).

Auto-disable logic (n≥15, avg P&L ≤ −0.5%) hasn't fired on anything yet — expected, since no live pattern has more than 4 trades.

## 2. Evidence-based rules.yaml changes

Given the tiny live sample, these are grounded primarily in the 3-year, large-N backtest (cited per item), not the 6-trade scorecard.

| # | Key | Suggested value | Support |
|---|---|---|---|
| 1 | `patterns.spring_reversal.enabled` | `false` | Backtest n=1486, PF 0.88, avg R −0.066 — persistent negative edge at scale; the one live instance also lost (−6.68%, R −1.04). |
| 2 | `patterns.higher_low_breakout.enabled` | `false` | Backtest n=292, PF 0.70, avg R −0.118 — one of the weaker patterns overall; was actually fired live this week (COST, 11/11). |
| 3 | `patterns.breakaway_gap.enabled` | `false` | Backtest n=46, win 23.9%, PF 0.62, avg R −0.045 — lowest win rate of any pattern with a meaningful sample. |
| 4 | `strategies.news.max_slippage_pct` (or `enabled`) | `0.3` (cap) / `false` | **Live only, n=2** — both trades lost (avg −9.8%) with slippage 0.624%, ~2x the swing baseline. Flagging as a process fix given the tiny sample, not a confident numeric tune. |
| 5 | *(process, no key)* | — | Hold off on further rules.yaml tuning from live results until the paper book has ≥20 closed trades per pattern; keep relying on the backtest table above in the meantime. |

## 3. Risks

- **Concentration in laggards:** JPM and XOM were negative on every single daily snapshot this week (JPM: −115 → −68; XOM: −272 → +2 only after the position was cut from 58 to 8 shares on 11/12) while their sectors (financials, energy/XLE) were flagged as laggards in the bot's own market regime readout. The book is long-only (shorts disabled) and sat in names misaligned with its own sector-leadership signal.
- **Slippage on news entries:** 0.624% vs 0.3% for swing — chasing headline-driven moves is costing roughly 2x the normal entry cost, on top of a 0% win rate for that signal so far.
- **Losing streak:** 4 of 6 closed trades lost (66.7%), and the book had a −0.37% single day (11/12) against a week that otherwise moved in small increments — a short but notable drawdown cluster.
- **Sample-size risk itself:** every rule-level conclusion drawn from live trades right now rests on n=1 or n=2. Any single large win or loss could flip the picture; don't over-react to this week's scorecard in isolation.
