# config.py
# ─────────────────────────────────────────────
# All constants, thresholds, weights, and
# persona configs live here.
# To tune the model, only edit this file.
# ─────────────────────────────────────────────

# ── RISK SCORE WEIGHTS (must sum to 1.0) ─────
WEIGHT_SAVINGS_RATE   = 0.40
WEIGHT_SURVIVAL       = 0.35
WEIGHT_EXPENSE_RATIO  = 0.25

# ── METRIC THRESHOLDS ────────────────────────
SAVINGS_RATE_EXCELLENT  = 30
SAVINGS_RATE_POOR       = 0

SURVIVAL_EXCELLENT      = 12
SURVIVAL_POOR           = 1

EXPENSE_RATIO_EXCELLENT = 50
EXPENSE_RATIO_POOR      = 100

# ── RISK BANDS ───────────────────────────────
RISK_SAFE_THRESHOLD     = 65
RISK_MODERATE_THRESHOLD = 35

RISK_COLORS = {
    "SAFE":     "green",
    "MODERATE": "orange",
    "RISKY":    "red",
}

# ── PERSONAS ─────────────────────────────────
# Different life stages → different targets.
PERSONAS = {
    "🎓 Student": {
        "key":                   "student",
        "survival_target":       3,
        "savings_rate_target":   10,
        "expense_ratio_warning": 85,
        "income_label":          "Monthly Stipend / Part-time Income (₹)",
        "tips": [
            "Even ₹500/month builds the saving habit — start today.",
            "Your biggest asset is your skill set. Invest time in learning.",
            "Avoid credit cards and EMIs as much as possible.",
            "Track every rupee — awareness is step one.",
        ],
    },
    "💼 Working Professional": {
        "key":                   "professional",
        "survival_target":       6,
        "savings_rate_target":   20,
        "expense_ratio_warning": 75,
        "income_label":          "Monthly Take-Home Salary (₹)",
        "tips": [
            "Automate savings — set a standing instruction on salary day.",
            "Build a 6-month emergency fund before investing in stocks.",
            "Keep all EMIs under 40% of take-home pay.",
            "Review subscriptions every 6 months. Cancel unused ones.",
        ],
    },
    "💻 Freelancer": {
        "key":                   "freelancer",
        "survival_target":       9,
        "savings_rate_target":   25,
        "expense_ratio_warning": 70,
        "income_label":          "Average Monthly Income (₹)",
        "tips": [
            "Aim for 9+ months emergency fund — income is variable.",
            "Set aside 30% of every payment for taxes and lean months.",
            "Keep fixed expenses minimal to survive slow seasons.",
            "Maintain a separate business buffer account.",
        ],
    },
    "🏢 Business Owner": {
        "key":                   "business",
        "survival_target":       12,
        "savings_rate_target":   30,
        "expense_ratio_warning": 65,
        "income_label":          "Monthly Personal Salary from Business (₹)",
        "tips": [
            "Separate personal and business finances completely.",
            "Pay yourself a fixed monthly salary from the business.",
            "Build 12 months personal runway before scaling.",
            "Maintain both a business and personal emergency fund.",
        ],
    },
}
