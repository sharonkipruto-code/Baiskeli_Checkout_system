import sqlite3

conn = sqlite3.connect("baiskeli.db")
cursor = conn.cursor()

# Add type column
cursor.execute("ALTER TABLE sales ADD COLUMN type TEXT DEFAULT 'product'")

# Add reference_id column (for linking repairs)
cursor.execute("ALTER TABLE sales ADD COLUMN reference_id INTEGER")

conn.commit()
conn.close()