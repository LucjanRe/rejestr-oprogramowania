from typing import List, Sequence
from models import ProgramEntry


class EntryRepository:
    def __init__(self) -> None:
        self._entries: List[ProgramEntry] = []

    def entries(self) -> List[ProgramEntry]:
        return list(self._entries)

    def set_all(self, entries: Sequence[ProgramEntry]) -> None:
        self._entries = list(entries)

    def add(self, entry: ProgramEntry) -> None:
        self._entries.append(entry)

    def update(self, index: int, entry: ProgramEntry) -> None:
        if not (0 <= index < len(self._entries)):
            raise IndexError("Nieprawidłowy indeks wpisu.")
        self._entries[index] = entry

    def get(self, index: int) -> ProgramEntry:
        if not (0 <= index < len(self._entries)):
            raise IndexError("Nieprawidłowy indeks wpisu.")
        return self._entries[index]