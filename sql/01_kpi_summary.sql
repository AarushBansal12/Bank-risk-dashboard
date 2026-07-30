-- 1. Base query to compute max DPD for each loan to derive asset classification
DROP VIEW IF EXISTS vw_loan_status;
CREATE VIEW vw_loan_status AS
SELECT 
    l.loan_id,
    l.disbursed_amount,
    COALESCE(MAX(r.dpd), 0) AS max_dpd,
    CASE 
        WHEN COALESCE(MAX(r.dpd), 0) = 0 THEN 'Standard'
        WHEN MAX(r.dpd) BETWEEN 1 AND 30 THEN 'SMA-0'
        WHEN MAX(r.dpd) BETWEEN 31 AND 60 THEN 'SMA-1'
        WHEN MAX(r.dpd) BETWEEN 61 AND 90 THEN 'SMA-2'
        ELSE 'NPA' 
    END AS asset_classification,
    CASE WHEN COALESCE(MAX(r.dpd), 0) > 90 THEN 1 ELSE 0 END AS is_npa
FROM loans l
LEFT JOIN repayment_schedule r ON l.loan_id = r.loan_id
GROUP BY l.loan_id, l.disbursed_amount;


-- 2. Executive KPI Summary
-- Calculates Total Portfolio, Gross NPA %, etc.
SELECT 
    COUNT(loan_id) AS total_loans,
    SUM(disbursed_amount) AS total_portfolio_outstanding,
    SUM(CASE WHEN is_npa = 1 THEN disbursed_amount ELSE 0 END) AS gross_npa_amount,
    ROUND((SUM(CASE WHEN is_npa = 1 THEN disbursed_amount ELSE 0 END) / SUM(disbursed_amount)) * 100, 2) AS gross_npa_percentage
FROM vw_loan_status;
