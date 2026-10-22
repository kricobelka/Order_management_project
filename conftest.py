
import os
import pytest
import psycopg
from psycopg import sql
from dotenv import load_dotenv

# Загружаем переменные из .env (там должны быть настройки для DB_TEST_NAME)
load_dotenv()

test_db_name = os.getenv("DB_TEST_NAME")
main_db_name = os.getenv("DB_NAME")

if not test_db_name:
    raise RuntimeError("DB_TEST_NAME is not configured")

if test_db_name == main_db_name:
    raise RuntimeError("Test database must differ from the main database")

@pytest.fixture(scope="session")
def db_connection():
    """Фикстура создает подключение к ТЕСТОВОЙ БД и строит структуру таблиц"""
    
    with psycopg.connect(
        dbname=test_db_name,
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    ) as connection:
        
        # 1. Читаем ваш файл со всеми ограничениями и создаем таблицы в тест-БД
        with connection.cursor() as cursor:
            with open("database_schema.sql", "r", encoding="utf-8") as f:
                file_content = f.read()
            
            cursor.execute(sql.SQL(file_content)) # type: ignore
            
        # Передаем это подключение в сессию тестов (пауза)
        yield connection
        
        # 2. УБОРКА: Когда ВСЕ тесты завершатся, полностью удаляем таблицы из тест-БД
        with connection.cursor() as cursor:
            # !!! ВНИМАНИЕ: Перечислите здесь через запятую названия ВАШИХ таблиц !!!
            # Например: DROP TABLE IF EXISTS users, orders, products CASCADE;
            cursor.execute("DROP TABLE IF EXISTS customers, products, orders_new, order_items CASCADE;")
     


@pytest.fixture(autouse=True)
def clean_tables(db_connection):
    """
    Эта фикстура запускается АВТОМАТИЧЕСКИ перед каждым отдельным тестом.
    Она быстро стирает данные из таблиц, чтобы тесты были изолированными.
    """
    with db_connection.cursor() as cursor:
        # !!! ВНИМАНИЕ: Укажите здесь названия ваших таблиц !!!
        # TRUNCATE полностью опустошает таблицы, а RESTART IDENTITY сбрасывает счетчики ID на 1
        cursor.execute("TRUNCATE TABLE customers, products, orders_new, order_items RESTART IDENTITY CASCADE;")
        db_connection.commit()


