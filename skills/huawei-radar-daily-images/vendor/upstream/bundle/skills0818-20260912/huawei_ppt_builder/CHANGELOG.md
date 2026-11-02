# CHANGELOG

README 中的版本变更详情统一收口到本文件；README 只描述当前能力与使用方式。

## v1.6.0-adaptive-recomposition — 2026-06-20

1. 新增 C1.5 语义保真视觉重构阶段，默认 adaptive，支持 strict fidelity。
2. Render contract 新增 `source_visual_plan`、`effective_visual_plan`、`recomposition_audit`。
3. 在保持核心判断、事实、证据、证明目标和关系语义的前提下，条件允许优化上屏文案、layout、region 和 chart type。
4. 新增 `validate_recomposition.py` 与 28 项回归；C3 改为审计语义不变量、授权差异和质量增量。

## v1.5.0-chart-components — 2026-06-19

1. 新增 `chart_components` 单源合同、一个 primary 与最多三个 supporting、版式区域兼容和逐组件 coverage。
2. 历史顶层主图字段只在无组件合同时兼容读取，主图投影由 primary 派生。
3. 右侧洞察栏不再允许承载独立图表组件。

## v1.4.0-density-preservation — 2026-06-02

### 升级目标

在角色 C 语义合同基线之上，补齐华为视觉强制精修、合同编译、输入校验、密度保真、客观自检和交付阻断能力，避免页面在施工或精修中丢失语义、证据和信息密度。

### 新增

1. 强制 `C2.5` 华为视觉精修阶段，以及页型精修矩阵、精修报告和负面风格门禁。
2. 渲染合同编译、输入校验、精修校验、评分、打包与 A→C 合同回归脚本。
3. `chart_type`、`layout_pattern`、`type` 和 `edge_roles` 的确定性合同校验。
4. 目录级渲染合同编译，继承角色 A 全局默认、页面级 overrides 和逐页视觉意图。
5. C0 fail-closed 行为：必要输入、schema、枚举或关键字段错误时阻断生成并返回 A。
6. 表格、卡片、路线图、风险和决策等结构化可见内容 coverage。
7. `density_budget`、`required_evidence` 和高密度页面保真规则。
8. L 型红线、contact sheet 重复骨架、高密度 underfill 和右侧空壳等客观 C3 门禁。

### 修改

1. 默认模式保持 `page_images`，仅当用户明确要求时启用 `pptx`。
2. 交付阈值统一为 `>=92`，同时要求无一票失败项。
3. 角色 C Skill 入口统一为 `huawei-ppt-builder`。
4. 角色 A 输入的 `visual_rules.md` 作为视觉单一事实源，角色 C 只保留最小 fallback。
5. `ROLE_C_SKILL_FULL_CONTENT.md` 调整为轻量索引。

### 修复

1. `edge_roles` 统一为以关系角色为键的对象结构。
2. 页型映射统一为优先读取角色 A 的 `type`，兼容历史 `page_type`，缺失时再按 `chart_type` 保守推断；新合同输出 `type` 与 `type_source`。
3. 渲染合同编译前再次执行 C0，避免绕过输入阻断门禁。

### 边界

1. 角色 C 不新增事实、不改变已确认结论，不把渲染合同升级为新的事实源。
2. 视觉精修不得删除 `required_evidence`、关键行列、图表节点、图注或来源。
3. 页面内容无法在不删除必需证据的情况下实现时，必须返回角色 A。
