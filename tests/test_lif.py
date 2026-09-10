# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

from fly_abgcrz.lif_toy import (
    GAIN_NOTE,
    THRESHOLD_HZ,
    THRESHOLD_NOTE,
    run_toy,
    write_log,
)

REPO = Path(__file__).resolve().parents[1]


def test_toy_does_not_cross_invented_bar() -> None:
    result = run_toy()
    assert result["n_partners"] == 20
    assert result["n_abnt_effectors"] == 13
    assert result["threshold_hz"] == THRESHOLD_HZ == 40.0
    assert result["threshold_note"] == THRESHOLD_NOTE
    assert result["gain_note"] == GAIN_NOTE
    assert result["crossed"] is False
    assert abs(result["abnt_mean_hz"] - 1052 / 39) < 1e-9
    assert "does not cross" in result["print_line"]
    assert "orgasm" not in result["print_line"].lower()
    assert THRESHOLD_NOTE not in result["print_line"]
    abnt = [r for r in result["rates"] if r["abnt_effector"]]
    assert [r["bodyId"] for r in abnt[:4]] == [808163, 809974, 907835, 814470]
    assert abnt[0]["hz"] == 50.0
    locked = json.loads((REPO / "logs" / "lif_toy.json").read_text(encoding="utf-8"))
    assert locked["crossed"] is False
    assert locked["abnt_mean_hz"] == result["abnt_mean_hz"]
    assert locked["threshold_note"] == THRESHOLD_NOTE


def test_write_log_roundtrip(tmp_path: Path, monkeypatch) -> None:
    import fly_abgcrz.lif_toy as lif_toy

    result = run_toy()
    monkeypatch.setattr(lif_toy, "LOGS", tmp_path)
    out = write_log(result)
    raw = json.loads((tmp_path / "lif_toy.json").read_text(encoding="utf-8"))
    assert raw["crossed"] == out["crossed"]
    assert raw["n_partners"] == 20
