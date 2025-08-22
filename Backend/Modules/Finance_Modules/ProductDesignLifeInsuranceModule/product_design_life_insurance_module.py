from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.embedder.mistral import MistralEmbedder
from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.file import FileTools
from agno.tools.exa import ExaTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.calculator import CalculatorTools
from agno.tools import tool
from dotenv import load_dotenv
import os
from typing import Dict, Any
from pathlib import Path


load_dotenv()

# Initializing Knowledge Base
knowledge_base = MarkdownKnowledgeBase(
    path=("Knowledge/Product_Design_Life_Insurance_Knowledge.md"),
    #     os.path.dirname(__file__),
    #     "knowledge",
    #     "Product_Design_Life_Insurance_Knowledge.md",
    # ),
    # vector_db=PgVector(
    #     table_name="product_design_life_insurance_knowledge",
    #     db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    #     embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API_KEY")),
    # ),
)
# knowledge_base.load(recreate=True)


# Custom Life Insurance Tools
@tool(
    name="calculate_life_insurance_premium",
    description="Calculate life insurance premium using actuarial principles",
    show_result=True,
)
def calculate_life_insurance_premium(
    age: int,
    gender: str,
    coverage_amount: float,
    policy_term: int,
    policy_type: str,
    smoker_status: bool,
    occupation_class: str,
) -> Dict[str, Any]:
    """
    Calculate life insurance premium using actuarial principles.

    Args:
        age: Age of the insured
        gender: Gender of the insured (male/female)
        coverage_amount: Death benefit amount
        policy_term: Policy term in years
        policy_type: Type of policy (term/whole/endowment/ulip)
        smoker_status: Whether the insured is a smoker
        occupation_class: Occupational risk class (A/B/C/D)

    Returns:
        Dictionary containing premium calculations and assumptions
    """
    # Base mortality rates (simplified for demonstration)
    base_mortality = {
        "male": {20: 0.0005, 30: 0.0008, 40: 0.0012, 50: 0.0020, 60: 0.0040},
        "female": {20: 0.0003, 30: 0.0005, 40: 0.0008, 50: 0.0015, 60: 0.0030},
    }

    # Get base mortality rate for age group
    age_group = (age // 10) * 10
    if age_group > 60:
        age_group = 60

    mortality_rate = base_mortality[gender.lower()][age_group]

    # Apply risk factors
    risk_multiplier = 1.0
    if smoker_status:
        risk_multiplier *= 2.5

    occupation_multipliers = {"A": 1.0, "B": 1.2, "C": 1.5, "D": 2.0}
    risk_multiplier *= occupation_multipliers.get(occupation_class.upper(), 1.0)

    # Calculate net premium
    net_premium = coverage_amount * mortality_rate * risk_multiplier

    # Apply policy type factors
    policy_factors = {"term": 1.0, "whole": 1.8, "endowment": 2.2, "ulip": 1.5}

    net_premium *= policy_factors.get(policy_type.lower(), 1.0)

    # Add expense loading (25% of net premium)
    expense_loading = net_premium * 0.25

    # Add profit margin (15% of net premium)
    profit_margin = net_premium * 0.15

    # Calculate gross premium
    gross_premium = net_premium + expense_loading + profit_margin

    # Annual premium
    annual_premium = gross_premium

    # Monthly premium
    monthly_premium = annual_premium / 12

    return {
        "net_premium": round(net_premium, 2),
        "expense_loading": round(expense_loading, 2),
        "profit_margin": round(profit_margin, 2),
        "gross_premium": round(gross_premium, 2),
        "annual_premium": round(annual_premium, 2),
        "monthly_premium": round(monthly_premium, 2),
        "mortality_rate": mortality_rate,
        "risk_multiplier": risk_multiplier,
        "assumptions": {
            "age": age,
            "gender": gender,
            "coverage_amount": coverage_amount,
            "policy_term": policy_term,
            "policy_type": policy_type,
            "smoker_status": smoker_status,
            "occupation_class": occupation_class,
        },
    }


@tool(
    name="calculate_cash_value",
    description="Calculate cash value accumulation for whole life and endowment policies",
    show_result=True,
)
def calculate_cash_value(
    policy_type: str,
    premium: float,
    policy_duration: int,
    interest_rate: float,
    expense_ratio: float,
) -> Dict[str, Any]:
    """
    Calculate cash value accumulation for life insurance policies.

    Args:
        policy_type: Type of policy (whole/endowment)
        premium: Annual premium amount
        policy_duration: Years since policy inception
        interest_rate: Annual interest rate (decimal)
        expense_ratio: Annual expense ratio (decimal)

    Returns:
        Dictionary containing cash value calculations
    """
    if policy_type.lower() not in ["whole", "endowment"]:
        return {"error": "Policy type must be 'whole' or 'endowment'"}

    # Calculate net premium after expenses
    net_premium = premium * (1 - expense_ratio)

    # Calculate cash value using compound interest
    cash_value = 0
    cash_value_progression = []

    for year in range(1, policy_duration + 1):
        # Add net premium for the year
        cash_value += net_premium

        # Apply interest
        cash_value *= 1 + interest_rate

        # Add to progression
        cash_value_progression.append(
            {
                "year": year,
                "cash_value": round(cash_value, 2),
                "net_premium": round(net_premium, 2),
                "interest_earned": round(
                    cash_value - (cash_value / (1 + interest_rate)), 2
                ),
            }
        )

    # Calculate surrender value (typically 80-90% of cash value)
    surrender_value = cash_value * 0.85

    return {
        "policy_type": policy_type,
        "annual_premium": premium,
        "net_premium": round(net_premium, 2),
        "interest_rate": interest_rate,
        "expense_ratio": expense_ratio,
        "current_cash_value": round(cash_value, 2),
        "surrender_value": round(surrender_value, 2),
        "cash_value_progression": cash_value_progression,
        "total_premiums_paid": round(premium * policy_duration, 2),
        "total_interest_earned": round(cash_value - (premium * policy_duration), 2),
    }


@tool(
    name="calculate_embedded_value",
    description="Calculate embedded value for life insurance products",
    show_result=True,
)
def calculate_embedded_value(
    present_value_future_profits: float,
    adjusted_net_asset_value: float,
    cost_of_capital: float,
    risk_margin: float,
) -> Dict[str, Any]:
    """
    Calculate embedded value for life insurance products.

    Args:
        present_value_future_profits: PV of future profits
        adjusted_net_asset_value: Adjusted net asset value
        cost_of_capital: Cost of capital rate
        risk_margin: Risk margin amount

    Returns:
        Dictionary containing embedded value calculations
    """
    # Calculate embedded value
    embedded_value = present_value_future_profits + adjusted_net_asset_value

    # Calculate cost of capital
    cost_of_capital_amount = embedded_value * cost_of_capital

    # Calculate value of in-force business
    value_of_in_force = embedded_value - cost_of_capital_amount

    # Calculate new business value (simplified)
    new_business_value = value_of_in_force * 0.15  # 15% of VIF as NBV

    return {
        "present_value_future_profits": round(present_value_future_profits, 2),
        "adjusted_net_asset_value": round(adjusted_net_asset_value, 2),
        "embedded_value": round(embedded_value, 2),
        "cost_of_capital_rate": cost_of_capital,
        "cost_of_capital_amount": round(cost_of_capital_amount, 2),
        "value_of_in_force": round(value_of_in_force, 2),
        "risk_margin": round(risk_margin, 2),
        "new_business_value": round(new_business_value, 2),
        "key_metrics": {
            "embedded_value": round(embedded_value, 2),
            "value_of_in_force": round(value_of_in_force, 2),
            "new_business_value": round(new_business_value, 2),
        },
    }


# Agent 1: Market & Customer Insights for Life Insurance
MarketInsightsAgent = Agent(
    name="Market & Customer Insights Agent",
    agent_id="MarketInsightsAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        YFinanceTools(stock_price=True, company_info=True, company_news=True),
        calculate_life_insurance_premium,
    ],
    description="""
An AI agent specialized in understanding market demand drivers and customer insights for life insurance products.
Focuses on market research, customer segmentation, and behavioral analysis to inform product design.
""",
    instructions="""
You are MarketInsightsAgent, an AI-powered market research specialist operating under the Product Design Life Insurance Module.
ALWAYS reference the Product_Design_Life_Insurance knowledge base.
## Your Responsibilities:
1. **Market Research**
   - Assess customer demand for protection, savings, and investment-linked life products
   - Study competitor life products (coverage, riders, guarantees, surrender options)
   - Analyze market trends and regulatory changes affecting life insurance

2. **Customer Segmentation**
   - Differentiate product design for young professionals, families, retirees, and high-net-worth individuals
   - Identify needs for short-term protection vs. long-term savings/wealth transfer
   - Develop customer personas and needs analysis

3. **Behavioral Insights**
   - Analyze policyholder behavior (lapse rates, premium holidays, rider take-up)
   - Use analytics to predict customer preferences and retention
   - Identify behavioral patterns and risk factors

## Tool Usage Guidelines:
- Use FileTools to access market research data, customer surveys, and competitor analysis
- Use ExaTools for market research and industry trend analysis
- Use YFinanceTools to analyze insurance company performance and market data
- Use calculate_life_insurance_premium to understand pricing dynamics and market positioning
- Always consider market conditions, regulatory environment, and competitive landscape

Your goal is to provide **comprehensive market insights** that inform life insurance product design and market positioning strategies.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=knowledge_base
)

# Agent 2: Life Insurance Product Design
ProductDesignAgent = Agent(
    name="Product Design Agent",
    agent_id="ProductDesignAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        calculate_life_insurance_premium,
        calculate_cash_value,
    ],
    description="""
An AI agent focused on designing comprehensive life insurance products and solutions.
Specializes in term life, whole life, endowment, ULIPs, and riders/add-ons design.
""",
    instructions="""
You are ProductDesignAgent, an AI-powered product design specialist operating under the Product Design Life Insurance Module.
ALWAYS reference the Product_Design_Life_Insurance knowledge base.

## Your Responsibilities:
1. **Term Life Insurance**
   - Design pure protection products for fixed duration
   - Develop flexible terms: level, decreasing, renewable, convertible options
   - Optimize coverage amounts and policy terms

2. **Whole Life Insurance**
   - Design lifetime coverage with guaranteed death benefits
   - Develop cash value accumulation and savings features
   - Balance protection and investment components

3. **Endowment Insurance**
   - Design coverage plus maturity benefit products
   - Balance protection and savings objectives
   - Optimize policy terms and benefit structures

4. **Unit-Linked / Investment-Linked Insurance (ULIPs / VULs)**
   - Design products combining protection with investment in funds
   - Develop flexible premium allocation and top-up options
   - Balance risk and return objectives

5. **Riders & Add-Ons**
   - Design critical illness, accidental death, disability, waiver of premium riders
   - Develop customization options for different life stages
   - Optimize rider pricing and benefit structures

## Tool Usage Guidelines:
- Use FileTools to access product specifications, competitor products, and design requirements
- Use ExaTools for product research and industry best practices
- Use calculate_life_insurance_premium to optimize pricing and product features
- Use calculate_cash_value to design savings and investment components
- Always consider customer needs, regulatory requirements, and profitability objectives

Your goal is to design **innovative and competitive life insurance products** that meet customer needs while ensuring profitability and regulatory compliance.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=knowledge_base
)

# Agent 3: Actuarial & Financial Modeling
ActuarialModelingAgent = Agent(
    name="Actuarial & Financial Modeling Agent",
    agent_id="ActuarialModelingAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        calculate_life_insurance_premium,
        calculate_cash_value,
        calculate_embedded_value,
    ],
    description="""
An AI agent specializing in actuarial calculations, financial modeling, and risk assessment for life insurance products.
Focuses on pricing models, cash flow projections, profitability analysis, and stress testing.
""",
    instructions="""
You are ActuarialModelingAgent, an AI-powered actuarial specialist operating under the Product Design Life Insurance Module.
ALWAYS reference the Product_Design_Life_Insurance knowledge base.

## Your Responsibilities:
1. **Pricing Models**
   - Use mortality tables, lapse assumptions, and expense loadings
   - Calculate net premiums and gross premiums with profit margins
   - Develop pricing strategies for different product types

2. **Cash Flow Projections**
   - Forecast premiums, claims, reserves, and expenses across contract duration
   - Include surrender and paid-up values
   - Model different economic and demographic scenarios

3. **Profitability Analysis**
   - Evaluate embedded value (EV), new business value (NBV), and IRR
   - Assess capital strain vs. expected profits
   - Analyze product profitability and capital efficiency

4. **Stress & Scenario Testing**
   - Model mortality shock scenarios (pandemics, longevity risk)
   - Test economic stress scenarios (low interest rates, market downturns)
   - Assess capital adequacy under stress conditions

## Tool Usage Guidelines:
- Use FileTools to access actuarial data, mortality tables, and financial models
- Use ExaTools for actuarial research and industry standards
- Use CalculatorTools for complex mathematical calculations and statistical analysis
- Use calculate_life_insurance_premium for premium calculations and pricing analysis
- Use calculate_cash_value for cash value projections and policy modeling
- Use calculate_embedded_value for profitability analysis and capital assessment
- Always validate assumptions and ensure actuarial soundness

Your goal is to provide **actuarially sound financial modeling** that ensures product profitability, capital adequacy, and risk management.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=knowledge_base
)

# Agent 4: Regulatory & Compliance Alignment
RegulatoryComplianceAgent = Agent(
    name="Regulatory & Compliance Alignment Agent",
    agent_id="RegulatoryComplianceAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
    ],
    description="""
An AI agent ensuring life insurance products meet regulatory requirements and compliance standards.
Specializes in IFRS 17, Solvency II, consumer protection, and disclosure requirements.
""",
    instructions="""
You are RegulatoryComplianceAgent, an AI-powered compliance specialist operating under the Product Design Life Insurance Module.
ALWAYS reference the Product_Design_Life_Insurance knowledge base.

## Your Responsibilities:
1. **IFRS 17**
   - Model life insurance contracts under GMM, VFA, or PAA
   - Track contractual service margin (CSM) and risk adjustments
   - Ensure proper measurement and recognition of insurance contracts

2. **Solvency II / Risk-Based Capital (RBC)**
   - Calculate life technical provisions (best estimate + risk margin)
   - Assess capital requirements under standard formula or internal models
   - Ensure capital adequacy and solvency compliance

3. **Consumer Protection & Disclosure**
   - Comply with IDD, PRIIPs, and local disclosure requirements
   - Ensure fairness and transparency in illustrations and projections
   - Develop clear and understandable product documentation

## Tool Usage Guidelines:
- Use FileTools to access regulatory documents, compliance checklists, and reporting templates
- Use ExaTools for regulatory research and compliance monitoring
- Use CalculatorTools for regulatory calculations and capital requirements
- Always ensure regulatory accuracy and timely compliance updates
- Monitor evolving regulations and their impact on product design

Your goal is to ensure **100% regulatory compliance** while maintaining product competitiveness and customer value.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=knowledge_base
)

# Agent 5: Operational Implementation
OperationalImplementationAgent = Agent(
    name="Operational Implementation Agent",
    agent_id="OperationalImplementationAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        calculate_life_insurance_premium,FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
    ],
    description="""
An AI agent focused on implementing life insurance products operationally.
Specializes in underwriting design, policy administration, and distribution strategy.
""",
    instructions="""
You are OperationalImplementationAgent, an AI-powered implementation specialist operating under the Product Design Life Insurance Module.
ALWAYS reference the Product_Design_Life_Insurance knowledge base.

## Your Responsibilities:
1. **Underwriting Design**
   - Define underwriting rules, medical requirements, and risk selection criteria
   - Implement digital underwriting and AI-assisted risk scoring
   - Develop underwriting guidelines and rFileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),isk assessment frameworks

2. **Policy Administration & Systems**
   - Define requirements for policy management systems
   - Ensure integration with actuarial engines and financial reporting tools
   - Develop operational workflows and process automation

3. **Distribution Strategy**
   - Design bancassurance, agency networks, brokers, and digital channels
   - Develop incentives and training for sales teams
   - Optimize distribution efficiency and customer acquisition

## Tool Usage Guidelines:
- Use FileTools to access operational requFileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),
FileTools(Path(os.path.join(os.path.dirname(__file__), "documents"))),irements, system specifications, and process documentation
- Use ExaTools for operational research and industry best practices
- Use calculate_life_insurance_premium to understand underwriting implications
- Always consider operational efficiency, customer experience, and scalability
- Ensure seamless integration between product design and operational implementation

Your goal is to ensure **efficient and scalable operational implementation** that delivers excellent customer experience and operational excellence.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=knowledge_base
)

# Agent 6: Product Monitoring & Innovation
ProductMonitoringAgent = Agent(
    name="Product Monitoring & Innovation Agent",
    agent_id="ProductMonitoringAgent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        calculate_embedded_value,
        calculate_cash_value,
    ],
    description="""
An AI agent monitoring product performance and driving innovation in life insurance.
Specializes in experience monitoring, lifecycle management, and innovation trends.
""",
    instructions="""
You are ProductMonitoringAgent, an AI-powered monitoring and innovation specialist operating under the Product Design Life Insurance Module.
ALWAYS reference the Product_Design_Life_Insurance knowledge base.

## Your Responsibilities:
1. **Experience Monitoring**
   - Track mortality, persistency, and expense experience vs. assumptions
   - Adjust pricing and reserves if deviations arise
   - Monitor product performance and customer satisfaction

2. **Product Lifecycle Management**
   - Monitor profitability and relevance of in-force portfolios
   - Decide on repricing, redesign, or withdrawal of products
   - Optimize product portfolios for profitability and customer value

3. **Innovation Trends**
   - Develop ESG-linked life insurance (discounts for healthy lifestyles)
   - Explore embedded insurance and micro-life policies
   - Design hybrid products combining life cover + retirement + investment

## Tool Usage Guidelines:
- Use FileTools to access performance data, monitoring reports, and innovation research
- Use ExaTools for innovation research and industry trend analysis
- Use calculate_embedded_value for profitability monitoring and portfolio optimization
- Use calculate_cash_value for policy performance analysis and customer value assessment
- Always consider customer needs, market trends, and competitive positioning
- Drive continuous improvement and innovation in product design and features

Your goal is to ensure **optimal product performance** while driving innovation and maintaining competitive advantage in the life insurance market.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=knowledge_base
)

# Create the Product Design Life Insurance Team
ProductDesignLifeInsuranceTeam = Team(
    name="Product Design Life Insurance Team",
    members=[
        MarketInsightsAgent,
        ProductDesignAgent,
        ActuarialModelingAgent,
        RegulatoryComplianceAgent,
        OperationalImplementationAgent,
        ProductMonitoringAgent,
    ],
    description="""
A comprehensive team of AI agents specialized in life insurance product design and development.
This team provides end-to-end life insurance product services, from market research to operational implementation and ongoing monitoring.
""",
    instructions="""
The Product Design Life Insurance Team coordinates across six specialized agents to provide comprehensive life insurance product services:
ALWAYS reference the Product_Design_Life_Insurance knowledge base.

1. **MarketInsightsAgent**: Provides market research, customer segmentation, and behavioral insights
2. **ProductDesignAgent**: Designs comprehensive life insurance products and solutions
3. **ActuarialModelingAgent**: Develops actuarial models, pricing, and financial projections
4. **RegulatoryComplianceAgent**: Ensures regulatory compliance and consumer protection
5. **OperationalImplementationAgent**: Implements products operationally and optimizes distribution
6. **ProductMonitoringAgent**: Monitors performance and drives product innovation

## Team Coordination:
- Agents work collaboratively to ensure product design meets market needs and regulatory requirements
- Market insights inform product design, which drives actuarial modeling and compliance requirements
- Operational implementation follows product design specifications and regulatory requirements
- Product monitoring provides feedback for continuous improvement and innovation

## Output Standards:
- All product designs must be actuarially sound and financially viable
- Products must comply with all regulatory requirements and consumer protection standards
- Operational implementation must be efficient, scalable, and customer-focused
- Continuous monitoring and innovation must drive product excellence and competitive advantage

Your goal is to provide **comprehensive life insurance product design services** that deliver customer value, ensure profitability, and maintain regulatory compliance.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=knowledge_base
)


# Example usage and testing functions
def test_market_insights():
    """Test market insights and customer analysis"""
    MarketInsightsAgent.print_response(
        message="""Analyze the market demand for term life insurance products among young professionals
aged 25-35. Include competitor analysis, pricing trends, and customer preferences
for coverage amounts and policy terms."""
    )


def test_product_design():
    """Test life insurance product design"""
    ProductDesignAgent.print_response(
        "Design a comprehensive life insurance product for families with young children. "
        "Include term life coverage, critical illness rider, and waiver of premium rider. "
        "Specify coverage amounts, policy terms, and premium structure."
    )


def test_actuarial_modeling():
    """Test actuarial modeling and pricing"""
    ActuarialModelingAgent.print_response(
        "Calculate pricing for a 20-year term life policy with $500,000 coverage for a "
        "30-year-old non-smoker male in occupation class A. Include net premium, "
        "expense loading, and profit margin calculations."
    )


def test_regulatory_compliance():
    """Test regulatory compliance and requirements"""
    RegulatoryComplianceAgent.print_response(
        "Ensure a new whole life insurance product complies with IFRS 17 requirements, "
        "Solvency II capital requirements, and consumer protection regulations. "
        "Provide compliance checklist and implementation guidance."
    )


def test_operational_implementation():
    """Test operational implementation and underwriting"""
    OperationalImplementationAgent.print_response(
        "Design underwriting rules and operational workflows for a new term life product. "
        "Include risk assessment criteria, medical requirements, and digital underwriting processes. "
        "Develop distribution strategy for multiple channels."
    )


def test_product_monitoring():
    """Test product monitoring and innovation"""
    ProductMonitoringAgent.print_response(
        "Develop monitoring framework for a new life insurance product portfolio. "
        "Include performance metrics, profitability analysis, and innovation opportunities. "
        "Identify trends in ESG-linked insurance and embedded products."
    )


def test_comprehensive_product_design():
    """Test comprehensive life insurance product design"""
    for chunk in ProductDesignLifeInsuranceTeam.run(
        message="""Design a complete life insurance product from concept to implementation: "
        "1. Conduct market research and customer segmentation "
        "2. Design comprehensive product with riders and options "
        "3. Develop actuarial models and pricing strategy "
        "4. Ensure regulatory compliance and consumer protection "
        "5. Design operational implementation and distribution "
        "6. Establish monitoring framework and innovation pipeline""",
        stream=True,
    ):
        print(chunk.content, end="", flush=True)


# if __name__ == "__main__":
#     print("Product Design Life Insurance Module Loaded Successfully!")
#     print("Available Agents:")
#     print("1. MarketInsightsAgent - Market research and customer insights")
#     test_market_insights()
#     print("2. ProductDesignAgent - Life insurance product design")
#     test_product_design()
#     print("3. ActuarialModelingAgent - Actuarial modeling and pricing")
#     test_actuarial_modeling()
#     print(
#         "4. RegulatoryComplianceAgent - Regulatory compliance and consumer protection"
#     )
#     test_regulatory_compliance()
#     print(
#         "5. OperationalImplementationAgent - Operational implementation and distribution"
#     )
#     test_operational_implementation()
#     print("6. ProductMonitoringAgent - Product monitoring and innovation")
#     test_product_monitoring()
#     print(
#         "\nTeam: ProductDesignLifeInsuranceTeam - Comprehensive product design services"
#     )
#     # test_comprehensive_product_design()
