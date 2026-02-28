from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence

from models import ProgramEntry
from storage import JsonStorage


class AutosaveManager:
    def __init__(self, autosave_dir: Path) -> None:
        self.autosave_dir = autosave_dir

    def _ensure_dir(self) -> None:
        self.autosave_dir.mkdir(parents=True, exist_ok=True)

    def autosave(self, entries: Sequence[ProgramEntry]) -> Path:

        self._ensure_dir()
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        path = self.autosave_dir / f"autosave_{stamp}.json"
        JsonStorage.save(path, entries)
        return path

    def _files_desc(self) -> List[Path]:
        if not self.autosave_dir.exists():
            return []
        return sorted(
            self.autosave_dir.glob("autosave_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

    def load_latest(self) -> Optional[List[ProgramEntry]]:

        for p in self._files_desc():
            try:
                return JsonStorage.load(p)
            except Exception:
                continue
        return None