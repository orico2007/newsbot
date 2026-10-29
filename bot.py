import csv, json, os, re, sys, time, logging, pathlib, argparse
from datetime import datetime, timezone, timedelta, date
from zoneinfo import ZoneInfo
from rules_loader import load_rules
from risk import evaluate_entry
import chart
import patterns
from market import Market, SECTOR_OF
from scoring import confluence, size_mult
from indicators import atr as _atr, pct_return

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
             "swing_done": s.get("swing_done"), "trades_today": 0, "halted": False,
             "cool": s.get("cool", {}), "tried": []}
    s.setdefault("meta", {}); s.setdefault("seen", []); s.setdefault("cool", {}); s.setdefault("tried", [])
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
        self.mkt = Market(broker, rules.get("market", {"enabled": False}), daily_start_iso)

    def _write_sectors(self):
        """data/sectors.json: משטר השוק ודירוג הסקטורים העדכני (אפשר לקרוא בגיטהאב)"""
        if not self.mkt.ranked or self.state.get("sectors_t") == self.mkt.t: return
        self.state["sectors_t"] = self.mkt.t
        try:
            (DATA / "sectors.json").write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(), "regime": self.mkt.regime,
                                                          "ranked": self.mkt.ranked}, indent=1), encoding="utf-8")
        except OSError: pass

    def _pos(self):
        """פוזיציות מניות בלבד (קריפטו מנוהל במנוע נפרד)"""
        return [p for p in self.b.positions() if p.get("asset_class") != "crypto" and "/" not in p["symbol"]]

    def _gate(self, sym, side):
        """Cooldown, תקרת סקטור והתאמה לשוק/סקטור. מחזיר (ok, הסבר, נקודות יישור)"""
        cd = self.r.get("cooldown_minutes", 0)
        if cd and time.time() - self.state.get("cool", {}).get(sym, 0) < cd * 60: return False, "cooldown after recent exit", 0.0
        sec, cap = SECTOR_OF.get(sym), self.r.get("sector_cap")
        if sec and cap and sum(1 for p in self._pos() if SECTOR_OF.get(p["symbol"]) == sec) >= cap:
            return False, f"sector cap ({sec})", 0.0
        veto, pts, why = self.mkt.alignment(sym, side)
        if veto: return False, f"against market/sector: {why}", pts
        return True, why, pts

    def _fund_ok(self, f, side):
        if not f or f.get("rev_yoy") is None: return None
        if side == "long": return False if (f["rev_yoy"] < 0 or f.get("eps_positive") is False and f["rev_yoy"] < 10) else (True if f["rev_yoy"] >= 10 else None)
        return False if f["rev_yoy"] > 25 else (True if f["rev_yoy"] < 5 else None)

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

    def _submit(self, now, sym, headline, v, strategy, side, dec, extra="", price=None, atr=None):
        try:
            self.b.submit_bracket(sym, dec.qty, dec.side, dec.stop_price, dec.take_profit_price, dec.tif)
        except Exception as e:
            self._j(now, sym, headline, v, strategy, side, "error", f"order failed: {e}")
            return False
        ref = price or ((dec.stop_price + dec.take_profit_price) / 2)
        self.state["meta"][sym] = {"strategy": strategy, "side": side, "entry_date": str(date.today()), "ts": time.time(),
                                   "entry": ref, "stop": dec.stop_price, "ext": ref,
                                   "atr": atr or max(abs(ref - dec.stop_price) / 1.5, 0.01)}
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
            if age > n["max_news_age_minutes"] or len(item.symbols) != 1 or "/" in item.symbols[0]: continue   # חדשות על מניה אחת בלבד
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
                okg, whyg, pts = self._gate(sym, side)
                if not okg:
                    self._j(now, sym, item.headline, v, strategy, side, "blocked", whyg); continue
                sc = confluence(0.6, pts, (snap.get("vol_spike") or 0) >= 1.5, v.score, True, self._fund_ok(f, side))
                mult = 1.0      # חדשות: הגודל נשאר בדיוק לפי הכלל (5% / 4%); הציון נרשם ביומן בלבד
                shortable = True
                if side == "short":
                    a = self.b.asset(sym); shortable = bool(a.get("shortable") and a.get("easy_to_borrow") and a.get("tradable", True))
                dec = evaluate_entry(self.r, strategy, side, sym, price, prev, adv, self.b.account(), self._pos(),
                                     self.state, is_open, atr=atr, shortable=shortable, size_mult=mult)
            except Exception as e:
                log.warning("eval failed for %s: %s", sym, e)
                self._j(now, sym, item.headline, v, strategy, side, "error", str(e)); continue
            if not dec.ok:
                self._j(now, sym, item.headline, v, strategy, side, "blocked", dec.reason); continue
            self._submit(now, sym, item.headline, v, strategy, side, dec, f"conf={sc} x{mult} {whyg} " + _fmt(snap), price=price, atr=atr)

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
        held = {p["symbol"] for p in self._pos()}
        for sym, m in list(self.state["meta"].items()):
            if m.get("strategy") == "swing" and sym in held and weekdays_between(m["entry_date"], today) >= s["max_hold_days"]:
                try:
                    self.b.close_position(sym)
                    self._j(now, sym, strategy="swing", side=m.get("side", ""), action="EXIT", detail=f"time stop {s['max_hold_days']}d")
                except Exception as e:
                    log.warning("time-stop failed %s: %s", sym, e)
        if s["scan"]["enabled"]:
            self._scan(now)

    def _pattern_scan(self, now):
        """סריקת תבניות גרף יומית על רשימת המעקב (לונג+שורט), עם סינון שוק/סקטור/דוחות וציון מפגש"""
        s, sg = self.r["swing"], self.r.get("signals", {}).get("swing", {})
        if not sg.get("enabled") or not sg.get("scan_watchlist_patterns"): return 0
        held = {p["symbol"] for p in self._pos()}
        cands = []
        for sym in s["watchlist"]:
            if sym in held: continue
            try:
                daily = self.b.bars(sym, "1Day", daily_start_iso(now))
                if len(daily) < 60: continue
                closes = [b["c"] for b in daily]
                rs = pct_return(closes, 60) or 0.0
                f = None
                for sig in patterns.detect_all(daily, sg.get("detectors") or None, {"rs": rs}, shorts=s["allow_short"]):
                    ok, why, pts = self._gate(sym, sig.side)
                    if not ok: continue
                    f = f or self._fund(sym)
                    fo = self._fund_ok(f, sig.side)
                    if fo is False: continue
                    sc = confluence(sig.quality, pts, sig.volume_ok, None, None, fo, rs if sig.side == "long" else -rs)
                    if sc >= sg["min_confluence"]: cands.append((sc, sym, sig, why, daily))
            except Exception as e:
                log.warning("pattern scan failed %s: %s", sym, e)
        cands.sort(key=lambda x: -x[0])
        taken, done = 0, set()
        for sc, sym, sig, why, daily in cands:
            if taken >= s["scan"]["new_per_day"]: break
            if sym in done: continue
            done.add(sym)
            if self._enter_signal(now, sym, "swing", sig, sc, why, True, daily): taken += 1
        return taken

    def _scan(self, now):
        s, held = self.r["swing"], {p["symbol"] for p in self._pos()}
        taken0 = self._pattern_scan(now)
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
        taken = taken0
        for rev, sym, daily, snap, f in cands:
            if taken >= s["scan"]["new_per_day"]: break
            price, prev = daily[-1]["c"], daily[-2]["c"]
            adv = sum(b["c"] * b["v"] for b in daily[-20:]) / len(daily[-20:])
            dec = evaluate_entry(self.r, "swing", "long", sym, price, prev, adv, self.b.account(), self._pos(),
                                 self.state, True, atr=snap["atr"])
            head = f"SCAN: uptrend + {snap.get('pullback_pct')}% pullback, rev_yoy={rev}%"
            if not dec.ok:
                self._j(now, sym, head, None, "swing", "long", "blocked", dec.reason); continue
            if self._submit(now, sym, head, None, "swing", "long", dec, _fmt(snap)): taken += 1


    # --- סיגנלים מגרף ליום (ORB / gap-and-go / VWAP reclaim), לונג ושורט ---
    def day_scan(self, now, mtc, is_open):
        d, sg = self.r["day"], self.r.get("signals", {}).get("day", {})
        if not (is_open and d["enabled"] and sg.get("enabled")): return
        if mtc is not None and mtc <= d["flatten_minutes_before_close"] + 15: return
        if time.time() - self.state.get("day_scan_ts", 0) < sg["scan_every_minutes"] * 60: return
        self.state["day_scan_ts"] = time.time()
        gain, lose = self.b.movers() if sg.get("use_movers") else ([], [])
        syms = [x for x in dict.fromkeys(list(gain) + list(lose) + self.r["swing"]["watchlist"]) if x.isalpha()][:sg["max_symbols"]]
        held = {p["symbol"] for p in self._pos()}
        cands = []
        for sym in syms:
            if sym in held or sym in self.state["tried"]: continue
            try:
                bars5 = self.b.bars(sym, "5Min", session_open_iso(now))
                if len(bars5) < 6: continue
                prev = None
                sigs = patterns.detect_day(bars5, {"prev_close": prev}, sg.get("detectors") or None, shorts=d["allow_short"])
                if any(x.name == "orb" for x in sigs):           # gap_and_go דורש סגירה קודמת
                    prev = self.b.snapshot(sym)[1]
                    sigs = patterns.detect_day(bars5, {"prev_close": prev}, sg.get("detectors") or None, shorts=d["allow_short"])
                for sig in sigs:
                    ok, why, pts = self._gate(sym, sig.side)
                    if not ok: continue
                    sc = confluence(sig.quality, pts, sig.volume_ok)
                    if sc >= sg["min_confluence"]: cands.append((sc, sym, sig, why))
            except Exception as e:
                log.warning("day scan failed %s: %s", sym, e)
        cands.sort(key=lambda x: -x[0])
        done = set()
        for sc, sym, sig, why in cands:
            if sym in done: continue
            done.add(sym)
            self._enter_signal(now, sym, "day", sig, sc, why, True)

    def _enter_signal(self, now, sym, strategy, sig, sc, why, is_open, daily=None):
        head = f"{strategy.upper()} {sig.name}: {sig.notes}"
        try:
            price, prev, adv = self.b.snapshot(sym)
            atr = (_atr(daily) if daily else None) or (abs(price - sig.stop) / 1.5)
            shortable = True
            if sig.side == "short":
                a = self.b.asset(sym); shortable = bool(a.get("shortable") and a.get("easy_to_borrow") and a.get("tradable", True))
            mult = size_mult(sc, self.r["signals"]["size_multiplier"]["min"], self.r["signals"]["size_multiplier"]["max"])
            dec = evaluate_entry(self.r, strategy, sig.side, sym, price, prev, adv, self.b.account(), self._pos(), self.state,
                                 is_open, atr=atr, shortable=shortable, override=(sig.stop, sig.target), size_mult=mult)
        except Exception as e:
            log.warning("signal eval failed %s: %s", sym, e)
            self._j(now, sym, head, None, strategy, sig.side, "error", str(e)); return False
        if strategy == "day": self.state["tried"].append(sym)
        if not dec.ok:
            self._j(now, sym, head, None, strategy, sig.side, "blocked", f"{dec.reason} conf={sc}"); return False
        return self._submit(now, sym, head, None, strategy, sig.side, dec, f"conf={sc} x{mult} {why}", price=price, atr=atr)

    # --- ניהול פוזיציות פתוחות: ברייק-אבן וסטופ נגרר ---
    def manage_positions(self, now, positions):
        t = self.r.get("trailing", {})
        if not t.get("enabled"): return
        for p in positions:
            m = self.state["meta"].get(p["symbol"])
            if not m or not m.get("atr") or not m.get("stop"): continue
            try: price, entry = float(p["current_price"]), float(p["avg_entry_price"])
            except (KeyError, TypeError, ValueError): continue
            a, long = m["atr"], m["side"] == "long"
            m["ext"] = max(m.get("ext", price), price) if long else min(m.get("ext", price), price)
            gain = (price - entry) if long else (entry - price)
            new = None
            if gain >= t["breakeven_atr"] * a: new = entry
            if gain >= t["trail_activate_atr"] * a:
                tr = m["ext"] - t["trail_atr"] * a if long else m["ext"] + t["trail_atr"] * a
                new = max(new or tr, tr) if long else min(new or tr, tr)
            if new is None: continue
            better = new > m["stop"] + 0.01 if long else new < m["stop"] - 0.01
            valid = new < price - 0.01 if long else new > price + 0.01
            if better and valid:
                try:
                    if self.b.raise_stop(p["symbol"], new):
                        self._j(now, p["symbol"], strategy=m["strategy"], side=m["side"], action="TRAIL", detail=f"stop {m['stop']} -> {round(new, 2)}")
                        m["stop"] = round(new, 2)
                except Exception as e:
                    log.warning("trail failed %s: %s", p["symbol"], e)

    def reconcile(self, positions):
        held, t = {p["symbol"] for p in positions}, time.time()
        for sym in list(self.state["meta"]):
            if sym not in held and t - self.state["meta"][sym].get("ts", 0) > 600:
                del self.state["meta"][sym]
                self.state.setdefault("cool", {})[sym] = t

    def step(self, now=None):
        now = now or datetime.now(timezone.utc)
        self.state = roll(self.state)
        c = self.b.clock()
        if self.r["account"]["market_hours_only"] and not c["is_open"]: return c
        mtc = (_ts(c["next_close"]) - _ts(c["timestamp"])).total_seconds() / 60 if c.get("next_close") else None
        self.mkt.refresh(now)
        self._write_sectors()
        positions = self._pos()
        self.reconcile(positions)
        self.day_flatten(mtc, positions)
        self.manage_positions(now, positions)
        self.news_pass(now, mtc, c["is_open"])
        self.day_scan(now, mtc, c["is_open"])
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
