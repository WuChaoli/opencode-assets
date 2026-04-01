---
name: agent-creator
description: 元技能：创建 OpenCode Agent（primary/subagent）。触发条件：创建新 agent、配置 agent、用户提到创建 agent、agent creator、new agent 时
---

# agent-creator 元技能

将需求转化为标准化的 OpenCode Agent 配置。遵循 glue-coding 原则：先搜索现有 Agent，再决定创建/复用/改编。

## When to Use This Skill

触发条件（满足任一即可）：
- 用户提到"创建 agent"、"new agent"、"agent creator"
- 需要配置 primary agent（Build/Plan 之外的主代理）
- 需要配置 subagent（General/Explore 之外的子代理）
- 需要调整 agent 权限、模型、prompt

## Not For / Boundaries

此技能不适用于：
- 修改 OpenCode 内置 agent（Build/Plan/General/Explore）
- 跳过搜索直接创建（违反 glue-coding 原则）
- 跳过用户确认直接创建

必要输入（缺失时需询问）：
1. Agent 用途/场景
2. 需要哪些工具权限
3. 期望的触发方式（Tab 切换 / @ 调用）
4. 期望使用的模型

## 工作流程（8 步，严格按顺序执行）

### 阶段一：需求确认

**Step 1: 深度沟通确认需求**
- Agent 要解决什么问题？目标用户是谁？
- 是 primary（Tab 切换）还是 subagent（@ 调用/自动触发）？
- 需要哪些工具权限？（读写/只读/网络访问）
- 期望使用哪个模型？（不同模型适合不同场景）
- 目标技术栈/框架是什么？（如 React/Vue/Android 等）
- 用 3-5 个问题澄清模糊点，确保充分理解需求

**Step 1.5: 模型建议（如用户未指定）**
- 开发型 agent: 推荐 `opencode/claude-sonnet-4-6`（速度快、代码质量高）
- 分析型 agent: 推荐 `opencode/gpt-5.4`（推理能力强）
- 创意型 agent: 推荐高 temperature 模型
- 如用户不确定，使用 `model-guide` skill 协助选择

### 阶段二：搜索与评估

**Step 2: 搜索现有 Agent**
- **Claude Code Market**：https://www.ccmarket.dev/agents
- **awesome-opencode**：github.com/awesome-opencode/awesome-opencode
- **GitHub 搜索**：`opencode agent` + 关键词
- 整理搜索结果，记录候选 Agent

**Step 3: 评估搜索结果**
- **功能匹配度**：0-100%
- **质量指标**：下载量、评分、更新日期
- 决策：匹配度 > 80% → 安装；50-80% → 改编；< 50% → 参考后创建；无结果 → 从零创建
- 向用户展示评估结果，确认下一步

### 阶段二点五：Skill 依赖分析

**Step 3.5: 分析并创建 Agent 所需的 Skills**
- 基于 Agent 的职责，分析需要哪些 Skills 支持：
  - 检查本地已有 Skills（`~/.config/opencode/skills/` 和 `.opencode/skills/`）
  - 列出缺失但必需的 Skills
- 对每个缺失的 Skill：
  - 调用 `skill-creator` 工作流搜索现有 Skills（SkillsMP/GitHub/Anthropic 官方）
  - 匹配度 > 50% → 推荐安装/改编
  - 匹配度 < 50% 或无结果 → 调用 `skill-creator` 从零创建
- 向用户展示 Skill 依赖清单，确认创建/安装方案
- **Agent 创建前，确保所有依赖 Skills 已就绪**
- 如用户不需要额外 Skills，可跳过此步

### 阶段三：方案设计

**Step 4: 调研与设计**
- 搜索网上可复用的 agent 实现和最佳实践
- 基于需求、搜索结果和调研，设计 agent：
  - 类型决策：primary vs subagent（见类型决策树）
  - Prompt 内容：角色 + 职责 + 可用资源 + 约束
- **权限配置（必须用户确认）**：
  - 展示 `tools` 配置建议（哪些工具开启/关闭）
  - 展示 `permission` 配置建议（ask/allow/deny）
  - 等待用户确认或修改权限配置
  - **未经用户确认，不得确定权限配置**
- 输出设计草案（包含已确认的权限配置）

**Step 5: 与用户确认方案**
- 展示：来源说明、名称/类型/描述、权限配置、Prompt 核心内容、依赖 Skills 清单
- 等待用户确认或提出修改意见
- **未经用户确认，不得开始创建**

**Step 6: 确认创建位置**
- **项目级**（默认）：`.opencode/agents/`
- **系统级**：`~/.config/opencode/agents/`
- **自定义**：用户指定的其他路径

### 阶段四：执行创建

**Step 7: 创建/改编 Agent**
- 改编：下载现有 Agent 并修改，注明来源
- 创建：运行脚手架 `python {baseDir}/scripts/init_agent.py <name> --type <primary|subagent> --path <dir>`

**Step 8: 验证与交付**
- 运行验证：`python {baseDir}/scripts/validate_agent.py <agent-path>`
- 或手动检查 `{baseDir}/references/quality-checklist.md`
- 向用户展示创建的 agent，说明使用方式和维护建议

## YAML Frontmatter 配置

详见 `references/quick-reference.md` 中的完整配置指南。

核心规则：
- `description` 和 `mode` 必填
- `model`/`temperature`/`steps` 可选，默认继承全局
- Subagent 的 `permission` 只能使用 `allow/deny`，禁止使用 `ask`
- Primary Agent 可使用 `ask/allow/deny` 全部三种模式

## Examples

### Example 1: 从零创建 subagent（含 Skill 依赖）

用户: 帮我创建一个代码审查 agent
→ Step 1-3: 确认需求 → 搜索 → 无匹配 → 从零创建
→ Step 3.5: 分析 Skill 依赖
  - 检查本地：缺少 `architecture-spec` → 调用 `skill-creator` 搜索 SkillsMP → 找到并安装
  - 依赖清单：`glue-coding`（已有）、`architecture-spec`（新安装）→ 用户确认
→ Step 4: 设计 draft → 展示权限配置（tools.write=false, edit=deny, bash=deny）→ 用户确认
→ Step 5-8: 确认方案 → 确认位置 → 创建 → 验证 + 交付

### Example 2: 改编现有 agent

用户: 把 CC Market 的 QA Engineer 改成 Python 专用的
→ Step 2-3: 找到 QA Engineer（匹配度 65%）→ 推荐改编
→ Step 3.5: 检查本地 Skills → 全部存在 → 无需额外创建
→ Step 4: 分析差异 → 展示权限配置（tools.write=true, edit=allow, bash=allow）→ 用户确认
→ Step 5-8: 确认方案 → 下载修改 → 验证 + 交付

### Example 3: 创建需要多个新 Skills 的 agent

用户: 创建一个能分析数据库性能并生成报告的 agent
→ Step 1-3: 确认需求 → 搜索 → 无匹配 → 从零创建
→ Step 3.5: 分析 Skill 依赖
  - 缺少 `db-analyzer` 和 `xlsx` → 调用 `skill-creator`
  - `xlsx` 找到官方实现 → 安装；`db-analyzer` 无匹配 → 从零创建
  - 依赖清单 → 用户确认
→ Step 4-8: 设计 → 确认权限 → 确认方案 → 创建 → 验证 + 交付

## 创作规则（不可协商）

1. 权限最小化：只给必要的工具权限
2. 描述必须可判定：包含具体使用场景
3. Prompt 必须包含 Available Resources（Skills/MCP/Tools）
4. **必须先搜索现有 Agent**，不要重复造轮子
5. **必须用户确认后再创建**，不要自作主张
6. 改编时注明来源，尊重开源协议
7. **必须分析并解决 Agent 的 Skill 依赖**，确保 Agent 有所需技能支持
8. **Subagent 的 permission 只能使用 allow/deny**，禁止使用 ask

详细规范见 `references/agent-spec.md`，常见模式见 `references/common-patterns.md`。

## 工具

- 搜索：`python {baseDir}/scripts/search_agents.py <关键词>`
- 验证：`python {baseDir}/scripts/validate_agent.py <agent-path>`
- 脚手架：`python {baseDir}/scripts/init_agent.py <name> --type <type> --path <dir>`

## References

- `references/index.md` - 完整导航
- `references/quick-reference.md` - Quick Reference（决策树/模板/权限表/搜索策略）
- `references/agent-spec.md` - Agent 规范详解（MUST/SHOULD/NEVER）
- `references/quality-checklist.md` - 质量检查清单
- `references/common-patterns.md` - 模式与反模式
- `references/evaluation-guide.md` - 评估标准与决策流程
- `references/adaptation-guide.md` - 改编指南
- `model-guide` skill - 模型选择
- `assets/template-primary.md` / `template-subagent.md` - 模板

## Maintenance

- Last updated: 2026-04-01
- Changes:
  - 新增 Step 3.5：Skill 依赖分析与创建流程（调用 skill-creator 同步创建/下载所需 Skills）
  - 修改 Step 4：权限配置必须用户确认，不得自动决定
  - 新增 Subagent permission 规范：只能使用 allow/deny，禁止使用 ask
  - 更新 Examples：添加 Skill 依赖分析示例
  - 更新创作规则：新增规则 7（Skill 依赖）和规则 8（subagent permission）
  - 更新 3 种典型场景表格：区分 primary 和 subagent 的 permission 值
- Known limits: 仅支持 OpenCode 格式；跨平台需手动转换
