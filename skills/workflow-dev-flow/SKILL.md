---
description: "开发工作流：从 PRD 到上线的完整开发流程。用于需要将已整理好的 PRD 拆解为架构和 task，并分步完成开发、测试、审查、GitHub 上传、CI/CD、合并等复杂开发任务时。"
---

# Workflow: Dev Flow

## Overview

将已整理好的 PRD 拆解为架构设计和具体 task，分步完成开发、测试、审查、GitHub 上传、CI/CD 配置、合并到主分支。

本工作流由 Orchestrator Agent 加载执行，通过分派 subagent 完成各阶段任务。

## Execution Phases

### Phase 1: 分析与架构设计

**目标**：理解 PRD，输出架构设计和 task 列表

**步骤**：
1. 读取用户提供的 PRD 文档
2. 委派 `architect` subagent 进行架构设计：
   - 输入：PRD 内容、项目上下文
   - 输出：架构文档（含技术选型、模块划分、接口设计、数据模型、Mermaid 架构图）
3. 将架构文档传递给 `planner` subagent 进行任务拆解：
   - 输入：架构设计文档
   - 输出：详细的 task 列表（含描述、类型、优先级、依赖关系、输入、输出、验证标准、分配的 subagent）
4. Orchestrator 汇总架构文档和 task 列表

**Checkpoint - 架构确认**：
- 向用户展示架构设计文档（来自 `architect`）
- 向用户展示 task 列表（来自 `planner`）
- 等待用户确认或提出修改意见
- **用户确认前不得进入 Phase 2**

### Phase 2: 开发实现

**目标**：按 task 列表分步完成开发

**步骤**：
1. 按依赖关系排序 task（无依赖的优先并行执行）
2. 分派 subagent 执行：
   - 前端任务 → `frontend-dev`
   - 后端任务 → `backend-dev`
   - Android 任务 → `android-dev`
   - 分析探索任务 → `analyze`
3. 执行策略：
   - 无依赖的 task 并行执行
   - 有依赖的 task 串行执行，等待前置 task 完成
4. 每个 task 完成后：
   - 验证输出是否符合预期
   - 记录完成状态
   - 如有失败，执行 Error Handling 流程

**注意**：
- 此阶段全自动执行，不向用户汇报中间进度
- 仅在完全失败（重试 3 次后）时暂停汇报

### Phase 3: 测试与审查

**目标**：确保代码质量

**步骤**：
1. 调用 `test-engineer` subagent：
   - 为新增功能编写单元测试
   - 执行现有测试套件
   - 修复测试失败（如是代码问题，分派回对应 subagent 修复）
2. 调用 `analyze` subagent 进行代码审查：
   - 检查代码质量、安全性、性能
   - 检查是否符合项目规范
   - 输出审查报告
3. 修复审查发现的问题：
   - 严重问题：分派回对应 subagent 修复
   - 轻微问题：记录到 TODO，不阻塞流程

**注意**：
- 此阶段全自动执行
- 测试全部通过且无严重审查问题后，进入 Phase 4

### Phase 4: GitHub 上传与 PR 创建

**目标**：创建 Pull Request

**步骤**：
1. 创建 Git 分支：
   - 分支命名：`feature/{task-description}` 或 `feat/{short-name}`
   - 从最新的主分支创建
2. 提交代码：
   - 按功能模块分组 commit
   - commit message 遵循 Conventional Commits 规范
3. 推送分支到远程仓库
4. 创建 Pull Request：
   - 标题：清晰描述功能
   - 描述：包含变更说明、测试情况、相关 issue
   - 设置合适的 labels 和 reviewers

**Checkpoint - PR 创建汇报**：
- 向用户展示 PR 信息：
  - PR 链接
  - 分支名
  - 变更摘要
  - 测试状态
- 等待用户审查 PR

### Phase 5: CI/CD 配置（如需要）

**目标**：配置持续集成/持续部署

**步骤**：
1. 检查项目是否已有 CI/CD 配置
2. 如需要新增或修改：
   - 创建/修改 CI/CD 配置文件（如 `.github/workflows/`）
   - 配置构建、测试、部署流程
3. 提交 CI/CD 配置变更
4. 验证 CI/CD pipeline 运行正常

**注意**：
- 如项目已有完善的 CI/CD，可跳过此阶段
- 此阶段全自动执行

### Phase 6: 合并准备

**目标**：准备合并到主分支

**步骤**：
1. 确认 PR 已通过所有 CI 检查
2. 确认代码审查已通过（无未解决的评论）
3. 确认测试全部通过
4. 解决可能的合并冲突

**Checkpoint - 合并前确认**：
- 向用户展示合并前的最终状态：
  - PR 状态（CI 通过、审查通过）
  - 变更文件列表
  - 测试结果摘要
- **等待用户确认后才能执行合并**
- 用户确认后，执行合并操作

## Task Assignment Matrix

| 任务类型 | Subagent | 所需权限 |
|---------|----------|---------|
| 架构设计 | `architect` | read, write |
| 任务拆解 | `planner` | read, write |
| 前端开发 | `frontend-dev` | read, write, bash |
| 后端开发 | `backend-dev` | read, write, bash |
| Android 开发 | `android-dev` | read, write, bash |
| 代码分析 | `analyze` | read |
| 测试编写与执行 | `test-engineer` | read, write, bash |
| Android 测试 | `android-test-engineer` | read, write, bash |

## Task Breakdown Format

每个 task 应按以下格式定义：

```markdown
### Task: {task-name}
- **描述**: {一句话描述任务内容}
- **类型**: {frontend|backend|android|test|analyze}
- **优先级**: {P0|P1|P2}
- **依赖**: [{依赖的 task 名称}]
- **输入**: {需要的输入，如接口文档、设计稿}
- **输出**: {期望的输出，如代码文件、文档}
- **验证标准**: {如何判断任务完成}
```

## Error Handling

当 subagent 执行失败时：

1. **分析原因**：检查错误信息，判断失败原因
2. **调整策略**：
   - 依赖缺失 → 安装依赖
   - 配置错误 → 修正配置
   - 代码问题 → 提供更多信息或调整 task 描述
3. **自动重试**：最多重试 3 次，每次重试前调整策略
4. **暂停汇报**：3 次重试后仍失败：
   - 记录失败的任务信息
   - 记录已尝试的重试策略
   - 记录错误详情
   - 提供建议的解决方案
   - 暂停执行，等待用户指示

## Constraints

- 严格按照 Phase 顺序执行，不得跳过 Phase
- Phase 1 完成后必须等待用户确认架构设计
- Phase 4 完成后必须展示 PR 信息
- Phase 6 完成后必须等待用户确认才能合并
- 除汇报点外，其他阶段全自动执行
- 不得在用户未确认的情况下合并到主分支
- 遵循 Orchestrator Agent 的所有约束条件
