import sqlite3
from datetime import datetime

DB_NAME = "Databases/baiskeli.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def process_sale(cart_items, payment_method="cash"):
    """
    cart_items = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 3, "quantity": 1}
    ]
    """
    
    conn = get_connection()
    cursor = conn.cursor()

    total_amount = 0
    detailed_items = []

    # 🔍 Step 1: Validate + calculate total
    for item in cart_items:
        cursor.execute("""
            SELECT name, selling_price, quantity_in_stock, category
            FROM products
            WHERE id = ?
        """, (item["product_id"],))
        
        product = cursor.fetchone()

        if not product:
            conn.close()
            raise Exception(f"❌ Product ID {item['product_id']} not found")

        name, price, stock, category = product

        # 🚨 Check stock ONLY for non-services
        if category != "service":
            if stock < item["quantity"]:
                conn.close()
                raise Exception(f"❌ Not enough stock for {name}")

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

    # 💾 Step 2: Save sale
    cursor.execute("""
        INSERT INTO sales (total_amount, payment_method, created_at)
        VALUES (?, ?, ?)
    """, (total_amount, payment_method, datetime.now()))

    sale_id = cursor.lastrowid

    # 📦 Step 3: Save items + update stock
    for item in detailed_items:
        # Save sale item
        cursor.execute("""
            INSERT INTO sale_items (sale_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (sale_id, item["product_id"], item["quantity"], item["price"]))

        # Reduce stock ONLY if not service
        if item["category"] != "service":
            cursor.execute("""
                UPDATE products
                SET quantity_in_stock = quantity_in_stock - ?
                WHERE id = ?
            """, (item["quantity"], item["product_id"]))

            # log inventory
            cursor.execute("""
                INSERT INTO inventory_logs (product_id, change, reason)
                VALUES (?, ?, ?)
            """, (item["product_id"], -item["quantity"], "sale"))

    conn.commit()
    conn.close()

    return sale_id, total_amount, detailed_items

#simple receipt generator(text-based)
def generate_receipt(sale_id, total, items):
    receipt = "\n===== 🚴 BAISKELI CENTRE RECEIPT =====\n"
    receipt += f"Sale ID: {sale_id}\n"
    receipt += f"Date: {datetime.now()}\n"
    receipt += "-------------------------------\n"

    for item in items:
        receipt += f"{item['name']} x{item['quantity']} = {item['item_total']}\n"

    receipt += "-------------------------------\n"
    receipt += f"TOTAL: {total}\n"
    receipt += "Thank you for your business!\n"

    return receipt