# Actuarial Model Developer – Knowledge Base

## 1) Life & Non-Life Modeling Principles

### Life Insurance
- **Core risks**: mortality, longevity, lapse/surrender, morbidity, expenses.
- **Cashflows**: premiums, benefits (death, survival, maturity), surrenders, expenses.
- **Projection**: cohort or policy-level time steps with survival and lapse decrements.
- **Discounting**: market-consistent yield curve (risk-free + adjustments per framework).
- **Validation**: reconcile to experience studies; sensitivity to qx, lapses, discount rates.

### Non-Life (P&C)
- **Reserving**: use deterministic (Chain-Ladder, BF) and stochastic (bootstrap) methods.
- **Triangles**: incremental vs. cumulative, consistent basis (paid or reported).
- **Assumptions**: homogeneity, stable development; diagnose via link ratios, tail factors.
- **Validation**: back-testing, diagnostics (Mack variance if applicable).

## 2) Pensions & Retirement (Defined Benefit)
- **Obligation measures**: PBO/DBO (present value of accrued benefits), ABO.
- **Key drivers**: discount rate, salary growth, retirement age/mortality, indexing.
- **Funding ratio**: assets / PBO; track service cost and interest cost.
- **Sensitivity**: discount ±100 bps, longevity ±1 year life expectancy.

## 3) Capital & Solvency
- **Frameworks**: Solvency II, IFRS 17, economic capital.
- **Risk measure**: typically VaR at 99.5% (1-year); TVaR for tail.
- **Aggregation**: consider dependencies/correlations; be explicit on copulas or simplifications.
- **Stresses**: yield curve shifts, equity shocks, credit spreads, lapse/mortality stresses.

## 4) ALM Integration
- **Aim**: align asset cashflows/risks with liability profile.
- **Metrics**: duration/convexity matching, liquidity gap, interest-rate sensitivity (PV01).
- **Constraints**: regulatory (e.g., admissible assets), risk appetite, liquidity buffers.

## 5) Modeling Standards & Governance
- **Documentation**: objectives, data, methods, assumptions, limitations.
- **Controls**: versioning, peer review, validation against experience/benchmarks.
- **Data quality**: completeness, accuracy, consistency; clear transformations.
- **Transparency**: reproducible code, clear parameter sources, audit trail.

## 6) Reporting – Minimums
- Define inputs/assumptions (tables, curves).
- Show key outputs (PV, reserves, SCR proxies, funding ratio).
- Include sensitivities and scenario results.
- Explain changes vs. prior period (method/assumption/data).
