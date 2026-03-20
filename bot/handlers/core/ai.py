import json
import sys
import re
from services.llm import call_llm
from services.tools import get_items_tool, get_pass_rates_tool


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get list of labs",
            "parameters": {"type": "object", "properties": {}}
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get pass rates for a lab (use lab-01 format)",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string"}
                },
                "required": ["lab"]
            },
        },
    }
]


def normalize_lab(lab):
    lab = lab.lower()

    if lab.startswith("lab-"):
        return lab

    if "lab" in lab:
        match = re.search(r'\d+', lab)
        if match:
            num = match.group().zfill(2)
            return f"lab-{num}"

    if lab.isdigit():
        return f"lab-{lab.zfill(2)}"

    return lab


def execute_tool(name, args):
    if name == "get_items":
        return get_items_tool()

    elif name == "get_pass_rates":
        lab = normalize_lab(args.get("lab", "lab-01"))
        return get_pass_rates_tool(lab)

    return {}


def route(user_message):
    if len(user_message.strip()) < 4:
    	return "I didn't understand your request."

    if user_message.lower() not in ["hello", "hi"] and "lab" not in user_message.lower() and "score" not in user_message.lower():
    	if len(user_message.split()) <= 2:
            return "I didn't understand your request."
    if "lowest pass rate" in user_message.lower():
        items = get_items_tool()
        labs = [x for x in items if x.get("type") == "lab"]

        best_lab = None
        best_score = 999

        for lab in labs:
            lab_id = normalize_lab(lab["title"])
            data = get_pass_rates_tool(lab_id)

            if not data:
                continue

            avg = sum(
                x.get("avg_score", x.get("pass_rate", 0))
                for x in data
            ) / len(data)

            if avg < best_score:
                best_score = avg
                best_lab = lab["title"]

        if best_lab:
            return f"Based on the data, {best_lab} has the lowest pass rate ({best_score:.1f}%)."

        return "Could not determine lowest pass rate."


    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant that MUST use tools to answer questions about labs.\n"
                "First call tools to gather data.\n"
                "After that STOP and give final answer.\n"
                "Do not loop forever."
            )
        },
        {"role": "user", "content": user_message}
    ]

    for _ in range(3):
        response = call_llm(messages, tools)

        if "error" in response:
            return response["error"]

        msg = response["choices"][0]["message"]

        if "tool_calls" in msg:
            tool_call = msg["tool_calls"][0]
            name = tool_call["function"]["name"]

            try:
                args = json.loads(tool_call["function"]["arguments"])
            except:
                args = {}

            print(f"[tool] calling {name} with {args}", file=sys.stderr)

            result = execute_tool(name, args)

            messages.append(msg)
            messages.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call["id"]
            })

            messages.append({
                "role": "system",
                "content": "You now have enough data. Provide final answer."
            })

            continue

        return msg.get("content", "I didn't understand.")

    return "I didn't understand your request."
