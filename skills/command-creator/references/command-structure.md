# 命令文件结构与配置

## 命令概述

自定义命令允许你在 OpenCode TUI 中通过 `/命令名` 快速执行重复任务。命令本质上是预定义的 prompt 模板，执行时会被发送给 LLM。

## Markdown 命令文件（默认推荐）

OpenCode 默认推荐使用 Markdown 文件定义命令。文件名即为命令名。

```markdown
---
description: 命令描述
agent: 执行 agent 名称（可选）
model: 模型覆盖（可选）
subtask: 是否强制 subagent（可选）
---
模板内容（发送给 LLM 的 prompt）
```

**文件位置**：
- **全局命令**：`~/.config/opencode/commands/`
- **项目命令**：`.opencode/commands/`

**命名规则**：文件名即为命令名，如 `test.md` → `/test`

**完整示例**：

```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-sonnet-4-20250514
---
Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

使用方式：在 TUI 中输入 `/test` 即可执行。

## YAML Frontmatter 格式说明

YAML frontmatter 必须满足以下规则：

1. **必须以 `---` 开头和结尾**：前后各有一行 `---`
2. **每个配置项独占一行**：`key: value` 格式
3. **冒号后必须有空格**：`description: Run tests`（注意冒号后的空格）
4. **值不需要引号**：除非值中包含特殊字符（如冒号、引号）
5. **布尔值使用小写**：`subtask: true`（不是 `True` 或 `TRUE`）

**正确示例**：

```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-sonnet-4-20250514
subtask: true
---
```

**错误示例**（常见陷阱）：

```markdown
# 错误：冒号后没有空格
---
description:Run tests with coverage
---

# 错误：前后 --- 不完整
--
description: Run tests
--

# 错误：布尔值大写
---
subtask: True
---
```

## JSON 配置方式（备选）

JSON 配置仅在 `opencode.json` 中使用，不作为默认推荐。

```json
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-sonnet-4-20250514"
    }
  }
}
```

**注意**：JSON 配置中的 `template` 字段对应 Markdown 文件中 frontmatter 之后的内容。

## 配置项详解

### description（描述）

| 属性 | 值 |
|------|------|
| 类型 | string |
| 必填 | 否 |
| 说明 | 命令的简短描述，TUI 中输入 `/` 后显示 |

```yaml
description: Run tests with coverage
```

### agent（执行 Agent）

| 属性 | 值 |
|------|------|
| 类型 | string |
| 必填 | 否 |
| 说明 | 指定执行此命令的 agent。未指定时使用当前 agent |

```yaml
agent: build
```

**注意**：如果指定的是 subagent，命令默认会触发 subagent 调用。可通过设置 `subtask: false` 禁用此行为。

### model（模型覆盖）

| 属性 | 值 |
|------|------|
| 类型 | string |
| 必填 | 否 |
| 说明 | 覆盖此命令使用的模型，格式为 `provider/model-id` |

```yaml
model: anthropic/claude-sonnet-4-20250514
```

**常见模型 ID**：
- `anthropic/claude-sonnet-4-20250514`
- `anthropic/claude-haiku-4-20250514`
- `anthropic/claude-opus-4-20250514`
- `openai/gpt-4o`

### subtask（强制 Subagent）

| 属性 | 值 |
|------|------|
| 类型 | boolean |
| 必填 | 否 |
| 说明 | 强制命令在 subagent 中执行，不污染主上下文 |

```yaml
subtask: true
```

**使用场景**：
- 命令执行大量操作，不想影响主对话上下文
- 即使 agent 配置为 primary，也会强制作为 subagent 执行
