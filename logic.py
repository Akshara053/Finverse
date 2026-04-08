# logic.py
# ─────────────────────────────────────────────
# All financial calculations for Finverse.
# No UI code here. Pure functions only.
# ─────────────────────────────────────────────

from config import (
    WEIGHT_SAVINGS_RATE, WEIGHT_SURVIVAL, WEIGHT_EXPENSE_RATIO,
    SAVINGS_RATE_EXCELLENT, SAVINGS_RATE_POOR,
    SURVIVAL_EXCELLENT, SURVIVAL_POOR,
    EXPENSE_RATIO_EXCELLENT, EXPENSE_RATIO_POOR,
    RISK_SAFE_THRESHOLD, RISK_MODERATE_THRESHOLD,
)


# ── HELPERS ──────────────────────────────────

def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))


def normalize(value, poor, excellent):
    """Convert a raw value to a 0–100 score using linear interpolation."""
    if excellent == poor:
        return 0.0
    raw = (value - poor) / (excellent - poor) * 100
    return clamp(raw, 0.0, 100.0)


# ── CORE METRICS ─────────────────────────────

def calculate_savings_rate(income, expenses):
    if income <= 0:
        return 0.0
    return ((income - expenses) / income) * 100


def calculate_survival_months(savings, expenses):
    if expenses <= 0:
        return 120.0
    if savings <= 0:
        return 0.0
    return clamp(savings / expenses, 0.0, 120.0)


def calculate_expense_ratio(income, expenses):
    if income <= 0:
        return 100.0
    return clamp((expenses / income) * 100, 0.0, 200.0)


# ── SUB-SCORES ───────────────────────────────

def score_savings_rate(savings_rate):
    return normalize(savings_rate, poor=SAVINGS_RATE_POOR, excellent=SAVINGS_RATE_EXCELLENT)


def score_survival_months(survival_months):
    return normalize(survival_months, poor=SURVIVAL_POOR, excellent=SURVIVAL_EXCELLENT)


def score_expense_ratio(expense_ratio):
    # For expense ratio, lower is better — so poor and excellent are reversed
    return normalize(expense_ratio, poor=EXPENSE_RATIO_POOR, excellent=EXPENSE_RATIO_EXCELLENT)


def calculate_composite_score(sr_score, sv_score, exp_score):
    return (
        WEIGHT_SAVINGS_RATE  * sr_score +
        WEIGHT_SURVIVAL      * sv_score +
        WEIGHT_EXPENSE_RATIO * exp_score
    )


def classify_risk(composite_score):
    if composite_score >= RISK_SAFE_THRESHOLD:
        return "SAFE"
    elif composite_score >= RISK_MODERATE_THRESHOLD:
        return "MODERATE"
    else:
        return "RISKY"


# ── MAIN FINANCIAL ANALYSIS ──────────────────

def analyse_finances(income, expenses, savings):
    """
    Main entry point. Returns all metrics needed by the UI.
    Usage: result = analyse_finances(50000, 35000, 120000)
    """
    savings_rate    = calculate_savings_rate(income, expenses)
    survival_months = calculate_survival_months(savings, expenses)
    expense_ratio   = calculate_expense_ratio(income, expenses)

    sr_score  = score_savings_rate(savings_rate)
    sv_score  = score_survival_months(survival_months)
    exp_score = score_expense_ratio(expense_ratio)

    composite  = calculate_composite_score(sr_score, sv_score, exp_score)
    risk_level = classify_risk(composite)

    return {
        "income":   income,
        "expenses": expenses,
        "savings":  savings,

        "savings_rate":    round(savings_rate, 1),
        "survival_months": round(survival_months, 1),
        "expense_ratio":   round(expense_ratio, 1),

        "score_savings_rate":  round(sr_score, 1),
        "score_survival":      round(sv_score, 1),
        "score_expense_ratio": round(exp_score, 1),

        "composite_score": round(composite, 1),
        "risk_level":      risk_level,
    }


# ── PARTNER COMPATIBILITY ────────────────────

def analyse_compatibility(r1, r2):
    """
    Takes two analyse_finances() result dicts.
    Returns compatibility metrics for the couple.
    """
    combined_income   = r1["income"]   + r2["income"]
    combined_expenses = r1["expenses"] + r2["expenses"]
    combined_savings  = r1["savings"]  + r2["savings"]

    combined = analyse_finances(combined_income, combined_expenses, combined_savings)

    # Alignment: how close are their financial behaviors?
    # Closer composite scores = better alignment
    score_diff     = abs(r1["composite_score"] - r2["composite_score"])
    alignment      = clamp(100 - score_diff * 1.5, 0, 100)

    # Compatibility: 60% combined health + 40% behavioral alignment
    compatibility  = combined["composite_score"] * 0.6 + alignment * 0.4

    stronger_saver = "You" if r1["savings_rate"] >= r2["savings_rate"] else "Partner"
    risk           = classify_risk(compatibility)

    return {
        "combined":              combined,
        "alignment_score":       round(alignment, 1),
        "compatibility_score":   round(compatibility, 1),
        "score_diff":            round(score_diff, 1),
        "stronger_saver":        stronger_saver,
        "risk_level":            risk,
        "combined_surplus":      round(combined_income - combined_expenses, 0),
    }


def recommended_partner_income(my_income, my_expenses, my_savings,
                                target_savings_rate=20.0,
                                target_survival_months=6.0):
    """
    Given your finances, what should a partner earn
    for combined financial safety?

    Assumes partner adds ~60% to your current expenses
    (shared rent, shared food, etc.).
    """
    # Estimate combined expenses (shared life ≈ 1.6× your expenses)
    combined_expenses_est = my_expenses * 1.6

    # For target savings rate:
    # (combined_income - combined_expenses) / combined_income = target_rate/100
    # → combined_income = combined_expenses / (1 - target_rate/100)
    if target_savings_rate >= 100:
        target_savings_rate = 99
    required_combined_income = combined_expenses_est / (1 - target_savings_rate / 100)
    min_partner_income = max(0, required_combined_income - my_income)

    # Emergency fund target
    target_combined_savings      = combined_expenses_est * target_survival_months
    additional_savings_needed    = max(0, target_combined_savings - my_savings)
    partner_monthly_savings_need = round(additional_savings_needed / 24, 0)  # 2-year build

    return {
        "estimated_combined_expenses":    round(combined_expenses_est, 0),
        "required_combined_income":       round(required_combined_income, 0),
        "min_partner_income":             round(min_partner_income, 0),
        "target_combined_savings":        round(target_combined_savings, 0),
        "partner_monthly_savings_target": partner_monthly_savings_need,
    }


# ── SAVINGS RULES ────────────────────────────

def calculate_savings_rules(income, expenses, savings, age=25):
    """
    Calculate popular personal finance rules
    personalized to the user's numbers.
    """
    annual_expenses = expenses * 12
    monthly_surplus = income - expenses

    # Time to 6-month emergency fund
    if monthly_surplus > 0:
        shortfall      = max(0, expenses * 6 - savings)
        months_to_6m   = round(shortfall / monthly_surplus, 1) if shortfall > 0 else 0
    else:
        months_to_6m   = None  # Can't build it at current rate

    # FIRE progress (25× annual expenses)
    fire_number  = annual_expenses * 25
    fire_progress = round((savings / fire_number * 100) if fire_number > 0 else 0, 1)

    # 100-age equity rule
    equity_pct = max(0, 100 - age)
    debt_pct   = 100 - equity_pct

    return {
        # 50/30/20 rule
        "rule_50_needs":    round(income * 0.50, 0),
        "rule_30_wants":    round(income * 0.30, 0),
        "rule_20_savings":  round(income * 0.20, 0),

        # Emergency fund targets
        "emergency_3m":        round(expenses * 3, 0),
        "emergency_6m":        round(expenses * 6, 0),
        "emergency_12m":       round(expenses * 12, 0),
        "current_coverage":    round(savings / expenses if expenses > 0 else 0, 1),
        "months_to_6m_fund":   months_to_6m,

        # FIRE
        "fire_number":    round(fire_number, 0),
        "fire_progress":  min(fire_progress, 100.0),

        # Monthly picture
        "monthly_surplus": round(monthly_surplus, 0),
        "annual_surplus":  round(monthly_surplus * 12, 0),

        # Investment allocation
        "equity_pct":      equity_pct,
        "debt_pct":        debt_pct,
        "equity_amount":   round(savings * equity_pct / 100, 0),
        "debt_amount":     round(savings * debt_pct / 100, 0),
    }
