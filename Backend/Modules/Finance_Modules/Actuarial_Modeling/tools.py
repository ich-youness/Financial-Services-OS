from agno.tools import tool
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from scipy import stats
import math

# ============================================================================
# LIFE & NON-LIFE INSURANCE MODELING TOOLS
# ============================================================================

@tool(
    name="fit_mortality_table",
    description="Fit mortality table using specified method (Gompertz, Makeham, etc.)",
    show_result=True,
)
def fit_mortality_table(
    ages: List[int], 
    deaths: List[int], 
    exposures: List[int], 
    method: str = "gompertz"
) -> Dict[str, Any]:
    """
    Fit mortality table using specified method.
    
    Args:
        ages: List of ages
        deaths: List of death counts
        exposures: List of exposure counts
        method: Fitting method ("gompertz", "makeham", "weibull")
    
    Returns:
        Dictionary containing fitted parameters and goodness-of-fit metrics
    """
    if len(ages) != len(deaths) or len(ages) != len(exposures):
        return {"error": "All input lists must have the same length"}
    
    # Calculate crude mortality rates
    qx_rates = [d/e if e > 0 else 0 for d, e in zip(deaths, exposures)]
    
    if method.lower() == "gompertz":
        # Gompertz: qx = B * c^x
        # log(qx) = log(B) + x * log(c)
        valid_indices = [i for i, q in enumerate(qx_rates) if q > 0]
        if len(valid_indices) < 2:
            return {"error": "Insufficient data for Gompertz fitting"}
        
        x_values = [ages[i] for i in valid_indices]
        log_qx = [math.log(qx_rates[i]) for i in valid_indices]
        
        # Linear regression on log scale
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, log_qx)
        slope = float(slope)
        intercept = float(intercept)
        r_value = float(r_value)
        p_value = float(p_value)
        
        B = math.exp(intercept)
        c = math.exp(slope)
        
        # Calculate fitted values
        fitted_qx = [B * (c ** age) for age in ages]
        
        return {
            "method": "gompertz",
            "parameters": {
                "B": round(B, 6),
                "c": round(c, 6)
            },
            "goodness_of_fit": {
                "r_squared": round(r_value ** 2, 4),
                "p_value": round(p_value, 4)
            },
            "fitted_rates": [round(q, 6) for q in fitted_qx],
            "crude_rates": [round(q, 6) for q in qx_rates]
        }
    
    elif method.lower() == "makeham":
        # Makeham: qx = A + B * c^x
        # This is a simplified implementation
        return {
            "method": "makeham",
            "error": "Makeham method not yet implemented",
            "crude_rates": [round(q, 6) for q in qx_rates]
        }
    
    else:
        return {
            "error": f"Method '{method}' not supported. Use 'gompertz'",
            "crude_rates": [round(q, 6) for q in qx_rates]
        }


@tool(
    name="project_life_liability",
    description="Project life insurance liabilities using mortality and discount assumptions",
    show_result=True,
)
def project_life_liability(
    policies: pd.DataFrame, 
    mortality_table: Dict[int, float], 
    discount_curve: Dict[int, float], 
    lapse_rate: float = 0.0
) -> Dict[str, Any]:
    """
    Project life insurance liabilities using mortality and discount assumptions.
    
    Args:
        policies: DataFrame with columns: PolicyID, IssueAge, Term, SumAssured, AnnualPremium, Product
        mortality_table: Dictionary of age -> qx (annual mortality probability)
        discount_curve: Dictionary of year -> annual spot rate
        lapse_rate: Annual lapse probability (constant)
    
    Returns:
        Dictionary containing liability projections and duration measures
    """
    try:
        results = []
        total_pv_benefits = 0
        total_pv_premiums = 0
        total_epv = 0
        total_duration = 0
        
        for _, row in policies.iterrows():
            pid = row["PolicyID"]
            age0 = int(row["IssueAge"])
            term = int(row["Term"])
            sa = float(row["SumAssured"])
            prem = float(row["AnnualPremium"])
            product = str(row.get("Product", "TermLife"))
            
            # Determine projection period
            T = term if product in ("TermLife", "Endowment") else 60
            
            surv = 1.0
            pv_ben = 0.0
            pv_prem = 0.0
            dur_weighted_ben = 0.0
            
            for t in range(1, T + 1):
                age_t = age0 + t - 1
                qx = mortality_table.get(age_t, 0.02)  # Default 2% mortality
                lx = lapse_rate
                
                # Death in year t
                death_prob = surv * qx
                # Premium in year t
                prem_prob = surv
                
                r = discount_curve.get(t, 0.05)  # Default 5% rate
                df = 1.0 / ((1.0 + r) ** t)
                
                # Benefits
                if product in ("TermLife", "WholeLife"):
                    pv_ben += death_prob * sa * df
                    dur_weighted_ben += t * death_prob * sa * df
                elif product == "Endowment":
                    pv_ben += death_prob * sa * df
                    if t == T:
                        pv_ben += surv * sa * df  # Maturity benefit
                        dur_weighted_ben += T * surv * sa * df
                
                # Premiums
                pv_prem += prem_prob * prem * df
                
                # Update survival probability
                surv *= (1 - qx) * (1 - lx)
            
            # Calculate duration
            duration_ben = dur_weighted_ben / pv_ben if pv_ben > 0 else 0
            epv = pv_ben - pv_prem
            
            results.append({
                "PolicyID": pid,
                "PV_Benefits": round(pv_ben, 2),
                "PV_Premiums": round(pv_prem, 2),
                "EPV": round(epv, 2),
                "Duration_Benefits": round(duration_ben, 2)
            })
            
            total_pv_benefits += pv_ben
            total_pv_premiums += pv_prem
            total_epv += epv
            total_duration += duration_ben
        
        return {
            "individual_policies": results,
            "portfolio_totals": {
                "Total_PV_Benefits": round(total_pv_benefits, 2),
                "Total_PV_Premiums": round(total_pv_premiums, 2),
                "Total_EPV": round(total_epv, 2),
                "Average_Duration": round(total_duration / len(policies), 2)
            },
            "assumptions": {
                "mortality_table": mortality_table,
                "discount_curve": discount_curve,
                "lapse_rate": lapse_rate
            }
        }
        
    except Exception as e:
        return {"error": f"Error in liability projection: {str(e)}"}


@tool(
    name="analyze_claims_triangle",
    description="Analyze claims triangle for development patterns and trends",
    show_result=True,
)
def analyze_claims_triangle(
    triangle: Dict[str, List[float]], 
    kind: str = "paid"
) -> Dict[str, Any]:
    """
    Analyze claims triangle for development patterns and trends.
    
    Args:
        triangle: Dictionary with accident years as keys and development arrays as values
        kind: Type of triangle ("paid" or "incurred")
    
    Returns:
        Dictionary containing triangle analysis and development factors
    """
    try:
        accident_years = list(triangle.keys())
        accident_years.sort()
        
        # Calculate development factors
        development_factors = []
        for i in range(len(accident_years) - 1):
            current_year = accident_years[i]
            next_year = accident_years[i + 1]
            
            current_values = triangle[current_year]
            next_values = triangle[next_year]
            
            # Calculate development factor for each development period
            for j in range(min(len(current_values), len(next_values))):
                if current_values[j] > 0:
                    dev_factor = next_values[j] / current_values[j]
                    development_factors.append({
                        "accident_year": current_year,
                        "development_period": j,
                        "development_factor": round(dev_factor, 4)
                    })
        
        # Calculate average development factors by development period
        dev_periods = {}
        for dev in development_factors:
            period = dev["development_period"]
            if period not in dev_periods:
                dev_periods[period] = []
            dev_periods[period].append(dev["development_factor"])
        
        avg_dev_factors = {}
        for period, factors in dev_periods.items():
            avg_dev_factors[period] = round(np.mean(factors), 4)
        
        # Calculate ultimate estimates using average development factors
        ultimate_estimates = {}
        for ay in accident_years:
            values = triangle[ay]
            if values:
                latest_value = values[-1]
                ultimate = latest_value
                
                # Apply remaining development factors
                for period in range(len(values), max(dev_periods.keys()) + 1):
                    if period in avg_dev_factors:
                        ultimate *= avg_dev_factors[period]
                
                ultimate_estimates[ay] = round(ultimate, 2)
        
        return {
            "triangle_type": kind,
            "accident_years": accident_years,
            "development_factors": development_factors,
            "average_development_factors": avg_dev_factors,
            "ultimate_estimates": ultimate_estimates,
            "triangle_data": triangle
        }
        
    except Exception as e:
        return {"error": f"Error in triangle analysis: {str(e)}"}


@tool(
    name="fit_catastrophe_model",
    description="Fit catastrophe loss model using specified distribution",
    show_result=True,
)
def fit_catastrophe_model(
    events: List[Dict], 
    losses: List[float], 
    exposures: List[float], 
    distribution: str = "pareto"
) -> Dict[str, Any]:
    """
    Fit catastrophe loss model using specified distribution.
    
    Args:
        events: List of event dictionaries
        losses: List of loss amounts
        exposures: List of exposure values
        distribution: Distribution type ("pareto", "lognormal", "gamma")
    
    Returns:
        Dictionary containing fitted parameters and model statistics
    """
    try:
        if len(losses) != len(exposures):
            return {"error": "Losses and exposures must have the same length"}
        
        # Calculate loss ratios
        loss_ratios = [l/e if e > 0 else 0 for l, e in zip(losses, exposures)]
        loss_ratios = [lr for lr in loss_ratios if lr > 0]  # Remove zero/negative ratios
        
        if len(loss_ratios) < 3:
            return {"error": "Insufficient data for distribution fitting"}
        
        if distribution.lower() == "pareto":
            # Fit Pareto distribution
            # Use method of moments for shape parameter
            mean_lr = np.mean(loss_ratios)
            var_lr = np.var(loss_ratios)
            
            if var_lr > mean_lr ** 2:
                shape = (2 * var_lr) / (var_lr - mean_lr ** 2)
                scale = mean_lr * (shape - 1) / shape
            else:
                shape = 2.1  # Default shape parameter
                scale = mean_lr
            
            # Generate fitted distribution
            fitted_dist = stats.pareto(shape, scale=scale)
            
            # Goodness of fit
            ks_stat, ks_pvalue = stats.kstest(loss_ratios, fitted_dist.cdf)
            
            return {
                "distribution": "pareto",
                "parameters": {
                    "shape": round(shape, 4),
                    "scale": round(scale, 4)
                },
                "goodness_of_fit": {
                    "ks_statistic": round(ks_stat, 4),
                    "ks_pvalue": round(ks_pvalue, 4)
                },
                "statistics": {
                    "mean": round(mean_lr, 4),
                    "variance": round(var_lr, 4),
                    "fitted_mean": round(fitted_dist.mean(), 4),
                    "fitted_variance": round(fitted_dist.var(), 4)
                },
                "data": {
                    "loss_ratios": [round(lr, 4) for lr in loss_ratios],
                    "count": len(loss_ratios)
                }
            }
        
        elif distribution.lower() == "lognormal":
            # Fit lognormal distribution
            log_losses = [math.log(lr) for lr in loss_ratios if lr > 0]
            
            if len(log_losses) < 3:
                return {"error": "Insufficient positive values for lognormal fitting"}
            
            mu = np.mean(log_losses)
            sigma = np.std(log_losses)
            
            fitted_dist = stats.lognorm(s=sigma, scale=math.exp(mu))
            
            # Goodness of fit
            ks_stat, ks_pvalue = stats.kstest(loss_ratios, fitted_dist.cdf)
            
            return {
                "distribution": "lognormal",
                "parameters": {
                    "mu": round(mu, 4),
                    "sigma": round(sigma, 4)
                },
                "goodness_of_fit": {
                    "ks_statistic": round(ks_stat, 4),
                    "ks_pvalue": round(ks_pvalue, 4)
                },
                "statistics": {
                    "mean": round(np.mean(loss_ratios), 4),
                    "variance": round(np.var(loss_ratios), 4),
                    "fitted_mean": round(fitted_dist.mean(), 4),
                    "fitted_variance": round(fitted_dist.var(), 4)
                },
                "data": {
                    "loss_ratios": [round(lr, 4) for lr in loss_ratios],
                    "count": len(loss_ratios)
                }
            }
        
        else:
            return {
                "error": f"Distribution '{distribution}' not supported. Use 'pareto' or 'lognormal'",
                "data": {
                    "loss_ratios": [round(lr, 4) for lr in loss_ratios],
                    "count": len(loss_ratios)
                }
            }
        
    except Exception as e:
        return {"error": f"Error in catastrophe model fitting: {str(e)}"}


# ============================================================================
# PENSION & RETIREMENT TOOLS
# ============================================================================

@tool(
    name="calculate_pbo",
    description="Calculate Projected Benefit Obligation for pension plan",
    show_result=True,
)
def calculate_pbo(
    participants: List[Dict], 
    benefit_formula: str, 
    discount_rate: float, 
    mortality_table: Dict[int, float]
) -> Dict[str, Any]:
    """
    Calculate Projected Benefit Obligation for pension plan.
    
    Args:
        participants: List of participant dictionaries with age, service, salary, etc.
        benefit_formula: Benefit formula (e.g., "2% * service * final_salary")
        discount_rate: Annual discount rate
        mortality_table: Dictionary of age -> survival probability
    
    Returns:
        Dictionary containing PBO calculations
    """
    try:
        total_pbo = 0
        participant_pbos = []
        
        for participant in participants:
            age = participant.get("age", 65)
            service_years = participant.get("service_years", 0)
            current_salary = participant.get("current_salary", 0)
            final_salary = participant.get("final_salary", current_salary)
            retirement_age = participant.get("retirement_age", 65)
            
            # Calculate annual benefit
            if benefit_formula == "2% * service * final_salary":
                annual_benefit = 0.02 * service_years * final_salary
            else:
                # Default formula
                annual_benefit = 0.02 * service_years * final_salary
            
            # Calculate PBO
            years_to_retirement = max(0, retirement_age - age)
            if years_to_retirement > 0:
                # Discount to retirement
                pv_at_retirement = annual_benefit / ((1 + discount_rate) ** years_to_retirement)
                
                # Apply survival probability to retirement
                survival_prob = 1.0
                for year in range(age, retirement_age):
                    qx = mortality_table.get(year, 0.02)
                    survival_prob *= (1 - qx)
                
                pbo = pv_at_retirement * survival_prob
            else:
                # Already retired
                pbo = annual_benefit
            
            participant_pbos.append({
                "age": age,
                "service_years": service_years,
                "annual_benefit": round(annual_benefit, 2),
                "pbo": round(pbo, 2)
            })
            
            total_pbo += pbo
        
        return {
            "total_pbo": round(total_pbo, 2),
            "participant_details": participant_pbos,
            "assumptions": {
                "benefit_formula": benefit_formula,
                "discount_rate": discount_rate,
                "mortality_table": mortality_table
            }
        }
        
    except Exception as e:
        return {"error": f"Error in PBO calculation: {str(e)}"}


@tool(
    name="project_funding_ratio",
    description="Project funding ratio over time with contributions and investment returns",
    show_result=True,
)
def project_funding_ratio(
    assets: float, 
    pbo: float, 
    contributions: List[float], 
    returns: List[float], 
    assumptions: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Project funding ratio over time with contributions and investment returns.
    
    Args:
        assets: Current plan assets
        pbo: Current projected benefit obligation
        contributions: List of annual contributions
        returns: List of annual investment returns
        assumptions: Dictionary of assumptions (pbo_growth, etc.)
    
    Returns:
        Dictionary containing funding ratio projections
    """
    try:
        pbo_growth = assumptions.get("pbo_growth", 0.03)
        projection_years = max(len(contributions), len(returns))
        
        current_funding_ratio = assets / pbo if pbo > 0 else 0
        
        projections = []
        current_assets = assets
        current_pbo = pbo
        
        for year in range(projection_years):
            # Get contribution and return for this year
            contribution = contributions[year] if year < len(contributions) else 0
            return_rate = returns[year] if year < len(returns) else 0.06
            
            # Project assets
            investment_return = current_assets * return_rate
            current_assets += contribution + investment_return
            
            # Project PBO
            current_pbo *= (1 + pbo_growth)
            
            # Calculate funding ratio
            funding_ratio = current_assets / current_pbo if current_pbo > 0 else 0
            
            projections.append({
                "year": year + 1,
                "assets": round(current_assets, 2),
                "pbo": round(current_pbo, 2),
                "funding_ratio": round(funding_ratio, 4),
                "contribution": round(contribution, 2),
                "investment_return": round(investment_return, 2)
            })
        
        return {
            "current_funding_ratio": round(current_funding_ratio, 4),
            "projections": projections,
            "assumptions": {
                "pbo_growth": pbo_growth,
                "projection_years": projection_years
            }
        }
        
    except Exception as e:
        return {"error": f"Error in funding ratio projection: {str(e)}"}


@tool(
    name="optimize_contributions",
    description="Optimize contribution strategy to achieve target funding ratio",
    show_result=True,
)
def optimize_contributions(
    pbo: float, 
    assets: float, 
    target_funding_ratio: float, 
    constraints: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Optimize contribution strategy to achieve target funding ratio.
    
    Args:
        pbo: Current projected benefit obligation
        assets: Current plan assets
        target_funding_ratio: Target funding ratio
        constraints: Dictionary of constraints (max_contribution, years, etc.)
    
    Returns:
        Dictionary containing optimized contribution strategy
    """
    try:
        max_contribution = constraints.get("max_contribution", pbo * 0.1)
        years = constraints.get("years", 5)
        return_rate = constraints.get("return_rate", 0.06)
        pbo_growth = constraints.get("pbo_growth", 0.03)
        
        target_assets = target_funding_ratio * pbo
        
        # Simple optimization: calculate required annual contribution
        required_growth = target_assets - assets
        if required_growth <= 0:
            return {
                "message": "Target funding ratio already achieved",
                "current_funding_ratio": round(assets / pbo, 4),
                "target_funding_ratio": target_funding_ratio
            }
        
        # Calculate required annual contribution
        # Using future value of annuity formula
        if return_rate > 0:
            required_contribution = required_growth / (((1 + return_rate) ** years - 1) / return_rate)
        else:
            required_contribution = required_growth / years
        
        # Check constraints
        if required_contribution > max_contribution:
            return {
                "error": f"Required contribution ({required_contribution:.2f}) exceeds maximum allowed ({max_contribution:.2f})",
                "required_contribution": round(required_contribution, 2),
                "max_contribution": round(max_contribution, 2)
            }
        
        # Project funding ratio with optimized contributions
        projections = []
        current_assets = assets
        current_pbo = pbo
        
        for year in range(years):
            # Apply contribution and return
            investment_return = current_assets * return_rate
            current_assets += required_contribution + investment_return
            
            # Project PBO
            current_pbo *= (1 + pbo_growth)
            
            # Calculate funding ratio
            funding_ratio = current_assets / current_pbo if current_pbo > 0 else 0
            
            projections.append({
                "year": year + 1,
                "assets": round(current_assets, 2),
                "pbo": round(current_pbo, 2),
                "funding_ratio": round(funding_ratio, 4),
                "contribution": round(required_contribution, 2),
                "investment_return": round(investment_return, 2)
            })
        
        return {
            "optimized_contribution": round(required_contribution, 2),
            "projections": projections,
            "constraints": constraints,
            "target_funding_ratio": target_funding_ratio
        }
        
    except Exception as e:
        return {"error": f"Error in contribution optimization: {str(e)}"}


# ============================================================================
# CAPITAL & SOLVENCY TOOLS
# ============================================================================

@tool(
    name="calculate_scr",
    description="Calculate Solvency Capital Requirement using correlation matrix",
    show_result=True,
)
def calculate_scr(
    risk_factors: Dict[str, float], 
    correlations: Dict[str, Dict[str, float]], 
    confidence_level: float = 0.995
) -> Dict[str, Any]:
    """
    Calculate Solvency Capital Requirement using correlation matrix.
    
    Args:
        risk_factors: Dictionary of risk factor names and amounts
        correlations: Dictionary of correlation coefficients between risk factors
        confidence_level: Confidence level for SCR calculation (default 99.5%)
    
    Returns:
        Dictionary containing SCR calculations and risk contributions
    """
    try:
        risk_names = list(risk_factors.keys())
        n_risks = len(risk_names)
        
        if n_risks == 0:
            return {"error": "No risk factors provided"}
        
        # Create correlation matrix
        corr_matrix = np.zeros((n_risks, n_risks))
        for i, risk1 in enumerate(risk_names):
            for j, risk2 in enumerate(risk_names):
                if i == j:
                    corr_matrix[i][j] = 1.0
                else:
                    corr_matrix[i][j] = correlations.get(risk1, {}).get(risk2, 0.0)
        
        # Calculate SCR using square root formula
        # SCR = sqrt(sum_i sum_j SCR_i * SCR_j * rho_ij)
        scr_squared = 0
        for i in range(n_risks):
            for j in range(n_risks):
                scr_squared += risk_factors[risk_names[i]] * risk_factors[risk_names[j]] * corr_matrix[i][j]
        
        scr = math.sqrt(scr_squared)
        
        # Calculate risk contributions
        risk_contributions = {}
        for i, risk_name in enumerate(risk_names):
            contribution = 0
            for j in range(n_risks):
                contribution += risk_factors[risk_names[j]] * corr_matrix[i][j]
            risk_contributions[risk_name] = round(contribution, 2)
        
        # Calculate diversification benefit
        sum_individual_scr = sum(risk_factors.values())
        diversification_benefit = sum_individual_scr - scr
        
        return {
            "scr": round(scr, 2),
            "confidence_level": confidence_level,
            "risk_factors": risk_factors,
            "correlation_matrix": corr_matrix.tolist(),
            "risk_contributions": risk_contributions,
            "diversification_benefit": round(diversification_benefit, 2),
            "diversification_ratio": round(scr / sum_individual_scr, 4) if sum_individual_scr > 0 else 0
        }
        
    except Exception as e:
        return {"error": f"Error in SCR calculation: {str(e)}"}


@tool(
    name="compute_risk_margin",
    description="Compute Risk Margin using cost-of-capital approach",
    show_result=True,
)
def compute_risk_margin(
    scr_path: List[float], 
    coc_rate: float, 
    discount_curve: Dict[int, float]
) -> Dict[str, Any]:
    """
    Compute Risk Margin using cost-of-capital approach.
    
    Args:
        scr_path: List of SCR values over time
        coc_rate: Cost of capital rate
        discount_curve: Dictionary of year -> discount rate
    
    Returns:
        Dictionary containing risk margin calculations
    """
    try:
        if not scr_path:
            return {"error": "SCR path cannot be empty"}
        
        risk_margin = 0
        discounted_scr = []
        
        for year, scr in enumerate(scr_path, 1):
            # Get discount rate for this year
            discount_rate = discount_curve.get(year, 0.05)  # Default 5%
            
            # Apply discounting and CoC
            # RM = sum_t (CoC * SCR_t) / (1 + r_t)^(t + 0.5)
            discounted_value = (coc_rate * scr) / ((1 + discount_rate) ** (year + 0.5))
            risk_margin += discounted_value
            
            discounted_scr.append({
                "year": year,
                "scr": round(scr, 2),
                "discount_rate": round(discount_rate, 4),
                "discounted_value": round(discounted_value, 2)
            })
        
        return {
            "risk_margin": round(risk_margin, 2),
            "cost_of_capital_rate": coc_rate,
            "scr_path": scr_path,
            "discounted_scr": discounted_scr,
            "total_scr": round(sum(scr_path), 2)
        }
        
    except Exception as e:
        return {"error": f"Error in risk margin calculation: {str(e)}"}


@tool(
    name="ifrs17_csm_calculation",
    description="Calculate IFRS 17 Contractual Service Margin",
    show_result=True,
)
def ifrs17_csm_calculation(
    cashflows: List[Dict], 
    locked_rates: List[float], 
    coverage_units: List[float]
) -> Dict[str, Any]:
    """
    Calculate IFRS 17 Contractual Service Margin.
    
    Args:
        cashflows: List of cashflow dictionaries with year, premium, claims, expenses
        locked_rates: List of locked-in discount rates
        coverage_units: List of coverage units for each period
    
    Returns:
        Dictionary containing CSM calculations
    """
    try:
        if len(cashflows) != len(locked_rates) or len(cashflows) != len(coverage_units):
            return {"error": "All input lists must have the same length"}
        
        # Calculate initial CSM
        initial_csm = 0
        for i, cf in enumerate(cashflows):
            year = cf.get("year", i + 1)
            premium = cf.get("premium", 0)
            claims = cf.get("claims", 0)
            expenses = cf.get("expenses", 0)
            
            # Net cashflow
            net_cf = premium - claims - expenses
            
            # Discount using locked rate
            locked_rate = locked_rates[i] if i < len(locked_rates) else 0.05
            discount_factor = 1 / ((1 + locked_rate) ** year)
            
            initial_csm += net_cf * discount_factor
        
        # Ensure CSM is non-negative
        initial_csm = max(0, initial_csm)
        
        # Calculate CSM release over time
        total_coverage_units = sum(coverage_units)
        csm_releases = []
        remaining_csm = initial_csm
        
        for i, cu in enumerate(coverage_units):
            release_ratio = 0
            release_amount = 0
            if total_coverage_units > 0:
                release_ratio = cu / total_coverage_units
                release_amount = initial_csm * release_ratio
                remaining_csm -= release_amount
            else:
                release_amount = 0
                remaining_csm = 0
            
            csm_releases.append({
                "period": i + 1,
                "coverage_units": cu,
                "release_ratio": round(release_ratio, 4),
                "release_amount": round(release_amount, 2),
                "remaining_csm": round(max(0, remaining_csm), 2)
            })
        
        return {
            "initial_csm": round(initial_csm, 2),
            "total_coverage_units": total_coverage_units,
            "csm_releases": csm_releases,
            "assumptions": {
                "locked_rates": locked_rates,
                "coverage_units": coverage_units
            }
        }
        
    except Exception as e:
        return {"error": f"Error in CSM calculation: {str(e)}"}


# ============================================================================
# ALM INTEGRATION TOOLS
# ============================================================================

@tool(
    name="calculate_duration",
    description="Calculate duration using specified method (Macaulay, Modified)",
    show_result=True,
)
def calculate_duration(
    cashflows: List[Dict], 
    discount_rate: float, 
    method: str = "macaulay"
) -> Dict[str, Any]:
    """
    Calculate duration using specified method.
    
    Args:
        cashflows: List of cashflow dictionaries with year and amount
        discount_rate: Annual discount rate
        method: Duration method ("macaulay" or "modified")
    
    Returns:
        Dictionary containing duration calculations
    """
    try:
        if not cashflows:
            return {"error": "Cashflows cannot be empty"}
        
        present_value = 0
        duration_weighted = 0
        
        for cf in cashflows:
            year = cf.get("year", 1)
            amount = cf.get("amount", 0)
            
            # Calculate present value
            discount_factor = 1 / ((1 + discount_rate) ** year)
            pv = amount * discount_factor
            present_value += pv
            
            # Weight by time for duration calculation
            duration_weighted += year * pv
        
        if present_value <= 0:
            return {"error": "Present value must be positive"}
        
        # Calculate Macaulay duration
        macaulay_duration = duration_weighted / present_value
        
        # Calculate modified duration
        modified_duration = macaulay_duration / (1 + discount_rate)
        
        # Calculate effective duration (approximation)
        effective_duration = modified_duration
        
        return {
            "method": method,
            "discount_rate": discount_rate,
            "present_value": round(present_value, 2),
            "macaulay_duration": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "effective_duration": round(effective_duration, 4),
            "cashflows": cashflows
        }
        
    except Exception as e:
        return {"error": f"Error in duration calculation: {str(e)}"}


@tool(
    name="duration_gap_analysis",
    description="Analyze duration gap between assets and liabilities",
    show_result=True,
)
def duration_gap_analysis(
    assets: List[Dict], 
    liabilities: List[Dict], 
    asset_durations: List[float], 
    liability_durations: List[float]
) -> Dict[str, Any]:
    """
    Analyze duration gap between assets and liabilities.
    
    Args:
        assets: List of asset dictionaries with amount
        liabilities: List of liability dictionaries with amount
        asset_durations: List of asset durations
        liability_durations: List of liability durations
    
    Returns:
        Dictionary containing duration gap analysis
    """
    try:
        if len(assets) != len(asset_durations) or len(liabilities) != len(liability_durations):
            return {"error": "Assets and durations must have matching lengths"}
        
        # Calculate weighted average durations
        total_assets = sum(asset.get("amount", 0) for asset in assets)
        total_liabilities = sum(liability.get("amount", 0) for liability in liabilities)
        
        if total_assets <= 0 or total_liabilities <= 0:
            return {"error": "Total assets and liabilities must be positive"}
        
        # Weighted average asset duration
        weighted_asset_duration = 0
        for asset, duration in zip(assets, asset_durations):
            weight = asset.get("amount", 0) / total_assets
            weighted_asset_duration += weight * duration
        
        # Weighted average liability duration
        weighted_liability_duration = 0
        for liability, duration in zip(liabilities, liability_durations):
            weight = liability.get("amount", 0) / total_liabilities
            weighted_liability_duration += weight * duration
        
        # Calculate duration gap
        duration_gap = weighted_asset_duration - weighted_liability_duration
        
        # Calculate gap ratio
        gap_ratio = duration_gap / weighted_liability_duration if weighted_liability_duration > 0 else 0
        
        # Risk assessment
        if abs(gap_ratio) <= 0.1:
            risk_level = "Low"
        elif abs(gap_ratio) <= 0.25:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            "total_assets": round(total_assets, 2),
            "total_liabilities": round(total_liabilities, 2),
            "weighted_asset_duration": round(weighted_asset_duration, 4),
            "weighted_liability_duration": round(weighted_liability_duration, 4),
            "duration_gap": round(duration_gap, 4),
            "gap_ratio": round(gap_ratio, 4),
            "risk_level": risk_level,
            "asset_details": [
                {
                    "amount": asset.get("amount", 0),
                    "duration": duration,
                    "weight": round(asset.get("amount", 0) / total_assets, 4)
                }
                for asset, duration in zip(assets, asset_durations)
            ],
            "liability_details": [
                {
                    "amount": liability.get("amount", 0),
                    "duration": duration,
                    "weight": round(liability.get("amount", 0) / total_liabilities, 4)
                }
                for liability, duration in zip(liabilities, liability_durations)
            ]
        }
        
    except Exception as e:
        return {"error": f"Error in duration gap analysis: {str(e)}"}


@tool(
    name="optimize_alm_portfolio",
    description="Optimize ALM portfolio to match liability characteristics",
    show_result=True,
)
def optimize_alm_portfolio(
    liabilities: List[Dict], 
    constraints: Dict[str, Any], 
    risk_tolerance: float
) -> Dict[str, Any]:
    """
    Optimize ALM portfolio to match liability characteristics.
    
    Args:
        liabilities: List of liability dictionaries with amount and duration
        constraints: Dictionary of constraints (max_duration, min_duration, etc.)
        risk_tolerance: Risk tolerance level (0-1)
    
    Returns:
        Dictionary containing optimized portfolio allocation
    """
    try:
        if not liabilities:
            return {"error": "Liabilities cannot be empty"}
        
        # Calculate target portfolio characteristics
        total_liabilities = sum(liability.get("amount", 0) for liability in liabilities)
        target_duration = sum(
            liability.get("amount", 0) * liability.get("duration", 0) 
            for liability in liabilities
        ) / total_liabilities if total_liabilities > 0 else 0
        
        # Get constraints
        max_duration = constraints.get("max_duration", target_duration * 1.2)
        min_duration = constraints.get("min_duration", target_duration * 0.8)
        max_concentration = constraints.get("max_concentration", 0.3)
        
        # Simple optimization: suggest asset allocation
        # This is a simplified approach - real implementation would use optimization algorithms
        
        # Asset classes with typical durations
        asset_classes = [
            {"name": "Cash", "duration": 0.1, "return": 0.02, "risk": 0.01},
            {"name": "Short-term Bonds", "duration": 2.0, "return": 0.04, "risk": 0.05},
            {"name": "Medium-term Bonds", "duration": 5.0, "return": 0.05, "risk": 0.08},
            {"name": "Long-term Bonds", "duration": 10.0, "return": 0.06, "risk": 0.12},
            {"name": "Equities", "duration": 15.0, "return": 0.08, "risk": 0.20}
        ]
        
        # Calculate optimal weights to match target duration
        optimal_weights = []
        for asset in asset_classes:
            if asset["duration"] >= min_duration and asset["duration"] <= max_duration:
                # Weight inversely proportional to distance from target
                weight = 1 / (1 + abs(asset["duration"] - target_duration))
                optimal_weights.append({
                    "asset_class": asset["name"],
                    "duration": asset["duration"],
                    "weight": round(weight, 4),
                    "expected_return": asset["return"],
                    "risk": asset["risk"]
                })
        
        # Normalize weights
        total_weight = sum(w["weight"] for w in optimal_weights)
        if total_weight > 0:
            for weight in optimal_weights:
                weight["weight"] = round(weight["weight"] / total_weight, 4)
        
        # Calculate portfolio metrics
        portfolio_duration = sum(w["weight"] * w["duration"] for w in optimal_weights)
        portfolio_return = sum(w["weight"] * w["expected_return"] for w in optimal_weights)
        portfolio_risk = sum(w["weight"] * w["risk"] for w in optimal_weights)
        
        return {
            "target_duration": round(target_duration, 4),
            "portfolio_duration": round(portfolio_duration, 4),
            "duration_gap": round(portfolio_duration - target_duration, 4),
            "portfolio_return": round(portfolio_return, 4),
            "portfolio_risk": round(portfolio_risk, 4),
            "optimal_allocation": optimal_weights,
            "constraints": constraints,
            "risk_tolerance": risk_tolerance
        }
        
    except Exception as e:
        return {"error": f"Error in ALM portfolio optimization: {str(e)}"}


# ============================================================================
# PRICING & PROFITABILITY TOOLS
# ============================================================================

@tool(
    name="calculate_technical_premium",
    description="Calculate technical premium for insurance product",
    show_result=True,
)
def calculate_technical_premium(
    expected_claims: float, 
    expenses: float, 
    profit_loading: float, 
    lapse_rate: float
) -> Dict[str, Any]:
    """
    Calculate technical premium for insurance product.
    
    Args:
        expected_claims: Expected claims amount
        expenses: Expected expenses
        profit_loading: Profit margin as percentage of technical premium
        lapse_rate: Expected lapse rate
    
    Returns:
        Dictionary containing premium calculations
    """
    try:
        if lapse_rate >= 1:
            return {"error": "Lapse rate must be less than 100%"}
        
        # Calculate net premium
        net_premium = expected_claims + expenses
        
        # Calculate technical premium with profit loading
        # Technical Premium = (Net Premium) / (1 - Lapse Rate - Profit Loading)
        technical_premium = net_premium / (1 - lapse_rate - profit_loading)
        
        # Calculate components
        claims_loading = expected_claims / technical_premium if technical_premium > 0 else 0
        expense_loading = expenses / technical_premium if technical_premium > 0 else 0
        profit_amount = technical_premium * profit_loading
        
        # Calculate loss ratio
        loss_ratio = expected_claims / technical_premium if technical_premium > 0 else 0
        
        # Calculate expense ratio
        expense_ratio = expenses / technical_premium if technical_premium > 0 else 0
        
        # Calculate combined ratio
        combined_ratio = loss_ratio + expense_ratio
        
        return {
            "expected_claims": round(expected_claims, 2),
            "expenses": round(expenses, 2),
            "profit_loading": profit_loading,
            "lapse_rate": lapse_rate,
            "net_premium": round(net_premium, 2),
            "technical_premium": round(technical_premium, 2),
            "profit_amount": round(profit_amount, 2),
            "loadings": {
                "claims_loading": round(claims_loading, 4),
                "expense_loading": round(expense_loading, 4),
                "profit_loading": round(profit_loading, 4)
            },
            "ratios": {
                "loss_ratio": round(loss_ratio, 4),
                "expense_ratio": round(expense_ratio, 4),
                "combined_ratio": round(combined_ratio, 4)
            }
        }
        
    except Exception as e:
        return {"error": f"Error in technical premium calculation: {str(e)}"}


@tool(
    name="stochastic_pricing_simulation",
    description="Run stochastic simulation for pricing analysis",
    show_result=True,
)
def stochastic_pricing_simulation(
    risk_factors: List[str], 
    scenarios: int, 
    confidence_level: float
) -> Dict[str, Any]:
    """
    Run stochastic simulation for pricing analysis.
    
    Args:
        risk_factors: List of risk factor names
        scenarios: Number of simulation scenarios
        confidence_level: Confidence level for analysis
    
    Returns:
        Dictionary containing simulation results
    """
    try:
        if scenarios <= 0:
            return {"error": "Number of scenarios must be positive"}
        
        if confidence_level <= 0 or confidence_level >= 1:
            return {"error": "Confidence level must be between 0 and 1"}
        
        # Generate random scenarios for demonstration
        np.random.seed(42)  # For reproducibility
        
        # Simulate risk factor values
        simulation_results = []
        for scenario in range(scenarios):
            scenario_data: Dict[str, Any] = {"scenario": scenario + 1}
            
            for factor in risk_factors:
                # Generate random values for each risk factor
                if "mortality" in factor.lower():
                    # Mortality rates (lognormal distribution)
                    value = np.random.lognormal(mean=0, sigma=0.3)
                elif "lapse" in factor.lower():
                    # Lapse rates (beta distribution)
                    value = np.random.beta(a=2, b=8)
                elif "interest" in factor.lower():
                    # Interest rates (normal distribution)
                    value = np.random.normal(loc=0.05, scale=0.02)
                elif "expense" in factor.lower():
                    # Expense ratios (gamma distribution)
                    value = np.random.gamma(shape=5, scale=0.01)
                else:
                    # Default normal distribution
                    value = np.random.normal(loc=0, scale=1)
                
                scenario_data[factor] = round(value, 6)
            
            simulation_results.append(scenario_data)
        
        # Calculate statistics
        factor_stats = {}
        for factor in risk_factors:
            values = [result[factor] for result in simulation_results]
            factor_stats[factor] = {
                "mean": round(np.mean(values), 6),
                "std": round(np.std(values), 6),
                "min": round(np.min(values), 6),
                "max": round(np.max(values), 6),
                "percentile_95": round(np.percentile(values, 95), 6),
                "percentile_99": round(np.percentile(values, 99), 6)
            }
        
        # Calculate VaR and CVaR
        # For demonstration, we'll use a simple metric
        total_risk_scores = []
        for result in simulation_results:
            risk_score = sum(abs(result[factor]) for factor in risk_factors)
            total_risk_scores.append(risk_score)
        
        var_percentile = int((1 - confidence_level) * 100)
        var_value = np.percentile(total_risk_scores, var_percentile)
        
        # CVaR (expected shortfall)
        tail_scenarios = [score for score in total_risk_scores if score >= var_value]
        cvar_value = np.mean(tail_scenarios) if tail_scenarios else var_value
        
        return {
            "scenarios": scenarios,
            "confidence_level": confidence_level,
            "risk_factors": risk_factors,
            "simulation_results": simulation_results[:10],  # Show first 10 scenarios
            "factor_statistics": factor_stats,
            "risk_metrics": {
                "var_percentile": var_percentile,
                "var_value": round(var_value, 6),
                "cvar_value": round(cvar_value, 6)
            }
        }
        
    except Exception as e:
        return {"error": f"Error in stochastic simulation: {str(e)}"}


@tool(
    name="calculate_roc",
    description="Calculate Return on Capital with optional risk adjustment",
    show_result=True,
)
def calculate_roc(
    net_profit: float, 
    capital_required: float, 
    risk_adjustment: bool = True
) -> Dict[str, Any]:
    """
    Calculate Return on Capital with optional risk adjustment.
    
    Args:
        net_profit: Net profit amount
        capital_required: Required capital amount
        risk_adjustment: Whether to apply risk adjustment
    
    Returns:
        Dictionary containing ROC calculations
    """
    try:
        if capital_required <= 0:
            return {"error": "Required capital must be positive"}
        
        # Basic ROC
        basic_roc = net_profit / capital_required
        
        # Risk-adjusted ROC (simplified)
        if risk_adjustment:
            # Assume risk adjustment based on capital volatility
            # This is a simplified approach
            risk_adjustment_factor = 0.9  # 10% risk adjustment
            risk_adjusted_profit = net_profit * risk_adjustment_factor
            risk_adjusted_roc = risk_adjusted_profit / capital_required
        else:
            risk_adjusted_profit = net_profit
            risk_adjusted_roc = basic_roc
        
        # Calculate additional metrics
        profit_margin = net_profit / (net_profit + capital_required) if (net_profit + capital_required) > 0 else 0
        
        # Risk metrics (simplified)
        risk_metrics = {
            "capital_efficiency": round(capital_required / (net_profit + capital_required), 4) if (net_profit + capital_required) > 0 else 0,
            "profit_volatility": round(net_profit * 0.1, 2),  # Simplified volatility estimate
            "risk_adjustment_factor": 0.9 if risk_adjustment else 1.0
        }
        
        return {
            "net_profit": round(net_profit, 2),
            "capital_required": round(capital_required, 2),
            "basic_roc": round(basic_roc, 4),
            "risk_adjusted_roc": round(risk_adjusted_roc, 4),
            "risk_adjusted_profit": round(risk_adjusted_profit, 2),
            "profit_margin": round(profit_margin, 4),
            "risk_metrics": risk_metrics,
            "risk_adjustment_applied": risk_adjustment
        }
        
    except Exception as e:
        return {"error": f"Error in ROC calculation: {str(e)}"}
