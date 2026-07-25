#!/usr/bin/env python3
"""Codex-native advisory hook implementations for Sigil."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_HELPER = PLUGIN_ROOT / "scripts" / "sigil-hook-json"
KNOWN_PHASES = {
    "specify": "sigil_specification",
    "clarify": "sigil_specification",
    "design": "sigil_design",
    "plan": "sigil_architecture",
    "research": "sigil_architecture",
    "decisions": "sigil_architecture",
    "tasks": "sigil_task_planning",
    "implement": "sigil_implementation",
    "validate": "sigil_validation",
    "code-review": "sigil_code_review",
    "security-review": "sigil_security",
    "handoff": "sigil_deployment_readiness",
}
PATCH_PATH = re.compile(
    r"^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$", re.MULTILINE
)
WATCHED = {
    "spec.md",
    "clarifications.md",
    "plan.md",
    "tasks.md",
    "project-context.md",
    "constitution.md",
    "security.md",
    "code-review.md",
}


def read_payload() -> Optional[Dict[str, Any]]:
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def project_root(payload: Dict[str, Any]) -> Optional[Path]:
    raw = payload.get("cwd")
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        root = Path(raw).expanduser().resolve(strict=True)
    except OSError:
        return None
    probe = root
    while probe != probe.parent:
        if (probe / ".git").exists():
            return probe
        probe = probe.parent
    return root


def output(
    event: str,
    *,
    context: Optional[str] = None,
    system_message: Optional[str] = None,
    stop_reason: Optional[str] = None,
) -> int:
    args = [str(OUTPUT_HELPER), "--event", event]
    if context:
        args.extend(["--context", context])
    if system_message:
        args.extend(["--system-message", system_message])
    if stop_reason:
        args.extend(["--stop-reason", stop_reason])
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode == 0 and result.stdout:
        sys.stdout.write(result.stdout)
    return 0


def parse_state(root: Path) -> Dict[str, str]:
    path = root / ".sigil" / "project-context.md"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def preflight(payload: Dict[str, Any], root: Path) -> int:
    dev_file = root / "CLAUDE.md"
    if dev_file.is_file() and "Sigil OS Development Environment" in dev_file.read_text(
        encoding="utf-8", errors="replace"
    ):
        return 0
    rules = root / ".sigil" / "SIGIL.md"
    agents = root / "AGENTS.md"
    if not (root / ".sigil").is_dir():
        return output(
            "SessionStart",
            context=(
                "Sigil is installed but this project is not configured. "
                "Use the setup skill if the user asks to use Sigil."
            ),
        )
    notices: List[str] = []
    if not rules.is_file():
        notices.append("Sigil rules are missing; use setup or update before workflow work.")
    elif "<!-- SIGIL-RULES format=1 " not in rules.read_text(
        encoding="utf-8", errors="replace"
    ):
        notices.append("Sigil rules use an unsupported format; use update.")
    if not agents.is_file() or "<!-- SIGIL-CODEX-START v1 -->" not in agents.read_text(
        encoding="utf-8", errors="replace"
    ):
        notices.append("The AGENTS.md Sigil marker block is missing; use setup.")
    if notices:
        return output("SessionStart", context=" ".join(notices))
    return output(
        "SessionStart",
        context=(
            "This is a configured Sigil project. When the request uses Sigil, "
            "read .sigil/SIGIL.md and validate resumable state before acting."
        ),
    )


def team_config(payload: Dict[str, Any], root: Path) -> int:
    path = root / ".sigil" / "team-config.yaml"
    if not path.is_file():
        return 0
    return output(
        "SessionStart",
        context=(
            "Sigil team configuration is present at .sigil/team-config.yaml. "
            "The coordinator should resolve it through project configuration; "
            "this hook did not modify any file."
        ),
    )


def design_context(payload: Dict[str, Any], root: Path) -> int:
    path = root / ".sigil" / "design.md"
    if not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    heading = next(
        (line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("#")),
        "Project design context",
    )
    version = "unknown"
    match = re.search(r"(?im)^(?:version|schema_version):\s*([^\s]+)", text)
    if match:
        version = match.group(1)
    return output(
        "SessionStart",
        context=(
            f"Sigil design context is available: {heading}; version {version}; "
            "path .sigil/design.md. Load it only for design-relevant work."
        ),
    )


def verify_context(payload: Dict[str, Any], root: Path) -> int:
    if payload.get("tool_name") != "apply_patch":
        return 0
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    command = tool_input.get("command")
    if not isinstance(command, str):
        return 0
    paths = PATCH_PATH.findall(command)
    watched_paths = set()
    for raw_path in paths:
        path = Path(raw_path)
        normalized_parts = tuple(part for part in path.parts if part not in {".", "/"})
        is_feature_artifact = len(normalized_parts) >= 2 and normalized_parts[:2] == (
            ".sigil",
            "specs",
        )
        if path.name in WATCHED or is_feature_artifact:
            watched_paths.add(raw_path)
    watched = sorted(watched_paths)
    if not watched or any(Path(path).name == "project-context.md" for path in watched):
        return 0
    if not (root / ".sigil" / "project-context.md").is_file():
        return 0
    return output(
        "PostToolUse",
        context=(
            "Sigil advisory: workflow artifacts changed ("
            + ", ".join(watched)
            + "). The root coordinator should validate whether durable state "
            "needs a confirmed transition. The hook did not infer or write state."
        ),
    )


def validate_routing(payload: Dict[str, Any], root: Path) -> int:
    agent = payload.get("agent_type")
    if not isinstance(agent, str) or not agent.startswith("sigil_"):
        return 0
    state = parse_state(root)
    expected = KNOWN_PHASES.get(state.get("current_phase", ""))
    if not expected or expected == agent:
        return 0
    message = (
        f"Sigil routing advisory: phase {state.get('current_phase')} normally "
        f"uses {expected}, but {agent} started. The parent should verify the "
        "delegation contract; the spawn is not blocked."
    )
    return output("SubagentStart", context=message, system_message=message)


def session_summary(payload: Dict[str, Any], root: Path) -> int:
    if payload.get("stop_hook_active") is True:
        return 0
    state = parse_state(root)
    if not state:
        return 0
    if state.get("pending_transition") == "true":
        return output(
            "Stop",
            stop_reason=(
                "A confirmed Sigil phase transition is still marked pending. "
                "Persist and verify project-context.md once, then allow stop."
            ),
        )
    return 0


HANDLERS = {
    "preflight": preflight,
    "team-config": team_config,
    "design-context": design_context,
    "verify-context": verify_context,
    "validate-routing": validate_routing,
    "session-summary": session_summary,
}


def main(name: str) -> int:
    payload = read_payload()
    if payload is None:
        return 0
    root = project_root(payload)
    if root is None:
        return 0
    try:
        return HANDLERS[name](payload, root)
    except Exception:
        return 0
