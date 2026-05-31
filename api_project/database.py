import os
from collections.abc import Generator

import psycopg2
from psycopg2.extensions import connection as PgConnection
from dotenv import load_dotenv


load_dotenv()


def connect() -> PgConnection | None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL is not set; skipping database connection")
        return None

    try:
        connection = psycopg2.connect(database_url)
        print("Connected to database successfully")
        return connection
    except Exception as exc:
        print("Connection failed:", exc)
        return None


def get_db() -> Generator[PgConnection, None, None]:
    connection = connect()
    if connection is None:
        raise RuntimeError("Could not connect to the database")

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db() -> None:
    connection = connect()
    if connection is None:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price NUMERIC(10, 2) NOT NULL DEFAULT 0,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
            )
        connection.commit()
    finally:
        connection.close()
