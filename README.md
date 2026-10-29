# NewsBot v2 - paper trading bot (news + earnings + chart rules)

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

## Run
Cloud: GitHub Actions (`.github/workflows/trade.yml`), secrets: ALPACA_KEY_ID, ALPACA_SECRET_KEY, CLAUDE_CODE_OAUTH_TOKEN.
Local: `pip install -r requirements.txt && python -m pytest -q && python bot.py`

Every decision (including skips and blocks) is logged to `data/journal.csv`. Paper only unless `mode: live` AND `ALLOW_LIVE=1`.
