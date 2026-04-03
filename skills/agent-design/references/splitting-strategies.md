# 切分策略：功能切分 vs 场景切分

## 概述

Agent 切分的两大范式：
- **功能切分（Capability-based）**：按"能力类型"分解
- **场景切分（Scenario-based）**：按"工作流阶段"分解

两种策略各有优劣，选择取决于任务特征。

---

## 1. 功能切分（Capability-based）

### 核心理念

将任务按照"能力类型"分解，每种能力有明确的工具边界和行为模式。

### 典型 Agent 类型

| Agent | 能力 | 工具集 | 行为模式 |
|-------|------|--------|----------|
| **explore** | 只读搜索 | `Read`, `Grep`, `Glob` | 探索代码库，返回摘要 |
| **plan** | 规划分析 | `Read`, `Grep` | 分析结构，输出计划 |
| **analyze** | 深度分析 | `Read`, `Grep`, `Bash` | 复杂推理，不修改 |
| **implement** | 代码实现 | `Read`, `Write`, `Edit` | 实现功能，写代码 |
| **review** | 代码审查 | `Read`, `Grep` | 审查质量，不修改 |

### 优势

1. **通用性强**：explore agent 可用于任何项目的代码探索
2. **工具边界清晰**：每个 agent 只拥有特定工具集
3. **可复用性高**：能力原语可在不同项目中复用
4. **并行化友好**：独立上下文，适合并行执行

### 劣势

1. **协调成本高**：需要 orchestrator 组装多个 agent
2. **端到端体验差**：用户需要等待多个 agent 依次执行
3. **上下文切换频繁**：任务在多个 agent 间传递

### 适用场景

✅ **适合功能切分：**
- 探索型任务（需要大范围搜索）
- 分析型任务（需要深度推理）
- 审查型任务（需要多维度评估）
- 并行化需求高（可独立执行）

❌ **不适合功能切分：**
- 端到端流程（写测试 → 运行 → 修复）
- 高上下文连续性的任务（UI 开发全流程）
- 步骤间强依赖（必须顺序执行）

### 示例：代码库探索

```yaml
# 内置 explore agent（功能切分）
description: "Read-only agent for searching and analyzing"
tools: [Read, Grep, Glob]
permission:
  read: allow
  write: deny
  edit: deny
```

**使用场景：**
```
用户: "Find all usages of AuthService"
主 Agent → Task(explore): "搜索 AuthService 所有用法"
explore agent → 返回摘要: "在 12 个文件中找到 28 处用法"
主 Agent → 基于摘要决策下一步
```

---

## 2. 场景切分（Scenario-based）

### 核心理念

将任务按照"工作流阶段"分解，每个场景是多种能力的组合。

### 典型 Agent 类型

| Agent | 场景 | 能力组合 | 工具集 |
|-------|------|----------|--------|
| **test-engineer** | 测试开发 | 写测试 + 运行 + 分析 | `Read`, `Write`, `Edit`, `Bash` |
| **dev** | 功能开发 | 设计 + 实现 + 调试 | `Read`, `Write`, `Edit`, `Bash` |
| **build-engineer** | 构建排错 | 构建 + 分析 + 修复 | `Read`, `Bash`, `Edit` |
| **docs-writer** | 文档编写 | 分析 + 生成 + 格式化 | `Read`, `Write`, `Edit` |

### 优势

1. **端到端体验好**：一个 agent 完成完整流程
2. **上下文连续**：不需要在多个 agent 间传递上下文
3. **协调成本低**：主 agent 只需调用一次
4. **职责清晰**：按工作流阶段定义，用户易理解

### 劣势

1. **通用性低**：test-engineer 只能用于测试场景
2. **工具集复杂**：需要多种工具组合
3. **可复用性低**：场景特定，难以跨项目复用
4. **职责可能膨胀**：如果不注意，可能变成"万能 agent"

### 适用场景

✅ **适合场景切分：**
- 端到端流程（测试、开发、构建）
- 高上下文连续性的任务（同一代码库内操作）
- 工作流阶段明确（需求 → 设计 → 实现 → 测试）
- 技术栈边界清晰（UI/后端/数据层）

❌ **不适合场景切分：**
- 通用探索任务（不需要特定场景）
- 需要高度并行化（场景 agent 通常是串行的）
- 工具集差异小（没必要拆分）

### 示例：Android 开发团队

```yaml
# android-dev（场景切分）
description: "Android 开发专家：处理 Kotlin + Jetpack + 架构。用于新功能开发、架构设计时。"
tools: [Read, Write, Edit, Bash]
permission:
  read: allow
  write: allow
  edit: allow
  bash: allow
```

```yaml
# android-test-engineer（场景切分）
description: "Android 测试专家：处理单元测试 + MockK。用于业务逻辑测试，不参与 UI 开发。"
tools: [Read, Write, Edit, Bash]
permission:
  read: allow
  write: allow
  edit: allow
  bash: allow
```

**使用场景：**
```
用户: "Implement user authentication"
主 Agent → Task(android-dev): "实现用户认证功能"
android-dev → 端到端完成（设计 + 实现 + 初步调试）
主 Agent → Task(android-test-engineer): "为认证功能写测试"
android-test-engineer → 端到端完成（写测试 + 运行 + 修复）
```

---

## 3. 混合策略（推荐）

### 分层架构

```
Level 1: 能力原语（功能切分）
├── explore → 只读搜索（通用）
├── analyze → 深度分析（通用）
└── implement → 代码实现（通用）

Level 2: 场景角色（场景切分）
├── test-engineer → 使用 explore + implement
├── dev → 使用 analyze + implement
└── build-engineer → 使用 implement + analyze

Level 3: 工作流编排（主 Agent）
└── 按阶段调用 Level 2 场景角色
```

### 为什么混合更好？

1. **Level 1（能力原语）**：内置 agent 提供通用能力
2. **Level 2（场景角色）**：用户自定义 agent 提供端到端体验
3. **Level 3（编排）**：主 agent 协调，保持灵活性

### 实际案例：Claude Code 设计

Claude Code 采用混合策略：
- **内置 agent（功能切分）**：explore、plan、general
- **用户自定义 agent（场景切分）**：test-engineer、security-auditor 等
- **主 Agent 编排**：根据任务选择调用哪个 agent

---

## 4. 决策指南

### 选择流程

```
评估任务特征
    │
    ├─ 上下文共享度 > 50%？
    │   ├─ 是 → 场景切分（保持连续性）
    │   └─ 否 → 继续
    │
    ├─ 工具能力差异大？
    │   ├─ 是 → 功能切分（专业化）
    │   └─ 否 → 继续
    │
    ├─ 需要并行执行？
    │   ├─ 是 → 功能切分（独立上下文）
    │   └─ 否 → 场景切分（减少协调）
    │
    └─ 端到端流程？
        ├─ 是 → 场景切分（完整体验）
        └─ 否 → 功能切分（灵活组合）
```

### 快速判断表

| 特征 | 功能切分 | 场景切分 |
|------|---------|---------|
| 探索代码库 | ✅ 适合 | ❌ 不适合 |
| 端到端测试 | ❌ 不适合 | ✅ 适合 |
| 并行分析 | ✅ 适合 | ❌ 不适合 |
| 功能开发 | ⚠️ 可组合 | ✅ 适合 |
| 多维度审查 | ✅ 适合 | ⚠️ 可扩展 |
| CI/CD 流程 | ⚠️ 可组合 | ✅ 适合 |

---

## 5. 常见错误

### 错误 1：过度功能切分

❌ **问题**：将端到端流程拆成太多小 agent
```
test-write → test-run → test-analyze → test-report
```
**后果**：上下文反复传递，协调成本高

✅ **修复**：合并为场景 agent
```
test-engineer（端到端）
```

### 错误 2：场景 agent 膨胀

❌ **问题**：场景 agent 变成"万能 agent"
```
super-dev: 能写代码、能测试、能部署、能写文档...
```
**后果**：职责不清，难以维护

✅ **修复**：按场景边界拆分
```
dev + test-engineer + build-engineer + docs-writer
```

### 错误 3：忽视上下文亲和度

❌ **问题**：将高亲和度任务拆给不同 agent
```
UI 设计 → UI 实现 → UI 测试（3 个 agent）
```
**后果**：上下文在 agent 间反复传递

✅ **修复**：保持高亲和度任务在一起
```
android-ui-engineer（设计 + 实现 + 测试）
```

---

## 6. 最佳实践总结

1. **内置 agent 用功能切分**：提供通用能力原语
2. **自定义 agent 用场景切分**：提供端到端体验
3. **主 agent 负责编排**：灵活组合不同 agent
4. **保持 3-5 个 agent**：过多导致协调复杂
5. **定期重构**：随着项目演进调整 agent 边界

---

## Related

- `decision-framework.md` - 完整决策框架
- `architecture-patterns.md` - 4 大架构模式详解
- `common-mistakes.md` - 常见设计错误
