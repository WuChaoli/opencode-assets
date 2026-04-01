# 搜索策略与 API 使用

## 搜索来源

### 1. SkillsMP（733,496+ Skills）

**网站**: https://skillsmp.com
**API**: https://skillsmp.com/docs/api

#### REST API

```bash
# 关键词搜索
curl -X GET "https://skillsmp.com/api/v1/skills/search?q=SEO&sortBy=stars&limit=10" \
  -H "Authorization: Bearer sk_live_your_api_key"

# AI 语义搜索
curl -X GET "https://skillsmp.com/api/v1/skills/ai-search?q=How+to+create+a+web+scraper" \
  -H "Authorization: Bearer sk_live_your_api_key"

# 按职业筛选
curl -X GET "https://skillsmp.com/api/v1/skills/search?q=automation&occupation=software-developers-151252&sortBy=stars" \
  -H "Authorization: Bearer sk_live_your_api_key"
```

#### API 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | ✓ | 搜索关键词 |
| page | number | - | 页码（默认 1） |
| limit | number | - | 每页数量（默认 20，最大 100） |
| sortBy | string | - | 排序：stars / recent（默认 recent） |
| category | string | - | 按分类筛选 |
| occupation | string | - | 按职业筛选 |

#### 速率限制

- 500 次/天/API Key
- 不支持通配符搜索

### 2. Anthropic 官方 Skills

**仓库**: https://github.com/anthropics/skills

#### 目录结构

```
anthropics/skills/
├── skills/
│   ├── docx/          # Word 文档处理
│   ├── pdf/           # PDF 处理
│   ├── pptx/          # PPT 处理
│   ├── xlsx/          # Excel 处理
│   └── ...            # 其他官方 skill
├── spec/              # Agent Skills 规范
└── template/          # Skill 模板
```

#### 使用方法

```bash
# Clone 官方仓库
git clone https://github.com/anthropics/skills.git

# 复制需要的 skill
cp -r skills/skills/docx ~/.config/opencode/skills/
```

### 3. GitHub 代码搜索

**搜索语法**:

```
"SKILL.md" <关键词>
```

**示例搜索**:

```
# 搜索 PDF 相关 Skill
"SKILL.md" pdf

# 搜索代码审查相关 Skill
"SKILL.md" code review

# 搜索特定分类
"SKILL.md" devops
```

**搜索 URL**:

```
https://github.com/search?q=%22SKILL.md%22+<关键词>&type=code
```

## 搜索策略

### Step 1: 提取关键词

从用户需求中提取：
- 核心领域词（如 "pdf", "code-review", "devops"）
- 功能词（如 "generate", "analyze", "convert"）
- 技术栈词（如 "python", "react", "docker"）

### Step 2: 多源搜索

按优先级搜索：
1. **SkillsMP** - 最大社区，AI 语义搜索
2. **Anthropic 官方** - 高质量官方实现
3. **GitHub 搜索** - 社区广泛贡献

### Step 3: 整理结果

对每个候选 Skill 记录：
- 名称和描述
- 来源链接
- Star 数（如有）
- 最后更新时间
- 匹配度评估

## 搜索脚本使用

```bash
# 搜索 SkillsMP
python scripts/search_skills.py <关键词>

# 带参数搜索
python scripts/search_skills.py <关键词> --limit 20 --sort stars

# AI 语义搜索
python scripts/search_skills.py <关键词> --ai-search
```
