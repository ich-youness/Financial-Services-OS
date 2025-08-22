# 🌱 ISR Consultant Module

## Overview
The ISR Consultant Module is a comprehensive AI-powered module designed for ethical and sustainable investment strategies. This module provides end-to-end ISR consulting services, from policy development to portfolio optimization and stakeholder engagement, ensuring alignment with international sustainability principles and regulatory requirements.

## 🎯 Module Purpose
This module addresses the critical need for sustainable investment solutions that align financial objectives with environmental, social, and governance (ESG) values, covering:
- **Ethical Investment Strategy Development** (SRI policies and values alignment)
- **ESG Integration** (Screening, impact measurement, and risk management)
- **Portfolio Construction & Optimization** (Sustainable asset allocation and performance)
- **Regulatory Compliance** (SFDR, EU Taxonomy, CSRD, and international standards)
- **Stakeholder Engagement** (Active ownership, proxy voting, and collaboration networks)

## 🤖 AI Agents

### 1. EthicalInvestmentAgent
**Purpose**: Advises on ethical and sustainable investment strategies, developing SRI policies and ensuring values alignment.

**Key Responsibilities**:
- **SRI Policy Development**
  - Define client's responsible investment philosophy and ethical boundaries
  - Establish ESG exclusion lists (tobacco, weapons, coal) and inclusion criteria
  - Integrate sustainability objectives with traditional investment strategies

- **Values Alignment**
  - Match investment opportunities with client's moral, environmental, and social priorities
  - Ensure consistency with international principles (UN PRI, OECD Guidelines, UN Global Compact)
  - Develop customized ESG frameworks for different client profiles

**Tools Used**: ExaTools, YFinanceTools

### 2. ESGIntegrationAgent
**Purpose**: Embeds environmental, social, and governance factors into investment decision-making processes.

**Key Responsibilities**:
- **ESG Screening**
  - Apply negative screening (exclusion), positive screening (best-in-class), and thematic investing
  - Use ESG ratings from specialized agencies (MSCI, Sustainalytics, Vigeo Eiris)
  - Develop multi-dimensional ESG scoring methodologies

- **Impact Measurement**
  - Quantify positive environmental and social contributions
  - Integrate KPIs into ongoing portfolio reporting
  - Develop impact measurement frameworks and metrics

- **Risk Management**
  - Identify ESG-related risks (climate, social, governance, reputational)
  - Incorporate these risks into portfolio construction and monitoring
  - Develop ESG risk assessment methodologies

**Tools Used**: ExaTools, CalculatorTools, YFinanceTools

### 3. PortfolioOptimizationAgent
**Purpose**: Creates and manages investment portfolios that meet both financial and sustainability objectives.

**Key Responsibilities**:
- **Asset Selection**
  - Choose equities, bonds, and alternative assets that meet SRI criteria
  - Use green bonds, social bonds, and sustainability-linked instruments
  - Develop ESG-aware asset selection frameworks

- **Strategic Asset Allocation**
  - Balance risk, return, and sustainability exposure
  - Maintain diversification while meeting ESG thresholds
  - Optimize portfolios for both financial and sustainability objectives

- **Performance Attribution**
  - Evaluate returns relative to sustainability benchmarks
  - Assess contribution of ESG factors to risk-adjusted returns
  - Develop ESG performance measurement frameworks

**Tools Used**: ExaTools, CalculatorTools, YFinanceTools

### 4. RegulatoryComplianceAgent
**Purpose**: Ensures investments meet evolving ESG-related financial regulations and disclosure standards.

**Key Responsibilities**:
- **Regulatory Alignment**
  - Comply with SFDR, EU Taxonomy, CSRD, and international standards
  - Align investment products with Article 8 and 9 requirements under SFDR
  - Monitor evolving ESG regulations and compliance requirements

- **Client Reporting**
  - Provide transparent, periodic reports detailing portfolio sustainability characteristics
  - Demonstrate compliance with regulatory and client-specific sustainability mandates
  - Develop comprehensive ESG reporting frameworks

**Tools Used**: ExaTools, CalculatorTools

### 5. StakeholderEngagementAgent
**Purpose**: Uses investor influence to promote sustainable corporate practices through active ownership and engagement.

**Key Responsibilities**:
- **Active Ownership**
  - Engage with portfolio companies to improve ESG performance
  - File or support shareholder resolutions on sustainability issues
  - Develop engagement strategies and communication frameworks

- **Proxy Voting**
  - Vote in line with SRI policy to support environmental and social initiatives
  - Develop proxy voting guidelines and decision frameworks
  - Monitor and report on proxy voting activities

- **Collaboration Networks**
  - Participate in investor coalitions (Climate Action 100+, Net Zero Asset Owner Alliance)
  - Develop collaborative engagement strategies
  - Monitor industry initiatives and best practices

**Tools Used**: ExaTools, YFinanceTools

## 🏗️ Team Structure

### ISRConsultantTeam
A coordinated team that integrates all five specialized agents to provide comprehensive sustainable investment services.

**Team Coordination**:
- Agents work collaboratively to ensure consistency across all ISR activities
- ESG criteria are consistently applied from policy development to portfolio construction
- Regulatory compliance is integrated throughout all investment processes
- Stakeholder engagement activities align with portfolio holdings and SRI policies

## 📊 Data Files

### Prototype Data
The module includes comprehensive prototype data for testing and development:

1. **`sri_policy_CLIENT_001.json`** - SRI policy development and values alignment
2. **`esg_integration_PORTFOLIO_001.json`** - ESG screening, impact measurement, and risk management
3. **`portfolio_optimization_PORTFOLIO_001.json`** - Sustainable portfolio construction and optimization
4. **`regulatory_compliance_ISR_001.json`** - ESG regulatory compliance and reporting
5. **`stakeholder_engagement_ISR_001.json`** - Active ownership and stakeholder engagement
6. **`isr_consultant_data.csv`** - Comprehensive ISR consulting dataset

### Data Structure
All data files follow consistent JSON/CSV formats with:
- Client and portfolio identification
- ESG metrics and sustainability characteristics
- Regulatory compliance status
- Engagement activities and outcomes
- Performance metrics and impact measurement

## 🧠 Knowledge Base

### ISR_Consultant_Knowledge.md
Comprehensive knowledge base covering:
- **Sustainable Investment Principles**: UN PRI, OECD Guidelines, UN Global Compact, SDGs
- **ESG Frameworks & Standards**: Environmental, social, and governance factors
- **SRI Policy Development**: Investment philosophy, exclusion/inclusion criteria, integration strategies
- **ESG Integration Methodologies**: Screening approaches, scoring methodologies, materiality assessment
- **Portfolio Construction & Optimization**: Asset selection, strategic allocation, performance measurement
- **Regulatory Compliance**: SFDR, EU Taxonomy, CSRD, US regulations
- **Stakeholder Engagement**: Active ownership, proxy voting, collaboration networks
- **Impact Measurement**: Environmental, social, and economic impact metrics

## 🚀 Usage Examples

### Basic Agent Usage
```python
# Test ethical investment strategy development
result = EthicalInvestmentAgent.run(
    "Develop an SRI policy for a client who wants to avoid tobacco, weapons, and fossil fuels, "
    "while supporting renewable energy and social housing. Include exclusion criteria, "
    "inclusion criteria, and alignment with UN PRI principles."
)

# Test ESG integration
result = ESGIntegrationAgent.run(
    "Analyze the ESG characteristics of a technology company portfolio, "
    "apply negative screening for human rights violations, positive screening for best-in-class ESG performers, "
    "and identify climate transition risks."
)

# Test sustainable portfolio construction
result = PortfolioOptimizationAgent.run(
    "Construct a sustainable portfolio with 60% equities, 30% bonds, and 10% alternatives "
    "that meets ESG criteria while maintaining diversification. Include green bonds and social impact investments."
)
```

### Team Coordination
```python
# Use the coordinated team for comprehensive ISR consulting
team_result = ISRConsultantTeam.run(
    "Provide comprehensive ISR consulting for a new client: "
    "1. Develop SRI policy aligned with UN PRI principles "
    "2. Integrate ESG criteria into investment decision-making "
    "3. Construct optimized sustainable portfolio "
    "4. Ensure regulatory compliance "
    "5. Develop stakeholder engagement strategy"
)
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Required packages: agno, numpy, pandas
- Environment variables for API keys (Mistral, OpenAI, Gemini)

### Environment Variables
```bash
export MISTRAL_API_KEY="your_mistral_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export EXA_API_KEY="your_gemini_api_key"
```

## 📋 Regulatory Compliance

### Supported Frameworks
- **SFDR**: Sustainable Finance Disclosure Regulation (Articles 8 & 9)
- **EU Taxonomy**: Climate and environmental objectives
- **CSRD**: Corporate Sustainability Reporting Directive
- **UN PRI**: Principles for Responsible Investment
- **OECD Guidelines**: Multinational enterprise standards
- **US Regulations**: SEC climate disclosure, DOL ESG rules

### Compliance Features
- Automated regulatory compliance monitoring
- SFDR Article 8/9 classification and reporting
- EU Taxonomy alignment assessment
- Principal adverse impact disclosure
- Sustainability indicators and metrics

## 🔍 Testing & Validation

### Test Functions
The module includes built-in test functions:
- `test_ethical_investment_strategy()`
- `test_esg_integration()`
- `test_portfolio_optimization()`
- `test_regulatory_compliance()`
- `test_stakeholder_engagement()`
- `test_comprehensive_isr_consulting()`

### Data Validation
- ESG criteria validation and verification
- Regulatory compliance checking
- Impact measurement accuracy
- Performance attribution analysis

### Quality Standards
- All recommendations must align with established SRI policies
- ESG criteria must be consistently applied across all investment decisions
- Regulatory compliance must be verified for all recommendations
- Stakeholder engagement must support portfolio sustainability objectives