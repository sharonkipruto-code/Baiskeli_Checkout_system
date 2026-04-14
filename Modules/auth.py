import sqlite3
import bcrypt

DB_NAME = "baiskeli.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- Initialize default users ---
def initialize_users():
    conn = get_connection()
    cursor = conn.cursor()

    # Ensure admin exists
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        hashed = bcrypt.hashpw("admin2026".encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("admin", hashed, "admin"))

    # Ensure cashier exists
    cursor.execute("SELECT * FROM users WHERE username='cashier'")
    if not cursor.fetchone():
        hashed = bcrypt.hashpw("cashier2026".encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("cashier", hashed, "cashier"))

    conn.commit()
    conn.close()

# --- Create new user (optional for future users) ---
def create_user(username, password, role="cashier"):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   (username, hashed, role))
    conn.commit()
    conn.close()

# --- Check login credentials ---
def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        stored_hash, role = row
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return {"username": username, "role": role}
    return None

def require_admin(user):
    if user["role"] != "admin":
        raise Exception("❌ Admin access only")

# --- Initialize default users on module load ---
create_users_table()
initialize_users()