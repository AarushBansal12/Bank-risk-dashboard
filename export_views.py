import sqlite3
import pandas as pd
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'credit_risk.db')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'data-generation', 'tableau_exports')

os.makedirs(OUTPUT_DIR, exist_ok=True)

views_to_export = [
    'vw_tableau_kpi',
    'vw_tableau_rating_dist',
    'vw_tableau_sector_exp',
    'vw_tableau_geo_map',
    'vw_tableau_ecl_summary'
]

conn = sqlite3.connect(DB_PATH)

for view in views_to_export:
    print(f"Exporting {view}...")
    df = pd.read_sql_query(f"SELECT * FROM {view}", conn)
    df.to_csv(os.path.join(OUTPUT_DIR, f"{view}.csv"), index=False)

print("Export complete!")
conn.close()
