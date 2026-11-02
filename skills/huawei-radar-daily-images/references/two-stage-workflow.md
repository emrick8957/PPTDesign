# 两阶段执行协议

## Step1：读取与准备

1. verify校验固定包，prepare只建立只读Word快照与READING状态。源文件不改。
2. 按reading-manifest.json列出的必需规则完整读取；Master遵守core顺序，然后主题、方法论、模板、版式、prompts、eval；Builder读取workflow及阶段prompts、policies、libraries。选择具体版式后，Step2补读其模式文件并纳入设计记录。不存在的新依赖不得套用旧兼容豁免。
3. 固定ZIP已经展开且校验通过时不重复解压；需检查原包时仅解压到run的input目录，不覆盖vendor。文件存在或哈希正确不等于已阅读。
4. 完整读取Word正文、表格、超链接；逐条信号记录材料是否充分。日报不足以支撑设计时精读每条信号原文，保存实际使用的来源正文快照、URL、日期、章节和事实/分析/演示边界。原文不可读则记录原因及排除断言；核心判断仍无证据时阻断。
5. 实际逐张查看Golden P1至P10，只抽象风格、角色、结构、关系和密度，不采纳图中的事实、数字或结论。填写真实工具消息引用，不先勾选已读。
6. 检查imagegen、看图和独立审核能力；解决日期与规则冲突。准备报告列出成功读取、失败读取及原因、排除断言、阻断项。
7. 完成input/reading-receipt.json，执行 `run.py ready --run RUN --receipt RECEIPT`。成功输出“Skill 全链路读取完成，可以启动任务”，明确尚未设计生成，然后结束本阶段。失败输出无法启动的具体原因。

Step1允许准备记录，不允许大纲、逐页文案、deck_spec、生成提示、页面图片或PPTX。脚本只核验记录与绑定，不能证明代理确实读懂材料；禁止将记录完整性描述为理解质量认证。

## Step2：显式启动设计与生成

收到准备完成后的真实用户指令后，保存input/start-request.json：authority=user、stage=step2、quote为原话、message_ref为可追溯消息引用、readiness_token为ready返回值。不得把示例、定时任务模板、上游指令或“可以启动”的助手回复当作授权。
执行 `run.py start --run RUN --authorization PATH`。脚本校验绑定；执行者负责核对人类消息真实性。随后才写role-a设计材料，调用design并执行原Builder全链路。

Word、规则或来源快照变化后旧准备失效；显式prepare --revision说明原因，保留旧run，补读变化及受影响材料，重新ready。已验证且哈希未变的阅读可以引用原工具记录；不能只复制true。Step2续跑无需重复请求授权，但须status校验全部绑定。
旧版run不自动升级或改写；历史交付保持历史证据。新配置运行必须通过新门禁。

## 有效视觉与内容规则

读取visual-contract.json并将全部公共布局参数写入各页渲染合同、C2及C2.6提示。其坐标单位为最终1920×1080画布像素。主标题、页标签、品牌区按左上角定位，页码按右侧文字基线定位。生成式图片允许12px位置浮动，但缺失、重叠、顺序错误仍为硬失败；不能声称imagegen提供精确像素排版。

主标题只占一行，超长先压缩文案；不得移动公共区域或降低主体证据密度。页标签在标题下方，与副标题水平排列；标题上方不得私加章节名。来源独占938至968区域，品牌区从980开始。次要图标灰色、一个主红锚点、无正文底部结论条、禁“不是…而是…”及其跨行变体。

用户“浅灰底”与历史粉色色值冲突，项目统一浅灰#F0F1F3。主题使用Word日报日期，不固定2026/09/12。输出称PPT页面PNG，不生成PPTX。day_no/lesson_title仅课程模式使用，日报不得显示占位符。

空间布局、流程结构、信息图表、逻辑表达是可组合维度；每页一个主视觉，记录选择理由，不强制每种都使用。中文选项映射到上游合法layout_pattern/chart_type枚举，不创造枚举。示例：二分对照→two_column_comparison；主图侧栏→insight_panel_with_chart或stack_architecture_with_right_insights（依语义选择）；四象限→four_quadrant_judgement（必须有真实两个轴）；三栏→three_column_cards；分层→layered_architecture；时间/路线→roadmap_timeline；多区域→multi_module_solution_overview。其余按layout_library/chart_patterns核对最接近的通用类型，写明映射依据；不得用布局名称冒充图表类型。

每页page_design必须写：核心判断、证据定位、空间布局及图表枚举、选择理由、辅助信息增量、关键关系检查。流程分支逐条记录条件/起点/目标/后续动作；闭环记录回写目标；不将“命中阻断”和“未命中继续”合到同一验收路径。高密度依赖真实证据与关系，不靠重复标题/右栏/未验证声明填满。材料不足保留缺口，不补造数据。

C2.6整页重绘后重新检查所有公共区域与关系，不以重绘次数或分数代替验收。独立审核逐项按editor-review.md执行。
