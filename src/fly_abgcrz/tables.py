# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from typing import Any, Iterable

from fly_abgcrz.paths import LOGS


def _load(name: str) -> Any:
    return json.loads((LOGS / name).read_text(encoding="utf-8"))


def _md(headers: list[str], rows: Iterable[Iterable[object]]) -> str:
    line = "| " + " | ".join(headers) + " |"
    align = []
    for h in headers:
        align.append("---:" if h.lower() in {"w", "hop1", "hop2", "n", "hz", "conf"} or "weight" in h.lower() else "---")
    sep = "| " + " | ".join(align) + " |"
    body = ["| " + " | ".join("" if c is None else str(c) for c in row) + " |" for row in rows]
    return "\n".join([line, sep, *body])


def hop_tables() -> str:
    summary = _load("drive_summary.json")
    hop1 = _load("hop1.json")
    hop2 = _load("hop2.json")
    h1 = summary["hop1"]
    h2 = summary["hop2"]
    chunks = []
    chunks.append("## Hop-1 from FOUR (weight = synapse count)")
    chunks.append(
        _md(
            ["pool", "n", "weight", "fraction"],
            [
                ["total", h1["n_posts"], h1["total_weight"], "1"],
                [
                    "local AG INs (A7-A9 vnc_intrinsic)",
                    h1["local_ag_a7a9_intrinsic_n"],
                    h1["local_ag_a7a9_intrinsic_weight"],
                    f"{h1['frac_local_ag_a7a9']:.4f}",
                ],
                [
                    "all vnc_intrinsic",
                    None,
                    h1["vnc_intrinsic_weight"],
                    f"{h1['frac_vnc_intrinsic']:.4f}",
                ],
                [
                    "exiting effectors (vnc_efferent + vnc_motor)",
                    h1["vnc_efferent_or_motor_n"],
                    h1["vnc_efferent_or_motor_weight"],
                    f"{h1['frac_exiting_effectors']:.4f}",
                ],
                [
                    "AbNT efferents + motor",
                    h1["abnt_efferent_or_motor_n"],
                    h1["abnt_efferent_or_motor_weight"],
                    f"{h1['frac_abnt_effectors']:.4f}",
                ],
                ["AbNT efferent", h1["abnt_efferent_n"], h1["abnt_efferent_weight"], None],
                ["AbNT motor", h1["abnt_motor_n"], h1["abnt_motor_weight"], None],
                ["OGN-like (OA AbNT / EN00B*)", h1["ogn_like_n"], h1["ogn_like_weight"], None],
                [
                    "SGN-like hole (unlabeled AbNT, NT not OA)",
                    h1["sgn_like_hole_n"],
                    h1["sgn_like_hole_weight"],
                    None,
                ],
            ],
        )
    )
    chunks.append("## Hop-1 EN00B*")
    chunks.append(
        _md(
            ["bodyId", "type", "exitNerve", "hop1", "consensus_nt"],
            [
                [r["bodyId"], r["type"], r["exitNerve"], r["hop1_weight"], r["consensus_nt"]]
                for r in hop1["en00b"]
            ],
        )
    )
    chunks.append("## Hop-1 unlabeled AbNT efferents (SGN-like hole)")
    chunks.append(
        _md(
            ["bodyId", "hop1", "consensus_nt", "predicted_nt", "pred_conf"],
            [
                [
                    r["bodyId"],
                    r["hop1_weight"],
                    r["consensus_nt"],
                    r["predicted_nt"],
                    f"{r['predicted_nt_confidence']:.3f}",
                ]
                for r in hop1["unlabeled_abnt_efferents"]
            ],
        )
    )
    chunks.append("## Hop-1 MNad* (weight >= 10; full list in logs/hop1.json)")
    chunks.append(
        _md(
            ["bodyId", "type", "exitNerve", "hop1", "consensus_nt"],
            [
                [r["bodyId"], r["type"], r["exitNerve"], r["hop1_weight"], r["consensus_nt"]]
                for r in hop1["mnad"]
                if r["hop1_weight"] >= 10
            ],
        )
    )
    chunks.append("## Hop-2 from hop-1 partners (weight = synapse count, FOUR excluded as pre)")
    chunks.append(
        _md(
            ["pool", "n", "weight", "fraction"],
            [
                ["total", h2["n_posts"], h2["total_weight"], "1"],
                [
                    "local AG INs (A7-A9 vnc_intrinsic)",
                    None,
                    h2["local_ag_a7a9_intrinsic_weight"],
                    f"{h2['frac_local_ag_a7a9']:.4f}",
                ],
                [
                    "exiting effectors",
                    None,
                    h2["vnc_efferent_or_motor_weight"],
                    f"{h2['frac_exiting_effectors']:.4f}",
                ],
                [
                    "AbNT efferents + motor",
                    h2["abnt_efferent_or_motor_n"],
                    h2["abnt_efferent_or_motor_weight"],
                    f"{h2['frac_abnt_effectors']:.4f}",
                ],
            ],
        )
    )
    chunks.append("## Hop-2 EN00B* (top 12 by synapse count)")
    chunks.append(
        _md(
            ["bodyId", "type", "hop2", "consensus_nt"],
            [
                [r["bodyId"], r["type"], r["hop2_weight"], r["consensus_nt"]]
                for r in hop2["en00b"][:12]
            ],
        )
    )
    chunks.append("## Hop-2 unlabeled AbNT efferents")
    chunks.append(
        _md(
            ["bodyId", "hop2", "consensus_nt", "pred_conf"],
            [
                [
                    r["bodyId"],
                    r["hop2_weight"],
                    r["consensus_nt"],
                    f"{r['predicted_nt_confidence']:.3f}",
                ]
                for r in hop2["unlabeled_abnt_efferents"]
            ],
        )
    )
    chunks.append("## Hop-2 MNad* (top 12)")
    chunks.append(
        _md(
            ["bodyId", "type", "exitNerve", "hop2", "consensus_nt"],
            [
                [r["bodyId"], r["type"], r["exitNerve"], r["hop2_weight"], r["consensus_nt"]]
                for r in hop2["mnad"][:12]
            ],
        )
    )
    return "\n\n".join(chunks) + "\n"
