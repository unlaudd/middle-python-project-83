import psycopg
from .db import get_db_connection
from datetime import datetime


def get_all_urls():
    """Получить все URL, сортировка по убыванию ID (новые первыми)"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT id, name, created_at
            FROM urls
            ORDER BY id DESC
        ''')
        rows = cur.fetchall()
    conn.close()

    return [
        {'id': row[0], 'name': row[1], 'created_at': row[2]}
        for row in rows
    ]


def get_url_by_id(url_id):
    """Получить URL по ID"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT id, name, created_at
            FROM urls
            WHERE id = %s
        ''', (url_id,))
        row = cur.fetchone()
    conn.close()

    if row:
        return {'id': row[0], 'name': row[1], 'created_at': row[2]}
    return None


def add_url(name):
    """Добавить URL в базу данных. Возвращает ID добавленной записи или None"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id
            ''', (name, datetime.now().date()))
            row = cur.fetchone()
        conn.commit()
        conn.close()
        return row[0]
    except psycopg.errors.UniqueViolation:
        conn.rollback()
        conn.close()
        return None


def get_url_by_name(name):
    """Получить URL по имени"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT id, name, created_at
            FROM urls
            WHERE name = %s
        ''', (name,))
        row = cur.fetchone()
    conn.close()

    if row:
        return {'id': row[0], 'name': row[1], 'created_at': row[2]}
    return None
