# NewsBot v3 - paper trading bot (news + earnings + chart patterns + sectors + crypto)

Flow: Alpaca news (full article text) -> Claude scores it (direction, strength 1-10, event type, horizon)
-> chart rules in code -> risk gate in code -> bracket order (entry + stop + target) at Alpaca.

## Strategies (all numbers live in `rules.yaml`)
**Day**: news with score >= 9. Long needs price above VWAP and a volume spike; short needs the mirror image.
Positions are closed 10 minutes before the US close. Longs 5% / shorts 3% of equity, stop 3%, target 6%.

**Swing**: held for days (max 10 trading days).
- Catalyst entries: news/earnings rated horizon=swing with score >= 8, confirmed by the daily trend (above/below SMA50).
- Daily scan near the close over `watchlist`: uptrend + 2-10% pullback + RSI 40-65 + revenue growth >= 10% YoY (SEC filings).
- Stop 2x ATR (capped at 8%), target 4x ATR, GTC orders at the broker.

**Earnings/reports**: Claude reads the article body, not only the headline, plus YoY revenue/EPS growth from SEC EDGAR.

**Risk gate** (code, not Claude): max 8 positions, 60% gross exposure, 2% daily loss stop, no chasing, price >= $5, liquidity filter.

## v3 additions
**Top-down filter** (`market.py`): S&P 500 regime (bull/bear/neutral) + ranking of 14 sector ETFs by relative strength
(5/20/60 days vs SPY, above SMA50). Longs are vetoed in lagging sectors or a bear market, shorts in leading sectors or a bull market.
The current ranking is written to `data/sectors.json` every hour.

**Chart patterns** (`patterns.py`, 15 swing detectors, each also run mirrored for shorts): flag, base breakout on volume,
double bottom/top, inverse head & shoulders, ascending/symmetrical triangles, breakaway/runaway gaps, island reversal,
trend pullback to SMA20, Fibonacci pullback with reversal candle, breakout-retest, 52-week high, oversold bounce, Bollinger squeeze.
Stops sit under/over the pattern structure and targets use the measured move. There is no minimum risk/reward and no fixed 1% risk rule.

**Day setups** (5-minute bars on today's movers + watchlist): opening-range breakout, gap-and-go, VWAP reclaim (and their short mirrors).

**Confluence score** (`scoring.py`): pattern quality + market/sector alignment + volume + news score + revenue growth.
It scales signal position size between 0.5x and 1.5x of the normal size (news trades keep the exact 5%/4% sizing).

**Position management**: break-even after +1 ATR, trailing stop after +2 ATR, 90-minute cooldown after an exit, max 2 positions per sector.

**Crypto** (`crypto.py`, 24/7, long only): BTC, ETH, SOL, AVAX, LINK, DOGE, LTC, BCH. Same pattern detectors on daily bars, gated by the BTC trend.
Alpaca has no crypto shorts or bracket orders, so the bot manages stop, target and trailing itself. Own state/journal: `data/state_crypto.json`, `data/journal_crypto.csv`.
Runs as a separate GitHub Actions job every 6 hours.

**Earnings blackout** (`earnings.py`): swing entries are skipped when the company reports within 2 trading days, and open swing positions
are closed the day before a report (calendar: Nasdaq; if it can't be fetched the bot carries on without the filter).

**Daily report**: `data/report.md` (and `data/reports/DATE.md`) is written just before the close: P&L, entries, exits, open positions, why ideas were blocked, sectors.

**Backtester** (`backtest.py`, weekly GitHub Action or run by hand): replays every pattern on 3 years of daily bars for the watchlist and writes
`data/backtest.md`. Patterns with 30+ trades and clearly negative expectancy are disabled automatically via `data/backtest.json`.

## Run
Cloud: GitHub Actions (`.github/workflows/trade.yml`), secrets: ALPACA_KEY_ID, ALPACA_SECRET_KEY, CLAUDE_CODE_OAUTH_TOKEN.
Local: `pip install -r requirements.txt && python -m pytest -q && python bot.py`

Every decision (including skips and blocks) is logged to `data/journal.csv`. Paper only unless `mode: live` AND `ALLOW_LIVE=1`.
