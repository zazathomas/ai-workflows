from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from agentic_coding.core.models import TaskState, WorkflowDefinition


class StateSummary(BaseModel):
    task_id: str
    workflow_id: str
    workflow_version: str
    current_stage: str
    stage_name: str
    previous_stage: str | None = None
    transition: str | None = None
    status: str
    next_action: str
    state_path: str


class CommandResponse(BaseModel):
    ok: bool
    command: str
    state: StateSummary | None = None
    workflows: list[dict[str, str]] | None = None
    workflow: dict | None = None
    warnings: list[str] = []
    errors: list[dict[str, object]] = []


def summarize_state(
    state: TaskState,
    workflow: WorkflowDefinition,
    previous_stage: str | None = None,
    transition: str | None = None,
) -> StateSummary:
    stage = workflow.stage(state.current_stage)
    return StateSummary(
        task_id=state.task_id,
        workflow_id=state.workflow_id,
        workflow_version=state.workflow_version,
        current_stage=state.current_stage,
        stage_name=stage.name,
        previous_stage=previous_stage if previous_stage is not None else state.previous_stage,
        transition=transition,
        status=state.status,
        next_action=f"Complete {stage.id} — {stage.name} gate.",
        state_path=str(Path(state.task_dir) / "state.json"),
    )
