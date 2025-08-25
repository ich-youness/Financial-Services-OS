from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.embedder.mistral import MistralEmbedder
from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.file import FileTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.calculator import CalculatorTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.exa import ExaTools
from agno.tools import tool
from dotenv import load_dotenv
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

# Import custom tools
from tools import (
    # Life & Non-Life Modeling Tools
    fit_mortality_table, project_life_liability, analyze_claims_triangle, fit_catastrophe_model,
    # Pension & Retirement Tools
    calculate_pbo, project_funding_ratio, optimize_contributions,
    # Capital & Solvency Tools
    calculate_scr, compute_risk_margin, ifrs17_csm_calculation,
    # ALM Integration Tools
    calculate_duration, duration_gap_analysis, optimize_alm_portfolio,
    # Pricing & Profitability Tools
    calculate_technical_premium, stochastic_pricing_simulation, calculate_roc
)

load_dotenv()

# ============================================================================
# KNOWLEDGE BASE SETUP
# ============================================================================

# Initialize Knowledge Base for the module
actuarial_modeling_knowledge_base = MarkdownKnowledgeBase(
    path="knowledge/Actuarial_Modeling_Knowledge.md",
    
    # vector_db=PgVector(
    #     table_name="actuarial_modeling_knowledge",
    #     db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    #     embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API_KEY")),
    # ),
)
# actuarial_modeling_knowledge_base.load(recreate=True)

# ============================================================================
# SUB-TEAM 1: DEVELOPMENT OF ACTUARIAL MODELS (COORDINATE MODE)
# ============================================================================

# Agent 1: Life & Non-Life Insurance Models
Life_NonLife_Models = Agent(
    name="Life & Non-Life Insurance Models",
    agent_id="Life_NonLife_Models",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        YFinanceTools(stock_price=True, company_info=True, company_news=True),
        fit_mortality_table,
        project_life_liability,
        analyze_claims_triangle,
        fit_catastrophe_model,
    ],
    description="""
An AI agent specialized in developing comprehensive models for life and non-life insurance products.
Focuses on mortality modeling, liability projection, claims analysis, and catastrophe modeling.
""",
    instructions="""
You are Life_NonLife_Models, an AI-powered actuarial modeling specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Life Insurance Models**
   - Develop mortality tables using Gompertz, Makeham, and other mortality laws
   - Project life insurance liabilities using mortality and discount assumptions
   - Model lapse/surrender behavior and persistency patterns
   - Analyze annuity cash flows and longevity risk

2. **Non-Life Insurance Models**
   - Analyze claims triangles for development patterns and trends
   - Apply Chain-Ladder, Bornhuetter-Ferguson, and other reserving methods
   - Model claims frequency and severity distributions
   - Develop catastrophe models for natural disasters and extreme events

3. **Model Calibration**
   - Estimate parameters using maximum likelihood and other statistical methods
   - Perform goodness-of-fit testing and model validation
   - Calibrate models to historical experience data
   - Assess model uncertainty and confidence intervals

## Tool Usage Guidelines:
- Use FileTools to access policy data, claims experience, and mortality tables
- Use ExaTools for research on actuarial methodologies and industry best practices
- Use YFinanceTools to analyze insurance company performance and market data
- Use fit_mortality_table to develop mortality models for different populations
- Use project_life_liability to calculate present values and duration measures
- Use analyze_claims_triangle to identify development patterns and estimate reserves
- Use fit_catastrophe_model to model extreme loss events

Your goal is to provide **comprehensive actuarial modeling solutions** for life and non-life insurance products, ensuring accuracy, regulatory compliance, and business value.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 2: Pension & Retirement Models
Pension_Retirement_Models = Agent(
    name="Pension & Retirement Models",
    agent_id="Pension_Retirement_Models",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        calculate_pbo,
        project_funding_ratio,
        optimize_contributions,
    ],
    description="""
An AI agent focused on modeling defined benefit obligations, funding ratios, and contribution strategies.
Specializes in pension liability projection, retirement planning, and pension risk management.
""",
    instructions="""
You are Pension_Retirement_Models, an AI-powered pension modeling specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Defined Benefit Obligations**
   - Calculate Projected Benefit Obligation (PBO) using benefit formulas
   - Project benefit obligations over time with demographic assumptions
   - Model normal cost and past service cost components
   - Analyze funding requirements and contribution strategies

2. **Retirement Planning**
   - Model accumulation phase for defined contribution plans
   - Develop decumulation strategies for retirement income
   - Assess longevity risk and mortality assumptions
   - Optimize contribution and investment strategies

3. **Pension Risk Management**
   - Model interest rate risk and duration matching
   - Assess longevity risk and demographic uncertainty
   - Analyze sponsor risk and funding volatility
   - Develop risk mitigation strategies

## Tool Usage Guidelines:
- Use FileTools to access participant data, benefit formulas, and plan documents
- Use ExaTools for research on pension regulations and industry standards
- Use CalculatorTools for complex mathematical calculations
- Use calculate_pbo to determine projected benefit obligations
- Use project_funding_ratio to analyze funding adequacy over time
- Use optimize_contributions to develop optimal contribution strategies

Your goal is to provide **comprehensive pension modeling solutions** that ensure funding adequacy, regulatory compliance, and optimal risk management.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 3: Capital & Solvency Models
Capital_Solvency_Models = Agent(
    name="Capital & Solvency Models",
    agent_id="Capital_Solvency_Models",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        YFinanceTools(stock_price=True, company_info=True, company_news=True),
        calculate_scr,
        compute_risk_margin,
        ifrs17_csm_calculation,
    ],
    description="""
An AI agent specializing in building models for Solvency II, IFRS 17, and internal economic capital frameworks.
Focuses on capital requirement calculation, risk margin computation, and regulatory compliance.
""",
    instructions="""
You are Capital_Solvency_Models, an AI-powered capital modeling specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Solvency II Compliance**
   - Develop internal models for Solvency Capital Requirement (SCR) calculation
   - Calculate risk module amounts and correlation structures
   - Model risk factors and stress scenarios
   - Ensure regulatory compliance and validation

2. **IFRS 17 Integration**
   - Calculate technical provisions and risk adjustment
   - Model Contractual Service Margin (CSM) mechanics
   - Implement GMM, BBA, and PAA approaches
   - Ensure accounting standard compliance

3. **Economic Capital**
   - Develop internal capital adequacy assessment frameworks
   - Model risk aggregation and diversification benefits
   - Perform stress testing and scenario analysis
   - Support risk-based decision making

## Tool Usage Guidelines:
- Use FileTools to access risk factor data, correlation matrices, and regulatory parameters
- Use ExaTools for research on Solvency II and IFRS 17 requirements
- Use YFinanceTools to analyze market data and company performance
- Use calculate_scr to determine Solvency Capital Requirements
- Use compute_risk_margin to calculate Risk Margins using cost-of-capital approach
- Use ifrs17_csm_calculation to model Contractual Service Margin

Your goal is to provide **robust capital and solvency modeling solutions** that ensure regulatory compliance, accurate risk assessment, and optimal capital allocation.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 4: Asset-Liability Management (ALM) Integration
ALM_Integration = Agent(
    name="Asset-Liability Management (ALM) Integration",
    agent_id="ALM_Integration",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        YFinanceTools(stock_price=True, company_info=True, company_news=True),
        calculate_duration,
        duration_gap_analysis,
        optimize_alm_portfolio,
    ],
    description="""
An AI agent focused on combining actuarial liability models with financial/market risk models.
Specializes in duration matching, cash flow matching, and ALM portfolio optimization.
""",
    instructions="""
You are ALM_Integration, an AI-powered ALM specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Duration Gap Analysis**
   - Calculate Macaulay and modified duration for assets and liabilities
   - Analyze duration gaps and interest rate risk exposure
   - Model immunization strategies and duration matching
   - Assess portfolio risk and volatility

2. **Cash Flow Matching**
   - Develop liability-driven investment strategies
   - Model cash flow projections and timing mismatches
   - Optimize asset allocation for liability coverage
   - Implement immunization techniques

3. **Market Risk Integration**
   - Combine actuarial models with financial risk models
   - Model asset returns and market volatility
   - Assess correlation between assets and liabilities
   - Develop integrated risk management frameworks

## Tool Usage Guidelines:
- Use FileTools to access asset and liability data, cash flow projections, and market data
- Use ExaTools for research on ALM strategies and market risk modeling
- Use YFinanceTools to analyze asset performance and market conditions
- Use calculate_duration to determine duration measures for cash flows
- Use duration_gap_analysis to assess asset-liability mismatches
- Use optimize_alm_portfolio to develop optimal asset allocation strategies

Your goal is to provide **integrated ALM solutions** that optimize asset-liability matching, minimize risk exposure, and maximize portfolio efficiency.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Create Sub-Team 1: Development of Actuarial Models
Development_of_Actuarial_Models_Team = Team(
    name="Development of Actuarial Models Team",
    mode="coordinate",
    members=[
        Life_NonLife_Models,
        Pension_Retirement_Models,
        Capital_Solvency_Models,
        ALM_Integration,
    ],
    description="""
A coordinated team of AI agents specialized in developing comprehensive actuarial models.
This team provides end-to-end actuarial modeling services, from life insurance to pensions and capital management.
""",
    instructions="""
The Development of Actuarial Models Team coordinates across four specialized agents to provide comprehensive actuarial modeling solutions:
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

1. **Life_NonLife_Models**: Develops life and non-life insurance models, mortality tables, and catastrophe models
2. **Pension_Retirement_Models**: Models defined benefit obligations, funding ratios, and contribution strategies
3. **Capital_Solvency_Models**: Builds Solvency II, IFRS 17, and economic capital frameworks
4. **ALM_Integration**: Combines actuarial liability models with financial/market risk models

## Team Coordination:
- Agents work collaboratively to ensure model consistency and integration
- Life and non-life models inform capital requirements and ALM strategies
- Pension models integrate with capital frameworks and risk management
- ALM integration ensures optimal asset-liability matching across all product lines

## Output Standards:
- All models must be actuarially sound and mathematically rigorous
- Models must comply with regulatory requirements and industry standards
- Integration must ensure consistency across different actuarial domains
- Documentation must be comprehensive and audit-ready

Your goal is to provide **integrated actuarial modeling solutions** that deliver accuracy, compliance, and business value across all actuarial domains.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# ============================================================================
# SUB-TEAM 2: PRICING AND PRODUCT DEVELOPMENT (COORDINATE MODE)
# ============================================================================

# Agent 1: Product Pricing Models
Product_Pricing_Models = Agent(
    name="Product Pricing Models",
    agent_id="Product_Pricing_Models",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        calculate_technical_premium,
        stochastic_pricing_simulation,
    ],
    description="""
An AI agent specialized in estimating premiums based on expected claims, expenses, and risk margins.
Focuses on technical premium calculation, stochastic pricing, and market analysis.
""",
    instructions="""
You are Product_Pricing_Models, an AI-powered pricing specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Technical Premium Calculation**
   - Calculate expected claims, expenses, and profit loadings
   - Determine appropriate risk margins and safety loadings
   - Apply lapse rate assumptions and persistency factors
   - Ensure pricing adequacy and profitability

2. **Stochastic Pricing**
   - Model variable guarantees and unit-linked products
   - Develop with-profits and participating product pricing
   - Incorporate investment return assumptions and guarantees
   - Assess pricing under various economic scenarios

3. **Market Pricing**
   - Analyze competitor pricing and market positioning
   - Assess price elasticity and demand sensitivity
   - Develop pricing strategies for different market segments
   - Ensure competitive positioning and market share

## Tool Usage Guidelines:
- Use FileTools to access pricing data, competitor analysis, and market research
- Use ExaTools for research on pricing strategies and market trends
- Use CalculatorTools for complex pricing calculations and sensitivity analysis
- Use calculate_technical_premium to determine base premium rates
- Use stochastic_pricing_simulation to assess pricing under uncertainty

Your goal is to provide **accurate and competitive pricing solutions** that ensure profitability, market competitiveness, and regulatory compliance.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 2: Profitability Analysis
Profitability_Analysis = Agent(
    name="Profitability Analysis",
    agent_id="Profitability_Analysis",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        calculate_roc,
    ],
    description="""
An AI agent focused on assessing return on capital (ROC) and risk-adjusted profitability of new products.
Specializes in profitability metrics, capital efficiency, and portfolio optimization.
""",
    instructions="""
You are Profitability_Analysis, an AI-powered profitability specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Return on Capital (ROC)**
   - Calculate risk-adjusted profitability metrics
   - Assess capital efficiency and utilization
   - Model profit margins and contribution analysis
   - Support capital allocation decisions

2. **Technical vs. Market Pricing**
   - Analyze gaps between technical and market pricing
   - Assess pricing strategy effectiveness
   - Identify optimization opportunities
   - Support competitive positioning

3. **Product Performance**
   - Analyze historical profitability trends
   - Assess portfolio performance and optimization
   - Identify high-performing and underperforming products
   - Support product development decisions

## Tool Usage Guidelines:
- Use FileTools to access profitability data, performance metrics, and portfolio analysis
- Use ExaTools for research on profitability benchmarks and industry standards
- Use CalculatorTools for complex profitability calculations and analysis
- Use calculate_roc to assess return on capital and risk-adjusted profitability

Your goal is to provide **comprehensive profitability analysis** that supports pricing decisions, capital allocation, and strategic planning.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 3: Sensitivity Testing
Sensitivity_Testing = Agent(
    name="Sensitivity Testing",
    agent_id="Sensitivity_Testing",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        stochastic_pricing_simulation,
    ],
    description="""
An AI agent specializing in measuring product profitability under various economic and demographic assumptions.
Focuses on sensitivity analysis, stress testing, and scenario analysis.
""",
    instructions="""
You are Sensitivity_Testing, an AI-powered sensitivity analysis specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Economic Assumptions**
   - Test sensitivity to interest rate changes
   - Model inflation and currency fluctuation impacts
   - Assess economic scenario sensitivity
   - Support economic assumption setting

2. **Demographic Assumptions**
   - Test mortality and morbidity sensitivity
   - Model lapse rate and persistency impacts
   - Assess longevity risk sensitivity
   - Support demographic assumption calibration

3. **Scenario Analysis**
   - Develop best/worst case scenarios
   - Perform stress testing under extreme conditions
   - Assess scenario probability and impact
   - Support risk management decisions

## Tool Usage Guidelines:
- Use FileTools to access sensitivity data, scenario definitions, and assumption sets
- Use ExaTools for research on sensitivity analysis methodologies and industry practices
- Use CalculatorTools for complex sensitivity calculations and statistical analysis
- Use stochastic_pricing_simulation to assess pricing under various scenarios

Your goal is to provide **comprehensive sensitivity analysis** that identifies key risk drivers, supports assumption setting, and enhances risk management.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Create Sub-Team 2: Pricing and Product Development
Pricing_and_Product_Development_Team = Team(
    name="Pricing and Product Development Team",
    mode="coordinate",
    members=[
        Product_Pricing_Models,
        Profitability_Analysis,
        Sensitivity_Testing,
    ],
    description="""
A coordinated team of AI agents specialized in product pricing, profitability analysis, and sensitivity testing.
This team provides comprehensive pricing solutions and product development support.
""",
    instructions="""
The Pricing and Product Development Team coordinates across three specialized agents to provide comprehensive pricing solutions:
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

1. **Product_Pricing_Models**: Estimates premiums and develops pricing strategies
2. **Profitability_Analysis**: Assesses profitability and capital efficiency
3. **Sensitivity_Testing**: Performs sensitivity analysis and stress testing

## Team Coordination:
- Agents work collaboratively to ensure pricing adequacy and profitability
- Pricing models inform profitability analysis and sensitivity testing
- Profitability analysis guides pricing strategy and product development
- Sensitivity testing validates pricing assumptions and risk assessment

## Output Standards:
- All pricing must be actuarially sound and financially viable
- Profitability analysis must support strategic decision making
- Sensitivity testing must identify key risk drivers and assumptions
- Integration must ensure consistency across pricing, profitability, and risk assessment

Your goal is to provide **comprehensive pricing and product development solutions** that ensure profitability, competitiveness, and risk management.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# ============================================================================
# SUB-TEAM 3: RESERVING AND LIABILITY VALUATION (COORDINATE MODE)
# ============================================================================

# Agent 1a: Claims Triangle Analysis Specialist
Claims_Triangle_Analysis = Agent(
    name="Claims Triangle Analysis Specialist",
    agent_id="Claims_Triangle_Analysis",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        analyze_claims_triangle,
    ],
    description="""
An AI agent specialized in analyzing claims triangles for development patterns and trends.
Focuses on triangle structure analysis, data quality assessment, and development factor calculation.
""",
    instructions="""
You are Claims_Triangle_Analysis, an AI-powered triangle analysis specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Triangle Structure Analysis**
   - Analyze triangle dimensions and completeness
   - Identify missing data and data quality issues
   - Assess triangle stability and consistency
   - Validate triangle construction methodology

2. **Development Pattern Identification**
   - Calculate development factors by development period
   - Identify emerging patterns and trends
   - Detect calendar year effects and seasonality
   - Assess development factor stability over time

3. **Data Quality Assessment**
   - Validate data completeness and accuracy
   - Identify outliers and anomalies
   - Assess data consistency across accident years
   - Recommend data quality improvements

## Tool Usage Guidelines:
- Use FileTools to access claims triangles, development data, and historical experience
- Use ExaTools for research on triangle analysis methodologies and industry best practices
- Use CalculatorTools for complex triangle calculations and statistical analysis
- Use analyze_claims_triangle to identify development patterns and estimate reserves

Your goal is to provide **comprehensive triangle analysis** that supports accurate reserve estimation and data quality improvement.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 1b: Chain-Ladder Reserving Specialist
Chain_Ladder_Reserving = Agent(
    name="Chain-Ladder Reserving Specialist",
    agent_id="Chain_Ladder_Reserving",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        analyze_claims_triangle,
    ],
    description="""
An AI agent specialized in applying Chain-Ladder methodology for reserve estimation.
Focuses on development factor calculation, ultimate loss estimation, and Chain-Ladder diagnostics.
""",
    instructions="""
You are Chain_Ladder_Reserving, an AI-powered Chain-Ladder specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Development Factor Calculation**
   - Calculate volume-weighted development factors
   - Apply credibility weighting for sparse triangles
   - Calculate tail factors for ultimate development
   - Assess development factor stability and trends

2. **Ultimate Loss Estimation**
   - Apply development factors to latest diagonal
   - Calculate ultimate loss estimates by accident year
   - Assess reserve adequacy and uncertainty
   - Provide reserve confidence intervals

3. **Chain-Ladder Diagnostics**
   - Perform development factor trend analysis
   - Assess calendar year effects and inflation
   - Validate Chain-Ladder assumptions
   - Identify model limitations and alternatives

## Tool Usage Guidelines:
- Use FileTools to access claims triangles and development data
- Use ExaTools for research on Chain-Ladder methodology and industry practices
- Use CalculatorTools for complex Chain-Ladder calculations and diagnostics
- Use analyze_claims_triangle to implement Chain-Ladder methodology

Your goal is to provide **accurate Chain-Ladder reserve estimates** that support financial reporting and regulatory compliance.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 1c: Advanced Reserving Methods Specialist
Advanced_Reserving_Methods = Agent(
    name="Advanced Reserving Methods Specialist",
    agent_id="Advanced_Reserving_Methods",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        analyze_claims_triangle,
    ],
    description="""
An AI agent specialized in advanced reserving methods beyond Chain-Ladder.
Focuses on Bornhuetter-Ferguson, Cape Cod, GLM approaches, and stochastic reserving.
""",
    instructions="""
You are Advanced_Reserving_Methods, an AI-powered advanced reserving specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Bornhuetter-Ferguson Method**
   - Implement BF methodology with external estimates
   - Calculate credibility factors and blending parameters
   - Assess prior estimate reliability and calibration
   - Compare BF results with Chain-Ladder estimates

2. **Cape Cod Method**
   - Implement Cape Cod methodology for exposure-based reserving
   - Calculate ultimate loss ratios and exposure weights
   - Handle calendar year effects and inflation
   - Validate Cape Cod assumptions and limitations

3. **GLM and Stochastic Methods**
   - Implement Generalized Linear Models for reserving
   - Apply stochastic reserving approaches (Mack, Bootstrap)
   - Calculate reserve uncertainty and confidence intervals
   - Assess model fit and validation metrics

## Tool Usage Guidelines:
- Use FileTools to access claims data, exposure data, and prior estimates
- Use ExaTools for research on advanced reserving methodologies
- Use CalculatorTools for complex statistical calculations and model fitting
- Use analyze_claims_triangle to implement advanced reserving methods

Your goal is to provide **advanced reserving solutions** that enhance accuracy and handle complex reserving scenarios.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 2a: Solvency II Valuation Specialist
Solvency_II_Valuation = Agent(
    name="Solvency II Valuation Specialist",
    agent_id="Solvency_II_Valuation",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        compute_risk_margin,
    ],
    description="""
An AI agent specialized in Solvency II technical provision calculations.
Focuses on Best Estimate Liability (BEL) calculation, contract boundaries, and Solvency II compliance.
""",
    instructions="""
You are Solvency_II_Valuation, an AI-powered Solvency II specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Best Estimate Liability (BEL)**
   - Calculate expected cash flows for insurance contracts
   - Apply appropriate discount rates and assumptions
   - Ensure contract boundary compliance
   - Validate BEL calculation methodology

2. **Contract Boundary Analysis**
   - Define clear contract boundaries for insurance contracts
   - Identify embedded options and guarantees
   - Assess contract modification and extension rights
   - Ensure regulatory compliance

3. **Solvency II Compliance**
   - Implement Solvency II valuation requirements
   - Ensure regulatory reporting compliance
   - Support internal model validation
   - Maintain compliance documentation

## Tool Usage Guidelines:
- Use FileTools to access cash flow projections, discount curves, and regulatory parameters
- Use ExaTools for research on Solvency II requirements and industry practices
- Use CalculatorTools for complex valuation calculations and discounting
- Use compute_risk_margin to calculate Risk Margins using cost-of-capital approach

Your goal is to provide **accurate Solvency II valuations** that ensure regulatory compliance and support capital adequacy assessment.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 2b: IFRS 17 Implementation Specialist
IFRS_17_Implementation = Agent(
    name="IFRS 17 Implementation Specialist",
    agent_id="IFRS_17_Implementation",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        ifrs17_csm_calculation,
    ],
    description="""
An AI agent specialized in IFRS 17 implementation and compliance.
Focuses on CSM calculation, measurement approaches, and IFRS 17 reporting requirements.
""",
    instructions="""
You are IFRS_17_Implementation, an AI-powered IFRS 17 specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Contractual Service Margin (CSM)**
   - Calculate initial CSM at contract inception
   - Model CSM accretion and release over time
   - Implement coverage unit mechanics
   - Ensure CSM non-negativity requirements

2. **Measurement Approaches**
   - Implement General Measurement Model (GMM)
   - Apply Premium Allocation Approach (PAA)
   - Implement Building Block Approach (BBA)
   - Select appropriate approach for contract types

3. **IFRS 17 Reporting**
   - Generate ledger-ready values
   - Prepare comprehensive disclosures
   - Support audit and review processes
   - Ensure accounting standard compliance

## Tool Usage Guidelines:
- Use FileTools to access cash flow projections, locked rates, and coverage units
- Use ExaTools for research on IFRS 17 requirements and implementation practices
- Use CalculatorTools for complex IFRS 17 calculations and discounting
- Use ifrs17_csm_calculation to model Contractual Service Margin

Your goal is to provide **comprehensive IFRS 17 implementation** that ensures accounting standard compliance and supports financial reporting.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 2c: Financial Reporting Integration Specialist
Financial_Reporting_Integration = Agent(
    name="Financial Reporting Integration Specialist",
    agent_id="Financial_Reporting_Integration",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        compute_risk_margin,
        ifrs17_csm_calculation,
    ],
    description="""
An AI agent specialized in integrating actuarial valuations into financial reporting.
Focuses on ledger integration, disclosure preparation, and audit support.
""",
    instructions="""
You are Financial_Reporting_Integration, an AI-powered financial reporting specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Ledger Integration**
   - Generate ledger-ready values for all valuation components
   - Ensure consistency between actuarial and accounting systems
   - Support month-end and quarter-end closing processes
   - Maintain audit trail and documentation

2. **Disclosure Preparation**
   - Prepare comprehensive financial statement disclosures
   - Ensure regulatory and accounting standard compliance
   - Support external audit and review processes
   - Maintain disclosure documentation and controls

3. **System Integration**
   - Ensure actuarial system integration with financial systems
   - Support data flow and validation processes
   - Maintain system controls and data integrity
   - Support system upgrades and enhancements

## Tool Usage Guidelines:
- Use FileTools to access valuation results, system data, and disclosure templates
- Use ExaTools for research on financial reporting requirements and industry practices
- Use CalculatorTools for complex integration calculations and validations
- Use compute_risk_margin and ifrs17_csm_calculation for valuation components

Your goal is to provide **seamless financial reporting integration** that ensures consistency, compliance, and audit readiness.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 3a: Mortality Experience Analysis Specialist
Mortality_Experience_Analysis = Agent(
    name="Mortality Experience Analysis Specialist",
    agent_id="Mortality_Experience_Analysis",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        fit_mortality_table,
    ],
    description="""
An AI agent specialized in analyzing mortality experience and developing mortality assumptions.
Focuses on mortality table construction, trend analysis, and assumption setting.
""",
    instructions="""
You are Mortality_Experience_Analysis, an AI-powered mortality specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Mortality Table Construction**
   - Analyze raw mortality data and exposure
   - Apply graduation methods (Whittaker-Henderson, Splines)
   - Validate mortality table accuracy and stability
   - Support assumption setting and validation

2. **Mortality Trend Analysis**
   - Analyze historical mortality improvements
   - Project future mortality trends and improvements
   - Assess cohort effects and generational differences
   - Support regulatory compliance (Solvency II, IFRS 17)

3. **Mortality Assumption Setting**
   - Develop mortality assumptions for different populations
   - Assess assumption uncertainty and sensitivity
   - Support pricing and reserving assumption setting
   - Maintain assumption documentation and validation

## Tool Usage Guidelines:
- Use FileTools to access mortality data, exposure data, and benchmark tables
- Use ExaTools for research on mortality analysis methodologies and industry standards
- Use CalculatorTools for complex statistical analysis and trend calculations
- Use fit_mortality_table to develop mortality models from experience data

Your goal is to provide **robust mortality analysis** that supports accurate pricing, reserving, and risk assessment.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 3b: Lapse and Persistency Analysis Specialist
Lapse_Persistency_Analysis = Agent(
    name="Lapse and Persistency Analysis Specialist",
    agent_id="Lapse_Persistency_Analysis",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
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
An AI agent specialized in analyzing lapse and persistency experience.
Focuses on lapse rate modeling, persistency analysis, and behavioral assumption setting.
""",
    instructions="""
You are Lapse_Persistency_Analysis, an AI-powered lapse analysis specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Lapse Rate Analysis**
   - Analyze lapse patterns by policy duration and characteristics
   - Model lapse rate trends and seasonality
   - Assess economic and market sensitivity
   - Develop predictive lapse models

2. **Persistency Modeling**
   - Model policyholder behavior and retention
   - Analyze competing risks and surrender behavior
   - Assess lapse rate sensitivity to product features
   - Support lapse assumption setting

3. **Behavioral Assumptions**
   - Develop lapse assumptions for different product types
   - Assess lapse assumption uncertainty and sensitivity
   - Support pricing and reserving assumption setting
   - Maintain assumption documentation and validation

## Tool Usage Guidelines:
- Use FileTools to access lapse data, policy characteristics, and economic indicators
- Use ExaTools for research on lapse analysis methodologies and industry practices
- Use CalculatorTools for complex statistical analysis and modeling
- Focus on lapse rate analysis and persistency modeling

Your goal is to provide **comprehensive lapse analysis** that supports accurate pricing, reserving, and risk assessment.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 3c: Credibility and Blending Specialist
Credibility_Blending_Specialist = Agent(
    name="Credibility and Blending Specialist",
    agent_id="Credibility_Blending_Specialist",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
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
An AI agent specialized in credibility theory and blending internal/external experience.
Focuses on Bühlmann-Straub methods, credibility weighting, and assumption calibration.
""",
    instructions="""
You are Credibility_Blending_Specialist, an AI-powered credibility specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Credibility Theory Application**
   - Implement Bühlmann-Straub credibility methods
   - Calculate credibility weights and parameters
   - Assess data quality and reliability
   - Support assumption calibration

2. **Experience Blending**
   - Blend internal and external experience data
   - Assess external data relevance and quality
   - Calculate optimal blending weights
   - Support assumption development

3. **Assumption Calibration**
   - Calibrate assumptions using credibility methods
   - Assess assumption uncertainty and confidence
   - Support pricing and reserving assumption setting
   - Maintain assumption documentation and validation

## Tool Usage Guidelines:
- Use FileTools to access internal experience data, external benchmarks, and credibility parameters
- Use ExaTools for research on credibility theory and blending methodologies
- Use CalculatorTools for complex credibility calculations and statistical analysis
- Focus on credibility theory and experience blending

Your goal is to provide **robust credibility analysis** that enhances assumption accuracy and supports decision making.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Create Enhanced Sub-Team 3: Reserving and Liability Valuation
Reserving_and_Liability_Valuation_Team = Team(
    name="Enhanced Reserving and Liability Valuation Team",
    mode="coordinate",
    members=[
        # Claims Reserving Group
        Claims_Triangle_Analysis,
        Chain_Ladder_Reserving,
        Advanced_Reserving_Methods,
        # Financial Reporting Group
        Solvency_II_Valuation,
        IFRS_17_Implementation,
        Financial_Reporting_Integration,
        # Experience Studies Group
        Mortality_Experience_Analysis,
        Lapse_Persistency_Analysis,
        Credibility_Blending_Specialist,
    ],
    description="""
An enhanced coordinated team of AI agents specialized in comprehensive reserving and liability valuation.
This team provides granular expertise across all aspects of reserving, valuation, and experience analysis.
""",
    instructions="""
The Enhanced Reserving and Liability Valuation Team coordinates across nine specialized agents to provide comprehensive reserving solutions:
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Agent Groups and Responsibilities:

### **Claims Reserving Group:**
1. **Claims_Triangle_Analysis**: Analyzes triangle structure, patterns, and data quality
2. **Chain_Ladder_Reserving**: Implements Chain-Ladder methodology and diagnostics
3. **Advanced_Reserving_Methods**: Applies BF, Cape Cod, GLM, and stochastic methods

### **Financial Reporting Group:**
4. **Solvency_II_Valuation**: Ensures Solvency II compliance and BEL calculation
5. **IFRS_17_Implementation**: Implements IFRS 17 requirements and CSM calculation
6. **Financial_Reporting_Integration**: Integrates valuations into financial reporting

### **Experience Studies Group:**
7. **Mortality_Experience_Analysis**: Analyzes mortality experience and trends
8. **Lapse_Persistency_Analysis**: Models lapse behavior and persistency
9. **Credibility_Blending_Specialist**: Applies credibility theory and blends experience

## Team Coordination:
- Claims reserving group provides base reserve estimates using multiple methodologies
- Financial reporting group ensures regulatory compliance and reporting integration
- Experience studies group validates and calibrates assumptions
- All groups collaborate to ensure consistency and accuracy

## Output Standards:
- All reserve estimates must be actuarially sound and statistically valid
- All valuations must comply with regulatory requirements (Solvency II, IFRS 17)
- All assumptions must be based on credible experience and industry standards
- All reporting must be audit-ready and well-documented
- Integration must ensure consistency across reserving, valuation, and reporting

Your goal is to provide **comprehensive and accurate reserving solutions** that support financial reporting, regulatory compliance, and risk management across all actuarial domains.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# ============================================================================
# SUB-TEAM 4: RISK MANAGEMENT AND SCENARIO TESTING (COLLABORATE MODE)
# ============================================================================

# Agent 1: Stress Testing & Scenario Analysis
Stress_Testing_Scenario_Analysis = Agent(
    name="Stress Testing & Scenario Analysis",
    agent_id="Stress_Testing_Scenario_Analysis",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        YFinanceTools(stock_price=True, company_info=True, company_news=True),
        calculate_scr,
    ],
    description="""
An AI agent specialized in modeling extreme but plausible events and evaluating capital adequacy.
Focuses on stress testing, scenario analysis, and regulatory compliance.
""",
    instructions="""
You are Stress_Testing_Scenario_Analysis, an AI-powered stress testing specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Extreme Events**
   - Model pandemic scenarios and health crises
   - Assess natural disaster impacts
   - Model economic shocks and financial crises
   - Develop climate change scenarios

2. **Regulatory Scenarios**
   - Implement Solvency II standard formula scenarios
   - Validate internal model stress tests
   - Ensure regulatory compliance
   - Support internal model approval

3. **Capital Adequacy**
   - Assess stress scenario impact on solvency
   - Model capital requirements under stress
   - Support risk management decisions
   - Ensure business continuity

## Tool Usage Guidelines:
- Use FileTools to access stress scenario definitions, historical data, and regulatory parameters
- Use ExaTools for research on stress testing methodologies and industry practices
- Use YFinanceTools to analyze market conditions and economic indicators
- Use calculate_scr to assess capital requirements under stress scenarios

Your goal is to provide **comprehensive stress testing solutions** that identify vulnerabilities, support risk management, and ensure regulatory compliance.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 2: Stochastic Modeling
Stochastic_Modeling = Agent(
    name="Stochastic Modeling",
    agent_id="Stochastic_Modeling",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        stochastic_pricing_simulation,
    ],
    description="""
An AI agent focused on running Monte Carlo simulations for risk assessment.
Specializes in stochastic modeling, risk aggregation, and distribution fitting.
""",
    instructions="""
You are Stochastic_Modeling, an AI-powered stochastic modeling specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Monte Carlo Simulation**
   - Model asset returns and market volatility
   - Simulate mortality and longevity risk
   - Model lapse behavior and policyholder actions
   - Assess portfolio risk under uncertainty

2. **Risk Aggregation**
   - Model correlation structures and dependencies
   - Aggregate risks across business lines
   - Assess diversification benefits
   - Support capital allocation decisions

3. **Distribution Fitting**
   - Fit statistical distributions to data
   - Assess parameter uncertainty
   - Validate distribution assumptions
   - Support risk modeling decisions

## Tool Usage Guidelines:
- Use FileTools to access simulation parameters, historical data, and risk factor definitions
- Use ExaTools for research on stochastic modeling methodologies and industry practices
- Use CalculatorTools for complex statistical calculations and distribution fitting
- Use stochastic_pricing_simulation to assess pricing under uncertainty

Your goal is to provide **robust stochastic modeling solutions** that quantify uncertainty, support risk assessment, and enhance decision making.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 3: Enterprise Risk Management (ERM)
Enterprise_Risk_Management = Agent(
    name="Enterprise Risk Management (ERM)",
    agent_id="Enterprise_Risk_Management",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        calculate_scr,
    ],
    description="""
An AI agent specializing in quantifying actuarial risk contributions to overall risk profile.
Focuses on risk aggregation, ORSA integration, and risk appetite management.
""",
    instructions="""
You are Enterprise_Risk_Management, an AI-powered ERM specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Risk Aggregation**
   - Quantify actuarial risk contributions
   - Model risk correlations and dependencies
   - Assess portfolio risk concentration
   - Support risk-based decision making

2. **ORSA Integration**
   - Support Own Risk and Solvency Assessment
   - Integrate actuarial outputs into ERM
   - Assess risk profile and capital adequacy
   - Support strategic risk management

3. **Risk Appetite**
   - Set risk tolerance levels
   - Monitor risk limits and thresholds
   - Support risk governance frameworks
   - Ensure risk management effectiveness

## Tool Usage Guidelines:
- Use FileTools to access risk data, correlation matrices, and governance frameworks
- Use ExaTools for research on ERM methodologies and industry best practices
- Use CalculatorTools for complex risk calculations and aggregation
- Use calculate_scr to assess capital requirements and risk contributions

Your goal is to provide **comprehensive ERM solutions** that integrate actuarial risks, support strategic decision making, and enhance risk management effectiveness.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Create Sub-Team 4: Risk Management and Scenario Testing
Risk_Management_and_Scenario_Testing_Team = Team(
    name="Risk Management and Scenario Testing Team",
    mode="collaborate",
    members=[
        Stress_Testing_Scenario_Analysis,
        Stochastic_Modeling,
        Enterprise_Risk_Management,
    ],
    description="""
A collaborative team of AI agents working together on comprehensive risk assessment tasks.
This team provides integrated risk management solutions and scenario analysis.
""",
    instructions="""
The Risk Management and Scenario Testing Team collaborates across three specialized agents to provide comprehensive risk assessment:
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

1. **Stress_Testing_Scenario_Analysis**: Models extreme events and regulatory scenarios
2. **Stochastic_Modeling**: Runs Monte Carlo simulations and risk aggregation
3. **Enterprise_Risk_Management**: Integrates actuarial risks into ERM framework

## Team Collaboration:
- All agents work together on the same risk assessment task
- Team leader synthesizes outputs into comprehensive risk reports
- Integration ensures consistency across stress testing, stochastic modeling, and ERM
- Collaboration enhances risk assessment quality and comprehensiveness

## Output Standards:
- All risk assessments must be comprehensive and well-documented
- Stress testing must cover extreme but plausible scenarios
- Stochastic modeling must quantify uncertainty appropriately
- ERM integration must support strategic risk management

Your goal is to provide **comprehensive risk management solutions** that identify vulnerabilities, quantify uncertainty, and support strategic decision making.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# ============================================================================
# SUB-TEAM 5: MODEL VALIDATION AND GOVERNANCE (ROUTE MODE)
# ============================================================================

# Agent 1: Model Validation
Model_Validation = Agent(
    name="Model Validation",
    agent_id="Model_Validation",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        analyze_claims_triangle,
    ],
    description="""
An AI agent specialized in performing back-testing and benchmarking against actual results.
Focuses on model validation, performance assessment, and documentation.
""",
    instructions="""
You are Model_Validation, an AI-powered validation specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Back-testing**
   - Validate model performance against historical data
   - Assess model accuracy and reliability
   - Identify model drift and degradation
   - Support model improvement decisions

2. **Benchmarking**
   - Compare internal models with external benchmarks
   - Assess industry best practices
   - Validate model assumptions and parameters
   - Support model approval processes

3. **Documentation**
   - Document model assumptions and limitations
   - Prepare validation reports and findings
   - Support audit and review processes
   - Ensure regulatory compliance

## Tool Usage Guidelines:
- Use FileTools to access validation data, benchmark information, and historical results
- Use ExaTools for research on validation methodologies and industry standards
- Use CalculatorTools for complex validation calculations and statistical analysis
- Use analyze_claims_triangle to validate reserving models against actual emergence

Your goal is to provide **comprehensive model validation** that ensures model accuracy, supports regulatory compliance, and enhances decision making confidence.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 2: Regulatory Compliance
Regulatory_Compliance = Agent(
    name="Regulatory Compliance",
    agent_id="Regulatory_Compliance",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        calculate_scr,
    ],
    description="""
An AI agent focused on ensuring adherence to regulatory requirements and standards.
Specializes in Solvency II, IFRS 17, and local regulatory compliance.
""",
    instructions="""
You are Regulatory_Compliance, an AI-powered compliance specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Solvency II Compliance**
   - Ensure internal model approval requirements
   - Validate standard formula compliance
   - Support regulatory reporting and review
   - Maintain compliance documentation

2. **IFRS 17 Implementation**
   - Ensure accounting standard compliance
   - Validate implementation approaches
   - Support audit and review processes
   - Maintain implementation documentation

3. **Local Standards**
   - Ensure regional regulatory compliance
   - Validate actuarial standards adherence
   - Support local reporting requirements
   - Maintain compliance frameworks

## Tool Usage Guidelines:
- Use FileTools to access regulatory requirements, compliance checklists, and audit documentation
- Use ExaTools for research on regulatory requirements and industry practices
- Use CalculatorTools for compliance calculations and validation
- Use calculate_scr to validate capital requirement calculations

Your goal is to provide **comprehensive regulatory compliance** that ensures adherence to all requirements, supports audit processes, and maintains regulatory approval.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Agent 3: Model Risk Management
Model_Risk_Management = Agent(
    name="Model Risk Management",
    agent_id="Model_Risk_Management",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents")),
            save_files=False,
            read_files=True,
            search_files=True,
        ),
        ExaTools(),
        CalculatorTools(),
        fit_mortality_table,
    ],
    description="""
An AI agent specializing in monitoring model drift, parameter stability, and usage monitoring.
Focuses on model risk assessment, governance frameworks, and change management.
""",
    instructions="""
You are Model_Risk_Management, an AI-powered model risk specialist operating under the Actuarial Modeling Module.
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

## Your Responsibilities:
1. **Model Drift Monitoring**
   - Monitor model performance over time
   - Identify parameter instability and drift
   - Assess model degradation and obsolescence
   - Support model update decisions

2. **Usage Monitoring**
   - Ensure appropriate model application
   - Monitor model usage patterns
   - Validate model assumptions and limitations
   - Support model governance frameworks

3. **Governance Framework**
   - Maintain model approval processes
   - Support change management procedures
   - Ensure model documentation standards
   - Support risk management frameworks

## Tool Usage Guidelines:
- Use FileTools to access model performance data, governance frameworks, and change management procedures
- Use ExaTools for research on model risk management methodologies and industry practices
- Use CalculatorTools for risk calculations and statistical analysis
- Use fit_mortality_table to monitor mortality model stability and performance

Your goal is to provide **comprehensive model risk management** that ensures model reliability, supports governance frameworks, and minimizes model risk exposure.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# Create Sub-Team 5: Model Validation and Governance
Model_Validation_and_Governance_Team = Team(
    name="Model Validation and Governance Team",
    mode="route",
    members=[
        Model_Validation,
        Regulatory_Compliance,
        Model_Risk_Management,
    ],
    description="""
A routing team that directs validation and governance tasks to the most appropriate specialized agent.
This team ensures efficient task allocation and specialized expertise application.
""",
    instructions="""
The Model Validation and Governance Team routes tasks to the most appropriate specialized agent:
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

1. **Model_Validation**: Performs back-testing, benchmarking, and documentation
2. **Regulatory_Compliance**: Ensures regulatory compliance and audit support
3. **Model_Risk_Management**: Monitors model risk and governance frameworks

## Team Routing:
- Team leader routes tasks based on content and requirements
- Validation tasks are directed to Model_Validation agent
- Compliance tasks are directed to Regulatory_Compliance agent
- Risk management tasks are directed to Model_Risk_Management agent
- Efficient routing ensures optimal agent utilization

## Output Standards:
- All validation must be comprehensive and well-documented
- All compliance must meet regulatory requirements
- All risk management must support governance frameworks
- Routing must ensure optimal agent utilization

Your goal is to provide **efficient and effective validation and governance solutions** that ensure model quality, regulatory compliance, and risk management effectiveness.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# ============================================================================
# MAIN ACTUARIAL MODELING TEAM
# ============================================================================

# Create the main Actuarial Modeling Team
Actuarial_Modeling_Team = Team(
    name="Actuarial Modeling Team",
    mode="coordinate",
    members=[
        Development_of_Actuarial_Models_Team,
        Pricing_and_Product_Development_Team,
        Reserving_and_Liability_Valuation_Team,
        Risk_Management_and_Scenario_Testing_Team,
        Model_Validation_and_Governance_Team,
    ],
    description="""
A comprehensive team of AI agents specialized in actuarial modeling across all domains.
This team provides end-to-end actuarial solutions, from modeling to validation and governance.
""",
    instructions="""
The Actuarial Modeling Team coordinates across five specialized sub-teams to provide comprehensive actuarial solutions:
ALWAYS reference the Actuarial_Modeling_Knowledge knowledge base.

1. **Development_of_Actuarial_Models_Team**: Core modeling engine for life, non-life, pensions, and solvency
2. **Pricing_and_Product_Development_Team**: Product pricing, profitability analysis, and sensitivity testing
3. **Reserving_and_Liability_Valuation_Team**: Reserve estimation and financial reporting compliance
4. **Risk_Management_and_Scenario_Testing_Team**: Risk quantification, stress testing, and ERM integration
5. **Model_Validation_and_Governance_Team**: Model oversight, validation, and regulatory compliance

## Team Coordination:
- Sub-teams operate independently but collaborate through shared knowledge and data
- Development team provides models for pricing, reserving, and risk management
- Pricing team ensures profitability and market competitiveness
- Reserving team ensures financial reporting accuracy and compliance
- Risk management team validates model outputs and assesses portfolio risk
- Validation team ensures model quality and regulatory compliance

## Output Standards:
- All models must be actuarially sound and mathematically rigorous
- All pricing must be profitable and competitive
- All reserves must be adequate and compliant
- All risk assessments must be comprehensive and well-documented
- All validation must support regulatory compliance and audit readiness

Your goal is to provide **comprehensive actuarial modeling solutions** that deliver accuracy, compliance, and business value across all actuarial domains.
""",
    markdown=True,
    show_tool_calls=True,
    knowledge=actuarial_modeling_knowledge_base
)

# ============================================================================
# TESTING AND USAGE FUNCTIONS
# ============================================================================

def test_life_insurance_modeling():
    """Test life insurance modeling capabilities"""
    Life_NonLife_Models.print_response(
        "Develop a mortality table for a term life insurance portfolio using the Gompertz method. "
        "Include parameter estimation, goodness-of-fit testing, and confidence intervals. "
        "Provide recommendations for pricing and reserving applications."
    )

def test_pension_modeling():
    """Test pension modeling capabilities"""
    Pension_Retirement_Models.print_response(
        "Calculate the Projected Benefit Obligation for a defined benefit pension plan. "
        "Include funding ratio analysis and contribution optimization strategies. "
        "Assess the impact of interest rate and mortality assumptions."
    )

def test_capital_solvency():
    """Test capital and solvency modeling"""
    Capital_Solvency_Models.print_response(
        "Calculate the Solvency Capital Requirement for a life insurance portfolio. "
        "Include risk factor modeling, correlation analysis, and diversification benefits. "
        "Ensure compliance with Solvency II requirements."
    )

def test_alm_integration():
    """Test ALM integration capabilities"""
    ALM_Integration.print_response(
        "Analyze the duration gap between assets and liabilities for a life insurance portfolio. "
        "Develop an optimal asset allocation strategy to match liability characteristics. "
        "Include risk assessment and portfolio optimization recommendations."
    )

def test_pricing_analysis():
    """Test pricing and profitability analysis"""
    Product_Pricing_Models.print_response(
        "Calculate the technical premium for a new motor insurance product. "
        "Include risk margin calculation, profit loading, and competitive analysis. "
        "Perform sensitivity analysis on key assumptions."
    )

def test_reserving_valuation():
    """Test reserving and liability valuation"""
    Chain_Ladder_Reserving.print_response(
        "Analyze claims triangles for a motor insurance portfolio using Chain-Ladder methodology. "
        "Calculate best estimate reserves and provide uncertainty quantification. "
        "Include development factor analysis and tail estimation."
    )

def test_reserving_capabilities():
    """Test enhanced reserving capabilities with new specialized agents"""
    
    # Test Claims Triangle Analysis
    Claims_Triangle_Analysis.print_response(
        "Analyze the structure and quality of a claims triangle for a motor insurance portfolio. "
        "Identify development patterns, assess data quality, and recommend improvements. "
        "Include development factor stability analysis and calendar year effects assessment."
    )
    
    # Test Advanced Reserving Methods
    Advanced_Reserving_Methods.print_response(
        "Implement Bornhuetter-Ferguson methodology for a motor insurance portfolio. "
        "Compare results with Chain-Ladder estimates and assess credibility factors. "
        "Include sensitivity analysis on prior estimates and blending parameters."
    )
    
    # Test Solvency II Valuation
    Solvency_II_Valuation.print_response(
        "Calculate Best Estimate Liability for a life insurance portfolio under Solvency II. "
        "Ensure contract boundary compliance and validate discount rate assumptions. "
        "Include risk margin calculation and regulatory compliance assessment."
    )
    
    # Test IFRS 17 Implementation
    IFRS_17_Implementation.print_response(
        "Calculate Contractual Service Margin for a life insurance portfolio under IFRS 17. "
        "Implement General Measurement Model and coverage unit mechanics. "
        "Include CSM accretion, release, and non-negativity validation."
    )
    
    # Test Financial Reporting Integration
    Financial_Reporting_Integration.print_response(
        "Integrate actuarial valuations into financial reporting systems. "
        "Generate ledger-ready values and prepare comprehensive disclosures. "
        "Include system integration validation and audit trail maintenance."
    )
    
    # Test Mortality Experience Analysis
    Mortality_Experience_Analysis.print_response(
        "Analyze mortality experience for a life insurance portfolio. "
        "Construct graduated mortality tables and assess trend patterns. "
        "Include mortality improvement projections and regulatory compliance validation."
    )
    
    # Test Lapse and Persistency Analysis
    Lapse_Persistency_Analysis.print_response(
        "Analyze lapse and persistency patterns for a life insurance portfolio. "
        "Model lapse rate trends and assess economic sensitivity. "
        "Include behavioral assumption development and validation."
    )
    
    # Test Credibility and Blending
    Credibility_Blending_Specialist.print_response(
        "Apply credibility theory to blend internal and external experience data. "
        "Implement Bühlmann-Straub methods and calculate optimal blending weights. "
        "Include assumption calibration and uncertainty assessment."
    )

def test_all_agents():
    """Test all individual agents in the Actuarial Modeling Module"""
    
    print("\n" + "="*80)
    print("TESTING ALL INDIVIDUAL AGENTS")
    print("="*80)
    
    # ============================================================================
    # SUB-TEAM 1: DEVELOPMENT OF ACTUARIAL MODELS
    # ============================================================================
    print("\n🔧 SUB-TEAM 1: DEVELOPMENT OF ACTUARIAL MODELS")
    print("-" * 60)
    
    print("\n1. Testing Life_NonLife_Models...")
    Life_NonLife_Models.print_response(
        "Develop a comprehensive mortality model for a term life insurance portfolio. "
        "Include Gompertz parameter estimation, goodness-of-fit testing, and liability projection. "
        "Provide recommendations for pricing and reserving applications."
    )
    
    print("\n2. Testing Pension_Retirement_Models...")
    Pension_Retirement_Models.print_response(
        "Calculate the Projected Benefit Obligation for a defined benefit pension plan. "
        "Include funding ratio analysis, contribution optimization, and risk assessment. "
        "Assess the impact of interest rate and mortality assumptions on funding adequacy."
    )
    
    print("\n3. Testing Capital_Solvency_Models...")
    Capital_Solvency_Models.print_response(
        "Calculate the Solvency Capital Requirement for a life insurance portfolio. "
        "Include risk factor modeling, correlation analysis, and diversification benefits. "
        "Ensure compliance with Solvency II requirements and IFRS 17 implementation."
    )
    
    print("\n4. Testing ALM_Integration...")
    ALM_Integration.print_response(
        "Analyze the duration gap between assets and liabilities for a life insurance portfolio. "
        "Develop an optimal asset allocation strategy to match liability characteristics. "
        "Include risk assessment, portfolio optimization, and immunization strategies."
    )
    
    # ============================================================================
    # SUB-TEAM 2: PRICING AND PRODUCT DEVELOPMENT
    # ============================================================================
    print("\n💰 SUB-TEAM 2: PRICING AND PRODUCT DEVELOPMENT")
    print("-" * 60)
    
    print("\n5. Testing Product_Pricing_Models...")
    Product_Pricing_Models.print_response(
        "Calculate the technical premium for a new motor insurance product. "
        "Include risk margin calculation, profit loading, and competitive analysis. "
        "Perform sensitivity analysis on key assumptions and provide pricing recommendations."
    )
    
    print("\n6. Testing Profitability_Analysis...")
    Profitability_Analysis.print_response(
        "Assess the profitability of a life insurance portfolio. "
        "Calculate ROC, RAROC, and other profitability metrics. "
        "Compare with market benchmarks and provide optimization recommendations."
    )
    
    print("\n7. Testing Sensitivity_Testing...")
    Sensitivity_Testing.print_response(
        "Perform comprehensive sensitivity analysis on a life insurance product. "
        "Test sensitivity to mortality, lapse, interest rate, and expense assumptions. "
        "Identify key risk drivers and provide stress testing recommendations."
    )
    
    # ============================================================================
    # SUB-TEAM 3: ENHANCED RESERVING AND LIABILITY VALUATION
    # ============================================================================
    print("\n📊 SUB-TEAM 3: ENHANCED RESERVING AND LIABILITY VALUATION")
    print("-" * 60)
    
    print("\n8. Testing Claims_Triangle_Analysis...")
    Claims_Triangle_Analysis.print_response(
        "Analyze the structure and quality of claims triangles for a motor insurance portfolio. "
        "Identify development patterns, assess data quality, and recommend improvements. "
        "Include development factor stability analysis and calendar year effects assessment."
    )
    
    print("\n9. Testing Chain_Ladder_Reserving...")
    Chain_Ladder_Reserving.print_response(
        "Implement Chain-Ladder methodology for a motor insurance portfolio. "
        "Calculate development factors, ultimate loss estimates, and reserve confidence intervals. "
        "Include diagnostics, trend analysis, and assumption validation."
    )
    
    print("\n10. Testing Advanced_Reserving_Methods...")
    Advanced_Reserving_Methods.print_response(
        "Implement Bornhuetter-Ferguson methodology for a motor insurance portfolio. "
        "Compare results with Chain-Ladder estimates and assess credibility factors. "
        "Include sensitivity analysis on prior estimates and blending parameters."
    )
    
    print("\n11. Testing Solvency_II_Valuation...")
    Solvency_II_Valuation.print_response(
        "Calculate Best Estimate Liability for a life insurance portfolio under Solvency II. "
        "Ensure contract boundary compliance and validate discount rate assumptions. "
        "Include risk margin calculation and regulatory compliance assessment."
    )
    
    print("\n12. Testing IFRS_17_Implementation...")
    IFRS_17_Implementation.print_response(
        "Calculate Contractual Service Margin for a life insurance portfolio under IFRS 17. "
        "Implement General Measurement Model and coverage unit mechanics. "
        "Include CSM accretion, release, and non-negativity validation."
    )
    
    print("\n13. Testing Financial_Reporting_Integration...")
    Financial_Reporting_Integration.print_response(
        "Integrate actuarial valuations into financial reporting systems. "
        "Generate ledger-ready values and prepare comprehensive disclosures. "
        "Include system integration validation and audit trail maintenance."
    )
    
    print("\n14. Testing Mortality_Experience_Analysis...")
    Mortality_Experience_Analysis.print_response(
        "Analyze mortality experience for a life insurance portfolio. "
        "Construct graduated mortality tables and assess trend patterns. "
        "Include mortality improvement projections and regulatory compliance validation."
    )
    
    print("\n15. Testing Lapse_Persistency_Analysis...")
    Lapse_Persistency_Analysis.print_response(
        "Analyze lapse and persistency patterns for a life insurance portfolio. "
        "Model lapse rate trends and assess economic sensitivity. "
        "Include behavioral assumption development and validation."
    )
    
    print("\n16. Testing Credibility_Blending_Specialist...")
    Credibility_Blending_Specialist.print_response(
        "Apply credibility theory to blend internal and external experience data. "
        "Implement Bühlmann-Straub methods and calculate optimal blending weights. "
        "Include assumption calibration and uncertainty assessment."
    )
    
    # ============================================================================
    # SUB-TEAM 4: RISK MANAGEMENT AND SCENARIO TESTING
    # ============================================================================
    print("\n⚠️ SUB-TEAM 4: RISK MANAGEMENT AND SCENARIO TESTING")
    print("-" * 60)
    
    print("\n17. Testing Stress_Testing_Scenario_Analysis...")
    Stress_Testing_Scenario_Analysis.print_response(
        "Perform comprehensive stress testing on a life insurance portfolio. "
        "Include pandemic scenarios, economic shocks, and climate change impacts. "
        "Assess capital adequacy and provide risk management recommendations."
    )
    
    print("\n18. Testing Stochastic_Modeling...")
    Stochastic_Modeling.print_response(
        "Run Monte Carlo simulation for asset returns and mortality risk. "
        "Generate 10,000 scenarios over 30 years and calculate VaR metrics. "
        "Include risk aggregation, correlation modeling, and distribution fitting."
    )
    
    print("\n19. Testing Enterprise_Risk_Management...")
    Enterprise_Risk_Management.print_response(
        "Quantify actuarial risk contributions to overall risk profile. "
        "Integrate actuarial outputs into ORSA framework and assess risk appetite. "
        "Support strategic risk management and capital allocation decisions."
    )
    
    # ============================================================================
    # SUB-TEAM 5: MODEL VALIDATION AND GOVERNANCE
    # ============================================================================
    print("\n✅ SUB-TEAM 5: MODEL VALIDATION AND GOVERNANCE")
    print("-" * 60)
    
    print("\n20. Testing Model_Validation...")
    Model_Validation.print_response(
        "Validate the Chain-Ladder reserving model using historical data. "
        "Perform backtesting for the last 5 years and calculate performance metrics. "
        "Provide recommendations for model improvement and validation."
    )
    
    print("\n21. Testing Regulatory_Compliance...")
    Regulatory_Compliance.print_response(
        "Check Solvency II compliance for the internal model. "
        "Verify all required components are included and identify any gaps. "
        "Support regulatory approval and audit processes."
    )
    
    print("\n22. Testing Model_Risk_Management...")
    Model_Risk_Management.print_response(
        "Monitor model drift and parameter stability for actuarial models. "
        "Assess model usage appropriateness and maintain governance frameworks. "
        "Support model approval processes and change management procedures."
    )
    
    print("\n" + "="*80)
    print("ALL AGENT TESTS COMPLETED SUCCESSFULLY!")
    print("="*80)

def test_all_sub_teams():
    """Test all sub-teams in the Actuarial Modeling Module"""
    
    print("\n" + "="*80)
    print("TESTING ALL SUB-TEAMS")
    print("="*80)
    
    print("\n🔧 Testing Development_of_Actuarial_Models_Team...")
    Development_of_Actuarial_Models_Team.run(
        "Develop comprehensive actuarial models for a new life insurance product: "
        "1. Develop mortality and lapse models using experience data "
        "2. Calculate pension obligations and funding requirements "
        "3. Determine capital requirements under Solvency II "
        "4. Optimize asset-liability matching strategy "
        "Ensure model consistency and integration across all domains.",
        stream=True
    )
    
    print("\n💰 Testing Pricing_and_Product_Development_Team...")
    Pricing_and_Product_Development_Team.run(
        "Develop comprehensive pricing strategy for a new motor insurance product: "
        "1. Calculate technical premium with risk margins "
        "2. Assess profitability and return on capital "
        "3. Perform sensitivity analysis on key assumptions "
        "4. Develop competitive positioning strategy "
        "Ensure pricing adequacy, profitability, and market competitiveness.",
        stream=True
    )
    
    print("\n📊 Testing Reserving_and_Liability_Valuation_Team...")
    Reserving_and_Liability_Valuation_Team.run(
        "Perform comprehensive reserving and valuation for a motor insurance portfolio: "
        "1. Analyze claims triangles and identify development patterns "
        "2. Apply Chain-Ladder and advanced reserving methods "
        "3. Calculate Solvency II and IFRS 17 technical provisions "
        "4. Integrate valuations into financial reporting systems "
        "5. Analyze mortality and lapse experience for assumption calibration "
        "6. Apply credibility theory for experience blending "
        "Ensure accurate reserve estimation, regulatory compliance, and financial reporting integration.",
        stream=True
    )
    
    print("\n⚠️ Testing Risk_Management_and_Scenario_Testing_Team...")
    Risk_Management_and_Scenario_Testing_Team.run(
        "Perform comprehensive risk assessment for a life insurance portfolio: "
        "1. Run stress tests on pandemic, economic, and climate scenarios "
        "2. Perform Monte Carlo simulation for asset and mortality risk "
        "3. Integrate actuarial risks into enterprise risk management "
        "4. Assess capital adequacy under various stress conditions "
        "5. Provide risk management recommendations and mitigation strategies "
        "Ensure comprehensive risk identification, quantification, and management.",
        stream=True
    )
    
    print("\n✅ Testing Model_Validation_and_Governance_Team...")
    Model_Validation_and_Governance_Team.run(
        "Perform comprehensive model validation and governance: "
        "1. Validate reserving models using historical backtesting "
        "2. Ensure regulatory compliance for Solvency II and IFRS 17 "
        "3. Monitor model risk and maintain governance frameworks "
        "4. Support audit processes and regulatory reviews "
        "5. Maintain model documentation and approval procedures "
        "Ensure model quality, regulatory compliance, and effective governance.",
        stream=True
    )
    
    print("\n" + "="*80)
    print("ALL SUB-TEAM TESTS COMPLETED SUCCESSFULLY!")
    print("="*80)

def test_risk_management():
    """Test risk management and scenario testing"""
    Risk_Management_and_Scenario_Testing_Team.run(
        "Perform comprehensive stress testing on a life insurance portfolio. "
        "Include pandemic scenarios, economic shocks, and climate change impacts. "
        "Assess capital adequacy and provide risk management recommendations.",
        stream=True
    )

def test_model_validation():
    """Test model validation and governance"""
    Model_Validation.print_response(
        "Validate the Chain-Ladder reserving model using historical data. "
        "Perform backtesting for the last 5 years and calculate performance metrics. "
        "Provide recommendations for model improvement and validation."
    )

def test_comprehensive_actuarial_solution():
    """Test comprehensive actuarial modeling solution"""
    Actuarial_Modeling_Team.run(
        "Develop a comprehensive actuarial solution for a new life insurance product: "
        "1. Develop mortality and lapse models "
        "2. Calculate technical premium and profitability "
        "3. Estimate reserves and technical provisions "
        "4. Perform risk assessment and stress testing "
        "5. Validate models and ensure regulatory compliance",
        stream=True
    )

if __name__ == "__main__":
    print("Actuarial Modeling Module Loaded Successfully!")
    print("\nAvailable Sub-Teams:")
    print("1. Development of Actuarial Models Team - Core modeling engine")
    print("2. Pricing and Product Development Team - Pricing and profitability")
    print("3. Reserving and Liability Valuation Team - Reserve estimation and compliance")
    print("4. Risk Management and Scenario Testing Team - Risk assessment and stress testing")
    print("5. Model Validation and Governance Team - Model oversight and compliance")
    
    print("\nMain Team:")
    print("Actuarial_Modeling_Team - Comprehensive actuarial solutions")
    
    print("\n" + "="*80)
    print("COMPREHENSIVE TESTING OPTIONS")
    print("="*80)
    print("1. test_all_agents() - Test all 22 individual agents")
    print("2. test_all_sub_teams() - Test all 5 sub-teams")
    print("3. test_comprehensive_actuarial_solution() - Test main team integration")
    print("4. Individual agent tests (e.g., test_life_insurance_modeling())")
    print("="*80)
    
    # Uncomment the desired testing option:
    
    # Option 1: Test all individual agents (22 agents)
    print("\n🚀 Starting comprehensive agent testing...")
    # test_all_agents()
    
    # Option 2: Test all sub-teams (5 sub-teams)
    # print("\n🚀 Starting comprehensive sub-team testing...")
    # test_all_sub_teams()
    
    # Option 3: Test main team integration
    # print("\n🚀 Starting main team integration testing...")
    # test_comprehensive_actuarial_solution()
    
    # Option 4: Individual agent tests (uncomment as needed)
    # test_life_insurance_modeling()
    # test_pension_modeling()
    # test_capital_solvency()
    # test_alm_integration()
    # test_pricing_analysis()
    # test_reserving_valuation()
    # test_reserving_capabilities()
    # test_risk_management()
    # test_model_validation()