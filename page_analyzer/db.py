import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    """Получить соединение с базой данных"""
    return psycopg.connect(DATABASE_URL)


def init_db():
    """Инициализация базы данных (для локальной разработки)"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                created_at DATE DEFAULT CURRENT_DATE
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS url_checks (
                id SERIAL PRIMARY KEY,
                url_id INTEGER REFERENCES urls(id),
                status_code INTEGER,
                h1 TEXT,
                title TEXT,
                description TEXT,
                created_at DATE DEFAULT CURRENT_DATE
            )
        ''')
    conn.commit()
    conn.close()
