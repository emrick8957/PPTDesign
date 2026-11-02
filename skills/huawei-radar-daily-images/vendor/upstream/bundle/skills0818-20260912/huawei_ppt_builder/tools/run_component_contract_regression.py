#!/usr/bin/env python3
"""Run the 25 acceptance cases for the multi-chart component contract."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT.parent
sys.path.insert(0, str(ROOT / "tools"))

from render_contract_builder import build_contract  # noqa: E402
from validate_inputs import LAYOUT_COMPONENT_REGIONS, validate_page, validate_root  # noqa: E402


def component(
    component_id: str,
    role: str,
    region: str,
    chart_type: str,
    goal: str,
    *,
    supports: str | None = None,
    boundary: list[str] | None = None,
    chart_data: dict[str, Any] | None = None,
    required_evidence: list[str] | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "component_id": component_id,
        "component_role": role,
        "component_region": region,
        "chart_type": chart_type,
        "chart_proof_goal": goal,
        "chart_data": chart_data if chart_data is not None else {"items": [{"label": f"证据{component_id}"}]},
        "chart_visual_boundary": boundary if boundary is not None else [f"边界{component_id}"],
    }
    if supports is not None:
        item["supports_component_id"] = supports
    if required_evidence is not None:
        item["required_evidence"] = required_evidence
    return item


def base_page() -> dict[str, Any]:
    return {
        "page_id": "P01",
        "title": "组件合同回归页",
        "conclusion": "主图承担判断，辅助图提供不同证据。",
        "core_judgement": "logic-only: component contract",
        "type": "executive_summary",
        "layout_pattern": "executive_summary_dashboard",
        "chart_components": [
            component("C1", "primary", "main", "key_findings_cards", "证明主判断成立")
        ],
    }


def validation_errors(page: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validate_page(page, 0, errors)
    return errors


def root_validation_errors(page: dict[str, Any]) -> list[str]:
    fixture = ROOT / "examples" / "regression" / "a_latest_delivery_snapshot"
    with tempfile.TemporaryDirectory(prefix="component-contract-root-") as temp_dir:
        target = Path(temp_dir) / "input"
        shutil.copytree(fixture, target)
        (target / "deck_spec.json").write_text(
            json.dumps({"pages": [page]}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return validate_root(str(target))[3]


def expect_pass(page: dict[str, Any]) -> None:
    errors = validation_errors(page)
    assert not errors, errors


def expect_fail(page: dict[str, Any], fragment: str) -> None:
    errors = validation_errors(page)
    assert errors, "case unexpectedly passed"
    assert any(fragment in message for message in errors), errors


def add_supporting(
    page: dict[str, Any], component_id: str, region: str, goal: str, **kwargs: Any
) -> None:
    page["chart_components"].append(
        component(
            component_id,
            "supporting",
            region,
            kwargs.pop("chart_type", "metric_showcase_grid"),
            goal,
            supports=kwargs.pop("supports", "C1"),
            **kwargs,
        )
    )


def load_html_builder() -> Any:
    path = SKILLS / "huawei_ppt_builder_html" / "tools" / "render_contract_builder.py"
    spec = importlib.util.spec_from_file_location("html_render_contract_builder", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_documented_regions() -> dict[str, dict[str, set[str]]]:
    path = SKILLS / "huawei_ppt_master" / "visual_patterns" / "layout_library.md"
    documented: dict[str, dict[str, set[str]]] = {}
    row_pattern = re.compile(r"^\| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \|")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = row_pattern.match(line)
        if not match:
            continue
        layout, primary, supporting = match.groups()
        documented[layout] = {
            "primary": set(primary.split(",")) if primary != "无" else set(),
            "supporting": set(supporting.split(",")) if supporting != "无" else set(),
        }
    return documented


def main() -> int:
    cases: list[tuple[str, Callable[[], None]]] = []

    cases.append(("MC2-RT-01 primary only", lambda: expect_pass(base_page())))

    def case02() -> None:
        page = base_page(); add_supporting(page, "C2", "bottom", "量化覆盖范围"); expect_pass(page)
    cases.append(("MC2-RT-02 primary + supporting", case02))

    def case03() -> None:
        page = base_page()
        add_supporting(page, "C2", "left", "量化覆盖范围")
        add_supporting(page, "C3", "right", "比较实施差异")
        add_supporting(page, "C4", "top", "标记关键风险")
        expect_pass(page)
    cases.append(("MC2-RT-03 three supporting", case03))

    def case04() -> None:
        page = base_page(); page["chart_type"] = "key_findings_cards"; expect_fail(page, "mixes chart_components")
    cases.append(("MC2-RT-04 mixed contract", case04))

    def case05() -> None:
        page = base_page(); add_supporting(page, "C2", "insight_panel", "量化覆盖范围"); expect_fail(page, "insight_panel")
    cases.append(("MC2-RT-05 insight panel enum", case05))

    def case06() -> None:
        page = base_page(); page["layout_pattern"] = "insight_panel_with_chart"; add_supporting(page, "C2", "right", "量化覆盖范围"); expect_fail(page, "incompatible")
    cases.append(("MC2-RT-06 insight layout right", case06))

    def case07() -> None:
        page = base_page(); page["layout_pattern"] = "four_quadrant_judgement"; add_supporting(page, "C2", "left", "量化覆盖范围"); expect_fail(page, "incompatible")
    cases.append(("MC2-RT-07 quadrant left", case07))

    def case08() -> None:
        page = base_page(); page["chart_components"][0]["component_region"] = "right"
        add_supporting(page, "C2", "left", "量化覆盖范围")
        add_supporting(page, "C3", "top", "标记关键风险")
        expect_pass(page)
    cases.append(("MC2-RT-08 executive regions", case08))

    def case09() -> None:
        page = base_page(); page["layout_pattern"] = "stack_architecture_with_right_insights"; add_supporting(page, "C2", "right", "量化覆盖范围"); expect_fail(page, "incompatible")
    cases.append(("MC2-RT-09 architecture right", case09))

    def case10() -> None:
        page = base_page(); page["layout_pattern"] = "image_background_section_divider"; page["chart_components"][0]["chart_type"] = "none"; page["chart_components"][0]["chart_data"] = {}; expect_pass(page)
    cases.append(("MC2-RT-10 divider none", case10))

    def case11() -> None:
        page = base_page(); page["layout_pattern"] = "image_background_section_divider"; page["chart_components"][0]["chart_type"] = "trend_curve"; expect_fail(page, "requires primary chart_type='none'")
    cases.append(("MC2-RT-11 divider chart", case11))

    def case12() -> None:
        page = base_page(); add_supporting(page, "C2", "main", "量化覆盖范围"); expect_fail(page, "component_region values must be unique")
    cases.append(("MC2-RT-12 duplicate region", case12))

    def case13() -> None:
        page = base_page(); add_supporting(page, "C2", "bottom", "量化覆盖范围"); page["bottom_bar_rule"] = "enabled"
        expect_pass(page)
        assert any("bottom_bar_rule" in message for message in root_validation_errors(page))
        try:
            build_contract(page)
        except ValueError as exc:
            assert "bottom" in str(exc)
        else:
            raise AssertionError("bottom component conflict unexpectedly passed compiler")
    cases.append(("MC2-RT-13 bottom bar conflict", case13))

    def case14() -> None:
        page = base_page(); add_supporting(page, "C2", "bottom", "证明主判断成立"); expect_fail(page, "proof goals")
    cases.append(("MC2-RT-14 duplicate primary goal", case14))

    def case15() -> None:
        page = base_page(); add_supporting(page, "C2", "left", "量化覆盖范围"); add_supporting(page, "C3", "right", "量化覆盖范围与质量"); expect_fail(page, "proof goals")
    cases.append(("MC2-RT-15 supporting prefix goals", case15))

    def case16() -> None:
        page = base_page(); add_supporting(page, "C2", "bottom", "量化覆盖范围", boundary=["禁止同权卡片"]); page["chart_components"][0]["chart_visual_boundary"] = ["禁止同权卡片"]; expect_fail(page, "chart_visual_boundary")
    cases.append(("MC2-RT-16 duplicate boundaries", case16))

    def case17() -> None:
        page = base_page(); add_supporting(page, "C2", "bottom", "量化覆盖范围", chart_type="none"); expect_fail(page, "supporting component chart_type")
    cases.append(("MC2-RT-17 supporting none", case17))

    def case18() -> None:
        page = base_page(); page["chart_components"][0]["chart_type"] = "none"; page["chart_components"][0]["chart_data"] = {}; add_supporting(page, "C2", "bottom", "量化覆盖范围"); expect_fail(page, "cannot have supporting")
    cases.append(("MC2-RT-18 primary none with support", case18))

    def case19() -> None:
        page = base_page()
        for index, region in enumerate(("left", "right", "top", "bottom"), start=2): add_supporting(page, f"C{index}", region, f"证据维度{index}")
        expect_fail(page, "at most 3")
    cases.append(("MC2-RT-19 too many supporting", case19))

    def case20() -> None:
        page = base_page(); page["chart_components"][0]["required_evidence"] = ["合同中不存在的证据"]
        expect_pass(page)
        try:
            build_contract(page)
        except ValueError as exc:
            assert "required evidence" in str(exc)
        else:
            raise AssertionError("missing component evidence unexpectedly passed compiler")
    cases.append(("MC2-RT-20 missing required evidence", case20))

    def case21() -> None:
        page = base_page(); add_supporting(page, "C2", "bottom", "量化覆盖范围", chart_data={"metrics": [{"label": "覆盖率", "value": "90%"}]})
        contract = build_contract(page)
        supporting = contract["render_intent"]["chart_components"][1]
        assert supporting["component_role"] == "supporting" and supporting["chart_data"]["metrics"]
    cases.append(("MC2-RT-21 supporting preserved", case21))

    def case22() -> None:
        page = base_page(); contract = build_contract(page); visible = contract["visible_text_plan"]["main_labels"]
        assert "C1" not in visible and "primary" not in visible and "main" not in visible
    cases.append(("MC2-RT-22 logic fields hidden", case22))

    def case23() -> None:
        page = base_page(); add_supporting(page, "C2", "bottom", "量化覆盖范围")
        html_builder = load_html_builder()
        assert build_contract(page) == html_builder.build_contract(copy.deepcopy(page))
    cases.append(("MC2-RT-23 builder parity", case23))

    def case24() -> None:
        assert parse_documented_regions() == LAYOUT_COMPONENT_REGIONS
    cases.append(("MC2-RT-24 compatibility parity", case24))

    def case25() -> None:
        text = (SKILLS / "huawei_ppt_master" / "eval" / "template_stamp_detection.md").read_text(encoding="utf-8")
        assert "component_id" in text and "组件" in text and ("连续" in text or "跨页" in text)
    cases.append(("MC2-RT-25 component stamp gate", case25))

    for name, test in cases:
        test()
        print(f"PASS: {name}")
    assert len(cases) == 25
    print("OK: 25 multi-chart component contract cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
