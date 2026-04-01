#!/usr/bin/env python3
"""Skill 质量验证脚本"""

import argparse
import json
import os
import re
import sys


def validate(skill_path):
    results = {"passed": [], "failed": [], "warnings": []}

    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        results["failed"].append("缺少 SKILL.md")
        return results

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Frontmatter 存在
    if content.startswith("---"):
        results["passed"].append("有 YAML frontmatter")
    else:
        results["failed"].append("缺少 YAML frontmatter")

    # 2. name 格式
    name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if name_match:
        name = name_match.group(1).strip()
        if re.match(r"^[a-z][a-z0-9-]*$", name):
            results["passed"].append(f"name 格式正确: {name}")
        else:
            results["failed"].append(
                f"name 格式错误: {name}（应匹配 ^[a-z][a-z0-9-]*$）"
            )
    else:
        results["failed"].append("缺少 name 字段")

    # 3. description 包含触发词
    desc_match = re.search(
        r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE
    )
    if desc_match:
        desc = desc_match.group(1)
        if len(desc) > 20:
            results["passed"].append("description 足够详细")
        else:
            results["warnings"].append("description 太短，建议包含具体触发词")
    else:
        results["failed"].append("缺少 description 字段")

    # 4. 必须章节
    for section in ["When to Use", "Not For", "Quick Reference", "Examples"]:
        if section in content:
            results["passed"].append(f'有 "{section}" 章节')
        else:
            results["failed"].append(f'缺少 "{section}" 章节')

    # 5. Examples 数量
    example_count = content.count("### Example")
    if example_count >= 3:
        results["passed"].append(f"Examples ≥ 3 个（{example_count} 个）")
    else:
        results["failed"].append(f"Examples 不足 3 个（当前 {example_count} 个）")

    # 6. Quick Reference 长度
    qr_start = content.find("## Quick Reference")
    if qr_start >= 0:
        next_section = content.find("\n## ", qr_start + 1)
        qr_content = (
            content[qr_start:next_section] if next_section > 0 else content[qr_start:]
        )
        pattern_count = qr_content.count("### ")
        if pattern_count > 20:
            results["warnings"].append(
                f"Quick Reference 超过 20 个模式（{pattern_count} 个）"
            )

    # 7. references/ 存在
    if os.path.isdir(os.path.join(skill_path, "references")):
        results["passed"].append("有 references/ 目录")
    else:
        results["warnings"].append("建议添加 references/ 目录")

    return results


def main():
    parser = argparse.ArgumentParser(description="验证 Skill 质量")
    parser.add_argument("path", help="Skill 目录路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    results = validate(args.path)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        score = len(results["passed"]) * 1 - len(results["failed"]) * 2
        status = "PASS" if not results["failed"] else "FAIL"
        print(f"\nSkill Validation: {status} (Score: {score})\n")

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
