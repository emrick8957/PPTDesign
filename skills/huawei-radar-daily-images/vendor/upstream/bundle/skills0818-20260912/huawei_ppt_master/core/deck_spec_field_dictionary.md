# deck_spec_field_dictionary

## 1. 文件定位

`deck_spec.json` 是 PPT 生成链路中的**页面语义合同**，用于把大纲、逐页文案、页面设计说明转换为角色 C 可理解的结构化输入。

它的核心作用是说明：

- 每页要表达什么判断；
- 每页标题、结论、展示文本和讲解口径是什么；
- 每页主图表要证明什么；
- 每页应使用哪类 `layout_pattern`，以及一个主图表组件与可选辅助图表组件的 `chart_type` 组合；
- 每页有哪些视觉强调、文本密度、压缩需求和数据缺口。

边界说明：

- `deck_spec.json` 不是 PPTX 文件；
- 不是像素级 shape 指令；
- 不直接规定坐标、字号、线条、连接线和组件宽高；
- 角色 C 需要基于 `chart_type`、`layout_pattern`、`chart_data` 和视觉规则，将其转换为具体页面渲染结构；这些视觉字段构成视觉基线，不是唯一合法施工解。
- Role C 不得回写 `deck_spec.json`；仅在 `adaptive_recomposition` 下，且页面语义、证据、关系、目标 schema 和华为视觉门禁全部通过时，才可在页面渲染合同中生成不同的有效渲染方案。

---

## 2. 顶层字段

| 字段 | 类型 | 作用 | 角色 C 使用方式 |
|---|---|---|---|
| `deck_title` | string | 整份 PPT 标题 | 用于封面标题、文件命名或交付物识别 |
| `audience` | string | 汇报对象 | 用于判断表达风格、信息密度和视觉克制程度 |
| `style` | string | 整体风格标识 | 用于选择华为汇报风格，如红黑灰白、白底、弱页脚 |
| `source` | string | 主要来源材料 | 用于页脚来源、证据追踪或备注，不应抢占主体视觉 |
| `slides` | array | 页面列表 | 角色 C 按 `slide_no` 顺序逐页消费并生成页面 |

---

## 3. slide 字段

| 字段 | 类型 | 作用 | 角色 C 使用方式 |
|---|---|---|---|
| `slide_no` | integer | 页码 | 决定页面顺序、页码和页面文件名 |
| `section` | string | 所属章节 | 可作为页眉小标签或章节归属，不应抢主标题焦点 |
| `type` | string | 页面类型 | 唯一页型字段。**必须严格来自 templates/page_types.md 定义的标准页型枚举**；不得另行输出 `page_type`；确需扩展时，只能先提交 patch proposal，不得在 deck_spec 中临时创造新值。 |
| `page_goal` | string | 页面目标 | 用于判断页面是否完成高层沟通目的，通常不直接上屏 |
| `title` | string | 页面主标题 | 直接进入标题区，需控制 1–2 行并保持结论型表达 |
| `conclusion` | string | 页面核心结论 | 可作为主卡、底部收口或讲解锚点，是否上屏由版式决定 |
| `core_judgement` | string | 本页唯一核心判断 | logic-only；指导全页内容和图表，永不原文上屏；不得等于 `conclusion` 或固定前缀 + `conclusion`，允许正当提炼 |
| `chart_proof_goal` | string | legacy 主图表证明目标 | 新合同不在 slide 顶层手写；由 Role C 从 primary 组件派生。legacy 输入继续按原规则消费。 |
| `chart_visual_boundary` | array[string] | legacy 主图视觉边界 | 新合同不在 slide 顶层手写；由 Role C 从 primary 组件派生。 |
| `chart_semantic_mapping` | object | legacy 主图语义映射 | 新合同不在 slide 顶层手写；由 Role C 从 primary 组件派生。 |
| `display_text` | array[string] | 页面展示文本 | 作为卡片、节点、标签、表格等上屏文本候选；应短语化，每条建议不超过 15 个汉字，长解释进入 `speaker_notes` 或 `chart_semantic_mapping` |
| `speaker_notes` | string | 讲解口径 | 可进入备注区或讲稿，不应作为主体长段落堆叠 |
| `chart_components` | array | 新合同图表事实源 | 必须恰好包含一个 primary，可包含 0~3 个 supporting；逐组件提供类型、数据、证明目标和边界。 |
| `chart_type` | string | legacy 主图表类型 | 仅用于没有 `chart_components` 的历史输入；新合同由 Role C 从 primary 派生。 |
| `chart_data` | object | legacy 主图表数据 | 仅用于没有 `chart_components` 的历史输入；新合同数据位于各组件内部。 |
| `layout_pattern` | string | 页面版式模式 | 必须来自 `layout_library.md`，角色 C 据此选择页面布局模板 |
| `visual_notes` | string | 视觉补充说明 | 用于指导配色、留白、主次和页面气质，不是直接上屏文本；通用视觉规范应下沉为全局默认，逐页只保留本页主图、红色锚点、布局偏离和主次策略 |
| `visual_focus` | array[string] | 视觉焦点 | 用于确定页面主视觉关注点和扫读路径 |
| `must_highlight` | array[string] | 必须强调内容 | 用于确定少量强调词或红色锚点，避免多处抢焦点 |
| `text_density` | string | 文本密度 | 用于决定字号、压缩策略、是否需要拆分或弱化说明 |
| `need_compression` | boolean | 是否需要压缩 | 为 true 时，角色 C 应优先压缩辅助文本而非压缩核心判断 |
| `data_gaps` | array[string] | 数据缺口 | 用于标注待补材料或备注，不能伪造成确定事实 |

### 3.1 非字段说明

- 逐页文案中的“正文模块”是 page_copy 阶段的自然语言小节，不对应 `deck_spec.json` 中的 `body` 字段；生成 deck_spec 时必须拆入 `display_text`、`chart_data`、`speaker_notes` 或 `chart_semantic_mapping`。
- 页型统一使用 `type` 字段；`page_type` 仅视为历史输入包中的同义字段，新 deck_spec 不应输出。

### 3.2 图表合同模式

每页必须且只能使用一种图表合同模式：

| 模式 | 判定 | 图表事实源 | Role A / Role C 规则 |
|---|---|---|---|
| `component_contract` | 存在 `chart_components` | `chart_components` | Role A 新输出必须使用；Role C 从 primary 派生主图兼容值。 |
| `legacy_single_chart` | 不存在 `chart_components` | 顶层旧主图字段 | 仅兼容历史输入；Role C 合成一个 `C1 primary`。 |

禁止同页同时出现 `chart_components` 与任一顶层旧主图字段：`chart_type`、`chart_data`、`chart_proof_goal`、`chart_visual_boundary`、`chart_semantic_mapping`。混用构成双事实源，必须 FAIL。

### 3.3 chart_components 字段合同

```json
{
  "component_id": "C1",
  "component_role": "primary",
  "component_region": "main",
  "supports_component_id": null,
  "chart_type": "priority_matrix",
  "chart_data": {},
  "chart_proof_goal": "证明高价值、低难度事项应优先推进",
  "chart_visual_boundary": ["优先区必须可见"],
  "chart_semantic_mapping": {}
}
```

规则：

1. `component_id` 在同页唯一，格式为 `C1`、`C2`……；
2. `component_role` 只允许 `primary`、`supporting`；
3. 每页恰好一个 primary，supporting 为 0~3 个；
4. `component_region` 只允许 `main`、`left`、`right`、`top`、`bottom`，同页不得重复；
5. `component_region` 必须命中 `layout_library.md` 的版式—区域兼容表；
6. `component_region` 不包含 `insight_panel`，右侧洞察栏不得承载独立图表组件；
7. supporting 的 `supports_component_id` 必须引用同页唯一 primary；primary 必须省略该字段或设为 `null`；
8. supporting 不得使用 `chart_type=none`；primary 为 none 时不得存在 supporting；
9. 每个组件分别遵守现有 `chart_type`、`chart_data`、`chart_proof_goal`、`chart_visual_boundary` 和 `chart_semantic_mapping` 规则；
10. `bottom` 组件与启用的底部结论条互斥；无合法区域或超过密度预算时必须拆页。


---

## 4. chart_data 字段通则与可见性约定

### 4.1 字段分层

不同 `chart_type` 的 `chart_data` 结构不同（cards / columns+rows / nodes+edges / layers+items / stages / lanes 等），但字段可统一归为三类：

| 类别 | 典型字段 | 是否需要规则 | 规则 |
|---|---|---|---|
| 拓扑/管道字段 | `nodes`、`edges`、`id`、`from`、`to`、`rows`、`columns`、`layers`、`stages`、`lanes` 等结构键 | 否 | 通用图/表结构语法，角色 C 按标准结构消费；不逐字段写渲染规则 |
| 显示内容字段 | `label`、`name`、`headline`、`items`、`description`、单元格文本、`edges.label`、`lane.name` 等 | 是 | 可上屏，但必须短语化、控制长度、避免长句；不得编造未提供的数字/案例；遵守 `wording_rules.md` 与 `visual_rules.md` 的节点短语化要求 |
| 逻辑字段 | `group`、`emphasis`、`source_status` 等仅用于分组/标记 | 是 | **logic-only：仅供逻辑分组、样式强弱或渲染判断，不得被字面渲染为节点/卡片/泳道可见标签** |

### 4.2 logic-only 字段清单（不得直接上屏）

以下字段仅用于逻辑、约束、分组或讲解，角色 C 不得将其原文渲染为页面主体可见文本：

- slide 级：
  - `page_goal`：只用于判断页面沟通目标，不直接上屏；
  - `core_judgement`：指导全页判断，永不原文上屏；标题、结论、主卡只能承载其转写后的可见表达；
  - `chart_proof_goal`：指导主图证明任务，不直接作为图中说明文字；
  - `section`：只可作为页眉/章节弱标签显示，不得作为主体节点、卡片标题或图表标签。
- chart_data 级：
  - `group`：仅用于内部归类、布局分组或样式分组，不得字面上屏；
  - `emphasis`：仅用于强弱层级或视觉强调判断，不得字面上屏；
  - `source_status`：仅用于来源状态判断，不得字面上屏。

### 4.3 可见分组标题应使用什么字段

如果页面需要可见分组标题，不得复用 logic-only 的 `group` 字段，应使用以下可见字段：

- 节点/卡片标题：`label`、`name`、`headline`；
- 页面展示候选：`display_text`；
- 泳道图标题：`lane.name` 可见，`node.group` 不可见；
- 分层图标题：`layer.name` 可见，层内节点的 `group` 不可见；
- 路线图阶段标题：`stage.name` 可见。

判断原则：

- 字段名表达的是“显示文本” → 可以上屏；
- 字段名表达的是“分组/状态/强弱/来源判断” → logic-only，不直接上屏。

### 4.4 edges.label 的可见性边界

`edges.label` 是可见内容字段，但只能承载短动作词或短关系词，例如：`回写`、`验证`、`编译`、`生成`、`仿真`、`审查`。

`edges.label` 不得承载复杂关系解释，例如为什么回写、回写形成什么闭环、两条 V 模型如何同层对应、层级支撑关系如何证明页面判断。

复杂关系语义必须写入：

- `chart_semantic_mapping.main_visual_logic`；
- `chart_semantic_mapping.stage_or_node_meaning`；
- `chart_semantic_mapping.forbidden_visualization`。

### 4.5 显示内容字段短语化判据

可见字段应短语化，避免长句撑爆节点或卡片：

- `label` / `name`：建议 ≤12 个汉字，或 ≤2 个短语；
- `headline`：建议 ≤16 个汉字；
- `items`：每项建议 ≤14 个汉字；
- `edges.label`：建议 2~6 个汉字，优先动词或动宾短语；
- 长解释应放入 `description`、`speaker_notes`、`chart_semantic_mapping` 或页面洞察区。

若可见字段过长，自检应 WARN；若导致图表变成文字容器，应返工。

### 4.6 关系语义的承载位置

方向（自顶向下 / 自底向上）、同层对应、层级支撑、闭环回写等复杂关系语义，统一由 `chart_semantic_mapping` 承载：

- `main_visual_logic`：说明主图通过什么关系证明判断；
- `stage_or_node_meaning`：说明节点、阶段、层级、泳道的语义；
- `forbidden_visualization`：说明禁止的退化形态，如禁线性化、禁错层、禁单向、禁散点化。

禁止在 `chart_data.nodes` / `chart_data.edges` 内新增 `relation_type`、`edge_style`、`position`、`anchor`、`x/y`、`layer_index` 等渲染或关系 DSL 字段。

### 4.7 关系角色与对应关系的结构化枚举（可选，高语义风险关系图建议）

当主图的论证依赖**同层对应、双分支方向、层级支撑或闭环**时，除散文说明外，`chart_semantic_mapping` 可输出结构化枚举，把关系语义升级为角色 C 可消费的清单。这是**语义分类**，不是渲染指令。

可选字段：

- `correspondence_pairs`：**同层对应关系的唯一事实源**。每项为 `{"left": <id>, "right": <id>, "meaning": <短语>}`，用于"双分支同层对应"类图（如 V 模型）。
- `edge_roles`：把 `chart_data.edges` 中**方向性边**按语义角色归组（不含同层对应）。每个角色的值是边引用数组，**每条边为结构化对象** `{"from": <id>, "to": <id>}`。角色取自：
  - `flow_decompose`（自顶向下分解流）
  - `flow_integrate`（自底向上集成流）
  - `lifecycle_close`（生命周期收尾，弱化）
  - `feedback_loop`（闭环回写）

约束：

- **同层对应只由 `correspondence_pairs` 承载**；`edge_roles` 不得出现 `same_level_correspondence` 角色，角色 C 读取同层对应只看 `correspondence_pairs`；
- `edge_roles` 的每条边 `{from,to}` 必须命中 `chart_data.edges` 中已存在的边；`correspondence_pairs` 的每个 id 必须命中 `chart_data` 中已存在的节点；不得引入影子边/影子节点；
- 不得使用 `"from->to"` 字符串引用，统一用结构化 `{"from":<id>,"to":<id>}`；
- `meaning` 为短语义说明（建议 ≤12 汉字），不得携带颜色/线宽/坐标；
- 该枚举**只解释语义角色**，角色 C 据此决定"同层对应应水平连接、不发散"，但具体线型/坐标仍由角色 C 自行决定；
- 禁止把这些角色名反向写回 `chart_data.edges`（那将复辟 `relation_type`）。

示例（V 模型）：

~~~json
"chart_semantic_mapping": {
  "main_visual_logic": "左支向下分解、右支向上集成，横向同层一一对应。",
  "correspondence_pairs": [
    {"left": "L3", "right": "R3", "meaning": "组件级验证"},
    {"left": "L2", "right": "R2", "meaning": "系统级验证"},
    {"left": "L1", "right": "R1", "meaning": "运行确认"}
  ],
  "edge_roles": {
    "flow_decompose": [
      {"from": "L1", "to": "L2"},
      {"from": "L2", "to": "L3"},
      {"from": "L3", "to": "B"}
    ],
    "flow_integrate": [
      {"from": "B", "to": "R3"},
      {"from": "R3", "to": "R2"},
      {"from": "R2", "to": "R1"}
    ],
    "lifecycle_close": [
      {"from": "R1", "to": "D"}
    ]
  },
  "forbidden_visualization": ["禁止把同层对应画成向中心发散/交叉的连线"]
}
~~~
