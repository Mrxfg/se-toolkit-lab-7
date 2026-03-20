from handlers.core.basic import start, help_cmd, health, labs, scores
from handlers.core.ai import route

def handle(cmd: str):
    if cmd.startswith("/start"):
        return start()
    elif cmd.startswith("/help"):
        return help_cmd()
    elif cmd.startswith("/health"):
        return health()
    elif cmd.startswith("/labs"):
        return labs()
    elif cmd.startswith("/scores"):
        return scores(cmd)
    else:
        return "Unknown command. Use /help"

def handle(cmd: str):
    if cmd.startswith("/"):
        # old commands
        ...
    else:
        return route(cmd)

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        cmd = sys.argv[idx + 1]
        print(handle(cmd))
        exit(0)
