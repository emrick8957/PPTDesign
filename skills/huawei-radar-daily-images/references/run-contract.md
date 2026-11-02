# 运行记录协议

辅助命令详见 `python skills/huawei-radar-daily-images/scripts/run.py --help`。脚本只校验可机器检查的条件，不能证实审稿者真的看过图。独立任务原始记录是审核来源。

input/reading-receipt.json：word_hash、date、full_word_read=true、golden_viewed=[1..10]、rule_files（实际完整读取的规则相对路径列表）、source_notes（原文差异和事实边界的非空说明）。不允许先填true再补读。

role-c/self-check.json：binding为binding命令原样结果；pages为恰好1..10条{page,score,hard_failures,notes}；分数为执行者自检。另写refinement-report.md记录每页C2.5/C2.6/C4的真实工具调用、原因与选择，cross-page-review.md记录C4.1及总览实际查看结果。

独立review.json：binding原样；reviewer为独立身份且不能等于run.actor；reviewer_task为实际任务ID；verdict=PASS或FAIL；pages恰好1..10，每项{page,viewed:true,verdict,notes}。备注必须是本页的事实/字形/关系/视觉判断。附review.md记录问题、严重度、修复及残余项。PASS绑定全部最终图；任何换图需新审核，不能拷贝旧绑定。

项目固定配置不可为复跑临时改动。设计冻结后事实/文案发生变化时，prepare --revision 一个有说明的新修订标识；revision进入身份，旧设计、图片、审核保留；同revision仍复用。只改图片走C4，审核自动失效。

独立审核sources_checked记录实际核查、允许出现在本地公共manifest的来源URL；禁止私有路径、内网地址和凭据。打包仅采纳已批准报告中的这些链接，并删除查询参数以避免夹带临时令牌。没有链接时输出空列表，不编造来源。

`references/project.json` 的 `upstream_lock_sha256` 绑定 `vendor/upstream/bundle.lock.json` 的入库字节。`verify` 在这份摘要不一致时退出，并给出期望摘要与实际摘要；若只有换行不同，错误写明 line ending mismatch。失败回报第一行写 `任务: 华为日报精读图片`，并原样引用该错误。verify 未通过时不创建 run。

命令成功退出0，失败退出1；JSON状态保存于run/state.json。状态含READING、PREPARATION_BLOCKED、READY_FOR_DESIGN、DESIGN_AUTHORIZED、DESIGNED、GENERATING、REVIEW_PENDING、APPROVED、DELIVERED。明确零信号单独SKIPPED记录，无Word/no-image；跳过不能算十页验收通过。

日期歧义澄清：prepare可加--date-evidence JSON，字段date、authority=user、quote（Word内逐字可定位且只含所选日期）、reason（至少10字符，记录用户确认依据）。只解决来源中存在的日期歧义，不能把唯一明确报告日期改成其他日期；原Word不改。确认JSON哈希进入运行身份，input/date-resolution.json保存解析依据。正文论文/事件日期仅保留在body_dates中，不作为报告日期冲突。

## v1.2 准备与启动字段

reading-receipt保留word_hash/date/full_word_read/golden_viewed/rule_files/source_notes，并增加：
- blockers: []（未解决关键问题不可为空）；capabilities: {imagegen:true,view_image:true,independent_review:true}。
- assets: [{path: 相对Skill路径, sha256: 实际摘要, status: READ, evidence: 真实读取或看图工具消息引用}]。覆盖reading-manifest全部required_rules/required_images，无重复；rule_files按manifest顺序填写。额外失败材料在准备报告中逐项说明。
- signals: 每条{id,word_locator,claims,source_status}。claims列出有证据支持的断言及事实/分析/演示类型；source_status为READ/WORD_SUFFICIENT/UNAVAILABLE。READ另填url,sections,read_at,snapshot（run内input/路径）,sha256；其余填reason；UNAVAILABLE须另列excluded_claims。是否覆盖日报全部信号由实际阅读复核，不以列表非空替代。

ready校验成功绑定资源和来源快照，返回readiness_token；失败写PREPARATION_BLOCKED及preparation_error。ready不产生设计、图或调用模型。start需后续真实用户Step2指令记录，字段见two-stage-workflow。设计与生成不接受仅READING/READY_FOR_DESIGN状态。

独立review.json每页增加hard_failures: []及checks对象。键必须覆盖visual-contract.review_checks，每项{verdict:PASS或FAIL,evidence:本页观察及定位}。有任何硬失败或缺少逐项证据，不得approve。脚本不能替代视觉判断，不能自动证明坐标/箭头正确。

role-a/design-audit.json在Step2设计期间生成：visual_contract为项目visual-contract.json完整内容；pages恰好1至10，每页包含page、layout_mapping（中文结构与合法枚举映射）、selection_reason、evidence_locations、supporting_increment、relationship_check及hard_failures:[]。无辅助组件或关系图时给出不适用理由，不留空。design检查此审计后才编译上游合同，文件随role-a设计一起冻结。实际含义与图中落实由独立审核判断，非空字段不代表语义正确。
