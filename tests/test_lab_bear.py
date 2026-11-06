import lab_bear

def test_bear_sleeve_only_trades_when_spy_below_200d():
    import sweep
    n = 300
    A = sweep.build([{"t": f"2021-01-{1+i%28:02d}T{i}", "o": 100.0, "h": 101.0, "l": 99.0, "c": 100.0, "v": 1} for i in range(n)])
    A["t"] = [f"d{i}" for i in range(n)]
    ctx_bull = {"a200": {f"d{i}": True for i in range(n)}, "reg": {}}
    assert lab_bear.bear_long({"X": A}, ctx_bull) == []
