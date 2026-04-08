# app.py  —  Finverse v4.0
# Professional dark fintech UI. Zero emojis.
# Run: streamlit run app.py

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
    page_icon="F",
    layout="centered",
)

# ══════════════════════════════════════════════
# DESIGN SYSTEM
# Dark navy fintech. Syne + DM Mono.
# Sharp emerald accent. No emojis anywhere.
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=Lato:wght@300;400;600&display=swap');

/* ── RESET & BASE ── */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif !important;
    color: #e2e8f0;
}

#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: #080d19;
}

.block-container {
    max-width: 820px !important;
    padding: 2.5rem 2rem 5rem !important;
}

/* ── TYPOGRAPHY ── */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.fv-wordmark {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.3px;
}
.fv-wordmark span {
    color: #10b981;
}
.fv-tagline {
    font-size: 13px;
    color: #475569;
    font-weight: 400;
    margin-top: 2px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── CARDS ── */
.fv-card {
    background: #0e1525;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 16px;
}
.fv-card-inset {
    background: #080d19;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 10px;
}

/* ── SECTION LABEL ── */
.fv-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #334155;
    margin: 0 0 16px 0;
    font-family: 'Lato', sans-serif;
}

/* ── DIVIDER ── */
.fv-divider {
    border: none;
    border-top: 1px solid #1e293b;
    margin: 18px 0;
}

/* ── SCORE DISPLAY ── */
.fv-score-number {
    font-family: 'DM Mono', monospace;
    font-size: 64px;
    font-weight: 500;
    line-height: 1;
    letter-spacing: -2px;
    color: #f8fafc;
}
.fv-score-denom {
    font-family: 'DM Mono', monospace;
    font-size: 20px;
    color: #334155;
    font-weight: 400;
}
.fv-score-label {
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-top: 6px;
}

/* ── LEVEL BADGE ── */
.fv-level-tag {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 4px;
    margin-bottom: 6px;
}
.level-platinum { background: #1e3a5f; color: #93c5fd; border: 1px solid #2563eb; }
.level-gold     { background: #3d2e00; color: #fcd34d; border: 1px solid #d97706; }
.level-silver   { background: #1e293b; color: #94a3b8; border: 1px solid #475569; }
.level-bronze   { background: #3d1a00; color: #fb923c; border: 1px solid #c2410c; }
.level-starter  { background: #0f2010; color: #6ee7b7; border: 1px solid #059669; }

/* ── RISK TAG ── */
.fv-risk {
    display: inline-block;
    font-family: 'Lato', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 3px;
}
.risk-safe     { background: #052e16; color: #10b981; border: 1px solid #065f46; }
.risk-moderate { background: #2d1b00; color: #f59e0b; border: 1px solid #92400e; }
.risk-risky    { background: #2d0a0a; color: #ef4444; border: 1px solid #991b1b; }

/* ── STAT ROW ── */
.fv-stat-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.fv-stat {
    flex: 1;
    min-width: 120px;
    background: #080d19;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 16px 18px;
}
.fv-stat-val {
    font-family: 'DM Mono', monospace;
    font-size: 24px;
    font-weight: 500;
    color: #f8fafc;
    letter-spacing: -0.5px;
    line-height: 1.1;
}
.fv-stat-key {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 5px;
    font-weight: 600;
}
.fv-stat-note {
    font-size: 11px;
    color: #334155;
    margin-top: 3px;
    line-height: 1.4;
}

/* ── PROGRESS BAR ── */
.fv-bar-track {
    background: #1e293b;
    border-radius: 2px;
    height: 3px;
    margin: 8px 0 14px 0;
}
.fv-bar-fill {
    height: 3px;
    border-radius: 2px;
}

/* ── SUGGESTION CARD ── */
.fv-suggestion {
    background: #0e1525;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 18px 20px;
    margin-bottom: 10px;
    position: relative;
}
.fv-sug-high   { border-left: 3px solid #ef4444; }
.fv-sug-medium { border-left: 3px solid #f59e0b; }
.fv-sug-low    { border-left: 3px solid #10b981; }
.fv-sug-title  {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 6px 0;
}
.fv-sug-detail {
    font-size: 13px;
    color: #64748b;
    margin: 0;
    line-height: 1.65;
}
.fv-impact-tag {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 3px;
    margin-left: 10px;
    vertical-align: middle;
}
.imp-high   { background: #2d0a0a; color: #ef4444; }
.imp-medium { background: #2d1b00; color: #f59e0b; }
.imp-low    { background: #052e16; color: #10b981; }

/* ── COMPARE ROW ── */
.fv-cmp-row   { display:flex; align-items:center; gap:12px; padding:8px 0; border-bottom:1px solid #1e293b; }
.fv-cmp-label { font-size:12px; color:#475569; width:140px; flex-shrink:0; letter-spacing:0.05em; text-transform:uppercase; font-weight:600; }
.fv-cmp-old   { font-family:'DM Mono',monospace; font-size:14px; color:#334155; width:80px; }
.fv-cmp-arrow { color:#1e293b; font-size:12px; }
.fv-cmp-up    { font-family:'DM Mono',monospace; font-size:14px; color:#10b981; font-weight:500; }
.fv-cmp-down  { font-family:'DM Mono',monospace; font-size:14px; color:#ef4444; font-weight:500; }
.fv-cmp-same  { font-family:'DM Mono',monospace; font-size:14px; color:#475569; font-weight:500; }

/* ── BADGE PILL ── */
.fv-badge {
    display: inline-block;
    background: #0e1525;
    border: 1px solid #1e293b;
    border-radius: 4px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 600;
    color: #94a3b8;
    margin: 3px;
    letter-spacing: 0.04em;
}

/* ── LEADERBOARD ROW ── */
.fv-lb-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 6px;
    border: 1px solid #1e293b;
}
.fv-lb-rank  { font-family:'DM Mono',monospace; font-size:13px; color:#334155; width:26px; }
.fv-lb-name  { flex:1; font-size:14px; color:#e2e8f0; font-weight:400; }
.fv-lb-level { font-size:11px; color:#475569; margin-right:12px; letter-spacing:0.06em; text-transform:uppercase; }
.fv-lb-score { font-family:'DM Mono',monospace; font-size:18px; color:#10b981; font-weight:500; }

/* ── QUOTE BLOCK ── */
.fv-quote {
    border-left: 3px solid #10b981;
    padding: 14px 20px;
    background: #080d19;
    border-radius: 0 8px 8px 0;
    margin-top: 8px;
}
.fv-quote-text {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: #f1f5f9;
    margin: 0 0 8px 0;
}
.fv-quote-sub {
    font-size: 13px;
    color: #475569;
    margin: 0;
    line-height: 1.65;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0e1525 !important;
    border-bottom: 1px solid #1e293b !important;
    gap: 0 !important;
    padding: 0 !important;
    border-radius: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 12px 20px !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-family: 'Lato', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #10b981 !important;
    border-bottom: 2px solid #10b981 !important;
}

/* ── INPUTS ── */
.stNumberInput input, .stTextInput input {
    background: #080d19 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 2px rgba(16,185,129,0.1) !important;
}
.stSelectbox > div > div {
    background: #080d19 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
}
label, .stNumberInput label, .stTextInput label, .stSelectbox label {
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #475569 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-family: 'Lato', sans-serif !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: #10b981 !important;
    color: #030712 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 12px 24px !important;
    width: 100% !important;
    font-family: 'Lato', sans-serif !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #059669 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(16,185,129,0.25) !important;
}

/* ── SLIDER ── */
.stSlider > div > div > div > div {
    background: #10b981 !important;
}
.stSlider > div > div > div {
    background: #1e293b !important;
}

/* ── METRIC ── */
[data-testid="metric-container"] {
    background: #080d19;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 14px 16px;
}
[data-testid="metric-container"] label {
    font-size: 11px !important;
    color: #475569 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 22px !important;
    color: #f1f5f9 !important;
}

/* ── ALERTS ── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 8px !important;
    font-size: 13px !important;
    font-family: 'Lato', sans-serif !important;
}

/* ── CAPTION / SMALL TEXT ── */
.stCaption, small, .caption {
    color: #334155 !important;
    font-size: 12px !important;
}

/* ── CODE BLOCK ── */
.stCodeBlock {
    background: #080d19 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
    color: #94a3b8 !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def score_svg(score, size=140):
    """SVG ring — no external libraries."""
    r     = 46
    circ  = 2 * 3.14159 * r
    dash  = round((score / 100) * circ, 1)
    gap   = round(circ - dash, 1)
    color = "#10b981" if score >= 65 else ("#f59e0b" if score >= 35 else "#ef4444")
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;">
      <svg width="{size}" height="{size}" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="{r}" fill="none" stroke="#1e293b" stroke-width="7"/>
        <circle cx="50" cy="50" r="{r}" fill="none" stroke="{color}" stroke-width="7"
                stroke-dasharray="{dash} {gap}"
                stroke-dashoffset="{circ * 0.25}"
                stroke-linecap="round"/>
        <text x="50" y="45" text-anchor="middle"
              font-family="DM Mono, monospace" font-size="22" font-weight="500"
              fill="#f8fafc">{score:.0f}</text>
        <text x="50" y="62" text-anchor="middle"
              font-family="Lato, sans-serif" font-size="9" fill="#334155"
              letter-spacing="1">SCORE</text>
      </svg>
    </div>"""


def bar(pct, color="#10b981"):
    pct = min(100, max(0, pct))
    return (f'<div class="fv-bar-track">'
            f'<div class="fv-bar-fill" style="width:{pct}%;background:{color};"></div>'
            f'</div>')


def risk_tag(risk):
    cfg = {
        "SAFE":     ("risk-safe",     "Safe"),
        "MODERATE": ("risk-moderate", "Moderate Risk"),
        "RISKY":    ("risk-risky",    "High Risk"),
    }
    cls, label = cfg[risk]
    return f'<span class="fv-risk {cls}">{label}</span>'


def level_tag(name):
    cls = {
        "Platinum": "level-platinum",
        "Gold":     "level-gold",
        "Silver":   "level-silver",
        "Bronze":   "level-bronze",
        "Starter":  "level-starter",
    }.get(name, "level-starter")
    return f'<span class="fv-level-tag {cls}">{name}</span>'


def cmp_row(label, before, after, fmt=None, higher_is_better=True):
    b = fmt(before) if fmt else f"{before:.1f}"
    a = fmt(after)  if fmt else f"{after:.1f}"
    d = after - before
    if   abs(d) < 0.05:                    cls = "fv-cmp-same"
    elif (d > 0) == higher_is_better:      cls = "fv-cmp-up"
    else:                                   cls = "fv-cmp-down"
    return (f'<div class="fv-cmp-row">'
            f'<span class="fv-cmp-label">{label}</span>'
            f'<span class="fv-cmp-old">{b}</span>'
            f'<span class="fv-cmp-arrow">&#8594;</span>'
            f'<span class="{cls}">{a}</span>'
            f'</div>')


# ══════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════
_def = {
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
        {"name": "Priya S.",  "score": 82.3, "level": "Gold"},
        {"name": "Rahul M.",  "score": 74.1, "level": "Gold"},
        {"name": "Aisha K.",  "score": 68.5, "level": "Gold"},
        {"name": "Vikram N.", "score": 61.2, "level": "Silver"},
        {"name": "Sneha R.",  "score": 55.8, "level": "Silver"},
        {"name": "Arjun T.",  "score": 44.3, "level": "Silver"},
        {"name": "Meera P.",  "score": 38.7, "level": "Bronze"},
    ],
}
for k, v in _def.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════
st.markdown("""
<div style="padding: 4px 0 28px 0; border-bottom: 1px solid #1e293b; margin-bottom: 28px;">
  <div class="fv-wordmark">FIN<span>VERSE</span></div>
  <div class="fv-tagline">Financial Safety Platform</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        "<div style='font-family:Syne,sans-serif;font-size:16px;font-weight:700;"
        "color:#f1f5f9;margin-bottom:18px;'>Profile</div>",
        unsafe_allow_html=True,
    )
    persona_name = st.selectbox("Profile Type", list(PERSONAS.keys()), index=1, label_visibility="collapsed")
    persona      = PERSONAS[persona_name]

    st.markdown(
        f"<div style='background:#080d19;border:1px solid #1e293b;border-radius:8px;"
        f"padding:14px 16px;font-size:13px;color:#64748b;line-height:2;'>"
        f"<span style='color:#334155;font-weight:700;text-transform:uppercase;"
        f"font-size:10px;letter-spacing:0.1em;'>Savings Target</span><br>"
        f"<span style='color:#f1f5f9;font-family:DM Mono,monospace;font-size:16px;'>"
        f"{persona['savings_rate_target']}%</span><br><br>"
        f"<span style='color:#334155;font-weight:700;text-transform:uppercase;"
        f"font-size:10px;letter-spacing:0.1em;'>Emergency Fund Goal</span><br>"
        f"<span style='color:#f1f5f9;font-family:DM Mono,monospace;font-size:16px;'>"
        f"{persona['survival_target']} months</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;"
        "text-transform:uppercase;color:#334155;margin:20px 0 10px 0;'>Guidance</div>",
        unsafe_allow_html=True,
    )
    for tip in persona["tips"]:
        st.markdown(
            f"<p style='font-size:12px;color:#475569;margin:0 0 8px 0;line-height:1.5;'>{tip}</p>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border-color:#1e293b;margin:20px 0;'>", unsafe_allow_html=True)
    total_xp = get_total_xp(st.session_state.challenges_done)
    st.markdown(
        f"<div style='background:#080d19;border:1px solid #1e293b;border-radius:8px;"
        f"padding:14px 16px;text-align:center;'>"
        f"<div style='font-family:DM Mono,monospace;font-size:28px;font-weight:500;"
        f"color:#10b981;'>{total_xp}</div>"
        f"<div style='font-size:10px;color:#334155;text-transform:uppercase;"
        f"letter-spacing:0.1em;margin-top:4px;'>XP Earned</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size:11px;color:#1e293b;margin-top:20px;text-align:center;'>"
        "Finverse v4.0 · Not financial advice</p>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Score", "What-If", "Suggestions", "Tracker", "Partner", "Leaderboard"
])


# ════════════════════════════════════════════
# TAB 1 — MY SCORE
# ════════════════════════════════════════════
with tab1:
    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-label">Monthly Snapshot</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        income  = st.number_input(persona["income_label"], min_value=0.0, value=50000.0, step=1000.0, key="t1_inc")
        savings = st.number_input("Total Savings (INR)", min_value=0.0, value=120000.0, step=5000.0, key="t1_sav")
    with c2:
        expenses = st.number_input("Monthly Expenses (INR)", min_value=0.0, value=35000.0, step=1000.0, key="t1_exp")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("CALCULATE SAFETY SCORE", key="t1_calc"):
        if income <= 0:
            st.error("Income must be greater than zero.")
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

        # ── SCORE CARD ──────────────────────
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        score_col, info_col = st.columns([1, 2])
        with score_col:
            st.markdown(score_svg(score), unsafe_allow_html=True)
        with info_col:
            st.markdown(
                f"<div style='padding: 8px 0;'>"
                f"{level_tag(level['name'])}"
                f"<div style='font-family:Syne,sans-serif;font-size:26px;font-weight:700;"
                f"color:#f8fafc;margin:10px 0 4px 0;line-height:1.15;'>"
                f"{level['message']}</div>"
                f"<div style='margin-bottom:10px;'>{risk_tag(risk)}</div>"
                f"<div style='font-size:12px;color:#475569;'>{get_risk_advice(risk)}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if next_l:
                st.markdown(
                    f"<div style='font-size:11px;color:#334155;margin-top:8px;'>"
                    f"{next_l['points_needed']} pts to reach {next_l['name']}"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)

        # ── METRICS ─────────────────────────
        sr   = result["savings_rate"]
        sm   = result["survival_months"]
        er   = result["expense_ratio"]
        sr_c = "#10b981" if sr >= 20 else ("#f59e0b" if sr >= 10 else "#ef4444")
        sm_c = "#10b981" if sm >= 6  else ("#f59e0b" if sm >= 3  else "#ef4444")
        er_c = "#10b981" if er <= 60 else ("#f59e0b" if er <= 80 else "#ef4444")

        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-label">Key Metrics</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="fv-stat-row">
            <div class="fv-stat">
                <div class="fv-stat-val" style="color:{sr_c};">{sr:.1f}%</div>
                <div class="fv-stat-key">Savings Rate</div>
                <div class="fv-stat-note">{get_savings_rate_message(sr)}</div>
            </div>
            <div class="fv-stat">
                <div class="fv-stat-val" style="color:{sm_c};">{format_months(sm)}</div>
                <div class="fv-stat-key">Survival Time</div>
                <div class="fv-stat-note">{get_survival_message(sm)}</div>
            </div>
            <div class="fv-stat">
                <div class="fv-stat-val" style="color:{er_c};">{er:.1f}%</div>
                <div class="fv-stat-key">Expense Ratio</div>
                <div class="fv-stat-note">of income on expenses</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(bar(min(100, int(sr / 30 * 100)), sr_c), unsafe_allow_html=True)
        st.markdown(bar(min(100, int(sm / 12 * 100)), sm_c), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── MONTHLY PICTURE ─────────────────
        surplus = income - expenses
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-label">Monthly Picture</p>', unsafe_allow_html=True)
        ms1, ms2, ms3 = st.columns(3)
        ms1.metric("Income",    format_currency(income))
        ms2.metric("Expenses",  format_currency(expenses))
        ms3.metric("Surplus" if surplus >= 0 else "Deficit",
                   format_currency(abs(surplus)),
                   delta_color="normal" if surplus >= 0 else "inverse")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── BADGES ──────────────────────────
        if badges:
            st.markdown('<div class="fv-card">', unsafe_allow_html=True)
            st.markdown('<p class="fv-label">Achievements</p>', unsafe_allow_html=True)
            st.markdown(
                "".join(f'<span class="fv-badge">{b["name"].split(" ", 1)[-1]}</span>' for b in badges),
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # ── CHALLENGES ──────────────────────
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-label">Active Challenges</p>', unsafe_allow_html=True)
        for ch in get_challenges():
            done = ch["id"] in st.session_state.challenges_done
            ca, cb = st.columns([5, 1])
            with ca:
                name_style = "color:#334155;text-decoration:line-through;" if done else "color:#e2e8f0;"
                st.markdown(
                    f"<div style='{name_style}font-size:14px;font-weight:600;"
                    f"margin-bottom:2px;'>{ch['name']}</div>"
                    f"<div style='font-size:12px;color:#334155;'>"
                    f"{ch['desc']} &nbsp;+{ch['reward_xp']} XP</div>",
                    unsafe_allow_html=True,
                )
            with cb:
                if not done and st.button("Mark Done", key=f"ch_{ch['id']}"):
                    st.session_state.challenges_done.add(ch["id"])
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="fv-card" style="text-align:center;padding:60px 28px;">
            <div style="font-family:DM Mono,monospace;font-size:48px;color:#1e293b;
                        font-weight:500;letter-spacing:-2px;">--</div>
            <div style="font-family:Syne,sans-serif;font-size:18px;font-weight:600;
                        color:#334155;margin-top:12px;">
                Enter your numbers and calculate
            </div>
            <div style="font-size:13px;color:#1e293b;margin-top:6px;">
                Your financial safety score appears here
            </div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2 — WHAT-IF SIMULATOR
# ════════════════════════════════════════════
with tab2:
    if not st.session_state.last_result:
        st.markdown(
            "<div class='fv-card' style='color:#334155;text-align:center;padding:40px;'>"
            "Calculate your score in the Score tab first."
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        base  = st.session_state.last_result
        b_inc = st.session_state.last_income
        b_exp = st.session_state.last_expenses
        b_sav = st.session_state.last_savings

        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-label">Adjust Scenario</p>', unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:13px;color:#475569;margin:0 0 18px 0;'>"
            "Slide to see the instant impact on your score. No recalculation needed.</p>",
            unsafe_allow_html=True,
        )
        inc_d = st.slider("Income change per month (INR)",   -20000, 50000,     0, 1000)
        exp_d = st.slider("Expense change per month (INR)",  -20000, 20000,     0,  500)
        sav_d = st.slider("Additional savings added (INR)",       0, 500000,    0, 5000)
        st.markdown('</div>', unsafe_allow_html=True)

        new_r   = calculate_whatif(b_inc, b_exp, b_sav,
                                    {"income_delta": inc_d,
                                     "expenses_delta": exp_d,
                                     "savings_delta": sav_d})
        n_score = new_r["composite_score"]
        o_score = base["composite_score"]
        diff    = n_score - o_score
        d_color = "#10b981" if diff >= 0 else "#ef4444"
        arrow   = "+" if diff >= 0 else ""

        # Ring comparison
        ra, rb = st.columns(2)
        with ra:
            st.markdown(
                f'<div class="fv-card" style="text-align:center;">'
                f'<p class="fv-label" style="text-align:center;">Current</p>'
                f'{score_svg(o_score, 120)}'
                f'<div style="margin-top:10px;">{risk_tag(base["risk_level"])}</div>'
                f'</div>', unsafe_allow_html=True)
        with rb:
            st.markdown(
                f'<div class="fv-card" style="text-align:center;">'
                f'<p class="fv-label" style="text-align:center;">New Scenario</p>'
                f'{score_svg(n_score, 120)}'
                f'<div style="margin-top:10px;">{risk_tag(new_r["risk_level"])}</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:16px;'
                f'font-weight:500;color:{d_color};margin-top:8px;">'
                f'{arrow}{diff:.1f} pts</div>'
                f'</div>', unsafe_allow_html=True)

        # Comparison table
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-label">Metric Breakdown</p>', unsafe_allow_html=True)
        st.markdown(
            cmp_row("Savings Rate",    base["savings_rate"],    new_r["savings_rate"],    lambda v: f"{v:.1f}%") +
            cmp_row("Survival Time",   base["survival_months"], new_r["survival_months"], lambda v: format_months(v)) +
            cmp_row("Expense Ratio",   base["expense_ratio"],   new_r["expense_ratio"],   lambda v: f"{v:.1f}%", higher_is_better=False) +
            cmp_row("Monthly Surplus", b_inc - b_exp, (b_inc + inc_d) - (b_exp + exp_d), lambda v: format_currency(v)),
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if   diff > 10: st.success(f"+{diff:.1f} points. Moves you to {new_r['risk_level']}.")
        elif diff > 0:  st.info(f"Small improvement of {diff:.1f} points.")
        elif diff < -10:st.error(f"{diff:.1f} points. Drops to {new_r['risk_level']}.")
        elif diff < 0:  st.warning(f"Small decline of {abs(diff):.1f} points.")
        else:           st.info("No meaningful change in this scenario.")


# ════════════════════════════════════════════
# TAB 3 — SUGGESTIONS
# ════════════════════════════════════════════
with tab3:
    if not st.session_state.last_result:
        st.markdown(
            "<div class='fv-card' style='color:#334155;text-align:center;padding:40px;'>"
            "Calculate your score in the Score tab first."
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        res   = st.session_state.last_result
        b_inc = st.session_state.last_income
        b_exp = st.session_state.last_expenses
        b_sav = st.session_state.last_savings
        suggs = generate_suggestions(b_inc, b_exp, b_sav, res)

        st.markdown(
            "<div style='margin-bottom:20px;'>"
            "<div style='font-family:Syne,sans-serif;font-size:20px;font-weight:700;"
            "color:#f1f5f9;'>Action Plan</div>"
            "<div style='font-size:13px;color:#475569;margin-top:4px;'>"
            "Ranked by financial impact. Work from top to bottom.</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        order = {"High": 0, "Medium": 1, "Low": 2}
        for s in sorted(suggs, key=lambda x: order.get(x["impact"], 3)):
            cls  = {"High":"fv-sug-high","Medium":"fv-sug-medium","Low":"fv-sug-low"}[s["impact"]]
            icls = {"High":"imp-high","Medium":"imp-medium","Low":"imp-low"}[s["impact"]]
            st.markdown(
                f'<div class="fv-suggestion {cls}">'
                f'<p class="fv-sug-title">{s["title"]}'
                f'<span class="fv-impact-tag {icls}">{s["impact"]}</span></p>'
                f'<p class="fv-sug-detail">{s["detail"]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("""
        <div class="fv-quote" style="margin-top:24px;">
            <p class="fv-quote-text">Save first. Spend what remains.</p>
            <p class="fv-quote-sub">
                Most people spend first and save whatever is left — which is usually nothing.
                Reverse the order: on salary day, immediately move your savings target to a
                separate account. Your spending is now naturally constrained.
                This single habit outperforms every other financial strategy at the same income level.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 4 — DAILY TRACKER
# ════════════════════════════════════════════
with tab4:
    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-label">Daily Tracker</p>', unsafe_allow_html=True)
    sb1, sb2 = st.columns(2)
    with sb1:
        st.metric("Tracking Streak", f"{st.session_state.streak} days")
    with sb2:
        st.session_state.daily_budget = st.number_input(
            "Daily Budget (INR)", min_value=0.0, value=st.session_state.daily_budget, step=100.0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-label">Add Expense</p>', unsafe_allow_html=True)
    ea, eb, ec = st.columns([2, 2, 3])
    with ea:
        cat = st.selectbox("Category", [
            "Food", "Transport", "Shopping", "Bills",
            "Entertainment", "Health", "Education", "Other",
        ])
    with eb:
        amt = st.number_input("Amount (INR)", min_value=0.0, value=0.0, step=10.0)
    with ec:
        note = st.text_input("Note", placeholder="e.g. Lunch at office")

    if st.button("ADD EXPENSE", key="add_exp"):
        if amt > 0:
            st.session_state.daily_expenses.append({
                "category": cat, "amount": amt,
                "note": note or "-", "time": datetime.now().strftime("%H:%M"),
            })
            st.rerun()
        else:
            st.warning("Enter an amount greater than zero.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.daily_expenses:
        total  = sum(e["amount"] for e in st.session_state.daily_expenses)
        budget = st.session_state.daily_budget
        left   = budget - total
        pct    = min(100, int(total / budget * 100)) if budget > 0 else 100
        b_clr  = "#10b981" if pct < 70 else ("#f59e0b" if pct < 90 else "#ef4444")

        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-label">Today</p>', unsafe_allow_html=True)
        ds1, ds2, ds3 = st.columns(3)
        ds1.metric("Spent",  format_currency(total))
        ds2.metric("Budget", format_currency(budget))
        ds3.metric("Remaining" if left >= 0 else "Over Budget", format_currency(abs(left)),
                   delta_color="normal" if left >= 0 else "inverse")
        st.markdown(bar(pct, b_clr), unsafe_allow_html=True)

        if pct >= 90: st.error("Approaching daily budget limit.")
        elif pct >= 70: st.warning("Budget usage is high.")
        else: st.success("On track.")

        st.markdown('<hr class="fv-divider">', unsafe_allow_html=True)
        for exp in reversed(st.session_state.daily_expenses):
            el, er = st.columns([4, 1])
            el.markdown(
                f"<span style='color:#94a3b8;font-size:14px;'>{exp['category']}</span>"
                f"<span style='color:#334155;font-size:13px;margin-left:10px;'>{exp['note']}</span>"
                f"<span style='color:#1e293b;font-size:11px;margin-left:8px;'>{exp['time']}</span>",
                unsafe_allow_html=True,
            )
            er.markdown(
                f"<span style='font-family:DM Mono,monospace;font-size:14px;"
                f"color:#f1f5f9;'>{format_currency(exp['amount'])}</span>",
                unsafe_allow_html=True,
            )

        st.markdown('<hr class="fv-divider">', unsafe_allow_html=True)
        if st.button("END DAY — SAVE STREAK", use_container_width=True):
            st.session_state.daily_expenses = []
            st.session_state.streak += 1
            st.success(f"Streak: {st.session_state.streak} days.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='fv-card' style='color:#334155;text-align:center;padding:36px;'>"
            "No expenses logged today. Add one above to begin tracking."
            "</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# TAB 5 — PARTNER TEST
# ════════════════════════════════════════════
with tab5:
    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-label">Financial Compatibility</p>', unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:13px;color:#475569;margin:0;'>"
        "Compare two financial profiles to see combined health, alignment, "
        "and the minimum partner income for a stable shared future.</p>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        st.markdown("<p style='font-size:11px;font-weight:700;letter-spacing:0.1em;color:#334155;text-transform:uppercase;'>You</p>", unsafe_allow_html=True)
        p1i = st.number_input("Income",   min_value=0.0, value=50000.0, step=1000.0, key="p1i")
        p1e = st.number_input("Expenses", min_value=0.0, value=35000.0, step=1000.0, key="p1e")
        p1s = st.number_input("Savings",  min_value=0.0, value=120000.0,step=5000.0, key="p1s")
    with pc2:
        st.markdown("<p style='font-size:11px;font-weight:700;letter-spacing:0.1em;color:#334155;text-transform:uppercase;'>Partner</p>", unsafe_allow_html=True)
        p2i = st.number_input("Income",   min_value=0.0, value=45000.0, step=1000.0, key="p2i")
        p2e = st.number_input("Expenses", min_value=0.0, value=30000.0, step=1000.0, key="p2e")
        p2s = st.number_input("Savings",  min_value=0.0, value=80000.0, step=5000.0, key="p2s")

    if st.button("CALCULATE COMPATIBILITY", use_container_width=True):
        r1     = analyse_finances(p1i, p1e, p1s)
        r2     = analyse_finances(p2i, p2e, p2s)
        compat = analyse_compatibility(r1, r2)
        cs     = compat["compatibility_score"]

        if   cs >= 75: lbl, clr = "Excellent Match",    "#10b981"
        elif cs >= 55: lbl, clr = "Good Match",         "#f59e0b"
        elif cs >= 35: lbl, clr = "Needs Alignment",    "#f59e0b"
        else:          lbl, clr = "Significant Gap",    "#ef4444"

        st.markdown(
            f"<div class='fv-card' style='text-align:center;padding:32px;'>"
            f"<div style='font-family:DM Mono,monospace;font-size:56px;font-weight:500;"
            f"color:{clr};letter-spacing:-2px;'>{cs:.0f}</div>"
            f"<div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;"
            f"color:#f1f5f9;margin-top:4px;'>{lbl}</div>"
            f"<div style='font-size:12px;color:#475569;margin-top:4px;'>out of 100</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        is1, is2, is3 = st.columns(3)
        is1.metric("Your Score",      f"{r1['composite_score']} / 100")
        is2.metric("Partner Score",   f"{r2['composite_score']} / 100")
        is3.metric("Alignment",       f"{compat['alignment_score']} / 100")

        combined = compat["combined"]
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-label">Combined Picture</p>', unsafe_allow_html=True)
        cf1, cf2, cf3 = st.columns(3)
        cf1.metric("Combined Income",  format_currency(combined["income"]))
        cf2.metric("Combined Savings", format_currency(combined["savings"]))
        cf3.metric("Survival Time",    format_months(combined["survival_months"]))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-label">Ideal Partner Income</p>', unsafe_allow_html=True)
        t_sr = st.slider("Target Combined Savings Rate (%)", 10, 40, 20, key="tsr")
        rec  = recommended_partner_income(p1i, p1e, p1s, t_sr)
        ri1, ri2 = st.columns(2)
        ri1.metric("Minimum Partner Income",    format_currency(rec["min_partner_income"]), "per month")
        ri2.metric("Emergency Fund Target",     format_currency(rec["target_combined_savings"]))
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 6 — LEADERBOARD
# ════════════════════════════════════════════
with tab6:
    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-label">Join the Leaderboard</p>', unsafe_allow_html=True)
    lb1, lb2 = st.columns([3, 1])
    with lb1:
        name_input = st.text_input("Name or nickname", placeholder="Your name")
    with lb2:
        if st.session_state.my_score:
            st.metric("Your Score", f"{st.session_state.my_score:.1f}")

    if st.button("JOIN LEADERBOARD", use_container_width=True):
        if not name_input:
            st.warning("Enter a name.")
        elif not st.session_state.my_score:
            st.warning("Calculate your score in the Score tab first.")
        else:
            lv    = get_level(st.session_state.my_score)
            entry = {"name": name_input, "score": st.session_state.my_score, "level": lv["name"]}
            lb    = st.session_state.leaderboard
            if any(e["name"] == name_input for e in lb):
                st.session_state.leaderboard = [entry if e["name"] == name_input else e for e in lb]
            else:
                st.session_state.leaderboard.append(entry)
            st.session_state.my_name = name_input
            st.success("Added to leaderboard.")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown('<p class="fv-label">Rankings</p>', unsafe_allow_html=True)
    sorted_lb = sorted(st.session_state.leaderboard, key=lambda x: -x["score"])
    for i, e in enumerate(sorted_lb):
        rank   = f"0{i+1}" if i + 1 < 10 else str(i + 1)
        is_me  = e["name"] == st.session_state.my_name
        bg     = "#0e1525" if not is_me else "#0a1f14"
        border = "1px solid #1e293b" if not is_me else "1px solid #065f46"
        st.markdown(
            f"<div class='fv-lb-row' style='background:{bg};border:{border};'>"
            f"<span class='fv-lb-rank'>{rank}</span>"
            f"<span class='fv-lb-name' style='{'color:#10b981;font-weight:600;' if is_me else ''}'>"
            f"{e['name']}</span>"
            f"<span class='fv-lb-level'>{e['level']}</span>"
            f"<span class='fv-lb-score'>{e['score']:.1f}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.my_score:
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-label">Share</p>', unsafe_allow_html=True)
        msg = (f"My Finverse Financial Safety Score: {st.session_state.my_score:.1f}/100\n"
               "Find out yours — [your link here]")
        st.code(msg, language=None)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════
st.markdown(
    "<div style='text-align:center;padding:32px 0 0;border-top:1px solid #1e293b;margin-top:16px;'>"
    "<span style='font-family:Syne,sans-serif;font-size:14px;font-weight:700;color:#1e293b;'>FINVERSE</span>"
    "<span style='font-size:12px;color:#1e293b;margin-left:16px;'>Financial Safety Platform</span>"
    "<span style='font-size:12px;color:#1e293b;margin-left:16px;'>v4.0</span>"
    "<span style='font-size:12px;color:#1e293b;margin-left:16px;'>Not financial advice</span>"
    "</div>",
    unsafe_allow_html=True,
)
