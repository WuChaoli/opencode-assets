---
name: model-guide
description: "元技能：帮助用户/Agent 选择 OpenCode 模型。触发条件：选择模型、推荐模型、用户提到'model guide'、'model selector'、'选择模型'、'哪个模型好'时。"
---

# model-guide 元技能

帮助用户和 Agent 在 OpenCode 海量模型中选择最合适的模型。

## When to Use This Skill

触发条件（满足任一即可）：
- 用户提到"选择模型"、"推荐模型"、"model guide"、"哪个模型好"
- 需要为特定任务推荐合适的模型
- 需要估算模型使用成本
- 需要配置新的 Provider
- 需要了解不同模型的能力差异

## Not For / Boundaries

此技能不适用于：
- 直接修改模型配置（那是手动操作）
- 推荐 OpenCode 之外的模型
- 跳过用户需求直接推荐

必要输入（缺失时需询问）：
1. 任务类型（编码/调试/架构/文档等）
2. 优先级（速度/成本/质量）
3. 是否有多模态需求

## 工作流程（5 步）

### Step 1: 了解需求

询问用户：
- 主要做什么任务？
- 更看重速度、成本还是质量？
- 是否需要图片/文档理解？
- 预算范围？

### Step 2: 推荐方案

根据需求提供阶梯性方案：
- 速度优先方案
- 成本优先方案
- 质量优先方案
- 平衡方案

每个方案包含：
- 推荐模型
- 预估成本
- 预估速度
- 预期质量

### Step 3: 展示对比

展示相关模型的横向对比：
- 基本信息
- 成本对比
- 能力评分
- 适用场景

### Step 4: 配置引导

如果用户需要配置：
- 指导 Provider 配置
- 指导 API Key 设置
- 验证配置是否生效

### Step 5: 交付说明

- 说明如何使用推荐模型
- 提供成本估算参考
- 建议后续观察点

## Quick Reference

### 模型选择决策树

```
需要多模态（图片/文档）？
  ├─ 是 → Claude 系列 / Gemini
  └─ 否 → 看任务类型
      ├─ 日常编码 → Sonnet 级别
      ├─ 复杂任务 → Opus 级别
      ├─ 简单查询 → Haiku 级别
      └─ 预算有限 → 免费模型
```

### 阶梯性方案速查

| 场景 | 速度优先 | 成本优先 | 质量优先 | 平衡方案 |
|------|---------|---------|---------|---------|
| 日常编码 | opencode/claude-haiku-4-5 | opencode/qwen3.6-plus-free | opencode/claude-sonnet-4-6 | opencode/claude-sonnet-4-6 |
| 复杂重构 | opencode/claude-sonnet-4-6 | opencode/claude-haiku-4-5 | opencode/claude-opus-4-6 | opencode/claude-sonnet-4-6 |
| 架构设计 | opencode/claude-sonnet-4-6 | opencode/claude-haiku-4-5 | opencode/claude-opus-4-6 | opencode/claude-sonnet-4-6 |
| Bug 调试 | opencode/claude-sonnet-4-6 | opencode/claude-haiku-4-5 | opencode/claude-opus-4-6 | opencode/claude-sonnet-4-6 |
| UI 开发 | opencode/claude-sonnet-4-6 | opencode/qwen3.6-plus-free | opencode/claude-sonnet-4-6 | opencode/claude-sonnet-4-6 |
| 文档编写 | opencode/claude-haiku-4-5 | opencode/qwen3.6-plus-free | opencode/claude-sonnet-4-6 | opencode/claude-haiku-4-5 |

### 成本估算公式

```
成本 = (输入 tokens / 1M) × 输入单价 + (输出 tokens / 1M) × 输出单价
```

典型场景 token 估算：
- 简单查询：~5K tokens
- 日常编码：~50K tokens
- 复杂重构：~200K tokens
- 大型项目：~500K+ tokens

### Zen 模型价格速查

| 模型 | 输入 ($/1M) | 输出 ($/1M) | 特点 |
|------|------------|------------|------|
| Qwen3.6 Plus Free | 免费 | 免费 | 免费可用 |
| MiniMax M2.5 Free | 免费 | 免费 | 免费可用 |
| Claude Haiku 4.5 | $1.00 | $5.00 | 快速便宜 |
| Claude Sonnet 4.6 | $3.00 | $15.00 | 平衡性价比 |
| Claude Opus 4.6 | $5.00 | $25.00 | 最强推理 |
| GPT 5.3 Codex | $1.75 | $14.00 | 编码专用 |

### 创作规则（不可协商）
1. 先了解需求再推荐，不要盲目推荐
2. 提供阶梯性方案，让用户有选择
3. 成本估算要透明
4. 推荐基于 OpenCode Zen 平台

## 工具

- 运行 `{baseDir}/scripts/cost_estimate.py --input <tokens> --output <tokens> --model <model>` 估算成本

## References

- `references/index.md` - 导航
- `references/zen-models.md` - Zen 平台模型详解
- `references/provider-setup.md` - Provider 配置指南
- `references/cost-calculator.md` - 成本估算指南
- `references/model-comparison.md` - 模型横向对比
- `assets/decision-tree.md` - 决策树可视化

## Maintenance

- Last updated: 2026-04-01
- Known limits: 模型价格可能变动，以官方为准；免费模型可能随时下线
