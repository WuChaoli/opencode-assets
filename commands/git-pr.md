---
description: 分析分支差异并自动生成PR标题和描述
agent: build
---
请分析当前分支与目标分支的差异，生成高质量的PR（Pull Request）信息。

!`git log --oneline (git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD origin/master)..HEAD`

!`git diff (git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD origin/master) HEAD --stat`

!`git branch --show-current`

请根据以上信息生成PR内容：
1. **标题**：简洁描述本次PR的核心变更（使用前缀如 feat:/fix:/docs:）
2. **变更摘要**：3-5个要点总结主要变更
3. **测试情况**：说明如何验证这些变更
4. **影响范围**：说明影响的功能模块

输出格式：
```markdown
## 标题
[建议的PR标题]

## 变更摘要
- [要点1]
- [要点2]
...

## 测试验证
[验证方法]

## 影响范围
[影响说明]
```

如果可能，直接使用 gh 命令创建PR：
```bash
gh pr create --title "标题" --body "描述"
```