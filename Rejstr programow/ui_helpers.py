from PyQt6.QtCore import QDate


def qdate_to_str(d: QDate) -> str:
    return d.toString("yyyy-MM-dd")


def str_to_qdate(s: str) -> QDate:
    parts = s.split("-")
    if len(parts) != 3:
        return QDate.currentDate()
    y, m, day = parts
    if not (y.isdigit() and m.isdigit() and day.isdigit()):
        return QDate.currentDate()
    d = QDate(int(y), int(m), int(day))
    return d if d.isValid() else QDate.currentDate()