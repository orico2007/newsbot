"""לוח דוחות: לא מחזיקים סווינג דרך דוח (פער מחיר לא נשלט). מקור: לוח הדוחות הציבורי של Nasdaq.
כל כשל = "לא ידוע" ואז לא חוסמים (fail-open) כדי שהבוט ימשיך לעבוד."""
import requests
from datetime import date, timedelta

URL = "https://api.nasdaq.com/api/calendar/earnings"
HEADERS = {"User-Agent": "Mozilla/5.0 (newsbot-paper)", "Accept": "application/json"}

def parse(payload):
    """מחזיר סט סימבולים מהתשובה של Nasdaq"""
    rows = (((payload or {}).get("data") or {}).get("rows")) or []
    return {r["symbol"].upper() for r in rows if r.get("symbol")}

class Earnings:
    def __init__(self, days_ahead=4, fetch=None):
        self.n, self.cache, self.fetch = days_ahead, {}, fetch or self._fetch

    @staticmethod
    def _fetch(d):
        r = requests.get(URL, params={"date": d.isoformat()}, headers=HEADERS, timeout=12)
        r.raise_for_status()
        return r.json()

    def on(self, d):
        """סט הסימבולים שמדווחים ביום d, או None אם לא ידוע"""
        if d in self.cache: return self.cache[d]
        try: self.cache[d] = parse(self.fetch(d))
        except Exception: self.cache[d] = None
        return self.cache[d]

    def days_until(self, sym, today=None):
        """כמה ימים עד הדוח הקרוב (0=היום), או None אם אין / לא ידוע"""
        today = today or date.today()
        for i in range(self.n + 1):
            d = today + timedelta(days=i)
            if d.weekday() >= 5: continue
            s = self.on(d)
            if s and sym.upper() in s: return i
        return None
