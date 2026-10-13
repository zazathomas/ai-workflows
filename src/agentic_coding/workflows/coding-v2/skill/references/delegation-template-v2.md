# Delegation Prompt Template

Use this template when delegating a scoped task from Agentic Coding v2.

```text
Implement T### using strict scoped execution.

TASK:
<paste exact task text>

CONTEXT:
- Repo root:
- Workflow mode:
- Risk level:
- Model tier: 🟢/🟡/🔴
- Stack/package manager:
- Relevant requirements/spec excerpts:
- Relevant plan/consequence-scan findings:
- Existing conventions:

FILES:
- Inspect first:
- May modify:
- Forbidden/out of scope:
- Expected touched files:

RULES:
1. Use TDD for behavior changes.
2. Confirm RED failure when practical.
3. Implement minimum GREEN code.
4. Do not broaden scope.
5. Do not add dependencies unless explicitly permitted.
6. Do not run repo-wide formatters unless required.
7. Do not commit unless explicitly instructed.
8. If out-of-scope changes are required, stop and report.

VALIDATION:
- Targeted commands:
- Affected-area commands:
- Manual/browser/API smoke if applicable:

RETURN FORMAT:
- Summary:
- Files changed:
- Tests added/updated:
- Commands run:
  - command:
    exit_code:
    result:
- TDD evidence:
  - failing test command/output summary:
  - passing test command/output summary:
- Known limitations:
- Suggested verification for controller:
```
