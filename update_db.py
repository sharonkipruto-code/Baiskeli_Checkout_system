import sqlite3

conn = sqlite3.connect("baiskeli.db")
cursor = conn.cursor()

# Get existing columns
cursor.execute("PRAGMA table_info(products)")
columns = [col[1] for col in cursor.fetchall()]

# Add missing columns safely
if "brand" not in columns:
    cursor.execute("ALTER TABLE products ADD COLUMN brand TEXT")

if "size" not in columns:
    cursor.execute("ALTER TABLE products ADD COLUMN size TEXT")

if "description" not in columns:
    cursor.execute("ALTER TABLE products ADD COLUMN description TEXT")

conn.commit()
conn.close()

print("✅ Database checked and updated successfully!")