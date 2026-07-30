-- Credit Rating Distribution
-- Breakdown of portfolio by internal credit rating

SELECT 
    cr.internal_rating,
    COUNT(l.loan_id) AS total_loans,
    SUM(l.disbursed_amount) AS total_exposure,
    ROUND(SUM(l.disbursed_amount) / (SELECT SUM(disbursed_amount) FROM loans) * 100, 2) AS exposure_percentage,
    ROUND(AVG(cr.PD), 2) AS average_PD
FROM loans l
JOIN credit_ratings cr ON l.loan_id = cr.loan_id
GROUP BY cr.internal_rating
ORDER BY cr.internal_rating;
