# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LOGS = REPO / "logs"
UNL = [
    814470,
    936838,
    815445,
    808454,
    816976,
    818737,
    800930,
    808456,
    909643,
    808457,
    911713,
    802978,
    810859,
]
OGN = [808163, 809974, 907835, 804275]


def test_unlabeled_map_does_not_invent_serotonin() -> None:
    raw = json.loads((LOGS / "unlabeled_abnt.json").read_text(encoding="utf-8"))
    hop = json.loads((LOGS / "drive_summary.json").read_text(encoding="utf-8"))
    assert hop["hop1"]["total_weight"] == 24234
    assert hop["serotonin"]["accessory_gland_step"] == "missing"
    assert raw["consensus_serotonin_abnt_n"] == 0
    assert [r["bodyId"] for r in raw["unlabeled_abnt"]] == UNL
    assert [r["bodyId"] for r in raw["en00b010_controls"]] == OGN
    for r in raw["unlabeled_abnt"]:
        assert r["type"] is None
        assert r["superclass"] == "vnc_efferent"
        assert r["exitNerve"] == "AbNT"
        assert r["consensus_nt"] == "unclear"
        assert r["predicted_nt"] == "unclear"
        assert r["consensus_serotonin"] is False
        assert r["mancType"] is None
        assert r["maggio_chaverra"] == "unknown"
        assert r["evidence_grade"] == "no data"
        assert r["axon_after_AbNT"].startswith("no organ target")
    missing_manc = [r["bodyId"] for r in raw["unlabeled_abnt"] if r["mancBodyid"] is None]
    assert missing_manc == [936838]
    for r in raw["en00b010_controls"]:
        assert r["type"] == "EN00B010"
        assert r["mancType"] == "EN00B010"
        assert r["consensus_nt"] == "octopamine"
        assert r["maggio_chaverra"] == "OGN-like"
        assert r["evidence_grade"] == "morphological guess"
        assert r["consensus_serotonin"] is False


def test_readme_quotes_unlabeled_map() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert "logs/unlabeled_abnt.json" in text
    assert "OGN-like" in text
    assert "The Tayler SGN step is not in these 13 as identified 5-HT." in text
    assert "Hop tables not rebuilt." in text
    assert "\u2014" not in text
    assert "orgasmed" not in text.lower()
