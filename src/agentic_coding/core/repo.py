from __future__ import annotations

from pathlib import Path


def find_upwards(start: Path, marker: str) -> Path | None:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for path in [current, *current.parents]:
        if (path / marker).exists():
            return path
    return None


def detect_root(root: Path | None = None) -> Path:
    if root is not None:
        return root.resolve()
    cwd = Path.cwd().resolve()
    git_root = find_upwards(cwd, ".git")
    if git_root:
        return git_root
    config_root = find_upwards(cwd, ".agentic/config.toml")
    if config_root:
        return config_root
    return cwd


def gitignore_warnings(root: Path) -> list[str]:
    if not (root / ".git").exists():
        return []
    gitignore = root / ".gitignore"
    content = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    warnings: list[str] = []
    if "docs/temp-*" not in content and "docs/temp-" not in content:
        warnings.append("Task artifacts appear unignored: add docs/temp-* to .gitignore.")
    if ".agentic/current" not in content and ".agentic/" not in content:
        warnings.append("Current task pointer appears unignored: add .agentic/current to .gitignore.")
    return warnings
