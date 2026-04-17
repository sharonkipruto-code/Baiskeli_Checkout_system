# import sqlite3
# import os

# DB_NAME = "Databases/baiskeli.db"

# def init_db():
#     conn = sqlite3.connect(DB_NAME)

#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     schema_path = os.path.join(base_dir, "schema.sql")

#     with open(schema_path, "r") as f:
#         conn.executescript(f.read())

#     conn.commit()
#     conn.close()

#     print("✅ Database created successfully!")

# # if __name__ == "__main__":
# #     init_db()

import os
import sqlite3

DB_NAME = "Databases/baiskeli.db"

def init_db():
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='products'
    """)

    if cursor.fetchone() is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(base_dir, "schema.sql")

        print("Using schema at:", schema_path)  # 👈 DEBUG

        with open(schema_path, "r") as f:
            sql = f.read()
            print("SCHEMA CONTENT:\n", sql)  # 👈 DEBUG
            conn.executescript(sql)

        print("✅ Database initialized")

    else:
        print("ℹ️ DB already exists")

    conn.commit()
    conn.close()