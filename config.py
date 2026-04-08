# config.py
# ─────────────────────────────────────────────
# All magic numbers live here.
# To tune your model, only edit this file.
# ─────────────────────────────────────────────

# --- Risk Score Weights (must sum to 1.0) ---
WEIGHT_SAVINGS_RATE   = 0.40
WEIGHT_SURVIVAL       = 0.35
WEIGHT_EXPENSE_RATIO  = 0.25

# --- Savings Rate Thresholds (%) ---
# What % of income is left after expenses?
SAVINGS_RATE_EXCELLENT = 30   # >= 30% → full score
SAVINGS_RATE_POOR      = 0    # <= 0%  → zero score (spending more than earning)

# --- Survival Months Thresholds ---
# How many months can you survive without income?
SURVIVAL_EXCELLENT = 12   # >= 12 months → full score
SURVIVAL_POOR      = 1    # <= 1 month   → zero score

# --- Expense-to-Income Ratio Thresholds (%) ---
# What % of income goes to expenses?
EXPENSE_RATIO_EXCELLENT = 50   # <= 50% → full score (spending half or less)
EXPENSE_RATIO_POOR      = 100  # >= 100% → zero score (spending everything or more)

# --- Final Risk Bands ---
# Based on composite score 0–100
RISK_SAFE_THRESHOLD     = 65   # score >= 65 → SAFE
RISK_MODERATE_THRESHOLD = 35   # score >= 35 → MODERATE, else → RISKY

# --- Display Labels ---
RISK_LABELS = {
    "SAFE":     "✅ SAFE",
    "MODERATE": "⚠️  MODERATE",
    "RISKY":    "🔴 RISKY",
}

RISK_COLORS = {
    "SAFE":     "green",
    "MODERATE": "orange",
    "RISKY":    "red",
}
