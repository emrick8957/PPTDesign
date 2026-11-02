#!/usr/bin/env python3
"""Validate Role C source inputs before rendering."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_FILES = [
    "deck_spec.json",
    "page_design.md",
    "chart_patterns.md",
    "layout_library.md",
    "deck_spec_field_dictionary.md",
]

OPTIONAL_FALLBACK_FILES = {
    "visual_rules.md": "use policies/huawei_visual_gate.md as the minimal fallback",
}

BASE_REQUIRED_PAGE_FIELDS = ["title", "conclusion", "core_judgement", "layout_pattern"]
LEGACY_REQUIRED_PAGE_FIELDS = ["chart_type", "chart_proof_goal"]
LEGACY_PRIMARY_FIELDS = {
    "chart_type",
    "chart_data",
    "chart_proof_goal",
    "chart_visual_boundary",
    "chart_semantic_mapping",
}

CHART_TYPES = {
    "none",
    "key_findings_cards",
    "quadrant_matrix",
    "comparison_table",
    "capability_radar",
    "capability_map",
    "layered_stack_diagram",
    "architecture_flow_diagram",
    "roadmap_timeline_chart",
    "trend_curve",
    "ecosystem_relationship_map",
    "gap_heatmap",
    "risk_matrix",
    "decision_table",
    "value_chain_loop",
    "swimlane_process",
    "priority_matrix",
    "metric_showcase_grid",
    "case_gallery_cards",
    "hub_spoke_relationship_map",
}

LAYOUT_PATTERNS = {
    "executive_summary_dashboard",
    "two_column_comparison",
    "four_quadrant_judgement",
    "three_column_cards",
    "layered_architecture",
    "stack_architecture_with_right_insights",
    "roadmap_timeline",
    "trend_curve_with_strategy",
    "ecosystem_map",
    "insight_panel_with_chart",
    "risk_decision_matrix",
    "multi_module_solution_overview",
    "left_logic_right_proof",
    "hub_spoke_ecosystem_canvas",
    "metric_case_showcase_grid",
    "image_background_section_divider",
}

PAGE_TYPES = {
    "cover",
    "agenda",
    "executive_summary",
    "context_trend",
    "problem_diagnosis",
    "comparison",
    "architecture",
    "capability_map",
    "roadmap",
    "risk_matrix",
    "decision_table",
    "thank_you",
}

CHART_TYPE_TO_PAGE_TYPE = {
    "none": "executive_summary",
    "key_findings_cards": "executive_summary",
    "quadrant_matrix": "comparison",
    "comparison_table": "comparison",
    "capability_radar": "capability_map",
    "capability_map": "capability_map",
    "layered_stack_diagram": "architecture",
    "architecture_flow_diagram": "architecture",
    "roadmap_timeline_chart": "roadmap",
    "trend_curve": "context_trend",
    "ecosystem_relationship_map": "architecture",
    "gap_heatmap": "problem_diagnosis",
    "risk_matrix": "risk_matrix",
    "decision_table": "decision_table",
    "value_chain_loop": "architecture",
    "swimlane_process": "architecture",
    "priority_matrix": "comparison",
    "metric_showcase_grid": "executive_summary",
    "case_gallery_cards": "executive_summary",
    "hub_spoke_relationship_map": "architecture",
}

COMPONENT_ROLES = {"primary", "supporting"}
COMPONENT_REGIONS = {"main", "left", "right", "top", "bottom"}
MAX_SUPPORTING_COMPONENTS = 3

# Single source of truth for layout_pattern x component_role x component_region.
LAYOUT_COMPONENT_REGIONS: dict[str, dict[str, set[str]]] = {
    "executive_summary_dashboard": {"primary": {"main", "left", "right"}, "supporting": {"left", "right", "top", "bottom"}},
    "two_column_comparison": {"primary": {"main", "left", "right"}, "supporting": {"left", "right", "bottom"}},
    "four_quadrant_judgement": {"primary": {"main"}, "supporting": {"bottom"}},
    "three_column_cards": {"primary": {"main", "left", "right"}, "supporting": {"left", "right", "bottom"}},
    "layered_architecture": {"primary": {"main"}, "supporting": {"bottom"}},
    "stack_architecture_with_right_insights": {"primary": {"main"}, "supporting": {"bottom"}},
    "roadmap_timeline": {"primary": {"main"}, "supporting": {"bottom"}},
    "trend_curve_with_strategy": {"primary": {"main", "left"}, "supporting": {"bottom"}},
    "ecosystem_map": {"primary": {"main"}, "supporting": {"bottom"}},
    "insight_panel_with_chart": {"primary": {"main", "left"}, "supporting": {"bottom"}},
    "risk_decision_matrix": {"primary": {"main", "left", "right"}, "supporting": {"left", "right", "top", "bottom"}},
    "multi_module_solution_overview": {"primary": {"main", "left", "right"}, "supporting": {"left", "right", "top", "bottom"}},
    "left_logic_right_proof": {"primary": {"main", "right"}, "supporting": {"right", "bottom"}},
    "hub_spoke_ecosystem_canvas": {"primary": {"main"}, "supporting": {"bottom"}},
    "metric_case_showcase_grid": {"primary": {"main", "left", "right"}, "supporting": {"left", "right", "top", "bottom"}},
    "image_background_section_divider": {"primary": {"main"}, "supporting": set()},
}

EDGE_ROLE_TYPES = {"flow_decompose", "flow_integrate", "lifecycle_close", "feedback_loop"}
DEPRECATED_REGION_TERMS = ("正文区", "内容区")


def error(message: str, errors: list[str]) -> None:
    errors.append(message)


def as_list(value: object) -> list[object]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def normalize_goal(value: object) -> str:
    return re.sub(r"[\W_]+", "", str(value), flags=re.UNICODE).lower()


def bottom_bar_enabled(value: object) -> bool:
    text = str(value or "").strip().lower()
    if not text:
        return False
    disabled_tokens = ("disabled", "disable", "off", "none", "不启用", "不使用", "禁用", "取消", "无")
    return not any(token in text for token in disabled_tokens)


def page_design_bottom_bar_rules(text: str) -> dict[str, str]:
    rules: dict[str, str] = {}
    current_page: str | None = None
    for raw_line in text.splitlines():
        heading = re.match(r"^##\s+P0*(\d+)\b", raw_line)
        if heading:
            current_page = f"P{int(heading.group(1)):02d}"
            continue
        if raw_line.startswith("## "):
            current_page = None
            continue
        if current_page:
            match = re.match(r"^-\s+`bottom_bar_rule`：\s*(.+)$", raw_line.strip())
            if match:
                rules[current_page] = match.group(1).strip()
    return rules


def normalize_chart_contract(page: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    """Return one normalized component list without mutating Role A's source object."""
    if "chart_components" in page:
        components = page.get("chart_components")
        return "chart_components", [dict(item) for item in components] if isinstance(components, list) else []
    legacy = {
        "component_id": "C1",
        "component_role": "primary",
        "component_region": "main",
        "chart_type": page.get("chart_type"),
        "chart_data": page.get("chart_data", {}),
        "chart_proof_goal": page.get("chart_proof_goal"),
        "chart_visual_boundary": page.get("chart_visual_boundary", []),
        "chart_semantic_mapping": page.get("chart_semantic_mapping", {}),
        "required_evidence": page.get("required_evidence", []),
    }
    return "legacy_top_level", [legacy]


def primary_component(page: dict[str, Any]) -> dict[str, Any]:
    _, components = normalize_chart_contract(page)
    for component in components:
        if component.get("component_role") == "primary":
            return component
    return components[0] if components else {}


def validate_terminology(page: dict[str, object], page_id: str, warnings: list[str]) -> None:
    component_values: list[object] = []
    for component in as_list(page.get("chart_components")):
        if isinstance(component, dict):
            component_values.extend(as_list(component.get("chart_visual_boundary")))
            component_values.extend(as_list(component.get("display_text")))
    scan_values = [
        page.get("visual_notes", ""),
        " ".join(str(item) for item in as_list(page.get("chart_visual_boundary"))),
        " ".join(str(item) for item in as_list(page.get("display_text"))),
        " ".join(str(item) for item in component_values),
    ]
    joined = " ".join(str(value) for value in scan_values)
    for term in DEPRECATED_REGION_TERMS:
        if term in joined:
            warnings.append(f"{page_id}: deprecated region term appears: {term}; use 主体区/文字区")
    display_items = as_list(page.get("display_text"))
    for component in as_list(page.get("chart_components")):
        if isinstance(component, dict):
            display_items.extend(as_list(component.get("display_text")))
    for item in display_items:
        if len(str(item)) > 15:
            warnings.append(f"{page_id}: display_text item is longer than 15 Chinese chars; consider phrase compression")


def normalized_page_id(page: dict[str, object], index: int, errors: list[str]) -> str | None:
    page_id = page.get("page_id")
    if isinstance(page_id, str) and re.fullmatch(r"P\d{2,}", page_id):
        return page_id
    slide_no = page.get("slide_no")
    if isinstance(slide_no, int) and slide_no > 0:
        return f"P{slide_no:02d}"
    error(f"pages[{index}] requires page_id=Pxx or a positive slide_no", errors)
    return None


def validate_semantic_mapping(
    owner: str,
    chart_data: object,
    mapping: object,
    errors: list[str],
) -> None:
    data = chart_data if isinstance(chart_data, dict) else {}
    nodes = data.get("nodes")
    nodes = nodes if isinstance(nodes, list) else []
    node_ids = {
        node.get("id") for node in nodes
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    edges = data.get("edges")
    edges = edges if isinstance(edges, list) else []
    edge_refs = {
        (edge.get("from"), edge.get("to")) for edge in edges
        if isinstance(edge, dict) and isinstance(edge.get("from"), str) and isinstance(edge.get("to"), str)
    }
    if mapping is None:
        return
    if not isinstance(mapping, dict):
        error(f"{owner}.chart_semantic_mapping must be an object", errors)
        return
    for field in ("correspondence_pairs", "forbidden_visualization"):
        value = mapping.get(field)
        if value is not None and not isinstance(value, list):
            error(f"{owner}.chart_semantic_mapping.{field} must be an array", errors)
    pairs = mapping.get("correspondence_pairs")
    if isinstance(pairs, list):
        for pair in pairs:
            if not isinstance(pair, dict):
                error(f"{owner}.correspondence_pairs items must be objects", errors)
                continue
            for side in ("left", "right"):
                node_id = pair.get(side)
                if not isinstance(node_id, str) or node_id not in node_ids:
                    error(f"{owner}.correspondence_pairs.{side} references unknown node: {node_id!r}", errors)
    edge_roles = mapping.get("edge_roles")
    if edge_roles is not None and not isinstance(edge_roles, dict):
        error(f"{owner}.chart_semantic_mapping.edge_roles must be an object", errors)
    elif isinstance(edge_roles, dict):
        for role, role_edges in edge_roles.items():
            if role not in EDGE_ROLE_TYPES:
                error(f"{owner}.edge_roles contains unsupported role: {role!r}", errors)
            if not isinstance(role_edges, list):
                error(f"{owner}.edge_roles.{role} must be an array", errors)
                continue
            for edge in role_edges:
                if not isinstance(edge, dict):
                    error(f"{owner}.edge_roles.{role} items must be objects", errors)
                    continue
                edge_ref = (edge.get("from"), edge.get("to"))
                if edge_ref not in edge_refs:
                    error(f"{owner}.edge_roles.{role} references unknown edge: {edge_ref!r}", errors)


def validate_component_contract(
    page: dict[str, Any], page_id: str, layout_pattern: object, errors: list[str]
) -> str | None:
    mixed = sorted(field for field in LEGACY_PRIMARY_FIELDS if field in page)
    if mixed:
        error(f"{page_id} mixes chart_components with legacy top-level fields: {mixed}", errors)
    components = page.get("chart_components")
    if not isinstance(components, list) or not components:
        error(f"{page_id}.chart_components must be a non-empty array", errors)
        return None

    primary_items = [item for item in components if isinstance(item, dict) and item.get("component_role") == "primary"]
    supporting_items = [item for item in components if isinstance(item, dict) and item.get("component_role") == "supporting"]
    if len(primary_items) != 1:
        error(f"{page_id}.chart_components requires exactly one primary component", errors)
    if len(supporting_items) > MAX_SUPPORTING_COMPONENTS:
        error(f"{page_id}.chart_components allows at most {MAX_SUPPORTING_COMPONENTS} supporting components", errors)
    primary_id = primary_items[0].get("component_id") if len(primary_items) == 1 else None
    primary_type = primary_items[0].get("chart_type") if len(primary_items) == 1 else None

    ids: list[str] = []
    regions: list[str] = []
    goals: list[tuple[str, str]] = []
    boundaries: list[tuple[str, tuple[str, ...]]] = []
    compatibility = LAYOUT_COMPONENT_REGIONS.get(str(layout_pattern), {})
    for component_index, component in enumerate(components):
        owner = f"{page_id}.chart_components[{component_index}]"
        if not isinstance(component, dict):
            error(f"{owner} must be an object", errors)
            continue
        component_id = component.get("component_id")
        role = component.get("component_role")
        region = component.get("component_region")
        chart_type = component.get("chart_type")
        proof_goal = component.get("chart_proof_goal")
        if not isinstance(component_id, str) or not re.fullmatch(r"C[1-9]\d*", component_id):
            error(f"{owner}.component_id must match C1, C2, ...", errors)
        else:
            ids.append(component_id)
        if role not in COMPONENT_ROLES:
            error(f"{owner}.component_role is not supported: {role!r}", errors)
        if region not in COMPONENT_REGIONS:
            error(f"{owner}.component_region is not supported: {region!r}; insight_panel is never a component region", errors)
        else:
            regions.append(str(region))
            allowed = compatibility.get(str(role), set())
            if region not in allowed:
                error(f"{owner}.component_region={region!r} is incompatible with layout_pattern={layout_pattern!r} and role={role!r}", errors)
        if chart_type not in CHART_TYPES:
            error(f"{owner}.chart_type is not a supported enum: {chart_type!r}", errors)
        if not isinstance(component.get("chart_data"), dict):
            error(f"{owner}.chart_data must be an object", errors)
        if not isinstance(proof_goal, str) or not proof_goal.strip():
            error(f"{owner}.chart_proof_goal must be a non-empty string", errors)
        elif isinstance(component_id, str):
            goals.append((component_id, normalize_goal(proof_goal)))
        if not isinstance(component.get("chart_visual_boundary"), list):
            error(f"{owner}.chart_visual_boundary must be an array", errors)
        elif isinstance(component_id, str):
            normalized_boundary = tuple(
                sorted(
                    normalize_goal(item)
                    for item in component["chart_visual_boundary"]
                    if normalize_goal(item)
                )
            )
            boundaries.append((component_id, normalized_boundary))
        if role == "primary" and component.get("supports_component_id") not in (None, ""):
            error(f"{owner}.supports_component_id must be empty for primary", errors)
        if role == "supporting":
            if chart_type == "none":
                error(f"{owner}: supporting component chart_type cannot be 'none'", errors)
            if component.get("supports_component_id") != primary_id:
                error(f"{owner}.supports_component_id must reference primary component {primary_id!r}", errors)
        validate_semantic_mapping(owner, component.get("chart_data"), component.get("chart_semantic_mapping"), errors)

    if len(ids) != len(set(ids)):
        error(f"{page_id}.chart_components component_id values must be unique", errors)
    if len(regions) != len(set(regions)):
        error(f"{page_id}.chart_components component_region values must be unique", errors)
    if primary_type == "none" and supporting_items:
        error(f"{page_id}: primary chart_type='none' cannot have supporting components", errors)
    if layout_pattern == "image_background_section_divider" and primary_type != "none":
        error(f"{page_id}: image_background_section_divider requires primary chart_type='none'", errors)

    for left_index, (left_id, left_goal) in enumerate(goals):
        for right_id, right_goal in goals[left_index + 1:]:
            if left_goal and right_goal and (left_goal == right_goal or left_goal.startswith(right_goal) or right_goal.startswith(left_goal)):
                error(f"{page_id}: component proof goals must be differentiated; {left_id} and {right_id} repeat/prefix one another", errors)
    for left_index, (left_id, left_boundary) in enumerate(boundaries):
        for right_id, right_boundary in boundaries[left_index + 1:]:
            if left_boundary and left_boundary == right_boundary:
                error(f"{page_id}: component chart_visual_boundary values must be differentiated; {left_id} and {right_id} are identical", errors)
    return str(primary_type) if isinstance(primary_type, str) else None


def validate_page(page: object, index: int, errors: list[str], allow_legacy_types: bool = False) -> str | None:
    if not isinstance(page, dict):
        error(f"pages[{index}] must be an object", errors)
        return None
    page_id = normalized_page_id(page, index, errors)
    owner = page_id or f"pages[{index}]"
    for field in BASE_REQUIRED_PAGE_FIELDS:
        value = page.get(field)
        if not isinstance(value, str) or not value.strip():
            error(f"{owner} missing non-empty field: {field}", errors)

    layout_pattern = page.get("layout_pattern")
    if layout_pattern not in LAYOUT_PATTERNS:
        error(f"{owner}.layout_pattern is not a supported enum: {layout_pattern!r}", errors)

    if "chart_components" in page:
        chart_type = validate_component_contract(page, owner, layout_pattern, errors)
    else:
        for field in LEGACY_REQUIRED_PAGE_FIELDS:
            value = page.get(field)
            if not isinstance(value, str) or not value.strip():
                error(f"{owner} missing non-empty legacy field: {field}", errors)
        chart_type = page.get("chart_type")
        if chart_type not in CHART_TYPES:
            error(f"{owner}.chart_type is not a supported enum: {chart_type!r}", errors)
        boundary = page.get("chart_visual_boundary")
        if boundary is not None and not isinstance(boundary, list):
            error(f"{owner}.chart_visual_boundary must be an array", errors)
        validate_semantic_mapping(owner, page.get("chart_data"), page.get("chart_semantic_mapping"), errors)

    page_type = page.get("type") or page.get("page_type") or CHART_TYPE_TO_PAGE_TYPE.get(chart_type)
    if page_type not in PAGE_TYPES and not allow_legacy_types:
        error(f"{owner}.type is not a supported enum: {page_type!r}", errors)
    return page_id


def validate_root(root: str, allow_legacy_types: bool = False) -> tuple[int, int, list[str], list[str]]:
    base = Path(root)
    errors: list[str] = []
    warnings: list[str] = []
    missing = [name for name in REQUIRED_FILES if not (base / name).is_file()]
    for name in missing:
        error(f"missing required file: {name}", errors)
    for name, fallback in OPTIONAL_FALLBACK_FILES.items():
        if not (base / name).is_file():
            warnings.append(f"missing optional file: {name}; {fallback}")
    if errors:
        return 0, len(REQUIRED_FILES), warnings, errors
    try:
        deck = json.loads((base / "deck_spec.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return 0, len(REQUIRED_FILES), warnings, [f"invalid deck_spec.json: {exc}"]
    pages = (deck.get("pages") or deck.get("slides")) if isinstance(deck, dict) else None
    if not isinstance(pages, list) or not pages:
        return 0, len(REQUIRED_FILES), warnings, ["deck_spec.json must contain a non-empty pages or slides array"]

    page_ids: list[str | None] = []
    for index, page in enumerate(pages):
        page_id = validate_page(page, index, errors, allow_legacy_types)
        page_ids.append(page_id)
        if page_id is not None and isinstance(page, dict):
            validate_terminology(page, page_id, warnings)
    valid_ids = [page_id for page_id in page_ids if page_id is not None]
    if len(set(valid_ids)) != len(valid_ids):
        error("page_id values must be unique", errors)
    numbers = [int(page_id[1:]) for page_id in valid_ids]
    if numbers != sorted(numbers):
        error(f"page_id values must be ordered: {valid_ids}", errors)
    elif numbers and numbers != list(range(numbers[0], numbers[0] + len(numbers))):
        warnings.append(f"page_id values are not continuous; treating as selected-page delivery: {valid_ids}")
    page_design = (base / "page_design.md").read_text(encoding="utf-8")
    bottom_bar_rules = page_design_bottom_bar_rules(page_design)
    for page_id in valid_ids:
        if page_id not in page_design:
            warnings.append(f"{page_id} is not explicitly referenced in page_design.md")
    for page, page_id in zip(pages, page_ids):
        if not isinstance(page, dict) or page_id is None or "chart_components" not in page:
            continue
        has_bottom_component = any(
            isinstance(component, dict) and component.get("component_region") == "bottom"
            for component in as_list(page.get("chart_components"))
        )
        explicit_rule = page.get("bottom_bar_rule", bottom_bar_rules.get(page_id, ""))
        if has_bottom_component and bottom_bar_enabled(explicit_rule):
            error(f"{page_id}: component_region='bottom' conflicts with enabled bottom_bar_rule", errors)
    return len(pages), len(REQUIRED_FILES), warnings, errors


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Validate Role C source inputs.")
    parser.add_argument("root", nargs="?", default=".", help="Root directory containing input files.")
    parser.add_argument("--legacy", action="store_true", help="Bypass strict type enum validation for legacy files.")
    args = parser.parse_args()
    pages, required_files, warnings, errors = validate_root(args.root, allow_legacy_types=args.legacy)
    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        print("BLOCKED: input validation failed; return_to_A_required=true")
        return 1
    print(f"OK: validated {pages} pages and {required_files} required files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
