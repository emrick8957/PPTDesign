# Tools

这些脚本提供确定性辅助，不替代逐页视觉判断。

- `validate_inputs.py`：校验输入文件、JSON、页码、合同模式、图表组件数量/引用、版式—区域兼容、合法枚举和逐组件复杂关系字段。
- `render_contract_builder.py`：从完整输入目录编译逐页施工合同；归一化新/旧图表合同，从唯一主图表组件派生主图投影并输出逐组件 coverage。
- `validate_recomposition.py`：校验视觉基线与有效渲染方案的真实差异、语义不变量、图表转换、版式区域、证据覆盖和重构审计。
- `score_self_check.py`：汇总报告中的逐页分数，并判断是否达到 92 分交付阈值。
- `validate_refinement.py`：阻止低分页面、一票失败项、L 型红线、重复骨架或高密度 underfill 进入交付。
- `pack_delivery.py`：打包交付目录。
- `run_contract_regression.py`：使用最新 Role A 交付快照验证 A → C 合同边界、枚举门禁、关系角色、结构化可见内容 coverage、fallback 和自检强门禁。
- `run_component_contract_regression.py`：执行 `MC2-RT-01` 至 `MC2-RT-25` 多图表组件合同回归。
- `run_recomposition_regression.py`：执行 `AVR-RT-01` 至 `AVR-RT-28` 自适应视觉重构回归。
