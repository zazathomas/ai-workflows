from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from agentic_coding.constants import MANAGED_END, MANAGED_START
from agentic_coding.core.models import EvidenceRecord, TaskState, WorkflowDefinition


def update_managed_file(path: Path, title: str, managed: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    block = f"{MANAGED_START}\n{managed.rstrip()}\n{MANAGED_END}"
    if not path.exists():
        path.write_text(f"# {title}\n\n{block}\n\n## Notes\n\n", encoding="utf-8")
        return
    content = path.read_text(encoding="utf-8")
    if MANAGED_START in content and MANAGED_END in content:
        before, rest = content.split(MANAGED_START, 1)
        _, after = rest.split(MANAGED_END, 1)
        path.write_text(f"{before}{block}{after}", encoding="utf-8")
    else:
        path.write_text(f"{content.rstrip()}\n\n{block}\n", encoding="utf-8")


def stage_status(state: TaskState, stage_id: str) -> str:
    if stage_id == state.current_stage:
        return "current"
    if stage_id in state.completed_stages:
        return "completed"
    if stage_id in state.skipped_stages:
        return "skipped"
    return "pending"


def next_action(state: TaskState, workflow: WorkflowDefinition) -> str:
    stage = workflow.stage(state.current_stage)
    return f"Complete {stage.id} — {stage.name} gate."


def render_todos(state: TaskState, workflow: WorkflowDefinition) -> str:
    rows = ["| Stage | Name | Status | Evidence |", "| --- | --- | --- | --- |"]
    for stage in workflow.stages:
        evidence = "; ".join(e.summary for e in state.evidence if e.stage == stage.id)
        rows.append(f"| {stage.id} | {stage.name} | {stage_status(state, stage.id)} | {evidence} |")
    return "\n".join(rows)


def render_checkpoint(state: TaskState, workflow: WorkflowDefinition) -> str:
    stage = workflow.stage(state.current_stage)
    ac = "\n".join(f"- {item.id}: {item.text} [{item.status}]" for item in state.acceptance_criteria) or "- None recorded"
    completed = ", ".join(state.completed_stages) or "None"
    latest = state.evidence[-1].summary if state.evidence else "None"
    return f"""Task: {state.task_id}
Goal: {state.goal}
Workflow: {state.workflow_id} {state.workflow_version}
Mode/Risk/Tier: {state.mode.value} / {state.risk.value} / {state.model_tier.value}
Current stage: {stage.id} {stage.name}
Completed stages: {completed}
Latest evidence: {latest}
Next action: {next_action(state, workflow)}
State path: {Path(state.task_dir) / 'state.json'}

## Acceptance criteria

{ac}
"""


def render_capsule(state: TaskState, workflow: WorkflowDefinition) -> str:
    ac = "\n".join(f"- {item.id}: {item.text} [{item.status}]" for item in state.acceptance_criteria) or "- None recorded"
    return f"""Task ID: {state.task_id}
Goal: {state.goal}
Current stage: {state.current_stage} {workflow.stage(state.current_stage).name}
Mode/Risk/Tier: {state.mode.value} / {state.risk.value} / {state.model_tier.value}

Acceptance criteria:
{ac}

Completed stages: {', '.join(state.completed_stages) or 'None'}
Blockers: {len(state.blockers)} unresolved
Next action: {next_action(state, workflow)}
"""


def refresh_artifacts(state: TaskState, workflow: WorkflowDefinition) -> None:
    task_dir = Path(state.task_dir)
    update_managed_file(task_dir / "todos.md", "Todos", render_todos(state, workflow))
    update_managed_file(task_dir / "checkpoint.md", "Checkpoint", render_checkpoint(state, workflow))
    update_managed_file(task_dir / "context-capsule.md", "Context Capsule", render_capsule(state, workflow))


def write_stage_snapshot(
    state: TaskState,
    workflow: WorkflowDefinition,
    completed_stage: str,
    evidence: EvidenceRecord,
    next_stage: str | None,
) -> None:
    task_dir = Path(state.task_dir)
    stage = workflow.stage(completed_stage)
    next_label = "None" if next_stage is None else f"{next_stage} {workflow.stage(next_stage).name}"
    content = f"""# {completed_stage} Summary

Completed at: {datetime.now(timezone.utc).isoformat()}
Stage: {completed_stage} {stage.name}
Evidence: {evidence.summary}
Transition: {completed_stage} -> {next_label}
"""
    path = task_dir / "snapshots" / f"{completed_stage}-summary.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
