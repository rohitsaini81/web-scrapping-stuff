from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
import sys

def say_hello():
    QMessageBox.information(window, "Hello", "Welcome to PySide6 GUI!")

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("PySide6 Example")
window.setGeometry(100, 100, 300, 150)

layout = QVBoxLayout()

label = QLabel("Hello PySide6!")
layout.addWidget(label)

button = QPushButton("Click Me")
button.clicked.connect(say_hello)
layout.addWidget(button)

window.setLayout(layout)
window.show()
sys.exit(app.exec())

