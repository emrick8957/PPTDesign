# huawei_ppt_master 主题路由与术语边界速查表

> 用途：快速查看“主题 → 触发包 → 允许/禁止词”的规则。
> 适用 Skill：`huawei_ppt_master`
> 更新时间：2026-05-02

## 总表

| 主题类型 | 触发的 domain profile | 典型触发词 | 允许重点术语 | 禁止无故出现 |
|---|---|---|---|---|
| 通用汇报 / 无明确领域 | `default_general.md` | 无明确领域词 | 业务目标、当前问题、建设思路、核心能力、实施路径、风险保障、决策建议 | 昇腾、英伟达、NVIDIA、CUDA、CANN、GPU、NPU、模型迁移、算力调度 |
| AI算力 / 昇腾-NVIDIA | `ai_compute_ascend_nvidia.md` | 昇腾、Ascend、英伟达、NVIDIA、GPU、NPU、CUDA、CANN、算力、训练、推理 | 硬件、软件栈、生态、模型迁移、集群互联、算力闭环、供应链 | 无此类限制，属于合法主题术语 |
| 公安 / 政务 | `gov_public_security.md` | 公安、市局、分局、区县、政务、警情、视频解析、公共安全 | 市局/区县部署、视频解析、警情研判、治理闭环、实战场景 | 除非用户明确提 AI 算力，否则不能带入昇腾/NVIDIA/CUDA/GPU |
| AI平台 / 模型平台 | `ai_platform.md` | AI平台、模型平台、大模型平台、MLOps、模型服务、训练平台 | 模型管理、训练服务、推理服务、平台能力、统一纳管 | 若未提算力底座，不应强行带昇腾/NVIDIA |
| 持续运营 / 运维治理 | `project_operation.md` | 持续运营、运维、运营规划、SLA、指标体系、年度运营 | 运营机制、服务保障、考核闭环、运维治理 | 不得误写成芯片/算力方案 |
| 客户方案 / 售前方案 | `customer_solution.md` | 客户汇报、解决方案、客户方案、行业方案、售前、价值主张 | 客户痛点、方案价值、交付路径、合作模式 | 除非客户题目明确是 AI算力，否则禁带昇腾/NVIDIA |
| 数据治理 | `data_governance.md` | 数据治理、数据资产、数据质量、数据标准、数据目录 | 数据资产、数据标准、质量治理、指标体系 | 禁止 GPU/NPU/CUDA/CANN 等 AI算力词 |
| 网络安全 | `cybersecurity.md` | 网络安全、安全运营、SOC、漏洞、等保、合规 | 安全运营、风险防控、主机安全、威胁治理、合规 | 禁止误引入算力芯片体系词 |

## 快速结论

1. 先看主题有没有明确领域词。
2. 没命中专属领域时，默认走 `default_general.md`。
3. 只要不是明确 AI 算力主题，就要严格防止昇腾/NVIDIA/CUDA/CANN/GPU/NPU 污染。
4. 这张表优先用于：Skill 检查、路由解释、输出前自检。

## 推荐调取方式

- 直接读取：`skills/huawei_ppt_master/REFERENCE_ROUTING_TABLE.md`
- 若只想看入口说明，再读：`skills/huawei_ppt_master/QUICK_INDEX.md`
