# Bank Credit Risk Analytics Dashboard — Masterplan

**Project:** Bank Credit Risk Analytics Dashboard (Tableau + SQL)
**Dataset:** Simulated Indian bank loan portfolio
**Skills demonstrated:** SQL, Tableau, dashboarding, credit risk analytics

This is built to look like a genuine bank risk-analytics deliverable, not a tutorial project. It's broken into chunks you can execute one at a time. Each chunk has a clear output, so you always know when you're "done" with that piece.

---

## Chunk 0 — Define the story before touching data (30 min)

Every strong analytics project answers a business question, not just "here's a dashboard." Decide upfront:

- **Portfolio size**: e.g., 15,000–25,000 loans (big enough to look real, small enough to compute fast)
- **Time window**: e.g., disbursements from 2018–2025, monthly snapshots
- **Business question you're answering**: "Where is credit risk concentrated in this portfolio, and how much capital should be provisioned against expected losses?"

Write this as a 3-line problem statement — you'll reuse it as your dashboard's intro and your resume bullet.

---

## Chunk 1 — Design the data model (this determines everything downstream)

Build these tables (simulate in Python/SQL, not Excel — it's more credible and reusable):

**1. `customers`**
`customer_id, name (fake), age, occupation, annual_income, state, city, customer_since_date`

**2. `loans`**
`loan_id, customer_id, loan_type (Home/Auto/Personal/MSME/Agri/Education), sanction_amount, disbursed_amount, interest_rate, tenure_months, disbursement_date, sector (e.g., Manufacturing, Retail, Agriculture, IT, Real Estate), branch_id, region (North/South/East/West)`

**3. `repayment_schedule`**
`loan_id, installment_no, due_date, due_amount, paid_amount, paid_date, dpd (days past due)`

**4. `credit_ratings`**
`loan_id, rating_date, external_rating (AAA→D scale) or internal_rating (1–10), PD (probability of default)`

**5. `npa_flags`** (better derived than hardcoded)
`loan_id, as_of_date, dpd_bucket (0, 1-30, 31-60, 61-90, 90+), asset_classification (Standard/SMA-0/SMA-1/SMA-2/NPA)`
NPA per RBI norms = 90+ DPD.

**6. `branches`**
`branch_id, branch_name, city, state, region`

### Realism tips (this is what makes it "Indian bank" specific)
- Use RBI's actual asset classification logic: Standard → SMA-0 (1-30 DPD) → SMA-1 (31-60) → SMA-2 (61-90) → NPA (90+)
- Sectors: Agriculture, MSME, Retail Trade, Manufacturing, Real Estate, Infrastructure, Services, IT/ITES — these mirror real RBI sectoral exposure reports
- Regional skew: more loan volume in Maharashtra, Gujarat, Delhi, Karnataka, Tamil Nadu, UP (matches real geographic concentration)
- Build in *deliberate risk patterns* — e.g., Agri loans with seasonal defaults, Real Estate with high-ticket concentration, one or two branches with abnormally high NPA — so your dashboard has real insights to surface, not flat random noise

**Deliverable:** A data dictionary (1-page doc) listing every table/column — this alone is a portfolio artifact recruiters like seeing.

---

## Chunk 2 — Generate the synthetic dataset (Python, not manually)

Use Python (`pandas`, `numpy`, `faker`) to generate this. Key generation logic:
- Sample customers with realistic income/age distributions
- Assign loans with sector/region weighting as above
- Simulate repayment behavior using a probability-of-default model tied to rating + sector + macro shock (e.g., simulate a stress period in one region/sector)
- Derive DPD, asset classification, and NPA flags from the simulated repayment schedule (don't hardcode NPA — derive it, so it's defensible)

**Deliverable:** CSVs (or a SQLite/Postgres DB) with 15k–25k loans, multi-year repayment history.

---

## Chunk 3 — Load into a real SQL environment

Use PostgreSQL, MySQL, or even SQLite/BigQuery sandbox — anything queryable and showable in your resume ("SQL: PostgreSQL"). Load your CSVs, define primary/foreign keys, add indexes on `loan_id`, `customer_id`, `as_of_date`.

---

## Chunk 4 — Write the SQL layer (proof of the "SQL" skill)

Organize as a set of `.sql` files in a GitHub repo, each solving a specific analytical need:

**a) KPI queries** (feed Executive Overview page)
Total portfolio outstanding, total disbursed YTD, Gross NPA %, Net NPA %, Provision Coverage Ratio (PCR), average ticket size, YoY portfolio growth.

**b) Sector exposure aggregation**
`GROUP BY sector` → total exposure, % of portfolio, NPA % by sector, average PD by sector.

**c) Geographic exposure**
`GROUP BY state/region` → exposure concentration, NPA heatmap inputs.

**d) High-risk borrower identification**
Window functions (`RANK()`, `DENSE_RANK()`) to rank customers/loans by PD × exposure (expected loss contribution). Flag "watchlist" accounts: SMA-2 status + high ticket size + declining rating trend.

**e) Credit rating migration / distribution**
Rating distribution by count and by exposure value. (Stretch) rating migration matrix: rating at T0 vs T1 using `LAG()`.

**f) Expected Credit Loss (ECL) — the differentiator**
- ECL = PD × LGD × EAD (Loss Given Default × Exposure at Default)
- Stage loans per Ind AS 109 / IFRS 9 logic: Stage 1 (Standard, 12-month ECL), Stage 2 (SMA, lifetime ECL), Stage 3 (NPA, lifetime ECL with higher LGD)
- Build a `view` or summary table: ECL by sector, by stage, total provisioning requirement

**g) Summary tables for Tableau**
Pre-aggregate what's expensive to compute live: `vw_kpi_summary`, `vw_sector_exposure`, `vw_geo_exposure`, `vw_rating_distribution`, `vw_ecl_summary`, `vw_top_risk_borrowers` — Tableau connects to these views, not raw tables. This is exactly how it's done in real banking BI teams, and it's a great talking point in interviews ("I built a semantic layer of SQL views rather than dashboarding off raw transactional tables").

**Deliverable:** A `/sql` folder with these queries + comments explaining business logic.

---

## Chunk 5 — Build the Tableau dashboard (page by page)

Connect Tableau to your SQL views. Build in this order (easiest → hardest):

1. **Credit Rating Distribution** — bar/donut of rating buckets by count and exposure. Simple, builds comfort with the data.
2. **Sector-wise Exposure** — treemap or bar chart of exposure by sector, NPA % overlay (dual-axis or color-coded).
3. **Geographic Exposure** — filled map of India by state, exposure/NPA concentration (Tableau has built-in India geo-roles at state level).
4. **Loan Portfolio** — portfolio composition by loan type, vintage analysis (disbursement trends over time), ticket size distribution.
5. **NPA Analysis** — Gross/Net NPA trend over time, NPA by sector/region/vintage, movement (fresh slippage vs recoveries).
6. **Expected Credit Loss Analysis** — ECL by stage (1/2/3), provisioning trend, ECL as % of exposure by sector — the most "advanced" page.
7. **Executive Overview** — build this **last**. It's a summary of everything above: KPI cards (Gross NPA%, Net NPA%, PCR, Total ECL, Portfolio Growth) + 2-3 headline charts + a "key risk callouts" text box. This is the page a CRO/hiring manager sees first, so it needs to be the tightest.

### Design tips
- Use consistent color logic across pages: red/amber/green for risk, one color per region/sector reused everywhere
- Add filters: date range, region, sector, loan type — global filters actioned across the workbook
- Add tooltips with context, not just numbers
- Use parameters for a toggle like "View by: Count / Exposure Value"

**Deliverable:** A published Tableau Public workbook link.

---

## Chunk 6 — Package it for your resume/portfolio

- **GitHub repo** with: `/data-generation` (Python script), `/sql` (queries + views), `/docs` (data dictionary, ER diagram, 1-page methodology note on ECL/NPA logic), Tableau `.twbx` file, and a README with screenshots + the Tableau Public link
- **1-page write-up**: problem → data → approach → key findings (e.g., "Agri sector showed 3.2x higher NPA ratio, driving 40% of total ECL despite being 18% of exposure") — findings like this are what interviewers actually want to discuss
- **Resume bullet (draft)**: *"Built an end-to-end credit risk analytics dashboard on a simulated ₹X Cr Indian bank loan portfolio — designed SQL data models and views to compute NPA, sector/geographic exposure, and Expected Credit Loss (Ind AS 109), visualized in a 7-page Tableau dashboard used to identify high-risk borrower segments."*

---

## Suggested pace

| Chunk | Content | Time |
|---|---|---|
| 0–1 | Design | 1 day |
| 2–3 | Data generation + loading | 1–2 days |
| 4 | SQL (the meatiest part) | 2–3 days |
| 5 | Tableau, page by page | 3–4 days |
| 6 | Packaging | 1 day |

**Total: roughly 1.5–2 weeks done properly.**
