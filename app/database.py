import sqlite3
from pathlib import Path

# ==========================================================
# Database Configuration
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "medical_ai.db"


# ==========================================================
# Database Connection
# ==========================================================

def get_connection():
    """Create and return a SQLite connection."""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================================
# Initialize Database
# ==========================================================

def initialize_database():
    """Create all required tables."""

    conn = get_connection()
    cursor = conn.cursor()

    # ----------------------------------------
    # Chat Sessions
    # ----------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT DEFAULT 'New Chat',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ----------------------------------------
    # Chat Messages
    # ----------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id)
                REFERENCES chat_sessions(session_id)
                ON DELETE CASCADE
        )
    """)

    # ----------------------------------------
    # Patient Profiles
    # ----------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            chronic_conditions TEXT,
            allergies TEXT,
            medications TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ----------------------------------------
    # Appointments (Scheduling & Intake)
    # ----------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            appointment_date TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'Scheduled',
            insurance_details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_id) REFERENCES patient_profiles(id) ON DELETE CASCADE
        )
    """)

    # ----------------------------------------
    # Care Routines (Medications & Follow-ups)
    # ----------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS care_routines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            task_type TEXT NOT NULL,
            description TEXT NOT NULL,
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_id) REFERENCES patient_profiles(id) ON DELETE CASCADE
        )
    """)

    # ----------------------------------------
    # HIPAA Audit Logs
    # ----------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            patient_id INTEGER,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# Utility
# ==========================================================

def database_exists():
    return DATABASE_PATH.exists()

def log_audit(action, patient_id=None, details=""):
    """Write an event to the HIPAA audit log."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audit_logs (action, patient_id, details) VALUES (?, ?, ?)", (action, patient_id, details))
    conn.commit()
    conn.close()


# ==========================================================
# Run Directly
# ==========================================================

if __name__ == "__main__":

    initialize_database()

    print("=" * 50)
    print(" Medical AI Assistant Database")
    print("=" * 50)
    print(f"Database Location : {DATABASE_PATH}")
    print("Status            : Initialized Successfully")
    print("=" * 50)