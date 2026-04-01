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
3. 当前模型是否满足需求
4. 技术栈/框架是否有变化

## 工作流程（7 步，严格按顺序执行）

### 阶段一：诊断分析

**Step 1: 深度诊断分析**
- 当前 Agent 在什么场景下表现不佳？
- 期望的改进方向是什么？
- 当前配置的模型是否满足需求？是否需要调整？
- Agent 的目标技术栈/框架是否有变化？
- 用 3-5 个问题澄清模糊点，确保充分理解优化目标

**Step 1.5: 模型评估与优化建议**
- 评估当前 model 配置是否匹配 Agent 类型（格式: `opencode/<model-id>`）：
  - 开发型：推荐 `opencode/claude-sonnet-4-6`
  - 分析型：推荐 `opencode/gpt-5.4`
  - 创意型：推荐高 temperature 模型
- 如不匹配，提出调整建议
- 如用户不确定，使用 `model-guide` skill 协助

**Step 2: 收集反馈和问题**
- 询问用户具体问题：
  - 什么场景下不好用？
  - 期望的改进方向？
- 如果没有具体反馈，基于诊断结果提出改进建议

**Step 2.5: 分析 Agent 的 Skill 依赖**
- 检查 Agent 中 Available Resources 列出的 Skills：
  - 确认列出的 Skills 是否仍然存在于本地
  - 确认 Skills 是否过时或需要更新
- 基于优化后的 Agent 职责，分析是否需要新增 Skills：
  - 如需要新 Skill，调用 `skill-creator` 工作流搜索/创建
  - 如已有 Skill 需要更新，调用 `skill-update` 工作流
- 向用户展示 Skill 依赖变更清单，确认更新方案
- 如无需变更 Skill 依赖，可跳过此步

### 阶段二：方案设计

**Step 3: 制定优化方案**
- 基于诊断结果，制定具体修改计划：
  - 权限：调整 tools/permission 配置
  - Prompt：重写 Role/Responsibilities/Constraints
  - 资源：更新 Available Resources
  - 触发：优化 description
  - 模型：评估并调整 model 字段（如需要）
  - 参数：调整 temperature/steps
- **权限配置（必须用户确认）**：
  - 展示当前权限配置 vs 建议的新配置
  - 说明每个权限变更的原因
  - 等待用户确认或修改权限配置
  - **未经用户确认，不得确定权限配置**
- 输出修改预览（diff 形式，包含已确认的权限配置）

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

详见 `references/diagnostic-guide.md` 和 `references/permission-guide.md`。

核心规则：
- Subagent 的 `permission` 只能使用 `allow/deny`，禁止使用 `ask`
- 权限配置必须用户确认
- 必须分析并更新 Skill 依赖
- 每次只改 1-2 个变量，方便归因

## Examples

### Example 1: 优化触发不可靠的 Agent

用户: 我的代码审查 agent 有时触发有时不触发
→ Step 1: 诊断（什么场景下不触发？期望的触发词是什么？）
→ Step 1.5: 评估模型配置 → 当前配置合理
→ Step 2: 收集反馈 → description 太模糊，缺少具体触发词
→ Step 2.5: 检查 Skill 依赖 → `architecture-spec` 仍存在，无需更新
→ Step 3: 制定方案
  - 优化 description：添加具体触发词（"PR 审查"、"代码质量检查"）
  - 权限配置确认：保持 edit=deny, bash=deny → 用户确认
→ Step 4: 用户确认方案
→ Step 5-7: 执行修改 → 验证 → 交付

### Example 2: 调整 Agent 权限并添加新 Skill

用户: 我的分析 agent 需要访问数据库，还要生成 Excel 报告
→ Step 1: 诊断（需要哪些数据库权限？报告格式是什么？）
→ Step 1.5: 评估模型 → 推荐 opencode/gpt-5.4（分析型）
→ Step 2: 收集反馈 → 需要数据库访问 + Excel 生成能力
→ Step 2.5: 分析 Skill 依赖
  - 检查现有 Skills：缺少 `xlsx` → 调用 `skill-creator` 搜索 → 找到官方实现 → 安装
  - 依赖清单：`xlsx`（新安装）→ 用户确认
→ Step 3: 制定方案
  - 权限变更：bash: deny → allow（数据库查询需要）
  - 新增 Available Resources：`xlsx` skill
  - 权限配置确认 → 用户确认
→ Step 4-7: 确认 → 执行 → 验证 → 交付

### Example 3: Subagent 权限优化（移除 ask）

用户: 我的 subagent 总是卡住等待确认
→ Step 1: 诊断（什么操作卡住了？频率如何？）
→ Step 2: 收集反馈 → permission 中使用了 ask，subagent 后台执行时阻塞
→ Step 2.5: 检查 Skill 依赖 → 全部存在，无需更新
→ Step 3: 制定方案
  - 权限变更：edit: ask → allow（subagent 不能用 ask）
  - 权限变更：bash: ask → deny（不需要 bash 操作）
  - 说明变更原因 → 用户确认
→ Step 4-7: 确认 → 执行 → 验证 → 交付

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
- Changes:
  - 新增 Step 2.5：Skill 依赖分析与更新流程
  - 修改 Step 3：权限配置必须用户确认
  - 新增 Subagent permission 规范：只能使用 allow/deny
  - 新增 Examples 章节（3 个示例）
  - 更新创作规则：新增规则 6-8
- Known limits: 需要用户反馈才能精准优化；自动诊断只能发现结构问题
