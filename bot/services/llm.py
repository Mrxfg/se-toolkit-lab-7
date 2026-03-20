import requests
from config import LLM_API_KEY, LLM_API_BASE_URL, LLM_API_MODEL

def call_llm(messages, tools=None):
    url = f"{LLM_API_BASE_URL}/chat/completions"

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": LLM_API_MODEL,
        "messages": messages
    }

    if tools:
        data["tools"] = tools
        data["tool_choice"] = "auto"

    res = requests.post(url, headers=headers, json=data)

    if res.status_code != 200:
        return {"error": f"LLM error: {res.status_code} {res.text}"}

    return res.json()
