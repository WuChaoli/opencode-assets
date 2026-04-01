---
name: glue-coding
description: "胶水开发模式：强依赖复用成熟库，仅编写最小胶水代码。触发条件：新功能开发、架构设计、代码生成时。核心原则：能抄不写，能连不造，能复用不原创。"
---

# glue-coding Skill

胶水开发（Glue Coding）是一种强依赖复用的开发模式。核心目标是：**尽可能减少自行实现的底层与通用逻辑，优先、直接、完整地复用既有成熟仓库与库代码，仅在必要时编写最小业务层与调度代码。**

## When to Use This Skill

触发条件（满足任一即可）：
- 需要实现新功能时
- 进行架构设计或技术选型时
- AI 准备生成代码之前
- 代码审查发现"重新造轮子"迹象时
- 用户提到"胶水"、"复用"、"glue"等关键词时

## Not For / Boundaries

此技能不适用于：
- 底层库/框架本身的开发（那是"造轮子"的正当场景）
- 学习目的的代码练习
- 性能极致优化需要定制实现的场景

必要输入（缺失时需询问）：
1. 目标功能描述
2. 当前技术栈/语言
3. 是否有推荐的库或参考仓库？

## Quick Reference

### 核心原则（MUST）

| 原则 | 说明 |
|:---|:---|
| **能抄不写** | 优先使用已验证的成熟代码 |
| **能连不造** | 优先组合现有模块而非新建 |
| **能复用不原创** | 除非有充分理由，否则不自己实现 |

### 依赖集成方式

允许并支持以下方式：
```python
# 方式1: 包管理器安装
pip install some-library
from some_library import feature

# 方式2: 本地源码直连
import sys
sys.path.append('/path/to/external/repo')
from external_module import function

# 方式3: editable install
pip install -e /path/to/local/repo
```

### 禁止行为（NEVER）

**禁止以下行为**：

1. **禁止 Mock/Stub/Demo**
   - 不允许用占位代码替代真实实现
   - 不允许"先占位、后实现"的空逻辑

2. **禁止功能裁剪**
   - 不允许复制代码到当前项目后修改
   - 不允许对依赖模块进行逻辑重写或降级封装

3. **禁止重复造轮子**
   - 若依赖库已提供功能，禁止自行重写同类逻辑
   - 先问"有没有现成的库"再动手写

4. **禁止伪集成**
   - 禁止"只导入不用"的假引用
   - 所有导入必须在运行期真实参与执行

### 当前项目的职责边界（SHOULD）

当前项目**仅允许**承担以下角色：
- 业务流程编排（Orchestration）
- 模块组合与调度
- 参数配置与调用组织
- 输入输出适配（不改变核心语义）

**明确禁止**：
- 重复实现算法
- 重写已有数据结构
- 将复杂逻辑从依赖库中"拆出来自己写"

### AI 生成代码时的输出规范

生成代码时，你必须：
1. **明确标注**哪些功能来自外部依赖
2. **不生成**依赖库内部的实现代码
3. **仅生成**最小必要的胶水代码与业务逻辑
4. 假设依赖库是**权威且不可修改的黑箱实现**

```python
# 正确示例：胶水代码
from validated_lib import DataProcessor, Validator

def process_user_request(request):
    """胶水代码：仅负责编排，不实现核心逻辑"""
    # 1. 使用外部库的验证器
    validated_data = Validator.validate(request)
    
    # 2. 使用外部库的处理器
    result = DataProcessor.process(validated_data)
    
    # 3. 胶水逻辑：格式化输出
    return {"status": "success", "data": result}
```

```python
# 错误示例：重复造轮子
def process_user_request(request):
    # 错误：自己实现验证逻辑
    if not isinstance(request, dict):
        raise ValueError("Invalid request")
    if "data" not in request:
        raise ValueError("Missing data field")
    
    # 错误：自己实现处理逻辑
    processed = {}
    for key, value in request["data"].items():
        processed[key] = transform(value)  # 自己写的 transform
    
    return processed
```

## Rules & Constraints

### MUST（必须遵守）

- 新功能开发前，先搜索是否有成熟库可用
- 使用的库必须是生产级实现，非 Demo 版本
- 所有依赖必须真实参与执行，禁止伪导入

### SHOULD（强烈建议）

- 优先使用官方/主流库而非小众实现
- 保持依赖版本锁定（requirements.txt / package-lock.json）
- 记录依赖来源与选择理由

### NEVER（禁止）

- 不要重写依赖库已有的功能
- 不要裁剪/修改第三方库源码
- 不要生成大段实现代码（应该调用库）

## Examples

### Example 1: HTTP 客户端

**需求**: 实现一个 HTTP 请求功能

**错误做法（造轮子）**:
```python
import socket
def http_get(url):
    # 自己实现 HTTP 协议...
    sock = socket.socket(...)
```

**正确做法（胶水）**:
```python
import httpx  # 成熟的 HTTP 库

async def fetch_data(url: str) -> dict:
    """胶水代码：仅组织调用，不实现 HTTP 细节"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Example 2: 数据验证

**需求**: 验证用户输入数据

**错误做法**:
```python
def validate_email(email):
    # 自己写正则表达式验证...
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@...'
```

**正确做法**:
```python
from pydantic import BaseModel, EmailStr

class UserInput(BaseModel):
    """胶水代码：使用 Pydantic 的验证能力"""
    email: EmailStr
    name: str
```

### Example 3: 文件处理

**需求**: 解析 Excel 文件

**错误做法**:
```python
def parse_excel(filepath):
    # 自己读取二进制格式...
    with open(filepath, 'rb') as f:
        magic_bytes = f.read(4)
```

**正确做法**:
```python
import pandas as pd

def parse_excel(filepath: str) -> pd.DataFrame:
    """胶水代码：pandas 处理所有细节"""
    return pd.read_excel(filepath)
```

## FAQ

**Q: 什么时候可以自己写代码？**
- A: 当且仅当：1) 找不到合适的库；2) 现有库无法满足特定需求；3) 性能瓶颈需要定制优化。即使如此，也应该先尝试扩展/包装现有库。

**Q: 如何判断一个库是否"生产级"？**
- A: 检查：1) GitHub Stars > 1000；2) 有持续维护（最近6个月有更新）；3) 有完整文档和测试；4) 被其他知名项目使用。

**Q: 胶水代码会不会太简单，显得没价值？**
- A: 恰恰相反！**评价标准不是"写了多少代码"，而是"是否正确、完整地站在成熟系统之上构建新系统"。** 最好的代码是不需要写的代码。

## References

- `references/index.md` - 参考文档导航
- [vibe-coding-cn 原始文档](https://github.com/tukuaiai/vibe-coding-cn)

## Maintenance

- Sources: vibe-coding-cn/prompts/02-编程提示词/胶水开发.md
- Last updated: 2026-01-15
- Known limits: 不适用于底层库开发场景
