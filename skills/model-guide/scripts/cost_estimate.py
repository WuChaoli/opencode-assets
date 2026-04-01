#!/usr/bin/env python3
"""Model cost estimation script for OpenCode Zen models"""

import argparse
import json
import sys

# Zen model prices (per 1M tokens)
MODELS = {
    # GPT series
    "gpt-5.4": {"input": 2.50, "output": 15.00, "name": "GPT 5.4"},
    "gpt-5.4-pro": {"input": 30.00, "output": 180.00, "name": "GPT 5.4 Pro"},
    "gpt-5.4-mini": {"input": 0.75, "output": 4.50, "name": "GPT 5.4 Mini"},
    "gpt-5.4-nano": {"input": 0.20, "output": 1.25, "name": "GPT 5.4 Nano"},
    "gpt-5.3-codex": {"input": 1.75, "output": 14.00, "name": "GPT 5.3 Codex"},
    "gpt-5.3-codex-spark": {
        "input": 1.75,
        "output": 14.00,
        "name": "GPT 5.3 Codex Spark",
    },
    "gpt-5.2": {"input": 1.75, "output": 14.00, "name": "GPT 5.2"},
    "gpt-5.2-codex": {"input": 1.75, "output": 14.00, "name": "GPT 5.2 Codex"},
    "gpt-5.1": {"input": 1.07, "output": 8.50, "name": "GPT 5.1"},
    "gpt-5.1-codex": {"input": 1.07, "output": 8.50, "name": "GPT 5.1 Codex"},
    "gpt-5.1-codex-max": {"input": 1.25, "output": 10.00, "name": "GPT 5.1 Codex Max"},
    "gpt-5.1-codex-mini": {"input": 0.25, "output": 2.00, "name": "GPT 5.1 Codex Mini"},
    "gpt-5": {"input": 1.07, "output": 8.50, "name": "GPT 5"},
    "gpt-5-codex": {"input": 1.07, "output": 8.50, "name": "GPT 5 Codex"},
    "gpt-5-nano": {"input": 0, "output": 0, "name": "GPT 5 Nano (Free)"},
    # Claude series
    "claude-opus-4-6": {"input": 5.00, "output": 25.00, "name": "Claude Opus 4.6"},
    "claude-opus-4-5": {"input": 5.00, "output": 25.00, "name": "Claude Opus 4.5"},
    "claude-opus-4-1": {"input": 15.00, "output": 75.00, "name": "Claude Opus 4.1"},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00, "name": "Claude Sonnet 4.6"},
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00, "name": "Claude Sonnet 4.5"},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00, "name": "Claude Sonnet 4"},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00, "name": "Claude Haiku 4.5"},
    "claude-3-5-haiku": {"input": 0.80, "output": 4.00, "name": "Claude 3.5 Haiku"},
    # Gemini series
    "gemini-3.1-pro": {"input": 2.00, "output": 12.00, "name": "Gemini 3.1 Pro"},
    "gemini-3-flash": {"input": 0.50, "output": 3.00, "name": "Gemini 3 Flash"},
    # Other models
    "minimax-m2.5": {"input": 0.30, "output": 1.20, "name": "MiniMax M2.5"},
    "minimax-m2.5-free": {"input": 0, "output": 0, "name": "MiniMax M2.5 Free"},
    "glm-5": {"input": 1.00, "output": 3.20, "name": "GLM 5"},
    "kimi-k2.5": {"input": 0.60, "output": 3.00, "name": "Kimi K2.5"},
    "big-pickle": {"input": 0, "output": 0, "name": "Big Pickle (Free)"},
    "mimo-v2-pro-free": {"input": 0, "output": 0, "name": "MiMo V2 Pro Free"},
    "mimo-v2-omni-free": {"input": 0, "output": 0, "name": "MiMo V2 Omni Free"},
    "qwen3.6-plus-free": {"input": 0, "output": 0, "name": "Qwen3.6 Plus Free"},
    "nemotron-3-super-free": {"input": 0, "output": 0, "name": "Nemotron 3 Super Free"},
}


def estimate(input_tokens, output_tokens, model_key):
    if model_key not in MODELS:
        print(f"Unknown model: {model_key}")
        print(f"Available: {', '.join(sorted(MODELS.keys()))}")
        sys.exit(1)

    model = MODELS[model_key]
    input_cost = (input_tokens / 1_000_000) * model["input"]
    output_cost = (output_tokens / 1_000_000) * model["output"]
    total = input_cost + output_cost

    return {
        "model": model["name"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Estimate OpenCode Zen model usage cost"
    )
    parser.add_argument("--input", type=int, required=True, help="Input tokens")
    parser.add_argument("--output", type=int, required=True, help="Output tokens")
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-6",
        help="Model key (default: claude-sonnet-4-6)",
    )
    parser.add_argument("--all", action="store_true", help="Show all models")
    args = parser.parse_args()

    if args.all:
        print(
            f"Cost estimate for {args.input:,} input + {args.output:,} output = {args.input + args.output:,} total tokens\n"
        )
        print(f"{'Model':<30} {'Input Cost':>12} {'Output Cost':>12} {'Total':>12}")
        print("-" * 70)
        sorted_models = sorted(
            MODELS.items(),
            key=lambda x: (x[1]["input"] + x[1]["output"]) / 2
            if (x[1]["input"] + x[1]["output"]) > 0
            else -1,
        )
        for key, model in sorted_models:
            input_cost = (args.input / 1_000_000) * model["input"]
            output_cost = (args.output / 1_000_000) * model["output"]
            total = input_cost + output_cost
            print(
                f"{model['name']:<30} ${input_cost:>10.4f} ${output_cost:>10.4f} ${total:>10.4f}"
            )
    else:
        result = estimate(args.input, args.output, args.model)
        print(f"Cost Estimate")
        print(f"=============")
        print(f"Model: {result['model']}")
        print(f"Input tokens: {result['input_tokens']:,}")
        print(f"Output tokens: {result['output_tokens']:,}")
        print(f"Total tokens: {result['total_tokens']:,}")
        print(f"Input cost: ${result['input_cost']:.4f}")
        print(f"Output cost: ${result['output_cost']:.4f}")
        print(f"Total cost: ${result['total_cost']:.4f}")


if __name__ == "__main__":
    main()
