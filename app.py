
# import streamlit as st
# import os

# st.set_page_config(
#     page_title="Baiskeli POS",
#     layout="wide"
# )

# #show logo and title in header
# if "user" not in st.session_state or st.session_state.user is None:
#     # LOGIN SCREEN → keep full header
#     col1, col2 = st.columns([1, 5])

#     with col1:
#         st.image("Assets/logo.png", width=100)

#     with col2:
#         st.title("Baiskeli POS System")

#     st.markdown("---")

# else:
#     # AFTER LOGIN → logo only on right
#     col1, col2 = st.columns([6, 1])

#     with col2:
#         st.image("Assets/logo.png", width=60)

#     st.markdown("---")
    
# from init_db import init_db

# # Only create DB if it doesn't exist
# if not os.path.exists("Databases/baiskeli.db"):
#     init_db()

# from Modules.auth import login, create_user
# from Modules.inventory import get_all_products, add_product, restock_product, update_product, delete_product
# from Modules.pos import process_sale, generate_receipt
# from Modules.analytics import get_sales_summary, get_daily_sales, get_top_products
# from Modules.repairs import create_repair, add_repair_item, get_repairs, update_repair_status, get_repair_items, get_repair_service_cost, record_repair_sale, get_repair_details
# from Modules.receipt import generate_pdf_receipt
# from Modules.parking import check_in, check_out, get_active_parking, get_parking_history
# from datetime import datetime
# from migration import run_migrations

# run_migrations()

# if "initialized" not in st.session_state:
#     st.session_state.initialized = True


# with st.sidebar:
#     st.image("Assets/logo.png", width=120)
#     st.markdown("## Baiskeli Centre")
#     st.markdown("🚲 POS System")
#     st.markdown("---")

#     if "user" in st.session_state and st.session_state.user:
#         st.success(f"Logged in as: {st.session_state.user['role']}")

#     st.markdown("### Navigation")


#     # if st.session_state.user and st.session_state.user["role"] == "admin":
#     #     if st.button("⚠️ Reset Database"):
#     #         os.remove("baiskeli.db")
#     #         init_db()
#     #         st.success("Database reset!")
#     #         st.rerun()


    
# # ---------------- SESSION STATE ----------------
# if "user" not in st.session_state:
#     st.session_state.user = None

# if "cart" not in st.session_state:
#     st.session_state.cart = []


# # ---------------- LOGIN ----------------
# def login_screen():
#     st.title("🔐 Hello Please Login")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         user = login(username, password)

#         if user:
#             st.session_state.user = user
#             st.success("Login successful")
#             st.rerun()
#         else:
#             st.error("Invalid username or password")


# def inventory_screen():
#     st.subheader("📦 Inventory")

#     df = get_all_products()

#     # --- SELECT PRODUCT ---
#     product_map = {
#         f"{row['Name']} (Stock: {row['Stock']})": row
#         for _, row in df.iterrows()
#     }

#     selected = st.selectbox("Select Product to Edit", list(product_map.keys()))
#     product = product_map[selected]

#     # --- EDIT FORM ---
#     st.markdown("### ✏️ Edit Product")

#     name = st.text_input("Name", value=product["Name"])
#     category = st.selectbox(
#         "Category",
#         ["bike", "accessory", "part", "service"],
#         index=["bike", "accessory", "part", "service"].index(product["Category"])
#     )
#     subcategory = st.text_input("Subcategory", value=product["Subcategory"])
#     cost = st.number_input("Cost Price", value=float(product["Cost Price"]))
#     price = st.number_input("Selling Price", value=float(product["Selling Price"]))
#     brand = st.text_input("Brand", value=product["Brand"])
#     size = st.text_input("Size", value=product["Size"])
#     description = st.text_area("Description", value=product["Description"])
    


#     col1, col2 = st.columns(2)

#     # --- UPDATE ---
#     if col1.button("💾 Update Product"):
#         update_product(
#             product["ID"],
#             name,
#             category,
#             subcategory,
#             brand,
#             size,
#             description,
#             cost,
#             price
#         )
#         st.success("Product updated!")
#         st.rerun()

#     # --- DELETE ----
#     confirm=col2.checkbox("Confirm delete", key=f"confirm_delete_{product['ID']}")
    
#     if confirm and col2.button("🗑 Delete Product"):
#         delete_product(product["ID"])
#         st.warning("Product deleted!")
#         st.rerun()

#     st.markdown("---")

#     # --- VIEW TABLE ---
#     st.subheader("📋 All Products")

#     # Hide cost price for cashier
#     if st.session_state.user["role"] != "admin":
#         df = df.drop(columns=["Cost Price"])

#     st.dataframe(df, use_container_width=True)

# def sales_history_screen():
#     st.subheader("📑 Sales History")

#     import pandas as pd
#     import sqlite3

#     conn = sqlite3.connect("Databases/baiskeli.db")

#     query = """
#     SELECT 
#         s.id AS sale_id,
#         s.created_at AS sale_date,
#         s.total_amount,
#         s.type,
#         r.customer_name,
#         r.bike_type
#     FROM sales s
#     LEFT JOIN repairs r 
#         ON s.reference_id = r.id AND s.type='repair'
#     ORDER BY s.created_at DESC
#     """

#     df = pd.read_sql_query(query, conn)
#     conn.close()

#     st.dataframe(df, use_container_width=True)

# def add_product_screen():
#     st.subheader("➕ Add Product")

#     name = st.text_input("Product Name")

#     category = st.selectbox(
#         "Category",
#         ["bike", "accessory", "part", "service"]
#     )

#     subcategory = st.text_input("Subcategory")

#     cost = st.number_input("Cost Price", min_value=0.0)
#     price = st.number_input("Selling Price", min_value=0.0)
#     qty = st.number_input("Initial Stock", min_value=0)
#     brand = st.text_input("Brand")
#     size = st.text_input("Size")
#     description = st.text_area("Description")

#     if st.button("Add Product"):
#         if name and price:
#             add_product(name, category, subcategory, brand, size, description, cost, price, qty)
#             st.success(f"{name} added successfully!")
#         else:
#             st.error("Please fill required fields")

# def restock_screen():
#     st.subheader("🔄 Restock Product")

#     df = get_all_products()

#     product_map = {
#         f"{row['Name']} (Stock: {row['Stock']})": row["ID"]
#         for _, row in df.iterrows()
#     }

#     selected = st.selectbox("Select Product", list(product_map.keys()))
#     qty = st.number_input("Quantity to Add", min_value=1)

#     if st.button("Restock"):
#         product_id = product_map[selected]
#         restock_product(product_id, qty)
#         st.success("Stock updated!")

# def create_user_screen():
#     st.subheader("👥 Create User")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     role = st.selectbox("Role", ["admin", "cashier"])

#     if st.button("Create User"):
#         if username and password:
#             create_user(username, password, role)
#             st.success("User created!")
#         else:
#             st.error("Fill all fields")


# # ---------------- POS ----------------
# def pos_screen():
#     st.title("💰 Checkout")

#     df = get_all_products()

#     # --- CREATE PRODUCT MAP FROM DATAFRAME ---
#     product_dict = {
#         f"{row['Name']} (KES {row['Selling Price']})": {
#             "id": row["ID"],
#             "name": row["Name"],
#             "price": row["Selling Price"],
#             "stock": row["Stock"]
#         }
#         for _, row in df.iterrows()
#     }
    

#     # --- ADD TO CART ---
#     st.subheader("🛒 Add Item")

#     col1, col2, col3 = st.columns([3, 1, 1])

#     selected = col1.selectbox("Product", list(product_dict.keys()))
#     qty = col2.number_input("Qty", min_value=1, value=1)

#     if col3.button("Add"):
#         product = product_dict[selected]

#         # Merge duplicates
#         found = False
#         for item in st.session_state.cart:
#             if item["product_id"] == product["id"]:
#                 item["quantity"] += qty
#                 found = True
#                 break

#         if not found:
#             st.session_state.cart.append({
#                 "product_id": product["id"],
#                 "name": product["name"],
#                 "price": product["price"],
#                 "quantity": qty
#             })

#         st.success(f"Added {product['name']}")

#     # --- CART DISPLAY ---
#     st.subheader("🧾 Cart")

#     if not st.session_state.cart:
#         st.info("Cart is empty")
#         return

#     total = 0

#     for i, item in enumerate(st.session_state.cart):
#         item_total = item["price"] * item["quantity"]
#         total += item_total

#         col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

#         col1.write(item["name"])
#         col2.write(item["quantity"])
#         col3.write(f"KES {item['price']}")
#         col4.write(f"KES {item_total}")

#         if col5.button("❌", key=f"remove_{i}"):
#             st.session_state.cart.pop(i)
#             st.rerun()

#     st.markdown("---")
#     st.subheader(f"💵 Total: KES {total}")

#     # --- CHECKOUT OPTIONS (must be outside the button block) ---
#     st.markdown("### 🧾 Checkout Details")
#     customer_name = st.text_input("Customer Name (optional)", key="pos_customer_name")
#     payment_method = st.selectbox("Payment Method", ["Cash", "M-Pesa", "Paybill"], key="pos_payment_method")

#     # --- CHECKOUT ---
#     if "last_receipt" not in st.session_state:
#         st.session_state.last_receipt = None

#     if st.button("✅ Checkout"):
#         try:
#             cart_items = [
#                 {"product_id": item["product_id"], "quantity": item["quantity"]}
#                 for item in st.session_state.cart
#             ]

#             sale_id, total, items = process_sale(cart_items)

#             pdf = generate_pdf_receipt(
#                 sale_id,
#                 items,
#                 total,
#                 customer_name if customer_name else "Walk-in",
#                 payment_method
#             )

#             st.session_state.last_receipt = {
#                 "pdf": pdf,
#                 "sale_id": sale_id,
#                 "filename": f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#             }
#             st.session_state.cart = []
#             st.success("✅ Sale completed!")

#         except Exception as e:
#             st.error(str(e))

#     # --- SHOW RECEIPT DOWNLOAD (persists after rerun) ---
#     if st.session_state.last_receipt:
#         st.download_button(
#             label="📄 Download Receipt",
#             data=st.session_state.last_receipt["pdf"],
#             file_name=st.session_state.last_receipt["filename"],
#             mime="application/pdf",
#             key="download_pos_receipt"
#         )
#         if st.button("🆕 New Sale"):
#             st.session_state.last_receipt = None
#             st.rerun()

# def repairs_screen():
#     st.subheader("🔧 Repairs Management")

#     tabs = st.tabs(["New Repair", "Manage Repairs"])

#     # ---------------- NEW REPAIR ----------------
#     with tabs[0]:
#         st.markdown("### ➕ Create Repair Job")

#         customer = st.text_input("Customer Name")
#         phone = st.text_input("Phone")
#         bike = st.text_input("Bike Type")
#         issue = st.text_area("Issue Description")
#         service_cost = st.number_input("Service Cost", min_value=0.0, format="%.2f")

#         if st.button("Create Repair"):
#             repair_id = create_repair(customer, phone, bike, issue, service_cost)
#             st.success(f"Repair created! ID: {repair_id}")
#             st.session_state.current_repair = repair_id
#             st.session_state.repair_parts = []  # Track parts added

#         # --- ADD PARTS ---
#         if "current_repair" in st.session_state:
#             st.markdown("### 🧩 Add Parts Used")

#             df = get_all_products()
#             product_map = {f"{row['Name']} (Stock: {row['Stock']})": row["ID"] for _, row in df.iterrows()}

#             selected = st.selectbox("Select Part", list(product_map.keys()))
#             qty = st.number_input(
#                 "Quantity", min_value=1, value=1, key=f"qty_{selected}"
#             )
#             price = st.number_input(
#                 "Price per Unit", min_value=0.0, value=0.0, format="%.2f", key=f"price_{selected}"
#             )

#             if st.button("Add Part"):
#                 part_id = product_map[selected]
#                 st.session_state.repair_parts.append({
#                     "part_id": part_id,
#                     "name": selected,
#                     "qty": qty,
#                     "price": price,
#                 })
#                 add_repair_item(st.session_state.current_repair, part_id, qty, price)
#                 st.success(f"Added {qty} x {selected} at {price:.2f} each")
#                 st.rerun()

#             # Show current parts summary
#             if st.session_state.repair_parts:
#                 st.markdown("#### 📝 Parts Added for this Repair")
#                 total_parts_cost = 0
#                 for idx, part in enumerate(st.session_state.repair_parts, 1):
#                     line_total = part["qty"] * part["price"]
#                     total_parts_cost += line_total
#                     st.write(f"{idx}. {part['name']} - Qty: {part['qty']} x {part['price']:.2f} = {line_total:.2f}")

#                 st.write(f"**Service Cost:** {service_cost:.2f}")
#                 st.write(f"**Total Cost:** {service_cost + total_parts_cost:.2f}")


#             if st.button("Generate Receipt"):
#                 st.markdown("### 🧾 Repair Receipt")
#                 st.write(f"**Customer:** {customer}")
#                 st.write(f"**Phone:** {phone}")
#                 st.write(f"**Bike:** {bike}")
#                 st.write(f"**Issue:** {issue}")
#                 st.write("---")
#                 st.markdown("#### Parts Used")
#                 total_parts_cost = 0
#                 for idx, part in enumerate(st.session_state.repair_parts, 1):
#                     line_total = part["qty"] * part["price"]
#                     total_parts_cost += line_total
#                     st.write(f"{idx}. {part['name']} - Qty: {part['qty']} x {part['price']:.2f} = {line_total:.2f}")
#                 st.write(f"**Service Cost:** {service_cost:.2f}")
#                 st.write(f"**Total Amount:** {service_cost + total_parts_cost:.2f}")
#     # ---------------- MANAGE REPAIRS ----------------
#     with tabs[1]:
#         st.markdown("### 📋 All Repairs")
#         df = get_repairs()
#         st.dataframe(df, use_container_width=True)

#         if not df.empty:
#             repair_id = st.selectbox("Select Repair ID", df["id"])
#             status = st.selectbox("Update Status", ["pending", "completed", "paid"])

#             if st.button("Update Status"):
#                 update_repair_status(repair_id, status)
#                 st.success("Status updated!")
#                 st.rerun()

#             # Fetch existing parts for the repair
#             existing_parts = get_repair_items(repair_id)  # Should return list of dicts with name, qty, price
#             st.markdown("### 🧩 Parts Used")
#             total_parts_cost = 0
#             for idx, part in enumerate(existing_parts, 1):
#                 line_total = part["qty"] * part["price"]
#                 total_parts_cost += line_total
#                 st.write(f"{idx}. {part['name']} - Qty: {part['qty']} x {part['price']:.2f} = {line_total:.2f}")

#             service_cost = get_repair_service_cost(repair_id)
#             st.write(f"**Service Cost:** {service_cost:.2f}")
#             st.write(f"**Total Cost:** {service_cost + total_parts_cost:.2f}")

#             # Optionally add more parts
#             st.markdown("### ➕ Add More Parts to Existing Repair")
#             df_parts = get_all_products()
#             product_map = {f"{row['Name']} (Stock: {row['Stock']})": row["ID"] for _, row in df_parts.iterrows()}
#             selected = st.selectbox("Select Part to Add", list(product_map.keys()), key="manage_select")
#             qty = st.number_input("Quantity", min_value=1, value=1, key=f"manage_qty_{selected}")
#             price = st.number_input("Price per Unit", min_value=0.0, value=0.0, format="%.2f", key=f"manage_price_{selected}")

#             if st.button("Add Part to Repair"):
#                 add_repair_item(repair_id, product_map[selected], qty, price)
#                 st.success(f"Added {qty} x {selected} at {price:.2f} each")
#                 st.rerun()

#             # if st.button("Mark as Paid"):
#             #     update_repair_status(repair_id, "paid")
#             #     record_repair_sale(repair_id)  # <-- record in sales history
#             #     st.success("Repair marked as paid and recorded in sales history!")
#             #     st.rerun()
#             st.markdown("### 💳 Checkout Repair")

#             repair_customer = st.text_input("Customer Name (optional)", key=f"repair_customer_{repair_id}")
#             repair_payment = st.selectbox("Payment Method", ["Cash", "M-Pesa", "Paybill"], key=f"repair_payment_{repair_id}")

#             if "last_repair_receipt" not in st.session_state:
#                 st.session_state.last_repair_receipt = None

#             if st.button("✅ Checkout Repair", key=f"checkout_{repair_id}"):

#                 # 1. Record sale
#                 record_repair_sale(repair_id)

#                 # 2. Update status
#                 update_repair_status(repair_id, "paid")

#                 # 3. Prepare receipt data
#                 parts = get_repair_items(repair_id)
#                 service_cost = get_repair_service_cost(repair_id)

#                 items = [
#                     {"name": p["name"], "quantity": p["qty"], "price": p["price"]}
#                     for p in parts
#                 ]

#                 total_parts = sum(p["qty"] * p["price"] for p in parts)
#                 total = total_parts + service_cost

#                 # 4. Add service fee as line item
#                 items.append({"name": "--- Service Fee ---", "quantity": 1, "price": service_cost})

#                 # 5. Pull bike + issue for repair receipt
#                 repair_details = get_repair_details(repair_id)

#                 # 6. Generate receipt
#                 pdf = generate_pdf_receipt(
#                     repair_id,
#                     items,
#                     total,
#                     repair_customer if repair_customer else "Walk-in",
#                     repair_payment,
#                     repair_info={
#                         "bike": repair_details.get("bike_type", ""),
#                         "issue": repair_details.get("issue", ""),
#                         "phone": repair_details.get("phone", "")
#                     }
#                 )

#                 st.session_state.last_repair_receipt = {
#                     "pdf": pdf,
#                     "repair_id": repair_id
#                 }
#                 st.success("✅ Repair checked out successfully!")

#             if st.session_state.get("last_repair_receipt") and \
#                st.session_state.last_repair_receipt["repair_id"] == repair_id:
#                 st.download_button(
#                     label="📄 Download Repair Receipt",
#                     data=st.session_state.last_repair_receipt["pdf"],
#                     file_name=f"repair_{repair_id}.pdf",
#                     mime="application/pdf",
#                     key=f"dl_repair_{repair_id}"
#                 )
#                 if st.button("🆕 New Repair", key=f"new_repair_{repair_id}"):
#                     st.session_state.last_repair_receipt = None
#                     st.rerun()


# # ---------------- PARKING ----------------
# def parking_screen():
#     st.subheader("🅿️ Bicycle Parking")

#     tabs = st.tabs(["Check In", "Check Out", "History"])

#     with tabs[0]:
#         st.markdown("### 🚲 New Check-In")
#         customer = st.text_input("Customer Name", key="park_customer")
#         bike_desc = st.text_input("Bike Description (colour, model)", key="park_bike")
#         daily_rate = st.number_input("Daily Rate (KES)", min_value=10.0, value=100.0, step=10.0)

#         if st.button("✅ Check In"):
#             if customer and bike_desc:
#                 pid = check_in(customer, bike_desc, daily_rate)
#                 st.success(f"Checked in! Parking ID: **{pid}**")
#                 st.info("Give the customer their Parking ID to use at check-out.")
#             else:
#                 st.error("Please fill customer name and bike description.")

#         st.markdown("---")
#         st.markdown("### 🟢 Currently Parked")
#         active = get_active_parking()
#         if active.empty:
#             st.info("No bikes currently parked.")
#         else:
#             st.dataframe(active, use_container_width=True)

#     with tabs[1]:
#         st.markdown("### 🏁 Check Out")
#         active = get_active_parking()

#         if active.empty:
#             st.info("No bikes currently parked.")
#         else:
#             options = {
#                 f"ID {row['id']} — {row['customer_name']} ({row['bike_description']})": row["id"]
#                 for _, row in active.iterrows()
#             }
#             selected = st.selectbox("Select Bike to Check Out", list(options.keys()))

#             if st.button("✅ Check Out & Calculate Fee"):
#                 pid = options[selected]
#                 try:
#                     fee, hours = check_out(pid)
#                     st.success(f"✅ Checked out after **{hours:.1f} hours**")
#                     st.metric("Fee Charged", f"KES {fee:.2f}")
#                 except Exception as e:
#                     st.error(str(e))

#     with tabs[2]:
#         st.markdown("### 📋 Parking History")
#         history = get_parking_history()
#         if history.empty:
#             st.info("No parking history yet.")
#         else:
#             st.dataframe(history, use_container_width=True)
#             total_earned = history["fee"].sum()
#             st.metric("Total Parking Revenue", f"KES {total_earned:.2f}")


# # ---------------- ADMIN ----------------
# def admin_screen():
#     st.markdown("## 🧑‍💼 Admin Dashboard")


#     tabs = st.tabs([
#         "Dashboard","Inventory", "Add Product", "Restock", 
#         "Checkout", "Sales History","Repairs","Parking","Create User"])

#     with tabs[0]:
#         menu = "Dashboard"
#         # Dashboard code here
#         st.subheader("📊 Sales Dashboard")
#         filter_type = st.selectbox(
#         "Select Period",
#         ["Today", "This Week", "This Month", "All"]
#     )
#         summary = get_sales_summary(filter_type)
#         col1, col2, col3 = st.columns(3)
#         col1.metric("💰 Revenue", f"KES {summary['total_revenue'] or 0}")
#         col2.metric("📈 Profit", f"KES {summary['total_profit'] or 0}")
#         col3.metric("🧾 Transactions", int(summary['total_transactions'] or 0))
#         st.markdown("---")
#         daily = get_daily_sales(filter_type)
#         if not daily.empty:
#             st.line_chart(daily.set_index("date"))
#         else:
#             st.info("No sales data yet")
#         st.markdown("---")

#         top_products = get_top_products(filter_type)
#         if not top_products.empty:
#             st.dataframe(top_products)
#         else:
#             st.info("No sales yet")

#     with tabs[1]:
       
#         menu = "Inventory"
#         st.subheader("📦 Inventory")
#         df = get_all_products()


#         # # --- SEARCH ---
#         search = st.text_input("🔍 Search product")
#         if search:
#             df = df[df["Name"].str.contains(search, case=False)]

#     # --- FILTER BY CATEGORY ---
#         category_filter = st.selectbox(
#             "Filter by Category",
#             ["All"] + sorted(df["Category"].dropna().unique().tolist())
#         )

#         if category_filter != "All":
#             df = df[df["Category"] == category_filter]

#     # --- LOW STOCK FILTER ---
#         if st.checkbox("⚠️ Show Low Stock Only"):
#             df = df[df["Stock"] <= df["Reorder Level"]]

#     # --- HIDE COST PRICE FOR NON-ADMIN (safety) ---
#         if st.session_state.user["role"] != "admin":
#             df = df.drop(columns=["Cost Price"])

#     # --- HIGHLIGHT LOW STOCK ---
#         def highlight_low_stock(row):
#             if row["Stock"] <= row["Reorder Level"]:
#                 return ["background-color: #ffcccc"] * len(row)
#             return [""] * len(row)

#         st.dataframe(
#             df.style.apply(highlight_low_stock, axis=1),
#             use_container_width=True
#         )

#     with tabs[2]:
#         menu = "Add Product"
#         st.subheader("➕ Add Product")
#         name = st.text_input("Name")
#         category = st.selectbox(
#             "Category",
#               ["bike", "accessory", "part", "service"])
#         subcategory = st.text_input("Subcategory")
#         brand = st.text_input("Brand(optional)")
#         size = st.text_input("Size(optional)")
#         description = st.text_area("Description(optional)")
#         cost = st.number_input("Cost Price")
#         price = st.number_input("Selling Price")
#         qty = st.number_input("Initial Quantity", min_value=0)
#         if st.button("Add Product"):
#                if name and price:
#                     add_product(
#                         name,
#                         category,
#                         subcategory,
#                         brand if brand else None,
#                         size if size else None,
#                         description if description else None,
#                         cost,
#                         price,
#                         qty
#                     )
#                     st.success(f"{name} added successfully!")
#         else:
#                 st.error("Please fill required fields")

#     with tabs[3]:
#         menu = "Restock"
#         st.subheader("🔄 Restock Product")
#         product_id = st.number_input("Product ID", min_value=1)
#         qty = st.number_input("Quantity", min_value=1)
#         if st.button("Restock"):
#             restock_product(product_id, qty)
#             st.success("Stock updated!")

#     with tabs[4]:
#         pos_screen()

#     with tabs[5]:
#         sales_history_screen()

#     with tabs[6]:
#         repairs_screen()

#     with tabs[7]:
#         parking_screen()

#     with tabs[8]:
#         menu = "Create User"
#         st.subheader("👥 Create User")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         role = st.selectbox("Role", ["admin", "cashier"])
#         if st.button("Create"):
#             create_user(username, password, role)
#             st.success("User created!")
    
    

# # ---------------- Cashier ----------------  
# def cashier_screen():
#     st.markdown("## 🧑‍💼 Cashier Dashboard")

#     tabs = st.tabs(["Checkout", "Inventory", "Repairs", "Parking"])

#     with tabs[0]:
#         menu = "Checkout"
#         pos_screen()

#     with tabs[1]:
#         menu = "Inventory"
#         st.subheader("📦 Inventory")
#         df = get_all_products()

#         # Hide cost price for cashier
#         if "Cost Price" in df.columns and st.session_state.user["role"] != "admin":
#             df = df.drop(columns=["Cost Price"])

#         st.dataframe(df, use_container_width=True)

#     with tabs[2]:
#         menu = "Repairs"
#         # st.subheader("🔧 Repairs Management")
#         repairs_screen()

#     with tabs[3]:
#         parking_screen()

# # ---------------- MAIN ----------------
# if st.session_state.user is None:
#     login_screen()
# else:
#     role = st.session_state.user["role"]

#     st.sidebar.write(f"Logged in as: {role}")

#     if role == "admin":
#         admin_screen()
#     else:
#         cashier_screen()

"""
app.py — Baiskeli Centre POS System
Run with: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import os
import sqlite3
from datetime import datetime

# ── Page config (MUST be first Streamlit call) ───────────────
st.set_page_config(
    page_title="Baiskeli Centre POS",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DB bootstrap ─────────────────────────────────────────────
os.makedirs("Databases", exist_ok=True)
os.makedirs("Backups", exist_ok=True)
os.makedirs("Assets", exist_ok=True)

if not os.path.exists("Databases/baiskeli.db"):
    from init_db import init_db
    init_db()

from migration import run_migrations
run_migrations()

# ── Module imports ────────────────────────────────────────────
from Modules.auth import (login, create_user, get_all_users,
                           deactivate_user, log_action, get_audit_logs,
                           change_password)
from Modules.inventory import (get_all_products, add_product, restock_product,
                                update_product, delete_product, get_inventory_log)
from Modules.pos import process_sale, delete_sale
from Modules.analytics import (get_sales_summary, get_daily_sales, get_monthly_sales,
                                get_top_products, get_category_breakdown,
                                get_payment_breakdown, get_repairs_summary,
                                get_parking_revenue, get_full_sales_history)
from Modules.repairs import (create_repair, add_repair_item, get_repairs,
                              update_repair_status, get_repair_items,
                              get_repair_service_cost, record_repair_sale,
                              get_repair_details, delete_repair)
from Modules.receipt import generate_pdf_receipt
from Modules.parking import check_in, check_out, get_active_parking, get_parking_history
from Modules.backup import backup_database, export_to_excel, list_backups, read_backup

# ── Session state defaults ────────────────────────────────────
for key, default in [
    ("user", None),
    ("cart", []),
    ("last_receipt", None),
    ("last_repair_receipt", None),
    ("current_repair", None),
    ("repair_parts", []),
    ("delete_confirm", {}),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def is_admin():
    return st.session_state.user and st.session_state.user["role"] == "admin"

def current_user():
    return st.session_state.user["username"] if st.session_state.user else "unknown"

def double_confirm(key, label, danger_label, action_fn, danger=True):
    """Two-step confirmation widget. Returns True if action was executed."""
    confirm_key = f"confirm_{key}"
    btn_class = "danger" if danger else "primary"
    if st.checkbox(f"✅ Confirm: {label}", key=confirm_key):
        if st.button(f"🗑️ {danger_label}", key=f"btn_{key}", type="primary"):
            action_fn()
            return True
    return False


# ─────────────────────────────────────────────────────────────
# LOGIN SCREEN
# ─────────────────────────────────────────────────────────────
def login_screen():
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if os.path.exists("Assets/logo.png"):
            st.image("Assets/logo.png", width=160)
        st.markdown("## 🔐 Baiskeli Centre POS")
        st.markdown("---")

        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        if st.button("Login", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("Please enter username and password.")
                return
            try:
                user = login(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")
            except Exception as e:
                st.error(str(e))

        st.markdown(
            "<div style='text-align:center;color:#999;font-size:12px;margin-top:20px;'>"
            "Baiskeli Centre © 2026</div>",
            unsafe_allow_html=True
        )


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        if os.path.exists("Assets/logo.png"):
            st.image("Assets/logo.png", width=100)
        st.markdown("### 🚴 Baiskeli Centre")
        st.markdown("---")

        if st.session_state.user:
            u = st.session_state.user
            st.success(f"👤 {u['username']}  |  {u['role'].upper()}")
            st.markdown("---")

            if st.button("🚪 Log Out", use_container_width=True):
                log_action(u["username"], "LOGOUT")
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        st.markdown("---")
        st.caption("Baiskeli Centre POS v2.0")
        st.caption(f"🕐 {datetime.now().strftime('%d %b %Y %H:%M')}")


# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────
def dashboard_screen():
    st.markdown("## 📊 Analytics Dashboard")

    filter_type = st.selectbox(
        "📅 Period",
        ["Today", "This Week", "This Month", "Last Month", "This Year", "All"],
        horizontal=True, key="dash_filter"
    )

    # ── KPI row ────────────────────────────────────────────
    summary  = get_sales_summary(filter_type)
    repairs  = get_repairs_summary(filter_type)
    parking  = get_parking_revenue(filter_type)

    revenue  = float(summary["total_revenue"] or 0)
    profit   = float(summary["total_profit"] or 0)
    txns     = int(summary["total_transactions"] or 0)
    units    = int(summary["total_units_sold"] or 0)
    disc     = float(summary["total_discounts"] or 0)
    margin   = (profit / revenue * 100) if revenue > 0 else 0

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("💰 Revenue",     f"KES {revenue:,.0f}")
    k2.metric("📈 Profit",      f"KES {profit:,.0f}")
    k3.metric("📊 Margin",      f"{margin:.1f}%")
    k4.metric("🧾 Transactions",str(txns))
    k5.metric("📦 Units Sold",  str(units))
    k6.metric("🎁 Discounts",   f"KES {disc:,.0f}")

    st.markdown("---")

    # ── Row 2: Repairs + Parking ───────────────────────────
    rc1, rc2, rc3, rc4, pc1, pc2 = st.columns(6)
    rc1.metric("🔧 Repairs Total", int(repairs["total_repairs"] or 0))
    rc2.metric("⏳ Pending",        int(repairs["pending"] or 0))
    rc3.metric("✅ Completed",      int(repairs["completed"] or 0))
    rc4.metric("💳 Paid",           int(repairs["paid"] or 0))
    pc1.metric("🅿️ Parking Sessions", int(parking["sessions"] or 0))
    pc2.metric("🅿️ Parking Revenue", f"KES {float(parking['revenue'] or 0):,.0f}")

    st.markdown("---")

    # ── Charts ─────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📈 Daily Revenue vs Profit")
        daily = get_daily_sales(filter_type)
        if not daily.empty:
            daily = daily.set_index("date")
            st.line_chart(daily[["revenue", "profit"]])
        else:
            st.info("No sales data for this period.")

    with col_b:
        st.subheader("🏷️ Revenue by Category")
        cat = get_category_breakdown(filter_type)
        if not cat.empty:
            st.bar_chart(cat.set_index("category")["revenue"])
        else:
            st.info("No category data.")

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("🏆 Top Products")
        top = get_top_products(filter_type, limit=10)
        if not top.empty:
            st.dataframe(top, use_container_width=True, hide_index=True)
        else:
            st.info("No product sales yet.")

    with col_d:
        st.subheader("💳 Payment Methods")
        pay = get_payment_breakdown(filter_type)
        if not pay.empty:
            st.dataframe(pay, use_container_width=True, hide_index=True)
        else:
            st.info("No payment data.")

    st.markdown("---")

    # ── Monthly trend ──────────────────────────────────────
    st.subheader("📆 Monthly Revenue & Profit Trend")
    monthly = get_monthly_sales()
    if not monthly.empty:
        st.bar_chart(monthly.set_index("month")[["revenue", "profit"]])
    else:
        st.info("No monthly data yet.")

    # ── Low stock alerts ───────────────────────────────────
    st.markdown("---")
    st.subheader("⚠️ Low Stock Alerts")
    all_products = get_all_products()
    low = all_products[all_products["Stock"] <= all_products["Reorder Level"]]
    if low.empty:
        st.success("All products are adequately stocked.")
    else:
        st.warning(f"{len(low)} product(s) below reorder level!")
        st.dataframe(low[["Name", "Category", "Stock", "Reorder Level"]],
                     use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────
# INVENTORY
# ─────────────────────────────────────────────────────────────
def inventory_screen():
    st.markdown("## 📦 Inventory Management")

    tab_view, tab_edit, tab_add, tab_restock, tab_log = st.tabs([
        "📋 View Stock", "✏️ Edit Product", "➕ Add Product",
        "🔄 Restock", "📜 Inventory Log"
    ])

    with tab_view:
        df = get_all_products()
        col1, col2, col3 = st.columns([3, 2, 2])
        search = col1.text_input("🔍 Search", placeholder="Type product name...")
        cat_opts = ["All"] + sorted(df["Category"].dropna().unique().tolist())
        cat_f = col2.selectbox("Category", cat_opts)
        low_only = col3.checkbox("⚠️ Low Stock Only")

        if search:
            df = df[df["Name"].str.contains(search, case=False, na=False)]
        if cat_f != "All":
            df = df[df["Category"] == cat_f]
        if low_only:
            df = df[df["Stock"] <= df["Reorder Level"]]

        # Hide cost price from cashier
        display_df = df.copy()
        if not is_admin():
            display_df = display_df.drop(columns=["Cost Price"])

        def highlight_low(row):
            if row["Stock"] <= row["Reorder Level"]:
                return ["background-color: #ffe0e0"] * len(row)
            return [""] * len(row)

        st.dataframe(
            display_df.style.apply(highlight_low, axis=1),
            use_container_width=True, hide_index=True
        )
        st.caption(f"Showing {len(display_df)} products")

    with tab_edit:
        if not is_admin():
            st.warning("Admin only.")
            return
        df = get_all_products()
        product_map = {f"{r['Name']} (ID:{r['ID']} | Stock:{r['Stock']})": r
                       for _, r in df.iterrows()}
        selected = st.selectbox("Select Product", list(product_map.keys()))
        p = product_map[selected]

        with st.form("edit_product_form"):
            c1, c2 = st.columns(2)
            name   = c1.text_input("Name", value=str(p["Name"]))
            category = c2.selectbox("Category", ["bike","accessory","part","service"],
                                    index=["bike","accessory","part","service"].index(
                                        p["Category"]) if p["Category"] in
                                        ["bike","accessory","part","service"] else 0)
            c3, c4 = st.columns(2)
            subcategory = c3.text_input("Subcategory", value=str(p["Subcategory"] or ""))
            brand       = c4.text_input("Brand",       value=str(p["Brand"] or ""))
            c5, c6 = st.columns(2)
            size    = c5.text_input("Size",   value=str(p["Size"] or ""))
            desc    = c6.text_input("Description", value=str(p["Description"] or ""))
            c7, c8 = st.columns(2)
            cost  = c7.number_input("Cost Price",    value=float(p["Cost Price"] or 0))
            price = c8.number_input("Selling Price", value=float(p["Selling Price"] or 0))

            submitted = st.form_submit_button("💾 Update Product", type="primary")
            if submitted:
                update_product(p["ID"], name, category, subcategory, brand, size, desc, cost, price)
                log_action(current_user(), "UPDATE_PRODUCT", f"id={p['ID']} name={name}")
                st.success(f"✅ {name} updated!")
                st.rerun()

        st.markdown("---")
        st.markdown("### 🗑️ Delete Product")
        st.warning("⚠️ Deleting removes the product from inventory. Sales history is preserved.")
        confirmed = st.checkbox(f"I confirm I want to permanently delete **{p['Name']}**",
                                key=f"del_prod_{p['ID']}")
        if confirmed:
            if st.button("🗑️ DELETE PRODUCT", type="primary", key="del_prod_btn"):
                delete_product(p["ID"])
                log_action(current_user(), "DELETE_PRODUCT", f"id={p['ID']} name={p['Name']}")
                st.success("Product deleted.")
                st.rerun()

    with tab_add:
        if not is_admin():
            st.warning("Admin only.")
            return
        with st.form("add_product_form"):
            c1, c2 = st.columns(2)
            name     = c1.text_input("Product Name *")
            category = c2.selectbox("Category *", ["bike","accessory","part","service"])
            c3, c4   = st.columns(2)
            subcategory = c3.text_input("Subcategory")
            brand    = c4.text_input("Brand")
            c5, c6   = st.columns(2)
            size     = c5.text_input("Size")
            desc     = c6.text_input("Description")
            c7, c8, c9 = st.columns(3)
            cost     = c7.number_input("Cost Price",    min_value=0.0)
            price    = c8.number_input("Selling Price *", min_value=0.0)
            qty      = c9.number_input("Initial Stock", min_value=0, step=1)

            if st.form_submit_button("➕ Add Product", type="primary"):
                if name and price:
                    add_product(name, category, subcategory or None, brand or None,
                                size or None, desc or None, cost, price, qty)
                    log_action(current_user(), "ADD_PRODUCT", f"name={name}")
                    st.success(f"✅ {name} added!")
                else:
                    st.error("Name and Selling Price are required.")

    with tab_restock:
        df = get_all_products()
        product_map2 = {f"{r['Name']} (Stock: {r['Stock']})": r["ID"]
                        for _, r in df.iterrows()}
        selected2 = st.selectbox("Select Product to Restock", list(product_map2.keys()))
        qty2 = st.number_input("Quantity to Add", min_value=1, step=1)
        if st.button("🔄 Restock", type="primary"):
            pid = product_map2[selected2]
            restock_product(pid, qty2)
            log_action(current_user(), "RESTOCK", f"product_id={pid} qty={qty2}")
            st.success(f"✅ Restocked {qty2} units!")

    with tab_log:
        if not is_admin():
            st.warning("Admin only.")
            return
        log_df = get_inventory_log()
        st.dataframe(log_df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────
# POS / CHECKOUT
# ─────────────────────────────────────────────────────────────
def pos_screen():
    st.markdown("## 💰 Checkout")

    df = get_all_products()
    product_dict = {
        f"{r['Name']} — KES {r['Selling Price']:,.0f}": {
            "id": r["ID"], "name": r["Name"],
            "price": r["Selling Price"], "stock": r["Stock"]
        }
        for _, r in df.iterrows()
    }

    # ── Add to cart ────────────────────────────────────────
    col1, col2, col3 = st.columns([4, 1, 1])
    selected = col1.selectbox("Product", list(product_dict.keys()))
    qty = col2.number_input("Qty", min_value=1, value=1, step=1)
    if col3.button("➕ Add", type="primary"):
        product = product_dict[selected]
        found = False
        for item in st.session_state.cart:
            if item["product_id"] == product["id"]:
                item["quantity"] += qty
                found = True
                break
        if not found:
            st.session_state.cart.append({
                "product_id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": qty
            })
        st.success(f"Added {product['name']}")
        st.rerun()

    # ── Cart display ───────────────────────────────────────
    st.markdown("---")
    st.subheader("🛒 Cart")

    if not st.session_state.cart:
        st.info("Cart is empty. Add items above.")
    else:
        subtotal = 0
        header = st.columns([4, 1, 2, 2, 1])
        header[0].markdown("**Product**")
        header[1].markdown("**Qty**")
        header[2].markdown("**Unit Price**")
        header[3].markdown("**Line Total**")
        header[4].markdown("**Remove**")

        for i, item in enumerate(st.session_state.cart):
            line = item["price"] * item["quantity"]
            subtotal += line
            c1, c2, c3, c4, c5 = st.columns([4, 1, 2, 2, 1])
            c1.write(item["name"])
            c2.write(item["quantity"])
            c3.write(f"KES {item['price']:,.2f}")
            c4.write(f"KES {line:,.2f}")
            if c5.button("❌", key=f"rm_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        st.markdown("---")

        # ── Checkout form ──────────────────────────────────
        st.subheader("🧾 Complete Sale")
        cf1, cf2 = st.columns(2)
        customer_name  = cf1.text_input("Customer Name", placeholder="Walk-in",
                                        key="pos_customer")
        payment_method = cf2.selectbox("Payment Method", ["Cash","M-Pesa","Paybill","Card"],
                                       key="pos_payment")

        df1, df2 = st.columns(2)
        discount   = df1.number_input("Discount (KES)", min_value=0.0, value=0.0,
                                      step=50.0, key="pos_discount")
        amount_paid = df2.number_input(
            "Amount Paid by Customer (KES)",
            min_value=0.0,
            value=float(subtotal - discount),
            step=50.0,
            key="pos_amount_paid",
            help="Enter actual cash/M-Pesa received"
        )

        final_total = max(0, subtotal - discount)
        change      = amount_paid - final_total

        tot1, tot2, tot3 = st.columns(3)
        tot1.metric("Subtotal",   f"KES {subtotal:,.2f}")
        tot2.metric("Discount",   f"KES {discount:,.2f}")
        tot3.metric("TOTAL",      f"KES {final_total:,.2f}")

        if change >= 0:
            st.info(f"💵 Change to give customer: **KES {change:,.2f}**")
        else:
            st.warning(f"⚠️ Short by KES {abs(change):,.2f}")

        if st.button("✅ Process Sale", type="primary", use_container_width=True):
            try:
                cart_items = [{"product_id": i["product_id"], "quantity": i["quantity"]}
                              for i in st.session_state.cart]
                cname = customer_name.strip() or "Walk-in"
                sale_id, total, items = process_sale(
                    cart_items, payment_method, cname, discount, amount_paid
                )
                pdf = generate_pdf_receipt(
                    sale_id, items, total, cname, payment_method,
                    discount=discount, amount_paid=amount_paid
                )
                st.session_state.last_receipt = {
                    "pdf": pdf,
                    "sale_id": sale_id,
                    "filename": f"receipt_{sale_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                }
                log_action(current_user(), "SALE", f"sale_id={sale_id} total={total}")
                st.session_state.cart = []
                st.success(f"✅ Sale #{sale_id} completed! Total: KES {total:,.2f}")
                st.rerun()
            except Exception as e:
                st.error(str(e))

    # ── Receipt download ──────────────────────────────────
    if st.session_state.last_receipt:
        st.success("🧾 Receipt ready!")
        st.download_button(
            label="📄 Download Receipt (PDF)",
            data=st.session_state.last_receipt["pdf"],
            file_name=st.session_state.last_receipt["filename"],
            mime="application/pdf",
            use_container_width=True
        )
        if st.button("🆕 New Sale"):
            st.session_state.last_receipt = None
            st.rerun()


# ─────────────────────────────────────────────────────────────
# SALES HISTORY
# ─────────────────────────────────────────────────────────────
def sales_history_screen():
    st.markdown("## 📑 Sales History")

    df = get_full_sales_history()

    if df.empty:
        st.info("No sales recorded yet.")
        return

    # Search/filter
    c1, c2 = st.columns(2)
    search = c1.text_input("🔍 Search customer")
    pay_f  = c2.selectbox("Payment Method", ["All"] +
                           sorted(df["payment_method"].dropna().unique().tolist()))

    if search:
        df = df[df["customer_name"].str.contains(search, case=False, na=False)]
    if pay_f != "All":
        df = df[df["payment_method"] == pay_f]

    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"{len(df)} sales shown | Total: KES {df['total_amount'].sum():,.2f}")

    # ── Delete sale (admin only) ───────────────────────────
    if is_admin():
        st.markdown("---")
        st.markdown("### 🗑️ Delete Sale (Admin)")
        st.warning("Deleting a sale will RESTORE stock for non-service items.")
        sale_ids = df["sale_id"].tolist()
        if sale_ids:
            del_id = st.selectbox("Select Sale ID to Delete", sale_ids,
                                  key="del_sale_select")
            confirmed = st.checkbox(f"I confirm deletion of Sale #{del_id}",
                                    key=f"confirm_del_sale_{del_id}")
            if confirmed:
                confirmed2 = st.checkbox("FINAL CHECK — This cannot be undone.",
                                         key=f"confirm2_del_sale_{del_id}")
                if confirmed2:
                    if st.button("🗑️ DELETE SALE", type="primary"):
                        delete_sale(del_id)
                        log_action(current_user(), "DELETE_SALE", f"sale_id={del_id}")
                        st.success(f"Sale #{del_id} deleted and stock restored.")
                        st.rerun()


# ─────────────────────────────────────────────────────────────
# REPAIRS
# ─────────────────────────────────────────────────────────────
def repairs_screen():
    st.markdown("## 🔧 Repairs Management")
    tab_new, tab_manage = st.tabs(["➕ New Repair", "📋 Manage Repairs"])

    # ── NEW REPAIR ─────────────────────────────────────────
    with tab_new:
        with st.form("new_repair_form"):
            c1, c2 = st.columns(2)
            customer = c1.text_input("Customer Name *")
            phone    = c2.text_input("Phone *")
            c3, c4   = st.columns(2)
            bike     = c3.text_input("Bike Type")
            service_cost = c4.number_input("Service Cost (KES)", min_value=0.0, format="%.2f")
            issue    = st.text_area("Issue Description")

            if st.form_submit_button("🔧 Create Repair Job", type="primary"):
                if customer and phone:
                    rid = create_repair(customer, phone, bike, issue, service_cost)
                    log_action(current_user(), "CREATE_REPAIR", f"id={rid} customer={customer}")
                    st.session_state.current_repair = rid
                    st.session_state.repair_parts = []
                    st.success(f"✅ Repair job created! ID: **{rid}**")
                else:
                    st.error("Customer name and phone are required.")

        # Parts for current repair
        if st.session_state.current_repair:
            rid = st.session_state.current_repair
            st.markdown(f"### 🧩 Add Parts — Repair #{rid}")

            df_prod = get_all_products()
            part_map = {f"{r['Name']} (Stock:{r['Stock']})": r["ID"]
                        for _, r in df_prod.iterrows()}

            with st.form("add_part_form"):
                pc1, pc2, pc3 = st.columns(3)
                part_sel = pc1.selectbox("Part", list(part_map.keys()))
                part_qty = pc2.number_input("Qty", min_value=1, value=1)
                part_price = pc3.number_input("Price/Unit", min_value=0.0, format="%.2f")

                if st.form_submit_button("➕ Add Part"):
                    try:
                        pid2 = part_map[part_sel]
                        add_repair_item(rid, pid2, part_qty, part_price)
                        st.session_state.repair_parts.append({
                            "name": part_sel, "qty": part_qty, "price": part_price
                        })
                        st.success(f"Added {part_sel}")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

            # Show added parts
            if st.session_state.repair_parts:
                st.markdown("#### Parts Added")
                for idx, part in enumerate(st.session_state.repair_parts, 1):
                    line = part["qty"] * part["price"]
                    st.write(f"{idx}. {part['name']} × {part['qty']} @ KES {part['price']:.2f} = KES {line:.2f}")

    # ── MANAGE REPAIRS ─────────────────────────────────────
    with tab_manage:
        df = get_repairs()
        if df.empty:
            st.info("No repair jobs yet.")
            return

        # Filter
        status_f = st.selectbox("Filter by Status",
                                 ["All","pending","completed","paid"],
                                 key="rep_status_filter")
        if status_f != "All":
            df = df[df["status"] == status_f]

        st.dataframe(df, use_container_width=True, hide_index=True)

        repair_id = st.selectbox("Select Repair ID", df["id"].tolist(), key="rep_select")

        # Status update
        col_s1, col_s2 = st.columns(2)
        new_status = col_s1.selectbox("Update Status", ["pending","completed","paid"],
                                       key="rep_new_status")
        if col_s2.button("✅ Update Status"):
            update_repair_status(repair_id, new_status)
            st.success("Status updated!")
            st.rerun()

        # Existing parts
        existing_parts = get_repair_items(repair_id)
        service_cost   = get_repair_service_cost(repair_id)
        total_parts    = sum(float(p["qty"]) * float(p["price"]) for p in existing_parts)
        total_repair   = total_parts + service_cost

        st.markdown(f"**Parts cost:** KES {total_parts:,.2f}  |  "
                    f"**Service:** KES {service_cost:,.2f}  |  "
                    f"**Total:** KES {total_repair:,.2f}")

        if existing_parts:
            for idx, p in enumerate(existing_parts, 1):
                st.write(f"{idx}. {p['name']} × {p['qty']} @ KES {p['price']:.2f}")

        # Add more parts
        with st.expander("➕ Add More Parts"):
            df_p = get_all_products()
            pm2 = {f"{r['Name']} (Stock:{r['Stock']})": r["ID"]
                   for _, r in df_p.iterrows()}
            with st.form("add_more_parts"):
                am1, am2, am3 = st.columns(3)
                am_sel = am1.selectbox("Part", list(pm2.keys()))
                am_qty = am2.number_input("Qty", min_value=1)
                am_price = am3.number_input("Price/Unit", min_value=0.0, format="%.2f")
                if st.form_submit_button("Add Part"):
                    try:
                        add_repair_item(repair_id, pm2[am_sel], am_qty, am_price)
                        st.success("Part added!")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

        # Checkout
        st.markdown("---")
        st.markdown("### 💳 Checkout Repair")
        rep_info = get_repair_details(repair_id)

        # Re-fetch totals after any additions
        existing_parts = get_repair_items(repair_id)
        service_cost   = get_repair_service_cost(repair_id)
        total_parts    = sum(float(p["qty"]) * float(p["price"]) for p in existing_parts)
        full_total     = total_parts + service_cost

        co1, co2 = st.columns(2)
        rep_customer = co1.text_input("Customer Name",
                                       value=rep_info.get("customer_name",""),
                                       key=f"rep_cust_{repair_id}")
        rep_payment  = co2.selectbox("Payment Method",
                                      ["Cash","M-Pesa","Paybill","Card"],
                                      key=f"rep_pay_{repair_id}")
        co3, co4 = st.columns(2)
        rep_discount  = co3.number_input("Discount (KES)", min_value=0.0,
                                          key=f"rep_disc_{repair_id}")
        rep_amt_paid  = co4.number_input("Amount Paid",
                                          value=float(full_total - co3),
                                          min_value=0.0,
                                          key=f"rep_paid_{repair_id}")

        final_repair_total = max(0, full_total - rep_discount)
        rep_change = rep_amt_paid - final_repair_total
        if rep_change >= 0:
            st.info(f"💵 Change: KES {rep_change:,.2f}")

        if "last_repair_receipt" not in st.session_state:
            st.session_state.last_repair_receipt = None

        if st.button("✅ Checkout Repair", type="primary", key=f"checkout_rep_{repair_id}"):
            try:
                record_repair_sale(repair_id, rep_payment, rep_discount, rep_amt_paid)
                update_repair_status(repair_id, "paid")
                log_action(current_user(), "REPAIR_CHECKOUT",
                           f"repair_id={repair_id} total={final_repair_total}")

                parts = get_repair_items(repair_id)
                items_for_receipt = [
                    {"name": p["name"], "quantity": p["qty"], "price": p["price"]}
                    for p in parts
                ]
                items_for_receipt.append(
                    {"name": "── Service Fee ──", "quantity": 1, "price": service_cost}
                )
                details = get_repair_details(repair_id)
                pdf = generate_pdf_receipt(
                    repair_id, items_for_receipt, final_repair_total,
                    rep_customer or "Walk-in", rep_payment,
                    discount=rep_discount, amount_paid=rep_amt_paid,
                    repair_info={
                        "bike": details.get("bike_type",""),
                        "issue": details.get("issue",""),
                        "phone": details.get("phone","")
                    }
                )
                st.session_state.last_repair_receipt = {
                    "pdf": pdf, "repair_id": repair_id
                }
                st.success("✅ Repair checked out!")
                st.rerun()
            except Exception as e:
                st.error(str(e))

        if (st.session_state.last_repair_receipt and
                st.session_state.last_repair_receipt["repair_id"] == repair_id):
            st.download_button(
                "📄 Download Repair Receipt",
                data=st.session_state.last_repair_receipt["pdf"],
                file_name=f"repair_receipt_{repair_id}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # Delete repair (admin)
        if is_admin():
            st.markdown("---")
            st.markdown("### 🗑️ Delete Repair")
            d1 = st.checkbox(f"Confirm delete Repair #{repair_id}",
                             key=f"del_rep1_{repair_id}")
            if d1:
                d2 = st.checkbox("FINAL CHECK — cannot be undone",
                                 key=f"del_rep2_{repair_id}")
                if d2 and st.button("🗑️ DELETE REPAIR", type="primary"):
                    delete_repair(repair_id)
                    log_action(current_user(), "DELETE_REPAIR", f"id={repair_id}")
                    st.success("Repair deleted.")
                    st.rerun()


# ─────────────────────────────────────────────────────────────
# PARKING
# ─────────────────────────────────────────────────────────────
def parking_screen():
    st.markdown("## 🅿️ Bicycle Parking")
    tab_in, tab_out, tab_hist = st.tabs(["Check In", "Check Out", "History"])

    with tab_in:
        with st.form("parking_checkin"):
            c1, c2 = st.columns(2)
            customer  = c1.text_input("Customer Name *")
            bike_desc = c2.text_input("Bike Description (colour/model) *")
            daily_rate = st.number_input("Daily Rate (KES)", min_value=10.0,
                                          value=100.0, step=10.0)
            if st.form_submit_button("✅ Check In", type="primary"):
                if customer and bike_desc:
                    pid = check_in(customer, bike_desc, daily_rate)
                    st.success(f"✅ Checked in! **Parking ID: {pid}** — give this to customer.")
                else:
                    st.error("Fill all required fields.")

        st.markdown("---")
        st.markdown("### 🟢 Currently Parked")
        active = get_active_parking()
        if active.empty:
            st.info("No bikes currently parked.")
        else:
            st.dataframe(active, use_container_width=True, hide_index=True)

    with tab_out:
        active = get_active_parking()
        if active.empty:
            st.info("No bikes currently parked.")
        else:
            options = {
                f"ID {r['id']} — {r['customer_name']} ({r['bike_description']})": r["id"]
                for _, r in active.iterrows()
            }
            selected = st.selectbox("Select Bike to Check Out", list(options.keys()))
            if st.button("✅ Check Out & Calculate Fee", type="primary"):
                pid = options[selected]
                try:
                    fee, hours = check_out(pid)
                    log_action(current_user(), "PARKING_CHECKOUT",
                               f"id={pid} fee={fee} hours={hours:.1f}")
                    st.success(f"✅ Checked out after **{hours:.1f} hours**")
                    st.metric("Fee Charged", f"KES {fee:,.2f}")
                except Exception as e:
                    st.error(str(e))

    with tab_hist:
        history = get_parking_history()
        if history.empty:
            st.info("No parking history yet.")
        else:
            st.dataframe(history, use_container_width=True, hide_index=True)
            st.metric("Total Parking Revenue", f"KES {history['fee'].sum():,.2f}")


# ─────────────────────────────────────────────────────────────
# ADMIN TOOLS
# ─────────────────────────────────────────────────────────────
def admin_tools_screen():
    st.markdown("## 🛠️ Admin Tools")

    tab_users, tab_backup, tab_audit, tab_pwd = st.tabs([
        "👥 Users", "💾 Backup & Export", "📋 Audit Log", "🔑 Change Password"
    ])

    with tab_users:
        st.subheader("All Users")
        df_users = get_all_users()
        st.dataframe(df_users, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Create New User")
        with st.form("create_user_form"):
            cu1, cu2, cu3 = st.columns(3)
            new_user = cu1.text_input("Username")
            new_pass = cu2.text_input("Password", type="password")
            new_role = cu3.selectbox("Role", ["cashier","admin"])
            if st.form_submit_button("➕ Create User", type="primary"):
                if new_user and new_pass:
                    try:
                        create_user(new_user, new_pass, new_role)
                        log_action(current_user(), "CREATE_USER",
                                   f"username={new_user} role={new_role}")
                        st.success(f"User {new_user} created!")
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.error("Fill all fields.")

        st.markdown("---")
        st.subheader("Deactivate User")
        all_u = get_all_users()
        active_users = all_u[all_u["username"] != current_user()]["username"].tolist()
        if active_users:
            deact_user = st.selectbox("Select User to Deactivate", active_users)
            if st.checkbox(f"Confirm deactivate {deact_user}"):
                if st.button("🚫 Deactivate", type="primary"):
                    deactivate_user(deact_user)
                    log_action(current_user(), "DEACTIVATE_USER", f"username={deact_user}")
                    st.success(f"{deact_user} deactivated.")
                    st.rerun()

    with tab_backup:
        st.subheader("💾 Database Backup")
        st.info("Backups are stored in the `Backups/` folder on the server. "
                "Only admins can download the backup file.")

        if st.button("📦 Create Backup Now", type="primary"):
            try:
                path = backup_database()
                log_action(current_user(), "BACKUP", f"path={path}")
                st.success(f"✅ Backup created: `{path}`")
            except Exception as e:
                st.error(str(e))

        backups = list_backups()
        if backups:
            st.markdown("### Existing Backups")
            st.write(backups)
            selected_backup = st.selectbox("Download a Backup", backups)
            if st.button("⬇️ Download Selected Backup"):
                data = read_backup(selected_backup)
                st.download_button(
                    "📥 Click to Download DB",
                    data=data,
                    file_name=selected_backup,
                    mime="application/octet-stream"
                )

        st.markdown("---")
        st.subheader("📊 Export to Excel")
        st.info("Exports all tables: Sales, Products, Repairs, Parking, Inventory Log.")
        if st.button("📊 Generate Excel Export", type="primary"):
            try:
                excel_buf = export_to_excel()
                log_action(current_user(), "EXPORT_EXCEL")
                st.download_button(
                    "⬇️ Download Excel",
                    data=excel_buf,
                    file_name=f"baiskeli_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(str(e))

    with tab_audit:
        st.subheader("📋 Audit Log")
        st.caption("All sensitive actions are logged here.")
        audit_df = get_audit_logs()
        st.dataframe(audit_df, use_container_width=True, hide_index=True)

    with tab_pwd:
        st.subheader("🔑 Change Your Password")
        with st.form("change_pwd_form"):
            old_pwd = st.text_input("Current Password", type="password")
            new_pwd = st.text_input("New Password", type="password")
            confirm_pwd = st.text_input("Confirm New Password", type="password")
            if st.form_submit_button("🔑 Change Password", type="primary"):
                if new_pwd != confirm_pwd:
                    st.error("New passwords do not match.")
                elif len(new_pwd) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        change_password(current_user(), old_pwd, new_pwd)
                        log_action(current_user(), "CHANGE_PASSWORD")
                        st.success("Password changed successfully!")
                    except Exception as e:
                        st.error(str(e))


# ─────────────────────────────────────────────────────────────
# MAIN SCREENS
# ─────────────────────────────────────────────────────────────
def admin_screen():
    tabs = st.tabs([
        "📊 Dashboard", "📦 Inventory", "💰 Checkout",
        "📑 Sales History", "🔧 Repairs", "🅿️ Parking", "🛠️ Admin Tools"
    ])
    with tabs[0]: dashboard_screen()
    with tabs[1]: inventory_screen()
    with tabs[2]: pos_screen()
    with tabs[3]: sales_history_screen()
    with tabs[4]: repairs_screen()
    with tabs[5]: parking_screen()
    with tabs[6]: admin_tools_screen()


def cashier_screen():
    tabs = st.tabs(["💰 Checkout", "📦 Inventory", "🔧 Repairs", "🅿️ Parking"])
    with tabs[0]: pos_screen()
    with tabs[1]:
        # Cashier sees inventory but not cost prices, cannot edit
        st.markdown("## 📦 Inventory")
        df = get_all_products()
        if "Cost Price" in df.columns:
            df = df.drop(columns=["Cost Price"])
        search = st.text_input("🔍 Search")
        if search:
            df = df[df["Name"].str.contains(search, case=False, na=False)]
        st.dataframe(df, use_container_width=True, hide_index=True)
    with tabs[2]: repairs_screen()
    with tabs[3]: parking_screen()


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────
render_sidebar()

if st.session_state.user is None:
    login_screen()
else:
    role = st.session_state.user["role"]
    if role == "admin":
        admin_screen()
    else:
        cashier_screen()
