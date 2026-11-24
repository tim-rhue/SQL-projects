"""The helpers switch (rules/CORE.md section 3): Claude works alone unless Tim turned helpers on.

Claude Code runs this hook at two moments (.claude/settings.json):
- UserPromptSubmit, on every message: "helpers on" or "turn on helpers" opens a scope for this
  request and tells Claude to ask how long; "helpers off" closes it; any other message ends a
  request-only scope, or an expired one.
- PreToolUse, before a helper starts (Agent, Task, Workflow, a new session): refused unless a
  scope is open.

After Tim answers, Claude records the scope from Bash, and only in the request that turned
helpers on:
    python3 .claude/hooks/helpers.py scope request|session|until YYYY-MM-DDTHH:MM

The state lives outside the repo (one small file per checkout), so git never sees it. A payload
the hook cannot read never blocks the session. tims-rules helpers hook, rules v1: a copy of tim-
rhue/lean-app-template's file.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ON = re.compile(r"\b(helpers on|turn on helpers)\b", re.IGNORECASE)
OFF = re.compile(r"\bhelpers off\b", re.IGNORECASE)
HELPER_TOOLS = re.compile(r"^(Agent|Task|Workflow)$|__create_session$")
ASK = (
    "Tim turned helpers on (rules/CORE.md section 3). Before using any, ask him once how "
    "long: this request only (the default), the whole session, or until a day and time he"
    " names. Then record it: python3 .claude/hooks/helpers.py scope request|session|until"
    " YYYY-MM-DDTHH:MM"
)
REFUSED = (
    "Helpers are off: Claude works alone (rules/CORE.md section 3). Do this step here, in"
    ' this session. Tim turns helpers on with "helpers on".'
)


def state_path(project: Path | None = None) -> Path:
    """One state file per checkout, under XDG_STATE_HOME (or ~/.local/state)."""
    root = project or Path(__file__).resolve().parents[2]
    base = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state")
    key = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:16]
    return base / "claude-helpers" / f"{key}.json"


def load(path: Path) -> dict:
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return state if isinstance(state, dict) else {}


def save(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state), encoding="utf-8")


def is_open(state: dict, now: datetime) -> bool:
    scope = state.get("scope")
    if scope in ("request", "session"):
        return True
    if scope == "until":
        try:
            return datetime.fromisoformat(str(state.get("until"))) > now
        except ValueError:
            return False
    return False


def on_prompt(prompt: str, path: Path, now: datetime) -> str:
    """Called on every message. Returns the note Claude sees, or an empty string."""
    if OFF.search(prompt):
        save(path, {})
        return "Helpers are off again (rules/CORE.md section 3)."
    if ON.search(prompt):
        save(path, {"scope": "request", "asked": True})
        return ASK
    state = load(path)
    if state.get("scope") == "request" or not is_open(state, now):
        save(path, {})
    elif state.get("asked"):
        save(path, {**state, "asked": False})
    return ""


def on_tool(tool_name: str, path: Path, now: datetime) -> str | None:
    """Called before a tool runs. Returns why a helper is refused, or None to let the tool run."""
    if not HELPER_TOOLS.search(tool_name) or is_open(load(path), now):
        return None
    return REFUSED


def set_scope(args: list[str], path: Path, now: datetime) -> tuple[int, str]:
    state = load(path)
    if not state.get("asked"):
        return 1, "refused: Tim has not turned helpers on in this request"
    kind = args[0] if args else ""
    if kind in ("request", "session") and len(args) == 1:
        save(path, {"scope": kind, "asked": True})
        return 0, f"helpers on for this {kind}"
    if kind == "until" and len(args) == 2:
        try:
            until = datetime.fromisoformat(args[1])
        except ValueError:
            return 2, "usage: until YYYY-MM-DDTHH:MM"
        if until <= now:
            return 2, "refused: that time has passed"
        save(path, {"scope": "until", "until": until.isoformat(timespec="minutes"), "asked": True})
        return 0, f"helpers on until {until.isoformat(timespec='minutes')}"
    return 2, "usage: scope request|session|until YYYY-MM-DDTHH:MM"


def main(argv: list[str]) -> int:
    now = datetime.now()
    if argv[1:2] == ["scope"]:
        code, message = set_scope(argv[2:], state_path(), now)
        print(message)
        return code
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    if not isinstance(payload, dict):
        return 0
    event = payload.get("hook_event_name", "")
    if event == "UserPromptSubmit":
        note = on_prompt(str(payload.get("prompt", "")), state_path(), now)
        if note:
            print(note)
        return 0
    if event == "PreToolUse":
        why = on_tool(str(payload.get("tool_name", "")), state_path(), now)
        if why:
            print(why, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
