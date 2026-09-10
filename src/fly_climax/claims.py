# Copyright (c) 2026 Martial Systems LLC
"""Fail closed on banned claim tokens. Scan designated surfaces only."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

BANNED: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("orgasmed", re.compile(r"\borgasmed\b", re.I)),
    ("orgasm_yes", re.compile(r"orgasm simulated\?\s*yes", re.I)),
    ("the_fly_came", re.compile(r"the fly came\b", re.I)),
    ("fly_ejaculated", re.compile(r"the fly ejaculated", re.I)),
    ("crz01_as_abg", re.compile(r"CRZ01.{0,40}abgCrz|abgCrz.{0,40}CRZ01", re.I | re.S)),
    ("crz02_as_abg", re.compile(r"CRZ02.{0,40}abgCrz|abgCrz.{0,40}CRZ02", re.I | re.S)),
    ("locked_identity", re.compile(r"identity is locked", re.I)),
)


class ClaimBanError(RuntimeError):
    pass


def scan_text(text: str) -> list[str]:
    return [name for name, pat in BANNED if pat.search(text or "")]


def require_clean(text: str, *, source: str) -> None:
    hits = scan_text(text)
    if hits:
        raise ClaimBanError(f"{source}: banned claims {hits}")
    if "\u2014" in (text or ""):
        raise ClaimBanError(f"{source}: em dash")


def require_paths_clean(paths: Iterable[Path]) -> None:
    for path in paths:
        if path.is_file():
            require_clean(path.read_text(encoding="utf-8"), source=str(path))


def scan_log_claim_fields(path: Path) -> None:
    raw = json.loads(path.read_text(encoding="utf-8"))
    for key in ("claim", "banner", "summary", "verdict"):
        if key in raw and isinstance(raw[key], str):
            require_clean(raw[key], source=f"{path}:{key}")
