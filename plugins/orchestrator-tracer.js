// Orchestrator Tracer Plugin for OpenCode
// Automatically logs all task calls made by orchestrator agent

// Required: Plugin auth configuration (must be top-level export)
export const auth = {
  type: "none",
  required: false
};

// Required: Default plugin function
export default async function OrchestratorTracer({ project, client, $, directory, worktree }) {
  const callChains = new Map();
  let currentSessionId = null;
  
  function generateId() {
    return `call-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
  
  function summarize(result) {
    if (!result) return null;
    if (typeof result === "string") {
      return result.substring(0, 500) + (result.length > 500 ? "..." : "");
    }
    try {
      const str = JSON.stringify(result);
      return str.substring(0, 500) + (str.length > 500 ? "..." : "");
    } catch {
      return "[Object]";
    }
  }
  
  async function saveCallChain() {
    try {
      const fs = await import("fs");
      const path = await import("path");
      
      const logDir = path.join(directory, ".opencode", "logs");
      const logFile = path.join(logDir, `orchestrator-calls-${currentSessionId || 'unknown'}.json`);
      
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
      
      const data = {
        project: project?.name || "unknown",
        projectPath: directory,
        sessionId: currentSessionId,
        timestamp: new Date().toISOString(),
        totalCalls: callChains.size,
        calls: Array.from(callChains.values())
      };
      
      fs.writeFileSync(logFile, JSON.stringify(data, null, 2));
      console.log(`[OrchestratorTracer] Saved: ${logFile}`);
    } catch (error) {
      console.error("[OrchestratorTracer] Save error:", error);
    }
  }
  
  console.log(`[OrchestratorTracer] Initialized: ${project?.name || 'unknown'}`);
  
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool === "task") {
        const callId = generateId();
        const taskArgs = output.args || {};
        const targetAgent = taskArgs.subagent || taskArgs.agent || "unknown";
        const taskDescription = taskArgs.description || taskArgs.task || "No description";
        
        callChains.set(callId, {
          id: callId,
          timestamp: new Date().toISOString(),
          type: "TASK_CALL",
          sessionId: currentSessionId,
          targetAgent: targetAgent,
          taskDescription: taskDescription.substring(0, 200),
          inputSummary: summarize(taskArgs.input || taskArgs.context),
          status: "PENDING"
        });
        
        output.__tracer_callId = callId;
        output.__tracer_startTime = Date.now();
        console.log(`[OrchestratorTracer] Start: ${targetAgent}`);
      }
    },
    
    "tool.execute.after": async (input, output) => {
      if (input.tool === "task") {
        const callId = input.__tracer_callId;
        const startTime = input.__tracer_startTime;
        const callRecord = callChains.get(callId);
        
        if (callRecord) {
          const duration = startTime ? Date.now() - startTime : null;
          
          callRecord.status = output.error ? "FAILED" : "SUCCESS";
          callRecord.completedAt = new Date().toISOString();
          callRecord.durationMs = duration;
          callRecord.resultSummary = output.error ? null : summarize(output.result);
          callRecord.error = output.error ? (output.error.message || String(output.error)).substring(0, 500) : null;
          
          console.log(`[OrchestratorTracer] Done: ${callRecord.targetAgent} - ${callRecord.status} (${duration}ms)`);
          await saveCallChain();
        }
      }
    },
    
    "session.created": async (event) => {
      if (event.agent === "orchestrator" || event.agent?.includes("orchestrator")) {
        currentSessionId = event.sessionId;
        callChains.clear();
        console.log(`[OrchestratorTracer] New session: ${event.sessionId}`);
      }
    },
    
    "session.error": async (event) => {
      if (event.sessionId === currentSessionId) {
        console.error(`[OrchestratorTracer] Error: ${event.error?.message || String(event.error)}`);
        await saveCallChain();
      }
    }
  };
}
