from dataclasses import dataclass


@dataclass(frozen=True)
class ProgramEntry:
    machine_type: str
    program_name: str
    software_type: str
    download_date: str
    upload_date: str
    modified_by: str
    ordered_by: str
    tested_by: str
    ordered_changes_description: str
    changes: str


class TableSchema:
    HEADERS = [
        "Typ maszyny",
        "Nazwa programu",
        "Rodzaj oprogramowania",
        "Data pobrania",
        "Data wgrania",
        "Kto modyfikował",
        "Na czyje polecenie",
        "Zmiany przetestowane przez",
        "Opis zleconych zmian",
        "Dokonane zmiany",
    ]

    KEYS = [
        "machine_type",
        "program_name",
        "software_type",
        "download_date",
        "upload_date",
        "modified_by",
        "ordered_by",
        "tested_by",
        "ordered_changes_description",
        "changes",
    ]

    SORT_FIELDS = [
        ("Typ maszyny", 0),
        ("Nazwa programu", 1),
        ("Rodzaj oprogramowania", 2),
        ("Data pobrania", 3),
        ("Data wgrania", 4),
    ]