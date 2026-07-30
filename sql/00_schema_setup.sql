-- Since we are using SQLite and pandas' `to_sql` method, the schema is auto-generated based on the DataFrame dtypes. 
-- However, for reference and documentation (e.g., if migrating to PostgreSQL), here is the expected schema:

CREATE TABLE IF NOT EXISTS branches (
    branch_id TEXT PRIMARY KEY,
    branch_name TEXT,
    city TEXT,
    state TEXT,
    region TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    occupation TEXT,
    annual_income REAL,
    state TEXT,
    city TEXT,
    customer_since_date DATE
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id TEXT PRIMARY KEY,
    customer_id TEXT,
    loan_type TEXT,
    sanction_amount REAL,
    disbursed_amount REAL,
    interest_rate REAL,
    tenure_months INTEGER,
    disbursement_date DATE,
    sector TEXT,
    branch_id TEXT,
    region TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE IF NOT EXISTS credit_ratings (
    loan_id TEXT,
    rating_date DATE,
    internal_rating INTEGER,
    PD REAL,
    FOREIGN KEY(loan_id) REFERENCES loans(loan_id)
);

CREATE TABLE IF NOT EXISTS repayment_schedule (
    loan_id TEXT,
    installment_no INTEGER,
    due_date DATE,
    due_amount REAL,
    paid_amount REAL,
    paid_date DATE,
    dpd INTEGER,
    FOREIGN KEY(loan_id) REFERENCES loans(loan_id)
);
