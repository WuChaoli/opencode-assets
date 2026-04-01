# 权限优化指南

## tools vs permission

| 字段 | 层级 | 作用 | 值类型 |
|------|------|------|--------|
| `tools` | 上游 | 控制工具是否可用 | boolean |
| `permission` | 下游 | 控制工具如何执行 | ask/allow/deny |

## 权限配置原则

### 最小权限原则

只给 Agent 必要的权限：

```yaml
# 只读审查 Agent
tools:
  write: false
  edit: false
  bash: false
permission:
  edit: deny
  bash: deny
  webfetch: allow
```

### 常见 Agent 权限配置

| Agent 类型 | tools | permission |
|-----------|-------|------------|
| 只读审查 | write/edit/bash: false | edit: deny, bash: deny |
| 规划分析 | 默认 | edit: ask, bash: ask |
| 文档编写 | bash: false | edit: allow, bash: deny |
| 完整开发 | 默认 | 默认 (allow) |

## 权限调优步骤

1. 分析 Agent 职责
2. 确定必要工具集
3. 配置 tools 字段关闭不需要的
4. 配置 permission 字段精细化控制
5. 测试验证行为
