#!/usr/bin/env python3
"""Fuzzy-find skills and toggle Claude Code/Codex model invocation together."""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
# Skill folders live in their own subtree under the vault root; the generated
# human layer lives beside it. Keep in sync with build.py's SKILLS_SUBDIR.
SKILLS_SUBDIR = "skills"
# Generated wrapper notes, grouped by domain. Keep in sync with build.py.
NOTES_SUBDIR = "vault/notes"
CLAUDE_FIELD = "disable-model-invocation"
CODEX_FIELD = "allow_implicit_invocation"
SNAPSHOT_SCHEMA_VERSION = 1


class MetadataError(ValueError):
    """Raised when invocation metadata cannot be changed without guessing."""


class InvocationState(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    MIXED = "mixed"
    ERROR = "error"


@dataclass(frozen=True)
class Skill:
    key: str
    name: str
    description: str
    directory: Path
    claude_enabled: bool | None
    codex_enabled: bool | None
    error: str | None = None
    category: str = "uncategorized"

    @property
    def state(self) -> InvocationState:
        if self.error or self.claude_enabled is None or self.codex_enabled is None:
            return InvocationState.ERROR
        if self.claude_enabled and self.codex_enabled:
            return InvocationState.ENABLED
        if not self.claude_enabled and not self.codex_enabled:
            return InvocationState.DISABLED
        return InvocationState.MIXED


def _frontmatter_lines(text: str, path: Path) -> tuple[list[str], int]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise MetadataError(f"{path}: SKILL.md has no YAML frontmatter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines, index
    raise MetadataError(f"{path}: SKILL.md frontmatter is not closed")


def _decode_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return str(json.loads(value))
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        try:
            return str(ast.literal_eval(value))
        except (SyntaxError, ValueError):
            return value[1:-1].replace("''", "'")
    return value


def _frontmatter_scalar(lines: Sequence[str], closing_index: int, key: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:[ \t]*(.*?)[ \t]*(?:\r?\n)?$")
    for index in range(1, closing_index):
        match = pattern.match(lines[index])
        if not match:
            continue
        value = match.group(1).strip()
        if value not in {">", ">-", ">+", "|", "|-", "|+"}:
            return _decode_scalar(value)
        parts: list[str] = []
        for continuation in lines[index + 1 : closing_index]:
            if continuation.startswith((" ", "\t")):
                parts.append(continuation.strip())
            else:
                break
        return " ".join(part for part in parts if part)
    return ""


def _read_boolean_field(
    text: str,
    field: str,
    *,
    default: bool,
    path: Path,
    top_level: bool,
) -> bool:
    indentation = "" if top_level else r"[ \t]+"
    valid = re.compile(
        rf"(?m)^{indentation}{re.escape(field)}:[ \t]*(true|false)"
        rf"[ \t]*(?:#.*)?$"
    )
    values = valid.findall(text)
    any_field = re.findall(rf"(?m)^[ \t]*{re.escape(field)}:[^\n]*$", text)
    if len(any_field) > 1 or len(values) > 1:
        raise MetadataError(f"{path}: duplicate {field} fields")
    if any_field and not values:
        raise MetadataError(f"{path}: {field} must be true or false")
    return default if not values else values[0] == "true"


def load_skill(directory: Path, *, category: str = "uncategorized") -> Skill:
    directory = Path(directory)
    skill_path = directory / "SKILL.md"
    try:
        skill_text = skill_path.read_text(encoding="utf-8")
        lines, closing_index = _frontmatter_lines(skill_text, skill_path)
        name = _frontmatter_scalar(lines, closing_index, "name") or directory.name
        description = _frontmatter_scalar(lines, closing_index, "description")
        claude_disabled = _read_boolean_field(
            "".join(lines[1:closing_index]),
            CLAUDE_FIELD,
            default=False,
            path=skill_path,
            top_level=True,
        )
        openai_path = directory / "agents" / "openai.yaml"
        if openai_path.exists():
            openai_text = openai_path.read_text(encoding="utf-8")
            codex_enabled = _read_boolean_field(
                openai_text,
                CODEX_FIELD,
                default=True,
                path=openai_path,
                top_level=False,
            )
        else:
            codex_enabled = True
        return Skill(
            key=directory.name,
            name=name,
            description=" ".join(description.split()),
            directory=directory,
            claude_enabled=not claude_disabled,
            codex_enabled=codex_enabled,
            category=category,
        )
    except (MetadataError, OSError, UnicodeError) as exc:
        return Skill(
            key=directory.name,
            name=directory.name,
            description="",
            directory=directory,
            claude_enabled=None,
            codex_enabled=None,
            error=str(exc),
            category=category,
        )


def _wrapper_categories(root: Path) -> dict[str, str]:
    """Map skill key -> domain.

    Wrapper notes live at vault/notes/<domain>/<skill>.md, so the domain is the
    folder name -- no frontmatter parsing, and one directory scan instead of one
    file read per skill.
    """
    categories: dict[str, str] = {}
    notes = root / NOTES_SUBDIR
    if not notes.is_dir():
        return categories
    for domain_directory in notes.iterdir():
        if not domain_directory.is_dir():
            continue
        for note in domain_directory.glob("*.md"):
            categories[note.stem] = domain_directory.name
    return categories


def discover_skills(root: Path) -> list[Skill]:
    root = Path(root).resolve()
    skills_root = root / SKILLS_SUBDIR
    if not skills_root.is_dir():
        raise MetadataError(
            f"{skills_root}: no skills directory under the vault root. "
            f"Pass --root pointing at the vault (the parent of {SKILLS_SUBDIR}/)."
        )
    categories = _wrapper_categories(root)
    skills: list[Skill] = []
    for directory in skills_root.iterdir():
        if (
            directory.name.startswith(".")
            or directory.name.startswith("gstack-")
            or directory.name.startswith("_gstack")
            or not (directory / "SKILL.md").is_file()
        ):
            continue
        try:
            directory.resolve().relative_to(skills_root)
        except (OSError, ValueError):
            continue
        skills.append(
            load_skill(
                directory,
                category=categories.get(directory.name, "uncategorized"),
            )
        )
    return sorted(
        skills, key=lambda skill: (skill.name.casefold(), skill.key.casefold())
    )


def _replace_boolean_line(
    line: str, field: str, value: bool, *, top_level: bool
) -> str | None:
    indentation = "" if top_level else r"[ \t]+"
    pattern = re.compile(
        rf"^({indentation}{re.escape(field)}:[ \t]*)(?:true|false)"
        rf"([ \t]*(?:#.*)?)(\r?\n)?$"
    )
    match = pattern.match(line)
    if not match:
        return None
    newline = match.group(3) or ""
    boolean = "true" if value else "false"
    return f"{match.group(1)}{boolean}{match.group(2)}{newline}"


def _transform_skill_md_field(text: str, path: Path, *, disabled: bool | None) -> str:
    lines, closing_index = _frontmatter_lines(text, path)
    matches = [
        index
        for index in range(1, closing_index)
        if re.match(rf"^{re.escape(CLAUDE_FIELD)}:", lines[index])
    ]
    if len(matches) > 1:
        raise MetadataError(f"{path}: duplicate {CLAUDE_FIELD} fields")
    if matches:
        index = matches[0]
        if disabled is None:
            lines.pop(index)
            return "".join(lines)
        replacement = _replace_boolean_line(
            lines[index], CLAUDE_FIELD, disabled, top_level=True
        )
        if replacement is None:
            raise MetadataError(f"{path}: {CLAUDE_FIELD} must be true or false")
        lines[index] = replacement
    elif disabled is not None:
        newline = "\r\n" if lines[0].endswith("\r\n") else "\n"
        lines.insert(
            closing_index,
            f"{CLAUDE_FIELD}: {'true' if disabled else 'false'}{newline}",
        )
    return "".join(lines)


def _transform_skill_md(text: str, path: Path, *, enabled: bool) -> str:
    return _transform_skill_md_field(text, path, disabled=not enabled)


def _default_openai_yaml(skill: Skill, *, enabled: bool) -> str:
    display_name = skill.key.replace("-", " ").title()
    return (
        "interface:\n"
        f"  display_name: {json.dumps(display_name)}\n"
        '  short_description: "Invoke this skill explicitly when needed."\n'
        f"  default_prompt: {json.dumps(f'Use ${skill.key} for this task.')}\n"
        "\n"
        "policy:\n"
        f"  {CODEX_FIELD}: {'true' if enabled else 'false'}\n"
    )


def _transform_openai_yaml_field(text: str, path: Path, *, enabled: bool | None) -> str:
    lines = text.splitlines(keepends=True)
    field_matches = [
        index
        for index, line in enumerate(lines)
        if re.match(rf"^[ \t]+{re.escape(CODEX_FIELD)}:", line)
    ]
    if len(field_matches) > 1:
        raise MetadataError(f"{path}: duplicate {CODEX_FIELD} fields")
    if field_matches:
        index = field_matches[0]
        if enabled is None:
            lines.pop(index)
            policy_matches = [
                policy_index
                for policy_index, line in enumerate(lines)
                if re.match(r"^policy:[ \t]*(?:#.*)?(?:\r?\n)?$", line)
            ]
            if len(policy_matches) == 1:
                policy_index = policy_matches[0]
                block_end = len(lines)
                for candidate in range(policy_index + 1, len(lines)):
                    line = lines[candidate]
                    if line.strip() and not line.startswith((" ", "\t")):
                        block_end = candidate
                        break
                meaningful = [
                    line
                    for line in lines[policy_index + 1 : block_end]
                    if line.strip() and not line.lstrip().startswith("#")
                ]
                if not meaningful:
                    lines.pop(policy_index)
                    # Adding a new policy block also adds one blank separator.
                    # Remove exactly that separator when the block becomes
                    # empty, while preserving any older trailing blank lines.
                    if policy_index > 0 and not lines[policy_index - 1].strip():
                        lines.pop(policy_index - 1)
            return "".join(lines)
        replacement = _replace_boolean_line(
            lines[index], CODEX_FIELD, enabled, top_level=False
        )
        if replacement is None:
            raise MetadataError(f"{path}: {CODEX_FIELD} must be true or false")
        lines[index] = replacement
        return "".join(lines)

    if enabled is None:
        return text

    policy_matches = [
        index
        for index, line in enumerate(lines)
        if re.match(r"^policy:[ \t]*(?:#.*)?(?:\r?\n)?$", line)
    ]
    if len(policy_matches) > 1:
        raise MetadataError(f"{path}: duplicate policy blocks")
    if policy_matches:
        index = policy_matches[0]
        newline = "\r\n" if lines[index].endswith("\r\n") else "\n"
        lines.insert(
            index + 1,
            f"  {CODEX_FIELD}: {'true' if enabled else 'false'}{newline}",
        )
        return "".join(lines)

    if re.search(r"(?m)^policy:[^\n]+$", text):
        raise MetadataError(f"{path}: inline policy mappings are not supported")
    suffix = "" if not text or text.endswith(("\n", "\r")) else "\n"
    separator = "" if not text.strip() else "\n"
    return (
        text
        + suffix
        + separator
        + "policy:\n"
        + f"  {CODEX_FIELD}: {'true' if enabled else 'false'}\n"
    )


def _transform_openai_yaml(text: str, path: Path, *, enabled: bool) -> str:
    return _transform_openai_yaml_field(text, path, enabled=enabled)


def _atomic_write(path: Path, text: str, mode: int | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        if mode is not None:
            os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def set_skill_product_states(
    skill: Skill,
    *,
    claude_enabled: bool | None = None,
    codex_enabled: bool | None = None,
) -> Skill:
    if skill.error:
        raise MetadataError(skill.error)
    if claude_enabled is None and codex_enabled is None:
        return skill

    skill_path = skill.directory / "SKILL.md"
    openai_path = skill.directory / "agents" / "openai.yaml"
    skill_original = (
        skill_path.read_text(encoding="utf-8") if claude_enabled is not None else None
    )
    openai_original = (
        openai_path.read_text(encoding="utf-8")
        if codex_enabled is not None and openai_path.exists()
        else None
    )
    operations: list[tuple[Path, str | None, str, int | None]] = []
    if claude_enabled is not None and skill_original is not None:
        skill_updated = _transform_skill_md(
            skill_original, skill_path, enabled=claude_enabled
        )
        if skill_updated != skill_original:
            operations.append(
                (skill_path, skill_original, skill_updated, skill_path.stat().st_mode)
            )
    if codex_enabled is not None:
        openai_updated = (
            _transform_openai_yaml(openai_original, openai_path, enabled=codex_enabled)
            if openai_original is not None
            else _default_openai_yaml(skill, enabled=codex_enabled)
        )
        if openai_updated != openai_original:
            operations.append(
                (
                    openai_path,
                    openai_original,
                    openai_updated,
                    openai_path.stat().st_mode if openai_path.exists() else None,
                )
            )

    completed: list[tuple[Path, str | None, int | None]] = []
    try:
        for path, original, updated, mode in operations:
            _atomic_write(path, updated, mode)
            completed.append((path, original, mode))
    except Exception:
        for path, original, mode in reversed(completed):
            if original is None:
                path.unlink(missing_ok=True)
                try:
                    path.parent.rmdir()
                except OSError:
                    pass
            else:
                _atomic_write(path, original, mode)
        raise
    return load_skill(skill.directory, category=skill.category)


def set_skill_enabled(skill: Skill, *, enabled: bool) -> Skill:
    return set_skill_product_states(
        skill,
        claude_enabled=enabled,
        codex_enabled=enabled,
    )


def toggle_skill(skill: Skill) -> Skill:
    return set_skill_enabled(
        skill,
        enabled=skill.state != InvocationState.ENABLED,
    )


def _snapshot_path(root: Path, path: Path | None = None) -> Path:
    if path is None:
        return root / ".skill-vault" / "skill-toggle-state.json"
    return path if path.is_absolute() else Path.cwd() / path


def _snapshot_payload(root: Path, skills: Sequence[Skill]) -> dict[str, object]:
    return {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "saved_at": dt.datetime.now(dt.UTC).isoformat(),
        "root": str(root),
        "skills": {
            skill.key: {
                "claude_enabled": skill.claude_enabled,
                "codex_enabled": skill.codex_enabled,
            }
            for skill in skills
            if skill.error is None
        },
    }


def save_snapshot(root: Path, path: Path | None = None) -> Path:
    root = root.resolve()
    destination = _snapshot_path(root, path)
    payload = _snapshot_payload(root, discover_skills(root))
    _atomic_write(destination, json.dumps(payload, indent=2) + "\n", None)
    return destination


def _restore_original_files(
    originals: dict[Path, tuple[str | None, int | None]],
) -> None:
    for path, (text, mode) in reversed(originals.items()):
        if text is None:
            path.unlink(missing_ok=True)
            try:
                path.parent.rmdir()
            except OSError:
                pass
        else:
            _atomic_write(path, text, mode)


def load_snapshot(root: Path, path: Path | None = None) -> tuple[Path, int]:
    root = root.resolve()
    source = _snapshot_path(root, path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise MetadataError(f"cannot read snapshot {source}: {exc}") from exc
    if payload.get("schema_version") != SNAPSHOT_SCHEMA_VERSION:
        raise MetadataError(f"{source}: unsupported snapshot schema")
    states = payload.get("skills")
    if not isinstance(states, dict):
        raise MetadataError(f"{source}: skills must be an object")

    skills = {skill.key: skill for skill in discover_skills(root)}
    originals: dict[Path, tuple[str | None, int | None]] = {}
    changed = 0
    try:
        for key, state in states.items():
            skill = skills.get(key)
            if skill is None or not isinstance(state, dict):
                continue
            claude = state.get("claude_enabled")
            codex = state.get("codex_enabled")
            if not isinstance(claude, bool) or not isinstance(codex, bool):
                raise MetadataError(f"{source}: invalid state for {key}")
            skill_path = skill.directory / "SKILL.md"
            openai_path = skill.directory / "agents" / "openai.yaml"
            for candidate in (skill_path, openai_path):
                if candidate not in originals:
                    originals[candidate] = (
                        candidate.read_text(encoding="utf-8")
                        if candidate.exists()
                        else None,
                        candidate.stat().st_mode if candidate.exists() else None,
                    )
            if skill.claude_enabled != claude or skill.codex_enabled != codex:
                set_skill_product_states(
                    skill,
                    claude_enabled=claude,
                    codex_enabled=codex,
                )
                changed += 1
    except Exception:
        _restore_original_files(originals)
        raise
    return source, changed


def _git_head_texts(root: Path, paths: Sequence[Path]) -> dict[Path, str | None]:
    relative_paths = [path.relative_to(root).as_posix() for path in paths]
    process = subprocess.Popen(
        ["git", "-C", str(root), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    assert process.stderr is not None
    results: dict[Path, str | None] = {}
    error_output = b""
    try:
        for path, relative in zip(paths, relative_paths, strict=True):
            process.stdin.write(f"HEAD:{relative}\n".encode())
            process.stdin.flush()
            header = process.stdout.readline().decode("utf-8", errors="replace").strip()
            if header.endswith(" missing"):
                results[path] = None
                continue
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise MetadataError(f"git cat-file returned: {header}")
            size = int(parts[2])
            data = process.stdout.read(size)
            process.stdout.read(1)
            results[path] = data.decode("utf-8")
    finally:
        process.stdin.close()
        process.wait()
        error_output = process.stderr.read()
        process.stdout.close()
        process.stderr.close()
    if process.returncode != 0:
        error = error_output.decode("utf-8", errors="replace").strip()
        raise MetadataError(error or "could not read Git HEAD")
    return results


def _matches_generated_openai_yaml(skill: Skill, text: str) -> bool:
    return text in {
        _default_openai_yaml(skill, enabled=True),
        _default_openai_yaml(skill, enabled=False),
    }


def pre_commit_reset(root: Path, snapshot_path: Path | None = None) -> tuple[Path, int]:
    """Save the current invocation states, then activate every skill.

    Committed skills are model-invocable by default, so the reset drops the two
    opt-out fields instead of restoring them: `SKILL.md` loses
    `disable-model-invocation` and `agents/openai.yaml` loses
    `policy.allow_implicit_invocation`, which both products read as enabled. An
    `agents/openai.yaml` this tool generated for a skill that has none in Git
    HEAD is removed outright, since a missing file also means enabled. Personal
    opt-outs live on in the snapshot, so `load` restores them after committing.
    Unrelated working edits are left untouched.
    """
    root = root.resolve()
    snapshot = save_snapshot(root, snapshot_path)
    skills = discover_skills(root)
    openai_paths = [skill.directory / "agents" / "openai.yaml" for skill in skills]
    head = _git_head_texts(root, openai_paths)
    operations: list[tuple[Path, str | None, str | None, int | None]] = []

    for skill in skills:
        skill_path = skill.directory / "SKILL.md"
        openai_path = skill.directory / "agents" / "openai.yaml"
        current_skill = skill_path.read_text(encoding="utf-8")
        updated_skill = _transform_skill_md_field(
            current_skill,
            skill_path,
            disabled=None,
        )
        if updated_skill != current_skill:
            operations.append(
                (
                    skill_path,
                    current_skill,
                    updated_skill,
                    skill_path.stat().st_mode,
                )
            )

        if not openai_path.exists():
            continue
        current_openai = openai_path.read_text(encoding="utf-8")
        if head[openai_path] is None and _matches_generated_openai_yaml(
            skill, current_openai
        ):
            updated_openai = None
        else:
            updated_openai = _transform_openai_yaml_field(
                current_openai,
                openai_path,
                enabled=None,
            )
        if updated_openai != current_openai:
            operations.append(
                (
                    openai_path,
                    current_openai,
                    updated_openai,
                    openai_path.stat().st_mode,
                )
            )

    completed: dict[Path, tuple[str | None, int | None]] = {}
    try:
        for path, original, updated, mode in operations:
            completed[path] = (original, mode)
            if updated is None:
                path.unlink(missing_ok=True)
                try:
                    path.parent.rmdir()
                except OSError:
                    pass
            else:
                _atomic_write(path, updated, mode)
    except Exception:
        _restore_original_files(completed)
        raise
    return snapshot, len(operations)


def _resolve_skills(root: Path, requested: Iterable[str]) -> list[Skill]:
    skills = discover_skills(root)
    by_key = {skill.key: skill for skill in skills}
    by_name: dict[str, list[Skill]] = {}
    for skill in skills:
        by_name.setdefault(skill.name, []).append(skill)
    resolved: list[Skill] = []
    for value in requested:
        if value in by_key:
            resolved.append(by_key[value])
            continue
        matches = by_name.get(value, [])
        if len(matches) == 1:
            resolved.append(matches[0])
            continue
        if len(matches) > 1:
            keys = ", ".join(skill.key for skill in matches)
            raise MetadataError(f"ambiguous skill name {value!r}; use one of: {keys}")
        raise MetadataError(f"unknown skill: {value}")
    return resolved


def _clean_cell(value: str) -> str:
    return " ".join(value.replace("\t", " ").split())


def _print_preview(skill: Skill) -> None:
    print(f"{skill.name}  [{skill.state.value}]")
    print(f"Directory: {skill.directory}")
    print(f"Category: {skill.category}")
    print(
        "Claude Code: " + ("enabled" if skill.claude_enabled else "disabled")
        if skill.claude_enabled is not None
        else "Claude Code: metadata error"
    )
    print(
        "Codex: " + ("enabled" if skill.codex_enabled else "disabled")
        if skill.codex_enabled is not None
        else "Codex: metadata error"
    )
    if skill.description:
        print(f"\n{skill.description}")
    if skill.error:
        print(f"\nError: {skill.error}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fuzzy-find skills and toggle Claude Code/Codex invocation."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"skill vault root (default: {DEFAULT_ROOT})",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="list skills and invocation states")
    subparsers.add_parser("catalog", help="print the skill catalog as JSON")
    preview = subparsers.add_parser("preview", help="show one skill's invocation state")
    preview.add_argument("skill")
    for action in ("enable", "disable", "toggle"):
        action_parser = subparsers.add_parser(action, help=f"{action} named skills")
        action_parser.add_argument(
            "--product",
            choices=("both", "claude", "codex"),
            default="both",
            help="product to change (default: both)",
        )
        action_parser.add_argument("skills", nargs="+")
    save = subparsers.add_parser("save", help="save all invocation states")
    save.add_argument("path", nargs="?", type=Path)
    load = subparsers.add_parser("load", help="reload saved invocation states")
    load.add_argument("path", nargs="?", type=Path)
    reset = subparsers.add_parser(
        "pre-commit-reset",
        help="save current states and activate every skill for both products",
    )
    reset.add_argument("--snapshot", type=Path)
    return parser


def _skill_json(skill: Skill) -> dict[str, object]:
    return {
        "key": skill.key,
        "name": skill.name,
        "description": skill.description,
        "directory": str(skill.directory),
        "category": skill.category,
        "claude_enabled": skill.claude_enabled,
        "codex_enabled": skill.codex_enabled,
        "state": skill.state.value,
        "error": skill.error,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command is None:
            parser.print_help()
            return 0
        if args.command == "list":
            for skill in discover_skills(root):
                print(
                    f"{skill.state.value}\t{skill.key}\t{skill.category}\t"
                    f"{_clean_cell(skill.description)}"
                )
            return 0
        if args.command == "catalog":
            skills = discover_skills(root)
            print(
                json.dumps(
                    {
                        "skills": [_skill_json(skill) for skill in skills],
                        "categories": sorted(
                            {skill.category for skill in skills}, key=str.casefold
                        ),
                    }
                )
            )
            return 0
        if args.command == "preview":
            _print_preview(_resolve_skills(root, [args.skill])[0])
            return 0
        if args.command == "save":
            destination = save_snapshot(root, args.path)
            print(f"saved\t{destination}")
            return 0
        if args.command == "load":
            source, changed = load_snapshot(root, args.path)
            print(f"loaded\t{changed}\t{source}")
            return 0
        if args.command == "pre-commit-reset":
            snapshot, changed = pre_commit_reset(root, args.snapshot)
            print(f"reset\t{changed}\t{snapshot}")
            return 0
        for skill in _resolve_skills(root, args.skills):
            product = args.product
            if args.command == "enable":
                if product == "both":
                    changed = set_skill_enabled(skill, enabled=True)
                else:
                    changed = set_skill_product_states(
                        skill,
                        claude_enabled=True if product == "claude" else None,
                        codex_enabled=True if product == "codex" else None,
                    )
            elif args.command == "disable":
                if product == "both":
                    changed = set_skill_enabled(skill, enabled=False)
                else:
                    changed = set_skill_product_states(
                        skill,
                        claude_enabled=False if product == "claude" else None,
                        codex_enabled=False if product == "codex" else None,
                    )
            else:
                if product == "both":
                    changed = toggle_skill(skill)
                elif product == "claude":
                    if skill.claude_enabled is None:
                        raise MetadataError(f"{skill.key}: Claude metadata error")
                    changed = set_skill_product_states(
                        skill, claude_enabled=not skill.claude_enabled
                    )
                else:
                    if skill.codex_enabled is None:
                        raise MetadataError(f"{skill.key}: Codex metadata error")
                    changed = set_skill_product_states(
                        skill, codex_enabled=not skill.codex_enabled
                    )
            print(f"{changed.state.value}\t{changed.key}")
        return 0
    except (MetadataError, OSError) as exc:
        print(f"skill-toggle: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
