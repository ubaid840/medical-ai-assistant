import sqlite3
import uuid
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "medical_ai.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# CREATE CHAT SESSION
# =====================================================

def create_session(title="New Chat"):

    session_id = str(uuid.uuid4())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_sessions(session_id, title)
        VALUES (?, ?)
        """,
        (session_id, title),
    )

    conn.commit()
    conn.close()

    return session_id


# =====================================================
# SAVE MESSAGE
# =====================================================

def save_message(session_id, role, message):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_messages(session_id, role, message)
        VALUES (?, ?, ?)
        """,
        (
            session_id,
            role,
            message,
        ),
    )

    conn.commit()
    conn.close()


# =====================================================
# GET ALL MESSAGES
# =====================================================

def get_messages(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM chat_messages
        WHERE session_id = ?
        ORDER BY created_at
        """,
        (session_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================================================
# GET ALL SESSIONS
# =====================================================

def get_all_sessions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM chat_sessions
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================================================
# DELETE SESSION
# =====================================================

def delete_session(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM chat_messages
        WHERE session_id = ?
        """,
        (session_id,),
    )

    cursor.execute(
        """
        DELETE FROM chat_sessions
        WHERE session_id = ?
        """,
        (session_id,),
    )

    conn.commit()
    conn.close()


# =====================================================
# GET SESSION TITLE
# =====================================================

def get_session_title(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title
        FROM chat_sessions
        WHERE session_id = ?
        """,
        (session_id,),
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["title"]

    return "New Chat"


# =====================================================
# UPDATE SESSION TITLE
# =====================================================

def update_session_title(session_id, title):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE chat_sessions
        SET title = ?
        WHERE session_id = ?
        """,
        (
            title,
            session_id,
        ),
    )

    conn.commit()
    conn.close()