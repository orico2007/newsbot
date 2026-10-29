"""קריפטו 24/7 (Alpaca Paper): לונג בלבד, בלי bracket - הבוט עצמו מנהל סטופ, יעד וטריילינג.
מנוע נפרד עם state/journal משלו כדי לא להתנגש עם סשן המניות."""
import csv, json, time, logging, pathlib, argparse, os, sys
from datetime import datetime, timezone, timedelta
import patterns
from indicators import sma, atr
from structure import trend_structure
from scoring import confluence, size_mult
from rules_loader import load_rules

log = logging.getLogger("crypto")
DATA = pathlib.Path("data"); DATA.mkdir(exist_ok=True)
STATE_FILE, JOURNAL = DATA / "state_crypto.json", DATA / "journal_crypto.csv"
COLS = ["time", "symbol", "headline", "score", "strategy", "action", "detail"]

def key(sym): return sym.replace("/", "")
def is_crypto_sym(s): return "/" in s or (s.endswith("USD") and len(s) > 5 and s[:-3].isalpha() and s[:-3] in {"BTC", "ETH", "SOL", "AVAX", "LINK", "DOGE", "LTC", "BCH", "DOT", "UNI", "AAVE", "XRP", "SHIB"})
def slash(s): return s if "/" in s else s[:-3] + "/USD"

def load_state():
    return json.loads(STATE_FILE.read_text(encoding="utf-8")) if STATE_FILE.exists() else {"meta": {}, "seen": [], "last_scan": 0}

def save_state(s):
    s["seen"] = s["seen"][-500:]
    STATE_FILE.write_text(json.dumps(s), encoding="utf-8")

def journal(row):
    new = not JOURNAL.exists()
    with open(JOURNAL, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(COLS)
        w.writerow(row)

class CryptoEngine:
    def __init__(self, broker, brain, rules, state, clock=time.time):
        self.b, self.brain, self.r, self.state, self.clock = broker, brain, rules, state, clock
        self.c = rules["crypto"]

    def _j(self, now, sym, headline="", score="", strategy="", action="", detail=""):
        journal([now.isoformat(), sym, headline, score, strategy, action, detail])

    def _held(self):
        return {p["symbol"]: p for p in self.b.positions() if p.get("asset_class") == "crypto" or is_crypto_sym(p["symbol"])}

    def _daily(self, sym, now, days=320):
        return self.b.crypto_bars(sym, "1Day", (now - timedelta(days=days)).strftime("%Y-%m-%d"))

    def btc_ok(self, now):
        """משטר הקריפטו: BTC מעל SMA50 ולא במבנה ירידה"""
        try:
            d = self._daily("BTC/USD", now)
            closes = [x["c"] for x in d]
            if len(closes) < 55: return True, 0.0
            up = closes[-1] > sma(closes, 50) and trend_structure(d)["trend"] != "down"
            s200 = sma(closes, 200) if len(closes) >= 200 else None
            down = closes[-1] < sma(closes, 50) and (trend_structure(d)["trend"] == "down" or (s200 is not None and sma(closes, 50) < s200))
            return (not down), (0.5 if up else -0.5 if down else 0.0)
        except Exception:
            return True, 0.0

    # ---------- ניהול פוזיציות פתוחות ----------
    def manage(self, now):
        held, t = self._held(), self.c["trail"]
        for k, m in list(self.state["meta"].items()):
            if k not in held:
                if self.clock() - m.get("ts", 0) > 600: del self.state["meta"][k]
                continue
            sym = m["symbol"]
            try: price = self.b.crypto_price(sym)
            except Exception as e: log.warning("price %s: %s", sym, e); continue
            m["high"] = max(m.get("high", price), price)
            a = m["atr"]
            if m["high"] >= m["entry"] + t["activate_atr"] * a:
                new = m["high"] - t["trail_atr"] * a
                if new > m["stop"]:
                    m["stop"] = round(new, 6)
                    self._j(now, sym, strategy="crypto", action="TRAIL", detail=f"stop->{m['stop']}")
            age = (now - datetime.fromisoformat(m["entry_time"])).days
            reason = None
            if price <= m["stop"]: reason = f"stop {m['stop']}"
            elif price >= m["target"]: reason = f"target {m['target']}"
            elif age >= self.c["max_hold_days"]: reason = f"time stop {age}d"
            if reason:
                try:
                    self.b.close_position(k)
                    self._j(now, sym, strategy="crypto", action="EXIT", detail=f"{reason} price={price} entry={m['entry']}")
                except Exception as e:
                    log.warning("crypto exit failed %s: %s", sym, e)

    # ---------- כניסה ----------
    def _enter(self, now, sym, price, a, stop, target, mult, why, score, headline=""):
        c, acct = self.c, self.b.account()
        equity = float(acct["equity"]); held = self._held()
        if len(held) >= c["max_positions"]: return False, "max crypto positions"
        if key(sym) in held: return False, "already holding"
        gross = sum(abs(float(p.get("market_value", 0) or 0)) for p in held.values())
        budget = min(equity * c["position_pct"] / 100 * mult, equity * c["max_gross_pct"] / 100 - gross, float(acct["buying_power"]))
        if budget < 10: return False, "budget too small / exposure cap"
        cap = c["max_stop_pct"] / 100
        if stop >= price or (price - stop) / price > cap: stop = price * (1 - min(cap, a * c["atr_stop_mult"] / price))
        if target <= price: target = price + a * c["atr_stop_mult"] * 2
        qty = round(budget / price, 6)
        try: self.b.submit_simple(sym, qty, "buy", "gtc")
        except Exception as e:
            self._j(now, sym, headline, score, why, "error", str(e)); return False, str(e)
        self.state["meta"][key(sym)] = {"symbol": sym, "entry": price, "stop": round(stop, 6), "target": round(target, 6), "atr": a,
                                        "high": price, "entry_time": now.isoformat(), "ts": self.clock()}
        self._j(now, sym, headline, score, why, "ENTER", f"qty={qty} entry={price} stop={stop:.6g} tp={target:.6g} x{mult}")
        return True, "ok"

    def scan(self, now):
        c = self.c
        ok, regime_pts = self.btc_ok(now)
        taken = 0
        cands = []
        for sym in c["symbols"]:
            if key(sym) in self._held(): continue
            try:
                d = self._daily(sym, now)
                if len(d) < 60: continue
                sigs = [s for s in patterns.detect_all(d, shorts=False, ctx={"rs": 0.0}) ]
                if not sigs: continue
                a = atr(d) or 0
                if not a: continue
                for s in sigs:
                    align = regime_pts + (0.3 if sym == "BTC/USD" else 0)
                    sc = confluence(s.quality, align, s.volume_ok)
                    cands.append((sc, sym, s, a))
            except Exception as e:
                log.warning("crypto scan %s: %s", sym, e)
        cands.sort(key=lambda x: -x[0])
        for sc, sym, s, a in cands:
            if taken >= c["new_per_scan"]: break
            if not ok and sym != "BTC/USD":
                self._j(now, sym, score=sc, strategy=s.name, action="blocked", detail="BTC regime down"); continue
            if sc < c["min_confluence"]:
                continue
            price = self.b.crypto_price(sym)
            done, why = self._enter(now, sym, price, a, s.stop, s.target, size_mult(sc), s.name, sc, s.notes)
            if done: taken += 1
            else: self._j(now, sym, s.notes, sc, s.name, "blocked", why)

    def news(self, now):
        c = self.c
        for item in self.b.news(minutes=c["news_max_age_minutes"] + 5):
            if item.id in self.state["seen"]: continue
            syms = [s for s in item.symbols if is_crypto_sym(s)]
            if not syms: continue
            self.state["seen"].append(item.id)
            if (now - item.created_at).total_seconds() / 60 > c["news_max_age_minutes"] or len(syms) != 1: continue
            sym = slash(syms[0])
            if sym not in c["symbols"]: continue
            v = self.brain.rate(sym, item.headline, item.summary, item.content, None)
            self._j(now, sym, item.headline, v.score, "news", "scored", f"{v.direction} {v.event}")
            if v.direction == "bearish" and v.score >= c["news_min_score"] and key(sym) in self._held():
                try:
                    self.b.close_position(key(sym)); self._j(now, sym, item.headline, v.score, "news", "EXIT", "bearish news")
                except Exception as e: log.warning("news exit failed: %s", e)
                continue
            if v.direction != "bullish" or v.score < c["news_min_score"]: continue
            d = self._daily(sym, now)
            closes = [x["c"] for x in d]
            if len(closes) < 55 or closes[-1] < sma(closes, 20):
                self._j(now, sym, item.headline, v.score, "news", "blocked", "below SMA20"); continue
            ok, rp = self.btc_ok(now)
            if not ok and sym != "BTC/USD":
                self._j(now, sym, item.headline, v.score, "news", "blocked", "BTC regime down"); continue
            a = atr(d) or 0
            price = self.b.crypto_price(sym)
            sc = confluence(0.6, rp, False, v.score, True)
            self._enter(now, sym, price, a, price - a * c["atr_stop_mult"], price + a * c["atr_stop_mult"] * 2, size_mult(sc), "news", sc, item.headline)

    def step(self, now=None):
        if not self.c["enabled"]: return
        now = now or datetime.now(timezone.utc)
        self.manage(now)
        try: self.news(now)
        except Exception as e: log.warning("crypto news failed: %s", e)
        if self.clock() - self.state.get("last_scan", 0) >= self.c["scan_every_minutes"] * 60:
            self.state["last_scan"] = self.clock()
            self.scan(now)
        save_state(self.state)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--session", action="store_true"); ap.add_argument("--minutes", type=int, default=345)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    rules = load_rules()
    if rules["mode"] == "live" and os.getenv("ALLOW_LIVE") != "1": sys.exit("live mode blocked")
    from broker import AlpacaBroker
    from brain import Brain
    eng = CryptoEngine(AlpacaBroker(paper=rules["mode"] != "live"), Brain(), rules, load_state())
    t0 = time.monotonic()
    while True:
        try: eng.step()
        except Exception as e: log.exception("crypto loop error: %s", e)
        if not args.session or (time.monotonic() - t0) / 60 > args.minutes: return
        time.sleep(60)

if __name__ == "__main__":
    main()
