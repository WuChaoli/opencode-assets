---
description: 全自动 Git 工作流：fetch → pull --rebase → commit → push
agent: build
---

请帮我全自动完成 Git 推送工作流。

## 当前状态检查

**当前分支：**
!`git branch --show-current`

**未提交的更改：**
!`git status --porcelain`

**获取远程更新：**
!`git fetch origin`

**检查远程新提交：**
!`git log --oneline HEAD..origin/$(git branch --show-current) 2>/dev/null || echo "无远程更新"`

**检查本地未推送的提交：**
!`git log --oneline origin/$(git branch --show-current)..HEAD 2>/dev/null || echo "无本地提交"`

## 全自动执行流程

请按以下顺序自动执行：

1. **如果有远程新提交，先 pull --rebase：**
   - 执行：`git pull --rebase origin $(git branch --show-current)`
   - 如果 rebase 成功，继续下一步
   - 如果 rebase 失败（有冲突），提示冲突文件并暂停等待解决

2. **如果有未提交的更改，自动 commit：**
   - 添加到暂存区：`git add .`
   - 创建提交：`git commit -m "update"`

3. **执行 push：**
   - 执行：`git push origin $(git branch --show-current)`

4. **显示最终结果：**
   - 推送状态（成功/失败）
   - 最新 3 条提交历史：`git log --oneline -3`
   - 当前分支状态摘要

## 冲突自动处理

- **简单冲突**（同一文件的独立部分）：尝试自动解决并继续
- **复杂冲突**：显示冲突文件列表，暂停并提示手动解决
- 冲突解决后继续执行 push

请现在开始全自动执行，并实时报告每一步的状态。
