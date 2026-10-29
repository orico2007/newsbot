from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class NewsItem:
    id: str
    headline: str
    summary: str
    symbols: list
    created_at: datetime

@dataclass
class Verdict:
    score: int
    direction: str       # bullish | bearish | neutral
    reason: str

@dataclass
class Decision:
    ok: bool
    reason: str
    qty: int = 0
    stop_price: float = 0.0
    take_profit_price: float = 0.0
