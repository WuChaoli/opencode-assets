---
name: agent-design
description: "Agent 架构设计指导：如何切分 subagent、选择架构模式、设计多 agent 协作。触发条件：agent 设计、subagent 切分、架构模式选择、agent 体系规划。"
---

# agent-design 元技能

提供 Agent/Subagent 系统的**设计哲学、决策框架和架构模式**。帮助用户回答"如何设计"而非"如何创建"。

与 `agent-creator`（创建流程）形成互补：
- **agent-design** → 决定"设计成什么样"（架构、切分、模式）
- **agent-creator** → 执行"如何创建"（配置、权限、prompt）

---

## When to Use This Skill

**触发条件（满足任一即可）：**
- 用户问"如何设计 agent"、"怎么切分 subagent"
- 需要选择功能切分 vs 场景切分
- 需要设计多 agent 协作架构（Orchestrator-Worker、层级等）
- 需要评估现有 agent 体系的问题和改进方案
- 规划大型项目的 agent 团队结构

**典型场景：**
1. 新项目启动：从零规划 agent 架构
2. 现有系统重构：agent 职责不清、上下文污染严重
3. 性能优化：减少 token 浪费、提升并行效率
4. 团队协作：设计可复用的 agent 角色体系

---

## Not For / Boundaries

**此技能不适用于：**
- 直接创建 agent 文件（用 `agent-creator`）
- 修改单个 agent 的 prompt 细节（用 `agent-creator`）
- 不经过设计讨论直接创建（违反设计优先原则）
- 凭空设计无业务场景的 agent 体系

**必要输入（缺失时需询问）：**
1. 项目类型/技术栈（如 Android、Web、后端服务）
2. 任务复杂度（简单/中等/复杂，涉及多少文件/模块）
3. 当前痛点（上下文污染？协调困难？职责不清？）
4. 团队规模（单人/小团队/大团队）

---

## Quick Reference

### 切分决策矩阵

| 维度 | 按功能切分 | 按场景切分 |
|------|-----------|-----------|
| **上下文共享** | 低 | 高 |
| **工具差异** | 大（每个 agent 工具集不同） | 小 |
| **可复用性** | 高（通用能力） | 中（特定场景） |
| **协调成本** | 高（需要 orchestrator 组装） | 低（端到端完成） |
| **适合场景** | 探索、分析、审查等通用任务 | 开发、测试、构建等流程 |

### 3 步设计检查清单

```
Step 1: 评估任务特征
  □ 任务间上下文共享度 > 50%？→ 场景切分
  □ 工具能力差异大？→ 功能切分
  □ 需要并行执行？→ 功能切分（独立上下文）

Step 2: 定义 agent 边界
  □ 输入：明确的任务描述 + 上下文范围
  □ 输出：可交付的单一结果（摘要/代码/报告）
  □ 工具：最少必要集（2-5 个工具）

Step 3: 验证设计合理性
  □ 如果去掉这个 agent，主 agent 工作量增加 > 2x？→ 保留
  □ agent 职责能用 1 句话描述清楚？→ 保留
  □ 和其他 agent 共享工具集完全相同？→ 考虑合并
```

### 架构模式速查

| 模式 | 结构 | 适用场景 | 代表实现 |
|------|------|---------|---------|
| **Orchestrator-Worker** | 1 主 + N 从 | 复杂任务分解、并行探索 | Claude 研究系统 |
| **Hierarchical** | 层级嵌套 | 大型项目、多阶段流水线 | OpenCode PR#7756 |
| **Peer-to-Peer** | 平等协作 | 多专家会诊、代码审查 | Agent Teams |
| **Pipeline** | 阶段串联 | 构建、CI/CD 流程 | Build → Test → Deploy |

### 关键设计原则

1. **Conway's Law for Agents**：Agent 切分应反映真实依赖结构
2. **Context Affinity**：高上下文亲和度操作放在同一个 agent
3. **Single Responsibility + Composability**：单一职责，可组合输出
4. **权限最小化**：只给必要工具，subagent 用 `allow/deny`（不用 `ask`）

---

## Examples

### Example 1: 从需求推导切分方案

**输入**：Android 项目，需要处理 UI、网络、存储、测试
**步骤**：
1. 识别技术栈边界（UI/网络/存储 工具链差异大）
2. 评估上下文：UI 开发和网络开发共享上下文 < 30%
3. 决策：按技术栈场景切分
4. 设计：
   - `android-ui-engineer`：Compose + XML + 截图对比
   - `android-dev`：Kotlin + 架构 + Room/Hilt
   - `android-test-engineer`：单元测试 + MockK
5. 验证：每个 agent 工具集不同，职责清晰
**验收**：产出 3 个场景化 agent 设计方案，上下文隔离良好

### Example 2: 选择功能切分 vs 场景切分

**输入**：需要探索代码库 + 重构认证逻辑
**步骤**：
1. 分析任务：探索（只读）vs 重构（读写）
2. 上下文特征：探索产生 20+ 文件历史，会污染重构上下文
3. 决策：功能切分（explore + implement 分离）
4. 设计：
   - 内置 `explore` agent：只读搜索，返回摘要
   - 自定义 `auth-refactor` agent：基于摘要执行重构
5. 验证：主 agent 上下文保持干净，聚焦协调
**验收**：使用功能切分避免上下文污染，token 使用减少 40%

### Example 3: 设计 Orchestrator-Worker 架构

**输入**：复杂研究任务（多数据源 + 综合分析）
**步骤**：
1. 识别子任务：文档研究、代码分析、问题排查（可并行）
2. 选择模式：Orchestrator-Worker
3. 设计层级：
   - Orchestrator（Opus）：战略分析 + 任务分解
   - Worker 1（Sonnet）：文档研究 subagent
   - Worker 2（Sonnet）：代码分析 subagent
   - Worker 3（Sonnet）：问题排查 subagent
4. 协调机制：每个 worker 返回结构化摘要，orchestrator 综合
5. 验证：并行执行，token 使用增加 15x 但质量提升 90%
**验收**：产出 4-agent 协作架构，明确输入输出和协调机制

### Example 4: 重构混乱的 agent 体系

**输入**：现有 8 个 agent，职责重叠，经常重复工作
**步骤**：
1. 分析现状：列出所有 agent 的工具集和职责
2. 识别问题：3 个 agent 工具集完全相同（冗余）
3. 合并决策：合并重复 agent，保留差异化能力
4. 重新设计：
   - 保留：`explore`（只读）、`implement`（读写）
   - 合并：`test-write` + `test-run` → `test-engineer`（端到端）
5. 验证：从 8 个减少到 5 个，协调成本降低 30%
**验收**：产出重构方案，明确保留/合并/删除决策

---

## References

- `references/decision-framework.md` - 完整决策框架（Conway's Law、Context Affinity 等）
- `references/splitting-strategies.md` - 功能切分 vs 场景切分详细对比
- `references/architecture-patterns.md` - 4 大架构模式详解
- `references/common-mistakes.md` - 常见设计错误和修复方案
- `references/evaluation-guide.md` - 如何评估 agent 设计质量
- `assets/templates/capability-based.md` - 功能切分模板
- `assets/templates/scenario-based.md` - 场景切分模板
- `assets/templates/orchestrator-worker.md` - 编排者模式模板

---

## Maintenance

- Created: 2026-04-03
- Related: `agent-creator`（执行创建）、`model-guide`（模型选择）
- Complementary: 先用 `agent-design` 设计方案，再用 `agent-creator` 创建文件
