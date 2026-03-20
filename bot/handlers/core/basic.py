from services.api import get_items, get_scores

def start():
    return "Welcome to LMS Bot!"

def help_cmd():
    return "/start - start bot\n/help - list commands\n/health - backend status\n/labs - list labs\n/scores <lab> - lab scores"

def health():
    data = get_items()
    if isinstance(data, str):
        return f"Backend error: {data}"
    return f"Backend is healthy. {len(data)} items available."

def labs():
    data = get_items()
    if isinstance(data, str):
        return f"Backend error: {data}"

    labs = [item for item in data if item["type"] == "lab"]
    result = "Available labs:\n"
    for lab in labs:
        result += f"- {lab['title']}\n"
    return result

def scores(cmd):
    parts = cmd.split()
    if len(parts) < 2:
        return "Usage: /scores lab-01"

    lab = parts[1]
    data = get_scores(lab)

    if isinstance(data, str):
        return f"Backend error: {data}"

    if not data:
        return f"No data found for {lab}"

    result = f"Pass rates for {lab}:\n"
    for item in data:
        result += f"- {item.get('task_name', 'task')}: {item.get('pass_rate', 0)}%\n"
    return result
