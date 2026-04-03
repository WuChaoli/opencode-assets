# 常见错误：Agent 设计反模式

## 1. 过度拆分（Over-fragmentation）

### 症状
- 8+ 个 agent，每个只做一件事
- 任务在 agent 之间反复传递
- 协调成本超过实际工作成本

### 案例

❌ **错误设计**
```
test-write → test-run → test-analyze → test-report
security-scan → security-analyze → security-report
```

**问题**：
- 上下文在 4 个 agent 间传递
- 主 agent 需要协调 8 次调用
- Token 浪费严重

✅ **修复方案**
```
test-engineer（端到端：写 + 运行 + 分析 + 报告）
security-auditor（端到端：扫描 + 分析 + 报告）
```

**原则**：高上下文亲和度的任务合并，低亲和度的任务拆分。

---

## 2. 万能 Agent（God Agent）

### 症状
- 1 个 agent 能做所有事情
- 职责模糊，description 空泛
- 工具集包含所有可用工具

### 案例

❌ **错误设计**
```yaml
---
name: super-dev
description: "帮助开发者完成所有工作"
tools: "*"  # 所有工具
permission:
  read: allow
  write: allow
  edit: allow
  bash: allow
---

## Role
You are a developer who can do anything.

## Responsibilities
- Write code
- Write tests
- Deploy applications
- Write documentation
- Fix bugs
- Review code
- And more...
```

**问题**：
- 职责不清晰
- 无法判定何时触发
- 可能与其他 agent 冲突

✅ **修复方案**
```yaml
---
name: feature-dev
description: "功能开发专家：实现新功能。触发条件：新功能开发、实现需求时。"
tools: [Read, Write, Edit, Bash]
---

## Role
You are a feature development specialist.

## Responsibilities
- Analyze requirements
- Design implementation
- Write production code
- Handle edge cases
```

**原则**：每个 agent 职责不超过 5 条，能用 1 句话描述清楚。

---

## 3. 工具集冗余（Tool Redundancy）

### 症状
- 多个 agent 拥有完全相同的工具集
- 职责描述不同但能力相同
- 调用时随机选择一个

### 案例

❌ **错误设计**
```yaml
# code-reviewer.yaml
tools: [Read, Grep, Glob]

# security-reviewer.yaml
tools: [Read, Grep, Glob]

# performance-reviewer.yaml
tools: [Read, Grep, Glob]
```

**问题**：
- 工具集完全相同
- 只有 prompt 不同
- 浪费维护成本

✅ **修复方案**
```yaml
# reviewer.yaml（合并）
tools: [Read, Grep, Glob]
prompt: "Review code for: 1) Security 2) Performance 3) Style"

# 或按维度拆分，但工具集不同
# security-reviewer.yaml（专用工具）
tools: [Read, Grep, SecurityScanner]

# performance-reviewer.yaml（专用工具）
tools: [Read, Grep, Profiler]
```

**原则**：工具集完全相同的 agent 应该合并，除非有特殊理由。

---

## 4. 忽视上下文污染（Context Pollution）

### 症状
- 单 agent 处理复杂任务，历史记录爆炸
- 早期探索信息淹没后续决策
- "Wait, what was in file1 again?"

### 案例

❌ **错误设计**
```
Main Agent:
  1. Read 20 files to explore codebase
  2. Now refactor authentication...
  3. "Wait, where was the auth logic?"
```

**问题**：
- 探索阶段污染主上下文
- 重构时失去焦点
- Token 使用效率低

✅ **修复方案**
```
Main Agent:
  1. Task(explore): "Find auth-related files"
     → Subagent reads 20 files
     → Returns: "Auth is in src/auth/"
  2. Now refactor with clean context
     → Focus on src/auth/ only
```

**原则**：探索型任务委托给 subagent，保持主上下文干净。

---

## 5. 权限过度（Over-permission）

### 症状
- Agent 拥有不需要的写权限
- Subagent 使用 `permission: ask`（阻塞）
- `tools: "*"` 给予所有工具

### 案例

❌ **错误设计**
```yaml
# 只读审查 agent 拥有写权限
tools:
  write: true
  edit: true
permission:
  edit: allow
  bash: allow
```

**问题**：
- 审查 agent 可能意外修改代码
- 安全风险
- 违反职责边界

✅ **修复方案**
```yaml
# 只读审查 agent
tools:
  write: false
  edit: false
permission:
  read: allow
  grep: allow
  edit: deny
  bash: deny
```

**原则**：
- 只给必要权限
- Subagent 只能用 `allow/deny`，不能用 `ask`
- 审查类 agent 设为只读

---

## 6. 触发条件模糊（Vague Triggers）

### 症状
- Description 太宽泛："Helps with code"
- 用户不知道该何时调用
- Agent 被误触发或不被触发

### 案例

❌ **错误设计**
```yaml
description: "Helps developers write better code"
```

**问题**：
- 何时触发？不清楚
- 做什么？不清楚

✅ **修复方案**
```yaml
description: "代码安全审查专家：检查 SQL 注入、XSS 等漏洞。触发条件：代码审查、PR review、安全检查时。"
```

**原则**：Description 必须包含：
1. 做什么（能力）
2. 何时用（触发条件）
3. 具体关键词

---

## 7. 资源罗列（Resource Enumeration）

### 症状
- Available Resources 列出所有 skills/MCP
- 20+ 项资源，agent 无法聚焦
- 资源与职责无关

### 案例

❌ **错误设计**
```markdown
## Available Resources

### Skills
- skill-creator
- glue-coding
- architecture-spec
- canvas-dev
- docx
- pdf
- xlsx
- android-development
- android-test-engineer
- ... (20+ more)

### MCP Servers
- mcp-github
- mcp-slack
- mcp-notion
- ... (10+ more)
```

**问题**：
- 资源太多，agent 不知道用哪个
- 无关资源分散注意力

✅ **修复方案**
```markdown
## Available Resources

### Skills
- `glue-coding` - 优先复用成熟库，编写最小胶水代码
- `architecture-spec` - 分析架构问题，生成架构图

### MCP Servers
- `mcp-github` - 查询 PR、Issues、代码库状态
```

**原则**：只列出 2-5 个最相关的资源，agent 实际会用到的。

---

## 8. 缺乏约束（Missing Constraints）

### 症状
- Constraints 章节空泛："Be careful"
- Agent 不知道不能做什么
- 经常越界操作

### 案例

❌ **错误设计**
```markdown
## Constraints
- Be careful
- Pay attention to quality
- Don't make mistakes
```

**问题**：
- 无法执行
- 太主观

✅ **修复方案**
```markdown
## Constraints
- 不要修改测试文件（*.test.ts, *.spec.ts）
- 只输出审查意见，不直接修改代码
- 发现严重问题时标注具体行号
- 每个意见必须包含：严重级别 + 位置 + 建议
```

**原则**：约束要具体、可执行、可验证。

---

## 9. 模型选择不当（Wrong Model）

### 症状
- 简单任务用 Opus（浪费）
- 复杂任务用 Haiku（质量差）
- 所有 agent 用相同模型

### 案例

❌ **错误设计**
```yaml
# 代码格式化 agent 用 Opus
model: opencde/opus-4.6
description: "Format code according to style guide"
```

**问题**：
- 格式化是模式匹配，不需要深度推理
- Opus 成本高，速度慢

✅ **修复方案**
```yaml
# 代码格式化 agent 用 Haiku
model: opencde/haiku-4.5
description: "Format code according to style guide"

# 架构设计 agent 用 Opus
model: opencde/opus-4.6
description: "Design system architecture for complex requirements"
```

**原则**：
- 模式匹配（格式化、lint）→ Haiku
- 日常编码（实现、调试）→ Sonnet
- 深度推理（架构、研究）→ Opus

---

## 10. 跳过设计直接创建（Design-less Creation）

### 症状
- 用户说"创建几个 agent"，立即开始创建
- 没有讨论切分策略
- 创建后发现不合适再修改

### 案例

❌ **错误流程**
```
User: "帮我创建几个 subagent"
AI: 立即开始创建 agent 文件...
```

**问题**：
- 可能切分不合理
- 后期重构成本高

✅ **正确流程**
```
User: "帮我创建几个 subagent"
AI:
  1. 询问项目类型、技术栈、任务复杂度
  2. 分析选择功能切分 vs 场景切分
  3. 设计 agent 架构和边界
  4. 用户确认设计方案
  5. 调用 agent-creator 执行创建
```

**原则**：先设计，后创建。使用 `agent-design` 设计方案，再用 `agent-creator` 执行。

---

## 修复优先级

| 错误 | 影响 | 修复难度 | 优先级 |
|------|------|---------|--------|
| 过度拆分 | 高 | 中 | P0 |
| 万能 Agent | 高 | 中 | P0 |
| 权限过度 | 高 | 低 | P0 |
| 上下文污染 | 中 | 低 | P1 |
| 触发模糊 | 中 | 低 | P1 |
| 工具集冗余 | 低 | 中 | P2 |
| 资源罗列 | 低 | 低 | P2 |
| 缺乏约束 | 中 | 低 | P2 |
| 模型不当 | 中 | 低 | P2 |
| 跳过设计 | 高 | 低 | P0 |

---

## Related

- `decision-framework.md` - 完整决策框架
- `splitting-strategies.md` - 功能切分 vs 场景切分
- `architecture-patterns.md` - 4 大架构模式
