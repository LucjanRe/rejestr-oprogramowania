import json
import csv
from dataclasses import asdict
from pathlib import Path
from typing import List, Sequence

from models import ProgramEntry, TableSchema


class JsonStorage:
    @staticmethod
    def save(path: Path, entries: Sequence[ProgramEntry]) -> None:
        data = [asdict(e) for e in entries]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def load(path: Path) -> List[ProgramEntry]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [ProgramEntry(**item) for item in raw]


class CsvExporterExcelPL:

    @staticmethod
    def export(path: Path, entries: Sequence[ProgramEntry]) -> None:
        with path.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(TableSchema.HEADERS)
            for e in entries:
                writer.writerow([getattr(e, k) for k in TableSchema.KEYS])