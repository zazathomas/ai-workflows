from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from agentic_coding.constants import STATE_SCHEMA_VERSION


class Mode(str, Enum):
    lightweight = "lightweight"
    standard = "standard"
    strict = "strict"


class Risk(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ModelTier(str, Enum):
    tier_1 = "tier-1-mechanical"
    tier_2 = "tier-2-normal"
    tier_3 = "tier-3-critical"


class StageDefinition(BaseModel):
    id: str
    name: str
    purpose: str
    next: str | None = None
    skippable: dict[str, bool] = Field(default_factory=dict)


class WorkflowTransitions(BaseModel):
    forward: dict[str, str | None]
    revisits: dict[str, list[str]] = Field(default_factory=dict)


class WorkflowDefinition(BaseModel):
    id: str
    version: str
    display_name: str
    default_stage: str
    stages: list[StageDefinition]
    transitions: WorkflowTransitions

    def stage(self, stage_id: str) -> StageDefinition:
        for stage in self.stages:
            if stage.id == stage_id:
                return stage
        raise KeyError(f"unknown stage: {stage_id}")

    def next_stage(self, stage_id: str) -> str | None:
        return self.transitions.forward.get(stage_id)


class AcceptanceCriterion(BaseModel):
    id: str
    text: str
    status: Literal["pending", "completed"] = "pending"
    evidence: list[str] = Field(default_factory=list)


class EvidenceRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"EV-{uuid4().hex[:8]}")
    stage: str
    summary: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    artifact_ids: list[str] = Field(default_factory=list)

    @field_validator("summary")
    @classmethod
    def summary_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("evidence summary cannot be empty")
        return value


class FSMEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"EVT-{uuid4().hex}")
    timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    type: str
    actor: str = "cli"
    stage_before: str | None = None
    stage_after: str | None = None
    summary: str
    evidence: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    state_version_after: str = STATE_SCHEMA_VERSION


class TaskState(BaseModel):
    state_schema_version: str = STATE_SCHEMA_VERSION
    task_id: str
    goal: str
    workflow_id: str
    workflow_version: str
    root: str
    task_dir: str
    current_stage: str
    previous_stage: str | None = None
    status: Literal["active", "blocked", "completed"] = "active"
    mode: Mode = Mode.standard
    risk: Risk = Risk.medium
    model_tier: ModelTier = ModelTier.tier_2
    acceptance_criteria: list[AcceptanceCriterion] = Field(default_factory=list)
    completed_stages: list[str] = Field(default_factory=list)
    skipped_stages: dict[str, str] = Field(default_factory=dict)
    invalidated_stages: dict[str, str] = Field(default_factory=dict)
    stage_attempts: dict[str, int] = Field(default_factory=dict)
    blockers: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def root_path(self) -> Path:
        return Path(self.root)

    @property
    def task_path(self) -> Path:
        return Path(self.task_dir)
