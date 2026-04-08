# app.py  —  Finverse v3.0
# Run: streamlit run app.py
# ─────────────────────────────────────────────

import streamlit as st
from datetime import datetime

from logic        import analyse_finances, calculate_savings_rules, analyse_compatibility, recommended_partner_income
from config       import PERSONAS
from gamification import get_level, get_next_level, get_badges, get_challenges, get_total_xp
from suggestions  import generate_suggestions, calculate_whatif
from utils        import (
    format_currency, format_percent, format_months,
    get_savings_rate_message, get_survival_message, get_risk_advice,
)

# ══════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="Finverse — Financial Safety",
    page_icon="💰",
    layout="centered",
)

# ══════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }
#MainMenu, footer, header   { visibility: hidden; }

.stApp { background: #f4f6fb; }

.block-container {
    max-width: 780px !important;
    padding: 2rem 1.5rem 4rem !important;
}

/* ── CARD ── */
.fv-card {
    background: #fff;
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.055);
    border: 1px solid #eef0f6;
}

/* ── SECTION TITLE ── */
.fv-section-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #9aa5bc;
    margin: 0 0 14px 0;
}

/* ── METRIC CHIPS ── */
.fv-chip-row { display:flex; gap:10px; flex-wrap:wrap; }
.fv-chip {
    background:#f4f6fb; border-radius:12px;
    padding:14px 16px; flex:1; min-width:130px; text-align:center;
}
.fv-chip-value { font-size:21px; font-weight:700; font-family:'DM Mono',monospace; color:#1a2035; }
.fv-chip-label { font-size:12px; color:#9aa5bc; font-weight:500; margin-top:3px; }
.fv-chip-sub   { font-size:11px; color:#b8c0d0; margin-top:2px; line-height:1.4; }

/* ── RISK BADGES ── */
.fv-risk-safe     { background:#e8f9f0; color:#1a7a4a; border:1.5px solid #a8e6c3; border-radius:8px; padding:3px 12px; font-weight:700; font-size:13px; display:inline-block; }
.fv-risk-moderate { background:#fff7e6; color:#b86a00; border:1.5px solid #fcd58a; border-radius:8px; padding:3px 12px; font-weight:700; font-size:13px; display:inline-block; }
.fv-risk-risky    { background:#fdecea; color:#c0392b; border:1.5px solid #f5b8b3; border-radius:8px; padding:3px 12px; font-weight:700; font-size:13px; display:inline-block; }

/* ── LEVEL BANNER ── */
.fv-level-banner { border-radius:12px; padding:20px 22px; display:flex; align-items:center; gap:16px; }
.fv-level-icon   { font-size:46px; line-height:1; }
.fv-level-title  { font-size:21px; font-weight:700; color:#1a2035; margin:0 0 3px 0; }
.fv-level-msg    { font-size:13px; color:#5a6479; margin:0; }

/* ── PROGRESS BAR ── */
.fv-bar-bg   { background:#eef0f6; border-radius:99px; height:7px; margin:4px 0 12px 0; }
.fv-bar-fill { height:7px; border-radius:99px; }

/* ── SUGGESTION ── */
.fv-suggestion {
    border-radius:12px; padding:15px 17px; margin-bottom:10px;
    border-left:4px solid transparent; background:#fff;
    box-shadow:0 1px 6px rgba(0,0,0,0.05);
}
.fv-sug-high   { border-left-color:#e74c3c; }
.fv-sug-medium { border-left-color:#f39c12; }
.fv-sug-low    { border-left-color:#27ae60; }
.fv-sug-title  { font-size:15px; font-weight:700; color:#1a2035; margin:0 0 5px 0; }
.fv-sug-detail { font-size:13px; color:#5a6479; margin:0; line-height:1.6; }
.fv-sug-impact { font-size:11px; font-weight:700; padding:2px 8px; border-radius:4px; margin-left:8px; vertical-align:middle; }
.fv-impact-high   { background:#fdecea; color:#c0392b; }
.fv-impact-medium { background:#fff7e6; color:#b86a00; }
.fv-impact-low    { background:#e8f9f0; color:#1a7a4a; }

/* ── WHAT-IF COMPARE ── */
.fv-compare-row  { display:flex; gap:10px; align-items:center; margin-bottom:8px; }
.fv-compare-label  { font-size:13px; color:#9aa5bc; width:130px; flex-shrink:0; }
.fv-compare-before { font-family:'DM Mono',monospace; font-size:14px; color:#9aa5bc; width:72px; }
.fv-compare-arrow  { color:#c8cfe0; font-size:13px; }
.fv-compare-after-up   { font-family:'DM Mono',monospace; font-size:14px; color:#1a7a4a; font-weight:700; }
.fv-compare-after-down { font-family:'DM Mono',monospace; font-size:14px; color:#c0392b; font-weight:700; }
.fv-compare-after-same { font-family:'DM Mono',monospace; font-size:14px; color:#5a6479; font-weight:600; }

/* ── BADGE PILL ── */
.fv-badge-pill {
    display:inline-block; background:#f4f6fb; border:1px solid #e2e8f5;
    border-radius:20px; padding:5px 13px; font-size:13px; font-weight:600;
    color:#2d3a56; margin:3px;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap:3px; background:#eef0f6; padding:4px; border-radius:12px;
}
.stTabs [data-baseweb="tab"] {
    border-radius:9px; padding:7px 14px; font-weight:600; font-size:13px;
}
.stTabs [aria-selected="true"] {
    background:#fff !important; color:#1a2035 !important;
    box-shadow:0 1px 4px rgba(0,0,0,0.08);
}

/* ── BUTTONS ── */
.stButton > button {
    background:#1a2035; color:#fff; border:none; border-radius:10px;
    font-weight:700; font-size:14px; padding:12px 20px; width:100%;
    transition:all 0.2s;
}
.stButton > button:hover {
    background:#2d3a56;
    box-shadow:0 4px 12px rgba(26,32,53,0.22);
    transform:translateY(-1px);
}

/* ── INPUTS ── */
.stNumberInput > div > div { border-radius:10px !important; border-color:#dde2ef !important; }
.stSelectbox  > div > div { border-radius:10px !important; border-color:#dde2ef !important; }
label { font-size:14px !important; font-weight:600 !important; color:#2d3a56 !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def score_ring(score, size=130):
    """Pure SVG circular score ring — no external libraries."""
    pct   = score / 100
    r     = 44
    circ  = 2 * 3.14159 * r
    dash  = round(pct * circ, 1)
    gap   = round(circ - dash, 1)
    color = "#1a7a4a" if score >= 65 else ("#d97706" if score >= 35 else "#c0392b")
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;padding:8px 0 4px 0;">
      <svg width="{size}" height="{size}" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="{r}" fill="none" stroke="#eef0f6" stroke-width="9"/>
        <circle cx="50" cy="50" r="{r}" fill="none" stroke="{color}" stroke-width="9"
                stroke-dasharray="{dash} {gap}"
                stroke-dashoffset="{circ * 0.25}"
                stroke-linecap="round"/>
        <text x="50" y="46" text-anchor="middle"
              font-family="DM Mono, monospace" font-size="20" font-weight="700" fill="#1a2035">{score:.0f}</text>
        <text x="50" y="62" text-anchor="middle"
              font-family="DM Sans, sans-serif" font-size="10" fill="#9aa5bc">/ 100</text>
      </svg>
      <span style="font-size:12px;color:#9aa5bc;font-weight:500;margin-top:4px;">Health Score</span>
    </div>"""


def bar(pct, color="#1a2035"):
    pct = min(100, max(0, pct))
    return (
        f'<div class="fv-bar-bg">'
        f'<div class="fv-bar-fill" style="width:{pct}%;background:{color};"></div>'
        f'</div>'
    )


def risk_badge(risk):
    cls = {"SAFE":"fv-risk-safe","MODERATE":"fv-risk-moderate","RISKY":"fv-risk-risky"}
    lbl = {"SAFE":"✅ SAFE","MODERATE":"⚠️ MODERATE","RISKY":"🔴 RISKY"}
    return f'<span class="{cls[risk]}">{lbl[risk]}</span>'


def compare_row(label, before, after, fmt_fn=None, higher_is_better=True):
    b_str = fmt_fn(before) if fmt_fn else str(round(before, 1))
    a_str = fmt_fn(after)  if fmt_fn else str(round(after,  1))
    diff  = after - before
    if   abs(diff) < 0.05:                        cls = "fv-compare-after-same"
    elif (diff > 0) == higher_is_better:          cls = "fv-compare-after-up"
    else:                                          cls = "fv-compare-after-down"
    return (
        f'<div class="fv-compare-row">'
        f'<span class="fv-compare-label">{label}</span>'
        f'<span class="fv-compare-before">{b_str}</span>'
        f'<span class="fv-compare-arrow">→</span>'
        f'<span class="{cls}">{a_str}</span>'
        f'</div>'
    )


# ══════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════
_defaults = {
    "daily_expenses":  [],
    "daily_budget":    1000.0,
    "streak":          1,
    "challenges_done": set(),
    "my_score":        None,
    "my_name":         "",
    "last_result":     None,
    "last_income":     50000.0,
    "last_expenses":   35000.0,
    "last_savings":    120000.0,
    "leaderboard": [
        {"name":"Priya S.",  "score":82.3,"level":"🥇 Gold"},
        {"name":"Rahul M.",  "score":74.1,"level":"🥇 Gold"},
        {"name":"Aisha K.",  "score":68.5,"level":"🥇 Gold"},
        {"name":"Vikram N.", "score":61.2,"level":"🥈 Silver"},
        {"name":"Sneha R.",  "score":55.8,"level":"🥈 Silver"},
        {"name":"Arjun T.",  "score":44.3,"level":"🥈 Silver"},
        {"name":"Meera P.",  "score":38.7,"level":"🥉 Bronze"},
    ],
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════
st.markdown("""
<div style="padding:8px 0 22px 0;">
  <div style="font-size:27px;font-weight:800;color:#1a2035;letter-spacing:-0.5px;">💰 Finverse</div>
  <div style="font-size:14px;color:#9aa5bc;margin-top:2px;font-weight:500;">
      Your Personal Financial Safety Platform
  </div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    persona_name = st.selectbox("Who are you?", list(PERSONAS.keys()), index=1)
    persona      = PERSONAS[persona_name]

    st.markdown(
        f"<div style='background:#f4f6fb;border-radius:10px;padding:12px 14px;"
        f"font-size:13px;color:#2d3a56;'>"
        f"🎯 <b>Savings target:</b> {persona['savings_rate_target']}%<br>"
        f"🛟 <b>Emergency goal:</b> {persona['survival_target']} months"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("### 💡 Tips for You")
    for tip in persona["tips"]:
        st.caption(f"• {tip}")
    st.divider()
    total_xp = get_total_xp(st.session_state.challenges_done)
    st.markdown(
        f"<div style='text-align:center;padding:14px;background:#f4f6fb;border-radius:10px;'>"
        f"<div style='font-size:22px;font-weight:800;color:#1a2035;'>⚡ {total_xp} XP</div>"
        f"<div style='font-size:12px;color:#9aa5bc;'>Complete challenges to earn more</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.caption("Finverse v3.0 · Not financial advice")


# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 My Score", "🔭 What-If", "💡 Suggestions",
    "📅 Tracker",  "💑 Partner", "🏆 Leaderboard",
])


# ════════════════════════════════════════════
# TAB 1 — MY SCORE
# ════════════════════════════════════════════
with tab1:
    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-section-title">Your Monthly Numbers</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        income  = st.number_input(persona["income_label"], min_value=0.0, value=50000.0, step=1000.0, key="t1_inc")
        savings = st.number_input("Total Savings (₹)",      min_value=0.0, value=120000.0, step=5000.0, key="t1_sav")
    with c2:
        expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=35000.0, step=1000.0, key="t1_exp")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("📊  Calculate My Financial Safety Score", key="t1_calc"):
        if income <= 0:
            st.error("Please enter a valid income greater than ₹0.")
            st.stop()

        result = analyse_finances(income, expenses, savings)
        level  = get_level(result["composite_score"])
        next_l = get_next_level(result["composite_score"])
        badges = get_badges(result)
        score  = result["composite_score"]
        risk   = result["risk_level"]

        st.session_state.my_score    = score
        st.session_state.last_result = result
        st.session_state.last_income   = income
        st.session_state.last_expenses = expenses
        st.session_state.last_savings  = savings

        # Score + Level
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        ring_col, info_col = st.columns([1, 2])
        with ring_col:
            st.markdown(score_ring(score), unsafe_allow_html=True)
        with info_col:
            st.markdown(
                f'<div class="fv-level-banner" style="background:{level["color"]};margin-bottom:0;">'
                f'<span class="fv-level-icon">{level["icon"]}</span>'
                f'<div><p class="fv-level-title">{level["name"]} Level</p>'
                f'<p class="fv-level-msg">{level["message"]}</p>'
                f'<br>{risk_badge(risk)}</div></div>',
                unsafe_allow_html=True,
            )
            if next_l:
                st.caption(f"🎯 {next_l['points_needed']} pts to {next_l['icon']} {next_l['name']}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Metric Chips
        sr = result["savings_rate"]
        sm = result["survival_months"]
        er = result["expense_ratio"]
        sr_clr = "#1a7a4a" if sr >= 20 else ("#d97706" if sr >= 10 else "#c0392b")
        sm_clr = "#1a7a4a" if sm >= 6  else ("#d97706" if sm >= 3  else "#c0392b")
        er_clr = "#1a7a4a" if er <= 60 else ("#d97706" if er <= 80 else "#c0392b")

        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-section-title">Key Metrics</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="fv-chip-row">
            <div class="fv-chip">
                <div class="fv-chip-value" style="color:{sr_clr};">{sr:.1f}%</div>
                <div class="fv-chip-label">💾 Savings Rate</div>
                <div class="fv-chip-sub">{get_savings_rate_message(sr)}</div>
            </div>
            <div class="fv-chip">
                <div class="fv-chip-value" style="color:{sm_clr};">{format_months(sm)}</div>
                <div class="fv-chip-label">🛟 Survival Time</div>
                <div class="fv-chip-sub">{get_survival_message(sm)}</div>
            </div>
            <div class="fv-chip">
                <div class="fv-chip-value" style="color:{er_clr};">{er:.1f}%</div>
                <div class="fv-chip-label">📤 Expense Ratio</div>
                <div class="fv-chip-sub">of income on expenses</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Savings Rate")
        st.markdown(bar(min(100, int(sr / 30 * 100)), sr_clr), unsafe_allow_html=True)
        st.caption("Survival Coverage")
        st.markdown(bar(min(100, int(sm / 12 * 100)), sm_clr), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Monthly summary
        surplus = income - expenses
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-section-title">Monthly Picture</p>', unsafe_allow_html=True)
        ms1, ms2, ms3 = st.columns(3)
        ms1.metric("Income",   format_currency(income))
        ms2.metric("Expenses", format_currency(expenses))
        ms3.metric(
            "Surplus" if surplus >= 0 else "Deficit",
            format_currency(abs(surplus)),
            delta_color="normal" if surplus >= 0 else "inverse",
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Badges
        if badges:
            st.markdown('<div class="fv-card">', unsafe_allow_html=True)
            st.markdown('<p class="fv-section-title">Earned Badges</p>', unsafe_allow_html=True)
            st.markdown("".join(f'<span class="fv-badge-pill">{b["name"]}</span>' for b in badges), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Challenges
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-section-title">Active Challenges</p>', unsafe_allow_html=True)
        for ch in get_challenges():
            done = ch["id"] in st.session_state.challenges_done
            ca, cb = st.columns([5, 1])
            with ca:
                st.markdown(f"{'~~' if done else '**'}{ch['name']}{'~~' if done else '**'} {'✅' if done else ''}")
                st.caption(f"{ch['desc']} · +{ch['reward_xp']} XP")
            with cb:
                if not done and st.button("Done", key=f"ch_{ch['id']}"):
                    st.session_state.challenges_done.add(ch["id"])
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.caption("💡 Check **Suggestions** and **What-If** tabs for your action plan.")

    else:
        st.markdown("""
        <div class="fv-card" style="text-align:center;padding:44px 28px;">
            <div style="font-size:46px;margin-bottom:12px;">📊</div>
            <div style="font-size:17px;font-weight:600;color:#2d3a56;">Enter your numbers above</div>
            <div style="font-size:14px;color:#9aa5bc;margin-top:6px;">Your financial safety score appears here</div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2 — WHAT-IF SIMULATOR
# ════════════════════════════════════════════
with tab2:
    if not st.session_state.last_result:
        st.info("👈 Calculate your score in **My Score** first, then come back here.")
    else:
        base  = st.session_state.last_result
        b_inc = st.session_state.last_income
        b_exp = st.session_state.last_expenses
        b_sav = st.session_state.last_savings

        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-section-title">Adjust Your Scenario</p>', unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:13px;color:#5a6479;margin:0 0 14px 0;'>"
            "Move the sliders to see the instant impact on your financial health score.</p>",
            unsafe_allow_html=True,
        )
        inc_delta = st.slider("📈 Income change (₹/month)",   -20000, 50000, 0, 1000)
        exp_delta = st.slider("✂️ Expense change (₹/month)",  -20000, 20000, 0,  500)
        sav_delta = st.slider("💰 Extra savings added (₹)",        0, 500000, 0, 5000)
        st.markdown('</div>', unsafe_allow_html=True)

        new_res   = calculate_whatif(b_inc, b_exp, b_sav,
                                     {"income_delta": inc_delta,
                                      "expenses_delta": exp_delta,
                                      "savings_delta": sav_delta})
        new_score = new_res["composite_score"]
        old_score = base["composite_score"]
        diff      = new_score - old_score

        # Ring comparison
        r_a, r_b = st.columns(2)
        with r_a:
            st.markdown(
                f'<div class="fv-card" style="text-align:center;">'
                f'<p class="fv-section-title" style="text-align:center;">Current</p>'
                f'{score_ring(old_score, 118)}'
                f'<div style="margin-top:8px;">{risk_badge(base["risk_level"])}</div>'
                f'</div>', unsafe_allow_html=True)
        with r_b:
            diff_color = "#1a7a4a" if diff >= 0 else "#c0392b"
            arrow      = "↑" if diff > 0 else ("↓" if diff < 0 else "→")
            st.markdown(
                f'<div class="fv-card" style="text-align:center;">'
                f'<p class="fv-section-title" style="text-align:center;">New Scenario</p>'
                f'{score_ring(new_score, 118)}'
                f'<div style="margin-top:8px;">{risk_badge(new_res["risk_level"])}</div>'
                f'<div style="font-size:15px;font-weight:700;color:{diff_color};margin-top:6px;">'
                f'{arrow} {abs(diff):.1f} pts</div>'
                f'</div>', unsafe_allow_html=True)

        # Metric diff
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-section-title">Metric Comparison</p>', unsafe_allow_html=True)
        rows = (
            compare_row("Savings Rate",
                        base["savings_rate"], new_res["savings_rate"],
                        lambda v: f"{v:.1f}%") +
            compare_row("Survival Time",
                        base["survival_months"], new_res["survival_months"],
                        lambda v: format_months(v)) +
            compare_row("Expense Ratio",
                        base["expense_ratio"], new_res["expense_ratio"],
                        lambda v: f"{v:.1f}%", higher_is_better=False) +
            compare_row("Monthly Surplus",
                        b_inc - b_exp,
                        (b_inc + inc_delta) - (b_exp + exp_delta),
                        lambda v: format_currency(v))
        )
        st.markdown(rows, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if   diff > 10: st.success(f"🚀 +{diff:.1f} pts! Moves you to **{new_res['risk_level']}**.")
        elif diff > 0:  st.info(f"📈 Small gain of {diff:.1f} points.")
        elif diff < -10:st.error(f"⚠️ -{abs(diff):.1f} pts. Drops to **{new_res['risk_level']}**.")
        elif diff < 0:  st.warning(f"📉 Small decline of {abs(diff):.1f} points.")
        else:           st.info("↔️ No meaningful change.")


# ════════════════════════════════════════════
# TAB 3 — SUGGESTIONS
# ════════════════════════════════════════════
with tab3:
    if not st.session_state.last_result:
        st.info("👈 Calculate your score in **My Score** first.")
    else:
        res   = st.session_state.last_result
        b_inc = st.session_state.last_income
        b_exp = st.session_state.last_expenses
        b_sav = st.session_state.last_savings
        suggs = generate_suggestions(b_inc, b_exp, b_sav, res)

        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-section-title">Your Personalised Action Plan</p>', unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:14px;color:#5a6479;margin:0 0 4px 0;'>"
            "Based on your exact numbers — highest impact moves first.</p>",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        order = {"High": 0, "Medium": 1, "Low": 2}
        for s in sorted(suggs, key=lambda x: order.get(x["impact"], 3)):
            cls  = {"High":"fv-sug-high","Medium":"fv-sug-medium","Low":"fv-sug-low"}[s["impact"]]
            icls = {"High":"fv-impact-high","Medium":"fv-impact-medium","Low":"fv-impact-low"}[s["impact"]]
            st.markdown(
                f'<div class="fv-suggestion {cls}">'
                f'<p class="fv-sug-title">{s["icon"]} {s["title"]}'
                f'<span class="fv-sug-impact {icls}">{s["impact"]} Impact</span></p>'
                f'<p class="fv-sug-detail">{s["detail"]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("""
        <div class="fv-card" style="background:#0f1724;color:#fff;margin-top:8px;">
            <p style="font-size:17px;font-weight:700;margin:0 0 8px 0;color:#fff;">
                "Save first. Spend what's left."
            </p>
            <p style="font-size:13px;color:#8892a4;margin:0;line-height:1.7;">
                Most people spend first and save whatever remains — usually nothing.
                Flip the order: on salary day, instantly move your savings target to a
                separate account. Your spending is now naturally capped.
                This single habit outperforms all other advice combined.
            </p>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 4 — DAILY TRACKER
# ════════════════════════════════════════════
with tab4:
    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-section-title">Daily Expense Tracker</p>', unsafe_allow_html=True)
    sb1, sb2 = st.columns(2)
    with sb1:
        st.metric("🔥 Streak", f"{st.session_state.streak} day(s)")
    with sb2:
        st.session_state.daily_budget = st.number_input(
            "Daily Budget (₹)", min_value=0.0, value=st.session_state.daily_budget, step=100.0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-section-title">Add Expense</p>', unsafe_allow_html=True)
    ea, eb, ec = st.columns([2, 2, 3])
    with ea:
        cat = st.selectbox("Category", ["🍜 Food","🚗 Transport","🛒 Shopping",
                                         "💡 Bills","🎬 Entertainment","💊 Health",
                                         "📚 Education","🎁 Others"])
    with eb:
        amt = st.number_input("Amount (₹)", min_value=0.0, value=0.0, step=10.0)
    with ec:
        note = st.text_input("Note", placeholder="e.g. Lunch at office")

    if st.button("➕  Add Expense", key="add_exp"):
        if amt > 0:
            st.session_state.daily_expenses.append({
                "category": cat, "amount": amt,
                "note": note or "—", "time": datetime.now().strftime("%H:%M"),
            })
            st.rerun()
        else:
            st.warning("Enter an amount greater than ₹0.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.daily_expenses:
        total   = sum(e["amount"] for e in st.session_state.daily_expenses)
        budget  = st.session_state.daily_budget
        left    = budget - total
        pct     = min(100, int(total / budget * 100)) if budget > 0 else 100
        b_color = "#1a7a4a" if pct < 70 else ("#d97706" if pct < 90 else "#c0392b")

        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-section-title">Today\'s Summary</p>', unsafe_allow_html=True)
        ds1, ds2, ds3 = st.columns(3)
        ds1.metric("Spent",  format_currency(total))
        ds2.metric("Budget", format_currency(budget))
        ds3.metric("Left" if left >= 0 else "Over", format_currency(abs(left)),
                   delta_color="normal" if left >= 0 else "inverse")
        st.caption(f"Budget used: {pct}%")
        st.markdown(bar(pct, b_color), unsafe_allow_html=True)
        if pct >= 90: st.error("⚠️ Almost at daily limit!")
        elif pct >= 70: st.warning("Spending is high today.")
        else: st.success("On track ✅")

        st.divider()
        for exp in reversed(st.session_state.daily_expenses):
            el, er = st.columns([4, 1])
            el.markdown(f"**{exp['category']}** · {exp['note']} <span style='color:#b0b8cc;font-size:12px;'>({exp['time']})</span>",
                        unsafe_allow_html=True)
            er.markdown(f"**{format_currency(exp['amount'])}**")

        st.divider()
        if st.button("✅  End Day & Save Streak", use_container_width=True):
            st.session_state.daily_expenses = []
            st.session_state.streak += 1
            st.success(f"🔥 Streak: {st.session_state.streak} days!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No expenses yet today. Start tracking to build your streak! 🔥")


# ════════════════════════════════════════════
# TAB 5 — PARTNER TEST
# ════════════════════════════════════════════
with tab5:
    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-section-title">Partner Financial Compatibility</p>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;color:#5a6479;margin:0;'>"
                "Enter both profiles for combined health score, compatibility rating, "
                "and ideal partner income for a stable future together.</p>",
                unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        st.markdown("**👤 You**")
        p1i = st.number_input("Your Income",   min_value=0.0, value=50000.0, step=1000.0, key="p1i")
        p1e = st.number_input("Your Expenses", min_value=0.0, value=35000.0, step=1000.0, key="p1e")
        p1s = st.number_input("Your Savings",  min_value=0.0, value=120000.0,step=5000.0, key="p1s")
    with pc2:
        st.markdown("**👤 Partner**")
        p2i = st.number_input("Partner Income",   min_value=0.0, value=45000.0, step=1000.0, key="p2i")
        p2e = st.number_input("Partner Expenses", min_value=0.0, value=30000.0, step=1000.0, key="p2e")
        p2s = st.number_input("Partner Savings",  min_value=0.0, value=80000.0, step=5000.0, key="p2s")

    if st.button("💑  Calculate Compatibility", use_container_width=True):
        r1     = analyse_finances(p1i, p1e, p1s)
        r2     = analyse_finances(p2i, p2e, p2s)
        compat = analyse_compatibility(r1, r2)
        cs     = compat["compatibility_score"]

        if   cs >= 75: lbl, bg, bdr = "💚 Excellent Match",    "#e8f9f0", "#1a7a4a"
        elif cs >= 55: lbl, bg, bdr = "💛 Good Match",         "#fffde7", "#d97706"
        elif cs >= 35: lbl, bg, bdr = "🟠 Needs Work",         "#fff3cd", "#f39c12"
        else:          lbl, bg, bdr = "🔴 Financial Mismatch", "#fdecea", "#c0392b"

        st.markdown(
            f"<div style='background:{bg};border-left:5px solid {bdr};"
            f"border-radius:12px;padding:18px 22px;text-align:center;margin-bottom:14px;'>"
            f"<h3 style='margin:0;color:{bdr};'>{lbl}</h3>"
            f"<div style='font-size:38px;font-weight:800;color:{bdr};margin:4px 0;'>"
            f"{cs:.0f}<span style='font-size:16px;'> / 100</span></div></div>",
            unsafe_allow_html=True,
        )
        ia, ib, ic = st.columns(3)
        ia.metric("Your Score",      f"{r1['composite_score']} / 100")
        ib.metric("Partner's Score", f"{r2['composite_score']} / 100")
        ic.metric("Alignment",       f"{compat['alignment_score']} / 100")

        combined = compat["combined"]
        st.divider()
        cf1, cf2, cf3 = st.columns(3)
        cf1.metric("Combined Income",  format_currency(combined["income"]))
        cf2.metric("Combined Savings", format_currency(combined["savings"]))
        cf3.metric("Survive Together", format_months(combined["survival_months"]))

        st.divider()
        t_sr = st.slider("Target Combined Savings Rate (%)", 10, 40, 20, key="tsr")
        rec  = recommended_partner_income(p1i, p1e, p1s, t_sr)
        ri1, ri2 = st.columns(2)
        ri1.metric("Min. Partner Income",   format_currency(rec["min_partner_income"]), "per month")
        ri2.metric("Emergency Fund Target", format_currency(rec["target_combined_savings"]))


# ════════════════════════════════════════════
# TAB 6 — LEADERBOARD
# ════════════════════════════════════════════
with tab6:
    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-section-title">Join the Leaderboard</p>', unsafe_allow_html=True)
    lb1, lb2 = st.columns([3, 1])
    with lb1:
        name_input = st.text_input("Your name or nickname", placeholder="e.g. Aashi")
    with lb2:
        if st.session_state.my_score:
            st.metric("Your Score", f"{st.session_state.my_score:.1f}")

    if st.button("🏆  Join Leaderboard", use_container_width=True):
        if not name_input:
            st.warning("Enter your name.")
        elif not st.session_state.my_score:
            st.warning("Calculate your score in 'My Score' first.")
        else:
            lv    = get_level(st.session_state.my_score)
            entry = {"name": name_input, "score": st.session_state.my_score,
                     "level": f"{lv['icon']} {lv['name']}"}
            lb    = st.session_state.leaderboard
            names = [e["name"] for e in lb]
            if name_input in names:
                st.session_state.leaderboard = [entry if e["name"] == name_input else e for e in lb]
            else:
                st.session_state.leaderboard.append(entry)
            st.session_state.my_name = name_input
            st.success("You're on the board! 🎉")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-section-title">Rankings</p>', unsafe_allow_html=True)
    sorted_lb = sorted(st.session_state.leaderboard, key=lambda x: -x["score"])
    icons     = ["🥇", "🥈", "🥉"]
    for i, e in enumerate(sorted_lb):
        rank   = icons[i] if i < 3 else f"#{i+1}"
        is_me  = e["name"] == st.session_state.my_name
        bg     = "#fffde7" if is_me else "#fafafa"
        border = "1px solid #fcd58a" if is_me else "1px solid #eef0f6"
        st.markdown(
            f"<div style='background:{bg};border:{border};border-radius:10px;"
            f"padding:11px 16px;margin-bottom:7px;display:flex;align-items:center;gap:12px;'>"
            f"<span style='font-size:18px;width:26px;'>{rank}</span>"
            f"<span style='flex:1;font-weight:{'700' if is_me else '500'};color:#1a2035;'>"
            f"{e['name']}{'  ⭐' if is_me else ''}</span>"
            f"<span style='color:#9aa5bc;font-size:12px;margin-right:12px;'>{e['level']}</span>"
            f"<span style='font-family:DM Mono,monospace;font-weight:700;font-size:16px;'>{e['score']:.1f}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.my_score:
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-section-title">Challenge a Friend</p>', unsafe_allow_html=True)
        msg = (f"I scored {st.session_state.my_score:.1f}/100 on Finverse 💰\n"
               "Know your Financial Safety Score?\n👉 [your Streamlit link here]")
        st.code(msg, language=None)
        st.caption("Copy → send on WhatsApp. That's your viral loop 🚀")
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════
st.markdown(
    "<div style='text-align:center;padding:20px 0 0;color:#b0b8cc;font-size:12px;'>"
    "Finverse v3.0 · Data stays in your session · Not financial advice"
    "</div>",
    unsafe_allow_html=True,
)
