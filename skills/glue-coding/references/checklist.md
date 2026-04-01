# 胶水代码审查清单

## 快速检查（5 分钟）

### 依赖使用

- [ ] 是否优先使用了成熟的第三方库？
- [ ] 使用的库是否为生产级实现（非 Demo/Mock）？
- [ ] 依赖版本是否已锁定？

### 代码职责

- [ ] 当前项目代码是否仅负责编排/调度？
- [ ] 是否存在重复实现的算法？
- [ ] 是否存在重写的数据结构？

### 禁止行为

- [ ] 是否存在 Mock/Stub/Demo 代码？
- [ ] 是否有"只导入不用"的伪集成？
- [ ] 是否有复制后修改的第三方代码？

## 详细审查（15 分钟）

### 1. 依赖选择审查

**检查项**:
- [ ] 每个自写功能是否有对应的成熟库？
- [ ] 选择的库是否是该领域的主流方案？
- [ ] 库的 GitHub Star 数是否 > 1000？
- [ ] 库在最近 6 个月内是否有更新？
- [ ] 库是否有完整的文档和测试？

**发现问题时的行动**:
1. 搜索替代库
2. 评估迁移成本
3. 记录选择理由

### 2. 代码职责审查

**检查项**:
- [ ] 函数是否只做编排，不做实现？
- [ ] 是否有超过 50 行的业务逻辑函数？
- [ ] 是否有自己实现的通用算法（排序、搜索、加密等）？
- [ ] 是否有自己实现的协议处理（HTTP、JSON、XML 等）？

**发现问题时的行动**:
1. 识别可以提取到库的部分
2. 搜索替代库
3. 重构为胶水代码

### 3. 禁止行为审查

**检查项**:
- [ ] 搜索代码中的 "TODO", "FIXME", "HACK"
- [ ] 检查是否有空函数体或 pass 语句
- [ ] 检查是否有注释掉的实现代码
- [ ] 检查导入是否都被使用

**发现问题时的行动**:
1. 移除或实现 TODO
2. 删除伪代码
3. 清理未使用的导入

## 审查结果模板

```markdown
## 胶水代码审查结果

**文件/模块**: [文件路径或模块名]
**审查人**: [姓名/AI]
**日期**: [YYYY-MM-DD]

### 1. 依赖使用评分: [1-5]/5

**现状**:
- 使用的库: [列表]
- 自写功能: [列表]

**问题**:
- [ ] [问题描述]

**建议**:
- [ ] [改进建议]

### 2. 代码职责评分: [1-5]/5

**现状**:
- 编排代码占比: [百分比]
- 实现代码占比: [百分比]

**问题**:
- [ ] [问题描述]

**建议**:
- [ ] [改进建议]

### 3. 禁止行为评分: [1-5]/5

**发现的问题**:
- [ ] [问题描述]

**建议**:
- [ ] [改进建议]

### 总评

**总分**: [X]/15
**是否符合胶水编程原则**: [是/否/部分符合]

**优先改进项**:
1. [最重要的改进]
2. [次要改进]
3. [可选改进]

**下次审查日期**: [YYYY-MM-DD]
```

## 自动化检查脚本（示例）

```python
#!/usr/bin/env python3
"""胶水代码自动检查脚本"""

import ast
import sys
from pathlib import Path

# 可能表示"造轮子"的函数名模式
WHEEL_REINVENTION_PATTERNS = [
    'http_get', 'http_post', 'http_request',
    'parse_json', 'parse_xml', 'parse_csv',
    'validate_email', 'validate_phone', 'validate_url',
    'hash_password', 'encrypt', 'decrypt',
    'send_email', 'send_sms',
    'connect_db', 'execute_sql',
]

def check_file(filepath: Path) -> list[str]:
    """检查单个文件"""
    issues = []
    
    with open(filepath) as f:
        tree = ast.parse(f.read())
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # 检查函数名
            for pattern in WHEEL_REINVENTION_PATTERNS:
                if pattern in node.name.lower():
                    issues.append(
                        f"Line {node.lineno}: 函数 '{node.name}' "
                        f"可能在重复造轮子，考虑使用现有库"
                    )
            
            # 检查函数长度
            if len(node.body) > 30:
                issues.append(
                    f"Line {node.lineno}: 函数 '{node.name}' "
                    f"有 {len(node.body)} 行，可能包含应该由库处理的逻辑"
                )
    
    return issues

if __name__ == '__main__':
    for filepath in sys.argv[1:]:
        issues = check_file(Path(filepath))
        if issues:
            print(f"\n{filepath}:")
            for issue in issues:
                print(f"  - {issue}")
```

使用方法:
```bash
python glue_checker.py src/**/*.py
```
