# References Index

## 核心参考文档

### 决策与原则
- [`decision-framework.md`](decision-framework.md) - Agent 设计核心原则
  - Conway's Law for Agents
  - Context Affinity（上下文亲和度）
  - Single Responsibility + Composability
  - 权限最小化原则
  - Token 经济性
  - 设计决策树

### 切分策略
- [`splitting-strategies.md`](splitting-strategies.md) - 功能切分 vs 场景切分
  - 功能切分详解
  - 场景切分详解
  - 混合策略（推荐）
  - 决策指南
  - 常见错误

### 架构模式
- [`architecture-patterns.md`](architecture-patterns.md) - 4 大架构模式
  - Orchestrator-Worker
  - Hierarchical
  - Peer-to-Peer
  - Pipeline
  - 模式对比与选择

### 错误与修复
- [`common-mistakes.md`](common-mistakes.md) - 常见设计错误
  - 过度拆分
  - 万能 Agent
  - 工具集冗余
  - 上下文污染
  - 权限过度
  - 触发模糊
  - 资源罗列
  - 缺乏约束
  - 模型选择不当
  - 跳过设计直接创建

### 评估指南
- [`evaluation-guide.md`](evaluation-guide.md) - 如何评估 Agent 设计质量
  - 6 大评估维度
  - 评分公式
  - 评估流程
  - 持续改进

---

## 模板目录

位于 `../assets/templates/`：

- [`capability-based.md`](../assets/templates/capability-based.md) - 功能切分 Agent 模板
- [`scenario-based.md`](../assets/templates/scenario-based.md) - 场景切分 Agent 模板
- [`orchestrator-worker.md`](../assets/templates/orchestrator-worker.md) - 编排者模式模板

---

## 使用指南

### 新手入门

1. 先读 [`decision-framework.md`](decision-framework.md) 理解核心原则
2. 根据任务特征选择切分策略（[`splitting-strategies.md`](splitting-strategies.md)）
3. 参考对应模板创建 Agent
4. 用 [`evaluation-guide.md`](evaluation-guide.md) 评估设计质量

### 设计审查

创建 Agent 前，检查 [`common-mistakes.md`](common-mistakes.md)：
- 是否犯了常见错误？
- 如何修复？

### 架构选择

不确定用哪种架构？查看 [`architecture-patterns.md`](architecture-patterns.md)：
- 模式对比表
- 决策树
- 代表实现

---

## 快速参考

### 决策矩阵（摘要）

| 维度 | 功能切分 | 场景切分 |
|------|---------|---------|
| 上下文共享 | 低 | 高 |
| 工具差异 | 大 | 小 |
| 可复用性 | 高 | 中 |
| 协调成本 | 高 | 低 |
| 适合场景 | 探索、分析、审查 | 开发、测试、构建 |

### 架构模式选择

| 场景 | 推荐模式 |
|------|---------|
| 复杂研究、多数据源 | Orchestrator-Worker |
| 大型项目、多阶段 | Hierarchical |
| 多专家会诊 | Peer-to-Peer |
| CI/CD、流程化 | Pipeline |

### 3 步设计检查清单

```
Step 1: 评估任务特征
  □ 任务间上下文共享度 > 50%？→ 场景切分
  □ 工具能力差异大？→ 功能切分
  □ 需要并行执行？→ 功能切分

Step 2: 定义 agent 边界
  □ 输入：明确的任务描述 + 上下文范围
  □ 输出：可交付的单一结果
  □ 工具：最少必要集（2-5 个工具）

Step 3: 验证设计合理性
  □ 如果去掉这个 agent，主 agent 工作量增加 > 2x？→ 保留
  □ agent 职责能用 1 句话描述清楚？→ 保留
  □ 和其他 agent 共享工具集完全相同？→ 考虑合并
```

---

## 相关技能

- `agent-creator` - 执行创建 Agent（与 agent-design 互补）
- `model-guide` - 模型选择指导

---

## 更新日志

- **2026-04-03**: 初始版本，包含 5 篇参考文档和 3 个模板
