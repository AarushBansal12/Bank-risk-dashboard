-- High Risk Borrowers Identification (Watchlist)
-- Focuses on SMA-2 and NPA accounts with high exposure and poor credit rating

WITH risk_ranked AS (
    SELECT 
        c.customer_id,
        c.name,
        l.loan_id,
        l.disbursed_amount,
        v.asset_classification,
        v.max_dpd,
        cr.internal_rating,
        cr.PD,
        (l.disbursed_amount * cr.PD) AS expected_loss_contribution,
        DENSE_RANK() OVER (ORDER BY (l.disbursed_amount * cr.PD) DESC) as risk_rank
    FROM loans l
    JOIN customers c ON l.customer_id = c.customer_id
    JOIN vw_loan_status v ON l.loan_id = v.loan_id
    JOIN credit_ratings cr ON l.loan_id = cr.loan_id
    WHERE v.asset_classification IN ('SMA-2', 'NPA')
)
SELECT * 
FROM risk_ranked
WHERE risk_rank <= 100
ORDER BY risk_rank;
