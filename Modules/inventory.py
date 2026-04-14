import sqlite3
import pandas as pd

DB_NAME = "baiskeli.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

# ---------------- ADD PRODUCT ----------------
def add_product(name, category, subcategory, brand, size, description, cost_price, selling_price, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products 
        (name, category, subcategory, brand, size, description, cost_price, selling_price, quantity_in_stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, category, subcategory, brand, size, description, cost_price, selling_price, quantity))

    product_id = cursor.lastrowid

    # log inventory
    cursor.execute("""
        INSERT INTO inventory_logs (product_id, change, reason)
        VALUES (?, ?, ?)
    """, (product_id, quantity, "initial stock"))

    conn.commit()
    conn.close()

# ---------------- RESTOCK ----------------
def restock_product(product_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET quantity_in_stock = quantity_in_stock + ?
        WHERE id = ?
    """, (quantity, product_id))

    cursor.execute("""
        INSERT INTO inventory_logs (product_id, change, reason)
        VALUES (?, ?, ?)
    """, (product_id, quantity, "restock"))

    conn.commit()
    conn.close()

# ---------------- REDUCE STOCK ----------------
def reduce_stock(product_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT quantity_in_stock FROM products WHERE id = ?", (product_id,))
    result = cursor.fetchone()

    if not result:
        raise Exception("Product not found")

    if result[0] < quantity:
        raise Exception("Not enough stock")

    cursor.execute("""
        UPDATE products
        SET quantity_in_stock = quantity_in_stock - ?
        WHERE id = ?
    """, (quantity, product_id))

    cursor.execute("""
        INSERT INTO inventory_logs (product_id, change, reason)
        VALUES (?, ?, ?)
    """, (product_id, -quantity, "sale"))

    conn.commit()
    conn.close()

# ---------------- GET ALL PRODUCTS (DATAFRAME) ----------------
def get_all_products():
    conn = get_connection()

    query = """
        SELECT id, name, category, subcategory,
               brand, size, description,
               cost_price, selling_price,
               quantity_in_stock, reorder_level
        FROM products
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    df.columns = [
        "ID", "Name", "Category", "Subcategory",
        "Brand", "Size", "Description",
        "Cost Price", "Selling Price",
        "Stock", "Reorder Level"
    ]

    return df

# ---------------- LOW STOCK ----------------
def get_low_stock():
    conn = get_connection()

    query = """
        SELECT name, quantity_in_stock, reorder_level
        FROM products
        WHERE quantity_in_stock <= reorder_level
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df

# ---------------- UPDATE PRODUCT ----------------
def update_product(product_id, name, category, subcategory, brand, size, description, cost, price):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET name = ?, category = ?, subcategory = ?,
            brand = ?, size = ?, description = ?,
            cost_price = ?, selling_price = ?
        WHERE id = ?
    """, (name, category, subcategory, brand, size, description, cost, price, product_id))

    conn.commit()
    conn.close()

# ---------------- DELETE PRODUCT ----------------
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

    conn.commit()
    conn.close()