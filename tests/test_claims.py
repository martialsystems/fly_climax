# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import io
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from fly_climax import BANNER
from fly_climax.claims import ClaimBanError, require_clean, scan_text
from fly_climax.cli import main

REPO = Path(__file__).resolve().parents[1]
PLAIN_HOOK = (
    "Public-connectome equivalent of the 2018 abdominal pulse. "
    "Candidate INXXX149. Climax not simulated."
)


def test_banner_is_clean() -> None:
    assert scan_text(BANNER) == []
    require_clean(BANNER, source="banner")


def test_readme_and_cli_help_are_clean() -> None:
    require_clean((REPO / "README.md").read_text(encoding="utf-8"), source="README.md")
    buf = io.StringIO()
    with redirect_stdout(buf):
        with pytest.raises(SystemExit):
            main(["--help"])
    require_clean(buf.getvalue(), source="cli-help")
    require_clean((REPO / "AGENTS.md").read_text(encoding="utf-8"), source="AGENTS.md")
    require_clean((REPO / "THIRD_PARTY.md").read_text(encoding="utf-8"), source="THIRD_PARTY.md")
    desc = (REPO / "description.txt").read_text(encoding="utf-8").strip()
    assert desc == PLAIN_HOOK
    require_clean(desc, source="description.txt")


def test_banned_tokens_fail() -> None:
    with pytest.raises(ClaimBanError):
        require_clean("the fly orgasmed", source="x")
    with pytest.raises(ClaimBanError):
        require_clean("Orgasm simulated? Yes", source="x")
    with pytest.raises(ClaimBanError):
        require_clean("the fly ejaculated today", source="x")
    with pytest.raises(ClaimBanError):
        require_clean("identity is locked on INXXX149", source="x")
    require_clean("Orgasm simulated? No", source="locked-row")
