# Agent 搜索策略

## 搜索来源

### 1. Claude Code Market

**网站**: https://www.ccmarket.dev/agents
**规模**: 53+ agents, 50K+ 下载

#### 特点
- 专业 sub-agents 集合
- 评分系统（4.8/5 平均）
- 按分类浏览（Frontend/Backend/Testing/DevOps 等）
- 一键安装（curl + mv）

#### 安装方式
```bash
# 下载 agent
curl -o frontend-architect.md https://marketplace.claude.com/agents/frontend-architect/download

# 移动到 OpenCode agents 目录
mv frontend-architect.md ~/.config/opencode/agents/
```

### 2. awesome-opencode

**仓库**: https://github.com/awesome-opencode/awesome-opencode
**规模**: 4235 stars

#### 特点
- OpenCode 专用 agents 集合
- 预配置 agent 列表
- 分类浏览（Agents/Plugins/Themes）

#### 访问方式
```bash
# Clone 仓库
git clone https://github.com/awesome-opencode/awesome-opencode.git

# 查看 agents 章节
open awesome-opencode/README.md
```

### 3. GitHub 代码搜索

**搜索语法**:

```
# 搜索 OpenCode agent 配置
".opencode/agents/" <关键词>

# 搜索 agent markdown 文件
"mode: subagent" <关键词>

# 搜索特定类型 agent
"description:" "code review" ".md"
```

**搜索 URL**:

```
https://github.com/search?q=%22.opencode%2Fagents%2F+<关键词>&type=code
```

## 搜索策略

### Step 1: 提取关键词

从用户需求中提取：
- 功能词（如 "code-review", "docs", "testing"）
- 技术栈词（如 "python", "react", "docker"）
- 角色词（如 "architect", "reviewer", "writer"）

### Step 2: 多源搜索

按优先级搜索：
1. **Claude Code Market** - 专业 agents，评分系统
2. **awesome-opencode** - OpenCode 专用
3. **GitHub 搜索** - 社区广泛贡献

### Step 3: 整理结果

对每个候选 Agent 记录：
- 名称和描述
- 来源链接
- 下载量/评分（如有）
- 最后更新时间
- 匹配度评估

## 搜索脚本使用

```bash
# 搜索 Agent
python scripts/search_agents.py <关键词>

# 带参数搜索
python scripts/search_agents.py <关键词> --limit 20 --sort downloads
```
