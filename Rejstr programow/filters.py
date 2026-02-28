from typing import List, Sequence
from models import ProgramEntry, TableSchema


class FilterEngine:
    @staticmethod
    def _norm(s: str) -> str:
        return (s or "").strip().lower()

    @staticmethod
    def filter_indices(
        entries: Sequence[ProgramEntry],
        search_text: str,
        machine_filter: str,
        software_filter: str,
        all_token: str = "(Wszystkie)",
    ) -> List[int]:
        q = FilterEngine._norm(search_text)
        idxs: List[int] = []

        for i, e in enumerate(entries):
            if machine_filter != all_token and e.machine_type.strip() != machine_filter:
                continue
            if software_filter != all_token and e.software_type.strip() != software_filter:
                continue

            if q:
                blob = " ".join(getattr(e, k) for k in TableSchema.KEYS)
                if q not in FilterEngine._norm(blob):
                    continue

            idxs.append(i)

        return idxs