from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


def utc_now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def slugify(text: str, max_len: int = 48) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return (slug[:max_len].strip("-") or "task")


def make_task_id(goal: str, root: Path) -> str:
    base = f"temp-{utc_now_compact()}-{slugify(goal)}"
    candidate = base
    counter = 2
    while (root / "docs" / candidate).exists():
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate


def current_pointer_path(root: Path) -> Path:
    return root / ".agentic" / "current"


def project_lock_path(root: Path) -> Path:
    return root / ".agentic" / "agentic.lock"


def task_dir_for(root: Path, task_id: str) -> Path:
    return root / "docs" / task_id


def resolve_task_id(root: Path, task_id: str | None) -> str:
    if task_id:
        return task_id
    pointer = current_pointer_path(root)
    if not pointer.exists():
        raise FileNotFoundError("no current task set; pass --task-id or run agentic init/use")
    value = pointer.read_text(encoding="utf-8").strip()
    if not value:
        raise FileNotFoundError("current task pointer is empty")
    return value
