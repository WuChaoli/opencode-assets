#!/usr/bin/env python3
"""生成 OpenCode Agent 脚手架"""

import argparse
import os
import sys

PRIMARY_TEMPLATE = """---
description: {description}
mode: primary
# tools:              # 可选：控制哪些工具可用（上游 boolean）
#   write: false
#   edit: false
#   bash: false
---

# {name} Agent

## Role
You are a specialized agent for {purpose}.

## Responsibilities
- [职责 1]
- [职责 2]
- [职责 3]

## Available Resources

### Skills
- `[skill-name]` - [用途]

### MCP Servers
- `[mcp-name]` - [用途]

### Tools
- `[tool-name]` - [用途]

## Constraints
- [约束 1]
- [约束 2]
"""

SUBAGENT_TEMPLATE = """---
description: {description}
mode: subagent
# tools:              # 可选：控制哪些工具可用（上游 boolean）
#   write: false
#   edit: false
#   bash: false
permission:
  edit: {edit_perm}
  bash: {bash_perm}
  webfetch: {webfetch_perm}
---

# {name} Agent

## Role
You are a specialized agent for {purpose}.

## Responsibilities
- [职责 1]
- [职责 2]

## Available Resources

### Skills
- `[skill-name]` - [用途]

### MCP Servers
- `[mcp-name]` - [用途]

### Tools
- `[tool-name]` - [用途]

## Constraints
- [约束 1]
- [约束 2]
"""


def main():
    parser = argparse.ArgumentParser(description="生成 OpenCode Agent 脚手架")
    parser.add_argument("name", help="Agent 名称")
    parser.add_argument(
        "--type",
        choices=["primary", "subagent"],
        default="subagent",
        help="Agent 类型（默认: subagent）",
    )
    parser.add_argument("--path", default=".opencode/agents", help="输出目录")
    args = parser.parse_args()

    os.makedirs(args.path, exist_ok=True)
    filepath = os.path.join(args.path, f"{args.name}.md")

    if os.path.exists(filepath):
        print(f"Error: File already exists: {filepath}")
        sys.exit(1)

    purpose = f"{args.name} related tasks"
    description = f"Specialized agent for {args.name}"

    if args.type == "primary":
        content = PRIMARY_TEMPLATE.format(
            name=args.name, purpose=purpose, description=description
        )
    else:
        content = SUBAGENT_TEMPLATE.format(
            name=args.name,
            purpose=purpose,
            description=description,
            edit_perm="ask",
            bash_perm="ask",
            webfetch_perm="allow",
        )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Agent scaffold generated: {filepath}")
    print(f"  Type: {args.type}")
    print(
        f"  Next: Edit the file to fill in responsibilities, resources, and constraints"
    )


if __name__ == "__main__":
    main()
