# app/ui_login.py
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from .ui_main import MainWindow
from .storage import Storage

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в Task Manager")
        self.resize(300, 200)
        self.storage = Storage()
        self.init_ui()

    def init_ui(self):
        self.label = QLabel("Введите логин:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            return
        # временно просто сохраняем имя пользователя
        self.storage.current_user = username
        # открываем главное окно
        self.main_window = MainWindow(self.storage)
        self.main_window.show()
        self.close()
