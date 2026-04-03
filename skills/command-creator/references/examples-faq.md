# 完整实例与常见问题

## 完整实例

### 实例 1：基础命令（无参数）

```markdown
---
description: Run tests with coverage
agent: build
---
Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

**使用**：`/run-tests`

### 实例 2：带参数命令

```markdown
---
description: Create a new React component
---
Create a new React component named $1 with the following requirements:
- TypeScript support
- Proper typing for props
- Basic component structure
- Export as default
```

**使用**：`/new-component Button`

### 实例 3：Shell 输出注入

```markdown
---
description: Review recent changes
---
Recent git commits:
!`git log --oneline -10`

Review these changes and suggest any improvements.
```

**使用**：`/review-changes`

### 实例 4：文件引用

```markdown
---
description: Review component
---
Review the component in @src/components/Button.tsx.
Check for:
- Performance issues
- Accessibility concerns
- Code quality
- Best practices
```

**使用**：`/review-component`

### 实例 5：指定 Agent 和 Model

```markdown
---
description: Security audit
agent: plan
model: anthropic/claude-opus-4-20250514
subtask: true
---
Perform a security audit of the codebase.
Focus on:
- OWASP Top 10 vulnerabilities
- Authentication and authorization issues
- Input validation
- Secret management
```

**使用**：`/security-audit`

### 实例 6：综合使用所有语法

```markdown
---
description: Generate API endpoint
---
Generate a REST API for the $1 resource with the following endpoints:
- GET /api/$1
- POST /api/$1
- PUT /api/$1/$2
- DELETE /api/$1/$2

Current project structure:
!`ls -la src/`

Reference the existing API pattern in @src/api/example.ts.

Include:
- Route handlers
- Validation middleware
- TypeScript types
- Error handling
```

**使用**：`/generate-api users id`

**结果**：
- `$1` → `users`
- `$2` → `id`
- Shell 命令输出注入 `ls -la src/` 的结果
- `src/api/example.ts` 文件内容被引用

## 存储位置说明

### 全局命令

```
~/.config/opencode/commands/
├── run-tests.md
├── new-component.md
└── review-changes.md
```

**特点**：所有项目都可用

### 项目命令

```
.opencode/commands/
├── deploy.md
├── generate-migration.md
└── lint-fix.md
```

**特点**：仅当前项目可用

### 优先级

- 项目命令优先于全局命令
- 自定义命令可覆盖内置命令（如 `/init`, `/help` 等）
- 同名命令，项目级 > 全局级

## 最佳实践

1. **保持专注**：一个命令做一件事
2. **使用参数**：避免为相似任务创建多个命令
3. **合理选择 agent**：分析用 `plan`，执行用 `build`
4. **subtask 隔离**：复杂操作使用 `subtask: true` 避免污染主上下文
5. **描述清晰**：description 要简洁明了，方便 TUI 中识别

## 常见问题

### 命令不生效？

1. 检查文件位置是否正确（`commands/` 目录）
2. 检查文件名是否为 `.md` 格式
3. 检查 frontmatter 格式是否正确（`---` 分隔符）

### 参数没有被替换？

1. 确认占位符拼写正确（`$ARGUMENTS` 或 `$1`）
2. 确认调用时提供了参数

### Shell 命令执行失败？

1. 确认命令在当前环境可用
2. 确认工作目录正确（项目根目录）
3. 检查命令语法是否正确
