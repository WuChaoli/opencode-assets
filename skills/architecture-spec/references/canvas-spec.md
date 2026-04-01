# Canvas JSON 输出规范

基于 Obsidian Canvas 格式，定义 AI 生成架构白板的标准规范。

## 文件格式

Canvas 文件是 `.canvas` 扩展名的 JSON 文件。

## 顶层结构

```json
{
  "nodes": [],
  "edges": []
}
```

## 节点 (nodes)

### 通用属性

| 属性 | 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `id` | string | ✅ | 唯一标识符（建议使用 uuid 或语义化 ID） |
| `type` | string | ✅ | 节点类型：text/file/link/group |
| `x` | number | ✅ | X 坐标（像素） |
| `y` | number | ✅ | Y 坐标（像素） |
| `width` | number | ✅ | 宽度（像素） |
| `height` | number | ✅ | 高度（像素） |
| `color` | string | ❌ | 颜色编号 ("1"-"6") |

### 文本节点 (text)

用于表示代码模块、服务、组件。

```json
{
  "id": "user-service",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 250,
  "height": 120,
  "text": "**UserService**\n`src/services/user.py`\n\n**职责**: 用户管理\n**复杂度**: Medium",
  "color": "4"
}
```

### 文件节点 (file)

用于链接实际代码文件。

```json
{
  "id": "config-file",
  "type": "file",
  "x": 300,
  "y": 0,
  "width": 200,
  "height": 80,
  "file": "config/settings.py"
}
```

### 链接节点 (link)

用于外部资源引用。

```json
{
  "id": "api-docs",
  "type": "link",
  "x": 600,
  "y": 0,
  "width": 200,
  "height": 80,
  "url": "https://api.example.com/docs"
}
```

### 分组节点 (group)

用于逻辑分层。

```json
{
  "id": "backend-layer",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 600,
  "height": 400,
  "label": "后端服务层"
}
```

## 连线 (edges)

### 属性

| 属性 | 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `id` | string | ✅ | 唯一标识符 |
| `fromNode` | string | ✅ | 起始节点 id |
| `toNode` | string | ✅ | 目标节点 id |
| `fromSide` | string | ❌ | 起始边：top/right/bottom/left |
| `toSide` | string | ❌ | 目标边：top/right/bottom/left |
| `fromEnd` | string | ❌ | 起始端样式：none/arrow |
| `toEnd` | string | ❌ | 目标端样式：none/arrow |
| `label` | string | ❌ | 连线标签（必须标注关系类型） |

### 示例

```json
{
  "id": "edge-api-to-service",
  "fromNode": "api-gateway",
  "toNode": "user-service",
  "fromSide": "right",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "HTTP 调用"
}
```

## 颜色编码

与 Mermaid 规范统一：

| color | 颜色 | 用途 |
|:---|:---|:---|
| `"1"` | 🔴 红色 | 缓存、热点、警告 |
| `"2"` | 🟠 橙色 | 消息队列、异步 |
| `"3"` | 🟡 黄色 | 入口、网关、外部输入 |
| `"4"` | 🟢 绿色 | 数据库、持久化 |
| `"5"` | 🔵 蓝色 | 外部服务、第三方 API |
| `"6"` | 🟣 紫色 | 注释、设计决策 |

## 节点内容模板

### 标准模块节点

```markdown
**{组件名}**
`{文件路径}`

**职责**: {一句话描述}
**复杂度**: Low/Medium/High
```

### 带风险标注的节点

```markdown
**{组件名}**
`{文件路径}`

**职责**: {描述}
**复杂度**: High
**⚠️ 风险**: {循环依赖/性能热点/技术债}
```

### 数据库节点

```markdown
**{数据库名}**
`{连接信息}`

**类型**: PostgreSQL/MySQL/MongoDB
**表数量**: {N}
```

## 布局规范

### 三层架构布局

```
x: -400    x: 0      x: 400    x: 800
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ 前端   │→│ API    │→│ 服务   │→│ 数据   │
└────────┘ └────────┘ └────────┘ └────────┘
y: 0
```

### 微服务布局

```
         x: 0
         ┌────────┐
         │ Gateway│  y: -200
         └────────┘
              │
    ┌─────────┼─────────┐
    ↓         ↓         ↓
┌────────┐ ┌────────┐ ┌────────┐
│Service1│ │Service2│ │Service3│  y: 0
└────────┘ └────────┘ └────────┘
x: -300    x: 0      x: 300
    │         │         │
    ↓         ↓         ↓
┌────────┐ ┌────────┐ ┌────────┐
│  DB1   │ │  DB2   │ │ Cache  │  y: 200
└────────┘ └────────┘ └────────┘
```

### 尺寸建议

| 元素 | 建议值 |
|:---|:---|
| 节点宽度 | 200-280 |
| 节点高度 | 80-150 |
| 水平间距 | 100-150 |
| 垂直间距 | 120-150 |
| 分组内边距 | 50 |

## 完整示例

```json
{
  "nodes": [
    {
      "id": "group-api",
      "type": "group",
      "x": -50,
      "y": -50,
      "width": 350,
      "height": 250,
      "label": "API 层"
    },
    {
      "id": "api-gateway",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 100,
      "text": "**API Gateway**\n`src/api/main.py`\n\n**职责**: 路由分发、认证\n**复杂度**: Medium",
      "color": "3"
    },
    {
      "id": "group-service",
      "type": "group",
      "x": 350,
      "y": -50,
      "width": 350,
      "height": 250,
      "label": "服务层"
    },
    {
      "id": "user-service",
      "type": "text",
      "x": 400,
      "y": 0,
      "width": 250,
      "height": 100,
      "text": "**UserService**\n`src/services/user.py`\n\n**职责**: 用户管理\n**复杂度**: Low"
    },
    {
      "id": "group-data",
      "type": "group",
      "x": 750,
      "y": -50,
      "width": 300,
      "height": 250,
      "label": "数据层"
    },
    {
      "id": "database",
      "type": "text",
      "x": 800,
      "y": 0,
      "width": 200,
      "height": 80,
      "text": "**PostgreSQL**\n`主数据库`",
      "color": "4"
    },
    {
      "id": "cache",
      "type": "text",
      "x": 800,
      "y": 100,
      "width": 200,
      "height": 80,
      "text": "**Redis**\n`缓存层`",
      "color": "1"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "api-gateway",
      "toNode": "user-service",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow",
      "label": "调用"
    },
    {
      "id": "e2",
      "fromNode": "user-service",
      "toNode": "database",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow",
      "label": "读写"
    },
    {
      "id": "e3",
      "fromNode": "user-service",
      "toNode": "cache",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow",
      "label": "缓存"
    }
  ]
}
```

## 生成规则

1. **ID 命名**：使用 kebab-case，语义化（如 `user-service`）
2. **坐标计算**：按层级自动计算，保持间距一致
3. **分组优先**：先创建 group 节点，再创建内部节点
4. **连线方向**：统一从左到右（fromSide: right, toSide: left）
5. **标签必填**：所有 edge 必须有 label 说明关系
