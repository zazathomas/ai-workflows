from __future__ import annotations

from importlib import resources
from pathlib import Path

import yaml

from agentic_coding.constants import DEFAULT_WORKFLOW_ID
from agentic_coding.core.models import WorkflowDefinition

WORKFLOW_PACKAGE = "agentic_coding.workflows"


def list_workflows() -> list[WorkflowDefinition]:
    base = resources.files(WORKFLOW_PACKAGE)
    workflows: list[WorkflowDefinition] = []
    for item in base.iterdir():
        if item.is_dir() and (item / "workflow.yaml").is_file():
            workflows.append(load_workflow(item.name))
    return sorted(workflows, key=lambda workflow: workflow.id)


def load_workflow(workflow_id: str = DEFAULT_WORKFLOW_ID) -> WorkflowDefinition:
    workflow_path = resources.files(WORKFLOW_PACKAGE).joinpath(workflow_id).joinpath("workflow.yaml")
    if not workflow_path.is_file():
        raise FileNotFoundError(f"workflow not found: {workflow_id}")
    data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    return WorkflowDefinition.model_validate(data)


def stage_card_text(workflow_id: str, stage_id: str) -> str:
    path = resources.files(WORKFLOW_PACKAGE).joinpath(workflow_id).joinpath("stages").joinpath(f"{stage_id}.md")
    if not path.is_file():
        raise FileNotFoundError(f"stage card not found: {workflow_id}/{stage_id}")
    return path.read_text(encoding="utf-8")


def workflow_resource_root(workflow_id: str) -> Path | str:
    return str(resources.files(WORKFLOW_PACKAGE).joinpath(workflow_id))
