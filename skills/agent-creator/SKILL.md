---
name: agent-creator
description: "元技能：创建 OpenCode Agent（primary/subagent）。触发条件：创建新 agent、配置 agent、用户提到'创建 agent'、'agent creator'、'new agent'时。"
---

# agent-creator 元技能

将需求转化为标准化的 OpenCode Agent 配置（`.opencode/agents/xxx.md` 或 `opencode.json`）。遵循 glue-coding 原则：先搜索现有 Agent，再决定创建/复用/改编。

## When to Use This Skill

触发条件（满足任一即可）：
- 用户提到"创建 agent"、"new agent"、"agent creator"
- 需要配置 primary agent（Build/Plan 之外的主代理）
- 需要配置 subagent（General/Explore 之外的子代理）
- 需要调整 agent 权限、模型、prompt

## Not For / Boundaries

此技能不适用于：
- 修改 OpenCode 内置 agent（Build/Plan/General/Explore）
- 创建跨平台 agent（那是通用 agent 定义的事）
- 跳过搜索直接创建（违反 glue-coding 原则）
- 跳过用户确认直接创建

必要输入（缺失时需询问）：
1. Agent 用途/场景
2. 需要哪些工具权限（读/写/bash/网络）
3. 期望的触发方式（Tab 切换 / @ 调用）

## 工作流程（10 步，严格按顺序执行）

### 阶段一：需求确认

**Step 1: 沟通确认需求**
- 与用户充分沟通，确保完全理解：
  - Agent 要解决什么问题？
  - 是 primary（Tab 切换）还是 subagent（@ 调用/自动触发）？
  - 需要哪些工具权限？
- 用 1-3 个问题澄清模糊点
- 确认用户对需求理解无异议后再继续

### 阶段二：搜索与评估

**Step 2: 搜索现有 Agent**
- **Claude Code Market**（53+ agents，50K+ 下载）：
  - 访问 https://www.ccmarket.dev/agents 搜索
  - 按分类浏览（Frontend/Backend/Testing/DevOps 等）
  - 查看评分和下载量
- **awesome-opencode**（4235 stars）：
  - 访问 github.com/awesome-opencode/awesome-opencode
  - 查看 Agents 章节
- **GitHub 搜索**：
  - 搜索 `opencode agent` + 关键词
  - 搜索 `.opencode/agents/` 目录
- 整理搜索结果，记录候选 Agent

**Step 3: 评估搜索结果**
- 对每个候选 Agent 评估：
  - **功能匹配度**：是否覆盖用户需求？（0-100%）
  - **质量指标**：下载量、评分、更新日期
  - **兼容性**：是否符合 OpenCode agent 格式？
  - **可改编性**：是否容易适配用户需求？
- 根据评估结果决策：
  - 匹配度 > 80% → 推荐直接安装
  - 匹配度 50-80% → 推荐改编
  - 匹配度 < 50% → 推荐参考后创建
  - 无结果 → 从零创建
- 向用户展示评估结果，确认下一步

### 阶段三：方案设计

**Step 4: 在线调研**
- 搜索网上可复用的 agent 实现：
  - 类似用途的 agent 配置
  - 最佳实践和常见陷阱
- 整理调研结果，提炼可复用模式

**Step 5: 设计方案**
- 基于需求、搜索结果和调研，设计 agent：
  - 如果是改编：确定需要修改的部分
  - 如果是创建：设计 prompt 结构
  - 类型决策：primary vs subagent
  - 权限范围：最小化原则
  - Prompt 内容：角色 + 职责 + 可用资源 + 约束
- 输出设计草案

**Step 6: 与用户确认方案**
- 向用户展示设计草案：
  - 来源说明（改编/参考/从零创建）
  - Agent 名称、类型、描述
  - 权限配置
  - Prompt 核心内容
- 等待用户确认或提出修改意见
- **未经用户确认，不得开始创建**

**Step 7: 确认创建位置**
- 询问用户 agent 创建位置：
  - **项目级**（默认）：`.opencode/agents/`
  - **系统级**：`~/.config/opencode/agents/`
  - **自定义**：用户指定的其他路径
- 确认目标路径存在或可创建

### 阶段四：执行创建

**Step 8: 创建/改编 Agent**
- 如果是改编：下载现有 Agent 并修改
- 如果是创建：运行脚手架脚本
  - `python {baseDir}/scripts/init_agent.py <name> --type <primary|subagent> --path <dir>`
- 按确认的方案填充内容
- 改编时注明来源，尊重开源协议

**Step 9: 质量验证**
- 运行验证脚本：
  - `python {baseDir}/scripts/validate_agent.py <agent-path>`
- 或手动检查 `{baseDir}/references/quality-checklist.md`
- 修复所有失败项

**Step 10: 交付与说明**
- 向用户展示创建的 agent
- 说明如何使用和测试
- 告知后续维护建议

## Quick Reference

### Agent 类型决策树

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

### 目录结构
```
.opencode/agents/
├── code-reviewer.md          # Subagent 示例
├── docs-writer.md            # Subagent 示例
└── security-auditor.md       # Subagent 示例
```

### Markdown Agent 格式
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

[角色定义 + 职责 + 可用资源 + 约束]
```

### tools vs permission

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

### Agent Prompt 结构

一个完整的 Agent prompt 应包含：

```markdown
---
description: [做什么 + 何时使用]
mode: [primary|subagent]
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
- `another-skill` - [用途说明]

### MCP Servers（可用的 MCP 工具）
- `mcp-name` - [用途说明]

### Tools（可用的工具）
- `tool-name` - [用途说明]

## Constraints
- [约束 1]
- [约束 2]
```

### 资源推荐原则
1. **Skills**：推荐与 agent 职责相关的流程性知识
2. **MCP**：推荐 agent 需要的外部系统连接
3. **Tools**：推荐 agent 需要的内置工具
4. **只推荐必要的**：不要罗列所有可用资源，只列真正会用到的

### 权限最小化原则

| Agent 类型 | edit | bash | webfetch |
|-----------|------|------|----------|
| 只读审查 | deny | deny | allow |
| 规划分析 | ask | ask | allow |
| 文档编写 | allow | deny | allow |
| 完整开发 | allow | allow | allow |

### 模型选择

- 默认不指定 model，继承全局配置
- 需要特定模型时，使用 `model-guide` skill 获取最新推荐

### 搜索策略

| 来源 | 规模 | 访问方式 | 特点 |
|------|------|---------|------|
| Claude Code Market | 53+ agents | 网站 | 专业 sub-agents，评分系统 |
| awesome-opencode | 4235 stars | GitHub | OpenCode 专用 agents |
| GitHub 搜索 | 海量 | code search | 社区广泛贡献 |

### 评估决策树

```
搜索到现有 Agent？
  ├─ 是 → 匹配度 > 80%？
  │   ├─ 是 → 推荐直接安装
  │   └─ 否 → 匹配度 50-80%？
  │       ├─ 是 → 推荐改编
  │       └─ 否 → 推荐参考后创建
  └─ 否 → 从零创建
```

### 创作规则（不可协商）
1. 权限最小化：只给必要的工具权限
2. 描述必须可判定：包含具体使用场景
3. Prompt 必须包含 Available Resources（Skills/MCP/Tools）
4. **必须先搜索现有 Agent**，不要重复造轮子（glue-coding 原则）
5. **必须先调研再创建**，不要闭门造车
6. **必须用户确认后再创建**，不要自作主张
7. 改编时注明来源，尊重开源协议

## 工具

- 搜索：`python {baseDir}/scripts/search_agents.py <关键词>`
- 验证：`python {baseDir}/scripts/validate_agent.py <agent-path>`
- 脚手架：`python {baseDir}/scripts/init_agent.py <name> --type <type> --path <dir>`

## References

- `references/index.md` - 导航
- `references/agent-spec.md` - Agent 规范详解
- `references/quality-checklist.md` - 检查清单
- `references/common-patterns.md` - 模式与反模式
- `references/search-guide.md` - Agent 搜索策略
- `references/evaluation-guide.md` - 评估标准与决策流程
- `references/adaptation-guide.md` - 改编现有 Agent 的指南
- `model-guide` skill - 模型选择指南（34 个 Zen 模型 + 场景推荐）
- `assets/template-primary.md` - Primary Agent 模板
- `assets/template-subagent.md` - Subagent 模板

## Maintenance

- Last updated: 2026-04-01
- Known limits: 仅支持 OpenCode 格式；跨平台需手动转换
