-- Materialized views (semantic layer) for Tableau Dashboard
-- Tableau connects directly to these views instead of raw tables for better performance and organization

-- 1. KPI Summary
DROP VIEW IF EXISTS vw_tableau_kpi;
CREATE VIEW vw_tableau_kpi AS
SELECT 
    COUNT(loan_id) AS total_loans,
    SUM(disbursed_amount) AS total_exposure,
    SUM(CASE WHEN is_npa = 1 THEN disbursed_amount ELSE 0 END) AS total_npa_exposure,
    ROUND((SUM(CASE WHEN is_npa = 1 THEN disbursed_amount ELSE 0 END) / SUM(disbursed_amount)) * 100, 2) AS npa_percentage
FROM vw_loan_status;

-- 2. Rating Distribution
DROP VIEW IF EXISTS vw_tableau_rating_dist;
CREATE VIEW vw_tableau_rating_dist AS
SELECT 
    cr.internal_rating,
    COUNT(l.loan_id) AS total_loans,
    SUM(l.disbursed_amount) AS total_exposure,
    AVG(cr.PD) AS average_PD
FROM loans l
JOIN credit_ratings cr ON l.loan_id = cr.loan_id
GROUP BY cr.internal_rating;

-- 3. Sector Exposure
DROP VIEW IF EXISTS vw_tableau_sector_exp;
CREATE VIEW vw_tableau_sector_exp AS
SELECT 
    l.sector,
    COUNT(l.loan_id) AS total_loans,
    SUM(l.disbursed_amount) AS total_exposure,
    SUM(CASE WHEN v.is_npa = 1 THEN l.disbursed_amount ELSE 0 END) AS npa_exposure
FROM loans l
JOIN vw_loan_status v ON l.loan_id = v.loan_id
GROUP BY l.sector;

-- 4. Geographic Map Data
DROP VIEW IF EXISTS vw_tableau_geo_map;
CREATE VIEW vw_tableau_geo_map AS
SELECT 
    b.state,
    b.region,
    SUM(l.disbursed_amount) AS state_exposure,
    SUM(CASE WHEN v.is_npa = 1 THEN l.disbursed_amount ELSE 0 END) AS state_npa_exposure
FROM loans l
JOIN vw_loan_status v ON l.loan_id = v.loan_id
JOIN branches b ON l.branch_id = b.branch_id
GROUP BY b.state, b.region;

-- 5. ECL Summary
DROP VIEW IF EXISTS vw_tableau_ecl_summary;
CREATE VIEW vw_tableau_ecl_summary AS
SELECT 
    CASE 
        WHEN v.asset_classification IN ('Standard', 'SMA-0') THEN 'Stage 1'
        WHEN v.asset_classification IN ('SMA-1', 'SMA-2') THEN 'Stage 2'
        ELSE 'Stage 3'
    END AS ecl_stage,
    l.sector,
    SUM(l.disbursed_amount) AS EAD,
    SUM(l.disbursed_amount * (cr.PD/100.0) * 0.5) AS approx_ECL -- Simplified LGD=50% for visualization
FROM loans l
JOIN vw_loan_status v ON l.loan_id = v.loan_id
JOIN credit_ratings cr ON l.loan_id = cr.loan_id
GROUP BY 
    CASE 
        WHEN v.asset_classification IN ('Standard', 'SMA-0') THEN 'Stage 1'
        WHEN v.asset_classification IN ('SMA-1', 'SMA-2') THEN 'Stage 2'
        ELSE 'Stage 3'
    END,
    l.sector;
