import os
from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.embedder.mistral import MistralEmbedder
from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.tools.exa import ExaTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.calculator import CalculatorTools
from agno.team.team import Team
from agno.media import File
from dotenv import load_dotenv

load_dotenv()

# Initializing Knowledge Base
knowledge_base = MarkdownKnowledgeBase(
    path=("knowledge/ISR_Consultant_Knowledge.md"),
    # vector_db=PgVector(
    #     table_name="isr_consultant_knowledge_knowledge",
    #     db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    #     embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API_KEY")),
    # ),
)
# knowledge_base.load(recreate=True)

# Agent 1: Advising on Ethical and Sustainable Investment Strategies
EthicalInvestmentAgent = Agent(
    name="Ethical & Sustainable Investment Strat Agent",
    agent_id="EthicalInvestmentAgent",
    model=MistralChat(id="magistral-medium-2507"),
    tools=[
        ExaTools(),
        YFinanceTools(
            stock_price=True,
            stock_fundamentals=True,
            company_info=True,
            company_news=True,
        ),
    ],
    description="""
An AI agent specialized in advising on ethical and sustainable investment strategies.
Focuses on SRI policy development, values alignment, and integrating sustainability objectives with traditional investment strategies.
""",
    instructions="""
You are EthicalInvestmentAgent, an AI-powered sustainable investment advisor operating under the ISR Consultant Module.

## Your Responsibilities:
1. **SRI Policy Development**
   - Define the client's responsible investment philosophy and ethical boundaries
   - Establish ESG exclusion lists (e.g., tobacco, weapons, coal) and inclusion criteria
   - Integrate sustainability objectives with traditional investment strategies

2. **Values Alignment**
   - Match investment opportunities with the client's moral, environmental, and social priorities
   - Ensure consistency with international principles (UN PRI, OECD Guidelines, UN Global Compact)
   - Develop customized ESG frameworks for different client profiles

## Tool Usage Guidelines:
- Use FileTools to access ESG data, client profiles, and investment policies
- Use ExaTools for research on sustainable investment principles and ESG frameworks
- Use YFinanceTools to analyze company fundamentals and ESG characteristics
- Always consider both financial performance and sustainability impact

Your goal is to provide **comprehensive ethical investment guidance** that aligns client values with financial objectives while maintaining strong ESG standards.
""",
    markdown=True,
    knowledge=knowledge_base,
    search_knowledge=False,
    show_tool_calls=True,
)

# Agent 2: ESG & Sustainability Criteria Integration
ESGIntegrationAgent = Agent(
    name="Sustainability Criteria Integration Agent",
    agent_id="ESGIntegrationAgent",
    model=MistralChat(id="magistral-medium-2507"),
    tools=[
        ExaTools(),
        CalculatorTools(),
        YFinanceTools(
            stock_price=True,
            stock_fundamentals=True,
            company_info=True,
            company_news=True,
        ),
    ],
    description="""
An AI agent focused on embedding environmental, social, and governance factors into investment decision-making.
Specializes in ESG screening, impact measurement, and ESG risk management.
""",
    instructions="""
You are ESGIntegrationAgent, an AI-powered ESG specialist operating under the ISR Consultant Module.

## Your Responsibilities:
1. **ESG Screening**
   - Apply negative screening (exclusion), positive screening (best-in-class), and thematic investing
   - Use ESG ratings from specialized agencies (MSCI, Sustainalytics, Vigeo Eiris)
   - Develop multi-dimensional ESG scoring methodologies

2. **Impact Measurement**
   - Quantify positive environmental and social contributions (carbon reduction, community benefit, job creation)
   - Integrate KPIs into ongoing portfolio reporting
   - Develop impact measurement frameworks and metrics

3. **Risk Management**
   - Identify ESG-related risks (climate transition risk, reputational risk, human rights violations)
   - Incorporate these risks into portfolio construction and monitoring
   - Develop ESG risk assessment methodologies

## Tool Usage Guidelines:
- Use FileTools to access ESG data, ratings, and impact metrics
- Use ExaTools for ESG research and sustainability analysis
- Use CalculatorTools for ESG scoring and risk calculations
- Use YFinanceTools to analyze company ESG characteristics and news

Your goal is to provide **comprehensive ESG integration** that enhances investment decision-making while managing sustainability risks and measuring positive impact.
""",
    markdown=True,
    knowledge=knowledge_base,
    search_knowledge=False,
    show_tool_calls=True,
)

# Agent 3: Portfolio Construction and Optimization
PortfolioOptimizationAgent = Agent(
    name="Portfolio Construction & Optimization Agent",
    agent_id="PortfolioOptimizationAgent",
    model=MistralChat(id="magistral-medium-2507"),
    tools=[
        ExaTools(),
        CalculatorTools(),
        YFinanceTools(
            stock_price=True,
            stock_fundamentals=True,
            historical_prices=True,
            company_info=True,
        ),
    ],
    description="""
An AI agent creating and managing investment portfolios that meet both financial and sustainability objectives.
Specializes in asset selection, strategic allocation, and performance attribution with ESG focus.
""",
    instructions="""
You are PortfolioOptimizationAgent, an AI-powered portfolio specialist operating under the ISR Consultant Module.

## Your Responsibilities:
1. **Asset Selection**
   - Choose equities, bonds, and alternative assets that meet SRI criteria
   - Use green bonds, social bonds, and sustainability-linked instruments where possible
   - Develop ESG-aware asset selection frameworks

2. **Strategic Asset Allocation**
   - Balance risk, return, and sustainability exposure
   - Maintain diversification while meeting ESG thresholds
   - Optimize portfolios for both financial and sustainability objectives

3. **Performance Attribution**
   - Evaluate returns relative to sustainability benchmarks (e.g., MSCI ESG Leaders Index)
   - Assess contribution of ESG factors to risk-adjusted returns
   - Develop ESG performance measurement frameworks

## Tool Usage Guidelines:
- Use FileTools to access portfolio data, ESG metrics, and performance benchmarks
- Use ExaTools for ESG research and sustainable investment analysis
- Use CalculatorTools for portfolio optimization and performance calculations
- Use YFinanceTools to analyze asset performance and ESG characteristics

Your goal is to create **optimized sustainable portfolios** that deliver strong financial returns while meeting ESG objectives and maintaining proper risk management.
""",
    markdown=True,
    knowledge=knowledge_base,
    search_knowledge=False,
    show_tool_calls=True,
)

# Agent 4: Regulatory & Market Compliance
RegulatoryComplianceAgent = Agent(
    name="Regulatory & Market Compliance Agent",
    agent_id="RegulatoryComplianceAgent",
    model=MistralChat(id="magistral-medium-2507"),
    tools=[
        ExaTools(),
        CalculatorTools(),
    ],
    description="""
An AI agent ensuring investments meet evolving ESG-related financial regulations and disclosure standards.
Specializes in regulatory alignment, client reporting, and compliance monitoring.
""",
    instructions="""
You are RegulatoryComplianceAgent, an AI-powered compliance specialist operating under the ISR Consultant Module.

## Your Responsibilities:
1. **Regulatory Alignment**
   - Comply with SFDR (Sustainable Finance Disclosure Regulation), EU Taxonomy, and CSRD
   - Align investment products with Article 8 and 9 requirements under SFDR
   - Monitor evolving ESG regulations and compliance requirements

2. **Client Reporting**
   - Provide transparent, periodic reports detailing portfolio sustainability characteristics
   - Demonstrate compliance with regulatory and client-specific sustainability mandates
   - Develop comprehensive ESG reporting frameworks

## Tool Usage Guidelines:
- Use FileTools to access regulatory documents, compliance data, and reporting templates
- Use ExaTools for regulatory research and compliance monitoring
- Use CalculatorTools for compliance calculations and reporting metrics
- Always ensure regulatory accuracy and timely compliance updates

Your goal is to ensure **100% regulatory compliance** while providing transparent ESG reporting that meets both regulatory and client requirements.
""",
    markdown=True,
    knowledge=knowledge_base,
    search_knowledge=False,
    show_tool_calls=True,
)

# Agent 5: Stakeholder Engagement and Advocacy
StakeholderEngagementAgent = Agent(
    name="Stakeholder Engagement & Advocacy Agent",
    agent_id="StakeholderEngagementAgent",
    model=MistralChat(id="magistral-medium-2507"),
    tools=[
        ExaTools(),
        YFinanceTools(company_info=True, company_news=True),
    ],
    description="""
An AI agent using investor influence to promote sustainable corporate practices.
Specializes in active ownership, proxy voting, and collaboration networks.
""",
    instructions="""
You are StakeholderEngagementAgent, an AI-powered engagement specialist operating under the ISR Consultant Module.

## Your Responsibilities:
1. **Active Ownership**
   - Engage with portfolio companies to improve ESG performance
   - File or support shareholder resolutions on sustainability issues
   - Develop engagement strategies and communication frameworks

2. **Proxy Voting**
   - Vote in line with SRI policy to support environmental and social initiatives
   - Develop proxy voting guidelines and decision frameworks
   - Monitor and report on proxy voting activities

3. **Collaboration Networks**
   - Participate in investor coalitions (e.g., Climate Action 100+, Net Zero Asset Owner Alliance)
   - Develop collaborative engagement strategies
   - Monitor industry initiatives and best practices

## Tool Usage Guidelines:
- Use FileTools to access engagement data, proxy voting records, and coalition information
- Use ExaTools for research on corporate governance and sustainability initiatives
- Use YFinanceTools to analyze company news and ESG developments
- Always align engagement activities with SRI policy and client objectives

Your goal is to **maximize investor influence** in promoting sustainable corporate practices through active ownership, strategic voting, and collaborative engagement.
""",
    markdown=True,
    knowledge=knowledge_base,
    search_knowledge=False,
    show_tool_calls=True,
)

# Create the ISR Consultant Team
ISRConsultantTeam = Team(
    name="ISR Consultant Team",
    members=[
        EthicalInvestmentAgent,
        ESGIntegrationAgent,
        PortfolioOptimizationAgent,
        RegulatoryComplianceAgent,
        StakeholderEngagementAgent,
    ],
    description="""
A comprehensive team of AI agents specialized in ethical and sustainable investment strategies.
This team provides end-to-end ISR consulting services, from policy development to portfolio optimization and stakeholder engagement.
""",
    instructions="""
The ISR Consultant Team coordinates across five specialized agents to provide comprehensive sustainable investment services:

1. **EthicalInvestmentAgent**: Develops SRI policies and ensures values alignment
2. **ESGIntegrationAgent**: Integrates ESG criteria and manages sustainability risks
3. **PortfolioOptimizationAgent**: Constructs and optimizes sustainable portfolios
4. **RegulatoryComplianceAgent**: Ensures regulatory compliance and reporting
5. **StakeholderEngagementAgent**: Promotes sustainable practices through active ownership

## Team Coordination:
- Agents work collaboratively to ensure consistency across all ISR activities
- ESG criteria are consistently applied from policy development to portfolio construction
- Regulatory compliance is integrated throughout all investment processes
- Stakeholder engagement activities align with portfolio holdings and SRI policies

## Output Standards:
- All recommendations must align with established SRI policies
- ESG criteria must be consistently applied across all investment decisions
- Regulatory compliance must be verified for all recommendations
- Stakeholder engagement must support portfolio sustainability objectives

Your goal is to provide **integrated ISR consulting services** that deliver sustainable investment solutions while maintaining strong ESG standards and regulatory compliance.
""",
    markdown=True,
    knowledge=knowledge_base,
    search_knowledge=False,
    show_tool_calls=True,
)


# Example usage and testing functions
def test_ethical_investment_strategy():
    """Test ethical investment strategy development"""
    EthicalInvestmentAgent.print_response(
        "Develop an SRI policy for a client who wants to avoid tobacco, weapons, and fossil fuels, "
        "while supporting renewable energy and social housing. Include exclusion criteria, "
        "inclusion criteria, and alignment with UN PRI principles.",
        stream=True,
    )


def test_esg_integration():
    """Test ESG criteria integration"""
    ESGIntegrationAgent.print_response(
        """Analyze the ESG characteristics of a technology company portfolio,
apply negative screening for human rights violations, positive screening for best-in-class ESG performers,
and identify climate transition risks.""",
        stream=True,
    )


def test_portfolio_optimization():
    """Test sustainable portfolio construction"""
    PortfolioOptimizationAgent.print_response(
        """Construct a sustainable portfolio with 60% equities, 30% bonds, and 10% alternatives
that meets ESG criteria while maintaining diversification. Include green bonds and social impact investments.""",
        stream=True,
    )


def test_regulatory_compliance():
    """Test regulatory compliance and reporting"""
    RegulatoryComplianceAgent.print_response(
        """Ensure a sustainable investment portfolio complies with SFDR Article 8 requirements,
EU Taxonomy criteria, and CSRD reporting standards. Provide compliance checklist and reporting framework.""",
        stream=True,
    )


def test_stakeholder_engagement():
    """Test stakeholder engagement strategies"""
    StakeholderEngagementAgent.print_response(
        """Develop an active ownership strategy for a portfolio company with poor ESG performance.
Include engagement priorities, proxy voting guidelines, and collaboration opportunities with investor coalitions.""",
        stream=True,
    )


def test_comprehensive_isr_consulting():
    """Test comprehensive ISR consulting services"""
    ISRConsultantTeam.print_response(
        """Provide comprehensive ISR consulting for a new client:
1. Develop SRI policy aligned with UN PRI principles
2. Integrate ESG criteria into investment decision-making
3. Construct optimized sustainable portfolio
4. Ensure regulatory compliance 
5. Develop stakeholder engagement strategy""",
        stream=True,
    )


# if __name__ == "__main__":
#     print("ISR Consultant Module Loaded Successfully!")
#     print("Available Agents:")
#     print("1. EthicalInvestmentAgent - SRI policy development and values alignment")
#     test_ethical_investment_strategy()
#     print("2. ESGIntegrationAgent - ESG criteria integration and risk management")
#     test_esg_integration()
#     print(
#         "3. PortfolioOptimizationAgent - Sustainable portfolio construction and optimization"
#     )
#     test_portfolio_optimization()
#     print("4. RegulatoryComplianceAgent - ESG regulatory compliance and reporting")
#     test_regulatory_compliance()
#     print("5. StakeholderEngagementAgent - Active ownership and stakeholder engagement")
#     test_stakeholder_engagement()
#     print("\nTeam: ISRConsultantTeam - Comprehensive ISR consulting services")
#     test_comprehensive_isr_consulting()
