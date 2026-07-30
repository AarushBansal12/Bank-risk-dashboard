import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker('en_IN')
Faker.seed(42)
np.random.seed(42)
random.seed(42)

NUM_CUSTOMERS = 20000
NUM_LOANS = 22000

# Setup Output Directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

print("Starting Data Generation...")

# 1. Generate Branches
branches_data = [
    {"branch_id": "B001", "branch_name": "Mumbai Main", "city": "Mumbai", "state": "Maharashtra", "region": "West"},
    {"branch_id": "B002", "branch_name": "Pune Camp", "city": "Pune", "state": "Maharashtra", "region": "West"},
    {"branch_id": "B003", "branch_name": "Delhi Connaught Place", "city": "New Delhi", "state": "Delhi", "region": "North"},
    {"branch_id": "B004", "branch_name": "Bangalore MG Road", "city": "Bangalore", "state": "Karnataka", "region": "South"},
    {"branch_id": "B005", "branch_name": "Chennai Anna Salai", "city": "Chennai", "state": "Tamil Nadu", "region": "South"},
    {"branch_id": "B006", "branch_name": "Ahmedabad SG Highway", "city": "Ahmedabad", "state": "Gujarat", "region": "West"},
    {"branch_id": "B007", "branch_name": "Kolkata Park Street", "city": "Kolkata", "state": "West Bengal", "region": "East"},
    {"branch_id": "B008", "branch_name": "Hyderabad Banjara Hills", "city": "Hyderabad", "state": "Telangana", "region": "South"},
    {"branch_id": "B009", "branch_name": "Lucknow Hazratganj", "city": "Lucknow", "state": "Uttar Pradesh", "region": "North"},
    {"branch_id": "B010", "branch_name": "Jaipur MI Road", "city": "Jaipur", "state": "Rajasthan", "region": "North"},
]
df_branches = pd.DataFrame(branches_data)
df_branches.to_csv(os.path.join(OUTPUT_DIR, 'branches.csv'), index=False)
print("Branches generated.")

# 2. Generate Customers
print("Generating Customers...")
customer_ids = [f"C{str(i).zfill(6)}" for i in range(1, NUM_CUSTOMERS + 1)]
occupations = ['Salaried', 'Self-Employed', 'Business', 'Professional', 'Retired']

customers = []
for cid in customer_ids:
    age = np.random.randint(21, 70)
    income = np.random.lognormal(mean=13, sigma=0.8) # Right skewed income
    income = round(income, -3)
    if income < 150000: income = 150000
    if income > 50000000: income = 50000000
    
    customers.append({
        "customer_id": cid,
        "name": fake.name(),
        "age": age,
        "occupation": np.random.choice(occupations, p=[0.5, 0.2, 0.2, 0.05, 0.05]),
        "annual_income": income,
        "state": np.random.choice(df_branches['state']),
        "city": "To Be Mapped", # Simplified for now, real model would map city to state
        "customer_since_date": fake.date_between(start_date="-10y", end_date="today")
    })
df_customers = pd.DataFrame(customers)
# Fix cities based on state
state_to_city = df_branches.set_index('state')['city'].to_dict()
df_customers['city'] = df_customers['state'].map(state_to_city)
df_customers.to_csv(os.path.join(OUTPUT_DIR, 'customers.csv'), index=False)
print("Customers generated.")

# 3. Generate Loans
print("Generating Loans...")
loan_types = ['Home', 'Auto', 'Personal', 'MSME', 'Agri', 'Education']
sectors = ['Manufacturing', 'Retail Trade', 'Agriculture', 'IT/ITES', 'Real Estate', 'Infrastructure', 'Services']

loans = []
for i in range(1, NUM_LOANS + 1):
    lid = f"L{str(i).zfill(6)}"
    cid = np.random.choice(customer_ids)
    ltype = np.random.choice(loan_types, p=[0.3, 0.2, 0.25, 0.1, 0.1, 0.05])
    
    # Dependent logic
    if ltype == 'Home':
        sanction = np.random.randint(1500000, 20000000)
        tenure = np.random.choice([120, 180, 240, 360])
        rate = round(np.random.uniform(8.0, 10.5), 2)
        sector = 'Real Estate'
    elif ltype == 'Auto':
        sanction = np.random.randint(300000, 3000000)
        tenure = np.random.choice([36, 48, 60, 84])
        rate = round(np.random.uniform(9.0, 12.0), 2)
        sector = 'Services'
    elif ltype == 'Personal':
        sanction = np.random.randint(50000, 1000000)
        tenure = np.random.choice([12, 24, 36, 48, 60])
        rate = round(np.random.uniform(11.0, 18.0), 2)
        sector = 'Services'
    elif ltype == 'MSME':
        sanction = np.random.randint(1000000, 50000000)
        tenure = np.random.choice([24, 36, 60, 84, 120])
        rate = round(np.random.uniform(9.5, 14.0), 2)
        sector = np.random.choice(['Manufacturing', 'Retail Trade', 'Services', 'IT/ITES'])
    elif ltype == 'Agri':
        sanction = np.random.randint(50000, 5000000)
        tenure = np.random.choice([12, 24, 36])
        rate = round(np.random.uniform(7.0, 11.0), 2)
        sector = 'Agriculture'
    else: # Education
        sanction = np.random.randint(200000, 5000000)
        tenure = np.random.choice([60, 84, 120])
        rate = round(np.random.uniform(9.0, 13.0), 2)
        sector = 'Services'
        
    branch = df_branches.sample(1).iloc[0]
    disbursed = sanction * np.random.uniform(0.9, 1.0) # Assume some limit not fully drawn
    
    loans.append({
        "loan_id": lid,
        "customer_id": cid,
        "loan_type": ltype,
        "sanction_amount": round(sanction, 2),
        "disbursed_amount": round(disbursed, 2),
        "interest_rate": rate,
        "tenure_months": tenure,
        "disbursement_date": fake.date_between(start_date="-5y", end_date="-1m"),
        "sector": sector,
        "branch_id": branch['branch_id'],
        "region": branch['region']
    })
df_loans = pd.DataFrame(loans)
df_loans.to_csv(os.path.join(OUTPUT_DIR, 'loans.csv'), index=False)
print("Loans generated.")

# 4 & 5. Generate Repayment Schedule & Ratings
print("Generating Repayments and Ratings (This might take a minute)...")
repayments = []
ratings = []

current_date = datetime.now().date()

for _, loan in df_loans.iterrows():
    lid = loan['loan_id']
    tenure = loan['tenure_months']
    disb_date = loan['disbursement_date']
    
    # Calculate EMI roughly
    r = loan['interest_rate'] / 12 / 100
    p = loan['disbursed_amount']
    if r == 0:
        emi = p / tenure
    else:
        emi = p * r * ((1+r)**tenure) / (((1+r)**tenure) - 1)
    
    # Risk Profile
    risk_factor = np.random.uniform(0, 1)
    
    # Deliberate Risk Adjustments
    if loan['sector'] == 'Agriculture': risk_factor += 0.1
    if loan['loan_type'] == 'Personal': risk_factor += 0.05
    if loan['region'] == 'East': risk_factor += 0.05
    
    base_rating = 1
    if risk_factor > 0.9: base_rating = np.random.randint(8, 11)
    elif risk_factor > 0.7: base_rating = np.random.randint(4, 8)
    else: base_rating = np.random.randint(1, 4)
    
    # Record Rating
    ratings.append({
        "loan_id": lid,
        "rating_date": current_date, # Assume latest rating
        "internal_rating": base_rating,
        "PD": round((base_rating ** 2.2) * 0.1, 2) # Exponential PD
    })
    
    is_defaulting = base_rating > 7
    default_start_month = np.random.randint(1, tenure) if is_defaulting else 999
    
    for i in range(1, tenure + 1):
        due_date = disb_date + timedelta(days=30 * i)
        if due_date > current_date:
            break # Hasn't happened yet
            
        due_amount = round(emi, 2)
        paid_amount = due_amount
        dpd = 0
        
        # Simulate payment behavior
        if i >= default_start_month:
            # Stopped paying entirely
            paid_amount = 0
            dpd = (current_date - due_date).days
        else:
            # Late payments
            if risk_factor > 0.6 and np.random.random() < 0.2:
                delay = np.random.randint(5, 45)
                paid_date = due_date + timedelta(days=delay)
                if paid_date > current_date:
                    dpd = (current_date - due_date).days
                    paid_amount = 0 # Not paid yet as of today
                else:
                    dpd = delay # Was late, but paid
            else:
                # Paid on time
                delay = np.random.randint(-5, 2)
                paid_date = due_date + timedelta(days=delay)
                
        repayments.append({
            "loan_id": lid,
            "installment_no": i,
            "due_date": due_date,
            "due_amount": due_amount,
            "paid_amount": paid_amount,
            "paid_date": due_date if paid_amount > 0 else None, # Simplifying paid date
            "dpd": max(0, dpd)
        })

df_repayments = pd.DataFrame(repayments)
df_repayments.to_csv(os.path.join(OUTPUT_DIR, 'repayment_schedule.csv'), index=False)

df_ratings = pd.DataFrame(ratings)
df_ratings.to_csv(os.path.join(OUTPUT_DIR, 'credit_ratings.csv'), index=False)

print("Data generation complete! Files saved to data-generation/ folder.")
