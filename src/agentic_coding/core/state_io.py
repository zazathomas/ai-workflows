from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from agentic_coding.core.models import TaskState


def state_path(task_dir: Path) -> Path:
    return task_dir / "state.json"


def read_state(task_dir: Path) -> TaskState:
    path = state_path(task_dir)
    if not path.exists():
        raise FileNotFoundError(f"state not found: {path}")
    return TaskState.model_validate_json(path.read_text(encoding="utf-8"))


def write_state_atomic(state: TaskState) -> None:
    state.updated_at = datetime.now(timezone.utc)
    task_dir = Path(state.task_dir)
    task_dir.mkdir(parents=True, exist_ok=True)
    path = state_path(task_dir)
    tmp = task_dir / ".state.json.tmp"
    data = json.dumps(state.model_dump(mode="json"), indent=2, sort_keys=True) + "\n"
    with tmp.open("w", encoding="utf-8") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
