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
from agno.embedder.mistral import MistralEmbedder
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.tools.googlesearch import GoogleSearchTools
from agno.knowledge.markdown import MarkdownKnowledgeBase

load_dotenv()

# Initializing Knowledge Base
knowledge_base = MarkdownKnowledgeBase(
    path="MarkdownKnowledge/company_data.md",
    # vector_db=PgVector(
    #     table_name="treasurer_knowledge",
    #     db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    #     embedder=MistralEmbedder(api_key=os.getenv('MISTRAL_API_KEY')),
    # ),
)
# knowledge_base.load(recreate=True)

CashFlowManagement = Agent(
    name="Cash Flow Management Agent",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="CashFlow Management Assistant",
    description="You are a Treasurer specialized in managing the company’s cash flow by monitoring current balances, forecasting future inflows/outflows, optimizing liquidity buffers, and identifying risks.",
    instructions=dedent("""
    1. **Data Ingestion**  
    - Read transaction history from CSV using `CsvTools()`.  
    - Consolidate inflows and outflows across all accounts.  
    - Validate balances against internal policies from the Knowledge Base.  

    2. **Cash Position Monitoring**  
    - Calculate current balances by account and currency.  
    - Generate a consolidated liquidity view across all banks.  
    - Flag discrepancies where balance variance exceeds company policy thresholds.  

    3. **Cash Flow Forecasting**  
    - Project inflows (customer payments, interest income) and outflows (payroll, loan repayments, supplier invoices) using the CSV data.  
    - Adjust forecasts for payment delays or revenue shifts.  
    - Retrieve market variables (interest rates, FX rates) via `yfinance` and integrate them into projections.  
    - Run scenario analysis: base case, optimistic, and stress test (e.g., delayed collections, higher FX volatility).  

    4. **Liquidity Buffer Optimization**  
    - Compare available liquidity to the Knowledge Base minimum buffer policy (e.g., 2 months payroll or $50,000).  
    - If surplus exists, suggest moving funds to short-term investment accounts.  
    - If a shortfall is projected, suggest credit line usage or delaying non-critical payments.  

    5. **Risk Management**  
    - Detect timing mismatches between receivables and payables.  
    - Use `yfinance` to check currency exposures; if monthly exposure exceeds thresholds, recommend hedging.  
    - Identify unusual transactions (non-recurring suppliers, large unexpected outflows) and flag them for fraud review.  

    6. **Knowledge Base Integration**  
    - Use the KB to ensure compliance with company rules (dual approval, supplier payment approval limits, escalation protocols).  
    - Provide explanations and reasoning to users based on financial best practices.  
    """),
    expected_output=dedent("""
    - Deliver a structured report including:  
        - Current liquidity position.  
        - Forecasted inflows and outflows.  
        - Buffer analysis (surplus/shortfall).  
        - Risk alerts (FX, timing mismatches, anomalies).  
        - Recommendations (invest idle cash, secure credit line, adjust payments).  
    """),
    knowledge=knowledge_base,
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/cashflow_transactions.csv']), YFinanceTools(historical_prices=True)],
    # debug_mode=True,
)

# CashFlowManagement.print_response("""
# Analyze the company’s current cash flow situation using the latest CSV file. 
# Give me a forecast for the next 30 days, including expected inflows and outflows. 
# Check if we are meeting the liquidity buffer requirements from our internal policies, 
# and highlight any risks such as timing mismatches, FX exposure, or unusual payments. 
# Finally, provide clear recommendations on what actions Treasury should take.
# """, stream=True)

OverseeingFinancing = Agent(
    name="Overseeing Financing Agent",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Overseeing Financing Assistant",
    description="You are an agent responsible for overseeing the company’s financing activities. You ensure that capital is available at optimal cost and structure to fund operations, investments, and growth.",
    instructions=dedent("""
    1. **Data Ingestion**
    - Read the company’s debt, credit, and equity schedule from the CSV using CsvTools().
    - Consolidate all financial instruments and validate data against internal policies from the Knowledge Base.

    2. **Capital Structure Management**
    - Calculate current leverage ratios and compare them with target thresholds (Debt/EBITDA, equity proportion).
    - Ensure the funding mix follows company policy (retained earnings → debt → equity issuance).

    3. **Debt Management**
    - Monitor principal, interest rates, maturities, and covenants for all debt instruments.
    - Check compliance with covenants and flag potential violations.
    - Evaluate refinancing opportunities by comparing current debt terms with market interest rates obtained via yfinance.
    - Advise on fixed vs. floating rate allocations based on market outlook.

    4. **Funding Strategy**
    - Assess available credit lines, commercial paper programs, and repo facilities.
    - Recommend funding options for specific projects or acquisitions, weighing public vs. private financing trade-offs.
    - Ensure liquidity coverage meets minimum operational needs.

    5. **Relationship Management**
    - Maintain regular communications with banks, credit rating agencies, and institutional investors.
    - Provide negotiation recommendations for borrowing terms and covenants.
    - Alert the CFO if any covenant breach, funding risk, or refinancing issue is detected.

    6. **Knowledge Base Integration**
    - Use the Knowledge Base to check internal policies regarding leverage limits, covenant rules, approval requirements, and escalation protocols.
    - Reference financial best practices to explain reasoning behind recommendations.
    """),
    expected_output=dedent("""
    - Provide a structured report including:
        - Current capital structure and leverage ratios.
        - Upcoming debt maturities and interest obligations.
        - Refinancing or funding recommendations.
        - Risk alerts (covenant breaches, market exposure, funding gaps).
        - Suggested actions for CFO and Treasury.
    """),
    knowledge=knowledge_base,
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/financing_schedule.csv']), YFinanceTools(historical_prices=True)],
    # debug_mode=True,
)

# OverseeingFinancing.print_response("""
# Analyze the company’s current financing situation using the latest financing schedule CSV. 
# Evaluate the capital structure, including debt, equity, and retained earnings, and check if we are within target leverage and credit metrics. 
# Review upcoming debt maturities, interest obligations, and covenants, and suggest any refinancing opportunities. 
# Assess funding options for planned projects, including credit lines, bonds, and equity issuance. 
# Highlight any risks such as covenant breaches, interest rate exposure, or liquidity gaps. 
# Finally, provide clear recommendations and action steps for the CFO and Treasury team.
# """, stream=True)

OverseeingInvestment = Agent(
    name="Overseeing Investment Agent",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    role="Overseeing Investment Assistant",
    description="You are an agent responsible for overseeing the company’s investment portfolio. You ensure that surplus cash is invested according to internal policies while safeguarding liquidity and capital.",
    instructions=dedent("""
    1. **Data Ingestion**
    - Read the company’s investment portfolio from the CSV using CsvTools().
    - Consolidate all instruments and validate data against the shared Knowledge Base for policy compliance.

    2. **Investment Policy Compliance**
    - Check that all instruments comply with approved asset classes, credit quality limits, and duration limits.
    - Evaluate counterparty risk for each investment.

    3. **Portfolio Allocation**
    - Allocate funds across operational liquidity, reserve liquidity, and strategic surplus according to internal guidelines.
    - Adjust allocations based on interest rate outlook, projected liquidity needs, and risk appetite.

    4. **Performance Monitoring**
    - Track portfolio returns vs. benchmarks (e.g., LIBOR, Treasury yield, corporate bond indices).
    - Monitor mark-to-market values and unrealized gains/losses.
    - Alert if losses exceed internal risk thresholds.

    5. **Regulatory & Accounting Compliance**
    - Ensure all investments follow IFRS/GAAP accounting standards.
    - Verify compliance with internal liquidity requirements (and Basel III/IV if applicable).

    6. **Knowledge Base Integration**
    - Reference the shared KB for all investment policies, liquidity rules, and risk thresholds.
    - Explain recommendations and reasoning using best practices from the KB.

    7. **External Data & Tools**
    - Use yfinance to retrieve current market yields, FX rates, and historical price trends.
    - CsvTools() is required to read the portfolio CSV.
    - A calculator or math tool is recommended for allocation, ratio, and yield calculations.
    - Web search is not needed.
    """),
    expected_output=dedent("""
    - Provide a structured report including:
        - Portfolio allocation by instrument type and liquidity bucket.
        - Policy compliance checks (asset class, credit, duration).
        - Performance vs. benchmarks.
        - Risk alerts (credit limits, liquidity gaps, mark-to-market losses).
        - Recommendations for reallocations, additional investments, or divestments.
    """),
    knowledge=knowledge_base,
    tools=[ReasoningTools(add_instructions=True), CsvTools(csvs=['Documents/investment_portfolio.csv']), YFinanceTools(historical_prices=True)],
    # debug_mode=True,
)

# OverseeingInvestment.print_response("""
# Analyze the company’s current investment portfolio using the latest investment portfolio CSV. 
# Check that all investments comply with internal policies regarding asset classes, credit quality, and duration limits. 
# Evaluate portfolio allocation across operational, reserve, and strategic liquidity buckets, and suggest adjustments based on interest rate outlook and projected cash needs. 
# Monitor performance against benchmarks and highlight any unrealized losses or risk exposures. 
# Finally, provide actionable recommendations for reallocations, new investments, or divestments to optimize yield while safeguarding liquidity.
# """, stream=True)

manager_agent = Team(
    name = 'Treasurer Manager',
    mode='route',
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API_KEY')),
    members=[CashFlowManagement, OverseeingFinancing, OverseeingInvestment],
    description='You are the Treasury & Finance Team Leader. Your role is to analyze user queries and route them to the most appropriate specialized agent based on the topic. You manage the CashFlow Management, Overseeing Financing, and Overseeing Investment agents. Your goal is to ensure that each query is handled by the correct expert agent and that outputs are accurate, compliant, and actionable.',
    instructions=dedent("""
    - Identify the main topic of the user's query and direct it to the relevant agent.
    - If the query is about cash flow monitoring, forecasting, liquidity buffer optimization, or cash flow risk management, route to the CashFlow Management agent.
    - If the query is about capital structure, debt management, funding strategy, or relationships with lenders and investors, route to the Overseeing Financing agent.
    - If the query is about treasury investment policy compliance, portfolio allocation, performance monitoring, or regulatory accounting integration, route to the Overseeing Investment agent.
    - If the query does not match any of the above categories, respond in English with:
    "I can only handle queries related to cash flow management, financing oversight, or treasury investments. Please rephrase your question accordingly."
    - Always carefully analyze the query’s content before routing.
    - For ambiguous queries, ask the user for clarification before routing.
    - Ensure that each agent uses the appropriate CSV documents, yfinance tools, and the shared knowledge base to provide accurate and professional outputs.
    - Maintain structured output when applicable, and ensure each agent’s response is returned directly to the user.
    """),
    show_members_responses=True,
    show_tool_calls=True,
    # debug_mode=True,
)

# manager_agent.print_response("""
# Can you analyze our upcoming debt maturities and suggest refinancing options to minimize interest costs? Also, please check if our current leverage ratio is within the target threshold and highlight any covenant risks.
# """, stream=True)