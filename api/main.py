from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
import os

app = FastAPI(title="Risk Dashboard API")

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, lock this down
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to get DB connection
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'credit_risk.db')
    conn = sqlite3.connect(db_path)
    # Enable dict factory so rows are returned as dictionaries
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def read_root():
    return {"status": "API is running"}

# --- Credit Risk Endpoints ---

@app.get("/api/credit/kpis")
def get_credit_kpis():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM v_tableau_kpi", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/api/credit/sector-exposure")
def get_sector_exposure():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM v_tableau_sector_exp", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/api/credit/rating-dist")
def get_rating_distribution():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM v_tableau_rating_dist", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/api/credit/ecl-summary")
def get_ecl_summary():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM v_tableau_ecl_summary", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/api/credit/geo-map")
def get_geo_map():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM v_tableau_geo_map", conn)
    conn.close()
    return df.to_dict(orient="records")


# --- ALM Risk Endpoints ---

@app.get("/api/alm/portfolio")
def get_alm_portfolio():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM v_alm_portfolio_summary", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/api/alm/repricing-gap")
def get_repricing_gap():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM v_alm_repricing_gap", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/api/alm/rate-shocks")
def get_rate_shocks():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM v_alm_rate_shock_impact", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/api/alm/lcr")
def get_lcr():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM v_alm_lcr_dashboard", conn)
    conn.close()
    return df.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
