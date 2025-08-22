import os
from agno.team import Team
from textwrap import dedent
from agno.agent import Agent
from datetime import datetime
from dotenv import load_dotenv
from agno.models.xai import xAI
# from agno.models.openai import OpenAIChat
from agno.tools.csv_toolkit import CsvTools
from agno.models.mistral import MistralChat
from agno.vectordb.pgvector import PgVector
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.calculator import CalculatorTools
from agno.embedder.mistral import MistralEmbedder
from agno.tools.googlesearch import GoogleSearchTools
from agno.knowledge.markdown import MarkdownKnowledgeBase

load_dotenv()

# Initializing Knowledge Base
knowledge_base = MarkdownKnowledgeBase(
    path="MarkdownKnowledge/company_data.md",
    # vector_db=PgVector(
    #     table_name="analyst_fin_reporting_and_ref_knowledge",
    #     db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    #     embedder=MistralEmbedder(api_key=os.getenv('MISTRAL_API_KEY')),
    # ),
)
# knowledge_base.load(recreate=True)

MarketAndCustomerNeedsAnalysis = Agent(
    name="Market and Customer Needs Analysis",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Market and Customer Needs Analysis Assistant",
    description="You are an agent specialized in Market & Customer Needs Analysis for the insurance industry.",
    instructions=dedent("""
    You are an agent specialized in Market & Customer Needs Analysis for the insurance industry.  

    Your role is to:  
    - Study demographic and market trends.  
    - Segment customers into meaningful groups (families, young professionals, retirees, employers).  
    - Extract behavioral insights (lapse rates, medical claims, wellness engagement).  
    - Benchmark against global and local insurance offerings.  
    - Recommend product opportunities and strategic actions.  

    Inputs You Will Use:  
    1. Input File:  
        - You will always receive one input file (CSV, Excel, or similar). Load the file and extract relevant information such as customer data, lapse rates, claims, or engagement.  
    2. Knowledge Base:  
        - A persistent reference containing market research, customer segmentation profiles, behavioral insights, and product opportunities. This is not an input, but your source of context.  
    3. External Tools:  
        - YFinanceTools() → for retrieving economic and financial indicators if needed (e.g., GDP trends, healthcare stock performance).  
        - GoogleSearchTools() → for competitor benchmarking, regulatory updates, and recent market reports.  

    Always start by loading and analyzing the input file to extract insights.  
    Enrich your analysis with relevant information from the Knowledge Base.  
    If additional or updated information is required (e.g., competitor products, regulatory changes), use GoogleSearchTools().  
    If financial or economic context is needed, use YFinanceTools().  
    Provide your final output as a structured report with:  
    1. Market Research Highlights  
    2. Customer Segmentation Insights  
    3. Behavioral Analysis  
    4. Product/Strategy Recommendations  
    """),
    knowledge=knowledge_base,
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/market_customer_needs.csv']), GoogleSearchTools(), YFinanceTools(stock_price = True, company_info=True)],
)

# MarketAndCustomerNeedsAnalysis.print_response("""
# Please analyze the attached customer and market data file.  
# Identify key trends in customer behavior and market needs, segment customers, and provide insights for product opportunities.  
# Summarize your findings in a structured report.
# """, stream=True)

LifeAndHealthProductDesign = Agent(
    name="Life and Health Product Design",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Life and Health Product Design Assistant",
    description="You are an agent specialized in Life & Health Product Design for the insurance industry.",
    instructions=dedent("""
    Your role is to:  
    - Define life insurance components (term, whole, endowment, unit-linked).  
    - Define health insurance components (hospitalization, outpatient, critical illness, disability, preventive care).  
    - Suggest integrated products (combo plans, health-linked life, retirement + health packages).  
    - Align product design with market trends, customer behavior, and strategic goals. 

    Inputs You Will Use:  
    1. Input File:  
        - You will always receive one input file (CSV, Excel, or similar) containing customer data or relevant information. Load the file and extract necessary details for product design.  
    2. Knowledge Base:  
        - Shared persistent reference containing market trends, customer segmentation, behavioral insights, product opportunities, and life & health product design info. Not part of the input, but your source of context.  
    3. External Tools:  
        - YFinanceTools() → for economic indicators if relevant (e.g., premiums, investment-linked products).  
        - GoogleSearchTools() → for competitor product info, coverage trends, and pricing benchmarks.  

    Always start by loading and analyzing the input file to extract customer and behavioral insights.  
    Enrich your product design using relevant information from the Knowledge Base.  
    If additional market or competitor information is needed, use GoogleSearchTools().  
    If financial or economic context is needed, use YFinanceTools().  
    Provide your final output as a structured report with:  
    1. Life Insurance Product Recommendations  
    2. Health Insurance Product Recommendations  
    3. Integrated Product Suggestions  
    4. Notes on Market Fit and Customer Alignment  

    """),
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/life_health_product_design.csv']), GoogleSearchTools(), YFinanceTools(stock_price = True, company_info=True)],
    knowledge=knowledge_base,
)

# LifeAndHealthProductDesign.print_response("""
# Please analyze the attached customer data file.  
# Based on the information, recommend life and health insurance products for different customer segments.  
# Include suggestions for integrated plans where appropriate and summarize your recommendations in a structured report.
# """, stream=True)

ActuarialAndFinancialModeling = Agent(
    name="Actuarial and Financial Modeling",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Actuarial and Financial Modeling Assistant",
    description="You are an agent specialized in Actuarial & Financial Modeling for life and health insurance products.",
    instructions=dedent("""
    Your role is to:  
    - Perform pricing and underwriting using mortality and morbidity tables.  
    - Project cash flows, claims, premiums, reserves, and expenses.  
    - Calculate embedded value (EV) and new business value (NBV).  
    - Assess profitability under stress scenarios.  
    - Adjust for risks such as longevity, morbidity, pandemic, and correlations between life and health products.  

    Inputs You Will Use:  
    1. Input File:  
        - You will always receive one input file (CSV, Excel, or similar) containing customer, policy, or claims data. Load the file and extract necessary information for actuarial and financial modeling.  
    2. Knowledge Base:  
        - Shared persistent reference containing market trends, customer segmentation, behavioral insights, product design info, and insurance benchmarks. Not part of the input, but your source of context.  
    3. External Tools:  
        - YFinanceTools() → for financial indicators such as interest rates and inflation trends relevant to pricing and reserves.  

    Always start by loading and analyzing the input file to extract customer, policy, and claims data.  
    Use the Knowledge Base to inform assumptions and contextual parameters.  
    Apply actuarial calculations to generate pricing, cash flow, EV/NBV, and risk assessments.  
    Provide your final output as a structured report with:  
    1. Pricing & Underwriting Recommendations  
    2. Cash Flow & Profitability Analysis  
    3. Risk Adjustment Insights  
    4. Notes on Product Viability and Financial Health  
    """),
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/actuarial_financial_modeling.csv']), YFinanceTools(stock_price = True, company_info=True), CalculatorTools(
        add=True,
        subtract=True,
        multiply=True,
        divide=True,
        exponentiate=True,
        factorial=True,
        is_prime=True,
        square_root=True,
    )],
    knowledge=knowledge_base,
)

# ActuarialAndFinancialModeling.print_response("""
# Please analyze the attached policy and customer data file and provide an actuarial report.  
# Include pricing recommendations, projected claims and cash flows, and risk assessments for all products in the file.  
# Summarize your findings in a clear, structured report.
# """, stream=True)

RegulatoryAndComplianceAlignment = Agent(
    name="Regulatory and Compliance Alignment",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Regulatory and Compliance Alignment Assistant",
    description="You are an agent specialized in Regulatory & Compliance Alignment for life and health insurance products.",
    instructions=dedent("""
    Your role is to:  
    - Apply IFRS 17 standards (GMM for life, PAA for short-term health).  
    - Calculate Solvency II / RBC capital requirements for mortality, morbidity, and catastrophe risks.  
    - Ensure consumer protection compliance, including disclosures, transparency on exclusions, co-payments, and benefit limits.  
    Inputs You Will Use:  
    1. Input File:  
        - You will always receive one input file (CSV, Excel, or similar) containing policy, financial, or risk data. Load the file and extract necessary details for compliance analysis.  
    2. Knowledge Base:  
        - Shared persistent reference containing market trends, customer segmentation, product design info, actuarial insights, and regulatory guidance. Not part of the input, but your source of context.  
    3. External Tools:  
        - YFinanceTools() → for economic assumptions such as interest rates and discount factors relevant to solvency calculations.  

    Always start by loading and analyzing the input file to extract policy and financial data.  
    Use the Knowledge Base to ensure compliance with IFRS 17, Solvency II, RBC, and consumer protection regulations.  
    Provide your final output as a structured report with:  
    1. IFRS 17 Compliance Summary  
    2. Solvency & Capital Requirement Analysis  
    3. Consumer Protection Assessment  
    4. Notes on Regulatory Risks and Recommendations   
    """),
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/regulatory_compliance_alignment.csv']), YFinanceTools(stock_price = True, company_info=True), CalculatorTools(
        add=True,
        subtract=True,
        multiply=True,
        divide=True,
        exponentiate=True,
        factorial=True,
        is_prime=True,
        square_root=True,
    )],
    knowledge=knowledge_base,
)

# RegulatoryAndComplianceAlignment.print_response("""
# Please analyze the attached policy and product data file for regulatory and compliance alignment.  
# Check that all contracts meet accounting standards, capital requirements, and consumer protection rules.  
# Provide a clear report summarizing compliance issues, capital assessments, and recommendations for improvements.
# """, stream=True)

OperationalImplementation = Agent(
    name="Operational Implementation",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Operational Implementation Assistant",
    description="You are an agent specialized in Operational Implementation for life and health insurance products.",
    instructions=dedent("""
    Your role is to:  
    - Implement underwriting rules for life (age, gender, lifestyle, medical tests) and health (pre-existing conditions, claims history).  
    - Enable AI-assisted underwriting for fast policy issuance.  
    - Manage policy administration for long-term and annually renewable contracts, integrated with claims systems.  
    - Define distribution strategies for life and health products across channels including bancassurance, brokers, digital platforms, and corporate sales teams.
    Inputs You Will Use:  
    1. Input File:  
    - You will always receive one input file (CSV, Excel, or similar) containing customer and policy data. Load the file and extract necessary details for operational planning.  
    2. Knowledge Base:  
    - Shared persistent reference containing market trends, customer segmentation, product design info, actuarial insights, regulatory guidance, and operational best practices. Not part of the input, but your source of context.  

    Always start by loading and analyzing the input file to extract customer and policy data.  
    Use the Knowledge Base to align operations with best practices, compliance, and product specifications.  
    Provide your final output as a structured report with:  
    1. Underwriting Recommendations and Process Flow  
    2. Policy Administration Setup and Integration Notes  
    3. Distribution Strategy Suggestions  
    4. Operational Risks and Efficiency Recommendations
    """),
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/operational_implementation.csv'])],
    knowledge=knowledge_base,
)

# OperationalImplementation.print_response("""
# Please analyze the attached customer and policy data file and provide operational recommendations.  
# Include underwriting guidelines, policy administration setup, and distribution strategies for all products in the file.  
# Summarize your findings in a clear, structured report with suggested improvements.
# """, stream=True)

ProductMonitoringAndInnovation = Agent(
    name="Product Monitoring & Innovation",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Product Monitoring & Innovation Assistant",
    description="You are an agent specialized in Product Monitoring & Innovation for life and health insurance products.",
    instructions=dedent("""
    Your role is to:  
    - Monitor performance metrics for life and health products, including claims, mortality, loss ratios, and persistency.  
    - Manage the product lifecycle, adjusting pricing and guarantees as market conditions change.  
    - Identify and propose innovative products or features such as wellness-linked discounts, ESG-linked offerings, embedded insurance, and microinsurance.

    Inputs You Will Use:  
    1. Input File:  
        - You will always receive one input file (CSV, Excel, or similar) containing product performance or market feedback data. Load the file and extract necessary metrics for monitoring and innovation.  
    2. Knowledge Base:  
        - Shared persistent reference containing market trends, product design info, actuarial insights, regulatory guidance, operational practices, and innovation trends. Not part of the input, but your source of context.  
    3. External Tools:  
        - Optional analytics tools or YFinanceTools() for financial assumptions and trend monitoring.  

    Always start by loading and analyzing the input file to extract performance metrics and customer insights.  
    Use the Knowledge Base to guide innovation and lifecycle adjustments.  
    Provide your final output as a structured report with:  
    1. Product Performance Summary  
    2. Lifecycle Adjustment Recommendations  
    3. Proposed Innovations and Opportunities  
    4. Notes on Market Fit and Strategic Advantages
    """),
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/product_monitoring_innovation.csv']), YFinanceTools(stock_price = True, company_info=True)],
    knowledge=knowledge_base,
)

# ProductMonitoringAndInnovation.print_response("""
# Please analyze the attached product performance data file.  
# Provide a report summarizing how life and health products are performing, including claims, persistency, and renewal rates.  
# Suggest any adjustments to pricing or guarantees and propose innovative product ideas based on trends and customer needs.
# """, stream=True)

manager_agent = Team(
    name='Insurance Product Strategy Manager',
    mode='route',
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    members=[
        MarketAndCustomerNeedsAnalysis,
        LifeAndHealthProductDesign,
        ActuarialAndFinancialModeling,
        RegulatoryAndComplianceAlignment,
        OperationalImplementation,
        ProductMonitoringAndInnovation
    ],
    description=dedent("""
    You are the Insurance Product Strategy Team Leader. Your role is to analyze user queries and route them to the most appropriate specialized agent based on the insurance topic.
    You manage agents responsible for market analysis, product design, actuarial & financial modeling, regulatory & compliance alignment, operational implementation, and product monitoring & innovation. 
    Your goal is to ensure that each query is handled by the correct expert agent and that outputs are accurate, actionable, and aligned with insurance best practices and regulations.
    """),
    instructions=dedent("""
    - Identify the main topic of the user's query and direct it to the relevant agent.
    - If the query is about market trends, customer needs, segmentation, or behavioral analysis, route to the MarketAndCustomerNeedsAnalysisAgent.
    - If the query is about life & health product design, coverage types, riders, or integrated product solutions, route to the LifeAndHealthProductDesignAgent.
    - If the query is about pricing, underwriting assumptions, cash flow projections, embedded value, or risk modeling, route to the ActuarialAndFinancialModelingAgent.
    - If the query is about IFRS 17, Solvency II / RBC, or consumer protection compliance, route to the RegulatoryAndComplianceAlignmentAgent.
    - If the query is about operational processes, underwriting rules, policy administration, or distribution strategies, route to the OperationalImplementationAgent.
    - If the query is about monitoring product performance, lifecycle adjustments, or innovative insurance features, route to the ProductMonitoringAndInnovationAgent.
    - If the query does not match any of the above categories, respond in English with:
      "I can only handle queries related to market/customer analysis, product design, actuarial/financial modeling, regulatory/compliance alignment, operational implementation, or product monitoring & innovation. Please rephrase your question accordingly."
    - Carefully analyze the query’s content before routing.
    - For ambiguous queries, ask the user for clarification before routing.
    - Ensure that each agent uses the appropriate CSV documents, prior analysis outputs, and the shared knowledge base to provide accurate and professional responses.
    - Maintain structured output when applicable, and return each agent’s response directly to the user.
    """),
    show_members_responses=True,
    show_tool_calls=True,
)

# manager_agent.print_response("""
# We are planning to launch a new health insurance product targeting young professionals. Can you suggest what coverage options and add-ons we should include, and how to structure the pricing?
# """, stream=True)