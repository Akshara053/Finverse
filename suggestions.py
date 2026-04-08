# suggestions.py
# ─────────────────────────────────────────────
# Smart suggestion engine for Finverse.
# Generates personalized, actionable advice
# based on the user's financial snapshot.
# ─────────────────────────────────────────────

def generate_suggestions(income, expenses, savings, result):
    """
    Returns a list of suggestion dicts, each with:
      - icon, title, detail, impact (High/Medium/Low), action_label
    Ordered by priority (highest impact first).
    """
    suggestions = []
    sr     = result["savings_rate"]
    sm     = result["survival_months"]
    er     = result["expense_ratio"]
    risk   = result["risk_level"]
    surplus = income - expenses

    # ── EXPENSE REDUCTION ────────────────────
    if er > 70:
        target_expenses = income * 0.65           # bring ratio to 65%
        cut_needed      = round(expenses - target_expenses, 0)
        if cut_needed > 0:
            suggestions.append({
                "icon":         "✂️",
                "title":        f"Cut expenses by ₹{cut_needed:,.0f}/month",
                "detail":       (
                    f"Your expenses are {er:.0f}% of income. "
                    f"Cutting ₹{cut_needed:,.0f} would bring it to 65% — "
                    f"a much healthier ratio. Start with dining, subscriptions, and impulse buys."
                ),
                "impact":       "High",
                "new_expenses": round(expenses - cut_needed, 0),
            })

    # ── INCREASE SAVINGS ─────────────────────
    if sr < 20:
        target_savings  = income * 0.20
        save_more       = round(target_savings - max(0, surplus), 0)
        if save_more > 0:
            suggestions.append({
                "icon":       "💾",
                "title":      f"Save ₹{save_more:,.0f} more each month",
                "detail":     (
                    f"You currently save {sr:.1f}% of income. "
                    f"Saving ₹{save_more:,.0f} more reaches the 20% benchmark. "
                    f"Set a standing instruction on salary day — automate it so you never skip."
                ),
                "impact":     "High",
                "new_savings_monthly": save_more,
            })

    # ── EMERGENCY FUND ────────────────────────
    if sm < 6:
        shortfall     = round(expenses * 6 - savings, 0)
        monthly_boost = round(shortfall / 12, 0) if shortfall > 0 else 0
        if monthly_boost > 0:
            suggestions.append({
                "icon":       "🛟",
                "title":      f"Add ₹{monthly_boost:,.0f}/month to your emergency fund",
                "detail":     (
                    f"You have {sm:.1f} months of runway. The target is 6 months "
                    f"({_fmt(expenses * 6)}). At ₹{monthly_boost:,.0f}/month, "
                    f"you'd be there in 12 months. Keep it in a liquid savings account."
                ),
                "impact":     "High",
                "months_to_goal": 12,
            })

    # ── INCOME INCREASE ───────────────────────
    if risk in ("RISKY", "MODERATE") and sr < 15:
        income_boost = round(expenses * 0.30, 0)   # 30% income increase
        suggestions.append({
            "icon":   "📈",
            "title":  f"Grow income by ₹{income_boost:,.0f}/month",
            "detail": (
                "When cutting expenses isn't enough, growing income changes everything. "
                "Freelance on weekends, upskill for a raise, or monetize a hobby. "
                f"Even ₹{income_boost//2:,.0f}/month extra makes a big difference."
            ),
            "impact": "High",
        })

    # ── SUBSCRIPTION AUDIT ────────────────────
    if er > 60:
        suggestions.append({
            "icon":   "📱",
            "title":  "Audit your subscriptions",
            "detail": (
                "The average person pays for 3+ subscriptions they barely use. "
                "List everything: OTT, gym, SaaS tools, food apps. Cancel any you "
                "haven't used in 30 days. This typically frees ₹500–₹2,000/month."
            ),
            "impact": "Medium",
        })

    # ── INVESTMENT NUDGE ──────────────────────
    if sr >= 20 and sm >= 6:
        invest_amount = round(surplus * 0.5, 0)
        suggestions.append({
            "icon":   "🌱",
            "title":  f"Invest ₹{invest_amount:,.0f}/month in index funds",
            "detail": (
                "You have a healthy surplus and emergency fund. "
                f"Putting ₹{invest_amount:,.0f}/month in a Nifty 50 index fund "
                "builds long-term wealth with minimal effort. Start a SIP today."
            ),
            "impact": "Medium",
        })

    # ── AUTOMATE SAVINGS ─────────────────────
    if sr > 0 and sr < 30:
        suggestions.append({
            "icon":   "⚙️",
            "title":  "Automate your savings on Day 1",
            "detail": (
                "Set a standing instruction to move a fixed amount to savings "
                "the same day your salary arrives. "
                "'Pay yourself first' is the #1 habit of financially stable people."
            ),
            "impact": "Medium",
        })

    # ── POSITIVE REINFORCEMENT ────────────────
    if risk == "SAFE" and sm >= 12:
        suggestions.append({
            "icon":   "🎯",
            "title":  "You're in great shape — now optimize",
            "detail": (
                "Your basics are covered. Focus on: (1) maximizing NPS/PPF for tax savings, "
                "(2) diversifying investments beyond FDs, "
                "(3) reviewing insurance cover — term + health."
            ),
            "impact": "Low",
        })

    # Always return at least 1 suggestion
    if not suggestions:
        suggestions.append({
            "icon":   "✅",
            "title":  "Keep doing what you're doing",
            "detail": (
                "Your finances are healthy. Review once a month, stay consistent, "
                "and focus on growing your investments."
            ),
            "impact": "Low",
        })

    return suggestions[:5]   # Cap at 5 — don't overwhelm


def _fmt(val):
    return f"₹{val:,.0f}"


# ── WHAT-IF ENGINE ───────────────────────────

def calculate_whatif(income, expenses, savings, changes):
    """
    Given a base snapshot and a dict of changes:
      changes = {
          "income_delta":   +5000,
          "expenses_delta": -3000,
          "savings_delta":  +10000,
      }
    Returns new metrics for instant comparison.
    """
    from logic import analyse_finances
    new_income   = max(0, income   + changes.get("income_delta",   0))
    new_expenses = max(0, expenses + changes.get("expenses_delta", 0))
    new_savings  = max(0, savings  + changes.get("savings_delta",  0))

    return analyse_finances(new_income, new_expenses, new_savings)
