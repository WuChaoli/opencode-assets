# 胶水编程核心原则

## 哲学基础

胶水编程的核心哲学源自软件工程的基本原则：

> "最好的代码是不需要写的代码" — Jeff Atwood

> "评价标准不是写了多少代码，而是是否正确、完整地站在成熟系统之上构建新系统"

## 三大核心原则

### 1. 能抄不写

**含义**: 优先复制和使用已验证的成熟代码。

**实践**:
- 先搜索 GitHub/PyPI/npm 是否有现成实现
- 优先使用官方库或广泛使用的社区库
- 阅读优秀开源项目的实现方式

**检查点**:
- [ ] 我搜索过是否有现成的库了吗？
- [ ] 这个库的 Star 数和维护状态如何？
- [ ] 有没有更主流的替代方案？

### 2. 能连不造

**含义**: 优先组合现有模块而非新建模块。

**实践**:
- 使用管道/组合模式连接现有功能
- 通过配置而非代码实现差异化
- 使用适配器模式对接不兼容的接口

**检查点**:
- [ ] 能否通过组合现有模块实现需求？
- [ ] 是否可以用配置替代代码？
- [ ] 适配器能否解决接口不兼容问题？

### 3. 能复用不原创

**含义**: 除非有充分理由，否则不自己实现。

**实践**:
- 记录"为什么不能用现有库"的理由
- 定期审查自写代码，看是否能被库替换
- 新人入职时重点介绍项目依赖的库

**检查点**:
- [ ] 我有充分的理由自己实现吗？
- [ ] 这个自写代码将来能被库替换吗？
- [ ] 团队成员都了解这个决定吗？

## 反模式识别

### 重复造轮子的信号

当你看到或想到以下内容时，要警惕：

- "我来实现一个简单的 XXX"
- "这个功能很简单，不需要引入库"
- "现有库太重了，我写个轻量版"
- 代码中出现大段算法实现
- 自己写正则表达式验证常见格式
- 手动处理 HTTP/JSON/XML 等协议

### 正确的思维模式

培养这样的思考习惯：

- "有没有现成的库可以用？"
- "这个库的哪个 API 能解决我的问题？"
- "我需要写的只是连接这两个库的胶水"
- "让我先看看别人是怎么解决这个问题的"

## 胶水代码的特征

### 好的胶水代码

```python
# 特征：
# 1. 导入明确，来源清晰
# 2. 函数只做编排，不做实现
# 3. 注释说明"为什么"而非"怎么做"

from auth_lib import authenticate
from db_lib import get_user
from email_lib import send_welcome

async def register_user(email: str, password: str):
    """用户注册流程 - 编排三个外部服务"""
    user = await authenticate(email, password)  # 认证库处理
    await get_user(user.id)                      # 数据库库处理
    await send_welcome(email)                    # 邮件库处理
    return user
```

### 坏的"胶水"代码

```python
# 反模式：
# 1. 自己实现了应该由库处理的逻辑
# 2. 函数太长，包含实现细节
# 3. 重复造轮子

import hashlib
import smtplib

def register_user(email: str, password: str):
    # 自己实现密码哈希 - 应该用专业库
    hashed = hashlib.sha256(password.encode()).hexdigest()
    
    # 自己实现邮件发送 - 应该用邮件库
    server = smtplib.SMTP('localhost')
    server.sendmail('noreply@example.com', email, 'Welcome!')
    
    # 自己实现数据库操作 - 应该用 ORM
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users ...")
```

## 常见领域的库推荐

| 领域 | Python | JavaScript/Node | Go |
|:---|:---|:---|:---|
| HTTP 客户端 | httpx, requests | axios, got | net/http, resty |
| 数据验证 | pydantic, attrs | zod, yup | validator |
| 日期时间 | pendulum, arrow | dayjs, luxon | time (标准库) |
| JSON 处理 | orjson, ujson | (内置) | encoding/json |
| 数据库 ORM | SQLAlchemy, Tortoise | Prisma, TypeORM | GORM, ent |
| 测试 | pytest | jest, vitest | testing (标准库) |
| CLI | click, typer | commander, yargs | cobra |
| Web 框架 | FastAPI, Django | Express, Fastify | Gin, Echo |
