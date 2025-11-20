class Storage:
    def __init__(self):
        self.current_user = None
        self.data = {}
        self.completed_tasks = {}  # <--- история выполненных задач

    def add_task(self, username, task):
        self.data.setdefault(username, [])
        self.data[username].append(task)

    def get_tasks(self, username):
        return self.data.get(username, [])

    def delete_task(self, username, task):
        if username in self.data:
            self.data[username] = [t for t in self.data[username] if t != task]
            # добавляем в историю
            self.completed_tasks.setdefault(username, [])
            self.completed_tasks[username].append(task)

    def get_completed_tasks(self, username):
        return self.completed_tasks.get(username, [])
