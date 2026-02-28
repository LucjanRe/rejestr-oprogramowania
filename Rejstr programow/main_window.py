from pathlib import Path

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QDateEdit, QTableWidget,
    QLabel, QGroupBox, QComboBox
)

from models import TableSchema
from repository import EntryRepository
from autosave import AutosaveManager
from ui_form import FormController
from ui_filters_sorts import FiltersSortsController
from ui_actions import ActionsController
from ui_files import FilesController


class MainWindow(QMainWindow):
    APP_TITLE = "Rejestr oprogramowania hala zachodnia"
    ALL = "(Wszystkie)"

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(self.APP_TITLE)
        self.resize(1300, 740)

        self.repo = EntryRepository()
        self.autosave_mgr = AutosaveManager(Path.cwd() / "autosave_json")

        root = QWidget()
        self.setCentralWidget(root)
        main_layout = QHBoxLayout(root)

        left = QVBoxLayout()
        main_layout.addLayout(left, 2)

        filters_bar = QHBoxLayout()
        filters_bar.addWidget(QLabel("Szukaj:"))
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("np. HMI, falownik.")
        filters_bar.addWidget(self.txt_search, 3)

        filters_bar.addWidget(QLabel("Typ maszyny:"))
        self.cmb_machine_filter = QComboBox()
        filters_bar.addWidget(self.cmb_machine_filter, 1)

        filters_bar.addWidget(QLabel("Rodzaj oprogramowania:"))
        self.cmb_software_filter = QComboBox()
        filters_bar.addWidget(self.cmb_software_filter, 1)

        self.btn_clear_filters = QPushButton("Wyczyść filtry")
        filters_bar.addWidget(self.btn_clear_filters)
        left.addLayout(filters_bar)

        sort_bar = QHBoxLayout()
        sort_bar.addWidget(QLabel("Sortuj po:"))
        self.cmb_sort_field = QComboBox()
        for label, _col in TableSchema.SORT_FIELDS:
            self.cmb_sort_field.addItem(label)
        sort_bar.addWidget(self.cmb_sort_field)

        self.cmb_sort_order = QComboBox()
        self.cmb_sort_order.addItems(["Rosnąco", "Malejąco"])
        sort_bar.addWidget(self.cmb_sort_order)

        self.btn_sort = QPushButton("Sortuj")
        sort_bar.addWidget(self.btn_sort)



        left.addLayout(sort_bar)

        self.table = QTableWidget(0, len(TableSchema.HEADERS))
        self.table.setHorizontalHeaderLabels(TableSchema.HEADERS)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setWordWrap(True)
        self.table.setSortingEnabled(True)

        left.addWidget(QLabel("Lista wpisów:"))
        left.addWidget(self.table)

        file_btns = QHBoxLayout()
        self.btn_new = QPushButton("Nowy wpis")
        self.btn_save_json = QPushButton("Zapisz JSON")
        self.btn_load_json = QPushButton("Wczytaj JSON")
        self.btn_export_csv = QPushButton("Eksport CSV")

        file_btns.addWidget(self.btn_new)
        file_btns.addStretch(1)
        file_btns.addWidget(self.btn_load_json)
        file_btns.addWidget(self.btn_save_json)
        file_btns.addWidget(self.btn_export_csv)
        left.addLayout(file_btns)

        right = QVBoxLayout()
        main_layout.addLayout(right, 1)

        form_group = QGroupBox("Szczegóły wpisu")
        right.addWidget(form_group)
        form = QFormLayout(form_group)

        # kolejność wymagana:
        self.txt_machine_type = QLineEdit()
        form.addRow("Typ maszyny:", self.txt_machine_type)

        self.txt_program_name = QLineEdit()
        form.addRow("Nazwa programu:", self.txt_program_name)

        self.txt_software_type = QLineEdit()
        form.addRow("Rodzaj oprogramowania:", self.txt_software_type)

        self.date_download = QDateEdit()
        self.date_download.setCalendarPopup(True)
        self.date_download.setDisplayFormat("yyyy-MM-dd")
        self.date_download.setDate(QDate.currentDate())
        form.addRow("Data pobrania:", self.date_download)

        self.date_upload = QDateEdit()
        self.date_upload.setCalendarPopup(True)
        self.date_upload.setDisplayFormat("yyyy-MM-dd")
        self.date_upload.setDate(QDate.currentDate())
        form.addRow("Data wgrania:", self.date_upload)

        self.txt_modified_by = QLineEdit()
        form.addRow("Kto modyfikował:", self.txt_modified_by)

        self.txt_ordered_by = QLineEdit()
        form.addRow("Na czyje polecenie:", self.txt_ordered_by)

        self.txt_tested_by = QLineEdit()
        form.addRow("Zmiany przetestowane przez:", self.txt_tested_by)

        self.txt_ordered_changes_description = QTextEdit()
        self.txt_ordered_changes_description.setPlaceholderText("Wpisz opis zleconych zmian...")
        form.addRow("Opis zleconych zmian:", self.txt_ordered_changes_description)

        self.txt_changes = QTextEdit()
        self.txt_changes.setPlaceholderText("Wpisz dokonane zmiany...")
        form.addRow("Dokonane zmiany:", self.txt_changes)

        self.btn_add_update = QPushButton("Dodaj wpis")
        right.addWidget(self.btn_add_update)
        right.addStretch(1)

        self.form_ctrl = FormController(
            self.txt_machine_type,
            self.txt_program_name,
            self.txt_software_type,
            self.date_download,
            self.date_upload,
            self.txt_modified_by,
            self.txt_ordered_by,
            self.txt_tested_by,
            self.txt_ordered_changes_description,
            self.txt_changes,
            msg_parent=self,
        )

        self.filters_ctrl = FiltersSortsController(
            repo=self.repo,
            txt_search=self.txt_search,
            cmb_machine_filter=self.cmb_machine_filter,
            cmb_software_filter=self.cmb_software_filter,
            cmb_sort_field=self.cmb_sort_field,
            cmb_sort_order=self.cmb_sort_order,
            table=self.table,
            all_token=self.ALL,
        )

        self.actions_ctrl = ActionsController(
            repo=self.repo,
            autosave=self.autosave_mgr,
            form=self.form_ctrl,
            filters_sorts=self.filters_ctrl,
            table=self.table,
            btn_add_update=self.btn_add_update,
            statusbar=self.statusBar(),
        )

        self.files_ctrl = FilesController(repo=self.repo, parent=self)

        loaded = self.autosave_mgr.load_latest()
        if loaded is not None:
            self.repo.set_all(loaded)
            self.statusBar().showMessage("Wczytano najnowszy autosave.")
        else:
            self.statusBar().showMessage(f"Autosave folder: {self.autosave_mgr.autosave_dir}")

        self.filters_ctrl.rebuild_filter_lists()
        self.actions_ctrl.refresh_table()

        # Signals
        self.txt_search.textChanged.connect(self.on_filters_changed)
        self.cmb_machine_filter.currentIndexChanged.connect(self.on_filters_changed)
        self.cmb_software_filter.currentIndexChanged.connect(self.on_filters_changed)
        self.btn_clear_filters.clicked.connect(self.on_clear_filters)

        self.btn_sort.clicked.connect(self.filters_ctrl.apply_sort)

        self.table.cellClicked.connect(lambda row, _col: self.actions_ctrl.row_selected(row))

        self.btn_new.clicked.connect(self.actions_ctrl.new_entry)
        self.btn_add_update.clicked.connect(self.actions_ctrl.add_or_update)

        self.btn_save_json.clicked.connect(self.files_ctrl.save_json_manual)
        self.btn_load_json.clicked.connect(self.on_load_json)
        self.btn_export_csv.clicked.connect(self.files_ctrl.export_csv)

    def on_filters_changed(self) -> None:
        self.actions_ctrl.selected_repo_index = None
        self.btn_add_update.setText("Dodaj wpis")
        self.actions_ctrl.refresh_table()

    def on_clear_filters(self) -> None:
        self.filters_ctrl.clear_filters()
        self.on_filters_changed()

    def on_load_json(self) -> None:
        ok = self.files_ctrl.load_json_manual()
        if ok:
            self.filters_ctrl.rebuild_filter_lists()
            self.actions_ctrl.refresh_table()
            self.actions_ctrl.new_entry()