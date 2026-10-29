"""תמונת שוק מלמעלה למטה (Top-Down): משטר S&P500 → סקטורים מובילים/נחלשים → מניה."""
import time
from indicators import sma, pct_return
from structure import trend_structure

SECTORS = {"XLK": "Technology", "SMH": "Semiconductors", "XLF": "Financials", "XLE": "Energy", "XLV": "Healthcare",
           "XBI": "Biotech", "XLY": "Consumer Discretionary", "XLP": "Consumer Staples", "XLI": "Industrials",
           "XLB": "Materials", "XLU": "Utilities", "XLRE": "Real Estate", "XLC": "Communication", "ITA": "Aerospace & Defense"}

SECTOR_OF = {}
for etf, syms in {
    "XLK": "AAPL MSFT CRM ADBE ORCL NOW INTU PANW CRWD SHOP UBER IBM CSCO PLTR SNOW DDOG NET",
    "SMH": "NVDA AVGO AMD INTC QCOM MU AMAT LRCX TSM ASML MRVL KLAC TXN ON",
    "XLF": "JPM V MA BAC GS MS WFC C AXP BLK SCHW PYPL COIN SQ",
    "XLE": "XOM CVX COP SLB EOG OXY MPC PSX",
    "XLV": "UNH LLY ABBV JNJ MRK PFE TMO ISRG ABT DHR",
    "XBI": "MRNA VRTX REGN GILD AMGN BIIB",
    "XLY": "AMZN TSLA HD NKE MCD SBUX LOW BKNG TJX F GM ABNB",
    "XLP": "COST WMT PG KO PEP PM MDLZ CL",
    "XLI": "CAT GE HON UPS DE LMT RTX UNP ETN",
    "XLB": "LIN SHW FCX NEM APD",
    "XLU": "NEE DUK SO D AEP",
    "XLRE": "PLD AMT EQIX O SPG",
    "XLC": "GOOGL GOOG META NFLX DIS T VZ CMCSA TMUS",
    "ITA": "BA NOC GD LHX",
}.items():
    for s in syms.split(): SECTOR_OF[s] = etf

def regime(spy):
    """bull / bear / neutral לפי SMA50, SMA200 ומבנה גבוהים-נמוכים"""
    closes = [b["c"] for b in spy]
    if len(closes) < 55: return "neutral"
    s50 = sma(closes, 50); s200 = sma(closes, 200) if len(closes) >= 200 else None
    up = closes[-1] > s50 and (s200 is None or closes[-1] > s200)
    dn = closes[-1] < s50 and (s200 is None or closes[-1] < s200)
    tr = trend_structure(spy)["trend"]
    if up and tr != "down": return "bull"
    if dn and tr != "up": return "bear"
    return "neutral"

def sector_score(bars, spy):
    """חוזק יחסי מול ה-S&P: 5/20/60 ימים + מעל SMA50 (ככל שגבוה יותר הסקטור חם יותר)"""
    c, sc = [b["c"] for b in bars], [b["c"] for b in spy]
    if len(c) < 55 or len(sc) < 55: return None
    rs = lambda n: (pct_return(c, n) or 0) - (pct_return(sc, n) or 0)
    s50 = sma(c, 50)
    score = 0.2 * rs(5) + 0.5 * rs(20) + 0.3 * rs(60) + (1.5 if c[-1] > s50 else -1.5)
    return {"score": round(score, 2), "ret20": round(pct_return(c, 20) or 0, 1), "above50": c[-1] > s50}

def rank_sectors(bars_by_etf, spy):
    out = []
    for etf, bars in bars_by_etf.items():
        s = sector_score(bars, spy)
        if s: out.append({"etf": etf, "name": SECTORS.get(etf, etf), **s})
    return sorted(out, key=lambda x: -x["score"])

class Market:
    """מטמון: מרענן כל שעה. מחליט אם צד (לונג/שורט) במניה מתיישר עם השוק והסקטור."""
    def __init__(self, broker, cfg, start_iso_fn):
        self.b, self.cfg, self.start = broker, cfg, start_iso_fn
        self.regime, self.ranked, self.t = "neutral", [], 0

    def refresh(self, now, force=False):
        if not self.cfg.get("enabled", True): return
        if not force and time.time() - self.t < 3600: return
        try:
            start = self.start(now)
            spy = self.b.bars("SPY", "1Day", start)
            bars = {e: self.b.bars(e, "1Day", start) for e in SECTORS}
            self.regime, self.ranked, self.t = regime(spy), rank_sectors(bars, spy), time.time()
        except Exception:
            self.t = time.time() - 3000      # ננסה שוב בעוד ~10 דקות

    def tiers(self):
        n = self.cfg.get("top_n", 3)
        return {r["etf"] for r in self.ranked[:n]}, {r["etf"] for r in self.ranked[-n:]}

    def sector(self, sym): return SECTOR_OF.get(sym)

    def alignment(self, sym, side):
        """-1..+1: כמה הכיוון מיושר עם השוק והסקטור. (veto, ציון, הסבר)"""
        top, bottom = self.tiers() if self.ranked else (set(), set())
        sec, pts, why = self.sector(sym), 0.0, []
        if self.regime == "bull": pts += 0.4 if side == "long" else -0.4
        elif self.regime == "bear": pts += 0.4 if side == "short" else -0.4
        if sec in top: pts += 0.6 if side == "long" else -0.6; why.append(f"{sec} leading")
        if sec in bottom: pts += 0.6 if side == "short" else -0.6; why.append(f"{sec} lagging")
        veto = self.cfg.get("veto_against", True) and ((side == "long" and sec in bottom) or (side == "short" and sec in top))
        if self.cfg.get("veto_against", True) and ((side == "long" and self.regime == "bear" and sec not in top) or
                                                   (side == "short" and self.regime == "bull" and sec not in bottom)):
            veto = True
        return veto, pts, f"{self.regime} market; " + ", ".join(why or ["sector neutral"])

    def summary(self):
        return [(r["etf"], r["name"], r["score"]) for r in self.ranked]
