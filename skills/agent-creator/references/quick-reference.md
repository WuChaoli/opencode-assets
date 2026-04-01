# Quick Reference

## Agent 类型决策树

```
需要 Tab 切换作为主代理？
  ├─ 是 → primary agent
  └─ 否 → subagent

subagent 需要并行执行？
  ├─ 是 → subagent（general 类型）
  └─ 否 → 是否需要隔离上下文？
      ├─ 是 → subagent
      └─ 否 → 考虑是否需要 agent
```

## 目录结构

```
.opencode/agents/
├── code-reviewer.md          # Subagent 示例
├── docs-writer.md            # Subagent 示例
└── security-auditor.md       # Subagent 示例
```

## Markdown Agent 完整格式

```markdown
---
description: [做什么 + 何时用]
mode: [primary|subagent|all]
model: [可选，不填则继承全局]
temperature: [0.0-1.0，可选]
steps: [最大迭代次数，可选]
tools:                    # 上游：控制哪些工具可用（boolean）
  write: false
  edit: false
  bash: false
permission:               # 下游：精细化控制（ask/allow/deny）
  edit: [ask|allow|deny]
  bash: [ask|allow|deny]
  webfetch: [ask|allow|deny]
---

# [name] Agent

## Role
[角色定义：你是谁，擅长什么]

## Responsibilities
- [职责 1]
- [职责 2]
- [职责 3]

## Available Resources

### Skills（推荐使用的技能）
- `skill-name` - [用途说明]

### MCP Servers（可用的 MCP 工具）
- `mcp-name` - [用途说明]

### Tools（可用的工具）
- `tool-name` - [用途说明]

## Constraints
- [约束 1]
- [约束 2]
```

## tools vs permission 详解

| 字段 | 层级 | 作用 | 值类型 |
|------|------|------|--------|
| `tools` | 上游 | 控制工具是否可用 | boolean (true/false) |
| `permission` | 下游 | 控制工具如何执行 | ask/allow/deny |

**使用原则**：
- `tools: false` → 工具完全不可见（模型不知道有这个工具）
- `tools: true` + `permission: deny` → 工具可见但被拒绝
- `tools: true` + `permission: ask` → 工具可见但需确认
- `tools: true` + `permission: allow` → 工具可见且自动执行

**推荐做法**：
- 简单场景：只用 `permission`（tools 默认全开启）
- 严格场景：`tools` 关闭不需要的 + `permission` 精细化控制

**Subagent 特殊规则**：
- Subagent 的 `permission` **只能使用 `allow` 或 `deny`**
- **禁止在 subagent 中使用 `permission: ask`**
- 原因：subagent 在后台执行，使用 `ask` 会阻塞等待用户确认
- 如需要人工介入，应在 Agent prompt 中说明并通过输出告知用户

**Primary Agent 规则**：
- Primary Agent 可使用 `ask/allow/deny` 全部三种模式
- 对敏感操作（文件写入、bash 执行）推荐使用 `ask`

## 资源推荐原则

1. **Skills**：推荐与 agent 职责相关的流程性知识
2. **MCP**：推荐 agent 需要的外部系统连接
3. **Tools**：推荐 agent 需要的内置工具
4. **只推荐必要的**：不要罗列所有可用资源，只列真正会用到的（2-5 项）

## 权限最小化原则

| Agent 类型 | edit (primary) | edit (subagent) | bash (primary) | bash (subagent) | webfetch |
|-----------|----------------|-----------------|----------------|-----------------|----------|
| 只读审查 | ask | deny | ask | deny | allow |
| 规划分析 | ask | deny | ask | deny | allow |
| 文档编写 | allow | allow | ask | deny | allow |
| 完整开发 | allow | allow | allow | allow | allow |

> 注意：subagent 的 permission 只能使用 `allow` 或 `deny`，不能使用 `ask`

## 模型选择

- 默认不指定 model，继承全局配置
- 需要特定模型时，使用 `model-guide` skill 获取最新推荐
- 分析推理类任务推荐 `opus 4.6` 或 `gpt-5.4`
- 日常编码推荐 `sonnet 4.6`

## 搜索策略

| 来源 | 规模 | 访问方式 | 特点 |
|------|------|---------|------|
| Claude Code Market | 53+ agents | 网站 | 专业 sub-agents，评分系统 |
| awesome-opencode | 4235 stars | GitHub | OpenCode 专用 agents |
| GitHub 搜索 | 海量 | code search | 社区广泛贡献 |

## 评估决策树

```
搜索到现有 Agent？
  ├─ 是 → 匹配度 > 80%？
  │   ├─ 是 → 推荐直接安装
  │   └─ 否 → 匹配度 50-80%？
  │       ├─ 是 → 推荐改编
  │       └─ 否 → 推荐参考后创建
  └─ 否 → 从零创建
```
