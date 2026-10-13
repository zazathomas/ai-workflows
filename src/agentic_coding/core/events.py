from __future__ import annotations

from pathlib import Path

from agentic_coding.core.models import FSMEvent


def append_event(task_dir: Path, event: FSMEvent) -> None:
    path = task_dir / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(event.model_dump_json() + "\n")
