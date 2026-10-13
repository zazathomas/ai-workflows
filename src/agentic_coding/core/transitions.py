from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from agentic_coding.constants import DEFAULT_WORKFLOW_ID
from agentic_coding.core.artifacts import refresh_artifacts, write_stage_snapshot
from agentic_coding.core.events import append_event
from agentic_coding.core.locking import Lock
from agentic_coding.core.models import (
    AcceptanceCriterion,
    EvidenceRecord,
    FSMEvent,
    Mode,
    ModelTier,
    Risk,
    TaskState,
)
from agentic_coding.core.paths import current_pointer_path, make_task_id, project_lock_path, resolve_task_id, task_dir_for
from agentic_coding.core.repo import gitignore_warnings
from agentic_coding.core.state_io import read_state, write_state_atomic
from agentic_coding.core.workflow_loader import load_workflow


class AgenticError(RuntimeError):
    code = "agentic_error"


class ValidationError(AgenticError):
    code = "validation_failed"


class TaskNotFoundError(AgenticError):
    code = "task_not_found"


def validate_classification(mode: Mode, risk: Risk, tier: ModelTier) -> None:
    if mode == Mode.lightweight and risk == Risk.high:
        raise ValidationError("lightweight mode cannot be used with high risk")
    if mode == Mode.lightweight and tier == ModelTier.tier_3:
        raise ValidationError("lightweight mode cannot be used with tier-3-critical")


def init_task(
    root: Path,
    goal: str,
    acceptance: list[str],
    mode: Mode = Mode.standard,
    risk: Risk = Risk.medium,
    tier: ModelTier = ModelTier.tier_2,
    workflow_id: str = DEFAULT_WORKFLOW_ID,
) -> tuple[TaskState, list[str]]:
    if not goal.strip():
        raise ValidationError("--goal is required")
    validate_classification(mode, risk, tier)
    workflow = load_workflow(workflow_id)
    with Lock(project_lock_path(root)):
        task_id = make_task_id(goal, root)
        task_dir = task_dir_for(root, task_id)
        task_dir.mkdir(parents=True, exist_ok=False)
        (root / ".agentic").mkdir(parents=True, exist_ok=True)
        state = TaskState(
            task_id=task_id,
            goal=goal,
            workflow_id=workflow.id,
            workflow_version=workflow.version,
            root=str(root),
            task_dir=str(task_dir),
            current_stage=workflow.default_stage,
            mode=mode,
            risk=risk,
            model_tier=tier,
            acceptance_criteria=[
                AcceptanceCriterion(id=f"AC-{idx}", text=text) for idx, text in enumerate(acceptance, start=1)
            ],
            stage_attempts={workflow.default_stage: 1},
        )
        write_state_atomic(state)
        append_event(
            task_dir,
            FSMEvent(
                type="task_initialized",
                stage_after=state.current_stage,
                summary=f"Initialized task {task_id}",
                payload={"goal": goal, "acceptance_count": len(acceptance)},
            ),
        )
        refresh_artifacts(state, workflow)
        current_pointer_path(root).write_text(task_id + "\n", encoding="utf-8")
    return state, gitignore_warnings(root)


def load_task(root: Path, task_id: str | None = None) -> TaskState:
    try:
        resolved = resolve_task_id(root, task_id)
        task_dir = task_dir_for(root, resolved)
        return read_state(task_dir)
    except FileNotFoundError as exc:
        raise TaskNotFoundError(str(exc)) from exc


def complete_stage(root: Path, task_id: str | None, stage_assertion: str | None, evidence_text: str) -> TaskState:
    if not evidence_text or not evidence_text.strip():
        raise ValidationError("--evidence is required")
    state = load_task(root, task_id)
    workflow = load_workflow(state.workflow_id)
    task_dir = Path(state.task_dir)
    with Lock(task_dir / ".agentic.lock"):
        state = read_state(task_dir)
        current = state.current_stage
        if stage_assertion and stage_assertion != current:
            raise ValidationError(f"stage assertion {stage_assertion} does not match current stage {current}")
        next_stage = workflow.next_stage(current)
        if current not in workflow.transitions.forward:
            raise ValidationError(f"no forward transition is defined for {current}")
        evidence = EvidenceRecord(stage=current, summary=evidence_text.strip())
        state.evidence.append(evidence)
        if current not in state.completed_stages:
            state.completed_stages.append(current)
        state.stage_attempts[current] = state.stage_attempts.get(current, 0) + 1
        state.previous_stage = current
        if next_stage is None:
            state.status = "completed"
        else:
            state.current_stage = next_stage
            state.stage_attempts.setdefault(next_stage, 1)
        state.updated_at = datetime.now(timezone.utc)
        write_state_atomic(state)
        append_event(
            task_dir,
            FSMEvent(
                type="stage_completed",
                stage_before=current,
                stage_after=state.current_stage,
                summary=f"Completed {current}",
                evidence=evidence.summary,
                payload={"evidence_id": evidence.id, "next_stage": next_stage},
            ),
        )
        write_stage_snapshot(state, workflow, current, evidence, next_stage)
        refresh_artifacts(state, workflow)
    return state
