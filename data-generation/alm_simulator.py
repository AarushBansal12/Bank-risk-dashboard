import pandas as pd
import numpy as np
import sqlite3
import os

# Set seed for reproducibility
np.random.seed(42)

def generate_alm_portfolio(num_records=1000):
    """Generates a simplified Asset and Liability portfolio for the bank."""
    print("Generating ALM Portfolio...")
    
    # Asset Categories
    asset_types = ['Retail Loan', 'Corporate Loan', 'Mortgage', 'Government Bond (HQLA)']
    asset_probs = [0.3, 0.35, 0.25, 0.1]
    
    # Liability Categories
    liability_types = ['Retail CASA Deposit', 'Term Deposit', 'Wholesale Funding']
    liability_probs = [0.4, 0.4, 0.2]
    
    portfolio = []
    
    # Generate Assets
    for _ in range(int(num_records * 1.5)): # More assets, to be balanced out later
        a_type = np.random.choice(asset_types, p=asset_probs)
        balance = np.random.uniform(50000, 5000000)
        
        if a_type == 'Retail Loan':
            duration = np.random.uniform(1.0, 5.0)
            rate = np.random.uniform(0.06, 0.10)
        elif a_type == 'Corporate Loan':
            duration = np.random.uniform(0.5, 3.0)
            rate = np.random.uniform(0.05, 0.08)
        elif a_type == 'Mortgage':
            duration = np.random.uniform(5.0, 15.0)
            rate = np.random.uniform(0.04, 0.07)
        else: # HQLA
            duration = np.random.uniform(0.1, 2.0)
            rate = np.random.uniform(0.02, 0.04)
            
        portfolio.append({
            'product_id': f"A_{len(portfolio)+1:05d}",
            'type': 'Asset',
            'category': a_type,
            'balance': balance,
            'interest_rate': rate,
            'duration_years': duration,
            'repricing_maturity_years': duration * np.random.uniform(0.8, 1.0) # slightly less or equal to duration
        })

    # Generate Liabilities
    for _ in range(num_records):
        l_type = np.random.choice(liability_types, p=liability_probs)
        balance = np.random.uniform(10000, 8000000)
        
        if l_type == 'Retail CASA Deposit':
            duration = np.random.uniform(0.0, 0.5) # typically non-maturity, modelled short
            rate = np.random.uniform(0.00, 0.02)
        elif l_type == 'Term Deposit':
            duration = np.random.uniform(0.5, 3.0)
            rate = np.random.uniform(0.03, 0.05)
        else: # Wholesale Funding
            duration = np.random.uniform(1.0, 5.0)
            rate = np.random.uniform(0.04, 0.06)
            
        portfolio.append({
            'product_id': f"L_{len(portfolio)+1:05d}",
            'type': 'Liability',
            'category': l_type,
            'balance': balance,
            'interest_rate': rate,
            'duration_years': duration,
            'repricing_maturity_years': duration * np.random.uniform(0.8, 1.0)
        })

    df = pd.DataFrame(portfolio)
    
    # Scale liabilities so total assets approx = total liabilities + equity (assume 10% equity)
    total_assets = df[df['type'] == 'Asset']['balance'].sum()
    total_liabilities = df[df['type'] == 'Liability']['balance'].sum()
    
    target_liabilities = total_assets * 0.90 # 10% equity buffer
    scaling_factor = target_liabilities / total_liabilities
    
    df.loc[df['type'] == 'Liability', 'balance'] *= scaling_factor
    
    return df

def calculate_irrbb_metrics(df):
    """Calculates Interest Rate Risk in the Banking Book metrics."""
    print("Calculating IRRBB Metrics...")
    
    assets = df[df['type'] == 'Asset']
    liabilities = df[df['type'] == 'Liability']
    
    total_assets = assets['balance'].sum()
    total_liabilities = liabilities['balance'].sum()
    
    # 1. Duration Gap Analysis
    asset_duration = np.average(assets['duration_years'], weights=assets['balance'])
    liability_duration = np.average(liabilities['duration_years'], weights=liabilities['balance'])
    
    duration_gap = asset_duration - (total_liabilities / total_assets) * liability_duration
    
    # 2. Earnings Perspective (NII Sensitivity over 1 Year)
    # Rate sensitive assets/liabilities within 1 year
    rsa_1y = assets[assets['repricing_maturity_years'] <= 1.0]['balance'].sum()
    rsl_1y = liabilities[liabilities['repricing_maturity_years'] <= 1.0]['balance'].sum()
    
    one_year_gap = rsa_1y - rsl_1y
    
    shocks = [-0.02, -0.01, 0.01, 0.02] # -200bps, -100bps, +100bps, +200bps
    
    nii_impacts = []
    
    for shock in shocks:
        nii_impact = one_year_gap * shock
        # EVE Impact = - Duration Gap * Total Assets * Shock
        eve_impact = -duration_gap * total_assets * shock
        
        nii_impacts.append({
            'shock_bps': int(shock * 10000),
            'nii_impact': nii_impact,
            'eve_impact': eve_impact
        })
        
    metrics = {
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'asset_duration': asset_duration,
        'liability_duration': liability_duration,
        'duration_gap': duration_gap,
        'rsa_1y': rsa_1y,
        'rsl_1y': rsl_1y,
        'one_year_gap': one_year_gap
    }
    
    return metrics, pd.DataFrame(nii_impacts)

def calculate_lcr(df):
    """Calculates Liquidity Coverage Ratio (simplified 30-day)."""
    print("Calculating LCR Components...")
    
    # 1. HQLA
    hqla = df[df['category'] == 'Government Bond (HQLA)']['balance'].sum()
    
    # 2. Cash Outflows (30 days)
    # Applying standard run-off assumptions to balances
    liabilities = df[df['type'] == 'Liability'].copy()
    
    # Assume a certain % of liabilities mature or run off in 30 days
    outflow_factors = {
        'Retail CASA Deposit': 0.05, # 5% run-off for stable retail deposits
        'Term Deposit': 0.10, # 10% run-off
        'Wholesale Funding': 0.40 # 40% run-off for unsecured wholesale
    }
    
    liabilities['outflow_factor'] = liabilities['category'].map(outflow_factors)
    liabilities['expected_outflow_30d'] = liabilities['balance'] * liabilities['outflow_factor']
    total_outflows = liabilities['expected_outflow_30d'].sum()
    
    # 3. Cash Inflows (30 days)
    assets = df[df['type'] == 'Asset'].copy()
    
    inflow_factors = {
        'Retail Loan': 0.02,
        'Corporate Loan': 0.05,
        'Mortgage': 0.01,
        'Government Bond (HQLA)': 0.00 # HQLA is already counted in numerator
    }
    
    assets['inflow_factor'] = assets['category'].map(inflow_factors)
    assets['expected_inflow_30d'] = assets['balance'] * assets['inflow_factor']
    total_inflows = assets['expected_inflow_30d'].sum()
    
    # Basel rules usually cap inflows at 75% of outflows
    capped_inflows = min(total_inflows, total_outflows * 0.75)
    
    net_cash_outflows = total_outflows - capped_inflows
    
    lcr = hqla / net_cash_outflows if net_cash_outflows > 0 else float('inf')
    
    lcr_metrics = {
        'hqla': hqla,
        'total_outflows_30d': total_outflows,
        'total_inflows_30d': total_inflows,
        'capped_inflows_30d': capped_inflows,
        'net_cash_outflows_30d': net_cash_outflows,
        'lcr_ratio': lcr
    }
    
    return pd.DataFrame([lcr_metrics])

def save_results(portfolio_df, irrbb_metrics, nii_df, lcr_df, db_path='../credit_risk.db'):
    # Fix db_path relative to script execution. If run from data-generation, it's ../credit_risk.db
    # If run from project root, it's credit_risk.db
    if not os.path.exists(db_path) and os.path.exists('credit_risk.db'):
        db_path = 'credit_risk.db'
    
    print(f"Saving results to {db_path}...")
    conn = sqlite3.connect(db_path)
    
    # Save to SQLite
    portfolio_df.to_sql('alm_portfolio', conn, if_exists='replace', index=False)
    
    irrbb_df = pd.DataFrame([irrbb_metrics])
    irrbb_df.to_sql('alm_irrbb_summary', conn, if_exists='replace', index=False)
    
    nii_df.to_sql('alm_nii_eve_shocks', conn, if_exists='replace', index=False)
    
    lcr_df.to_sql('alm_lcr_summary', conn, if_exists='replace', index=False)
    
    conn.close()
    
    # Save to CSV for Tableau
    print("Exporting CSVs for Tableau...")
    out_dir = 'output' if os.path.basename(os.getcwd()) == 'data-generation' else 'data-generation/output'
    os.makedirs(out_dir, exist_ok=True)
    
    portfolio_df.to_csv(os.path.join(out_dir, 'alm_portfolio.csv'), index=False)
    irrbb_df.to_csv(os.path.join(out_dir, 'alm_irrbb_summary.csv'), index=False)
    nii_df.to_csv(os.path.join(out_dir, 'alm_nii_eve_shocks.csv'), index=False)
    lcr_df.to_csv(os.path.join(out_dir, 'alm_lcr_summary.csv'), index=False)

if __name__ == "__main__":
    portfolio = generate_alm_portfolio(1500)
    
    irrbb_metrics, nii_df = calculate_irrbb_metrics(portfolio)
    
    lcr_df = calculate_lcr(portfolio)
    
    print("\n--- IRRBB SUMMARY ---")
    for k, v in irrbb_metrics.items():
        if 'duration' in k or 'gap' in k and not 'one_year' in k:
            print(f"{k}: {v:.2f} years")
        else:
            print(f"{k}: ${v:,.2f}")
            
    print("\n--- RATE SHOCKS ---")
    print(nii_df)
    
    print("\n--- LCR SUMMARY ---")
    for col in lcr_df.columns:
        if 'ratio' in col:
            print(f"{col}: {lcr_df[col].iloc[0]:.2%}")
        else:
            print(f"{col}: ${lcr_df[col].iloc[0]:,.2f}")
            
    save_results(portfolio, irrbb_metrics, nii_df, lcr_df)
    print("Done!")
