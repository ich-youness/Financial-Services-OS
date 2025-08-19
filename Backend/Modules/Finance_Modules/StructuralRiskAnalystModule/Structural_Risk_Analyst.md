# 🏦 Structural Risk Analyst Module

## Overview
The Structural Risk Analyst Module is a comprehensive AI-powered module designed for financial and regulatory reporting, focusing on structural risk analysis across multiple regulatory frameworks. This module ensures compliance with international banking standards while providing deep insights into structural risks.

## 🎯 Module Purpose
This module addresses the critical need for accurate, timely, and compliant regulatory reporting in financial institutions, covering:
- **Solvency and Capital Adequacy** (Basel III/CRR3)
- **Liquidity Risk Management** (LCR/NSFR)
- **Interest Rate Risk** (IRRBB/CSRBB)
- **Foreign Exchange Risk** (FX exposure monitoring)
- **Multi-Regulatory Compliance** (MiFID II, EMIR, Dodd-Frank, IFRS, Basel)

## 🤖 AI Agents

### 1. SolvencyReportingAgent
**Purpose**: Produces and ensures accuracy of solvency metrics required by banking and insurance regulators.

**Key Responsibilities**:
- **Solvency Indicator Calculation**
  - Compute Risk-Weighted Assets (RWA) by asset class, counterparty, and exposure type
  - Determine Risk Weights (RW) according to Basel standards and local regulation
  - Apply standardized or internal ratings-based (IRB) approaches

- **Capital Adequacy Ratios**
  - Calculate CET1, Tier 1, and Total Capital Ratios
  - Compare against minimum regulatory requirements and internal targets

- **Data Quality Controls**
  - Reconcile source data with accounting and risk systems
  - Identify anomalies before regulatory submission

**Tools Used**: ExaTools, CalculatorTools

### 2. LiquidityRiskAgent
**Purpose**: Measures liquidity resilience under Basel III and other regulatory frameworks.

**Key Responsibilities**:
- **Liquidity Coverage Ratio (LCR)**
  - Calculate HQLA to net cash outflows over 30-day stress period
  - Apply regulatory haircuts and outflow assumptions

- **Net Stable Funding Ratio (NSFR)**
  - Calculate available vs. required stable funding over 1-year horizon
  - Assess long-term liquidity profile

- **Stress Testing**
  - Simulate liquidity shocks and assess ratio impacts
  - Model deposit runs and wholesale funding withdrawal scenarios

**Tools Used**: ExaTools, CalculatorTools

### 3. InterestRateRiskAgent
**Purpose**: Produces risk measures for interest rate and spread movements over different time horizons.

**Key Responsibilities**:
- **Net Present Value (NPV) Sensitivity**
  - Measure EVE changes from parallel and non-parallel rate shifts
  - Calculate duration and convexity measures

- **Earnings at Risk / Margin at Risk**
  - Forecast NII impact from rate changes over 12-month and multi-year horizons
  - Model earnings volatility under various scenarios

- **IRRBB & CSRBB**
  - Compute standardized approach and internal model metrics
  - Assess compliance with BCBS 368 and EBA guidelines

- **ITS IRRBB**
  - Prepare and submit mandatory EBA templates

**Tools Used**: ExaTools, CalculatorTools

### 4. FXRiskAgent
**Purpose**: Monitors and reports currency-related exposures across trading and banking books.

**Key Responsibilities**:
- **Net Open Position (NOP)**
  - Calculate FX positions across all books
  - Include spot, forward, options, and structural positions

- **Sensitivity & Stress Testing**
  - Model currency shock impacts on capital and liquidity ratios
  - Calculate FX sensitivity measures (delta, gamma, vega)

- **Hedging Effectiveness**
  - Monitor FX hedging strategy performance
  - Assess hedge effectiveness ratios

**Tools Used**: ExaTools, CalculatorTools

### 5. RegulatoryCorrectionAgent
**Purpose**: Ensures accurate compliance with multiple regulatory regimes through error correction and re-submission.

**Key Responsibilities**:
- **Error Identification**
  - Detect inaccuracies through regulator feedback or internal audits
  - Analyze error patterns and root causes

- **Correction Process**
  - Amend calculations and regenerate impacted reports
  - Maintain full audit trail of corrections

- **Multi-Regulatory Compliance**
  - Handle corrections across MiFID II, EMIR, Dodd-Frank, IFRS, and Basel regimes
  - Ensure coordinated compliance updates

**Tools Used**: ExaTools, CalculatorTools

## 🏗️ Team Structure

### StructuralRiskAnalystTeam
A coordinated team that integrates all five specialized agents to provide comprehensive risk analysis and regulatory compliance.

**Team Coordination**:
- Agents work collaboratively to ensure data consistency
- Regulatory reporting follows unified approach with shared validation
- Stress testing scenarios coordinated across all risk types
- Compliance monitoring integrated across all regulatory requirements

## 🧠 Knowledge Base

### Structural_Risk_Analyst_Knowledge.md
Comprehensive knowledge base covering:
- **Regulatory Frameworks**: Basel III, Solvency II, IFRS, US regulations
- **Calculation Methodologies**: RWA, capital ratios, liquidity metrics
- **Risk Management**: IRRBB, CSRBB, FX risk, stress testing
- **Compliance Requirements**: Multi-regulatory reporting standards
- **Best Practices**: Industry standards and implementation guidance

## 🚀 Usage Examples

### Basic Agent Usage
```python
# Test solvency calculations
result = SolvencyReportingAgent.run(
    "Calculate CET1, Tier 1, and Total Capital Ratios for a bank with: "
    "Common Equity Tier 1: $50M, Additional Tier 1: $10M, Tier 2: $15M, "
    "Risk-Weighted Assets: $400M. Also calculate the minimum regulatory requirements."
)

# Test liquidity analysis
result = LiquidityRiskAgent.run(
    "Calculate the Liquidity Coverage Ratio (LCR) for a bank with: "
    "High-Quality Liquid Assets: $200M, Net Cash Outflows: $150M. "
    "Apply regulatory haircuts and assess compliance with Basel III requirements."
)
```

### Team Coordination
```python
# Use the coordinated team for comprehensive analysis
team_result = StructuralRiskAnalystTeam.run(
    "Provide a comprehensive structural risk analysis for BANK_001, "
    "including solvency, liquidity, interest rate risk, and FX risk metrics. "
    "Identify any compliance issues and provide recommendations."
)
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Required packages: agno, mistralai, openai, pgvector
- Environment variables for API keys (Mistral, OpenAI, EXA)

### Environment Variables
```bash
export MISTRAL_API_KEY="your_mistral_api_key"
export OPENAI_API_KEY="your_mistral_api_key"
export EXA_API_KEY="your_exa_api_key"
```

## 📋 Regulatory Compliance

### Supported Frameworks
- **Basel III/CRR3**: Capital adequacy, liquidity, leverage
- **Solvency II**: Insurance supervision requirements
- **MiFID II**: Markets in financial instruments
- **EMIR**: European market infrastructure regulation
- **Dodd-Frank Act**: US financial reform
- **IFRS**: International financial reporting standards

### Compliance Features
- Automated regulatory calculation engines
- Real-time compliance monitoring
- Multi-regulatory report generation
- Audit trail maintenance
- Error detection and correction workflows

## 🔍 Testing & Validation

### Test Functions
The module includes built-in test functions:
- `test_solvency_calculations()`
- `test_liquidity_analysis()`
- `test_interest_rate_risk()`
- `test_fx_risk()`
- `test_regulatory_compliance()`


## 🏆 Benefits

### For Financial Institutions
- **Regulatory Compliance**: Automated compliance with multiple regimes
- **Risk Management**: Comprehensive structural risk analysis
- **Operational Efficiency**: Streamlined reporting processes
- **Data Quality**: Enhanced data validation and reconciliation

### For Regulators
- **Standardization**: Consistent reporting across institutions
- **Transparency**: Clear audit trails and calculation methodologies
- **Efficiency**: Automated compliance monitoring
- **Risk Assessment**: Comprehensive risk metrics for supervision

### For Stakeholders
- **Confidence**: Reliable risk metrics and compliance status
- **Transparency**: Clear understanding of risk positions
- **Decision Support**: Actionable insights for risk management
- **Compliance Assurance**: Verified regulatory compliance