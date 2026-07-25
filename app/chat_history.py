import uuid

from database import get_connection


# ==========================================================
# Chat Session Functions
# ==========================================================

def create_session(title="New Chat"):
    """Create a new chat session."""

    session_id = str(uuid.uuid4())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_sessions (session_id, title)
        VALUES (?, ?)
        """,
        (session_id, title),
    )

    conn.commit()
    conn.close()

    return session_id


def get_all_sessions():
    """Return all chat sessions."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM chat_sessions
        ORDER BY created_at DESC
        """
    )

    sessions = cursor.fetchall()

    conn.close()

    return sessions


def cleanup_empty_sessions(active_session_id=None):
    """Delete any chat session that has no messages, except the currently active one."""
    conn = get_connection()
    cursor = conn.cursor()

    if active_session_id:
        cursor.execute(
            """
            DELETE FROM chat_sessions
            WHERE session_id NOT IN (SELECT DISTINCT session_id FROM chat_history)
            AND session_id != ?
            """,
            (active_session_id,)
        )
    else:
        cursor.execute(
            """
            DELETE FROM chat_sessions
            WHERE session_id NOT IN (SELECT DISTINCT session_id FROM chat_history)
            """
        )

    conn.commit()
    conn.close()


def rename_session(session_id, title):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE chat_sessions
        SET title = ?
        WHERE session_id = ?
        """,
        (title, session_id),
    )

    conn.commit()
    conn.close()


def delete_session(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM chat_sessions
        WHERE session_id = ?
        """,
        (session_id,),
    )

    conn.commit()
    conn.close()


# ==========================================================
# Message Functions
# ==========================================================

def save_message(session_id, role, message):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        (session_id, role, message)
        VALUES (?, ?, ?)
        """,
        (session_id, role, message),
    )

    conn.commit()
    conn.close()


def get_messages(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message, timestamp
        FROM chat_history
        WHERE session_id = ?
        ORDER BY id ASC
        """,
        (session_id,),
    )

    messages = cursor.fetchall()

    conn.close()

    return messages


def clear_messages(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM chat_history
        WHERE session_id = ?
        """,
        (session_id,),
    )

    conn.commit()
    conn.close()