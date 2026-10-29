import csv, json, os, re, sys, time, logging, pathlib, argparse
from datetime import datetime, timezone, timedelta, date
from zoneinfo import ZoneInfo
from rules_loader import load_rules
from risk import evaluate_entry
import chart

log = logging.getLogger("bot")
DATA = pathlib.Path("data"); DATA.mkdir(exist_ok=True)
STATE_FILE = DATA / "state.json"
JOURNAL = DATA / "journal.csv"
COLS = ["time", "symbol", "headline", "score", "direction", "event", "horizon", "strategy", "side", "action", "detail", "reason"]

# ---------- state / journal ----------
def load_state():
    s = json.loads(STATE_FILE.read_text(encoding="utf-8")) if STATE_FILE.exists() else {}
    return roll(s)

def roll(s):
    today = str(date.today())
    if s.get("day") != today:
        s = {"day": today, "seen": s.get("seen", [])[-2000:], "meta": s.get("meta", {}),
             "swing_done": s.get("swing_done"), "trades_today": 0, "halted": False}
    s.setdefault("meta", {}); s.setdefault("seen", [])
    return s

def save_state(s): STATE_FILE.write_text(json.dumps(s), encoding="utf-8")

def journal(row):
    new = not JOURNAL.exists()
    with JOURNAL.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if new: w.writerow(COLS)
        w.writerow(row)

# ---------- helpers ----------
def _ts(s):
    s = re.sub(r"(\.\d{6})\d+", r"\1", s)      # Alpaca שולח ננו-שניות
    return datetime.fromisoformat(s)

def session_open_iso(now):
    et = now.astimezone(ZoneInfo("America/New_York")).replace(hour=9, minute=30, second=0, microsecond=0)
    return et.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def daily_start_iso(now):
    return (now - timedelta(days=400)).strftime("%Y-%m-%dT%H:%M:%SZ")

def weekdays_between(d1, d2):
    d1, d2, n = date.fromisoformat(d1), date.fromisoformat(d2), 0
    while d1 < d2:
        d1 += timedelta(days=1)
        if d1.weekday() < 5: n += 1
    return n

# ---------- engine ----------
class Engine:
    def __init__(self, broker, brain, rules, state, funds=None):
        self.b, self.brain, self.r, self.state, self.funds = broker, brain, rules, state, funds

    def _j(self, now, sym, headline="", v=None, strategy="", side="", action="", detail=""):
        journal([now.isoformat(), sym, headline, v.score if v else "", v.direction if v else "", v.event if v else "",
                 v.horizon if v else "", strategy, side, action, detail, v.reason if v else ""])

    def _fund(self, sym):
        try: return self.funds.get(sym) if self.funds else None
        except Exception: return None

    def _route(self, v):
        d, s = self.r["day"], self.r["swing"]
        if v.direction not in ("bullish", "bearish"): return None
        side = "long" if v.direction == "bullish" else "short"
        if v.horizon == "swing" and s["enabled"] and v.score >= s["catalyst_min_score"]: return "swing", side
        if d["enabled"] and v.score >= d["min_score"]: return "day", side
        return None

    def _submit(self, now, sym, headline, v, strategy, side, dec, extra=""):
        try:
            self.b.submit_bracket(sym, dec.qty, dec.side, dec.stop_price, dec.take_profit_price, dec.tif)
        except Exception as e:
            self._j(now, sym, headline, v, strategy, side, "error", f"order failed: {e}")
            return False
        self.state["meta"][sym] = {"strategy": strategy, "side": side, "entry_date": str(date.today()), "ts": time.time()}
        self.state["trades_today"] = self.state.get("trades_today", 0) + 1
        self._j(now, sym, headline, v, strategy, side, "ENTER",
                f"{dec.side} qty={dec.qty} stop={dec.stop_price} tp={dec.take_profit_price} {extra}".strip())
        log.info("ENTER %s %s %s x%d stop %.2f tp %.2f | %s", strategy, side, sym, dec.qty, dec.stop_price, dec.take_profit_price, headline)
        return True

    # --- חדשות ודוחות ---
    def news_pass(self, now, mtc, is_open):
        n, d = self.r["news"], self.r["day"]
        for item in self.b.news(minutes=n["max_news_age_minutes"] + 5):
            if item.id in self.state["seen"]: continue
            self.state["seen"].append(item.id)
            age = (now - item.created_at).total_seconds() / 60
            if age > n["max_news_age_minutes"] or len(item.symbols) != 1: continue   # חדשות על מניה אחת בלבד
            sym = item.symbols[0]
            f = self._fund(sym)
            v = self.brain.rate(sym, item.headline, item.summary, item.content, f)
            route = self._route(v)
            if not route:
                self._j(now, sym, item.headline, v, action="skip", detail="below threshold / neutral"); continue
            strategy, side = route
            if strategy == "day" and mtc is not None and mtc <= d["flatten_minutes_before_close"] + 5:
                self._j(now, sym, item.headline, v, strategy, side, "blocked", "too close to market close"); continue
            try:
                price, prev, adv = self.b.snapshot(sym)
                atr, snap = None, {}
                if strategy == "day":
                    ok, why, snap = chart.intraday_check(self.b.bars(sym, "5Min", session_open_iso(now)), side, d["chart"])
                else:
                    ok, why, snap = chart.trend_ok(self.b.bars(sym, "1Day", daily_start_iso(now)), side)
                    atr = snap.get("atr")
                    if ok and f and f.get("rev_yoy") is not None and ((side == "long" and f["rev_yoy"] < 0) or (side == "short" and f["rev_yoy"] > 25)):
                        ok, why = False, f"fundamentals disagree (rev_yoy {f['rev_yoy']}%)"
                if not ok:
                    self._j(now, sym, item.headline, v, strategy, side, "blocked", f"chart: {why} {_fmt(snap)}"); continue
                shortable = True
                if side == "short":
                    a = self.b.asset(sym); shortable = bool(a.get("shortable") and a.get("easy_to_borrow") and a.get("tradable", True))
                dec = evaluate_entry(self.r, strategy, side, sym, price, prev, adv, self.b.account(), self.b.positions(),
                                     self.state, is_open, atr=atr, shortable=shortable)
            except Exception as e:
                log.warning("eval failed for %s: %s", sym, e)
                self._j(now, sym, item.headline, v, strategy, side, "error", str(e)); continue
            if not dec.ok:
                self._j(now, sym, item.headline, v, strategy, side, "blocked", dec.reason); continue
            self._submit(now, sym, item.headline, v, strategy, side, dec, _fmt(snap))

    # --- יציאת Day לפני הסגירה ---
    def day_flatten(self, mtc, positions):
        if mtc is None or mtc > self.r["day"]["flatten_minutes_before_close"]: return
        now = datetime.now(timezone.utc)
        for p in positions:
            m = self.state["meta"].get(p["symbol"], {})
            if m.get("strategy") == "day":
                try:
                    self.b.close_position(p["symbol"])
                    self._j(now, p["symbol"], strategy="day", side=m.get("side", ""), action="EXIT", detail="end-of-day flatten")
                    log.info("EXIT day %s end-of-day", p["symbol"])
                except Exception as e:
                    log.warning("flatten failed %s: %s", p["symbol"], e)

    # --- סווינג: יציאות זמן + סריקה יומית ---
    def swing_pass(self, now, mtc):
        s = self.r["swing"]
        today = str(date.today())
        if not s["enabled"] or mtc is None or mtc > s["scan_minutes_before_close"] or self.state.get("swing_done") == today: return
        self.state["swing_done"] = today
        held = {p["symbol"] for p in self.b.positions()}
        for sym, m in list(self.state["meta"].items()):
            if m.get("strategy") == "swing" and sym in held and weekdays_between(m["entry_date"], today) >= s["max_hold_days"]:
                try:
                    self.b.close_position(sym)
                    self._j(now, sym, strategy="swing", side=m.get("side", ""), action="EXIT", detail=f"time stop {s['max_hold_days']}d")
                except Exception as e:
                    log.warning("time-stop failed %s: %s", sym, e)
        if s["scan"]["enabled"]:
            self._scan(now)

    def _scan(self, now):
        s, held = self.r["swing"], {p["symbol"] for p in self.b.positions()}
        cands = []
        for sym in s["watchlist"]:
            if sym in held: continue
            try:
                daily = self.b.bars(sym, "1Day", daily_start_iso(now))
                ok, why, snap = chart.swing_scan_ok(daily, s["scan"])
                if not ok: continue
                f = self._fund(sym)
                if chart.fundamentals_ok(f, s["scan"]):
                    cands.append((f["rev_yoy"], sym, daily, snap, f))
            except Exception as e:
                log.warning("scan failed %s: %s", sym, e)
        cands.sort(reverse=True)
        taken = 0
        for rev, sym, daily, snap, f in cands:
            if taken >= s["scan"]["new_per_day"]: break
            price, prev = daily[-1]["c"], daily[-2]["c"]
            adv = sum(b["c"] * b["v"] for b in daily[-20:]) / len(daily[-20:])
            dec = evaluate_entry(self.r, "swing", "long", sym, price, prev, adv, self.b.account(), self.b.positions(),
                                 self.state, True, atr=snap["atr"])
            head = f"SCAN: uptrend + {snap.get('pullback_pct')}% pullback, rev_yoy={rev}%"
            if not dec.ok:
                self._j(now, sym, head, None, "swing", "long", "blocked", dec.reason); continue
            if self._submit(now, sym, head, None, "swing", "long", dec, _fmt(snap)): taken += 1

    def reconcile(self, positions):
        held, t = {p["symbol"] for p in positions}, time.time()
        for sym in list(self.state["meta"]):
            if sym not in held and t - self.state["meta"][sym].get("ts", 0) > 600:
                del self.state["meta"][sym]

    def step(self, now=None):
        now = now or datetime.now(timezone.utc)
        self.state = roll(self.state)
        c = self.b.clock()
        if self.r["account"]["market_hours_only"] and not c["is_open"]: return c
        mtc = (_ts(c["next_close"]) - _ts(c["timestamp"])).total_seconds() / 60 if c.get("next_close") else None
        positions = self.b.positions()
        self.reconcile(positions)
        self.day_flatten(mtc, positions)
        self.news_pass(now, mtc, c["is_open"])
        self.swing_pass(now, mtc)
        save_state(self.state)
        return c

def _fmt(snap):
    return json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in (snap or {}).items()}) if snap else ""

# ---------- runners ----------
def session(engine, max_minutes=345, early_minutes=20, sleep=time.sleep):
    """סשן אחד (ל-GitHub Actions): מחכה לפתיחת השוק, רץ עד הסגירה או עד max_minutes, ואז יוצא."""
    t0, opened = time.monotonic(), False
    while True:
        c = engine.b.clock()
        if c["is_open"]:
            opened = True
        elif opened:
            log.info("market closed - session over"); return
        else:
            wait = (_ts(c["next_open"]) - _ts(c["timestamp"])).total_seconds() / 60
            if wait > early_minutes:
                log.info("market opens in %.0f min - nothing to do now", wait); return
        if (time.monotonic() - t0) / 60 > max_minutes:
            log.info("max session length reached - handing over"); return
        try:
            engine.step()
        except Exception as e:
            log.exception("loop error: %s", e)
        sleep(20 if c["is_open"] else 30)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--session", action="store_true"); args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    rules = load_rules()
    live = rules["mode"] == "live"
    if live and os.getenv("ALLOW_LIVE") != "1":
        sys.exit("live mode blocked: set ALLOW_LIVE=1 deliberately. Run on paper first.")
    from broker import AlpacaBroker
    from brain import Brain
    from fundamentals import Fundamentals
    engine = Engine(AlpacaBroker(paper=not live), Brain(), rules, load_state(), Fundamentals())
    log.info("started in %s mode", "LIVE" if live else "PAPER")
    if args.session:
        return session(engine)
    while True:
        try:
            c = engine.step()
        except Exception as e:
            log.exception("loop error: %s", e); c = {"is_open": False}
        time.sleep(20 if c.get("is_open") else 60)

if __name__ == "__main__":
    main()
