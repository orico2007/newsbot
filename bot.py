import csv, json, os, re, sys, time, logging, pathlib, argparse
from datetime import datetime, timezone, timedelta, date
from zoneinfo import ZoneInfo
from rules_loader import load_rules
from risk import evaluate_entry
import chart
import tools
import features as _feat
from structure import pivots
import patterns
import mr
from models import Verdict
from market import Market, SECTOR_OF
from scoring import confluence, size_mult
from earnings import Earnings
import report as _report
import scorecard
import timeframes as tf
import alerts
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
             "cool": s.get("cool", {}), "tried": [], "queue": s.get("queue", [])}
    s.setdefault("meta", {}); s.setdefault("seen", []); s.setdefault("cool", {}); s.setdefault("tried", []); s.setdefault("queue", [])
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
    return (now - timedelta(days=900)).strftime("%Y-%m-%dT%H:%M:%SZ")

def weekdays_between(d1, d2):
    d1, d2, n = date.fromisoformat(d1), date.fromisoformat(d2), 0
    while d1 < d2:
        d1 += timedelta(days=1)
        if d1.weekday() < 5: n += 1
    return n

# ---------- engine ----------
class Engine:
    def __init__(self, broker, brain, rules, state, funds=None, earnings=None):
        self.b, self.brain, self.r, self.state, self.funds = broker, brain, rules, state, funds
        self.earn = earnings
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
        kill = self.mkt.kill(side)
        if kill: return False, f"kill switch: {kill}", 0.0
        veto, pts, why = self.mkt.alignment(sym, side)
        if veto: return False, f"against market/sector: {why}", pts
        return True, why, pts

    def _earnings_block(self, sym, strategy):
        """סווינג לא נכנס כשדוח קרוב (פער לא נשלט). יום-מסחר לא מושפע"""
        e = self.r.get("earnings", {})
        if not self.earn or strategy != "swing" or not e.get("blackout_days"): return None
        n = self.earn.days_until(sym)
        return f"earnings in {n}d" if n is not None and n <= e["blackout_days"] else None

    def _fund_ok(self, f, side):
        if not f or f.get("rev_yoy") is None: return None
        if side == "long": return False if (f["rev_yoy"] < 0 or f.get("eps_positive") is False and f["rev_yoy"] < 10) else (True if f["rev_yoy"] >= 10 else None)
        return False if f["rev_yoy"] > 25 else (True if f["rev_yoy"] < 5 else None)

    def _j(self, now, sym, headline="", v=None, strategy="", side="", action="", detail=""):
        if action in ("ENTER", "EXIT") or (action == "error" and "order failed" in detail):
            alerts.send(f"{action} {sym} {strategy} {side}\n{(headline or '')[:80]} {detail[:100]}", "NewsBot")
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

    def _submit(self, now, sym, headline, v, strategy, side, dec, extra="", price=None, atr=None, pattern=""):
        try:
            self.b.submit_bracket(sym, dec.qty, dec.side, dec.stop_price, dec.take_profit_price, dec.tif)
        except Exception as e:
            self._j(now, sym, headline, v, strategy, side, "error", f"order failed: {e}")
            return False
        ref = price or ((dec.stop_price + dec.take_profit_price) / 2)
        self.state["meta"][sym] = {"strategy": strategy, "side": side, "entry_date": str(date.today()), "ts": time.time(),
                                   "entry": ref, "qty": dec.qty, "qty0": dec.qty, "take": dec.take_profit_price, "stop": dec.stop_price, "stop0": dec.stop_price, "ext": ref, "pattern": pattern or ("news" if v else "scan"), "open_ts": datetime.now(timezone.utc).isoformat(),
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
            self._act(now, mtc, is_open, sym, item.headline, v, f, route)

    def premarket(self, now, c):
        """לפני הפתיחה: Claude מדרג חדשות/דוחות שיצאו בלילה והעסקאות נכנסות לתור לפתיחה"""
        pm = self.r.get("premarket", {})
        if not pm.get("enabled") or not c.get("next_open"): return
        wait = (_ts(c["next_open"]) - _ts(c["timestamp"])).total_seconds() / 60
        if wait > pm["window_minutes"]: return
        for item in self.b.news(minutes=pm["news_lookback_minutes"]):
            if item.id in self.state["seen"]: continue
            self.state["seen"].append(item.id)
            if len(item.symbols) != 1 or "/" in item.symbols[0]: continue
            sym = item.symbols[0]
            f = self._fund(sym)
            v = self.brain.rate(sym, item.headline, item.summary, item.content, f)
            route = self._route(v)
            if not route:
                self._j(now, sym, item.headline, v, action="skip", detail="premarket: below threshold / neutral"); continue
            self.state["queue"].append({"sym": sym, "headline": item.headline, "v": v.__dict__, "route": list(route), "expire": time.time() + pm["retry_minutes_after_open"] * 60})
            self._j(now, sym, item.headline, v, route[0], route[1], "queued", "premarket - will act at the open")

    def process_queue(self, now, mtc, is_open):
        keep = []
        for q in self.state.get("queue", []):
            if time.time() > q["expire"]: continue
            v = Verdict(**q["v"])
            try: res = self._act(now, mtc, is_open, q["sym"], q["headline"], v, self._fund(q["sym"]), tuple(q["route"]))
            except Exception as e:
                log.warning("queue item failed: %s", e); res = None
            if res == "retry": keep.append(q)
        self.state["queue"] = keep

    def _act(self, now, mtc, is_open, sym, headline, v, f, route):
        """מהחלטת Claude להזמנה: גרף -> שוק/סקטור -> Risk Gate. מחזיר 'retry' אם אין עדיין מספיק נרות 5 דקות"""
        d = self.r["day"]
        strategy, side = route
        if strategy == "day" and mtc is not None and mtc <= d["flatten_minutes_before_close"] + 5:
            self._j(now, sym, headline, v, strategy, side, "blocked", "too close to market close"); return
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
                self._j(now, sym, headline, v, strategy, side, "blocked", f"chart: {why} {_fmt(snap)}")
                return "retry" if why.startswith("not enough") else None
            okg, whyg, pts = self._gate(sym, side)
            if not okg:
                self._j(now, sym, headline, v, strategy, side, "blocked", whyg); return
            sc = confluence(0.6, pts, (snap.get("vol_spike") or 0) >= 1.5, v.score, True, self._fund_ok(f, side))
            mult = 1.0      # חדשות: הגודל נשאר בדיוק לפי הכלל (5% / 4%); הציון נרשם ביומן בלבד
            shortable = True
            if side == "short":
                a = self.b.asset(sym); shortable = bool(a.get("shortable") and a.get("easy_to_borrow") and a.get("tradable", True))
            dec = evaluate_entry(self.r, strategy, side, sym, price, prev, adv, self.b.account(), self._pos(),
                                 self.state, is_open, atr=atr, shortable=shortable, size_mult=mult)
        except Exception as e:
            log.warning("eval failed for %s: %s", sym, e)
            self._j(now, sym, headline, v, strategy, side, "error", str(e)); return
        if not dec.ok:
            self._j(now, sym, headline, v, strategy, side, "blocked", dec.reason); return
        self._submit(now, sym, headline, v, strategy, side, dec, f"conf={sc} x{mult} {whyg} " + _fmt(snap), price=price, atr=atr)


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
        if self.earn and self.r.get("earnings", {}).get("exit_before"):
            for sym, m in list(self.state["meta"].items()):
                if m.get("strategy") == "swing" and sym in held and self.earn.days_until(sym) in (0, 1) and not m.get("earn_ok"):
                    try:
                        self.b.close_position(sym); held.discard(sym)
                        self._j(now, sym, strategy="swing", side=m.get("side", ""), action="EXIT", detail="earnings tomorrow/today - flatten")
                    except Exception as e:
                        log.warning("earnings exit failed %s: %s", sym, e)
        mr_cfg = s.get("mr", {})
        for sym, m in list(self.state["meta"].items()):
            if not str(m.get("pattern", "")).startswith("mr_") or sym not in held: continue
            try:
                daily = self.b.bars(sym, "1Day", daily_start_iso(now))
                why = "close above prior-day high" if mr.exit_now(daily) else (f"time stop {mr_cfg.get('hold_days', 7)}d" if weekdays_between(m["entry_date"], today) >= mr_cfg.get("hold_days", 7) else None)
                if why:
                    self.b.close_position(sym); held.discard(sym)
                    self._j(now, sym, strategy="swing", side="long", action="EXIT", detail=f"mean-reversion exit: {why}")
            except Exception as e:
                log.warning("mr exit failed %s: %s", sym, e)
        for sym, m in list(self.state["meta"].items()):
            if m.get("strategy") == "swing" and sym in held and weekdays_between(m["entry_date"], today) >= self._hold_days():
                try:
                    self.b.close_position(sym)
                    self._j(now, sym, strategy="swing", side=m.get("side", ""), action="EXIT", detail=f"time stop {self._hold_days()}d")
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
        extra = [x for x in (self.b.actives() if sg.get("use_actives") else []) if x.isalpha()]
        universe = list(dict.fromkeys(list(s["watchlist"]) + extra))[:sg.get("max_universe", 120)]
        for sym in universe:
            if sym in held: continue
            try:
                daily = self.b.bars(sym, "1Day", daily_start_iso(now))
                if len(daily) < 60: continue
                closes = [b["c"] for b in daily]
                rs = (pct_return(closes, 60) or 0.0) - (self.mkt.spy_ret60 or 0.0)
                f = None
                det = dict(sg.get("detectors") or {})
                for name in self._disabled_patterns(): det.setdefault(name, False)
                sigs = patterns.detect_all(daily, det or None, {"rs": rs}, shorts=s["allow_short"])
                weekly = tf.resample_weekly(daily)
                if len(weekly) >= 60:
                    for w in patterns.detect_all(weekly, det or None, {"rs": rs}, shorts=s["allow_short"]):
                        w.name += "_W"; w.quality = min(1.0, w.quality + 0.1); w.notes = "weekly " + w.notes
                        sigs.append(w)
                feat = _feat.compute(daily); rsch = self._research()
                for sig in sigs:
                    if self._side_blocked(sig): continue
                    if not self._research_ok(sig, feat, rsch): continue
                    ok, why, pts = self._gate(sym, sig.side)
                    if not ok: continue
                    htf = tf.htf_points(daily, sig.side)
                    pts += 0.5 * htf
                    why += f"; weekly {'agrees' if htf > 0 else 'against' if htf < 0 else 'neutral'}"
                    f = f or self._fund(sym)
                    fo = self._fund_ok(f, sig.side)
                    if fo is False: continue
                    sc = confluence(sig.quality, pts, sig.volume_ok, None, None, fo, rs if sig.side == "long" else -rs)
                    nt, tl = tools.count(sig, daily)
                    nt += (1 if htf > 0 else 0) + (1 if pts - 0.5 * htf > 0 else 0)
                    if nt < sg.get("min_tools", 3):
                        log.debug("%s %s skipped: only %d tools (%s)", sym, sig.name, nt, ", ".join(tl)); continue
                    why += f"; {nt} tools: {', '.join(tl)}"
                    if sc >= sg["min_confluence"] and not self._side_blocked(sig, sc): cands.append((sc, sym, sig, why, daily))
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

    def _mr_news(self, now, sym, cfg):
        """A pullback caused by bad news/fundamentals is a falling knife, not a dip. Returns (veto, rank_bonus, text)"""
        if not cfg.get("news_filter", True): return False, 0, ""
        f = self._fund(sym)
        if self._fund_ok(f, "long") is False: return True, 0, "weak fundamentals (revenue shrinking)"
        bonus, notes = 0, []
        try: items = self.b.news(minutes=cfg.get("news_lookback_hours", 48) * 60, limit=10, symbol=sym)
        except Exception as e:
            log.warning("mr news fetch failed %s: %s", sym, e); return False, 0, ""
        for it in [i for i in items if i.symbols and len(i.symbols) <= 2][:cfg.get("max_headlines", 3)]:
            try: v = self.brain.rate(sym, it.headline, it.summary, it.content, f)
            except Exception as e:
                log.warning("mr news rate failed %s: %s", sym, e); continue
            if v.direction == "bearish" and v.score >= cfg.get("veto_score", 6):
                return True, 0, f"bearish news ({v.score}/10): {it.headline[:70]}"
            if v.direction == "bullish" and v.score >= 7: bonus += 10; notes.append(f"bullish news: {it.headline[:50]}")
        return False, min(bonus, 20), "; ".join(notes)

    def _mr_scan(self, now):
        """mean-reversion longs (rules A/E): bull market only, strongest rule first"""
        s = self.r["swing"]; cfg = s.get("mr", {})
        if not cfg.get("enabled") or self.mkt.regime != "bull": return 0
        held = {p["symbol"] for p in self._pos()}
        cands = []
        for sym in s["watchlist"]:
            if sym in held: continue
            try:
                daily = self.b.bars(sym, "1Day", daily_start_iso(now))
                sig = mr.detect(daily, cfg.get("stop_atr", 4.0))
                if not sig: continue
                ok, why, pts = self._gate(sym, "long")
                if not ok: continue
                veto, bonus, nwhy = self._mr_news(now, sym, cfg)
                if veto:
                    self._j(now, sym, sig.notes, None, "swing", "long", "blocked", f"{sig.name}: {nwhy}"); continue
                cands.append((mr.RULES[sig.name]["rank"] + bonus, sym, sig, f"{why}; {nwhy}" if nwhy else why, daily))
            except Exception as e:
                log.warning("mr scan failed %s: %s", sym, e)
        cands.sort(key=lambda x: -x[0])
        taken = 0
        for rank, sym, sig, why, daily in cands:
            if taken >= cfg.get("new_per_day", 2): break
            if self._enter_signal(now, sym, "swing", sig, rank, f"{why}; {sig.notes}", True, daily): taken += 1
        return taken

    def _scan(self, now):
        s, held = self.r["swing"], {p["symbol"] for p in self._pos()}
        taken0 = self._mr_scan(now)
        taken0 += self._pattern_scan(now)
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
            eb = self._earnings_block(sym, "swing")
            if eb:
                self._j(now, sym, f"SCAN candidate rev_yoy={rev}%", None, "swing", "long", "blocked", eb); continue
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
        act = self.b.actives() if sg.get("use_actives") else []
        syms = [x for x in dict.fromkeys(list(gain) + list(lose) + list(act) + self.r["swing"]["watchlist"]) if x.isalpha()][:sg["max_symbols"]]
        held = {p["symbol"] for p in self._pos()}
        cands = []
        for sym in syms:
            if sym in held or sym in self.state["tried"]: continue
            try:
                bars5 = self.b.bars(sym, "5Min", session_open_iso(now))
                if len(bars5) < 6: continue
                daily_ctx = self._daily_cached(sym, now)
                ctx = self._prev_day(daily_ctx, now)
                sigs = patterns.detect_day(bars5, ctx, sg.get("detectors") or None, shorts=d["allow_short"])
                m15 = tf.resample_n(bars5, 3)
                if len(m15) >= 12:
                    only15 = {k: k in ("vwap_reclaim", "vwap_bounce", "intraday_flag") for k in patterns.DAY_DETECTORS}
                    for x in patterns.detect_day(m15, {}, only15, shorts=d["allow_short"]):
                        x.name += "_15m"; x.quality = min(1.0, x.quality + 0.05); sigs.append(x)
                off = self._disabled_patterns()
                for sig in sigs:
                    if sig.name.replace("_15m", "") in off or self._side_blocked(sig): continue
                    lvl = tf.near_level(daily_ctx, sig.price, sig.side) if daily_ctx else None
                    if lvl:
                        self._j(now, sym, f"DAY {sig.name}", None, "day", sig.side, "blocked", f"daily level {lvl:.2f} right in front"); continue
                    ok, why, pts = self._gate(sym, sig.side)
                    if not ok: continue
                    sc = confluence(sig.quality, pts, sig.volume_ok)
                    nt, tl = tools.count(sig, bars5, "day")
                    nt += 1 if pts > 0 else 0
                    if nt < sg.get("min_tools", 3): continue
                    why += f"; {nt} tools: {', '.join(tl)}"
                    if sc >= sg["min_confluence"] and not self._side_blocked(sig, sc, "day"): cands.append((sc, sym, sig, why))
            except Exception as e:
                log.warning("day scan failed %s: %s", sym, e)
        cands.sort(key=lambda x: -x[0])
        done = set()
        for sc, sym, sig, why in cands:
            if sym in done: continue
            done.add(sym)
            self._enter_signal(now, sym, "day", sig, sc, why, True)

    def _daily_cached(self, sym, now):
        """נרות יומיים פעם ביום לכל מניה (הקשר לסטאפים של יום: אתמול, רמות)"""
        key = now.astimezone(ZoneInfo("America/New_York")).date().isoformat()
        if getattr(self, "_dc_day", None) != key: self._dc, self._dc_day = {}, key
        if sym not in self._dc:
            try: self._dc[sym] = self.b.bars(sym, "1Day", daily_start_iso(now))
            except Exception: self._dc[sym] = []
        return self._dc[sym]

    @staticmethod
    def _prev_day(daily, now):
        """סגירה/שיא/שפל של יום המסחר הקודם. ריק אם אין נתונים"""
        if not daily: return {}
        today = now.astimezone(ZoneInfo("America/New_York")).date().isoformat()
        past = [b for b in daily if str(b.get("t", ""))[:10] < today]
        p = past[-1] if past else (daily[-2] if len(daily) >= 2 else None)
        return {"prev_close": p["c"], "prev_high": p["h"], "prev_low": p["l"]} if p else {}

    def _enter_signal(self, now, sym, strategy, sig, sc, why, is_open, daily=None):
        head = f"{strategy.upper()} {sig.name}: {sig.notes}"
        eb = self._earnings_block(sym, strategy)
        if eb:
            self._j(now, sym, head, None, strategy, sig.side, "blocked", eb); return False
        try:
            price, prev, adv = self.b.snapshot(sym)
            atr = (_atr(daily) if daily else None) or (abs(price - sig.stop) / 1.5)
            shortable = True
            if sig.side == "short":
                a = self.b.asset(sym); shortable = bool(a.get("shortable") and a.get("easy_to_borrow") and a.get("tradable", True))
            mult = size_mult(sc, self.r["signals"]["size_multiplier"]["min"], self.r["signals"]["size_multiplier"]["max"])
            if sig.name.startswith("mr_"): mult = self.r["swing"].get("mr", {}).get("size_mult", 2.5)
            if strategy == "swing" and self.r.get("research", {}).get("enforce"):
                ve = self._research()["validated"].get(f"{sig.name.replace('_W', '')}:{sig.side}")
                if ve: mult = round(max(self.r["signals"]["size_multiplier"]["min"], min(self.r["signals"]["size_multiplier"]["max"], mult * ve.get("mult", 1.0))), 2)
            ov = self._apply_exits(sig, price, atr) if strategy == "swing" else (sig.stop, sig.target)
            dec = evaluate_entry(self.r, strategy, sig.side, sym, price, prev, adv, self.b.account(), self._pos(), self.state,
                                 is_open, atr=atr, shortable=shortable, override=ov, size_mult=mult)
        except Exception as e:
            log.warning("signal eval failed %s: %s", sym, e)
            self._j(now, sym, head, None, strategy, sig.side, "error", str(e)); return False
        if strategy == "day": self.state["tried"].append(sym)
        if not dec.ok:
            self._j(now, sym, head, None, strategy, sig.side, "blocked", f"{dec.reason} conf={sc}"); return False
        return self._submit(now, sym, head, None, strategy, sig.side, dec, f"conf={sc} x{mult} {why}", price=price, atr=atr, pattern=sig.name)

    # --- ניהול פוזיציות פתוחות: ברייק-אבן וסטופ נגרר ---
    def _swing_stop(self, sym, m, now, price):
        """'הנמוך הבא': הפיבוט התחתון (לונג) / העליון (שורט) הקרוב ביותר למחיר, מעל הסטופ הנוכחי - ומתחתיו מרווח קטן"""
        try:
            bars = self.b.bars(sym, "1Day", daily_start_iso(now)) if m["strategy"] == "swing" else self.b.bars(sym, "5Min", session_open_iso(now))
            piv = pivots(bars[-80:], 2, 2); a = m.get("atr") or 0; buf = 0.1 * a
            if m["side"] == "long":
                c = [p[1] - buf for p in piv if p[2] == "L" and m["stop"] + 0.01 < p[1] - buf < price - 0.01]
                return max(c) if c else None
            c = [p[1] + buf for p in piv if p[2] == "H" and price + 0.01 < p[1] + buf < m["stop"] - 0.01]
            return min(c) if c else None
        except Exception as e:
            log.warning("swing stop failed %s: %s", sym, e)
            return None

    def scale_out(self, now, positions):
        """מימוש רווח חלקי ביעדי ביניים; אחרי כל יעד הסטופ מוצמד לנמוך (שיא לשורט) הבא; אחר כך נגרר לפי מבנה"""
        so = dict(self.r.get("scale_out", {}))
        if not so.get("enabled"): return
        ex = self._research()["exits"] if self.r.get("research", {}).get("enforce") else {}
        if ex.get("scale"): so["levels"] = [{"r": r, "pct": p} for r, p in ex["scale"]]
        for p in positions:
            sym = p["symbol"]; m = self.state["meta"].get(sym)
            if not m or not m.get("stop0") or not m.get("take") or p.get("asset_class") == "crypto" or str(m.get("pattern", "")).startswith("mr_"): continue
            try: price, entry, qty = float(p["current_price"]), float(p["avg_entry_price"]), abs(int(float(p["qty"])))
            except (KeyError, TypeError, ValueError): continue
            long = m["side"] == "long"; risk = abs(m["entry"] - m["stop0"]); done = m.setdefault("tp_done", [])
            if risk <= 0: continue
            tdist = abs(m["take"] - entry)
            for i, lv in enumerate(so.get("levels", [])):
                if i in done: continue
                dist = lv["r"] * risk
                if dist >= 0.9 * tdist: done.append(i); continue                  # היעד הסופי קרוב מדי - אין טעם בחלקי
                lvl = entry + dist if long else entry - dist
                if not (price >= lvl if long else price <= lvl): break
                chunk = max(1, int(m.get("qty0", qty) * lv["pct"] / 100))
                if qty - chunk < max(1, so.get("min_remaining", 1)): done.append(i); continue
                closing = "sell" if long else "buy"
                try:
                    self.b.partial_close(sym, chunk)
                    swing = self._swing_stop(sym, m, now, price)
                    prev = entry if i == 0 else (entry + so["levels"][i - 1]["r"] * risk if long else entry - so["levels"][i - 1]["r"] * risk)
                    new = max(swing or prev, prev) if long else min(swing or prev, prev)
                    if not (new < price - 0.01 if long else new > price + 0.01): new = prev
                    self.b.protect(sym, qty - chunk, closing, new, m["take"])
                except Exception as e:
                    self._j(now, sym, strategy=m["strategy"], side=m["side"], action="error", detail=f"order failed: partial TP {e}")
                    done.append(i); break
                usd = ((price - entry) if long else (entry - price)) * chunk
                m.setdefault("partials", []).append((chunk, price)); m["qty"] = qty - chunk; m["stop"] = round(new, 2); done.append(i)
                alerts.send(f"TAKE PROFIT {i + 1} {sym} {m['side']}: sold {chunk} @ {price:.2f} ({usd:+,.2f} USD)\nstop -> {new:.2f}, {qty - chunk} left", "NewsBot")
                journal([now.isoformat(), sym, "", "", "", "", "", m["strategy"], m["side"], "PARTIAL", f"TP{i + 1} sold {chunk} @ {price:.2f} stop->{new:.2f}", ""])
                break
            if done and so.get("structure_trail", True) and m.get("tp_done"):
                new = self._swing_stop(sym, m, now, price)
                if new and (new > m["stop"] + 0.01 if long else new < m["stop"] - 0.01):
                    try:
                        if self.b.raise_stop(sym, new):
                            self._j(now, sym, strategy=m["strategy"], side=m["side"], action="TRAIL", detail=f"structure stop {m['stop']} -> {round(new, 2)}")
                            m["stop"] = round(new, 2)
                    except Exception as e:
                        log.warning("structure trail failed %s: %s", sym, e)

    def manage_positions(self, now, positions):
        t = self.r.get("trailing", {})
        if not t.get("enabled"): return
        for p in positions:
            m = self.state["meta"].get(p["symbol"])
            if not m or not m.get("atr") or not m.get("stop") or str(m.get("pattern", "")).startswith("mr_"): continue
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

    def daily_report(self, now, mtc):
        today = str(date.today())
        if mtc is None or mtc > 4 or self.state.get("report_done") == today: return
        self.state["report_done"] = today
        try:
            _report.write(today, self.b.account(), self._pos(), JOURNAL, DATA / "journal_crypto.csv", DATA / "sectors.json", DATA)
            scorecard.write(DATA / "trades.csv", DATA)
            acct = self.b.account(); pnl = float(acct["equity"]) - float(acct["last_equity"])
            alerts.send(f"Day summary: {pnl:+,.2f} USD ({pnl / float(acct['last_equity']) * 100:+.2f}%)\nEquity {float(acct['equity']):,.2f}", "NewsBot daily")
        except Exception as e:
            log.warning("report failed: %s", e)

    def _research(self):
        """תוצרי research.py: תבניות מאומתות (whitelist + משטרי שוק + מכפיל גודל), מסנני מאפיינים, והגדרות יציאה"""
        out = {"validated": {}, "filters": {}, "exits": {}}
        for k, f in (("validated", "validated.json"), ("filters", "filters.json"), ("exits", "exits.json")):
            try:
                d = json.loads((DATA / f).read_text(encoding="utf-8"))
                out[k] = d.get("patterns", {}) if k == "validated" else d
            except Exception: pass
        return out

    def _research_ok(self, sig, feat, rs):
        """False = לדלג. whitelist רק כשיש מספיק תבניות מאומתות; מסננים לפי מאפיינים; משטר שוק מתאים"""
        cfg = self.r.get("research", {})
        if not cfg.get("enforce"): return True
        v = rs["validated"]; base = sig.name.replace("_W", "")
        if len(v) >= cfg.get("min_validated", 5):
            e = v.get(f"{base}:{sig.side}")
            if not e: return False
            if self.mkt.regime in ("bull", "bear", "neutral") and self.mkt.regime not in e.get("regimes", []): return False
        return _feat.passes(feat, (rs["filters"] or {}).get(sig.side))

    def _hold_days(self):
        ex = self._research()["exits"] if self.r.get("research", {}).get("enforce") else {}
        return int(ex.get("hold") or self.r["swing"]["max_hold_days"])

    def _apply_exits(self, sig, price, atr):
        """הגדרות יציאה שנבחרו במחקר (רק אם שיפרו גם על נתוני האימות וגם על ה-holdout)"""
        ex = self._research()["exits"]
        if not ex or not self.r.get("research", {}).get("enforce"): return sig.stop, sig.target
        long = sig.side == "long"; stop, target = sig.stop, sig.target
        if ex.get("stop_atr") and atr: stop = price - ex["stop_atr"] * atr if long else price + ex["stop_atr"] * atr
        risk = abs(price - stop)
        if ex.get("target_r"): target = price + ex["target_r"] * risk if long else price - ex["target_r"] * risk
        elif ex.get("no_target"): target = price + 6 * risk if long else price - 6 * risk
        ok = (stop < price < target) if long else (target < price < stop)
        return (stop, target) if ok and risk > 0 else (sig.stop, sig.target)

    def _bt(self):
        try: return json.loads((DATA / "backtest.json").read_text(encoding="utf-8"))
        except Exception: return {}

    def _side_blocked(self, sig, sc=None, strategy="swing"):
        """True = דלג: כיוון שה-backtest הראה שמפסיד, או short בלי הוכחת edge (רק ב-bear ובביטחון גבוה)"""
        bt = self._bt(); base = sig.name.replace("_15m", "").replace("_W", "")
        if f"{base}:{sig.side}" in set(bt.get("disabled_sides", [])): return True
        if sig.side == "short":
            st = (bt.get("stats") or {}).get("ALL_short")
            if st and st["n"] >= 100 and ((st["profit_factor"] or 0) < 1.0 or st["avg_R"] < 0):
                need = self.r.get("signals", {}).get(strategy, {}).get("min_confluence", 45) + 10
                if self.mkt.regime != "bear" or (sc is not None and sc < need): return True
        return False

    def _disabled_patterns(self):
        """גלאים שה-backtest סימן כמפסידים (data/backtest.json) - מכבים אוטומטית"""
        out = set()
        for f in ("backtest.json", "scorecard.json"):
            try: out |= set(json.loads((DATA / f).read_text(encoding="utf-8")).get("disabled", []))
            except Exception: pass
        return out

    def track_positions(self, now, positions):
        """רושם מחיר אחרון ואת ההחלקה בכניסה (מחיר מבוקש מול מחיר מילוי)"""
        for p in positions:
            m = self.state["meta"].get(p["symbol"])
            if not m: continue
            try: m["last"] = float(p["current_price"])
            except (KeyError, TypeError, ValueError): pass
            if "fill" not in m:
                try: fill = float(p["avg_entry_price"])
                except (KeyError, TypeError, ValueError): continue
                m["fill"] = fill
                if m.get("entry"):
                    m["slip"] = round(((fill / m["entry"] - 1) if m["side"] == "long" else (m["entry"] / fill - 1)) * 100, 3)
                    self._j(now, p["symbol"], strategy=m["strategy"], side=m["side"], action="FILL", detail=f"wanted {m['entry']:.2f} got {fill:.2f} slippage {m['slip']}%")

    def _record_trade(self, sym, m):
        try:
            fill = m.get("fill") or m.get("entry")
            if not fill: return
            exit_px = None
            try: exit_px = self.b.last_fill(sym, "sell" if m["side"] == "long" else "buy")
            except Exception: pass
            exit_px = exit_px or m.get("last")
            if not exit_px: return
            if m.get("partials"):                           # ממוצע משוקלל של המימושים החלקיים והיציאה האחרונה
                rem = max(0, m.get("qty") or 0); tot = rem + sum(q for q, _ in m["partials"])
                if tot: exit_px = (sum(q * px for q, px in m["partials"]) + rem * exit_px) / tot
            long = m["side"] == "long"
            pnl = ((exit_px / fill - 1) if long else (fill / exit_px - 1)) * 100
            risk = abs(fill - m["stop0"]) if m.get("stop0") else 0
            r = ((exit_px - fill) if long else (fill - exit_px)) / risk if risk else ""
            held = weekdays_between(m["entry_date"], str(date.today())) if m.get("entry_date") else ""
            reason = "stop/target/other"
            scorecard.append_trade(DATA / "trades.csv", {"closed": datetime.now(timezone.utc).isoformat(), "symbol": sym, "strategy": m["strategy"],
                                   "pattern": m.get("pattern", ""), "side": m["side"], "entry": round(fill, 4), "exit": round(exit_px, 4),
                                   "pnl_pct": round(pnl, 3), "R": round(r, 2) if r != "" else "", "held_days": held,
                                   "entry_slip_pct": m.get("slip", ""), "reason": reason})
            usd = ((exit_px - fill) if long else (fill - exit_px)) * (m.get("qty0") or m.get("qty") or 0)
            icon = "WIN" if pnl > 0 else "LOSS"
            alerts.send(f"{icon} {sym} {m['strategy']} {m['side']}: {pnl:+.2f}%" + (f" ({usd:+,.2f} USD)" if m.get("qty") else "") +
                        f"\nentry {fill:.2f} -> exit {exit_px:.2f}", "NewsBot")
        except Exception as e:
            log.warning("record trade failed %s: %s", sym, e)

    def reconcile(self, positions):
        held, t = {p["symbol"] for p in positions}, time.time()
        for sym in list(self.state["meta"]):
            if sym not in held and t - self.state["meta"][sym].get("ts", 0) > 600:
                self._record_trade(sym, self.state["meta"][sym])
                del self.state["meta"][sym]
                self.state.setdefault("cool", {})[sym] = t

    def step(self, now=None):
        now = now or datetime.now(timezone.utc)
        self.state = roll(self.state)
        c = self.b.clock()
        if not c["is_open"]:
            try: self.premarket(now, c)
            except Exception as e: log.warning("premarket failed: %s", e)
            save_state(self.state)
            if self.r["account"]["market_hours_only"]: return c
        mtc = (_ts(c["next_close"]) - _ts(c["timestamp"])).total_seconds() / 60 if c.get("next_close") else None
        self.mkt.refresh(now)
        self.mkt.refresh_risk()
        self._write_sectors()
        positions = self._pos()
        self.reconcile(positions)
        self.day_flatten(mtc, positions)
        self.track_positions(now, positions)
        self.scale_out(now, positions)
        self.manage_positions(now, positions)
        self.process_queue(now, mtc, c["is_open"])
        self.news_pass(now, mtc, c["is_open"])
        self.day_scan(now, mtc, c["is_open"])
        self.swing_pass(now, mtc)
        self.daily_report(now, mtc)
        save_state(self.state)
        return c

def _fmt(snap):
    return json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in (snap or {}).items()}) if snap else ""

# ---------- runners ----------
def session(engine, max_minutes=345, early_minutes=100, sleep=time.sleep):
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
            errs = getattr(engine, "_errs", 0) + 1; engine._errs = errs
            if errs in (3, 20): alerts.send(f"Bot loop error x{errs}: {str(e)[:200]}", "NewsBot ERROR")
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
    engine = Engine(AlpacaBroker(paper=not live), Brain(), rules, load_state(), Fundamentals(), Earnings())
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
