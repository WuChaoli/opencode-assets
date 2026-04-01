#!/usr/bin/env python3
"""Agent audit diagnostic script"""

import argparse
import json
import os
import re
import sys


def audit(agent_path):
    results = {
        "basic": {},
        "structure": {"passed": [], "failed": [], "warnings": []},
        "content": {"passed": [], "failed": [], "warnings": []},
        "permissions": {"passed": [], "failed": [], "warnings": []},
        "issues": [],
    }

    if not os.path.exists(agent_path):
        results["issues"].append("CRITICAL: Agent file not found")
        return results

    with open(agent_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")

    results["basic"] = {
        "agent_path": agent_path,
        "prompt_lines": len(lines),
        "prompt_chars": len(content),
    }

    if content.startswith("---"):
        results["structure"]["passed"].append("Has YAML frontmatter")
    else:
        results["structure"]["failed"].append("Missing YAML frontmatter")

    desc_match = re.search(
        r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE
    )
    if desc_match:
        desc = desc_match.group(1).strip().strip('"').strip("'")
        if len(desc) > 10:
            results["content"]["passed"].append(
                f"description detailed ({len(desc)} chars)"
            )
        else:
            results["content"]["warnings"].append("description too short")
    else:
        results["content"]["failed"].append("Missing description")

    mode_match = re.search(r"^mode:\s*(primary|subagent|all)", content, re.MULTILINE)
    if mode_match:
        results["structure"]["passed"].append(f"mode specified: {mode_match.group(1)}")
    else:
        results["structure"]["warnings"].append("mode not specified")

    for section, desc in [
        ("## Role", "Role"),
        ("## Responsibilities", "Responsibilities"),
        ("## Available Resources", "Available Resources"),
        ("## Constraints", "Constraints"),
    ]:
        if section in content:
            results["structure"]["passed"].append("Has " + desc)
        else:
            results["structure"]["failed"].append("Missing " + desc)

    if "## Available Resources" in content:
        if "### Skills" in content or "### MCP" in content or "### Tools" in content:
            results["content"]["passed"].append("Available Resources has content")
        else:
            results["content"]["warnings"].append("Available Resources is empty")

    resp_start = content.find("## Responsibilities")
    if resp_start >= 0:
        resp_end = content.find("\n## ", resp_start + 1)
        resp_content = (
            content[resp_start:resp_end] if resp_end > 0 else content[resp_start:]
        )
        resp_count = resp_content.count("- [")
        if resp_count <= 5:
            results["content"]["passed"].append(f"Responsibilities <= 5 ({resp_count})")
        else:
            results["content"]["warnings"].append("Responsibilities > 5")

    if len(lines) <= 100:
        results["content"]["passed"].append(f"Prompt <= 100 lines ({len(lines)})")
    else:
        results["content"]["warnings"].append("Prompt > 100 lines")

    has_tools = re.search(r"^tools:", content, re.MULTILINE)
    has_permission = re.search(r"^permission:", content, re.MULTILINE)
    if has_tools or has_permission:
        results["permissions"]["passed"].append("Has tools/permission config")
    else:
        results["permissions"]["warnings"].append("No explicit tools/permission config")

    total_failed = len(results["structure"]["failed"]) + len(
        results["content"]["failed"]
    )
    total_warnings = (
        len(results["structure"]["warnings"])
        + len(results["content"]["warnings"])
        + len(results["permissions"]["warnings"])
    )

    if total_failed > 0:
        results["issues"].append(f"CRITICAL: {total_failed} issues found")
    if total_warnings > 0:
        results["issues"].append(f"WARNING: {total_warnings} improvements suggested")
    if total_failed == 0 and total_warnings == 0:
        results["issues"].append("OK: No issues detected")

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = audit(args.path)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print("Agent Audit Report")
        print("Path:", results["basic"].get("agent_path", "N/A"))
        print("Prompt:", results["basic"].get("prompt_lines", 0), "lines")
        print("STRUCTURE:")
        for item in results["structure"]["passed"]:
            print("  +", item)
        for item in results["structure"]["failed"]:
            print("  -", item)
        for item in results["structure"]["warnings"]:
            print("  !", item)
        print("CONTENT:")
        for item in results["content"]["passed"]:
            print("  +", item)
        for item in results["content"]["failed"]:
            print("  -", item)
        for item in results["content"]["warnings"]:
            print("  !", item)
        print("PERMISSIONS:")
        for item in results["permissions"]["passed"]:
            print("  +", item)
        for item in results["permissions"]["warnings"]:
            print("  !", item)
        print("ISSUES:")
        for issue in results["issues"]:
            print("  *", issue)

    sys.exit(1 if any("CRITICAL" in i for i in results["issues"]) else 0)


if __name__ == "__main__":
    main()
