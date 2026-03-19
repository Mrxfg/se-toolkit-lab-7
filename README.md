# Lab 7 — Build a Client with an AI Coding Agent

The lab gets updated regularly, so do [sync your fork with the upstream](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork#syncing-a-fork-branch-from-the-command-line) from time to time.

<h2>Table of contents</h2>

- [Lab story](#lab-story)
- [Learning advice](#learning-advice)
- [Learning outcomes](#learning-outcomes)
- [Tasks](#tasks)
  - [Prerequisites](#prerequisites)
  - [Required](#required)

## Lab story

> "The best way to understand an API is to build a client for it."

You will use an AI coding agent (Qwen Code) to build a Telegram bot client for your LMS backend. The bot connects to your backend, fetches real data, and uses an LLM to answer natural language questions.

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌──────────────┐     ┌──────────────────────────────────┐   │
│  │  Telegram    │────▶│  Your Bot                        │   │
│  │  User        │◀────│  (aiogram / python-telegram-bot) │   │
│  └──────────────┘     └──────┬───────────────────────────┘   │
│                              │                               │
│                              │ slash commands + plain text   │
│                              ├───────▶ /start, /help         │
│                              ├───────▶ /health, /labs        │
│                              ├───────▶ intent router ──▶ LLM |
│                              │                    │          │
│                              │                    ▼          │
│  ┌──────────────┐     ┌──────┴───────┐    tools/actions      │
│  │  Docker      │     │  LMS Backend │◀───── GET /items      │
│  │  Compose     │     │  (FastAPI)   │◀───── GET /analytics  │
│  │              │     │  + PostgreSQL│◀───── POST /sync      │
│  └──────────────┘     └──────────────┘                       │
└──────────────────────────────────────────────────────────────┘
```

## Learning advice

This lab is about learning to collaborate with an AI coding agent as a development partner. You are not following step-by-step instructions — you are building a product.

The bot you build is practical (~200-400 lines). The learning comes from the iterative process of planning, building, testing, and debugging with agent assistance. Document your design decisions and architecture.

## Learning outcomes

By the end of this lab, you should be able to:

- Use an AI coding agent to plan and implement a client application.
- Design a testable handler architecture (logic separated from transport).
- Connect a client to an existing REST API with authentication.
- Implement natural language intent routing using LLM tool/function calling.
- Debug integration issues iteratively with agent assistance.
- Deploy a multi-service system (backend + bot) on a remote VM.

In simple words, you should be able to say:
>
> 1. I built a Telegram bot that talks to my backend!
> 2. I can ask it questions in plain language and it fetches the right data!
> 3. I used an AI coding agent to plan and build the whole thing!

## Tasks

### Prerequisites

1. Complete the [lab setup](./lab/tasks/setup-simple.md#lab-setup)

> **Note**: If this is the first lab you are attempting in this course, you need to do the [full version of the setup](./lab/tasks/setup.md#lab-setup)

### Required

1. [Plan and Scaffold](./lab/tasks/required/task-1.md#plan-and-scaffold)
2. [Backend Integration](./lab/tasks/required/task-2.md#backend-integration)
3. [Intent-Based Natural Language Routing](./lab/tasks/required/task-3.md#intent-based-natural-language-routing)
4. [Deploy and Document](./lab/tasks/required/task-4.md#deploy-and-document)
