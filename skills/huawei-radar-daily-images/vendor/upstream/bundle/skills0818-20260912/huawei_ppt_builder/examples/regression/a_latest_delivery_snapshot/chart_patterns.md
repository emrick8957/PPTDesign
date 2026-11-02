# 通用图表模式库

> 文件定位：本文件只定义 `deck_spec.json` 中 `chart_type` 字段的可选值、使用场景、数据结构和图表表达规则。  
> 注意：本文件不定义页面整体排版。页面整体排版由 `visual_patterns/layout_library.md` 中的 `layout_pattern` 定义。

---

## 0. chart_type 与 layout_pattern 的边界

### 0.1 字段职责

| 字段 | 来源文件 | 解决的问题 | 示例 |
|---|---|---|---|
| `layout_pattern` | `visual_patterns/layout_library.md` | 这一页怎么排版：标题区、主体区、图表区、文字区、洞察区如何组织 | `executive_summary_dashboard`、`two_column_comparison`、`layered_architecture`、`roadmap_timeline` |
| `chart_type` | `templates/chart_patterns.md` | 这一页用什么主图表表达信息：对比、趋势、架构、风险、决策、闭环等 | `quadrant_matrix`、`comparison_table`、`layered_stack_diagram`、`risk_matrix`、`decision_table` |

### 0.2 简单判断法

- 如果回答的是 **“页面结构怎么摆”**，属于 `layout_pattern`。
- 如果回答的是 **“图表本身表达什么关系”**，属于 `chart_type`。
- 如果一个名称描述的是“左中右、上下、卡片区、右侧洞察栏”等页面布局，放入 `layout_library`。
- 如果一个名称描述的是“矩阵、热力图、时间轴、架构图、关系图、决策表”等信息表达方式，放入 `chart_patterns`。

### 0.3 禁止混用

以下名称属于 `layout_pattern`，不得作为 `chart_type` 使用：

- `executive_summary_dashboard`
- `two_column_comparison`
- `four_quadrant_judgement`
- `three_column_cards`
- `layered_architecture`
- `stack_architecture_with_right_insights`
- `roadmap_timeline`
- `trend_curve_with_strategy`
- `ecosystem_map`
- `insight_panel_with_chart`
- `risk_decision_matrix`

以下名称属于 `chart_type`，不得作为 `layout_pattern` 使用：

- `key_findings_cards`
- `quadrant_matrix`
- `comparison_table`
- `capability_radar`
- `capability_map`
- `layered_stack_diagram`
- `architecture_flow_diagram`
- `roadmap_timeline_chart`
- `trend_curve`
- `ecosystem_relationship_map`
- `gap_heatmap`
- `risk_matrix`
- `decision_table`
- `value_chain_loop`
- `swimlane_process`
- `priority_matrix`


### 0.4 chart_data 字段可见性边界

`chart_data` 字段规则与可见性约定见 `core/deck_spec_field_dictionary.md` 的“chart_data 字段通则与可见性约定”。

原则：

- `chart_data` 承载拓扑和可见内容；
- `group`、`emphasis`、`source_status` 等 logic-only 字段不得字面上屏；
- `edges.label` 可作为短动作词上屏，但复杂方向、对应、层级、闭环语义必须写入 `chart_semantic_mapping`；
- 不得在 `chart_data` 内发明 `relation_type` 等关系字段。

表达"同层对应/双分支/闭环"时（如 V 模型），同层对应用 `correspondence_pairs`、方向性边用 `edge_roles`（边引用为结构化 `{from,to}`），均见 `core/deck_spec_field_dictionary.md` §4.7，写入 `chart_semantic_mapping`；不得在 edges 内发明关系字段，也不得在 `edge_roles` 内重复声明 `same_level_correspondence`。

---

## 1. chart_type 总表

| chart_type | 中文名称 | 适用场景 | 典型搭配 layout_pattern |
|---|---|---|---|
| `none` | 无主图表 | 封面、目录、纯结论页、Thank you 页 | 任意 |
| `key_findings_cards` | 关键结论卡片组 | 总览页、核心判断页 | `executive_summary_dashboard`、`three_column_cards` |
| `quadrant_matrix` | 四象限判断矩阵 | 领先/差距/风险/建议，价值/难度判断 | `four_quadrant_judgement`、`executive_summary_dashboard` |
| `comparison_table` | 多维对比表 | 竞品对比、方案对比、现状/目标对比 | `two_column_comparison`、`insight_panel_with_chart` |
| `capability_radar` | 能力雷达图 | 多维能力成熟度、竞争力对比 | `insight_panel_with_chart` |
| `capability_map` | 能力地图 | 能力域、现状、目标、补齐动作 | `executive_summary_dashboard`、`insight_panel_with_chart` |
| `layered_stack_diagram` | 分层堆栈图 | 技术架构、平台能力、体系分层 | `layered_architecture`、`stack_architecture_with_right_insights` |
| `architecture_flow_diagram` | 架构流转图 | 数据流、业务流、模型流、系统交互 | `stack_architecture_with_right_insights` |
| `roadmap_timeline_chart` | 路线图时间轴 | 三阶段路径、年度规划、产品演进 | `roadmap_timeline` |
| `trend_curve` | 趋势曲线图 | 产业趋势、增长趋势、技术演进 | `trend_curve_with_strategy` |
| `ecosystem_relationship_map` | 生态关系图 | 产业生态、伙伴体系、平台生态 | `ecosystem_map` |
| `gap_heatmap` | 差距热力图 | 短板、优先级、补齐难度 | `insight_panel_with_chart`、`risk_decision_matrix` |
| `risk_matrix` | 风险矩阵 | 风险概率、影响、应对措施 | `risk_decision_matrix` |
| `decision_table` | 决策清单表 | 高层拍板事项、资源申请、行动闭环 | `risk_decision_matrix` |
| `value_chain_loop` | 价值闭环图 | 输入、处理、输出、反馈、优化 | `ecosystem_map`、`stack_architecture_with_right_insights` |
| `swimlane_process` | 泳道流程图 | 跨部门流程、角色协同、阶段交付 | `roadmap_timeline`、`stack_architecture_with_right_insights` |
| `priority_matrix` | 优先级矩阵 | 场景优先级、项目排序、投入判断 | `four_quadrant_judgement` |
| `metric_showcase_grid` | 指标展示网格 | 成果、规模、覆盖、增长、案例背书 | `metric_case_showcase_grid`、`executive_summary_dashboard` |
| `case_gallery_cards` | 案例图卡组 | 行业案例、客户样板、产品截图、生态伙伴展示 | `metric_case_showcase_grid`、`left_logic_right_proof` |
| `hub_spoke_relationship_map` | 中心辐射关系图 | 平台—伙伴—场景、中心能力—周边角色关系 | `hub_spoke_ecosystem_canvas`、`ecosystem_map` |

---

## 2. chart_type 详细定义

### 2.1 `none`

**中文名称**：无主图表  
**用途**：用于封面、目录、章节页、Thank you 页，或用户明确要求纯文字页时。  
**推荐数据结构**：

```json
{
  "chart_type": "none",
  "chart_data": {}
}
```

**使用规则**：

- 允许没有主图表；
- 但仍应通过 `layout_pattern` 定义页面结构；
- 若页面包含装饰性小图标，不应因此设置 chart_type。

---

### 2.2 `key_findings_cards`

**中文名称**：关键结论卡片组  
**用途**：用于高层总览页，把 3~5 个关键判断做成卡片。  
**适合表达**：核心判断、关键数字、主要矛盾、机会点、风险提示、行动建议。  
**不适合表达**：复杂流程、多层技术架构、大量数据明细。

**推荐数据结构**：

```json
{
  "chart_type": "key_findings_cards",
  "chart_data": {
    "cards": [
      {
        "label": "判断一",
        "headline": "核心判断",
        "description": "简短说明",
        "emphasis": "high"
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `executive_summary_dashboard`
- `three_column_cards`

---

### 2.3 `quadrant_matrix`

**中文名称**：四象限判断矩阵  
**用途**：用于表达两组维度交叉下的判断。  
**适合表达**：领先/差距/风险/建议、价值/难度、成熟度/优先级、影响/紧急度。

**推荐数据结构**：

```json
{
  "chart_type": "quadrant_matrix",
  "chart_data": {
    "x_axis": "价值",
    "y_axis": "难度",
    "quadrants": [
      {
        "name": "高价值低难度",
        "items": ["优先推进事项"]
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `four_quadrant_judgement`
- `executive_summary_dashboard`

---

### 2.4 `comparison_table`

**中文名称**：多维对比表  
**用途**：用于对象 A/B、现状/目标、方案 1/方案 2 的多维度对比。  
**适合表达**：竞品对比、能力对比、方案取舍、当前状态与目标状态对比。

**推荐数据结构**：

```json
{
  "chart_type": "comparison_table",
  "chart_data": {
    "columns": ["维度", "对象A", "对象B", "判断"],
    "rows": [
      ["生态", "成熟", "建设中", "对象A领先"]
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `two_column_comparison`
- `insight_panel_with_chart`

---

### 2.5 `capability_radar`

**中文名称**：能力雷达图  
**用途**：用于多维能力成熟度、竞争力、能力短板的直观比较。  
**适合表达**：多维能力打分、竞争力对比、能力成熟度、当前能力与目标能力差距。

**推荐数据结构**：

```json
{
  "chart_type": "capability_radar",
  "chart_data": {
    "dimensions": ["性能", "生态", "成本", "安全", "交付"],
    "series": [
      {
        "name": "对象A",
        "values": [4, 5, 3, 4, 5]
      },
      {
        "name": "对象B",
        "values": [3, 3, 4, 5, 3]
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `insight_panel_with_chart`

---

### 2.6 `capability_map`

**中文名称**：能力地图  
**用途**：用于展示能力域、当前状态、目标状态、补齐动作。  
**适合表达**：平台能力清单、能力成熟度、能力补齐路线、能力与业务场景映射。

**推荐数据结构**：

```json
{
  "chart_type": "capability_map",
  "chart_data": {
    "domains": [
      {
        "name": "能力域",
        "current_state": "当前状态",
        "target_state": "目标状态",
        "actions": ["补齐动作"]
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `executive_summary_dashboard`
- `insight_panel_with_chart`

---

### 2.7 `layered_stack_diagram`

**中文名称**：分层堆栈图  
**用途**：用于展示技术平台、数据治理、AI 平台、安全运营、系统架构的层次关系。  
**适合表达**：基础设施层、平台层、能力层、应用层、运营层。

**推荐数据结构**：

```json
{
  "chart_type": "layered_stack_diagram",
  "chart_data": {
    "layers": [
      {
        "name": "基础设施层",
        "items": ["资源池", "网络", "存储"]
      },
      {
        "name": "平台层",
        "items": ["调度", "治理", "监控"]
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `layered_architecture`
- `stack_architecture_with_right_insights`

---

### 2.8 `architecture_flow_diagram`

**中文名称**：架构流转图  
**用途**：用于表达系统、数据、模型、业务之间的流转关系。  
**适合表达**：数据流、业务流、模型训练/推理链路、系统集成关系、云边端协同链路。

**推荐数据结构**：

```json
{
  "chart_type": "architecture_flow_diagram",
  "chart_data": {
    "nodes": [
      {"id": "A", "label": "数据源", "group": "输入"}
    ],
    "edges": [
      {"from": "A", "to": "B", "label": "汇聚"}
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `stack_architecture_with_right_insights`
- `layered_architecture`

---

### 2.9 `roadmap_timeline_chart`

**中文名称**：路线图时间轴  
**用途**：用于三阶段路径、年度规划、产品演进、项目里程碑。  
**适合表达**：短期/中期/长期、试点/沉淀/复制、年度规划、里程碑计划。

**推荐数据结构**：

```json
{
  "chart_type": "roadmap_timeline_chart",
  "chart_data": {
    "stages": [
      {
        "name": "短期",
        "time_range": "0-3个月",
        "goals": ["目标"],
        "actions": ["动作"],
        "milestones": ["里程碑"]
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `roadmap_timeline`

---

### 2.10 `trend_curve`

**中文名称**：趋势曲线图  
**用途**：用于产业趋势、增长趋势、技术成熟度演进。  
**适合表达**：增长曲线、成熟度曲线、技术演进趋势、市场变化趋势。

**推荐数据结构**：

```json
{
  "chart_type": "trend_curve",
  "chart_data": {
    "x_axis": ["2024", "2025", "2026"],
    "series": [
      {
        "name": "趋势",
        "values": [1, 2, 3]
      }
    ],
    "annotations": [
      {
        "x": "2026",
        "label": "关键拐点"
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `trend_curve_with_strategy`
- `insight_panel_with_chart`

---

### 2.11 `ecosystem_relationship_map`

**中文名称**：生态关系图  
**用途**：用于产业生态、伙伴体系、平台生态、标准组织关系。  
**适合表达**：中心主体与周边角色、伙伴协同、价值流、生态位关系。

**推荐数据结构**：

```json
{
  "chart_type": "ecosystem_relationship_map",
  "chart_data": {
    "center": "中心主体",
    "actors": [
      {
        "name": "伙伴",
        "role": "角色",
        "relationship": "协同关系"
      }
    ],
    "flows": [
      {
        "from": "中心主体",
        "to": "伙伴",
        "value": "价值流"
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `ecosystem_map`

---

### 2.12 `gap_heatmap`

**中文名称**：差距热力图  
**用途**：用于识别短板优先级、补齐难度和行动优先级。  
**适合表达**：差距项、影响程度、紧急度、补齐难度、优先级。

**推荐数据结构**：

```json
{
  "chart_type": "gap_heatmap",
  "chart_data": {
    "rows": [
      {
        "gap": "差距项",
        "impact": "高",
        "urgency": "中",
        "difficulty": "高",
        "action": "补齐动作"
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `insight_panel_with_chart`
- `risk_decision_matrix`

---

### 2.13 `risk_matrix`

**中文名称**：风险矩阵  
**用途**：用于风险概率、影响、应对措施和责任闭环。  
**适合表达**：风险识别、风险等级、概率/影响判断、应对动作、责任方。

**推荐数据结构**：

```json
{
  "chart_type": "risk_matrix",
  "chart_data": {
    "risks": [
      {
        "risk": "风险项",
        "probability": "高",
        "impact": "高",
        "mitigation": "应对动作",
        "owner": "责任方"
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `risk_decision_matrix`

---

### 2.14 `decision_table`

**中文名称**：决策清单表  
**用途**：用于高层拍板事项、资源申请、行动闭环。  
**适合表达**：决策事项、推荐方案、资源需求、时点、责任方、预期产出。

**推荐数据结构**：

```json
{
  "chart_type": "decision_table",
  "chart_data": {
    "columns": ["事项", "推荐方案", "资源", "时点", "责任方", "产出"],
    "rows": [
      ["事项一", "方案", "资源", "时间", "责任方", "产出"]
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `risk_decision_matrix`

---

### 2.15 `value_chain_loop`

**中文名称**：价值闭环图  
**用途**：用于展示输入、处理、输出、反馈、优化的闭环。  
**适合表达**：持续运营闭环、数据价值链、模型迭代闭环、安全运营闭环、客户经营闭环。

**推荐数据结构**：

```json
{
  "chart_type": "value_chain_loop",
  "chart_data": {
    "steps": [
      {"name": "输入", "description": "输入内容"},
      {"name": "处理", "description": "处理机制"},
      {"name": "输出", "description": "业务结果"},
      {"name": "反馈", "description": "反馈机制"},
      {"name": "优化", "description": "持续优化"}
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `ecosystem_map`
- `stack_architecture_with_right_insights`

---

### 2.16 `swimlane_process`

**中文名称**：泳道流程图  
**用途**：用于跨角色、跨组织、跨阶段协作流程。  
**适合表达**：多角色协作、项目流程、交付流程、审批流程、运维闭环流程。

**推荐数据结构**：

```json
{
  "chart_type": "swimlane_process",
  "chart_data": {
    "lanes": [
      {
        "name": "角色A",
        "steps": ["动作1", "动作2"]
      },
      {
        "name": "角色B",
        "steps": ["动作1", "动作2"]
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `roadmap_timeline`
- `stack_architecture_with_right_insights`

---

### 2.17 `priority_matrix`

**中文名称**：优先级矩阵  
**用途**：用于场景优先级、项目排序、资源投入判断。  
**适合表达**：价值/难度、收益/投入、影响/紧急度、可复制性/技术可达性。

**推荐数据结构**：

```json
{
  "chart_type": "priority_matrix",
  "chart_data": {
    "x_axis": "实施难度",
    "y_axis": "业务价值",
    "items": [
      {
        "name": "场景A",
        "x": "低",
        "y": "高",
        "recommendation": "优先推进"
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `four_quadrant_judgement`

---

### 2.18 `metric_showcase_grid`

**中文名称**：指标展示网格  
**用途**：用于呈现成果、规模、覆盖、增长、生态数量、案例数量等指标组合。  
**适合表达**：多组关键数字、一页成果总览、行业覆盖证明。  
**不适合表达**：无来源的事实断言、复杂因果推导。

**推荐数据结构**：

```json
{
  "chart_type": "metric_showcase_grid",
  "chart_data": {
    "metrics": [
      {
        "label": "指标名称",
        "value": "待填",
        "unit": "",
        "note": "口径/来源/待核验"
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `metric_case_showcase_grid`
- `executive_summary_dashboard`

---

### 2.19 `case_gallery_cards`

**中文名称**：案例图卡组  
**用途**：用于展示行业案例、样板项目、产品截图、场景图和伙伴 Logo。  
**适合表达**：多案例证明、行业覆盖、场景落地。  
**不适合表达**：替代方案论证；没有案例来源时不得生成虚构案例。

**推荐数据结构**：

```json
{
  "chart_type": "case_gallery_cards",
  "chart_data": {
    "cards": [
      {
        "title": "案例/场景名称",
        "image_ref": "待提供",
        "proof_point": "证明的能力或价值",
        "source_status": "provided_or_pending"
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `metric_case_showcase_grid`
- `left_logic_right_proof`

---

### 2.20 `hub_spoke_relationship_map`

**中文名称**：中心辐射关系图  
**用途**：用于表达中心平台/核心能力与周边伙伴、行业、场景、组织角色之间的关系。  
**适合表达**：平台生态、伙伴体系、场景协同、组织协同。  
**不适合表达**：普通能力清单；无明确关系的模块堆叠。

**推荐数据结构**：

```json
{
  "chart_type": "hub_spoke_relationship_map",
  "chart_data": {
    "center": "中心主体",
    "nodes": [
      {
        "name": "周边角色/能力/场景",
        "relationship": "协同关系或价值流"
      }
    ]
  }
}
```

**典型搭配 layout_pattern**：

- `hub_spoke_ecosystem_canvas`
- `ecosystem_map`

---

## 3. layout_pattern 与 chart_type 推荐组合

| layout_pattern | 推荐 chart_type | 说明 |
|---|---|---|
| `executive_summary_dashboard` | `key_findings_cards` / `quadrant_matrix` / `capability_map` | 总览页用图表承载判断和决策提示 |
| `two_column_comparison` | `comparison_table` / `capability_radar` | 页面是左右对比结构，图表是对比表或雷达图 |
| `four_quadrant_judgement` | `quadrant_matrix` / `priority_matrix` | 页面采用四象限布局，图表表达二维判断 |
| `three_column_cards` | `key_findings_cards` / `capability_map` | 页面是三列卡片，图表可为结论卡片或能力地图 |
| `layered_architecture` | `layered_stack_diagram` / `architecture_flow_diagram` | 页面是架构布局，图表是分层或流转结构 |
| `stack_architecture_with_right_insights` | `layered_stack_diagram` / `architecture_flow_diagram` / `value_chain_loop` | 页面包含右侧洞察栏，图表承载体系结构 |
| `roadmap_timeline` | `roadmap_timeline_chart` / `swimlane_process` | 页面是路线图布局，图表是时间轴或泳道流程 |
| `trend_curve_with_strategy` | `trend_curve` | 页面是趋势 + 策略解读，图表是趋势曲线 |
| `ecosystem_map` | `ecosystem_relationship_map` / `value_chain_loop` | 页面是生态布局，图表是关系或闭环 |
| `insight_panel_with_chart` | `trend_curve` / `comparison_table` / `gap_heatmap` / `capability_radar` | 页面是图表 + 洞察卡片 |
| `risk_decision_matrix` | `risk_matrix` / `decision_table` / `gap_heatmap` | 页面是风险/决策布局，图表是矩阵或清单 |

---

## 4. deck_spec.json 示例

### 4.1 正确示例：layout_pattern 和 chart_type 分工清晰

```json
{
  "slide_no": 4,
  "section": "第一章 结论与判断框架",
  "type": "framework",
  "title": "要形成有效判断，必须从硬件、软件、生态、场景、成本、风险六维对比",
  "conclusion": "若只看理论算力或单项 benchmark，容易误判实际落地价值与战略风险。",
  "display_text": [
    "硬件能力",
    "软件栈",
    "模型生态",
    "场景适配",
    "成本与供应链",
    "风险闭环"
  ],
  "layout_pattern": "insight_panel_with_chart",
  "chart_type": "comparison_table",
  "chart_data": {
    "columns": ["维度", "评估口径", "关键判断"],
    "rows": [
      ["硬件", "性能、显存、互联", "决定基础能力"],
      ["软件", "工具链、框架、调优", "决定开发效率"]
    ]
  },
  "visual_notes": "左侧为六维对比表，右侧为高层判断卡片。"
}
```

### 4.2 错误示例：把 layout_pattern 写进 chart_type

```json
{
  "layout_pattern": "insight_panel_with_chart",
  "chart_type": "insight_panel_with_chart"
}
```

错误原因：`insight_panel_with_chart` 是页面布局，不是图表类型。

### 4.3 错误示例：把 chart_type 写进 layout_pattern

```json
{
  "layout_pattern": "risk_matrix",
  "chart_type": "risk_matrix"
}
```

错误原因：`risk_matrix` 是风险矩阵图表，不是页面整体版式。正确写法应为：

```json
{
  "layout_pattern": "risk_decision_matrix",
  "chart_type": "risk_matrix"
}
```

---

## 5. 图表使用规则

1. `chart_type` 必须来自本文件定义的图表类型。
2. `layout_pattern` 必须来自 `visual_patterns/layout_library.md`。
3. 图表必须承载观点，不做装饰。
4. 每个图表必须回答：“看完后高层应该形成什么判断？”
5. 主题专属图表必须来自相应 `domain_profiles/`，不能全局默认使用。
6. 如果一页没有图表，应将 `chart_type` 设置为 `none`，且 `chart_data` 设置为 `{}`。
7. 同一页可以有主图表和辅助图表，但 `chart_type` 只记录主图表，辅助图表写入 `visual_notes`。
8. 不允许使用 `layout_pattern` 名称作为 `chart_type`。
9. 不允许使用 `chart_type` 名称作为 `layout_pattern`。
10. 如果无法判断，应优先选择更通用的 `chart_type`，并在 `visual_notes` 中说明不确定点。

---

## 6. 推荐枚举值

### 6.1 layout_pattern 枚举值

来自 `visual_patterns/layout_library.md`：

```text
executive_summary_dashboard
two_column_comparison
four_quadrant_judgement
three_column_cards
layered_architecture
stack_architecture_with_right_insights
roadmap_timeline
trend_curve_with_strategy
ecosystem_map
insight_panel_with_chart
risk_decision_matrix
```

### 6.2 chart_type 枚举值

来自本文件：

```text
none
key_findings_cards
quadrant_matrix
comparison_table
capability_radar
capability_map
layered_stack_diagram
architecture_flow_diagram
roadmap_timeline_chart
trend_curve
ecosystem_relationship_map
gap_heatmap
risk_matrix
decision_table
value_chain_loop
swimlane_process
priority_matrix
```
---

## 7. 视觉组件约束补充

本节约束 Builder 绘制图表时的视觉语法，避免同一套 PPT 内卡片、表格、流程、闭环图风格漂移。

### 7.1 `key_findings_cards` 视觉规则

- 同页卡片等宽等高，内边距一致。
- 强卡片最多 1 张；其余卡片用弱边框、浅灰底或较低文字权重降级。
- 红色只用于编号、核心数字或关键词，不使用整块红色标题栏铺满多张卡片。
- 每张卡片建议包含：短标签、核心短句、1 行说明；避免长段落。

### 7.2 `comparison_table` 视觉规则

- 表格是证据区，不承担全部结论；必须配独立结论区、右侧指标卡或标题结论。
- 行列线使用浅灰细线；高亮项不超过 2~3 个。
- 表头可加粗或用红色关键词强调，但避免大面积深色底。
- 高密度表格应优先减少列数或只展示 Top 项，其余放讲解口径或备注。

### 7.3 `swimlane_process` 视觉规则

- 泳道节点高度、宽度、间距统一；箭头细线化。
- 每个节点控制为短语，不写长句。
- 红色只标记关键判定节点、终点或当前阶段，不标满所有节点。
- 右侧洞察栏只承载 1 句结论 + 3~4 条短要点。

### 7.4 `value_chain_loop` 视觉规则

- 闭环节点建议 4~5 个，每个节点使用“动词 + 名词”短语。
- 闭环图是概念锚点，不是文字容器；详细说明放到右侧洞察栏或讲解口径。
- 箭头和连接线用浅灰/深灰，红色只用于闭环起点、关键节点或中心结论。
- 不得同时使用复杂箭头、厚重底部红条和多组红色标签。

---

## 3. 图表语义失败条件与降级规则

### 3.1 `quadrant_matrix` 失败条件

出现以下情况时，不得使用 `quadrant_matrix`：

- x/y 轴不能解释每个象限的位置；
- 页面只是四类能力、四类问题或四类概念并列；
- 没有风险区、目标区、优先区或迁移路径；
- 四象限只是为了填满页面，而非支撑标题结论。

若触发以上条件，应降级为 `comparison_table`、`capability_map`、`priority_matrix`，或在版式上改用 `three_column_cards` / `multi_module_solution_overview`。

### 3.2 `architecture_flow_diagram` 因果链要求

- 流程图必须表达输入、处理、输出、缺口或治理动作。
- 不允许把不同层级概念放成同级节点。
- 如果页面核心是“A 能做到，但不能支撑 B”，必须把 A 能力与 B 缺口拆成两个节点。
- 如果页面核心矛盾是“A ≠ B”，必须通过节点、分隔线、断点或红色锚点显式表达差异。

### 3.3 `gap_heatmap` 使用边界

- 如果只有三类缺口，但没有热度、严重度、优先级或成熟度矩阵，不应使用 `gap_heatmap`。
- 只有当页面需要表达“缺口 × 维度”的强弱差异时，才使用 `gap_heatmap`。
- 如果要表达风险传导、递归放大或流程污染，优先使用 `swimlane_process` 或 `value_chain_loop`。

### 3.4 图表服务结论检查

输出 deck_spec 或页面图片前，必须检查：

1. 图表是否回答标题中的核心判断；
2. 坐标、箭头、层级、分组是否有真实语义；
3. 页面核心矛盾是否被视觉化；
4. 图表是否只是概念摆放或装饰性模板。

若图表无法把结论讲透，应优先重选更通用的 `chart_type`，并在 `visual_notes` 中说明降级原因。

---

## 6. 生成图片反馈沉淀：图表语义失败条件

来源：生成 PPT 图片与华为模板对标后的通用沉淀。以下规则用于防止“图表有形、结论无力”。

### 6.1 `case_gallery_cards` 失败条件

出现以下情况时，不应使用或应降级处理：

- 图片或案例数量多，但没有证明同一个标题判断；
- 右侧证据与左侧逻辑各讲一套；
- 案例页变成素材墙、Logo 墙或截图墙；
- 没有来源或未经核验的数字被当成事实。

触发时应降级为 `left_logic_right_proof` 中的单案例证明，或标注为待验证样例。

### 6.2 `decision_table` 失败条件

出现以下情况时，应重构页面：

- 表格占满主体区，拍板事项不突出；
- 表格只有原则，没有责任、资源、时点、产出；
- 高层看完仍不知道需要拍什么。

触发时应将页面改为“拍板事项卡 + 执行清单表”。

### 6.3 `capability_map` 失败条件

出现以下情况时，应降级或重构：

- 只列能力名称，没有连接到场景、机制或闭环；
- 所有能力同权，无法看出主能力和支撑能力；
- 图表无法解释标题中的关键判断。

### 6.4 `layered_stack_diagram` 失败条件

出现以下情况时，应重构层级关系：

- 只展示组成清单，没有说明层间支撑关系；
- 底座、平台、能力、应用之间没有输入/输出/约束/承载关系；
- 每层文字过多，导致分层图退化为表格。

### 6.5 `roadmap_timeline_chart` 失败条件

- 三阶段只是并列计划，没有阶段门槛、验收产出或复制条件；
- 后一阶段不依赖前一阶段沉淀结果；
- 时间轴看完后无法判断下一步先做什么。


---

## 7. deck_spec 图表证明契约

本节用于约束 `deck_spec.json` 中新增字段 `chart_proof_goal` 与 `chart_visual_boundary`，防止“chart_type 合法但图表不证明结论”。

### 7.1 通用规则

每页选择 `chart_type` 前，必须先明确：

1. `core_judgement`：本页唯一核心判断；
2. `chart_proof_goal`：主图表必须证明什么；
3. `chart_visual_boundary`：主图表不能画偏成什么、必须体现什么、红色和主次如何控制。

`chart_type` 的选择必须服务 `chart_proof_goal`，不得因为版式好看而选择不承担证明任务的图表。

### 7.2 常见 chart_type 的 proof_goal 示例与视觉边界

| chart_type | 典型 chart_proof_goal | chart_visual_boundary 示例 |
|---|---|---|
| `key_findings_cards` | 证明多个支撑判断共同指向一个主判断 | 不得所有卡片同权；必须有主卡或主结论；红色只用于主判断或关键风险 |
| `comparison_table` | 证明两个对象/状态之间存在明确差异并导出管理含义 | 不得退化为大表格；必须有差异结论；表格承担证据，结论独立呈现 |
| `quadrant_matrix` | 证明对象在两条有效坐标轴下的优先级/风险/目标位置 | 必须有真实 x/y 轴；不得只是四类概念并列；目标区/风险区必须可见 |
| `capability_map` | 证明能力与场景、机制或闭环之间存在支撑关系 | 不得只是能力清单；中心能力和周边对象必须有关系线；避免连接线过多交叉 |
| `layered_stack_diagram` | 证明底座、平台、能力、应用之间存在层间支撑关系 | 不得只是层级堆叠；每层支撑上一层；右侧说明不得压过主架构 |
| `architecture_flow_diagram` | 证明系统/数据/模型/业务之间存在可执行流转关系 | 必须有输入、处理、输出或回写；不同层级概念不得同级摆放 |
| `roadmap_timeline_chart` | 证明阶段之间存在产出继承、门槛和验收关系 | 不得只是并列计划；必须有阶段门槛/验收产出；红色不得贯穿整条时间轴 |
| `value_chain_loop` | 证明输入、处理、输出、反馈、优化形成闭环 | 必须形成闭合路径；回写/反馈节点必须可见；不得画成单向流程 |
| `swimlane_process` | 证明多角色/阶段之间存在责任分工和交付流转 | 泳道必须有角色差异；节点文字不可过长；箭头和交付物必须清晰 |
| `gap_heatmap` | 证明差距项在影响、紧急度、难度等维度上的优先级 | 不得伪装成普通列表；必须有轻重差异；红色只标最高风险/优先项 |
| `decision_table` | 证明高层需要拍板的事项、责任、资源和产出 | 拍板事项必须独立突出；表格不能吞没结论；不得只是原则清单 |
| `case_gallery_cards` | 证明案例/截图/图片支撑同一个核心判断 | 不得变成图片墙/Logo墙；必须有主证明图；每个素材要有证明点 |
| `metric_showcase_grid` | 证明关键指标共同支撑成果/规模/趋势判断 | 数字必须有来源或待核验；不得无依据生成指标；不得多个大数字同权抢焦点 |
| `hub_spoke_relationship_map` | 证明中心主体与周边角色/场景/能力存在协同关系 | 不得只是中心大词+周边名词；连接线少而清晰；中心节点可为唯一红色锚点 |
| `risk_matrix` | 证明风险在概率、影响、应对和责任上形成闭环 | 不得只列风险；必须体现应对动作和责任；最高风险可唯一红色标识 |
| `priority_matrix` | 证明事项在价值/难度等维度下的推进优先级 | 坐标必须成立；优先区必须可见；不得四格同权 |
| `trend_curve` | 证明趋势变化、拐点或阶段转换支撑策略判断 | 不得画无数据依据的精确曲线；拐点标注必须服务策略结论 |
| `ecosystem_relationship_map` | 证明生态角色之间存在价值流或协同关系 | 不得画成 Logo 墙；关系线必须有语义；中心与周边主次明确 |

### 7.3 chart_semantic_mapping 语义解释映射

`chart_semantic_mapping` 用于说明主图表如何证明 `chart_proof_goal`，避免图表沦为装饰、模板或误读。它不是渲染 DSL，不规定坐标、字号或 shape 参数；它是 deck_spec 中面向角色 C 的图表语义解释层。

#### 7.3.1 触发规则

- `chart_type = trend_curve` 时，必须输出 `chart_semantic_mapping`。
- 以下高语义风险图表建议输出：`quadrant_matrix`、`roadmap_timeline_chart`、`architecture_flow_diagram`、`layered_stack_diagram`、`value_chain_loop`、`swimlane_process`、`ecosystem_relationship_map`。
- 普通 `key_findings_cards`、`comparison_table` 可按页面复杂度选择是否输出。

#### 7.3.2 字段结构

```json
{
  "chart_semantic_mapping": {
    "chart_reading_intent": "读者看完图后必须得出的判断",
    "main_visual_logic": "主图通过什么视觉关系证明判断",
    "axis_semantics": {},
    "stage_or_node_meaning": {},
    "insight_panel_logic": [],
    "forbidden_visualization": []
  }
}
```

#### 7.3.3 六个核心字段

| 字段 | 解决的问题 |
|---|---|
| `chart_reading_intent` | 图表到底要让读者得出什么判断 |
| `main_visual_logic` | 主图应该怎么证明判断 |
| `axis_semantics` | 坐标轴、矩阵、趋势语义是否成立 |
| `stage_or_node_meaning` | 阶段、节点、卡片不是空标签 |
| `insight_panel_logic` | 右侧洞察栏解释主图，而非备注 |
| `forbidden_visualization` | 明确禁止误画、乱画、越界画 |

#### 7.3.4 `trend_curve` 必填语义要求

当 `chart_type=trend_curve` 时，必须说明：

1. 这条趋势到底证明增长、下降、拐点、成熟度变化还是阶段转换；
2. x 轴是否代表时间、阶段、成熟度或其他序列，不能伪造精确年份；
3. y 轴是否有真实度量，若没有真实数据，应标注为趋势/成熟度示意，不得画成精确数值曲线；
4. 拐点、注释和右侧策略解读必须服务同一个 `chart_proof_goal`；
5. 禁止用平滑上升曲线表达未经验证的确定增长。

`trend_curve` 示例：

```json
{
  "chart_type": "trend_curve",
  "chart_semantic_mapping": {
    "chart_reading_intent": "读者应判断：技术演进已从单点工具辅助进入可学习、可解释、可审查的工程闭环阶段。",
    "main_visual_logic": "曲线表达能力成熟度从低到高演进，关键拐点标注语义模型和AI回写机制成为阶段转换条件。",
    "axis_semantics": {
      "x_axis": "阶段序列，不代表精确年份",
      "y_axis": "工程闭环成熟度示意，不代表量化指标"
    },
    "stage_or_node_meaning": {
      "现状": "模型辅助，AI多为孤立应用",
      "转折": "语义模型、仿真和XAI开始接入工程过程",
      "目标态": "模型可学习、可解释、可审查并可回写"
    },
    "insight_panel_logic": [
      "右侧洞察只解释拐点为何成立",
      "策略建议必须从曲线阶段转换推出"
    ],
    "forbidden_visualization": [
      "不得画成无来源的精确增长曲线",
      "不得用大红上升箭头暗示确定收益",
      "不得让右侧洞察变成与曲线无关的备注"
    ]
  }
}
```

### 7.4 失败条件

出现以下任一情况，必须重写 `chart_proof_goal`、调整 `chart_type` 或拆页：

- `chart_proof_goal` 与 `core_judgement` 无直接关系；
- `chart_type` 无法证明 `chart_proof_goal`；
- `chart_visual_boundary` 为空、泛化或不可执行；
- 图表只是展示信息清单，不能形成判断；
- 图表视觉表达违反 `templates/visual_rules.md` 或 `eval/visual_scorecard.md` 的一票降级项。
