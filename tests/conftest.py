from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from agentic_coding.cli import app


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    (tmp_path / ".git").mkdir()
    return tmp_path


def invoke(runner: CliRunner, repo: Path, args: list[str]):
    return runner.invoke(app, [*args, "--root", str(repo)])


def current_task(repo: Path) -> str:
    return (repo / ".agentic" / "current").read_text(encoding="utf-8").strip()
