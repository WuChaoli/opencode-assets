# OpenCode 全栈开发环境计划

> 基于 Context Engineering 和 Harness Engineering 最佳实践
> 创建日期: 2026-04-02

---

## 核心概念

### Context Engineering（上下文工程）
- **本质**: 设计整个信息系统来管理AI的上下文窗口
- **核心原则**: 渐进式披露（Progressive Disclosure）- 只在需要时提供需要的信息
- **关键发现**: 上下文腐烂（Context Rot）- 上下文越长，性能越差；保持上下文文件简洁（<60行）

### Harness Engineering（约束工程）
- **公式**: Agent = Model + Harness
- **本质**: 围绕AI模型构建系统、工具、约束和反馈循环
- **核心组件**:
  1. 上下文工程（AGENTS.md等）
  2. 架构约束
  3. 工具与MCP服务器
  4. 子代理与上下文防火墙
  5. Hooks与反向压力
  6. 自验证循环
  7. 进度文档

---

## 项目结构

```
your-project/
│
├── 📋 AGENTS.md                    # 主上下文文件（<60行）
├── 🔧 .opencode/                   # OpenCode配置目录
│   ├── agents/                    # 子代理定义
│   ├── skills/                    # 技能定义
│   └── hooks/                     # Hooks配置
├── 📚 docs/                        # 项目文档库
│   ├── architecture.md            # 架构概览
│   ├── decisions/                 # 架构决策记录（ADR）
│   └── api/                       # API文档
├── 📝 dev-log/                     # 开发日志
│   ├── sessions/                  # 会话记录
│   ├── active-work/               # 进行中的工作
│   └── completed/                 # 已完成的工作
├── 🧪 test/                        # 测试目录
│   ├── verification/             # 验证脚本
│   ├── unit/                     # 单元测试
│   ├── integration/              # 集成测试
│   ├── e2e/                      # 端到端测试
│   ├── archives/                 # 历史测试归档
│   └── fixtures/                 # 测试数据
├── 📊 monitoring/                  # 监控与观测
├── 🛠️ scripts/                     # 工具脚本
├── 📦 src/                         # 源代码
│   ├── frontend/
│   ├── backend/
│   └── shared/
└── 📄 README.md
```

---

## 1. 文档记录与同步机制

### 文档生命周期

```
开发中                    开发完成后
┌─────────────┐          ┌──────────────────┐
│ active-work/ │ ───────→ │ completed/       │
│ (详细记录)   │  归档    │ (精简总结)       │
└─────────────┘          └──────────────────┘
       │                          │
       ↓                          ↓
┌─────────────┐          ┌──────────────────┐
│ sessions/   │ ───────→ │ docs/decisions/  │
│ (原始日志)   │  提炼    │ (正式ADR)        │
└─────────────┘          └──────────────────┘
                                │
                                ↓
                         ┌──────────────────┐
                         │ AGENTS.md        │
                         │ (进度更新)       │
                         └──────────────────┘
```

### 文档模板

#### active-work 模板
```markdown
# Feature/Refactor/Test: [名称]

## 状态: 🟡 规划中 / 🟢 进行中 / ✅ 已完成

## 背景
[为什么做这个]

## 决策记录
- [ ] 决策1
- [ ] 决策2

## 实施计划
1. 步骤1
2. 步骤2
3. 步骤3

## 会话记录
### YYYY-MM-DD Session N
- 完成内容
- 遇到问题
- 下一步
```

#### ADR 模板
```markdown
# ADR-XXX: [标题]

## 状态: Proposed / Accepted / Deprecated

## 背景
[上下文和问题陈述]

## 决策
[我们决定...]

## 后果
- 正面: ...
- 负面: ...

## 替代方案
- 方案1: ...
- 方案2: ...
```

### 同步脚本

```bash
#!/bin/bash
# scripts/sync-dev-log.sh

DATE=$(date +%Y-%m-%d)

# 1. 归档完成的工作
for file in dev-log/active-work/*.md; do
  if grep -q "✅ 已完成" "$file"; then
    TASK_NAME=$(basename "$file" .md)
    mv "$file" "dev-log/completed/${DATE}_${TASK_NAME}.md"
    echo "✅ Archived: $TASK_NAME"
  fi
done

# 2. 更新AGENTS.md进度（保持<60行）
# 仅更新状态，不添加详细历史

# 3. 清理旧会话（保留30天）
find dev-log/sessions/ -mtime +30 -delete

echo "📋 Sync complete"
```

---

## 2. Hooks 钩子设计

### Hooks 架构

```
.opencode/hooks/
├── post-action/                   # 动作执行后（最高ROI）
│   └── verify-changes.sh         # 验证变更
├── pre-commit/                    # 提交前
│   └── prepare-commit.sh         # 格式化+安全检查
└── post-session/                  # 会话结束后
    └── archive-session.sh        # 归档会话
```

### 核心 Hook: verify-changes.sh

**设计原则**: 成功时完全静默，失败时输出详细错误

```bash
#!/bin/bash
set -e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
cd "$PROJECT_DIR"

ERRORS=""

# 前端检查
if [ -d "src/frontend" ]; then
  cd src/frontend
  if ! npx tsc --noEmit 2>/tmp/frontend-typecheck.err; then
    ERRORS+="❌ Frontend typecheck failed:\n$(cat /tmp/frontend-typecheck.err)\n\n"
  fi
  if ! npx eslint . --quiet 2>/tmp/frontend-lint.err; then
    ERRORS+="❌ Frontend lint errors:\n$(cat /tmp/frontend-lint.err)\n\n"
  fi
  cd ../..
fi

# 后端检查
if [ -d "src/backend" ]; then
  cd src/backend
  if ! npx tsc --noEmit 2>/tmp/backend-typecheck.err; then
    ERRORS+="❌ Backend typecheck failed:\n$(cat /tmp/backend-typecheck.err)\n\n"
  fi
  cd ../..
fi

# 运行变更相关的测试
CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || echo "")
if [ -n "$CHANGED_FILES" ]; then
  TEST_PATTERNS=""
  for file in $CHANGED_FILES; do
    base=$(basename "$file" | sed 's/\.[^.]*$//')
    TEST_PATTERNS+="--grep $base "
  done
  
  if ! npm test -- $TEST_PATTERNS --silent 2>/tmp/test.err; then
    ERRORS+="❌ Tests failed:\n$(cat /tmp/test.err)\n\n"
  fi
fi

# 结果处理
if [ -n "$ERRORS" ]; then
  echo -e "\n⚠️  Verification failed:\n\n$ERRORS"
  echo "📋 Please fix the above issues before continuing."
  exit 2  # 通知harness重新介入
else
  exit 0  # 成功时完全静默
fi
```

### Hooks 配置

```json
{
  "hooks": {
    "post-action": ".opencode/hooks/post-action/verify-changes.sh",
    "pre-commit": ".opencode/hooks/pre-commit/prepare-commit.sh",
    "post-session": ".opencode/hooks/post-session/archive-session.sh"
  }
}
```

---

## 3. 测试文件组织管理

### 测试目录结构

```
test/
├── README.md                      # 归档索引
├── verification/                  # 验证脚本
├── unit/                          # 单元测试
│   ├── frontend/
│   ├── backend/
│   └── shared/
├── integration/                   # 集成测试
├── e2e/                           # 端到端测试
├── archives/                      # 历史归档
│   └── YYYY-MM-DD_task-name/
│       ├── test_*.py/ts
│       ├── TEST_RESULTS.md
│       └── README.md
└── fixtures/                      # 测试数据
```

### 测试生命周期

1. **开发阶段**: 根目录创建临时测试文件
2. **测试完成**: 运行归档脚本
3. **归档**: 移动到 `test/archives/YYYY-MM-DD_task/`
4. **索引**: 更新 `test/README.md`

### 归档脚本

```bash
#!/bin/bash
# scripts/archive-tests.sh
# 用法: ./archive-tests.sh <task-name> [test-files...]

TASK_NAME=$1
shift
TEST_FILES=$@

DATE=$(date +%Y-%m-%d)
ARCHIVE_DIR="test/archives/${DATE}_${TASK_NAME}"

mkdir -p "$ARCHIVE_DIR"

for file in $TEST_FILES; do
  [ -f "$file" ] && mv "$file" "$ARCHIVE_DIR/"
done

cat > "$ARCHIVE_DIR/README.md" << EOF
# Test Archive: $TASK_NAME

- **Date**: $DATE
- **Files**: $(ls $ARCHIVE_DIR | grep -v README.md | wc -l)
- **Status**: ✅ Passed / ❌ Failed

## Related Commits
$(git log --since="$DATE" --oneline 2>/dev/null | head -5)
EOF

echo "- [$DATE] $TASK_NAME: $(ls $ARCHIVE_DIR | grep -v README.md | wc -l) files" >> test/README.md
echo "✅ Archived to $ARCHIVE_DIR"
```

---

## 完整工作流示例

### 场景：开发用户认证功能

```
1. 开发前
   ├── 创建 dev-log/active-work/FEATURE-auth-system.md
   ├── 记录决策和计划
   └── 更新 AGENTS.md（如需要）

2. 开发中
   ├── 代理在 src/backend/ 实现代码
   ├── 根目录创建 test_auth_temp.py
   ├── 每次停止自动触发 post-action hook
   │   ├── 类型检查
   │   ├── lint检查
   │   └── 相关测试
   └── 会话日志记录到 dev-log/sessions/2026-04-02.md

3. 开发完成
   ├── 运行完整测试套件
   ├── 归档测试: ./scripts/archive-tests.sh auth-system test_auth_temp.py
   ├── 移动测试到 test/unit/backend/
   ├── 归档工作日志到 dev-log/completed/
   ├── 如有决策，创建 docs/decisions/ADR-003.md
   └── 触发 post-session hook

4. 提交
   ├── pre-commit hook 自动格式化
   ├── 安全检查
   ├── 更新开发日志
   └── 生成提交消息
```

---

## 实施阶段

### Phase 1: 核心上下文 + 验证（立即）
- [ ] AGENTS.md
- [ ] 子代理定义
- [ ] post-action hook
- [ ] 测试目录结构

### Phase 2: 文档系统（后续）
- [ ] dev-log 结构
- [ ] ADR 模板
- [ ] 同步脚本

### Phase 3: 监控 + 评估（进阶）
- [ ] monitoring/ 目录
- [ ] 评估管道
- [ ] 成本跟踪

---

## 关键设计原则

| 组件 | 原则 | 实现 |
|------|------|------|
| **文档** | 渐进式披露 | active-work → completed → ADR |
| **Hooks** | 成功静默，失败大声 | exit 0 vs exit 2 |
| **测试** | 按日期归档 | test/archives/YYYY-MM-DD_task/ |
| **上下文** | 保持<60行 | AGENTS.md 只记录核心规则 |
| **同步** | 自动化 | scripts/ 自动归档脚本 |
