-- Geographic Exposure Aggregation
-- Exposes concentration risk by State and Region

SELECT 
    l.region,
    b.state,
    COUNT(l.loan_id) AS total_loans,
    SUM(l.disbursed_amount) AS total_exposure,
    SUM(CASE WHEN v.is_npa = 1 THEN l.disbursed_amount ELSE 0 END) AS npa_exposure,
    ROUND((SUM(CASE WHEN v.is_npa = 1 THEN l.disbursed_amount ELSE 0 END) / SUM(l.disbursed_amount)) * 100, 2) AS npa_percentage
FROM loans l
JOIN vw_loan_status v ON l.loan_id = v.loan_id
JOIN branches b ON l.branch_id = b.branch_id
GROUP BY l.region, b.state
ORDER BY npa_percentage DESC;
