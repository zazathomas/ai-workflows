from __future__ import annotations

import json

from conftest import current_task, invoke


def test_init_creates_files_and_json(runner, repo):
    result = invoke(
        runner,
        repo,
        ["init", "--goal", "Test task", "--acceptance", "Demo criterion", "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["ok"] is True
    assert payload["state"]["current_stage"] == "DISC-00"
    assert any("docs/temp-*" in warning for warning in payload["warnings"])

    task_id = current_task(repo)
    task_dir = repo / "docs" / task_id
    assert task_id.startswith("temp-")
    assert (task_dir / "state.json").exists()
    assert (task_dir / "events.jsonl").exists()
    assert (task_dir / "todos.md").exists()
    assert (task_dir / "checkpoint.md").exists()
    assert (task_dir / "context-capsule.md").exists()

    state = json.loads((task_dir / "state.json").read_text())
    assert state["acceptance_criteria"][0]["id"] == "AC-1"
    events = (task_dir / "events.jsonl").read_text().strip().splitlines()
    assert len(events) == 1
    assert json.loads(events[0])["type"] == "task_initialized"
