# architecture-spec 参考文档导航

## 文档索引

| 文档 | 说明 | 适用场景 |
|:---|:---|:---|
| [mermaid-spec.md](./mermaid-spec.md) | Mermaid 输出详细规范 | 生成架构图、时序图、类图 |
| [canvas-spec.md](./canvas-spec.md) | Canvas JSON 详细规范 | Obsidian 白板驱动开发 |
| [interaction-protocol.md](./interaction-protocol.md) | AI ↔ 人类交互协议 | 标准化请求/响应格式 |

## 模板索引

| 模板 | 说明 |
|:---|:---|
| [../templates/mermaid-flowchart.md](../templates/mermaid-flowchart.md) | 架构图 Mermaid 模板 |
| [../templates/canvas-template.json](../templates/canvas-template.json) | Canvas JSON 项目模板 |

## 快速跳转

### 按格式

- **Mermaid**: [规范](./mermaid-spec.md) | [模板](../templates/mermaid-flowchart.md)
- **Canvas**: [规范](./canvas-spec.md) | [模板](../templates/canvas-template.json)

### 按场景

- **生成架构图**: SKILL.md → mermaid-spec.md
- **白板驱动开发**: canvas-spec.md → canvas-dev Skill
- **标准化交互**: interaction-protocol.md

## 相关 Skills

- `canvas-dev` - Canvas 白板驱动开发技能
- `glue-coding` - 胶水开发模式（架构审查时参考）
- `skill-creator` - 可用于生成领域特定架构规范
