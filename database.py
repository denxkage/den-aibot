import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
SQLITE_PATH = os.getenv("SQLITE_PATH", "deden_ai.db")

@contextmanager
def get_connection():
if DATABASE_URL:
import psycopg
from psycopg.rows import dict_row

    with psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
        connect_timeout=10,
    ) as conn:
        yield conn
else:
    conn = sqlite3.connect(
        SQLITE_PATH,
        timeout=10,
    )
    conn.row_factory = sqlite3.Row

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_database():
if DATABASE_URL:
statements = [
"""
CREATE TABLE IF NOT EXISTS users (
user_id BIGINT PRIMARY KEY,
username TEXT,
first_name TEXT,
created_at TEXT NOT NULL
)
""",
"""
CREATE TABLE IF NOT EXISTS messages (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
user_id BIGINT NOT NULL,
role TEXT NOT NULL,
content TEXT NOT NULL,
created_at TEXT NOT NULL
)
""",
"""
CREATE INDEX IF NOT EXISTS idx_messages_user
ON messages(user_id, id)
""",
"""
CREATE TABLE IF NOT EXISTS knowledge (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
question TEXT UNIQUE NOT NULL,
answer TEXT NOT NULL
)
""",
]
else:
statements = [
"""
CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY,
username TEXT,
first_name TEXT,
created_at TEXT NOT NULL
)
""",
"""
CREATE TABLE IF NOT EXISTS messages (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
role TEXT NOT NULL,
content TEXT NOT NULL,
created_at TEXT NOT NULL
)
""",
"""
CREATE INDEX IF NOT EXISTS idx_messages_user
ON messages(user_id, id)
""",
"""
CREATE TABLE IF NOT EXISTS knowledge (
id INTEGER PRIMARY KEY AUTOINCREMENT,
question TEXT UNIQUE NOT NULL,
answer TEXT NOT NULL
)
""",
]

with get_connection() as conn:
    for statement in statements:
        conn.execute(statement)

    initial_knowledge = [
        (
            "siapa kamu",
            "Aku Deden AI, asisten virtual berbasis AI.",
        ),
        (
            "apa kemampuanmu",
            "Aku bisa membantu menjawab pertanyaan, "
            "menerjemahkan bahasa, menjelaskan materi, "
            "dan membantu menulis.",
        ),
        (
            "siapa pembuatmu",
            "Aku adalah bot AI yang dikonfigurasi "
            "oleh pemilik bot ini.",
        ),
        (
            "bahasa indonesia",
            "Aku bisa berkomunikasi menggunakan "
            "bahasa Indonesia.",
        ),
    ]

    for question, answer in initial_knowledge:
        if DATABASE_URL:
            conn.execute(
                """
                INSERT INTO knowledge (question, answer)
                VALUES (%s, %s)
                ON CONFLICT (question) DO NOTHING
                """,
                (question, answer),
            )
        else:
            conn.execute(
                """
                INSERT OR IGNORE INTO knowledge
                (question, answer)
                VALUES (?, ?)
                """,
                (question, answer),
            )

def save_user(user):
now = datetime.now(timezone.utc).isoformat()

with get_connection() as conn:
    if DATABASE_URL:
        conn.execute(
            """
            INSERT INTO users
                (user_id, username, first_name, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name
            """,
            (user.id, user.username, user.first_name, now),
        )
    else:
        conn.execute(
            """
            INSERT INTO users
                (user_id, username, first_name, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name
            """,
            (user.id, user.username, user.first_name, now),
        )

def save_message(user_id, role, content):
now = datetime.now(timezone.utc).isoformat()

with get_connection() as conn:
    if DATABASE_URL:
        conn.execute(
            """
            INSERT INTO messages
                (user_id, role, content, created_at)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, role, content, now),
        )
    else:
        conn.execute(
            """
            INSERT INTO messages
                (user_id, role, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, role, content, now),
        )

def get_history(user_id, limit=12):
with get_connection() as conn:
if DATABASE_URL:
rows = conn.execute(
"""
SELECT role, content
FROM messages
WHERE user_id = %s
ORDER BY id DESC
LIMIT %s
""",
(user_id, limit),
).fetchall()
else:
rows = conn.execute(
"""
SELECT role, content
FROM messages
WHERE user_id = ?
ORDER BY id DESC
LIMIT ?
""",
(user_id, limit),
).fetchall()

return list(reversed(rows))

def get_knowledge():
with get_connection() as conn:
rows = conn.execute(
"""
SELECT question, answer
FROM knowledge
ORDER BY id
"""
).fetchall()

return rows

def reset_history(user_id):
with get_connection() as conn:
if DATABASE_URL:
conn.execute(
"DELETE FROM messages WHERE user_id = %s",
(user_id,),
)
else:
conn.execute(
"DELETE FROM messages WHERE user_id = ?",
(user_id,),
)
