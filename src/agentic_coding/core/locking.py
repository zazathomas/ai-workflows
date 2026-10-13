from __future__ import annotations

from pathlib import Path

from filelock import FileLock, Timeout


class AgenticLockTimeout(RuntimeError):
    pass


class Lock:
    def __init__(self, path: Path, timeout: int = 10) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = FileLock(str(path), timeout=timeout)

    def __enter__(self) -> "Lock":
        try:
            self._lock.acquire()
        except Timeout as exc:
            raise AgenticLockTimeout(f"timed out waiting for lock: {self.path}") from exc
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        self._lock.release()
