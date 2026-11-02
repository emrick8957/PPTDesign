# 模板印章检测

## 1. 检测目标

识别 `deck_spec.json`、逐页文案和页面设计说明中因机械套版导致的重复字段、骨架填词和伪差异化。

字段职责与分层以 `core/field_differentiation_rules.md` 为唯一真相源。

## 2. 混合阈值模型

设：

```text
N = deck 页数
repeat_threshold = max(3, ceil(N * 0.5))
```

### 2.1 N <= 3 小包规则

- 对关键差异化字段做两两比较；
- 任意关键差异化字段全同：WARN；
- 两个及以上关键差异化字段全同：FAIL；
- `chart_visual_boundary` 或 `visual_notes` / page_design overrides 全同：FAIL；
- 若字段已下沉为 `global_design_defaults`，且每页 overrides 有足够差异，则不判 FAIL。

### 2.2 N >= 4 通用规则

- 关键差异化字段重复页数 >= `repeat_threshold`：FAIL；
- 关键差异化字段重复页数 >= 3 且 < `repeat_threshold`：WARN；
- 若字段已下沉为 `global_design_defaults`，且每页 overrides 有足够差异，则不判 FAIL；
- 页脚、基础配色、安全边距、全局负面风格边界等白名单字段不参与 FAIL 判定。

## 3. 必检字段

必检字段引用 `core/field_differentiation_rules.md` 的“必须逐页有设计增量”与“可半重复但必须带差异项”章节。

## 4. 语义检测

必须使用 `core/field_differentiation_rules.md` 中 `core_judgement`、`chart_proof_goal`、`chart_visual_boundary` 的 FAIL/PASS 特征与正反例进行判断。

## 5. 清单印章检测

### 5.1 检测目标

识别 `deck_spec.json`、逐页文案和页面设计说明中因过度依赖表格清单、卡片矩阵和同构版式导致的视觉疲劳与证明力退化。

清单印章检测不是反对高密度信息，而是防止高密度被错误实现为“连续清单堆叠”。Role A 必须证明每页为何需要当前主视觉结构，不能只替换标题、栏目名和指标名。

### 5.2 必检对象

至少检查以下字段或等价内容：

- `type`
- `layout_pattern`
- `chart_type`
- `chart_proof_goal`
- `chart_semantic_mapping.main_visual_logic`
- `chart_semantic_mapping.edge_roles`
- `chart_semantic_mapping.correspondence_pairs`
- `chart_visual_boundary`
- `visual_notes`
- page_design 中的主体区、图表区、卡片/表格/泳道/流程说明
- page_copy 中的图表说明、证据组织方式和讲解顺序

### 5.3 清单页判定：排版与图表双集并集

不得新增 deck_spec 字段。自检中临时计算 `is_list_page`，用于判断清单印章风险。

#### 5.3.1 清单特征集

自检逻辑只能使用项目已定义的标准枚举，不得新增或虚构版式名 / 图表类型。

```text
List_Layouts = [
  "three_column_cards",
  "multi_module_solution_overview",
  "metric_case_showcase_grid",
  "risk_decision_matrix"
]

List_Charts = [
  "key_findings_cards",
  "metric_showcase_grid",
  "case_gallery_cards",
  "comparison_table",
  "decision_table",
  "gap_heatmap"
]
```

若某页存在明显清单化风险，但其 `layout_pattern` 或 `chart_type` 不在上述集合中，不得临时创造新枚举；只能在 self_check 的证据说明中引用原始字段值，并建议后续单独扩展标准版式库。

#### 5.3.2 默认判定

对任意页面 P：

```text
if P.layout_pattern in List_Layouts
or P.chart_type in List_Charts:
  is_list_page = true
else:
  is_list_page = false
```

该规则用于堵住两类漏检：

- `chart_type` 填为 `none`，但 `layout_pattern` 仍是标准清单类排版；
- `layout_pattern` 写得较泛化，但 `chart_type` 实际是标准清单、表格或卡片网格。

#### 5.3.3 逻辑升级豁免

即使默认判定为清单页，若满足以下任一条件，可在 self_check 中说明证据，并将其豁免为非清单页：

- 升级为因果/流向图：page_design 显式要求箭头、流程线或主路径串联组件，且 `chart_semantic_mapping.main_visual_logic` 说明传导关系；
- 升级为关系图：`chart_semantic_mapping.edge_roles` 或 `correspondence_pairs` 明确声明拓扑传导、双分支、同层对应或层级支撑关系；
- 升级为决策门禁：页面核心为判断，且 page_design 明确要求判断分支、通过/不通过路径或决策条件树；
- 升级为运营闭环：`main_visual_logic` 明确声明“监控 -> 阈值触发 -> 决策 -> 动作 -> 效果回写”等反馈循环；
- 升级为拍板决策表：仅针对 `decision_table`，表格必须包含拍板事项、责任人、输入条件、验收物、风险闭环等控制域，而非只读参数清单；
- 表格作为辅助证据：page_design 明确另有主证明图，表格只承载补充证据。

若只是给卡片之间加装饰线、编号、淡箭头，但没有说明真实因果、钻取、门禁、血缘或闭环关系，不得豁免。

### 5.4 WARN / FAIL 规则

设：

```text
N = deck 页数
list_pages = is_list_page == true 的页面集合
```

#### 连续重复

- 连续 2 页均为 `is_list_page=true`：WARN；
- 连续 3 页及以上均为 `is_list_page=true`：FAIL；
- 连续 3 页 `layout_pattern + chart_type` 组合完全相同：WARN；
- 连续 4 页 `layout_pattern + chart_type` 组合完全相同：FAIL。

#### 全 deck 占比

全 deck 占比规则仅在 `N >= 4` 时启用。

- 当 `N >= 4`，`list_pages / N > 40%`：WARN；
- 当 `N >= 4`，`list_pages / N > 55%`：FAIL；
- 当 `N <= 3`，豁免全 deck 占比限制，仅执行连续重复与语义错配规则；
- 若 deck 明确为 appendix-heavy，可将占比 FAIL 降为 WARN，但正文页仍不得连续 3 页清单化。

#### 语义错配

以下任一情况直接 FAIL：

- `chart_proof_goal` 声明钻取、因果、门禁、血缘、闭环、决策或权衡关系，但 `layout_pattern` / page_design 只给出同权卡片或表格清单；
- 页面标题强调“路径、闭环、门禁、归因、演进、先后依赖”，但 page_design 未要求箭头、层级、条件、时间、关系线或主路径；
- `chart_visual_boundary` 写明“不得只是清单/卡片/表格”，但 page_design 主体仍是清单/卡片/表格；
- 页面中的卡片全部同权，无法判断主图、辅证和结论之间的阅读优先级；
- `main_visual_logic` 声明存在 `edge_roles` 或 `correspondence_pairs`，但 page_design 没有要求在视觉上呈现这些关系。

#### 标题换词但版式不变

若 3 页及以上满足以下条件，判 WARN；若 5 页及以上满足，判 FAIL：

- `layout_pattern + chart_type` 组合相同或高度相似；
- page_design 主体结构高度相似；
- 每页只是替换标题、栏目名、指标名；
- `chart_proof_goal` 的关系类型没有在主视觉中体现。

### 5.5 允许例外

以下情况不判 FAIL，但必须在 self_check 中说明：

- 附录页、指标字典页、字段字典页明确声明为 appendix/table；
- 用户明确要求“表格版/清单版/高密度字典版”；
- `N <= 3` 小包中的单页卡片/表格，不触发占比 WARN/FAIL；
- 连续清单页属于分包交付的一部分，但完整 deck 的宏观节奏仍满足要求；
- page_design 明确把表格作为辅助证据，且页面另有主证明图。

### 5.6 修复建议

命中 WARN/FAIL 时，Role A 必须优先替换主视觉结构，而不是只改措辞。

| 当前退化形态 | 优先替换为 |
|---|---|
| 指标卡片矩阵 | 分层指标树 / 运营闭环 / 主次 KPI rail |
| API 清单 | 用户动作泳道 / 调用路径 / 操作闭环 |
| 数据表名清单 | ER 图 / 数据血缘 / join path |
| 扩容条件清单 | 决策门禁 / 条件树 / 通过-不通过路径 |
| Trace 节点清单 | 瀑布图 / Span breakdown / 慢调用路径 |
| 阶段卡片 | 路线图 + 阶段门槛 + 验收物 |
| 拍板事项清单 | 决策表 + 责任人 + 输入 + 验收 + 风险 |

### 5.7 自检输出要求

每次生成交付物时，自检必须新增：

| 检查项 | 结果 | 证据 | 处理建议 |
|---|---|---|---|
| 清单页占比 | PASS/WARN/FAIL | `is_list_page=true` 页数 / N；N<=3 标注占比豁免 | 替换为证明型主视觉 |
| 连续清单检测 | PASS/WARN/FAIL | 连续页码 + `layout_pattern/chart_type` | 打散宏观节奏 |
| 同构版式检测 | PASS/WARN/FAIL | 重复 `layout_pattern + chart_type` 页码 | 改写 page_design 主体结构 |
| 语义错配检测 | PASS/WARN/FAIL | `chart_proof_goal` vs page_design | 补充链路/门禁/血缘/闭环图 |
| 逻辑升级豁免 | PASS/WARN/FAIL | 被豁免页码 + 因果/门禁/闭环/血缘证据 | 无证据则取消豁免 |
| 标题换词检测 | PASS/WARN/FAIL | 标题不同但版式相同的页码 | 重做主图与阅读路径 |

## 6. 视觉漂移印章检测

### 6.1 检测目标

识别多页重复使用暗色背景、暗红渐变、大红章节号、科技感网格或 `image_background_section_divider` 造成的发布会风模板印章。

### 6.2 必检触发词

检查 page_design、visual_notes、PPTX Builder 注意事项和 self_check 中是否出现以下词或等价表达：

- 暗色背景、暗红渐变、深红渐变、冷灰到深红渐变；
- 科技感背景、未来感、futuristic、炫光、霓虹、透视网格；
- 暗色智算中心拓扑背景、大图背景、背景图压底；
- 巨大红色章节号、超大章节数字、大面积红色块，黑色块；
- `image_background_section_divider`。

### 6.3 WARN / FAIL

- 单页普通封面或章节页命中上述触发词：WARN；
- 未经用户明确要求，普通封面页命中全屏暗色背景或暗红渐变：FAIL；
- 未经用户明确要求，章节页命中暗红/深灰渐变 + 大红章节号：FAIL；
- 2 页及以上章节页共享暗红渐变 + 大红章节号骨架：FAIL；
- 章节号成为页面最大视觉块：FAIL。

### 6.4 修复方式

命中 FAIL 时，必须改写 page_design：

- 暗色/暗红渐变改为白底或极浅灰底；
- 大红章节号改为小号章节标签或细红线；
- 大图背景改为淡灰工程线框或资源池轮廓；
- “提升视觉档次 / 科技氛围”改为“工程化、克制、有秩序”。

## 7. 可见版式术语检测

### 7.1 检测目标

识别 `deck_spec.json`、逐页文案、page_design 与最终 page_copy 中，是否存在将内部版式术语、区域名称、组件说明词错误输出为页面可见文字的问题。

该检测不是限制 Role A 使用版式术语进行设计说明，而是防止“版式说明词上屏”，导致页面出现模板痕迹、解释性噪声和自动套版感。

### 7.2 检测边界

本检测只检查页面可见字段，不检查内部设计说明。

#### 必检对象

至少检查以下最终可能进入页面画布的可见文案：

- page_copy 中的标题、副标题、模块标题、卡片标题、图表标题、右侧辅助区标题；
- deck_spec 中会被 Role C 消费为页面文字的字段；
- 逐页文案中的 visible bullets、visible labels、callout title、insight title；
- page_design 中明确标记为 visible text、visible heading、page visible copy 的内容；
- self_check 中标注为最终页面可见文案的内容。

正式汇报页正文要点中出现内部版式术语，按上屏污染处理；模板规范说明页、结构分析附录页除外。

#### 明确豁免对象

以下内容不纳入本检测：

- page_design 中的内部版式说明；
- layout_pattern、chart_type、chart_semantic_mapping 等结构字段；
- output_contract、terminology_dictionary、field dictionary 中的内部术语；
- self_check、handoff、status、交接单等非页面画布产物；
- 用于解释模板规范、页面结构或设计规则的附录页。

### 7.3 检测模式

本检测不做全文 contains，不把内部术语作为全局禁词；只检测页面可见字段中出现的“组件说明式标题”或“区域名上屏”模式。

#### 组件说明式标题禁止模式

```text
右侧洞察：xxx
洞察栏：xxx
右侧洞察栏：xxx
右侧栏：xxx
辅助解释区：xxx
主体区：xxx
图表区：xxx
文字区：xxx
强调区：xxx
底部结论条：xxx
卡片区：xxx
备注区：xxx
说明栏：xxx
```

#### 高风险模式

若以下术语单独作为页面可见标题、模块标题或卡片标题出现，也应判为高风险：

```text
洞察栏
右侧洞察栏
右侧洞察
右侧栏
辅助解释区
主体区
图表区
文字区
强调区
底部结论条
卡片区
备注区
说明栏
```

但这些词如果只出现在内部 page_design 说明中，不判 WARN / FAIL。

### 7.4 判定规则

对任意页面 P：

```text
if P.visible_fields matches Forbidden_Visible_Layout_Patterns:
  visible_layout_term_hit = true
else:
  visible_layout_term_hit = false
```

其中：

```text
visible_fields = 最终可能进入页面画布的可见标题、模块名、卡片标题、图表标题、callout 标题、右侧辅助区标题、正文要点、页脚以外说明文字。
```

禁止使用以下粗粒度检测方式：

```text
全文 contains "主体区"
全文 contains "图表区"
全文 contains "底部结论条"
```

原因是这些术语在内部设计说明中是合法术语，不应误伤。

### 7.5 WARN / FAIL 规则

#### 单页判定

- 页面可见文字中出现 1 处组件说明式标题禁止模式：FAIL；
- 页面主标题、副标题或一级模块标题中出现内部版式术语：FAIL；
- 页面可见文字中出现“右侧洞察：xxx”“洞察栏：xxx”“右侧洞察栏：xxx”等组件说明式标题：FAIL；
- 页面主标题、副标题、一级模块标题中单独出现区域名：FAIL；
- 二级卡片标题或辅助区标题中单独出现区域名：WARN；
- 同页 2 处及以上出现内部版式术语上屏：FAIL。

#### 全 deck 判定

- 全 deck 出现 2 页及以上 `visible_layout_term_hit=true`：FAIL；
- 连续 2 页出现类似“右侧洞察：xxx”的标题模式：FAIL；
- 同一版式术语在 3 页及以上作为页面可见标题重复出现：FAIL。

### 7.6 允许例外

以下情况不判 FAIL，但必须在 self_check 中说明：

- 术语只出现在 page_design 的内部设计说明中；
- 术语只出现在 `layout_pattern`、`chart_type`、`chart_semantic_mapping` 等结构字段中；
- 术语只出现在 self_check、handoff、status、交接单等非页面画布产物中；
- 用户明确要求展示版式结构分析，而不是生成正式汇报页面；
- 附录页用于解释模板规范、页面结构或设计规则。

### 7.7 修复方式

命中 WARN / FAIL 时，Role A 必须优先执行以下修复：

| 问题形态 | 修复方式 |
|---|---|
| “右侧洞察：验证边界” | 改为“验证边界” |
| “右侧洞察：迁移价值” | 改为“迁移价值” |
| “洞察栏：风险转换” | 改为“风险转换” |
| “右侧洞察：优先级” | 改为“优先级” |
| “右侧洞察：技术雷达应关注什么” | 改为“雷达关注点” |
| “主体区：核心链路” | 删除“主体区：”，保留“核心链路” |
| “图表区：验证路径” | 删除“图表区：”，保留“验证路径” |
| “底部结论条：建议动作” | 改为“建议动作”或直接保留结论句 |
| 多页重复出现“右侧洞察：xxx” | 删除标题，仅保留业务判断要点 |

修复优先级：

```text
删除版式标题 > 替换为业务语义标题 > 将第一条判断提升为短结论
```

禁止仅通过以下方式规避检测：

- 缩小字号；
- 降低透明度；
- 移到页面角落；
- 改成浅灰但仍保留；
- 把“右侧洞察：xxx”拆成两行显示。

### 7.8 推荐业务语义标题

若页面必须保留右侧辅助区标题，只允许使用业务语义标题：

| 页面类型 | 推荐标题 |
|---|---|
| 背景页 | 信号判断 |
| 催化页 | 触发因素 |
| 风险页 | 风险转换 |
| 应用页 | 验证边界 |
| 趋势页 | 趋势判断 |
| 行动页 | 优先级 |
| 方法页 | 迁移价值 |
| 对比页 | 关键差异 |
| 决策页 | 判断依据 |

### 7.9 自检输出要求

每次 Role A 输出交付物时，self_check 必须新增：

| 检查项 | 结果 | 证据 | 处理建议 |
|---|---|---|---|
| 可见版式术语检测 | PASS/WARN/FAIL | 命中页码 + 命中文案 + 所属可见字段；内部设计说明豁免证据 | 删除版式词 / 替换为业务语义标题 / 无标题化 |

## 8. 自检输出格式

每次生成交付物时，自检必须包含：

| 检查项 | 结果 | 证据 | 处理建议 |
|---|---|---|---|
| 重复字段统计 | PASS/WARN/FAIL | 字段名 + 重复页数 + 阈值 | 下沉全局默认 / 重写逐页字段 |
| 复述检测 | PASS/WARN/FAIL | 字段与来源文本 | 改为正当提炼或补充唯一带走点 |
| 骨架填词检测 | PASS/WARN/FAIL | 固定前后缀/关键词拼接证据 | 补充因果/对比/演进/闭环/决策关系 |
| 设计增量检测 | PASS/WARN/FAIL | 每页差异信号数量 | 补充主图/锚点/边界/讲解差异 |
| 清单印章检测 | PASS/WARN/FAIL | 清单页占比 + 连续页码 + 同构结构证据 + 逻辑升级豁免证据 | 替换为证明型主视觉 / 拆分附录 |
| 视觉漂移印章检测 | PASS/WARN/FAIL | 暗色/渐变/发布会触发词 + 页码 | 降级为白底工程化版式 |
| 可见版式术语检测 | PASS/WARN/FAIL | 命中页码 + 命中文案 + 所属可见字段；内部设计说明豁免证据 | 删除版式词 / 替换为业务语义标题 / 无标题化 |
| 允许重复项 | PASS | 白名单字段 | 保留或下沉全局默认 |

## 9. 失败处理

出现 FAIL 时，不得输出最终交付包；必须重写对应字段或将通用规则下沉为全局默认并补齐每页 overrides。

清单印章检测出现 FAIL 时，不得仅通过改标题、换栏目名或减少字数修复；必须重写 page_design 的主体结构，明确主视觉如何证明 `chart_proof_goal`。

视觉漂移印章检测出现 FAIL 时，不得仅通过降低亮度、减少光效或替换背景图修复；必须重写 page_design 的底色、章节号、红色锚点和版式模式，使其回到白底/浅灰底/细红线定锚的华为高层汇报风。

可见版式术语检测出现 FAIL 时，必须删除或替换页面可见字段中的版式术语；不得通过缩小字号、降低透明度、移动位置、拆分换行等视觉方式规避检测。

## 10. 图表组件印章检测

字段差异化判断以 `core/field_differentiation_rules.md` 第 8 节为唯一真相源。

### 10.1 页内两两检测

- supporting proof goal 与 primary 全同：FAIL；
- 任意两个 supporting proof goal 全同：FAIL；
- 同页两个组件仅 chart_type 不同，但证明目标和证据相同：WARN；
- 同页两个组件的 chart_visual_boundary 全同：FAIL；
- 组件数量增加但没有新增证明关系：FAIL。

### 10.2 跨页模板印章

- 页面级同构统计使用 `layout_pattern + primary.chart_type`；
- supporting 不得被用于伪造页面差异；
- 若 3 页及以上只替换 supporting 标签，而 primary、主视觉和证明关系不变：WARN；
- 若 5 页及以上满足上述条件：FAIL；
- `component_region`、组件数量和字段骨架本身不构成设计增量。

### 10.3 自检输出补充

| 检查项 | 结果 | 证据 | 处理建议 |
|---|---|---|---|
| 组件页内复述 | PASS/WARN/FAIL | 页码 + component_id + proof goal/boundary | 合并组件或重写增量目标 |
| 组件跨页印章 | PASS/WARN/FAIL | 重复 primary/supporting 组合和页码 | 重做主视觉关系，不只换标签 |
| 版式—区域兼容 | PASS/WARN/FAIL | layout + role + region | 更换合法槽位或拆页 |
