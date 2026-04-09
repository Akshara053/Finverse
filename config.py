# config.py  —  Finverse v7.0

# ── RISK SCORE WEIGHTS ────────────────────────
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

RISK_COLORS = {"SAFE": "green", "MODERATE": "orange", "RISKY": "red"}

# ── PERSONAS ─────────────────────────────────
PERSONAS = {
    "Student": {
        "key":                   "student",
        "icon":                  "🎓",
        "survival_target":       3,
        "savings_rate_target":   10,
        "expense_ratio_warning": 85,
        "income_label":          "Monthly Stipend / Part-time Income (₹)",
        "tips": [
            "Even ₹500/month saved builds the habit that matters most.",
            "Your skills are your biggest asset. Invest time in learning.",
            "Avoid credit cards and EMIs completely at this stage.",
            "Track every rupee — awareness precedes improvement.",
        ],
    },
    "Working Professional": {
        "key":                   "professional",
        "icon":                  "💼",
        "survival_target":       6,
        "savings_rate_target":   20,
        "expense_ratio_warning": 75,
        "income_label":          "Monthly Take-Home Salary (₹)",
        "tips": [
            "Automate savings on salary day — pay yourself first.",
            "Build a 6-month emergency fund before investing in stocks.",
            "Keep all EMIs combined under 40% of take-home pay.",
            "Review and cancel unused subscriptions every 6 months.",
        ],
    },
    "Freelancer": {
        "key":                   "freelancer",
        "icon":                  "💻",
        "survival_target":       9,
        "savings_rate_target":   25,
        "expense_ratio_warning": 70,
        "income_label":          "Average Monthly Income (₹)",
        "tips": [
            "Target 9+ months emergency fund — your income is irregular.",
            "Set aside 30% of every payment for lean months and taxes.",
            "Keep fixed monthly commitments minimal.",
            "Maintain a separate 'dry season' savings account.",
        ],
    },
    "Business Owner": {
        "key":                   "business",
        "icon":                  "🏢",
        "survival_target":       12,
        "savings_rate_target":   30,
        "expense_ratio_warning": 65,
        "income_label":          "Monthly Personal Salary from Business (₹)",
        "tips": [
            "Separate personal and business finances completely.",
            "Pay yourself a fixed monthly salary. Never mix accounts.",
            "Build 12 months personal runway before scaling.",
            "Maintain both a business and personal emergency fund.",
        ],
    },
    "Homemaker": {
        "key":                   "homemaker",
        "icon":                  "🏠",
        "survival_target":       6,
        "savings_rate_target":   15,
        "expense_ratio_warning": 80,
        "income_label":          "Monthly Household Budget (₹)",
        "tips": [
            "Track household spending weekly — small leaks add up.",
            "Negotiate better rates on recurring bills annually.",
            "Build personal savings separate from household funds.",
            "Start a small recurring investment for financial independence.",
        ],
    },
    "Retired": {
        "key":                   "retired",
        "icon":                  "🌅",
        "survival_target":       24,
        "savings_rate_target":   10,
        "expense_ratio_warning": 90,
        "income_label":          "Monthly Pension / Investment Income (₹)",
        "tips": [
            "Preserve capital first. Growth is secondary.",
            "Keep 24 months of expenses liquid and accessible.",
            "Allocate 60%+ to debt instruments for stability.",
            "Review medical insurance cover annually.",
        ],
    },
}
