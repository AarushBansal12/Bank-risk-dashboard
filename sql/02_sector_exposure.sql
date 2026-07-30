-- Sector Exposure Aggregation
-- We use vw_loan_status to get the NPA flag and combine it with loan metadata

SELECT 
    l.sector,
    COUNT(l.loan_id) AS total_loans,
    SUM(l.disbursed_amount) AS total_exposure,
    SUM(CASE WHEN v.is_npa = 1 THEN l.disbursed_amount ELSE 0 END) AS npa_exposure,
    ROUND((SUM(CASE WHEN v.is_npa = 1 THEN l.disbursed_amount ELSE 0 END) / SUM(l.disbursed_amount)) * 100, 2) AS npa_percentage,
    ROUND(AVG(cr.PD), 2) AS avg_probability_of_default
FROM loans l
JOIN vw_loan_status v ON l.loan_id = v.loan_id
LEFT JOIN credit_ratings cr ON l.loan_id = cr.loan_id
GROUP BY l.sector
ORDER BY total_exposure DESC;
