---
name: skill-creator
description: "元技能：从领域资料（文档/API/代码/规范）生成标准化 Skill。触发条件：创建新 Skill、重构现有 Skill、从资料提取可复用能力、用户提到'创建技能'或'skill creator'时。"
---

# skill-creator 元技能

将零散领域资料转化为可复用、可维护、可靠激活的 Skill。遵循 glue-coding 原则：先搜索现有 Skill，再决定创建/复用/改编。

## When to Use This Skill

触发条件（满足任一即可）：
- 用户提到"创建技能"、"生成 Skill"、"skill creator"
- 需要从文档/规范/仓库创建新 Skill
- 需要重构现有 Skill（太长、不清晰、触发不可靠）
- 需要从大量资料中提取简洁的 Quick Reference

## Not For / Boundaries

此技能不适用于：
- 作为领域 Skill 本身使用（它是用来**构建** Skill 的）
- 凭空发明资料中没有的内容
- 跳过搜索直接创建（违反 glue-coding 原则）
- 跳过用户确认直接创建

必要输入（缺失时需询问）：
1. 领域资料（文档、API 文档、代码仓库、规范等）
2. Skill 的目标用途/场景
3. 期望的触发关键词

## 工作流程（10 步，严格按顺序执行）

### 阶段一：需求确认

**Step 1: 沟通确认需求**
- 与用户充分沟通，确保完全理解：
  - Skill 要解决什么问题？
  - 目标用户是谁？
  - 期望的触发场景是什么？
  - 有哪些输入/输出要求？
- 用 1-3 个问题澄清模糊点，不要猜测
- 确认用户对需求理解无异议后再继续

### 阶段二：搜索与评估

**Step 2: 搜索现有 Skill**
- **SkillsMP 搜索**（733,496+ skills）：
  - 运行 `python {baseDir}/scripts/search_skills.py <关键词>`
  - 或访问 https://skillsmp.com 搜索
  - 按 star 数排序，查看前 10 个结果
- **Anthropic 官方搜索**：
  - 检查 github.com/anthropics/skills/skills/ 目录
  - 查看官方 docx/pdf/pptx/xlsx 等 skill 实现
- **GitHub 搜索**：
  - 搜索 `SKILL.md` + 关键词
  - 按 star 数排序
- 整理搜索结果，记录候选 Skill

**Step 3: 评估搜索结果**
- 对每个候选 Skill 评估：
  - **功能匹配度**：是否覆盖用户需求？（0-100%）
  - **质量指标**：star 数、更新日期、维护状态
  - **兼容性**：是否符合 SKILL.md 规范？
  - **可改编性**：是否容易适配用户需求？
- 根据评估结果决策：
  - 匹配度 > 80% → 推荐直接安装
  - 匹配度 50-80% → 推荐改编
  - 匹配度 < 50% → 推荐参考后创建
  - 无结果 → 从零创建
- 向用户展示评估结果，确认下一步

### 阶段三：方案设计

**Step 4: 在线调研**
- 搜索网上可复用的经验和最佳实践：
  - 官方文档和社区指南
  - 类似 Skill 的实现方案
  - 常见陷阱和反模式
- 整理调研结果，提炼可复用的模式
- 记录参考来源

**Step 5: 设计方案**
- 基于需求、搜索结果和调研，设计 Skill：
  - 如果是改编：确定需要修改的部分
  - 如果是创建：设计目录结构、章节规划
  - 需要哪些 references/scripts/assets
- 输出设计草案

**Step 6: 与用户确认方案**
- 向用户展示设计草案：
  - 来源说明（改编/参考/从零创建）
  - Skill 名称和 description
  - 目录结构
  - 核心章节内容
  - 触发条件和边界
- 等待用户确认或提出修改意见
- **未经用户确认，不得开始创建**

**Step 7: 确认创建位置**
- 询问用户 Skill 创建位置：
  - **项目级**（默认）：`.opencode/skills/`
  - **系统级**：`~/.config/opencode/skills/`
  - **自定义**：用户指定的其他父目录
- 确认目标路径存在或可创建

### 阶段四：执行创建

**Step 8: 创建/改编 Skill**
- 如果是改编：clone 现有 Skill 并修改
- 如果是创建：运行脚手架脚本
  - `python {baseDir}/scripts/init_skill.py <name> --path <dir>`
- 按确认的方案填充内容：
  - 填写 frontmatter（name, description）
  - 编写 When to Use / Not For / Quick Reference
  - 添加 ≥3 个 Examples
  - 拆分长内容到 references/
- 改编时注明来源，尊重开源协议

**Step 9: 质量验证**
- 运行验证脚本：
  - `python {baseDir}/scripts/validate_skill.py <skill-path>`
- 或手动检查 `{baseDir}/references/quality-checklist.md`
- 修复所有失败项

**Step 10: 交付与说明**
- 向用户展示创建的 Skill 结构
- 说明如何使用和测试
- 告知后续维护建议

## Quick Reference

### 目录结构
```
skill-name/
├── SKILL.md              # 必须：入口 + frontmatter
├── references/           # 可选：长篇参考
├── scripts/              # 可选：辅助脚本
└── assets/               # 可选：模板/静态资源
```

### Frontmatter 规则
```yaml
---
name: skill-name                    # 必须：^[a-z][a-z0-9-]*$
description: "做什么 + 何时用"       # 必须：带具体触发词
---
```

### SKILL.md 最小骨架
```markdown
---
name: my-skill
description: "[领域]能力。触发条件：[关键词1]、[关键词2]。"
---

# my-skill Skill

一句话说明边界和交付物。

## When to Use This Skill
- [触发条件 1]
- [触发条件 2]

## Not For / Boundaries
- 不做什么
- 必要输入

## Quick Reference
### 模式 1
[可直接复制的命令/代码]

## Examples

### Example 1: 搜索后改编现有 Skill

**输入**: 用户需要 PDF 处理 Skill
**步骤**:
1. 沟通确认需求（PDF 提取/合并/转换）
2. 搜索 SkillsMP 和 GitHub，找到 pdf-toolkit（匹配度 75%）
3. 评估：需要添加转换功能，改编工作量 40%
4. 在线调研 PDF 处理最佳实践
5. 设计方案：基于 pdf-toolkit 改编，添加转换模块
6. 用户确认改编方案
7. Clone 并修改，注明来源
8. 运行 validate_skill.py 验证
**验收**: Skill 功能完整，验证通过，已注明改编自 pdf-toolkit

### Example 2: 从零创建新 Skill

**输入**: 用户需要特定业务逻辑的 Skill，无现有匹配
**步骤**:
1. 沟通确认需求（业务规则、触发场景）
2. 搜索 SkillsMP/GitHub，无匹配结果（匹配度 < 30%）
3. 在线调研类似实现
4. 设计方案（目录结构、章节规划）
5. 用户确认方案
6. 运行 init_skill.py 生成脚手架
7. 填充具体内容
8. 运行 validate_skill.py 验证
**验收**: Skill 可被正确触发，Quick Reference 可直接使用，验证通过

### Example 3: 重构"文档堆砌"型 Skill

**输入**: 现有 SKILL.md，包含大段粘贴的文档
**步骤**:
1. 搜索是否有更好的现有 Skill 可替代
2. 识别哪些是模式 vs 长篇解释
3. 长篇文本移到 references/（按主题拆分）
4. Quick Reference 重写为短小复制/粘贴模式
5. 添加/修复 Examples 直到可复现
6. 添加 Not For / Boundaries 减少误触发
7. 运行验证脚本确认
**验收**: SKILL.md 精简到 < 200 行，验证通过

## References
- `references/index.md`: 导航
```

### 搜索策略

| 来源 | 规模 | 访问方式 | 特点 |
|------|------|---------|------|
| SkillsMP | 733,496+ | API / 网站 | 最大社区，AI 语义搜索 |
| Anthropic 官方 | 25 个 | GitHub | 官方实现，高质量 |
| GitHub 搜索 | 海量 | code search | 社区贡献，需筛选 |

### 评估决策树

```
搜索到现有 Skill？
  ├─ 是 → 匹配度 > 80%？
  │   ├─ 是 → 推荐直接安装
  │   └─ 否 → 匹配度 50-80%？
  │       ├─ 是 → 推荐改编
  │       └─ 否 → 推荐参考后创建
  └─ 否 → 从零创建
```

### 创作规则（不可协商）
1. Quick Reference ≤ 20 个模式，需要段落解释的放 references/
2. 激活必须可判定：description 说"什么 + 何时"，带具体关键词
3. Not For / Boundaries 是可靠性的必要条件
4. 不确定的声明，给出验证路径
5. **必须先搜索现有 Skill**，不要重复造轮子（glue-coding 原则）
6. **必须先调研再创建**，不要闭门造车
7. **必须用户确认后再创建**，不要自作主张
8. 改编时注明来源，尊重开源协议

## 工具

- 搜索：`python {baseDir}/scripts/search_skills.py <关键词>`
- 验证：`python {baseDir}/scripts/validate_skill.py <skill-path>`
- 脚手架：`python {baseDir}/scripts/init_skill.py <name> --path <dir>`

## References

- `references/index.md` - 导航
- `references/skill-spec.md` - 规范详解
- `references/quality-checklist.md` - 检查清单
- `references/common-patterns.md` - 模式与反模式
- `references/research-guide.md` - 调研指南
- `references/search-guide.md` - 搜索策略与 API 使用
- `references/evaluation-guide.md` - 评估标准与决策流程
- `references/adaptation-guide.md` - 改编现有 Skill 的指南
- `assets/template-minimal.md` - 最小模板
- `assets/template-complete.md` - 完整模板

## Maintenance

- Last updated: 2026-04-01
- Known limits: 依赖输入资料质量；不能凭空创造领域知识；SkillsMP API 有 500 次/天限制
