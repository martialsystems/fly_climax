# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from pathlib import Path

PKG = Path(__file__).resolve().parent
SRC = PKG.parent
REPO = SRC.parent
LOGS = REPO / "logs"
PROVENANCE = REPO / "data-provenance"
