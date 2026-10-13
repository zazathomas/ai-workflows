from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError as PydanticValidationError

from agentic_coding.constants import DEFAULT_WORKFLOW_ID
from agentic_coding.core.locking import AgenticLockTimeout
from agentic_coding.core.models import Mode, ModelTier, Risk
from agentic_coding.core.repo import detect_root
from agentic_coding.core.responses import CommandResponse, summarize_state
from agentic_coding.core.transitions import (
    AgenticError,
    TaskNotFoundError,
    ValidationError,
    complete_stage,
    init_task,
    load_task,
)
from agentic_coding.core.workflow_loader import list_workflows, load_workflow
from agentic_coding.exit_codes import LOCK_TIMEOUT, TASK_NOT_FOUND, VALIDATION_FAILED

app = typer.Typer(help="Agentic Coding state-machine CLI")
workflow_app = typer.Typer(help="Inspect bundled workflows")
app.add_typer(workflow_app, name="workflow")


def emit(response: CommandResponse, as_json: bool = False) -> None:
    if as_json:
        typer.echo(response.model_dump_json(indent=2))
        return
    if response.workflows is not None:
        for workflow in response.workflows:
            typer.echo(f"{workflow['id']}\t{workflow['version']}\t{workflow['display_name']}")
    elif response.workflow is not None:
        workflow = response.workflow
        typer.echo(f"{workflow['id']} {workflow['version']} — {workflow['display_name']}")
        for stage in workflow.get("stages", []):
            typer.echo(f"  {stage['id']} {stage['name']} -> {stage.get('next')}")
    elif response.state is not None:
        state = response.state
        if state.transition:
            typer.echo(
                f"FSM: {state.transition}; current={state.current_stage} {state.stage_name}; "
                f"next={state.next_action}"
            )
        else:
            typer.echo(f"Task: {state.task_id}")
            typer.echo(f"Workflow: {state.workflow_id} {state.workflow_version}")
            typer.echo(f"Current: {state.current_stage} {state.stage_name}")
            typer.echo(f"Status: {state.status}")
            typer.echo(f"Next: {state.next_action}")
            typer.echo(f"State: {state.state_path}")
    for warning in response.warnings:
        typer.echo(f"Warning: {warning}", err=True)


def fail(message: str, code: int, as_json: bool = False, err_code: str = "error") -> None:
    response = CommandResponse(ok=False, command="", errors=[{"code": err_code, "message": message}])
    if as_json:
        typer.echo(response.model_dump_json(indent=2), err=True)
    else:
        typer.echo(f"Error: {message}", err=True)
    raise typer.Exit(code)


@app.command()
def init(
    goal: Annotated[str, typer.Option("--goal", help="Task goal")],
    acceptance: Annotated[list[str], typer.Option("--acceptance", help="Acceptance criterion")] = [],
    mode: Annotated[Mode, typer.Option("--mode")] = Mode.standard,
    risk: Annotated[Risk, typer.Option("--risk")] = Risk.medium,
    tier: Annotated[ModelTier, typer.Option("--tier")] = ModelTier.tier_2,
    workflow: Annotated[str, typer.Option("--workflow")] = DEFAULT_WORKFLOW_ID,
    root: Annotated[Path | None, typer.Option("--root")] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    repo_root = detect_root(root)
    try:
        state, warnings = init_task(repo_root, goal, acceptance, mode, risk, tier, workflow)
        wf = load_workflow(state.workflow_id)
        response = CommandResponse(
            ok=True,
            command="init",
            state=summarize_state(state, wf),
            warnings=warnings,
        )
        emit(response, json_output)
    except AgenticLockTimeout as exc:
        fail(str(exc), LOCK_TIMEOUT, json_output, "lock_timeout")
    except (AgenticError, PydanticValidationError, FileNotFoundError) as exc:
        fail(str(exc), VALIDATION_FAILED, json_output, getattr(exc, "code", "validation_failed"))


@app.command()
def status(
    task_id: Annotated[str | None, typer.Option("--task-id")] = None,
    root: Annotated[Path | None, typer.Option("--root")] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    repo_root = detect_root(root)
    try:
        state = load_task(repo_root, task_id)
        wf = load_workflow(state.workflow_id)
        emit(CommandResponse(ok=True, command="status", state=summarize_state(state, wf)), json_output)
    except TaskNotFoundError as exc:
        fail(str(exc), TASK_NOT_FOUND, json_output, "task_not_found")
    except (AgenticError, PydanticValidationError, FileNotFoundError) as exc:
        fail(str(exc), VALIDATION_FAILED, json_output, getattr(exc, "code", "validation_failed"))


@app.command()
def complete(
    stage: Annotated[str | None, typer.Option("--stage", help="Assert current stage")] = None,
    evidence: Annotated[str | None, typer.Option("--evidence", help="Completion evidence")] = None,
    task_id: Annotated[str | None, typer.Option("--task-id")] = None,
    root: Annotated[Path | None, typer.Option("--root")] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    repo_root = detect_root(root)
    try:
        state = complete_stage(repo_root, task_id, stage, evidence or "")
        wf = load_workflow(state.workflow_id)
        transition = f"{state.previous_stage}->{state.current_stage}"
        emit(
            CommandResponse(
                ok=True,
                command="complete",
                state=summarize_state(state, wf, previous_stage=state.previous_stage, transition=transition),
            ),
            json_output,
        )
    except TaskNotFoundError as exc:
        fail(str(exc), TASK_NOT_FOUND, json_output, "task_not_found")
    except AgenticLockTimeout as exc:
        fail(str(exc), LOCK_TIMEOUT, json_output, "lock_timeout")
    except (ValidationError, PydanticValidationError, FileNotFoundError) as exc:
        fail(str(exc), VALIDATION_FAILED, json_output, getattr(exc, "code", "validation_failed"))


@workflow_app.command("list")
def workflow_list(json_output: Annotated[bool, typer.Option("--json")] = False) -> None:
    workflows = list_workflows()
    response = CommandResponse(
        ok=True,
        command="workflow list",
        workflows=[
            {"id": wf.id, "version": wf.version, "display_name": wf.display_name} for wf in workflows
        ],
    )
    emit(response, json_output)


@workflow_app.command("show")
def workflow_show(
    workflow_id: Annotated[str, typer.Argument()] = DEFAULT_WORKFLOW_ID,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    try:
        wf = load_workflow(workflow_id)
    except FileNotFoundError as exc:
        fail(str(exc), VALIDATION_FAILED, json_output, "workflow_not_found")
    response = CommandResponse(
        ok=True,
        command="workflow show",
        workflow=json.loads(wf.model_dump_json()),
    )
    emit(response, json_output)
