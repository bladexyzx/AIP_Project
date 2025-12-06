# app/storage.py
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://taskuser:taskpassword@localhost:5432/taskdb"
)


Base = declarative_base()



class EmptyUsernameError(Exception):
    """Логин не указан"""
    pass


class EmptyPasswordError(Exception):
    """Пароль пустой"""
    pass


class UserAlreadyExistsError(Exception):
    """Пользователь с таким логином уже существует"""
    pass


class UserNotFoundError(Exception):
    """Пользователь не найден"""
    pass


class WrongPasswordError(Exception):
    """Пароль не совпадает"""
    pass



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="tasks")

class Storage:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.create_all(self.engine)

        self.current_user = None

    # -------------------- АВТОРИЗАЦИЯ ------------------------
        

    def register_user(self, username: str, password: str) -> bool:
        username = username.strip()

        if not username:
            raise EmptyUsernameError("Имя пользователя не может быть пустым")

        if not password:
            raise EmptyPasswordError("Пароль не может быть пустым")

        with self.SessionLocal() as session:
            exists = session.query(User).filter_by(username=username).first()
            if exists:
                raise UserAlreadyExistsError(f"Пользователь '{username}' уже существует")

            user = User(username=username, password_hash=password)
            session.add(user)
            session.commit()
            return True

    def check_login(self, username: str, password: str) -> bool:
        with self.SessionLocal() as session:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return False

            if password == user.password_hash:
                return True


            return False

    # -------------------- РАБОТА С ЗАДАЧАМИ ------------------------

    def _get_user(self, session, username):
        return session.query(User).filter(User.username == username).one_or_none()

    def add_task(self, username, task):
        with self.SessionLocal() as session:
            user = self._get_user(session, username)
            if not user:
                return
            new_task = Task(user_id=user.id, description=task)
            session.add(new_task)
            session.commit()

    def get_tasks(self, username):
        with self.SessionLocal() as session:
            user = self._get_user(session, username)
            if not user:
                return []
            rows = session.query(Task).filter(
                Task.user_id == user.id, Task.completed == False
            ).all()
            return [r.description for r in rows]

    def delete_task(self, username, task):
        with self.SessionLocal() as session:
            user = self._get_user(session, username)
            if not user:
                return
            rows = session.query(Task).filter(
                Task.user_id == user.id,
                Task.description == task,
                Task.completed == False
            ).all()

            for r in rows:
                r.completed = True
                r.completed_at = datetime()

            session.commit()

    def get_completed_tasks(self, username):
        with self.SessionLocal() as session:
            user = self._get_user(session, username)
            if not user:
                return []
            rows = session.query(Task).filter(
                Task.user_id == user.id,
                Task.completed == True
            ).order_by(Task.completed_at).all()
            return [r.description for r in rows]
