# 改编现有 Agent 的指南

## 改编原则

1. **尊重开源协议**: 检查原 Agent 的 LICENSE 文件
2. **注明来源**: 在 Agent 文件的 Maintenance 章节注明原始来源
3. **保持兼容**: 改编后仍符合 OpenCode agent 格式
4. **最小修改**: 只修改必要的部分，保持原有结构

## 改编流程

### Step 1: 获取原始 Agent

```bash
# 从 Claude Code Market 下载
curl -o agent-name.md https://marketplace.claude.com/agents/agent-name/download

# 从 GitHub 下载
curl -o agent-name.md https://raw.githubusercontent.com/xxx/agent-name/main/agent-name.md
```

### Step 2: 分析差异

对比用户需求与现有 Agent：

| 对比项 | 现有 Agent | 用户需求 | 需要修改？ |
|--------|-----------|---------|-----------|
| 功能范围 | [列出] | [列出] | [是/否] |
| 触发条件 | [列出] | [列出] | [是/否] |
| 权限配置 | [列出] | [列出] | [是/否] |
| 可用资源 | [列出] | [列出] | [是/否] |

### Step 3: 执行修改

**修改 Agent 文件**:

```markdown
---
description: <新描述>
mode: <primary|subagent>
# Based on: <原始来源>
---

# <新名称> Agent

[基于 <原始来源> 改编]

## Role
[更新角色定义]

## Responsibilities
[更新职责]

## Available Resources
[更新资源推荐]

## Constraints
[更新约束]

## Maintenance
- Based on: <原始来源链接>
- Original author: <原作者>
- License: <原协议>
- Last updated: <日期>
```

### Step 4: 验证

```bash
# 运行验证脚本
python scripts/validate_agent.py <agent-path>

# 手动检查
- [ ] Frontmatter 正确
- [ ] 所有章节存在
- [ ] Available Resources 存在
- [ ] 来源已注明
```

### Step 5: 文档化

在改编后的 Agent 中注明：

```markdown
## Maintenance

- Based on: https://www.ccmarket.dev/agents/original-agent
- Original author: @username
- License: MIT
- Adapted by: <你的名字>
- Last updated: 2026-04-01
- Changes:
  - Added: [新增内容]
  - Modified: [修改内容]
  - Removed: [删除内容]
```

## 常见改编场景

### 场景 1: 功能扩展

**原 Agent**: 只支持代码审查
**需求**: 需要代码审查 + 安全审计

**改编方式**:
- 保留原有审查逻辑
- 添加安全检查规则
- 更新 Responsibilities

### 场景 2: 领域适配

**原 Agent**: 通用代码审查
**需求**: Python 项目专用代码审查

**改编方式**:
- 添加 Python 特定规则
- 更新 Examples 为 Python 示例
- 修改 description 注明 Python 专用

### 场景 3: 权限调整

**原 Agent**: 所有权限开启
**需求**: 只读审查

**改编方式**:
- 修改 permission 配置
- 添加 tools 限制
- 更新 Constraints

## 改编检查清单

- [ ] 已检查原 Agent 的 LICENSE
- [ ] 已注明原始来源
- [ ] 已保留原作者信息
- [ ] 修改部分有明确记录
- [ ] 改编后符合 OpenCode agent 格式
- [ ] 运行验证脚本通过
- [ ] 测试改编后的功能
