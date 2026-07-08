"""
Database models and query functions for Page Analyzer.

This module provides functions to interact with the PostgreSQL database,
handling CRUD operations for URLs and their associated checks. All
database connections are managed through the db module.

Tables:
    urls: Stores analyzed URLs with their creation dates
    url_checks: Stores check results including status codes and SEO metadata
"""

import psycopg
from .db import get_db_connection
from datetime import datetime


def get_all_urls():
    """
    Retrieve all URLs from the database.

    Returns:
        list[dict]: List of URL records sorted by ID in descending order
                   (newest first). Each dict contains:
                   - id (int): URL ID
                   - name (str): URL address
                   - created_at (date): Creation date
    """
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
    """
    Retrieve a URL record by its ID.

    Args:
        url_id (int): The ID of the URL to retrieve.

    Returns:
        dict: URL record with id, name, and created_at fields,
             or None if not found.
    """
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
    """
    Add a new URL to the database.

    Args:
        name (str): The URL address to add.

    Returns:
        int: The ID of the newly created URL record,
            or None if the URL already exists (unique violation).
    """
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
    """
    Retrieve a URL record by its address.

    Args:
        name (str): The URL address to search for.

    Returns:
        dict: URL record with id, name, and created_at fields,
             or None if not found.
    """
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


def add_check(url_id, status_code=None, h1=None, title=None,
              description=None):
    """
    Add a new check record for a URL.

    Args:
        url_id (int): The ID of the URL being checked.
        status_code (int, optional): HTTP response status code.
        h1 (str, optional): Text content of the h1 tag.
        title (str, optional): Text content of the title tag.
        description (str, optional): Content of meta description tag.

    Returns:
        int: The ID of the newly created check record,
            or None if an error occurred.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (url_id, status_code, h1, title, description,
                  datetime.now().date()))
            row = cur.fetchone()
        conn.commit()
        conn.close()
        return row[0]
    except Exception:
        conn.rollback()
        conn.close()
        return None


def get_checks_by_url_id(url_id):
    """
    Retrieve all check records for a specific URL.

    Args:
        url_id (int): The ID of the URL to get checks for.

    Returns:
        list[dict]: List of check records sorted by ID in descending
                   order (newest first). Each dict contains:
                   - id (int): Check ID
                   - status_code (int): HTTP status code
                   - h1 (str): H1 tag content
                   - title (str): Title tag content
                   - description (str): Meta description content
                   - created_at (date): Check creation date
    """
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
    """
    Get the date of the most recent check for a URL.

    Args:
        url_id (int): The ID of the URL.

    Returns:
        date: The date of the last check, or None if no checks exist.
    """
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
    """
    Retrieve all URLs with their most recent check information.

    Returns:
        list[dict]: List of URL records with last check data,
                   sorted by ID in descending order. Each dict contains:
                   - id (int): URL ID
                   - name (str): URL address
                   - created_at (date): URL creation date
                   - last_check (date): Date of last check (or None)
                   - last_status_code (int): Status code of last
                     check (or None)
    """
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
