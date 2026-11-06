import lab_breadth, sweep

def test_breadth_series_counts_oversold_fraction():
    n = 40
    def mk(down):
        bars = [{"t": f"2021-01-01T{i:03d}", "o": 100.0, "h": 101.0, "l": 99.0, "c": (100.0 - (i if down and i > 30 else 0)), "v": 1} for i in range(n)]
        A = sweep.build(bars); A["t"] = [f"d{i:03d}" for i in range(n)]; return A
    AS = {f"S{k}": mk(k < 10) for k in range(40)}
    B = lab_breadth.breadth_series(AS)
    assert B["d039"][0] == 10 / 40 and B["d039"][1] == 1.0  # flat stocks tie at the 5d low
    assert B["d010"][0] == 0
