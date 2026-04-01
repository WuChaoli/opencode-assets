#!/usr/bin/env python3
"""Search for existing agents from various sources"""

import argparse
import json
import sys

SOURCES = {
    "claude_code_market": {
        "name": "Claude Code Market",
        "url": "https://www.ccmarket.dev/agents",
        "desc": "53+ agents, 50K+ downloads, rating system",
    },
    "awesome_opencode": {
        "name": "awesome-opencode",
        "url": "https://github.com/awesome-opencode/awesome-opencode",
        "desc": "4235 stars, OpenCode-specific agents",
    },
    "github": {
        "name": "GitHub Code Search",
        "url": "https://github.com/search?q=%22.opencode%2Fagents%2F+{query}&type=code",
        "desc": "Community-contributed agents",
    },
}


def search_agents(query, source="all", limit=10):
    """Search for agents across multiple sources"""
    results = []

    sources_to_search = [source] if source != "all" else list(SOURCES.keys())

    for src in sources_to_search:
        if src not in SOURCES:
            continue

        info = SOURCES[src]
        url = info["url"].replace("{query}", query.replace(" ", "+"))

        results.append(
            {
                "source": info["name"],
                "query_url": url,
                "description": info["desc"],
                "note": "Visit the URL to browse available agents",
            }
        )

    return results


def format_results(results, query):
    """Format search results for display"""
    if not results:
        print(f"No search sources available for query: {query}")
        return

    print(f"Agent search results for '{query}':\n")
    print(f"{'#':<4} {'Source':<25} {'Description':<40}")
    print("-" * 70)

    for i, result in enumerate(results, 1):
        source = result["source"][:23]
        desc = result["description"][:38]
        print(f"{i:<4} {source:<25} {desc:<40}")
        print(f"     URL: {result['query_url']}")
        print()

    print(f"\nSearch tips:")
    print(f"1. Visit Claude Code Market for rated agents")
    print(f"2. Check awesome-opencode for OpenCode-specific agents")
    print(f"3. Use GitHub search for community contributions")


def main():
    parser = argparse.ArgumentParser(description="Search for existing agents")
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--source",
        choices=["claude_code_market", "awesome_opencode", "github", "all"],
        default="all",
        help="Search source (default: all)",
    )
    parser.add_argument("--limit", type=int, default=10, help="Max results per source")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    results = search_agents(args.query, args.source, args.limit)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        format_results(results, args.query)


if __name__ == "__main__":
    main()
