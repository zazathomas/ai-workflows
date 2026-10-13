from __future__ import annotations

import json

from conftest import invoke


def test_status_reads_current_pointer(runner, repo):
    init = invoke(runner, repo, ["init", "--goal", "Status task", "--acceptance", "Demo"])
    assert init.exit_code == 0, init.output
    result = invoke(runner, repo, ["status", "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["state"]["current_stage"] == "DISC-00"
    assert payload["state"]["workflow_id"] == "coding-v2"


def test_status_fails_without_current_task(runner, repo):
    result = invoke(runner, repo, ["status", "--json"])
    assert result.exit_code == 7
    payload = json.loads(result.stderr or result.output)
    assert payload["ok"] is False
    assert payload["errors"][0]["code"] == "task_not_found"
