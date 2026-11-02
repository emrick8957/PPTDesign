# huawei_ppt_master_skill_v0_2 本次升级文件清单

## 一、根目录文件

| 文件 | 状态 | 说明 |
|---|---|---|
| `SKILL.md` | 修改 | 重新定义为通用华为风格 PPT Skill；增加主题路由与防污染规则 |
| `README.md` | 修改 | 增加 v0.2 定位、安装方式、三/四角色协同说明 |
| `VERSION.md` | 新增 | 记录当前版本与版本定位 |
| `CHANGELOG.md` | 新增 | 记录 v0.2 相对 v0.1 的升级内容 |
| `UPGRADE_FILE_LIST_v0.2.md` | 新增 | 本文件，列出本次升级文件清单 |

## 二、core/ 通用生成内核

| 文件 | 状态 | 说明 |
|---|---|---|
| `core/generation_workflow.md` | 新增 | 定义从主题识别到大纲、文案、页面设计的通用流程 |
| `core/topic_router.md` | 新增 | 定义如何选择 default_general 或特定 domain_profile |
| `core/output_contracts.md` | 新增 | 定义大纲、逐页文案、页面设计说明、deck_spec 的输出字段 |
| `core/anti_overfit_rules.md` | 新增 | 防止昇腾/NVIDIA/AI算力内容污染其他主题 |
| `core/audience_rules.md` | 新增 | 定义高层、客户、技术团队、项目团队等对象的表达差异 |

## 三、templates/ 通用模板库

| 文件 | 状态 | 说明 |
|---|---|---|
| `templates/page_types.md` | 修改 | 扩展为通用页型库，不再绑定 AI 算力主题 |
| `templates/narrative_patterns.md` | 修改 | 增加战略规划、技术方案、客户方案、复盘、运营治理等叙事结构 |
| `templates/visual_rules.md` | 修改 | 融入本次版式截图的视觉规律 |
| `templates/chart_patterns.md` | 修改 | 通用图表模式与主题专属图表解耦 |
| `templates/wording_rules.md` | 修改 | 移除全局昇腾专属句式，保留通用华为式表达规则 |
| `templates/huawei_style_reference.md` | 保留/修改 | 保留 v0.1 华为模板提取规则，并补充截图版式特征 |

## 四、domain_profiles/ 主题知识包

| 文件 | 状态 | 说明 |
|---|---|---|
| `domain_profiles/default_general.md` | 新增 | 默认通用主题包 |
| `domain_profiles/ai_compute_ascend_nvidia.md` | 新增 | 昇腾/NVIDIA/AI算力主题包 |
| `domain_profiles/gov_public_security.md` | 新增 | 公安政务主题包 |
| `domain_profiles/ai_platform.md` | 新增 | AI平台/模型平台主题包 |
| `domain_profiles/project_operation.md` | 新增 | 持续运营/项目运营主题包 |
| `domain_profiles/customer_solution.md` | 新增 | 客户方案主题包 |
| `domain_profiles/data_governance.md` | 新增 | 数据治理主题包 |
| `domain_profiles/cybersecurity.md` | 新增 | 网络安全/安全运营主题包 |

## 五、visual_patterns/ 版式模式库

| 文件 | 状态 | 说明 |
|---|---|---|
| `visual_patterns/screenshot_layout_analysis.md` | 新增 | 对附件版式截图的抽象分析 |
| `visual_patterns/layout_library.md` | 新增 | 通用页面版式库 |
| `visual_patterns/executive_summary_patterns.md` | 新增 | 高层总览页模式 |
| `visual_patterns/comparison_page_patterns.md` | 新增 | 对比页模式 |
| `visual_patterns/architecture_page_patterns.md` | 新增 | 架构/分层/栈式页面模式 |
| `visual_patterns/roadmap_page_patterns.md` | 新增 | 路线图/演进图模式 |
| `visual_patterns/risk_decision_patterns.md` | 新增 | 风险与决策页模式 |

## 六、eval/ 测试与验收

| 文件 | 状态 | 说明 |
|---|---|---|
| `eval/acceptance_checklist.md` | 修改 | 增加通用主题、页面设计、主题防污染验收项 |
| `eval/regression_cases.md` | 修改 | 增加非 AI 算力主题测试 |
| `eval/visual_scorecard.md` | 新增 | 版式与视觉质量评分表 |
| `eval/domain_contamination_tests.md` | 新增 | 检查主题专属术语是否误入通用主题 |

## 七、prompts/ 提示词

| 文件 | 状态 | 说明 |
|---|---|---|
| `prompts/generate_outline.md` | 新增 | 大纲生成提示词 |
| `prompts/generate_page_copy.md` | 新增 | 逐页文案生成提示词 |
| `prompts/generate_page_design.md` | 新增 | 页面设计说明生成提示词 |
| `prompts/screenshot_analysis.md` | 新增 | 截图版式分析提示词 |
| `prompts/deck_spec_generation.md` | 新增 | 生成 PPTX Builder 输入的提示词 |
| `prompts/self_review.md` | 新增 | 自检提示词 |
