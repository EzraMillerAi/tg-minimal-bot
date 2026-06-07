import sqlite3


DB_NAME = "bot.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            city TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_settings (
            telegram_id INTEGER PRIMARY KEY,
            theme TEXT,
            notifications TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            role TEXT,
            message_text TEXT
        )
        """
    )

    cursor.execute("PRAGMA table_info(messages)")
    columns = [column[1] for column in cursor.fetchall()]

    if "role" not in columns:
        cursor.execute(
            """
            ALTER TABLE messages
            ADD COLUMN role TEXT DEFAULT 'user'
            """
        )

    connection.commit()
    connection.close()

def save_user_profile(telegram_id, name=None, age=None, city=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (telegram_id, name, age, city)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
            name = excluded.name,
            age = excluded.age,
            city = excluded.city
        """,
        (telegram_id, name, age, city),
    )

    connection.commit()
    connection.close()

def load_user_profile(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name, age, city
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

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
        WHERE telegram_id = ?
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

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

    connection.close()

    return rows

def save_user_settings(telegram_id, theme=None, notifications=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO user_settings (telegram_id, theme, notifications)
        VALUES (?, ?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
            theme = excluded.theme,
            notifications = excluded.notifications
        """,
        (telegram_id, theme, notifications),
    )

    connection.commit()
    connection.close()

def load_user_settings(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT theme, notifications
        FROM user_settings
        WHERE telegram_id = ?
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

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
        WHERE telegram_id = ?
        """,
        (telegram_id,),
    )

    row = cursor.fetchone()

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
        VALUES (?, ?, ?)
        """,
        (telegram_id, role, message_text),
    )

    connection.commit()
    connection.close()

def get_user_messages(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, message_text
        FROM messages
        WHERE telegram_id = ?
        ORDER BY id DESC
        LIMIT 5
        """,
        (telegram_id,),
    )

    rows = cursor.fetchall()

    connection.close()

    return rows

def get_messages_count(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM messages
        WHERE telegram_id = ?
        """,
        (telegram_id,),
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count    

def get_recent_messages_for_ai(telegram_id, limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, message_text
        FROM messages
        WHERE telegram_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (telegram_id, limit),
    )

    rows = cursor.fetchall()

    connection.close()

    rows.reverse()

    return [
        {
            "role": role,
            "content": message_text,
        }
        for role, message_text in rows
    ]

def clear_user_messages(telegram_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM messages
        WHERE telegram_id = ?
        """,
        (telegram_id,),
    )

    connection.commit()
    connection.close()
