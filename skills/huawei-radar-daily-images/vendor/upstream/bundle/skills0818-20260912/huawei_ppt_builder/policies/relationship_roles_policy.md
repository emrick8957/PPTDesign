# 关系角色策略 v0.4.2

## correspondence_pairs

当 deck_spec 声明 correspondence_pairs 时，每一对 `{left, right}` 必须渲染为：

- 同层；
- 水平对齐；
- 直接连接；
- 不交叉；
- 不向中心发散；
- 不跨层连接；
- 不丢失任何一对。

字段名 `correspondence_pairs`、`left`、`right` 不得上屏。

## edge_roles

### flow_decompose

语义：自顶向下分解。

要求：方向向下，箭头或结构层级必须可见。

### flow_integrate

语义：自底向上集成。

要求：方向向上，不能画成普通并列箭头。

### lifecycle_close

语义：生命周期收尾。

要求：弱化，不得与主结构同权。

### feedback_loop

语义：闭环回写。

要求：必须形成闭合回路，回写方向必须可见。

## 禁止

- 把角色名写到页面上；
- 把 flow_decompose 等字段名当连线标签；
- 用无箭头直线表达方向关系；
- 用装饰性环线替代真实闭环；
- 把收尾节点画成主红色锚点。
