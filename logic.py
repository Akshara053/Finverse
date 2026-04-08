# logic.py
# ─────────────────────────────────────────────
# All financial calculations for Finverse.
# No UI code here. Pure functions only.
# Each function does ONE thing and is testable.
# ─────────────────────────────────────────────

from config import (
    WEIGHT_SAVINGS_RATE, WEIGHT_SURVIVAL, WEIGHT_EXPENSE_RATIO,
    SAVINGS_RATE_EXCELLENT, SAVINGS_RATE_POOR,
    SURVIVAL_EXCELLENT, SURVIVAL_POOR,
    EXPENSE_RATIO_EXCELLENT, EXPENSE_RATIO_POOR,
    RISK_SAFE_THRESHOLD, RISK_MODERATE_THRESHOLD,
)


# ── HELPER ───────────────────────────────────

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Restrict a value to [min_val, max_val]."""
    return max(min_val, min(max_val, value))


def normalize(value: float, poor: float, excellent: float) -> float:
    """
    Convert a raw metric into a 0–100 score.

    - At or below `poor`      → 0   (worst)
    - At or above `excellent` → 100 (best)
    - In between              → linear interpolation

    Works for both "higher is better" (savings rate)
    and "lower is better" (expense ratio) depending on
    which direction poor vs excellent sits.
    """
    if excellent == poor:
        return 0.0
    raw = (value - poor) / (excellent - poor) * 100
    return clamp(raw, 0.0, 100.0)


# ── CORE METRICS ─────────────────────────────

def calculate_savings_rate(income: float, expenses: float) -> float:
    """
    Savings Rate = (Income - Expenses) / Income × 100

    Tells you what % of your income you keep each month.
    Negative means you're spending more than you earn.
    """
    if income <= 0:
        return 0.0
    return ((income - expenses) / income) * 100


def calculate_survival_months(savings: float, expenses: float) -> float:
    """
    Survival Months = Savings / Monthly Expenses

    Answers: "If I lose my income today, how long can I survive?"
    Capped at 120 months (10 years) to avoid display issues.
    """
    if expenses <= 0:
        return 120.0  # No expenses? Infinite survival — cap at 10 years
    if savings <= 0:
        return 0.0
    return clamp(savings / expenses, 0.0, 120.0)


def calculate_expense_ratio(income: float, expenses: float) -> float:
    """
    Expense Ratio = Expenses / Income × 100

    Tells you what % of your income is consumed by expenses.
    Lower is healthier. Above 100% = you're going into debt.
    """
    if income <= 0:
        return 100.0  # No income → worst case
    return clamp((expenses / income) * 100, 0.0, 200.0)


# ── SUB-SCORES ───────────────────────────────

def score_savings_rate(savings_rate: float) -> float:
    """Score the savings rate on a 0–100 scale."""
    return normalize(savings_rate, poor=SAVINGS_RATE_POOR, excellent=SAVINGS_RATE_EXCELLENT)


def score_survival_months(survival_months: float) -> float:
    """Score survival months on a 0–100 scale."""
    return normalize(survival_months, poor=SURVIVAL_POOR, excellent=SURVIVAL_EXCELLENT)


def score_expense_ratio(expense_ratio: float) -> float:
    """
    Score expense ratio on a 0–100 scale.
    Note: for expense ratio, LOWER is BETTER.
    So `poor` = high ratio, `excellent` = low ratio.
    """
    return normalize(expense_ratio, poor=EXPENSE_RATIO_POOR, excellent=EXPENSE_RATIO_EXCELLENT)


# ── COMPOSITE SCORE ──────────────────────────

def calculate_composite_score(
    savings_rate_score: float,
    survival_score: float,
    expense_ratio_score: float,
) -> float:
    """
    Weighted composite financial health score (0–100).

    Higher = healthier finances.
    Weights are defined in config.py — tune them there.
    """
    return (
        WEIGHT_SAVINGS_RATE  * savings_rate_score +
        WEIGHT_SURVIVAL      * survival_score +
        WEIGHT_EXPENSE_RATIO * expense_ratio_score
    )


# ── RISK LABEL ───────────────────────────────

def classify_risk(composite_score: float) -> str:
    """
    Translate composite score into a human-readable risk label.

    SAFE     → score >= 65
    MODERATE → score >= 35
    RISKY    → score <  35
    """
    if composite_score >= RISK_SAFE_THRESHOLD:
        return "SAFE"
    elif composite_score >= RISK_MODERATE_THRESHOLD:
        return "MODERATE"
    else:
        return "RISKY"


# ── MAIN ENTRY POINT ─────────────────────────

def analyse_finances(income: float, expenses: float, savings: float) -> dict:
    """
    Single function the UI calls.
    Returns a dict with every metric the app needs to display.

    Usage:
        result = analyse_finances(50000, 30000, 120000)
    """
    # Core metrics
    savings_rate    = calculate_savings_rate(income, expenses)
    survival_months = calculate_survival_months(savings, expenses)
    expense_ratio   = calculate_expense_ratio(income, expenses)

    # Sub-scores (0–100 each)
    sr_score  = score_savings_rate(savings_rate)
    sv_score  = score_survival_months(survival_months)
    exp_score = score_expense_ratio(expense_ratio)

    # Composite score
    composite = calculate_composite_score(sr_score, sv_score, exp_score)

    # Risk classification
    risk_level = classify_risk(composite)

    return {
        # Raw inputs (echoed back for display)
        "income":   income,
        "expenses": expenses,
        "savings":  savings,

        # Core metrics
        "savings_rate":    round(savings_rate, 1),     # e.g. 28.5  (%)
        "survival_months": round(survival_months, 1),  # e.g. 4.0   (months)
        "expense_ratio":   round(expense_ratio, 1),    # e.g. 71.5  (%)

        # Sub-scores
        "score_savings_rate":  round(sr_score, 1),
        "score_survival":      round(sv_score, 1),
        "score_expense_ratio": round(exp_score, 1),

        # Final output
        "composite_score": round(composite, 1),        # 0–100
        "risk_level":      risk_level,                 # SAFE / MODERATE / RISKY
    }
