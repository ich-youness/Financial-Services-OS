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
import numpy as np
import pandas as pd
from agno.knowledge.markdown import MarkdownKnowledgeBase


load_dotenv()
id_gemini=os.getenv("id")
api_key_gemini=os.getenv("api_key_gemini_v2")
id_openai = os.getenv("id_openai")
api_key_openai = os.getenv("api_key_openai")

def RatioCalculatorTool(financial_data):
    """
    Compute key financial ratios from given financial statement data.
    Accepts dicts only (JSON-serializable), converts DataFrames if needed.
    """

    def df_to_dict(source):
        if isinstance(source, pd.DataFrame):
            return source.fillna(0).to_dict()
        return source or {}

    income_statement = df_to_dict(financial_data.get("income_statement"))
    balance_sheet = df_to_dict(financial_data.get("balance_sheet"))

    # Helper to extract values
    def get_value(source, key):
        try:
            return float(source.get(key, list(source.values())[0].get(key, 0)))
        except Exception:
            return None

    net_income = get_value(income_statement, "Net Income")
    total_revenue = get_value(income_statement, "Total Revenue")
    total_assets = get_value(balance_sheet, "Total Assets")
    total_equity = get_value(balance_sheet, "Total Stockholder Equity")
    current_assets = get_value(balance_sheet, "Total Current Assets")
    current_liabilities = get_value(balance_sheet, "Total Current Liabilities")
    total_liabilities = get_value(balance_sheet, "Total Liabilities")

    ratios = {
        "Profitability": {
            "Net Profit Margin (%)": (net_income / total_revenue * 100) if net_income and total_revenue else None,
            "Return on Assets (%)": (net_income / total_assets * 100) if net_income and total_assets else None,
            "Return on Equity (%)": (net_income / total_equity * 100) if net_income and total_equity else None,
        },
        "Liquidity": {
            "Current Ratio": (current_assets / current_liabilities) if current_assets and current_liabilities else None,
            "Quick Ratio": ((current_assets - get_value(balance_sheet, "Inventory")) / current_liabilities) if current_assets and current_liabilities else None,
        },
        "Solvency": {
            "Debt-to-Equity": (total_liabilities / total_equity) if total_liabilities and total_equity else None,
            "Equity Ratio (%)": (total_equity / total_assets * 100) if total_equity and total_assets else None,
        }
    }

    return ratios

# --- Agent ---
Financial_Performance_Analyst = Agent(
    name="Financial Performance Analyst",
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API')),
    # model = Gemini(id=id_gemini,api_key=api_key_gemini,),
    stream=True,
    # show_tool_calls=True,
    tools=[
        YFinanceTools(),
        RatioCalculatorTool,
        
    ],
    reasoning=True,
    description="""
    A financial analysis agent specialized in evaluating an organization's financial health.
    It reviews financial statements, compares results to benchmarks, and identifies strengths,
    weaknesses, risks, and opportunities.
    """,
    instructions="""
    1. Fetch financial data using YFinanceTools.
    2. Compute key ratios using RatioCalculatorTool.
    4. Produce a well structered markdown output: Summary, Detailed Analysis, Recommendations.
    """
)

# --- Test prompt ---
# Financial_Performance_Analyst.print_response("""
# Please perform a full financial performance analysis for Apple Inc. (ticker: 'AAPL').
# Fetch the latest financial statements, compute profitability, liquidity, and solvency ratios,

# """, stream=True)

def BudgetingTool(actuals, planned_budget=None):
    """
    Create or compare budget plans based on actuals.

    Parameters:
        actuals (dict): Historical financial data, e.g.,
            {"Revenue": 100000, "COGS": 40000, "Expenses": 20000}
        planned_budget (dict, optional): Existing budget to compare against

    Returns:
        dict: Budget plan and variance analysis
    """
    budget_plan = planned_budget or {}
    variance_analysis = {}

    # Simple approach: create a new budget as a % increase over actuals
    for key, value in actuals.items():
        if key not in budget_plan:
            budget_plan[key] = value * 1.05  # assume 5% growth if no budget provided
        variance_analysis[key] = budget_plan[key] - value

    return {
        "budget_plan": {k: round(v, 2) for k, v in budget_plan.items()},
        "variance_analysis": {k: round(v, 2) for k, v in variance_analysis.items()}
    }

def CashFlowForecastingTool(cash_inflows, cash_outflows, periods=12):
    """
    Forecast monthly cash flows based on inflows and outflows.

    Parameters:
        cash_inflows (list or np.array): historical inflows
        cash_outflows (list or np.array): historical outflows
        periods (int): number of future periods to forecast

    Returns:
        dict: projected cash flow per period and cumulative cash
    """
    import numpy as np

    # Simple linear projection using average historical inflows/outflows
    avg_inflow = np.mean(cash_inflows)
    avg_outflow = np.mean(cash_outflows)

    projected_cash_flow = []
    cumulative_cash = 0
    for i in range(periods):
        net = avg_inflow - avg_outflow
        cumulative_cash += net
        projected_cash_flow.append({
            "period": i + 1,
            "net_cash_flow": round(net, 2),
            "cumulative_cash": round(cumulative_cash, 2)
        })

    return projected_cash_flow
def CostOptimizationTool(expenses, threshold=0.1):
    """
    Analyze expenses and suggest optimization opportunities.

    Parameters:
        expenses (dict): category-wise expense data, e.g.,
            {"Salaries": 50000, "Marketing": 10000, "IT": 8000}
        threshold (float): fraction of total expense considered reducible

    Returns:
        dict: suggested cost reductions
    """
    total_expense = sum(expenses.values())
    optimization_suggestions = {}

    for category, amount in expenses.items():
        reducible = amount * threshold
        optimization_suggestions[category] = round(reducible, 2)

    return {
        "total_expense": total_expense,
        "optimization_suggestions": optimization_suggestions
    }

Budget_Forecast_Manager = Agent(
    name="Budget Forecast Manager",
    # model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API')),
    stream=True,
    show_tool_calls=True,
    tools=[
        # YFinanceTools(),
        BudgetingTool,
        CashFlowForecastingTool,
        CostOptimizationTool
    ],
    reasoning=True,
    description="""
    The Budget & Forecast Manager is a financial planning agent focused on creating, analyzing,
    and optimizing budgets and cash flow forecasts. It evaluates historical financial data,
    projects future cash inflows and outflows, and identifies cost optimization opportunities.
    The agent is designed to help organizations plan budgets, maintain liquidity, and
    make strategic financial decisions using both historical and real-time financial data.
    """,
    instructions="""
    1. **Purpose**:
       - Prepare and manage budgets based on historical actuals or planned targets.
       - Forecast future cash flows to ensure sufficient liquidity.
       - Identify cost optimization opportunities to improve efficiency and profitability.
       - Provide actionable recommendations for financial planning and cost control.

    2. **Data Handling**:
       - Validate all input data (historical actuals, existing budgets, cash inflows/outflows, expenses).
       - If any data is missing, clearly mark the gaps and proceed with partial analysis.

    3. **Analysis Tasks**:
       - Use **BudgetingTool** to create or update budgets, calculate variances, and compare against actuals.
       - Use **CashFlowForecastingTool** to project future cash flows for the defined periods.
       - Use **CostOptimizationTool** to analyze expenses and suggest areas for cost reduction.
       - Optionally, use **YFinanceTools** to retrieve relevant financial data for benchmarking or planning.

    4. **Output Format**:
       - **Budget Plan:** Detailed budget by category with variance analysis.
       - **Cash Flow Forecast:** Monthly or quarterly projections with cumulative cash.
       - **Cost Optimization Report:** Suggested reductions and impact on total expenses.
       - **Recommendations:** Practical actions to improve budget adherence and liquidity.
       - Use clear headers, tables, and bullet points for readability.

    5. **Tool Usage Workflow**:
       Step 1 — If historical financial data is available, prepare it in a clean JSON/dict format.
       Step 2 — Use BudgetingTool to generate or compare budget plans and analyze variances.
       Step 3 — Use CashFlowForecastingTool to project cash flows over the forecast horizon.
       Step 4 — Use CostOptimizationTool to suggest expense reductions and efficiency improvements.
       Step 5 — Integrate results into a structured financial plan with actionable recommendations.

    6. **Tone & Style**:
       - Professional, concise, and data-driven.
       - Avoid unnecessary jargon; explain technical terms simply if needed.
       - Focus on providing clear financial insights and actionable steps.

    7. **Limitations**:
       - Do not make speculative assumptions beyond the available data.
       - Clearly indicate any insights derived from incomplete or estimated inputs.
    """
)

# Budget_Forecast_Manager.print_response("""
# You are asked to create a financial plan for the company "Tech Solutions Inc." using the following historical data:

# 1. Historical actuals for last year (in USD):
#    - Revenue: 1,200,000
#    - COGS: 480,000
#    - Operating Expenses: 300,000
#    - Salaries: 250,000
#    - Marketing: 50,000
#    - IT Expenses: 30,000

# 2. Historical monthly cash inflows (last 12 months): 
#    [100000, 110000, 120000, 95000, 105000, 115000, 125000, 100000, 110000, 120000, 130000, 140000]

# 3. Historical monthly cash outflows (last 12 months): 
#    [90000, 95000, 100000, 85000, 95000, 100000, 105000, 90000, 95000, 100000, 110000, 115000]

# Tasks:

# 1. Generate a **budget plan** for the next year, including variances from last year’s actuals.
# 2. Forecast **monthly cash flows** for the next 12 months, showing cumulative cash.
# 3. Analyze expenses using **Cost Optimization**, and suggest areas to reduce costs by 10%.
# 4. Provide a **structured output** with the following sections:
#    - Budget Plan and Variance Analysis
#    - Cash Flow Forecast
#    - Cost Optimization Report
#    - Recommendations for financial planning and cost control

# Use clear headers, bullet points, and round all monetary values to two decimals. Highlight any assumptions made.
# """,stream=True)

Reporting_Dashboard_Developer = Agent(
    name="Reporting Dashboard Developer",
    # model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    # model=Gemini(id="gemini-2.5-flash", api_key=api_key_gemini),
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API')),
    stream=True,
    show_tool_calls=True,
    reasoning=True,
    tools=[YFinanceTools(), FileTools(), ExaTools(),],
    description="""
    A presentation-focused agent specialized in transforming raw financial analyses and insights
    into professional, visually appealing, and well-structured HTML reports or dashboards.
    Designed for executives, stakeholders, and decision-makers who require clean,
    modern, and responsive layouts for web-based or PDF-ready reports.
    """,
instructions="""
You are a financial reporting agent that generates structured HTML for embedding inside a React <pre> block as the 'output' variable.

### Output Requirements:
1. **Format**:
   - Output only valid HTML markup for the report body.
   - Do NOT include <html>, <head>, <body>, or DOCTYPE tags — only the inner HTML that will be injected.
   - No extra explanations, comments, or markdown formatting — HTML only.

2. **Design Guidelines**:
   - Use semantic HTML5 (e.g., <section>, <header>, <article>, <footer>).
   - Apply inline styles or minimal CSS classes so it renders cleanly when placed inside the application's <pre> block.
   - Keep it responsive and readable inside the UI, with proper headings, spacing, and emphasis.
   - Use a clean, modern, corporate look (muted colors, clear typography, subtle dividers).

3. **Content Structure**:
   - **Header**: Company name, report title, and date.
   - **Key Metrics**: Present as a responsive grid or cards with bold numbers and percentage changes.
   - **Executive Summary**: Concise paragraph highlighting major results.
   - **Detailed Analysis**: Bullet points or short paragraphs for profitability, liquidity, and solvency.
   - **Recommendations**: Numbered or bulleted list of action items.

4. **Constraints**:
   - Never include scripts, external assets, or data-fetching code.
   - Never break out of HTML context with extra text or explanations.
   - Assume the HTML will be styled externally by the app — keep inline styles minimal.

Your job: Transform provided financial data into visually clean, semantic, HTML-based reports ready for embedding in the application's 'output' display.

Rules:
    -Don't start or finish the results with ```
    -Always return only the HTML body content, no additional text or explanations.
    -
"""
)

# Reporting_Dashboard_Developer.print_response("""
# Generate a modern, responsive HTML financial performance report using the following data:

# {
#     "report_title": "Q2 2025 Financial Performance Overview",
#     "company_name": "TechNova Inc.",
#     "report_date": "August 15, 2025",
#     "executive_summary": "TechNova maintained strong profitability in Q2 2025, with revenue growth of 12% year-over-year and a notable improvement in liquidity ratios. Operating expenses increased due to R&D expansion, but cost optimization efforts have started to take effect.",
#     "key_metrics": {
#         "Revenue": "$2.45B ( 12%)",
#         "Net Income": "$580M ( 8%)",
#         "ROE": "18.5%",
#         "Current Ratio": "2.1",
#         "Debt-to-Equity": "0.45"
#     },
#     "detailed_analysis": {
#         "Profitability": "Strong net margin sustained despite increased operating expenses.",
#         "Liquidity": "Improved current ratio due to efficient receivables collection.",
#         "Solvency": "Debt levels remain conservative, allowing room for strategic investments."
#     },
#     "recommendations": [
#         "Continue investment in R&D but monitor expense growth.",
#         "Explore debt financing to leverage current low interest rates.",
#         "Expand market share in emerging markets to sustain revenue growth."
#     ]
# }


# """, stream=True)

def DataCleaningTool(data, *, drop_duplicate_rows=True, impute_missing=True, winsorize_outliers=True):
    """
    Clean tabular data (list[dict] or pandas.DataFrame).
    - Normalizes column names (snake_case)
    - Strips strings, coerces numerics
    - Optional: drop duplicates, impute missing (median for numeric), winsorize outliers (IQR fences)

    Returns:
      {
        "cleaned_data": list[dict],   # JSON-serializable table
        "report": {                   # what was done
           "original_rows": int,
           "rows_after_cleaning": int,
           "dropped_duplicates": int,
           "imputed_values": {col: count},
           "winsorized_values": {col: count},
           "notes": [str]
        }
      }
    """
    import pandas as pd
    import numpy as np
    notes = []

    # Normalize to DataFrame
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        df = pd.DataFrame(list(data or []))  # handles None or empty

    # Normalize column names
    def norm_col(c):
        return (
            str(c).strip()
            .replace("%", "pct")
            .replace("/", "_")
            .replace("-", "_")
            .replace(" ", "_")
            .lower()
        )
    df.rename(columns={c: norm_col(c) for c in df.columns}, inplace=True)

    original_rows = len(df)

    # Strip strings
    for c in df.select_dtypes(include=["object"]).columns:
        df[c] = df[c].astype(str).str.strip()

    # Coerce numerics (safe)
    for c in df.columns:
        coerced = pd.to_numeric(df[c], errors="ignore")
        if not coerced.equals(df[c]):
            df[c] = coerced

    dropped_dups = 0
    if drop_duplicate_rows:
        before = len(df)
        df = df.drop_duplicates()
        dropped_dups = before - len(df)

    imputed_counts = {}
    if impute_missing:
        for c in df.columns:
            if pd.api.types.is_numeric_dtype(df[c]):
                if df[c].isna().any():
                    median_val = df[c].median()
                    imputed_counts[c] = int(df[c].isna().sum())
                    df[c] = df[c].fillna(median_val)
            else:
                if df[c].isna().any():
                    mode_vals = df[c].mode(dropna=True)
                    if not mode_vals.empty:
                        fill_val = mode_vals.iloc[0]
                        imputed_counts[c] = int(df[c].isna().sum())
                        df[c] = df[c].fillna(fill_val)
                    else:
                        # fallback to empty string
                        imputed_counts[c] = int(df[c].isna().sum())
                        df[c] = df[c].fillna("")

    winsorized_counts = {}
    if winsorize_outliers:
        for c in df.select_dtypes(include=["number"]).columns:
            q1 = df[c].quantile(0.25)
            q3 = df[c].quantile(0.75)
            iqr = q3 - q1
            if np.isfinite(iqr) and iqr > 0:
                lo = q1 - 1.5 * iqr
                hi = q3 + 1.5 * iqr
                before = df[c].copy()
                df[c] = df[c].clip(lower=lo, upper=hi)
                winsorized_counts[c] = int((before != df[c]).sum())

    report = {
        "original_rows": int(original_rows),
        "rows_after_cleaning": int(len(df)),
        "dropped_duplicates": int(dropped_dups),
        "imputed_values": imputed_counts,
        "winsorized_values": winsorized_counts,
        "notes": notes,
    }

    cleaned = df.replace({np.nan: None}).to_dict(orient="records")
    return {"cleaned_data": cleaned, "report": report}

def StatisticalAnalysisTool(data):
    """
    Compute descriptive stats and Pearson correlation matrix for numeric columns.

    Input: list[dict] or pandas.DataFrame
    Output:
      {
        "summary": {col: {"count":..,"mean":..,"std":..,"min":..,"median":..,"max":..,"missing":..,"unique":..}},
        "correlation": {col1: {col2: corr, ...}, ...},
        "columns_analyzed": [str]
      }
    """
    import pandas as pd
    import numpy as np

    df = pd.DataFrame(list(data or []))
    summary = {}

    for c in df.columns:
        col = df[c]
        if pd.api.types.is_numeric_dtype(col):
            summary[c] = {
                "count": int(col.count()),
                "mean": float(col.mean()) if col.count() else None,
                "std": float(col.std()) if col.count() > 1 else None,
                "min": float(col.min()) if col.count() else None,
                "median": float(col.median()) if col.count() else None,
                "max": float(col.max()) if col.count() else None,
                "missing": int(col.isna().sum()),
                "unique": int(col.nunique(dropna=True)),
                "type": "numeric",
            }
        else:
            summary[c] = {
                "count": int(col.count()),
                "missing": int(col.isna().sum()),
                "unique": int(col.nunique(dropna=True)),
                "top": (col.mode(dropna=True).iloc[0] if not col.mode(dropna=True).empty else None),
                "type": "categorical",
            }

    # Correlations for numeric columns only
    num_df = df.select_dtypes(include=["number"])
    if num_df.shape[1] >= 2:
        corr = num_df.corr(numeric_only=True).replace({np.nan: None})
        correlation = {r: {c: (None if pd.isna(v) else float(v)) for c, v in corr.loc[r].items()} for r in corr.index}
    else:
        correlation = {}

    return {
        "summary": summary,
        "correlation": correlation,
        "columns_analyzed": list(df.columns),
    }


def RatioAnalysisTool(financials):
    """
    Compute key financial ratios from income statement & balance sheet.

    Input:
      financials = {
        "income_statement": dict OR pandas.DataFrame,
        "balance_sheet": dict OR pandas.DataFrame
      }

    Keys recognized (case-insensitive, with common aliases):
      - Net Income / NetProfit
      - Total Revenue / Revenue / Sales
      - Total Assets
      - Total Stockholder Equity / Shareholders' Equity / Equity
      - Total Current Assets / Current Assets
      - Total Current Liabilities / Current Liabilities
      - Total Liabilities / Liabilities
      - Inventory

    Output:
      { "profitability": {...}, "liquidity": {...}, "solvency": {...} }
    """
    import pandas as pd

    def df_to_flat_dict(obj):
        if isinstance(obj, pd.DataFrame):
            # yfinance-like: index are line items, columns are periods
            # take the most recent non-null value per line item
            latest = {}
            for row_label, row in obj.iterrows():
                val = row.dropna()
                if not val.empty:
                    latest[str(row_label)] = float(val.iloc[0])
            return latest
        return {k: (float(v) if isinstance(v, (int, float)) else v) for k, v in (obj or {}).items()}

    inc = df_to_flat_dict(financials.get("income_statement"))
    bs = df_to_flat_dict(financials.get("balance_sheet"))

    def get(source, *aliases):
        aliases = [a.lower() for a in aliases]
        for k, v in source.items():
            if str(k).lower() in aliases:
                try:
                    return float(v)
                except Exception:
                    pass
        return None

    net_income = get(inc, "net income", "netincome", "net profit", "profit")
    revenue = get(inc, "total revenue", "revenue", "sales")
    total_assets = get(bs, "total assets", "assets")
    equity = get(bs, "total stockholder equity", "shareholders' equity", "equity")
    current_assets = get(bs, "total current assets", "current assets")
    current_liabilities = get(bs, "total current liabilities", "current liabilities")
    total_liabilities = get(bs, "total liabilities", "liabilities")
    inventory = get(bs, "inventory")

    ratios = {
        "profitability": {
            "net_profit_margin_pct": (net_income / revenue * 100) if net_income and revenue else None,
            "return_on_assets_pct": (net_income / total_assets * 100) if net_income and total_assets else None,
            "return_on_equity_pct": (net_income / equity * 100) if net_income and equity else None,
        },
        "liquidity": {
            "current_ratio": (current_assets / current_liabilities) if current_assets and current_liabilities else None,
            "quick_ratio": ((current_assets - (inventory or 0)) / current_liabilities) if current_assets and current_liabilities else None,
        },
        "solvency": {
            "debt_to_equity": (total_liabilities / equity) if total_liabilities and equity else None,
            "equity_ratio_pct": (equity / total_assets * 100) if equity and total_assets else None,
        },
        "inputs_detected": {
            "net_income": net_income, "revenue": revenue, "total_assets": total_assets, "equity": equity,
            "current_assets": current_assets, "current_liabilities": current_liabilities,
            "total_liabilities": total_liabilities, "inventory": inventory
        }
    }

    # Round nicely
    def rnd(x):
        return None if x is None else round(x, 4) if abs(x) < 1000 else round(x, 2)
    for cat in ["profitability", "liquidity", "solvency"]:
        for k in list(ratios[cat].keys()):
            ratios[cat][k] = rnd(ratios[cat][k])

    return ratios


Financial_Data_Analyst = Agent(
    name="Financial Data Analyst",
    # model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API')),
    # model=Gemini(id="gemini-2.5-flash", api_key=api_key_gemini),
    
    stream=True,
    reasoning=True,
    tools=[
        DataCleaningTool,          # cleans raw tabular data
        StatisticalAnalysisTool,   # summary stats + correlations
        RatioAnalysisTool           # finance ratios from statements
    ],
    description="""
A specialist in processing, cleaning, and analyzing raw financial datasets to extract meaningful insights.
This agent uses automated data cleaning to prepare datasets, performs statistical and correlation analysis,
and calculates key financial ratios to assess profitability, liquidity, and solvency.
""",
    instructions="""
You are the Financial Data Analyst for this system.

Your objectives:
1. **Data Cleaning** – Use the DataCleaningTool to normalize column names, remove duplicates, handle missing values, and winsorize outliers when necessary.
2. **Statistical Analysis** – Apply StatisticalAnalysisTool to generate descriptive statistics, identify correlations, and highlight trends or anomalies in the data.
3. **Ratio Analysis** – Use RatioAnalysisTool to compute profitability, liquidity, and solvency ratios from the provided financial statements.
4. **Presentation** – Return results in a clear, structured format that can be directly rendered inside the application’s `output` variable, preserving readability in a `<pre>` block.
5. **Clarity & Insights** – Whenever possible, provide short interpretations of the results so that decision-makers can quickly understand the implications.

Always ensure your outputs are:
- Structured Summary of all the tool's outputs with bulleted or numbered lists
- Readable and concise for textual explanations
- Well-labeled so that each section is easy to identify
"""
)
# Financial_Data_Analyst.print_response("""
# You are given the following sample financial dataset:

# Income Statement:
# - Total Revenue: 1,200,000
# - Net Income: 240,000

# Balance Sheet:
# - Total Assets: 3,000,000
# - Total Equity: 1,800,000
# - Total Current Assets: 900,000
# - Total Current Liabilities: 450,000
# - Inventory: 150,000
# - Total Liabilities: 1,200,000

# Cashflow Statement:
# - Operating Cash Flow: 320,000
# - Investing Cash Flow: -120,000
# - Financing Cash Flow: 80,000

# Perform the following:
# 1. Automatically clean the dataset if necessary.
# 2. Provide summary statistics and correlation insights where applicable.
# 3. Calculate profitability, liquidity, and solvency ratios.
# 4. Present results in a clean structured format, optimized for display in the application output panel.
# """, stream=True)

from yfinance import Ticker
import pandas as pd
import os



def ScenarioPlanningTool(historical_data, assumptions, num_simulations=1000):
    """
    Local scenario simulator using Monte Carlo for sensitivity analysis.
    Inputs: historical_data (dict like above), assumptions (dict: {'growth_mean': 0.05, 'growth_std': 0.01, 'scenarios': ['base', 'optimistic', 'pessimistic']}).
    Outputs: Dict with simulated forecasts and sensitivity results.
    """
    df = pd.DataFrame(historical_data)
    last_value = df['value'].iloc[-1]
    periods = 12  # e.g., 1 year
    
    # Base forecast with variations
    growth_mean = assumptions.get('growth_mean', 0.05)
    growth_std = assumptions.get('growth_std', 0.01)
    
    # Monte Carlo simulations
    simulations = np.random.normal(growth_mean, growth_std, (num_simulations, periods))
    forecasts = np.cumprod(1 + simulations, axis=1) * last_value
    
    # Scenarios
    results = {
        'base': np.mean(forecasts, axis=0).tolist(),
        'optimistic': np.percentile(forecasts, 95, axis=0).tolist(),  # 95th percentile
        'pessimistic': np.percentile(forecasts, 5, axis=0).tolist()   # 5th percentile
    }
    
    # Sensitivity analysis: Vary one assumption (e.g., growth ±10%)
    sensitivity = {
        'growth_up': (last_value * (1 + growth_mean * 1.1) ** periods),
        'growth_down': (last_value * (1 + growth_mean * 0.9) ** periods)
    }
    
    return {
        'simulated_forecasts': results,
        'sensitivity_analysis': sensitivity
    }

# Example: ScenarioPlanningTool(historical_data, {'growth_mean': 0.05, 'growth_std': 0.02})def ScenarioPlanningTool(historical_data, assumptions, num_simulations=1000):
    """
    Local scenario simulator using Monte Carlo for sensitivity analysis.
    Inputs: historical_data (dict like above), assumptions (dict: {'growth_mean': 0.05, 'growth_std': 0.01, 'scenarios': ['base', 'optimistic', 'pessimistic']}).
    Outputs: Dict with simulated forecasts and sensitivity results.
    """
    df = pd.DataFrame(historical_data)
    last_value = df['value'].iloc[-1]
    periods = 12  # e.g., 1 year
    
    # Base forecast with variations
    growth_mean = assumptions.get('growth_mean', 0.05)
    growth_std = assumptions.get('growth_std', 0.01)
    
    # Monte Carlo simulations
    simulations = np.random.normal(growth_mean, growth_std, (num_simulations, periods))
    forecasts = np.cumprod(1 + simulations, axis=1) * last_value
    
    # Scenarios
    results = {
        'base': np.mean(forecasts, axis=0).tolist(),
        'optimistic': np.percentile(forecasts, 95, axis=0).tolist(),  # 95th percentile
        'pessimistic': np.percentile(forecasts, 5, axis=0).tolist()   # 5th percentile
    }
    
    # Sensitivity analysis: Vary one assumption (e.g., growth ±10%)
    sensitivity = {
        'growth_up': (last_value * (1 + growth_mean * 1.1) ** periods),
        'growth_down': (last_value * (1 + growth_mean * 0.9) ** periods)
    }
    
    return {
        'simulated_forecasts': results,
        'sensitivity_analysis': sensitivity
    }


Forecasting_Specialist = Agent(
    name="Forecasting Specialist",
    # model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API')),
    stream=True,
    reasoning=True,
    tools=[
        YFinanceTools(),       # fetch historical market data
        ScenarioPlanningTool,  # simulate scenarios based on historical data and assumptions
        ExaTools()             # interpret macroeconomic indicators
    ],
    description="""
A specialized agent for financial and market forecasting. It gathers historical market trends,
interprets macroeconomic indicators, performs scenario simulations, and provides actionable insights
for strategic planning. The agent can generate base, optimistic, and pessimistic forecasts, 
and analyze sensitivity to key assumptions.
""",
    instructions="""
You are the Forecasting Specialist agent.

1. **Data Acquisition**
   - Use **YFinanceTools** to fetch historical market data for stock indices, ETFs, or other tickers.
   - Use **ExaTools** to interpret macroeconomic indicators (GDP, unemployment rate, inflation, etc.) 
     provided as input. Compute trends, growth rates, and summarize patterns for decision-making.

2. **Scenario Simulation**
   - Use **ScenarioPlanningTool** to run Monte Carlo simulations based on historical market data and input assumptions
     (growth mean, growth std, scenario types).

3. **Forecast Outputs**
   - Produce forecasts for base, optimistic, and pessimistic scenarios.
   - Include sensitivity analysis to key assumptions (e.g., ±10% growth variations).

4. **Presentation**
   - Format results clearly in labeled sections:
     - Market Data Summary (from YFinanceTools)
     - Macroeconomic Insights (from ExaTools)
     - Forecast Scenarios (from ScenarioPlanningTool)
     - Sensitivity Analysis
   - Ensure output is readable in the application's `<pre>` block.

5. **Insights**
   - Highlight key trends, risks, and opportunities for decision-makers.
   - Provide explanations for why trends are positive, negative, or stable.

6. **Accuracy Notes**
   - Clearly mark any assumptions, limitations, or gaps in data.
"""
)

# Example test prompt
# Forecasting_Specialist.print_response("""
# Please fetch market trends for the S&P 500 (ticker '^GSPC') using YFinanceTools. 
# Interpret macroeconomic indicators GDP, UNRATE, and CPI using ExaTools for the past 2 years.
# Then, simulate 12-month forecasts using ScenarioPlanningTool with the following assumptions:
# - Growth mean: 0.04
# - Growth standard deviation: 0.02
# - Scenarios: base, optimistic, pessimistic

# Present the results including sensitivity analysis to ±10% changes in growth, 
# and summarize key market and macroeconomic trends, risks, and opportunities.
# """, stream=True)



# Load your knowledge base from a Markdown file
reporting_rules_kb = MarkdownKnowledgeBase(
    file_path="Knowledge/reporting_standards.md",  # your markdown file with IFRS, GAAP, local rules
    
)

Reporting_Compliance_Officer = Agent(
    name="Reporting Compliance Officer",
    # model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    model=MistralChat(id='mistral-large-latest', api_key=os.getenv('MISTRAL_API')),
    stream=True,
    reasoning=True,
    knowledge=reporting_rules_kb,
    tools=[
        ExaTools(),           # optional tool for interpreting complex rules if needed
    ],
    description="""
A specialized agent that ensures all financial and operational reports comply with internal,
regulatory, and international accounting standards (IFRS, GAAP, local regulations). 
The agent validates raw data, applies reporting rules, and produces audit-ready documentation.
""",
    instructions="""
You are the Reporting Compliance Officer agent.

1. **Data Input**
   - Receive raw financial and operational data in any structured format.
   - Reference the Markdown knowledge base for reporting standards, regulatory requirements, 
     and internal templates.

2. **Validation**
   - Check all data against IFRS, GAAP, and local regulations.
   - Highlight missing or inconsistent data.
   - Ensure all computations (ratios, totals, subtotals) follow the standards.

3. **Report Generation**
   - Produce regulatory-compliant reports (IFRS, GAAP, tax filings, local laws).
   - Produce internal management reports with proper structure.
   - Ensure reports are audit-ready and include notes, assumptions, and explanations.

4. **Output**
   - Structure output clearly using labeled sections.
   - Include warnings for any deviations or incomplete data.
   - Use the Markdown knowledge base to ensure adherence to rules.

5. **Style**
   - Professional, clear, and concise.
   - Highlight key compliance points and discrepancies.
"""
)

# Example test prompt
# Reporting_Compliance_Officer.print_response("""
# You received the raw financial statements for company 'ACME Corp' for FY2024.
# Validate the data against IFRS and local accounting standards as per the knowledge base.
# Generate an internal management report and a regulatory report,
# highlighting any missing information or deviations from compliance rules.
# """, stream=True)
