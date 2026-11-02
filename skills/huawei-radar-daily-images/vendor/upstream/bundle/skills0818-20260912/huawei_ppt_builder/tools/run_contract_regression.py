#!/usr/bin/env python3
"""Exercise the Role A to Role C contract boundary with bundled fixtures."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
FIXTURE = ROOT / "examples" / "regression" / "a_latest_delivery_snapshot"
MINIMAL = ROOT / "examples" / "deck_spec_minimal_example.json"
SELF_CHECK_EXAMPLE = ROOT / "examples" / "self_check_example.md"


def run(command: list[str], expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    output = (result.stdout + result.stderr).strip()
    if expect_success and result.returncode != 0:
        raise AssertionError(f"command failed: {' '.join(command)}\n{output}")
    if not expect_success and result.returncode == 0:
        raise AssertionError(f"command unexpectedly passed: {' '.join(command)}")
    return result


def validate(input_dir: Path, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(TOOLS / "validate_inputs.py"), str(input_dir)], expect_success)


def prepare_case(source: Path, target: Path) -> None:
    shutil.copytree(source, target)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="huawei-ppt-builder-regression-") as temp_dir:
        temp = Path(temp_dir)

        validate(FIXTURE)
        contracts = temp / "contracts"
        run(
            [
                sys.executable,
                str(TOOLS / "render_contract_builder.py"),
                str(FIXTURE),
                str(contracts),
            ]
        )
        contract = json.loads((contracts / "P01_render_contract.json").read_text(encoding="utf-8"))
        assert contract["render_intent"]["type"] == "architecture"
        assert contract["recomposition_mode"] == "adaptive_recomposition"
        assert contract["source_visual_plan"] == contract["effective_visual_plan"]
        assert contract["recomposition_audit"]["layout_changed"] is False
        assert contract["render_intent"]["type_source"] == "type"
        assert isinstance(contract["semantic_constraints"]["edge_roles"], dict)
        assert contract["visible_text_plan"]["bottom_conclusion"] == ""
        assert contract["visible_text_plan"]["insight_panel"]
        assert contract["render_intent"]["visual_focus"] == [
            "五类架构指导",
            "三条数字化主链",
            "五站纵向映射",
            "数字主线平台",
        ]
        assert contract["visual_constraints"]["right_insight_width"] == "8%"
        assert "单页仅 1 个红色主锚点" in contract["visual_constraints"]["red_anchor"]
        assert any(
            "数字主线平台" in line
            for line in contract["source_design"]["page_design_override"]
        )
        assert contract["visual_constraints"]["page_type_gate"]
        assert contract["source_design"]["global_design_defaults"]
        assert contract["source_design"]["page_design_override"]

        minimal_case = temp / "minimal"
        prepare_case(FIXTURE, minimal_case)
        shutil.copy2(MINIMAL, minimal_case / "deck_spec.json")
        validate(minimal_case)
        minimal_contracts = temp / "minimal-contracts"
        run(
            [
                sys.executable,
                str(TOOLS / "render_contract_builder.py"),
                str(minimal_case),
                str(minimal_contracts),
            ]
        )
        minimal_contract = json.loads(
            (minimal_contracts / "P01_render_contract.json").read_text(encoding="utf-8")
        )
        assert minimal_contract["render_intent"]["type"] == "executive_summary"
        assert minimal_contract["render_intent"]["type_source"] == "type"
        assert minimal_contract["render_intent"]["chart_contract_source"] == "chart_components"
        assert minimal_contract["visible_text_plan"]["title"] == minimal_contract["effective_visual_plan"]["visible_title"]
        assert minimal_contract["visible_text_plan"]["conclusion"] == minimal_contract["effective_visual_plan"]["visible_conclusion"]
        assert minimal_contract["render_intent"]["chart_type"] == "key_findings_cards"
        assert len(minimal_contract["render_intent"]["chart_components"]) == 2
        assert minimal_contract["render_intent"]["chart_components"][1]["supports_component_id"] == "C1"
        assert len(minimal_contract["visible_content_coverage"]["component_coverage"]) == 2

        mixed_contract_case = temp / "mixed-contract"
        prepare_case(FIXTURE, mixed_contract_case)
        shutil.copy2(MINIMAL, mixed_contract_case / "deck_spec.json")
        mixed_contract = json.loads(
            (mixed_contract_case / "deck_spec.json").read_text(encoding="utf-8")
        )
        mixed_contract["pages"][0]["chart_type"] = "key_findings_cards"
        (mixed_contract_case / "deck_spec.json").write_text(
            json.dumps(mixed_contract, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        validate(mixed_contract_case, expect_success=False)

        invalid_region_case = temp / "invalid-component-region"
        prepare_case(FIXTURE, invalid_region_case)
        shutil.copy2(MINIMAL, invalid_region_case / "deck_spec.json")
        invalid_region = json.loads(
            (invalid_region_case / "deck_spec.json").read_text(encoding="utf-8")
        )
        invalid_region["pages"][0]["chart_components"][1]["component_region"] = "insight_panel"
        (invalid_region_case / "deck_spec.json").write_text(
            json.dumps(invalid_region, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        validate(invalid_region_case, expect_success=False)

        incompatible_region_case = temp / "incompatible-component-region"
        prepare_case(FIXTURE, incompatible_region_case)
        shutil.copy2(MINIMAL, incompatible_region_case / "deck_spec.json")
        incompatible_region = json.loads(
            (incompatible_region_case / "deck_spec.json").read_text(encoding="utf-8")
        )
        incompatible_region["pages"][0]["layout_pattern"] = "four_quadrant_judgement"
        incompatible_region["pages"][0]["chart_components"][1]["component_region"] = "right"
        (incompatible_region_case / "deck_spec.json").write_text(
            json.dumps(incompatible_region, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        validate(incompatible_region_case, expect_success=False)

        inferred_type_case = temp / "inferred-type"
        prepare_case(FIXTURE, inferred_type_case)
        inferred_type = json.loads(
            (inferred_type_case / "deck_spec.json").read_text(encoding="utf-8")
        )
        inferred_type["slides"][0].pop("type")
        (inferred_type_case / "deck_spec.json").write_text(
            json.dumps(inferred_type, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        validate(inferred_type_case)
        inferred_contracts = temp / "inferred-contracts"
        run(
            [
                sys.executable,
                str(TOOLS / "render_contract_builder.py"),
                str(inferred_type_case),
                str(inferred_contracts),
            ]
        )
        inferred_contract = json.loads(
            (inferred_contracts / "P01_render_contract.json").read_text(encoding="utf-8")
        )
        assert inferred_contract["render_intent"]["type"] == "architecture"
        assert inferred_contract["render_intent"]["type_source"] == "chart_type_inference"

        structured_case = temp / "structured-visible-content"
        prepare_case(FIXTURE, structured_case)
        structured = json.loads((structured_case / "deck_spec.json").read_text(encoding="utf-8"))
        structured["slides"][0]["chart_data"]["cards"] = [
            {
                "title": "工程闭环",
                "description": "保留卡片说明",
                "items": ["数据绑定", "模型回写"],
                "metrics": ["五站贯通"],
            }
        ]
        structured["slides"][0]["chart_data"]["table"] = {
            "columns": ["维度", "现状", "目标"],
            "rows": [["数据", "孤立", "可追溯"]],
            "notes": ["表格注释必须保留"],
        }
        structured["slides"][0]["required_evidence"] = ["工程闭环", "表格注释必须保留"]
        (structured_case / "deck_spec.json").write_text(
            json.dumps(structured, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        validate(structured_case)
        structured_contracts = temp / "structured-contracts"
        run(
            [
                sys.executable,
                str(TOOLS / "render_contract_builder.py"),
                str(structured_case),
                str(structured_contracts),
            ]
        )
        structured_contract = json.loads(
            (structured_contracts / "P01_render_contract.json").read_text(encoding="utf-8")
        )
        structured_labels = structured_contract["visible_text_plan"]["main_labels"]
        for expected in (
            "工程闭环",
            "保留卡片说明",
            "数据绑定",
            "模型回写",
            "维度",
            "现状",
            "目标",
            "数据",
            "孤立",
            "可追溯",
            "表格注释必须保留",
        ):
            assert expected in structured_labels, expected
        assert structured_contract["visible_content_coverage"]["missing_required_evidence"] == []
        assert (
            structured_contract["render_intent"]["density_budget"]["density_profile"]
            == "technical_deep_dive"
        )

        invalid_chart_case = temp / "invalid-chart"
        prepare_case(FIXTURE, invalid_chart_case)
        invalid_chart = json.loads((invalid_chart_case / "deck_spec.json").read_text(encoding="utf-8"))
        invalid_chart["slides"][0]["chart_type"] = "stack_architecture_with_right_insights"
        (invalid_chart_case / "deck_spec.json").write_text(
            json.dumps(invalid_chart, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        validate(invalid_chart_case, expect_success=False)

        invalid_edge_case = temp / "invalid-edge"
        prepare_case(FIXTURE, invalid_edge_case)
        invalid_edge = json.loads((invalid_edge_case / "deck_spec.json").read_text(encoding="utf-8"))
        invalid_edge["slides"][0]["chart_semantic_mapping"]["edge_roles"]["flow_integrate"].append(
            {"from": "P5", "to": "SHADOW"}
        )
        (invalid_edge_case / "deck_spec.json").write_text(
            json.dumps(invalid_edge, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        validate(invalid_edge_case, expect_success=False)
        invalid_contracts = temp / "invalid-contracts"
        run(
            [
                sys.executable,
                str(TOOLS / "render_contract_builder.py"),
                str(invalid_edge_case),
                str(invalid_contracts),
            ],
            expect_success=False,
        )
        assert not invalid_contracts.exists()

        fallback_case = temp / "fallback-visual-rules"
        prepare_case(FIXTURE, fallback_case)
        (fallback_case / "visual_rules.md").unlink()
        fallback_validation = validate(fallback_case)
        assert "missing optional file: visual_rules.md" in fallback_validation.stdout

        run([sys.executable, str(TOOLS / "validate_refinement.py"), str(SELF_CHECK_EXAMPLE)])
        incomplete_report = temp / "incomplete-self-check.md"
        incomplete_report.write_text(
            "# P01\n\n- 总分：95\n- 是否触发一票失败项：否\n",
            encoding="utf-8",
        )
        run(
            [sys.executable, str(TOOLS / "validate_refinement.py"), str(incomplete_report)],
            expect_success=False,
        )

    print("OK: Role A to Role C contract regression passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
