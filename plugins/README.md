# Orchestrator Tracer Plugin

自动记录 OpenCode Orchestrator 的任务调用链路。

## 功能

- 自动拦截所有 `task` 工具调用
- 记录调用开始时间、目标 Agent、任务描述
- 记录调用完成时间、执行耗时、执行结果
- 保存调用链到 JSON 文件
- 实时日志记录到 OpenCode 日志系统

## 安装

本插件已安装到全局 plugin 目录：
```
~/.config/opencode/plugins/orchestrator-tracer.js
```

OpenCode 启动时会自动加载。

## 工作原理

使用 OpenCode Plugin 系统的 Hook 机制：

1. `tool.execute.before` - 在 task 调用前记录开始信息
2. `tool.execute.after` - 在 task 调用后记录完成信息
3. `session.created` - 识别新的 orchestrator 会话
4. `session.error` - 记录会话错误

## 输出文件

调用链日志保存在项目目录：
```
.opencode/logs/orchestrator-calls-{sessionId}.json
```

### 日志格式

```json
{
  "project": "glassdemo",
  "projectPath": "/path/to/project",
  "sessionId": "session-uuid",
  "timestamp": "2026-04-03T10:30:00Z",
  "totalCalls": 3,
  "calls": [
    {
      "id": "call-1743678600123-abc123",
      "timestamp": "2026-04-03T10:30:00Z",
      "type": "TASK_CALL",
      "sessionId": "session-uuid",
      "targetAgent": "architect",
      "taskDescription": "设计认证模块架构",
      "inputSummary": "需要设计用户认证...",
      "status": "SUCCESS",
      "completedAt": "2026-04-03T10:31:30Z",
      "durationMs": 90000,
      "resultSummary": "建议使用 MVI + Room + Hilt...",
      "error": null
    }
  ]
}
```

## 使用场景

1. **性能分析** - 查看每个 subagent 的执行耗时
2. **故障排查** - 追踪任务调用链，定位失败点
3. **审计追踪** - 记录完整的编排过程
4. **优化分析** - 分析 subagent 调用频率和模式

## 调试

查看实时日志：
```bash
# 在 OpenCode 中运行任意使用 orchestrator 的任务
# 日志会自动输出到 OpenCode 日志系统
```

查看调用链文件：
```bash
cat .opencode/logs/orchestrator-calls-*.json
```

## 注意事项

- 插件只记录 `task` 工具调用，不影响其他工具
- 每次 task 调用后都会保存文件，确保数据不丢失
- 日志文件按 session ID 区分，方便追踪单次编排过程
