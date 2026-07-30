# Methodology & Logic Notes

## 1. Asset Classification (RBI Norms)
The dashboard simulates non-performing assets (NPAs) strictly according to the Reserve Bank of India (RBI) income recognition and asset classification (IRAC) norms:
- **Standard**: 0 DPD (Days Past Due)
- **SMA-0 (Special Mention Account)**: 1 to 30 DPD
- **SMA-1**: 31 to 60 DPD
- **SMA-2**: 61 to 90 DPD
- **NPA**: 90+ DPD

*Note: In reality, SMA starts upon failure to pay on the due date. The logic applied here derives the classification directly from the max DPD in the repayment schedule as of the reporting date.*

## 2. Expected Credit Loss (ECL) Calculation
The model implements a simplified version of Ind AS 109 / IFRS 9 ECL calculation.
ECL is computed as: **ECL = PD × LGD × EAD**
- **PD (Probability of Default)**: Assigned based on the internal credit rating (1 to 10 scale). 
- **LGD (Loss Given Default)**: Assumed to be a fixed percentage based on staging and loan type (e.g., Home loans might have 20% LGD due to collateral, whereas Personal loans might have 60% LGD).
- **EAD (Exposure at Default)**: The outstanding principal balance + accrued interest.

### ECL Staging
- **Stage 1 (Performing)**: Loans classified as Standard or SMA-0. Requires 12-month ECL.
- **Stage 2 (Under-Performing)**: Loans classified as SMA-1 or SMA-2, indicating a Significant Increase in Credit Risk (SICR). Requires Lifetime ECL.
- **Stage 3 (Non-Performing)**: Loans classified as NPA (90+ DPD). Requires Lifetime ECL with potentially higher LGD assumptions.

## 3. Synthetic Data Logic
To prevent the dashboard from looking like flat, random noise, the Python data generator enforces deliberate risk patterns:
1. **Sectoral Risk**: Agriculture and MSME sectors have a slightly higher baseline PD and are more susceptible to defaults.
2. **Geographic Concentration**: Loan volumes are realistically skewed towards major commercial states (Maharashtra, Gujarat, Delhi, Karnataka, Tamil Nadu).
3. **Rating Migration**: Some borrower ratings degrade intentionally over time to show migration into Stage 2 and Stage 3.
