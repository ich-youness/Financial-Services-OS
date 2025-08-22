# ESG_Master_Knowledge.md

A comprehensive, **code-free** reference on Environmental, Social, and Governance (ESG) topics. This handbook defines concepts, boundaries, data shapes (plain language), formulas, mappings to common frameworks, evidence and assurance rules, acceptance criteria, sector notes, and example tables. It is designed so agents can **reason, extract, calculate, and explain** ESG topics consistently without relying on any implementation details.

---

## Table of Contents
1. Purpose & Scope 
2. Core Concepts
3. Reporting Boundaries & Periods  
4. Canonical Data (Plain Language)  
5. Environmental Pillar
   - 5.1 Climate (GHG Scopes 1, 2, 3)  
   - 5.2 Energy Management  
   - 5.3 Water Stewardship  
   - 5.4 Circularity & Waste  
   - 5.5 Pollution (Air/Water/Soil)  
   - 5.6 Biodiversity & Land Use  
6. Social Pillar 
   - 6.1 Workforce (Employment, Labor Practices)  
   - 6.2 Health & Safety  
   - 6.3 Diversity, Equity & Inclusion  
   - 6.4 Human Rights & Supply Chain Social Standards  
   - 6.5 Customer & Product Responsibility  
   - 6.6 Community & Social Investment  
7. Governance Pillar  
   - 7.1 Board Composition & Oversight  
   - 7.2 Ethics, Anti-Corruption & Compliance  
   - 7.3 Risk Management & Internal Control  
   - 7.4 Data Governance, Privacy & Cybersecurity  
   - 7.5 Remuneration & ESG Incentives  
   - 7.6 Tax Transparency & Responsible Lobbying  
8. Materiality & Stakeholder Engagement  
9. Targets, Pathways & Transition Planning  
10. Frameworks & Mappings  
11. EU Taxonomy (Eligibility, Alignment, DNSH, Safeguards)
12. Evidence, Assurance & Data Quality 
13. Dashboards & Standard Reports 
14. Maturity Model & Roadmap 
15. Sector Notes (Examples) 
16. Common Pitfalls & Acceptance Criteria  
17. Glossary  
18. Versioning & Change Log Template 
19. Appendix A: Example Tables

---

## Purpose & Scope
**Objective.** Provide a single, authoritative reference to standardize ESG definitions, formulas, mappings, and acceptance criteria.  
**Use cases.** ESG strategy & governance, emissions accounting, regulatory disclosures, EU Taxonomy KPIs, social & governance metrics, investor communications, and internal decision-making.  
**Non-goals.** No implementation or system instructions. No references to any software or “tools.”

---

## Core Concepts
- **ESG:** Non-financial dimensions with material impact on enterprise value and stakeholder outcomes.  
- **Double Materiality:**  
  - *Impact materiality* (effects on people and environment).  
  - *Financial materiality* (effects on the company’s performance, cash flows, valuation).  
- **GHG Scopes:**  
  - *Scope 1* (direct emissions), *Scope 2* (purchased energy), *Scope 3* (value chain—15 categories).  
- **Assurance Readiness:** Every number must be reproducible from defined inputs, methods, parameters, and approvals.  
- **DNSH & Minimum Safeguards:** EU Taxonomy requirements in addition to technical screening criteria.

---

## Reporting Boundaries & Periods
- **Organizational boundary:** equity share / financial control / operational control (choose and document).  
- **Operational boundary:** which scopes and categories are in scope (explicitly list).  
- **Periodicity:** annual (fiscal year) with optional quarterly or monthly views for management.  
- **Restatements:** allowed for boundary or method changes; disclose rationale, magnitude, and restated prior periods.

---

## Canonical Data (Plain Language)
**Entity:** identifier, parent, country (ISO), sector (NACE/ISIC), reporting currency, consolidation method.  
**Activity record (emissions):** entity, date, scope, category, quantity, unit, emission-factor reference, GWP table (AR5/AR6), source type (meter/invoice/supplier/model), uncertainty %, evidence links.  
**Energy:** period, energy type (electricity/steam/heat/cooling/fuel), amount, unit, renewable instrument metadata (if claimed).  
**Water:** period, withdrawal, discharge, consumption, unit, source (municipal/groundwater/surface/third-party).  
**Waste:** period, amount, unit, stream (hazardous/non-hazardous), treatment (recycled/reused/incinerated/landfilled/composted).  
**Workforce KPIs:** headcount, turnover, training hours, TRIR, LTIFR, gender pay gap, diversity %, union coverage.  
**Governance:** board size, independence %, gender mix, ESG committee, anti-corruption training %, incidents, whistleblowing cases.  
**EU Taxonomy KPI line:** entity, period, activity code (NACE/ISIC), KPI type (revenue/CAPEX/OPEX), amount, currency, eligibility, alignment, DNSH result, minimum safeguards result, evidence references.  
**Materiality item:** topic, impact score (0–5), financial score (0–5), stakeholder weight(s), rationale, evidence references.

---

## Environmental Pillar

### 5.1 Climate (GHG Scopes 1, 2, 3)
**Definition.** Greenhouse gas emissions across direct operations, purchased energy, and the full value chain.  
**Key metrics.** Total emissions by scope; emissions intensity; progress vs targets; renewable electricity share; avoided emissions (where relevant).

**Formulas (plain language).**
- **General:** CO₂e = *Activity Quantity* × *Emission Factor* × *GWP adjustment*.  
- **Scope 2 – electricity:**  
  - *Location-based:* use grid factor of region/country.  
  - *Market-based:* use supplier-specific factor; where certificates are missing/expired, apply residual mix.  
- **Refrigerants:** CO₂e = *mass leaked (kg)* × *GWP100*.  
- **Logistics (S3.4):** tonne-kilometres × mode-specific factor.

**Evidence.** Meter readings, invoices, supplier attestations, emission factor library/version, GWP table version, certificate metadata for market claims.

---

### 5.2 Energy Management
**Definition.** Energy use and efficiency across fuels, electricity, steam, heating, and cooling.  
**Metrics.** Total energy use; renewable share; energy intensity; energy savings from projects; PPA coverage.  
**Evidence.** Utility bills, sub-metering logs, energy management system records.

---

### 5.3 Water Stewardship
**Definition.** Responsible withdrawal, consumption, discharge, and quality.  
**Metrics.** Withdrawal, discharge, consumption, water intensity, % sites in water-stressed areas, compliance incidents.  
**Consumption (when feasible).** *withdrawal − discharge*.  
**Evidence.** Flow meters, permits, site logs, watershed stress assessments.

---

### 5.4 Circularity & Waste
**Definition.** Resource efficiency, use of secondary materials, and waste management.  
**Metrics.** Hazardous/non-hazardous waste; recycling/recovery rates; circular material use; product take-back.  
**Evidence.** Manifests, contractor certificates, chain-of-custody documents.

---

### 5.5 Pollution (Air/Water/Soil)
**Definition.** Non-GHG pollutants (NOx, SOx, VOCs, particulates), effluents, and spills.  
**Metrics.** Pollutant mass per unit output; exceedance events; spill count/volume; remediation actions.  
**Evidence.** Permit conditions, monitoring logs, calibration records.

---

### 5.6 Biodiversity & Land Use
**Definition.** Impacts and dependencies on ecosystems and species.  
**Metrics.** Land disturbed/restored; proximity to protected areas; dependency on ecosystem services; offsets and restoration outcomes.  
**Evidence.** Screening against protected areas, mitigation hierarchy (avoid → minimize → restore → offset).

---

## Social Pillar

### 6.1 Workforce (Employment, Labor Practices)
**Metrics.** Headcount, voluntary turnover rate, training hours per employee, union coverage, engagement, fair remuneration indicators.  
**Evidence.** HRIS, payroll, learning systems, survey methodologies.

### 6.2 Health & Safety
**Metrics.**  
- **TRIR:** (Total Recordable Cases × 200,000) / Hours Worked.  
- **LTIFR:** (Lost Time Injuries × 1,000,000) / Hours Worked.  
- **Other:** fatalities, near-miss reporting, contractor safety performance.  
**Evidence.** Incident logs, investigation reports, hours worked, corrective action tracking.

### 6.3 Diversity, Equity & Inclusion
**Metrics.** Representation by level, pay equity gaps, hiring/promotion rates, inclusion index.  
**Evidence.** HR analytics; ensure privacy protections and lawful processing by jurisdiction.

### 6.4 Human Rights & Supply Chain Social Standards
**Metrics.** Supplier risk screening coverage, audits, non-conformities, corrective action closure rate, grievance cases and outcomes.  
**Evidence.** Procurement records, audit reports, CAP follow-up logs.

### 6.5 Customer & Product Responsibility
**Metrics.** Product safety incidents, data privacy incidents, customer satisfaction indices, responsible marketing compliance.  
**Evidence.** Incident registers, privacy logs, customer feedback systems.

### 6.6 Community & Social Investment
**Metrics.** Investment amounts, volunteer hours, outcome indicators aligned to material topics.  
**Evidence.** Project charters, outcome frameworks, third-party validations where applicable.

---

## Governance Pillar

### 7.1 Board Composition & Oversight
**Metrics.** Board size, independence %, gender mix, ESG competence, committee charters, oversight cadence.  
**Evidence.** Board profiles, charters, evaluation records.

### 7.2 Ethics, Anti-Corruption & Compliance
**Metrics.** Training coverage, incidents and sanctions, third-party due diligence coverage.  
**Evidence.** Policies, case records, due-diligence attestations.

### 7.3 Risk Management & Internal Control
**Metrics.** ESG risk register coverage, control testing results, scenario analyses, internal audit findings.  
**Evidence.** Risk registers, test plans, audit reports.

### 7.4 Data Governance, Privacy & Cybersecurity
**Metrics.** Privacy incidents, time to contain, certifications, coverage of critical systems.  
**Evidence.** Access reviews, encryption standards, backup/recovery test logs.

### 7.5 Remuneration & ESG Incentives
**Metrics.** Share of variable pay linked to ESG KPIs, clarity of KPI definitions and weights, outcome vs target.  
**Evidence.** Remuneration policies, KPI sheets, compensation committee minutes.

### 7.6 Tax Transparency & Responsible Lobbying
**Metrics.** Effective tax rate reconciliation, country-by-country reporting coverage, lobbying disclosures.  
**Evidence.** Tax disclosures, public policy positions, governance records.

---

## Materiality & Stakeholder Engagement
**Approach.** Combine impact and financial lenses; weight stakeholder views (investors, regulators, employees, customers, communities).  
**Output.** A ranked list of material topics with rationale and evidence references.  
**Quality gates.** Weights sum to 1; scores in [0–5]; stakeholder groups clearly defined; decisions justified.

---

## Targets, Pathways & Transition Planning
- **Absolute targets:** \(E_t = E_0 × (1 − r)^t\).  
- **Intensity targets:** Emissions per activity driver (e.g., tCO₂e/MWh or tCO₂e/unit).  
- **Pathways:** Pledged trajectory should be at least as ambitious as sector pathway at each milestone year.  
- **Transition plan:** List levers (abatement in tCO₂e, cost, NPV, timing, dependencies); identify no-regret levers and strategic levers; construct a marginal abatement cost curve (€/tCO₂e).

---

## Frameworks & Mappings
- **CSRD/ESRS:** Strategy & business model; governance; material impacts, risks and opportunities; metrics and targets. Environmental standards cover climate, pollution, water & marine, biodiversity, and resource use/circular economy. Social standards cover own workforce, value-chain workers, affected communities, and consumers.  
- **ISSB/TCFD:** Governance, Strategy & resilience, Risk management, Metrics & targets (climate-related).  
- **GRI & SASB:** Topic-specific indicators to improve comparability and sector relevance.  
- **SFDR (for financial products):** Principal Adverse Impacts (PAIs) and Taxonomy alignment of underlying investments.

---

## EU Taxonomy (Eligibility, Alignment, DNSH, Safeguards)
**Steps.**
1) Map economic activities to **technical screening criteria** (TSC).  
2) Determine **eligibility** (activity is covered by the Taxonomy).  
3) Determine **alignment** (meets TSC + DNSH + minimum safeguards).  
4) Compute **%Revenue, %CAPEX, %OPEX** that are eligible/aligned.  
5) Attach **evidence** for every aligned determination.  
6) Maintain a **change log** of delegated acts and criteria updates.

**Evidence.** Technical performance metrics (e.g., emissions intensity thresholds), permits, supplier certifications, policy documents (for minimum safeguards), DNSH rationale.  
**Common pitfalls.** Missing activity codes, double counting across entities, inconsistent boundaries, lack of evidence linkage, outdated criteria versions.

---

## Evidence, Assurance & Data Quality
**Dimensions.** Completeness, validity, accuracy, consistency, timeliness, security.  
**Acceptance rules (illustrative).**
- No nulls in key identifiers (entity, period, scope/category).  
- Units match the metric domain (e.g., electricity in kWh/MWh; water in m³).  
- Market-based Scope 2 requires certificate metadata; otherwise apply residual mix.  
- Ledger totals reconcile to financial statements when computing Taxonomy KPIs.  
- High-materiality lines sampled with a defined tolerance (e.g., ±2%).  

**Evidence minimum.** File hash, file name, source system, uploader, timestamp, linked records, approver, approval timestamp.  
**Audit trail.** Store inputs, method versions, parameters, and output hashes for every published number.

---

## Dashboards & Standard Reports
- **Executive scorecard:** top ESG KPIs vs targets; Taxonomy %; risk heatmaps.  
- **GHG inventory:** scope waterfall, trend lines, intensity metrics; breakdowns by entity and category.  
- **Water/Waste:** trends, intensities, site hotspots.  
- **Workforce:** safety trends, turnover, diversity, pay equity.  
- **Taxonomy KPI:** eligibility/alignment by entity/activity; evidence completeness.  
- **Regulatory calendar:** obligations, owners, due dates, status.  

**Export formats.** CSV/XLSX/JSON for data tables; PDF for narrative sections with references.

---

## Maturity Model & Roadmap
- **M1 (Ad-hoc):** spreadsheets, partial coverage.  
- **M2 (Defined):** canonical schemas, periodic reporting, initial controls.  
- **M3 (Integrated):** system connections, automated calculations, dashboards.  
- **M4 (Assured):** formal control testing, external assurance readiness.  
- **M5 (Optimized):** scenario planning, portfolio optimization, green finance integration.

**Suggested sequence.** Boundary & data gap assessment → schema adoption → emissions & resource accounting → taxonomy mapping → target setting & pathways → assurance preparation → continuous improvement.

---

## Sector Notes (Examples)
- **Manufacturing:** process emissions, fuel switching, energy efficiency, water reuse, waste minimization.  
- **Utilities:** grid mix, PPAs, network losses, SF₆ management.  
- **Real Estate:** energy intensity per floor area (kWh/m²), building certifications, embodied carbon in CAPEX.  
- **Logistics:** modal shift, load factor, route optimization, fleet electrification.  
- **Financials:** financed emissions methodologies, PAIs, use-of-proceeds and sustainability-linked financing frameworks.

---

## Common Pitfalls & Acceptance Criteria
**Pitfalls.**  
- Ambiguous or inconsistent boundaries.  
- Mixing market-based and location-based Scope 2 without reconciliation.  
- Using emission factors without version control or provenance.  
- Double counting in EU Taxonomy allocations.  
- Social metrics with unclear coverage (own workforce vs contractors).  
- Governance metrics without documented definitions (e.g., “independence”).  

**Acceptance criteria (summary).**  
- Boundaries, methods, and versions are explicit.  
- Units and denominators are consistent and valid.  
- Evidence is linked at the line level for assured metrics.  
- For Taxonomy KPIs, totals reconcile to financial statements; DNSH & safeguards decisions have documented rationale.  
- For safety metrics, rates computed with the correct hours-worked denominator.

---

## Glossary
**AR5/AR6:** IPCC GWP tables (100-year horizon).  
**DNSH:** Do No Significant Harm (environmental safeguards beyond technical criteria).  
**Minimum Safeguards:** Social/governance safeguards aligned to international principles.  
**Residual Mix:** Grid factor used when supplier certificates are missing or expired.  
**MACC:** Marginal Abatement Cost Curve—ranking levers by €/tCO₂e.  
**Double Materiality:** Combined impact and financial materiality lenses to prioritize topics.

---

## Versioning & Change Log Template
**Versioning rules.** Increment when methodologies, boundaries, factors, or criteria versions change. Maintain restatement notes and golden examples.

**Change log template.**
- Version: `X.Y.Z`  
- Date: `YYYY-MM-DD`  
- Sections changed:  
- Rationale:  
- Impacted metrics (and magnitude):  
- Restatement (if any):  
- Evidence references updated:  

---

## Appendix A: Example Tables

### A1. Materiality Matrix (excerpt)
| Topic | Impact (0–5) | Financial (0–5) | Stakeholder-Weighted (0–5) | Score | Rank | Rationale |
|---|---:|---:|---:|---:|---:|---|
| Climate | 5.0 | 4.5 | 4.6 | 4.7 | 1 | High emissions profile and investor focus |
| Water Stress | 3.5 | 2.5 | 3.0 | 3.0 | 2 | Sites in water-stressed basins |
| Safety | 3.0 | 3.5 | 3.2 | 3.2 | 3 | Incident history and regulatory scrutiny |

### A2. Scope 2 Disclosure (location vs market)
| Entity | Period | Electricity (MWh) | Location EF (tCO₂e/MWh) | Market EF | Location-based tCO₂e | Market-based tCO₂e | Certificates Metadata Present |
|---|---|---:|---:|---:|---:|---:|---|
| FR01 | 2024 | 3,500 | 0.20 | 0.18 | 700 | 630 | Yes (IDs, expiry) |

### A3. EU Taxonomy KPI (illustrative)
| Entity | Period | Activity Code | KPI Type | Amount (EUR) | Eligible | Aligned | DNSH | Safeguards | Evidence |
|---|---|---|---|---:|---|---|---|---|---|
| ES01 | 2024 | C27.2 | Revenue | 180,000,000 | Yes | Yes | Pass | Pass | Tech dossier #A12 |

### A4. Safety Rates
| Entity | Period | Hours Worked | Recordable Cases | TRIR | Lost Time Injuries | LTIFR |
|---|---|---:|---:|---:|---:|---:|
| DE01 | 2024 | 2,400,000 | 18 | 1.50 | 3 | 1.25 |

### A5. Governance Snapshot (excerpt)
| Entity | Period | Board Size | Independent % | Female % | ESG Committee | Anti-Corruption Training % |
|---|---|---:|---:|---:|---|---:|
| Group | 2024 | 10 | 70% | 40% | Yes | 96% |

---

**End of ESG_Master_Knowledge.md**
