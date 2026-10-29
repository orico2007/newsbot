import pathlib
from datetime import datetime, timezone, timedelta
from rules_loader import load_rules
from models import Verdict, NewsItem

R = load_rules(str(pathlib.Path(__file__).parent.parent / "rules.yaml"))

def bar(c, v=1000, spread=0.1):
    return {"t": "x", "o": c, "h": c + spread, "l": c - spread, "c": c, "v": v}

def intraday_up(n=25, spike=3000):
    bars = [bar(50 + 0.05 * i + (0.15 if i % 2 else -0.15), 1000) for i in range(n)]
    for b in bars[-3:]: b["v"] = spike
    return bars

def intraday_down(n=25, spike=3000):
    bars = [bar(50 - 0.05 * i + (0.15 if i % 2 else -0.15), 1000) for i in range(n)]
    for b in bars[-3:]: b["v"] = spike
    return bars

def daily_pullback(n_up=110, drop=6, drop_step=0.004):
    closes = [80 + 40 * i / n_up for i in range(n_up)]
    for i in range(drop): closes.append(closes[-1] * (1 - drop_step))
    return [bar(c, 2_000_000, spread=c * 0.01) for c in closes]

def daily_downtrend(n=110):
    closes = [120 - 40 * i / n for i in range(n)]
    return [bar(c, 2_000_000, spread=c * 0.01) for c in closes]

class FakeBrain:
    def __init__(self, score, direction="bullish", horizon="intraday", event="other"):
        self.v = Verdict(score, direction, "t", event, horizon); self.calls = []
    def rate(self, *a):
        self.calls.append(a); return self.v

def news(id="1", symbols=("AAA",), age_min=1, headline="Big contract", content=""):
    return NewsItem(id, headline, "", list(symbols), datetime.now(timezone.utc) - timedelta(minutes=age_min), content)
