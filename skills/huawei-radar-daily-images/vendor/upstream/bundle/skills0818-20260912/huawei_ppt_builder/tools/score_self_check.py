#!/usr/bin/env python3
"""Summarize Role C self-check scores and enforce the delivery threshold."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main(report_path: str, threshold: int = 92) -> int:
    text = Path(report_path).read_text(encoding="utf-8")
    scores = [int(value) for value in re.findall(r"总分[:：]\s*(\d+)", text)]
    if not scores:
        print("ERROR: no page scores found")
        return 1

    low_scores = [score for score in scores if score < threshold]
    average = sum(scores) / len(scores)
    print(f"pages={len(scores)} average={average:.1f} threshold={threshold}")
    print(f"scores={scores}")
    if low_scores:
        print(f"BLOCKED: {len(low_scores)} page(s) below threshold: {low_scores}")
        return 1
    print("OK: every page meets the delivery threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 92))
