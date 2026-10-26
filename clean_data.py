import numpy as np
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine

password = quote_plus("YOUR_PASSWORD")
engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/ecommerce")

# --- Clean orders ---
orders = pd.read_sql("SELECT * FROM orders", engine)
before = len(orders)
orders = orders.drop_duplicates("order_id")
orders = orders.dropna(subset=["order_id", "customer_id"])
orders["order_status"] = orders["order_status"].str.lower().str.strip()
for col in ["order_purchase_timestamp", "order_delivered_customer_date"]:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")
print("Orders: removed", before - len(orders), "bad rows")
orders.to_sql("orders", engine, if_exists="replace", index=False)

# --- Clean products ---
products = pd.read_sql("SELECT * FROM products", engine)
missing = products["product_category_name"].isna().sum()
products["product_category_name"] = products["product_category_name"].fillna("unknown")
print("Products: filled", missing, "missing categories")
products.to_sql("products", engine, if_exists="replace", index=False)

# --- Create simulated inventory ---
np.random.seed(42)
inventory = pd.DataFrame({"product_id": products["product_id"]})
inventory["stock_qty"] = np.random.randint(0, 200, len(inventory))
inventory["reorder_level"] = np.random.randint(20, 60, len(inventory))
inventory.to_sql("inventory", engine, if_exists="replace", index=False)
print("Inventory table created:", len(inventory), "products")