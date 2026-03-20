from handlers.core.basic import start, help_cmd, health, labs, scores
from handlers.core.ai import route

# 9 tool/function schemas for LLM intent routing
TOOLS = [
    {"type": "function", "function": {"name": "get_items", "description": "List all available labs and tasks", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_learners", "description": "Get enrolled students and their groups", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_scores", "description": "Get score distribution for a lab. Lab format: 'lab-01'", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_pass_rates", "description": "Get per-task pass rates and attempt counts for a lab. Lab format: 'lab-01'", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_timeline", "description": "Get submissions per day timeline for a lab. Lab format: 'lab-01'", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_groups", "description": "Get per-group scores and student counts for a lab. Lab format: 'lab-01'", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_top_learners", "description": "Get top N learners by score for a lab. Lab format: 'lab-01'", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}, "limit": {"type": "integer", "description": "Number of top learners to return"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_completion_rate", "description": "Get completion rate percentage for a lab. Lab format: 'lab-01'", "parameters": {"type": "object", "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "trigger_sync", "description": "Refresh and sync data from the autochecker", "parameters": {"type": "object", "properties": {}}}},
]

# Inline keyboard buttons for common queries
BUTTONS = {
    "inline_keyboard": [
        [{"text": "📋 List Labs", "callback_data": "what labs are available?"}],
        [{"text": "📊 Best Lab", "callback_data": "which lab has the highest pass rate?"}],
        [{"text": "📉 Worst Lab", "callback_data": "which lab has the lowest pass rate?"}],
        [{"text": "🏆 Top Students", "callback_data": "who are the top 5 students?"}],
        [{"text": "👥 Students", "callback_data": "how many students are enrolled?"}],
        [{"text": "🔄 Sync Data", "callback_data": "sync data"}],
    ]
}


def get_buttons():
    return BUTTONS


def handle(cmd: str):
    # Slash commands routed directly, everything else goes to LLM router
    if cmd.startswith("/start"):
        return start()
    elif cmd.startswith("/help"):
        return help_cmd()
    elif cmd.startswith("/health"):
        return health()
    else:
        return route(cmd)


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        cmd = sys.argv[idx + 1]
        print(handle(cmd))
        exit(0)
