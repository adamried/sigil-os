#!/usr/bin/env python3
"""Deterministic helpers for the Sigil Codex plugin.

Exit codes:
  0 success
  1 validation failure
  2 usage error
  3 missing runtime dependency
  4 permission or authorization failure
  5 conflict or stale state
  6 remote/provider failure
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import difflib
import hashlib
import json
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


OK = 0
VALIDATION = 1
USAGE = 2
DEPENDENCY = 3
PERMISSION = 4
CONFLICT = 5
REMOTE = 6

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
STATE_MANIFEST = PLUGIN_ROOT / "references" / "state-files.json"
TEMPLATES = PLUGIN_ROOT / "skills" / "setup" / "references" / "templates"
START_MARKER = "<!-- SIGIL-CODEX-START v1 -->"
END_MARKER = "<!-- SIGIL-CODEX-END -->"
AGENTS_BLOCK = "\n".join(
    [
        START_MARKER,
        "When a request uses Sigil, read `.sigil/SIGIL.md` before acting.",
        "Use the installed Sigil public skill that matches the requested outcome.",
        "Sigil workflow pacing never changes Codex permissions or managed policy.",
        END_MARKER,
    ]
)
STATE_REQUIRED = {
    "sigil_state_version",
    "revision",
    "current_phase",
    "feature",
    "track",
    "artifact_root",
    "status",
    "pending_transition",
}
PHASES = {
    "none",
    "assess",
    "specify",
    "clarify",
    "design",
    "plan",
    "research",
    "decisions",
    "tasks",
    "implement",
    "validate",
    "code-review",
    "security-review",
    "handoff",
    "complete",
}
CONFIG_DEFAULTS: Dict[str, Any] = {
    "user_track": "non-technical",
    "execution_mode": "automatic",
    "audit_mode": False,
    "commits": "disabled",
    "global_config_opt_in": False,
}
CONFIG_ENUMS = {
    "user_track": {"non-technical", "technical"},
    "execution_mode": {"automatic", "directed", "autonomous"},
    "audit_mode": {True, False},
    "commits": {"enabled", "disabled"},
    "global_config_opt_in": {True, False},
}
SECRET_PATTERNS = [
    re.compile(r"(?i)(authorization\s*:\s*(?:bearer|basic)\s+)[^\s\"']+"),
    re.compile(r"(?i)((?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password)\s*[:=]\s*)[^\s,;\"']+"),
    re.compile(r"\b(?:gh[oprsu]_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})\b"),
    re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?"
        r"-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        re.DOTALL,
    ),
]
FORBIDDEN_CREDENTIAL_KEYS = {
    "apikey",
    "authorization",
    "clientsecret",
    "credential",
    "credentials",
    "password",
    "privatekey",
    "refreshtoken",
    "secret",
    "token",
}


class SigilError(Exception):
    def __init__(self, message: str, code: int = VALIDATION):
        super().__init__(message)
        self.code = code


def runtime_check() -> None:
    if sys.version_info < (3, 9):
        raise SigilError("Sigil requires Python 3.9 or newer.", DEPENDENCY)
    if platform.system() not in {"Darwin", "Linux"}:
        raise SigilError(
            "This Sigil preview supports macOS and Linux only.", DEPENDENCY
        )


def emit(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))


def run_command(
    args: Sequence[str], cwd: Optional[Path] = None
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            list(args),
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise SigilError(f"Unable to run required command: {args[0]}", DEPENDENCY) from exc


def resolve_root(raw_root: Optional[str], raw_cwd: Optional[str] = None) -> Path:
    candidate = Path(raw_root or raw_cwd or os.getcwd()).expanduser()
    try:
        candidate = candidate.resolve(strict=True)
    except OSError as exc:
        raise SigilError(f"Project directory does not exist: {candidate}") from exc
    if not candidate.is_dir():
        raise SigilError(f"Project root is not a directory: {candidate}")
    if raw_root:
        return candidate
    proc = run_command(["git", "rev-parse", "--show-toplevel"], candidate)
    if proc.returncode == 0 and proc.stdout.strip():
        return Path(proc.stdout.strip()).resolve(strict=True)
    raise SigilError(
        "This directory is not a Git repository. Confirm a project directory with --root.",
        USAGE,
    )


def path_within(root: Path, raw: str, *, allow_missing: bool = True) -> Path:
    candidate_input = Path(raw)
    if candidate_input.is_absolute():
        candidate = candidate_input
    else:
        candidate = root / candidate_input
    if "\x00" in str(candidate):
        raise SigilError("Path contains an invalid NUL byte.")
    # strict=False is intentional: setup must be able to validate a path before
    # creating its parent directories. Path.resolve still follows every existing
    # symlink component, so a missing descendant cannot hide an escape.
    candidate = candidate.resolve(strict=False)
    try:
        candidate.relative_to(root.resolve(strict=True))
    except ValueError as exc:
        raise SigilError(f"Path escapes the approved project root: {raw}") from exc
    if not allow_missing and not candidate.exists():
        raise SigilError(f"Required path does not exist: {raw}")
    return candidate


def atomic_write(path: Path, text: str, root: Path) -> None:
    path_within(root, str(path), allow_missing=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_symlink():
        raise SigilError(f"Refusing to replace symlink: {path}")
    temporary: Optional[Path] = None
    try:
        handle, raw_temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
        temporary = Path(raw_temp)
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(str(temporary), str(path))
        temporary = None
        if path.read_text(encoding="utf-8") != text:
            raise SigilError(f"Read-back verification failed for {path}")
    except PermissionError as exc:
        raise SigilError(f"Permission denied while writing {path}", PERMISSION) from exc
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def redact(text: str) -> str:
    result = text
    for index, pattern in enumerate(SECRET_PATTERNS):
        if index < 2:
            result = pattern.sub(r"\1[REDACTED]", result)
        else:
            result = pattern.sub("[REDACTED]", result)
    return result


def yaml_runtime():
    try:
        from ruamel.yaml import YAML  # type: ignore
    except ImportError as exc:
        raise SigilError(
            "Configuration commands require ruamel.yaml 0.18.x. "
            "Install it in the active Python environment.",
            DEPENDENCY,
        ) from exc
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    return yaml


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as stream:
            value = yaml_runtime().load(stream)
    except SigilError:
        raise
    except Exception as exc:
        raise SigilError(f"Invalid YAML in {path}: {exc}", CONFLICT) from exc
    return value or {}


def dump_yaml(path: Path, value: Any, root: Path) -> None:
    yaml = yaml_runtime()
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, raw_temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    os.close(handle)
    temporary = Path(raw_temp)
    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as stream:
            yaml.dump(value, stream)
            stream.flush()
            os.fsync(stream.fileno())
        text = temporary.read_text(encoding="utf-8")
        atomic_write(path, text, root)
    finally:
        if temporary.exists():
            temporary.unlink()


def parse_scalar(raw: str) -> Any:
    stripped = raw.strip()
    if stripped in {"null", "~"}:
        return None
    if stripped.lower() in {"true", "false"}:
        return stripped.lower() == "true"
    if re.fullmatch(r"-?\d+", stripped):
        return int(stripped)
    return stripped.strip("\"'")


def contains_credential_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = re.sub(r"[^a-z0-9]", "", str(key).lower())
            if normalized in FORBIDDEN_CREDENTIAL_KEYS:
                return True
            if contains_credential_key(child):
                return True
    elif isinstance(value, list):
        return any(contains_credential_key(item) for item in value)
    return False


def parse_state(text: str) -> Tuple[Dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise SigilError("State has no versioned frontmatter.", CONFLICT)
    end = text.find("\n---\n", 4)
    if end < 0:
        raise SigilError("State frontmatter is not closed.", CONFLICT)
    metadata: Dict[str, Any] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise SigilError(f"Invalid state frontmatter line: {line}", CONFLICT)
        key, raw_value = line.split(":", 1)
        metadata[key.strip()] = parse_scalar(raw_value)
    return metadata, text[end + 5 :]


def serialize_state(metadata: Dict[str, Any], body: str) -> str:
    ordered = [
        "sigil_state_version",
        "revision",
        "current_phase",
        "feature",
        "track",
        "artifact_root",
        "status",
        "pending_transition",
    ]
    lines = ["---"]
    for key in ordered:
        value = metadata[key]
        if value is None:
            rendered = "null"
        elif isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            rendered = str(value)
        lines.append(f"{key}: {rendered}")
    lines.extend(["---", body.lstrip("\n")])
    return "\n".join(lines).rstrip() + "\n"


def validate_state(metadata: Dict[str, Any]) -> List[str]:
    errors = []
    missing = sorted(STATE_REQUIRED - set(metadata))
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if metadata.get("sigil_state_version") != 1:
        errors.append("unsupported sigil_state_version")
    revision = metadata.get("revision")
    if not isinstance(revision, int) or revision < 0:
        errors.append("revision must be a non-negative integer")
    if metadata.get("current_phase") not in PHASES:
        errors.append("current_phase is invalid")
    if not isinstance(metadata.get("pending_transition"), bool):
        errors.append("pending_transition must be true or false")
    return errors


def read_manifest() -> Dict[str, Any]:
    try:
        return json.loads(STATE_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SigilError("Packaged state manifest is missing or invalid.", DEPENDENCY) from exc


def agents_block_text(action: str, current: str) -> str:
    start_count = current.count("<!-- SIGIL-CODEX-START")
    end_count = current.count(END_MARKER)
    if start_count != end_count or start_count > 1:
        raise SigilError(
            "AGENTS.md has duplicate or unbalanced Sigil markers; review it manually.",
            CONFLICT,
        )
    if start_count == 1 and START_MARKER not in current:
        raise SigilError(
            "AGENTS.md contains an unsupported Sigil marker version; review it manually.",
            CONFLICT,
        )
    if action == "remove":
        if start_count == 0:
            return current
        start = current.index(START_MARKER)
        end = current.index(END_MARKER, start) + len(END_MARKER)
        prefix, suffix = current[:start], current[end:]
        # Upsert owns one separator newline before and after its marker block.
        # Remove only those delimiters and preserve all user-authored content.
        if prefix.endswith("\n\n"):
            prefix = prefix[:-1]
        if suffix.startswith("\n"):
            suffix = suffix[1:]
        return prefix + suffix
    if start_count == 0:
        separator = "" if not current else ("\n" if current.endswith("\n") else "\n\n")
        return current + separator + AGENTS_BLOCK + "\n"
    start = current.index(START_MARKER)
    end = current.index(END_MARKER, start) + len(END_MARKER)
    return current[:start] + AGENTS_BLOCK + current[end:]


def config_path(root: Path) -> Path:
    return root / ".sigil" / "config.yaml"


def global_opted_in(project: Dict[str, Any]) -> bool:
    return project.get("global_config_opt_in") is True


def read_config_layers(root: Path) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    project = load_yaml(config_path(root))
    if not isinstance(project, dict):
        raise SigilError("Project config must contain a YAML mapping.", CONFLICT)
    global_layer: Dict[str, Any] = {}
    if global_opted_in(project):
        loaded = load_yaml(Path.home() / ".sigil" / "config.yaml")
        if not isinstance(loaded, dict):
            raise SigilError("Global config must contain a YAML mapping.", CONFLICT)
        global_layer = loaded
    return project, global_layer


def effective_config(root: Path) -> Dict[str, Dict[str, Any]]:
    project, global_layer = read_config_layers(root)
    keys = sorted(set(CONFIG_DEFAULTS) | set(global_layer) | set(project))
    result: Dict[str, Dict[str, Any]] = {}
    for key in keys:
        if key in project:
            result[key] = {"value": project[key], "source": "project"}
        elif key in global_layer:
            result[key] = {"value": global_layer[key], "source": "global"}
        elif key in CONFIG_DEFAULTS:
            result[key] = {"value": CONFIG_DEFAULTS[key], "source": "default"}
    return result


def validate_config_value(key: str, value: Any) -> None:
    allowed = CONFIG_ENUMS.get(key)
    if allowed is None:
        raise SigilError(f"Unknown setting: {key}", USAGE)
    if value not in allowed:
        values = ", ".join(sorted(str(item).lower() for item in allowed))
        raise SigilError(f"Invalid value for {key}; expected one of: {values}")


def gitignore_entries() -> List[str]:
    manifest = read_manifest()
    entries = []
    for item in manifest["files"]:
        if item["git"] == "ignore":
            entries.append(item["path"])
    entries.extend([".sigil/audit-log.md", ".sigil/audit-log.md.migrated"])
    if ".sigil/waivers.md" in entries:
        raise SigilError("State manifest must not ignore .sigil/waivers.md.")
    return entries


def merge_gitignore(current: str) -> str:
    additions = [entry for entry in gitignore_entries() if entry not in current.splitlines()]
    if not additions:
        return current
    separator = "" if not current else ("\n" if current.endswith("\n") else "\n\n")
    return current + separator + "# Sigil OS local state\n" + "\n".join(additions) + "\n"


def waiver_ignore_lines(current: str) -> List[str]:
    ignored = {".sigil/waivers.md", "/" + ".sigil/waivers.md"}
    return [
        line
        for line in current.splitlines()
        if line.strip() in ignored and not line.lstrip().startswith("#")
    ]


def remove_waiver_ignores(current: str) -> str:
    ignored = {".sigil/waivers.md", "/" + ".sigil/waivers.md"}
    lines = [
        line
        for line in current.splitlines()
        if line.strip() not in ignored or line.lstrip().startswith("#")
    ]
    if not current:
        return current
    return "\n".join(lines) + ("\n" if current.endswith("\n") else "")


def setup_plan(root: Path, generate_agents: bool) -> Dict[str, Any]:
    existing_sigil = (root / ".sigil").is_dir()
    candidates = [
        "AGENTS.md (Sigil marker block only)",
        ".gitignore (append missing local-state entries)",
        ".sigil/SIGIL.md",
        ".sigil/config.yaml",
        ".sigil/project-context.md",
        ".sigil/waivers.md",
        ".sigil/constitution.md",
    ]
    if generate_agents:
        candidates.append(".codex/agents/*.toml")
    actions = []
    for label in candidates:
        path_label = label.split(" ", 1)[0]
        path = root / path_label.replace("/*.toml", "")
        if label.startswith("AGENTS.md"):
            status = "merge marker block"
        elif label.startswith(".gitignore"):
            status = "merge ignore entries"
        elif path.exists():
            status = "preserve existing"
        else:
            status = "create missing"
        actions.append({"path": label, "action": status})
    legacy_waivers = root / "memory" / "waivers.md"
    current_waivers = root / ".sigil" / "waivers.md"
    if legacy_waivers.is_file() and not current_waivers.exists():
        actions.append(
            {
                "path": "memory/waivers.md",
                "action": (
                    "migrate to tracked .sigil/waivers.md and keep "
                    "memory/waivers.md.migrated as recovery"
                ),
            }
        )
    ignore_path = root / ".gitignore"
    ignore_text = ignore_path.read_text(encoding="utf-8") if ignore_path.exists() else ""
    ignored_waivers = waiver_ignore_lines(ignore_text)
    if ignored_waivers:
        actions.append(
            {
                "path": ".gitignore",
                "action": "remove waiver ignore entry: " + ", ".join(ignored_waivers),
            }
        )
    return {
        "mode": "migration-verification" if existing_sigil else "fresh",
        "root": str(root),
        "actions": actions,
        "requires_confirmation": True,
    }


def apply_setup(root: Path, generate_agents: bool) -> Dict[str, Any]:
    created: List[str] = []
    preserved: List[str] = []
    legacy_waivers = root / "memory" / "waivers.md"
    migrated_waivers = root / "memory" / "waivers.md.migrated"
    current_waivers = root / ".sigil" / "waivers.md"
    if legacy_waivers.is_file() and not current_waivers.exists():
        atomic_write(
            current_waivers,
            legacy_waivers.read_text(encoding="utf-8"),
            root,
        )
        if not migrated_waivers.exists():
            os.replace(str(legacy_waivers), str(migrated_waivers))
        created.append(".sigil/waivers.md (migrated from memory/waivers.md)")
    mapping = {
        root / ".sigil" / "SIGIL.md": TEMPLATES / "SIGIL.md",
        root / ".sigil" / "config.yaml": TEMPLATES / "config.yaml",
        root / ".sigil" / "project-context.md": TEMPLATES / "project-context.md",
        root / ".sigil" / "waivers.md": TEMPLATES / "waivers.md",
        root / ".sigil" / "constitution.md": TEMPLATES / "constitution.md",
    }
    for target, template in mapping.items():
        if target.exists():
            preserved.append(str(target.relative_to(root)))
            continue
        atomic_write(target, template.read_text(encoding="utf-8"), root)
        created.append(str(target.relative_to(root)))

    agents_path = root / "AGENTS.md"
    before = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    after = agents_block_text("upsert", before)
    if before != after:
        atomic_write(agents_path, after, root)
        created.append("AGENTS.md marker block")

    ignore_path = root / ".gitignore"
    ignore_before = ignore_path.read_text(encoding="utf-8") if ignore_path.exists() else ""
    ignore_after = merge_gitignore(remove_waiver_ignores(ignore_before))
    if ignore_before != ignore_after:
        atomic_write(ignore_path, ignore_after, root)
        created.append(".gitignore entries")

    for directory in (root / ".sigil" / "specs", root / ".sigil" / "learnings"):
        directory.mkdir(parents=True, exist_ok=True)
    if generate_agents:
        generate_agent_files(root)
        created.append(".codex/agents/*.toml")
    return {"created_or_updated": created, "preserved": preserved}


AGENT_SPECS = {
    "sigil_specification": (
        "Specification and clarification work using a parent-supplied Sigil role contract.",
        "read-only",
    ),
    "sigil_design": (
        "Read-focused UI, UX, and accessibility design using a parent-supplied Sigil role contract.",
        "read-only",
    ),
    "sigil_architecture": (
        "Architecture, research, and decision planning using a parent-supplied Sigil role contract.",
        "read-only",
    ),
    "sigil_task_planning": (
        "Task decomposition using a parent-supplied Sigil role contract.",
        "workspace-write",
    ),
    "sigil_implementation": (
        "Scoped implementation using a parent-supplied Sigil role contract.",
        "workspace-write",
    ),
    "sigil_validation": (
        "Validation and bounded fix analysis using a parent-supplied Sigil role contract.",
        "workspace-write",
    ),
    "sigil_code_review": (
        "Read-only correctness and regression review using a parent-supplied Sigil role contract.",
        "read-only",
    ),
    "sigil_security": (
        "Read-only security review using a parent-supplied Sigil role contract.",
        "read-only",
    ),
    "sigil_deployment_readiness": (
        "Read-only deployment readiness assessment using a parent-supplied Sigil role contract.",
        "read-only",
    ),
}


def generate_agent_files(root: Path) -> None:
    directory = root / ".codex" / "agents"
    directory.mkdir(parents=True, exist_ok=True)
    for name, (description, sandbox) in AGENT_SPECS.items():
        path = directory / f"{name}.toml"
        if path.exists():
            continue
        content = (
            f'name = "{name}"\n'
            f'description = "{description}"\n'
            f'sandbox_mode = "{sandbox}"\n'
            'developer_instructions = """\n'
            "Use only the role, overlay, repository root, file scope, and acceptance "
            "contract supplied by the parent. Do not infer hidden Sigil state and do "
            "not write .sigil/project-context.md. Return the requested structured "
            "handoff and evidence to the parent.\n"
            '"""\n'
        )
        atomic_write(path, content, root)


def toml_merge_agents(current: str) -> str:
    try:
        import tomllib  # type: ignore
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore
        except ImportError as exc:
            raise SigilError(
                "TOML validation requires Python 3.11+ or the tomli package.",
                DEPENDENCY,
            ) from exc
    try:
        tomllib.loads(current or "")
    except Exception as exc:
        raise SigilError(f"Existing config.toml is invalid: {exc}", CONFLICT) from exc
    if re.search(r"(?m)^\s*enabled\s*=", current) and "[agents]" in current:
        return current
    block = "[agents]\nenabled = true\n"
    if "[agents]" in current:
        position = current.index("[agents]") + len("[agents]")
        return current[:position] + "\nenabled = true" + current[position:]
    separator = "" if not current else ("\n" if current.endswith("\n") else "\n\n")
    return current + separator + block


def command_root(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-root")
    parser.add_argument("--root")
    parser.add_argument("--cwd")
    args = parser.parse_args(argv)
    emit({"root": str(resolve_root(args.root, args.cwd))})
    return OK


def command_config(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-config")
    parser.add_argument(
        "action", choices=["show", "set", "integration-show", "integration-set"]
    )
    parser.add_argument("key", nargs="?")
    parser.add_argument("value", nargs="?")
    parser.add_argument("--root", required=True)
    parser.add_argument("--global", dest="global_layer", action="store_true")
    parser.add_argument("--allow-outside-workspace", action="store_true")
    parser.add_argument("--mapping-file")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    if args.action == "show":
        emit({"effective": effective_config(root)})
        return OK
    if args.action == "integration-show":
        project, _ = read_config_layers(root)
        registry = project.get("integrations", {})
        if not isinstance(registry, dict):
            raise SigilError("Project integrations must contain a mapping.", CONFLICT)
        emit({"integrations": registry, "source": "project"})
        return OK
    if args.action == "integration-set":
        if args.global_layer:
            raise SigilError("Integration registry is project-scoped.", USAGE)
        if args.key not in {"jira", "figma", "shared_context"}:
            raise SigilError(
                "integration-set requires jira, figma, or shared_context", USAGE
            )
        if args.value is None:
            raise SigilError("integration-set requires true or false", USAGE)
        enabled = parse_scalar(args.value)
        if not isinstance(enabled, bool):
            raise SigilError("integration-set value must be true or false", USAGE)
        project, _ = read_config_layers(root)
        registry = project.setdefault("integrations", {})
        if not isinstance(registry, dict):
            raise SigilError("Project integrations must contain a mapping.", CONFLICT)
        entry = registry.setdefault(args.key, {})
        if not isinstance(entry, dict):
            raise SigilError(
                f"Integration {args.key} must contain a mapping.", CONFLICT
            )
        entry["enabled"] = enabled
        if args.mapping_file:
            mapping_path = path_within(root, args.mapping_file, allow_missing=False)
            try:
                mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise SigilError(
                    "Integration mapping file must be valid JSON.", CONFLICT
                ) from exc
            if not isinstance(mapping, dict):
                raise SigilError(
                    "Integration mapping file must contain an object.", CONFLICT
                )
            if contains_credential_key(mapping):
                raise SigilError(
                    "Integration mappings may not contain credentials.", PERMISSION
                )
            for mapping_key, mapping_value in mapping.items():
                entry[mapping_key] = mapping_value
        dump_yaml(config_path(root), project, root)
        emit({"integration": args.key, "enabled": enabled, "source": "project"})
        return OK
    if not args.key or args.value is None:
        raise SigilError("set requires a key and value", USAGE)
    value = parse_scalar(args.value)
    validate_config_value(args.key, value)
    project, _ = read_config_layers(root)
    target = config_path(root)
    allowed_root = root
    if args.global_layer:
        if not args.allow_outside_workspace or not global_opted_in(project):
            raise SigilError(
                "Global writes require recorded opt-in and --allow-outside-workspace.",
                PERMISSION,
            )
        target = Path.home() / ".sigil" / "config.yaml"
        allowed_root = Path.home() / ".sigil"
        allowed_root.mkdir(parents=True, exist_ok=True)
    layer = load_yaml(target)
    if not isinstance(layer, dict):
        raise SigilError("Config must contain a YAML mapping.", CONFLICT)
    layer[args.key] = value
    dump_yaml(target, layer, allowed_root)
    emit({"updated": args.key, "value": value, "layer": "global" if args.global_layer else "project"})
    return OK


def command_state(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-state")
    parser.add_argument("action", choices=["validate", "migrate", "transition"])
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--expected-revision", type=int)
    parser.add_argument("--phase")
    parser.add_argument("--artifact")
    parser.add_argument("--feature")
    parser.add_argument("--track")
    parser.add_argument("--status")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    path = root / ".sigil" / "project-context.md"
    if not path.exists():
        raise SigilError("No .sigil/project-context.md exists.", VALIDATION)
    original = path.read_text(encoding="utf-8")
    try:
        metadata, body = parse_state(original)
    except SigilError:
        if args.action != "migrate":
            raise
        template = (TEMPLATES / "project-context.md").read_text(encoding="utf-8")
        metadata, template_body = parse_state(template)
        legacy_phase = re.search(r"\*\*Current Phase:\*\*\s*([A-Za-z-]+)", original)
        legacy_feature = re.search(r"\*\*Feature:\*\*\s*(.+)", original)
        if legacy_phase and legacy_phase.group(1).lower() in PHASES:
            metadata["current_phase"] = legacy_phase.group(1).lower()
        if legacy_feature and legacy_feature.group(1).strip().lower() not in {"null", "none"}:
            metadata["feature"] = legacy_feature.group(1).strip()
        migrated = serialize_state(
            metadata,
            template_body
            + "\n## Preserved legacy state\n\n"
            + original.rstrip()
            + "\n",
        )
        diff = "".join(
            difflib.unified_diff(
                original.splitlines(True),
                migrated.splitlines(True),
                fromfile="project-context.md",
                tofile="project-context.md (v1)",
            )
        )
        if args.dry_run:
            print(diff, end="")
            return OK
        backup = path.with_suffix(path.suffix + ".pre-v1")
        if not backup.exists():
            atomic_write(backup, original, root)
        atomic_write(path, migrated, root)
        emit({"migrated": True, "backup": str(backup.relative_to(root))})
        return OK

    errors = validate_state(metadata)
    if args.action == "validate":
        emit({"valid": not errors, "errors": errors, "state": metadata})
        return OK if not errors else VALIDATION
    if args.action == "migrate":
        emit({"migrated": False, "reason": "already version 1"})
        return OK
    if errors:
        raise SigilError("State is invalid: " + "; ".join(errors))
    if args.expected_revision is None or args.phase is None or args.artifact is None:
        raise SigilError(
            "transition requires --expected-revision, --phase, and --artifact", USAGE
        )
    if metadata["revision"] != args.expected_revision:
        raise SigilError(
            f"Stale state revision: expected {args.expected_revision}, "
            f"current {metadata['revision']}",
            CONFLICT,
        )
    if args.phase not in PHASES:
        raise SigilError(f"Invalid phase: {args.phase}")
    artifact = path_within(root, args.artifact, allow_missing=False)
    if not artifact.is_file() or not artifact.read_text(encoding="utf-8").strip():
        raise SigilError("Transition artifact is empty or not a file.")
    metadata["revision"] += 1
    metadata["current_phase"] = args.phase
    metadata["pending_transition"] = False
    if args.feature is not None:
        metadata["feature"] = args.feature
    if args.track is not None:
        metadata["track"] = args.track
    if args.status is not None:
        metadata["status"] = args.status
    atomic_write(path, serialize_state(metadata, body), root)
    emit({"transitioned": True, "revision": metadata["revision"], "phase": args.phase})
    return OK


def command_agents_block(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-agents-block")
    parser.add_argument("action", choices=["upsert", "remove", "check"])
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    path = root / "AGENTS.md"
    before = path.read_text(encoding="utf-8") if path.exists() else ""
    after = agents_block_text("remove" if args.action == "remove" else "upsert", before)
    if args.action == "check":
        emit({"valid": before == after and START_MARKER in before})
        return OK if before == after and START_MARKER in before else VALIDATION
    if args.dry_run:
        print(
            "".join(
                difflib.unified_diff(
                    before.splitlines(True),
                    after.splitlines(True),
                    fromfile="AGENTS.md",
                    tofile="AGENTS.md (planned)",
                )
            ),
            end="",
        )
        return OK
    if before != after:
        atomic_write(path, after, root)
    emit({"changed": before != after, "action": args.action})
    return OK


def command_gitignore(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-gitignore")
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    path = root / ".gitignore"
    before = path.read_text(encoding="utf-8") if path.exists() else ""
    after = merge_gitignore(before)
    if args.dry_run:
        print(
            "".join(
                difflib.unified_diff(
                    before.splitlines(True), after.splitlines(True), "a/.gitignore", "b/.gitignore"
                )
            ),
            end="",
        )
    elif before != after:
        atomic_write(path, after, root)
    emit({"changed": before != after, "entries": gitignore_entries()})
    return OK


def command_audit_migrate(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-audit-migrate")
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    legacy = root / ".sigil" / "audit-log.md"
    migrated = root / ".sigil" / "audit-log.md.migrated"
    audit_dir = root / ".sigil" / "audit"
    if not legacy.exists() or migrated.exists() or audit_dir.exists():
        emit({"migrated": False, "reason": "no eligible legacy file"})
        return OK
    target_name = (
        dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
        + "_legacy-migration.md"
    )
    target = audit_dir / target_name
    plan = {
        "source": str(legacy.relative_to(root)),
        "target": str(target.relative_to(root)),
        "rename_source": str(migrated.relative_to(root)),
    }
    if args.dry_run:
        emit({"dry_run": True, "plan": plan})
        return OK
    audit_dir.mkdir(parents=True, exist_ok=False)
    text = (
        "# Migrated Sigil Audit Session\n\n"
        "> Imported from the legacy audit log without changing its content.\n\n"
        + legacy.read_text(encoding="utf-8")
    )
    atomic_write(target, text, root)
    os.replace(str(legacy), str(migrated))
    emit({"migrated": True, "plan": plan})
    return OK


def command_task_row(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-task-row")
    parser.add_argument("action", choices=["read", "set"])
    parser.add_argument("--root", required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--status", choices=[" ", "~", "x", "!"])
    parser.add_argument("--expected-status")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    path = path_within(root, args.file, allow_missing=False)
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"(?m)^(\s*-\s*\[)([ ~x!])(\]\s*\**{re.escape(args.task)}\b)")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise SigilError(f"Expected exactly one task row for {args.task}.", CONFLICT)
    current = matches[0].group(2)
    if args.action == "read":
        emit({"task": args.task, "status": current})
        return OK
    if args.status is None:
        raise SigilError("set requires --status", USAGE)
    if args.expected_status is not None and current != args.expected_status:
        raise SigilError("Task row changed since it was read.", CONFLICT)
    updated = pattern.sub(rf"\g<1>{args.status}\g<3>", text, count=1)
    if not args.dry_run:
        atomic_write(path, updated, root)
    emit({"task": args.task, "from": current, "to": args.status, "dry_run": args.dry_run})
    return OK


def command_manifest_check(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-manifest-check")
    parser.add_argument("--plugin-root", required=True)
    parser.add_argument("--marketplace", required=True)
    args = parser.parse_args(argv)
    plugin = Path(args.plugin_root).resolve(strict=True)
    marketplace_path = Path(args.marketplace).resolve(strict=True)
    manifest = json.loads(
        (plugin / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    entries = [item for item in marketplace.get("plugins", []) if item.get("name") == manifest.get("name")]
    errors = []
    if plugin.name != manifest.get("name"):
        errors.append("plugin directory and manifest name differ")
    if len(entries) != 1:
        errors.append("marketplace must contain exactly one matching entry")
    elif entries[0].get("source", {}).get("path") != "./plugins/sigil":
        errors.append("marketplace source path is not ./plugins/sigil")
    emit({"valid": not errors, "errors": errors})
    return OK if not errors else VALIDATION


def command_normalize(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-response-normalize")
    parser.add_argument("--kind", choices=["jira", "external-write"], required=True)
    args = parser.parse_args(argv)
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as exc:
        raise SigilError("stdin must contain one JSON object.", USAGE) from exc
    if not isinstance(payload, dict):
        raise SigilError("stdin must contain one JSON object.", USAGE)
    if args.kind == "external-write":
        outcome = payload.get("outcome")
        if outcome not in {"succeeded", "failed", "queued", "skipped"}:
            raise SigilError("external-write outcome is invalid")
        normalized = {
            "outcome": outcome,
            "reason": redact(str(payload.get("reason", ""))),
            "local_fallback": payload.get("local_fallback"),
        }
    else:
        fields = [
            "key",
            "summary",
            "description",
            "type",
            "status",
            "parent",
            "acceptance_criteria",
            "labels",
            "custom_fields",
            "source",
            "retrieved",
        ]
        normalized = {field: payload.get(field) for field in fields}
        normalized["description"] = redact(str(normalized.get("description") or ""))
    emit(normalized)
    return OK


def command_hook_json(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-hook-json")
    parser.add_argument("--event", required=True)
    parser.add_argument("--context")
    parser.add_argument("--system-message")
    parser.add_argument("--stop-reason")
    args = parser.parse_args(argv)
    payload: Dict[str, Any] = {}
    if args.system_message:
        payload["systemMessage"] = redact(args.system_message)
    if args.context:
        payload["hookSpecificOutput"] = {
            "hookEventName": args.event,
            "additionalContext": redact(args.context),
        }
    if args.stop_reason:
        if args.event != "Stop":
            raise SigilError("--stop-reason is valid only for Stop.", USAGE)
        payload["continue"] = False
        payload["stopReason"] = redact(args.stop_reason)
    emit(payload)
    return OK


def command_setup(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-setup")
    parser.add_argument("action", choices=["plan", "apply"])
    parser.add_argument("--root", required=True)
    parser.add_argument("--confirmed", action="store_true")
    parser.add_argument("--generate-agents", action="store_true")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    if args.action == "plan":
        emit(setup_plan(root, args.generate_agents))
        return OK
    if not args.confirmed:
        raise SigilError("Apply requires --confirmed after the plan is shown.", PERMISSION)
    emit(apply_setup(root, args.generate_agents))
    return OK


def command_agent_generate(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-agent-generate")
    parser.add_argument(
        "action", nargs="?", choices=["generate", "remove"], default="generate"
    )
    parser.add_argument("--root", required=True)
    parser.add_argument("--confirmed", action="store_true")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    if not args.confirmed:
        raise SigilError("Agent changes require --confirmed.", PERMISSION)
    if args.action == "remove":
        directory = root / ".codex" / "agents"
        recovery = directory / ".sigil-removed"
        moved = []
        for name in sorted(AGENT_SPECS):
            source = directory / f"{name}.toml"
            if not source.exists():
                continue
            recovery.mkdir(parents=True, exist_ok=True)
            target = recovery / source.name
            if target.exists():
                raise SigilError(
                    f"Recovery copy already exists for {source.name}; review manually.",
                    CONFLICT,
                )
            os.replace(str(source), str(target))
            moved.append(str(source.relative_to(root)))
        emit(
            {
                "removed_from_discovery": moved,
                "recovery_directory": str(recovery.relative_to(root)),
            }
        )
        return OK
    generate_agent_files(root)
    emit({"generated": sorted(AGENT_SPECS)})
    return OK


def command_config_toml(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-config-toml")
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    path = root / ".codex" / "config.toml"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    updated = toml_merge_agents(current)
    if args.dry_run:
        print(
            "".join(
                difflib.unified_diff(
                    current.splitlines(True), updated.splitlines(True), "config.toml", "config.toml (planned)"
                )
            ),
            end="",
        )
    elif current != updated:
        atomic_write(path, updated, root)
    emit({"changed": current != updated, "dry_run": args.dry_run})
    return OK


def integrity_errors(directory: Path, max_bytes: int) -> List[str]:
    if not directory.is_dir():
        raise SigilError("Integrity target must be a directory.")
    errors = []
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory).as_posix()
        if path.is_symlink():
            errors.append(f"{relative}: symlinks are not allowed")
            continue
        if path.is_file():
            mode = path.stat().st_mode
            if mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                errors.append(f"{relative}: executable content is not allowed")
            if path.stat().st_size > max_bytes:
                errors.append(f"{relative}: file exceeds {max_bytes} bytes")
    return errors


def command_integrity(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-integrity-check")
    parser.add_argument("--root", required=True)
    parser.add_argument("--directory", required=True)
    parser.add_argument("--max-bytes", type=int, default=1024 * 1024)
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    directory = path_within(root, args.directory, allow_missing=False)
    errors = integrity_errors(directory, args.max_bytes)
    emit({"valid": not errors, "errors": errors})
    return OK if not errors else VALIDATION


def command_redact(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-redact")
    parser.add_argument("--input")
    args = parser.parse_args(argv)
    text = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
    sys.stdout.write(redact(text))
    return OK


def queue_directory(root: Path) -> Path:
    return root / ".sigil" / "queue" / "shared-context"


def queue_remote_write(
    root: Path,
    repo: str,
    branch: str,
    target: str,
    content: str,
    expected_sha: str,
    reason: str,
) -> Path:
    scrubbed = redact(content)
    identity = hashlib.sha256(
        (repo + "\0" + branch + "\0" + target + "\0" + scrubbed).encode("utf-8")
    ).hexdigest()
    directory = queue_directory(root)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{identity}.json"
    payload = {
        "schema_version": 1,
        "id": identity,
        "operation": "put-content",
        "repo": repo,
        "branch": branch,
        "target": target,
        "content": scrubbed,
        "expected_sha": expected_sha,
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "reason": redact(reason),
    }
    atomic_write(path, json.dumps(payload, indent=2, sort_keys=True) + "\n", root)
    return path


def validate_remote_target(repo: str, branch: str, target: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise SigilError("--repo must be owner/name", USAGE)
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", branch) or ".." in branch:
        raise SigilError("--branch is invalid", USAGE)
    candidate = Path(target)
    if candidate.is_absolute() or ".." in candidate.parts or not target:
        raise SigilError("--target must be a repository-relative remote path", USAGE)


def require_gh(root: Path) -> None:
    if shutil.which("gh") is None:
        raise SigilError("Shared context requires the gh CLI.", DEPENDENCY)
    auth = run_command(["gh", "auth", "status"], root)
    if auth.returncode != 0:
        raise SigilError(
            "The gh CLI is installed but not authenticated. Run gh auth login.",
            PERMISSION,
        )


def gh_api(root: Path, arguments: Sequence[str]) -> subprocess.CompletedProcess:
    return run_command(["gh", "api"] + list(arguments), root)


def current_remote_sha(root: Path, repo: str, branch: str, target: str) -> Optional[str]:
    endpoint = (
        f"repos/{repo}/contents/{urllib.parse.quote(target, safe='/')}"
        f"?ref={urllib.parse.quote(branch, safe='')}"
    )
    response = gh_api(root, [endpoint, "--jq", ".sha"])
    if response.returncode == 0:
        value = response.stdout.strip()
        return value or None
    combined = (response.stdout + response.stderr).lower()
    if "not found" in combined or "http 404" in combined:
        return None
    raise SigilError("Unable to read the shared-context remote target.", REMOTE)


def git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def perform_remote_write(
    root: Path,
    repo: str,
    branch: str,
    target: str,
    content: str,
    expected_sha: str,
) -> Dict[str, Any]:
    require_gh(root)
    current = current_remote_sha(root, repo, branch, target)
    scrubbed = redact(content)
    blob_sha = git_blob_sha(scrubbed.encode("utf-8"))
    if current == blob_sha:
        return {"outcome": "succeeded", "reason": "content already present", "sha": current}
    expected = None if expected_sha == "none" else expected_sha
    if current != expected:
        raise SigilError(
            "Shared-context conflict: the remote target changed; nothing was overwritten.",
            CONFLICT,
        )
    endpoint = f"repos/{repo}/contents/{urllib.parse.quote(target, safe='/')}"
    fields = [
        endpoint,
        "--method",
        "PUT",
        "-f",
        f"message=sigil: update {target}",
        "-f",
        f"content={base64.b64encode(scrubbed.encode('utf-8')).decode('ascii')}",
        "-f",
        f"branch={branch}",
    ]
    if current:
        fields.extend(["-f", f"sha={current}"])
    response = gh_api(root, fields)
    if response.returncode != 0:
        raise SigilError("The shared-context remote write failed.", REMOTE)
    return {"outcome": "succeeded", "reason": "remote content updated"}


def command_shared_context(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-shared-context")
    parser.add_argument("action", choices=["check", "push", "replay"])
    parser.add_argument("--root", required=True)
    parser.add_argument("--repo")
    parser.add_argument("--branch")
    parser.add_argument("--target")
    parser.add_argument("--content-file")
    parser.add_argument("--expected-sha", default="none")
    parser.add_argument("--authorized", action="store_true")
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    if args.action == "check":
        require_gh(root)
        emit({"available": True, "authenticated": True})
        return OK
    if not args.authorized:
        emit(
            {
                "outcome": "skipped",
                "reason": "external write was not explicitly authorized",
            }
        )
        return PERMISSION
    if args.action == "push":
        if not all([args.repo, args.branch, args.target, args.content_file]):
            raise SigilError(
                "push requires --repo, --branch, --target, and --content-file", USAGE
            )
        validate_remote_target(args.repo, args.branch, args.target)
        content_path = path_within(root, args.content_file, allow_missing=False)
        content = content_path.read_text(encoding="utf-8")
        try:
            result = perform_remote_write(
                root,
                args.repo,
                args.branch,
                args.target,
                content,
                args.expected_sha,
            )
            emit(result)
            return OK
        except SigilError as exc:
            if exc.code == CONFLICT:
                raise
            queued = queue_remote_write(
                root,
                args.repo,
                args.branch,
                args.target,
                content,
                args.expected_sha,
                str(exc),
            )
            emit(
                {
                    "outcome": "queued",
                    "reason": "remote write failed after one attempt",
                    "queue_file": str(queued.relative_to(root)),
                }
            )
            return REMOTE

    directory = queue_directory(root)
    if not directory.exists():
        emit({"outcome": "succeeded", "replayed": 0})
        return OK
    replayed = 0
    for entry in sorted(directory.glob("*.json")):
        payload = json.loads(entry.read_text(encoding="utf-8"))
        validate_remote_target(payload["repo"], payload["branch"], payload["target"])
        result = perform_remote_write(
            root,
            payload["repo"],
            payload["branch"],
            payload["target"],
            payload["content"],
            payload["expected_sha"],
        )
        if result["outcome"] == "succeeded":
            entry.unlink()
            replayed += 1
    emit({"outcome": "succeeded", "replayed": replayed})
    return OK


def validate_design_source(url: str, revision: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise SigilError("Design-skill source URL must use HTTPS.", USAGE)
    if not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
        raise SigilError("Design-skill revision must be a full commit SHA.", USAGE)


def command_design_source(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="sigil-design-source")
    parser.add_argument("action", choices=["add", "propose-refresh", "apply-refresh"])
    parser.add_argument("--root", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--directory", required=True)
    parser.add_argument("--confirmed", action="store_true")
    parser.add_argument("--max-bytes", type=int, default=1024 * 1024)
    args = parser.parse_args(argv)
    root = resolve_root(args.root)
    validate_design_source(args.url, args.revision)
    source_dir = path_within(root, args.directory, allow_missing=False)
    if not source_dir.is_dir():
        raise SigilError("Staged design-skill source must be a directory.")
    errors = integrity_errors(source_dir, args.max_bytes)
    if errors:
        emit({"valid": False, "errors": errors})
        return VALIDATION
    manifest_path = root / ".sigil" / "design-skills" / ".manifest.json"
    existing: Dict[str, Any] = {"schema_version": 1, "sources": []}
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidate = {
        "url": args.url,
        "revision": args.revision.lower(),
        "directory": str(source_dir.relative_to(root)),
        "trust": "untrusted-advisory",
    }
    prior = next(
        (item for item in existing.get("sources", []) if item.get("url") == args.url),
        None,
    )
    if args.action == "propose-refresh":
        emit({"current": prior, "proposed": candidate, "requires_confirmation": True})
        return OK
    if not args.confirmed:
        raise SigilError(
            "Adding or refreshing an external design source requires --confirmed.",
            PERMISSION,
        )
    sources = [
        item for item in existing.get("sources", []) if item.get("url") != args.url
    ]
    sources.append(candidate)
    existing["sources"] = sorted(sources, key=lambda item: item["url"])
    atomic_write(
        manifest_path,
        json.dumps(existing, indent=2, sort_keys=True) + "\n",
        root,
    )
    emit({"recorded": candidate})
    return OK


COMMANDS = {
    "root": command_root,
    "config": command_config,
    "state": command_state,
    "agents-block": command_agents_block,
    "gitignore": command_gitignore,
    "audit-migrate": command_audit_migrate,
    "task-row": command_task_row,
    "manifest-check": command_manifest_check,
    "response-normalize": command_normalize,
    "hook-json": command_hook_json,
    "setup": command_setup,
    "agent-generate": command_agent_generate,
    "config-toml": command_config_toml,
    "integrity-check": command_integrity,
    "redact": command_redact,
    "shared-context": command_shared_context,
    "design-source": command_design_source,
}


def main(command: str, argv: Optional[Sequence[str]] = None) -> int:
    try:
        runtime_check()
        handler = COMMANDS[command]
        return handler(list(argv if argv is not None else sys.argv[1:]))
    except SigilError as exc:
        print(redact(str(exc)), file=sys.stderr)
        return exc.code
    except SystemExit as exc:
        return int(exc.code or 0)
    except Exception as exc:
        print(redact(f"Unexpected helper failure: {exc}"), file=sys.stderr)
        return VALIDATION
