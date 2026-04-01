# Skill 规范详解

## MUST（必须遵守）

### 1. YAML Frontmatter

每个 `SKILL.md` 必须以 YAML frontmatter 开头：

```yaml
---
name: skill-name
description: "简短描述 + 触发条件"
---
```

### 2. name 命名规则

- 必须匹配正则: `^[a-z][a-z0-9-]*$`
- 必须与目录名一致
- 推荐 2-3 个单词，用连字符连接

✅ 正确: `glue-coding`, `canvas-dev`, `postgresql`
❌ 错误: `GlueCoding`, `glue_coding`, `123-skill`

### 3. description 格式

必须包含两部分：
1. **做什么**: 简短的能力描述
2. **何时用**: 具体的触发条件/关键词

✅ 正确: `"胶水开发模式：强依赖复用成熟库。触发条件：新功能开发、代码生成时。"`
❌ 错误: `"帮助开发者写更好的代码"`（太模糊）

### 4. 必须的章节

- `## When to Use This Skill` - 可判定的触发条件
- `## Not For / Boundaries` - 范围外内容和边界
- `## Quick Reference` - 可直接使用的模式
- `## Examples` - >= 3 个端到端示例

## SHOULD（强烈建议）

### 1. Quick Reference 精简

- 保持 <= 20 个模式
- 每个模式可以直接复制使用
- 需要解释的内容放 `references/`

### 2. Examples 格式

每个示例包含：
- **输入**: 起始条件
- **步骤**: 执行过程
- **验收标准**: 如何判断成功

### 3. 长内容拆分

超过 50 行的解释性内容应该：
- 移到 `references/` 目录
- 在 `references/index.md` 中建立导航
- 在 SKILL.md 中保留链接

## NEVER（禁止）

### 1. 禁止文档堆砌

不要把整个文档原样粘贴到 SKILL.md。

❌ 错误:
```markdown
## API Reference

### GET /users
返回用户列表...
（接下来 500 行 API 文档）
```

✅ 正确:
```markdown
## Quick Reference

### 获取用户列表
```bash
curl -X GET https://api.example.com/users
```

详细 API 文档见 `references/api.md`
```

### 2. 禁止模糊触发

不要使用无法判定的触发条件。

❌ 错误: "当你需要帮助时使用此技能"
✅ 正确: "当用户提到 'PostgreSQL'、'数据库优化'、'SQL 查询' 时触发"

### 3. 禁止凭空发明

如果资料中没有提到，不要自己编造。

❌ 错误: "这个库支持异步操作"（文档没说）
✅ 正确: "文档未提及异步支持，需要验证"
