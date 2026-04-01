#!/usr/bin/env python3
"""Skill 审计诊断脚本"""

import argparse
import json
import os
import sys


def audit(skill_path):
    results = {
        "basic": {},
        "structure": {"passed": [], "failed": [], "warnings": []},
        "content": {"passed": [], "failed": [], "warnings": []},
        "context": {"passed": [], "failed": [], "warnings": []},
        "issues": [],
    }

    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        results["issues"].append("CRITICAL: SKILL.md not found")
        return results

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    # Basic info
    results["basic"] = {
        "skill_path": skill_path,
        "skill_md_lines": len(lines),
        "skill_md_chars": len(content),
    }

    # Structure checks
    required_sections = [
        ("When to Use", "触发条件"),
        ("Not For", "边界定义"),
        ("Quick Reference", "快速参考"),
        ("Examples", "示例"),
    ]
    for section, desc in required_sections:
        if section in content:
            results["structure"]["passed"].append(f'Has "{section}" ({desc})')
        else:
            results["structure"]["failed"].append(f'Missing "{section}" ({desc})')

    # Content checks
    # description detail
    import re

    desc_match = re.search(
        r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE
    )
    if desc_match:
        desc = desc_match.group(1)
        if len(desc) > 20:
            results["content"]["passed"].append(
                f"description detailed ({len(desc)} chars)"
            )
        else:
            results["content"]["warnings"].append(
                f"description too short ({len(desc)} chars)"
            )
    else:
        results["content"]["failed"].append("Missing description")

    # Examples count
    example_count = content.count("### Example")
    if example_count >= 3:
        results["content"]["passed"].append(f"Examples >= 3 ({example_count})")
    else:
        results["content"]["warnings"].append(f"Examples < 3 ({example_count})")

    # Context checks
    if len(lines) <= 200:
        results["context"]["passed"].append(f"SKILL.md <= 200 lines ({len(lines)})")
    else:
        results["context"]["warnings"].append(
            f"SKILL.md > 200 lines ({len(lines)}), consider splitting"
        )

    # Quick Reference patterns
    qr_start = content.find("## Quick Reference")
    if qr_start >= 0:
        next_section = content.find("\n## ", qr_start + 1)
        qr_content = (
            content[qr_start:next_section] if next_section > 0 else content[qr_start:]
        )
        pattern_count = qr_content.count("### ")
        if pattern_count <= 20:
            results["context"]["passed"].append(
                f"Quick Reference <= 20 patterns ({pattern_count})"
            )
        else:
            results["context"]["warnings"].append(
                f"Quick Reference > 20 patterns ({pattern_count})"
            )

    # references/ directory
    ref_dir = os.path.join(skill_path, "references")
    if os.path.isdir(ref_dir):
        ref_files = [f for f in os.listdir(ref_dir) if f.endswith(".md")]
        results["context"]["passed"].append(
            f"references/ exists ({len(ref_files)} files)"
        )

        # Check index.md
        if os.path.exists(os.path.join(ref_dir, "index.md")):
            results["context"]["passed"].append("references/index.md exists")
        else:
            results["context"]["warnings"].append("Missing references/index.md")

        # Check individual file sizes
        for ref_file in ref_files:
            ref_path = os.path.join(ref_dir, ref_file)
            with open(ref_path, "r", encoding="utf-8") as f:
                ref_lines = len(f.readlines())
            if ref_lines > 300:
                results["context"]["warnings"].append(
                    f"{ref_file} > 300 lines ({ref_lines})"
                )
    else:
        results["context"]["warnings"].append("No references/ directory")

    # Collect issues
    total_failed = len(results["structure"]["failed"]) + len(
        results["content"]["failed"]
    )
    total_warnings = (
        len(results["structure"]["warnings"])
        + len(results["content"]["warnings"])
        + len(results["context"]["warnings"])
    )

    if total_failed > 0:
        results["issues"].append(
            f"CRITICAL: {total_failed} structure/content issues found"
        )
    if total_warnings > 0:
        results["issues"].append(f"WARNING: {total_warnings} improvements suggested")
    if total_failed == 0 and total_warnings == 0:
        results["issues"].append("OK: No issues detected")

    return results


def main():
    parser = argparse.ArgumentParser(description="Audit Skill quality")
    parser.add_argument("path", help="Skill directory path")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    results = audit(args.path)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"\nSkill Audit Report")
        print(f"==================")
        print(f"Path: {results['basic'].get('skill_path', 'N/A')}")
        print(
            f"SKILL.md: {results['basic'].get('skill_md_lines', 0)} lines, {results['basic'].get('skill_md_chars', 0)} chars"
        )
        print()

        print("STRUCTURE:")
        for item in results["structure"]["passed"]:
            print(f"  + {item}")
        for item in results["structure"]["failed"]:
            print(f"  - {item}")
        for item in results["structure"]["warnings"]:
            print(f"  ! {item}")
        print()

        print("CONTENT:")
        for item in results["content"]["passed"]:
            print(f"  + {item}")
        for item in results["content"]["failed"]:
            print(f"  - {item}")
        for item in results["content"]["warnings"]:
            print(f"  ! {item}")
        print()

        print("CONTEXT:")
        for item in results["context"]["passed"]:
            print(f"  + {item}")
        for item in results["context"]["warnings"]:
            print(f"  ! {item}")
        print()

        print("ISSUES:")
        for issue in results["issues"]:
            print(f"  * {issue}")

    sys.exit(1 if any("CRITICAL" in i for i in results["issues"]) else 0)


if __name__ == "__main__":
    main()
