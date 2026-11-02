#!/usr/bin/env python3
"""Block delivery when refinement scores or one-vote gates fail."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PASS_VALUES = {"否", "无", "未触发", "none", "no", "false", "0"}
OBJECTIVE_GATE_PATTERNS = {
    "l-shape redline": r"L\s*型红线包围感判断[:：]\s*([^\r\n]+)",
    "repeated skeleton": r"contact sheet\s*跨页重复骨架判断[:：]\s*([^\r\n]+)",
    "high-density underfill": r"高密度\s*underfill\s*判断[:：]\s*([^\r\n]+)",
    "semantic invariants": r"语义不变量判断[:：]\s*([^\r\n]+)",
    "recomposition authorization": r"重构授权判断[:：]\s*([^\r\n]+)",
    "evidence coverage": r"证据覆盖判断[:：]\s*([^\r\n]+)",
    "relation preservation": r"关系保真判断[:：]\s*([^\r\n]+)",
    "unrecorded diff": r"未记录差异判断[:：]\s*([^\r\n]+)",
}


def is_pass(value: str) -> bool:
    normalized = value.strip().lower()
    return normalized in PASS_VALUES or normalized.startswith(("否", "无", "未触发", "pass", "ok"))


def main(report_path: str, threshold: int = 92) -> int:
    text = Path(report_path).read_text(encoding="utf-8")
    scores = [int(value) for value in re.findall(r"总分[:：]\s*(\d+)", text)]
    gate_values = [
        value.strip().lower()
        for value in re.findall(r"(?:是否触发)?一票(?:失败|降级)项[:：]\s*([^\r\n]+)", text)
    ]

    errors: list[str] = []
    if not scores:
        errors.append("no page scores found")
    elif any(score < threshold for score in scores):
        errors.append(f"page score below {threshold}: {[score for score in scores if score < threshold]}")

    failed_gates = [value for value in gate_values if not is_pass(value)]
    if failed_gates:
        errors.append(f"one-vote failure gate triggered: {failed_gates}")

    for gate_name, pattern in OBJECTIVE_GATE_PATTERNS.items():
        values = re.findall(pattern, text, flags=re.IGNORECASE)
        if not values:
            errors.append(f"missing objective gate result: {gate_name}")
            continue
        failed_values = [value for value in values if not is_pass(value)]
        if failed_values:
            errors.append(f"{gate_name} gate triggered: {failed_values}")

    if errors:
        for message in errors:
            print(f"BLOCKED: {message}")
        return 1

    print(f"OK: refinement report passed for {len(scores)} page(s); threshold={threshold}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 92))
