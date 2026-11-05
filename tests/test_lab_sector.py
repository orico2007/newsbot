import challenger

def test_post_peers_filter_and_rank():
    T = [{"sym": "A", "t": "d1", "score": 90}, {"sym": "B", "t": "d1", "score": 60}, {"sym": "C", "t": "d1", "score": 50}]
    F = {("A", "d1"): {"m3": -2.0}, ("B", "d1"): {"m3": 1.0}}
    assert [t["sym"] for t in challenger.post(T, "peers_lt0", F)] == ["A"]
    r = challenger.post(T, "peers_rank", F)
    assert [t["sym"] for t in r] == ["A", "B"] and r[0]["score"] == 2.0 and r[1]["score"] == -1.0
    assert challenger.post(T, "other", F) is T
