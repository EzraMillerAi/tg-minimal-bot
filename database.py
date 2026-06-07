import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL отсутствует в переменных окружения")

    return psycopg2.connect(DATABASE_URL)


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            city TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_settings (
            telegram_id BIGINT PRIMARY KEY,
            theme TEXT,
            notifications TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT,
            role TEXT,
            message_text TEXT
        )
        """
    )

    connection.commit()
    cursor.close()
    connection.close()


def save_user_profile(telegram_id, name=None, age=None, city=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (telegram_id, name, age, city)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (telegram_id) DO UPDATE SET
            name = EXCLUDED.name,
            age = EXCLUDED.age,
            city = EXCLUDED.city
        """,
        (telegram_id, name, age, city),
    )

    connection.commit()
    cursor.close()
    connection.close()


def load_user_profile(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name, age, city
        FROM users
        WHERE telegram_id = %s
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return None

    return {
        "name": row[0],
        "age": row[1],
        "city": row[2],
    }


def get_user_profile(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT telegram_id, name, age, city
        FROM users
        WHERE telegram_id = %s
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row


def get_all_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT telegram_id, name, age, city
        FROM users
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def save_user_settings(telegram_id, theme=None, notifications=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO user_settings (telegram_id, theme, notifications)
        VALUES (%s, %s, %s)
        ON CONFLICT (telegram_id) DO UPDATE SET
            theme = EXCLUDED.theme,
            notifications = EXCLUDED.notifications
        """,
        (telegram_id, theme, notifications),
    )

    connection.commit()
    cursor.close()
    connection.close()


def load_user_settings(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT theme, notifications
        FROM user_settings
        WHERE telegram_id = %s
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return None

    return {
        "theme": row[0],
        "notifications": row[1],
    }


def get_user_settings(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT theme, notifications
        FROM user_settings
        WHERE telegram_id = %s
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row


def save_message(telegram_id, message_text, role="user"):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            telegram_id,
            role,
            message_text
        )
        VALUES (%s, %s, %s)
        """,
        (telegram_id, role, message_text),
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_user_messages(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, message_text
        FROM messages
        WHERE telegram_id = %s
        ORDER BY id DESC
        LIMIT 5
        """,
        (telegram_id,),
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def get_recent_messages_for_ai(telegram_id, limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, message_text
        FROM messages
        WHERE telegram_id = %s
        ORDER BY id DESC
        LIMIT %s
        """,
        (telegram_id, limit),
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    rows.reverse()

    return [
        {
            "role": role,
            "content": message_text,
        }
        for role, message_text in rows
    ]


def get_messages_count(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM messages
        WHERE telegram_id = %s
        """,
        (telegram_id,),
    )

    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return count


def clear_user_messages(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM messages
        WHERE telegram_id = %s
        """,
        (telegram_id,),
    )

    connection.commit()
    cursor.close()
    connection.close()