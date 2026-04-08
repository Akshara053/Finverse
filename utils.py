# utils.py
# ─────────────────────────────────────────────
# Formatting helpers. Keep display logic here,
# not in logic.py or app.py.
# ─────────────────────────────────────────────


def format_currency(amount: float, symbol: str = "₹") -> str:
    """Format a number as currency with commas. e.g. 150000 → ₹1,50,000"""
    try:
        return f"{symbol}{amount:,.0f}"
    except (ValueError, TypeError):
        return f"{symbol}0"


def format_percent(value: float) -> str:
    """Format a float as a percentage string. e.g. 28.5 → '28.5%'"""
    return f"{value:.1f}%"


def format_months(months: float) -> str:
    """
    Convert decimal months to a readable string.
    e.g. 4.0  → '4 months'
         13.5 → '13 months 15 days'
         120  → '10+ years'
    """
    if months >= 120:
        return "10+ years"
    whole_months = int(months)
    remaining_days = int((months - whole_months) * 30)
    if remaining_days > 0:
        return f"{whole_months} months, {remaining_days} days"
    return f"{whole_months} months"


def get_savings_rate_message(savings_rate: float) -> str:
    """Human-readable interpretation of savings rate."""
    if savings_rate >= 30:
        return "Excellent! You save more than 30% of your income."
    elif savings_rate >= 20:
        return "Good. You save a healthy portion of your income."
    elif savings_rate >= 10:
        return "Fair. Try to increase savings to at least 20%."
    elif savings_rate >= 0:
        return "Low. You have very little margin each month."
    else:
        return "Warning: You are spending more than you earn."


def get_survival_message(months: float) -> str:
    """Human-readable interpretation of survival months."""
    if months >= 12:
        return "Strong emergency fund. You have 12+ months of coverage."
    elif months >= 6:
        return "Decent buffer. Aim for 6–12 months as your target."
    elif months >= 3:
        return "Thin buffer. Unexpected events could cause stress."
    elif months >= 1:
        return "Vulnerable. You have less than 3 months of runway."
    else:
        return "Critical. A single month of job loss could be devastating."


def get_risk_advice(risk_level: str) -> str:
    """Actionable one-liner based on risk level."""
    advice = {
        "SAFE":     "Keep it up. Focus on investing your surplus.",
        "MODERATE": "You're okay, but increase savings and reduce discretionary spending.",
        "RISKY":    "Urgent: Cut expenses, build an emergency fund of at least 3 months.",
    }
    return advice.get(risk_level, "")
