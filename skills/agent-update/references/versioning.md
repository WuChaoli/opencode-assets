# 版本管理

## 语义化版本 (SemVer)

Agent 版本格式：`MAJOR.MINOR.PATCH`

### 版本号规则

| 变更类型 | 版本变化 | 示例 |
|---------|---------|------|
| 不兼容的变更 | MAJOR +1 | 1.0.0 → 2.0.0 |
| 向后兼容的功能添加 | MINOR +1 | 1.0.0 → 1.1.0 |
| 向后兼容的 bug 修复 | PATCH +1 | 1.0.0 → 1.0.1 |

## 变更记录格式

在 agent.md 的 Maintenance 章节中记录：

```markdown
## Maintenance

- Version: 1.2.0
- Last updated: 2026-04-01
- Changes:
  - Added: [新增内容]
  - Fixed: [修复问题]
  - Changed: [修改内容]
  - Removed: [删除内容]
```
