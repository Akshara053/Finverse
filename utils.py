# utils.py
# ─────────────────────────────────────────────
# Formatting helpers. All display logic here,
# not in logic.py or app.py.
# ─────────────────────────────────────────────


def format_currency(amount, symbol="₹"):
    try:
        return f"{symbol}{amount:,.0f}"
    except (ValueError, TypeError):
        return f"{symbol}0"


def format_percent(value):
    return f"{value:.1f}%"


def format_months(months):
    if months >= 120:
        return "10+ years"
    whole  = int(months)
    days   = int((months - whole) * 30)
    if days > 0:
        return f"{whole}m {days}d"
    return f"{whole} months"


def get_savings_rate_message(rate):
    if rate >= 30:
        return "Excellent! Saving 30%+ of income."
    elif rate >= 20:
        return "Good. Healthy savings discipline."
    elif rate >= 10:
        return "Fair. Push toward 20%."
    elif rate >= 0:
        return "Low. Very little monthly margin."
    else:
        return "⚠️ Spending more than earning."


def get_survival_message(months):
    if months >= 12:
        return "Strong. 12+ months of coverage."
    elif months >= 6:
        return "Good. Aim to maintain 6–12 months."
    elif months >= 3:
        return "Thin. Unexpected events could hurt."
    elif months >= 1:
        return "Vulnerable. Under 3 months runway."
    else:
        return "Critical. No financial cushion."


def get_risk_advice(risk_level):
    advice = {
        "SAFE":     "Keep it up. Focus on investing your surplus.",
        "MODERATE": "You're stable — increase savings and cut discretionary spend.",
        "RISKY":    "Urgent: Cut expenses and build a 3-month emergency fund first.",
    }
    return advice.get(risk_level, "")
