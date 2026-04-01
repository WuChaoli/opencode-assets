# glue-coding 参考文档

## 文档索引

| 文档 | 说明 |
|:---|:---|
| [principles.md](./principles.md) | 胶水编程核心原则详解 |
| [checklist.md](./checklist.md) | 代码审查清单 |

## 核心原则速查

### 三大原则

1. **能抄不写** - 优先使用已验证的成熟代码
2. **能连不造** - 优先组合现有模块而非新建
3. **能复用不原创** - 除非有充分理由，否则不自己实现

### 禁止行为

- Mock/Stub/Demo 代码
- 功能裁剪或逻辑重写
- 重复造轮子
- "只导入不用"的伪集成

### 允许行为

- 业务流程编排
- 模块组合与调度
- 参数配置与调用组织
- 输入输出适配

## 外部资源

- [vibe-coding-cn 原始文档](https://github.com/tukuaiai/vibe-coding-cn)
- [胶水编程哲学](https://github.com/tukuaiai/vibe-coding-cn/blob/main/i18n/zh/documents/00-基础指南/胶水编程.md)
