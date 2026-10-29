"""צמיחת הכנסות ורווח למניה מדוחות SEC (EDGAR XBRL, חינם). כל כשל מחזיר None, לא עוצר את הבוט."""
import os, requests
from datetime import date

REV_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet",
            "RevenueFromContractWithCustomerIncludingAssessedTax"]
UA = os.getenv("SEC_USER_AGENT", "newsbot-paper github.com/orico2007/newsbot")

def _days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days

def quarterly(facts, tags, units):
    """בוחר את התג עם הרבעון העדכני ביותר; מחזיר {end_date: value} לרבעונים בלבד (80-100 ימים)"""
    best = {}
    for tag in tags:
        node = facts.get("us-gaap", {}).get(tag)
        if not node:
            continue
        for unit in units:
            rows = node.get("units", {}).get(unit, [])
            q = {}
            for r in rows:
                if r.get("form") not in ("10-Q", "10-K") or "start" not in r:
                    continue
                if 80 <= _days(r["start"], r["end"]) <= 100:
                    if r["end"] not in q or r.get("filed", "") >= q[r["end"]][1]:
                        q[r["end"]] = (r["val"], r.get("filed", ""))
            q = {k: v[0] for k, v in q.items()}
            if q and (not best or max(q) > max(best)):
                best = q
    return best

def yoy(series):
    if not series:
        return None, None
    end = max(series)
    for e, v in series.items():
        if 350 <= _days(e, end) <= 380 and v:
            return (series[end] / v - 1) * 100 if v > 0 else None, series[end]
    return None, series[end]

def parse_facts(data):
    facts = data.get("facts", {})
    rev = quarterly(facts, REV_TAGS, ["USD"])
    eps = quarterly(facts, ["EarningsPerShareDiluted", "EarningsPerShareBasic"], ["USD/shares"])
    rev_yoy, rev_last = yoy(rev)
    eps_yoy, eps_last = yoy(eps)
    return {"rev_yoy": round(rev_yoy, 1) if rev_yoy is not None else None,
            "eps_yoy": round(eps_yoy, 1) if eps_yoy is not None else None,
            "eps_positive": (eps_last > 0) if eps_last is not None else None,
            "as_of": max(rev) if rev else None}

class Fundamentals:
    def __init__(self, http=requests):
        self.http, self._cik, self._cache = http, None, {}

    def _get(self, url):
        r = self.http.get(url, headers={"User-Agent": UA}, timeout=20)
        r.raise_for_status()
        return r.json()

    def get(self, symbol):
        if symbol in self._cache:
            return self._cache[symbol]
        out = None
        try:
            if self._cik is None:
                self._cik = {v["ticker"]: v["cik_str"] for v in self._get("https://www.sec.gov/files/company_tickers.json").values()}
            cik = self._cik.get(symbol.upper())
            if cik:
                out = parse_facts(self._get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json"))
        except Exception:
            out = None
        self._cache[symbol] = out
        return out
