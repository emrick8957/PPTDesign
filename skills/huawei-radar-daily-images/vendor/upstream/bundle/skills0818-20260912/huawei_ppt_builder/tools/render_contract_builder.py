#!/usr/bin/env python3
"""Compile page render contracts from the complete Role A design delivery."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_inputs import normalize_chart_contract, validate_root
from validate_recomposition import validate_contract as validate_recomposition_contract

GENERIC_VISIBLE_KEYS = {
    "label",
    "headline",
    "display_text",
    "title",
    "text",
    "name",
    "value",
    "description",
    "items",
    "metrics",
    "tags",
    "columns",
    "rows",
    "cells",
    "notes",
    "phases",
    "milestones",
    "goals",
    "actions",
    "owners",
    "risk",
    "impact",
    "probability",
    "mitigation",
    "owner",
    "option",
    "criteria",
    "tradeoff",
    "recommendation",
    "annotations",
    "legend",
}
LOGIC_ONLY_KEYS = {
    "id",
    "from",
    "to",
    "group",
    "role",
    "logic",
    "logic_only",
    "chart_proof_goal",
    "core_judgement",
    "forbidden_visualization",
}
DESIGN_KEYS = {
    "red_anchor",
    "card_hierarchy",
    "spacing_rule",
    "bottom_bar_rule",
    "visual_simplification",
    "visual_boundary",
    "page_type_gate",
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
RECOMPOSITION_MODES = {"strict_fidelity", "adaptive_recomposition"}


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if value.strip()))


def collect_visible_text(value: Any, key: str | None = None) -> list[str]:
    if key in LOGIC_ONLY_KEYS:
        return []
    if isinstance(value, dict):
        result: list[str] = []
        for child_key, child_value in value.items():
            result.extend(collect_visible_text(child_value, child_key))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(collect_visible_text(item, key))
        return result
    if key in GENERIC_VISIBLE_KEYS and isinstance(value, (str, int, float)):
        text = str(value).strip()
        if text and not text.lower().startswith("logic-only"):
            return [text]
    return []


def extract_structured_visible_content(chart_data: dict[str, Any]) -> list[str]:
    """Preserve component content while excluding relationship-only fields."""
    return unique(collect_visible_text(chart_data))


def density_profile(page: dict[str, Any]) -> str:
    budget = page.get("density_budget")
    if isinstance(budget, dict) and budget.get("density_profile"):
        return str(budget["density_profile"])
    text_density = str(page.get("text_density", "")).lower()
    if "high" in text_density or "高" in text_density:
        return "technical_deep_dive"
    return "executive_clean"


def build_density_budget(page: dict[str, Any]) -> dict[str, Any]:
    budget = page.get("density_budget")
    result = dict(budget) if isinstance(budget, dict) else {}
    result.setdefault("density_profile", density_profile(page))
    result.setdefault("underfill_action", "return_to_A")
    return result


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def normalized_page_id(page: dict[str, Any]) -> str:
    page_id = page.get("page_id")
    if isinstance(page_id, str) and page_id:
        return page_id
    slide_no = page.get("slide_no")
    if isinstance(slide_no, int) and slide_no > 0:
        return f"P{slide_no:02d}"
    raise KeyError("page_id or slide_no")


def parse_page_design(text: str) -> tuple[list[str], dict[str, dict[str, Any]]]:
    """Keep Role A prose intact while extracting stable visual override keys."""
    global_lines: list[str] = []
    pages: dict[str, dict[str, Any]] = {}
    current_page: str | None = None
    current_section = ""
    in_global_defaults = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        heading = re.match(r"^##\s+P0*(\d+)\b(.*)$", line)
        if heading:
            current_page = f"P{int(heading.group(1)):02d}"
            pages[current_page] = {
                "title": heading.group(2).strip(),
                "raw_lines": [],
                "sections": {},
                "visual_constraints": {},
            }
            current_section = ""
            in_global_defaults = False
            continue
        if re.match(r"^##\s+global_design_defaults\s*$", line, re.IGNORECASE):
            in_global_defaults = True
            current_page = None
            current_section = ""
            continue
        if line.startswith("## "):
            in_global_defaults = False
            current_page = None
            current_section = ""
            continue
        if line.startswith("### "):
            current_section = line[4:].strip()
            if current_page:
                pages[current_page]["sections"].setdefault(current_section, [])
            continue
        if in_global_defaults and line.strip():
            global_lines.append(line.strip())
        if current_page and line.strip():
            pages[current_page]["raw_lines"].append(line.strip())
            if current_section:
                pages[current_page]["sections"].setdefault(current_section, []).append(line.strip())
            constraint = re.match(r"^-\s+`([^`]+)`：\s*(.+)$", line.strip())
            if constraint and constraint.group(1) in DESIGN_KEYS:
                pages[current_page]["visual_constraints"][constraint.group(1)] = constraint.group(2).strip()

    return global_lines, pages


def resolve_input(input_path: str) -> tuple[Path, Path | None]:
    source = Path(input_path)
    if source.is_dir():
        return source / "deck_spec.json", source / "page_design.md"
    page_design = source.parent / "page_design.md"
    return source, page_design if page_design.is_file() else None


def right_insight_width(page: dict[str, Any], design: dict[str, Any]) -> str:
    searchable = " ".join(
        [
            str(page.get("visual_notes", "")),
            " ".join(design.get("raw_lines", [])),
        ]
    )
    match = re.search(r"右侧\s*(\d{1,2}%)(?:\s*[~～-]\s*(\d{1,2}%))?", searchable)
    if match:
        return f"{match.group(1)}-{match.group(2)}" if match.group(2) else match.group(1)
    return "inherit visual_rules.md or page-level override; use fallback only when absent"


def resolve_type(page: dict[str, Any], primary_chart_type: str) -> tuple[str, str]:
    if page.get("type"):
        return str(page["type"]), "type"
    if page.get("page_type"):
        return str(page["page_type"]), "page_type_legacy"
    return CHART_TYPE_TO_PAGE_TYPE.get(primary_chart_type, "executive_summary"), "chart_type_inference"


def build_component_plan(component: dict[str, Any]) -> dict[str, Any]:
    chart_data = component.get("chart_data")
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    mapping = component.get("chart_semantic_mapping")
    mapping = mapping if isinstance(mapping, dict) else {}
    structured_labels = extract_structured_visible_content(chart_data)
    required_evidence = [str(item) for item in as_list(component.get("required_evidence"))]
    visible_labels = unique(
        structured_labels
        + [str(item) for item in as_list(component.get("display_text"))]
    )
    boundary = [str(item) for item in as_list(component.get("chart_visual_boundary"))]
    forbidden = unique(
        boundary + [str(item) for item in as_list(mapping.get("forbidden_visualization"))]
    )
    return {
        "component_id": component["component_id"],
        "component_role": component["component_role"],
        "component_region": component["component_region"],
        "supports_component_id": component.get("supports_component_id"),
        "chart_type": component["chart_type"],
        "chart_proof_goal": component["chart_proof_goal"],
        "chart_data": chart_data,
        "visible_labels": visible_labels,
        "semantic_constraints": {
            "main_visual_logic": mapping.get("main_visual_logic", ""),
            "stage_or_node_meaning": mapping.get("stage_or_node_meaning", []),
            "forbidden_visualization": forbidden,
            "correspondence_pairs": mapping.get("correspondence_pairs", []),
            "edge_roles": mapping.get("edge_roles", {}),
        },
        "component_coverage": {
            "structured_label_count": len(structured_labels),
            "required_evidence": required_evidence,
            "missing_required_evidence": [
                item for item in required_evidence if item not in visible_labels
            ],
        },
    }


def bottom_bar_enabled(value: object) -> bool:
    text = str(value or "").strip().lower()
    if not text:
        return False
    disabled_tokens = ("disabled", "disable", "off", "none", "不启用", "不使用", "禁用", "取消", "无")
    return not any(token in text for token in disabled_tokens)


def build_contract(
    page: dict[str, Any],
    global_defaults: dict[str, Any] | None = None,
    page_design_globals: list[str] | None = None,
    design: dict[str, Any] | None = None,
    recomposition_mode: str = "adaptive_recomposition",
) -> dict[str, Any]:
    if recomposition_mode not in RECOMPOSITION_MODES:
        raise ValueError(f"unsupported recomposition_mode: {recomposition_mode!r}")
    chart_contract_source, normalized_components = normalize_chart_contract(page)
    primary_candidates = [
        component for component in normalized_components
        if component.get("component_role") == "primary"
    ]
    if len(primary_candidates) != 1:
        raise ValueError("normalized chart contract requires exactly one primary component")
    primary = primary_candidates[0]
    component_plans = [build_component_plan(component) for component in normalized_components]
    missing_component_evidence = [
        f"{component['component_id']}:{item}"
        for component in component_plans
        for item in component["component_coverage"]["missing_required_evidence"]
    ]
    if missing_component_evidence:
        raise ValueError(
            "component required evidence is missing from visible chart data: "
            + ", ".join(missing_component_evidence)
        )
    mapping = primary.get("chart_semantic_mapping") or {}
    design = design or {}
    design_constraints = design.get("visual_constraints", {})
    boundary = as_list(primary.get("chart_visual_boundary"))
    forbidden = unique(
        [str(item) for item in boundary]
        + [str(item) for item in as_list(mapping.get("forbidden_visualization"))]
    )
    chart_data = primary.get("chart_data", {})
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    structured_labels = extract_structured_visible_content(chart_data)
    component_labels = [
        str(label)
        for component in component_plans
        for label in component["visible_labels"]
    ]
    labels = component_labels + [str(item) for item in as_list(page.get("display_text"))]
    required_evidence = [
        str(item)
        for component in component_plans
        for item in component["component_coverage"]["required_evidence"]
    ]
    visible_labels = unique(labels + required_evidence)
    primary_chart_type = str(primary["chart_type"])
    page_type, type_source = resolve_type(page, primary_chart_type)
    bottom_bar_rule = design_constraints.get("bottom_bar_rule", page.get("bottom_bar_rule", ""))
    if any(component.get("component_region") == "bottom" for component in normalized_components) and bottom_bar_enabled(bottom_bar_rule):
        raise ValueError("component_region='bottom' conflicts with enabled bottom_bar_rule")

    source_visual_plan = {
        "layout_pattern": page["layout_pattern"],
        "chart_components": copy.deepcopy(component_plans),
        "visible_title": page["title"],
        "visible_conclusion": page["conclusion"],
    }
    effective_visual_plan = copy.deepcopy(source_visual_plan)
    evidence_required = len(required_evidence)
    recomposition_audit = {
        "trigger_reasons": [],
        "layout_changed": False,
        "chart_type_changed": False,
        "component_region_changed": False,
        "copy_adjustments": [],
        "semantic_invariants": {
            "core_judgement_preserved": True,
            "chart_proof_goals_preserved": True,
            "facts_preserved": True,
            "relations_preserved": True,
        },
        "evidence_coverage": {
            "required": evidence_required,
            "covered": evidence_required,
            "missing": [],
        },
        "compatibility_checks": {
            "layout_region": "PASS",
            "chart_target_schema": "NOT_CHANGED",
            "chart_transform": "NOT_CHANGED",
        },
        "quality_delta": {
            "baseline_score": None,
            "effective_score": None,
        },
        "return_to_A_required": False,
    }

    return {
        "page_id": normalized_page_id(page),
        "recomposition_mode": recomposition_mode,
        "source_contract": {
            "title": page["title"],
            "conclusion": page["conclusion"],
            "section": page.get("section", ""),
            "core_judgement": page["core_judgement"],
            "chart_proof_goal": primary["chart_proof_goal"],
        },
        "source_design": {
            "global_design_defaults": global_defaults or {},
            "page_design_global_defaults": page_design_globals or [],
            "page_design_override": design.get("raw_lines", []),
            "page_design_sections": design.get("sections", {}),
        },
        "source_visual_plan": source_visual_plan,
        "effective_visual_plan": effective_visual_plan,
        "recomposition_audit": recomposition_audit,
        "render_intent": {
            "layout_pattern": effective_visual_plan["layout_pattern"],
            "chart_type": primary_chart_type,
            "chart_contract_source": chart_contract_source,
            "chart_components": component_plans,
            "type": page_type,
            "type_source": type_source,
            "main_visual_goal": mapping.get("main_visual_logic", primary["chart_proof_goal"]),
            "visual_notes": page.get("visual_notes", ""),
            "visual_focus": as_list(page.get("visual_focus")),
            "must_highlight": as_list(page.get("must_highlight")),
            "text_density": page.get("text_density", ""),
            "density_budget": build_density_budget(page),
            "need_compression": bool(page.get("need_compression", False)),
            "data_gaps": as_list(page.get("data_gaps")),
        },
        "visible_text_plan": {
            "title": effective_visual_plan["visible_title"],
            "conclusion": effective_visual_plan["visible_conclusion"],
            "main_labels": visible_labels,
            "insight_panel": as_list(mapping.get("insight_panel_logic")),
            "bottom_conclusion": page.get("bottom_conclusion", ""),
        },
        "visible_content_coverage": {
            "structured_label_count": len(structured_labels),
            "display_text_count": len(as_list(page.get("display_text"))),
            "required_evidence": required_evidence,
            "missing_required_evidence": [
                item for item in required_evidence if item not in visible_labels
            ],
            "component_coverage": [
                {
                    "component_id": component["component_id"],
                    **component["component_coverage"],
                }
                for component in component_plans
            ],
        },
        "semantic_constraints": {
            "main_visual_logic": mapping.get("main_visual_logic", ""),
            "stage_or_node_meaning": mapping.get("stage_or_node_meaning", []),
            "forbidden_visualization": forbidden,
            "correspondence_pairs": mapping.get("correspondence_pairs", []),
            "edge_roles": mapping.get("edge_roles", {}),
        },
        "visual_constraints": {
            "red_anchor": design_constraints.get(
                "red_anchor", "one primary red anchor; ordinary-page red area stays low"
            ),
            "card_hierarchy": design_constraints.get("card_hierarchy", ""),
            "spacing_rule": design_constraints.get("spacing_rule", ""),
            "bottom_bar_rule": bottom_bar_rule,
            "visual_simplification": design_constraints.get("visual_simplification", ""),
            "visual_boundary": design_constraints.get("visual_boundary", ""),
            "page_type_gate": design_constraints.get("page_type_gate", ""),
            "right_insight_width": right_insight_width(page, design),
            "footer": (global_defaults or {}).get("footer", "low-emphasis unified footer"),
            "safe_area": "left/right >=4%; top/bottom >=3%",
        },
        "fail_conditions": unique(
            forbidden
            + [
                "logic-only field rendered visibly",
                "main visual does not prove chart_proof_goal",
                "layout_pattern and chart_type are mixed",
                "component_region is incompatible with layout_pattern",
                "supporting component is rendered inside insight_panel",
                "primary projection differs from the normalized primary component",
                "correspondence_pairs or edge_roles lose their intended relationship",
            ]
        ),
    }


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Compile page render contracts from Role A design.")
    parser.add_argument("input_path", help="Path to input directory or deck_spec.json.")
    parser.add_argument("output_dir", help="Path to output directory for compiled contracts.")
    parser.add_argument("--legacy", action="store_true", help="Bypass strict type enum check for legacy files.")
    parser.add_argument(
        "--recomposition-mode",
        choices=sorted(RECOMPOSITION_MODES),
        default="adaptive_recomposition",
        help="Initialize strict fidelity or adaptive recomposition render contracts.",
    )
    args = parser.parse_args()

    deck_path, page_design_path = resolve_input(args.input_path)
    output = Path(args.output_dir)
    input_dir = deck_path.parent
    _, _, warnings, errors = validate_root(str(input_dir), allow_legacy_types=args.legacy)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for message in errors:
            print(f"ERROR: {message}")
        print("BLOCKED: render contract compilation refused; return_to_A_required=true")
        return 1
    try:
        deck = json.loads(deck_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read deck spec: {exc}")
        return 1

    pages = (deck.get("pages") or deck.get("slides")) if isinstance(deck, dict) else None
    if not isinstance(pages, list) or not pages:
        print("ERROR: deck_spec.json must contain a non-empty pages or slides array")
        return 1

    page_design_globals: list[str] = []
    page_design_pages: dict[str, dict[str, Any]] = {}
    if page_design_path and page_design_path.is_file():
        page_design_globals, page_design_pages = parse_page_design(
            page_design_path.read_text(encoding="utf-8")
        )

    output.mkdir(parents=True, exist_ok=True)
    index: list[str] = []
    for page in pages:
        try:
            page_id = normalized_page_id(page)
            contract = build_contract(
                page,
                global_defaults=deck.get("global_design_defaults", {}),
                page_design_globals=page_design_globals,
                design=page_design_pages.get(page_id, {}),
                recomposition_mode=args.recomposition_mode,
            )
            recomposition_errors, _ = validate_recomposition_contract(contract)
            if recomposition_errors:
                raise ValueError("; ".join(recomposition_errors))
        except (KeyError, ValueError) as exc:
            label = exc.args[0] if exc.args else str(exc)
            print(f"ERROR: render contract compilation failed: {label}")
            return 1
        filename = f"{contract['page_id']}_render_contract.json"
        (output / filename).write_text(
            json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        index.append(filename)

    (output / "index.json").write_text(
        json.dumps(
            {"recomposition_mode": args.recomposition_mode, "contracts": index},
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(f"OK: compiled {len(index)} render contract(s) into {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
