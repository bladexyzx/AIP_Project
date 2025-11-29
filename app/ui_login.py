# app/ui_login.py
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from .ui_main import MainWindow
from .ui_register import RegisterWindow
from .storage import Storage

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.resize(300, 200)
        self.storage = Storage()

        self.init_ui()

    def init_ui(self):
        self.label = QLabel("Введите логин и пароль")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.open_register)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def open_register(self):
        self.reg_window = RegisterWindow()
        self.reg_window.show()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        ok = self.storage.check_login(username, password)
        if not ok:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
            return

        self.storage.current_user = username

        self.main_window = MainWindow(self.storage)
        self.main_window.show()
        self.close()
