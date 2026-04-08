# app.py
# ─────────────────────────────────────────────
# Finverse – Financial Stability Platform
# UI layer only. All math is in logic.py.
# Run with: streamlit run app.py
# ─────────────────────────────────────────────

import streamlit as st
from logic import analyse_finances
from config import RISK_COLORS
from utils import (
    format_currency,
    format_percent,
    format_months,
    get_savings_rate_message,
    get_survival_message,
    get_risk_advice,
)

# ── PAGE CONFIG ──────────────────────────────
st.set_page_config(
    page_title="Finverse – Financial Safety",
    page_icon="💰",
    layout="centered",
)

# ── HEADER ───────────────────────────────────
st.title("💰 Finverse")
st.subheader("Your Personal Financial Safety Score")
st.markdown(
    "Enter your monthly numbers below to find out if you're financially safe.",
)
st.divider()

# ── INPUTS ───────────────────────────────────
st.markdown("### 📥 Your Financial Snapshot")

col1, col2 = st.columns(2)

with col1:
    income = st.number_input(
        "Monthly Income (₹)",
        min_value=0.0,
        value=50000.0,
        step=1000.0,
        help="Your total take-home income per month after taxes.",
    )
    savings = st.number_input(
        "Total Savings (₹)",
        min_value=0.0,
        value=120000.0,
        step=5000.0,
        help="Total money you currently have saved or in liquid accounts.",
    )

with col2:
    expenses = st.number_input(
        "Monthly Expenses (₹)",
        min_value=0.0,
        value=35000.0,
        step=1000.0,
        help="All fixed + variable expenses: rent, food, EMIs, subscriptions, etc.",
    )

st.divider()

# ── CALCULATE ────────────────────────────────
calculate = st.button("📊 Calculate My Financial Safety", use_container_width=True)

if calculate:

    # Input validation
    if income <= 0:
        st.error("Please enter a valid monthly income greater than 0.")
        st.stop()

    # Run the model
    result = analyse_finances(income, expenses, savings)
    risk   = result["risk_level"]
    color  = RISK_COLORS[risk]

    st.divider()

    # ── RISK BADGE ───────────────────────────
    st.markdown("### 🎯 Your Financial Safety Rating")

    risk_display = {
        "SAFE":     ("✅ SAFE",     "You are in a strong financial position."),
        "MODERATE": ("⚠️ MODERATE", "You are stable but should improve your cushion."),
        "RISKY":    ("🔴 RISKY",    "Your finances need immediate attention."),
    }
    badge, headline = risk_display[risk]

    st.markdown(
        f"""
        <div style="
            background-color: {'#d4edda' if risk == 'SAFE' else '#fff3cd' if risk == 'MODERATE' else '#f8d7da'};
            border-left: 6px solid {'green' if risk == 'SAFE' else 'orange' if risk == 'MODERATE' else 'red'};
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 16px;
        ">
            <h2 style="margin: 0; color: {'green' if risk == 'SAFE' else 'darkorange' if risk == 'MODERATE' else 'crimson'};">
                {badge}
            </h2>
            <p style="margin: 6px 0 0 0; font-size: 16px;">{headline}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── COMPOSITE SCORE ──────────────────────
    score = result["composite_score"]
    st.markdown(f"**Financial Health Score: {score} / 100**")
    st.progress(int(score))

    st.caption(get_risk_advice(risk))
    st.divider()

    # ── KEY METRICS ──────────────────────────
    st.markdown("### 📊 Key Metrics")

    m1, m2, m3 = st.columns(3)

    with m1:
        sr = result["savings_rate"]
        st.metric(
            label="💾 Savings Rate",
            value=format_percent(sr),
            delta="of income saved",
        )
        st.caption(get_savings_rate_message(sr))

    with m2:
        sm = result["survival_months"]
        st.metric(
            label="🛟 Survival Time",
            value=format_months(sm),
            delta="without income",
        )
        st.caption(get_survival_message(sm))

    with m3:
        er = result["expense_ratio"]
        st.metric(
            label="📤 Expense Ratio",
            value=format_percent(er),
            delta="of income spent",
            delta_color="inverse",  # Higher is worse — show red for high values
        )

    st.divider()

    # ── SCORE BREAKDOWN ──────────────────────
    st.markdown("### 🔍 Score Breakdown")
    st.caption("Each component is scored 0–100. Your final score is a weighted average.")

    b1, b2, b3 = st.columns(3)

    components = [
        (b1, "Savings Rate",  result["score_savings_rate"],  "40% weight"),
        (b2, "Survival Time", result["score_survival"],      "35% weight"),
        (b3, "Expense Ratio", result["score_expense_ratio"], "25% weight"),
    ]

    for col, label, score_val, weight in components:
        with col:
            st.markdown(f"**{label}**")
            st.markdown(f"**{score_val:.0f} / 100**")
            st.progress(int(score_val))
            st.caption(weight)

    st.divider()

    # ── MONTHLY SUMMARY ──────────────────────
    st.markdown("### 💼 Monthly Summary")

    monthly_surplus = income - expenses
    s1, s2, s3 = st.columns(3)

    s1.metric("Income",   format_currency(income),   "per month")
    s2.metric("Expenses", format_currency(expenses),  "per month")
    s3.metric(
        "Monthly Surplus",
        format_currency(abs(monthly_surplus)),
        "saved" if monthly_surplus >= 0 else "overspent",
        delta_color="normal" if monthly_surplus >= 0 else "inverse",
    )

# ── FOOTER ───────────────────────────────────
st.divider()
st.caption("Finverse v1.0 · Financial data stays on your device · Not financial advice")
