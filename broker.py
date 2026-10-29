import os, re, time, requests
from datetime import datetime, timezone, timedelta
from models import NewsItem

OPEN_STATES = {"new", "accepted", "held", "pending_new", "partially_filled", "pending_replace", "accepted_for_bidding"}

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
    def asset(self, symbol): return self._get(self.t, f"/v2/assets/{symbol}")

    def news(self, minutes=30, limit=50):
        start = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
        items = self._get(self.d, "/v1beta1/news", start=start, limit=limit, sort="desc", include_content="true").get("news", [])
        return [NewsItem(str(n["id"]), n.get("headline", ""), n.get("summary", ""), n.get("symbols", []),
                         datetime.fromisoformat(n["created_at"].replace("Z", "+00:00")), n.get("content", "")) for n in items]

    def bars(self, symbol, timeframe, start):
        """timeframe: '5Min' או '1Day'; start: ISO UTC"""
        return self._get(self.d, f"/v2/stocks/{symbol}/bars", timeframe=timeframe, start=start,
                         feed="iex", limit=1000, adjustment="split").get("bars") or []

    def snapshot(self, symbol):
        """מחיר אחרון, סגירה קודמת, ומחזור דולרי ממוצע (IEX בלבד, ~3% מהמחזור האמיתי, לכן הסף בכללים נמוך)"""
        s = self._get(self.d, f"/v2/stocks/{symbol}/snapshot", feed="iex")
        price = s["latestTrade"]["p"]
        prev = s.get("prevDailyBar", {}).get("c", 0)
        start = (datetime.now(timezone.utc) - timedelta(days=35)).strftime("%Y-%m-%d")
        bars = self.bars(symbol, "1Day", start)
        adv = sum(b["c"] * b["v"] for b in bars[-20:]) / max(1, len(bars[-20:]))
        return price, prev, adv

    def submit_bracket(self, symbol, qty, side, stop, take, tif="day"):
        body = {"symbol": symbol, "qty": str(qty), "side": side, "type": "market", "time_in_force": tif,
                "order_class": "bracket", "take_profit": {"limit_price": str(take)}, "stop_loss": {"stop_price": str(stop)}}
        r = requests.post(self.t + "/v2/orders", headers=self.h, json=body, timeout=15)
        if not r.ok:
            raise RuntimeError(f"order rejected {r.status_code}: {r.text[:200]}")
        return r.json()

    def cancel_open_orders(self, symbol):
        orders = self._get(self.t, "/v2/orders", status="all", symbols=symbol, limit=50)
        for o in orders:
            if o.get("status") in OPEN_STATES:
                requests.delete(f"{self.t}/v2/orders/{o['id']}", headers=self.h, timeout=15)

    def close_position(self, symbol):
        self.cancel_open_orders(symbol)
        time.sleep(1.5)
        r = requests.delete(f"{self.t}/v2/positions/{symbol}", headers=self.h, timeout=15)
        if not r.ok:
            raise RuntimeError(f"close failed {r.status_code}: {r.text[:200]}")

    # ---- קריפטו (24/7, ללא bracket וללא שורט ב-Alpaca) ----
    def crypto_bars(self, symbol, timeframe, start):
        d = self._get(self.d, "/v1beta3/crypto/us/bars", symbols=symbol, timeframe=timeframe, start=start, limit=1000)
        return (d.get("bars") or {}).get(symbol, [])

    def crypto_price(self, symbol):
        d = self._get(self.d, "/v1beta3/crypto/us/latest/trades", symbols=symbol)
        return d["trades"][symbol]["p"]

    def submit_simple(self, symbol, qty, side, tif="gtc"):
        body = {"symbol": symbol, "qty": str(qty), "side": side, "type": "market", "time_in_force": tif}
        r = requests.post(self.t + "/v2/orders", headers=self.h, json=body, timeout=15)
        if not r.ok:
            raise RuntimeError(f"order rejected {r.status_code}: {r.text[:200]}")
        return r.json()

    def movers(self, top=20):
        """הנעים הגדולים של היום (שוק המניות) - מועמדים לסשן יומי"""
        try:
            d = self._get(self.d, "/v1beta1/screener/stocks/movers", top=top)
            return [m["symbol"] for m in d.get("gainers", [])] , [m["symbol"] for m in d.get("losers", [])]
        except Exception:
            return [], []

    def raise_stop(self, symbol, new_stop):
        """מזיז את רגל הסטופ של ה-bracket הפתוח (טריילינג / ברייק-אבן)"""
        orders = self._get(self.t, "/v2/orders", status="open", symbols=symbol, nested="true", limit=50)
        done = False
        for o in orders:
            for leg in [o] + (o.get("legs") or []):
                if leg.get("type") in ("stop", "stop_limit") and leg.get("status") in OPEN_STATES:
                    r = requests.patch(f"{self.t}/v2/orders/{leg['id']}", headers=self.h, json={"stop_price": str(round(new_stop, 2))}, timeout=15)
                    done = done or r.ok
        return done

class MockBroker:
    """לבדיקות וסימולציה בלבד"""
    def __init__(self, equity=100000):
        self._eq = equity; self.orders = []; self.closed = []; self._pos = []; self.is_open = True
        self._news = []; self.snap = {}; self.bar_data = {}; self.assets = {}; self.prices = {}; self.simple = []; self.mv = ([], []); self.raised = []
        self._clock = {"is_open": True, "timestamp": "2026-10-29T12:00:00-04:00", "next_close": "2026-10-29T16:00:00-04:00"}
    def account(self): return {"equity": self._eq, "last_equity": self._eq, "buying_power": self._eq * 2}
    def positions(self): return self._pos
    def market_open(self): return self.is_open
    def clock(self): return self._clock
    def news(self, minutes=30, limit=50): return self._news
    def snapshot(self, symbol): return self.snap[symbol]
    def bars(self, symbol, timeframe, start): return self.bar_data.get((symbol, timeframe), [])
    def asset(self, symbol): return self.assets.get(symbol, {"shortable": True, "easy_to_borrow": True, "tradable": True})
    def submit_bracket(self, symbol, qty, side, stop, take, tif="day"):
        self.orders.append((symbol, qty, side, stop, take, tif))
        self._pos.append({"symbol": symbol, "qty": str(qty), "side": "long" if side == "buy" else "short", "market_value": "0"})
        return {"id": "mock"}
    def crypto_bars(self, symbol, timeframe, start): return self.bar_data.get((symbol, timeframe), [])
    def crypto_price(self, symbol): return self.prices[symbol]
    def submit_simple(self, symbol, qty, side, tif="gtc"):
        self.simple.append((symbol, qty, side))
        self._pos.append({"symbol": symbol.replace("/", ""), "qty": str(qty), "side": "long", "market_value": str(qty * self.prices.get(symbol, 0)), "asset_class": "crypto"})
    def movers(self, top=20): return self.mv
    def raise_stop(self, symbol, new_stop): self.raised.append((symbol, new_stop)); return True
    def close_position(self, symbol):
        self.closed.append(symbol); self._pos = [p for p in self._pos if p["symbol"] != symbol]
