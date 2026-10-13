from __future__ import annotations

import json

from conftest import current_task, invoke


def test_complete_advances_disc_to_scan(runner, repo):
    init = invoke(runner, repo, ["init", "--goal", "Complete task", "--acceptance", "Demo"])
    assert init.exit_code == 0, init.output
    result = invoke(
        runner,
        repo,
        ["complete", "--stage", "DISC-00", "--evidence", "Repo discovery completed", "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["state"]["current_stage"] == "SCAN-05"
    assert payload["state"]["transition"] == "DISC-00->SCAN-05"

    task_dir = repo / "docs" / current_task(repo)
    state = json.loads((task_dir / "state.json").read_text())
    assert state["completed_stages"] == ["DISC-00"]
    assert state["evidence"][0]["summary"] == "Repo discovery completed"
    assert (task_dir / "snapshots" / "DISC-00-summary.md").exists()
    events = [json.loads(line) for line in (task_dir / "events.jsonl").read_text().splitlines()]
    assert [event["type"] for event in events] == ["task_initialized", "stage_completed"]


def test_complete_requires_evidence(runner, repo):
    assert invoke(runner, repo, ["init", "--goal", "No evidence"]).exit_code == 0
    result = invoke(runner, repo, ["complete", "--stage", "DISC-00", "--json"])
    assert result.exit_code == 3


def test_complete_stage_assertion_must_match(runner, repo):
    assert invoke(runner, repo, ["init", "--goal", "Wrong stage"]).exit_code == 0
    result = invoke(
        runner,
        repo,
        ["complete", "--stage", "PLAN-20", "--evidence", "Nope", "--json"],
    )
    assert result.exit_code == 3
    payload = json.loads(result.stderr or result.output)
    assert "does not match" in payload["errors"][0]["message"]


def test_markdown_preserves_unmanaged_notes(runner, repo):
    assert invoke(runner, repo, ["init", "--goal", "Notes task"]).exit_code == 0
    task_dir = repo / "docs" / current_task(repo)
    checkpoint = task_dir / "checkpoint.md"
    checkpoint.write_text(checkpoint.read_text() + "Human note stays.\n", encoding="utf-8")
    assert invoke(runner, repo, ["complete", "--evidence", "Done"]).exit_code == 0
    assert "Human note stays." in checkpoint.read_text(encoding="utf-8")
