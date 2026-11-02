# 输出契约

## 1. 大纲输出契约

输出必须包含：

1. 汇报对象；
2. 汇报目标；
3. 总体叙事主线；
4. 章节分组；
5. 每页页码；
6. 每页结论型标题；
7. 每页核心结论；
8. 每页建议图表；
9. 每页回答的问题；
10. 后续逐页文案建议。


每页必须包含：

```text
P{n} {页标题}
核心结论：
页面类型：
建议图表：
页面设计说明：
该页回答的问题：
```

超过 12 页必须增加章节分组。

## 2. 逐页文案输出契约

输出必须包含：

1. 页码；
2. 页标题；
3. 一句话结论；
4. 正文模块；
5. 图表内容说明；
6. 版式建议；
7. 讲解口径；
8. 数据缺口或待补材料；
9. 是否适合直接进入 PPTX 生成。

每页必须包含：

```text
页标题：
一句话结论：
正文模块：
图表内容：
版式说明：
讲解口径：
数据缺口：
```

## 3. 页面设计说明输出契约

输出必须包含：

1. 页面类型；
2. 推荐版式模式；
3. 标题区设计；
4. 文字区设计；
5. 图表区设计；
6. 页脚规则；
7. 配色建议；
8. 信息密度控制；
9. PPTX Builder 实现提示；
10. 可能的压缩/拆页建议。
11. 视觉降噪约束，包括红色锚点、卡片层级、间距规则、底部结论条规则、需弱化的装饰元素、负面视觉边界和页型门禁。

必须包含：

```text
版式模式：
区域划分：
标题区：
图表区：
文字区：
强调元素：
页脚：
PPTX Builder 注意事项：
视觉降噪约束：
  red_anchor：
  card_hierarchy：
  spacing_rule：
  bottom_bar_rule：
  visual_simplification：
  visual_boundary：
  page_type_gate：
```

术语约束：“正文区”和“内容区”为废弃术语；一级区域使用“主体区”，主体区内细分“图表区 / 文字区 / 强调区 / 右侧洞察栏 / 底部结论条”。

## 4. deck_spec.json 输出契约

当用户要求输出 `deck_spec.json`，或用户未明确限制交付范围且当前任务采用本 Skill 默认全套交付链路时，输出严格 JSON。

### 4.0 deck_spec 证明契约字段

每页必须建立以下证明合同，用于约束“本页到底要证明什么”：

- `core_judgement`：本页唯一核心判断。它不是展示标题，也不是普通结论句，而是本页所有内容、图表和视觉元素必须共同服务的判断锚点。
- `chart_components`：新合同的图表事实源。每个组件分别包含 `chart_type`、`chart_data`、`chart_proof_goal`、`chart_visual_boundary` 和按触发规则输出的 `chart_semantic_mapping`。

字段边界：

- `core_judgement` 管“这一页唯一判断是什么”；
- primary 组件的 `chart_proof_goal` 管“主图要证明什么”；
- supporting 组件的 `chart_proof_goal` 管“它为主图增加什么证据、解释、局部比较、验证或行动收口”；
- 每个组件的 `chart_visual_boundary` 管该图表不能怎么画；
- 每个组件的 `chart_semantic_mapping` 管该图表如何被阅读和证明；
- 每个组件的 `chart_type` 仍只允许使用 `templates/chart_patterns.md` 中的合法枚举；
- `layout_pattern` 仍只允许使用 `visual_patterns/layout_library.md` 中的合法枚举。

新合同不得在 slide 顶层同时输出 `chart_type`、`chart_data`、`chart_proof_goal`、`chart_visual_boundary`、`chart_semantic_mapping`。这些字段仅作为 legacy 输入兼容，由 Role C 从 primary 组件机器派生。

### 4.0.1 字段差异化要求

`core_judgement` 以及每个组件的 `chart_proof_goal`、`chart_visual_boundary` 都必须承载设计决策。具体字段职责、页内两两比较、允许重复白名单、正反例和下沉规则以 `core/field_differentiation_rules.md` 为准。

关键要求：

- `core_judgement` 不得等于 `conclusion`，也不得只是固定前缀 + `conclusion`；允许对 `conclusion` 做正当提炼或收口；
- primary 的 `chart_proof_goal` 必须说明主图证明的因果、对比、演进、闭环、分层、决策或权衡关系；
- supporting 的 `chart_proof_goal` 不得复述 primary 或其他 supporting，必须说明独立增量；
- 每个组件的 `chart_visual_boundary` 必须结合自身图表风险和 `chart_semantic_mapping.forbidden_visualization`；
- 通用视觉规范应下沉为全局默认，不得逐页重复伪装成页面设计。
- 页型统一使用 `type`，不得输出同义字段 `page_type`；
- 逐页文案中的“正文模块”必须映射到 `display_text`、`chart_data`、`speaker_notes` 或 `chart_semantic_mapping`，不得作为 `body` 字段输出。

输出严格 JSON：

```json
{
  "deck_title": "",
  "audience": "",
  "style": "huawei_executive",
  "slides": [
    {
  "slide_no": 1,
  "section": "第一章 核心判断",
  "type": "executive_summary",
  "page_goal": "让高层在1分钟内看懂整体结论",
  "title": "当前竞争焦点不是“哪张卡更强”，而是“谁能形成可持续算力体系”",
  "conclusion": "英伟达整体领先，但昇腾在国产化、安全可控和重点行业适配上具备战略价值。",
  "core_judgement": "本页唯一要让高层带走的判断：竞争焦点从单卡性能转向可持续体系能力。",
  "display_text": [
    "英伟达领先在通用生态、开发者心智和训练体系",
    "昇腾具备国产化、安全可控和供应连续性优势",
    "核心短板在生态成熟度、迁移效率和复制能力",
    "建议以样板场景牵引补齐算力—模型—工具—运营闭环"
  ],
  "speaker_notes": "先讲总体判断，再讲差距和动作建议",
  "layout_pattern": "executive_summary_dashboard",
  "chart_components": [
    {
      "component_id": "C1",
      "component_role": "primary",
      "component_region": "main",
      "chart_type": "key_findings_cards",
      "chart_data": {"cards": []},
      "chart_proof_goal": "证明领先、差距、风险和建议共同指向体系化竞争",
      "chart_visual_boundary": [
        "不得画成无主次的并列卡片",
        "必须突出唯一主判断",
        "红色只能用于核心判断或关键风险"
      ],
      "chart_semantic_mapping": {
        "chart_reading_intent": "读者看完图后应形成的唯一判断",
        "main_visual_logic": "主卡与支撑卡共同证明体系化竞争",
        "axis_semantics": {},
        "stage_or_node_meaning": {},
        "insight_panel_logic": [],
        "forbidden_visualization": ["不得把图表画成装饰性模板"]
      }
    },
    {
      "component_id": "C2",
      "component_role": "supporting",
      "component_region": "bottom",
      "supports_component_id": "C1",
      "chart_type": "metric_showcase_grid",
      "chart_data": {
        "metrics": [
          {"label": "国产化", "value": "战略价值"},
          {"label": "生态成熟度", "value": "关键短板"}
        ]
      },
      "chart_proof_goal": "用关键指标标签收口战略价值与核心短板",
      "chart_visual_boundary": [
        "不得扩展为第二张架构图",
        "不得与主卡争夺红色锚点"
      ]
    }
  ],
  "visual_notes": "白底，红色强调结论，四象限卡片式布局",
  "visual_focus": [
    "领先",
    "差距",
    "风险",
    "建议"
  ],
  "must_highlight": [
    "体系竞争",
    "国产化",
    "生态成熟度"
  ],
  "text_density": "medium",
  "need_compression": false,
  "data_gaps": []
}
  ]
}
```

### 4.1 deck_spec 契约检查
- 是否只使用 component contract 或 legacy contract 其中一种模式；
- `chart_components` 是否恰好一个 primary、0~3 个 supporting；
- 每个组件的 `chart_type` 是否描述图表/信息结构，而非页面版式；
- `layout_pattern` 是否为版式模式，且可在版式库中找到；
- `component_region` 是否命中版式—区域兼容表；
- Builder 是否可直接据此生成 page_images / pptx。

### 4.2 deck_spec 字段边界补充
- `chart_type` 表示单个图表组件的信息结构类型；
- `layout_pattern` 表示页面布局模式；
- 两者不得混用。
- `component_region` 表示组件在页面版式中的相对槽位，不是第二个 layout。

#### 生成 deck_spec.json 时，每个组件的 `chart_type` 必须从 `templates/chart_patterns.md` 选择
推荐 `chart_type` 常用图表包括：


#### 生成 deck_spec.json 时，页面级 `layout_pattern` 必须从 `visual_patterns/layout_library.md` 选择；`component_region` 必须命中该版式的兼容表。





### 4.3 deck_spec 强门禁
生成 `deck_spec.json` 时，必须先完成以下检查：

1. 新输出必须包含 `chart_components`，不得与顶层 legacy 主图字段混用；
2. 每个组件的 `chart_type` 必须严格取自 `templates/chart_patterns.md` 已定义枚举；
3. `layout_pattern` 必须严格取自 `visual_patterns/layout_library.md` 已定义枚举；
4. 每个组件的 `component_region` 必须命中版式—区域兼容表且同页唯一；
5. `component_region` 不允许 `insight_panel`；右侧洞察栏不得承载独立图表组件；
6. 必须恰好一个 primary；supporting 不超过 3 个并全部指向 primary；
7. supporting 不得使用 `chart_type=none`；primary 为 none 时不得存在 supporting；
8. primary 的证明目标必须直接支撑 `core_judgement`；supporting 必须提供不同的证明增量；
9. 当任一组件 `chart_type=trend_curve` 时，该组件必须包含 `chart_semantic_mapping`；其他高语义风险图表按原规则执行；
10. 每个组件的 `chart_visual_boundary` 必须为数组，建议 3~5 条，不得为空泛口号；
11. 同页组件 proof goal 或 boundary 触发 `field_differentiation_rules.md` 的复述条件时 FAIL；
12. `bottom` 组件与启用的底部结论条互斥；
13. 必须通过 `eval/template_stamp_detection.md` 的模板印章检测。
14. 重复判定必须使用混合阈值模型：N<=3 两两比较，N>=4 使用 `repeat_threshold=max(3,ceil(N*0.5))`。
15. `core_judgement` 不得等于 `conclusion` 或固定前缀 + `conclusion`。
16. 组件 `chart_visual_boundary`、`visual_notes` / page_design overrides 若触发重复 FAIL，必须返工；
17. 每个组件 `chart_data` 的键名、列名、节点结构相似不判 FAIL，只判语义内容是否机械重复。
18. 每个组件 `chart_data` 中 logic-only 字段不得作为可见标签上屏，包括但不限于 `group`、`emphasis`、`source_status`；
19. 若需要可见分组标题，必须使用 `label`、`name`、`headline`、`display_text`、`lane.name`、`layer.name` 或 `stage.name` 等显示内容字段，不得复用 `group`；
20. `edges.label` 只能承载短动作词或短关系词，不得承载复杂关系语义；复杂关系语义必须进入 `chart_semantic_mapping`；
21. 不得在 `chart_data` 内新增 `relation_type`、`edge_style`、`position`、`anchor`、`x/y`、`layer_index` 等渲染或关系 DSL 字段。
22. 高语义风险关系图（双分支 / 同层对应 / 层级支撑 / 闭环）若需声明关系角色：同层对应只能由 `chart_semantic_mapping.correspondence_pairs` 承载，`edge_roles` 不得出现 `same_level_correspondence` 角色（单一事实源）。
23. `chart_semantic_mapping.edge_roles` 的边引用必须为结构化 `{"from":<id>,"to":<id>}`，不得使用 `"from->to"` 字符串；`edge_roles` 引用的边必须命中 `chart_data.edges` 已存在的边，`correspondence_pairs` 引用的 id 必须命中 `chart_data` 已存在的节点，不得引入影子边/影子节点。


### 4.4 无精确匹配时的唯一合法处理
如果设想的图表或版式没有精确匹配项，必须按以下顺序处理：

1. 优先选择最接近的通用 `chart_type`；
2. 再选择最接近的通用 `layout_pattern`；
3. 将差异、特化要求、视觉补充说明写入 `visual_notes`；
4. 不得自造新的 `chart_type` 或 `layout_pattern` 枚举值；
5. 如确实需要新增模式，只能在评审/优化环节输出 patch proposal，不得直接写入正式交付物。

