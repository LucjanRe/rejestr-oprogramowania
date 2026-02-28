from typing import Optional
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLineEdit, QTextEdit, QDateEdit, QMessageBox

from models import ProgramEntry
from ui_helpers import qdate_to_str, str_to_qdate


class FormController:
    def __init__(
        self,
        txt_machine_type: QLineEdit,
        txt_program_name: QLineEdit,
        txt_software_type: QLineEdit,
        date_download: QDateEdit,
        date_upload: QDateEdit,
        txt_modified_by: QLineEdit,
        txt_ordered_by: QLineEdit,
        txt_tested_by: QLineEdit,
        txt_ordered_changes_description: QTextEdit,
        txt_changes: QTextEdit,
        msg_parent,
    ) -> None:
        self.txt_machine_type = txt_machine_type
        self.txt_program_name = txt_program_name
        self.txt_software_type = txt_software_type
        self.date_download = date_download
        self.date_upload = date_upload
        self.txt_modified_by = txt_modified_by
        self.txt_ordered_by = txt_ordered_by
        self.txt_tested_by = txt_tested_by
        self.txt_ordered_changes_description = txt_ordered_changes_description
        self.txt_changes = txt_changes
        self.msg_parent = msg_parent

    def clear(self) -> None:
        self.txt_machine_type.clear()
        self.txt_program_name.clear()
        self.txt_software_type.clear()
        self.date_download.setDate(QDate.currentDate())
        self.date_upload.setDate(QDate.currentDate())
        self.txt_modified_by.clear()
        self.txt_ordered_by.clear()
        self.txt_tested_by.clear()
        self.txt_ordered_changes_description.clear()
        self.txt_changes.clear()

    def read(self) -> Optional[ProgramEntry]:
        machine_type = self.txt_machine_type.text().strip()
        program_name = self.txt_program_name.text().strip()
        software_type = self.txt_software_type.text().strip()

        if not machine_type:
            self.info("Pole 'Typ maszyny' jest wymagane.")
            return None
        if not program_name:
            self.info("Pole 'Nazwa programu' jest wymagane.")
            return None
        if not software_type:
            self.info("Pole 'Rodzaj oprogramowania' jest wymagane.")
            return None

        return ProgramEntry(
            machine_type=machine_type,
            program_name=program_name,
            software_type=software_type,
            download_date=qdate_to_str(self.date_download.date()),
            upload_date=qdate_to_str(self.date_upload.date()),
            modified_by=self.txt_modified_by.text().strip(),
            ordered_by=self.txt_ordered_by.text().strip(),
            tested_by=self.txt_tested_by.text().strip(),
            ordered_changes_description=self.txt_ordered_changes_description.toPlainText().strip(),
            changes=self.txt_changes.toPlainText().strip(),
        )

    def fill(self, e: ProgramEntry) -> None:
        self.txt_machine_type.setText(e.machine_type)
        self.txt_program_name.setText(e.program_name)
        self.txt_software_type.setText(e.software_type)
        self.date_download.setDate(str_to_qdate(e.download_date))
        self.date_upload.setDate(str_to_qdate(e.upload_date))
        self.txt_modified_by.setText(e.modified_by)
        self.txt_ordered_by.setText(e.ordered_by)
        self.txt_tested_by.setText(e.tested_by)
        self.txt_ordered_changes_description.setPlainText(e.ordered_changes_description)
        self.txt_changes.setPlainText(e.changes)

    def info(self, text: str) -> None:
        QMessageBox.information(self.msg_parent, "Informacja", text)