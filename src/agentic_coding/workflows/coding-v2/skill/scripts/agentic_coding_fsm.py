#!/usr/bin/env python3
"""Hermes-native finite-state controller for the agentic-coding-v2 skill.

This runner deliberately uses only the Python standard library so it works in
Hermes environments without pip. It is not a coding agent; it is the control
plane that makes stage transitions explicit, durable, and auditable.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGES = [
    "DISC-00",
    "SCAN-05",
    "SPEC-10",
    "PLAN-20",
    "BUILD-30",
    "VERIFY-40",
    "REVIEW-50",
    "DOC-60",
    "SHIP-70",
]

STAGE_NAMES = {
    "DISC-00": "Discovery / Safety",
    "SCAN-05": "Consequence Scan",
    "SPEC-10": "Specify",
    "PLAN-20": "Plan",
    "BUILD-30": "Build",
    "VERIFY-40": "Verify",
    "REVIEW-50": "Review",
    "DOC-60": "Document",
    "SHIP-70": "Ship",
}

ALLOWED_TRANSITIONS = {
    "DISC-00": {"SCAN-05", "SPEC-10"},  # SPEC-10 only when SCAN-05 is explicitly skipped.
    "SCAN-05": {"SPEC-10"},
    "SPEC-10": {"PLAN-20"},
    "PLAN-20": {"BUILD-30"},
    "BUILD-30": {"VERIFY-40", "SPEC-10", "PLAN-20", "SCAN-05"},
    "VERIFY-40": {"REVIEW-50", "BUILD-30"},
    "REVIEW-50": {"DOC-60", "BUILD-30", "VERIFY-40"},
    "DOC-60": {"SHIP-70"},
    "SHIP-70": set(),
}

STRICT_APPROVAL_STAGE = "PLAN-20"

MODE_CHOICES = {"lightweight", "standard", "strict"}
RISK_CHOICES = {"low", "medium", "high"}
TIER_CHOICES = {"tier-1-mechanical", "tier-2-normal", "tier-3-critical"}
TERMINAL_STATUSES = {"done", "blocked", "skipped", "deferred-by-user"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str, max_len: int = 48) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return (value or "task")[:max_len].strip("-") or "task"


def repo_root(path: str | None) -> Path:
    return Path(path or os.getcwd()).resolve()


def task_dir(root: Path, task_id: str) -> Path:
    return root / "docs" / task_id


def state_path(root: Path, task_id: str) -> Path:
    return task_dir(root, task_id) / "state.json"


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"state file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}")


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text)


def read_state(root: Path, task_id: str) -> dict[str, Any]:
    state = load_json(state_path(root, task_id))
    current = state.get("current_stage")
    if current not in STAGES:
        raise SystemExit(f"invalid current_stage {current!r}; expected one of {', '.join(STAGES)}")
    state.setdefault("completed_stages", [])
    state.setdefault("skipped_stages", [])
    state.setdefault("blockers", [])
    state.setdefault("decisions", [])
    state.setdefault("validation", {"commands_planned": [], "commands_run": [], "evidence": [], "last_result": ""})
    state.setdefault("fsm_events", [])
    return state


def event(state: dict[str, Any], kind: str, **fields: Any) -> None:
    state.setdefault("fsm_events", []).append({"at": now(), "kind": kind, **fields})
    state["last_updated"] = now()


def init_files(root: Path, state: dict[str, Any], force: bool = False) -> None:
    task_id = state["task_id"]
    base = task_dir(root, task_id)
    if base.exists() and not force:
        raise SystemExit(f"task directory already exists: {base} (pass --force to overwrite state.json only)")
    (base / "snapshots").mkdir(parents=True, exist_ok=True)
    save_json(base / "state.json", state)
    if force:
        return
    (base / "todos.md").write_text(render_todos(state), encoding="utf-8")
    (base / "checkpoint.md").write_text(render_checkpoint(state, "Initialized FSM runtime artifacts."), encoding="utf-8")
    (base / "artifacts.md").write_text(render_artifacts(state), encoding="utf-8")


def render_todos(state: dict[str, Any]) -> str:
    rows = []
    for idx, stage in enumerate(STAGES, start=1):
        status = "pending"
        if stage == state.get("current_stage"):
            status = "in_progress"
        rows.append(
            f"| T-{idx:03d} | {stage} | {STAGE_NAMES[stage]} gate | controller | {status} | | |"
        )
    return f"""# Task Ledger

Task ID: `{state['task_id']}`  
Goal: {state.get('goal', '')}  
Mode/Risk/Tier: {state.get('mode')} / {state.get('risk')} / {state.get('model_tier')}  
Current Stage: `{state.get('current_stage')}`

## Ledger

| ID | Stage | Task | Owner | Status | Evidence | Blocker/Skip Reason |
| --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

## Status Vocabulary

- `pending`
- `in_progress`
- `done`
- `blocked`
- `skipped`
- `deferred-by-user`

## Rules

- Every activated stage must have at least one row.
- Skipped stages require a reason.
- Done rows require evidence.
- The final response is not allowed while required rows remain `pending` or `in_progress`.
"""


def render_checkpoint(state: dict[str, Any], note: str) -> str:
    return f"""# Checkpoint

Task ID: `{state['task_id']}`  
Updated: {now()}  
Current Stage: `{state.get('current_stage')}`  
Goal: {state.get('goal', '')}

## Latest FSM Note

{note}

## Next Action

{state.get('next_action', '')}

## Blockers

{chr(10).join('- ' + str(b) for b in state.get('blockers', [])) or '- None'}
"""


def render_artifacts(state: dict[str, Any]) -> str:
    return f"""# Artifact Manifest

Task ID: `{state['task_id']}`

| Artifact | Path | Notes |
| --- | --- | --- |
| State | `docs/{state['task_id']}/state.json` | Canonical FSM state |
| Todos | `docs/{state['task_id']}/todos.md` | Stage ledger |
| Checkpoint | `docs/{state['task_id']}/checkpoint.md` | Resume summary |
| Snapshots | `docs/{state['task_id']}/snapshots/` | Stage-boundary summaries |
"""


def add_snapshot(root: Path, state: dict[str, Any], stage: str, evidence: str) -> None:
    path = task_dir(root, state["task_id"]) / "snapshots" / f"{stage}-summary.md"
    path.write_text(
        f"""# {stage} — {STAGE_NAMES[stage]} Summary

Updated: {now()}

## Evidence

{evidence}

## Current State After Boundary

- Current stage: `{state.get('current_stage')}`
- Completed: {', '.join(state.get('completed_stages', [])) or 'none'}
- Skipped: {', '.join(s.get('stage', '') if isinstance(s, dict) else str(s) for s in state.get('skipped_stages', [])) or 'none'}
- Next action: {state.get('next_action', '')}
""",
        encoding="utf-8",
    )


def ensure_transition(state: dict[str, Any], target: str) -> None:
    current = state["current_stage"]
    if target not in STAGES:
        raise SystemExit(f"unknown target stage {target!r}; expected one of {', '.join(STAGES)}")
    if target not in ALLOWED_TRANSITIONS[current]:
        raise SystemExit(
            f"illegal transition: {current} -> {target}. Allowed: {sorted(ALLOWED_TRANSITIONS[current]) or 'none'}"
        )
    if current == "DISC-00" and target == "SPEC-10" and not stage_skipped(state, "SCAN-05"):
        raise SystemExit("DISC-00 -> SPEC-10 requires SCAN-05 to be explicitly skipped first")


def stage_skipped(state: dict[str, Any], stage: str) -> bool:
    for item in state.get("skipped_stages", []):
        if isinstance(item, dict) and item.get("stage") == stage:
            return True
        if item == stage:
            return True
    return False


def require_evidence(evidence: str | None) -> str:
    if not evidence or not evidence.strip():
        raise SystemExit("--evidence is required for complete/transition/final assertions")
    return evidence.strip()


def state_brief(state: dict[str, Any], root: Path, transition: str | None = None, previous_stage: str | None = None) -> dict[str, Any]:
    """Return a compact, precise state summary for transition output."""
    current = state.get("current_stage")
    brief: dict[str, Any] = {
        "task_id": state.get("task_id"),
        "current_stage": current,
        "stage_name": STAGE_NAMES.get(str(current), "unknown"),
        "next_action": state.get("next_action", ""),
        "state_path": str(state_path(root, state["task_id"])),
    }
    if previous_stage:
        brief["previous_stage"] = previous_stage
    if transition:
        brief["transition"] = transition
    return brief


def print_state(state: dict[str, Any], root: Path, transition: str | None = None, previous_stage: str | None = None, **extra: Any) -> None:
    payload = {"ok": True, "state": state_brief(state, root, transition=transition, previous_stage=previous_stage)}
    payload.update(extra)
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_init(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    task_id = args.task_id or f"temp-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{slugify(args.goal)}"
    if args.mode not in MODE_CHOICES:
        raise SystemExit(f"invalid mode: {args.mode}")
    if args.risk not in RISK_CHOICES:
        raise SystemExit(f"invalid risk: {args.risk}")
    if args.tier not in TIER_CHOICES:
        raise SystemExit(f"invalid tier: {args.tier}")
    state = {
        "task_id": task_id,
        "goal": args.goal,
        "mode": args.mode,
        "risk": args.risk,
        "model_tier": args.tier,
        "current_stage": "DISC-00",
        "completed_stages": [],
        "skipped_stages": [],
        "acceptance_criteria": args.acceptance or [],
        "assumptions": [],
        "decisions": [],
        "open_questions": [],
        "blockers": [],
        "touched_files": [],
        "out_of_scope": [],
        "validation": {"commands_planned": [], "commands_run": [], "evidence": [], "last_result": ""},
        "artifacts": {
            "plan": f"docs/{task_id}/PLAN.md",
            "todos": f"docs/{task_id}/todos.md",
            "checkpoint": f"docs/{task_id}/checkpoint.md",
            "manifest": f"docs/{task_id}/artifacts.md",
            "snapshots_dir": f"docs/{task_id}/snapshots/",
        },
        "next_action": "Complete DISC-00 discovery/safety gate.",
        "last_updated": now(),
        "fsm_events": [],
    }
    event(state, "init", stage="DISC-00")
    init_files(root, state, force=args.force)
    print_state(state, root, transition="init")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    state = read_state(root, args.task_id)
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    state = read_state(root, args.task_id)
    evidence = require_evidence(args.evidence)
    current = state["current_stage"]
    target = args.to or next_stage(current)
    if target is None:
        raise SystemExit(f"{current} is terminal; cannot complete to another stage")
    ensure_transition(state, target)
    if current == STRICT_APPROVAL_STAGE and state.get("mode") in {"standard", "strict"} and not args.user_approved:
        raise SystemExit("PLAN-20 -> BUILD-30 for standard/strict work requires --user-approved")
    if current not in state["completed_stages"]:
        state["completed_stages"].append(current)
    state["validation"].setdefault("evidence", []).append({"stage": current, "evidence": evidence, "at": now()})
    old = current
    state["current_stage"] = target
    state["next_action"] = args.next_action or f"Complete {target} — {STAGE_NAMES[target]} gate."
    event(state, "complete", frm=old, to=target, evidence=evidence)
    save_json(state_path(root, args.task_id), state)
    add_snapshot(root, state, old, evidence)
    update_checkpoint(root, state, f"Completed {old} -> {target}. Evidence: {evidence}")
    print_state(state, root, transition=f"{old}->{target}", previous_stage=old)
    return 0


def next_stage(stage: str) -> str | None:
    try:
        return STAGES[STAGES.index(stage) + 1]
    except IndexError:
        return None


def cmd_skip(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    state = read_state(root, args.task_id)
    stage = args.stage
    if stage not in STAGES:
        raise SystemExit(f"unknown stage {stage!r}")
    reason = require_evidence(args.reason)
    if stage == state["current_stage"]:
        target = args.to or next_stage(stage)
        if target is None:
            raise SystemExit(f"{stage} is terminal; cannot skip to another stage")
        ensure_transition(state, target)
        old = state["current_stage"]
        state["current_stage"] = target
        state["next_action"] = args.next_action or f"Complete {target} — {STAGE_NAMES[target]} gate."
        event(state, "skip_current", frm=old, to=target, reason=reason)
        transition = f"{old}->{target}"
        previous_stage = old
    else:
        event(state, "skip_future_or_past", stage=stage, reason=reason)
        transition = f"skip:{stage}"
        previous_stage = None
    if not stage_skipped(state, stage):
        state["skipped_stages"].append({"stage": stage, "reason": reason, "at": now()})
    save_json(state_path(root, args.task_id), state)
    update_checkpoint(root, state, f"Skipped {stage}. Reason: {reason}")
    print_state(state, root, transition=transition, previous_stage=previous_stage, skipped=stage)
    return 0


def cmd_block(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    state = read_state(root, args.task_id)
    reason = require_evidence(args.reason)
    state["blockers"].append({"stage": state["current_stage"], "reason": reason, "at": now()})
    state["next_action"] = args.next_action or "Resolve blocker or ask user for scoped decision."
    event(state, "block", stage=state["current_stage"], reason=reason)
    save_json(state_path(root, args.task_id), state)
    update_checkpoint(root, state, f"Blocked in {state['current_stage']}: {reason}")
    print_state(state, root, transition="blocked", blocked_stage=state["current_stage"], reason=reason)
    return 0


def cmd_assert_final(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    state = read_state(root, args.task_id)
    evidence = require_evidence(args.evidence)
    missing = []
    completed = set(state.get("completed_stages", []))
    skipped = {s.get("stage") if isinstance(s, dict) else s for s in state.get("skipped_stages", [])}
    for stage in STAGES[:-1]:
        if stage not in completed and stage not in skipped:
            missing.append(stage)
    if state.get("current_stage") != "SHIP-70":
        missing.append(f"current_stage_is_{state.get('current_stage')}_not_SHIP-70")
    if missing:
        raise SystemExit("final assertion failed; missing completed/skipped stages: " + ", ".join(missing))
    state["validation"].setdefault("evidence", []).append({"stage": "SHIP-70", "evidence": evidence, "at": now()})
    event(state, "assert_final", evidence=evidence)
    save_json(state_path(root, args.task_id), state)
    update_checkpoint(root, state, f"Final assertion passed. Evidence: {evidence}")
    print_state(state, root, transition="assert-final", final=True)
    return 0


def update_checkpoint(root: Path, state: dict[str, Any], note: str) -> None:
    path = task_dir(root, state["task_id"]) / "checkpoint.md"
    path.write_text(render_checkpoint(state, note), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Finite-state controller for Hermes agentic-coding-v2 runtime artifacts")
    p.add_argument("--root", help="Repository/workspace root. Defaults to current directory.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init", help="Initialize docs/<task-id>/ runtime artifacts at DISC-00")
    sp.add_argument("--task-id", help="Task directory name under docs/. Defaults to temp-YYYYMMDD-<goal-slug>.")
    sp.add_argument("--goal", required=True)
    sp.add_argument("--mode", required=True, choices=sorted(MODE_CHOICES))
    sp.add_argument("--risk", required=True, choices=sorted(RISK_CHOICES))
    sp.add_argument("--tier", required=True, choices=sorted(TIER_CHOICES))
    sp.add_argument("--acceptance", action="append", help="Acceptance criterion. Repeat as needed.")
    sp.add_argument("--force", action="store_true", help="Allow overwriting state.json when task dir already exists.")
    sp.set_defaults(func=cmd_init)

    for name, help_text in [
        ("status", "Print current state.json"),
        ("complete", "Complete current stage and advance to a legal next stage"),
        ("skip", "Record an explicit stage skip with reason"),
        ("block", "Record a blocker without advancing"),
        ("assert-final", "Assert SHIP-70 final-gate consistency before final response"),
    ]:
        sp = sub.add_parser(name, help=help_text)
        sp.add_argument("--task-id", required=True)
        if name == "complete":
            sp.add_argument("--to", choices=STAGES, help="Target stage. Defaults to next linear stage.")
            sp.add_argument("--evidence", required=True)
            sp.add_argument("--next-action")
            sp.add_argument("--user-approved", action="store_true", help="Required for PLAN-20 -> BUILD-30 in standard/strict mode.")
            sp.set_defaults(func=cmd_complete)
        elif name == "skip":
            sp.add_argument("--stage", required=True, choices=STAGES)
            sp.add_argument("--reason", required=True)
            sp.add_argument("--to", choices=STAGES, help="If skipping current stage, target stage. Defaults to next linear stage.")
            sp.add_argument("--next-action")
            sp.set_defaults(func=cmd_skip)
        elif name == "block":
            sp.add_argument("--reason", required=True)
            sp.add_argument("--next-action")
            sp.set_defaults(func=cmd_block)
        elif name == "assert-final":
            sp.add_argument("--evidence", required=True)
            sp.set_defaults(func=cmd_assert_final)
        else:
            sp.set_defaults(func=cmd_status)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
