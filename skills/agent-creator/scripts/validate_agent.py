#!/usr/bin/env python3
"""Agent 质量验证脚本"""

import argparse
import os
import re
import sys


def validate(agent_path):
    results = {"passed": [], "failed": [], "warnings": []}

    if not os.path.exists(agent_path):
        results["failed"].append("File does not exist")
        return results

    with open(agent_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Frontmatter exists
    if content.startswith("---"):
        results["passed"].append("Has YAML frontmatter")
    else:
        results["failed"].append("Missing YAML frontmatter")
        return results

    # 2. description exists
    desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
    if desc_match:
        desc = desc_match.group(1).strip().strip('"').strip("'")
        if len(desc) > 10:
            results["passed"].append(
                f"description is detailed enough ({len(desc)} chars)"
            )
        else:
            results["warnings"].append("description is too short")
    else:
        results["failed"].append("Missing description field")

    # 3. mode exists
    mode_match = re.search(r"^mode:\s*(primary|subagent|all)", content, re.MULTILINE)
    if mode_match:
        results["passed"].append(f"mode specified: {mode_match.group(1)}")
    else:
        results["warnings"].append("mode not specified (defaults to all)")

    # 4. Has Role/Responsibilities section
    has_role = "## Role" in content or "## role" in content.lower()
    has_resp = (
        "## Responsibilities" in content or "## responsibilities" in content.lower()
    )
    if has_role:
        results["passed"].append("Has Role section")
    else:
        results["warnings"].append("Missing Role section")
    if has_resp:
        results["passed"].append("Has Responsibilities section")
    else:
        results["warnings"].append("Missing Responsibilities section")

    # 5. Has Available Resources
    has_resources = "## Available Resources" in content
    if has_resources:
        results["passed"].append("Has Available Resources section")
        # Check if it has at least one resource type
        has_skills = "### Skills" in content
        has_mcp = "### MCP" in content
        has_tools = "### Tools" in content
        if has_skills or has_mcp or has_tools:
            results["passed"].append(
                "Available Resources contains at least one resource type"
            )
        else:
            results["warnings"].append("Available Resources is empty")
    else:
        results["failed"].append("Missing Available Resources section")

    # 6. Has Constraints
    has_constraints = "## Constraints" in content or "## constraints" in content.lower()
    if has_constraints:
        results["passed"].append("Has Constraints section")
    else:
        results["warnings"].append("Missing Constraints section")

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate Agent quality")
    parser.add_argument("path", help="Agent file path")
    args = parser.parse_args()

    results = validate(args.path)

    score = len(results["passed"]) * 1 - len(results["failed"]) * 2
    status = "PASS" if not results["failed"] else "FAIL"
    print(f"\nAgent Validation: {status} (Score: {score})\n")

    if results["passed"]:
        print("PASSED:")
        for item in results["passed"]:
            print(f"  + {item}")

    if results["failed"]:
        print("\nFAILED:")
        for item in results["failed"]:
            print(f"  - {item}")

    if results["warnings"]:
        print("\nWARNINGS:")
        for item in results["warnings"]:
            print(f"  ! {item}")

    print(
        f"\nTotal: {len(results['passed'])} passed, {len(results['failed'])} failed, {len(results['warnings'])} warnings"
    )
    sys.exit(1 if results["failed"] else 0)


if __name__ == "__main__":
    main()
