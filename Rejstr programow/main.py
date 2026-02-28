from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


def main() -> None:
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()