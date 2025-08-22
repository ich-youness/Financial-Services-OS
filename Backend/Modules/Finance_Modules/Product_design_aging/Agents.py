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
import json
from agno.knowledge.markdown import MarkdownKnowledgeBase

load_dotenv()

kb1= MarkdownKnowledgeBase(
    path="Knowledge/agent1.md"
)

def demographic_projection_tool(
    country: str = None,
    metric: str = "OldAgeDependencyRatio",
    start_year: int = 2020,
    end_year: int = 2050,
    csv_path: str = "Data/agent1.csv"
) -> str:
    """
    Analyze demographic projections from a CSV dataset.

    Args:
        country (str, optional): Filter results for a specific country. Defaults to None (all countries).
        metric (str): The demographic metric to analyze.
                      Options: Population_65plus, LifeExpectancy, OldAgeDependencyRatio, PensionCoverageRate
        start_year (int): Starting year of analysis. Defaults to 2020.
        end_year (int): Ending year of analysis. Defaults to 2050.
        csv_path (str): Path to CSV file containing demographic data.

    Returns:
        str: JSON string with filtered and projected demographic data.
    """
    try:
        # Load data
        df = pd.read_csv(csv_path)

        # Filter by years
        df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

        # Filter by country
        if country:
            df = df[df["Country"].str.lower() == country.lower()]

        # Select relevant columns
        if metric not in df.columns:
            return json.dumps({"error": f"Invalid metric '{metric}'"})
        
        result = df[["Country", "Year", metric]].to_dict(orient="records")

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})

Market_Demographic_Analysis=Agent(
    name="Market & Demographic Analysis",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    reasoning=True,
    stream=True,
    tools=[ExaTools(),
           ScrapeGraphTools(),
           demographic_projection_tool,  # add your custom tool
    ],
    knowledge=kb1,     
    description="""\
    An expert agent specialized in understanding global aging population dynamics,
    retirement readiness, and customer behavior. 
    It focuses on demographic projections, pension gaps, and behavioral economics 
    insights relevant to aging societies.
    """,
    instructions="""\
    You are responsible for analyzing and interpreting demographic and market trends 
    related to aging populations. Your outputs should provide insights useful for 
    designing financial and insurance products for retirees, pre-retirees, and 
    dependent elderly groups.

    Guidelines:
    - Use the knowledge base (OECD, UN, World Bank, insurance reports) for context.
    - Apply tools when relevant:
        * ExaTools → retrieve fresh market/demographic research.
        * ScrapeGraphTools → extract structured insights from reports.
        * demographic_projection_tool → query structured CSV projections.
    - Always provide both a *data-driven explanation* and a *strategic implication* 
      for product design or financial planning.
    - Highlight key risks (longevity risk, pension adequacy, healthcare costs).
    - Highlight opportunities (new insurance needs, investment-linked retirement solutions).
    - When unsure, reason step by step and explain assumptions clearly.
    """,
)

# Market_Demographic_Analysis.print_response(
#     "Using the demographic projections and OECD/UN aging population reports, analyze the expected impact of an aging population on insurance product demand over the next 10 years. Include quantitative insights from the CSV data (life expectancy, retirement age, dependency ratios) and qualitative insights from the knowledge base."
# )

########### 2end agent #############

kb2=MarkdownKnowledgeBase(
    path="Knowledge/agent2.md"
)

# custom_tools.py (or inline with your agent file)

import json
from textwrap import dedent
from typing import List, Dict, Any, Optional

def ProductBlueprintTool(
    customer_type: str,
    product_class: str,
    risk_profile: str = "moderate",
    target_age: Optional[int] = None,
    income_need: str = "medium",     # "low" | "medium" | "high"
    inflation_protection: bool = True,
    longevity_risk_concern: bool = True,
    health_status: str = "average",  # "good" | "average" | "impaired"
    budget_level: str = "medium",    # "low" | "medium" | "high"
    region: str = "generic",
    objectives: Optional[List[str]] = None
) -> str:
    """
    Generate a structured insurance product blueprint tailored to aging populations.

    Args:
        customer_type (str): One of ["pre-retiree", "retiree", "elderly_with_health_issues", "group/employer"].
        product_class (str): One of ["pension", "annuity_immediate", "annuity_deferred",
                                     "annuity_variable", "ltc", "hybrid_life_ltc",
                                     "group_pension", "innovative_flex_drawdown"].
        risk_profile (str): "conservative" | "moderate" | "aggressive".
        target_age (int, optional): Representative customer age; used for ranges & pricing hints.
        income_need (str): "low" | "medium" | "high" (decumulation need).
        inflation_protection (bool): Whether to include CPI/capped escalation features.
        longevity_risk_concern (bool): Whether to emphasize lifetime guarantees.
        health_status (str): "good" | "average" | "impaired" (affects LTC/underwriting flags).
        budget_level (str): "low" | "medium" | "high" (affects premium type & guarantees).
        region (str): Jurisdiction tag (e.g., "EU", "US", "JP", "MENA", "generic").
        objectives (List[str], optional): e.g., ["capital_preservation","income_stability","legacy","tax_efficiency"].

    Returns:
        str: JSON-encoded product blueprint with structure, guarantees, riders, ops & compliance hints.
    """

    # ----------------------------
    # Helper maps & small engines
    # ----------------------------
    def age_band(age: Optional[int], default: str) -> str:
        if age is None:
            return default
        if age < 45: return "35-45"
        if age < 55: return "45-55"
        if age < 65: return "55-65"
        if age < 75: return "65-75"
        return "75-85"

    def default_premium_type(prod: str, budget: str) -> str:
        if prod in ["annuity_immediate"]:
            return "Lump Sum"
        if prod in ["annuity_deferred", "pension", "group_pension"]:
            return "Fixed" if budget != "low" else "Flexible"
        if prod in ["ltc", "hybrid_life_ltc", "innovative_flex_drawdown"]:
            return "Annual" if budget != "low" else "Usage-Based"
        if prod == "annuity_variable":
            return "Variable"
        return "Flexible"

    def base_guarantees(prod: str, longevity: bool, inflation: bool) -> List[str]:
        g = []
        if prod.startswith("annuity") or prod in ["pension","group_pension","innovative_flex_drawdown"]:
            if longevity: g.append("Guaranteed lifetime income")
        if inflation:
            g.append("Inflation-linked escalation (CPI or capped)")
        if prod in ["annuity_deferred","pension","group_pension"]:
            g.append("Guaranteed Minimum Income Benefit (GMIB)")
        if prod == "annuity_variable":
            g.append("Capital protection floor on annuity units")
        if prod == "ltc":
            g.append("Benefit triggers: ADL/cognitive impairment")
        if prod == "hybrid_life_ltc":
            g.append("Accelerated death benefit for LTC")
        return g

    def suggest_riders(prod: str, risk: str, health: str, income_need: str) -> List[str]:
        r = []
        if prod.startswith("annuity"):
            if income_need == "high":
                r.append("Period certain (10-20y)")
            r.append("Joint & survivor (50%-100%)")
            r.append("Impaired life annuity underwriting (if eligible)")
        if prod in ["pension","group_pension","innovative_flex_drawdown"]:
            r.append("Longevity protection rider (late-life boost)")
            if risk != "aggressive":
                r.append("Capital preservation lock-in")
        if prod in ["ltc","hybrid_life_ltc"]:
            r.extend(["Waiver of premium","Return of premium on death (optional)"])
            if health != "good":
                r.append("Benefit step-up with waiting period")
        return r

    def model_allocation(prod: str, risk: str) -> Dict[str, float]:
        # simplistic glide/allocation suggestion
        if prod in ["annuity_immediate","ltc","hybrid_life_ltc"]:
            return {"Fixed Income": 75.0, "Alternatives": 10.0, "Equities": 15.0}
        if prod in ["annuity_deferred","pension","group_pension"]:
            if risk == "conservative":
                return {"Fixed Income": 65.0, "Equities": 25.0, "Alternatives": 10.0}
            if risk == "moderate":
                return {"Fixed Income": 50.0, "Equities": 40.0, "Alternatives": 10.0}
            return {"Fixed Income": 35.0, "Equities": 55.0, "Alternatives": 10.0}
        if prod == "annuity_variable":
            return {"Fixed Income": 30.0, "Equities": 60.0, "Alternatives": 10.0}
        if prod == "innovative_flex_drawdown":
            return {"Fixed Income": 45.0, "Equities": 45.0, "Alternatives": 10.0}
        return {"Fixed Income": 50.0, "Equities": 40.0, "Alternatives": 10.0}

    def indicative_pricing_hint(prod: str, age: Optional[int], risk: str, inflation: bool) -> Dict[str, Any]:
        # Not actuarial pricing—just guardrails to help product designers compare levers.
        # "premium_factor" ~ relative cost intensity (1.0 baseline).
        base = 1.0
        if prod in ["ltc","hybrid_life_ltc"]: base += 0.35
        if prod.startswith("annuity"): base += 0.15
        if prod == "annuity_variable" and risk == "aggressive": base += 0.10
        if inflation: base += 0.10
        if age and age >= 70 and prod.startswith("annuity"): base += 0.05  # higher late-age payout factor
        return {
            "premium_factor": round(base, 2),
            "notes": "Heuristic guidance only; use actuarial models for pricing & reserving."
        }

    def ifrs17_hint(prod: str) -> Dict[str, str]:
        if prod in ["ltc","hybrid_life_ltc"]:
            return {"measurement_model": "GMM", "notes": "Long-duration with significant insurance risk; check investment component split."}
        if prod.startswith("annuity") or prod in ["pension","group_pension","innovative_flex_drawdown"]:
            return {"measurement_model": "GMM", "notes": "Guarantee-heavy; assess discount rates, risk adjustment, and CSM amortization."}
        return {"measurement_model": "Assess", "notes": "Confirm contract boundary & renewability (PAA may apply if short-dur)."}

    def solvency_focus(prod: str) -> List[str]:
        f = ["Longevity risk", "Interest rate risk"]
        if prod in ["annuity_variable","pension","group_pension","innovative_flex_drawdown"]:
            f.append("Market risk (equity spread)")
        if prod in ["ltc","hybrid_life_ltc"]:
            f.append("Morbidity risk")
            f.append("Expense inflation risk")
        return f

    def distribution_suggestion(prod: str) -> List[str]:
        if prod in ["pension","group_pension"]:
            return ["Bancassurance", "Corporate partnerships", "Digital workplace portals"]
        if prod.startswith("annuity"):
            return ["Financial advisors/brokers", "Direct-to-consumer with guided advice"]
        if prod in ["ltc","hybrid_life_ltc"]:
            return ["Advisors/brokers", "Healthcare partnerships", "Insurer direct"]
        if prod == "innovative_flex_drawdown":
            return ["Robo-advice platforms", "Bancassurance", "Advisors"]
        return ["Advisors", "Bank channels"]

    def underwriting_hint(prod: str, health: str) -> str:
        if prod in ["ltc","hybrid_life_ltc"]:
            return "Medical underwriting with focus on chronic conditions, ADLs, cognitive screening."
        if prod.startswith("annuity"):
            return "Light financial & mortality underwriting; impaired-life annuity route if applicable."
        if prod in ["pension","group_pension","innovative_flex_drawdown"]:
            return "Financial suitability & KYC/AML; typically non-medical."
        return "Standard KYC/AML and affordability checks."

    # ----------------------------
    # Validation & normalization
    # ----------------------------
    customer_type = customer_type.lower().replace(" ", "_")
    product_class = product_class.lower().replace(" ", "_")
    risk_profile = risk_profile.lower()

    valid_customers = {"pre-retiree","retiree","elderly_with_health_issues","group/employer","group_employer","group"}
    valid_products = {
        "pension","annuity_immediate","annuity_deferred","annuity_variable",
        "ltc","hybrid_life_ltc","group_pension","innovative_flex_drawdown"
    }
    valid_risks = {"conservative","moderate","aggressive"}

    # Map group variants
    if customer_type in {"group/employer","group_employer","group"}:
        customer_type = "group_employer"

    errors = []
    if customer_type not in valid_customers:
        errors.append(f"Invalid customer_type: {customer_type}")
    if product_class not in valid_products:
        errors.append(f"Invalid product_class: {product_class}")
    if risk_profile not in valid_risks:
        errors.append(f"Invalid risk_profile: {risk_profile}")
    if errors:
        return json.dumps({"error": True, "messages": errors}, indent=2)

    # ----------------------------
    # Build blueprint core
    # ----------------------------
    age_range = {
        "pre-retiree": age_band(target_age, "45-60"),
        "retiree": age_band(target_age, "60-80"),
        "elderly_with_health_issues": age_band(target_age, "70-85"),
        "group_employer": "Workforce coverage (18-70)",
    }[customer_type]

    premium_type = default_premium_type(product_class, budget_level)
    guarantees = base_guarantees(product_class, longevity_risk_concern, inflation_protection)
    riders = suggest_riders(product_class, risk_profile, health_status, income_need)
    allocation = model_allocation(product_class, risk_profile)
    pricing_hint = indicative_pricing_hint(product_class, target_age, risk_profile, inflation_protection)
    ifrs17 = ifrs17_hint(product_class)
    solvency = solvency_focus(product_class)
    distribution = distribution_suggestion(product_class)
    underwriting = underwriting_hint(product_class, health_status)

    # Name synthesis
    name_parts = {
        "pension": "Lifetime Pension Plan",
        "annuity_immediate": "Immediate Income Annuity",
        "annuity_deferred": "Deferred Income Annuity",
        "annuity_variable": "Participating/Variable Annuity",
        "ltc": "Comprehensive LTC Insurance",
        "hybrid_life_ltc": "Hybrid Life + LTC",
        "group_pension": "Employer DC/Hybrid Pension",
        "innovative_flex_drawdown": "Flexible Retirement Drawdown",
    }
    product_name = name_parts[product_class]

    # Coverage synthesis
    coverage_map = {
        "pension": "Guaranteed lifetime income post-retirement",
        "annuity_immediate": "Immediate lifetime income starting at purchase",
        "annuity_deferred": "Lifetime income starting at selected deferral date",
        "annuity_variable": "Income linked to investment performance with floors",
        "ltc": "Daily/monthly benefit for home care, assisted living, nursing",
        "hybrid_life_ltc": "Life insurance with accelerated LTC benefits",
        "group_pension": "Employer-sponsored retirement accumulation & annuitization options",
        "innovative_flex_drawdown": "Systematic withdrawals with longevity rider options",
    }

    # Investment & de-risking levers
    derisking = {
        "glidepath": "Age-based equity de-risking (e.g., equity -10% per decade post 55).",
        "hedging": "ALM with duration matching; optional longevity reinsurance for tails.",
        "inflation": "CPI-linked or capped escalation; mix of ILBs/TIPS where available."
    }

    # Surrender/fees/ops
    fees = {
        "management": "0.40%-1.20% p.a. depending on complexity",
        "rider": "0.10%-0.60% p.a. for add-on guarantees/riders",
        "surrender": "Declining surrender charge 5%→0% over 5 years (if applicable)"
    }
    surrender_rules = "Early surrender may reduce benefits; MVA may apply for interest rate shifts."

    # KPIs for monitoring
    kpis = [
        "NBM (New Business Margin)",
        "IRR (Internal Rate of Return)",
        "EV/VNB (Embedded Value / Value of New Business)",
        "Persistency (13m/25m/37m)",
        "Claims ratio (for LTC/hybrid)",
        "Capital strain (Solvency coverage ratio)"
    ]

    blueprint: Dict[str, Any] = {
        "meta": {
            "region": region,
            "customer_type": customer_type,
            "product_class": product_class,
            "risk_profile": risk_profile,
            "target_age_range": age_range,
            "objectives": objectives or ["income_stability","capital_preservation"],
        },
        "product": {
            "product_id": None,  # fill when persisted
            "product_name": product_name,
            "category": product_class,
            "premium_type": premium_type,
            "coverage": coverage_map[product_class],
            "guarantees": guarantees,
            "optional_riders": riders,
            "investment_allocation": allocation,
            "de_risking": derisking,
            "fees": fees,
            "surrender_rules": surrender_rules,
        },
        "ops": {
            "underwriting": underwriting,
            "distribution": distribution,
            "policy_admin": [
                "Support long-duration contracts",
                "Benefit escalation logic (inflation/cap)",
                "Annuitization options & switch windows",
                "Claims workflows (for LTC/hybrid)"
            ],
        },
        "compliance": {
            "ifrs17": ifrs17,
            "solvency_focus": solvency,
            "consumer_protection": [
                "Clear disclosure of guarantees, escalation caps",
                "Transparent conversion/annuitization factors",
                "LTC exclusions, waiting periods, inflation adjustments"
            ],
        },
        "analytics": {
            "pricing_hint": pricing_hint,
            "sensitivity_levers": [
                "Interest rates / discount curve",
                "Longevity improvement",
                "Expense & claims inflation",
                "Equity/credit shocks (if participating/variable)"
            ],
            "target_kpis": kpis,
        },
        "versioning": {
            "status": "draft",
            "notes": "Auto-generated blueprint—use actuarial & compliance tools for validation.",
        }
    }

    return json.dumps(blueprint, indent=2)

Product_Design_Aging_Insurance = Agent(
    name="Product Design for Aging Insurance",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    
    stream=True,
    tools=[
        ProductBlueprintTool,     # ⬅️ add this
        FileTools(),              # to save versions/blueprints if you need
        CalculatorTools(),        # quick calcs during design tradeoffs
        ReasoningTools(),         # structured reasoning
    ],
    knowledge=kb2, # your markdown KB for agent 2
    description="Designs retirement income, annuity, LTC, hybrid and group products for aging populations.",
    instructions=dedent(""" 
You are the **Product Design for Aging Insurance Agent**.  
Your role is to **create and optimize insurance products tailored to aging populations**.  
You must integrate **knowledge base references** with **data analysis** and **custom tool outputs**.  

📚 Knowledge Base:  
- OECD, UN, World Bank reports on global aging demographics.  
- Insurance industry whitepapers on pensions, annuities, and long-term care (LTC).  
- Regulatory frameworks (IFRS 17, Solvency II) impacting insurance product design.  
- Historical mortality/morbidity tables for senior populations.  

📊 Data (CSV):  
Use the dataset `Data/agent2.csv` which contains:  
- Product_Type (Annuity, LTC, Pension, Hybrid)  
- Avg_Premium  
- Claims_Experience  
- Persistency_Rate  
- Target_Age_Group  
- Risk_Factors  

🛠️ Tools to Use:  
1. **ProductBlueprintTool** → Generate structured product blueprints (JSON-like specs).  
2. **FileTools** → Load, parse, and filter the CSV data for insights.  
3. **CalculatorTools** → Perform pricing, risk, and premium adequacy calculations.  
4. **ReasoningTools** → Apply actuarial and strategic reasoning to validate recommendations.  

🎯 Your Tasks:  
- Use the knowledge base to align product design with **global aging trends** and **regulatory requirements**.  
- Use the CSV data to identify **premium adequacy**, **claims experience patterns**, and **persistency insights**.  
- Generate one or more **ProductBlueprintTool outputs** describing new product ideas or optimizations.  
- Justify each recommendation with both **qualitative (knowledge base)** and **quantitative (data)** evidence.  
"""),
markdown=True
)

# Product_Design_Aging_Insurance.print_response(
#     "Design a new retirement-focused insurance product for a rapidly aging population in Asia. "
#     "Use the ProductBlueprintTool to draft the JSON blueprint structure, referencing the demographic, "
#     "claims, and persistency data (CSV: aging_insurance_products.csv). "
#     "Incorporate actuarial assumptions from historical claims trends and align with best practices from "
#     "the knowledge base (OECD, UN aging reports; insurance whitepapers on pensions/annuities/LTC; "
#     "IFRS 17, Solvency II regulatory guidelines). "
#     "Ensure the product structure includes: premium structure, coverage details, benefit triggers, "
#     "risk factors, and compliance considerations."
# )

########## 3rd agent #############

kb3 = MarkdownKnowledgeBase(
    path= "Knowledge/agent3.md"
)
# actuarial_modeling_tool.py
import json
import pandas as pd

def ActuarialModelingTool(
    product: str = None,
    metric: str = "LossRatio",
    start_year: int = 2015,
    end_year: int = 2020,
    csv_path: str = "Data/agent3.csv"
) -> str:
    """
    Perform actuarial analysis on historical claims & persistency data.

    Args:
        product (str, optional): Filter results for a specific insurance product
                                 (e.g., 'Whole Life', 'Annuity', 'Health').
                                 Defaults to None (all products).
        metric (str): The actuarial metric to calculate.
                      Options: LossRatio, PersistencyRate, ClaimsSeverity, ClaimsFrequency.
        start_year (int): Starting year of analysis. Defaults to 2015.
        end_year (int): Ending year of analysis. Defaults to 2020.
        csv_path (str): Path to CSV file with historical claims & persistency data.

    Returns:
        str: JSON string with computed actuarial results.
    """
    try:
        # Load dataset
        df = pd.read_csv(csv_path)

        # Filter by years
        df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

        # Filter by product
        if product:
            df = df[df["Product"].str.lower() == product.lower()]

        # Calculate requested metric
        results = []
        for _, row in df.iterrows():
            record = {"Year": int(row["Year"]), "Product": row["Product"]}
            
            if metric == "LossRatio":
                record["LossRatio"] = round(row["Claims_Paid"] / row["Premiums_Collected"], 4)
            elif metric == "PersistencyRate":
                record["PersistencyRate"] = row["Persistency_Rate"]
            elif metric == "ClaimsSeverity":
                record["ClaimsSeverity"] = round(row["Claims_Paid"] / row["Claims_Count"], 2) if row["Claims_Count"] > 0 else None
            elif metric == "ClaimsFrequency":
                record["ClaimsFrequency"] = round(row["Claims_Count"] / row["Policy_Count"], 4) if row["Policy_Count"] > 0 else None
            else:
                return json.dumps({"error": f"Invalid metric '{metric}'"}, indent=2)

            results.append(record)

        return json.dumps(results, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})

Actuarial_Financial_Modeling = Agent(
    name="Actuarial & Financial Modeling",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    stream=True,
    markdown=True,
    tools=[
        ActuarialModelingTool,
        FileTools(),              
        CalculatorTools(),        
        ReasoningTools(),  
    ],
    knowledge=kb3,
    description="""
The Actuarial & Financial Modeling Agent specializes in analyzing historical insurance data, 
performing actuarial calculations, and generating financial projections for aging-related insurance products. 
It supports pricing validation, reserving adequacy tests, and profitability analysis. 
This agent combines knowledge from actuarial best practices, regulatory frameworks (IFRS 17, Solvency II), 
and demographic trends to provide accurate, data-driven financial insights.
""",
    instructions="""
You are the **Actuarial & Financial Modeling Agent**.  
Your role is to analyze insurance products for aging populations using both quantitative and qualitative methods.  

📚 Knowledge Base:
- Markdown file 'Knowledge/agent3.md' containing actuarial methods, regulatory guidelines, and historical claims insights.
  
📊 Data (CSV):
- 'Data/agent3.csv' containing historical claims, premiums, policy counts, and persistency rates for various insurance products.

🛠️ Tools to Use:
1. **ActuarialModelingTool** → Compute Loss Ratios, Persistency Rates, Claims Severity, and Claims Frequency.
2. **FileTools** → Load, filter, and preprocess CSV data for analysis.
3. **CalculatorTools** → Perform financial and actuarial calculations (e.g., discounting, present value, risk-adjusted metrics).
4. **ReasoningTools** → Apply structured reasoning to validate assumptions and interpret results.

🎯 Tasks:
- Use the CSV data to calculate key actuarial metrics over specified years and product types.
- Align calculations with actuarial best practices and regulatory requirements (IFRS 17, Solvency II).
- Provide structured, data-driven insights on pricing adequacy, reserve sufficiency, and risk exposure.
- Justify recommendations using both historical data and knowledge base references.
"""
)

# Actuarial_Financial_Modeling.print_response(
#     "Analyze the historical claims and persistency data for 'Annuity' products between 2015 and 2020. "
#     # "Calculate key actuarial metrics including Loss Ratio, Persistency Rate, Claims Severity, and Claims Frequency using the ActuarialModelingTool. "
#     # "Provide insights on pricing adequacy, reserve sufficiency, and risk exposure. "
#     # "Reference the knowledge base (Knowledge/agent3.md) for best practices, regulatory compliance (IFRS 17, Solvency II), "
#     # "and actuarial assumptions. Present results in a structured, clear JSON or tabular format with justifications for each recommendation."
# )


####### 4th agent #########

# compliance_mapping_tool.py
kb4=MarkdownKnowledgeBase(
    path="Knowledge/agent4.md"
)


def ComplianceMappingTool(
    blueprint_csv: str = "Data/agent2_product_blueprints.csv",
    compliance_rules_csv: str = "Data/agent2.csv"
) -> str:
    """
    Check if insurance product blueprints comply with IFRS 17, Solvency II, and disclosure requirements.

    Args:
        blueprint_csv (str): Path to CSV containing product blueprint specifications.
        compliance_rules_csv (str): Path to CSV containing regulatory rules for compliance.

    Returns:
        str: JSON string with compliance evaluation for each product blueprint.
    """
    try:
        # Load product blueprints
        blueprints = pd.read_csv(blueprint_csv)

        # Load compliance rules
        rules = pd.read_csv(compliance_rules_csv)

        # Evaluate compliance for each product
        compliance_results = []
        for _, product in blueprints.iterrows():
            product_result = {"ProductID": product["ProductID"], "ProductName": product["ProductName"]}
            
            # IFRS17 check
            product_result["IFRS17_Compliant"] = all([
                product["InsuranceComponent"] >= rules["MinInsuranceComponent"].iloc[0],
                product["InvestmentComponent"] <= rules["MaxInvestmentComponent"].iloc[0]
            ])
            
            # Solvency II check
            product_result["SolvencyII_Compliant"] = product["CapitalRequirement"] >= rules["MinCapital"].iloc[0]
            
            # Disclosure check
            product_result["Disclosure_Compliant"] = all([
                product["AnnuityDisclosure"] == rules["RequiredAnnuityDisclosure"].iloc[0],
                product["LTCDisclosure"] == rules["RequiredLTCDisclosure"].iloc[0]
            ])
            
            compliance_results.append(product_result)

        return json.dumps(compliance_results, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})

Regulatory_Compliance_Alignment = Agent(
    name="Regulatory & Compliance Alignment",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    stream=True,
    markdown=True,
    tools=[
        ComplianceMappingTool,
        FileTools(),              
        CalculatorTools(),        
        ReasoningTools(),  
    ],
    knowledge=kb4,
    description="""
The Regulatory & Compliance Alignment Agent ensures that all insurance product designs for aging populations 
comply with applicable regulatory standards, including IFRS 17 and Solvency II, as well as consumer protection rules. 
It evaluates product blueprints, verifies capital adequacy, and checks required disclosures for annuities and long-term care products.
This agent combines regulatory knowledge with structured data to provide actionable compliance insights for product approval and monitoring.
""",
    instructions="""
You are the Regulatory & Compliance Alignment Agent.  
Your role is to analyze insurance product blueprints and ensure full compliance with regulatory and consumer protection standards.

📚 Knowledge Base:
- Markdown file 'Knowledge/agent4.md' containing IFRS 17, Solvency II, and disclosure rules.

📊 Data:
- Product blueprints CSV: 'Data/agent2.csv' 
- Regulatory rules CSV: 'Data/agent2.csv'

🛠️ Tools to Use:
1. **ComplianceMappingTool** → Map product blueprints against IFRS 17, Solvency II, and disclosure requirements.
2. **FileTools** → Load and filter CSV data for product and regulatory information.
3. **CalculatorTools** → Compute any capital or component ratios for compliance evaluation.
4. **ReasoningTools** → Apply structured reasoning to interpret compliance results and provide recommendations.

🎯 Tasks:
- Evaluate each product blueprint for IFRS 17 and Solvency II compliance.
- Check if all required disclosures are included.
- Flag any non-compliant products and provide justifications.
- Generate structured JSON output summarizing compliance status for all products.
"""
)


# Regulatory_Compliance_Alignment.print_response(
#     "Check all product blueprints for compliance with IFRS 17, Solvency II, and required disclosures. Provide a JSON summary of compliant and non-compliant products."
# )

####### 5th agent #########

kb5=MarkdownKnowledgeBase(
    path="Knowledge/agent2.md"
)

# ops_implementation_tool.py
import json
from textwrap import dedent
import pandas as pd

def OpsImplementationPlanner(
    product_blueprint_csv: str = "Data/agent2.csv",
    operational_guidelines_csv: str = "Data/agent2.csv"
) -> str:
    """
    Generate operational workflows for underwriting, policy administration, and distribution channels.

    Args:
        product_blueprint_csv (str): Path to CSV with product blueprint specifications.
        operational_guidelines_csv (str): CSV with operational guidelines and best practices.

    Returns:
        str: JSON string with suggested workflows for each product.
    """
    try:
        # Load product blueprints
        blueprints = pd.read_csv(product_blueprint_csv)
        # Load operational guidelines
        guidelines = pd.read_csv(operational_guidelines_csv)

        workflows = []
        for _, product in blueprints.iterrows():
            workflow = {
                "ProductID": product["ProductID"],
                "ProductName": product["ProductName"],
                "UnderwritingWorkflow": guidelines.get("Underwriting", "Standard financial/medical underwriting").values[0],
                "PolicyAdministrationWorkflow": guidelines.get("PolicyAdmin", "Standard long-term policy admin").values[0],
                "DistributionWorkflow": guidelines.get("Distribution", "Bancassurance / brokers / corporate partnerships").values[0]
            }
            workflows.append(workflow)

        return json.dumps(workflows, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})

Operational_Implementation=Agent(
    name="Operational Implementation",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    stream=True,
    markdown=True,
    tools=[
        OpsImplementationPlanner,
        FileTools(),              
        CalculatorTools(),        
        ReasoningTools(),  
    ],
    knowledge=kb5,    
    description="""
The Operational Implementation agent supports the practical execution of aging-focused insurance products.
It focuses on creating structured workflows for underwriting, policy administration, and distribution channels.
It ensures that product blueprints are translated into actionable operational processes, considering efficiency,
regulatory compliance, and scalability.
""",
    instructions="""
You are an Operational Implementation expert for aging insurance products. 
Your task is to plan workflows for each product based on the blueprint and operational guidelines.

Tools to use:
- OpsImplementationPlanner: Generate structured workflows for underwriting, policy administration, and distribution.
- FileTools: Access or read supporting CSV/Excel data files.
- CalculatorTools: Perform any operational calculations if required.
- ReasoningTools: Provide insights, check consistency, and ensure best practices.

Data:
- CSV: Product blueprints (Data/agent2.csv)
- CSV: Operational guidelines (Data/agent2.csv)

Knowledge Base:
- Markdown knowledge base (kb5) containing product features, pensions, annuities, LTC, innovation trends, and design challenges.

Respond with detailed operational workflows, highlighting the sequence of activities and any dependencies.
Provide output in a JSON format suitable for further processing.
""",
)

# Operational_Implementation.print_response("""
# Please generate operational workflows for all aging insurance products in the provided CSV.
# Focus on underwriting, policy administration, and distribution channels.
# """)

###### 6th agent ########
kb6= MarkdownKnowledgeBase(
    path="Knowldge/agent6.md"
)

# product_monitoring_tool.py

def ProductMonitoringTool(
    csv_path: str = "Data/agent6.csv",
    product: str = None,
    metric: str = None,
    start_year: int = 2020,
    end_year: int = 2021
) -> str:
    """
    Analyze product performance and innovation trends for aging insurance products.

    Args:
        csv_path (str): Path to CSV with historical product metrics.
        product (str, optional): Filter results for a specific product. Defaults to None (all products).
        metric (str, optional): Filter by metric (e.g., LossRatio, PersistencyRate, ClaimsFrequency, ClaimsSeverity). Defaults to None (all metrics).
        start_year (int): Starting year for analysis. Defaults to 2020.
        end_year (int): Ending year for analysis. Defaults to 2021.

    Returns:
        str: JSON string with filtered metrics and trends.
    """
    try:
        # Load dataset
        df = pd.read_csv(csv_path)

        # Filter by product
        if product:
            df = df[df["ProductName"].str.lower() == product.lower()]

        # Filter by metric
        if metric:
            df = df[df["Metric"].str.lower() == metric.lower()]

        # Filter by year
        df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

        # Convert to JSON
        result = df.to_dict(orient="records")
        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
Product_Monitoring_Innovation = Agent(
    name="Product Monitoring & Innovation",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    stream=True,
    markdown=True,
    tools=[
        ProductMonitoringTool,
        FileTools(),
        CalculatorTools(),
        ReasoningTools(),
    ],
    knowledge=kb6,
    description="""
Analyze and monitor performance of aging insurance products (annuities, LTC, pensions) 
by evaluating key metrics such as LossRatio, PersistencyRate, ClaimsFrequency, and ClaimsSeverity. 
Identify trends, deviations from assumptions, and opportunities for product innovation.
""",
    instructions="""
Use the ProductMonitoringTool to extract and filter historical product performance data from the CSV file (Data/agent6.csv). 
Apply filters by product name, metric, and year range. 
Leverage the Markdown knowledge base (Knowledge/agent6.md) to contextualize findings, assess deviations, and propose actionable improvements or innovations. 
Combine insights from metrics analysis with industry best practices to provide clear recommendations for product optimization and new product features.
""",
)

# Product_Monitoring_Innovation.print_response(
#     "Analyze the performance trends for all annuity products between 2020 and 2022, focusing on LossRatio and PersistencyRate."
# )


# Add this to your existing code after defining all your agents

# Create the team with route mode
InsuranceProductTeam = Team(
    name="Aging Insurance Product Team",
    mode="route",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    members=[
        Market_Demographic_Analysis,
        Product_Design_Aging_Insurance,
        Actuarial_Financial_Modeling,
        Regulatory_Compliance_Alignment,
        Operational_Implementation,
        Product_Monitoring_Innovation
    ],
    show_tool_calls=True,
    markdown=True,
    instructions=[
        "You are an expert insurance product team leader that routes queries to the most appropriate specialist agent.",
        "Analyze each user query to determine which team member has the right expertise to handle it.",
        "",
        "Team Members and Their Specializations:",
        "1. Market & Demographic Analysis - Focuses on global aging population dynamics, retirement readiness, demographic projections, pension gaps, and behavioral economics",
        "2. Product Design for Aging Insurance - Designs retirement income, annuity, LTC, hybrid and group products for aging populations",
        "3. Actuarial & Financial Modeling - Specializes in analyzing historical insurance data, actuarial calculations, and financial projections",
        "4. Regulatory & Compliance Alignment - Ensures compliance with IFRS 17, Solvency II, and consumer protection rules",
        "5. Operational Implementation - Creates workflows for underwriting, policy administration, and distribution channels",
        "6. Product Monitoring & Innovation - Analyzes product performance metrics and identifies innovation opportunities",
        "",
        "Routing Guidelines:",
        "- Demographic trends, market research, population data → Market & Demographic Analysis",
        "- Product design, blueprints, coverage specifications → Product Design for Aging Insurance", 
        "- Pricing, reserving, loss ratios, financial modeling → Actuarial & Financial Modeling",
        "- Regulatory compliance, IFRS 17, Solvency II → Regulatory & Compliance Alignment",
        "- Operational workflows, implementation plans → Operational Implementation",
        "- Performance monitoring, metrics analysis → Product Monitoring & Innovation",
        "",
        "If a query spans multiple areas, route to the most relevant specialist based on the primary focus.",
        "Always provide clear reasoning for your routing decision when appropriate."
    ],
    show_members_responses=True,
)

# Example usage (you can uncomment these to test):
# InsuranceProductTeam.print_response(
#     "Analyze aging population trends in Japan and their impact on insurance demand",
#     stream=True
# )

# InsuranceProductTeam.print_response(
#     "Design a new long-term care insurance product for retirees with chronic conditions",
#     stream=True
# )

# InsuranceProductTeam.print_response(
#     "Calculate the loss ratios and persistency rates for our annuity products from 2018-2023",
#     stream=True
# )

# InsuranceProductTeam.print_response(
#     "Check if our new pension product complies with IFRS 17 and Solvency II requirements",
#     stream=True
# )

# InsuranceProductTeam.print_response(
#     "Create operational workflows for underwriting and policy administration of our new hybrid life-LTC product",
#     stream=True
# )

# InsuranceProductTeam.print_response(
#     "Monitor the performance trends of our annuity products and suggest innovations for improvement",
#     stream=True
# )