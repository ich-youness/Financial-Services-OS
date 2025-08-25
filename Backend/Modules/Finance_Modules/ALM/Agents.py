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

load_dotenv()

import pandas as pd

# --- LCR Calculation ---
def calculate_lcr(high_quality_liquid_assets: float, total_net_cash_outflows: float) -> float:
    """
    Liquidity Coverage Ratio (LCR)
    LCR = High Quality Liquid Assets / Total Net Cash Outflows
    """
    if total_net_cash_outflows == 0:
        return float('inf')
    return high_quality_liquid_assets / total_net_cash_outflows * 100

# --- NSFR Calculation ---
def calculate_nsfr(stable_funding_available: float, required_stable_funding: float) -> float:
    """
    Net Stable Funding Ratio (NSFR)
    NSFR = Available Stable Funding / Required Stable Funding
    """
    if required_stable_funding == 0:
        return float('inf')
    return stable_funding_available / required_stable_funding * 100

# --- Liquidity Gap Analysis ---
def calculate_liquidity_gaps(balance_sheet: pd.DataFrame, time_buckets: list) -> pd.DataFrame:
    """
    Calculates cumulative liquidity gaps across different time buckets
    balance_sheet: DataFrame with columns ['Category','Amount','Maturity']
    time_buckets: list of days defining the time buckets, e.g., [0,30,90,180,360,730]
    Returns: DataFrame with liquidity gap per bucket
    """
    gaps = []
    for i in range(len(time_buckets)-1):
        start, end = time_buckets[i], time_buckets[i+1]
        inflows = balance_sheet[(balance_sheet['Category']=='Assets') & 
                                (balance_sheet['Maturity']>=start) & 
                                (balance_sheet['Maturity']<end)]['Amount'].sum()
        outflows = balance_sheet[(balance_sheet['Category']=='Liabilities') & 
                                 (balance_sheet['Maturity']>=start) & 
                                 (balance_sheet['Maturity']<end)]['Amount'].sum()
        gap = inflows - outflows
        gaps.append({'Bucket': f'{start}-{end} days', 'Liquidity Gap': gap})
    return pd.DataFrame(gaps)

# --- EVE Sensitivity ---
def calculate_eve_sensitivity(asset_cf: pd.DataFrame, liability_cf: pd.DataFrame, delta_rate: float) -> float:
    """
    Calculates the change in Economic Value of Equity (EVE) due to interest rate shock
    asset_cf & liability_cf: DataFrames with ['Maturity','Amount','Rate']
    delta_rate: shock in decimal (e.g., 0.01 for +100bps)
    """
    asset_change = (asset_cf['Amount'] * delta_rate * asset_cf['Maturity']/365).sum()
    liability_change = (liability_cf['Amount'] * delta_rate * liability_cf['Maturity']/365).sum()
    eve_change = asset_change - liability_change
    return eve_change

# --- NII Sensitivity ---
def calculate_nii_sensitivity(asset_cf: pd.DataFrame, liability_cf: pd.DataFrame, delta_rate: float) -> float:
    """
    Calculates the change in Net Interest Income (NII) for the next year
    asset_cf & liability_cf: DataFrames with ['Amount','Rate']
    delta_rate: shock in decimal (e.g., 0.01 for +100bps)
    """
    asset_impact = (asset_cf['Amount'] * (asset_cf['Rate'] + delta_rate)).sum()
    liability_impact = (liability_cf['Amount'] * (liability_cf['Rate'] + delta_rate)).sum()
    nii_change = asset_impact - liability_impact
    return nii_change

# Assessing Liquidity and Interest Rate Risks
Liquidity_Interest_Rate_Risk_Assessor = Agent(
    name="Liquidity Interest Rate Risk Assessor",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    show_tool_calls=True,
    tools=[
        calculate_nii_sensitivity,
        calculate_eve_sensitivity,
        calculate_liquidity_gaps,
    ],
    description="""
    The Liquidity & Interest Rate Risk Assessor is responsible for evaluating the institution’s liquidity 
    position and interest rate risk exposure. It monitors short-term and long-term liquidity, identifies 
    gaps in cash flow maturities, and measures sensitivity of the balance sheet to interest rate shocks. 
    The agent produces actionable insights and metrics such as LCR, NSFR, liquidity gaps, EVE, and NII changes 
    under different scenarios.
    """,
    instructions="""
    Step 1: Liquidity Gap Analysis
    - Input: Balance sheet data with Assets and Liabilities, including amount and maturity.
    - Tool: calculate_liquidity_gaps
    - Action: Compute liquidity gaps across defined time buckets to identify potential shortfalls.

    Step 2: Interest Rate Risk - EVE Sensitivity
    - Input: Asset and liability cash flow data including Amount, Rate, and Maturity.
    - Tool: calculate_eve_sensitivity
    - Action: Apply interest rate shock scenarios to compute the change in Economic Value of Equity (EVE).

    Step 3: Interest Rate Risk - NII Sensitivity
    - Input: Asset and liability cash flow data including Amount and Rate.
    - Tool: calculate_nii_sensitivity
    - Action: Apply interest rate shock scenarios to calculate projected changes in Net Interest Income (NII) over the next period.

    Step 4: Reporting & Recommendations
    - Input: Results from liquidity gaps, EVE, and NII calculations.
    - Action: Summarize findings, highlight vulnerabilities, and provide recommendations for liquidity management and interest rate risk mitigation.
    """
)
import json

# Balance Sheet
balance_sheet_json = json.dumps([
    {"Category": "Assets", "Amount": 500, "Maturity": 0},
    {"Category": "Assets", "Amount": 1200, "Maturity": 180},
    {"Category": "Liabilities", "Amount": 2500, "Maturity": 7},
    {"Category": "Liabilities", "Amount": 1800, "Maturity": 365}
], indent=4)

# Asset Cash Flows
asset_cf_json = json.dumps([
    {"Amount": 500, "Rate": 0.01, "Maturity": 30},
    {"Amount": 1200, "Rate": 0.025, "Maturity": 180}
], indent=4)

# Liability Cash Flows
liability_cf_json = json.dumps([
    {"Amount": 2500, "Rate": 0.002, "Maturity": 7},
    {"Amount": 1800, "Rate": 0.015, "Maturity": 365}
], indent=4)

# Interest Rate Shocks
rate_shocks_json = json.dumps([0.01, -0.01], indent=4)

# Time Buckets
time_buckets_json = json.dumps([0, 30, 180, 365], indent=4)



# Liquidity_Interest_Rate_Risk_Assessor.print_response(
#     f"""
# You are a Liquidity & Interest Rate Risk Assessor.

# Step 1: Liquidity Gap Analysis
# - Use the calculate_liquidity_gaps tool to compute liquidity gaps for the following balance sheet and time buckets:
# Balance Sheet: {balance_sheet_json}
# Time Buckets: {time_buckets_json}

# Step 2: Interest Rate Risk - EVE Sensitivity
# - Use calculate_eve_sensitivity tool to compute changes in EVE for each rate shock scenario:
# Asset Cash Flows: {asset_cf_json}
# Liability Cash Flows: {liability_cf_json}
# Rate Shocks: {rate_shocks_json}

# Step 3: Interest Rate Risk - NII Sensitivity
# - Use calculate_nii_sensitivity tool to compute changes in NII for each rate shock scenario using the same asset and liability cash flows.

# Step 4: Summarize the results
# - Highlight any liquidity gaps or interest rate vulnerabilities.
# - Provide recommendations for liquidity management and interest rate risk mitigation.
# """
# )


########### 2end agent ############

def simulate_contingency_funding(cash_flows: pd.DataFrame, liquidity_buffer: float, threshold: float = 0.1) -> dict:
    """
    Simulate funding gaps and check if contingency funding is needed.
    
    cash_flows: DataFrame with columns ['Date','Inflows','Outflows']
    liquidity_buffer: amount of pre-existing liquidity buffer
    threshold: fraction of short-term obligations triggering emergency funding
    
    Returns: dict with 'funding_gap' and 'trigger_contingency' boolean
    """
    cash_flows['Net'] = cash_flows['Inflows'] - cash_flows['Outflows']
    cumulative_net = cash_flows['Net'].cumsum() + liquidity_buffer
    min_balance = cumulative_net.min()
    
    trigger = min_balance < cash_flows['Outflows'].max() * threshold
    funding_gap = -min_balance if min_balance < 0 else 0
    
    return {
        'funding_gap': funding_gap,
        'trigger_contingency': trigger
    }

def optimize_balance_sheet(assets: pd.DataFrame, liabilities: pd.DataFrame, max_asset_share: float = 0.25) -> dict:
    """
    Suggest simple balance sheet adjustments to improve capital efficiency
    while remaining compliant.
    
    assets: DataFrame with columns ['AssetClass','Amount','Yield']
    liabilities: DataFrame with columns ['LiabilityClass','Amount','Cost']
    max_asset_share: maximum fraction of total assets for any single class
    
    Returns: dict with recommended allocations
    """
    total_assets = assets['Amount'].sum()
    recommended_assets = assets.copy()
    
    # Cap any asset class exceeding max share
    recommended_assets['AdjustedAmount'] = recommended_assets['Amount'].apply(
        lambda x: min(x, total_assets * max_asset_share)
    )
    
    # Suggest reallocating excess to highest yield compliant assets
    excess = total_assets - recommended_assets['AdjustedAmount'].sum()
    if excess > 0:
        high_yield_idx = recommended_assets['Yield'].idxmax()
        recommended_assets.loc[high_yield_idx, 'AdjustedAmount'] += excess
    
    # Suggest liability mix: prioritize low-cost term deposits
    recommended_liabilities = liabilities.copy()
    recommended_liabilities = recommended_liabilities.sort_values('Cost')
    
    return {
        'recommended_assets': recommended_assets.to_dict(orient='records'),
        'recommended_liabilities': recommended_liabilities.to_dict(orient='records')
    }

knowledge_base_Agent2 = MarkdownKnowledgeBase(
    path="Knowledge/Solvency_Capital_Strategist.md",
)

# Developing Strategies to Ensure Solvency
Solvency_Capital_Strategist = Agent(
    name="Solvency Capital Strategist",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        simulate_contingency_funding,
        optimize_balance_sheet,
    ],
    knowledge=knowledge_base_Agent2,
    description="""
    The Solvency & Capital Strategist agent is responsible for ensuring the institution maintains 
    adequate capital buffers and liquidity reserves to remain solvent under normal and stress conditions. 
    It leverages a knowledge base of regulatory rules, best practices, and contingency procedures, 
    alongside calculation tools to simulate funding gaps and optimize the asset-liability mix.
    """,
    instructions="""
    Step 1: Capital Adequacy Assessment
    - Input: Current balance sheet, capital levels, and optionally stress scenarios.
    - Knowledge: Reference the knowledge base for regulatory minimums and CET1/Tier1/Total Capital thresholds.
    - Action: Assess whether current capital levels meet regulatory requirements and advise if adjustments are needed.

    Step 2: Contingency Funding Simulation
    - Input: Short-term cash flow projections and existing liquidity buffers.
    - Tool: simulate_contingency_funding
    - Knowledge: Reference contingency funding rules for triggers and emergency measures.
    - Action: Identify potential funding gaps and determine whether contingency measures should be activated.

    Step 3: Balance Sheet Optimization
    - Input: Current asset and liability mix, yields, and funding costs.
    - Tool: optimize_balance_sheet
    - Knowledge: Reference rules on asset allocation limits, liability management, and regulatory compliance.
    - Action: Recommend adjustments to improve capital efficiency, reduce funding costs, and remain compliant.

    Step 4: Reporting & Recommendations
    - Input: Results from the simulations and optimizations.
    - Action: Summarize findings, highlight vulnerabilities, and provide actionable recommendations for capital management, funding strategy, and balance sheet adjustments.
    """
)
import json

# Balance Sheet
balance_sheet_json = json.dumps([
    {"Category": "Assets", "Amount": 500},
    {"Category": "Assets", "Amount": 1200},
    {"Category": "Liabilities", "Amount": 2500},
    {"Category": "Liabilities", "Amount": 1800}
], indent=4)

# Capital Levels
capital_json = json.dumps({
    "CET1": 200,
    "Tier1": 250,
    "TotalCapital": 300
}, indent=4)

# Short-term Cash Flows
cash_flows_json = json.dumps([
    {"Date": "2025-08-20", "Inflows": 300, "Outflows": 250},
    {"Date": "2025-08-21", "Inflows": 150, "Outflows": 400},
    {"Date": "2025-08-22", "Inflows": 100, "Outflows": 350}
], indent=4)

# Asset Mix
assets_json = json.dumps([
    {"AssetClass": "GovSec", "Amount": 500, "Yield": 0.02},
    {"AssetClass": "CorpLoan", "Amount": 1200, "Yield": 0.04},
    {"AssetClass": "Cash", "Amount": 500, "Yield": 0.0}
], indent=4)

# Liability Mix
liabilities_json = json.dumps([
    {"LiabilityClass": "DemandDep", "Amount": 2500, "Cost": 0.002},
    {"LiabilityClass": "TermDep", "Amount": 1800, "Cost": 0.015},
    {"LiabilityClass": "Wholesale", "Amount": 1000, "Cost": 0.028}
], indent=4)

# Solvency_Capital_Strategist.print_response(
    
#     f"""
# You are a Solvency & Capital Strategist agent.

# Step 1: Capital Adequacy Assessment
# - Use the knowledge base to check if current capital levels meet regulatory minimums.
# Balance Sheet: {balance_sheet_json}
# Capital Levels: {capital_json}

# Step 2: Contingency Funding Simulation
# - Use the simulate_contingency_funding tool to compute potential funding gaps and determine if contingency measures should be activated.
# Cash Flows: {cash_flows_json}
# Liquidity Buffer: 200

# Step 3: Balance Sheet Optimization
# - Use the optimize_balance_sheet tool to recommend adjustments to asset and liability mix for capital efficiency and regulatory compliance.
# Assets: {assets_json}
# Liabilities: {liabilities_json}

# Step 4: Summarize Results
# - Highlight any vulnerabilities in capital or funding.
# - Provide actionable recommendations for capital management, funding strategy, and balance sheet adjustments.
# """
# )

########## 3th agent #############
import pandas as pd

def optimize_yield(assets: pd.DataFrame, liquidity_buffer_pct: float = 0.10, max_asset_share: float = 0.25) -> dict:
    """
    Optimize asset allocation to maximize yield while maintaining liquidity and risk limits.
    
    assets: DataFrame with columns ['AssetClass','Amount','Yield']
    liquidity_buffer_pct: minimum fraction of total assets to keep liquid
    max_asset_share: maximum fraction of total assets per asset class
    
    Returns: dict with suggested allocation per asset class
    """
    total_assets = assets['Amount'].sum()
    min_liquid_amount = total_assets * liquidity_buffer_pct
    
    # Ensure liquid buffer (assume Cash or equivalent)
    if 'Cash' in assets['AssetClass'].values:
        assets.loc[assets['AssetClass']=='Cash', 'AdjustedAmount'] = max(
            assets.loc[assets['AssetClass']=='Cash', 'Amount'].iloc[0], min_liquid_amount
        )
    
    # Cap any asset class exceeding max share
    assets['AdjustedAmount'] = assets['Amount'].apply(lambda x: min(x, total_assets * max_asset_share))
    
    # Redistribute excess to highest yielding assets
    excess = total_assets - assets['AdjustedAmount'].sum()
    if excess > 0:
        high_yield_idx = assets['Yield'].idxmax()
        assets.loc[high_yield_idx, 'AdjustedAmount'] += excess
    
    return assets[['AssetClass','AdjustedAmount','Yield']].to_dict(orient='records')

def optimize_funding_cost(liabilities: pd.DataFrame, short_term_threshold: float = 0.15) -> dict:
    """
    Recommend adjustments to liability mix to reduce funding cost while staying within risk limits.
    
    liabilities: DataFrame with columns ['LiabilityClass','Amount','Cost']
    short_term_threshold: maximum fraction of short-term funding
    
    Returns: dict with recommended allocation per liability class
    """
    total_liabilities = liabilities['Amount'].sum()
    
    # Cap short-term liabilities if exceeding threshold
    short_term = ['Wholesale', 'ShortTerm']  # example short-term classes
    for cls in short_term:
        if cls in liabilities['LiabilityClass'].values:
            idx = liabilities[liabilities['LiabilityClass']==cls].index[0]
            max_allowed = total_liabilities * short_term_threshold
            liabilities.loc[idx, 'AdjustedAmount'] = min(liabilities.loc[idx, 'Amount'], max_allowed)
    
    # Redistribute remaining to lowest cost instruments
    remaining = total_liabilities - liabilities.get('AdjustedAmount', liabilities['Amount']).sum()
    if remaining > 0:
        low_cost_idx = liabilities['Cost'].idxmin()
        liabilities.loc[low_cost_idx, 'AdjustedAmount'] = liabilities.get('AdjustedAmount', liabilities['Amount']).iloc[low_cost_idx] + remaining
    
    return liabilities[['LiabilityClass','AdjustedAmount','Cost']].to_dict(orient='records')

def simulate_alm_investment(surplus_liquidity: float, investment_options: pd.DataFrame, risk_limit: float = 0.25) -> dict:
    """
    Allocate surplus liquidity across investment options while balancing return and risk.
    
    surplus_liquidity: available funds for investment
    investment_options: DataFrame with columns ['Instrument','Amount','Yield','Risk']
    risk_limit: maximum fraction of total liquidity in a single instrument
    
    Returns: dict with recommended investment allocation
    """
    total_liquidity = surplus_liquidity
    investment_options['Allocated'] = 0
    
    # Sort by highest yield
    sorted_options = investment_options.sort_values(by='Yield', ascending=False).copy()
    
    for idx, row in sorted_options.iterrows():
        max_alloc = min(row['Amount'], total_liquidity * risk_limit)
        investment_options.loc[idx, 'Allocated'] = max_alloc
        total_liquidity -= max_alloc
        if total_liquidity <= 0:
            break
    
    return investment_options[['Instrument','Allocated','Yield','Risk']].to_dict(orient='records')

knowledge_base_Agent3 = MarkdownKnowledgeBase(
    path="Knowledge/Profitability_Optimizer.md",
)

# Developing Strategies to Maximize Return on Assets
Profitability_Optimizer = Agent(
    name="Profitability Optimizer",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        optimize_yield,
        optimize_funding_cost,
    ],
    knowledge=knowledge_base_Agent3,
    description="""
    The Profitability Optimizer agent is designed to maximize the institution's return on assets 
    and minimize funding costs while staying compliant with regulatory and internal ALM rules. 
    It leverages a knowledge base containing best practices, risk limits, and ALM investment guidelines, 
    alongside calculation tools to optimize asset allocation and liability structure.
    """,
    instructions="""
    Step 1: Yield Optimization
    - Input: Current asset allocation with yields and amounts.
    - Knowledge: Reference the knowledge base for minimum liquidity buffer, maximum asset concentration, and risk-adjusted return rules.
    - Tool: optimize_yield
    - Action: Recommend adjusted asset allocations to maximize expected yield while maintaining liquidity and risk limits.

    Step 2: Funding Cost Reduction
    - Input: Current liability mix with funding costs.
    - Knowledge: Reference funding cost reduction rules and short-term funding concentration limits.
    - Tool: optimize_funding_cost
    - Action: Suggest adjustments to liability mix to reduce overall funding costs while remaining compliant and sufficiently liquid.

    Step 3: ALM Investment Simulation (optional, if surplus liquidity available)
    - Input: Surplus liquidity and potential investment options with yield and risk.
    - Knowledge: Reference ALM investment strategy rules for risk limits and regulatory constraints.
    - Tool: simulate_alm_investment
    - Action: Recommend investment allocations balancing return, liquidity, and risk compliance.

    Step 4: Reporting & Recommendations
    - Input: Results from the optimizations and simulations.
    - Action: Summarize recommended adjustments to assets, liabilities, and investments, highlighting potential profitability improvements while ensuring compliance and risk limits.
    """
)

import json

# Asset Allocation
assets_json = json.dumps([
    {"AssetClass": "GovSec", "Amount": 500, "Yield": 0.02},
    {"AssetClass": "CorpLoan", "Amount": 1200, "Yield": 0.04},
    {"AssetClass": "Cash", "Amount": 500, "Yield": 0.0}
], indent=4)

# Liability Mix
liabilities_json = json.dumps([
    {"LiabilityClass": "DemandDep", "Amount": 2500, "Cost": 0.002},
    {"LiabilityClass": "TermDep", "Amount": 1800, "Cost": 0.015},
    {"LiabilityClass": "Wholesale", "Amount": 1000, "Cost": 0.028}
], indent=4)

# Surplus Liquidity & Investment Options
investments_json = json.dumps([
    {"Instrument": "BondA", "Amount": 400, "Yield": 0.03, "Risk": 0.1},
    {"Instrument": "BondB", "Amount": 800, "Yield": 0.045, "Risk": 0.2},
    {"Instrument": "Repo", "Amount": 500, "Yield": 0.02, "Risk": 0.05}
], indent=4)


# Profitability_Optimizer.print_response(
    
#     f"""
# You are a Profitability Optimizer agent.

# Step 1: Yield Optimization
# - Use the knowledge base to ensure liquidity buffer and asset concentration rules are respected.
# Assets: {assets_json}

# Step 2: Funding Cost Reduction
# - Use the knowledge base to ensure short-term funding limits and cost optimization rules are respected.
# Liabilities: {liabilities_json}

# Step 3: ALM Investment Simulation
# - Use surplus liquidity to simulate investments, balancing yield and risk.
# Surplus Liquidity: 1000
# Investment Options: {investments_json}

# Step 4: Summarize Results
# - Provide recommended adjustments to assets and liabilities.
# - Suggest optimal investment allocations if surplus liquidity is available.
# - Highlight expected improvement in profitability and compliance with rules.
# """
# )


############# 4th agent #############

import pandas as pd

def project_liquidity(cash_flows: pd.DataFrame, off_balance_sheet: pd.DataFrame = None, stress_factor: float = 1.0) -> pd.DataFrame:
    """
    Projects liquidity positions over time, including off-balance-sheet items and optional stress adjustments.

    Parameters:
    - cash_flows: DataFrame with columns ['Date','Inflows','Outflows']
    - off_balance_sheet: DataFrame with columns ['Date','Commitments'] (optional)
    - stress_factor: Multiplier to simulate stressed outflows (>1 means more outflows)

    Returns:
    - DataFrame with projected liquidity and net positions
    """
    df = cash_flows.copy()
    df['NetCashFlow'] = df['Inflows'] - df['Outflows'] * stress_factor

    if off_balance_sheet is not None:
        df = df.merge(off_balance_sheet, on='Date', how='left')
        df['Commitments'] = df['Commitments'].fillna(0)
        df['NetCashFlow'] -= df['Commitments']

    df['CumulativeLiquidity'] = df['NetCashFlow'].cumsum()
    df['LiquidityGap'] = df['CumulativeLiquidity'].apply(lambda x: min(x, 0))  # Negative gaps only

    return df[['Date', 'Inflows', 'Outflows', 'NetCashFlow', 'CumulativeLiquidity', 'LiquidityGap']]

def calculate_interest_rate_sensitivity(portfolio: pd.DataFrame, rate_shifts: list) -> pd.DataFrame:
    """
    Calculates sensitivity of Net Interest Income (NII) and Economic Value of Equity (EVE) to interest rate changes.

    Parameters:
    - portfolio: DataFrame with columns ['Instrument','Type','Amount','Rate','Duration']
                 Type: 'Asset' or 'Liability'
    - rate_shifts: list of interest rate changes (in decimals, e.g., 0.01 for +1%)

    Returns:
    - DataFrame with sensitivity of NII and EVE for each rate shift
    """
    results = []
    for shift in rate_shifts:
        portfolio_shifted = portfolio.copy()
        portfolio_shifted['ShiftedRate'] = portfolio_shifted['Rate'] + shift
        portfolio_shifted['NII_Impact'] = portfolio_shifted.apply(
            lambda x: x['Amount'] * (x['ShiftedRate'] - x['Rate']) * (1 if x['Type']=='Asset' else -1),
            axis=1
        )
        portfolio_shifted['EVE_Impact'] = portfolio_shifted.apply(
            lambda x: x['Amount'] * x['Duration'] * (x['ShiftedRate'] - x['Rate']) * (1 if x['Type']=='Asset' else -1),
            axis=1
        )

        results.append({
            'RateShift': shift,
            'TotalNIIImpact': portfolio_shifted['NII_Impact'].sum(),
            'TotalEVEImpact': portfolio_shifted['EVE_Impact'].sum()
        })

    return pd.DataFrame(results)

knowledge_base_Agent4 = MarkdownKnowledgeBase(
    path="Knowledge/Risk_Model_Builder.md",
)

# Creation of Risk Models
Risk_Model_Builder = Agent(
    name="Risk Model Builder",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        project_liquidity,
        calculate_interest_rate_sensitivity,
    ],
    knowledge=knowledge_base_Agent4,
    description="""
    The Risk Model Builder agent is designed to create analytical tools for measuring and monitoring financial risks. 
    It focuses on liquidity projections and interest rate risk in the banking book (IRRBB). 
    The agent leverages a knowledge base containing modeling rules, regulatory guidelines, and stress testing best practices,
    alongside calculation tools to project liquidity gaps and calculate sensitivity of Net Interest Income (NII) and 
    Economic Value of Equity (EVE) under various interest rate scenarios.
    """,
    instructions="""
    Step 1: Liquidity Projection
    - Input: Cash inflows and outflows, optional off-balance-sheet commitments, and stress factors.
    - Knowledge: Reference the liquidity modeling rules from the knowledge base for minimum coverage ratios and gap limits.
    - Tool: project_liquidity
    - Action: Compute projected liquidity positions, cumulative liquidity, and identify potential liquidity gaps.

    Step 2: Interest Rate Sensitivity Analysis
    - Input: Portfolio of assets and liabilities with rates and durations, and list of interest rate shifts.
    - Knowledge: Reference interest rate modeling rules and IRRBB compliance guidance.
    - Tool: calculate_interest_rate_sensitivity
    - Action: Calculate sensitivity of NII and EVE to each interest rate shift and identify potential risks.

    Step 3: Reporting & Recommendations
    - Input: Results from liquidity projection and interest rate sensitivity analysis.
    - Action: Summarize key findings, highlight vulnerabilities in liquidity or interest rate exposure,
      and provide actionable recommendations for risk mitigation and balance sheet management.
    """
)

import json

# Cash flows
cash_flows_json = json.dumps([
    {"Date": "2025-08-20", "Inflows": 300, "Outflows": 250},
    {"Date": "2025-08-21", "Inflows": 150, "Outflows": 400},
    {"Date": "2025-08-22", "Inflows": 100, "Outflows": 350},
], indent=4)

# Off-balance-sheet commitments
off_balance_json = json.dumps([
    {"Date": "2025-08-20", "Commitments": 50},
    {"Date": "2025-08-21", "Commitments": 100},
    {"Date": "2025-08-22", "Commitments": 80},
], indent=4)

# Portfolio for interest rate sensitivity
portfolio_json = json.dumps([
    {"Instrument": "LoanA", "Type": "Asset", "Amount": 500, "Rate": 0.03, "Duration": 2},
    {"Instrument": "DepositB", "Type": "Liability", "Amount": 300, "Rate": 0.01, "Duration": 1},
    {"Instrument": "BondC", "Type": "Asset", "Amount": 400, "Rate": 0.025, "Duration": 3},
], indent=4)

# Rate shifts to test sensitivity (+1% and -1%)
rate_shifts_json = json.dumps([0.01, -0.01], indent=4)


# Risk_Model_Builder.print_response(
#     f"""
# You are a Risk Model Builder agent.

# Step 1: Liquidity Projection
# - Use the knowledge base to ensure minimum coverage ratios and gap limits are respected.
# Cash Flows: {cash_flows_json}
# Off-Balance-Sheet Commitments: {off_balance_json}
# Stress Factor: 1.2

# Step 2: Interest Rate Sensitivity Analysis
# - Use the knowledge base to follow IRRBB compliance rules.
# Portfolio: {portfolio_json}
# Rate Shifts: {rate_shifts_json}

# Step 3: Reporting & Recommendations
# - Summarize projected liquidity positions, identify liquidity gaps.
# - Provide NII and EVE sensitivity results.
# - Highlight any vulnerabilities and recommend mitigation actions.
# """
# )


#############3 5th agent ###########

import pandas as pd

def monitor_daily_liquidity(cash_positions: pd.DataFrame) -> pd.DataFrame:
    """
    Monitors daily liquidity positions and calculates key liquidity metrics.

    Parameters:
    - cash_positions: DataFrame with columns ['Date', 'Currency', 'Inflows', 'Outflows', 'StartingBalance']

    Returns:
    - DataFrame with calculated ending balances, net cash flow, and liquidity ratios
    """
    df = cash_positions.copy()
    df['NetCashFlow'] = df['Inflows'] - df['Outflows']
    df['EndingBalance'] = df['StartingBalance'] + df['NetCashFlow']
    df['LiquidityRatio'] = df['EndingBalance'] / (df['Outflows'].replace(0, 1))  # Avoid division by zero

    return df[['Date', 'Currency', 'StartingBalance', 'Inflows', 'Outflows', 'NetCashFlow', 'EndingBalance', 'LiquidityRatio']]

def simulate_funding_strategy(current_liquidity: float, funding_options: list) -> dict:
    """
    Simulates optimal funding allocation to meet liquidity needs at minimal cost.

    Parameters:
    - current_liquidity: Current cash position (float)
    - funding_options: List of dicts with keys:
        - 'Source': Funding source name
        - 'Available': Amount available
        - 'Cost': Interest rate or cost of funding

    Returns:
    - Dictionary with recommended funding allocation and total projected cost
    """
    funding_allocation = {}
    remaining_need = max(0, 0 - current_liquidity)  # Only fund if liquidity is negative
    total_cost = 0

    # Sort funding options by cost ascending
    sorted_options = sorted(funding_options, key=lambda x: x['Cost'])

    for option in sorted_options:
        if remaining_need <= 0:
            break
        allocated = min(option['Available'], remaining_need)
        funding_allocation[option['Source']] = allocated
        total_cost += allocated * option['Cost']
        remaining_need -= allocated

    return {
        'FundingAllocation': funding_allocation,
        'TotalCost': total_cost,
        'UnfundedAmount': remaining_need if remaining_need > 0 else 0
    }

Knowledge_base_Agent5 = MarkdownKnowledgeBase(
    path="Knowledge/Liquidity_Operations_Manager.md"
)
#Liquidity Operations Manager
Liquidity_Operations_Manager = Agent(
    name="Liquidity Operations Manager",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        monitor_daily_liquidity,
        simulate_funding_strategy,
    ],
    knowledge=Knowledge_base_Agent5,    
    description="""
    The Liquidity Operations Manager agent oversees daily liquidity management, funding strategy execution,
    and activation of contingency measures during stress events. It leverages a knowledge base containing
    rules, best practices, and regulatory guidelines, alongside calculation tools to monitor cash positions
    and simulate optimal funding allocations. The agent ensures liquidity adequacy, minimizes funding costs,
    and supports operational and regulatory compliance.
    """,
    instructions="""
    Step 1: Daily Liquidity Monitoring
    - Input: Daily inflows, outflows, starting balances, and currency allocations.
    - Knowledge: Reference daily liquidity operation rules for coverage ratios and reporting standards.
    - Tool: monitor_daily_liquidity
    - Action: Calculate net cash flow, ending balances, and liquidity ratios. Identify potential shortfalls.

    Step 2: Funding Strategy Simulation
    - Input: Current liquidity position and available funding options with costs.
    - Knowledge: Reference funding strategy execution rules to maintain diversification and cost efficiency.
    - Tool: simulate_funding_strategy
    - Action: Allocate funding optimally to cover liquidity needs at minimal cost. Highlight any unfunded shortfalls.

    Step 3: Reporting & Recommendations
    - Input: Results from liquidity monitoring and funding simulation.
    - Action: Summarize liquidity positions, funding allocations, and gaps. Recommend actions to senior management.
    - Reference contingency activation rules if stress thresholds are breached.
    """
)

import json

# Daily cash positions
cash_positions_json = json.dumps([
    {"Date": "2025-08-20", "Currency": "USD", "StartingBalance": 500, "Inflows": 300, "Outflows": 450},
    {"Date": "2025-08-21", "Currency": "USD", "StartingBalance": 350, "Inflows": 150, "Outflows": 400},
    {"Date": "2025-08-22", "Currency": "USD", "StartingBalance": 100, "Inflows": 200, "Outflows": 250},
], indent=4)

# Funding options
funding_options_json = json.dumps([
    {"Source": "ShortTermLoan", "Available": 500, "Cost": 0.02},
    {"Source": "TermDeposit", "Available": 300, "Cost": 0.015},
    {"Source": "CentralBank", "Available": 1000, "Cost": 0.025},
], indent=4)

# Liquidity_Operations_Manager.print_response(
#     f"""
# You are a Liquidity Operations Manager agent.

# Step 1: Daily Liquidity Monitoring
# - Use the knowledge base to ensure coverage ratios and reporting standards are respected.
# Daily Cash Positions: {cash_positions_json}

# Step 2: Funding Strategy Simulation
# - Use the knowledge base to maintain diversification and minimize funding cost.
# Current Liquidity Position: -150  # Negative balance indicates a shortfall
# Available Funding Options: {funding_options_json}

# Step 3: Reporting & Recommendations
# - Summarize ending balances, net cash flows, and liquidity ratios.
# - Provide optimal funding allocation and total projected funding cost.
# - Highlight any unfunded shortfalls and recommend actions.
# """
# )


##########333 6th agent #########

Knowledge_base_Agent6= MarkdownKnowledgeBase(
    path="Knowledge/Treasury_ALM_Risk_Controller.md",
)

import pandas as pd

def calculate_fx_counterparty_risk(cash_positions: pd.DataFrame, fx_rates: dict, counterparty_limits: dict) -> pd.DataFrame:
    """
    Calculates FX exposure and counterparty risk for treasury operations.

    Parameters:
    - cash_positions: DataFrame with columns ['Date', 'Currency', 'Counterparty', 'Amount']
    - fx_rates: Dictionary with currency codes as keys and FX rate to base currency as values
    - counterparty_limits: Dictionary with counterparty names as keys and maximum allowed exposure as values

    Returns:
    - DataFrame with calculated exposures, FX-adjusted amounts, and limit breaches
    """
    df = cash_positions.copy()
    df['FX_Amount'] = df.apply(lambda x: x['Amount'] * fx_rates.get(x['Currency'], 1), axis=1)
    df['Limit'] = df['Counterparty'].apply(lambda c: counterparty_limits.get(c, float('inf')))
    df['LimitBreach'] = df['FX_Amount'] > df['Limit']
    return df[['Date', 'Currency', 'Counterparty', 'Amount', 'FX_Amount', 'Limit', 'LimitBreach']]

def calculate_alm_metrics(balance_sheet: pd.DataFrame, interest_rates: dict) -> dict:
    """
    Calculates key ALM metrics including liquidity ratios, interest rate gaps, and capital adequacy.

    Parameters:
    - balance_sheet: DataFrame with columns ['Type','Amount','Maturity','Currency'] where Type = 'Asset' or 'Liability'
    - interest_rates: Dictionary with currency as key and current interest rate as value

    Returns:
    - Dictionary containing:
        - TotalAssets
        - TotalLiabilities
        - LiquidityRatio
        - InterestRateGap (Assets - Liabilities weighted by interest rate)
        - CapitalAdequacyRatio (simple approximation)
    """
    total_assets = balance_sheet[balance_sheet['Type']=='Asset']['Amount'].sum()
    total_liabilities = balance_sheet[balance_sheet['Type']=='Liability']['Amount'].sum()
    liquidity_ratio = total_assets / max(total_liabilities,1)  # Avoid division by zero

    # Interest rate gap
    def weighted_ir(row):
        rate = interest_rates.get(row['Currency'], 0)
        return row['Amount'] * rate * (1 if row['Type']=='Asset' else -1)
    
    interest_rate_gap = balance_sheet.apply(weighted_ir, axis=1).sum()
    
    # Simple capital adequacy approximation
    capital = total_assets - total_liabilities
    capital_adequacy_ratio = capital / max(total_assets,1)

    return {
        'TotalAssets': total_assets,
        'TotalLiabilities': total_liabilities,
        'LiquidityRatio': liquidity_ratio,
        'InterestRateGap': interest_rate_gap,
        'CapitalAdequacyRatio': capital_adequacy_ratio
    }


# Treasury and ALM Risk Management
Treasury_ALM_Risk_Controller = Agent(
    name="Treasury ALM Risk Controller",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        calculate_fx_counterparty_risk,
        calculate_alm_metrics,
    ],
    knowledge=Knowledge_base_Agent6, 
    description="""
    The Treasury & ALM Risk Controller agent oversees treasury operations and asset-liability management (ALM) 
    to maintain financial stability. It leverages a knowledge base containing rules, best practices, and 
    regulatory guidelines, alongside calculation tools to assess FX and counterparty risks, and compute key 
    ALM metrics. The agent ensures compliance with ALM policy, manages interest rate and liquidity gaps, 
    and provides actionable insights for maintaining financial equilibrium.
    """,
    instructions="""
    Step 1: FX & Counterparty Risk Assessment
    - Input: Cash positions with currency and counterparty information, FX rates, and counterparty limits.
    - Knowledge: Reference treasury risk oversight rules for limits and compliance.
    - Tool: calculate_fx_counterparty_risk
    - Action: Calculate FX-adjusted exposure for each counterparty, detect limit breaches, and highlight risk concentrations.

    Step 2: ALM Metrics Calculation
    - Input: Balance sheet data (assets, liabilities, maturities, currencies) and interest rates.
    - Knowledge: Reference ALM policy & compliance rules to validate risk exposure and reporting standards.
    - Tool: calculate_alm_metrics
    - Action: Compute total assets, total liabilities, liquidity ratio, interest rate gap, and capital adequacy ratio.

    Step 3: Reporting & Recommendations
    - Input: Results from risk assessment and ALM metrics.
    - Action: Summarize exposures, key ALM metrics, and any breaches of policy or limits.
    - Provide recommendations to maintain financial equilibrium and compliance with ALM policy.
    """
)

import json

# Sample cash positions for FX & counterparty risk
cash_positions_json = json.dumps([
    {"Date": "2025-08-20", "Currency": "USD", "Counterparty": "BankA", "Amount": 500},
    {"Date": "2025-08-20", "Currency": "EUR", "Counterparty": "BankB", "Amount": 400},
    {"Date": "2025-08-21", "Currency": "USD", "Counterparty": "BankC", "Amount": 300},
], indent=4)

# FX rates and counterparty limits
fx_rates_json = json.dumps({"USD": 1, "EUR": 1.1}, indent=4)
counterparty_limits_json = json.dumps({"BankA": 450, "BankB": 500, "BankC": 350}, indent=4)

# Balance sheet data for ALM metrics
balance_sheet_json = json.dumps([
    {"Type": "Asset", "Amount": 1000, "Maturity": 1, "Currency": "USD"},
    {"Type": "Liability", "Amount": 600, "Maturity": 1, "Currency": "USD"},
    {"Type": "Asset", "Amount": 500, "Maturity": 2, "Currency": "EUR"},
    {"Type": "Liability", "Amount": 400, "Maturity": 2, "Currency": "EUR"},
], indent=4)

interest_rates_json = json.dumps({"USD": 0.02, "EUR": 0.01}, indent=4)


# Treasury_ALM_Risk_Controller.print_response(
#     f"""
# You are a Treasury & ALM Risk Controller agent.

# Step 1: FX & Counterparty Risk Assessment
# - Use the knowledge base to ensure counterparty limits and compliance standards are respected.
# Cash Positions: {cash_positions_json}
# FX Rates: {fx_rates_json}
# Counterparty Limits: {counterparty_limits_json}

# Step 2: ALM Metrics Calculation
# - Use the knowledge base to validate balance sheet adjustments, interest rate exposure, and liquidity ratios.
# Balance Sheet: {balance_sheet_json}
# Interest Rates: {interest_rates_json}

# Step 3: Reporting & Recommendations
# - Summarize FX exposures, counterparty limit breaches, and key ALM metrics (liquidity ratio, interest rate gap, capital adequacy ratio).
# - Provide actionable recommendations to maintain financial equilibrium and ALM compliance.
# """
# )


# Add this to your existing code after defining all your agents

# Create the Treasury Risk Management Team with route mode
almTeam = Team(
    name="ALM Team",
    mode="route",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    members=[
        Liquidity_Interest_Rate_Risk_Assessor,
        Solvency_Capital_Strategist,
        Profitability_Optimizer,
        Risk_Model_Builder,
        Liquidity_Operations_Manager,
        Treasury_ALM_Risk_Controller
    ],
    show_tool_calls=True,
    markdown=True,
    instructions=[
        "You are a Treasury Risk Management Team Leader that routes queries to the most appropriate specialist agent.",
        "Analyze each user query to determine which team member has the right expertise to handle it.",
        "",
        "Team Members and Their Specializations:",
        "1. Liquidity Interest Rate Risk Assessor - Evaluates liquidity position, interest rate risk exposure, LCR, NSFR, liquidity gaps, EVE, and NII sensitivity",
        "2. Solvency Capital Strategist - Ensures capital adequacy, contingency funding, balance sheet optimization for regulatory compliance",
        "3. Profitability Optimizer - Maximizes return on assets, minimizes funding costs, optimizes asset allocation and liability structure",
        "4. Risk Model Builder - Creates analytical tools for liquidity projections and interest rate risk (IRRBB) modeling",
        "5. Liquidity Operations Manager - Oversees daily liquidity management, funding strategy execution, and contingency measures",
        "6. Treasury ALM Risk Controller - Manages treasury operations, FX/counterparty risk, and ALM metrics for financial stability",
        "",
        "Routing Guidelines:",
        "- Liquidity ratios, LCR, NSFR, interest rate gaps, EVE/NII sensitivity → Liquidity Interest Rate Risk Assessor",
        "- Capital adequacy, regulatory compliance, contingency funding, balance sheet optimization → Solvency Capital Strategist",
        "- Yield optimization, funding cost reduction, asset-liability mix optimization → Profitability Optimizer",
        "- Risk modeling, liquidity projections, IRRBB analysis, stress testing → Risk Model Builder",
        "- Daily liquidity monitoring, funding strategy, operational cash management → Liquidity Operations Manager",
        "- FX exposure, counterparty risk, ALM metrics, treasury risk oversight → Treasury ALM Risk Controller",
        "",
        "If a query spans multiple areas, route to the most relevant specialist based on the primary focus.",
        "Always provide clear reasoning for your routing decision when appropriate."
    ],
    show_members_responses=True,
)

# Example usage (you can uncomment these to test):
# almTeam.print_response(
#     "Calculate our liquidity coverage ratio and net stable funding ratio given current balance sheet",
#     stream=True
# )

# almTeam.print_response(
#     "Analyze interest rate sensitivity of our portfolio for +100bps and -100bps shocks",
#     stream=True
# )

# almTeam.print_response(
#     "Optimize our asset allocation to maximize yield while maintaining regulatory liquidity buffers",
#     stream=True
# )

# almTeam.print_response(
#     "Project our liquidity position over the next 30 days including off-balance sheet commitments",
#     stream=True
# )

# almTeam.print_response(
#     "Monitor daily cash positions and recommend funding strategy for current liquidity shortfall",
#     stream=True
# )

# almTeam.print_response(
#     "Assess FX exposure and counterparty risk across our treasury operations",
#     stream=True
# )


# Cash flows
cash_flows_json = json.dumps([
    {"Date": "2025-08-20", "Inflows": 300, "Outflows": 250},
    {"Date": "2025-08-21", "Inflows": 150, "Outflows": 400},
    {"Date": "2025-08-22", "Inflows": 100, "Outflows": 350},
], indent=4)

# Off-balance-sheet commitments
off_balance_json = json.dumps([
    {"Date": "2025-08-20", "Commitments": 50},
    {"Date": "2025-08-21", "Commitments": 100},
    {"Date": "2025-08-22", "Commitments": 80},
], indent=4)

# Portfolio for interest rate sensitivity
portfolio_json = json.dumps([
    {"Instrument": "LoanA", "Type": "Asset", "Amount": 500, "Rate": 0.03, "Duration": 2},
    {"Instrument": "DepositB", "Type": "Liability", "Amount": 300, "Rate": 0.01, "Duration": 1},
    {"Instrument": "BondC", "Type": "Asset", "Amount": 400, "Rate": 0.025, "Duration": 3},
], indent=4)

# Rate shifts to test sensitivity (+1% and -1%)
rate_shifts_json = json.dumps([0.01, -0.01], indent=4)


# almTeam.print_response(
#     f"""
# You are a Risk Model Builder agent.

# Step 1: Liquidity Projection
# - Use the knowledge base to ensure minimum coverage ratios and gap limits are respected.
# Cash Flows: {cash_flows_json}
# Off-Balance-Sheet Commitments: {off_balance_json}
# Stress Factor: 1.2

# Step 2: Interest Rate Sensitivity Analysis
# - Use the knowledge base to follow IRRBB compliance rules.
# Portfolio: {portfolio_json}
# Rate Shifts: {rate_shifts_json}

# Step 3: Reporting & Recommendations
# - Summarize projected liquidity positions, identify liquidity gaps.
# - Provide NII and EVE sensitivity results.
# - Highlight any vulnerabilities and recommend mitigation actions.
# """
# )

