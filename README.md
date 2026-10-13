# agentic-coding

`agentic` is a standalone CLI for running the Agentic Coding v2 workflow as a durable state machine.

M1 supports a vertical slice:

- `agentic workflow list`
- `agentic workflow show coding-v2`
- `agentic init --goal ... --acceptance ...`
- `agentic status`
- `agentic complete --stage DISC-00 --evidence ...`

Task state is written to `docs/temp-<task-id>/` and the current task pointer is `.agentic/current`.

## Development

```bash
uv run agentic --help
uv run pytest
uv build
```
