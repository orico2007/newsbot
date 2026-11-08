# Weekly review

# Weekly Review — Paper Bot (reports 2026-10-30 → 2026-11-06)

## 1. What worked / what didn't

**Closed trades: only 3** (all crypto). Win rate 33.3%, avg P&L **-4.04%**, profit factor **0.19**, avg R **-0.51**.
- cum_rsi2 (1 trade): win, +2.92%
- spring_reversal (1 trade): loss, -6.68%
- trend_pullback (1 trade): loss, -8.36%

**Equity, across the reports provided:** $99,883.97 (10/30) → $99,159.47 (11/06). The worst single day was 11/05: **-787.17 (-0.79%)**, when all four open long equity positions (ABBV, JPM, UNH, XOM) lost money simultaneously. Note: the 11/02 report wasn't in the set provided, so this isn't a strict day-by-day reconciliation.

**Activity was light:** only 2 new entries all week (V, AMZN swing longs on 11/06) and one crypto stop-out (BCH/USD, 11/04). 10 ideas were blocked on 11/06 alone (stop-too-wide, price<$5, no-uptrend, shorts-disabled).

**Backtest context (21,099 trades, 3y/40 symbols)** shows the live losses aren't surprising: spring_reversal has a negative long-run edge (1,479 trades, PF 0.88, avg -0.30%) — the live loss matches. trend_pullback is historically close to breakeven (540 trades, PF 1.01, avg +0.03%), so the live -8.36% loss looks like a single bad outcome, not a pattern flaw. Shorts underperform longs broadly in the backtest (longs PF 1.08/win 49.2% vs shorts PF 0.73/win 39.9%, n=8,992/12,107) — correctly, the live blocked-idea log confirms shorts are already disabled.

## 2. Changes — sample too small for rules.yaml tuning

Only 3 closed trades exist, far below the 20-trade minimum needed to responsibly adjust rules.yaml parameters. No numeric rule changes recommended this week. Process fixes instead:

1. **Fix slippage logging** — scorecard shows "None" for entry slippage on every row, even though the backtest assumes 0.05%/side. Without this you can't tell if live fills match backtest assumptions.
2. **Verify trailing-stop logic fires** — "Trailing-stop raises: 0" every day this week despite UNH swinging from +91.44 to -37.08 unrealized; confirm the trigger condition is actually reachable, not dormant.
3. **Audit the max-risk/structure-stop filter** — 2 of 10 blocked ideas on 11/06 were rejected for stop distance just over the cap (12.1%, 15.8% vs. 12.0% limit). Worth a manual check of whether that threshold is cutting off reasonable setups by a hair, before touching the number.
4. **Add portfolio-level correlation/exposure tracking** — all 4 open positions dropped together on 11/05 despite sitting in nominally different "leading" sectors; sector labels alone didn't prevent a correlated down day.
5. **Keep accumulating trade data** before acting on pattern-level stats — at n=1 per pattern, don't disable or favor cum_rsi2/spring_reversal/trend_pullback based on this week alone.

## 3. Risks

- **Concentration**: book is long-only equities (shorts disabled), so it carries undiversified long-market-beta risk — this showed up directly in the correlated -787 day on 11/05.
- **Statistical noise**: 3 trades is not a sample; current win-rate/PF/avg-R numbers should not drive decisions yet.
- **Losing streak**: 2 of the last 3 closed trades were losses, and the trend_pullback loss (-8.36%) was much worse than its historical average — worth a one-off look at execution/stop placement on that specific trade, not a pattern-level conclusion.
- **Slippage blind spot**: slippage isn't being recorded live, so there's no way to detect fill-quality drift versus the backtest's assumptions.
