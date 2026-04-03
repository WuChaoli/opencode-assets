---
description: 检查合并冲突风险并提供智能合并建议
agent: build
---
请分析当前分支与目标分支的合并情况，检查冲突风险并提供解决方案。

!`git branch --show-current`

!`git fetch origin`

!`git log --oneline --graph --left-right HEAD...(git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD origin/master) --decorate`

!`git merge-tree (git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD origin/master) HEAD (git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD origin/master)`

请根据以上分析：
1. **冲突风险评估**：判断是否有冲突风险（高/中/低）
2. **建议策略**：
   - 直接合并（无冲突）
   - 先rebase后合并（提交历史较乱）
   - 手动解决冲突（存在文件冲突）
3. **具体命令**：提供可执行的git命令
4. **注意事项**：合并前需要检查的关键点

输出合并建议：
```bash
# 方案1: 直接合并（推荐）
git merge origin/main 2>/dev/null || git merge origin/master

# 方案2: 先rebase
git rebase origin/main 2>/dev/null || git rebase origin/master
# 解决冲突后
git push --force-with-lease

# 方案3: 创建合并提交
git merge --no-ff (git merge origin/main 2>/dev/null || git merge origin/master) -m "合并分支"
```