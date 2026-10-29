import review

def test_gather_collects_files(tmp_path):
    (tmp_path / "reports").mkdir()
    (tmp_path / "scorecard.md").write_text("SC", encoding="utf-8")
    (tmp_path / "reports" / "2026-10-28.md").write_text("R1", encoding="utf-8")
    g = review.gather(str(tmp_path))
    assert "SC" in g and "R1" in g and review.gather(str(tmp_path / "none")) == "(no data yet)"
