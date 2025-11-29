from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                               QRadioButton, QCheckBox, QComboBox, QTextEdit, 
                               QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox)
import sys

class FormExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Form Example")
        self.setGeometry(100, 100, 400, 500)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Form Layout
        form_layout = QFormLayout()
        
        # Name
        self.name_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)
        
        # Email
        self.email_input = QLineEdit()
        form_layout.addRow("Email:", self.email_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_input)
        
        # Gender
        gender_layout = QHBoxLayout()
        self.gender_male = QRadioButton("Male")
        self.gender_male.setChecked(True)
        self.gender_female = QRadioButton("Female")
        gender_layout.addWidget(self.gender_male)
        gender_layout.addWidget(self.gender_female)
        form_layout.addRow("Gender:", gender_layout)
        
        # Subscribe
        self.subscribe_checkbox = QCheckBox("Subscribe to newsletter")
        form_layout.addRow("", self.subscribe_checkbox)
        
        # Country
        self.country_combo = QComboBox()
        self.country_combo.addItems(["Select", "USA", "India", "UK", "Canada"])
        form_layout.addRow("Country:", self.country_combo)
        
        # Comments
        self.comments_text = QTextEdit()
        form_layout.addRow("Comments:", self.comments_text)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_form)
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_form)
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def submit_form(self):
        gender = "Male" if self.gender_male.isChecked() else "Female"
        subscribe = "Yes" if self.subscribe_checkbox.isChecked() else "No"
        data = f"""
Name: {self.name_input.text()}
Email: {self.email_input.text()}
Password: {self.password_input.text()}
Gender: {gender}
Subscribe: {subscribe}
Country: {self.country_combo.currentText()}
Comments: {self.comments_text.toPlainText()}
"""
        QMessageBox.information(self, "Form Submitted", data)
    
    def reset_form(self):
        self.name_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.gender_male.setChecked(True)
        self.subscribe_checkbox.setChecked(False)
        self.country_combo.setCurrentIndex(0)
        self.comments_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormExample()
    window.show()
    sys.exit(app.exec())

