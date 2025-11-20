from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QMessageBox, QHBoxLayout

class MainWindow(QWidget):
    def __init__(self, storage):
        super().__init__()
        self.storage = storage
        self.setWindowTitle(f"Task Manager — {storage.current_user}")
        self.resize(500, 500)
        self.init_ui()
        self.load_tasks()
        self.load_completed_tasks()

    def init_ui(self):
        self.task_list = QListWidget()
        self.completed_list = QListWidget()  # <--- виджет для истории

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Описание задачи")

        self.add_button = QPushButton("Добавить задачу")
        self.add_button.clicked.connect(self.add_task)

        self.delete_button = QPushButton("Задача выполнена")
        self.delete_button.clicked.connect(self.delete_task)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Пользователь: {self.storage.current_user}"))
        layout.addWidget(self.task_input)
        layout.addWidget(self.add_button)
        layout.addWidget(QLabel("Текущие задачи:"))
        layout.addWidget(self.task_list)
        layout.addWidget(self.delete_button)
        layout.addWidget(QLabel("История выполненных задач:"))
        layout.addWidget(self.completed_list)

        self.setLayout(layout)

    def add_task(self):
        text = self.task_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Ошибка", "Введите описание задачи")
            return
        self.storage.add_task(self.storage.current_user, text)
        self.task_input.clear()
        self.load_tasks()

    def delete_task(self):
        current = self.task_list.currentItem()
        if current:
            self.storage.delete_task(self.storage.current_user, current.text())
            self.load_tasks()
            self.load_completed_tasks()  # обновляем историю
        else:
            QMessageBox.information(self, "Инфо", "Выберите задачу для выполнения")

    def load_tasks(self):
        self.task_list.clear()
        tasks = self.storage.get_tasks(self.storage.current_user)
        for t in tasks:
            self.task_list.addItem(t)

    def load_completed_tasks(self):
        self.completed_list.clear()
        completed = self.storage.get_completed_tasks(self.storage.current_user)
        for t in completed:
            self.completed_list.addItem(t)
