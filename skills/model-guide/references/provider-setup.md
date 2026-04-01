# Provider 配置指南

## OpenCode Zen（推荐）

### 配置步骤

1. 访问 https://opencode.ai/auth 注册/登录
2. 添加支付方式
3. 复制 API Key
4. 在 OpenCode 中运行 `/connect`
5. 选择 OpenCode Zen
6. 粘贴 API Key

### 验证配置

```bash
/models
```

查看可用模型列表。

## 其他 Provider

### Anthropic

```json
{
  "provider": {
    "anthropic": {
      "apiKey": "your-api-key"
    }
  }
}
```

### OpenAI

```json
{
  "provider": {
    "openai": {
      "apiKey": "your-api-key"
    }
  }
}
```

### Google

```json
{
  "provider": {
    "google": {
      "apiKey": "your-api-key"
    }
  }
}
```

## 模型配置

### 设置默认模型

```json
{
  "model": "opencode/claude-sonnet-4-6"
}
```

### Agent 级别覆盖

```json
{
  "agent": {
    "build": {
      "model": "opencode/claude-sonnet-4-6"
    },
    "plan": {
      "model": "opencode/claude-haiku-4-5"
    }
  }
}
```

## 常见问题

### Q: 如何选择 Provider？

A: 推荐使用 OpenCode Zen，已测试验证，质量有保障。

### Q: 可以配置多个 Provider 吗？

A: 可以，OpenCode 支持 75+ Provider。

### Q: 免费模型有哪些？

A: Qwen3.6 Plus Free、MiniMax M2.5 Free、Nemotron 3 Super Free 等。
