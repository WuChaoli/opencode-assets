# 诊断指南

## 诊断流程

### 1. 结构检查

运行审计脚本获取基础数据：

```bash
python scripts/audit_skill.py <skill-path>
```

关注指标：
- SKILL.md 行数（> 200 需要精简）
- 必须章节完整性
- references/ 文件数量和大小

### 2. 内容质量检查

#### 触发可靠性
- description 是否包含具体关键词？
- When to Use 是否具体可判定？
- 是否有 Not For 定义边界？

#### 指令一致性
- 是否有前后矛盾的说明？
- Quick Reference 和 references/ 是否冲突？
- 输出格式要求是否统一？

#### 示例可用性
- Examples 是否 >= 3 个？
- 每个示例是否有输入/步骤/验收？
- 示例是否可以复现？

### 3. 上下文负载检查

#### 200 行规则
- SKILL.md 是否超过 200 行？
- 如果超过，哪些内容可以移到 references/？

#### references 导航
- 是否有 index.md 导航？
- 每个 references 文件是否 < 300 行？
- SKILL.md 中是否正确引用了 references？

### 4. 范围检查

#### 工作流 vs 工具
- Skill 是按工作流组织的吗？
- 还是按工具组织的（容易膨胀）？
- 是否需要拆分成多个 Skill？

#### 职责聚焦
- Skill 是否做了太多事？
- 每个部分是否聚焦一个主题？

### 5. 用户反馈收集

询问用户：
- 什么场景下不好用？
- 期望的改进方向？
- 有没有具体的失败案例？

## 诊断输出模板

```markdown
# Skill 诊断报告

## 基本信息
- Skill: [name]
- SKILL.md 行数: [N]
- references 文件数: [N]

## 发现的问题

### 结构问题
- [ ] 缺少 Not For 章节
- [ ] Examples 不足 3 个

### 内容问题
- [ ] description 缺少具体关键词
- [ ] Quick Reference 超过 20 个模式

### 上下文问题
- [ ] SKILL.md 超过 200 行
- [ ] references/ 缺少 index.md

## 建议修改
1. [修改 1] - 预期效果: [效果]
2. [修改 2] - 预期效果: [效果]
```
