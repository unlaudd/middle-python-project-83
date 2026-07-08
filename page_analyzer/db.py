"""
Database connection and initialization module.

This module handles the connection to the PostgreSQL database
using the DATABASE_URL environment variable. It also provides
a helper function to initialize the database schema locally.
"""

import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    """
    Establish and return a connection to the PostgreSQL database.

    Returns:
        psycopg.Connection: An active database connection instance.
    """
    return psycopg.connect(DATABASE_URL)


def init_db():
    """
    Initialize the database schema for local development.

    Creates the 'urls' and 'url_checks' tables if they do not
    already exist. In production, schema migrations are handled
    via the database.sql script during the build process.
    """
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
