#!/usr/bin/env python3
import json, os, sys
from datetime import datetime, timezone

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    def tok(obj):
        try: return len(json.dumps(obj)) // 4
        except: return 0

    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": data.get("session_id", ""),
        "tool_name": data.get("tool_name", ""),
        "duration_ms": data.get("duration_ms"),
        "input_tokens_estimate": tok(data.get("tool_input")),
        "output_tokens_estimate": tok(data.get("tool_response")),
    }

    log_path = os.path.expanduser("~/.claude/dgai-invocations.jsonl")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(row) + "\n")

if __name__ == "__main__":
    main()
