# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

from fly_climax import FLY_INDEX_GIST, FLY_INDEX_ID, FOUR, QUESTION, SENSITIVITY
from fly_climax.claims import scan_text
from fly_climax.lif_toy import GAIN_NOTE, THRESHOLD_NOTE

REPO = Path(__file__).resolve().parents[1]


def test_readme_quotes_locks() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    summary = json.loads((REPO / "logs" / "drive_summary.json").read_text(encoding="utf-8"))
    working = json.loads((REPO / "logs" / "working_set.json").read_text(encoding="utf-8"))
    hop1 = json.loads((REPO / "logs" / "hop1.json").read_text(encoding="utf-8"))
    lif = json.loads((REPO / "logs" / "lif_toy.json").read_text(encoding="utf-8"))
    assert text.startswith("# fly_climax\n")
    assert "Climax is not simulated." in text
    assert "| Orgasm simulated? | No |" in text
    assert "| Did you find named abgCrz in MaleCNS? | No |" in text
    assert "not typed Crz" in text
    assert "Do not run another ejaculation threshold." in text
    assert QUESTION in text
    assert "24,234" in text
    assert "7,776" in text
    assert "0.4785" in text
    assert "0.3356" in text
    assert "0.3209" in text
    assert str(summary["hop1"]["total_weight"])[:2] == "24"
    assert summary["hop1"]["abnt_efferent_or_motor_weight"] == 7776
    assert summary["hop1"]["sgn_like_hole_n"] == 13
    assert summary["serotonin"]["accessory_gland_step"] == "missing"
    assert working["identity"] == "candidate"
    assert working["four"] == list(FOUR)
    assert working["sensitivity"] == list(SENSITIVITY)
    for body in FOUR:
        assert str(body) in text
    assert "INXXX149" in text
    assert "801013" in text and "800166" in text
    assert "808163" in text
    assert "814470" in text
    assert "EN00B010" in text
    assert hop1["unlabeled_abnt_efferents"][0]["bodyId"] == 814470
    assert "missing" in text.lower()
    assert "NeuronBridge" in text
    assert "Crz-GAL4" in text
    assert THRESHOLD_NOTE in text
    assert GAIN_NOTE in text
    assert "26.974" in text
    assert "does not cross" in text
    assert lif["crossed"] is False
    assert ".venv/bin/python" in text
    assert "logs/drive_summary.json" in text
    assert "CC BY" in (REPO / "THIRD_PARTY.md").read_text(encoding="utf-8")
    assert "What it is not" not in text
    assert "\u2014" not in text
    assert scan_text(text) == []
    assert "orgasmed" not in text.lower()
    footer = f"Fly research index: {FLY_INDEX_GIST}"
    assert footer in text
    assert FLY_INDEX_ID in text
    assert FLY_INDEX_ID != "REPLACE_FLY_INDEX"
    assert "identity is locked" not in text.lower()
