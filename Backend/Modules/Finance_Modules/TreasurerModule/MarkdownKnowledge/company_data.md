# 📘 Knowledge Base: Financial Best Practices & Internal Policies

## 1. Cash Flow Monitoring
- **Daily Balance Tracking**  
  - All operating accounts must be reconciled daily.  
  - Cash positions are consolidated across **BankA (Operating)**, **BankB (Loan)**, and **BankC (Investment)**.  
  - Any unexplained balance variance greater than **$5,000** must be flagged for review.

- **System of Record**  
  - The official cash ledger is maintained in **ERP Finance Module**.  
  - CSV imports from banks must be validated against ERP records daily.  

---

## 2. Cash Flow Forecasting
- **Revenue Inflows**  
  - Customer invoices are expected to be collected within **30 days of issue date**.  
  - A payment delay of more than **5 business days** must trigger a forecast adjustment.  

- **Expenditure Outflows**  
  - Payroll is processed on the **25th of every month**.  
  - Loan repayments follow the **quarterly schedule** defined in loan agreements.  
  - Supplier invoices exceeding **$10,000** require **CFO pre-approval** before payment.  

- **Forecasting Methodology**  
  - Forecasts are updated weekly using:  
    - Revenue pipeline (confirmed orders only).  
    - Debt maturities (sourced from Treasury database).  
    - Payroll and fixed expenses (from HR & Accounting systems).  

---

## 3. Liquidity Buffer Policy
- **Minimum Buffer Requirement**  
  - The company must maintain a minimum of **$50,000 or 2 months of payroll (whichever is higher)** across operating accounts.  
  - Cash in investment accounts is not considered part of the liquidity buffer.  

- **Idle Cash Optimization**  
  - Surplus above buffer may be moved to **short-term investment accounts** (≤ 90-day instruments).  
  - Treasury team decides allocation between:  
    - High-yield savings accounts.  
    - Money market funds.  
    - Treasury bills.  

---

## 4. Risk Management
- **Currency Exposure**  
  - All inflows/outflows in **EUR** must be reviewed for FX risk.  
  - If exposure exceeds **€100,000 in a month**, treasury must execute a forward contract hedge.  

- **Payment Timing Risk**  
  - Accounts Payable team must align supplier payments with forecasted inflows.  
  - Payments must not reduce buffer below the minimum threshold.  

- **Fraud Detection**  
  - Transactions over **$20,000** require dual approval (Treasury + CFO).  
  - Sudden unusual payments (non-regular suppliers, new beneficiaries) must trigger an anomaly check.  

---

## 5. Internal Governance
- **Roles & Responsibilities**  
  - **Treasury Department**: Monitors daily balances, executes investments, manages FX hedging.  
  - **Accounting Department**: Maintains ledger integrity, records inflows/outflows, ensures compliance.  
  - **CFO**: Approves major outflows, sets strategic liquidity policy, oversees treasury operations.  

- **Audit & Compliance**  
  - Monthly internal audit of cash flow reports.  
  - Quarterly external audit review.  
  - All records retained for **7 years** in compliance with financial regulations.  

---

## 6. Escalation Protocol
- **Liquidity Shortfall**  
  - If forecast shows a buffer shortfall within 30 days:  
    - Treasury informs CFO immediately.  
    - CFO approves short-term credit line usage if required.  

- **Unexpected Outflows**  
  - Any unplanned outflow above **$10,000** must be reported within **24 hours**.  
  - CFO decides whether to cover using buffer or short-term financing.  

---

✅ This KB provides financial best practices **(standardized forecasting, liquidity, and risk control)** combined with **internal company-specific rules** (buffer thresholds, approvals, escalation).  

# 📘 Knowledge Base: Financing Oversight & Internal Policies

## 1. Capital Structure Management
- **Leverage Targets**  
  - Maintain **Debt/EBITDA ≤ 3.0x** to ensure optimal credit rating.  
  - Equity and retained earnings should cover at least **40% of total capital**.  

- **Credit Metrics**  
  - Maintain **Interest Coverage ≥ 2.5x**.  
  - Ensure liquidity ratios comply with internal policy.  

- **Policy for Funding Mix**  
  - Preferred hierarchy: retained earnings → debt → equity issuance.  
  - Avoid excessive reliance on short-term debt for operational funding.  

---

## 2. Debt Management
- **Debt Monitoring**  
  - Track principal, interest rates, maturity, covenants, and amortization schedules.  
  - Review covenant compliance monthly.  

- **Refinancing Strategy**  
  - Monitor market interest rates via yfinance and compare with current debt terms.  
  - Consider refinancing when potential interest savings > 0.5% of principal.  

- **Interest Rate Exposure**  
  - Balance fixed vs. floating rate debt based on market outlook.  
  - Floating rate exposure should not exceed **50% of total debt** without CFO approval.  

---

## 3. Funding Strategy
- **Access to Capital**  
  - Maintain active credit lines, commercial paper programs, and repo facilities.  
  - Ensure undrawn credit lines cover at least **3 months of projected operating expenses**.  

- **Project/Acquisition Financing**  
  - Evaluate financing options for each project:  
    - Internal cash reserves  
    - Debt issuance  
    - Equity placement  

- **Public vs. Private Financing**  
  - For large-scale projects, compare cost and regulatory burden of public bonds vs. private placements.  

---

## 4. Relationship Management
- **Banks and Lenders**  
  - Maintain quarterly meetings to review covenant compliance and discuss refinancing.  
  - Negotiate favorable interest rates and flexible terms where possible.  

- **Investors & Credit Rating Agencies**  
  - Maintain transparent communication regarding company leverage and funding plans.  
  - Ensure timely submission of required financial metrics to credit rating agencies.  

- **Escalation Protocols**  
  - Significant covenant breach or inability to refinance must be reported to CFO immediately.  
  - Approval required for any new debt instrument exceeding **$2 million**.  

---

## 5. Reporting & Compliance
- **Internal Reporting**  
  - Monthly debt and capital structure report to CFO and Board.  
  - Highlight upcoming maturities, interest costs, and refinancing opportunities.  

- **External Compliance**  
  - Ensure all debt issuance and funding strategies comply with regulatory standards.  
  - Maintain records of all debt instruments for **7 years**.  

---

✅ This KB allows the agent to **reason about capital structure, refinancing, funding strategies, and lender relationships**, while following internal policies and best practices.

# 📘 Knowledge Base: Investment Oversight & Internal Policies

## 1. Investment Policy Compliance
- **Approved Asset Classes**  
  - Money market instruments, short-term bonds, government securities, corporate bonds with sufficient credit rating.  
  - No speculative or high-volatility instruments unless specifically approved by CFO.  

- **Credit Quality Limits**  
  - Minimum credit rating: AA for corporate bonds; AAA preferred for government bonds.  
  - Counterparty risk must be evaluated before each investment.  

- **Duration Limits**  
  - Money market: ≤ 12 months.  
  - Short-term bonds: ≤ 36 months.  
  - Government securities: ≤ 60 months unless approved for strategic allocation.  

---

## 2. Portfolio Allocation
- **Liquidity Buckets**  
  - Operational liquidity: cash for 1–2 months of operational expenses.  
  - Reserve liquidity: cash for 3–6 months of contingencies.  
  - Strategic surplus: long-term investments for yield optimization.  

- **Allocation Guidelines**  
  - Maintain sufficient allocation to operational and reserve liquidity before investing in strategic surplus.  
  - Adjust allocations based on interest rate outlook, risk appetite, and projected cash flow needs.  

---

## 3. Performance Monitoring
- **Benchmarking**  
  - Money market instruments vs. LIBOR or equivalent.  
  - Bonds vs. Treasury or corporate bond indices.  
- **Mark-to-Market Tracking**  
  - Track unrealized gains/losses daily for operational and strategic portfolios.  
  - Alert if losses exceed internal risk thresholds.  

---

## 4. Regulatory & Accounting Integration
- **Accounting Standards**  
  - Follow IFRS/GAAP for investment accounting.  
- **Liquidity Regulations**  
  - Ensure compliance with internal and external liquidity requirements (Basel III/IV if applicable).  

---

✅ Notes:
- Use this KB in combination with the **shared policies for CashFlow and Financing**.  
- The agent references these rules for allocation decisions, compliance checks, and risk alerts.  
