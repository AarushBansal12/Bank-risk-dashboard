import sqlite3
import pandas as pd
import os
import glob

# Paths
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(DATA_DIR)
DB_PATH = os.path.join(PROJECT_DIR, 'credit_risk.db')

def load_csv_to_sqlite():
    print(f"Connecting to SQLite Database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    csv_files = glob.glob(os.path.join(DATA_DIR, '*.csv'))
    
    if not csv_files:
        print("No CSV files found. Please run generate_data.py first.")
        return
        
    for file_path in csv_files:
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        print(f"Loading {table_name} into database...")
        
        # Read CSV in chunks to avoid memory issues for large files
        chunksize = 50000
        for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunksize)):
            # Write chunk to sqlite
            chunk.to_sql(name=table_name, con=conn, if_exists='replace' if i == 0 else 'append', index=False)
            
    print("Creating Indexes...")
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_repayment_loan_id ON repayment_schedule(loan_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_loans_customer_id ON loans(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_loans_loan_id ON loans(loan_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_customers_customer_id ON customers(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ratings_loan_id ON credit_ratings(loan_id);")
    conn.commit()

    print("Successfully loaded all data into SQLite database!")
    conn.close()

if __name__ == "__main__":
    load_csv_to_sqlite()
