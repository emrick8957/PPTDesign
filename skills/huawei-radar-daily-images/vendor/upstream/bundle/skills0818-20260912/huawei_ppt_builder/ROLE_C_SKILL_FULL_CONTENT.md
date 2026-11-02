# Role C Skill Content Index

本文件只提供索引。按任务需要读取对应文件，避免一次性加载全部内容。

## 入口

- `SKILL.md`：角色边界、核心不变量和完整执行流程
- `VERSION.md`：版本说明

## 视觉执行

- `libraries/c2_5_execution_policy.md`：C2.5 精修执行边界与密度保真
- `libraries/huawei_visual_refinement_rules.md`：deprecated 兼容跳转
- `libraries/page_visual_refinement_matrix.md`：按页型选择精修动作
- `policies/huawei_visual_gate.md`：缺少 A 输入视觉规则时的最小 fallback

## 语义门禁

- `policies/chart_semantic_mapping_policy.md`
- `policies/relationship_roles_policy.md`
- `policies/field_visibility_policy.md`
- `policies/content_boundary_policy.md`

## 工作流

- `workflows/page_images_workflow.md`
- `workflows/self_check_workflow.md`
- `workflows/optimization_workflow.md`
- `workflows/pptx_workflow.md`
- `workflows/A_B_C_handoff_protocol.md`

## 工具

- `tools/validate_inputs.py`
- `tools/render_contract_builder.py`
- `tools/score_self_check.py`
- `tools/validate_refinement.py`
- `tools/pack_delivery.py`
- `tools/run_contract_regression.py`
