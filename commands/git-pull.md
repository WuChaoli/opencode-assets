---
description: 安全拉取远程更新，检查冲突风险并提供备份建议
agent: build
---
请安全地拉取远程更新，分析潜在风险并提供保护建议。

!`git status --porcelain`

!`git stash list`

!`git log --oneline HEAD..origin/$(git branch --show-current) 2>/dev/null || echo "无法获取远程分支信息，请先执行 git fetch"`

!`git diff --stat HEAD origin/$(git branch --show-current) 2>/dev/null || echo "请先执行 git fetch 获取远程信息"`

请根据以上分析：
1. **风险检查**：
   - 本地是否有未提交变更？
   - 是否有未推送的提交？
   - 是否存在冲突风险？

2. **执行建议**：
   - 是否需要先stash本地变更？
   - 选择 merge 还是 rebase 策略？
   - 是否需要创建备份分支？

3. **具体命令序列**：

输出安全的pull方案：
```bash
# 步骤1: 创建备份（可选但推荐）
git branch backup-$(git branch --show-current)-$(date +%Y%m%d)

# 步骤2: 处理本地变更（如果有）
git stash push -m "自动备份: $(date)"

# 步骤3: 获取远程更新
git fetch origin

# 步骤4: 合并策略（二选一）
# 方案A: merge方式（保留历史）
git merge origin/$(git branch --show-current)

# 方案B: rebase方式（线性历史）
git pull --rebase origin $(git branch --show-current)

# 步骤5: 恢复本地变更（如果有暂存）
git stash pop
```

**提示**：如果只想查看远程更新而不合并，使用 `git fetch` 即可。