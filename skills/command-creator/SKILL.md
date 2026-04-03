---
name: command-creator
description: "创建 OpenCode 自定义命令。触发条件：create command、创建命令、生成命令、新建命令。"
---

# command-creator Skill

交互式引导用户创建 OpenCode TUI 自定义命令，生成符合规范的 Markdown 命令文件。

## When to Use This Skill

- 用户提到"create command"、"创建命令"、"生成命令"、"新建命令"
- 用户需要为重复任务创建快捷命令
- 用户想要定制 TUI 中 `/` 开头的命令

## Not For / Boundaries

- 不创建 Skill（使用 skill-creator）
- 不创建 Agent（使用 agent-creator）
- 不修改已有命令（直接编辑对应 markdown 文件）
- 不创建 Plugin（需要 npm 包开发）

## Quick Reference

### 交互式引导流程（7 步）

严格按顺序询问，每步得到回答后再进入下一步：

**Step 1: 命令名称和描述**
- 询问命令名称（英文小写+连字符，如 `run-tests`）
- 询问命令描述（TUI 中显示的简短说明）

**Step 2: 模板内容**
- 询问命令执行时要发送给 LLM 的 prompt 内容
- 确认是否需要参数占位符（见 Step 3）

**Step 3: 参数配置（可选）**
- `$ARGUMENTS` — 所有参数整体替换
- `$1`, `$2`, `$3` — 位置参数分别替换
- 如果不需要参数，跳过

**Step 4: Shell 输出注入（可选）**
- 是否需要 `` !`shell-command` `` 语法注入命令输出
- 如果需要，确认具体的 shell 命令

**Step 5: 文件引用（可选）**
- 是否需要 `@filename` 语法引用文件内容
- 如果需要，确认具体的文件路径

**Step 6: 高级配置（可选）**
- `agent` — 指定执行 agent（如 `build`, `plan`）
- `model` — 覆盖默认模型（如 `anthropic/claude-sonnet-4-20250514`）
- `subtask` — 是否强制 subagent 调用（true/false）
- 如果不需要高级配置，跳过

**Step 7: 创建位置**
- 全局：`~/.config/opencode/commands/`
- 项目级：`.opencode/commands/`（默认）
- 自定义路径

### 生成命令文件

根据收集的信息生成 Markdown 文件（**默认使用 Markdown 格式**，不使用 JSON）：

```markdown
---
description: <描述>
agent: <agent名称，可选>
model: <模型，可选>
subtask: <true/false，可选>
---
<模板内容>
```

**YAML 格式规则**：
1. 必须以 `---` 开头和结尾
2. 每个配置项独占一行：`key: value`
3. 冒号后必须有空格
4. 值不需要引号（除非包含特殊字符）
5. 布尔值使用小写：`true` / `false`

写入目标目录后告知用户完成。

## Examples

### Example 1: 创建基础测试命令

**输入**: 用户说 "create command"
**步骤**:
1. 名称: `run-tests`, 描述: "Run tests with coverage"
2. 模板: "Run the full test suite with coverage report and show any failures."
3. 参数: 无
4. Shell 注入: 无
5. 文件引用: 无
6. 高级配置: agent=`build`
7. 位置: 项目级
**输出**: `.opencode/commands/run-tests.md` 文件

### Example 2: 创建带参数的组件生成命令

**输入**: 用户说 "create command"
**步骤**:
1. 名称: `new-component`, 描述: "Create a new React component"
2. 模板: "Create a new React component named $1 with TypeScript support."
3. 参数: $1 = 组件名
4. Shell 注入: 无
5. 文件引用: 无
6. 高级配置: 无
7. 位置: 全局
**输出**: `~/.config/opencode/commands/new-component.md` 文件

### Example 3: 创建带 Shell 注入的代码审查命令

**输入**: 用户说 "create command"
**步骤**:
1. 名称: `review-changes`, 描述: "Review recent changes"
2. 模板: "Recent git commits:\n!`git log --oneline -10`\nReview these changes and suggest improvements."
3. 参数: 无
4. Shell 注入: `git log --oneline -10`
5. 文件引用: 无
6. 高级配置: 无
7. 位置: 项目级
**输出**: `.opencode/commands/review-changes.md` 文件

## References

- `references/command-structure.md`: 命令文件结构、YAML 格式、配置项详解
- `references/template-syntax.md`: 4 种模板语法详解
- `references/examples-faq.md`: 完整实例、最佳实践、常见问题
