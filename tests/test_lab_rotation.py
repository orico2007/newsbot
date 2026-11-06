import lab_rotation

def _bars(n, drift):
    import datetime
    d0 = datetime.date(2020, 1, 1); out = []; p = 100.0; k = 0; day = d0
    while len(out) < n:
        day += datetime.timedelta(days=1)
        if day.weekday() >= 5: continue
        p *= 1 + drift; out.append({"t": day.isoformat() + "T00:00:00Z", "o": p, "h": p, "l": p, "c": p, "v": 1})
    return out

def test_rotation_picks_strongest_and_exits_after_hold():
    n = 600
    bars = {"SPY": _bars(n, 0.0005), "UP": _bars(n, 0.002), "FLAT": _bars(n, 0.0), "DOWN": _bars(n, -0.001)}
    T = lab_rotation.rotation(bars, ["UP", "FLAT", "DOWN"], 252, 21, 1, False, hold=21, ctx={"a200": {}})
    assert T and all(t["sym"] == "UP" for t in T)
    assert all(t["held"] == 21 and t["pnl_pct"] > 0 for t in T)
    # gate on with an empty regime map blocks everything
    assert lab_rotation.rotation(bars, ["UP"], 252, 21, 1, True, ctx={"a200": {}}) == []
