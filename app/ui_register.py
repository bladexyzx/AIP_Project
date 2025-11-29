# app/ui_register.py
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from .storage import Storage

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.resize(300, 250)
        self.storage = Storage()

        self.init_ui()

    def init_ui(self):
        self.label = QLabel("Создайте аккаунт")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.button = QPushButton("Зарегистрироваться")
        self.button.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        success = self.storage.register_user(username, password)

        if not success:
            QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")
            return

        QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
        self.close()
