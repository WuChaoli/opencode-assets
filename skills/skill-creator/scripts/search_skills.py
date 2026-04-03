#!/usr/bin/env python3
"""Search SkillsMP for existing skills"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

SKILLSMP_API = "https://skillsmp.com/api/v1/skills"


def search_skills(query, api_key=None, limit=10, sort_by="stars", ai_search=False):
    """Search SkillsMP for skills matching query"""
    if not api_key:
        api_key = os.environ.get("SKILLSMP_API_KEY", "")

    if ai_search:
        url = f"{SKILLSMP_API}/ai-search?q={urllib.parse.quote(query)}"
    else:
        url = f"{SKILLSMP_API}/search?q={urllib.parse.quote(query)}&limit={limit}&sortBy={sort_by}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("Error: Invalid or missing API key")
            print("Set SKILLSMP_API_KEY environment variable or pass --api-key")
        elif e.code == 429:
            print("Error: Daily quota exceeded (500 requests/day)")
        else:
            print(f"Error: HTTP {e.code}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Cannot connect to SkillsMP: {e.reason}")
        sys.exit(1)


def format_results(data, query):
    """Format search results for display"""
    # Handle nested structure: data.skills or data.skills[]
    root = data.get("data", data)
    if isinstance(root, dict):
        skills = root.get("skills", [])
    elif isinstance(root, list):
        skills = root
    else:
        skills = []

    if not skills:
        print(f"No skills found for query: {query}")
        return

    total = data.get("data", {}).get("pagination", {}).get("total", len(skills))
    print(f"Found {total} skills for '{query}':\n")
    print(f"{'#':<4} {'Name':<35} {'Author':<20} {'Stars':<8} {'Description'}")
    print("-" * 100)

    for i, skill in enumerate(skills[:10], 1):
        name = skill.get("name", "Unknown")[:33]
        author = skill.get("author", "Unknown")[:18]
        stars = skill.get("stars", 0)
        desc = skill.get("description", "")[:40].replace("\n", " ")

        print(f"{i:<4} {name:<35} {author:<20} {stars:<8} {desc}")

    print(f"\nTotal: {total} skills found")
    print("Visit https://skillsmp.com for more details")


def main():
    parser = argparse.ArgumentParser(description="Search SkillsMP for existing skills")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--api-key", help="SkillsMP API key")
    parser.add_argument(
        "--limit", type=int, default=10, help="Max results (default: 10)"
    )
    parser.add_argument(
        "--sort", choices=["stars", "recent"], default="stars", help="Sort order"
    )
    parser.add_argument(
        "--ai-search", action="store_true", help="Use AI semantic search"
    )
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.api_key:
        os.environ["SKILLSMP_API_KEY"] = args.api_key

    data = search_skills(
        args.query, args.api_key, args.limit, args.sort, args.ai_search
    )

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        format_results(data, args.query)


if __name__ == "__main__":
    main()
