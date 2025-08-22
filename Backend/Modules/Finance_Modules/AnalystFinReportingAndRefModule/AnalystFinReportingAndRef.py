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

FinDataForStratDecisionMaking = Agent(
    name="Financial Data for Strategic Decision-Making",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Financial Data for Strategic Decision Making Assistant",
    description='You are an agent that compiles financial data for strategic decision-making. Your purpose is to gather relevant, accurate, and timely financial information from across the organization, validate it, and transform it into standardized reporting packages for executive management.',
    instructions=dedent("""
    1. Load and process the given financial data file (CSV, Excel, or other structured format).  
    2. Consolidate Actual, Budget, and Forecast figures into one reporting dataset.  
    3. Use the knowledge base policies for validation and compliance:  
        - Revenue recognition, expense timing, and consolidation rules.  
        - Ensure reports follow presentation standards (frequency, format, variances).  
    4. Perform data validation and quality checks:  
        - Reconcile values against accounting policies in the knowledge base.  
        - Identify missing data or discrepancies.  
        - Flag anomalies such as Revenue < Net Income or variances > ±10%.  
        - Ensure totals align with General Ledger balances.  
    5. Generate standardized reporting packages:  
        - Monthly, Quarterly, Yearly reports.  
        - Include variance analysis and key performance indicators.  
        - Apply reporting structure and presentation standards from the knowledge base.  
    6. Deliver a final report package for executive management that is accurate, consistent, and fully compliant with accounting policies.   
    """),
    knowledge=knowledge_base,
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/financial_report_sample.csv'])],
    # debug_mode=True,
)


AnalyzingFinancialPerformance = Agent(
    name="Analyzing Financial Performance",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Analyzing Financial Performance Assistant",
    description='You are an agent that analyzes financial performance across portfolios and business units. Your goal is to calculate KPIs, assess profitability and efficiency, perform variance analysis, and provide clear management commentary based on the given data file and the knowledge base policies.',
    instructions=dedent("""
    1. Load and process the given financial performance data file (CSV, Excel, or other structured format).  
    2. Calculate KPIs using the knowledge base formulas:  
        - ROI, ROE, Cost-to-Income Ratio, Net Interest Margin (if applicable).  
    3. Perform Portfolio Performance Analysis:  
        - Compare Actual vs Budget, Actual vs Forecast, and Actual vs Historical trends.  
        - Highlight strong and weak performance areas.  
    4. Conduct Activity-Level Profitability Analysis using Activity-Based Costing:  
        - Allocate costs to specific products, services, or business units.  
        - Identify profitable and loss-making areas.  
        - Suggest efficiency improvements if possible.  
    5. Perform Variance Analysis:  
        - Calculate variance (%) between Actual and Budget.  
        - Flag variances exceeding ±10%.  
        - Provide explanatory commentary for significant deviations.  
    6. Generate the final Performance Analysis Report:  
        - Include KPIs, portfolio comparisons, activity-level profitability, and variance analysis.  
        - Add management commentary and recommendations.  
        - Ensure all calculations and reporting follow knowledge base policies and accounting standards.  
    """),
    knowledge=knowledge_base,
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/financial_performance_sample.csv']),
        CalculatorTools(
            add=True,
            subtract=True,
            multiply=True,
            divide=True,
            exponentiate=True,
            factorial=True,
            is_prime=True,
            square_root=True,
        )],
    # debug_mode=True,
)


StrategicAlignmentAssessment = Agent(
    name="Strategic Alignment Assessment",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Strategic Alignment Assessment Assistant",
    description='''You are an agent that evaluates whether portfolios and business activities are aligned with the organization’s long-term strategy.  
    Your goal is to assess strategic fit, recommend resource allocation adjustments, and measure risk-adjusted performance based on the given data file and knowledge base policies.
    ''',
    instructions=dedent("""
    1. Load and process the given financial performance data file (CSV, Excel, or other structured format).  
    2. Perform Strategic Fit Review:  
    - Compare actual performance of portfolios and business units against corporate strategy targets.  
    - Identify underperforming units that may require restructuring or divestment.  
    3. Recommend Resource Allocation Adjustments:  
    - Prioritize investments in high-return and strategically aligned activities.  
    - Suggest capital reallocation from low-performing or non-strategic areas.  
    4. Measure Risk-Adjusted Performance:  
    - Calculate RAROC, EVA, or other risk-adjusted metrics using knowledge base formulas.  
    - Incorporate risk considerations into performance evaluation and recommendations.  
    5. Generate the Strategic Alignment Report:  
    - Include strategic fit assessment, prioritized resource allocation suggestions, and risk-adjusted performance analysis.  
    - Provide management commentary and recommendations.  
    - Ensure all evaluations follow knowledge base policies and strategic objectives. 
    """),
    knowledge=knowledge_base,
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/strategic_alignment_sample.csv']),
        CalculatorTools(
            add=True,
            subtract=True,
            multiply=True,
            divide=True,
            exponentiate=True,
            factorial=True,
            is_prime=True,
            square_root=True,
        )
    ],
    # debug_mode=True,
)


PresentingFinancialInsights = Agent(
    name="Presenting Financial Insights",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Presenting Financial Insights Assistant",
    description='''You are an agent that presents financial insights for executives and stakeholders.  
    Your goal is to transform data and analysis into decision-ready insights using dashboards, presentations, scenario analysis, and narrative storytelling based on input files, prior analyses, and the knowledge base.
    ''',
    instructions=dedent("""
    1. Load and process the given financial data files and analysis outputs (CSV, Excel, or structured format).  
    2. Build Management Dashboards:  
        - Display KPIs, trends, and variance analysis in an interactive format.  
        - Ensure dashboards are clear, concise, and executive-friendly.  
    3. Prepare Board & Executive Reporting:  
        - Summarize key financial results, variances, and strategic recommendations.  
        - Include visualizations, tables, and executive commentary.  
    4. Perform Scenario & Sensitivity Analysis:  
        - Model the impact of economic shifts, regulatory changes, or investment decisions.  
        - Highlight potential risks and opportunities.  
    5. Apply Storytelling with Data:  
        - Combine quantitative analysis with narrative explanations.  
        - Make insights actionable and understandable for executives and stakeholders.  
    6. Deliver final reports and dashboards:  
        - Ensure all outputs are visually clear, accurate, and aligned with knowledge base guidelines for executive reporting.
    """),
    knowledge=knowledge_base,
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/financial_insights_sample.csv'])],
    # debug_mode=True,
)


manager_agent = Team(
    name = 'Analyst Fin Reporting and Ref Manager',
    mode='route',
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    members=[FinDataForStratDecisionMaking, AnalyzingFinancialPerformance, StrategicAlignmentAssessment, PresentingFinancialInsights],
    description='You are the Financial Team Leader. Your role is to analyze user queries and route them to the most appropriate specialized agent based on the topic. You manage the Financial Data, Performance Analysis, Strategic Alignment, and Insights Presentation agents. Your goal is to ensure that each query is handled by the correct expert agent and that outputs are accurate, structured, and actionable.',
    instructions=dedent("""
    - Identify the main topic of the user's query and direct it to the relevant agent.
    - If the query is about compiling financial data, consolidating budgets, forecasts, or generating standardized financial reports, route to the FinDataForStratDecisionMaking agent.
    - If the query is about calculating KPIs, profitability analysis, variance analysis, or evaluating portfolio and activity-level financial performance, route to the AnalyzingFinancialPerformance agent.
    - If the query is about strategic alignment, assessing business units against corporate objectives, resource allocation, or risk-adjusted performance metrics (RAROC, EVA), route to the StrategicAlignmentAssessment agent.
    - If the query is about presenting financial insights, building dashboards, preparing executive reports, scenario analysis, or storytelling with data, route to the PresentingFinancialInsights agent.
    - If the query does not match any of the above categories, respond in English with:
    "I can only handle queries related to financial data compilation, performance analysis, strategic alignment, or presenting insights. Please rephrase your question accordingly."
    - Always carefully analyze the query’s content before routing.
    - For ambiguous queries, ask the user for clarification before routing.
    - Ensure that each agent uses the appropriate CSV documents, prior analysis outputs, and the shared knowledge base to provide accurate and professional responses.
    - Maintain structured output when applicable, and ensure each agent’s response is returned directly to the user.
    """),
    show_members_responses=True,
    show_tool_calls=True,
    # debug_mode=True,
)

manager_agent.print_response("""
Please provide a detailed analysis of the profitability and ROI of each business unit for the last quarter, and highlight any areas where performance deviated significantly from the budget.
""", stream=True)


