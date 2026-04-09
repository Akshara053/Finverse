# analytics.py  —  Finverse v6.0
# Charts, predictions, stress score, behavioral insights.
# All data science lives here — no UI code.

import math


# ══════════════════════════════════════════════
# FINANCIAL STRESS SCORE
# ══════════════════════════════════════════════

def calculate_stress_score(income, expenses, savings, result):
    """
    Stress score 0–100. Higher = more financial stress.
    Opposite of health score — measures financial anxiety pressure.

    Three drivers:
    1. Expense pressure   (how close expenses are to income)
    2. Runway anxiety     (how short emergency fund is)
    3. Cash flow fragility (negative or thin monthly surplus)
    """
    # 1. Expense pressure (0–40 points)
    er = result["expense_ratio"]
    if er >= 100:
        ep = 40
    elif er >= 85:
        ep = 30
    elif er >= 70:
        ep = 20
    elif er >= 55:
        ep = 10
    else:
        ep = 0

    # 2. Runway anxiety (0–40 points)
    sm = result["survival_months"]
    if sm < 1:
        ra = 40
    elif sm < 3:
        ra = 30
    elif sm < 6:
        ra = 20
    elif sm < 9:
        ra = 10
    else:
        ra = 0

    # 3. Cash flow fragility (0–20 points)
    surplus = income - expenses
    if surplus < 0:
        cf = 20
    elif surplus < income * 0.05:
        cf = 15
    elif surplus < income * 0.10:
        cf = 10
    elif surplus < income * 0.20:
        cf = 5
    else:
        cf = 0

    stress = ep + ra + cf
    return min(100, stress)


def get_stress_label(stress_score):
    if stress_score >= 70:
        return ("High Stress",   "#ef4444")
    elif stress_score >= 40:
        return ("Moderate Stress", "#f59e0b")
    elif stress_score >= 20:
        return ("Low Stress",    "#10b981")
    else:
        return ("Minimal Stress","#10b981")


# ══════════════════════════════════════════════
# SAVINGS PREDICTION
# ══════════════════════════════════════════════

def predict_savings(current_savings, monthly_surplus, months_ahead=12):
    """
    Simple linear savings projection.
    Returns list of (month, projected_savings).
    No fancy ML — just honest arithmetic.
    """
    points = []
    for m in range(1, months_ahead + 1):
        projected = current_savings + (monthly_surplus * m)
        points.append({"month": m, "savings": round(max(0, projected), 0)})
    return points


def predict_emergency_fund_date(current_savings, monthly_surplus, monthly_expenses, target_months=6):
    """How many months until the user hits a 6-month emergency fund?"""
    target = monthly_expenses * target_months
    if current_savings >= target:
        return 0
    if monthly_surplus <= 0:
        return None   # Can't reach it at current rate
    shortfall = target - current_savings
    return math.ceil(shortfall / monthly_surplus)


def predict_fire_date(current_savings, monthly_surplus, annual_expenses):
    """How many years to FIRE number (25x annual expenses)?"""
    fire_number = annual_expenses * 25
    if current_savings >= fire_number:
        return 0
    if monthly_surplus <= 0:
        return None
    months_needed = math.ceil((fire_number - current_savings) / monthly_surplus)
    return round(months_needed / 12, 1)


# ══════════════════════════════════════════════
# BEHAVIORAL INSIGHTS
# ══════════════════════════════════════════════

def get_behavioral_insights(score_history, expense_history):
    """
    Analyse patterns across historical data.
    Returns list of insight strings.
    """
    insights = []

    if not score_history:
        return ["Calculate your score at least twice to unlock behavioral insights."]

    scores = [h["score"] for h in score_history]

    # Trend
    if len(scores) >= 2:
        recent   = scores[0]
        previous = scores[1]
        diff     = recent - previous
        if diff > 5:
            insights.append(f"Your score improved by {diff:.1f} points since last check. Keep the momentum.")
        elif diff < -5:
            insights.append(f"Your score dropped by {abs(diff):.1f} points. Review what changed in your expenses.")
        else:
            insights.append("Your financial score has been stable. Stability is good — now focus on growing it.")

    # Consistency
    if len(scores) >= 5:
        avg   = sum(scores) / len(scores)
        stdev = math.sqrt(sum((s - avg) ** 2 for s in scores) / len(scores))
        if stdev > 10:
            insights.append("Your score fluctuates a lot. This suggests irregular income or spending patterns.")
        else:
            insights.append("Your finances are consistently managed. Low volatility is a strength.")

    # Risk level
    risk_levels = [h["risk_level"] for h in score_history[:5]]
    if risk_levels.count("RISKY") >= 3:
        insights.append("You have been in the RISKY zone for multiple periods. Focus on building your emergency fund first.")
    elif risk_levels.count("SAFE") >= 3:
        insights.append("You have consistently maintained the SAFE rating. Now focus on growing investments.")

    # Savings rate trend
    if len(score_history) >= 3:
        sr_values = [h.get("savings_rate", 0) for h in score_history[:3]]
        if sr_values[0] > sr_values[-1]:
            insights.append(f"Your savings rate is improving — from {sr_values[-1]:.1f}% to {sr_values[0]:.1f}%.")
        elif sr_values[0] < sr_values[-1]:
            insights.append(f"Your savings rate has declined. Check if lifestyle expenses have increased.")

    # Expense patterns
    if expense_history:
        top_cat = expense_history[0]["category"] if expense_history else None
        if top_cat:
            insights.append(f"Your biggest spending category this month is {top_cat}. "
                            f"Review if this aligns with your priorities.")

    return insights if insights else ["Track your finances regularly to unlock personalized insights."]


# ══════════════════════════════════════════════
# CHART DATA BUILDERS (return dicts for plotly)
# ══════════════════════════════════════════════

def build_score_trend_data(score_history):
    """Return x=dates, y=scores for line chart."""
    history = list(reversed(score_history))   # oldest first
    dates  = [h["created_at"][:10] for h in history]
    scores = [h["score"] for h in history]
    return {"dates": dates, "scores": scores}


def build_expense_trend_data(spending_trend):
    """Return x=dates, y=amounts for bar chart."""
    dates   = [r["expense_date"] for r in spending_trend]
    amounts = [r["total"] for r in spending_trend]
    return {"dates": dates, "amounts": amounts}


def build_category_data(monthly_expenses):
    """Return categories and totals for pie/bar chart."""
    cats    = [r["category"] for r in monthly_expenses]
    totals  = [r["total"] for r in monthly_expenses]
    return {"categories": cats, "totals": totals}


def build_prediction_data(current_savings, monthly_surplus):
    """Return months and projected savings for area chart."""
    predictions = predict_savings(current_savings, monthly_surplus, 12)
    months      = [f"M{p['month']}" for p in predictions]
    savings     = [p["savings"] for p in predictions]
    return {"months": months, "savings": savings}
