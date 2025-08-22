from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.calculator import CalculatorTools
from agno.tools.csv_toolkit import CsvTools
from agno.tools.exa import ExaTools
from agno.tools import tool
from dotenv import load_dotenv
from textwrap import dedent
from agno.vectordb.pgvector import PgVector
import os
from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.embedder.mistral import MistralEmbedder
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta

load_dotenv()

knowledge_base = MarkdownKnowledgeBase(
    path="Knowledge/Inventory_Actuary_Knowledge.md",
    # vector_db=PgVector(
    #     table_name="inventory_actuary_knowledge",
    #     db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    #     embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API")),
    # ),
)
# knowledge_base.load(recreate=True)



# =========================
# Agent 1 — Provisioning & Evaluation of Provisions
# =========================

@tool(
    name="calculate_chain_ladder_reserve",
    description="Basic Chain Ladder on a cumulative claims triangle with optional tail; returns ultimates, IBNR, and link ratios.",
    show_result=True,
)
def calculate_chain_ladder_reserve(
    cumulative_triangle: List[List[Optional[float]]],
    tail_factor: float = 1.00
) -> Dict[str, Any]:
    """
    Run a simple Chain Ladder on a cumulative triangle (origin rows x dev columns).
    None indicates missing cells (i.e., to be projected).

    Args:
        cumulative_triangle: 2D list of cumulative claims (origin x dev). Use None for missing cells.
        tail_factor: Additional tail factor applied to remaining LDF product.

    Returns:
        Dict with selected age-to-age factors, LDFs, ultimates, IBNR by origin, and totals.
    """
    n_origin = len(cumulative_triangle)
    if n_origin == 0:
        return {"error": "Empty triangle."}
    n_dev = max(len(row) for row in cumulative_triangle)

    # Compute age-to-age (link) ratios per column (j -> j+1), volume-weighted
    link_factors: List[float] = []
    for j in range(n_dev - 1):
        numer = 0.0
        denom = 0.0
        for i in range(n_origin):
            row = cumulative_triangle[i]
            if j + 1 < len(row) and row[j] is not None and row[j + 1] is not None:
                numer += float(row[j + 1])
                denom += float(row[j])
        link_factors.append((numer / denom) if denom > 0 else 1.0)

    # Build cumulative LDFs from each col to ultimate
    ldfs: List[float] = [1.0] * n_dev
    prod = tail_factor
    for j in range(n_dev - 2, -1, -1):
        prod *= link_factors[j]
        ldfs[j] = prod

    ultimate_by_origin: List[float] = []
    ibnr_by_origin: List[float] = []
    latest_cumulative: List[float] = []
    latest_col_index: List[int] = []

    for i in range(n_origin):
        row = cumulative_triangle[i]
        # find last observed dev col k
        k = -1
        last_val = None
        for j in range(len(row) - 1, -1, -1):
            if row[j] is not None:
                k = j
                last_val = float(row[j])
                break
        if k == -1 or last_val is None:
            ultimate_by_origin.append(0.0)
            ibnr_by_origin.append(0.0)
            latest_cumulative.append(0.0)
            latest_col_index.append(-1)
            continue

        ld = ldfs[k] if k < len(ldfs) else tail_factor
        ultimate = last_val * ld
        ibnr = max(0.0, ultimate - last_val)

        ultimate_by_origin.append(round(ultimate, 2))
        ibnr_by_origin.append(round(ibnr, 2))
        latest_cumulative.append(round(last_val, 2))
        latest_col_index.append(k)

    result = {
        "age_to_age_factors": [round(f, 6) for f in link_factors],
        "ldfs_to_ultimate": [round(x, 6) for x in ldfs],
        "tail_factor": tail_factor,
        "latest_cumulative_by_origin": latest_cumulative,
        "latest_column_index_by_origin": latest_col_index,
        "ultimate_by_origin": ultimate_by_origin,
        "ibnr_by_origin": ibnr_by_origin,
        "totals": {
            "ultimate_total": round(sum(ultimate_by_origin), 2),
            "latest_cumulative_total": round(sum(latest_cumulative), 2),
            "ibnr_total": round(sum(ibnr_by_origin), 2),
        },
    }
    return result


@tool(
    name="discount_cashflows_present_value",
    description="Discount annual cashflows with a simple zero-coupon curve: PV = sum(amount/(1+r_year)^year).",
    show_result=True,
)
def discount_cashflows_present_value(
    cashflows_by_year: Dict[int, float],
    zero_rates_by_year: Dict[int, float]
) -> Dict[str, Any]:
    """
    Present value cashflows using annual zero-coupon rates.

    Args:
        cashflows_by_year: {year_offset: cash_amount}, e.g., {1: -100.0, 2: -80.0, 3: 50.0}
        zero_rates_by_year: {year_offset: annual_rate}, e.g., {1: 0.02, 2: 0.025, 3: 0.03}

    Returns:
        Dict with PV by year and total PV.
    """
    pv_by_year: Dict[int, float] = {}
    total_pv = 0.0
    for t, amt in cashflows_by_year.items():
        r = zero_rates_by_year.get(t, 0.0)
        pv = amt / ((1.0 + r) ** t)
        pv_by_year[t] = round(pv, 2)
        total_pv += pv
    return {
        "present_value_by_year": pv_by_year,
        "present_value_total": round(total_pv, 2),
    }


@tool(
    name="backtest_reserve_adequacy",
    description="Simple actual-vs-expected back-test for prior IBNR.",
    show_result=True,
)
def backtest_reserve_adequacy(
    prior_ibnr_estimate: float,
    actual_paid_on_prior_year: float
) -> Dict[str, Any]:
    """
    Compare last year's IBNR estimate against actual cash emergence.

    Args:
        prior_ibnr_estimate: Last valuation's IBNR for the cohort.
        actual_paid_on_prior_year: Cash paid over the subsequent year for that cohort.

    Returns:
        Dict with adequacy, redundancy/deficiency, and percentages.
    """
    diff = prior_ibnr_estimate - actual_paid_on_prior_year
    status = "adequate" if abs(diff) <= 0.01 * max(1.0, prior_ibnr_estimate) else ("redundant" if diff > 0 else "deficient")
    pct = (diff / prior_ibnr_estimate) if prior_ibnr_estimate != 0 else 0.0
    return {
        "prior_ibnr_estimate": round(prior_ibnr_estimate, 2),
        "actual_paid_on_prior_year": round(actual_paid_on_prior_year, 2),
        "difference": round(diff, 2),
        "adequacy_status": status,
        "difference_pct_of_prior": round(pct, 4)
    }



Provisioning_Evaluation_of_Provisions = Agent(
    name="Provisioning & Evaluation of Provisions Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    tools=[ExaTools(), CsvTools(csvs=['Documents/provisioning_evaluation_data.csv']), CalculatorTools(), calculate_chain_ladder_reserve, discount_cashflows_present_value, backtest_reserve_adequacy],
    description="""
An AI agent specialized in actuarial reserving and technical provisions evaluation.
Focuses on reserve adequacy assessment, claims development analysis, and technical provision calculations for insurance portfolios.
""",
    instructions=dedent("""
You are Provisioning_Evaluation_of_Provisions_Agent, an AI-powered actuarial specialist operating under the Inventory Actuary Module.

## Input Handling & Tool Usage:
1. **Input Handling**
    - You have access to a **file**, using CsvTools(), containing relevant data. Accepted file types include:
        - CSV files containing claims data, reserve information, and actuarial calculations.
        - Text documents (PDF, DOCX, TXT) summarizing reserve studies, claims development, or actuarial reports.
    - Extract relevant information from the file, such as claims triangles, reserve estimates, and development patterns.
    - Pay particular attention to insurance-sector-specific data like IBNR, case reserves, and development factors.

2. **Knowledge & Research Usage**
    - Use your built-in knowledge of actuarial reserving, technical provisions, and insurance accounting standards.
    - Use ExaTools for research on current actuarial practices, regulatory requirements, and industry standards.
    - Apply this knowledge to:
        - Determine optimal reserving methodologies for different insurance portfolios.
        - Identify reserve adequacy and development patterns.
        - Guide the company to develop robust reserve estimates and technical provisions.
        - Suggest improvements and practical approaches for reserve management.

## Your Responsibilities:
1. **Technical Provisions & Reserves**
   - Calculate Best Estimate Liabilities (BEL) under Solvency II and IFRS 17
   - Assess claims reserves, premium provisions, IBNR, and IBNER
   - Apply appropriate reserving methodologies (Chain Ladder, Bornhuetter-Ferguson, Mack, GLM)
   - Implement stochastic methods for uncertainty analysis and validation
   - Ensure reserve adequacy through comprehensive analysis and back-testing

2. **Reserving Methodologies**
   - Apply Chain Ladder method for claims development triangles
   - Implement Bornhuetter-Ferguson for immature accident years
   - Use Mack method for statistical uncertainty quantification
   - Apply GLM methods for claims frequency and severity modeling
   - Implement bootstrap and Monte Carlo methods for stochastic analysis

3. **Validation & Back-Testing**
   - Compare actual vs. expected claims development over time
   - Ensure reserves are sufficient to cover future claim payments
   - Validate prior reserve estimates against actual experience
   - Assess impact of key assumptions on reserve levels
   - Perform sensitivity analysis for key reserve drivers

4. **Discounting & Present Value**
   - Apply appropriate discount curves (risk-free, liquidity-adjusted)
   - Calculate present value of future cash flows
   - Consider liquidity premiums for long-duration liabilities
   - Ensure compliance with regulatory discount rate requirements

## Tool Usage Guidelines:
- Use ExaTools for research on actuarial best practices and regulatory requirements
- Use CsvTools to process and analyze CSV data files for claims and reserve information
- Use CalculatorTools for complex actuarial calculations and validations
- Use calculate_chain_ladder_reserve for claims development analysis and reserve estimation
- Use discount_cashflows_present_value for present value calculations and discounting
- Use backtest_reserve_adequacy for reserve validation and back-testing
- Always reference actuarial standards and regulatory requirements

Your goal is to provide **comprehensive reserve analysis** that enables accurate technical provision calculations and ensures reserve adequacy for insurance portfolios.
"""),
expected_output=dedent("""
- Provide clear, structured reserve analysis and technical provision calculations
- Include tables or bullet points for reserve roll-forwards, development analysis, and adequacy indicators
- Reference actuarial standards, regulatory requirements, and industry best practices
- Emphasize reserve adequacy and validation through back-testing
- Deliver comprehensive reserve estimates with clear methodology documentation
- Provide actionable recommendations for reserve management and improvement
"""),
    knowledge=knowledge_base,
    markdown=True,
    stream=True,
)

# =========================
# Agent 2 — Behavioral Analyses (Lapse/Renewal/Fraud)
# =========================

@tool(
    name="compute_lapse_rates_by_duration",
    description="Compute lapse rates by policy duration with optional multiplicative shock for scenarios.",
    show_result=True,
)
def compute_lapse_rates_by_duration(
    exposures_by_duration: Dict[int, float],
    lapses_by_duration: Dict[int, float],
    shock_up: float = 0.0
) -> Dict[str, Any]:
    """
    Compute base and shocked lapse rates by duration.

    Args:
        exposures_by_duration: {duration: exposure_count}
        lapses_by_duration: {duration: lapse_count}
        shock_up: multiplicative shock (e.g., 0.10 for +10%)

    Returns:
        Dict of base rates, shocked rates, and weighted averages.
    """
    base: Dict[int, float] = {}
    shocked: Dict[int, float] = {}
    total_exp = 0.0
    total_lap = 0.0

    for d, exp in exposures_by_duration.items():
        laps = lapses_by_duration.get(d, 0.0)
        rate = (laps / exp) if exp > 0 else 0.0
        base[d] = round(rate, 6)
        shocked[d] = round(rate * (1.0 + shock_up), 6)
        total_exp += exp
        total_lap += laps

    weighted_base = (total_lap / total_exp) if total_exp > 0 else 0.0
    weighted_shocked = weighted_base * (1.0 + shock_up)
    return {
        "base_lapse_rates_by_duration": base,
        "shocked_lapse_rates_by_duration": shocked,
        "weighted_base_lapse_rate": round(weighted_base, 6),
        "weighted_shocked_lapse_rate": round(weighted_shocked, 6),
        "shock_applied": shock_up
    }


@tool(
    name="compute_renewal_rates_by_segment",
    description="Compute renewal rates by segment and overall weighted average.",
    show_result=True,
)
def compute_renewal_rates_by_segment(
    offers_by_segment: Dict[str, float],
    renewals_by_segment: Dict[str, float]
) -> Dict[str, Any]:
    """
    Compute renewal rates per segment and a weighted average.

    Args:
        offers_by_segment: {segment: number_of_offers}
        renewals_by_segment: {segment: number_of_renewals}

    Returns:
        Dict with per-segment rates and weighted average.
    """
    rates: Dict[str, float] = {}
    tot_offers = 0.0
    tot_ren = 0.0
    for seg, offers in offers_by_segment.items():
        rens = renewals_by_segment.get(seg, 0.0)
        rate = (rens / offers) if offers > 0 else 0.0
        rates[seg] = round(rate, 6)
        tot_offers += offers
        tot_ren += rens
    weighted = (tot_ren / tot_offers) if tot_offers > 0 else 0.0
    return {
        "renewal_rate_by_segment": rates,
        "weighted_renewal_rate": round(weighted, 6),
        "totals": {"offers": tot_offers, "renewals": tot_ren}
    }


@tool(
    name="detect_claim_outliers_zscore",
    description="Flag claim amount outliers using simple z-scores.",
    show_result=True,
)
def detect_claim_outliers_zscore(
    claim_amounts: List[float],
    z_threshold: float = 3.0
) -> Dict[str, Any]:
    """
    Compute mean and std, then flag outliers with |z| > threshold.

    Args:
        claim_amounts: list of claim amounts
        z_threshold: threshold in standard deviations

    Returns:
        Dict with summary stats, outlier indices and values.
    """
    n = len(claim_amounts)
    if n == 0:
        return {"error": "Empty list."}
    mean = sum(claim_amounts) / n
    var = sum((x - mean) ** 2 for x in claim_amounts) / n
    std = var ** 0.5
    outliers: List[Tuple[int, float, float]] = []
    if std == 0:
        # All equal amounts
        return {
            "mean": round(mean, 2),
            "std": 0.0,
            "z_threshold": z_threshold,
            "outliers": [],
            "note": "Standard deviation is zero; no outliers by z-score."
        }
    for idx, x in enumerate(claim_amounts):
        z = (x - mean) / std
        if abs(z) > z_threshold:
            outliers.append((idx, round(x, 2), round(z, 3)))
    return {
        "mean": round(mean, 2),
        "std": round(std, 2),
        "z_threshold": z_threshold,
        "outliers": [{"index": i, "amount": v, "z": z} for i, v, z in outliers],
        "outliers_count": len(outliers)
    }





Behavioral_Analyses = Agent(
    name="Behavioral Analyses Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
            tools=[ExaTools(), CsvTools(csvs=['Documents/behavioral_analyses_data.csv']), compute_lapse_rates_by_duration, compute_renewal_rates_by_segment, detect_claim_outliers_zscore],
    description="""
An AI agent specialized in policyholder behavior modeling and claims behavior analysis.
Focuses on lapse/surrender modeling, renewal behavior analysis, and fraud detection for insurance portfolios.
""",
    instructions=dedent("""
You are Behavioral_Analyses_Agent, an AI-powered behavioral modeling specialist operating under the Inventory Actuary Module.

## Input Handling & Tool Usage:
1. **Input Handling**
    - You have access to a **file**, using CsvTools(), containing relevant data. Accepted file types include:
        - CSV files containing policy data, behavioral metrics, and claims information.
        - Text documents (PDF, DOCX, TXT) summarizing behavioral studies, policy analysis, or claims reports.
    - Extract relevant information from the file, such as policy characteristics, behavioral patterns, and claims data.
    - Pay particular attention to insurance-sector-specific behavioral factors like lapse rates, renewal patterns, and claims frequency.

2. **Knowledge & Research Usage**
    - Use your built-in knowledge of behavioral economics, actuarial science, and insurance risk management.
    - Use ExaTools for research on current behavioral modeling practices and industry trends.
    - Apply this knowledge to:
        - Determine optimal behavioral assumptions for different insurance products.
        - Identify behavioral patterns and their impact on risk assessment.
        - Guide the company to develop robust behavioral models and risk frameworks.
        - Suggest improvements and practical approaches for behavioral risk management.

## Your Responsibilities:
1. **Policyholder Behavior Modeling**
   - Model lapse and surrender behavior by policy duration and product type
   - Analyze renewal behavior for health, P&C, and group contracts
   - Model option exercise behavior (guaranteed annuity options, early withdrawals)
   - Assess market sensitivity and economic impact on behavioral patterns
   - Develop behavioral assumptions for pricing and reserving

2. **Claims Behavior Analysis**
   - Analyze claim frequency and severity trends over time
   - Identify abnormal claims patterns and potential fraud indicators
   - Model catastrophe impact on claims experience
   - Assess behavioral response to market conditions and regulatory changes
   - Develop claims frequency and severity assumptions

3. **Market Behavior Impact**
   - Model behavioral response to interest rate changes and economic stress
   - Assess impact of regulatory changes on policyholder behavior
   - Analyze competitive factors and market dynamics
   - Model behavioral sensitivity to product design and pricing changes
   - Develop stress testing scenarios for behavioral assumptions

## Tool Usage Guidelines:
- Use ExaTools for research on behavioral modeling best practices and industry trends
- Use CsvTools to process and analyze CSV data files for behavioral and claims information
- Use compute_lapse_rates_by_duration for lapse rate analysis and duration-based modeling
- Use compute_renewal_rates_by_segment for renewal behavior analysis and segmentation
- Use detect_claim_outliers_zscore for fraud detection and abnormal claims identification
- Always reference actuarial standards and behavioral modeling best practices

Your goal is to provide **comprehensive behavioral analysis** that enables accurate risk assessment and supports pricing, reserving, and risk management decisions.
"""),
expected_output=dedent("""
- Provide clear, structured behavioral analysis and modeling results
- Include tables or bullet points for behavioral patterns, risk indicators, and trend analysis
- Reference behavioral modeling best practices, actuarial standards, and industry trends
- Emphasize risk management implications and business decision support
- Deliver comprehensive behavioral models with clear assumption documentation
- Provide actionable recommendations for behavioral risk management and pricing
"""),
    knowledge=knowledge_base,
    markdown=True,
    stream=True,
)

# =========================
# Agent 3 — Technical Margins Analysis (Risk Margin, Variance Bridge)
# =========================

@tool(
    name="calculate_risk_margin_coc",
    description="Cost-of-Capital Risk Margin: sum(SCR_t * CoC / (1+r_t)^t).",
    show_result=True,
)
def calculate_risk_margin_coc(
    scr_by_year: Dict[int, float],
    cost_of_capital_rate: float,
    discount_curve: Dict[int, float]
) -> Dict[str, Any]:
    """
    Compute Risk Margin using the cost-of-capital approach.

    Args:
        scr_by_year: {t: SCR_t}
        cost_of_capital_rate: annual CoC rate (e.g., 0.06)
        discount_curve: {t: risk-free rate for year t}

    Returns:
        Dict with RM by year and total.
    """
    rm_by_year: Dict[int, float] = {}
    total_rm = 0.0
    for t, scr in scr_by_year.items():
        r = discount_curve.get(t, 0.0)
        term = scr * cost_of_capital_rate / ((1.0 + r) ** t)
        rm_by_year[t] = round(term, 2)
        total_rm += term
    return {
        "risk_margin_by_year": rm_by_year,
        "risk_margin_total": round(total_rm, 2),
        "parameters": {
            "cost_of_capital_rate": cost_of_capital_rate
        }
    }


@tool(
    name="technical_margin_analysis",
    description="Compute technical margin = Premium - Claims - Expenses - Commissions, plus key ratios.",
    show_result=True,
)
def technical_margin_analysis(
    premium_earned: float,
    claims_incurred: float,
    expenses: float,
    commissions: float = 0.0
) -> Dict[str, Any]:
    """
    Compute a basic technical margin and ratios.

    Args:
        premium_earned: Earned premium
        claims_incurred: Incurred claims
        expenses: Operating expenses
        commissions: Commissions/brokerage

    Returns:
        Dict with margin and ratios (loss, expense, combined).
    """
    margin = premium_earned - claims_incurred - expenses - commissions
    loss_ratio = (claims_incurred / premium_earned) if premium_earned else 0.0
    expense_ratio = (expenses / premium_earned) if premium_earned else 0.0
    commission_ratio = (commissions / premium_earned) if premium_earned else 0.0
    combined_ratio = loss_ratio + expense_ratio + commission_ratio
    return {
        "premium_earned": round(premium_earned, 2),
        "claims_incurred": round(claims_incurred, 2),
        "expenses": round(expenses, 2),
        "commissions": round(commissions, 2),
        "technical_margin": round(margin, 2),
        "ratios": {
            "loss_ratio": round(loss_ratio, 4),
            "expense_ratio": round(expense_ratio, 4),
            "commission_ratio": round(commission_ratio, 4),
            "combined_ratio": round(combined_ratio, 4),
        }
    }


@tool(
    name="variance_bridge_expected_to_actual",
    description="Simple variance bridge: Expected vs Actual for premium, claims, expenses.",
    show_result=True,
)
def variance_bridge_expected_to_actual(
    expected: Dict[str, float],
    actual: Dict[str, float]
) -> Dict[str, Any]:
    """
    Decompose variance between Expected and Actual for key items.

    Args:
        expected: {"premium": x, "claims": y, "expenses": z}
        actual:   {"premium": x, "claims": y, "expenses": z}

    Returns:
        Dict with component variances, total variance, and percentage contributions.
    """
    keys = ["premium", "claims", "expenses"]
    components: Dict[str, float] = {}
    total = 0.0
    for k in keys:
        diff = actual.get(k, 0.0) - expected.get(k, 0.0)
        components[k] = round(diff, 2)
        total += diff

    pct_contrib = {k: (components[k] / total) if total != 0 else 0.0 for k in keys}
    return {
        "components": components,
        "total_variance": round(total, 2),
        "percentage_contribution": {k: round(v, 4) for k, v in pct_contrib.items()}
    }



Technical_Margins_Analysis = Agent(
    name="Technical Margins Analysis Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    tools=[ExaTools(), CsvTools(csvs=['Documents/technical_margins_data.csv']), CalculatorTools(), calculate_risk_margin_coc, technical_margin_analysis, variance_bridge_expected_to_actual],
    description="""
An AI agent specialized in technical margin analysis and profitability studies for insurance portfolios.
Focuses on technical margin calculation, risk margin assessment, and experience variance analysis.
""",
    instructions=dedent("""
You are Technical_Margins_Analysis_Agent, an AI-powered profitability analysis specialist operating under the Inventory Actuary Module.

## Input Handling & Tool Usage:
1. **Input Handling**
    - You have access to a **file**, using CsvTools(), containing relevant data. Accepted file types include:
        - CSV files containing premium data, claims information, and expense details.
        - Text documents (PDF, DOCX, TXT) summarizing profitability analysis, expense studies, or performance reports.
    - Extract relevant information from the file, such as premium volumes, claims costs, and operating expenses.
    - Pay particular attention to insurance-sector-specific metrics like loss ratios, expense ratios, and technical margins.

2. **Knowledge & Research Usage**
    - Use your built-in knowledge of insurance profitability analysis, risk management, and actuarial science.
    - Use ExaTools for research on current profitability trends and industry benchmarks.
    - Apply this knowledge to:
        - Determine optimal profitability analysis frameworks for different insurance portfolios.
        - Identify underperforming and overperforming product lines.
        - Guide the company to develop robust profitability management strategies.
        - Suggest improvements and practical approaches for margin optimization.

## Your Responsibilities:
1. **Profitability Studies**
   - Calculate technical margins (premium minus claims minus expenses minus commissions)
   - Analyze product line performance and identify improvement opportunities
   - Monitor profitability trends over time and across segments
   - Benchmark performance against industry standards and targets
   - Develop profitability improvement strategies and action plans

2. **Risk Margin Calculation**
   - Implement cost-of-capital approach for risk margin calculation
   - Apply confidence level methods for alternative risk assessment
   - Account for portfolio diversification effects in risk margin calculation
   - Ensure compliance with Solvency II and other regulatory frameworks
   - Develop risk margin methodologies for different risk types

3. **Experience Variance Analysis**
   - Compare expected vs. actual mortality and morbidity experience
   - Analyze lapse experience patterns and trends
   - Monitor claims frequency and severity against expectations
   - Establish feedback loops for assumption updates
   - Develop variance analysis frameworks for continuous improvement

## Tool Usage Guidelines:
- Use ExaTools for research on profitability analysis best practices and industry benchmarks
- Use CsvTools to process and analyze CSV data files for premium, claims, and expense information
- Use CalculatorTools for complex profitability calculations and risk margin computations
- Use calculate_risk_margin_coc for cost-of-capital risk margin calculations
- Use technical_margin_analysis for profitability analysis and ratio calculations
- Use variance_bridge_expected_to_actual for experience variance analysis and trend assessment
- Always reference actuarial standards and regulatory requirements

Your goal is to provide **comprehensive profitability analysis** that enables accurate technical margin assessment and supports business decision-making for insurance portfolios.
"""),
expected_output=dedent("""
- Provide clear, structured profitability analysis and technical margin calculations
- Include tables or bullet points for technical margins, loss ratios, and expense analysis
- Reference profitability analysis best practices, actuarial standards, and industry benchmarks
- Emphasize business improvement opportunities and risk management implications
- Deliver comprehensive profitability analysis with clear methodology documentation
- Provide actionable recommendations for margin optimization and performance improvement
"""),
    knowledge=knowledge_base,
    markdown=True,
    stream=True,
)

# =========================
# Agent 4 — Structuring Actuarial Functions (Governance & Process)
# =========================

@tool(
    name="generate_close_calendar",
    description="Generate a month-end close calendar from a period end date and step offsets.",
    show_result=True,
)
def generate_close_calendar(
    period_end_date: str,
    step_offsets_days: Dict[str, int] = None
) -> Dict[str, Any]:
    """
    Build a simple close calendar.

    Args:
        period_end_date: ISO date 'YYYY-MM-DD' (the accounting period end)
        step_offsets_days: {step_name: offset_in_days_relative_to_period_end}
                           Defaults to a common close sequence.

    Returns:
        Dict with steps and due dates.
    """
    if step_offsets_days is None:
        step_offsets_days = {
            "data_cutoff": 1,
            "dq_checks_complete": 2,
            "reserving_lock": 4,
            "margin_review": 6,
            "management_signoff": 8,
            "pack_assembled": 9
        }
    try:
        ped = datetime.strptime(period_end_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid period_end_date; expected YYYY-MM-DD."}

    schedule = []
    for step, offset in step_offsets_days.items():
        due = ped + timedelta(days=offset)
        schedule.append({
            "step": step,
            "due_date": due.strftime("%Y-%m-%d")
        })
    schedule.sort(key=lambda x: x["due_date"])
    return {"period_end_date": period_end_date, "schedule": schedule}


@tool(
    name="control_checklist_summary",
    description="Summarize control checklist statuses with counts and failing items.",
    show_result=True,
)
def control_checklist_summary(
    controls: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Summarize a list of controls with status.

    Args:
        controls: list of {"name": str, "status": "OK" | "Fail" | "NA", "owner": str (optional)}

    Returns:
        Dict with counts and failing controls list.
    """
    counts = {"OK": 0, "Fail": 0, "NA": 0}
    failing: List[Dict[str, Any]] = []
    for c in controls:
        status = str(c.get("status", "NA")).upper()
        if status not in counts:
            status = "NA"
        counts[status] += 1
        if status == "FAIL":
            failing.append({"name": c.get("name", "unknown"), "owner": c.get("owner", "")})
    return {"counts": counts, "failing_controls": failing}


@tool(
    name="assemble_regulatory_pack",
    description="Create an ordered outline of a regulatory/audit pack from sectioned items.",
    show_result=True,
)
def assemble_regulatory_pack(
    items: List[Dict[str, str]],
    section_order: List[str]
) -> Dict[str, Any]:
    """
    Assemble a pack outline from item summaries.

    Args:
        items: list of {"section": str, "title": str, "content_summary": str}
        section_order: desired section order

    Returns:
        Dict with ordered table of contents and counts.
    """
    toc: List[Dict[str, str]] = []
    for sec in section_order:
        for it in items:
            if it.get("section") == sec:
                toc.append({"section": sec, "title": it.get("title", "")})
    return {"table_of_contents": toc, "sections_count": len(set(section_order)), "items_count": len(items)}



Structuring_Actuarial_Functions = Agent(
    name="Structuring Actuarial Functions Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    tools=[ExaTools(), CsvTools(csvs=['Documents/structuring_actuarial_functions_data.csv']), generate_close_calendar, control_checklist_summary, assemble_regulatory_pack],
    description="""
An AI agent specialized in structuring actuarial functions and governance frameworks.
Focuses on process design, control frameworks, and regulatory pack assembly for actuarial operations.
""",
    instructions=dedent("""
You are Structuring_Actuarial_Functions_Agent, an AI-powered governance specialist operating under the Inventory Actuary Module.

## Input Handling & Tool Usage:
1. **Input Handling**
    - You have access to a **file**, using CsvTools(), containing relevant data. Accepted file types include:
        - CSV files containing process information, control frameworks, and governance data.
        - Text documents (PDF, DOCX, TXT) summarizing process documentation, control frameworks, or governance structures.
    - Extract relevant information from the file, such as process workflows, control requirements, and governance frameworks.
    - Pay particular attention to insurance-sector-specific requirements like regulatory compliance, audit readiness, and risk management.

2. **Knowledge & Research Usage**
    - Use your built-in knowledge of actuarial governance, process design, and regulatory compliance.
    - Use ExaTools for research on current governance best practices and regulatory requirements.
    - Apply this knowledge to:
        - Determine optimal governance frameworks for actuarial operations.
        - Identify process improvement opportunities and control requirements.
        - Guide the company to develop robust governance and control frameworks.
        - Suggest improvements and practical approaches for operational excellence.

## Your Responsibilities:
1. **Governance & Process Design**
   - Define actuarial policies for reserving, pricing, and risk management
   - Establish governance frameworks and oversight processes for actuarial work
   - Implement control frameworks for provisioning cycles and key processes
   - Define risk appetite and tolerance limits for actuarial assumptions
   - Develop process workflows and operational procedures

2. **Documentation & Methodology**
   - Write methodological notes for auditors and regulators
   - Standardize tools, templates, and processes across entities
   - Maintain version control for models, assumptions, and methodologies
   - Capture and share actuarial knowledge and best practices
   - Establish documentation standards and quality requirements

3. **Audit & Regulatory Interaction**
   - Support internal audit reviews of actuarial processes and controls
   - Ensure compliance with regulatory requirements and respond to requests
   - Support external actuarial opinions and regulatory reviews
   - Communicate actuarial results to management, board, and regulators
   - Prepare regulatory packs and audit documentation

4. **Cross-functional Coordination**
   - Coordinate with finance on closing accounts and financial reporting
   - Align with risk management on capital requirements and risk assessment
   - Collaborate with underwriting on pricing assumptions and product development
   - Coordinate with operations on data quality and process efficiency
   - Establish communication frameworks and escalation procedures

## Tool Usage Guidelines:
- Use ExaTools for research on governance best practices and regulatory requirements
- Use CsvTools to process and analyze CSV data files for process and control information
- Use generate_close_calendar for process timeline management and deadline tracking
- Use control_checklist_summary for control framework monitoring and status reporting
- Use assemble_regulatory_pack for regulatory documentation and audit pack preparation
- Always reference actuarial standards and regulatory requirements

Your goal is to provide **comprehensive governance solutions** that enable efficient and compliant actuarial operations through structured processes and robust control frameworks.
"""),
expected_output=dedent("""
- Provide clear, structured governance frameworks and process designs
- Include tables or bullet points for process workflows, control frameworks, and governance structures
- Reference governance best practices, regulatory requirements, and industry standards
- Emphasize operational efficiency and regulatory compliance
- Deliver comprehensive governance frameworks with clear process documentation
- Provide actionable recommendations for operational excellence and control improvement
"""),
    knowledge=knowledge_base,
    markdown=True,
    stream=True,
)

# =========================
# Agent 5 — Reg & Accounting Alignment (IFRS 17 / SII / Local GAAP)
# =========================

@tool(
    name="select_ifrs17_measurement_model",
    description="Rule-based selector: GMM vs PAA vs VFA based on product traits.",
    show_result=True,
)
def select_ifrs17_measurement_model(
    product_type: str,
    contract_length_years: float,
    has_direct_participation_features: bool,
    revenue_pattern: str = "level"
) -> Dict[str, Any]:
    """
    Select a plausible IFRS 17 measurement model (simplified rules).

    Args:
        product_type: e.g., 'short-tail non-life', 'life annuity', 'savings'
        contract_length_years: typical coverage duration in years
        has_direct_participation_features: True if direct participating contracts
        revenue_pattern: 'level'/'front-loaded' (informative only)

    Returns:
        Dict with selected model and rationale.
    """
    model = "GMM"
    rationale = []
    if has_direct_participation_features:
        model = "VFA"
        rationale.append("Direct participating features detected.")
    elif contract_length_years <= 1.0 and "non-life" in product_type.lower():
        model = "PAA"
        rationale.append("Short coverage period (<=1y) and non-life: PAA reasonable approximation.")
    else:
        rationale.append("Defaulting to GMM based on duration/features.")
    return {
        "selected_model": model,
        "rationale": rationale,
        "inputs": {
            "product_type": product_type,
            "contract_length_years": contract_length_years,
            "has_direct_participation_features": has_direct_participation_features,
            "revenue_pattern": revenue_pattern
        }
    }


@tool(
    name="build_qrt_simplified",
    description="Build a simplified Solvency II QRT-like snapshot from BEL, Risk Margin, Own Funds.",
    show_result=True,
)
def build_qrt_simplified(
    bel_net: float,
    risk_margin: float,
    own_funds: float
) -> Dict[str, Any]:
    """
    Construct a tiny QRT-like structure (highly simplified).

    Args:
        bel_net: Best Estimate Liabilities (net of reinsurance)
        risk_margin: Risk margin
        own_funds: Eligible own funds

    Returns:
        Dict with balance subtotals and solvency indicators.
    """
    technical_provisions = bel_net + risk_margin
    coverage = (own_funds / technical_provisions) if technical_provisions else 0.0
    return {
        "tp": {
            "bel_net": round(bel_net, 2),
            "risk_margin": round(risk_margin, 2),
            "technical_provisions": round(technical_provisions, 2),
        },
        "own_funds": round(own_funds, 2),
        "coverage_indicator": round(coverage, 4)
    }


@tool(
    name="reconcile_actuarial_to_ledger",
    description="Compare actuarial figures to ledger balances with tolerance flags.",
    show_result=True,
)
def reconcile_actuarial_to_ledger(
    actuarial: Dict[str, float],
    ledger: Dict[str, float],
    tolerance_abs: float = 1.0,
    tolerance_pct: float = 0.005
) -> Dict[str, Any]:
    """
    Reconcile key balances and flag differences.

    Args:
        actuarial: {"reserves": x, "premiums": y, "claims": z, ...}
        ledger: same keys as actuarial
        tolerance_abs: absolute difference tolerance
        tolerance_pct: percentage tolerance vs ledger

    Returns:
        Dict with differences, flags per key, and overall status.
    """
    diffs: Dict[str, Dict[str, Any]] = {}
    all_ok = True
    for k, led_val in ledger.items():
        act_val = actuarial.get(k, 0.0)
        diff = act_val - led_val
        pct = (diff / led_val) if led_val != 0 else 0.0
        ok = (abs(diff) <= tolerance_abs) or (abs(pct) <= tolerance_pct)
        if not ok:
            all_ok = False
        diffs[k] = {
            "actuarial": round(act_val, 2),
            "ledger": round(led_val, 2),
            "difference": round(diff, 2),
            "difference_pct_of_ledger": round(pct, 4),
            "within_tolerance": ok
        }
    return {
        "items": diffs,
        "overall_reconciled": all_ok,
        "tolerance_abs": tolerance_abs,
        "tolerance_pct": tolerance_pct
    }



Reg_Accounting_Alignment = Agent(
    name="Regulatory & Accounting Alignment Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    tools=[ExaTools(), CsvTools(csvs=['Documents/reg_accounting_alignment_data.csv']), CalculatorTools(), select_ifrs17_measurement_model, build_qrt_simplified, reconcile_actuarial_to_ledger],
    description="""
An AI agent specialized in regulatory and accounting alignment for insurance portfolios.
Focuses on IFRS 17 compliance, Solvency II alignment, and local GAAP/statutory reporting requirements.
""",
    instructions=dedent("""
You are Reg_Accounting_Alignment_Agent, an AI-powered regulatory compliance specialist operating under the Inventory Actuary Module.

## Input Handling & Tool Usage:
1. **Input Handling**
    - You have access to a **file**, using CsvTools(), containing relevant data. Accepted file types include:
        - CSV files containing regulatory data, accounting information, and compliance requirements.
        - Text documents (PDF, DOCX, TXT) summarizing regulatory frameworks, accounting standards, or compliance guidelines.
    - Extract relevant information from the file, such as regulatory requirements, accounting policies, and compliance frameworks.
    - Pay particular attention to insurance-sector-specific requirements like IFRS 17, Solvency II, and local statutory standards.

2. **Knowledge & Research Usage**
    - Use your built-in knowledge of IFRS 17, Solvency II, insurance accounting, and regulatory compliance.
    - Use ExaTools for research on current regulatory updates and accounting standard interpretations.
    - Apply this knowledge to:
        - Determine optimal compliance frameworks for different regulatory requirements.
        - Identify alignment opportunities between accounting and regulatory standards.
        - Guide the company to develop robust compliance and alignment strategies.
        - Suggest improvements and practical approaches for regulatory compliance.

## Your Responsibilities:
1. **IFRS 17 Compliance**
   - Ensure correct grouping of contracts into portfolios and annual cohorts
   - Support measurement under GMM, PAA, or VFA depending on product characteristics
   - Reconcile actuarial provisions with accounting entries and disclosures
   - Support transition from existing standards to IFRS 17
   - Develop measurement model selection criteria and application guidance

2. **Solvency II Alignment**
   - Align BEL and Risk Margin with ORSA requirements and regulatory standards
   - Support production of Quantitative Reporting Templates (QRTs) and regulatory reports
   - Ensure actuarial assumptions support capital adequacy assessment
   - Align with enterprise risk management framework and ORSA process
   - Develop reconciliation frameworks between IFRS 17 and Solvency II

3. **Local GAAP & Statutory**
   - Support local regulatory reporting requirements and statutory reserves
   - Ensure compliance with local accounting and regulatory standards
   - Support reporting across multiple regulatory jurisdictions
   - Maintain reconciliation between different reporting frameworks
   - Develop multi-jurisdiction compliance strategies

## Tool Usage Guidelines:
- Use ExaTools for research on regulatory updates and accounting standard interpretations
- Use CsvTools to process and analyze CSV data files for regulatory and accounting information
- Use CalculatorTools for compliance calculations and reconciliation analysis
- Use select_ifrs17_measurement_model for measurement model selection and compliance assessment
- Use build_qrt_simplified for Solvency II QRT preparation and regulatory reporting
- Use reconcile_actuarial_to_ledger for accounting reconciliation and compliance validation
- Always reference official regulatory guidance and accounting standards

Your goal is to provide **comprehensive regulatory alignment** that enables successful compliance with IFRS 17, Solvency II, and local regulatory requirements while maintaining consistency across accounting frameworks.
"""),
expected_output=dedent("""
- Provide clear, structured regulatory compliance and alignment solutions
- Include tables or bullet points for compliance frameworks, reconciliation matrices, and implementation requirements
- Reference regulatory guidance, accounting standards, and compliance best practices
- Emphasize regulatory compliance and cross-framework alignment
- Deliver comprehensive compliance frameworks with clear implementation guidance
- Provide actionable recommendations for regulatory compliance and alignment improvement
"""),
    knowledge=knowledge_base,
    markdown=True,
    stream=True,
)

# =========================
# Agent 6 — Monitoring & Continuous Improvement
# =========================

@tool(
    name="kpi_trend_and_alerts",
    description="Compute simple trend (first→last) for KPIs and raise alerts on threshold breaches.",
    show_result=True,
)
def kpi_trend_and_alerts(
    kpi_series: Dict[str, List[float]],
    alert_thresholds: Dict[str, float]
) -> Dict[str, Any]:
    """
    Trend KPIs and compare last value to threshold.

    Args:
        kpi_series: {kpi_name: [v1, v2, ..., vn]}
        alert_thresholds: {kpi_name: threshold_max_allowed} (alert if last > threshold)

    Returns:
        Dict with trend per KPI and alert flags.
    """
    output: Dict[str, Any] = {"kpis": {}}
    for name, series in kpi_series.items():
        if not series:
            output["kpis"][name] = {"error": "Empty series."}
            continue
        first, last = series[0], series[-1]
        trend_abs = last - first
        trend_pct = (trend_abs / first) if first != 0 else 0.0
        threshold = alert_thresholds.get(name, None)
        alert = (threshold is not None) and (last > threshold)
        output["kpis"][name] = {
            "first": round(first, 2),
            "last": round(last, 2),
            "trend_abs": round(trend_abs, 2),
            "trend_pct": round(trend_pct, 4),
            "threshold": threshold,
            "alert": alert
        }
    return output


@tool(
    name="detect_model_drift_simple",
    description="Compare baseline vs current model metrics; flag drift if relative change exceeds threshold.",
    show_result=True,
)
def detect_model_drift_simple(
    baseline_metrics: Dict[str, float],
    current_metrics: Dict[str, float],
    drift_threshold: float = 0.1
) -> Dict[str, Any]:
    """
    Simple drift detector on scalar metrics (e.g., MAE, AUC).

    Args:
        baseline_metrics: {metric: value}
        current_metrics: {metric: value}
        drift_threshold: relative change (e.g., 0.1 for 10%)

    Returns:
        Dict with per-metric drift pct and alerts.
    """
    results: Dict[str, Dict[str, Any]] = {}
    for m, base in baseline_metrics.items():
        cur = current_metrics.get(m, base)
        if base == 0:
            drift = 0.0 if cur == 0 else float("inf")
        else:
            drift = (cur - base) / base
        results[m] = {
            "baseline": round(base, 6),
            "current": round(cur, 6),
            "drift_pct": (None if drift == float("inf") else round(drift, 6)),
            "alert": (abs(drift) > drift_threshold) if drift != float("inf") else True
        }
    return {
        "drift_threshold": drift_threshold,
        "metrics": results
    }


@tool(
    name="build_dashboard_snapshot",
    description="Assemble a dashboard snapshot from named sections (KPIs, Risks, Actions).",
    show_result=True,
)
def build_dashboard_snapshot(
    sections: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Package a simple dashboard payload for UI rendering/logging.

    Args:
        sections: {"KPIs": {...}, "Risks": {...}, "Actions": {...}, ...}

    Returns:
        Dict with normalized keys and counts for each section.
    """
    normalized = {}
    counts = {}
    for sec, payload in sections.items():
        normalized[sec] = payload
        counts[sec] = (len(payload) if isinstance(payload, dict) else 1)
    return {
        "snapshot": normalized,
        "section_counts": counts,
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }


Monitoring_Continuous_Improvement = Agent(
    name="Monitoring & Continuous Improvement Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    tools=[ExaTools(), CsvTools(csvs=['Documents/monitoring_continuous_improvement_data.csv']), kpi_trend_and_alerts, detect_model_drift_simple, build_dashboard_snapshot],
    description="""
An AI agent specialized in monitoring and continuous improvement for actuarial operations.
Focuses on closing cycle optimization, model improvements, and early warning indicator development.
""",
    instructions=dedent("""
You are Monitoring_Continuous_Improvement_Agent, an AI-powered operational excellence specialist operating under the Inventory Actuary Module.

## Input Handling & Tool Usage:
1. **Input Handling**
    - You have access to a **file**, using CsvTools(), containing relevant data. Accepted file types include:
        - CSV files containing performance metrics, KPI data, and operational information.
        - Text documents (PDF, DOCX, TXT) summarizing performance reports, improvement initiatives, or operational analysis.
    - Extract relevant information from the file, such as performance trends, improvement opportunities, and operational metrics.
    - Pay particular attention to insurance-sector-specific metrics like reserve adequacy, model performance, and process efficiency.

2. **Knowledge & Research Usage**
    - Use your built-in knowledge of operational excellence, continuous improvement, and performance management.
    - Use ExaTools for research on current best practices and industry standards for operational improvement.
    - Apply this knowledge to:
        - Determine optimal monitoring frameworks for different operational areas.
        - Identify improvement opportunities and performance optimization strategies.
        - Guide the company to develop robust monitoring and improvement frameworks.
        - Suggest improvements and practical approaches for operational excellence.

## Your Responsibilities:
1. **Closing Cycle Optimization**
   - Streamline reserving processes to meet fast close deadlines
   - Automate data collection, validation, and calculation processes
   - Implement parallel processing where possible to reduce cycle time
   - Establish quality gates and checkpoints throughout the process
   - Develop performance metrics and monitoring frameworks

2. **Model Improvements**
   - Implement machine learning techniques for lapse prediction and claims modeling
   - Establish robust model validation and monitoring processes
   - Upgrade actuarial software and calculation engines
   - Optimize model performance and calculation speed
   - Develop model drift detection and alerting frameworks

3. **Early Warning Indicators**
   - Build dashboards to track key performance and risk indicators
   - Establish thresholds and alerts for key metrics
   - Monitor trends and identify early warning signals
   - Define escalation procedures for threshold breaches
   - Develop predictive analytics for risk assessment

## Tool Usage Guidelines:
- Use ExaTools for research on operational excellence best practices and industry standards
- Use CsvTools to process and analyze CSV data files for performance and operational information
- Use kpi_trend_and_alerts for performance monitoring and trend analysis
- Use detect_model_drift_simple for model validation and drift detection
- Use build_dashboard_snapshot for dashboard development and performance reporting
- Always reference operational excellence best practices and industry standards

Your goal is to provide **comprehensive monitoring solutions** that enable operational excellence and continuous improvement through effective performance management and early warning systems.
"""),
expected_output=dedent("""
- Provide clear, structured monitoring frameworks and improvement strategies
- Include tables or bullet points for performance metrics, improvement initiatives, and operational analysis
- Reference operational excellence best practices, industry standards, and continuous improvement methodologies
- Emphasize performance optimization and operational efficiency
- Deliver comprehensive monitoring frameworks with clear improvement guidance
- Provide actionable recommendations for operational excellence and performance improvement
"""),
    knowledge=knowledge_base,
    markdown=True,
    stream=True,
)


Inventory_Actuary_Manager_Agent = Team(
    name="Inventory Actuary Manager Agent",
    mode="coordinate",
    model = MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    members=[Provisioning_Evaluation_of_Provisions, Behavioral_Analyses, Technical_Margins_Analysis, Structuring_Actuarial_Functions, Reg_Accounting_Alignment, Monitoring_Continuous_Improvement],
    success_criteria="""
The Inventory Actuary Manager Agent successfully coordinates all actuarial activities to achieve:
1. Complete reserve adequacy and technical provision accuracy across all insurance portfolios
2. Successful implementation of behavioral modeling and risk assessment frameworks
3. Accurate technical margin analysis and profitability optimization
4. Robust governance frameworks and operational excellence in actuarial functions
5. Successful regulatory compliance with IFRS 17, Solvency II, and local requirements
6. Continuous improvement and operational excellence in actuarial operations
""",
    description="""
A comprehensive team coordinator managing all aspects of actuarial operations including reserving, behavioral modeling, profitability analysis, governance, regulatory compliance, and continuous improvement.
""",
    instructions=dedent("""
The Inventory Actuary Manager Agent coordinates across six specialized agents to provide comprehensive actuarial services:

1. **Provisioning_Evaluation_of_Provisions**: Manages technical provisions, reserve adequacy, and claims development analysis
2. **Behavioral_Analyses**: Develops behavioral models for lapse, renewal, and claims behavior
3. **Technical_Margins_Analysis**: Analyzes profitability, risk margins, and experience variance
4. **Structuring_Actuarial_Functions**: Establishes governance frameworks and operational processes
5. **Reg_Accounting_Alignment**: Ensures regulatory compliance and accounting alignment
6. **Monitoring_Continuous_Improvement**: Optimizes operations and implements continuous improvement

## Team Coordination:
- Agents work sequentially to feed outputs from one stage to the next
- Reserve analysis and technical provisions feed into behavioral modeling and risk assessment
- Behavioral models and risk analysis support technical margin calculations and profitability analysis
- Governance frameworks and operational processes enable regulatory compliance and reporting
- Monitoring and improvement frameworks ensure ongoing operational excellence

## Output Standards:
- All deliverables must meet actuarial standards and regulatory requirements
- Reserve estimates must be adequate and properly validated
- Behavioral models must be statistically sound and business-relevant
- Technical margins must be accurately calculated and properly documented
- Governance frameworks must be robust and audit-ready
- All outputs must support successful regulatory compliance and business decision-making

Your goal is to provide **integrated actuarial services** that ensure reserve adequacy, risk management excellence, and regulatory compliance through coordinated, end-to-end actuarial support.
"""),
    show_tool_calls=True,
    markdown=True,
    show_members_responses=True,
)


# ============================================================================
# TESTING FUNCTIONS
# ============================================================================

def test_provisioning_evaluation():
    """Test provisioning and evaluation agent"""
    Provisioning_Evaluation_of_Provisions.print_response(
        "Analyze reserve adequacy for a property and casualty insurance portfolio. "
        "Provide technical provision calculations using Chain Ladder method and "
        "validate reserve estimates through back-testing analysis.",
        stream=True,
    )

def test_behavioral_analyses():
    """Test behavioral analyses agent"""
    Behavioral_Analyses.print_response(
        "Analyze lapse and renewal behavior for a life insurance portfolio. "
        "Develop behavioral models for policyholder behavior and "
        "assess market sensitivity impact on behavioral patterns.",
        stream=True,
    )

def test_technical_margins():
    """Test technical margins analysis agent"""
    Technical_Margins_Analysis.print_response(
        "Analyze technical margins and profitability for an insurance portfolio. "
        "Calculate risk margins using cost-of-capital approach and "
        "perform experience variance analysis for key assumptions.",
        stream=True,
    )

def test_structuring_actuarial_functions():
    """Test structuring actuarial functions agent"""
    Structuring_Actuarial_Functions.print_response(
        "Design governance frameworks and operational processes for actuarial functions. "
        "Establish control frameworks for provisioning cycles and "
        "develop regulatory pack assembly procedures.",
        stream=True,
    )

def test_reg_accounting_alignment():
    """Test regulatory and accounting alignment agent"""
    Reg_Accounting_Alignment.print_response(
        "Ensure regulatory compliance and accounting alignment for insurance portfolios. "
        "Support IFRS 17 implementation and Solvency II alignment, "
        "and develop reconciliation frameworks between standards.",
        stream=True,
    )

def test_monitoring_continuous_improvement():
    """Test monitoring and continuous improvement agent"""
    Monitoring_Continuous_Improvement.print_response(
        "Optimize actuarial operations and implement continuous improvement initiatives. "
        "Develop monitoring frameworks for key performance indicators and "
        "establish early warning systems for risk assessment.",
        stream=True,
    )

def test_comprehensive_actuarial_services():
    """Test comprehensive actuarial services team"""
    Inventory_Actuary_Manager_Agent.print_response(
        "Provide comprehensive actuarial services for insurance portfolios. "
        "Coordinate across all actuarial areas: reserve adequacy, behavioral modeling, "
        "profitability analysis, governance, regulatory compliance, and operational excellence.",
        stream=True,
    )

# if __name__ == "__main__":
    #print("Inventory Actuary Module Loaded Successfully!")
    #print("\nAvailable Agents:")
    #print("1. Provisioning_Evaluation_of_Provisions - Reserve adequacy and technical provisions")
    #test_provisioning_evaluation()
    #
    #print("\n2. Behavioral_Analyses - Behavioral modeling and risk assessment")
    #test_behavioral_analyses()
    #
    #print("\n3. Technical_Margins_Analysis - Profitability analysis and risk margins")
    #test_technical_margins()
    #
    #print("\n4. Structuring_Actuarial_Functions - Governance and operational processes")
    #test_structuring_actuarial_functions()
    #
    #print("\n5. Reg_Accounting_Alignment - Regulatory compliance and accounting alignment")
    #test_reg_accounting_alignment()
    #
    #print("\n6. Monitoring_Continuous_Improvement - Operational excellence and continuous improvement")
    #test_monitoring_continuous_improvement()
    #
    # print("\n7. Team: Inventory_Actuary_Manager_Agent - Comprehensive actuarial services coordination")
    # test_comprehensive_actuarial_services()