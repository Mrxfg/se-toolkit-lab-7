import sys
from handlers.basic import start, help_cmd, health, labs

def handle(cmd: str):
    if cmd.startswith("/start"):
        return start()
    elif cmd.startswith("/help"):
        return help_cmd()
    elif cmd.startswith("/health"):
        return health()
    elif cmd.startswith("/labs"):
        return labs()
    else:
        return "Unknown command"

if __name__ == "__main__":
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        cmd = sys.argv[idx + 1]
        print(handle(cmd))
        exit(0)

    print("Run with --test")
