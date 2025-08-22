from __future__ import annotations
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


kb1 = MarkdownKnowledgeBase(
    path="Knowledge/ActurialModeling.md"
)

import math
import numpy as np
import pandas as pd
from typing import Dict, List, Iterable, Optional

# -----------------------------
# 1) LIFE LIABILITY PROJECTION
# -----------------------------
def project_life_liability(
    policies: pd.DataFrame,
    mortality_table: Dict[int, float],
    discount_curve: Dict[int, float],
    lapse_rate: float = 0.0,
    max_term_years: int = 60,
) -> pd.DataFrame:
    """
    Deterministic expected present value (EPV) for simple life products.
    Assumes annual steps, level premium and level sum assured per policy.
    
    policies columns:
      - PolicyID (str/int)
      - IssueAge (int)
      - Term (int)  # in years
      - SumAssured (float)
      - AnnualPremium (float)
      - Product (str) in {"TermLife","WholeLife","Endowment"}  # WholeLife ignores Term

    mortality_table: dict of age->qx (annual mortality prob)
    discount_curve: dict of t(year)->annual spot rate (continuously compounded not assumed; we use simple 1/(1+r)^t)
    lapse_rate: annual lapse probability applied to in-force each year (constant)
    max_term_years: safety cap

    Returns per policy:
      - PV_Benefits, PV_Premiums, EPV (Benefits - Premiums), Dur_Benefits (Macaulay-like)
    """
    results = []
    for _, row in policies.iterrows():
        pid = row["PolicyID"]
        age0 = int(row["IssueAge"])
        term = int(row["Term"])
        sa = float(row["SumAssured"])
        prem = float(row["AnnualPremium"])
        product = str(row.get("Product", "TermLife"))

        T = term if product in ("TermLife", "Endowment") else max_term_years
        T = min(T, max_term_years)

        surv = 1.0
        pv_ben = 0.0
        pv_prem = 0.0
        dur_weighted_ben = 0.0

        for t in range(1, T + 1):
            age_t = age0 + t - 1
            qx = mortality_table.get(age_t, min(0.999, mortality_table.get(max(mortality_table.keys()), 0.02)))
            lx = lapse_rate
            # Death in year t (approx): surv * qx
            death_prob = surv * qx
            # Premium in year t: paid at start of year t if still in-force at start ~ surv
            prem_prob = surv

            r = discount_curve.get(t, list(discount_curve.values())[-1])
            df = 1.0 / ((1.0 + r) ** t)

            # Benefits
            if product in ("TermLife", "WholeLife"):
                pv_ben += death_prob * sa * df
                dur_weighted_ben += t * death_prob * sa * df
            elif product == "Endowment":
                # death benefit during term; maturity at t==T if survive
                pv_ben += death_prob * sa * df
                if t == T:
                    pv_ben += surv * sa * df
                    dur_weighted_ben += t * surv * sa * df
                else:
                    dur_weighted_ben += t * death_prob * sa * df

            # Premiums (level, paid annually in advance approximation using surv at start)
            pv_prem += prem_prob * prem * df

            # Update survival for next step (no multiple decrements interaction refinement)
            surv *= (1.0 - qx) * (1.0 - lx)

        duration_ben = (dur_weighted_ben / pv_ben) if pv_ben > 0 else np.nan
        results.append({
            "PolicyID": pid,
            "PV_Benefits": pv_ben,
            "PV_Premiums": pv_prem,
            "EPV": pv_ben - pv_prem,
            "Dur_Benefits": duration_ben,
            "Product": product
        })

    return pd.DataFrame(results)


# ------------------------------------
# 2) NON-LIFE RESERVING: CHAIN-LADDER
# ------------------------------------
def chain_ladder_reserving(triangle: pd.DataFrame, tail_factor: Optional[float] = None) -> pd.DataFrame:
    """
    Simple deterministic Chain-Ladder on a cumulative development triangle (paid or reported).
    triangle columns:
      - AccidentYear (int)
      - Dev (int)   # development period number starting at 1
      - CumValue (float)

    Returns:
      DataFrame per AccidentYear with:
        - SelectedFactors (list)
        - Ultimate
        - Latest
        - IBNR = Ultimate - Latest
    """
    # Pivot to AY x Dev matrix
    piv = triangle.pivot(index="AccidentYear", columns="Dev", values="CumValue").sort_index()
    dev_cols = sorted([c for c in piv.columns if pd.notna(c)])
    # Development factors f_k = sum(C_{.,k+1}) / sum(C_{.,k}) across available AYs
    factors = []
    for k in range(len(dev_cols) - 1):
        c_k = piv[dev_cols[k]]
        c_k1 = piv[dev_cols[k + 1]]
        mask = c_k.notna() & c_k1.notna()
        f = c_k1[mask].sum() / max(c_k[mask].sum(), 1e-12)
        factors.append(f)
    if tail_factor is not None:
        factors.append(tail_factor)

    # Project to ultimate
    ultimates = []
    for ay, row in piv.iterrows():
        # latest observed dev col for this AY
        obs = row.dropna()
        if obs.empty:
            continue
        latest_dev = obs.index.max()
        latest_val = obs.loc[latest_dev]
        # multiply the remaining factors from latest_dev position
        start_idx = dev_cols.index(latest_dev)
        prod = 1.0
        for f in factors[start_idx:]:
            prod *= f
        ultimate = latest_val * prod
        ultimates.append({"AccidentYear": ay, "Latest": latest_val, "Ultimate": ultimate, "SelectedFactors": factors})

    out = pd.DataFrame(ultimates)
    out["IBNR"] = out["Ultimate"] - out["Latest"]
    return out


# ---------------------------------------
# 3) PENSION (DB) OBLIGATION & FUNDING
# ---------------------------------------
def calculate_pension_db_obligation(
    members: pd.DataFrame,
    discount_rate: float,
    salary_growth: float,
    retirement_age: int,
    plan_accrual_rate: float = 0.015,
    assets_fair_value: float = 0.0,
    mortality_table: Optional[Dict[int, float]] = None,
) -> Dict[str, float]:
    """
    Very simple PBO approximation for a final-salary DB plan.
    members columns:
      - MemberID, Age (int), ServiceYears (float), Salary (float)

    Benefit at retirement (annual): accrual_rate * FinalSalary * ServiceYears
    PBO: Present value of accrued benefit prorated to date using discount_rate and survival (optional).

    Returns dict with: PBO, Assets, FundingRatio, AvgDuration (rough), ServiceCost (approx).
    """
    pbo = 0.0
    dur_weighted = 0.0
    sc = 0.0  # crude service cost: one extra year of accrual

    for _, m in members.iterrows():
        age = int(m["Age"])
        yrs_to_ret = max(0, retirement_age - age)
        svc = float(m["ServiceYears"])
        sal = float(m["Salary"])
        # Project salary to retirement
        final_sal = sal * ((1.0 + salary_growth) ** yrs_to_ret)
        ann_benefit = plan_accrual_rate * final_sal * svc  # accrued to date
        # Survival probability to retirement (optional mortality)
        if mortality_table:
            surv = 1.0
            for a in range(age, retirement_age):
                qx = mortality_table.get(a, mortality_table.get(max(mortality_table.keys()), 0.01))
                surv *= (1.0 - qx)
        else:
            surv = 1.0
        df = 1.0 / ((1.0 + discount_rate) ** yrs_to_ret)
        pv = ann_benefit * surv * df
        pbo += pv
        dur_weighted += yrs_to_ret * pv
        # Service cost (one more year accrual on same salary path)
        ann_benefit_next = plan_accrual_rate * (sal * ((1.0 + salary_growth) ** (yrs_to_ret - 1 if yrs_to_ret > 0 else 0))) * (svc + 1)
        pv_next = ann_benefit_next * surv * (1.0 / ((1.0 + discount_rate) ** max(yrs_to_ret - 1, 0)))
        sc += max(pv_next - pv, 0.0)

    assets = float(assets_fair_value)
    funding_ratio = assets / pbo if pbo > 0 else np.nan
    avg_duration = (dur_weighted / pbo) if pbo > 0 else np.nan

    return {
        "PBO": pbo,
        "Assets": assets,
        "FundingRatio": funding_ratio,
        "AvgDurationYears": avg_duration,
        "ServiceCostApprox": sc
    }


# -----------------------------------------------------
# 4) SOLVENCY CAPITAL (POISSON-LOGNORMAL SIMULATION)
# -----------------------------------------------------
def simulate_solvency_capital_poisson_lognormal(
    lambda_freq: float,
    sev_mu: float,
    sev_sigma: float,
    sims: int = 100_000,
    confidence: float = 0.995,
    seed: Optional[int] = 42,
) -> Dict[str, float]:
    """
    Economic capital for annual loss modeled as compound Poisson(Lognormal).
    - Frequency ~ Poisson(lambda_freq)
    - Severity ~ Lognormal(mu, sigma) on natural log scale

    Returns VaR, TVaR, MeanLoss.
    """
    rng = np.random.default_rng(seed)
    N = rng.poisson(lambda_freq, size=sims)
    # draw severities efficiently
    losses = np.zeros(sims)
    idx_nonzero = np.where(N > 0)[0]
    if len(idx_nonzero) > 0:
        # expand severities per simulation
        for i in idx_nonzero:
            k = N[i]
            sev = rng.lognormal(mean=sev_mu, sigma=sev_sigma, size=k).sum()
            losses[i] = sev
    mean_loss = float(losses.mean())
    var_level = float(np.quantile(losses, confidence))
    # TVaR (conditional tail expectation)
    tvar = float(losses[losses >= var_level].mean()) if np.any(losses >= var_level) else var_level
    return {"VaR": var_level, "TVaR": tvar, "MeanLoss": mean_loss, "Confidence": confidence}


# --------------------------------------------
# 5) LIGHT ALM: DURATION MISMATCH DIAGNOSTICS
# --------------------------------------------
def _pv_and_duration(cashflows: List[Dict[str, float]], discount_curve: Dict[int, float]) -> Dict[str, float]:
    """
    Helper: cashflows = list of {'t': year_int, 'cf': amount}
    discount_curve: {t: rate}
    Returns PV and Macaulay Duration.
    """
    pv = 0.0
    dur_w = 0.0
    for leg in cashflows:
        t = int(leg["t"])
        cf = float(leg["cf"])
        r = discount_curve.get(t, list(discount_curve.values())[-1])
        df = 1.0 / ((1.0 + r) ** t)
        pv_cf = cf * df
        pv += pv_cf
        dur_w += t * pv_cf
    duration = (dur_w / pv) if pv != 0 else np.nan
    return {"PV": pv, "Duration": duration}

def alm_duration_mismatch(
    asset_cashflows: List[Dict[str, float]],
    liability_cashflows: List[Dict[str, float]],
    discount_curve: Dict[int, float],
) -> Dict[str, float]:
    """
    Compares asset vs liability PV and durations; reports gaps.
    """
    a = _pv_and_duration(asset_cashflows, discount_curve)
    l = _pv_and_duration(liability_cashflows, discount_curve)
    return {
        "PV_Assets": a["PV"],
        "PV_Liabilities": l["PV"],
        "Net_PV": a["PV"] - l["PV"],
        "Dur_Assets": a["Duration"],
        "Dur_Liabilities": l["Duration"],
        "Dur_Gap": (a["Duration"] - l["Duration"]) if (not math.isnan(a["Duration"]) and not math.isnan(l["Duration"])) else np.nan
    }


Actuarial_Model_Developer = Agent(
    name="Actuarial Model Developer",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        alm_duration_mismatch,
        calculate_pension_db_obligation,
        chain_ladder_reserving,
        project_life_liability,
        simulate_solvency_capital_poisson_lognormal,
    ],
    knowledge=kb1, 
    description="""
    The Actuarial Model Developer builds and runs core actuarial models across life, non-life (P&C), pensions,
    solvency capital, and light ALM diagnostics. It applies the knowledge base for standards (e.g., Solvency II,
    IFRS 17), documents assumptions, and returns transparent, reproducible results with key sensitivities.
    """,
    instructions="""
    Follow this route and use the explicit tools:

    Step 0: Data & Assumptions Check
    - Validate inputs (units, cumulative vs incremental triangles, curve tenors).
    - Reference the knowledge base for modeling principles and compliance notes.

    Step 1: Life Liability Projection (EPV)
    - Tool: project_life_liability
    - Input: policies, mortality_table, discount_curve, lapse_rate (if any).
    - Output: PV_Benefits, PV_Premiums, EPV, Dur_Benefits per policy.

    Step 2: Non-Life Reserving (Deterministic)
    - Tool: chain_ladder_reserving
    - Input: cumulative development triangle (AccidentYear, Dev, CumValue), optional tail_factor.
    - Output: Latest, Ultimate, IBNR per AccidentYear and selected factors.

    Step 3: Pension (DB) Obligation & Funding
    - Tool: calculate_pension_db_obligation
    - Input: members, discount_rate, salary_growth, retirement_age, plan_accrual_rate, assets_fair_value, (optional) mortality_table.
    - Output: PBO, Assets, FundingRatio, AvgDurationYears, ServiceCostApprox.

    Step 4: Solvency Capital (Loss Distribution)
    - Tool: simulate_solvency_capital_poisson_lognormal
    - Input: lambda_freq, sev_mu, sev_sigma, sims, confidence.
    - Output: VaR, TVaR, MeanLoss at the specified confidence.

    Step 5: ALM Diagnostics (Duration & PV)
    - Tool: alm_duration_mismatch
    - Input: asset_cashflows, liability_cashflows, discount_curve.
    - Output: PV_Assets, PV_Liabilities, Net_PV, Dur_Assets, Dur_Liabilities, Dur_Gap.

    Step 6: Reporting
    - Summarize results with assumptions and any caveats.
    - Flag data quality issues and compliance considerations from the knowledge base.
    """
)
import json

# --- Step 1: Life sample ---
policies_json = json.dumps([
    {"PolicyID": "P001", "IssueAge": 40, "Term": 20, "SumAssured": 100000, "AnnualPremium": 800, "Product": "TermLife"},
    {"PolicyID": "P002", "IssueAge": 55, "Term": 10, "SumAssured": 50000,  "AnnualPremium": 1200, "Product": "Endowment"}
], indent=4)

mortality_table_json = json.dumps({
    40: 0.0020, 41: 0.0021, 42: 0.0022, 43: 0.0023, 44: 0.0024,
    45: 0.0026, 50: 0.0040, 55: 0.0060, 60: 0.0090, 65: 0.0140, 70: 0.0220, 80: 0.0500
}, indent=4)

discount_curve_json = json.dumps({1: 0.02, 2: 0.022, 3: 0.023, 4: 0.024, 5: 0.025}, indent=4)  # used as flat beyond last key
lapse_rate_json = json.dumps(0.03, indent=4)

# --- Step 2: Non-life triangle (cumulative) ---
triangle_json = json.dumps([
    {"AccidentYear": 2021, "Dev": 1, "CumValue": 120},
    {"AccidentYear": 2021, "Dev": 2, "CumValue": 180},
    {"AccidentYear": 2021, "Dev": 3, "CumValue": 200},
    {"AccidentYear": 2022, "Dev": 1, "CumValue": 130},
    {"AccidentYear": 2022, "Dev": 2, "CumValue": 185},
    {"AccidentYear": 2023, "Dev": 1, "CumValue": 140}
], indent=4)

tail_factor_json = json.dumps(1.03, indent=4)  # optional

# --- Step 3: Pension DB sample ---
members_json = json.dumps([
    {"MemberID": "M1", "Age": 45, "ServiceYears": 15, "Salary": 50000},
    {"MemberID": "M2", "Age": 35, "ServiceYears": 8,  "Salary": 42000},
    {"MemberID": "M3", "Age": 58, "ServiceYears": 25, "Salary": 68000}
], indent=4)

pension_assumptions_json = json.dumps({
    "discount_rate": 0.03,
    "salary_growth": 0.02,
    "retirement_age": 65,
    "plan_accrual_rate": 0.015,
    "assets_fair_value": 1800000
}, indent=4)

# Optional mortality for pension
pension_mortality_json = json.dumps({58:0.009, 59:0.010, 60:0.011, 61:0.012, 62:0.013, 63:0.014, 64:0.015}, indent=4)

# --- Step 4: Solvency capital (compound Poisson-Lognormal) ---
solvency_params_json = json.dumps({
    "lambda_freq": 12.0,
    "sev_mu": 9.0,
    "sev_sigma": 1.0,
    "sims": 20000,
    "confidence": 0.995
}, indent=4)

# --- Step 5: ALM cashflows & curve ---
asset_cfs_json = json.dumps([
    {"t": 1, "cf": 300000},
    {"t": 2, "cf": 250000},
    {"t": 3, "cf": 200000},
    {"t": 4, "cf": 150000},
    {"t": 5, "cf": 100000}
], indent=4)

liability_cfs_json = json.dumps([
    {"t": 1, "cf": 200000},
    {"t": 2, "cf": 220000},
    {"t": 3, "cf": 230000},
    {"t": 4, "cf": 240000},
    {"t": 5, "cf": 250000}
], indent=4)

alm_discount_curve_json = discount_curve_json  # reuse the same curve

# Actuarial_Model_Developer.print_response(
#     f"""
# You are the Actuarial Model Developer. Use the knowledge base and the specified tools exactly as instructed.

# Step 1 — Life Projection (project_life_liability):
# Policies: {policies_json}
# MortalityTable: {mortality_table_json}
# DiscountCurve: {discount_curve_json}
# LapseRate: {lapse_rate_json}

# Step 2 — Non-Life Reserving (chain_ladder_reserving):
# CumulativeTriangle: {triangle_json}
# TailFactor: {tail_factor_json}

# Step 3 — Pension DB Obligation (calculate_pension_db_obligation):
# Members: {members_json}
# Assumptions: {pension_assumptions_json}
# OptionalPensionMortality: {pension_mortality_json}

# Step 4 — Solvency Capital (simulate_solvency_capital_poisson_lognormal):
# Params: {solvency_params_json}

# Step 5 — ALM Diagnostics (alm_duration_mismatch):
# AssetCashflows: {asset_cfs_json}
# LiabilityCashflows: {liability_cfs_json}
# DiscountCurve: {alm_discount_curve_json}

# Deliverables:
# - Key tables for each step (EPV results, Chain-Ladder ultimates/IBNR, Pension PBO & FundingRatio, VaR/TVaR, ALM PV & Duration Gap).
# - State assumptions and any data caveats. Keep it concise and structured.
# """
# )


################## 2end agent ##################

kb2= MarkdownKnowledgeBase(
    path="Knowledge/Pricing_Product_Developer.md"
)


def calculate_life_premium(self, mortality_table, benefits, discount_rate, expenses):
        """
        Calculate technical premium for life insurance products.
        Inputs:
            - mortality_table: dict or DataFrame with mortality rates
            - benefits: dict with benefit amounts per policy
            - discount_rate: float (annual)
            - expenses: dict with acquisition and maintenance costs
        Output:
            - premium: float
        """
        # Placeholder for calculation logic
        premium = sum(benefits.values()) * (1 + sum(expenses.values())) / (1 - discount_rate)
        return premium

def calculate_non_life_premium(self, expected_claims, expense_loading, risk_margin):
        """
        Calculate technical premium for non-life insurance products.
        Inputs:
            - expected_claims: float or array (frequency x severity)
            - expense_loading: float (percentage of claims)
            - risk_margin: float (percentage)
        Output:
            - premium: float
        """
        premium = expected_claims * (1 + expense_loading + risk_margin)
        return premium

def assess_profitability(self, premiums, expected_claims, expenses, capital, roc_target=0.1):
        """
        Evaluate risk-adjusted profitability (ROC, ROE)
        Inputs:
            - premiums: float
            - expected_claims: float
            - expenses: float
            - capital: float
            - roc_target: target return on capital
        Output:
            - profitability_metrics: dict
        """
        net_profit = premiums - expected_claims - expenses
        roc = net_profit / capital
        is_target_met = roc >= roc_target
        return {"net_profit": net_profit, "roc": roc, "target_met": is_target_met}

def sensitivity_analysis(self, base_premium, scenarios):
        """
        Run sensitivity analysis on premiums under different assumptions.
        Inputs:
            - base_premium: float
            - scenarios: dict of {scenario_name: adjustment_factor}
        Output:
            - results: dict of {scenario_name: adjusted_premium}
        """
        results = {}
        for scenario, factor in scenarios.items():
            results[scenario] = base_premium * factor
        return results

def stochastic_simulation(self, base_premium, n_simulations, random_seed=None):
        """
        Simulate premium outcomes under stochastic risk scenarios.
        Inputs:
            - base_premium: float
            - n_simulations: int
            - random_seed: int or None
        Output:
            - simulated_premiums: list of floats
        """
        import random
        if random_seed:
            random.seed(random_seed)
        simulated_premiums = [base_premium * (1 + random.gauss(0, 0.05)) for _ in range(n_simulations)]
        return simulated_premiums

Pricing_Product_Developer = Agent(
    name="Pricing Product Developer",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        calculate_life_premium,
        calculate_non_life_premium,
        assess_profitability,
        sensitivity_analysis,
        stochastic_simulation
    ],
    knowledge=kb2,
    description="""
Designs, prices, and evaluates insurance and financial products to ensure profitability, competitiveness, and compliance. 
It covers life, non-life, and pension products, integrating actuarial assumptions, capital requirements, and market data 
to recommend technical premiums, risk margins, and product adjustments.
""",
    instructions="""
You are the Pricing & Product Developer. Follow these steps, explicitly using the listed tools:

1. **Calculate Technical Premiums**
   - For life insurance products, use `calculate_life_premium`.
   - For non-life insurance products, use `calculate_non_life_premium`.
   - Inputs include mortality tables, claims data, benefits, expenses, and financial assumptions.

2. **Assess Product Profitability**
   - Use `assess_profitability` to compute net profit, ROC, and compare against target returns.
   - Inputs include calculated premiums, expected claims, expenses, and capital requirements.

3. **Perform Sensitivity Analysis**
   - Use `sensitivity_analysis` to test how premiums change under different economic, demographic, or risk assumptions.
   - Inputs include the base premium and a set of scenario adjustment factors.

4. **Run Stochastic Simulations**
   - Use `stochastic_simulation` to model the impact of uncertainty on premiums and profitability.
   - Inputs include base premiums, number of simulations, and optional random seed.

5. **Compare & Recommend**
   - Integrate results from profitability assessment, sensitivity analysis, and stochastic simulations.
   - Provide recommendations for premium adjustments or product design changes.
   - Ensure all recommendations comply with Solvency II, IFRS 17, and local actuarial standards.
"""
)

test_prompt = """
You are the Pricing & Product Developer. Using the following data:

- Life insurance product:
    - Mortality table: LifeTable2024
    - Benefits: $100,000 per policy
    - Discount rate: 3%
    - Expenses: Acquisition 5%, Maintenance 2%
- Non-life insurance product:
    - Expected claims: $500,000
    - Expense loading: 10%
    - Risk margin: 5%
- Capital allocated: $2,000,000
- Sensitivity scenarios:
    - Scenario 1: +10% claims
    - Scenario 2: -5% expenses
    - Scenario 3: +1% discount rate
- Stochastic simulations: 1000 runs, random seed 42

Tasks:

1. **Calculate technical premiums**
   - Use `calculate_life_premium` for the life product.
   - Use `calculate_non_life_premium` for the non-life product.

2. **Assess profitability**
   - Use `assess_profitability` to compute net profit and ROC for both products.
   - Compare ROC against a target of 10%.

3. **Perform sensitivity analysis**
   - Use `sensitivity_analysis` on both life and non-life premiums using the scenarios above.

4. **Run stochastic simulations**
   - Use `stochastic_simulation` on both premiums to evaluate variability under uncertainty.

5. **Provide recommendations**
   - Based on results, recommend adjustments to premiums or product design to ensure profitability, competitiveness, and compliance with Solvency II and IFRS 17.
"""
# Pricing_Product_Developer.print_response(test_prompt)


################# 3rd agent #############

def deterministic_reserve(self, claims_triangle, method="chain_ladder"):
        """
        Calculate reserves using deterministic methods.
        Inputs:
            - claims_triangle: DataFrame or 2D list of claims by origin and development year
            - method: "chain_ladder" or "bornhuetter_ferguson"
        Output:
            - reserve_estimate: float
        """
        # Placeholder logic
        if method == "chain_ladder":
            reserve_estimate = sum(claims_triangle[-1]) * 1.1  # simplified
        elif method == "bornhuetter_ferguson":
            reserve_estimate = sum(claims_triangle[-1]) * 1.05
        return reserve_estimate

def stochastic_reserve(self, claims_triangle, n_simulations=1000, random_seed=None):
        """
        Calculate reserves using stochastic methods (bootstrap, GLM).
        Inputs:
            - claims_triangle: DataFrame or 2D list
            - n_simulations: number of Monte Carlo simulations
            - random_seed: optional seed for reproducibility
        Output:
            - simulated_reserves: list of floats
            - reserve_statistics: dict with mean, std, percentiles
        """
        import random
        if random_seed:
            random.seed(random_seed)
        simulated_reserves = [sum(claims_triangle[-1]) * random.uniform(0.95, 1.15) for _ in range(n_simulations)]
        reserve_statistics = {
            "mean": sum(simulated_reserves)/len(simulated_reserves),
            "std": (sum((x - sum(simulated_reserves)/len(simulated_reserves))**2 for x in simulated_reserves)/len(simulated_reserves))**0.5,
            "5th_percentile": sorted(simulated_reserves)[int(0.05*n_simulations)],
            "95th_percentile": sorted(simulated_reserves)[int(0.95*n_simulations)]
        }
        return simulated_reserves, reserve_statistics

def liability_valuation(self, cash_flows, discount_rate):
        """
        Calculate the present value of liabilities using discounted cash flows.
        Inputs:
            - cash_flows: list of future cash flows
            - discount_rate: annual discount rate (float)
        Output:
            - present_value: float
        """
        present_value = sum(cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cash_flows, start=1))
        return present_value

def experience_study_adjustment(self, observed_data, expected_data, adjustment_factor=1.0):
        """
        Adjust assumptions based on experience studies.
        Inputs:
            - observed_data: actual claims or mortality data
            - expected_data: expected claims or mortality
            - adjustment_factor: scaling factor to update assumptions
        Output:
            - adjusted_assumptions: float
        """
        ratio = sum(observed_data) / sum(expected_data)
        adjusted_assumptions = ratio * adjustment_factor
        return adjusted_assumptions

def prudential_margin(self, best_estimate_reserve, confidence_level=0.75):
        """
        Calculate prudential margin for technical provisions.
        Inputs:
            - best_estimate_reserve: float
            - confidence_level: target confidence (default 75%)
        Output:
            - margin: float
        """
        margin = best_estimate_reserve * (confidence_level / 1.0)  # simple scaling example
        return margin

kb3= MarkdownKnowledgeBase(
    path="Knowledge/Reserving_Liability_Valuation.md"
)
Reserving_Liability_Valuation = Agent(
    name="Reserving & Liability Valuation",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        deterministic_reserve,
        stochastic_reserve,
        liability_valuation,
        experience_study_adjustment,
        prudential_margin
    ],
    knowledge=kb3,
    description="""
Estimates insurance reserves and liabilities for life, non-life, and pension products. 
Calculates best-estimate reserves, prudential margins, and technical provisions while ensuring compliance 
with Solvency II, IFRS 17, and local actuarial standards. Adjusts assumptions based on experience studies 
and integrates stochastic modeling to quantify reserve uncertainty.
""",
    instructions="""
You are the Reserving & Liability Valuation Specialist. Follow these steps using the specified tools:

1. **Deterministic Reserving**
   - Use `deterministic_reserve` to calculate reserves using Chain-Ladder or Bornhuetter-Ferguson methods.
   - Inputs: claims run-off triangles, exposure data, and selected method.

2. **Stochastic Reserving**
   - Use `stochastic_reserve` to estimate reserve variability under uncertainty.
   - Inputs: claims triangles, number of simulations, and optional random seed.

3. **Liability Valuation**
   - Use `liability_valuation` to compute the present value of future liabilities.
   - Inputs: projected cash flows and discount rate.

4. **Experience Study Adjustment**
   - Use `experience_study_adjustment` to update assumptions based on observed vs expected data.
   - Inputs: actual claims or mortality, expected assumptions, and adjustment factor.

5. **Prudential Margin**
   - Use `prudential_margin` to calculate prudential margins on best-estimate reserves for regulatory compliance.
   - Inputs: best-estimate reserve and confidence level.

6. **Reporting & Recommendations**
   - Aggregate results from deterministic and stochastic reserving, liability valuation, and prudential margins.
   - Provide reserve estimates, risk quantification, and regulatory-compliant technical provisions.
"""
)

test_prompt = """
You are the Reserving & Liability Valuation Specialist. Using the following data:

- Non-life claims triangle (in thousands USD):
    [[100, 120, 130, 140],
     [110, 125, 135, None],
     [120, 130, None, None],
     [130, None, None, None]]
- Life insurance projected cash flows (in thousands USD): [50, 55, 60, 65, 70]
- Discount rate: 3%
- Observed mortality vs expected: observed = [10, 12, 11, 13], expected = [9, 11, 10, 12]
- Prudential margin confidence level: 75%
- Stochastic simulations: 1000 runs, random seed = 42

Tasks:

1. **Deterministic Reserving**
   - Use `deterministic_reserve` on the non-life claims triangle with both Chain-Ladder and Bornhuetter-Ferguson methods.

2. **Stochastic Reserving**
   - Use `stochastic_reserve` to estimate reserve variability and provide mean, standard deviation, and 5th/95th percentiles.

3. **Liability Valuation**
   - Use `liability_valuation` to calculate the present value of life insurance projected cash flows.

4. **Experience Study Adjustment**
   - Use `experience_study_adjustment` to update mortality assumptions based on observed vs expected data.

5. **Prudential Margin**
   - Use `prudential_margin` to compute the margin on the best-estimate reserve.

6. **Reporting & Recommendations**
   - Aggregate results and provide reserve estimates, adjusted assumptions, liability valuation, and prudential margins in a clear regulatory-compliant format.
"""
# Reserving_Liability_Valuation.print_response(test_prompt)

############### 4th agent ###########3


def stress_test(self, liability_cash_flows, scenario_shocks):
        """
        Apply stress scenarios to liability cash flows.
        Inputs:
            - liability_cash_flows: list of floats (future cash flows)
            - scenario_shocks: dict of {scenario_name: shock_factor or function}
        Output:
            - stressed_results: dict of {scenario_name: stressed_cash_flows}
        """
        stressed_results = {}
        for scenario, shock in scenario_shocks.items():
            if callable(shock):
                stressed_results[scenario] = [shock(cf) for cf in liability_cash_flows]
            else:
                stressed_results[scenario] = [cf * shock for cf in liability_cash_flows]
        return stressed_results

def monte_carlo_simulation(self, base_cash_flows, n_simulations=1000, volatility=0.05, random_seed=None):
        """
        Run Monte Carlo simulations for liability cash flows under uncertainty.
        Inputs:
            - base_cash_flows: list of floats
            - n_simulations: number of Monte Carlo runs
            - volatility: standard deviation of shocks
            - random_seed: optional seed for reproducibility
        Output:
            - simulated_flows: list of lists, each inner list is a simulated cash flow path
        """
        import random
        if random_seed:
            random.seed(random_seed)
        simulated_flows = []
        for _ in range(n_simulations):
            simulated_flows.append([cf * (1 + random.gauss(0, volatility)) for cf in base_cash_flows])
        return simulated_flows

def aggregate_risks(self, risk_components, correlation_matrix=None):
        """
        Aggregate individual risk components into overall risk metrics.
        Inputs:
            - risk_components: dict of {risk_name: numeric exposure or capital requirement}
            - correlation_matrix: dict of dicts {risk_i: {risk_j: correlation}}
        Output:
            - total_risk: float
        """
        import math
        risks = list(risk_components.values())
        if correlation_matrix:
            # Simple approximation using correlations
            total_variance = 0
            keys = list(risk_components.keys())
            for i in range(len(keys)):
                for j in range(len(keys)):
                    corr = correlation_matrix.get(keys[i], {}).get(keys[j], 0 if i != j else 1)
                    total_variance += risks[i] * risks[j] * corr
            total_risk = math.sqrt(total_variance)
        else:
            total_risk = sum(risks)
        return total_risk

def scenario_analysis_summary(self, stressed_results):
        """
        Summarize stress test or Monte Carlo results.
        Inputs:
            - stressed_results: dict of {scenario_name: list of cash flows or simulations}
        Output:
            - summary: dict of {scenario_name: metrics (mean, min, max, percentiles)}
        """
        summary = {}
        for scenario, flows in stressed_results.items():
            flat = flows if isinstance(flows[0], (int, float)) else [sum(path) for path in flows]
            sorted_flows = sorted(flat)
            summary[scenario] = {
                "mean": sum(flat)/len(flat),
                "min": min(flat),
                "max": max(flat),
                "5th_percentile": sorted_flows[int(0.05*len(sorted_flows))],
                "95th_percentile": sorted_flows[int(0.95*len(sorted_flows))]
            }
        return summary

kb4 = MarkdownKnowledgeBase(
    path="Knowledge/Risk_Scenario_Tester.md"
)

Risk_Scenario_Tester = Agent(
    name="Risk & Scenario Tester",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        stress_test,
        monte_carlo_simulation,
        aggregate_risks,
        scenario_analysis_summary
    ],
    knowledge=kb4,
    description="""
Assesses actuarial and financial risks under stress and stochastic scenarios. 
It performs scenario-based stress tests, Monte Carlo simulations, and risk aggregation 
to evaluate capital adequacy, solvency, and overall resilience. 
Supports ERM and ORSA reporting with actionable risk insights.
""",
    instructions="""
You are the Risk & Scenario Tester. Follow these steps using the specified tools:

1. **Stress Testing**
   - Use `stress_test` to apply regulatory or internal stress scenarios to liability cash flows.
   - Inputs: liability cash flows and scenario shocks (market, demographic, or catastrophic).

2. **Monte Carlo Simulation**
   - Use `monte_carlo_simulation` to model uncertainty in liabilities or cash flows.
   - Inputs: base cash flows, number of simulations, volatility, and optional random seed.

3. **Risk Aggregation**
   - Use `aggregate_risks` to combine individual risk components into an overall risk metric.
   - Inputs: individual risk exposures and optional correlation matrix.

4. **Scenario Analysis Summary**
   - Use `scenario_analysis_summary` to summarize stress test and Monte Carlo results.
   - Outputs include mean, min, max, and percentiles for each scenario.

5. **Reporting & Recommendations**
   - Integrate all results to identify vulnerabilities, key risk drivers, and potential capital impacts.
   - Provide insights for solvency, ORSA reporting, and risk mitigation strategies.
"""
)
test_prompt = """
You are the Risk & Scenario Tester. Using the following data:

- Liability cash flows (in thousands USD): [100, 110, 120, 130, 140]
- Stress scenarios:
    - Market shock: equity drop 20% -> apply factor 1.2 to cash flows
    - Interest rate shock: +1% -> apply factor 0.98
    - Pandemic shock: mortality increase 10% -> apply factor 1.1
- Monte Carlo simulation:
    - 1000 runs
    - Volatility: 5%
    - Random seed: 42
- Risk components (in thousands USD): 
    - Market risk: 500
    - Credit risk: 300
    - Operational risk: 200
- Correlation matrix:
    Market-Credit: 0.3
    Market-Operational: 0.2
    Credit-Operational: 0.1

Tasks:

1. **Stress Testing**
   - Use `stress_test` to apply the scenarios to liability cash flows and calculate stressed cash flows.

2. **Monte Carlo Simulation**
   - Use `monte_carlo_simulation` to model variability in liability cash flows and produce simulated paths.

3. **Risk Aggregation**
   - Use `aggregate_risks` to combine individual risk components into an overall risk metric, applying the correlation matrix.

4. **Scenario Analysis Summary**
   - Use `scenario_analysis_summary` to summarize results from stress tests and Monte Carlo simulations.
   - Provide mean, min, max, 5th percentile, and 95th percentile for each scenario.

5. **Reporting & Recommendations**
   - Aggregate all results and provide insights on capital impact, solvency, and potential vulnerabilities.
   - Suggest risk mitigation actions if applicable.
"""
Risk_Scenario_Tester.print_response(test_prompt)

############ 5th agent  #########


def back_testing(self, model_outputs, actuals):
        """
        Compare model outputs against actual observed data to assess accuracy.
        Inputs:
            - model_outputs: list of predicted values
            - actuals: list of observed values
        Output:
            - metrics: dict with MAE, RMSE, and percentage error
        """
        import math
        n = len(model_outputs)
        errors = [model_outputs[i] - actuals[i] for i in range(n)]
        mae = sum(abs(e) for e in errors) / n
        rmse = math.sqrt(sum(e**2 for e in errors) / n)
        pct_error = sum(abs(e)/actuals[i] for i, e in enumerate(errors)) / n * 100
        return {"MAE": mae, "RMSE": rmse, "PctError": pct_error}

def benchmarking(self, model_results, peer_results):
        """
        Compare model outputs against industry peers or historical benchmarks.
        Inputs:
            - model_results: list of model predictions or metrics
            - peer_results: list of peer or historical metrics
        Output:
            - comparison: dict with mean difference, max deviation, and benchmarking score
        """
        n = len(model_results)
        differences = [model_results[i] - peer_results[i] for i in range(n)]
        mean_diff = sum(differences)/n
        max_dev = max(abs(d) for d in differences)
        benchmarking_score = 100 - (max_dev / max(peer_results)) * 100  # scaled score
        return {"MeanDiff": mean_diff, "MaxDeviation": max_dev, "BenchmarkScore": benchmarking_score}

def model_governance_tracker(self, model_inventory, last_validation_dates, validation_frequency_days=365):
        """
        Track model validation schedules and governance status.
        Inputs:
            - model_inventory: list of model names
            - last_validation_dates: list of datetime objects corresponding to last validation
            - validation_frequency_days: int, expected validation interval
        Output:
            - governance_status: dict {model_name: "Valid", "Due", "Overdue"}
        """
        from datetime import datetime, timedelta
        governance_status = {}
        today = datetime.today()
        for model, last_date in zip(model_inventory, last_validation_dates):
            next_validation = last_date + timedelta(days=validation_frequency_days)
            if next_validation > today:
                governance_status[model] = "Valid"
            elif next_validation == today:
                governance_status[model] = "Due"
            else:
                governance_status[model] = "Overdue"
        return governance_status

def model_risk_indicators(self, model_outputs, historical_outputs):
        """
        Calculate model risk indicators such as drift and instability.
        Inputs:
            - model_outputs: list of current predictions
            - historical_outputs: list of past predictions
        Output:
            - risk_metrics: dict with drift, volatility, and stability score
        """
        import statistics
        differences = [model_outputs[i] - historical_outputs[i] for i in range(len(model_outputs))]
        drift = sum(differences)/len(differences)
        volatility = statistics.stdev(differences)
        stability_score = max(0, 100 - volatility)  # higher is more stable
        return {"Drift": drift, "Volatility": volatility, "StabilityScore": stability_score}

kb5 = MarkdownKnowledgeBase(
    path="Knowledge/Model_Validation_Governance.md"
)



Model_Validation_Governance = Agent(
    name="Model Validation & Governance",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[
        back_testing,
        benchmarking,
        model_governance_tracker,
        model_risk_indicators
    ],
    knowledge=kb5,
    description="""
Ensures actuarial and financial models are accurate, robust, and compliant with regulatory 
and professional standards. Performs back-testing, benchmarking, and monitors model risk 
(drift, volatility, instability). Maintains model governance through validation schedules, 
documentation, and audit-ready reporting.
""",
    instructions="""
You are the Model Validator & Governance Specialist. Follow these steps using the specified tools:

1. **Back-Testing**
   - Use `back_testing` to compare model outputs against actual observed data.
   - Inputs: predicted values and corresponding actuals.
   - Outputs: MAE, RMSE, and percentage error metrics.

2. **Benchmarking**
   - Use `benchmarking` to compare model outputs against industry peers or historical benchmarks.
   - Inputs: model results and peer/historical results.
   - Outputs: mean difference, maximum deviation, and benchmarking score.

3. **Model Governance Tracking**
   - Use `model_governance_tracker` to monitor validation schedules and compliance status.
   - Inputs: model inventory, last validation dates, and validation frequency.
   - Outputs: governance status for each model ("Valid", "Due", "Overdue").

4. **Model Risk Indicators**
   - Use `model_risk_indicators` to calculate drift, volatility, and stability of model outputs over time.
   - Inputs: current model outputs and historical outputs.
   - Outputs: drift, volatility, stability score.

5. **Reporting & Recommendations**
   - Aggregate results from back-testing, benchmarking, governance, and risk indicators.
   - Identify model risks, regulatory compliance issues, and recommend corrective actions.
   - Document findings for audit readiness and governance logs.
"""
)

test_prompt = """
You are the Model Validator & Governance Specialist. Using the following data:

- Model outputs (predicted values in thousands USD): [100, 105, 110, 115, 120]
- Actual observed values: [102, 107, 108, 116, 121]
- Peer model results for benchmarking: [101, 106, 109, 114, 119]
- Model inventory: ["LifeModel1", "NonLifeModelA", "PensionModelX"]
- Last validation dates: [2024-08-01, 2024-07-15, 2024-06-30] (datetime objects)
- Validation frequency: 365 days
- Historical model outputs for risk indicators: [99, 104, 109, 113, 118]

Tasks:

1. **Back-Testing**
   - Use `back_testing` to assess model accuracy by comparing model outputs against actuals.
   - Provide MAE, RMSE, and percentage error.

2. **Benchmarking**
   - Use `benchmarking` to compare model outputs against peer results.
   - Provide mean difference, maximum deviation, and benchmarking score.

3. **Model Governance Tracking**
   - Use `model_governance_tracker` to evaluate validation schedules and governance status.
   - Output which models are "Valid", "Due", or "Overdue".

4. **Model Risk Indicators**
   - Use `model_risk_indicators` to assess drift, volatility, and stability compared to historical outputs.
   - Output drift, volatility, and stability score.

5. **Reporting & Recommendations**
   - Aggregate all results into a validation report.
   - Identify any model risks, governance issues, or compliance gaps.
   - Recommend corrective actions and document for audit readiness.
"""
# Model_Validation_Governance.print_response(test_prompt)

