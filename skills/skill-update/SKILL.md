---
name: skill-update
description: "元技能：迭代优化现有 Skill。触发条件：优化 Skill、改进 Skill、用户提到'skill update'、'skill refactor'、'优化技能'、'重构技能'时。"
---

# skill-update 元技能

诊断、优化、迭代现有 Skill，确保其保持高质量和可靠性。

## When to Use This Skill

触发条件（满足任一即可）：
- 用户提到"优化 Skill"、"改进 Skill"、"skill update"、"skill refactor"
- Skill 触发不可靠（有时触发有时不触发）
- Skill 输出质量下降或出现幻觉
- 需要精简过大的 SKILL.md（超过 200 行）
- 需要更新过时的 references
- 需要根据用户反馈调整行为

## Not For / Boundaries

此技能不适用于：
- 从零创建新 Skill（那是 skill-creator 的事）
- 修改 Skill 的核心用途（那应该创建新 Skill）
- 跳过诊断直接修改

必要输入（缺失时需询问）：
1. 要优化的 Skill 路径或名称
2. 具体问题或改进目标

## 工作流程（7 步，严格按顺序执行）

### 阶段一：诊断分析

**Step 1: 读取并分析当前 Skill**
- 读取 SKILL.md 和 references/ 内容
- 运行审计脚本统计行数、结构完整性
- 识别以下问题：
  - 内容膨胀（SKILL.md > 200 行）
  - 结构缺失（缺少 When to Use/Not For/Examples）
  - 指令冲突（前后矛盾的说明）
  - 范围漂移（做了太多事）
  - 示例不可复现
  - 触发词模糊

**Step 2: 收集反馈和问题**
- 询问用户具体问题：
  - 什么场景下不好用？
  - 期望的改进方向？
- 如果没有具体反馈，基于诊断结果提出改进建议

### 阶段二：方案设计

**Step 3: 制定优化方案**
- 基于诊断结果，制定具体修改计划：
  - 精简：哪些内容移到 references/
  - 补充：哪些章节缺失需要添加
  - 修正：哪些指令冲突需要解决
  - 拆分：是否需要按工作流拆分 Skill
  - 更新：哪些 references 需要更新
- 输出修改预览（diff 形式）

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
- 确认 SKILL.md 行数 < 200
- 确认所有必须章节存在

**Step 7: 交付与说明**
- 展示修改内容摘要
- 说明如何测试改进效果
- 建议后续观察点

## Quick Reference

### 诊断检查清单

| 检查项 | 标准 | 修复方式 |
|--------|------|---------|
| SKILL.md 行数 | < 200 行 | 移到 references/ |
| description | 包含具体触发词 | 添加关键词 |
| When to Use | 存在且具体 | 补充触发条件 |
| Not For | 存在且清晰 | 补充边界说明 |
| Quick Reference | <= 20 个模式 | 移到 references/ |
| Examples | >= 3 个可复现 | 补充或修正示例 |
| 指令冲突 | 无矛盾说明 | 消除冲突指令 |
| references 导航 | 有 index.md | 创建导航文件 |

### 优化策略

| 问题 | 策略 | 示例 |
|------|------|------|
| 内容太长 | 拆分到 references/ | API 文档移到 references/api.md |
| 触发不可靠 | 优化 description | 添加具体关键词 |
| 示例不可用 | 补充前提条件 | 添加环境/依赖说明 |
| 指令冲突 | 消除矛盾 | 统一输出格式要求 |
| 范围太广 | 按工作流拆分 | 拆成 skill-a + skill-b |
| 内容过时 | 更新 references | 替换废弃 API 引用 |

### 200 行规则

- SKILL.md 应保持在 200 行以内
- 超过 200 行时，优先拆分到 references/
- references/ 文件保持在 300 行以内

### 创作规则（不可协商）
1. 先诊断再修改，不要盲目修改
2. 必须用户确认后再修改
3. 保持向后兼容，不破坏现有触发
4. 每次只改 1-2 个变量，方便归因
5. 更新 Maintenance 章节记录变更

## 审计工具

- 运行 `python {baseDir}/scripts/audit_skill.py <skill-path>` 生成诊断报告
- 运行 `{baseDir}/../skill-creator/scripts/validate_skill.py <skill-path>` 验证质量

## References

- `references/index.md` - 导航
- `references/diagnostic-guide.md` - 诊断指南
- `references/refactor-patterns.md` - 重构模式
- `references/versioning.md` - 版本管理
- `assets/update-report.md` - 更新报告模板

## Maintenance

- Last updated: 2026-04-01
- Known limits: 需要用户反馈才能精准优化；自动诊断只能发现结构问题
