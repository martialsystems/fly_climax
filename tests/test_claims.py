# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import io
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from fly_abgcrz import BANNER
from fly_abgcrz.claims import ClaimBanError, require_clean, scan_text
from fly_abgcrz.cli import main

REPO = Path(__file__).resolve().parents[1]
PLAIN_HOOK = (
    "Candidate INXXX149 Gautham-4 hop-1/hop-2 on MaleCNS v1.0. "
    "Toy LIF pulse. Invented threshold. 5-HT accessory-gland step missing."
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
        require_clean("the fly ejaculated today", source="x")
    with pytest.raises(ClaimBanError):
        require_clean("identity is locked on INXXX149", source="x")
