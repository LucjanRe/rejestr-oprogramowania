from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget

from autosave import AutosaveManager
from models import TableSchema
from repository import EntryRepository
from ui_form import FormController
from ui_filters_sorts import FiltersSortsController


class ActionsController:
    def __init__(
        self,
        repo: EntryRepository,
        autosave: AutosaveManager,
        form: FormController,
        filters_sorts: FiltersSortsController,
        table: QTableWidget,
        btn_add_update,
        statusbar,
    ) -> None:
        self.repo = repo
        self.autosave = autosave
        self.form = form
        self.filters_sorts = filters_sorts
        self.table = table
        self.btn_add_update = btn_add_update
        self.statusbar = statusbar
        self.selected_repo_index: Optional[int] = None

    def new_entry(self) -> None:
        self.selected_repo_index = None
        self.btn_add_update.setText("Dodaj wpis")
        self.form.clear()

    def add_or_update(self) -> None:
        entry = self.form.read()
        if entry is None:
            return

        if self.selected_repo_index is None:
            self.repo.add(entry)
            self.statusbar.showMessage("Dodano wpis.")
        else:
            try:
                self.repo.update(self.selected_repo_index, entry)
                self.statusbar.showMessage("Zapisano zmiany.")
            except IndexError:
                self.statusbar.showMessage("Błąd: nieprawidłowy indeks wpisu.")
                return

        try:
            p = self.autosave.autosave(self.repo.entries())
            self.statusbar.showMessage(f"Autosave: {p}")
        except Exception as e:
            self.statusbar.showMessage(f"Błąd autosave: {e}")

        self.filters_sorts.rebuild_filter_lists()
        self.refresh_table()
        self.new_entry()

    def row_selected(self, row: int) -> None:
        item = self.table.item(row, 0)
        if item is None:
            return
        repo_index = item.data(Qt.ItemDataRole.UserRole)
        if repo_index is None:
            return

        self.selected_repo_index = int(repo_index)
        self.btn_add_update.setText("Zapisz zmiany")

        try:
            entry = self.repo.get(self.selected_repo_index)
        except IndexError:
            return
        self.form.fill(entry)

    def refresh_table(self) -> None:
        was_sorting = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)

        entries = self.repo.entries()
        filtered = self.filters_sorts.filtered_indices()

        self.table.setRowCount(len(filtered))
        for r, repo_i in enumerate(filtered):
            e = entries[repo_i]
            values = [getattr(e, k) for k in TableSchema.KEYS]

            for c, val in enumerate(values):
                cell = QTableWidgetItem(val)
                cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if c == 0:
                    cell.setData(Qt.ItemDataRole.UserRole, repo_i)
                self.table.setItem(r, c, cell)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setSortingEnabled(was_sorting)