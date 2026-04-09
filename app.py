# app.py  —  Finverse v5.0
# All features. SQLite persistence. Professional UI.
# Run: streamlit run app.py

import streamlit as st
from datetime import datetime, date

from logic        import (analyse_finances, calculate_savings_rules,
                           analyse_compatibility, recommended_partner_income)
from config       import PERSONAS
from gamification import get_level, get_next_level, get_badges, get_challenges, get_total_xp
from suggestions  import generate_suggestions, calculate_whatif
from utils        import (format_currency, format_percent, format_months,
                           get_savings_rate_message, get_survival_message, get_risk_advice)
from database     import (init_db, save_score, get_score_history, upsert_leaderboard,
                           get_leaderboard, save_expense, get_today_expenses, delete_expense,
                           get_monthly_expenses, get_spending_trend, save_challenge,
                           get_completed_challenges, get_user_settings, save_user_settings,
                           end_day_update_streak)

# ── INIT DB ─────────────────────────────────
init_db()

# ══════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="Finverse",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
# DESIGN SYSTEM — dark fintech, app-like
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@500;600;700;800&family=DM+Mono:wght@400;500&family=Mulish:wght@300;400;600;700&display=swap');

/* ── BASE ── */
html, body, [class*="css"] {
    font-family: 'Mulish', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: #050a14;
}
.block-container {
    max-width: 960px !important;
    padding: 0 2rem 4rem 2rem !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #080f1e !important;
    border-right: 1px solid #0d1a2e !important;
}
[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

/* ── CARDS ── */
.card {
    background: #080f1e;
    border: 1px solid #0d1a2e;
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 14px;
}
.card-dark {
    background: #050a14;
    border: 1px solid #0d1a2e;
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 14px;
}
.card-accent {
    background: #041810;
    border: 1px solid #064e35;
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 14px;
}

/* ── LABEL ── */
.lbl {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #1e3a5f;
    margin: 0 0 14px 0;
    display: block;
}

/* ── STAT GRID ── */
.stat-grid { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 4px; }
.stat-box {
    flex: 1; min-width: 130px;
    background: #050a14;
    border: 1px solid #0d1a2e;
    border-radius: 8px;
    padding: 14px 16px;
}
.stat-val {
    font-family: 'DM Mono', monospace;
    font-size: 22px; font-weight: 500;
    color: #e2e8f0; line-height: 1.1;
    letter-spacing: -0.3px;
}
.stat-key {
    font-size: 10px; color: #1e3a5f;
    text-transform: uppercase; letter-spacing: 0.12em;
    margin-top: 5px; font-weight: 700;
}
.stat-note { font-size: 11px; color: #1e3a5f; margin-top: 3px; line-height: 1.4; }

/* ── SCORE RING ── */
.ring-wrap { display: flex; flex-direction: column; align-items: center; }

/* ── RISK TAGS ── */
.risk {
    display: inline-block; font-size: 10px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 3px;
    font-family: 'Mulish', sans-serif;
}
.r-safe     { background: #041810; color: #10b981; border: 1px solid #064e35; }
.r-moderate { background: #1c1000; color: #f59e0b; border: 1px solid #78350f; }
.r-risky    { background: #1a0505; color: #ef4444; border: 1px solid #7f1d1d; }

/* ── LEVEL TAG ── */
.lvl {
    display: inline-block; font-size: 10px; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 3px; margin-bottom: 8px;
    font-family: 'Mulish', sans-serif;
}
.l-platinum { background: #0c1f3d; color: #60a5fa; border: 1px solid #1d4ed8; }
.l-gold     { background: #1c1000; color: #fbbf24; border: 1px solid #d97706; }
.l-silver   { background: #0d1a2e; color: #94a3b8; border: 1px solid #334155; }
.l-bronze   { background: #1a0a00; color: #fb923c; border: 1px solid #9a3412; }
.l-starter  { background: #041810; color: #34d399; border: 1px solid #065f46; }

/* ── BAR ── */
.bar-track { background: #0d1a2e; border-radius: 2px; height: 3px; margin: 6px 0 12px 0; }
.bar-fill  { height: 3px; border-radius: 2px; }

/* ── SUGGESTION ── */
.sug {
    background: #080f1e; border: 1px solid #0d1a2e;
    border-radius: 8px; padding: 16px 18px; margin-bottom: 8px;
}
.sug-h { border-left: 3px solid #ef4444; }
.sug-m { border-left: 3px solid #f59e0b; }
.sug-l { border-left: 3px solid #10b981; }
.sug-title {
    font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700;
    color: #e2e8f0; margin: 0 0 5px 0;
}
.sug-body { font-size: 12px; color: #334155; margin: 0; line-height: 1.65; }
.imp {
    display: inline-block; font-size: 9px; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 2px 7px; border-radius: 2px; margin-left: 8px; vertical-align: middle;
}
.imp-h { background: #1a0505; color: #ef4444; }
.imp-m { background: #1c1000; color: #f59e0b; }
.imp-l { background: #041810; color: #10b981; }

/* ── COMPARE ROW ── */
.cmp { display:flex; align-items:center; gap:10px; padding:9px 0; border-bottom:1px solid #0d1a2e; }
.cmp-lbl { font-size:11px; color:#1e3a5f; width:140px; flex-shrink:0; text-transform:uppercase; letter-spacing:0.08em; font-weight:700; }
.cmp-old  { font-family:'DM Mono',monospace; font-size:13px; color:#1e3a5f; width:80px; }
.cmp-arr  { color:#0d1a2e; font-size:11px; }
.cmp-up   { font-family:'DM Mono',monospace; font-size:13px; color:#10b981; font-weight:500; }
.cmp-dn   { font-family:'DM Mono',monospace; font-size:13px; color:#ef4444; font-weight:500; }
.cmp-eq   { font-family:'DM Mono',monospace; font-size:13px; color:#334155; font-weight:500; }

/* ── EXPENSE ROW ── */
.exp-row {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-radius: 6px;
    background: #050a14; border: 1px solid #0d1a2e;
    margin-bottom: 6px;
}
.exp-cat  { font-size: 12px; color: #475569; width: 100px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.exp-note { flex: 1; font-size: 13px; color: #64748b; }
.exp-time { font-size: 11px; color: #1e3a5f; width: 46px; font-family: 'DM Mono', monospace; }
.exp-amt  { font-family: 'DM Mono', monospace; font-size: 14px; color: #e2e8f0; width: 80px; text-align: right; }

/* ── LB ROW ── */
.lb-row {
    display: flex; align-items: center; gap: 14px;
    padding: 12px 16px; border-radius: 8px; margin-bottom: 6px;
    border: 1px solid #0d1a2e; background: #080f1e;
}
.lb-rank  { font-family:'DM Mono',monospace; font-size:12px; color:#1e3a5f; width:28px; }
.lb-name  { flex:1; font-size:13px; color:#94a3b8; font-weight:400; }
.lb-lvl   { font-size:10px; color:#1e3a5f; margin-right:10px; text-transform:uppercase; letter-spacing:0.08em; }
.lb-score { font-family:'DM Mono',monospace; font-size:18px; color:#10b981; font-weight:500; }

/* ── BADGE ── */
.badge {
    display: inline-block; background: #080f1e;
    border: 1px solid #0d1a2e; border-radius: 4px;
    padding: 4px 10px; font-size: 11px; font-weight: 700;
    color: #475569; margin: 3px; letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── QUOTE ── */
.quote {
    border-left: 3px solid #10b981; padding: 14px 18px;
    background: #041810; border-radius: 0 8px 8px 0; margin-top: 16px;
}
.quote-h { font-family:'Syne',sans-serif; font-size:15px; font-weight:700; color:#e2e8f0; margin:0 0 6px 0; }
.quote-b { font-size:12px; color:#334155; margin:0; line-height:1.65; }

/* ── CHALLENGE ROW ── */
.ch-row {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 12px 14px; border-radius: 6px;
    background: #050a14; border: 1px solid #0d1a2e;
    margin-bottom: 6px;
}
.ch-done { opacity: 0.35; }
.ch-name { font-size: 13px; color: #94a3b8; font-weight: 600; margin: 0 0 2px 0; }
.ch-desc { font-size: 11px; color: #1e3a5f; margin: 0; }
.ch-xp   { font-family:'DM Mono',monospace; font-size:11px; color:#10b981; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #080f1e !important;
    border-bottom: 1px solid #0d1a2e !important;
    gap: 0 !important; padding: 0 !important; border-radius: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #1e3a5f !important;
    font-size: 11px !important; font-weight: 700 !important;
    padding: 14px 18px !important; border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    letter-spacing: 0.1em; text-transform: uppercase;
    font-family: 'Mulish', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: transparent !important; color: #10b981 !important;
    border-bottom: 2px solid #10b981 !important;
}
[data-testid="stTabPanel"] {
    background: transparent !important;
    padding-top: 20px !important;
}

/* ── INPUTS ── */
.stNumberInput input, .stTextInput input, .stSelectbox input {
    background: #050a14 !important;
    border: 1px solid #0d1a2e !important;
    border-radius: 7px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 15px !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 2px rgba(16,185,129,0.08) !important;
}
[data-baseweb="select"] > div {
    background: #050a14 !important;
    border: 1px solid #0d1a2e !important;
    border-radius: 7px !important;
}
[data-baseweb="select"] span { color: #e2e8f0 !important; }

label {
    font-size: 10px !important; font-weight: 700 !important;
    color: #1e3a5f !important; text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: #10b981 !important;
    color: #020c07 !important;
    border: none !important;
    border-radius: 7px !important;
    font-weight: 800 !important;
    font-size: 11px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 11px 20px !important;
    font-family: 'Mulish', sans-serif !important;
    transition: all 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #059669 !important;
    box-shadow: 0 0 18px rgba(16,185,129,0.2) !important;
    transform: translateY(-1px) !important;
}
/* Delete button - smaller, red tint */
.stButton.delete > button {
    background: #1a0505 !important;
    color: #ef4444 !important;
    border: 1px solid #7f1d1d !important;
    font-size: 10px !important;
    padding: 6px 10px !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #050a14 !important;
    border: 1px solid #0d1a2e !important;
    border-radius: 8px !important;
    padding: 14px 16px !important;
}
[data-testid="stMetricLabel"] {
    font-size: 10px !important; color: #1e3a5f !important;
    text-transform: uppercase !important; letter-spacing: 0.1em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 20px !important; color: #e2e8f0 !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] > div > div > div > div { background: #10b981 !important; }
[data-testid="stSlider"] > div > div > div { background: #0d1a2e !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] {
    background: #080f1e !important;
    border: 1px solid #0d1a2e !important;
    border-radius: 7px !important;
    font-size: 12px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; background: #050a14; }
::-webkit-scrollbar-thumb { background: #0d1a2e; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def ring(score, size=130):
    r    = 44
    c    = 2 * 3.14159 * r
    d    = round(score / 100 * c, 1)
    g    = round(c - d, 1)
    col  = "#10b981" if score >= 65 else ("#f59e0b" if score >= 35 else "#ef4444")
    return f"""
    <div class="ring-wrap">
      <svg width="{size}" height="{size}" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="{r}" fill="none" stroke="#0d1a2e" stroke-width="7"/>
        <circle cx="50" cy="50" r="{r}" fill="none" stroke="{col}" stroke-width="7"
                stroke-dasharray="{d} {g}"
                stroke-dashoffset="{c*0.25}"
                stroke-linecap="round"/>
        <text x="50" y="46" text-anchor="middle"
              font-family="DM Mono,monospace" font-size="20" font-weight="500"
              fill="#e2e8f0">{score:.0f}</text>
        <text x="50" y="61" text-anchor="middle"
              font-family="Mulish,sans-serif" font-size="9" fill="#1e3a5f"
              letter-spacing="1">SCORE</text>
      </svg>
    </div>"""


def bar(pct, color="#10b981"):
    pct = min(100, max(0, pct))
    return (f'<div class="bar-track">'
            f'<div class="bar-fill" style="width:{pct}%;background:{color};"></div>'
            f'</div>')


def risk_tag(risk):
    c = {"SAFE": "r-safe", "MODERATE": "r-moderate", "RISKY": "r-risky"}
    l = {"SAFE": "Safe",   "MODERATE": "Moderate Risk", "RISKY": "High Risk"}
    return f'<span class="risk {c[risk]}">{l[risk]}</span>'


def level_tag(name):
    c = {"Platinum":"l-platinum","Gold":"l-gold","Silver":"l-silver",
         "Bronze":"l-bronze","Starter":"l-starter"}
    return f'<span class="lvl {c.get(name,"l-starter")}">{name}</span>'


def cmp_row(label, before, after, fmt=None, higher_better=True):
    b = fmt(before) if fmt else f"{before:.1f}"
    a = fmt(after)  if fmt else f"{after:.1f}"
    d = after - before
    if   abs(d) < 0.05:               cls = "cmp-eq"
    elif (d > 0) == higher_better:    cls = "cmp-up"
    else:                              cls = "cmp-dn"
    return (f'<div class="cmp">'
            f'<span class="cmp-lbl">{label}</span>'
            f'<span class="cmp-old">{b}</span>'
            f'<span class="cmp-arr">&#8594;</span>'
            f'<span class="{cls}">{a}</span>'
            f'</div>')


def section(title):
    st.markdown(f'<span class="lbl">{title}</span>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════
if "username" not in st.session_state:
    st.session_state.username = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_income" not in st.session_state:
    st.session_state.last_income = 50000.0
if "last_expenses" not in st.session_state:
    st.session_state.last_expenses = 35000.0
if "last_savings" not in st.session_state:
    st.session_state.last_savings = 120000.0


# ══════════════════════════════════════════════
# LOGIN GATE — lightweight username entry
# ══════════════════════════════════════════════
if not st.session_state.logged_in:
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; margin-bottom:32px;">
          <div style="font-family:Syne,sans-serif;font-size:32px;font-weight:800;
                      color:#e2e8f0;letter-spacing:-1px;">
            FIN<span style="color:#10b981;">VERSE</span>
          </div>
          <div style="font-size:12px;color:#1e3a5f;letter-spacing:0.2em;
                      text-transform:uppercase;margin-top:4px;">
            Financial Safety Platform
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Enter your name to begin")
        name_in = st.text_input("Name", placeholder="e.g. Aashi", label_visibility="collapsed")
        if st.button("ENTER FINVERSE"):
            if name_in.strip():
                st.session_state.username   = name_in.strip()
                st.session_state.logged_in  = True
                # Load saved settings
                settings = get_user_settings(name_in.strip())
                st.session_state.daily_budget = settings["daily_budget"]
                st.session_state.streak       = settings["streak"]
                # Load saved challenges
                st.session_state.challenges_done = get_completed_challenges(name_in.strip())
                st.rerun()
            else:
                st.warning("Enter a name to continue.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════
# MAIN APP  (only reached after login)
# ══════════════════════════════════════════════
username = st.session_state.username
persona_name = "💼 Working Professional"   # will be overridden by sidebar

# ── SIDEBAR ──────────────────────────────────
with st.sidebar:
    # User chip
    st.markdown(
        f"<div style='background:#050a14;border:1px solid #0d1a2e;border-radius:8px;"
        f"padding:12px 14px;margin-bottom:20px;'>"
        f"<div style='font-size:10px;color:#1e3a5f;text-transform:uppercase;"
        f"letter-spacing:0.12em;margin-bottom:4px;'>Signed in as</div>"
        f"<div style='font-family:Syne,sans-serif;font-size:16px;font-weight:700;"
        f"color:#10b981;'>{username}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;"
        "text-transform:uppercase;color:#1e3a5f;margin-bottom:8px;'>Profile Type</div>",
        unsafe_allow_html=True,
    )
    persona_name = st.selectbox(
        "Profile", list(PERSONAS.keys()), index=1, label_visibility="collapsed"
    )
    persona = PERSONAS[persona_name]

    st.markdown(
        f"<div style='background:#050a14;border:1px solid #0d1a2e;border-radius:8px;"
        f"padding:14px 16px;margin:14px 0;'>"
        f"<div style='font-size:10px;color:#1e3a5f;text-transform:uppercase;"
        f"letter-spacing:0.1em;'>Savings Target</div>"
        f"<div style='font-family:DM Mono,monospace;font-size:20px;color:#e2e8f0;"
        f"margin:2px 0 10px 0;'>{persona['savings_rate_target']}%</div>"
        f"<div style='font-size:10px;color:#1e3a5f;text-transform:uppercase;"
        f"letter-spacing:0.1em;'>Emergency Fund</div>"
        f"<div style='font-family:DM Mono,monospace;font-size:20px;color:#e2e8f0;"
        f"margin:2px 0;'>{persona['survival_target']} months</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;"
        "text-transform:uppercase;color:#1e3a5f;margin:16px 0 8px 0;'>Guidance</div>",
        unsafe_allow_html=True,
    )
    for tip in persona["tips"]:
        st.markdown(
            f"<p style='font-size:11px;color:#334155;margin:0 0 8px 0;"
            f"line-height:1.55;padding-left:8px;border-left:2px solid #0d1a2e;'>"
            f"{tip}</p>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border-color:#0d1a2e;margin:18px 0;'>", unsafe_allow_html=True)

    # XP
    xp = get_total_xp(st.session_state.get("challenges_done", set()))
    st.markdown(
        f"<div style='background:#050a14;border:1px solid #0d1a2e;border-radius:8px;"
        f"padding:14px;text-align:center;'>"
        f"<div style='font-family:DM Mono,monospace;font-size:32px;font-weight:500;"
        f"color:#10b981;'>{xp}</div>"
        f"<div style='font-size:10px;color:#1e3a5f;text-transform:uppercase;"
        f"letter-spacing:0.12em;margin-top:3px;'>Total XP</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border-color:#0d1a2e;margin:18px 0;'>", unsafe_allow_html=True)

    # Sign out
    if st.button("SIGN OUT"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown(
        "<p style='font-size:10px;color:#0d1a2e;text-align:center;margin-top:16px;'>"
        "Finverse v5.0 · Not financial advice</p>",
        unsafe_allow_html=True,
    )


# ── APP HEADER ────────────────────────────────
st.markdown("""
<div style="padding:20px 0 20px 0;border-bottom:1px solid #0d1a2e;margin-bottom:24px;
            display:flex;justify-content:space-between;align-items:center;">
  <div>
    <div style="font-family:Syne,sans-serif;font-size:20px;font-weight:800;
                color:#e2e8f0;letter-spacing:-0.3px;">
      FIN<span style="color:#10b981;">VERSE</span>
    </div>
    <div style="font-size:10px;color:#1e3a5f;letter-spacing:0.18em;
                text-transform:uppercase;margin-top:1px;">
      Financial Safety Platform
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tabs = st.tabs([
    "Score", "What-If", "Suggestions",
    "Tracker", "Money Rules", "Partner", "Leaderboard"
])
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = tabs


# ════════════════════════════════════════════
# TAB 1 — SCORE
# ════════════════════════════════════════════
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Monthly Snapshot")
    c1, c2 = st.columns(2)
    with c1:
        income   = st.number_input(persona["income_label"], min_value=0.0, value=50000.0, step=1000.0, key="t1_inc")
        savings  = st.number_input("Total Savings (INR)",   min_value=0.0, value=120000.0, step=5000.0, key="t1_sav")
    with c2:
        expenses = st.number_input("Monthly Expenses (INR)", min_value=0.0, value=35000.0, step=1000.0, key="t1_exp")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("CALCULATE SAFETY SCORE", key="t1_calc"):
        if income <= 0:
            st.error("Income must be greater than zero.")
            st.stop()

        result = analyse_finances(income, expenses, savings)
        lv     = get_level(result["composite_score"])
        next_l = get_next_level(result["composite_score"])
        bdgs   = get_badges(result)
        score  = result["composite_score"]
        risk   = result["risk_level"]

        # Persist
        save_score(username, persona_name, income, expenses, savings, result)
        upsert_leaderboard(username, score, lv["name"], persona_name)

        st.session_state.last_result   = result
        st.session_state.last_income   = income
        st.session_state.last_expenses = expenses
        st.session_state.last_savings  = savings

        # Score card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        rc1, rc2 = st.columns([1, 2])
        with rc1:
            st.markdown(ring(score), unsafe_allow_html=True)
        with rc2:
            st.markdown(
                f"<div style='padding:6px 0;'>"
                f"{level_tag(lv['name'])}"
                f"<div style='font-family:Syne,sans-serif;font-size:22px;font-weight:700;"
                f"color:#e2e8f0;margin:8px 0 6px 0;line-height:1.2;'>{lv['message']}</div>"
                f"{risk_tag(risk)}"
                f"<div style='font-size:12px;color:#334155;margin-top:8px;'>{get_risk_advice(risk)}</div>"
                f"{'<div style=\"font-size:11px;color:#1e3a5f;margin-top:6px;\">'+str(next_l[\"points_needed\"])+\" pts to \"+next_l[\"name\"]+\"</div>\" if next_l else ''}"
                f"</div>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Metrics
        sr  = result["savings_rate"];   sm = result["survival_months"];  er = result["expense_ratio"]
        sc  = "#10b981" if sr >= 20 else ("#f59e0b" if sr >= 10 else "#ef4444")
        smc = "#10b981" if sm >= 6  else ("#f59e0b" if sm >= 3  else "#ef4444")
        erc = "#10b981" if er <= 60 else ("#f59e0b" if er <= 80 else "#ef4444")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Key Metrics")
        st.markdown(f"""
        <div class="stat-grid">
          <div class="stat-box">
            <div class="stat-val" style="color:{sc};">{sr:.1f}%</div>
            <div class="stat-key">Savings Rate</div>
            <div class="stat-note">{get_savings_rate_message(sr)}</div>
          </div>
          <div class="stat-box">
            <div class="stat-val" style="color:{smc};">{format_months(sm)}</div>
            <div class="stat-key">Survival Time</div>
            <div class="stat-note">{get_survival_message(sm)}</div>
          </div>
          <div class="stat-box">
            <div class="stat-val" style="color:{erc};">{er:.1f}%</div>
            <div class="stat-key">Expense Ratio</div>
            <div class="stat-note">of income on expenses</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(bar(min(100, int(sr / 30 * 100)), sc),   unsafe_allow_html=True)
        st.markdown(bar(min(100, int(sm / 12 * 100)), smc),  unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Monthly picture
        surplus = income - expenses
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Monthly Picture")
        m1, m2, m3 = st.columns(3)
        m1.metric("Income",   format_currency(income))
        m2.metric("Expenses", format_currency(expenses))
        m3.metric("Surplus" if surplus >= 0 else "Deficit", format_currency(abs(surplus)),
                  delta_color="normal" if surplus >= 0 else "inverse")
        st.markdown('</div>', unsafe_allow_html=True)

        # Badges
        if bdgs:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            section("Achievements")
            st.markdown(
                "".join(f'<span class="badge">{b["name"].split(" ",1)[-1]}</span>' for b in bdgs),
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Score history
        history = get_score_history(username, limit=5)
        if len(history) > 1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            section("Your Score History")
            for h in history:
                dt = h["created_at"][:16]
                col = "#10b981" if h["risk_level"] == "SAFE" else ("#f59e0b" if h["risk_level"] == "MODERATE" else "#ef4444")
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:8px 0;border-bottom:1px solid #0d1a2e;'>"
                    f"<span style='font-size:11px;color:#1e3a5f;font-family:DM Mono,monospace;'>{dt}</span>"
                    f"<span style='font-family:DM Mono,monospace;font-size:16px;color:{col};'>{h['score']:.1f}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        # Challenges
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Active Challenges")
        for ch in get_challenges():
            done = ch["id"] in st.session_state.get("challenges_done", set())
            ca, cb = st.columns([5, 1])
            with ca:
                op = "ch-done" if done else ""
                st.markdown(
                    f"<div class='ch-row {op}'>"
                    f"<div><div class='ch-name'>{ch['name']}</div>"
                    f"<div class='ch-desc'>{ch['desc']}</div></div>"
                    f"<div class='ch-xp' style='margin-left:auto;white-space:nowrap;"
                    f"padding-left:10px;'>+{ch['reward_xp']} XP</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            with cb:
                if not done:
                    if st.button("Done", key=f"ch_{ch['id']}"):
                        save_challenge(username, ch["id"])
                        if "challenges_done" not in st.session_state:
                            st.session_state.challenges_done = set()
                        st.session_state.challenges_done.add(ch["id"])
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:56px 28px;">
          <div style="font-family:DM Mono,monospace;font-size:52px;color:#0d1a2e;
                      font-weight:500;letter-spacing:-2px;line-height:1;">--</div>
          <div style="font-family:Syne,sans-serif;font-size:17px;font-weight:700;
                      color:#1e3a5f;margin-top:14px;">Enter your numbers and calculate</div>
          <div style="font-size:12px;color:#0d1a2e;margin-top:5px;">
              Your financial safety score appears here</div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2 — WHAT-IF
# ════════════════════════════════════════════
with tab2:
    if not st.session_state.last_result:
        st.markdown('<div class="card" style="text-align:center;padding:40px;color:#1e3a5f;">Calculate your score in the Score tab first.</div>', unsafe_allow_html=True)
    else:
        base  = st.session_state.last_result
        bi    = st.session_state.last_income
        be    = st.session_state.last_expenses
        bs    = st.session_state.last_savings

        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Adjust Scenario")
        st.markdown('<p style="font-size:12px;color:#334155;margin:0 0 16px 0;">Drag sliders to see the instant impact. No recalculation needed.</p>', unsafe_allow_html=True)
        id_ = st.slider("Income change per month (INR)",  -20000, 50000,  0, 1000)
        ed_ = st.slider("Expense change per month (INR)", -20000, 20000,  0,  500)
        sd_ = st.slider("Extra savings added (INR)",           0, 500000, 0, 5000)
        st.markdown('</div>', unsafe_allow_html=True)

        nr    = calculate_whatif(bi, be, bs, {"income_delta": id_, "expenses_delta": ed_, "savings_delta": sd_})
        ns    = nr["composite_score"];  os_ = base["composite_score"];  diff = ns - os_
        dc    = "#10b981" if diff >= 0 else "#ef4444"

        ra, rb = st.columns(2)
        with ra:
            st.markdown(
                f'<div class="card" style="text-align:center;">'
                f'<span class="lbl" style="display:block;text-align:center;">Current</span>'
                f'{ring(os_, 120)}'
                f'<div style="margin-top:10px;">{risk_tag(base["risk_level"])}</div>'
                f'</div>', unsafe_allow_html=True)
        with rb:
            arrow = "+" if diff >= 0 else ""
            st.markdown(
                f'<div class="card" style="text-align:center;">'
                f'<span class="lbl" style="display:block;text-align:center;">New Scenario</span>'
                f'{ring(ns, 120)}'
                f'<div style="margin-top:10px;">{risk_tag(nr["risk_level"])}</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:15px;'
                f'color:{dc};margin-top:8px;font-weight:500;">{arrow}{diff:.1f} pts</div>'
                f'</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Metric Comparison")
        st.markdown(
            cmp_row("Savings Rate",    base["savings_rate"],    nr["savings_rate"],    lambda v: f"{v:.1f}%") +
            cmp_row("Survival Time",   base["survival_months"], nr["survival_months"], lambda v: format_months(v)) +
            cmp_row("Expense Ratio",   base["expense_ratio"],   nr["expense_ratio"],   lambda v: f"{v:.1f}%", higher_better=False) +
            cmp_row("Monthly Surplus", bi - be, (bi + id_) - (be + ed_),              lambda v: format_currency(v)),
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if   diff > 10: st.success(f"+{diff:.1f} points — moves to {nr['risk_level']}.")
        elif diff > 0:  st.info(f"Small improvement of {diff:.1f} points.")
        elif diff < -10:st.error(f"{diff:.1f} points — drops to {nr['risk_level']}.")
        elif diff < 0:  st.warning(f"Small decline of {abs(diff):.1f} points.")
        else:           st.info("No meaningful change.")


# ════════════════════════════════════════════
# TAB 3 — SUGGESTIONS
# ════════════════════════════════════════════
with tab3:
    if not st.session_state.last_result:
        st.markdown('<div class="card" style="text-align:center;padding:40px;color:#1e3a5f;">Calculate your score in the Score tab first.</div>', unsafe_allow_html=True)
    else:
        res   = st.session_state.last_result
        suggs = generate_suggestions(
            st.session_state.last_income,
            st.session_state.last_expenses,
            st.session_state.last_savings,
            res,
        )
        st.markdown(
            "<div style='margin-bottom:20px;'>"
            "<div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;"
            "color:#e2e8f0;'>Action Plan</div>"
            "<div style='font-size:12px;color:#334155;margin-top:3px;'>"
            "Ranked by impact. Work top to bottom.</div></div>",
            unsafe_allow_html=True,
        )
        order = {"High": 0, "Medium": 1, "Low": 2}
        for s in sorted(suggs, key=lambda x: order.get(x["impact"], 3)):
            cls  = {"High":"sug-h","Medium":"sug-m","Low":"sug-l"}[s["impact"]]
            icls = {"High":"imp-h","Medium":"imp-m","Low":"imp-l"}[s["impact"]]
            st.markdown(
                f'<div class="sug {cls}">'
                f'<div class="sug-title">{s["title"]}'
                f'<span class="imp {icls}">{s["impact"]}</span></div>'
                f'<div class="sug-body">{s["detail"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown("""
        <div class="quote">
          <div class="quote-h">Save first. Spend what remains.</div>
          <div class="quote-b">
            Most people spend first and save whatever is left — which is usually nothing.
            Reverse the order: move your savings target to a separate account on salary day.
            Your spending is then naturally constrained. This one habit compounds silently.
          </div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 4 — DAILY TRACKER
# ════════════════════════════════════════════
with tab4:
    settings = get_user_settings(username)

    # Top row
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Daily Tracker")
    hc1, hc2, hc3 = st.columns(3)
    hc1.metric("Streak", f"{settings['streak']} days")
    hc2.metric("Today's Budget", format_currency(settings["daily_budget"]))
    with hc3:
        new_budget = st.number_input(
            "Change Daily Budget (INR)",
            min_value=0.0, value=float(settings["daily_budget"]), step=100.0,
        )
        if new_budget != settings["daily_budget"]:
            save_user_settings(username, new_budget, settings["streak"], settings["last_tracked"])
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Add expense form
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Add Expense")
    ac1, ac2, ac3 = st.columns([2, 2, 3])
    with ac1:
        cat = st.selectbox("Category", [
            "Food", "Transport", "Shopping", "Bills",
            "Entertainment", "Health", "Education", "Other",
        ])
    with ac2:
        amt = st.number_input("Amount (INR)", min_value=0.0, value=0.0, step=10.0)
    with ac3:
        note = st.text_input("Note", placeholder="e.g. Lunch at office")

    if st.button("ADD EXPENSE", key="add_exp"):
        if amt > 0:
            save_expense(username, cat, float(amt), note)
            st.success(f"Added: {cat} — {format_currency(amt)}")
            st.rerun()
        else:
            st.warning("Enter an amount greater than zero.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Today's expenses
    today_exps = get_today_expenses(username)
    budget     = settings["daily_budget"]

    if today_exps:
        total   = sum(e["amount"] for e in today_exps)
        left    = budget - total
        pct     = min(100, int(total / budget * 100)) if budget > 0 else 100
        bc      = "#10b981" if pct < 70 else ("#f59e0b" if pct < 90 else "#ef4444")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Today's Summary")
        ds1, ds2, ds3 = st.columns(3)
        ds1.metric("Spent",     format_currency(total))
        ds2.metric("Budget",    format_currency(budget))
        ds3.metric("Remaining" if left >= 0 else "Over Budget",
                   format_currency(abs(left)),
                   delta_color="normal" if left >= 0 else "inverse")
        st.markdown(bar(pct, bc), unsafe_allow_html=True)
        if pct >= 90: st.error("Approaching daily budget limit.")
        elif pct >= 70: st.warning("Budget usage is high today.")
        else: st.success("On track today.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Expense list with DELETE button
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Expense Log — click Delete to remove any entry")
        for exp in reversed(today_exps):
            ec1, ec2, ec3, ec4, ec5 = st.columns([2, 3, 2, 2, 1])
            with ec1:
                st.markdown(
                    f"<span style='font-size:11px;color:#334155;font-weight:700;"
                    f"text-transform:uppercase;letter-spacing:0.08em;'>{exp['category']}</span>",
                    unsafe_allow_html=True,
                )
            with ec2:
                st.markdown(
                    f"<span style='font-size:12px;color:#475569;'>{exp['note']}</span>",
                    unsafe_allow_html=True,
                )
            with ec3:
                st.markdown(
                    f"<span style='font-family:DM Mono,monospace;font-size:13px;"
                    f"color:#1e3a5f;'>{exp['created_at'][11:16]}</span>",
                    unsafe_allow_html=True,
                )
            with ec4:
                st.markdown(
                    f"<span style='font-family:DM Mono,monospace;font-size:14px;"
                    f"color:#e2e8f0;'>{format_currency(exp['amount'])}</span>",
                    unsafe_allow_html=True,
                )
            with ec5:
                if st.button("Delete", key=f"del_{exp['id']}"):
                    delete_expense(exp["id"])
                    st.rerun()

        st.markdown("<hr style='border-color:#0d1a2e;margin:14px 0;'>", unsafe_allow_html=True)

        # Category breakdown
        section("By Category")
        cat_totals = {}
        for exp in today_exps:
            cat_totals[exp["category"]] = cat_totals.get(exp["category"], 0) + exp["amount"]
        for ct, ca in sorted(cat_totals.items(), key=lambda x: -x[1]):
            cp = int(ca / total * 100) if total > 0 else 0
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;"
                f"font-size:12px;margin-bottom:3px;'>"
                f"<span style='color:#475569;text-transform:uppercase;"
                f"letter-spacing:0.06em;font-size:11px;'>{ct}</span>"
                f"<span style='font-family:DM Mono,monospace;color:#94a3b8;'>"
                f"{format_currency(ca)} ({cp}%)</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown(bar(cp, "#334155"), unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#0d1a2e;margin:14px 0;'>", unsafe_allow_html=True)
        if st.button("END DAY — SAVE STREAK", use_container_width=True):
            new_streak = end_day_update_streak(username)
            st.success(f"Day saved. Streak: {new_streak} days.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Monthly summary
        monthly = get_monthly_expenses(username)
        if monthly:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            section("This Month — All Categories")
            month_total = sum(r["total"] for r in monthly)
            for row in monthly:
                pct = int(row["total"] / month_total * 100) if month_total > 0 else 0
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;"
                    f"align-items:center;font-size:12px;margin-bottom:3px;'>"
                    f"<span style='color:#475569;text-transform:uppercase;"
                    f"letter-spacing:0.06em;font-size:11px;'>{row['category']}"
                    f"<span style='color:#1e3a5f;margin-left:6px;'>({row['count']} entries)</span></span>"
                    f"<span style='font-family:DM Mono,monospace;color:#94a3b8;'>"
                    f"{format_currency(row['total'])}</span></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(bar(pct, "#0d1a2e"), unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-family:DM Mono,monospace;font-size:16px;"
                f"color:#e2e8f0;margin-top:12px;border-top:1px solid #0d1a2e;"
                f"padding-top:10px;'>Total: {format_currency(month_total)}</div>",
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='card' style='text-align:center;padding:40px;color:#1e3a5f;'>"
            "No expenses logged today. Add one above to start tracking."
            "</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# TAB 5 — MONEY RULES
# ════════════════════════════════════════════
with tab5:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Personal Finance Rules — Enter Your Numbers")
    rc1, rc2 = st.columns(2)
    with rc1:
        r_inc = st.number_input("Monthly Income (INR)",   min_value=0.0, value=50000.0, step=1000.0, key="r_i")
        r_sav = st.number_input("Current Savings (INR)",  min_value=0.0, value=120000.0, step=5000.0, key="r_s")
    with rc2:
        r_exp = st.number_input("Monthly Expenses (INR)", min_value=0.0, value=35000.0, step=1000.0, key="r_e")
        r_age = st.slider("Your Age", 18, 60, 25)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("SHOW MY NUMBERS", key="rules_btn"):
        rules = calculate_savings_rules(r_inc, r_exp, r_sav, r_age)

        # Rule 1
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Rule 1 — The 50 / 30 / 20 Rule")
        st.markdown(
            "<p style='font-size:12px;color:#334155;margin:0 0 14px 0;'>"
            "50% on needs, 30% on wants, 20% on savings. Simple. Proven.</p>",
            unsafe_allow_html=True,
        )
        r1a, r1b, r1c = st.columns(3)
        r1a.metric("50% — Needs",   format_currency(rules["rule_50_needs"]),   "rent, food, bills")
        r1b.metric("30% — Wants",   format_currency(rules["rule_30_wants"]),   "dining, shopping")
        r1c.metric("20% — Savings", format_currency(rules["rule_20_savings"]), "investments")
        actual = r_inc - r_exp
        gap    = rules["rule_20_savings"] - actual
        if actual >= rules["rule_20_savings"]:
            st.success(f"You save {format_currency(actual)}/month — above the 20% target.")
        else:
            st.warning(f"You are {format_currency(gap)} short of the 20% savings target.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Rule 2
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Rule 2 — Emergency Fund Rule")
        st.markdown(
            "<p style='font-size:12px;color:#334155;margin:0 0 14px 0;'>"
            "Keep 3–6 months of expenses in a liquid account. This is your survival buffer.</p>",
            unsafe_allow_html=True,
        )
        ef1, ef2, ef3 = st.columns(3)
        ef1.metric("3-Month Target",  format_currency(rules["emergency_3m"]))
        ef2.metric("6-Month Target",  format_currency(rules["emergency_6m"]))
        ef3.metric("Your Coverage",   format_months(rules["current_coverage"]))
        if rules["current_coverage"] >= 6:
            st.success("You have hit the 6-month emergency fund target.")
        elif rules["current_coverage"] >= 3:
            m = rules.get("months_to_6m_fund")
            if m:
                st.info(f"At current rate, you reach 6 months in {m:.0f} more months.")
        else:
            m = rules.get("months_to_6m_fund")
            if m:
                st.warning(f"Time to 6-month fund at current savings rate: {m:.0f} months.")
            else:
                st.error("Create a monthly surplus before building an emergency fund.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Rule 3
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Rule 3 — FIRE Number")
        st.markdown(
            "<p style='font-size:12px;color:#334155;margin:0 0 14px 0;'>"
            "Financial Independence = 25x your annual expenses. "
            "At a 4% withdrawal rate this corpus lasts indefinitely.</p>",
            unsafe_allow_html=True,
        )
        fi1, fi2 = st.columns(2)
        fi1.metric("Your FIRE Number", format_currency(rules["fire_number"]))
        fi2.metric("Current Progress", f"{rules['fire_progress']:.1f}%")
        st.markdown(bar(min(100, int(rules["fire_progress"])), "#10b981"), unsafe_allow_html=True)
        remaining = rules["fire_number"] - r_sav
        if remaining > 0 and (r_inc - r_exp) > 0:
            years = round(remaining / max(1, r_inc - r_exp) / 12, 1)
            st.info(f"{format_currency(remaining)} remaining to FIRE — approx {years} years at current surplus (before investment growth).")
        elif rules["fire_progress"] >= 100:
            st.success("You have reached your FIRE number.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Rule 4
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section(f"Rule 4 — 100-Age Investment Rule (Age {r_age})")
        st.markdown(
            f"<p style='font-size:12px;color:#334155;margin:0 0 14px 0;'>"
            f"Put {rules['equity_pct']}% in equity (stocks/mutual funds) and "
            f"{rules['debt_pct']}% in debt instruments (FD, bonds, PPF). Rebalance yearly.</p>",
            unsafe_allow_html=True,
        )
        ia1, ia2 = st.columns(2)
        ia1.metric(f"Equity {rules['equity_pct']}%", format_currency(rules["equity_amount"]), "stocks, mutual funds")
        ia2.metric(f"Debt {rules['debt_pct']}%",     format_currency(rules["debt_amount"]),   "FD, bonds, PPF")
        st.markdown('</div>', unsafe_allow_html=True)

        # Monthly picture
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Monthly Picture")
        mp1, mp2 = st.columns(2)
        mp1.metric("Monthly Surplus", format_currency(rules["monthly_surplus"]))
        mp2.metric("Annual Surplus",  format_currency(rules["annual_surplus"]))
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 6 — PARTNER
# ════════════════════════════════════════════
with tab6:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Financial Compatibility")
    st.markdown(
        "<p style='font-size:12px;color:#334155;margin:0 0 16px 0;'>"
        "Compare two financial profiles — combined health, alignment score, "
        "and the minimum partner income for a stable shared future.</p>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;color:#1e3a5f;text-transform:uppercase;margin-bottom:8px;'>You</div>", unsafe_allow_html=True)
        p1i = st.number_input("Your Income",   min_value=0.0, value=50000.0, step=1000.0, key="p1i")
        p1e = st.number_input("Your Expenses", min_value=0.0, value=35000.0, step=1000.0, key="p1e")
        p1s = st.number_input("Your Savings",  min_value=0.0, value=120000.0,step=5000.0, key="p1s")
    with pc2:
        st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;color:#1e3a5f;text-transform:uppercase;margin-bottom:8px;'>Partner</div>", unsafe_allow_html=True)
        p2i = st.number_input("Partner Income",   min_value=0.0, value=45000.0, step=1000.0, key="p2i")
        p2e = st.number_input("Partner Expenses", min_value=0.0, value=30000.0, step=1000.0, key="p2e")
        p2s = st.number_input("Partner Savings",  min_value=0.0, value=80000.0, step=5000.0, key="p2s")

    if st.button("CALCULATE COMPATIBILITY", use_container_width=True):
        r1     = analyse_finances(p1i, p1e, p1s)
        r2     = analyse_finances(p2i, p2e, p2s)
        compat = analyse_compatibility(r1, r2)
        cs     = compat["compatibility_score"]

        if   cs >= 75: lbl, col = "Excellent Match",   "#10b981"
        elif cs >= 55: lbl, col = "Good Match",        "#f59e0b"
        elif cs >= 35: lbl, col = "Needs Alignment",   "#f59e0b"
        else:          lbl, col = "Significant Gap",   "#ef4444"

        st.markdown(
            f"<div class='card' style='text-align:center;padding:32px;'>"
            f"<div style='font-family:DM Mono,monospace;font-size:60px;font-weight:500;"
            f"color:{col};letter-spacing:-3px;line-height:1;'>{cs:.0f}</div>"
            f"<div style='font-family:Syne,sans-serif;font-size:17px;font-weight:700;"
            f"color:#e2e8f0;margin-top:6px;'>{lbl}</div>"
            f"<div style='font-size:11px;color:#1e3a5f;margin-top:3px;'>out of 100</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        ia, ib, ic = st.columns(3)
        ia.metric("Your Score",     f"{r1['composite_score']} / 100")
        ib.metric("Partner Score",  f"{r2['composite_score']} / 100")
        ic.metric("Alignment",      f"{compat['alignment_score']} / 100")

        combined = compat["combined"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Combined Picture")
        cf1, cf2, cf3, cf4 = st.columns(4)
        cf1.metric("Combined Income",  format_currency(combined["income"]))
        cf2.metric("Combined Savings", format_currency(combined["savings"]))
        cf3.metric("Survive Together", format_months(combined["survival_months"]))
        cf4.metric("Combined Score",   f"{combined['composite_score']} / 100")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Ideal Partner Income Calculator")
        t_sr = st.slider("Target Combined Savings Rate (%)", 10, 40, 20, key="tsr")
        rec  = recommended_partner_income(p1i, p1e, p1s, t_sr)
        ri1, ri2, ri3 = st.columns(3)
        ri1.metric("Min. Partner Income",     format_currency(rec["min_partner_income"]), "per month")
        ri2.metric("Emergency Fund Target",   format_currency(rec["target_combined_savings"]))
        ri3.metric("Partner Monthly Savings", format_currency(rec["partner_monthly_savings_target"]))
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 7 — LEADERBOARD
# ════════════════════════════════════════════
with tab7:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Global Leaderboard — All Users")
    st.markdown(
        "<p style='font-size:12px;color:#334155;margin:0 0 14px 0;'>"
        "Every user who calculates a score is automatically ranked here. "
        "Data is saved in the database.</p>",
        unsafe_allow_html=True,
    )

    lb_data = get_leaderboard(limit=25)

    if lb_data:
        for i, e in enumerate(lb_data):
            is_me  = e["username"] == username
            bg     = "#041810" if is_me else "#080f1e"
            border = "1px solid #064e35" if is_me else "1px solid #0d1a2e"
            rank   = f"0{i+1}" if i + 1 < 10 else str(i + 1)
            st.markdown(
                f"<div class='lb-row' style='background:{bg};border:{border};'>"
                f"<span class='lb-rank'>{rank}</span>"
                f"<span class='lb-name' style='{'color:#10b981;font-weight:700;' if is_me else ''}'>"
                f"{e['username']}{'  (you)' if is_me else ''}</span>"
                f"<span class='lb-lvl'>{e['level_name']}</span>"
                f"<span class='lb-lvl' style='margin-right:0;'>{e['persona'].split()[-1]}</span>"
                f"<span class='lb-score'>{e['score']:.1f}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<div style='text-align:center;padding:32px;color:#1e3a5f;'>"
            "No scores yet. Be the first — calculate your score in the Score tab."
            "</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Share
    if st.session_state.last_result:
        sc = st.session_state.last_result["composite_score"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Share")
        msg = f"My Finverse Financial Safety Score: {sc:.1f}/100 — Find out yours: [your link]"
        st.code(msg, language=None)
        st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────
st.markdown(
    "<div style='text-align:center;padding:28px 0 0;border-top:1px solid #0d1a2e;"
    "margin-top:20px;'>"
    "<span style='font-family:Syne,sans-serif;font-size:13px;font-weight:800;"
    "color:#0d1a2e;'>FINVERSE</span>"
    "<span style='font-size:11px;color:#0d1a2e;margin-left:14px;'>v5.0</span>"
    "<span style='font-size:11px;color:#0d1a2e;margin-left:14px;'>Not financial advice</span>"
    "</div>",
    unsafe_allow_html=True,
)
