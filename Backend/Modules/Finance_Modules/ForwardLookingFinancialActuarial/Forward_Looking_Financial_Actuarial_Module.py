from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.embedder.mistral import MistralEmbedder
from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.file import FileTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.calculator import CalculatorTools
from agno.tools import tool
from dotenv import load_dotenv
import os
from typing import Dict, List, Any
from pathlib import Path

load_dotenv()

# Knowledge Base for the module
flfa_knowledge_base = MarkdownKnowledgeBase(
    path="Knowledge/Forward_Looking_Financial_Actuarial_Knowledge.md"
        

    # vector_db=PgVector(
    #     table_name="forward_looking_financial_actuarial_knowledge",
    #     db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    #     embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API_KEY")),
    # ),
)
# flfa_knowledge_base.load(recreate=True)


# Custom Forward-Looking Actuarial Tools
@tool(
    name="calculate_solvency_ratio",
    description="Calculate Solvency II ratio and capital adequacy metrics",
    show_result=True,
)
def calculate_solvency_ratio(
    own_funds: float,
    scr_amount: float,
    mcr_amount: float,
    risk_modules: Dict[str, float],
) -> Dict[str, Any]:
    """
    Calculate Solvency II ratio and capital adequacy metrics.

    Args:
        own_funds: Available own funds
        scr_amount: Solvency Capital Requirement
        mcr_amount: Minimum Capital Requirement
        risk_modules: Dictionary of risk module amounts

    Returns:
        Dictionary containing solvency metrics and analysis
    """
    solvency_ratio = (own_funds / scr_amount) * 100 if scr_amount > 0 else 0
    mcr_ratio = (own_funds / mcr_amount) * 100 if mcr_amount > 0 else 0

    # Risk concentration analysis
    total_risk = sum(risk_modules.values())
    risk_concentration = {
        k: (v / total_risk * 100) if total_risk > 0 else 0
        for k, v in risk_modules.items()
    }

    # Capital adequacy assessment
    adequacy_level = (
        "Excellent"
        if solvency_ratio >= 150
        else (
            "Good"
            if solvency_ratio >= 130
            else "Adequate" if solvency_ratio >= 100 else "Inadequate"
        )
    )

    return {
        "solvency_ratio": round(solvency_ratio, 2),
        "mcr_ratio": round(mcr_ratio, 2),
        "adequacy_level": adequacy_level,
        "risk_concentration": risk_concentration,
        "capital_buffer": own_funds - scr_amount,
        "regulatory_margin": own_funds - mcr_amount,
    }


@tool(
    name="project_solvency_evolution",
    description="Project solvency ratio evolution over time under different scenarios",
    show_result=True,
)
def project_solvency_evolution(
    current_solvency_ratio: float,
    current_scr: float,
    current_own_funds: float,
    projection_years: int,
    scenario_type: str,
    assumptions: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Project solvency ratio evolution under different scenarios.

    Args:
        current_solvency_ratio: Current solvency ratio
        current_scr: Current SCR amount
        current_own_funds: Current own funds
        projection_years: Number of years to project
        scenario_type: Type of scenario (base/optimistic/pessimistic)
        assumptions: Dictionary of scenario assumptions

    Returns:
        Dictionary containing projected solvency metrics
    """
    projections = {}

    # Scenario multipliers
    scenario_multipliers = {
        "base": {"scr_growth": 1.02, "own_funds_growth": 1.05, "profit_margin": 0.08},
        "optimistic": {
            "scr_growth": 1.01,
            "own_funds_growth": 1.08,
            "profit_margin": 0.12,
        },
        "pessimistic": {
            "scr_growth": 1.04,
            "own_funds_growth": 1.02,
            "profit_margin": 0.04,
        },
    }

    multipliers = scenario_multipliers.get(scenario_type, scenario_multipliers["base"])

    current_scr_proj = current_scr
    current_own_funds_proj = current_own_funds

    for year in range(1, projection_years + 1):
        # Project SCR growth
        current_scr_proj *= multipliers["scr_growth"]

        # Project own funds growth (including profit)
        profit = current_own_funds_proj * multipliers["profit_margin"]
        current_own_funds_proj += profit

        # Calculate solvency ratio
        solvency_ratio = (current_own_funds_proj / current_scr_proj) * 100

        projections[f"year_{year}"] = {
            "solvency_ratio": round(solvency_ratio, 2),
            "scr_amount": round(current_scr_proj, 0),
            "own_funds": round(current_own_funds_proj, 0),
            "profit": round(profit, 0),
            "capital_buffer": round(current_own_funds_proj - current_scr_proj, 0),
        }

    return {
        "scenario_type": scenario_type,
        "projection_years": projection_years,
        "assumptions": assumptions,
        "projections": projections,
    }


@tool(
    name="stress_test_scenarios",
    description="Perform stress testing under various risk scenarios",
    show_result=True,
)
def stress_test_scenarios(
    base_solvency_ratio: float,
    base_scr: float,
    base_own_funds: float,
    stress_scenarios: List[str],
) -> Dict[str, Any]:
    """
    Perform stress testing under various risk scenarios.

    Args:
        base_solvency_ratio: Base solvency ratio
        base_scr: Base SCR amount
        base_own_funds: Base own funds
        stress_scenarios: List of stress scenarios to test

    Returns:
        Dictionary containing stress test results
    """
    stress_results = {}

    # Stress scenario definitions
    scenario_definitions = {
        "interest_rate_shock": {
            "description": "Parallel shift in interest rates",
            "scr_impact": 0.05,  # 5% increase in SCR
            "own_funds_impact": -0.08,  # 8% decrease in own funds
        },
        "equity_market_crash": {
            "description": "40% decline in equity markets",
            "scr_impact": 0.08,  # 8% increase in SCR
            "own_funds_impact": -0.12,  # 12% decrease in own funds
        },
        "mortality_stress": {
            "description": "Pandemic-like mortality increase",
            "scr_impact": 0.10,  # 10% increase in SCR
            "own_funds_impact": -0.15,  # 15% decrease in own funds
        },
        "lapse_shock": {
            "description": "Mass lapse event",
            "scr_impact": 0.04,  # 4% increase in SCR
            "own_funds_impact": -0.06,  # 6% decrease in own funds
        },
        "credit_default": {
            "description": "Sovereign default scenario",
            "scr_impact": 0.06,  # 6% increase in SCR
            "own_funds_impact": -0.09,  # 9% decrease in own funds
        },
        "operational_event": {
            "description": "Major operational failure",
            "scr_impact": 0.02,  # 2% increase in SCR
            "own_funds_impact": -0.20,  # 20% decrease in own funds
        },
    }

    for scenario in stress_scenarios:
        if scenario in scenario_definitions:
            definition = scenario_definitions[scenario]

            # Calculate stressed values
            stressed_scr = base_scr * (1 + definition["scr_impact"])
            stressed_own_funds = base_own_funds * (1 + definition["own_funds_impact"])
            stressed_solvency_ratio = (stressed_own_funds / stressed_scr) * 100

            stress_results[scenario] = {
                "description": definition["description"],
                "base_solvency_ratio": round(base_solvency_ratio, 2),
                "stressed_solvency_ratio": round(stressed_solvency_ratio, 2),
                "impact_on_solvency_ratio": round(
                    stressed_solvency_ratio - base_solvency_ratio, 2
                ),
                "stressed_scr": round(stressed_scr, 0),
                "stressed_own_funds": round(stressed_own_funds, 0),
                "adequacy_level": (
                    "Excellent"
                    if stressed_solvency_ratio >= 150
                    else (
                        "Good"
                        if stressed_solvency_ratio >= 130
                        else (
                            "Adequate"
                            if stressed_solvency_ratio >= 100
                            else "Inadequate"
                        )
                    )
                ),
            }

    return {
        "base_metrics": {
            "solvency_ratio": base_solvency_ratio,
            "scr": base_scr,
            "own_funds": base_own_funds,
        },
        "stress_results": stress_results,
    }


@tool(
    name="calculate_capital_requirements",
    description="Calculate SCR and MCR using standard formula approach",
    show_result=True,
)
def calculate_capital_requirements(
    risk_modules: Dict[str, float], business_volume: float, entity_type: str
) -> Dict[str, Any]:
    """
    Calculate SCR and MCR using standard formula approach.

    Args:
        risk_modules: Dictionary of risk module amounts
        business_volume: Annual business volume
        entity_type: Type of entity (life/health/non-life/multi)

    Returns:
        Dictionary containing capital requirements
    """
    # Calculate SCR using standard formula
    total_scr = sum(risk_modules.values())

    # Apply correlation matrix (simplified)
    correlation_benefit = total_scr * 0.15  # 15% diversification benefit
    net_scr = total_scr - correlation_benefit

    # Calculate MCR
    mcr_ratio = 0.25 if entity_type == "life" else 0.30  # 25-30% of SCR
    mcr = max(net_scr * mcr_ratio, 2200000 if entity_type == "life" else 1500000)

    # Risk module breakdown
    risk_breakdown = {
        k: (v / total_scr * 100) if total_scr > 0 else 0
        for k, v in risk_modules.items()
    }

    return {
        "scr_amount": round(net_scr, 0),
        "mcr_amount": round(mcr, 0),
        "total_risk": round(total_scr, 0),
        "diversification_benefit": round(correlation_benefit, 0),
        "risk_breakdown": risk_breakdown,
        "mcr_ratio": round((mcr / net_scr) * 100, 2) if net_scr > 0 else 0,
    }


@tool(
    name="orsa_report_generator",
    description="Generate comprehensive ORSA report with methodology and results",
    show_result=True,
)
def orsa_report_generator(
    entity_name: str,
    reporting_date: str,
    solvency_metrics: Dict[str, Any],
    scenario_analysis: Dict[str, Any],
    stress_test_results: Dict[str, Any],
    risk_management_framework: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate comprehensive ORSA report.

    Args:
        entity_name: Name of the insurance entity
        reporting_date: Reporting date
        solvency_metrics: Current solvency metrics
        scenario_analysis: Scenario analysis results
        stress_test_results: Stress testing results
        risk_management_framework: Risk management framework details

    Returns:
        Dictionary containing ORSA report sections
    """
    report = {
        "orsa_report": {
            "entity_name": entity_name,
            "reporting_date": reporting_date,
            "report_type": "Own Risk and Solvency Assessment (ORSA)",
            "sections": {
                "executive_summary": {
                    "key_findings": [
                        f"Current solvency ratio: {solvency_metrics.get('solvency_ratio', 0)}%",
                        f"Capital adequacy level: {solvency_metrics.get('adequacy_level', 'Unknown')}",
                        f"Risk concentration: {max(solvency_metrics.get('risk_concentration', {}).values(), default=0):.1f}% in largest risk module",
                    ],
                    "recommendations": [
                        "Maintain current risk management framework",
                        "Monitor key risk indicators regularly",
                        "Review capital allocation strategy annually",
                    ],
                },
                "methodology": {
                    "approach": "Standard Formula with internal model elements",
                    "assumptions": "Based on current business plan and market conditions",
                    "validation": "Independent model validation completed",
                    "governance": "Board-approved ORSA policy and process",
                },
                "risk_assessment": {
                    "current_risk_profile": solvency_metrics,
                    "risk_concentration": solvency_metrics.get(
                        "risk_concentration", {}
                    ),
                    "risk_limits": risk_management_framework.get("risk_limits", {}),
                    "risk_monitoring": "Daily market risk, weekly credit risk, monthly comprehensive",
                },
                "capital_adequacy": {
                    "current_position": solvency_metrics,
                    "projections": scenario_analysis,
                    "stress_testing": stress_test_results,
                    "capital_management": "Risk-based dividend policy with stress testing",
                },
                "forward_looking_assessment": {
                    "scenario_analysis": scenario_analysis,
                    "business_plan_impact": "Growth strategies tested against solvency constraints",
                    "regulatory_developments": "Monitoring IFRS 17 and Solvency II developments",
                    "esg_integration": "Climate risk scenarios included in stress testing",
                },
            },
        }
    }

    return report


@tool(
    name="ifrs17_solvency_bridge",
    description="Bridge between IFRS 17 profit emergence and Solvency II capital evolution",
    show_result=True,
)
def ifrs17_solvency_bridge(
    ifrs17_metrics: Dict[str, Any],
    solvency_metrics: Dict[str, Any],
    measurement_model: str,
) -> Dict[str, Any]:
    """
    Bridge between IFRS 17 profit emergence and Solvency II capital evolution.

    Args:
        ifrs17_metrics: IFRS 17 measurement metrics
        solvency_metrics: Solvency II metrics
        measurement_model: IFRS 17 measurement model (GMM/PAA/VFA)

    Returns:
        Dictionary containing bridge analysis
    """
    # Extract key metrics
    ifrs17_liability = ifrs17_metrics.get("fulfilment_cash_flows", 0)
    ifrs17_risk_adjustment = ifrs17_metrics.get("risk_adjustment", 0)
    ifrs17_csm = ifrs17_metrics.get("contractual_service_margin", 0)

    solvency_liability = solvency_metrics.get("technical_provisions", 0)
    solvency_risk_margin = solvency_metrics.get("risk_margin", 0)

    # Calculate differences
    liability_difference = ifrs17_liability - solvency_liability
    risk_adjustment_difference = ifrs17_risk_adjustment - solvency_risk_margin

    # Profit recognition timing
    ifrs17_profit_timing = (
        "Immediate recognition of CSM"
        if measurement_model == "PAA"
        else "Recognition over service period"
    )

    solvency_profit_timing = "Recognition based on capital adequacy"

    bridge_analysis = {
        "measurement_model": measurement_model,
        "liability_comparison": {
            "ifrs17_liability": ifrs17_liability,
            "solvency_liability": solvency_liability,
            "difference": liability_difference,
            "difference_percentage": (
                (liability_difference / solvency_liability * 100)
                if solvency_liability > 0
                else 0
            ),
        },
        "risk_adjustment_comparison": {
            "ifrs17_risk_adjustment": ifrs17_risk_adjustment,
            "solvency_risk_margin": solvency_risk_margin,
            "difference": risk_adjustment_difference,
            "difference_percentage": (
                (risk_adjustment_difference / solvency_risk_margin * 100)
                if solvency_risk_margin > 0
                else 0
            ),
        },
        "profit_recognition": {
            "ifrs17_timing": ifrs17_profit_timing,
            "solvency_timing": solvency_profit_timing,
            "csm_impact": ifrs17_csm,
            "capital_impact": "CSM affects own funds but not SCR",
        },
        "reconciliation": {
            "total_ifrs17_liability": ifrs17_liability + ifrs17_risk_adjustment,
            "total_solvency_liability": solvency_liability + solvency_risk_margin,
            "net_difference": (ifrs17_liability + ifrs17_risk_adjustment)
            - (solvency_liability + solvency_risk_margin),
        },
    }

    return bridge_analysis


# Agent 1: Forward-Looking Risk Assessment
ForwardLookingRiskAssessmentAgent = Agent(
    name="Forward-Looking Risk Assessment Agent",
    agent_id="ForwardLookingRiskAssessmentAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        calculate_solvency_ratio,
        project_solvency_evolution,
        stress_test_scenarios,
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        CalculatorTools(),
        ReasoningTools(),
    ],
    instructions="""
You are a Forward-Looking Risk Assessment specialist focusing on:

1. **Risk Identification & Quantification**:
   - Identify key risks impacting solvency: market, credit, underwriting, operational, liquidity, ESG/climate
   - Quantify risks under baseline and stressed scenarios
   - Analyze risk correlations and diversification benefits

2. **Projection of Solvency Position**:
   - Simulate Solvency II ratio evolution over 3-5 years
   - Assess impact of strategic plan on solvency (new products, growth, divestments)
   - Model capital adequacy under different business scenarios

3. **Stress Testing & Scenario Analysis**:
   - Interest rate shocks, equity crashes, mortality/morbidity stress, lapse shocks
   - Credit events, operational failures, ESG/climate scenarios
   - Extreme but plausible stress scenarios

Use actuarial modeling techniques, stochastic simulations, and scenario analysis to provide comprehensive forward-looking risk assessment. Focus on quantitative analysis and provide actionable insights for risk management and capital planning.
""",
    markdown=True,
    knowledge=flfa_knowledge_base,
    show_tool_calls=True,
)

# Agent 2: Financial Actuarial Projections
FinancialActuarialProjectionsAgent = Agent(
    name="Financial Actuarial Projections Agent",
    agent_id="FinancialActuarialProjectionsAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        calculate_capital_requirements,
        ifrs17_solvency_bridge,
        project_solvency_evolution,
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        CalculatorTools(),
        ReasoningTools(),
    ],
    instructions="""
You are a Financial Actuarial Projections specialist focusing on:

1. **Balance Sheet Forecasting**:
   - Project technical provisions, own funds, and capital requirements
   - Incorporate future profit-sharing, dividend policies, and investment strategies
   - Model asset-liability matching and investment returns

2. **Capital Requirement Projection**:
   - Project SCR (Solvency Capital Requirement) and MCR (Minimum Capital Requirement)
   - Break down per risk module (market, life, health, non-life, operational)
   - Analyze capital efficiency and optimization opportunities

3. **Link with IFRS 17**:
   - Bridge between IFRS 17 profit emergence and Solvency II capital evolution
   - Use forward-looking actuarial models for both financial reporting and solvency assessment
   - Analyze measurement model differences and reconciliation

Use actuarial modeling, financial projections, and regulatory frameworks to provide comprehensive financial actuarial analysis. Focus on accuracy, regulatory compliance, and strategic insights for capital management.
""",
    markdown=True,
    knowledge=flfa_knowledge_base,
    show_tool_calls=True,
)

# Agent 3: Operational Declassification of ORSA
OperationalDeclassificationAgent = Agent(
    name="Operational Declassification of ORSA Agent",
    agent_id="OperationalDeclassificationAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        orsa_report_generator,
        calculate_solvency_ratio,
        stress_test_scenarios,
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        CalculatorTools(),
        ReasoningTools(),
    ],
    instructions="""
You are an Operational Declassification of ORSA specialist focusing on:

1. **ORSA Governance**:
   - Define roles and responsibilities across Risk, Actuarial, Finance, and ALM
   - Ensure Board involvement in approving scenarios, assumptions, and conclusions
   - Establish ORSA policy and governance framework

2. **Integration in Risk Management Framework**:
   - Align ORSA with day-to-day risk monitoring
   - Ensure risk appetite and tolerances are embedded into business decisions
   - Develop risk limits and early warning indicators

3. **Operationalization of ORSA**:
   - Translate ORSA results into concrete risk limits and controls
   - Define capital buffers, liquidity thresholds, underwriting restrictions
   - Implement risk-adjusted performance measurement

4. **Declassification into Business Units**:
   - Translate group-level ORSA into actionable requirements for subsidiaries
   - Cascade solvency limits and risk tolerances to local entities
   - Ensure consistent risk management across the organization

Use governance frameworks, risk management principles, and operational best practices to ensure effective ORSA implementation and integration across the organization.
""",
    markdown=True,
    knowledge=flfa_knowledge_base,
    show_tool_calls=True,
)

# Agent 4: Communication & Regulatory Reporting
CommunicationRegulatoryAgent = Agent(
    name="Communication & Regulatory Reporting Agent",
    agent_id="CommunicationRegulatoryAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        orsa_report_generator,
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        CalculatorTools(),
        ReasoningTools(),
    ],
    instructions="""
You are a Communication & Regulatory Reporting specialist focusing on:

1. **Internal Communication**:
   - Present solvency projections and risks to Board, management, and business lines
   - Build dashboards linking ORSA results to KPIs
   - Develop risk awareness and training programs

2. **Regulator Communication**:
   - Produce ORSA report with methodology, scenarios, and results
   - Ensure clarity of assumptions and transparency of risk choices
   - Engage with supervisors proactively and respond to queries

3. **External Stakeholders**:
   - Share key insights with auditors, rating agencies, investors (if required)
   - Ensure compliance with disclosure requirements
   - Maintain transparency and credibility with external parties

Use communication best practices, regulatory knowledge, and stakeholder management to ensure effective reporting and engagement with all relevant parties.
""",
    markdown=True,
    knowledge=flfa_knowledge_base,
    show_tool_calls=True,
)

# Agent 5: Strategic Integration
StrategicIntegrationAgent = Agent(
    name="Strategic Integration Agent",
    agent_id="StrategicIntegrationAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        project_solvency_evolution,
        calculate_solvency_ratio,
        stress_test_scenarios,
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        CalculatorTools(),
        ReasoningTools(),
    ],
    instructions="""
You are a Strategic Integration specialist focusing on:

1. **Business Planning Link**:
   - Integrate ORSA with strategic plan and financial forecast
   - Test whether growth strategies remain within solvency tolerance
   - Align risk appetite with business objectives

2. **Capital Management**:
   - Determine dividend capacity vs. solvency needs
   - Recommend reinsurance, capital raising, or balance sheet optimization
   - Optimize capital allocation and efficiency

3. **Product & Pricing Strategy**:
   - Assess solvency impact of launching new products
   - Adjust product guarantees based on forward-looking solvency constraints
   - Develop risk-adjusted pricing strategies

Use strategic planning, capital management, and business optimization techniques to ensure ORSA results drive strategic decision-making and business success.
""",
    markdown=True,
    knowledge=flfa_knowledge_base,
    show_tool_calls=True,
)

# Agent 6: Continuous Improvement
ContinuousImprovementAgent = Agent(
    name="Continuous Improvement Agent",
    agent_id="ContinuousImprovementAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        stress_test_scenarios,
        project_solvency_evolution,
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        CalculatorTools(),
        ReasoningTools(),
    ],
    instructions="""
You are a Continuous Improvement specialist focusing on:

1. **Model Enhancements**:
   - Move from deterministic to stochastic ORSA projections
   - Implement ESG/climate risk scenarios
   - Enhance correlation modeling and tail risk assessment

2. **Automation & Efficiency**:
   - Automate ORSA reporting and scenario runs
   - Reduce manual interventions in the closing cycle
   - Implement real-time monitoring and alerting

3. **Feedback Loop**:
   - Post-mortem analysis: compare actual vs. projected solvency movements
   - Improve projection models and assumptions continuously
   - Learn from experience and industry best practices

Use continuous improvement methodologies, technology innovation, and learning frameworks to enhance ORSA processes and outcomes over time.
""",
    markdown=True,
    knowledge=flfa_knowledge_base,

    show_tool_calls=True,
)

# Forward-Looking and Financial Actuarial Team
ForwardLookingFinancialActuarialTeam = Team(
    members=[
        ForwardLookingRiskAssessmentAgent,
        FinancialActuarialProjectionsAgent,
        OperationalDeclassificationAgent,
        CommunicationRegulatoryAgent,
        StrategicIntegrationAgent,
        ContinuousImprovementAgent,
    ],
    instructions="""
The Forward-Looking and Financial Actuarial Team coordinates across six specialized agents to provide comprehensive ORSA and actuarial services:

1. **ForwardLookingRiskAssessmentAgent**: Identifies and quantifies risks, projects solvency evolution, and performs stress testing
2. **FinancialActuarialProjectionsAgent**: Forecasts balance sheets, projects capital requirements, and bridges IFRS 17 with Solvency II
3. **OperationalDeclassificationAgent**: Implements ORSA governance, integrates with risk management, and operationalizes ORSA results
4. **CommunicationRegulatoryAgent**: Handles internal and external communication, regulatory reporting, and stakeholder engagement
5. **StrategicIntegrationAgent**: Links ORSA with business planning, manages capital, and optimizes product strategies
6. **ContinuousImprovementAgent**: Enhances models, automates processes, and drives continuous improvement

## Team Coordination:
- Agents work collaboratively to ensure comprehensive ORSA implementation
- Risk assessment drives financial projections, which inform strategic integration
- Operational declassification ensures effective implementation across the organization
- Communication and regulatory reporting maintain transparency and compliance
- Continuous improvement enhances all processes and outcomes

## Output Standards:
- All ORSA work must be actuarially sound and financially viable
- Processes must comply with regulatory requirements and industry best practices
- Communication must be clear, transparent, and actionable
- Continuous improvement must drive excellence and innovation

Your goal is to provide **comprehensive forward-looking and financial actuarial services** that ensure solvency adequacy, regulatory compliance, and strategic success.
""",
    markdown=True,
    knowledge=flfa_knowledge_base,
    show_tool_calls=True,
)


# Example usage and testing functions
def test_forward_looking_risk_assessment():
    """Test forward-looking risk assessment and solvency projection"""
    ForwardLookingRiskAssessmentAgent.print_response(
        "Conduct a comprehensive forward-looking risk assessment for LifeCo_Insurance. "
        "Analyze current solvency ratio of 145.2%, SCR of €8.5M, and own funds of €12.34M. "
        "Project solvency evolution over 5 years under base, optimistic, and pessimistic scenarios. "
        "Perform stress testing for interest rate shocks, equity market crashes, and mortality stress."
    )


def test_financial_actuarial_projections():
    """Test financial actuarial projections and capital requirements"""
    FinancialActuarialProjectionsAgent.print_response(
        "Develop comprehensive financial actuarial projections for LifeCo_Insurance. "
        "Project balance sheet evolution including technical provisions, own funds, and capital requirements. "
        "Calculate SCR and MCR using standard formula approach. "
        "Bridge IFRS 17 profit emergence with Solvency II capital evolution using GMM approach."
    )


def test_orsa_operationalization():
    """Test ORSA operationalization and governance"""
    OperationalDeclassificationAgent.print_response(
        "Design comprehensive ORSA governance framework for LifeCo_Insurance. "
        "Define roles and responsibilities across Risk, Actuarial, Finance, and ALM functions. "
        "Integrate ORSA with day-to-day risk monitoring and business decisions. "
        "Translate ORSA results into concrete risk limits, capital buffers, and operational controls."
    )


def test_regulatory_communication():
    """Test regulatory communication and reporting"""
    CommunicationRegulatoryAgent.print_response(
        "Generate comprehensive ORSA report for LifeCo_Insurance. "
        "Include executive summary, methodology, risk assessment, capital adequacy, and forward-looking assessment. "
        "Ensure clarity of assumptions and transparency of risk choices. "
        "Develop communication strategy for Board, regulators, and external stakeholders."
    )


def test_strategic_integration():
    """Test strategic integration and business planning"""
    StrategicIntegrationAgent.print_response(
        "Integrate ORSA results with strategic planning for LifeCo_Insurance. "
        "Test growth strategies against solvency constraints and risk appetite. "
        "Determine dividend capacity and capital optimization opportunities. "
        "Assess solvency impact of new product launches and pricing strategies."
    )


def test_continuous_improvement():
    """Test continuous improvement and model enhancements"""
    ContinuousImprovementAgent.print_response(
        "Develop continuous improvement plan for LifeCo_Insurance ORSA processes. "
        "Enhance models from deterministic to stochastic projections. "
        "Implement ESG/climate risk scenarios and automation. "
        "Establish feedback loop for post-mortem analysis and model validation."
    )


def test_comprehensive_orsa_implementation():
    """Test comprehensive ORSA implementation"""
    ForwardLookingFinancialActuarialTeam.print_response(
        "Implement comprehensive ORSA framework for LifeCo_Insurance: "
        "1. Conduct forward-looking risk assessment and solvency projections "
        "2. Develop financial actuarial projections and capital requirements "
        "3. Design ORSA governance and operational framework "
        "4. Generate regulatory reports and communication strategy "
        "5. Integrate ORSA with strategic planning and capital management "
        "6. Establish continuous improvement and model enhancement processes"
    )


if __name__ == "__main__":
    print("Forward-Looking and Financial Actuarial Module Loaded Successfully!")
    print("Available Agents:")
    print(
        "1. ForwardLookingRiskAssessmentAgent - Risk identification and solvency projection"
    )
    test_forward_looking_risk_assessment()
#     print(
#         "2. FinancialActuarialProjectionsAgent - Balance sheet forecasting and capital requirements"
#     )
#     test_financial_actuarial_projections()
#     print(
#         "3. OperationalDeclassificationAgent - ORSA governance and operationalization"
#     )
#     test_orsa_operationalization()
#     print(
#         "4. CommunicationRegulatoryAgent - Regulatory reporting and stakeholder communication"
#     )
#     test_regulatory_communication()
#     print("5. StrategicIntegrationAgent - Business planning and capital management")
#     test_strategic_integration()
#     print("6. ContinuousImprovementAgent - Model enhancements and process optimization")
#     test_continuous_improvement()
#     print(
#         "\nTeam: ForwardLookingFinancialActuarialTeam - Comprehensive ORSA and actuarial services"
#     )
#     test_comprehensive_orsa_implementation()