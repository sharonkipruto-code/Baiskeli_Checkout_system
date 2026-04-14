import sqlite3
import pandas as pd

DB_NAME = "baiskeli.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------------- DATE FILTER HELPER ----------------
def get_date_filter(filter_type):
    if filter_type == "Today":
        return "WHERE DATE(s.created_at) = DATE('now')"
    elif filter_type == "This Week":
        return "WHERE DATE(s.created_at) >= DATE('now', '-7 days')"
    elif filter_type == "This Month":
        return "WHERE strftime('%Y-%m', s.created_at) = strftime('%Y-%m', 'now')"
    else:
        return ""


# ---------------- SUMMARY (WITH PROFIT) ----------------
def get_sales_summary(filter_type="All"):
    conn = get_connection()
    date_filter = get_date_filter(filter_type)

    query = f"""
    SELECT 
        COUNT(DISTINCT s.id) as total_transactions,
        SUM(si.quantity * si.price) as total_revenue,
        SUM(si.quantity * (si.price - p.cost_price)) as total_profit
    FROM sales s
    JOIN sale_items si ON s.id = si.sale_id
    JOIN products p ON si.product_id = p.id
    {date_filter}
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.iloc[0]


# ---------------- DAILY SALES ----------------
def get_daily_sales(filter_type="All"):
    conn = get_connection()
    date_filter = get_date_filter(filter_type)

    query = f"""
    SELECT 
        DATE(s.created_at) as date,
        SUM(si.quantity * si.price) as revenue
    FROM sales s
    JOIN sale_items si ON s.id = si.sale_id
    {date_filter}
    GROUP BY DATE(s.created_at)
    ORDER BY date
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


# ---------------- TOP PRODUCTS ----------------
def get_top_products(filter_type="All"):
    conn = get_connection()
    date_filter = get_date_filter(filter_type)

    query = f"""
    SELECT 
        p.name,
        SUM(si.quantity) as total_sold,
        SUM(si.quantity * (si.price - p.cost_price)) as profit
    FROM sales s
    JOIN sale_items si ON s.id = si.sale_id
    JOIN products p ON si.product_id = p.id
    {date_filter}
    GROUP BY p.name
    ORDER BY total_sold DESC
    LIMIT 5
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df

