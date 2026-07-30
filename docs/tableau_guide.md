# Tableau Dashboard Build Guide

This guide walks you through connecting your generated data to Tableau and building the 7 pages required by the masterplan.

## 1. Connect to Data
1. Open Tableau Desktop (or Tableau Public).
2. Under "Connect To a File" or "Connect To a Server", select **SQLite** (if you have the driver installed) OR just connect directly to the generated CSV files in the `data-generation` folder. 
   - *Pro Tip:* If you are using Tableau Public (which doesn't support local SQLite natively), connect to the `customers.csv`, `loans.csv`, etc., and define the relationships manually, OR export the views from SQLite to CSV and connect to those.
3. Bring in the SQL materialized views: `vw_tableau_kpi`, `vw_tableau_rating_dist`, `vw_tableau_sector_exp`, `vw_tableau_geo_map`, and `vw_tableau_ecl_summary`.

---

## 2. Page-by-Page Construction

### Page 1: Credit Rating Distribution
**Goal:** Understand how exposure is distributed across internal ratings.
- **Data Source:** `vw_tableau_rating_dist`
- **Chart Type:** Bar Chart
- **Rows:** `internal_rating` (Discrete Dimension)
- **Columns:** `total_exposure` (Measure, Sum)
- **Color:** `average_PD` (Diverging Red-Green palette; Red = High PD)
- **Tooltips:** Add `total_loans` and formatted `average_PD`.

### Page 2: Sector-wise Exposure
**Goal:** See concentration risk and NPA ratio by sector.
- **Data Source:** `vw_tableau_sector_exp`
- **Chart Type:** Tree Map or Dual-Axis Bar Chart
- **Dimension (Columns):** `sector`
- **Measure 1 (Rows):** `total_exposure` (Bar)
- **Measure 2 (Rows):** `[npa_exposure] / [total_exposure]` (Line, Dual-Axis)
- **Color:** Color the bars by Sector, or color the Line by NPA %.

### Page 3: Geographic Exposure
**Goal:** Heatmap of India showing exposure and default hotspots.
- **Data Source:** `vw_tableau_geo_map`
- **Chart Type:** Filled Map
- **Geo-Role:** Assign `state` geographic role "State/Province" (Country = India).
- **Detail:** `state`
- **Size (if using bubbles):** `state_exposure`
- **Color (Filled Map):** `[state_npa_exposure] / [state_exposure]` (Red for high NPA)

### Page 4: Loan Portfolio Breakdown
**Goal:** Understand the mix of the portfolio.
- **Data Source:** `loans.csv` (or `vw_loan_status` joined with `loans`)
- **Chart Type:** Donut Chart or Pie Chart
- **Color:** `loan_type`
- **Angle/Size:** `disbursed_amount`
- Add a secondary timeline chart using `disbursement_date` to show vintage trends.

### Page 5: NPA Analysis
**Goal:** Deep dive into Non-Performing Assets.
- **Data Source:** `vw_tableau_sector_exp` & `vw_tableau_geo_map`
- **Action:** Create a dashboard that combines the NPA % from Sector and Geography, with a filter on "NPA Only" vs "All". 

### Page 6: Expected Credit Loss (ECL)
**Goal:** Visualize the provisioning requirements across Stages 1, 2, and 3.
- **Data Source:** `vw_tableau_ecl_summary`
- **Chart Type:** Stacked Bar Chart
- **Columns:** `sector`
- **Rows:** `approx_ECL`
- **Color:** `ecl_stage` (Green = Stage 1, Amber = Stage 2, Red = Stage 3)
- **Insight:** Notice how Stage 3 (NPA) drives a disproportionate amount of the total ECL.

### Page 7: Executive Overview
**Goal:** The headline page for the CRO / Hiring Manager.
- **Data Source:** `vw_tableau_kpi`
- **Layout:**
  - **Top Row (KPI Cards):** `total_exposure` (formatted as Currency), `total_loans`, `total_npa_exposure`, `npa_percentage`.
  - **Middle Row:** Bring in a miniature version of the Geographic Heatmap and the Sector Dual-Axis chart.
  - **Bottom Row:** Add a Text box titled "Key Risk Callouts". Write a brief summary of the findings (e.g., "Agriculture sector shows elevated NPA %, driving Stage 3 ECL.").

---

## 3. Finishing Touches
- **Interactivity:** Add dashboard actions. Clicking a Sector on the Executive Overview should filter the Geography map.
- **Formatting:** Use a dark mode theme (black/dark blue background) to make it look like a premium banking terminal. Ensure all currencies are formatted as INR (₹).
- **Publishing:** Save as a `.twbx` and publish to Tableau Public. Link it in your resume!
