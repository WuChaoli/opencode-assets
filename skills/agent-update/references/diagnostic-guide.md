# Agent 诊断指南

## 诊断流程

### 1. 结构检查

运行审计脚本获取基础数据：

```bash
python scripts/audit_agent.py <agent-path>
```

关注指标：
- Prompt 行数（> 100 需要精简）
- 必须章节完整性
- 权限配置合理性

### 2. 内容质量检查

#### 触发可靠性
- description 是否包含具体关键词？
- mode 是否正确指定？

#### Prompt 质量
- Role 是否清晰定义角色？
- Responsibilities 是否具体可执行（<= 5 条）？
- Constraints 是否具体明确？

#### 资源推荐
- Available Resources 是否存在？
- 资源数量是否 <= 5 项？
- 资源是否与 Agent 职责相关？

### 3. 权限配置检查

#### tools 字段
- 是否关闭了不需要的工具？
- 是否开启了必要的工具？

#### permission 字段
- 是否遵循最小权限原则？
- edit/bash/webfetch 是否合理配置？

### 4. 参数配置检查

- temperature 是否匹配任务类型？
- steps 是否合理限制迭代次数？
- model 是否匹配任务复杂度？

## 诊断输出模板

```markdown
# Agent 诊断报告

## 基本信息
- Agent: [name]
- Prompt 行数: [N]
- 类型: [primary/subagent]

## 发现的问题

### 结构问题
- [ ] 缺少 Role 章节
- [ ] 缺少 Available Resources

### 内容问题
- [ ] description 缺少具体关键词
- [ ] Responsibilities 超过 5 条

### 权限问题
- [ ] 权限过度
- [ ] 权限不足

## 建议修改
1. [修改 1] - 预期效果: [效果]
2. [修改 2] - 预期效果: [效果]
```
