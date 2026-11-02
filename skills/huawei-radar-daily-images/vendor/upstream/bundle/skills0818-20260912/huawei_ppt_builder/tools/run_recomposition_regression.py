#!/usr/bin/env python3
"""Exercise the 28 adaptive visual recomposition acceptance cases."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT.parent
sys.path.insert(0, str(ROOT / "tools"))

from render_contract_builder import build_contract  # noqa: E402
from validate_recomposition import validate_contract  # noqa: E402


def primary_component(
    chart_type: str = "key_findings_cards",
    chart_data: dict[str, Any] | None = None,
    required_evidence: list[str] | None = None,
) -> dict[str, Any]:
    component: dict[str, Any] = {
        "component_id": "C1",
        "component_role": "primary",
        "component_region": "main",
        "chart_type": chart_type,
        "chart_proof_goal": "证明现有证据共同支撑本页判断",
        "chart_data": chart_data if chart_data is not None else {
            "items": [
                {"label": "证据A", "value": "30%"},
                {"label": "证据B", "value": "已确认"},
            ]
        },
        "chart_visual_boundary": ["不得退化为同权信息墙"],
        "chart_semantic_mapping": {"main_visual_logic": "证据汇聚形成判断"},
    }
    if required_evidence is not None:
        component["required_evidence"] = required_evidence
    return component


def page(
    *,
    layout: str = "executive_summary_dashboard",
    chart_type: str = "key_findings_cards",
    chart_data: dict[str, Any] | None = None,
    title: str = "现有证据必须支持30%的明确改善",
    required_evidence: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "page_id": "P01",
        "title": title,
        "conclusion": "证据完整时才能形成可执行判断。",
        "core_judgement": "logic-only: evidence must prove the decision",
        "type": "executive_summary",
        "layout_pattern": layout,
        "chart_components": [primary_component(chart_type, chart_data, required_evidence)],
    }


def contract(**kwargs: Any) -> dict[str, Any]:
    mode = kwargs.pop("mode", "adaptive_recomposition")
    return build_contract(page(**kwargs), recomposition_mode=mode)


def effective_primary(item: dict[str, Any]) -> dict[str, Any]:
    return next(
        component
        for component in item["effective_visual_plan"]["chart_components"]
        if component["component_role"] == "primary"
    )


def authorize(
    item: dict[str, Any],
    *,
    trigger: str = "underfilled_without_structure",
    baseline: int = 88,
    effective: int = 95,
) -> None:
    source = item["source_visual_plan"]
    target = item["effective_visual_plan"]
    source_map = {component["component_id"]: component for component in source["chart_components"]}
    target_map = {component["component_id"]: component for component in target["chart_components"]}
    audit = item["recomposition_audit"]
    audit["layout_changed"] = source["layout_pattern"] != target["layout_pattern"]
    audit["chart_type_changed"] = any(
        source_map[key]["chart_type"] != target_map[key]["chart_type"] for key in source_map
    )
    audit["component_region_changed"] = any(
        source_map[key]["component_region"] != target_map[key]["component_region"] for key in source_map
    )
    copy_adjustments: list[dict[str, str]] = []
    for field in ("visible_title", "visible_conclusion"):
        if source[field] != target[field]:
            copy_adjustments.append({"field": field, "source": source[field], "effective": target[field]})
    audit["copy_adjustments"] = copy_adjustments
    changed = audit["layout_changed"] or audit["chart_type_changed"] or audit["component_region_changed"] or bool(copy_adjustments)
    audit["trigger_reasons"] = [trigger] if changed else []
    audit["quality_delta"] = {
        "baseline_score": baseline if changed else None,
        "effective_score": effective if changed else None,
    }
    item["render_intent"]["layout_pattern"] = target["layout_pattern"]
    item["render_intent"]["chart_components"] = copy.deepcopy(target["chart_components"])
    item["render_intent"]["chart_type"] = effective_primary(item)["chart_type"]
    item["visible_text_plan"]["title"] = target["visible_title"]
    item["visible_text_plan"]["conclusion"] = target["visible_conclusion"]


def errors(item: dict[str, Any]) -> list[str]:
    return validate_contract(item)[0]


def expect_pass(item: dict[str, Any]) -> None:
    found = errors(item)
    assert not found, found


def expect_fail(item: dict[str, Any], fragment: str) -> None:
    found = errors(item)
    assert found, "case unexpectedly passed"
    assert any(fragment in message for message in found), found


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    cases: list[tuple[str, Callable[[], None]]] = []

    cases.append(("AVR-RT-01 strict unchanged", lambda: expect_pass(contract(mode="strict_fidelity"))))

    def case02() -> None:
        item = contract(mode="strict_fidelity")
        item["effective_visual_plan"]["layout_pattern"] = "left_logic_right_proof"
        expect_fail(item, "strict_fidelity")
    cases.append(("AVR-RT-02 strict layout change", case02))

    def legal_layout(trigger: str = "underfilled_without_structure") -> dict[str, Any]:
        item = contract()
        item["effective_visual_plan"]["layout_pattern"] = "left_logic_right_proof"
        effective_primary(item)["component_region"] = "right"
        authorize(item, trigger=trigger)
        return item

    cases.append(("AVR-RT-03 adaptive legal layout", lambda: expect_pass(legal_layout())))

    def case04() -> None:
        item = contract(); item["effective_visual_plan"]["layout_pattern"] = "invented_layout"; authorize(item); expect_fail(item, "invalid effective layout")
    cases.append(("AVR-RT-04 invalid layout enum", case04))

    def case05() -> None:
        item = contract(); item["effective_visual_plan"]["layout_pattern"] = "four_quadrant_judgement"; effective_primary(item)["component_region"] = "right"; authorize(item); expect_fail(item, "incompatible")
    cases.append(("AVR-RT-05 incompatible region", case05))

    def case06() -> None:
        data = {"nodes": [{"id": "A"}, {"id": "B"}], "edges": [{"from": "A", "to": "B"}]}
        item = contract(layout="stack_architecture_with_right_insights", chart_type="architecture_flow_diagram", chart_data=data)
        item["effective_visual_plan"]["layout_pattern"] = "layered_architecture"; authorize(item); expect_pass(item)
    cases.append(("AVR-RT-06 remove empty insight layout", case06))

    def case07() -> None:
        item = contract(); effective_primary(item)["component_region"] = "insight_panel"; authorize(item); expect_fail(item, "incompatible")
    cases.append(("AVR-RT-07 insight panel component", case07))

    def case08() -> None:
        item = contract(); effective_primary(item)["chart_type"] = "metric_showcase_grid"; authorize(item); expect_pass(item)
    cases.append(("AVR-RT-08 cards to metrics", case08))

    def case09() -> None:
        item = contract(chart_data={"items": [{"label": "证据A"}]}); effective_primary(item)["chart_type"] = "metric_showcase_grid"; authorize(item); expect_fail(item, "target chart schema")
    cases.append(("AVR-RT-09 metrics missing value", case09))

    def case10() -> None:
        item = contract(); effective_primary(item)["chart_type"] = "roadmap_timeline_chart"; authorize(item); expect_fail(item, "chart transform not allowed")
    cases.append(("AVR-RT-10 cards to roadmap", case10))

    def case11() -> None:
        data = {"nodes": [{"id": "A"}, {"id": "B"}], "edges": [{"from": "A", "to": "B"}]}
        item = contract(layout="layered_architecture", chart_type="layered_stack_diagram", chart_data=data); effective_primary(item)["chart_type"] = "architecture_flow_diagram"; authorize(item); expect_pass(item)
    cases.append(("AVR-RT-11 layered to flow", case11))

    def case12() -> None:
        data = {"nodes": [{"id": "A"}, {"id": "B"}]}
        item = contract(layout="layered_architecture", chart_type="layered_stack_diagram", chart_data=data); effective_primary(item)["chart_type"] = "architecture_flow_diagram"; authorize(item); expect_fail(item, "target chart schema")
    cases.append(("AVR-RT-12 layered missing edges", case12))

    def case13() -> None:
        data = {"options": [], "criteria": [], "tradeoff": []}
        item = contract(layout="two_column_comparison", chart_type="comparison_table", chart_data=data); effective_primary(item)["chart_type"] = "decision_table"; authorize(item); expect_fail(item, "target chart schema")
    cases.append(("AVR-RT-13 comparison missing recommendation", case13))

    def case14() -> None:
        item = contract(title="AI方案必须提升30%")
        item["effective_visual_plan"]["visible_title"] = "AI方案必须实现30%提升"; authorize(item); expect_pass(item)
    cases.append(("AVR-RT-14 copy preserves tokens", case14))

    def case15() -> None:
        item = contract(title="AI方案必须提升30%")
        item["effective_visual_plan"]["visible_title"] = "AI方案必须实现40%提升"; authorize(item); expect_fail(item, "lost protected tokens")
    cases.append(("AVR-RT-15 copy changes number", case15))

    def case16() -> None:
        item = contract(title="AI方案必须提升30%")
        item["effective_visual_plan"]["visible_title"] = "AI方案实现30%提升"; authorize(item); expect_fail(item, "lost protected tokens")
    cases.append(("AVR-RT-16 copy drops modal", case16))

    def case17() -> None:
        item = contract(); item["source_contract"]["title"] = "被篡改的源标题"; expect_fail(item, "source_visual_plan.visible_title")
    cases.append(("AVR-RT-17 source contract mutation", case17))

    def case18() -> None:
        item = contract(required_evidence=["证据A"])
        effective_primary(item)["visible_labels"].remove("证据A"); authorize(item); expect_fail(item, "required evidence missing")
    cases.append(("AVR-RT-18 evidence loss", case18))

    def case19() -> None:
        item = contract(); effective_primary(item)["semantic_constraints"]["main_visual_logic"] = "被改写"; authorize(item); expect_fail(item, "semantic field changed")
    cases.append(("AVR-RT-19 relation loss", case19))

    def case20() -> None:
        item = legal_layout(); item["recomposition_audit"]["layout_changed"] = False; expect_fail(item, "does not match real diff")
    cases.append(("AVR-RT-20 audit mismatch", case20))

    def case21() -> None:
        item = legal_layout(); item["recomposition_audit"]["quality_delta"] = {"baseline_score": 94, "effective_score": 92}; expect_fail(item, "score higher")
    cases.append(("AVR-RT-21 degraded candidate", case21))

    cases.append(("AVR-RT-22 improved underfill candidate", lambda: expect_pass(legal_layout())))
    cases.append(("AVR-RT-23 user strict override", lambda: expect_pass(contract(mode="strict_fidelity"))))

    def case24() -> None:
        item = contract(); item["recomposition_audit"]["return_to_A_required"] = True; expect_fail(item, "return_to_A_required")
    cases.append(("AVR-RT-24 return to A", case24))

    def case25() -> None:
        html_builder = load_module("html_builder", SKILLS / "huawei_ppt_builder_html" / "tools" / "render_contract_builder.py")
        source_page = page()
        assert build_contract(source_page) == html_builder.build_contract(copy.deepcopy(source_page))
    cases.append(("AVR-RT-25 builder HTML parity", case25))

    def case26() -> None:
        html_validator = load_module("html_validator", SKILLS / "huawei_ppt_builder_html" / "tools" / "validate_html_delivery.py")
        item = contract()
        with tempfile.TemporaryDirectory(prefix="avr-html-") as temp_dir:
            path = Path(temp_dir) / "P01_render_contract.json"
            path.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
            found: list[str] = []
            html_validator.check_contract_metadata(
                Path("P01.html"),
                '<main class="slide" data-page-id="P01" data-recomposition-mode="adaptive_recomposition" data-effective-layout-pattern="executive_summary_dashboard"><div data-component-id="C1" data-effective-chart-type="roadmap_timeline_chart"></div></main>',
                path,
                found,
            )
            assert any("component metadata mismatch" in message for message in found), found
    cases.append(("AVR-RT-26 HTML metadata mismatch", case26))

    def case27() -> None:
        item = contract(title="AI方案必须提升30%")
        item["effective_visual_plan"]["visible_title"] = "AI方案必须实现30%提升"; authorize(item); item["recomposition_audit"]["copy_adjustments"] = []; expect_fail(item, "copy changes are not recorded")
    cases.append(("AVR-RT-27 unrecorded copy diff", case27))

    cases.append(("AVR-RT-28 repeated skeleton improvement", lambda: expect_pass(legal_layout("repeated_skeleton"))))

    for name, test in cases:
        test()
        print(f"PASS: {name}")
    assert len(cases) == 28
    print("OK: 28 adaptive visual recomposition cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
