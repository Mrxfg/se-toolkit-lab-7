# Plan

This bot will be implemented using a modular architecture with clear separation between handlers, services, and configuration. The handlers will be pure functions that accept input and return output without depending on Telegram. This allows easy testing using the CLI mode.

The bot will support commands such as /start, /help, /health, and /labs. In Task 2, these handlers will integrate with the backend API running on port 42002. In Task 3, we will add LLM-based intent routing using Qwen API.

The project will use Python with uv for dependency management. The entry point bot.py will support a --test mode for offline validation.

Finally, the bot will be deployed on the VM and optionally containerized.
