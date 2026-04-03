# 模板语法详解

## 1. $ARGUMENTS — 所有参数

将所有参数作为一个整体替换。

**定义**：
```markdown
---
description: Create a new component
---
Create a new React component named $ARGUMENTS with TypeScript support.
```

**使用**：
```
/component Button
```

**结果**：`$ARGUMENTS` 被替换为 `Button`

```
/component UserCard dark-mode
```

**结果**：`$ARGUMENTS` 被替换为 `UserCard dark-mode`

## 2. $1, $2, $3 — 位置参数

按位置分别替换各个参数。

**定义**：
```markdown
---
description: Create a new file with content
---
Create a file named $1 in the directory $2 with the following content: $3
```

**使用**：
```
/create-file config.json src "{ \"key\": \"value\" }"
```

**结果**：
- `$1` → `config.json`
- `$2` → `src`
- `$3` → `{ "key": "value" }`

## 3. !`command` — Shell 输出注入

执行 shell 命令并将其输出注入到 prompt 中。

**定义**：
```markdown
---
description: Analyze test coverage
---
Here are the current test results:
!`npm test`

Based on these results, suggest improvements to increase coverage.
```

**执行流程**：
1. 用户执行 `/analyze-coverage`
2. OpenCode 执行 `npm test` 命令
3. 将输出注入到 prompt 中
4. LLM 基于测试结果给出建议

**更多示例**：

```markdown
---
description: Review recent changes
---
Recent git commits:
!`git log --oneline -10`

Review these changes and suggest improvements.
```

```markdown
---
description: Check current branch status
---
Current git status:
!`git status`
!`git diff --stat`

Analyze the current state and suggest next steps.
```

**注意**：Shell 命令在项目根目录执行。

## 4. @filename — 文件引用

自动将文件内容注入到 prompt 中。

**定义**：
```markdown
---
description: Review component
---
Review the component in @src/components/Button.tsx.
Check for performance issues and suggest improvements.
```

**执行流程**：
1. 用户执行 `/review-component`
2. OpenCode 读取 `src/components/Button.tsx` 的内容
3. 将文件内容注入到 prompt 中
4. LLM 基于文件内容进行审查

**多文件引用**：
```markdown
---
description: Review API
---
Review the following files:
- @src/api/users.ts
- @src/api/auth.ts

Check for security issues and best practices.
```
