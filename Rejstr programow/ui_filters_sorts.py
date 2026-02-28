from typing import List
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QComboBox, QTableWidget

from filters import FilterEngine
from models import TableSchema
from repository import EntryRepository


class FiltersSortsController:
    def __init__(
        self,
        repo: EntryRepository,
        txt_search: QLineEdit,
        cmb_machine_filter: QComboBox,
        cmb_software_filter: QComboBox,
        cmb_sort_field: QComboBox,
        cmb_sort_order: QComboBox,
        table: QTableWidget,
        all_token: str = "(Wszystkie)",
    ) -> None:
        self.repo = repo
        self.txt_search = txt_search
        self.cmb_machine_filter = cmb_machine_filter
        self.cmb_software_filter = cmb_software_filter
        self.cmb_sort_field = cmb_sort_field
        self.cmb_sort_order = cmb_sort_order
        self.table = table
        self.all_token = all_token

    def rebuild_filter_lists(self) -> None:
        entries = self.repo.entries()
        machines = sorted({e.machine_type.strip() for e in entries if e.machine_type.strip()}, key=str.lower)
        softwares = sorted({e.software_type.strip() for e in entries if e.software_type.strip()}, key=str.lower)

        def refill(combo: QComboBox, values: List[str]) -> None:
            prev = combo.currentText().strip() if combo.count() else self.all_token
            combo.blockSignals(True)
            combo.clear()
            combo.addItem(self.all_token)
            combo.addItems(values)
            idx = combo.findText(prev)
            combo.setCurrentIndex(idx if idx >= 0 else 0)
            combo.blockSignals(False)

        refill(self.cmb_machine_filter, machines)
        refill(self.cmb_software_filter, softwares)

    def filtered_indices(self) -> List[int]:
        return FilterEngine.filter_indices(
            entries=self.repo.entries(),
            search_text=self.txt_search.text(),
            machine_filter=self.cmb_machine_filter.currentText().strip(),
            software_filter=self.cmb_software_filter.currentText().strip(),
            all_token=self.all_token,
        )

    def clear_filters(self) -> None:
        self.txt_search.blockSignals(True)
        self.txt_search.setText("")
        self.txt_search.blockSignals(False)
        self.cmb_machine_filter.setCurrentIndex(0)
        self.cmb_software_filter.setCurrentIndex(0)

    def apply_sort(self) -> None:
        idx = self.cmb_sort_field.currentIndex()
        if not (0 <= idx < len(TableSchema.SORT_FIELDS)):
            return
        _label, col = TableSchema.SORT_FIELDS[idx]
        order = Qt.SortOrder.AscendingOrder if self.cmb_sort_order.currentText() == "Rosnąco" else Qt.SortOrder.DescendingOrder
        self.table.sortItems(col, order)