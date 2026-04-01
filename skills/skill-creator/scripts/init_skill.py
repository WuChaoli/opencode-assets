#!/usr/bin/env python3
"""生成标准 Skill 脚手架"""

import argparse
import os
import sys
from datetime import date

FRONTMATTER = """---
name: {name}
description: "[领域]能力：[简短描述]。触发条件：[关键词1]、[关键词2]。"
---
"""

SKILL_MD = """# {name} Skill

一句话说明这个 Skill 做什么。

## When to Use This Skill

触发条件（满足任一即可）：
- 当用户提到 [关键词] 时
- 当需要 [具体任务] 时

## Not For / Boundaries

此技能不适用于：
- [范围外内容]

必要输入（缺失时需询问）：
1. [必要输入1]

## Quick Reference

### 模式 1: [名称]
```
[可直接复制的命令/代码]
```

## Examples

### Example 1: [场景]

**输入**: [起始条件]
**步骤**:
1. [步骤1]
2. [步骤2]
**验收标准**: [如何判断成功]

### Example 2: [场景]

**输入**: [起始条件]
**步骤**:
1. [步骤1]
**验收标准**: [如何判断成功]

### Example 3: [场景]

**输入**: [起始条件]
**步骤**:
1. [步骤1]
**验收标准**: [如何判断成功]

## References

- `references/index.md` - 参考文档导航

## Maintenance

- Sources: [来源]
- Last updated: {today}
- Known limits: [已知限制]
"""


def main():
    parser = argparse.ArgumentParser(description="生成 Skill 脚手架")
    parser.add_argument("name", help="Skill 名称（小写-连字符）")
    parser.add_argument("--path", default=".", help="输出目录")
    args = parser.parse_args()

    base = os.path.join(args.path, args.name)
    for d in [base, f"{base}/references", f"{base}/scripts", f"{base}/assets"]:
        os.makedirs(d, exist_ok=True)

    with open(f"{base}/SKILL.md", "w", encoding="utf-8") as f:
        f.write(
            FRONTMATTER.format(name=args.name)
            + "\n"
            + SKILL_MD.format(name=args.name, today=date.today().isoformat())
        )

    with open(f"{base}/references/index.md", "w", encoding="utf-8") as f:
        f.write(
            f"# {args.name} 参考文档\n\n## 文档索引\n\n| 文档 | 说明 |\n|:---|:---|\n"
        )

    print(f"✓ Skill 脚手架已生成: {base}/")
    print(f"  ├─ SKILL.md")
    print(f"  ├─ references/")
    print(f"  ├─ scripts/")
    print(f"  └─ assets/")
    print(f"\n下一步: 编辑 SKILL.md 填写具体内容")


if __name__ == "__main__":
    main()
