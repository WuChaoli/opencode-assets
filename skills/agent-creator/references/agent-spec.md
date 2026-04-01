# Agent 规范详解

## MUST（必须遵守）

### 1. YAML Frontmatter

每个 Agent markdown 文件必须以 YAML frontmatter 开头：

```yaml
---
description: "简短描述 + 触发条件"
mode: primary|subagent|all
---
```

### 2. description 格式

必须包含两部分：
1. **做什么**: 简短的能力描述
2. **何时用**: 具体的触发条件/场景

✅ 正确: `"代码审查助手：审查代码质量和安全性。用于 PR 审查、代码质量检查时。"`
❌ 错误: `"帮助开发者写更好的代码"`（太模糊）

### 3. mode 必须指定

- `primary` — 主代理，Tab 切换使用
- `subagent` — 子代理，@ 调用或自动触发
- `all` — 两种模式都支持（默认值）

### 3.1 tools 字段（上游：控制工具是否可用）

`tools` 控制 agent 可以使用哪些工具，是 boolean 开关。

```yaml
tools:
  write: false    # 不可创建文件
  edit: false     # 不可修改文件
  bash: false     # 不可执行命令
```

- `false` → 工具完全不可见（模型不知道有这个工具）
- `true` 或不写 → 工具可见

### 3.2 permission 字段（下游：精细化控制）

`permission` 控制工具如何执行，是 ask/allow/deny。

```yaml
permission:
  edit: ask       # 需要确认
  bash: deny      # 禁止执行
  webfetch: allow # 自动允许
```

### tools vs permission 关系

| 组合 | 效果 |
|------|------|
| `tools: false` | 工具完全不可见 |
| `tools: true` + `permission: deny` | 工具可见但被拒绝 |
| `tools: true` + `permission: ask` | 工具可见但需确认 |
| `tools: true` + `permission: allow` | 工具可见且自动执行 |

**推荐**：简单场景只用 `permission`；严格场景 `tools` + `permission` 组合。

### 4. 必须包含的章节

- `## Role` — 角色定义
- `## Responsibilities` — 职责列表
- `## Available Resources` — 可用资源（Skills/MCP/Tools）
- `## Constraints` — 约束条件

### 5. Available Resources 必须存在

Agent prompt 必须明确列出可用资源，帮助 agent 做决策：

```markdown
## Available Resources

### Skills
- `skill-name` - [用途]

### MCP Servers
- `mcp-name` - [用途]

### Tools
- `tool-name` - [用途]
```

## SHOULD（强烈建议）

### 1. 权限最小化

只给必要的工具权限：

```yaml
permission:
  edit: ask    # 需要时询问
  bash: deny   # 不需要就拒绝
  webfetch: allow
```

### 2. 模型不指定

不指定 `model` 字段，让 agent 继承全局配置，最灵活。

### 3. 职责聚焦

每个 agent 只做一件事，职责不超过 5 条。

### 4. 约束具体化

约束要具体可执行：

✅ 正确: "不要修改测试文件"
❌ 错误: "小心一点"

## NEVER（禁止）

### 1. 禁止权限过度

不要给 agent 不需要的权限。

❌ 错误: 审查 agent 给了 write 权限
✅ 正确: 审查 agent 设为 edit: deny

### 2. 禁止资源罗列

不要列出所有可用资源，只列 agent 会用到的。

❌ 错误: 列出 20 个 skills 和 10 个 MCP
✅ 正确: 列出 2-3 个最相关的

### 3. 禁止模糊描述

不要使用无法判定的描述。

❌ 错误: "当你需要帮助时使用此 agent"
✅ 正确: "当用户提到 '代码审查'、'PR review' 时触发"

### 4. 禁止跳过确认

不要在未与用户确认的情况下直接创建 agent。
