# Compliance Validation Knowledge Base

## 1. Group Accounting Standards
The group adheres to **International Financial Reporting Standards (IFRS)** as the primary framework, with specific group policies outlined below:
- **Revenue Recognition**: Follow IFRS 15. Revenue is recognized when control of goods or services is transferred, based on performance obligations.
- **Consolidation**: All subsidiaries must consolidate financials per IFRS 10. Full consolidation required for entities with >50% ownership.
- **Fixed Assets**: Depreciate per IAS 16 using straight-line method unless otherwise specified by group policy.
- **Leases**: Apply IFRS 16. All leases (except short-term/low-value) recognized as right-of-use assets and lease liabilities.
- **Group Chart of Accounts**: All subsidiaries must map local accounts to the group’s standardized chart of accounts (available in `Group_Accounting_Manual_v3.pdf`).

### Deviations
- Any deviation from IFRS or group policies must be documented with justification and approved by the Group CFO.
- Common issues: Incorrect revenue recognition timing, unadjusted goodwill impairments (IAS 36), or non-standard depreciation methods.

## 2. Local GAAP Adjustments
- Subsidiaries must adjust local GAAP financials to align with IFRS for group reporting.
- Common adjustments:
  - **Revenue**: Adjust for differences in revenue recognition (e.g., US GAAP ASC 606 vs. IFRS 15).
  - **Inventory**: Convert LIFO (if used locally) to FIFO per IFRS (IAS 2).
  - **Provisions**: Adjust for differences in recognition thresholds (IAS 37 vs. local standards).
- Adjustment template: Available in `Local_GAAP_Adjustment_Form.xlsx`.
- Flag any unadjusted differences >5% of reported revenue or assets.

### Corrective Actions
- Provide subsidiaries with the adjustment template and IFRS reference.
- Escalate unadjusted material differences to Group Finance for review.

## 3. Foreign Exchange (FX) Translation
- **Functional Currency**: Determined per IAS 21. Use subsidiary’s primary economic environment currency.
- **Translation to Presentation Currency**: Use group presentation currency (USD).
  - **Assets/Liabilities**: Use closing rate at reporting date.
  - **Income/Expenses**: Use average rate for the period (sourced from `Group_FX_Rates_Monthly.xlsx`).
  - **Equity**: Use historical rates for initial recognition.
- **Approved FX Rates**: Sourced from `Group_FX_Rates_Monthly.xlsx`, updated monthly by Group Treasury.
- **Hedging**: Apply IFRS 9 for hedge accounting. Document hedge effectiveness if applicable.
- Deviations: Flag use of non-approved FX rates or incorrect translation methods.

### Corrective Actions
- Recalculate using approved rates and provide corrected figures to subsidiary.
- Advise on proper documentation for hedge accounting if missing.

## 4. Intercompany Eliminations
- **Process**: Per IFRS 10, eliminate all intercompany transactions (e.g., sales, loans, dividends) in consolidation.
- **Common Issues**:
  - Mismatched intercompany balances (e.g., Subsidiary A reports receivable, but Subsidiary B omits payable).
  - Unreported intercompany loans or interest.
- **Reconciliation**:
  - Use `Intercompany_Reconciliation_Template.xlsx` to match balances.
  - Flag mismatches >1% of total intercompany balances.
- **Corrective Actions**:
  - Request subsidiary to resubmit corrected intercompany schedules.
  - Escalate persistent mismatches to Group Consolidation Team.

## 5. Adoption of New Accounting Standards
- **New Standards (as of August 2025)**:
  - **IFRS 17 (Insurance Contracts)**: Mandatory for insurance subsidiaries. Effective for periods beginning on/after January 1, 2023.
  - **IAS 1 Amendments**: Enhanced disclosure for accounting policies (effective January 1, 2023).
- **Adoption Process**:
  - Subsidiaries must submit an **Adoption Checklist** (`New_Standard_Checklist.xlsx`) confirming compliance.
  - Flag subsidiaries not adopting new standards or missing documentation.
- **Common Issues**:
  - Incomplete IFRS 17 transition disclosures.
  - Inconsistent application of IAS 1 disclosure requirements.
- **Corrective Actions**:
  - Provide subsidiaries with adoption checklist and IFRS guidance.
  - Summarize adoption status across subsidiaries in validation report.

## 6. Handling Missing or Inconsistent Data
- **Steps for Reconciliation**:
  1. Identify missing data (e.g., trial balance, intercompany schedules).
  2. Request resubmission from subsidiary with a 5-day deadline.
  3. Cross-check with prior period submissions for consistency.
  4. Use FileTools to access subsidiary submissions if available.
- **Inconsistencies**:
  - Flag discrepancies >2% of reported figures (e.g., revenue, assets).
  - Compare with group benchmarks (e.g., industry ratios in `Group_Benchmark_Data.xlsx`).
- **Corrective Actions**:
  - Advise subsidiary on specific data gaps and provide templates.
  - Escalate unresolved issues to Group Finance for audit.

## 7. Reporting and Flagging
- **Validation Report**:
  - Summarize compliance status, deviations, and corrective actions.
  - Include adoption status of new standards.
  - Use `Compliance_Validation_Report_Template.docx` for consistency.
- **Flagging Thresholds**:
  - Material deviations: >5% of revenue, assets, or equity.
  - Non-material but recurring issues: Flag after 2 periods of non-compliance.
- **Escalation**:
  - Material issues: Escalate to Group CFO and Audit Committee.
  - Non-material issues: Track in `Compliance_Issue_Tracker.xlsx` for follow-up.  

---

## 4. FAQs

- **Q:** What if a subsidiary hasn’t adopted a new IFRS standard?  
  **A:** Flag the deviation, provide guidance on implementation, and track for next period.  

- **Q:** How should intercompany FX mismatches be resolved?  
  **A:** Recalculate using approved FX rates, update elimination entries, and document adjustments.  

- **Q:** How to report partial compliance?  
  **A:** Include in the compliance report with notes on which accounts or standards are not fully adopted.
