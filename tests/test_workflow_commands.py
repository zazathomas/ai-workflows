from __future__ import annotations

import json

from agentic_coding.cli import app


def test_workflow_list_and_show(runner):
    result = runner.invoke(app, ["workflow", "list", "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["workflows"][0]["id"] == "coding-v2"

    show = runner.invoke(app, ["workflow", "show", "coding-v2", "--json"])
    assert show.exit_code == 0, show.output
    data = json.loads(show.output)
    assert data["workflow"]["default_stage"] == "DISC-00"
