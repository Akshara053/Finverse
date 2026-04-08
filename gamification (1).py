# gamification.py
# ─────────────────────────────────────────────
# Levels, badges, and challenges.
# All gamification logic lives here.
# ─────────────────────────────────────────────

# ── LEVELS ───────────────────────────────────
# (min_score, name, icon, background_color)
LEVELS = [
    (85, "Platinum", "💎", "#e3f2fd"),
    (70, "Gold",     "🥇", "#fffde7"),
    (50, "Silver",   "🥈", "#f5f5f5"),
    (25, "Bronze",   "🥉", "#fff3e0"),
    (0,  "Starter",  "🌱", "#f1f8e9"),
]

LEVEL_MESSAGES = {
    "Platinum": "Top tier financial health. You're an inspiration.",
    "Gold":     "Excellent finances. You're almost at the peak!",
    "Silver":   "Solid foundation. A few tweaks can push you to Gold.",
    "Bronze":   "You've started the journey. Small steps = big change.",
    "Starter":  "Your financial story begins here. Every rupee counts.",
}


def get_level(score):
    """Return level dict for a given composite score."""
    for threshold, name, icon, color in LEVELS:
        if score >= threshold:
            return {
                "name":      name,
                "icon":      icon,
                "color":     color,
                "threshold": threshold,
                "message":   LEVEL_MESSAGES[name],
            }
    # Fallback (score < 0)
    return {
        "name": "Starter", "icon": "🌱",
        "color": "#f1f8e9", "threshold": 0,
        "message": LEVEL_MESSAGES["Starter"],
    }


def get_next_level(score):
    """Return the next level to unlock, or None if already at max."""
    for i, (threshold, name, icon, color) in enumerate(LEVELS):
        if score >= threshold:
            if i > 0:
                next_threshold, next_name, next_icon, _ = LEVELS[i - 1]
                return {
                    "name":          next_name,
                    "icon":          next_icon,
                    "points_needed": round(next_threshold - score, 1),
                }
            return None  # Already Platinum
    return None


# ── BADGES ───────────────────────────────────
# (metric_key, operator, threshold, badge_name, description)
# Ordered so more impressive badges come first for deduplication.
BADGE_RULES = [
    ("savings_rate",    ">=", 30,  "💰 Super Saver",        "Saving 30%+ of income"),
    ("savings_rate",    ">=", 20,  "📈 Good Saver",          "Saving 20%+ of income"),
    ("savings_rate",    ">=", 10,  "🌱 Saver Seedling",      "Saving 10%+ of income"),
    ("survival_months", ">=", 12,  "🏰 Financial Fortress",  "12+ months emergency fund"),
    ("survival_months", ">=", 6,   "🛟 Emergency Ready",     "6 months of runway"),
    ("survival_months", ">=", 3,   "⛑️  Safety Net",          "3 months of runway"),
    ("expense_ratio",   "<=", 50,  "✂️  Lean Spender",        "Expenses under 50% of income"),
    ("expense_ratio",   "<=", 70,  "⚖️  Balanced",            "Expenses under 70% of income"),
    ("composite_score", ">=", 85,  "🌟 Financial Star",      "Score above 85"),
    ("composite_score", ">=", 65,  "✅ Safe Zone",            "Achieved SAFE rating"),
]

# Category keys for deduplication (one badge per category)
BADGE_CATEGORY = {
    "Super Saver": "saver", "Good Saver": "saver", "Saver Seedling": "saver",
    "Financial Fortress": "survival", "Emergency Ready": "survival", "Safety Net": "survival",
    "Lean Spender": "expense", "Balanced": "expense",
    "Financial Star": "score", "Safe Zone": "score",
}


def get_badges(result):
    """Return list of earned badge dicts, one per category."""
    earned = []
    seen_categories = set()

    for metric, op, threshold, name, desc in BADGE_RULES:
        val = result.get(metric, 0)
        qualifies = (op == ">=" and val >= threshold) or (op == "<=" and val <= threshold)
        if qualifies:
            # Extract short name for category lookup
            short_name = name.split(" ", 1)[1] if " " in name else name
            category = BADGE_CATEGORY.get(short_name, short_name)
            if category not in seen_categories:
                earned.append({"name": name, "desc": desc})
                seen_categories.add(category)

    return earned


# ── CHALLENGES ───────────────────────────────
CHALLENGES = [
    {
        "id":         "no_eat_out",
        "name":       "🍱 Home Chef Week",
        "desc":       "Don't eat out for 7 days straight",
        "reward_xp":  50,
    },
    {
        "id":         "save_extra",
        "name":       "💾 Save ₹1,000 Extra",
        "desc":       "Save ₹1,000 more than your usual this month",
        "reward_xp":  75,
    },
    {
        "id":         "track_7_days",
        "name":       "📅 7-Day Tracker Streak",
        "desc":       "Track your expenses every day for 7 days",
        "reward_xp":  100,
    },
    {
        "id":         "cut_subs",
        "name":       "✂️ Subscription Audit",
        "desc":       "Cancel at least 1 unused subscription",
        "reward_xp":  30,
    },
    {
        "id":         "no_impulse",
        "name":       "🧘 Mindful Spender",
        "desc":       "Zero impulse purchases for 7 days",
        "reward_xp":  80,
    },
    {
        "id":         "emergency_step",
        "name":       "🛟 Emergency Fund Step",
        "desc":       "Add ₹5,000 to your emergency fund",
        "reward_xp":  90,
    },
]


def get_challenges():
    return CHALLENGES


def get_total_xp(completed_ids):
    """Calculate total XP earned from completed challenge IDs."""
    xp_map = {ch["id"]: ch["reward_xp"] for ch in CHALLENGES}
    return sum(xp_map.get(cid, 0) for cid in completed_ids)
