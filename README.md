# Bank Credit Risk Analytics Dashboard

## Problem Statement
"Where is credit risk concentrated in this portfolio, and how much capital should be provisioned against expected losses?"

This project analyzes a simulated Indian bank loan portfolio to identify risk concentrations, monitor non-performing assets (NPAs), and calculate Expected Credit Loss (ECL) in accordance with RBI guidelines and Ind AS 109 / IFRS 9 standards.

## Project Architecture
1. **Data Generation (`data-generation/`)**: A Python script generates a synthetic but highly realistic dataset of ~20,000 loans, integrating deliberate risk patterns, regional skews, and macroeconomic logic.
2. **Database & SQL (`sql/`)**: The data is loaded into a SQLite database (`credit_risk.db`). SQL scripts provide the semantic layer for KPI calculation, portfolio aggregation, and ECL provisioning.
3. **Visualization (`docs/tableau_guide.md`)**: A Tableau dashboard visualizes the SQL materialized views, providing insights into credit rating distribution, geographic/sectoral exposure, and high-risk accounts.

## Getting Started

### 1. Generate the Data
Make sure you have Python installed.
```bash
cd data-generation
pip install -r requirements.txt
python generate_data.py
```
This will generate `customers.csv`, `loans.csv`, `repayment_schedule.csv`, `credit_ratings.csv`, and `branches.csv` in the `data-generation` folder.

### 2. Load into Database
Load the generated CSVs into a SQLite database:
```bash
python load_to_sqlite.py
```
This will create `credit_risk.db` in the root folder.

### 3. Build the Tableau Views
Open your SQLite database (e.g. using DB Browser for SQLite or standard sqlite3 CLI) and run the `.sql` scripts in the `sql/` folder in order to generate the KPIs and materialized views.

### 4. Connect to Tableau
Open Tableau Desktop/Public, connect to the SQLite database `credit_risk.db`, and follow the steps in `docs/tableau_guide.md` to build the dashboard.

## Key Findings (Sample)
- **Sectoral Risk**: The Agriculture sector demonstrated a 3.2x higher NPA ratio, driving 40% of the total Expected Credit Loss despite representing only 18% of the total exposure.
- **Geographic Concentration**: Maharashtra and Gujarat accounted for the majority of the exposure, but highest default rates were observed in specific seasonal pockets.
- **Provisioning**: Transition to Stage 3 (NPA) necessitated a significant jump in lifetime ECL provisions, highlighting the need for early warning signals (SMA-1/2 monitoring).
