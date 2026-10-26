import os
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine

folder = r"P:\project schema\archive"   # your extracted folder
password = quote_plus("YOUR_PASSWORD")          # your MySQL root password

engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/ecommerce")

for file in os.listdir(folder):
    if file.endswith(".csv"):
        name = file.replace("olist_", "").replace("_dataset.csv", "").replace(".csv", "")
        df = pd.read_csv(os.path.join(folder, file))
        df.to_sql(name, engine, if_exists="replace", index=False)
        print("Loaded", name, len(df), "rows")