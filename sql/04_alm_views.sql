-- 04_alm_views.sql
-- Views for Interest Rate Risk in the Banking Book (IRRBB) and Liquidity Coverage Ratio (LCR) analysis

-- 1. Portfolio Composition view
CREATE VIEW IF NOT EXISTS v_alm_portfolio_summary AS
SELECT 
    type,
    category,
    COUNT(product_id) as total_accounts,
    SUM(balance) as total_balance,
    AVG(interest_rate) as avg_interest_rate,
    AVG(duration_years) as avg_duration,
    AVG(repricing_maturity_years) as avg_repricing_maturity
FROM 
    alm_portfolio
GROUP BY 
    type, category;

-- 2. Repricing Gap View (Short-term vs Long-term)
CREATE VIEW IF NOT EXISTS v_alm_repricing_gap AS
SELECT
    '<= 1 Year' as time_bucket,
    SUM(CASE WHEN type = 'Asset' THEN balance ELSE 0 END) as rate_sensitive_assets,
    SUM(CASE WHEN type = 'Liability' THEN balance ELSE 0 END) as rate_sensitive_liabilities,
    SUM(CASE WHEN type = 'Asset' THEN balance ELSE -balance END) as repricing_gap
FROM alm_portfolio
WHERE repricing_maturity_years <= 1.0
UNION ALL
SELECT
    '> 1 Year' as time_bucket,
    SUM(CASE WHEN type = 'Asset' THEN balance ELSE 0 END) as rate_sensitive_assets,
    SUM(CASE WHEN type = 'Liability' THEN balance ELSE 0 END) as rate_sensitive_liabilities,
    SUM(CASE WHEN type = 'Asset' THEN balance ELSE -balance END) as repricing_gap
FROM alm_portfolio
WHERE repricing_maturity_years > 1.0;

-- 3. NII & EVE Rate Shock View
CREATE VIEW IF NOT EXISTS v_alm_rate_shock_impact AS
SELECT 
    shock_bps,
    nii_impact,
    eve_impact
FROM 
    alm_nii_eve_shocks
ORDER BY 
    shock_bps ASC;

-- 4. LCR Components View
CREATE VIEW IF NOT EXISTS v_alm_lcr_dashboard AS
SELECT
    hqla,
    total_outflows_30d,
    total_inflows_30d,
    capped_inflows_30d,
    net_cash_outflows_30d,
    lcr_ratio,
    CASE 
        WHEN lcr_ratio >= 1.0 THEN 'Healthy (>100%)'
        ELSE 'Deficit (<100%)'
    END as lcr_status
FROM
    alm_lcr_summary;
