import os, requests
from datetime import datetime, timezone, timedelta
from models import NewsItem

class AlpacaBroker:
    def __init__(self, paper=True):
        self.paper = paper
        self.t = "https://paper-api.alpaca.markets" if paper else "https://api.alpaca.markets"
        self.d = "https://data.alpaca.markets"
        self.h = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}

    def _get(self, base, path, **params):
        r = requests.get(base + path, headers=self.h, params=params, timeout=15)
        r.raise_for_status()
        return r.json()

    def account(self): return self._get(self.t, "/v2/account")
    def positions(self): return self._get(self.t, "/v2/positions")
    def clock(self): return self._get(self.t, "/v2/clock")
    def market_open(self): return self.clock()["is_open"]

    def news(self, minutes=30, limit=50):
        start = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
        items = self._get(self.d, "/v1beta1/news", start=start, limit=limit, sort="desc").get("news", [])
        return [NewsItem(str(n["id"]), n.get("headline", ""), n.get("summary", ""), n.get("symbols", []),
                         datetime.fromisoformat(n["created_at"].replace("Z", "+00:00"))) for n in items]

    def snapshot(self, symbol):
        """returns price, prev_close, avg dollar volume (approx, last 20 daily bars)"""
        s = self._get(self.d, f"/v2/stocks/{symbol}/snapshot", feed="iex")
        price = s["latestTrade"]["p"]
        prev = s.get("prevDailyBar", {}).get("c", 0)
        start = (datetime.now(timezone.utc) - timedelta(days=35)).strftime("%Y-%m-%d")
        bars = self._get(self.d, f"/v2/stocks/{symbol}/bars", timeframe="1Day", start=start, feed="iex", limit=30).get("bars") or []
        adv = sum(b["c"] * b["v"] for b in bars[-20:]) / max(1, len(bars[-20:]))
        # volume מ-IEX הוא רק חלק מהמחזור הכולל, לכן הסינון מחמיר יותר (בכוונה)
        return price, prev, adv

    def buy_bracket(self, symbol, qty, stop, take):
        body = {"symbol": symbol, "qty": str(qty), "side": "buy", "type": "market", "time_in_force": "day",
                "order_class": "bracket", "take_profit": {"limit_price": str(take)}, "stop_loss": {"stop_price": str(stop)}}
        r = requests.post(self.t + "/v2/orders", headers=self.h, json=body, timeout=15)
        r.raise_for_status()
        return r.json()

class MockBroker:
    """לבדיקות וסימולציה בלבד"""
    def __init__(self, equity=100000):
        self._eq = equity; self.orders = []; self._pos = []; self.is_open = True; self._news = []; self.snap = {}; self._clock = {"is_open": True}
    def account(self): return {"equity": self._eq, "last_equity": self._eq, "buying_power": self._eq * 2}
    def positions(self): return self._pos
    def market_open(self): return self.is_open
    def clock(self): return self._clock
    def news(self, minutes=30, limit=50): return self._news
    def snapshot(self, symbol): return self.snap[symbol]
    def buy_bracket(self, symbol, qty, stop, take):
        self.orders.append((symbol, qty, stop, take)); self._pos.append({"symbol": symbol}); return {"id": "mock"}
