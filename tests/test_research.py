import random, research, features

def bar(o, h, l, c, v=1e6, t="2024-01-01"): return {"t": t, "o": o, "h": h, "l": l, "c": c, "v": v}

def _path(highs, lows, closes, start=100):
    bars = [bar(start, start + 1, start - 1, start)]
    for k, (h, l, c) in enumerate(zip(highs, lows, closes)): bars.append(bar(closes[k - 1] if k else start, h, l, c))
    return bars

def test_run_trade_stop_target_time_and_scale():
    rec = {"i": 0, "p": "x", "side": "long", "stop": 95, "target": 115, "t": "2024-01-01", "sym": "S", "f": {}, "tools": 3, "atr": 2}
    cfg = {"stop": "pattern", "stop_k": None, "target": "pattern", "target_k": None, "hold": 10, "scale": []}
    hit_t = research.run_trade(_path([106, 116], [99, 104], [105, 115]), rec, cfg)
    assert hit_t["R"] > 2.5                                           # יעד 115: ~+3R
    hit_s = research.run_trade(_path([101, 102], [94, 94], [96, 95]), rec, cfg)
    assert -1.3 < hit_s["R"] < -0.9                                   # סטופ
    tm = research.run_trade(_path([101] * 3, [99] * 3, [100.5] * 3), rec, dict(cfg, hold=2))
    assert tm["held"] == 2 and abs(tm["R"]) < 0.3                     # יציאת זמן
    sc = dict(cfg, scale=[(1.0, 50)])
    s1 = research.run_trade(_path([106, 106, 100.5], [99, 99, 99], [105, 105, 100]), rec, sc)   # TP1 ב-105 ואז חוזר לברייק-אבן
    assert s1["R"] > 0.35 and s1["R"] < 0.6                           # חצי ב-+1R, חצי בברייק-אבן
    short = {"i": 0, "p": "x", "side": "short", "stop": 105, "target": 85, "t": "2024-01-01", "sym": "S", "f": {}, "tools": 3, "atr": 2}
    st = research.run_trade(_path([101, 100], [94, 84], [95, 86]), short, cfg)
    assert st["R"] > 2.5

def test_filter_search_keeps_only_confirmed_rules():
    random.seed(3)
    mk = lambda good, day: {"f": {"rvol": (2.0 if good else 0.7) + random.random() * .2, "adx": random.random() * 40}, "R": (0.6 if good else -0.4) + random.gauss(0, .5),
                            "pnl_pct": 1.0, "side": "long", "pattern": "p", "t": day}
    train = [mk(i % 2 == 0, "2023-01-01") for i in range(600)]; test = [mk(i % 2 == 0, "2024-06-01") for i in range(300)]
    rules = research.search_filters(train, test)
    assert rules and rules[0]["f"] == "rvol" and rules[0]["op"] == ">="
    noise_tr = [{"f": {"rvol": random.random()}, "R": random.gauss(0, 1), "pnl_pct": 0, "side": "long", "pattern": "p", "t": "x"} for _ in range(600)]
    noise_te = [{"f": {"rvol": random.random()}, "R": random.gauss(0, 1), "pnl_pct": 0, "side": "long", "pattern": "p", "t": "y"} for _ in range(300)]
    assert len(research.search_filters(noise_tr, noise_te)) <= 1      # רעש לא אמור לייצר כללים (בדרך כלל 0)

def test_validate_requires_both_periods():
    mk = lambda p, side, R, n, day: [{"pattern": p, "side": side, "R": R if i % 3 else -1.0, "pnl_pct": R, "t": day, "regime": "bull", "f": {}} for i in range(n)]
    train = mk("good", "long", 1.0, 40, "2023-01-01") + mk("lucky", "long", 1.0, 40, "2023-01-01")
    test = mk("good", "long", 1.0, 20, "2024-06-01") + mk("lucky", "long", -0.5, 20, "2024-06-01")     # lucky מתמוטט על נתונים חדשים
    v = research.validate(train, test)
    assert "good:long" in v and "lucky:long" not in v

def test_split_and_filter_pass():
    assert research.split_cut([{"t": f"2023-01-{d:02d}"} for d in range(1, 10)]) == "2023-01-07"
    assert features.passes({"rvol": 2}, [{"f": "rvol", "op": ">=", "v": 1.5}]) and not features.passes({"rvol": 1}, [{"f": "rvol", "op": ">=", "v": 1.5}])
    assert features.passes({}, [{"f": "rvol", "op": ">=", "v": 1.5}])      # מאפיין חסר לא חוסם

def test_selection_bias_is_exposed_by_holdout():
    """על רעש טהור: מה שנבחר על A+B נראה טוב על B אבל על C (שלא נגענו בו) התוחלת ~0"""
    random.seed(11)
    A, B, C = [], [], []
    for k in range(80):                         # 80 תבניות ללא edge
        for bucket, day in ((A, "2021"), (B, "2023"), (C, "2025")):
            for _ in range(60):
                R = random.gauss(0, 1)
                bucket.append({"pattern": f"p{k}", "side": "long", "R": R, "pnl_pct": R, "t": day, "regime": "bull", "f": {}})
    v = research.validate(A, B, min_tr=20, min_te=8)
    keep = lambda ts: [t for t in ts if f"{t['pattern']}:{t['side']}" in v]
    on_b, on_c = research.stat(keep(B)), research.stat(keep(C))
    assert len(v) >= 1 and on_b["avgR"] > on_c["avgR"] + 0.05          # הנפח "נראה" טוב ב-B רק בגלל הבחירה
    assert abs(on_c["avgR"]) < 0.2                                     # ב-holdout אין edge אמיתי

def test_pipeline_has_three_periods():
    import inspect
    assert "holdout" in inspect.getsource(research.pipeline) and "res[\"cut2\"]" in inspect.getsource(research.main)
