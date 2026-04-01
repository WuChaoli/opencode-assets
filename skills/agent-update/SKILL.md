---
name: agent-update
description: "元技能：迭代优化现有 OpenCode Agent。触发条件：优化 Agent、改进 Agent、用户提到'agent update'、'agent refactor'、'优化 agent'、'重构 agent'时。"
---

# agent-update 元技能

诊断、优化、迭代现有 OpenCode Agent，确保其保持高质量和可靠性。

## When to Use This Skill

触发条件（满足任一即可）：
- 用户提到"优化 Agent"、"改进 Agent"、"agent update"、"agent refactor"
- Agent 触发不可靠（有时触发有时不触发）
- Agent 行为不符合预期（权限问题、输出质量差）
- 需要调整权限配置（tools/permission）
- 需要更新 Available Resources（Skills/MCP/Tools）
- 需要根据用户反馈调整行为

## Not For / Boundaries

此技能不适用于：
- 从零创建新 Agent（那是 agent-creator 的事）
- 修改 Agent 的核心用途（那应该创建新 Agent）
- 跳过诊断直接修改

必要输入（缺失时需询问）：
1. 要优化的 Agent 路径或名称
2. 具体问题或改进目标

## 工作流程（7 步，严格按顺序执行）

### 阶段一：诊断分析

**Step 1: 读取并分析当前 Agent**
- 读取 agent.md 文件内容
- 运行审计脚本统计行数、结构完整性
- 识别以下问题：
  - 权限配置（过度/不足）
  - Prompt 质量（角色模糊、职责不聚焦）
  - 资源推荐过时（Skills/MCP/Tools）
  - 触发词模糊（description）
  - 模型选择不匹配
  - 参数不合理（temperature/steps）

**Step 2: 收集反馈和问题**
- 询问用户具体问题：
  - 什么场景下不好用？
  - 期望的改进方向？
- 如果没有具体反馈，基于诊断结果提出改进建议

### 阶段二：方案设计

**Step 3: 制定优化方案**
- 基于诊断结果，制定具体修改计划：
  - 权限：调整 tools/permission 配置
  - Prompt：重写 Role/Responsibilities/Constraints
  - 资源：更新 Available Resources
  - 触发：优化 description
  - 模型：调整 model 字段
  - 参数：调整 temperature/steps
- 输出修改预览（diff 形式）

**Step 4: 与用户确认方案**
- 展示修改预览
- 说明每个修改的原因和预期效果
- **未经用户确认，不得开始修改**

### 阶段三：执行修改

**Step 5: 执行修改**
- 按确认的方案修改文件
- 保持向后兼容（不破坏现有触发）
- 更新 Maintenance 章节（最后更新日期、变更说明）

**Step 6: 质量验证**
- 运行验证脚本确认修改后质量
- 确认 Prompt 行数 < 100
- 确认所有必须章节存在
- 确认权限配置合理

**Step 7: 交付与说明**
- 展示修改内容摘要
- 说明如何测试改进效果
- 建议后续观察点

## Quick Reference

### 诊断检查清单

| 检查项 | 标准 | 修复方式 |
|--------|------|---------|
| description | 包含具体触发词 | 添加关键词 |
| mode | 已指定 | 设为 primary/subagent |
| Role | 存在且清晰 | 重写角色定义 |
| Responsibilities | 存在且 <= 5 条 | 精简职责 |
| Available Resources | 存在且 <= 5 项 | 聚焦相关资源 |
| Constraints | 存在且具体 | 补充约束 |
| 权限配置 | 最小化 | 调整 tools/permission |
| Prompt 行数 | < 100 行 | 精简内容 |

### 优化策略

| 问题 | 策略 | 示例 |
|------|------|------|
| 权限过度 | 调整为最小权限 | edit: deny |
| 权限不足 | 添加必要权限 | bash: ask |
| Prompt 模糊 | 重写角色+职责 | 具体化行为描述 |
| 资源过时 | 更新 Skills/MCP | 替换废弃引用 |
| 触发不可靠 | 优化 description | 添加具体场景 |
| 模型不匹配 | 调整 model | sonnet → opus |

### tools vs permission 关系

| 组合 | 效果 |
|------|------|
| `tools: false` | 工具完全不可见 |
| `tools: true` + `permission: deny` | 工具可见但被拒绝 |
| `tools: true` + `permission: ask` | 工具可见但需确认 |
| `tools: true` + `permission: allow` | 工具可见且自动执行 |

### 创作规则（不可协商）
1. 先诊断再修改，不要盲目修改
2. 必须用户确认后再修改
3. 保持向后兼容，不破坏现有触发
4. 每次只改 1-2 个变量，方便归因
5. 更新 Maintenance 章节记录变更

## 审计工具

- 运行 `{baseDir}/scripts/audit_agent.py <agent-path>` 生成诊断报告
- 运行 `{baseDir}/../agent-creator/scripts/validate_agent.py <agent-path>` 验证质量

## References

- `references/index.md` - 导航
- `references/diagnostic-guide.md` - 诊断指南
- `references/refactor-patterns.md` - 重构模式
- `references/permission-guide.md` - 权限优化指南
- `references/versioning.md` - 版本管理
- `assets/update-report.md` - 更新报告模板

## Maintenance

- Last updated: 2026-04-01
- Known limits: 需要用户反馈才能精准优化；自动诊断只能发现结构问题
