-- Expected Credit Loss (ECL) Calculation
-- ECL = PD * LGD * EAD
-- Stages: Stage 1 (Standard/SMA-0), Stage 2 (SMA-1/2), Stage 3 (NPA)

WITH ecl_base AS (
    SELECT 
        l.loan_id,
        l.sector,
        l.disbursed_amount AS EAD,
        cr.PD / 100.0 AS PD_decimal,
        v.asset_classification,
        CASE 
            WHEN v.asset_classification IN ('Standard', 'SMA-0') THEN 'Stage 1'
            WHEN v.asset_classification IN ('SMA-1', 'SMA-2') THEN 'Stage 2'
            ELSE 'Stage 3'
        END AS ecl_stage,
        -- LGD Assumptions based on staging and loan type (Simplified for demo)
        CASE 
            WHEN l.loan_type = 'Home' THEN 0.20
            WHEN l.loan_type IN ('Auto', 'Agri') THEN 0.40
            WHEN v.asset_classification = 'NPA' THEN 0.70 -- Higher LGD for default
            ELSE 0.50
        END AS LGD
    FROM loans l
    JOIN vw_loan_status v ON l.loan_id = v.loan_id
    JOIN credit_ratings cr ON l.loan_id = cr.loan_id
)
SELECT 
    ecl_stage,
    sector,
    COUNT(loan_id) AS loan_count,
    SUM(EAD) AS total_exposure,
    SUM(EAD * PD_decimal * LGD) AS expected_credit_loss,
    ROUND((SUM(EAD * PD_decimal * LGD) / SUM(EAD)) * 100, 2) AS ecl_percentage
FROM ecl_base
GROUP BY ecl_stage, sector
ORDER BY ecl_stage, expected_credit_loss DESC;
