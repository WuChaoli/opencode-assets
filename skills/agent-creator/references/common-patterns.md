# 常见模式与反模式

## 好 vs 坏对比

### 1. description 写法

❌ 坏: `"帮助开发者写更好的代码"`（太模糊，无法判定触发）
✅ 好: `"代码审查助手：审查代码质量和安全性。用于 PR 审查、代码质量检查时。"`

### 2. 权限配置

❌ 坏: 审查 agent 给了所有权限
```yaml
permission:
  edit: allow
  bash: allow
```
✅ 好: 审查 agent 最小权限
```yaml
permission:
  edit: deny
  bash: deny
  webfetch: allow
```

### 3. Available Resources

❌ 坏: 罗列所有可用资源
```markdown
### Skills
- skill-creator
- glue-coding
- architecture-spec
- canvas-dev
- docx
- pdf
- xlsx
... (10+ 个)
```
✅ 好: 只推荐相关的
```markdown
### Skills
- `glue-coding` - 代码生成时优先复用成熟库
- `architecture-spec` - 分析架构问题时参考
```

### 4. 职责定义

❌ 坏: 职责模糊
```markdown
## Responsibilities
- 帮助开发者
- 写更好的代码
```
✅ 好: 职责具体可执行
```markdown
## Responsibilities
- 审查代码中的安全漏洞
- 检查性能问题和内存泄漏
- 评估代码可读性和可维护性
```

### 5. 约束定义

❌ 坏: 约束空泛
```markdown
## Constraints
- 小心一点
- 注意质量
```
✅ 好: 约束具体明确
```markdown
## Constraints
- 不要修改测试文件
- 只输出审查意见，不直接修改代码
- 发现严重问题时标注具体行号
```

## 常见错误

| 错误 | 症状 | 修复 |
|------|------|------|
| 触发不可靠 | 有时触发有时不触发 | description 加入具体场景 |
| 权限过度 | agent 有不需要的权限 | 设为最小必要权限 |
| 资源罗列 | Available Resources 太长 | 只保留 2-5 个相关资源 |
| 职责模糊 | agent 不知道做什么 | 职责具体到可执行动作 |
| 跳过确认 | 用户不满意创建结果 | 严格执行 8 步流程 |
| 闭门造车 | 忽略网上可复用经验 | 创建前先调研 |
