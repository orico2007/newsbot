import market as M, scoring as S
from tests.test_patterns import ramp, flat

def test_regime_bull_bear():
    assert M.regime(ramp(80, 120, 220)) == "bull"
    assert M.regime(ramp(120, 80, 220)) == "bear"
    assert M.regime(ramp(100, 101, 20)) == "neutral"

def test_sector_ranking_orders_leaders_first():
    spy = ramp(100, 105, 80)
    r = M.rank_sectors({"XLK": ramp(100, 125, 80), "XLU": ramp(100, 95, 80), "XLE": ramp(100, 105, 80)}, spy)
    assert [x["etf"] for x in r][0] == "XLK" and r[-1]["etf"] == "XLU"

class FakeB:
    def __init__(self): self.d = {"SPY": ramp(100, 110, 220)}
    def bars(self, s, tf, start): return self.d.get(s, ramp(100, 100, 80))

def test_alignment_veto_and_bonus():
    b = FakeB(); b.d["SMH"] = ramp(100, 140, 220); b.d["XLU"] = ramp(100, 80, 220)
    m = M.Market(b, {"enabled": True, "top_n": 2, "veto_against": True}, lambda n: "x")
    m.refresh(None, force=True)
    assert m.regime == "bull"
    veto, pts, _ = m.alignment("NVDA", "long")
    assert not veto and pts > 0.9
    assert m.alignment("NEE", "long")[0] is True        # סקטור חלש = וטו ללונג
    assert m.alignment("NVDA", "short")[0] is True      # שורט בסקטור מוביל בשוק שורי = וטו
    assert m.alignment("ZZZZ", "long")[0] is False      # לא ממופה = לא חוסמים

def test_confluence_and_size():
    hi = S.confluence(0.9, 1.0, True, 10, True, True, 20)
    lo = S.confluence(0.5, -1.0, False, 9, False, False)
    assert hi > 80 > 40 > lo
    assert S.size_mult(lo) == 0.5 and S.size_mult(hi) > 1.4 and S.size_mult(62) == 1.0 or 0.9 < S.size_mult(62) < 1.1
