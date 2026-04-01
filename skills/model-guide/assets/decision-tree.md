# 模型选择决策树

## 文本版决策树

```
开始
│
├─ 需要多模态（图片/文档理解）？
│   ├─ 是 → 需要大上下文（>200K）？
│   │   ├─ 是 → Gemini 3.1 Pro
│   │   └─ 否 → Claude Sonnet 4.6
│   └─ 否 → 看任务类型
│       │
│       ├─ 日常编码（80% 场景）
│       │   ├─ 质量优先 → Claude Sonnet 4.6
│       │   ├─ 速度优先 → Claude Haiku 4.5
│       │   ├─ 成本优先 → Qwen3.6 Free
│       │   └─ 平衡方案 → Claude Sonnet 4.5
│       │
│       ├─ 复杂任务（架构/深度调试）
│       │   ├─ 质量优先 → Claude Opus 4.6
│       │   ├─ 速度优先 → Claude Sonnet 4.6
│       │   ├─ 成本优先 → Claude Haiku 4.5
│       │   └─ 平衡方案 → Claude Sonnet 4.6
│       │
│       ├─ 简单查询/快速响应
│       │   ├─ 质量优先 → Claude Haiku 4.5
│       │   ├─ 成本优先 → Qwen3.6 Free
│       │   └─ 平衡方案 → Claude Haiku 4.5
│       │
│       ├─ 代码审查
│       │   ├─ 质量优先 → Claude Sonnet 4.6
│       │   ├─ 成本优先 → Claude Haiku 4.5
│       │   └─ 平衡方案 → Claude Haiku 4.5
│       │
│       ├─ 文档编写
│       │   ├─ 质量优先 → Claude Sonnet 4.6
│       │   ├─ 成本优先 → Qwen3.6 Free
│       │   └─ 平衡方案 → Claude Haiku 4.5
│       │
│       └─ 预算有限
│           ├─ 零预算 → Qwen3.6 Free / MiniMax M2.5 Free
│           ├─ 低预算 → Claude Haiku 4.5
│           └─ 中预算 → Claude Sonnet 4.6
```

## 快速决策表

| 如果你... | 选择 |
|-----------|------|
| 不知道选什么 | Claude Sonnet 4.6 |
| 想要最好的 | Claude Opus 4.6 |
| 想要最便宜的 | Qwen3.6 Free |
| 想要最快的 | Claude Haiku 4.5 |
| 需要看图片 | Claude Sonnet 4.6 |
| 需要大上下文 | Gemini 3.1 Pro |
| 偏好 OpenAI | GPT 5.3 Codex |
