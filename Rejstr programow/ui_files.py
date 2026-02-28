from pathlib import Path
from PyQt6.QtWidgets import QFileDialog, QMessageBox

from repository import EntryRepository
from storage import JsonStorage, CsvExporterExcelPL


class FilesController:
    def __init__(self, repo: EntryRepository, parent) -> None:
        self.repo = repo
        self.parent = parent

    def save_json_manual(self) -> None:
        path_str, _ = QFileDialog.getSaveFileName(self.parent, "Zapisz jako JSON", "", "JSON (*.json)")
        if not path_str:
            return
        try:
            JsonStorage.save(Path(path_str), self.repo.entries())
            QMessageBox.information(self.parent, "Informacja", "Zapisano plik JSON.")
        except Exception as e:
            QMessageBox.information(self.parent, "Informacja", f"Błąd zapisu: {e}")

    def load_json_manual(self) -> bool:
        path_str, _ = QFileDialog.getOpenFileName(self.parent, "Wczytaj JSON", "", "JSON (*.json)")
        if not path_str:
            return False
        try:
            entries = JsonStorage.load(Path(path_str))
            self.repo.set_all(entries)
            QMessageBox.information(self.parent, "Informacja", "Wczytano plik JSON.")
            return True
        except Exception as e:
            QMessageBox.information(self.parent, "Informacja", f"Błąd wczytywania: {e}")
            return False

    def export_csv(self) -> None:
        path_str, _ = QFileDialog.getSaveFileName(self.parent, "Eksportuj do CSV", "", "CSV (*.csv)")
        if not path_str:
            return
        try:
            CsvExporterExcelPL.export(Path(path_str), self.repo.entries())
            QMessageBox.information(self.parent, "Informacja", "Wyeksportowano CSV (Excel).")
        except Exception as e:
            QMessageBox.information(self.parent, "Informacja", f"Błąd eksportu: {e}")