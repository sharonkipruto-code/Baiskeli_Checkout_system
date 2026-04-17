# import sqlite3
# from datetime import datetime

# DB_NAME = "Databases/baiskeli.db"

# def get_connection():
#     return sqlite3.connect(DB_NAME)

# def process_sale(cart_items, payment_method="cash"):
#     """
#     cart_items = [
#         {"product_id": 1, "quantity": 2},
#         {"product_id": 3, "quantity": 1}
#     ]
#     """
    
#     conn = get_connection()
#     cursor = conn.cursor()

#     total_amount = 0
#     detailed_items = []

#     # 🔍 Step 1: Validate + calculate total
#     for item in cart_items:
#         cursor.execute("""
#             SELECT name, selling_price, quantity_in_stock, category
#             FROM products
#             WHERE id = ?
#         """, (item["product_id"],))
        
#         product = cursor.fetchone()

#         if not product:
#             conn.close()
#             raise Exception(f"❌ Product ID {item['product_id']} not found")

#         name, price, stock, category = product

#         # 🚨 Check stock ONLY for non-services
#         if category != "service":
#             if stock < item["quantity"]:
#                 conn.close()
#                 raise Exception(f"❌ Not enough stock for {name}")

#         item_total = price * item["quantity"]
#         total_amount += item_total

#         detailed_items.append({
#             "product_id": item["product_id"],
#             "name": name,
#             "price": price,
#             "quantity": item["quantity"],
#             "item_total": item_total,
#             "category": category
#         })

#     # 💾 Step 2: Save sale
#     cursor.execute("""
#         INSERT INTO sales (total_amount, payment_method, created_at)
#         VALUES (?, ?, ?)
#     """, (total_amount, payment_method, datetime.now()))

#     sale_id = cursor.lastrowid

#     # 📦 Step 3: Save items + update stock
#     for item in detailed_items:
#         # Save sale item
#         cursor.execute("""
#             INSERT INTO sale_items (sale_id, product_id, quantity, price)
#             VALUES (?, ?, ?, ?)
#         """, (sale_id, item["product_id"], item["quantity"], item["price"]))

#         # Reduce stock ONLY if not service
#         if item["category"] != "service":
#             cursor.execute("""
#                 UPDATE products
#                 SET quantity_in_stock = quantity_in_stock - ?
#                 WHERE id = ?
#             """, (item["quantity"], item["product_id"]))

#             # log inventory
#             cursor.execute("""
#                 INSERT INTO inventory_logs (product_id, change, reason)
#                 VALUES (?, ?, ?)
#             """, (item["product_id"], -item["quantity"], "sale"))

#     conn.commit()
#     conn.close()

#     return sale_id, total_amount, detailed_items

# #simple receipt generator(text-based)
# def generate_receipt(sale_id, total, items):
#     receipt = "\n===== 🚴 BAISKELI CENTRE RECEIPT =====\n"
#     receipt += f"Sale ID: {sale_id}\n"
#     receipt += f"Date: {datetime.now()}\n"
#     receipt += "-------------------------------\n"

#     for item in items:
#         receipt += f"{item['name']} x{item['quantity']} = {item['item_total']}\n"

#     receipt += "-------------------------------\n"
#     receipt += f"TOTAL: {total}\n"
#     receipt += "Thank you for your business!\n"

#     return receipt

import sqlite3
from datetime import datetime

DB_NAME = "Databases/baiskeli.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def process_sale(cart_items, payment_method="cash", customer_name="Walk-in", discount=0.0, amount_paid=None):
    """
    cart_items = [{"product_id": 1, "quantity": 2}, ...]
    discount = amount discounted (KES)
    amount_paid = actual amount received from customer
    """
    conn = get_connection()
    cursor = conn.cursor()

    total_amount = 0
    detailed_items = []

    for item in cart_items:
        cursor.execute("""
            SELECT name, selling_price, quantity_in_stock, category
            FROM products WHERE id=?
        """, (item["product_id"],))
        product = cursor.fetchone()

        if not product:
            conn.close()
            raise Exception(f"Product ID {item['product_id']} not found")

        name, price, stock, category = product

        if category != "service":
            if stock < item["quantity"]:
                conn.close()
                raise Exception(f"Not enough stock for {name} (have {stock}, need {item['quantity']})")

        item_total = price * item["quantity"]
        total_amount += item_total

        detailed_items.append({
            "product_id": item["product_id"],
            "name": name,
            "price": price,
            "quantity": item["quantity"],
            "item_total": item_total,
            "category": category
        })

    # Apply discount
    final_amount = max(0, total_amount - discount)
    if amount_paid is None:
        amount_paid = final_amount

    cursor.execute("""
        INSERT INTO sales (total_amount, payment_method, created_at, customer_name, discount, amount_paid)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (final_amount, payment_method, datetime.now(), customer_name, discount, amount_paid))

    sale_id = cursor.lastrowid

    for item in detailed_items:
        cursor.execute("""
            INSERT INTO sale_items (sale_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (sale_id, item["product_id"], item["quantity"], item["price"]))

        if item["category"] != "service":
            cursor.execute("""
                UPDATE products SET quantity_in_stock = quantity_in_stock - ? WHERE id=?
            """, (item["quantity"], item["product_id"]))
            cursor.execute("""
                INSERT INTO inventory_logs (product_id, change, reason) VALUES (?, ?, ?)
            """, (item["product_id"], -item["quantity"], "sale"))

    conn.commit()
    conn.close()

    return sale_id, final_amount, detailed_items

def delete_sale(sale_id):
    """Admin only: reverse a sale and restore stock."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT product_id, quantity FROM sale_items WHERE sale_id=?", (sale_id,))
    items = cursor.fetchall()

    # Restore stock for each item
    for product_id, quantity in items:
        cursor.execute("SELECT category FROM products WHERE id=?", (product_id,))
        row = cursor.fetchone()
        if row and row[0] != "service":
            cursor.execute("""
                UPDATE products SET quantity_in_stock = quantity_in_stock + ? WHERE id=?
            """, (quantity, product_id))
            cursor.execute("""
                INSERT INTO inventory_logs (product_id, change, reason) VALUES (?, ?, ?)
            """, (product_id, quantity, "sale reversed"))

    cursor.execute("DELETE FROM sale_items WHERE sale_id=?", (sale_id,))
    cursor.execute("DELETE FROM sales WHERE id=?", (sale_id,))

    conn.commit()
    conn.close()
