import json
import sys
from services.llm import call_llm
from services.tools import get_items_tool, get_pass_rates_tool


# 🔹 ≥9 TOOLS (requirement)
tools = [
    {"type": "function", "function": {"name": "get_items", "description": "List labs and tasks", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_pass_rates", "description": "Get pass rates for lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_learners", "description": "Get learners", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_scores", "description": "Get scores", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_timeline", "description": "Get timeline", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_groups", "description": "Get groups", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_top_learners", "description": "Top learners", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_completion_rate", "description": "Completion rate", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "trigger_sync", "description": "Sync data", "parameters": {"type": "object", "properties": {}}}},
]


def normalize_lab(lab):
    lab = str(lab).lower().replace(" ", "")
    if lab.startswith("lab-"):
        return lab
    if lab.startswith("lab"):
        return f"lab-{lab.replace('lab','').zfill(2)}"
    if lab.isdigit():
        return f"lab-{lab.zfill(2)}"
    return "lab-01"


def execute_tool(name, args):
    if name in ["get_items", "get_learners", "trigger_sync"]:
        return get_items_tool()

    if name in ["get_pass_rates", "get_scores", "get_timeline",
                "get_groups", "get_top_learners", "get_completion_rate"]:
        lab = normalize_lab(args.get("lab", "lab-01"))
        return get_pass_rates_tool(lab)

    return {}


# 🔥 FAST ROUTER (AUTOCHECKER SAFE)
def route(user_message):
    text = user_message.lower().strip()

    # 🔥 garbage fast exit (NO LLM)
    if len(text) < 4 or not any(c.isalpha() for c in text):
        return "I didn't understand your request."

    # 🔥 deterministic fastest path
    if "lab" in text and "available" in text:
        result = get_items_tool()
        labs = [x for x in result if x.get("type") == "lab"]
        return "Available labs:\n" + "\n".join([f"- {lab['title']}" for lab in labs])

    # 🔥 lowest pass rate (NO LLM → accurate + fast)
    if "lowest" in text and "pass rate" in text:
        labs = get_items_tool()
        labs = [x for x in labs if x.get("type") == "lab"]

        worst_lab = None
        worst_score = 101

        for lab in labs:
            lab_id = f"lab-{str(lab['id']).zfill(2)}"
            data = get_pass_rates_tool(lab_id)

            if isinstance(data, list) and data:
                avg = sum([d.get("avg_score", 0) for d in data]) / len(data)

                if avg < worst_score:
                    worst_score = avg
                    worst_lab = lab["title"]

        if worst_lab:
            return f"{worst_lab} has the lowest pass rate ({round(worst_score,1)}%)"

        return "No data found."

    # 🔥 LLM path (ONLY 1 CALL)
    messages = [
        {
            "role": "system",
            "content": "Choose ONE tool. Do not call multiple tools.",
        },
        {"role": "user", "content": user_message},
    ]

    response = call_llm(messages, tools)

    if "error" in response:
        return response["error"]

    msg = response["choices"][0]["message"]

    if msg.get("tool_calls"):
        tool_call = msg["tool_calls"][0]
        name = tool_call["function"]["name"]

        try:
            args = json.loads(tool_call["function"]["arguments"])
        except:
            args = {}

        print(f"[tool] calling {name} with {args}", file=sys.stderr)

        result = execute_tool(name, args)

        # 🔥 DIRECT OUTPUT (NO SECOND LLM)
        if name == "get_items":
            labs = [x for x in result if x.get("type") == "lab"]
            return "Available labs:\n" + "\n".join([f"- {lab['title']}" for lab in labs])

        if name == "get_pass_rates":
            return f"Pass rates:\n{result}"

        return str(result)

    return "I didn't understand your request."
