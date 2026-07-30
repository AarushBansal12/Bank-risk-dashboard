# Data Dictionary

## 1. `customers`
Contains demographic and financial information for the borrowers.
- `customer_id` (VARCHAR): Unique identifier for the customer.
- `name` (VARCHAR): Full name of the customer (Synthetic).
- `age` (INT): Age of the customer in years.
- `occupation` (VARCHAR): Employment type (Salaried, Self-Employed, Business, etc.).
- `annual_income` (FLOAT): Annual income in INR.
- `state` (VARCHAR): State of residence.
- `city` (VARCHAR): City of residence.
- `customer_since_date` (DATE): Date when the customer onboarded.

## 2. `loans`
Contains details of the loan facilities sanctioned and disbursed.
- `loan_id` (VARCHAR): Unique identifier for the loan account.
- `customer_id` (VARCHAR): Foreign key referencing `customers`.
- `loan_type` (VARCHAR): Category of loan (Home, Auto, Personal, MSME, Agri, Education).
- `sanction_amount` (FLOAT): Total limit approved by the bank.
- `disbursed_amount` (FLOAT): Actual amount disbursed to the borrower.
- `interest_rate` (FLOAT): Annual interest rate on the loan.
- `tenure_months` (INT): Duration of the loan in months.
- `disbursement_date` (DATE): Date of loan disbursement.
- `sector` (VARCHAR): Economic sector (Manufacturing, Retail Trade, Agriculture, IT/ITES, Real Estate, Infrastructure, Services).
- `branch_id` (VARCHAR): Foreign key referencing `branches`.
- `region` (VARCHAR): Geographical region (North, South, East, West).

## 3. `repayment_schedule`
Tracks the installment history and days past due.
- `loan_id` (VARCHAR): Foreign key referencing `loans`.
- `installment_no` (INT): Installment number (1 to tenure).
- `due_date` (DATE): Date the payment is due.
- `due_amount` (FLOAT): Amount due for the installment.
- `paid_amount` (FLOAT): Actual amount paid by the borrower.
- `paid_date` (DATE): Date when the payment was made.
- `dpd` (INT): Days Past Due (calculated as `paid_date` - `due_date`, or `current_date` - `due_date` if unpaid).

## 4. `credit_ratings`
Internal ratings and corresponding probability of default.
- `loan_id` (VARCHAR): Foreign key referencing `loans`.
- `rating_date` (DATE): Date of the rating assessment.
- `internal_rating` (INT): 1 (Best) to 10 (Default).
- `PD` (FLOAT): Probability of Default (%) assigned to this rating scale.

## 5. `npa_flags`
Derived status of the loan account per RBI norms.
- `loan_id` (VARCHAR): Foreign key referencing `loans`.
- `as_of_date` (DATE): Snapshot date for the classification.
- `dpd_bucket` (VARCHAR): '0', '1-30', '31-60', '61-90', '90+'.
- `asset_classification` (VARCHAR): Standard, SMA-0, SMA-1, SMA-2, NPA.

## 6. `branches`
Branch locations originating the loans.
- `branch_id` (VARCHAR): Unique branch identifier.
- `branch_name` (VARCHAR): Name of the branch.
- `city` (VARCHAR): City location.
- `state` (VARCHAR): State location.
- `region` (VARCHAR): Region location.
