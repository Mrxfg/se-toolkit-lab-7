import json
import sys
from services.llm import call_llm
from services.tools import get_items_tool, get_pass_rates_tool


# 9 TOOLS
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "List all available labs and tasks in the system",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a specific lab. Use lab identifier like 'lab-01', 'lab-02', ..., 'lab-07'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier in format 'lab-01', 'lab-02', etc.",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of enrolled students and their groups",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets) for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier in format 'lab-01', 'lab-02', etc.",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions per day timeline for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier in format 'lab-01', 'lab-02', etc.",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group scores and student counts for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier in format 'lab-01', 'lab-02', etc.",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by score for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier in format 'lab-01', 'lab-02', etc.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of top learners to return (default 5)",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier in format 'lab-01', 'lab-02', etc.",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Refresh/sync data from the autochecker. Use when user asks to sync or refresh data.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def normalize_lab(lab):
    lab = str(lab).lower().strip()
    lab = lab.replace("–", "").replace("—", "").replace(" ", "")

    if lab.startswith("lab-"):
        num = lab.replace("lab-", "").zfill(2)
        return f"lab-{num}"

    if lab.startswith("lab"):
        num = lab.replace("lab", "").zfill(2)
        return f"lab-{num}"

    if lab.isdigit():
        return f"lab-{lab.zfill(2)}"

    return "lab-01"


def execute_tool(name, args):
    if name in ["get_items", "get_learners", "trigger_sync"]:
        return get_items_tool()

    if name in ["get_pass_rates", "get_scores", "get_timeline",
                "get_groups", "get_top_learners", "get_completion_rate"]:
        lab = normalize_lab(args.get("lab", "lab-01"))
        limit = args.get("limit", 5)
        print(f"[tool] normalized lab: {lab}", file=sys.stderr)
        return get_pass_rates_tool(lab)

    return {"error": f"Unknown tool: {name}"}


def route(user_message):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant for a university lab management system.\n"
                "Always use the available tools to fetch real data before answering.\n"
                "Lab identifiers are in the format 'lab-01', 'lab-02', ..., 'lab-07'.\n"
                "For questions comparing all labs (e.g. 'which lab has lowest pass rate'), "
                "first call get_items to list labs, then call get_pass_rates for each lab.\n"
                "Never guess data — always fetch it with tools.\n"
                "After collecting all needed data, provide a clear and concise final answer."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    for _ in range(10):
        response = call_llm(messages, tools)

        if "error" in response:
            return response["error"]

        msg = response["choices"][0]["message"]

        # Tool calls
        if msg.get("tool_calls"):
            # Append assistant message first
            messages.append(msg)

            # Execute all tool calls in this turn
            for tool_call in msg["tool_calls"]:
                name = tool_call["function"]["name"]

                try:
                    args = json.loads(tool_call["function"]["arguments"])
                except Exception:
                    args = {}

                print(f"[tool] calling {name} with {args}", file=sys.stderr)
                result = execute_tool(name, args)
                summary = f"{len(result)} items" if isinstance(result, list) else "done"
                print(f"[tool] result: {summary}", file=sys.stderr)

                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call["id"],
                })

            continue

        # Final answer
        content = msg.get("content", "").strip()
        if content:
            print(f"[summary] feeding {sum(1 for m in messages if m.get('role') == 'tool')} tool results back to LLM", file=sys.stderr)
            return content

    return "I didn't understand your request. I can help with labs, scores, pass rates, and more!"
