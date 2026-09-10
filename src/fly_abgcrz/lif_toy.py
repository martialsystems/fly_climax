# Copyright (c) 2026 Martial Systems LLC
"""One-synapse LIF toy: four command cells clamped, top-20 hop-1 partners."""
from __future__ import annotations

import json
from typing import Any

import numpy as np

from fly_abgcrz.paths import LOGS

THRESHOLD_NOTE = "The ejaculation threshold is invented and is not biology."
GAIN_NOTE = (
    "0.01 mV per contact is a grid pick because 0.005 left AbNT silent, "
    "not a fly biophysics constant."
)
FOUR = (800571, 800986, 802096, 904047)
THRESHOLD_HZ = 40.0
CLAMP_HZ = 100.0
PULSE_S = 3.0
DT_MS = 0.5
TAU_M_MS = 20.0
V_REST_MV = -52.0
V_THRESH_MV = -45.0
V_RESET_MV = -52.0
REFRACTORY_MS = 2.0
MV_PER_CONTACT = 0.01


def load_partners(path: Any | None = None) -> list[dict]:
    raw = json.loads((path or (LOGS / "hop1_top20.json")).read_text(encoding="utf-8"))
    return list(raw["partners"])


def is_abnt_effector(row: dict) -> bool:
    return bool(row.get("abnt") and (row.get("is_efferent") or row.get("is_motor")))


def run_toy(partners: list[dict] | None = None) -> dict:
    partners = partners if partners is not None else load_partners()
    n = len(partners)
    if n != 20:
        raise ValueError(f"toy is one-synapse hop to the top 20 partners, got {n}")
    weights = np.array([[int(p[f"from_{c}"]) for c in FOUR] for p in partners], dtype=float)
    abnt_mask = np.array([is_abnt_effector(p) for p in partners], dtype=bool)
    steps = int(round(PULSE_S * 1000.0 / DT_MS))
    period = int(round((1000.0 / CLAMP_HZ) / DT_MS))
    refrac_steps = int(round(REFRACTORY_MS / DT_MS))
    v = np.full(n, V_REST_MV, dtype=float)
    refrac = np.zeros(n, dtype=int)
    spikes = np.zeros(n, dtype=np.int64)
    add = (weights * MV_PER_CONTACT).sum(axis=1)
    for t in range(steps):
        v += (V_REST_MV - v) * (DT_MS / TAU_M_MS)
        holding = refrac > 0
        v[holding] = V_RESET_MV
        if t % period == 0:
            v += add
        fire = (v >= V_THRESH_MV) & (refrac == 0)
        spikes += fire
        v[fire] = V_RESET_MV
        refrac[fire] = refrac_steps
        refrac = np.maximum(refrac - 1, 0)
    hz = spikes.astype(float) / PULSE_S
    abnt_hz = hz[abnt_mask]
    abnt_mean = float(abnt_hz.mean()) if abnt_mask.any() else 0.0
    crossed = bool(abnt_mean >= THRESHOLD_HZ)
    rates = []
    for i, p in enumerate(partners):
        rates.append(
            {
                "bodyId": int(p["bodyId"]),
                "type": p.get("type"),
                "hop1_weight": int(p["hop1_weight"]),
                "abnt_effector": bool(abnt_mask[i]),
                "spikes": int(spikes[i]),
                "hz": float(hz[i]),
            }
        )
    return {
        "command": list(FOUR),
        "clamp_hz": CLAMP_HZ,
        "pulse_s": PULSE_S,
        "n_partners": n,
        "n_abnt_effectors": int(abnt_mask.sum()),
        "mV_per_contact": MV_PER_CONTACT,
        "gain_note": GAIN_NOTE,
        "threshold_hz": THRESHOLD_HZ,
        "threshold_note": THRESHOLD_NOTE,
        "abnt_mean_hz": abnt_mean,
        "abnt_max_hz": float(abnt_hz.max()) if abnt_mask.any() else 0.0,
        "crossed": crossed,
        "rates": rates,
        "print_line": (
            f"AbNT effector mean {abnt_mean:.3f} Hz "
            f"{'crosses' if crossed else 'does not cross'} "
            f"invented threshold {THRESHOLD_HZ:.0f} Hz."
        ),
    }


def write_log(result: dict | None = None) -> dict:
    result = result if result is not None else run_toy()
    (LOGS / "lif_toy.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    return result
