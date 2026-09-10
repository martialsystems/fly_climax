# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

from fly_abgcrz import FOUR, SENSITIVITY, TYPE
from fly_abgcrz.claims import scan_log_claim_fields

REPO = Path(__file__).resolve().parents[1]
LOGS = REPO / "logs"


def test_working_set() -> None:
    working = json.loads((LOGS / "working_set.json").read_text(encoding="utf-8"))
    assert working["four"] == list(FOUR)
    assert working["sensitivity"] == list(SENSITIVITY)
    assert working["type"] == TYPE
    assert working["identity"] == "candidate"
    assert working["do_not_search"] == ["CRZ01", "CRZ02"]


def test_hop1_totals() -> None:
    summary = json.loads((LOGS / "drive_summary.json").read_text(encoding="utf-8"))
    hop1 = json.loads((LOGS / "hop1.json").read_text(encoding="utf-8"))
    h = summary["hop1"]
    assert h["total_weight"] == 24234
    assert h["n_posts"] == 457
    assert h["abnt_efferent_or_motor_weight"] == 7776
    assert h["abnt_efferent_weight"] == 6891
    assert h["abnt_motor_weight"] == 885
    assert h["local_ag_a7a9_intrinsic_weight"] == 11596
    assert h["vnc_efferent_or_motor_weight"] == 8132
    assert h["ogn_like_weight"] == 3327
    assert h["ogn_like_n"] == 21
    assert h["sgn_like_hole_n"] == 13
    assert h["sgn_like_hole_weight"] == 3564
    assert h["en00b010_weight"] == 1636
    assert abs(h["frac_local_ag_a7a9"] - 11596 / 24234) < 1e-12
    assert abs(h["frac_exiting_effectors"] - 8132 / 24234) < 1e-12
    assert hop1["en00b"][0]["bodyId"] == 808163
    assert hop1["en00b"][0]["type"] == "EN00B010"
    assert hop1["en00b"][0]["consensus_nt"] == "octopamine"
    assert all(r["consensus_nt"] == "octopamine" for r in hop1["en00b"])
    assert all(r["consensus_nt"] != "octopamine" for r in hop1["sgn_like_hole"])
    assert [r["bodyId"] for r in hop1["unlabeled_abnt_efferents"]] == [
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
    assert hop1["mnad"][0]["bodyId"] == 802114
    assert FOUR[0] not in {r["bodyId"] for r in hop1["sgn_like_hole"]}


def test_hop2_totals() -> None:
    summary = json.loads((LOGS / "drive_summary.json").read_text(encoding="utf-8"))
    hop2 = json.loads((LOGS / "hop2.json").read_text(encoding="utf-8"))
    h = summary["hop2"]
    assert h["total_weight"] == 850051
    assert h["abnt_efferent_or_motor_weight"] == 154333
    assert h["n_posts"] == 11675
    assert hop2["en00b"][0]["bodyId"] == 903484
    assert hop2["unlabeled_abnt_efferents"][0]["bodyId"] == 936838
    assert hop2["mnad"][0]["bodyId"] == 802201


def test_serotonin_missing() -> None:
    summary = json.loads((LOGS / "drive_summary.json").read_text(encoding="utf-8"))
    ser = summary["serotonin"]
    assert ser["consensus_abnt_n"] == 0
    assert ser["consensus_vnc_efferent_or_motor_n"] == 0
    assert ser["accessory_gland_step"] == "missing"
    assert ser["predicted_abnt"][0]["bodyId"] == 806679
    assert ser["predicted_abnt"][0]["hop1_weight"] == 0


def test_log_claim_fields() -> None:
    for name in (
        "drive_summary.json",
        "working_set.json",
        "hop1.json",
        "hop2.json",
        "lif_toy.json",
    ):
        scan_log_claim_fields(LOGS / name)
