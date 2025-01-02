from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

# Настройка логирования
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Создаем движок базы данных
DATABASE_URL = 'sqlite:///taskmanager.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

# Создаем локальную сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей
Base = declarative_base()

def create_tables():
    from app.models import User, Task  # Отложенный импорт
    Base.metadata.create_all(bind=engine)  # Создаем все таблицы

    # Проверяем, что таблицы созданы
    if 'users' in Base.metadata.tables:
        print("SQL для User:")
        print(str(Base.metadata.tables['users'].compile(engine)))
    else:
        print("Таблица 'users' не найдена.")

    if 'tasks' in Base.metadata.tables:
        print("\nSQL для Task:")
        print(str(Base.metadata.tables['tasks'].compile(engine)))
    else:
        print("Таблица 'tasks' не найдена.")

# Создание таблиц и вывод SQL-запросов
if __name__ == "__main__":
    create_tables()

