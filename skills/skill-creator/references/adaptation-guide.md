# 改编现有 Skill 的指南

## 改编原则

1. **尊重开源协议**: 检查原 Skill 的 LICENSE 文件
2. **注明来源**: 在 SKILL.md 的 Maintenance 章节注明原始来源
3. **保持兼容**: 改编后仍符合 SKILL.md 规范
4. **最小修改**: 只修改必要的部分，保持原有结构

## 改编流程

### Step 1: 获取原始 Skill

```bash
# Clone 整个仓库
git clone <repo-url>

# 或只下载 Skill 目录
svn export <repo-url>/trunk/skills/<skill-name> <skill-name>
```

### Step 2: 分析差异

对比用户需求与现有 Skill：

| 对比项 | 现有 Skill | 用户需求 | 需要修改？ |
|--------|-----------|---------|-----------|
| 功能范围 | [列出] | [列出] | [是/否] |
| 触发条件 | [列出] | [列出] | [是/否] |
| 输出格式 | [列出] | [列出] | [是/否] |
| 依赖项 | [列出] | [列出] | [是/否] |

### Step 3: 执行修改

**修改 SKILL.md**:

```markdown
---
name: <新名称>
description: <新描述>
---

# <新名称> Skill

[基于 <原始来源> 改编]

## When to Use This Skill
[更新触发条件]

## Not For / Boundaries
[更新边界]

## Quick Reference
[更新模式]

## Examples
[更新示例]

## References
[更新引用]

## Maintenance
- Based on: <原始来源链接>
- Original author: <原作者>
- License: <原协议>
- Last updated: <日期>
```

**修改 references/**:

- 保留相关的参考文档
- 删除不需要的
- 添加新的

**修改 scripts/**:

- 保留可用的脚本
- 修改不适配的
- 添加缺失的

### Step 4: 验证

```bash
# 运行验证脚本
python scripts/validate_skill.py <skill-path>

# 手动检查
- [ ] Frontmatter 正确
- [ ] 所有章节存在
- [ ] Examples >= 3
- [ ] 来源已注明
```

### Step 5: 文档化

在改编后的 Skill 中注明：

```markdown
## Maintenance

- Based on: https://github.com/xxx/original-skill
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

**原 Skill**: 只支持 PDF 提取
**需求**: 需要支持 PDF 提取 + 合并 + 转换

**改编方式**:
- 保留原有提取逻辑
- 添加合并和转换模块
- 更新 Quick Reference

### 场景 2: 领域适配

**原 Skill**: 通用代码审查
**需求**: Python 项目专用代码审查

**改编方式**:
- 添加 Python 特定规则
- 更新 Examples 为 Python 示例
- 修改 description 注明 Python 专用

### 场景 3: 规范对齐

**原 Skill**: 使用旧版 SKILL.md 格式
**需求**: 适配最新规范

**改编方式**:
- 更新 frontmatter 格式
- 调整章节顺序
- 添加缺失的必须章节

### 场景 4: 工具链集成

**原 Skill**: 独立运行
**需求**: 集成到项目工作流

**改编方式**:
- 添加 scripts/ 目录
- 创建自动化脚本
- 更新 references/ 文档

## 改编检查清单

- [ ] 已检查原 Skill 的 LICENSE
- [ ] 已注明原始来源
- [ ] 已保留原作者信息
- [ ] 修改部分有明确记录
- [ ] 改编后符合 SKILL.md 规范
- [ ] 运行验证脚本通过
- [ ] 测试改编后的功能
