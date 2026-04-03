# 架构模式：4 大 Agent 协作模式

## 概述

多 Agent 系统的 4 种核心架构模式：
1. **Orchestrator-Worker**（编排者-工作者）
2. **Hierarchical**（层级嵌套）
3. **Peer-to-Peer**（平等协作）
4. **Pipeline**（流水线）

---

## 1. Orchestrator-Worker（编排者-工作者）

### 模式描述

一个中心 Agent（Orchestrator）负责任务分解和协调，多个 Worker Agent 并行执行子任务。

```
┌─────────────────────────────────────────┐
│         Orchestrator (Opus)             │
│    战略分析 + 任务分解 + 结果综合        │
└──────────────────┬──────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌───────┐    ┌───────┐    ┌───────┐
│Worker A│    │Worker B│    │Worker C│
│(Sonnet)│    │(Sonnet)│    │(Sonnet)│
└───────┘    └───────┘    └───────┘
文档研究      代码分析      问题排查
```

### 关键特征

- **单点协调**：Orchestrator 是唯一的决策者
- **并行执行**：Worker 可以并行运行
- **结果综合**：Orchestrator 整合 Worker 输出
- **模型分层**：通常 Orchestrator 用强模型（Opus），Worker 用中等模型（Sonnet）

### 适用场景

✅ **适合：**
- 复杂研究任务（多数据源分析）
- 需要并行探索的问题
- 结果需要综合决策的场景

❌ **不适合：**
- 简单任务（协调 overhead 不值得）
- 步骤间强依赖（无法并行）
- 实时性要求高（并行增加延迟）

### 代表实现

**Anthropic 研究系统**：
- Lead Agent（Orchestrator）：Opus 4，分析查询、制定策略、协调
- Subagents（Workers）：Sonnet 4，并行探索特定方面
- 性能提升：**90.2%** 相比单 Agent

### 优缺点

| 优点 | 缺点 |
|------|------|
| 并行化效率高 | 协调 overhead 大 |
| 任务分解清晰 | 单点故障风险 |
| 结果综合全面 | Token 使用量大（~15x）|
| 易于扩展 Worker | 需要强模型作为 Orchestrator |

---

## 2. Hierarchical（层级嵌套）

### 模式描述

Agent 可以嵌套创建 Subagent，形成层级结构。支持多层级委托。

```
Level 0: Main Agent
    │
    ├─ Level 1: Subagent A
    │       │
    │       └─ Level 2: Sub-subagent A1
    │
    ├─ Level 1: Subagent B
    │       │
    │       ├─ Level 2: Sub-subagent B1
    │       └─ Level 2: Sub-subagent B2
    │
    └─ Level 1: Subagent C
```

### 关键特征

- **层级委托**：Subagent 可以创建 Sub-subagent
- **预算控制**：每层有 token 预算限制
- **持久化 Session**：支持跨会话保持状态
- **层级导航**：可以在层级间切换上下文

### 适用场景

✅ **适合：**
- 大型项目（多阶段、多模块）
- 需要层层分解的复杂任务
- 长期项目（需要持久化状态）

❌ **不适合：**
- 简单任务（层级 overhead 不值得）
- 短会话（不需要持久化）
- 资源受限（层级增加 token 消耗）

### 代表实现

**OpenCode PR #7756**：
- 支持 subagent-to-subagent delegation
- Budgets：每层有 token 预算
- Persistent sessions：支持 task_id 恢复会话
- Hierarchical navigation：层级间切换

### 优缺点

| 优点 | 缺点 |
|------|------|
| 支持复杂项目 | 层级管理复杂 |
| 可逐层细化 | Token 消耗指数级增长 |
| 状态可持久化 | 调试困难 |
| 职责边界清晰 | 需要仔细设计层级深度 |

---

## 3. Peer-to-Peer（平等协作）

### 模式描述

多个 Agent 平等协作，通过消息传递协调。没有中心节点。

```
┌─────────┐         ┌─────────┐
│ Agent A │◄───────►│ Agent B │
│ (专家1) │         │ (专家2) │
└────┬────┘         └────┬────┘
     │                   │
     └─────────┬─────────┘
               │
          ┌────┴────┐
          │ Agent C │
          │ (专家3) │
          └─────────┘
```

### 关键特征

- **去中心化**：没有单一协调者
- **消息传递**：Agent 通过命名消息通信
- **多模型支持**：不同 Agent 可用不同模型
- **TUI 集成**：终端 UI 显示协作状态

### 适用场景

✅ **适合：**
- 多专家会诊（代码审查、架构评审）
- 需要多视角分析的问题
- 民主决策场景

❌ **不适合：**
- 需要快速决策（协商耗时）
- 任务依赖复杂（协调困难）
- 强一致性要求（可能产生分歧）

### 代表实现

**OpenCode Agent Teams（Issue #12711）**：
- Flat teams with named messaging
- Multi-model support
- TUI integration
- 支持 GPT-5.3、Gemini 3、Claude Opus 协作

### 优缺点

| 优点 | 缺点 |
|------|------|
| 去中心化，无单点故障 | 协调复杂 |
| 多视角全面 | 决策可能不一致 |
| 可扩展性强 | 消息传递 overhead |
| 模拟真实团队协作 | 需要设计通信协议 |

---

## 4. Pipeline（流水线）

### 模式描述

任务按阶段串联，前一阶段的输出作为后一阶段的输入。

```
Input
   │
   ▼
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│ Stage 1│───►│ Stage 2│───►│ Stage 3│───►│ Stage 4│
│  Build │    │  Test  │    │ Deploy │    │ Notify │
└────────┘    └────────┘    └────────┘    └────────┘
```

### 关键特征

- **阶段串联**：输出 → 输入
- **顺序执行**：每个阶段完成后才进入下一阶段
- **可中断**：任一阶段失败可停止流水线
- **可观察**：每个阶段状态可见

### 适用场景

✅ **适合：**
- CI/CD 流程（构建 → 测试 → 部署）
- 数据处理流水线（清洗 → 转换 → 加载）
- 文档生成（分析 → 编写 → 格式化 → 发布）

❌ **不适合：**
- 需要并行处理（流水线是串行的）
- 分支逻辑复杂（流水线是线性的）
- 实时性要求高（阶段间有延迟）

### 代表实现

**GitHub Actions / CI/CD**：
- Build Stage：编译代码
- Test Stage：运行测试
- Deploy Stage：部署到环境
- 每个阶段可配置不同的 Agent

### 优缺点

| 优点 | 缺点 |
|------|------|
| 流程清晰 | 无法并行 |
| 易于监控 | 阶段间延迟 |
| 可中断失败 | 不适合复杂分支 |
| 可复用阶段 | 资源利用率低 |

---

## 5. 模式对比

| 维度 | Orchestrator-Worker | Hierarchical | Peer-to-Peer | Pipeline |
|------|---------------------|--------------|--------------|----------|
| **结构** | 1 主 + N 从 | 层级嵌套 | 平等网络 | 阶段串联 |
| **协调** | 中心化 | 逐层委托 | 去中心化 | 顺序传递 |
| **并行** | ✅ 支持 | ⚠️ 有限 | ✅ 支持 | ❌ 不支持 |
| **复杂度** | 中 | 高 | 高 | 低 |
| **扩展性** | 高（加 Worker）| 高（加深层级）| 高（加 Peer）| 中（加 Stage）|
| **故障恢复** | 中 | 难 | 难 | 易（重跑 Stage）|
| **代表** | Claude 研究系统 | OpenCode PR#7756 | Agent Teams | CI/CD |

---

## 6. 混合模式

### 实际项目中常混合使用

```
Orchestrator（模式1）
    │
    ├─ Worker A（Pipeline 模式4）
    │   ├─ Stage 1: Build
    │   ├─ Stage 2: Test
    │   └─ Stage 3: Deploy
    │
    ├─ Worker B（Hierarchical 模式2）
    │   └─ Sub-worker B1（Peer-to-Peer 模式3）
    │       ├─ Expert B1a
    │       └─ Expert B1b
    │
    └─ Worker C（独立执行）
```

### 选择建议

1. **默认选择**：Orchestrator-Worker（大多数场景适用）
2. **大型项目**：Hierarchical（支持复杂分解）
3. **多专家协作**：Peer-to-Peer（去中心化决策）
4. **流程化任务**：Pipeline（CI/CD、数据处理）

---

## 7. 模式选择决策树

```
评估任务特征
    │
    ├─ 需要并行执行？
    │   ├─ 是 → Orchestrator-Worker 或 Peer-to-Peer
    │   └─ 否 → 继续
    │
    ├─ 需要多阶段流水线？
    │   ├─ 是 → Pipeline
    │   └─ 否 → 继续
    │
    ├─ 需要层级分解？
    │   ├─ 是 → Hierarchical
    │   └─ 否 → 继续
    │
    └─ 默认 → Orchestrator-Worker
```

---

## Related

- `decision-framework.md` - 完整决策框架
- `splitting-strategies.md` - 功能切分 vs 场景切分
- `common-mistakes.md` - 常见设计错误
