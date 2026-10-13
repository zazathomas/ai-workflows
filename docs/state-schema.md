# State schema

M1 state is stored at `docs/temp-<task-id>/state.json` and includes:

- `state_schema_version`
- `task_id`
- `goal`
- `workflow_id`
- `workflow_version`
- `root`
- `task_dir`
- `current_stage`
- `previous_stage`
- `status`
- `mode`
- `risk`
- `model_tier`
- `acceptance_criteria`
- `completed_stages`
- `skipped_stages`
- `invalidated_stages`
- `stage_attempts`
- `blockers`
- `evidence`
- `artifacts`
- timestamps

The append-only audit log is `events.jsonl`.
