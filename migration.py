import sqlite3

def run_migrations():
    conn = sqlite3.connect("Databases/baiskeli.db")
    cursor = conn.cursor()

    # Example: add column safely
    cursor.execute("PRAGMA table_info(products)")
    columns = [col[1] for col in cursor.fetchall()]

    if "brand" not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN brand TEXT")

    if "description" not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN description TEXT")

    conn.commit()
    conn.close()