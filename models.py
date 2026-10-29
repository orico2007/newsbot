from dataclasses import dataclass
from datetime import datetime

@dataclass
class NewsItem:
    id: str
    headline: str
    summary: str
    symbols: list
    created_at: datetime
    content: str = ""

@dataclass
class Verdict:
    score: int            # עוצמת ההשפעה הצפויה בכיוון שנבחר, 1-10
    direction: str        # bullish | bearish | neutral
    reason: str
    event: str = "other"  # earnings | guidance | contract | mna | analyst | regulatory | product | legal | macro | other
    horizon: str = "intraday"   # intraday | swing

@dataclass
class Decision:
    ok: bool
    reason: str
    qty: int = 0
    side: str = "buy"
    stop_price: float = 0.0
    take_profit_price: float = 0.0
    tif: str = "day"
