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


def add_check(url_id, status_code=None):
    """Добавить проверку. Возвращает ID созданной проверки"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO url_checks (url_id, status_code, created_at)
                VALUES (%s, %s, %s)
                RETURNING id
            ''', (url_id, status_code, datetime.now().date()))
            row = cur.fetchone()
        conn.commit()
        conn.close()
        return row[0]
    except Exception:
        conn.rollback()
        conn.close()
        return None


def get_checks_by_url_id(url_id):
    """Получить все проверки для URL"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT id, status_code, h1, title, description, created_at
            FROM url_checks
            WHERE url_id = %s
            ORDER BY id DESC
        ''', (url_id,))
        rows = cur.fetchall()
    conn.close()

    return [
        {
            'id': row[0],
            'status_code': row[1],
            'h1': row[2],
            'title': row[3],
            'description': row[4],
            'created_at': row[5]
        }
        for row in rows
    ]


def get_last_check_date(url_id):
    """Получить дату последней проверки для URL"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT MAX(created_at)
            FROM url_checks
            WHERE url_id = %s
        ''', (url_id,))
        row = cur.fetchone()
    conn.close()

    return row[0] if row else None


def get_urls_with_last_check():
    """Получить все URL с датой и статусом последней проверки"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT
                u.id,
                u.name,
                u.created_at,
                (SELECT created_at
                 FROM url_checks
                 WHERE url_id = u.id
                 ORDER BY id DESC LIMIT 1) as last_check,
                (SELECT status_code
                 FROM url_checks
                 WHERE url_id = u.id
                 ORDER BY id DESC LIMIT 1) as last_status_code
            FROM urls u
            ORDER BY u.id DESC
        ''')
        rows = cur.fetchall()
    conn.close()

    return [
        {
            'id': row[0],
            'name': row[1],
            'created_at': row[2],
            'last_check': row[3],
            'last_status_code': row[4]
        }
        for row in rows
    ]
