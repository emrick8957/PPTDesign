#!/usr/bin/env python3
"""Validate source/effective Role C visual recomposition contracts."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

from validate_inputs import CHART_TYPES, LAYOUT_COMPONENT_REGIONS, LAYOUT_PATTERNS

RECOMPOSITION_MODES = {"strict_fidelity", "adaptive_recomposition"}
MODAL_TOKENS = ("不得", "不能", "不", "仅", "必须", "可能", "建议", "至少", "最多")

LAYOUT_FAMILIES = {
    "executive_summary_dashboard": "argument",
    "three_column_cards": "argument",
    "multi_module_solution_overview": "argument",
    "left_logic_right_proof": "argument",
    "metric_case_showcase_grid": "argument",
    "insight_panel_with_chart": "argument",
    "two_column_comparison": "comparison",
    "four_quadrant_judgement": "comparison",
    "risk_decision_matrix": "comparison",
    "layered_architecture": "architecture",
    "stack_architecture_with_right_insights": "architecture",
    "ecosystem_map": "architecture",
    "hub_spoke_ecosystem_canvas": "architecture",
    "roadmap_timeline": "temporal",
    "trend_curve_with_strategy": "temporal",
    "image_background_section_divider": "image",
}


def list_items(data: dict[str, Any], *keys: str) -> list[dict[str, Any]]:
    for key in keys:
        value = data.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def metrics_ready(data: dict[str, Any]) -> bool:
    items = list_items(data, "metrics", "items", "cards")
    return bool(items) and all(
        any(key in item for key in ("label", "name", "headline"))
        and "value" in item
        for item in items
    )


def cases_ready(data: dict[str, Any]) -> bool:
    items = list_items(data, "cases", "items", "cards")
    return bool(items) and all(
        any(key in item for key in ("takeaway", "proof"))
        and any(key in item for key in ("source", "source_status"))
        for item in items
    )


def decision_ready(data: dict[str, Any]) -> bool:
    required = {"options", "criteria", "tradeoff", "recommendation"}
    return required.issubset(data)


def flow_ready(data: dict[str, Any]) -> bool:
    nodes = data.get("nodes")
    edges = data.get("edges")
    return (
        isinstance(nodes, list)
        and bool(nodes)
        and isinstance(edges, list)
        and bool(edges)
        and all(isinstance(edge, dict) and edge.get("from") and edge.get("to") for edge in edges)
    )


def layers_ready(data: dict[str, Any]) -> bool:
    layers = data.get("layers")
    if isinstance(layers, list) and layers:
        return True
    nodes = data.get("nodes")
    return isinstance(nodes, list) and bool(nodes) and all(
        isinstance(node, dict) and node.get("layer") for node in nodes
    )


CHART_TRANSFORMS: dict[tuple[str, str], Callable[[dict[str, Any]], bool]] = {
    ("key_findings_cards", "metric_showcase_grid"): metrics_ready,
    ("metric_showcase_grid", "key_findings_cards"): metrics_ready,
    ("case_gallery_cards", "key_findings_cards"): cases_ready,
    ("comparison_table", "decision_table"): decision_ready,
    ("layered_stack_diagram", "architecture_flow_diagram"): flow_ready,
    ("architecture_flow_diagram", "layered_stack_diagram"): layers_ready,
}


def component_map(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    components = plan.get("chart_components")
    if not isinstance(components, list):
        return {}
    return {
        str(item.get("component_id")): item
        for item in components
        if isinstance(item, dict) and item.get("component_id")
    }


def critical_tokens(text: object) -> set[str]:
    value = str(text or "")
    tokens = set(re.findall(r"\d+(?:\.\d+)?%?|[A-Za-z][A-Za-z0-9_.+-]*", value))
    tokens.update(token for token in MODAL_TOKENS if token in value)
    return tokens


def legacy_plans(contract: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    intent = contract.get("render_intent") if isinstance(contract.get("render_intent"), dict) else {}
    source = contract.get("source_contract") if isinstance(contract.get("source_contract"), dict) else {}
    plan = {
        "layout_pattern": intent.get("layout_pattern"),
        "chart_components": copy.deepcopy(intent.get("chart_components", [])),
        "visible_title": source.get("title", ""),
        "visible_conclusion": source.get("conclusion", ""),
    }
    return plan, copy.deepcopy(plan)


def validate_contract(contract: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    page_id = str(contract.get("page_id", "UNKNOWN"))
    mode = contract.get("recomposition_mode")
    source = contract.get("source_visual_plan")
    effective = contract.get("effective_visual_plan")
    audit = contract.get("recomposition_audit")
    legacy_mode = source is None and effective is None

    if legacy_mode:
        warnings.append(f"{page_id}: legacy render contract treated as strict_fidelity")
        mode = "strict_fidelity"
        source, effective = legacy_plans(contract)
        audit = {}
    if mode not in RECOMPOSITION_MODES:
        errors.append(f"{page_id}: unsupported recomposition_mode={mode!r}")
    if not isinstance(source, dict) or not isinstance(effective, dict):
        errors.append(f"{page_id}: source_visual_plan and effective_visual_plan must be objects")
        return errors, warnings
    audit = audit if isinstance(audit, dict) else {}

    source_contract = contract.get("source_contract")
    source_contract = source_contract if isinstance(source_contract, dict) else {}
    if source.get("visible_title") != source_contract.get("title"):
        errors.append(f"{page_id}: source_visual_plan.visible_title differs from source_contract.title")
    if source.get("visible_conclusion") != source_contract.get("conclusion"):
        errors.append(f"{page_id}: source_visual_plan.visible_conclusion differs from source_contract.conclusion")

    if mode == "strict_fidelity" and source != effective:
        errors.append(f"{page_id}: strict_fidelity requires source_visual_plan == effective_visual_plan")

    source_layout = source.get("layout_pattern")
    target_layout = effective.get("layout_pattern")
    if source_layout not in LAYOUT_PATTERNS:
        errors.append(f"{page_id}: invalid source layout_pattern={source_layout!r}")
    if target_layout not in LAYOUT_PATTERNS:
        errors.append(f"{page_id}: invalid effective layout_pattern={target_layout!r}")
    elif source_layout != target_layout and LAYOUT_FAMILIES.get(str(source_layout)) != LAYOUT_FAMILIES.get(str(target_layout)):
        errors.append(f"{page_id}: cross-family layout transform is not allowed: {source_layout!r} -> {target_layout!r}")

    source_components = component_map(source)
    target_components = component_map(effective)
    if set(source_components) != set(target_components):
        errors.append(f"{page_id}: effective component IDs must equal source component IDs")

    used_regions: list[str] = []
    chart_changed = False
    region_changed = False
    for component_id, source_component in source_components.items():
        target = target_components.get(component_id)
        if target is None:
            continue
        for field in ("component_role", "supports_component_id", "chart_proof_goal", "chart_data", "semantic_constraints", "component_coverage"):
            if source_component.get(field) != target.get(field):
                errors.append(f"{page_id}.{component_id}: semantic field changed: {field}")
        role = target.get("component_role")
        region = target.get("component_region")
        used_regions.append(str(region))
        allowed_regions = LAYOUT_COMPONENT_REGIONS.get(str(target_layout), {}).get(str(role), set())
        if region not in allowed_regions:
            errors.append(f"{page_id}.{component_id}: region={region!r} incompatible with effective layout={target_layout!r} role={role!r}")
        if region != source_component.get("component_region"):
            region_changed = True
        source_type = source_component.get("chart_type")
        target_type = target.get("chart_type")
        if target_type not in CHART_TYPES:
            errors.append(f"{page_id}.{component_id}: invalid effective chart_type={target_type!r}")
        if target_type != source_type:
            chart_changed = True
            checker = CHART_TRANSFORMS.get((str(source_type), str(target_type)))
            data = source_component.get("chart_data")
            data = data if isinstance(data, dict) else {}
            if checker is None:
                errors.append(f"{page_id}.{component_id}: chart transform not allowed: {source_type!r} -> {target_type!r}")
            elif not checker(data):
                errors.append(f"{page_id}.{component_id}: source chart_data does not satisfy target chart schema")
        required = source_component.get("component_coverage", {}).get("required_evidence", [])
        missing = target.get("component_coverage", {}).get("missing_required_evidence", [])
        labels = target.get("visible_labels", [])
        if isinstance(required, list):
            missing_from_labels = [item for item in required if item not in labels]
            if missing_from_labels or missing:
                errors.append(f"{page_id}.{component_id}: required evidence missing: {missing_from_labels or missing}")
    if len(used_regions) != len(set(used_regions)):
        errors.append(f"{page_id}: effective component regions must be unique")

    title_changed = source.get("visible_title") != effective.get("visible_title")
    conclusion_changed = source.get("visible_conclusion") != effective.get("visible_conclusion")
    for field in ("visible_title", "visible_conclusion"):
        source_tokens = critical_tokens(source.get(field))
        target_tokens = critical_tokens(effective.get(field))
        missing_tokens = sorted(source_tokens - target_tokens)
        if missing_tokens:
            errors.append(f"{page_id}: {field} lost protected tokens: {missing_tokens}")

    layout_changed = source_layout != target_layout
    any_change = layout_changed or chart_changed or region_changed or title_changed or conclusion_changed
    if audit:
        expected_flags = {
            "layout_changed": layout_changed,
            "chart_type_changed": chart_changed,
            "component_region_changed": region_changed,
        }
        for field, expected in expected_flags.items():
            if audit.get(field) is not expected:
                errors.append(f"{page_id}: recomposition_audit.{field} does not match real diff")
        copy_adjustments = audit.get("copy_adjustments")
        if (title_changed or conclusion_changed) and not isinstance(copy_adjustments, list):
            errors.append(f"{page_id}: copy changes require copy_adjustments")
        if (title_changed or conclusion_changed) and isinstance(copy_adjustments, list) and not copy_adjustments:
            errors.append(f"{page_id}: copy changes are not recorded")
        invariants = audit.get("semantic_invariants")
        if not isinstance(invariants, dict) or not all(invariants.get(key) is True for key in (
            "core_judgement_preserved", "chart_proof_goals_preserved", "facts_preserved", "relations_preserved"
        )):
            errors.append(f"{page_id}: semantic_invariants must all PASS")
        total_required = sum(
            len(component.get("component_coverage", {}).get("required_evidence", []))
            for component in source_components.values()
        )
        coverage = audit.get("evidence_coverage")
        if not isinstance(coverage, dict) or coverage.get("required") != total_required or coverage.get("covered") != total_required or coverage.get("missing") != []:
            errors.append(f"{page_id}: recomposition_audit.evidence_coverage is incomplete")
        if any_change and not audit.get("trigger_reasons"):
            errors.append(f"{page_id}: changed effective plan requires trigger_reasons")
        quality = audit.get("quality_delta")
        if any_change:
            if not isinstance(quality, dict) or not isinstance(quality.get("baseline_score"), (int, float)) or not isinstance(quality.get("effective_score"), (int, float)):
                errors.append(f"{page_id}: changed effective plan requires numeric baseline/effective scores")
            elif quality["effective_score"] <= quality["baseline_score"]:
                errors.append(f"{page_id}: effective plan must score higher than baseline")
        if audit.get("return_to_A_required") is True:
            errors.append(f"{page_id}: return_to_A_required=true blocks rendering")
    elif any_change:
        errors.append(f"{page_id}: changed effective plan requires recomposition_audit")

    intent = contract.get("render_intent")
    intent = intent if isinstance(intent, dict) else {}
    effective_primary = next(
        (item for item in target_components.values() if item.get("component_role") == "primary"),
        None,
    )
    if intent.get("layout_pattern") != target_layout:
        errors.append(f"{page_id}: render_intent.layout_pattern must derive from effective_visual_plan")
    if effective_primary and intent.get("chart_type") != effective_primary.get("chart_type"):
        errors.append(f"{page_id}: render_intent.chart_type must derive from effective primary")
    if intent.get("chart_components") != effective.get("chart_components"):
        errors.append(f"{page_id}: render_intent.chart_components must derive from effective_visual_plan")
    visible = contract.get("visible_text_plan")
    visible = visible if isinstance(visible, dict) else {}
    if visible.get("title") != effective.get("visible_title"):
        errors.append(f"{page_id}: visible_text_plan.title must derive from effective_visual_plan")
    if not legacy_mode and visible.get("conclusion") != effective.get("visible_conclusion"):
        errors.append(f"{page_id}: visible_text_plan.conclusion must derive from effective_visual_plan")
    return errors, warnings


def contract_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(path.glob("P*_render_contract.json"))


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Validate Role C visual recomposition contracts.")
    parser.add_argument("path", help="Render contract JSON file or directory.")
    args = parser.parse_args()
    files = contract_files(Path(args.path))
    if not files:
        print("ERROR: no render contract files found")
        return 1
    all_errors: list[str] = []
    for path in files:
        try:
            contract = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            all_errors.append(f"{path}: invalid JSON: {exc}")
            continue
        errors, warnings = validate_contract(contract)
        for warning in warnings:
            print(f"WARNING: {warning}")
        all_errors.extend(errors)
    for message in all_errors:
        print(f"ERROR: {message}")
    if all_errors:
        print("BLOCKED: visual recomposition validation failed; return_to_A_required=true")
        return 1
    print(f"OK: validated {len(files)} visual recomposition contract(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
