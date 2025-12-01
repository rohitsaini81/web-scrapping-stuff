import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt

# -------------------------------------
# TEMP DATA (replace with API later)
# -------------------------------------
temp_apps = [
    {"app_id": 1001, "name": "DrinkNow", "platform": "Android"},
    {"app_id": 1002, "name": "WhatsApp", "platform": "Android"},
    {"app_id": 1003, "name": "Instagram", "platform": "Android"},
    {"app_id": 1004, "name": "Snapchat", "platform": "Android"},
]

import requests

response_apps = requests.get("http://localhost:5000/api/apps")
apps = response_apps.json()




class AppListWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Apps List")
        self.setMinimumSize(600, 400)

        # Main container
        container = QWidget()
        layout = QVBoxLayout(container)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["App ID", "Name", "Platform"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only

        layout.addWidget(self.table)
        self.setCentralWidget(container)

        # Load temp data
        self.load_apps(apps)

    def load_apps(self, apps):
        """Load list of apps into the table."""
        self.table.setRowCount(len(apps))

        for row, app in enumerate(apps):
            self.table.setItem(row, 0, QTableWidgetItem(str(app["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(app["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(app["downloads"]))


# -------------------------------------
# RUN APP
# -------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppListWindow()
    window.show()
    sys.exit(app.exec())
