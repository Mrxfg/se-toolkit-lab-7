FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

# 🔥 MUHIM: infinite run
CMD ["sh", "-c", "uv run bot.py && tail -f /dev/null"]
