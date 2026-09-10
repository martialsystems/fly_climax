#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Rebuild locked hop tables from MaleCNS v1.0 feathers. Needs pandas and pyarrow."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

FOUR = [800571, 800986, 802096, 904047]
SENS = [801013, 800166]
EXC = {"acetylcholine", "glutamate", "octopamine", "serotonin"}
INH = {"gaba"}


def nt_sign(name: object) -> int:
    if name in EXC:
        return 1
    if name in INH:
        return -1
    return 0


def has_abnt(x: object) -> bool:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return False
    return "AbNT" in str(x)


def nan_none(x: object) -> object:
    if x is None:
        return None
    if isinstance(x, float) and math.isnan(x):
        return None
    try:
        import pandas as pd

        if pd.isna(x):
            return None
    except Exception:
        pass
    return x


def main() -> None:
    import pandas as pd

    ap = argparse.ArgumentParser()
    ap.add_argument("--ann", required=True)
    ap.add_argument("--nt", required=True)
    ap.add_argument("--weights", required=True)
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "logs"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    ann = pd.read_feather(args.ann)
    nt = pd.read_feather(args.nt)
    w = pd.read_feather(args.weights)

    ann = ann.copy()
    for col in ("type", "superclass", "subclass", "exitNerve", "somaNeuromere", "instance"):
        if col in ann.columns:
            ann[col] = ann[col].astype(object)
    ann["abnt"] = ann["exitNerve"].map(has_abnt)
    type_s = ann["type"].fillna("").astype(str)
    ann["is_en00b"] = type_s.str.startswith("EN00B")
    ann["is_mnad"] = type_s.str.startswith("MNad")
    ann["unlabeled"] = ann["type"].isna() | (type_s.str.strip() == "") | (type_s == "nan")
    sc = ann["superclass"].fillna("").astype(str)
    ann["is_efferent"] = sc.eq("vnc_efferent")
    ann["is_motor"] = sc.eq("vnc_motor")
    ann["is_intrinsic"] = sc.eq("vnc_intrinsic")

    nt1 = nt.rename(columns={"body": "bodyId"})
    meta_cols = [
        "bodyId",
        "type",
        "instance",
        "superclass",
        "subclass",
        "somaSide",
        "somaNeuromere",
        "exitNerve",
        "mancBodyid",
        "mancType",
        "abnt",
        "is_en00b",
        "is_mnad",
        "unlabeled",
        "is_efferent",
        "is_motor",
        "is_intrinsic",
    ]

    h1 = w[w["body_pre"].isin(FOUR)].copy()
    g1 = (
        h1.groupby("body_post", as_index=False)["weight"]
        .sum()
        .rename(columns={"body_post": "bodyId", "weight": "hop1_weight"})
    )
    piv = h1.pivot_table(
        index="body_post", columns="body_pre", values="weight", aggfunc="sum", fill_value=0
    )
    piv = piv.reindex(columns=FOUR, fill_value=0)
    piv.columns = [f"from_{c}" for c in FOUR]
    g1 = g1.merge(piv.reset_index().rename(columns={"body_post": "bodyId"}), on="bodyId", how="left")
    g1 = g1.merge(ann[meta_cols], on="bodyId", how="left")
    g1 = g1.merge(
        nt1[
            [
                "bodyId",
                "predicted_nt",
                "predicted_nt_confidence",
                "consensus_nt",
                "celltype_predicted_nt",
                "celltype_predicted_nt_confidence",
            ]
        ],
        on="bodyId",
        how="left",
    )
    g1["sign"] = g1["consensus_nt"].map(nt_sign)
    g1["signed_weight"] = g1["hop1_weight"] * g1["sign"]
    g1 = g1.sort_values(["hop1_weight", "bodyId"], ascending=[False, True])

    total = int(g1["hop1_weight"].sum())
    ag = g1[
        g1["is_intrinsic"]
        & g1["somaNeuromere"].fillna("").astype(str).isin(["A7", "A8", "A9"])
    ]
    intrinsic = g1[g1["is_intrinsic"]]
    exiting = g1[g1["is_efferent"] | g1["is_motor"]]
    abnt_eff_mn = g1[g1["abnt"] & (g1["is_efferent"] | g1["is_motor"])]
    abnt_eff = g1[g1["abnt"] & g1["is_efferent"]]
    abnt_mn = g1[g1["abnt"] & g1["is_motor"]]
    en = g1[g1["is_en00b"]].sort_values(["hop1_weight", "bodyId"], ascending=[False, True])
    unlabeled = g1[g1["abnt"] & g1["unlabeled"] & g1["is_efferent"]].sort_values(
        ["hop1_weight", "bodyId"], ascending=[False, True]
    )
    mnad = g1[g1["is_mnad"]].sort_values(["hop1_weight", "bodyId"], ascending=[False, True])
    ogn = g1[
        g1["abnt"]
        & (
            g1["type"].fillna("").astype(str).eq("EN00B010")
            | g1["consensus_nt"].eq("octopamine")
            | g1["predicted_nt"].eq("octopamine")
        )
    ].sort_values(["hop1_weight", "bodyId"], ascending=[False, True])
    sgn = unlabeled[
        (unlabeled["consensus_nt"].fillna("") != "octopamine")
        & (unlabeled["predicted_nt"].fillna("") != "octopamine")
    ]

    rec = w[(w["body_pre"].isin(FOUR)) & (w["body_post"].isin(FOUR))]

    h1_posts = set(int(x) for x in g1["bodyId"].tolist())
    h2e = w[w["body_pre"].isin(h1_posts) & ~w["body_pre"].isin(FOUR)].copy()
    h2e = h2e.merge(
        g1[["bodyId", "hop1_weight"]].rename(columns={"bodyId": "body_pre", "hop1_weight": "w1"}),
        on="body_pre",
        how="left",
    )
    h2e["drive"] = h2e["weight"].astype("int64") * h2e["w1"].astype("int64")
    h2 = h2e.groupby("body_post", as_index=False).agg(
        hop2_weight=("weight", "sum"), hop2_drive=("drive", "sum"), n_mids=("body_pre", "nunique")
    )
    h2 = h2.rename(columns={"body_post": "bodyId"})
    h2 = h2.merge(ann[meta_cols], on="bodyId", how="left")
    h2 = h2.merge(
        nt1[["bodyId", "predicted_nt", "predicted_nt_confidence", "consensus_nt"]],
        on="bodyId",
        how="left",
    )
    h2["sign"] = h2["consensus_nt"].map(nt_sign)
    h2["also_hop1"] = h2["bodyId"].isin(h1_posts)
    h2 = h2.sort_values(["hop2_weight", "bodyId"], ascending=[False, True])

    h2_total = int(h2["hop2_weight"].sum())
    h2_ag = h2[
        h2["is_intrinsic"]
        & h2["somaNeuromere"].fillna("").astype(str).isin(["A7", "A8", "A9"])
    ]
    h2_intrinsic = h2[h2["is_intrinsic"]]
    h2_exiting = h2[h2["is_efferent"] | h2["is_motor"]]
    h2_abnt = h2[h2["abnt"] & (h2["is_efferent"] | h2["is_motor"])]
    h2_en = h2[h2["is_en00b"]].sort_values(["hop2_weight", "bodyId"], ascending=[False, True])
    h2_unl = h2[h2["abnt"] & h2["unlabeled"] & h2["is_efferent"]].sort_values(
        ["hop2_weight", "bodyId"], ascending=[False, True]
    )
    h2_mnad = h2[h2["is_mnad"]].sort_values(["hop2_weight", "bodyId"], ascending=[False, True])

    def row_h1(r) -> dict:
        return {
            "bodyId": int(r.bodyId),
            "type": nan_none(r.type),
            "instance": nan_none(r.instance),
            "superclass": nan_none(r.superclass),
            "somaSide": nan_none(r.somaSide),
            "somaNeuromere": nan_none(r.somaNeuromere),
            "exitNerve": nan_none(r.exitNerve),
            "hop1_weight": int(r.hop1_weight),
            "from_800571": int(r.from_800571),
            "from_800986": int(r.from_800986),
            "from_802096": int(r.from_802096),
            "from_904047": int(r.from_904047),
            "consensus_nt": nan_none(r.consensus_nt),
            "predicted_nt": nan_none(r.predicted_nt),
            "predicted_nt_confidence": (
                None
                if nan_none(r.predicted_nt_confidence) is None
                else float(r.predicted_nt_confidence)
            ),
            "celltype_predicted_nt": nan_none(r.celltype_predicted_nt),
            "celltype_predicted_nt_confidence": (
                None
                if nan_none(r.celltype_predicted_nt_confidence) is None
                else float(r.celltype_predicted_nt_confidence)
            ),
            "sign": int(r.sign),
            "abnt": bool(r.abnt),
            "unlabeled": bool(r.unlabeled),
            "is_en00b": bool(r.is_en00b),
            "is_mnad": bool(r.is_mnad),
            "is_efferent": bool(r.is_efferent),
            "is_motor": bool(r.is_motor),
            "is_intrinsic": bool(r.is_intrinsic),
        }

    def row_h2(r) -> dict:
        return {
            "bodyId": int(r.bodyId),
            "type": nan_none(r.type),
            "superclass": nan_none(r.superclass),
            "somaNeuromere": nan_none(r.somaNeuromere),
            "exitNerve": nan_none(r.exitNerve),
            "hop2_weight": int(r.hop2_weight),
            "hop2_drive": int(r.hop2_drive),
            "n_mids": int(r.n_mids),
            "consensus_nt": nan_none(r.consensus_nt),
            "predicted_nt": nan_none(r.predicted_nt),
            "predicted_nt_confidence": (
                None
                if nan_none(r.predicted_nt_confidence) is None
                else float(r.predicted_nt_confidence)
            ),
            "sign": int(r.sign),
            "also_hop1": bool(r.also_hop1),
            "abnt": bool(r.abnt),
            "unlabeled": bool(r.unlabeled),
            "is_en00b": bool(r.is_en00b),
            "is_mnad": bool(r.is_mnad),
            "is_efferent": bool(r.is_efferent),
            "is_motor": bool(r.is_motor),
            "is_intrinsic": bool(r.is_intrinsic),
        }

    four_meta = []
    for b in FOUR + SENS:
        r = ann[ann["bodyId"] == b].iloc[0]
        ntr = nt1[nt1["bodyId"] == b].iloc[0]
        four_meta.append(
            {
                "bodyId": int(b),
                "set": "four" if b in FOUR else "sensitivity",
                "type": nan_none(r.type),
                "instance": nan_none(r.instance),
                "somaSide": nan_none(r.somaSide),
                "somaNeuromere": nan_none(r.somaNeuromere),
                "mancBodyid": int(r.mancBodyid) if nan_none(r.mancBodyid) is not None else None,
                "consensus_nt": nan_none(ntr.consensus_nt),
                "predicted_nt": nan_none(ntr.predicted_nt),
                "predicted_nt_confidence": float(ntr.predicted_nt_confidence),
            }
        )

    ser_pred_abnt = nt1.merge(ann[["bodyId", "type", "superclass", "exitNerve", "abnt"]], on="bodyId")
    ser_pred_abnt = ser_pred_abnt[
        (ser_pred_abnt["predicted_nt"] == "serotonin") & ser_pred_abnt["abnt"]
    ]
    ser_cons = int((nt1["consensus_nt"] == "serotonin").sum())
    ser_cons_abnt = int(
        (
            (nt1["consensus_nt"] == "serotonin")
            & nt1["bodyId"].isin(ann.loc[ann["abnt"], "bodyId"])
        ).sum()
    )

    partners = g1[~g1["bodyId"].isin(FOUR)].sort_values(
        ["hop1_weight", "bodyId"], ascending=[False, True]
    )
    top20 = [row_h1(r) for r in partners.head(20).itertuples(index=False)]

    summary = {
        "dataset": "male-cns:v1.0",
        "weights": "significant-only",
        "command": FOUR,
        "type": "INXXX149",
        "sensitivity": SENS,
        "identity": "candidate",
        "hop1": {
            "n_edges": int(len(h1)),
            "n_posts": int(len(g1)),
            "total_weight": total,
            "weight_ge5": int(h1[h1["weight"] >= 5]["weight"].sum()),
            "n_posts_ge5": int(h1[h1["weight"] >= 5]["body_post"].nunique()),
            "reciprocal_four": int(rec["weight"].sum()),
            "signed_excitatory": int(g1.loc[g1["sign"] == 1, "hop1_weight"].sum()),
            "signed_inhibitory": int(g1.loc[g1["sign"] == -1, "hop1_weight"].sum()),
            "unsigned": int(g1.loc[g1["sign"] == 0, "hop1_weight"].sum()),
            "abnt_efferent_weight": int(abnt_eff["hop1_weight"].sum()),
            "abnt_efferent_n": int(len(abnt_eff)),
            "abnt_motor_weight": int(abnt_mn["hop1_weight"].sum()),
            "abnt_motor_n": int(len(abnt_mn)),
            "abnt_efferent_or_motor_weight": int(abnt_eff_mn["hop1_weight"].sum()),
            "abnt_efferent_or_motor_n": int(len(abnt_eff_mn)),
            "vnc_efferent_or_motor_weight": int(exiting["hop1_weight"].sum()),
            "vnc_efferent_or_motor_n": int(len(exiting)),
            "local_ag_a7a9_intrinsic_weight": int(ag["hop1_weight"].sum()),
            "local_ag_a7a9_intrinsic_n": int(len(ag)),
            "vnc_intrinsic_weight": int(intrinsic["hop1_weight"].sum()),
            "frac_local_ag_a7a9": ag["hop1_weight"].sum() / total,
            "frac_vnc_intrinsic": intrinsic["hop1_weight"].sum() / total,
            "frac_exiting_effectors": exiting["hop1_weight"].sum() / total,
            "frac_abnt_effectors": abnt_eff_mn["hop1_weight"].sum() / total,
            "ogn_like_weight": int(ogn["hop1_weight"].sum()),
            "ogn_like_n": int(len(ogn)),
            "en00b010_weight": int(
                g1[g1["type"].fillna("").astype(str).eq("EN00B010")]["hop1_weight"].sum()
            ),
            "sgn_like_hole_weight": int(sgn["hop1_weight"].sum()),
            "sgn_like_hole_n": int(len(sgn)),
            "en00b_weight": int(en["hop1_weight"].sum()),
            "unlabeled_abnt_efferent_weight": int(unlabeled["hop1_weight"].sum()),
            "mnad_weight": int(mnad["hop1_weight"].sum()),
            "mnad_abnt_weight": int(mnad[mnad["abnt"]]["hop1_weight"].sum()),
        },
        "hop2": {
            "n_posts": int(len(h2)),
            "total_weight": h2_total,
            "abnt_efferent_or_motor_weight": int(h2_abnt["hop2_weight"].sum()),
            "abnt_efferent_or_motor_n": int(len(h2_abnt)),
            "local_ag_a7a9_intrinsic_weight": int(h2_ag["hop2_weight"].sum()),
            "vnc_intrinsic_weight": int(h2_intrinsic["hop2_weight"].sum()),
            "vnc_efferent_or_motor_weight": int(h2_exiting["hop2_weight"].sum()),
            "frac_local_ag_a7a9": h2_ag["hop2_weight"].sum() / h2_total,
            "frac_exiting_effectors": h2_exiting["hop2_weight"].sum() / h2_total,
            "frac_abnt_effectors": h2_abnt["hop2_weight"].sum() / h2_total,
        },
        "serotonin": {
            "consensus_n": ser_cons,
            "consensus_abnt_n": ser_cons_abnt,
            "consensus_vnc_efferent_or_motor_n": int(
                (
                    (nt1["consensus_nt"] == "serotonin")
                    & nt1["bodyId"].isin(
                        ann.loc[ann["is_efferent"] | ann["is_motor"], "bodyId"]
                    )
                ).sum()
            ),
            "predicted_abnt": [
                {
                    "bodyId": int(r.bodyId),
                    "type": nan_none(r.type),
                    "superclass": nan_none(r.superclass),
                    "exitNerve": nan_none(r.exitNerve),
                    "predicted_nt": nan_none(r.predicted_nt),
                    "predicted_nt_confidence": float(r.predicted_nt_confidence),
                    "consensus_nt": nan_none(r.consensus_nt),
                    "hop1_weight": int(
                        g1.loc[g1["bodyId"] == r.bodyId, "hop1_weight"].sum()
                    ),
                }
                for r in ser_pred_abnt.itertuples(index=False)
            ],
            "accessory_gland_step": "missing",
        },
        "nt_sign": {
            "excitatory": sorted(EXC),
            "inhibitory": sorted(INH),
            "unsigned": "unclear and any NT not in those two sets",
        },
    }

    hop1_tables = {
        "en00b": [row_h1(r) for r in en.itertuples(index=False)],
        "unlabeled_abnt_efferents": [row_h1(r) for r in unlabeled.itertuples(index=False)],
        "mnad": [row_h1(r) for r in mnad.itertuples(index=False)],
        "ogn_like": [row_h1(r) for r in ogn.itertuples(index=False)],
        "sgn_like_hole": [row_h1(r) for r in sgn.itertuples(index=False)],
        "top40": [row_h1(r) for r in g1.head(40).itertuples(index=False)],
    }
    hop2_tables = {
        "en00b": [row_h2(r) for r in h2_en.itertuples(index=False)],
        "unlabeled_abnt_efferents": [row_h2(r) for r in h2_unl.itertuples(index=False)],
        "mnad": [row_h2(r) for r in h2_mnad.itertuples(index=False)],
        "abnt_effectors_top40": [
            row_h2(r)
            for r in h2_abnt.sort_values(
                ["hop2_weight", "bodyId"], ascending=[False, True]
            )
            .head(40)
            .itertuples(index=False)
        ],
        "top40": [row_h2(r) for r in h2.head(40).itertuples(index=False)],
    }

    working = {
        "dataset": "male-cns:v1.0",
        "neuprint_uuid": "4b2087c0fbe046bfaf0d60bc970e3e5d",
        "four": FOUR,
        "type": "INXXX149",
        "sensitivity": SENS,
        "identity": "candidate",
        "cells": four_meta,
        "do_not_search": ["CRZ01", "CRZ02"],
        "do_not_search_note": "Those are brain cells. Cell ID is closed on INXXX149.",
    }

    def dump(name: str, obj: object) -> None:
        (out / name).write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n", encoding="utf-8")

    dump("working_set.json", working)
    dump("drive_summary.json", summary)
    dump("hop1.json", hop1_tables)
    dump("hop2.json", hop2_tables)
    dump("hop1_top20.json", {"partners": top20, "excluded_command": FOUR})
    print("wrote", out)


if __name__ == "__main__":
    main()
