from agno.agent import Agent
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.models.mistral import MistralChat
from agno.tools.scrapegraph import ScrapeGraphTools
from agno.tools.file import FileTools
from agno.tools.exa import ExaTools
from agno.tools.reasoning import ReasoningTools
from agno.models.huggingface import HuggingFace
from agno.tools.yfinance import YFinanceTools
from agno.tools.calculator import CalculatorTools
from dotenv import load_dotenv
import os
from polygon import RESTClient
import numpy as np
import pandas as pd
from scipy.stats import norm
from agno.knowledge.markdown import MarkdownKnowledgeBase


# from huggingface_hub import login
# login(token="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")


load_dotenv()
id_gemini=os.getenv("id")
api_key_gemini=os.getenv("api_key_gemini_v2")
id_openai = os.getenv("id_openai")
api_key_openai = os.getenv("api_key_openai")
# print(api_key_openai)

def calculate_credit_score(
    late_payments: int,
    bankruptcy: bool,
    credit_utilization: float,  # %
    dti: float,                 # %
    years_employed: int,
    collateral_value: float,
    loan_amount: float,
    savings_months: int
):
    """
    Credit score calculator with detailed breakdown.
    """
    score = 0
    breakdown = []

    # 1. Payment History (35%)
    if bankruptcy:
        ph_score = 0
        reason = "Bankruptcy present"
    elif late_payments == 0:
        ph_score = 350
        reason = "No late payments"
    elif late_payments <= 2:
        ph_score = 300
        reason = "1–2 late payments"
    elif late_payments <= 5:
        ph_score = 200
        reason = "3–5 late payments"
    else:
        ph_score = 100
        reason = "More than 5 late payments"
    score += ph_score
    breakdown.append(("Payment History (35%)", ph_score, reason))

    # 2. Credit Utilization (20%)
    if credit_utilization <= 30:
        cu_score = 200
        reason = "≤ 30% utilization"
    elif credit_utilization <= 50:
        cu_score = 150
        reason = "31–50% utilization"
    elif credit_utilization <= 75:
        cu_score = 100
        reason = "51–75% utilization"
    else:
        cu_score = 50
        reason = "> 75% utilization"
    score += cu_score
    breakdown.append(("Credit Utilization (20%)", cu_score, reason))

    # 3. Debt-to-Income Ratio (15%)
    if dti <= 20:
        dti_score = 150
        reason = "≤ 20% DTI"
    elif dti <= 35:
        dti_score = 120
        reason = "21–35% DTI"
    elif dti <= 50:
        dti_score = 80
        reason = "36–50% DTI"
    else:
        dti_score = 40
        reason = "> 50% DTI"
    score += dti_score
    breakdown.append(("Debt-to-Income (15%)", dti_score, reason))

    # 4. Employment Stability (10%)
    if years_employed >= 5:
        es_score = 100
        reason = "≥ 5 years employed"
    elif years_employed >= 3:
        es_score = 80
        reason = "3–4 years employed"
    elif years_employed >= 1:
        es_score = 60
        reason = "1–2 years employed"
    else:
        es_score = 40
        reason = "< 1 year employed"
    score += es_score
    breakdown.append(("Employment Stability (10%)", es_score, reason))

    # 5. Collateral Coverage Ratio (10%)
    coverage_ratio = collateral_value / loan_amount * 100
    if coverage_ratio >= 200:
        cc_score = 100
        reason = "≥ 200% coverage"
    elif coverage_ratio >= 150:
        cc_score = 80
        reason = "150–199% coverage"
    elif coverage_ratio >= 100:
        cc_score = 60
        reason = "100–149% coverage"
    else:
        cc_score = 40
        reason = "< 100% coverage"
    score += cc_score
    breakdown.append(("Collateral Coverage (10%)", cc_score, reason))

    # 6. Savings & Liquidity (10%)
    if savings_months >= 6:
        sl_score = 100
        reason = "≥ 6 months savings"
    elif savings_months >= 3:
        sl_score = 80
        reason = "3–5 months savings"
    elif savings_months >= 1:
        sl_score = 60
        reason = "1–2 months savings"
    else:
        sl_score = 40
        reason = "< 1 month savings"
    score += sl_score
    breakdown.append(("Savings & Liquidity (10%)", sl_score, reason))

    # Risk Tier & Decision
    if score >= 800:
        tier = "Low"
        decision = "Approve"
    elif score >= 650:
        tier = "Medium"
        decision = "Conditional Approve"
    else:
        tier = "High"
        decision = "Reject"

    return {
        "score": score,
        "risk_tier": tier,
        "decision": decision,
        "breakdown": breakdown
    }


knowledge_base = MarkdownKnowledgeBase(
    path="Knowledge/Rules_CreditAnalyzer.md",
    # vector_db=PgVector(
    #     table_name="markdown_documents",
    #     db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    # ),
)

CreditAnalyzerAgent = Agent(
    name="Credit Analyzer Agent",
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[calculate_credit_score],
    description="""
An AI-powered credit underwriting agent designed to assess the creditworthiness of individuals or businesses.
It evaluates applicant data such as credit reports, income, debt-to-income ratios, employment history, and collateral values.
The agent applies configured scoring models and decision thresholds to produce a credit score, assign a risk tier,
and provide an approve/reject/conditional recommendation with clear reason codes for regulatory compliance.
""",
    instructions="""
You are the CreditAnalyzerAgent, a specialized AI credit underwriting system.

## Role
Analyze applicant financial and behavioral data to determine their likelihood of repaying a loan or meeting credit obligations.

## Inputs
- Credit reports
- Income verification
- Debt-to-income ratios
- Employment history
- Collateral values
- Any additional relevant financial metrics

## Process
1. Validate and interpret the provided data.
2. Use the `calculate_credit_score` tool to compute the applicant's score, risk tier, and decision.
3. Provide clear reason codes and explanations for the decision, ensuring compliance with fair lending regulations.
4. Follow all rules and decision-making criteria from the knowledge base (`Rules_CreditAnalyzer.md`).

## Output Format
1. Respond in JSON:
{
  "score": <numeric_score>,
  "risk_tier": "<Low|Medium|High>",
  "decision": "<Approve|Conditional Approve|Reject>",
  "reasons": ["reason_1", "reason_2", ...],
  "recommendations": ["optional improvement tips"],
  "model_used": "<model_name>"
}

2. Always include a Markdown table showing the score breakdown from the calculate_credit_score output.


""",
    knowledge=knowledge_base,
    markdown=True,
    stream=True,
)
# CreditAnalyzerAgent.print_response("I'm a new graduate, i am 23 years old, i have 100$ as savings in my account, i wanna buy a car with a loan of 9k $, and i just strated working in a company as an ai engineer with a salary of 1k $ per month?",)
# CreditAnalyzerAgent.print_response("I'm an ai engineer, i am 25 years old, i have 3500$ as savings in my account, i wanna buy a car with a loan of 14k $, and i just strated working in a company as an ai engineer with a salary of 1.8k $ per month?",)

CreditAnalyzerAgent.print_response("""
Evaluate the creditworthiness of the following applicant:

Name: John Smith
Credit Report: 2 late payments in the last 24 months, credit utilization at 35%, no bankruptcies.
Income Verification: $78,000 annual salary.
Debt-to-Income Ratio: 28%
Employment History: 6 years at the same company, stable industry.
Collateral Value: $150,000 property against a $60,000 loan request.

""")

def get_historical_stock_data(self, ticker: str, from_date: str, to_date: str, timespan: str = "day", multiplier: int = 1) -> list:
        """
        Retrieve historical aggregate bars (OHLCV data) for a given stock ticker using Polygon.io API.

        Args:
        - ticker: The stock ticker symbol (e.g., "AAPL").
        - from_date: Start date in YYYY-MM-DD format.
        - to_date: End date in YYYY-MM-DD format.
        - timespan: The timespan for each bar (e.g., "minute", "hour", "day", "week", "month"). Default: "day".
        - multiplier: The size of the timespan multiplier (e.g., 1 for daily, 5 for 5-minute). Default: 1.

        Returns:
        A list of dictionaries, each containing:
        - timestamp: Unix timestamp (milliseconds)
        - open: Open price
        - high: High price
        - low: Low price
        - close: Close price
        - volume: Volume

        Note: This uses the free tier of Polygon.io, which has usage limits. For production, consider a paid subscription.
        If the data volume is large, it paginates automatically up to 50,000 results.
        """
        if not self.historical_prices:
            raise ValueError("Historical prices tool is not enabled.")
        
        client = RESTClient(api_key="dysGAAQXVwQzjjYg4e1ISIYS4g5c4q5L")
        aggs = []
        for a in client.list_aggs(
            ticker=ticker,
            multiplier=multiplier,
            timespan=timespan,
            from_=from_date,
            to=to_date,
            limit=50000  # Max limit to minimize API calls
        ):
            aggs.append({
                "timestamp": a.timestamp,
                "open": a.open,
                "high": a.high,
                "low": a.low,
                "close": a.close,
                "volume": a.volume,
            })
        return aggs

def calculate_historical_var(self, portfolio: dict, from_date: str, to_date: str, confidence: float = 0.99, timespan: str = "day") -> dict:
        """
        Calculate Historical Value at Risk (VaR) and Conditional VaR (CVaR) for a portfolio.

        Args:
        - portfolio: Dict of {ticker: value} e.g., {'TSLA': 80000, 'QQQ': 120000}
        - from_date: Start date YYYY-MM-DD
        - to_date: End date YYYY-MM-DD
        - confidence: Confidence level (0.99 for 99%)
        - timespan: 'day' or other

        Returns:
        {'var': value, 'cvar': value}
        """
        if not self.var_calc:
            raise ValueError("VaR calculation is not enabled.")

        total_value = sum(portfolio.values())
        weights = {t: v / total_value for t, v in portfolio.items()}
        
        # Fetch historical data for each ticker
        historical_returns = {}
        for ticker in portfolio:
            data = self.get_historical_stock_data(ticker, from_date, to_date, timespan)
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df['returns'] = df['close'].pct_change().dropna()
            historical_returns[ticker] = df['returns']

        # Align dates and compute portfolio returns
        returns_df = pd.DataFrame(historical_returns).dropna()
        portfolio_returns = (returns_df * pd.Series(weights)).sum(axis=1)
        
        # Historical VaR
        sorted_returns = np.sort(portfolio_returns)
        var_index = int((1 - confidence) * len(sorted_returns))
        var = -sorted_returns[var_index] * total_value
        
        # CVaR
        cvar_returns = sorted_returns[:var_index]
        cvar = -np.mean(cvar_returns) * total_value if len(cvar_returns) > 0 else var
        
        return {'var': var, 'cvar': cvar}

def monte_carlo_simulation(self, portfolio: dict, from_date: str, to_date: str, num_simulations: int = 10000, time_horizon: int = 1, confidence: float = 0.99, timespan: str = "day") -> dict:
        """
        Perform Monte Carlo simulation for portfolio VaR.

        Args:
        - portfolio: Dict of {ticker: value}
        - from_date, to_date: Dates
        - num_simulations: Number of simulations
        - time_horizon: Days ahead
        - confidence: For VaR
        - timespan: Data granularity

        Returns:
        {'var': value, 'simulated_losses': list of top losses}
        """
        if not self.monte_carlo:
            raise ValueError("Monte Carlo simulation is not enabled.")

        total_value = sum(portfolio.values())
        weights = np.array(list({t: v / total_value for t, v in portfolio.items()}.values()))
        
        # Fetch historical data
        historical_returns = {}
        for ticker in portfolio:
            data = self.get_historical_stock_data(ticker, from_date, to_date, timespan)
            df = pd.DataFrame(data)
            df['returns'] = df['close'].pct_change().dropna()
            historical_returns[ticker] = df['returns'].values

        returns_df = pd.DataFrame(historical_returns).dropna()
        
        mean_returns = returns_df.mean().values
        cov_matrix = returns_df.cov().values
        
        # Simulate
        sim_returns = np.random.multivariate_normal(mean_returns, cov_matrix, num_simulations)
        sim_port_returns = np.dot(sim_returns, weights) * time_horizon ** 0.5  # Scale for horizon if needed
        
        sim_values = total_value * (1 + sim_port_returns)
        sim_losses = total_value - sim_values
        
        var = np.percentile(sim_losses, confidence * 100)
        
        return {'var': var, 'simulated_losses': sim_losses.tolist()[:100]}  # Return sample

def correlation_matrix_analysis(self, tickers: list, from_date: str, to_date: str, timespan: str = "day") -> dict:
        """
        Compute correlation matrix for given tickers.

        Args:
        - tickers: List of tickers e.g., ['TSLA', 'QQQ']
        - from_date, to_date: Dates
        - timespan: Data granularity

        Returns:
        Dict of correlation matrix as {ticker1: {ticker2: corr, ...}, ...}
        """
        if not self.correlation:
            raise ValueError("Correlation analysis is not enabled.")

        historical_returns = {}
        for ticker in tickers:
            data = self.get_historical_stock_data(ticker, from_date, to_date, timespan)
            df = pd.DataFrame(data)
            df['returns'] = df['close'].pct_change().dropna()
            historical_returns[ticker] = df['returns']

        returns_df = pd.DataFrame(historical_returns).dropna()
        corr_matrix = returns_df.corr()
        
        return corr_matrix.to_dict()




MarketRiskBot = Agent(
    name="Market Risk agent",
   
    model=Gemini(id=id_gemini,api_key=api_key_gemini),
    # model=Gemini(id="gemini-2.0-flash-lite",api_key=api_key_gemini),
    # model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    tools=[
        # CustomMarketDataTool(api_key=os.getenv("MARKET_API_KEY")),  # Your live data fetcher
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, historical_prices=True, company_info=True, income_statements=True, key_financial_ratios=True, company_news=True),
        get_historical_stock_data,
        calculate_historical_var,
        monte_carlo_simulation,
        CalculatorTools(),
    ],
    
    
    description="""
    An AI-powered market risk analysis agent that monitors portfolio exposure,
    runs VaR and stress testing, and issues alerts when market conditions breach configured limits.
    """,
    instructions="""
    You are MarketRiskBot, a market risk analysis system.

    Inputs:
    - Market data feeds
    - Portfolio positions
    - Volatility indices
    - Correlation matrices
    - Stress scenarios

    Process:
    1. Fetch and validate market & portfolio data 
    2. Calculate Value at Risk (VaR) and Conditional VaR (CVaR)
    3. Run stress tests for historical and hypothetical scenarios 
    4. Identify concentration and correlation risks
    5. Compare metrics to configured risk limits .
    6. Output alerts and recommendations.

    Output in JSON format:
    {
      "portfolio_var": <value>,
      "cvar": <value>,
      "stress_test_results": [...],
      "alerts": [...],
      "recommendations": [...]
    }
    """,
    markdown=True,
    show_tool_calls=True,
    stream=True,
    reasoning=True,
)


# MarketRiskBot.print_response("""
# You are provided with the following simulated market and portfolio data:

# Portfolio Positions:
# - AAPL: 1,000 shares @ $180.50
# - MSFT: 800 shares @ $325.75
# - TSLA: 500 shares @ $245.20
# - SPY: 200 shares @ $450.00

# Market Data (last 30 days volatility - annualized %):
# - AAPL: 22%
# - MSFT: 18%
# - TSLA: 45%
# - SPY: 15%

# Correlation Matrix:
#            AAPL   MSFT   TSLA   SPY
# AAPL       1.00   0.85   0.65   0.80
# MSFT       0.85   1.00   0.60   0.75
# TSLA       0.65   0.60   1.00   0.55
# SPY        0.80   0.75   0.55   1.00

# Stress Scenario:
# - S&P 500 drops 10% in one week
# - Tech sector drops 15% in one week

# Risk Limits:
# - Max allowed daily VaR (99% confidence): $50,000
# - Max allowed single-stock exposure: 40% of portfolio value

# Tasks:
# 1. Calculate the current portfolio VaR (99% confidence, 1-day horizon).
# 2. Estimate losses under the provided stress scenario.
# 3. Identify any breaches of the risk limits.
# 4. Provide risk alerts and recommendations.

# NOTE: use the tools needed if you don't have the capacity to do it by yourself.
# """)

knowledge_base_Compliance = MarkdownKnowledgeBase(
    path="Knowledge/US_Compliance_Rules.md",
    # vector_db=PgVector(
    #     table_name="markdown_documents",
    #     db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    # ),
)
TransactionMonitoringAgent = Agent(
    name="Transaction Checker Agent",
    # model=Gemini(id=id_gemini, api_key=api_key_gemini),
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    # tools=[],
    description="""
An AI-powered compliance and anti–money laundering (AML) monitoring agent that analyzes transaction data, 
customer profiles, and jurisdiction-specific regulations to detect and flag potential compliance violations. 
The agent uses the internal compliance knowledge base to apply jurisdiction-specific rules, monitor for 
suspicious activity patterns, check against sanctions lists, and ensure adherence to reporting requirements. 
Designed to support KYC, AML, and CFT compliance while maintaining a detailed audit trail for regulatory review.
""",
    instructions="""
You are the TransactionMonitoringAgent, a compliance and AML specialist. 
You must **only** reference and apply compliance rules from the provided knowledge base (`knowledge_base_Compliance`). 
Do not search for rules outside this knowledge base.

## Process
1. Review incoming transaction data along with customer profiles and the applicable jurisdiction code.
2. Retrieve relevant compliance rules for the given jurisdiction **from the knowledge base**.
3. Apply these rules and violation thresholds to the transaction data.
4. Check against sanctions lists, politically exposed persons (PEPs), and high-risk jurisdictions as defined in the knowledge base.
5. Detect suspicious transaction patterns (e.g., structuring, layering, rapid movement of funds, unusually large transfers).
6. Classify detected issues by severity: Low, Medium, or High.
7. Generate a detailed compliance review.

## Output Format
Return results in the following JSON structure:
{
  "violations_detected": [
      {
        "rule_id": "<unique_rule_code_from_kb>",
        "description": "<rule_violation_description>",
        "severity": "<Low|Medium|High>"
      }
  ],
  "alerts": ["<short_alert_message>", ...],
  "compliance_status": "<Compliant|Non-Compliant>",
  "recommendations": ["<preventive_or_remedial_action>", ...],
  "audit_log_reference": "<unique_audit_reference_id>"
}

## Rules
- Only flag violations if they are supported by the rules in the knowledge base.
- If no violations are found, set `compliance_status` to "Compliant" and list any minor observations in `alerts`.
- Do not invent or assume rules that are not explicitly in the knowledge base.
- Use exact wording and severity guidance as stored in the knowledge base.
""",
    knowledge=knowledge_base_Compliance,
    markdown=True,
    stream=True,
)




# TransactionMonitoringAgent.print_response("""
# Evaluate the following transaction for compliance risks:

# Transaction ID: TX-982173
# Date: 2025-08-08
# Amount: $250,000
# Currency: USD
# Sender: GreenWave Imports LLC (Customer ID: C-45012)
# Sender Country: United States
# Receiver: SunBright Trading Co.
# Receiver Country: North Korea
# Payment Type: Wire Transfer
# Purpose: "Equipment purchase"

# Customer Profile:
# - Business type: Import/Export
# - Industry: Electronics
# - KYC Status: Verified
# - PEP Status: No
# - Transaction history: Mostly under $50,000, domestic and to low-risk jurisdictions

# Jurisdiction Requirements:
# - US regulations (OFAC sanctions apply)
# - Report all transactions over $10,000 to FinCEN within 24 hours

# Config:
# - Compliance ruleset: US AML + OFAC
# - Violation threshold: >$10,000 without due diligence
# - Alert severity mapping: Sanctioned country = High

# Please:
# 1. Check for violations of AML or sanctions rules.
# 2. Assign a compliance status.
# 3. List alerts and violations in JSON format.
# 4. Provide recommended next steps.
# 5. Include an audit log reference.
# """, stream=True)

# TransactionMonitoringAgent.print_response("""
# Evaluate the following transaction for compliance risks:

# Transaction ID: TX-983245
# Date: 2025-08-09
# Amount: $18,500
# Currency: USD
# Sender: BrightFuture Technologies Inc. (Customer ID: C-56123)
# Sender Country: United States
# Receiver: GreenLeaf Solutions LLC
# Receiver Country: Canada
# Payment Type: Wire Transfer
# Purpose: "Consulting services"

# Customer Profile:
# - Business type: Technology Services
# - Industry: IT Consulting
# - KYC Status: Verified
# - PEP Status: No
# - Transaction history: Multiple transactions under $20,000 to various low-risk countries

# Jurisdiction Requirements:
# - US regulations (OFAC sanctions apply)
# - Report transactions over $10,000 to FinCEN within 24 hours

# Config:
# - Compliance ruleset: US AML + OFAC
# - Violation threshold: >$10,000 requires reporting and due diligence
# - Alert severity mapping: Transactions over $10,000 = Medium

# Please:
# 1. Check for any AML or sanctions violations.
# 2. Assign a compliance status.
# 3. List any alerts or observations in JSON format.
# 4. Provide recommended next steps.
# 5. Include an audit log reference.
# """)



financial_router_team = Team(
    name="Financial Router Team",
    mode="route",
    # model=OpenAIChat("gpt-4o"),
    model=Gemini(id=id_gemini, api_key=api_key_gemini),
    members=[CreditAnalyzerAgent, MarketRiskBot, TransactionMonitoringAgent],
    show_tool_calls=True,
    markdown=True,
    description="You are a financial query router that directs questions to the appropriate specialized agent.",
    instructions=[
        "Identify the main topic of the user's query and direct it to the relevant agent.",
        "If the query is about credit scoring, loan approval, creditworthiness assessment, or related financial underwriting, route to CreditAnalyzerAgent.",
        "If the query is about market risk analysis, Value at Risk (VaR), portfolio stress testing, stock data, or related market monitoring, route to MarketRiskBot.",
        "If the query is about transaction compliance, AML checks, sanctions screening, or regulatory violations in transactions, route to TransactionMonitoringAgent.",
        "If the query does not match any of the above categories, respond in English with: 'I can only handle queries related to credit analysis, market risk, or transaction compliance. Please rephrase your question accordingly.'",
        "Always analyze the query's content before routing to an agent.",
        "For ambiguous queries, ask for clarification before routing.",
    ],
    show_members_responses=True,
)