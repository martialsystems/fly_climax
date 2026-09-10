# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import argparse
import json
import sys

from fly_climax import BANNER
from fly_climax.lif_toy import THRESHOLD_NOTE, run_toy, write_log
from fly_climax.tables import hop_tables


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="fly-climax")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tables", help="print hop-1 and hop-2 tables from logs/")
    sub.add_parser("lif", help="run the one-synapse toy LIF and print the threshold line")
    args = parser.parse_args(argv)
    if args.cmd == "tables":
        sys.stdout.write(BANNER + "\n\n")
        sys.stdout.write(hop_tables())
        return 0
    if args.cmd == "lif":
        result = write_log(run_toy())
        sys.stdout.write(result["print_line"] + "\n")
        sys.stdout.write(THRESHOLD_NOTE + "\n")
        sys.stdout.write(json.dumps({"crossed": result["crossed"], "abnt_mean_hz": result["abnt_mean_hz"]}) + "\n")
        return 0
    return 2
