import streamlit as st

st.set_page_config(
    page_title="Baiskeli POS",
    layout="wide"
)
#show logo and title in header
col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo.jpeg", width=100)

with col2:
    st.title("Baiskeli POS System")

st.markdown("---")


from auth import login, create_user
from inventory import get_all_products, add_product, restock_product, update_product, delete_product
from pos import process_sale, generate_receipt
from analytics import get_sales_summary, get_daily_sales, get_top_products
from repairs import create_repair, add_repair_item, get_repairs, update_repair_status,get_repair_items,get_repair_service_cost, record_repair_sale
from receipt import generate_pdf_receipt
from parking import check_in, check_out, get_active_parking, get_parking_history
from datetime import datetime

if "initialized" not in st.session_state:
    st.session_state.initialized = True


# with st.sidebar:
#     st.image("logo.jpeg", width=100)
#     st.markdown("### Baiskeli POS")
#     st.markdown("---")
    
# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "cart" not in st.session_state:
    st.session_state.cart = []


# ---------------- LOGIN ----------------
def login_screen():
    st.title("🔐 Hello Please Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(username, password)

        if user:
            st.session_state.user = user
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")


def inventory_screen():
    st.subheader("📦 Inventory")

    df = get_all_products()

    # --- SELECT PRODUCT ---
    product_map = {
        f"{row['Name']} (Stock: {row['Stock']})": row
        for _, row in df.iterrows()
    }

    selected = st.selectbox("Select Product to Edit", list(product_map.keys()))
    product = product_map[selected]

    # --- EDIT FORM ---
    st.markdown("### ✏️ Edit Product")

    name = st.text_input("Name", value=product["Name"])
    category = st.selectbox(
        "Category",
        ["bike", "accessory", "part", "service"],
        index=["bike", "accessory", "part", "service"].index(product["Category"])
    )
    subcategory = st.text_input("Subcategory", value=product["Subcategory"])
    cost = st.number_input("Cost Price", value=float(product["Cost Price"]))
    price = st.number_input("Selling Price", value=float(product["Selling Price"]))
    brand = st.text_input("Brand", value=product["Brand"])
    size = st.text_input("Size", value=product["Size"])
    description = st.text_area("Description", value=product["Description"])
    


    col1, col2 = st.columns(2)

    # --- UPDATE ---
    if col1.button("💾 Update Product"):
        update_product(
            product["ID"],
            name,
            category,
            subcategory,
            brand,
            size,
            description,
            cost,
            price
        )
        st.success("Product updated!")
        st.rerun()

    # --- DELETE ----
    confirm=col2.checkbox("Confirm delete", key=f"confirm_delete_{product['ID']}")
    
    if confirm and col2.button("🗑 Delete Product"):
        delete_product(product["ID"])
        st.warning("Product deleted!")
        st.rerun()

    st.markdown("---")

    # --- VIEW TABLE ---
    st.subheader("📋 All Products")

    # Hide cost price for cashier
    if st.session_state.user["role"] != "admin":
        df = df.drop(columns=["Cost Price"])

    st.dataframe(df, use_container_width=True)

def sales_history_screen():
    st.subheader("📑 Sales History")

    import pandas as pd
    import sqlite3

    conn = sqlite3.connect("baiskeli.db")

    query = """
    SELECT 
        s.id AS sale_id,
        s.created_at AS sale_date,
        s.total_amount,
        s.type,
        r.customer_name,
        r.bike_type
    FROM sales s
    LEFT JOIN repairs r 
        ON s.reference_id = r.id AND s.type='repair'
    ORDER BY s.created_at DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    st.dataframe(df, use_container_width=True)

def add_product_screen():
    st.subheader("➕ Add Product")

    name = st.text_input("Product Name")

    category = st.selectbox(
        "Category",
        ["bike", "accessory", "part", "service"]
    )

    subcategory = st.text_input("Subcategory")

    cost = st.number_input("Cost Price", min_value=0.0)
    price = st.number_input("Selling Price", min_value=0.0)
    qty = st.number_input("Initial Stock", min_value=0)
    brand = st.text_input("Brand")
    size = st.text_input("Size")
    description = st.text_area("Description")

    if st.button("Add Product"):
        if name and price:
            add_product(name, category, subcategory, brand, size, description, cost, price, qty)
            st.success(f"{name} added successfully!")
        else:
            st.error("Please fill required fields")

def restock_screen():
    st.subheader("🔄 Restock Product")

    df = get_all_products()

    product_map = {
        f"{row['Name']} (Stock: {row['Stock']})": row["ID"]
        for _, row in df.iterrows()
    }

    selected = st.selectbox("Select Product", list(product_map.keys()))
    qty = st.number_input("Quantity to Add", min_value=1)

    if st.button("Restock"):
        product_id = product_map[selected]
        restock_product(product_id, qty)
        st.success("Stock updated!")

def create_user_screen():
    st.subheader("👥 Create User")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["admin", "cashier"])

    if st.button("Create User"):
        if username and password:
            create_user(username, password, role)
            st.success("User created!")
        else:
            st.error("Fill all fields")


# ---------------- POS ----------------
def pos_screen():
    st.title("💰 Checkout")

    df = get_all_products()

    # --- CREATE PRODUCT MAP FROM DATAFRAME ---
    product_dict = {
        f"{row['Name']} (KES {row['Selling Price']})": {
            "id": row["ID"],
            "name": row["Name"],
            "price": row["Selling Price"],
            "stock": row["Stock"]
        }
        for _, row in df.iterrows()
    }
    

    # --- ADD TO CART ---
    st.subheader("🛒 Add Item")

    col1, col2, col3 = st.columns([3, 1, 1])

    selected = col1.selectbox("Product", list(product_dict.keys()))
    qty = col2.number_input("Qty", min_value=1, value=1)

    if col3.button("Add"):
        product = product_dict[selected]

        # Merge duplicates
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

    # --- CART DISPLAY ---
    st.subheader("🧾 Cart")

    if not st.session_state.cart:
        st.info("Cart is empty")
        return

    total = 0

    for i, item in enumerate(st.session_state.cart):
        item_total = item["price"] * item["quantity"]
        total += item_total

        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

        col1.write(item["name"])
        col2.write(item["quantity"])
        col3.write(f"KES {item['price']}")
        col4.write(f"KES {item_total}")

        if col5.button("❌", key=f"remove_{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

    st.markdown("---")
    st.subheader(f"💵 Total: KES {total}")

    # --- CHECKOUT OPTIONS (must be outside the button block) ---
    st.markdown("### 🧾 Checkout Details")
    customer_name = st.text_input("Customer Name (optional)", key="pos_customer_name")
    payment_method = st.selectbox("Payment Method", ["Cash", "M-Pesa", "Paybill"], key="pos_payment_method")

    # --- CHECKOUT ---
    if "last_receipt" not in st.session_state:
        st.session_state.last_receipt = None

    if st.button("✅ Checkout"):
        try:
            cart_items = [
                {"product_id": item["product_id"], "quantity": item["quantity"]}
                for item in st.session_state.cart
            ]

            sale_id, total, items = process_sale(cart_items)

            pdf = generate_pdf_receipt(
                sale_id,
                items,
                total,
                customer_name if customer_name else "Walk-in",
                payment_method
            )

            st.session_state.last_receipt = {
                "pdf": pdf,
                "sale_id": sale_id,
                "filename": f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            }
            st.session_state.cart = []
            st.success("✅ Sale completed!")

        except Exception as e:
            st.error(str(e))

    # --- SHOW RECEIPT DOWNLOAD (persists after rerun) ---
    if st.session_state.last_receipt:
        st.download_button(
            label="📄 Download Receipt",
            data=st.session_state.last_receipt["pdf"],
            file_name=st.session_state.last_receipt["filename"],
            mime="application/pdf",
            key="download_pos_receipt"
        )
        if st.button("🆕 New Sale"):
            st.session_state.last_receipt = None
            st.rerun()

def repairs_screen():
    st.subheader("🔧 Repairs Management")

    tabs = st.tabs(["New Repair", "Manage Repairs"])

    # ---------------- NEW REPAIR ----------------
    with tabs[0]:
        st.markdown("### ➕ Create Repair Job")

        customer = st.text_input("Customer Name")
        phone = st.text_input("Phone")
        bike = st.text_input("Bike Type")
        issue = st.text_area("Issue Description")
        service_cost = st.number_input("Service Cost", min_value=0.0, format="%.2f")

        if st.button("Create Repair"):
            repair_id = create_repair(customer, phone, bike, issue, service_cost)
            st.success(f"Repair created! ID: {repair_id}")
            st.session_state.current_repair = repair_id
            st.session_state.repair_parts = []  # Track parts added

        # --- ADD PARTS ---
        if "current_repair" in st.session_state:
            st.markdown("### 🧩 Add Parts Used")

            df = get_all_products()
            product_map = {f"{row['Name']} (Stock: {row['Stock']})": row["ID"] for _, row in df.iterrows()}

            selected = st.selectbox("Select Part", list(product_map.keys()))
            qty = st.number_input(
                "Quantity", min_value=1, value=1, key=f"qty_{selected}"
            )
            price = st.number_input(
                "Price per Unit", min_value=0.0, value=0.0, format="%.2f", key=f"price_{selected}"
            )

            if st.button("Add Part"):
                part_id = product_map[selected]
                st.session_state.repair_parts.append({
                    "part_id": part_id,
                    "name": selected,
                    "qty": qty,
                    "price": price,
                })
                add_repair_item(st.session_state.current_repair, part_id, qty, price)
                st.success(f"Added {qty} x {selected} at {price:.2f} each")
                st.rerun()

            # Show current parts summary
            if st.session_state.repair_parts:
                st.markdown("#### 📝 Parts Added for this Repair")
                total_parts_cost = 0
                for idx, part in enumerate(st.session_state.repair_parts, 1):
                    line_total = part["qty"] * part["price"]
                    total_parts_cost += line_total
                    st.write(f"{idx}. {part['name']} - Qty: {part['qty']} x {part['price']:.2f} = {line_total:.2f}")

                st.write(f"**Service Cost:** {service_cost:.2f}")
                st.write(f"**Total Cost:** {service_cost + total_parts_cost:.2f}")


            if st.button("Generate Receipt"):
                st.markdown("### 🧾 Repair Receipt")
                st.write(f"**Customer:** {customer}")
                st.write(f"**Phone:** {phone}")
                st.write(f"**Bike:** {bike}")
                st.write(f"**Issue:** {issue}")
                st.write("---")
                st.markdown("#### Parts Used")
                total_parts_cost = 0
                for idx, part in enumerate(st.session_state.repair_parts, 1):
                    line_total = part["qty"] * part["price"]
                    total_parts_cost += line_total
                    st.write(f"{idx}. {part['name']} - Qty: {part['qty']} x {part['price']:.2f} = {line_total:.2f}")
                st.write(f"**Service Cost:** {service_cost:.2f}")
                st.write(f"**Total Amount:** {service_cost + total_parts_cost:.2f}")
    # ---------------- MANAGE REPAIRS ----------------
    with tabs[1]:
        st.markdown("### 📋 All Repairs")
        df = get_repairs()
        st.dataframe(df, use_container_width=True)

        if not df.empty:
            repair_id = st.selectbox("Select Repair ID", df["id"])
            status = st.selectbox("Update Status", ["pending", "completed", "paid"])

            if st.button("Update Status"):
                update_repair_status(repair_id, status)
                st.success("Status updated!")
                st.rerun()

            # Fetch existing parts for the repair
            existing_parts = get_repair_items(repair_id)  # Should return list of dicts with name, qty, price
            st.markdown("### 🧩 Parts Used")
            total_parts_cost = 0
            for idx, part in enumerate(existing_parts, 1):
                line_total = part["qty"] * part["price"]
                total_parts_cost += line_total
                st.write(f"{idx}. {part['name']} - Qty: {part['qty']} x {part['price']:.2f} = {line_total:.2f}")

            service_cost = get_repair_service_cost(repair_id)
            st.write(f"**Service Cost:** {service_cost:.2f}")
            st.write(f"**Total Cost:** {service_cost + total_parts_cost:.2f}")

            # Optionally add more parts
            st.markdown("### ➕ Add More Parts to Existing Repair")
            df_parts = get_all_products()
            product_map = {f"{row['Name']} (Stock: {row['Stock']})": row["ID"] for _, row in df_parts.iterrows()}
            selected = st.selectbox("Select Part to Add", list(product_map.keys()), key="manage_select")
            qty = st.number_input("Quantity", min_value=1, value=1, key=f"manage_qty_{selected}")
            price = st.number_input("Price per Unit", min_value=0.0, value=0.0, format="%.2f", key=f"manage_price_{selected}")

            if st.button("Add Part to Repair"):
                add_repair_item(repair_id, product_map[selected], qty, price)
                st.success(f"Added {qty} x {selected} at {price:.2f} each")
                st.rerun()

            # if st.button("Mark as Paid"):
            #     update_repair_status(repair_id, "paid")
            #     record_repair_sale(repair_id)  # <-- record in sales history
            #     st.success("Repair marked as paid and recorded in sales history!")
            #     st.rerun()
            st.markdown("### 💳 Checkout Repair")

            repair_customer = st.text_input("Customer Name (optional)", key=f"repair_customer_{repair_id}")
            repair_payment = st.selectbox("Payment Method", ["Cash", "M-Pesa", "Paybill"], key=f"repair_payment_{repair_id}")

            if "last_repair_receipt" not in st.session_state:
                st.session_state.last_repair_receipt = None

            if st.button("✅ Checkout Repair", key=f"checkout_{repair_id}"):

                # 1. Record sale
                record_repair_sale(repair_id)

                # 2. Update status
                update_repair_status(repair_id, "paid")
                
                # 3. Prepare receipt data
                parts = get_repair_items(repair_id)
                service_cost = get_repair_service_cost(repair_id)

                items = [
                   {
                       "name": p["name"],
                       "quantity": p["qty"],
                        "price": p["price"]
                    }
                    for p in parts
                ]

                total_parts = sum(p["qty"] * p["price"] for p in parts)
                total = total_parts + service_cost

                # 4. Add service as item
                items.append({
                    "name": "Service Fee",
                    "quantity": 1,
                    "price": service_cost
                })

                # 5. Generate receipt
                pdf = generate_pdf_receipt(
                    repair_id,
                    items,
                    total,
                    repair_customer if repair_customer else "Walk-in",
                    repair_payment
                )

                st.session_state.last_repair_receipt = {
                    "pdf": pdf,
                    "repair_id": repair_id
                }
                st.success("✅ Repair checked out successfully!")

            if st.session_state.get("last_repair_receipt") and \
               st.session_state.last_repair_receipt["repair_id"] == repair_id:
                st.download_button(
                    label="📄 Download Repair Receipt",
                    data=st.session_state.last_repair_receipt["pdf"],
                    file_name=f"repair_{repair_id}.pdf",
                    mime="application/pdf",
                    key=f"dl_repair_{repair_id}"
                )
                if st.button("🆕 New Repair", key=f"new_repair_{repair_id}"):
                    st.session_state.last_repair_receipt = None
                    st.rerun()


# ---------------- PARKING ----------------
def parking_screen():
    st.subheader("🅿️ Bicycle Parking")

    tabs = st.tabs(["Check In", "Check Out", "History"])

    with tabs[0]:
        st.markdown("### 🚲 New Check-In")
        customer = st.text_input("Customer Name", key="park_customer")
        bike_desc = st.text_input("Bike Description (colour, model)", key="park_bike")
        daily_rate = st.number_input("Daily Rate (KES)", min_value=10.0, value=100.0, step=10.0)

        if st.button("✅ Check In"):
            if customer and bike_desc:
                pid = check_in(customer, bike_desc, daily_rate)
                st.success(f"Checked in! Parking ID: **{pid}**")
                st.info("Give the customer their Parking ID to use at check-out.")
            else:
                st.error("Please fill customer name and bike description.")

        st.markdown("---")
        st.markdown("### 🟢 Currently Parked")
        active = get_active_parking()
        if active.empty:
            st.info("No bikes currently parked.")
        else:
            st.dataframe(active, use_container_width=True)

    with tabs[1]:
        st.markdown("### 🏁 Check Out")
        active = get_active_parking()

        if active.empty:
            st.info("No bikes currently parked.")
        else:
            options = {
                f"ID {row['id']} — {row['customer_name']} ({row['bike_description']})": row["id"]
                for _, row in active.iterrows()
            }
            selected = st.selectbox("Select Bike to Check Out", list(options.keys()))

            if st.button("✅ Check Out & Calculate Fee"):
                pid = options[selected]
                try:
                    fee, hours = check_out(pid)
                    st.success(f"✅ Checked out after **{hours:.1f} hours**")
                    st.metric("Fee Charged", f"KES {fee:.2f}")
                except Exception as e:
                    st.error(str(e))

    with tabs[2]:
        st.markdown("### 📋 Parking History")
        history = get_parking_history()
        if history.empty:
            st.info("No parking history yet.")
        else:
            st.dataframe(history, use_container_width=True)
            total_earned = history["fee"].sum()
            st.metric("Total Parking Revenue", f"KES {total_earned:.2f}")


# ---------------- ADMIN ----------------
def admin_screen():
    st.title("🧑‍💼 Admin Dashboard")


    tabs = st.tabs([
        "Dashboard","Inventory", "Add Product", "Restock", 
        "Checkout", "Sales History","Repairs","Parking","Create User"])

    with tabs[0]:
        menu = "Dashboard"
        # Dashboard code here
        st.subheader("📊 Sales Dashboard")
        filter_type = st.selectbox(
        "Select Period",
        ["Today", "This Week", "This Month", "All"]
    )
        summary = get_sales_summary(filter_type)
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Revenue", f"KES {summary['total_revenue'] or 0}")
        col2.metric("📈 Profit", f"KES {summary['total_profit'] or 0}")
        col3.metric("🧾 Transactions", int(summary['total_transactions'] or 0))
        st.markdown("---")
        daily = get_daily_sales(filter_type)
        if not daily.empty:
            st.line_chart(daily.set_index("date"))
        else:
            st.info("No sales data yet")
        st.markdown("---")

        top_products = get_top_products(filter_type)
        if not top_products.empty:
            st.dataframe(top_products)
        else:
            st.info("No sales yet")

    with tabs[1]:
       
        menu = "Inventory"
        st.subheader("📦 Inventory")
        df = get_all_products()


        # # --- SEARCH ---
        search = st.text_input("🔍 Search product")
        if search:
            df = df[df["Name"].str.contains(search, case=False)]

    # --- FILTER BY CATEGORY ---
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + sorted(df["Category"].dropna().unique().tolist())
        )

        if category_filter != "All":
            df = df[df["Category"] == category_filter]

    # --- LOW STOCK FILTER ---
        if st.checkbox("⚠️ Show Low Stock Only"):
            df = df[df["Stock"] <= df["Reorder Level"]]

    # --- HIDE COST PRICE FOR NON-ADMIN (safety) ---
        if st.session_state.user["role"] != "admin":
            df = df.drop(columns=["Cost Price"])

    # --- HIGHLIGHT LOW STOCK ---
        def highlight_low_stock(row):
            if row["Stock"] <= row["Reorder Level"]:
                return ["background-color: #ffcccc"] * len(row)
            return [""] * len(row)

        st.dataframe(
            df.style.apply(highlight_low_stock, axis=1),
            use_container_width=True
        )

    with tabs[2]:
        menu = "Add Product"
        st.subheader("➕ Add Product")
        name = st.text_input("Name")
        category = st.selectbox(
            "Category",
              ["bike", "accessory", "part", "service"])
        subcategory = st.text_input("Subcategory")
        brand = st.text_input("Brand(optional)")
        size = st.text_input("Size(optional)")
        description = st.text_area("Description(optional)")
        cost = st.number_input("Cost Price")
        price = st.number_input("Selling Price")
        qty = st.number_input("Initial Quantity", min_value=0)
        if st.button("Add Product"):
               if name and price:
                    add_product(
                        name,
                        category,
                        subcategory,
                        brand if brand else None,
                        size if size else None,
                        description if description else None,
                        cost,
                        price,
                        qty
                    )
                    st.success(f"{name} added successfully!")
        else:
                st.error("Please fill required fields")

    with tabs[3]:
        menu = "Restock"
        st.subheader("🔄 Restock Product")
        product_id = st.number_input("Product ID", min_value=1)
        qty = st.number_input("Quantity", min_value=1)
        if st.button("Restock"):
            restock_product(product_id, qty)
            st.success("Stock updated!")

    with tabs[4]:
        pos_screen()

    with tabs[5]:
        sales_history_screen()

    with tabs[6]:
        repairs_screen()

    with tabs[7]:
        parking_screen()

    with tabs[8]:
        menu = "Create User"
        st.subheader("👥 Create User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin", "cashier"])
        if st.button("Create"):
            create_user(username, password, role)
            st.success("User created!")
    
    

# ---------------- Cashier ----------------  
def cashier_screen():
    st.title("🧑‍💼 Cashier Dashboard")

    tabs = st.tabs(["Checkout", "Inventory", "Repairs", "Parking"])

    with tabs[0]:
        menu = "Checkout"
        pos_screen()

    with tabs[1]:
        menu = "Inventory"
        st.subheader("📦 Inventory")
        df = get_all_products()

        # Hide cost price for cashier
        if "Cost Price" in df.columns and st.session_state.user["role"] != "admin":
            df = df.drop(columns=["Cost Price"])

        st.dataframe(df, use_container_width=True)

    with tabs[2]:
        menu = "Repairs"
        st.subheader("🔧 Repairs Management")
        repairs_screen()

    with tabs[3]:
        parking_screen()

# ---------------- MAIN ----------------
if st.session_state.user is None:
    login_screen()
else:
    role = st.session_state.user["role"]

    st.sidebar.write(f"Logged in as: {role}")

    if role == "admin":
        admin_screen()
    else:
        cashier_screen()

# # ROUTING
#     if page == "Checkout":
#         pos_screen()

#     elif page == "Inventory":
#         inventory_screen()

#     elif page == "Dashboard" and role == "admin":
#         admin_screen()

#     elif page == "Add Product" and role == "admin":
#         add_product_screen()

#     elif page == "Restock" and role == "admin":
#         restock_screen()

#     elif page == "Create User" and role == "admin":
#         create_user_screen()

#     elif page == "Sales History" and role == "admin":
#         sales_history_screen()

   
# import streamlit as st
# import os
# from datetime import datetime

# from auth import login, create_user
# from inventory import get_all_products, add_product, restock_product, update_product, delete_product
# from pos import process_sale
# from analytics import get_sales_summary, get_daily_sales, get_top_products
# from repairs import (
#     create_repair, add_repair_item, get_repairs,
#     update_repair_status, get_repair_items,
#     get_repair_service_cost, record_repair_sale
# )
# from receipt import generate_pdf_receipt

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(page_title="Baiskeli POS", layout="wide")

# # ---------------- HEADER ----------------
# BASE_DIR = os.path.dirname(__file__)
# logo_path = os.path.join(BASE_DIR, "logo.jpeg")

# col1, col2 = st.columns([1, 5])
# with col1:
#     if os.path.exists(logo_path):
#         st.image(logo_path, width=100)
# with col2:
#     st.title("🚲 Baiskeli POS System")

# st.markdown("---")

# # ---------------- SESSION ----------------
# if "user" not in st.session_state:
#     st.session_state.user = None
# if "cart" not in st.session_state:
#     st.session_state.cart = []

# # ---------------- LOGIN ----------------
# def login_screen():
#     st.title("🔐 Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         user = login(username, password)
#         if user:
#             st.session_state.user = user
#             st.rerun()
#         else:
#             st.error("Invalid credentials")

# # ---------------- INVENTORY ----------------
# def inventory_screen():
#     df = get_all_products()

#     st.subheader("📦 Inventory")

#     search = st.text_input("Search")
#     if search:
#         df = df[df["Name"].str.contains(search, case=False)]

#     if st.session_state.user["role"] != "admin":
#         df = df.drop(columns=["Cost Price"], errors="ignore")

#     st.dataframe(df, use_container_width=True)

# # ---------------- ADD PRODUCT ----------------
# def add_product_screen():
#     st.subheader("➕ Add Product")

#     name = st.text_input("Name")
#     category = st.selectbox("Category", ["bike", "accessory", "part", "service"])
#     subcategory = st.text_input("Subcategory")
#     brand = st.text_input("Brand (optional)")
#     size = st.text_input("Size (optional)")
#     description = st.text_area("Description (optional)")
#     cost = st.number_input("Cost Price")
#     price = st.number_input("Selling Price")
#     qty = st.number_input("Quantity", min_value=0)

#     if st.button("Add Product"):
#         if name and price:
#             add_product(name, category, subcategory, brand or None, size or None, description or None, cost, price, qty)
#             st.success("Product added")
#         else:
#             st.error("Fill required fields")

# # ---------------- RESTOCK ----------------
# def restock_screen():
#     df = get_all_products()
#     product_map = {f"{r['Name']} (Stock {r['Stock']})": r['ID'] for _, r in df.iterrows()}

#     selected = st.selectbox("Product", list(product_map.keys()))
#     qty = st.number_input("Quantity", min_value=1)

#     if st.button("Restock"):
#         restock_product(product_map[selected], qty)
#         st.success("Updated")

# # ---------------- POS ----------------
# def pos_screen():
#     st.subheader("💰 Checkout")

#     df = get_all_products()
#     products = {f"{r['Name']} (KES {r['Selling Price']})": r for _, r in df.iterrows()}

#     col1, col2, col3 = st.columns([3,1,1])
#     selected = col1.selectbox("Product", list(products.keys()))
#     qty = col2.number_input("Qty", min_value=1, value=1)

#     if col3.button("Add"):
#         p = products[selected]
#         st.session_state.cart.append({
#             "product_id": p["ID"],
#             "name": p["Name"],
#             "price": p["Selling Price"],
#             "quantity": qty
#         })

#     total = 0
#     for i, item in enumerate(st.session_state.cart):
#         total += item["price"] * item["quantity"]
#         if st.button("❌", key=f"rm{i}"):
#             st.session_state.cart.pop(i)
#             st.rerun()

#     st.write(f"Total: KES {total}")

#     if st.button("Checkout"):
#         sale_id, total, items = process_sale([
#             {"product_id": i["product_id"], "quantity": i["quantity"]}
#             for i in st.session_state.cart
#         ])

#         filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         pdf = generate_pdf_receipt(filename, items, total)

#         st.download_button("Download Receipt", pdf, file_name=filename)
#         st.session_state.cart = []
#         st.rerun()

# # ---------------- REPAIRS ----------------
# def repairs_screen():
#     st.subheader("🔧 Repairs")

#     tabs = st.tabs(["New", "Manage"])

#     with tabs[0]:
#         name = st.text_input("Customer")
#         phone = st.text_input("Phone")
#         bike = st.text_input("Bike")
#         issue = st.text_area("Issue")
#         cost = st.number_input("Service Cost")

#         if st.button("Create"):
#             rid = create_repair(name, phone, bike, issue, cost)
#             st.session_state.repair = rid

#     with tabs[1]:
#         df = get_repairs()
#         st.dataframe(df)

# # ---------------- DASHBOARD ----------------
# def dashboard():
#     st.subheader("📊 Dashboard")

#     period = st.selectbox("Period", ["Today","This Week","This Month","All"])
#     s = get_sales_summary(period)

#     c1,c2,c3 = st.columns(3)
#     c1.metric("Revenue", s['total_revenue'] or 0)
#     c2.metric("Profit", s['total_profit'] or 0)
#     c3.metric