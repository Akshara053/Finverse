# app.py  —  Finverse v8.0
# Run: streamlit run app.py

import streamlit as st
from datetime import datetime, date

from logic        import (analyse_finances, calculate_savings_rules,
                           analyse_compatibility, recommended_partner_income)
from config       import PERSONAS
from gamification import get_level, get_next_level, get_badges, get_challenges, get_total_xp
from suggestions  import generate_suggestions, calculate_whatif
from analytics    import (calculate_stress_score, get_stress_label,
                           predict_emergency_fund_date, predict_fire_date,
                           get_behavioral_insights, build_score_trend_data,
                           build_expense_trend_data, build_category_data,
                           build_prediction_data)
from database     import (
    init_db, upsert_user_profile, get_user_profile, get_platform_stats,
    save_score, get_score_history,
    save_expense, get_today_expenses, delete_expense,
    get_monthly_expenses, get_spending_trend,
    add_lend_borrow, get_lend_borrow, settle_lend_borrow,
    delete_lend_borrow, get_lend_borrow_summary,
    add_post, get_posts, upvote_post, delete_post,
    mark_module_complete, get_education_progress,
    save_survey_response, get_survey_responses, has_answered_survey,
    upsert_leaderboard, get_leaderboard,
    save_challenge, get_completed_challenges,
    get_user_settings, save_user_settings, end_day_update_streak,
)
from utils import (format_currency, format_months,
                   get_savings_rate_message, get_survival_message, get_risk_advice)

# Safe imports from education — handles both old and new versions
try:
    from education import (LEARNING_MODULES, BOOK_LIST, get_modules_by_level, get_module_by_id)
    try:
        from education import FREE_RESOURCES
    except ImportError:
        FREE_RESOURCES = [
            {"name": "Zerodha Varsity", "url": "https://zerodha.com/varsity",
             "desc": "Best free course on stock markets and investing in India."},
            {"name": "SEBI Investor Education", "url": "https://investor.sebi.gov.in",
             "desc": "Official SEBI portal for investor education."},
            {"name": "Khan Academy Personal Finance",
             "url": "https://www.khanacademy.org/college-careers-more/personal-finance",
             "desc": "Free structured personal finance education."},
        ]
except ImportError:
    LEARNING_MODULES = []
    BOOK_LIST        = []
    FREE_RESOURCES   = []
    def get_modules_by_level(): return {}
    def get_module_by_id(x): return None

try:
    import plotly.graph_objects as go
    PLOTLY = True
except ImportError:
    PLOTLY = False

# ─────────────────────────────────────────────
init_db()

st.set_page_config(
    page_title="Finverse — Your Financial Safety Score",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════
# DESIGN SYSTEM
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #07080f; }
.block-container { max-width: 1100px !important; padding: 0 1.5rem 5rem !important; }

/* ── TOP NAV ── */
.topnav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 0; border-bottom: 1px solid #12182b;
    margin-bottom: 28px; position: sticky; top: 0;
    background: #07080f; z-index: 100;
}
.nav-logo {
    font-size: 20px; font-weight: 800; color: #f1f5f9;
    letter-spacing: -0.5px;
}
.nav-logo span { color: #22c55e; }
.nav-links { display: flex; gap: 4px; }
.nav-btn {
    background: transparent; border: none;
    color: #475569; font-size: 12px; font-weight: 600;
    padding: 7px 14px; border-radius: 8px; cursor: pointer;
    letter-spacing: 0.04em; transition: all 0.15s;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.nav-btn:hover { background: #12182b; color: #e2e8f0; }
.nav-btn.active { background: #12182b; color: #22c55e; }
.nav-user {
    display: flex; align-items: center; gap: 10px;
}
.nav-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 800; color: #fff;
}

/* ── CARDS ── */
.card {
    background: #0d1117; border: 1px solid #12182b;
    border-radius: 16px; padding: 22px 24px; margin-bottom: 16px;
}
.card-hover { transition: all 0.2s; }
.card-hover:hover { border-color: #22c55e; transform: translateY(-1px); box-shadow: 0 8px 24px rgba(34,197,94,0.08); }
.card-green { background: #021a0b; border: 1px solid #14532d; border-radius: 16px; padding: 22px 24px; margin-bottom: 16px; }
.card-red   { background: #1a0508; border: 1px solid #7f1d1d; border-radius: 16px; padding: 22px 24px; margin-bottom: 16px; }
.card-amber { background: #1a0e01; border: 1px solid #78350f; border-radius: 16px; padding: 22px 24px; margin-bottom: 16px; }
.card-blue  { background: #020d1a; border: 1px solid #1e3a5f; border-radius: 16px; padding: 22px 24px; margin-bottom: 16px; }
.card-grad  { background: linear-gradient(135deg, #021a0b, #020d1a); border: 1px solid #14532d; border-radius: 16px; padding: 22px 24px; margin-bottom: 16px; }

/* ── SECTION LABEL ── */
.lbl {
    font-size: 10px; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: #1e3a5f;
    margin: 0 0 14px 0; display: block;
}
.section-title {
    font-size: 18px; font-weight: 800; color: #f1f5f9;
    margin: 0 0 4px 0; letter-spacing: -0.3px;
}
.section-sub { font-size: 13px; color: #334155; margin: 0 0 18px 0; }

/* ── SCORE RING ── */
.ring-wrap { display: flex; flex-direction: column; align-items: center; }

/* ── STAT BOXES ── */
.sg { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 6px; }
.sb {
    flex: 1; min-width: 120px;
    background: #07080f; border: 1px solid #12182b;
    border-radius: 12px; padding: 14px 16px;
}
.sv { font-family: 'Space Mono', monospace; font-size: 22px; font-weight: 700; color: #f1f5f9; line-height: 1.1; }
.sk { font-size: 10px; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 5px; font-weight: 700; }
.sn { font-size: 11px; color: #1e3a5f; margin-top: 3px; line-height: 1.4; }

/* ── RISK / LEVEL TAGS ── */
.tag { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 3px 10px; border-radius: 4px; }
.r-s { background: #021a0b; color: #22c55e; border: 1px solid #14532d; }
.r-m { background: #1a0e01; color: #f59e0b; border: 1px solid #78350f; }
.r-r { background: #1a0508; color: #f87171; border: 1px solid #991b1b; }
.l-pl { background: #0a1f3d; color: #60a5fa; border: 1px solid #1d4ed8; }
.l-go { background: #1a0e01; color: #fbbf24; border: 1px solid #d97706; }
.l-si { background: #0d1a2e; color: #94a3b8; border: 1px solid #334155; }
.l-br { background: #1a0800; color: #fb923c; border: 1px solid #9a3412; }
.l-st { background: #021a0b; color: #34d399; border: 1px solid #065f46; }

/* ── BAR ── */
.bt { background: #12182b; border-radius: 2px; height: 4px; margin: 5px 0 12px 0; }
.bf { height: 4px; border-radius: 2px; }

/* ── SUGGESTION ── */
.sug { background: #0d1117; border: 1px solid #12182b; border-radius: 12px; padding: 16px 18px; margin-bottom: 10px; }
.sug-h { border-left: 3px solid #f87171; }
.sug-m { border-left: 3px solid #f59e0b; }
.sug-l { border-left: 3px solid #22c55e; }
.stit { font-size: 14px; font-weight: 700; color: #f1f5f9; margin: 0 0 5px 0; }
.sbod { font-size: 12px; color: #334155; margin: 0; line-height: 1.7; }
.imp { display: inline-block; font-size: 9px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 2px 7px; border-radius: 3px; margin-left: 8px; vertical-align: middle; }
.i-h { background: #1a0508; color: #f87171; }
.i-m { background: #1a0e01; color: #f59e0b; }
.i-l { background: #021a0b; color: #22c55e; }

/* ── CMP ── */
.cmp { display: flex; align-items: center; gap: 10px; padding: 9px 0; border-bottom: 1px solid #12182b; }
.cl  { font-size: 11px; color: #1e3a5f; width: 130px; flex-shrink: 0; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; }
.co  { font-family: 'Space Mono', monospace; font-size: 13px; color: #1e3a5f; width: 75px; }
.ca  { font-size: 11px; color: #12182b; }
.cu  { font-family: 'Space Mono', monospace; font-size: 13px; color: #22c55e; font-weight: 700; }
.cd  { font-family: 'Space Mono', monospace; font-size: 13px; color: #f87171; font-weight: 700; }
.ce  { font-family: 'Space Mono', monospace; font-size: 13px; color: #475569; font-weight: 500; }

/* ── LB ROW ── */
.lbr { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 12px; margin-bottom: 6px; border: 1px solid #12182b; background: #0d1117; }
.lrk { font-family: 'Space Mono', monospace; font-size: 12px; color: #1e3a5f; width: 28px; }
.lnm { flex: 1; font-size: 13px; color: #94a3b8; }
.llv { font-size: 10px; color: #1e3a5f; margin-right: 8px; text-transform: uppercase; letter-spacing: 0.07em; }
.lsc { font-family: 'Space Mono', monospace; font-size: 17px; color: #22c55e; font-weight: 700; }

/* ── POST ── */
.post { background: #0d1117; border: 1px solid #12182b; border-radius: 12px; padding: 16px 18px; margin-bottom: 10px; }
.ptag { font-size: 10px; color: #334155; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; display: inline-block; background: #07080f; border: 1px solid #12182b; padding: 2px 8px; border-radius: 3px; margin-bottom: 8px; }
.paut { font-size: 11px; color: #334155; margin-bottom: 6px; }
.ptxt { font-size: 13px; color: #64748b; line-height: 1.75; }
.pft  { font-size: 11px; color: #1e3a5f; margin-top: 8px; }

/* ── BOOK ── */
.book { background: #0d1117; border: 1px solid #12182b; border-radius: 12px; padding: 16px 18px; margin-bottom: 8px; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117 !important; border-bottom: 1px solid #12182b !important;
    gap: 0 !important; padding: 0 !important; border-radius: 12px 12px 0 0 !important;
    overflow-x: auto !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #334155 !important;
    font-size: 11px !important; font-weight: 700 !important;
    padding: 14px 18px !important; border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    letter-spacing: 0.08em; text-transform: uppercase;
    white-space: nowrap !important;
}
.stTabs [aria-selected="true"] {
    background: transparent !important; color: #22c55e !important;
    border-bottom: 2px solid #22c55e !important;
}
[data-testid="stTabPanel"] { background: transparent !important; padding-top: 20px !important; }

/* ── INPUTS ── */
.stNumberInput input, .stTextInput input {
    background: #07080f !important; border: 1px solid #12182b !important;
    border-radius: 10px !important; color: #f1f5f9 !important;
    font-family: 'Space Mono', monospace !important; font-size: 15px !important;
    padding: 11px 14px !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.1) !important;
}
.stTextArea textarea {
    background: #07080f !important; border: 1px solid #12182b !important;
    border-radius: 10px !important; color: #f1f5f9 !important; font-size: 13px !important;
}
.stTextArea textarea:focus { border-color: #22c55e !important; }
[data-baseweb="select"] > div {
    background: #07080f !important; border: 1px solid #12182b !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] span { color: #f1f5f9 !important; }
label {
    font-size: 10px !important; font-weight: 700 !important; color: #334155 !important;
    text-transform: uppercase !important; letter-spacing: 0.1em !important;
}

/* ── PRIMARY BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: #fff !important; border: none !important; border-radius: 10px !important;
    font-weight: 800 !important; font-size: 12px !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    padding: 13px 24px !important; width: 100% !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    box-shadow: 0 4px 14px rgba(34,197,94,0.25) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(34,197,94,0.35) !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #07080f !important; border: 1px solid #12182b !important;
    border-radius: 12px !important; padding: 14px 16px !important;
}
[data-testid="stMetricLabel"] { font-size: 10px !important; color: #1e3a5f !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }
[data-testid="stMetricValue"] { font-family: 'Space Mono', monospace !important; font-size: 20px !important; color: #f1f5f9 !important; }

/* ── SLIDER ── */
[data-testid="stSlider"] > div > div > div > div { background: #22c55e !important; }
[data-testid="stSlider"] > div > div > div { background: #12182b !important; }

/* ── RADIO / CHECKBOX ── */
.stRadio label  { font-size: 13px !important; color: #64748b !important; text-transform: none !important; letter-spacing: 0 !important; }
.stCheckbox label { font-size: 13px !important; color: #64748b !important; text-transform: none !important; letter-spacing: 0 !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] { background: #0d1117 !important; border: 1px solid #12182b !important; border-radius: 10px !important; font-size: 13px !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] { display: none !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader { background: #0d1117 !important; border: 1px solid #12182b !important; border-radius: 10px !important; color: #94a3b8 !important; font-size: 13px !important; font-weight: 600 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; background: transparent; }
::-webkit-scrollbar-thumb { background: #12182b; border-radius: 4px; }

/* ── LANDING SPECIFIC ── */
.hero-badge {
    display: inline-block; background: #021a0b; border: 1px solid #14532d;
    border-radius: 20px; padding: 5px 16px; font-size: 11px; font-weight: 700;
    color: #22c55e; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 20px;
}
.feature-pill {
    display: inline-block; background: #0d1117; border: 1px solid #12182b;
    border-radius: 20px; padding: 6px 14px; font-size: 12px; font-weight: 600;
    color: #475569; margin: 4px;
}
.stat-hero {
    text-align: center; padding: 20px;
    background: #0d1117; border: 1px solid #12182b;
    border-radius: 14px;
}

/* ── ME PAGE ── */
.profile-card {
    background: linear-gradient(135deg, #021a0b, #020d1a);
    border: 1px solid #14532d; border-radius: 20px;
    padding: 28px; margin-bottom: 16px;
}
.avatar-large {
    width: 64px; height: 64px; border-radius: 50%;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; font-weight: 800; color: #fff; margin-bottom: 14px;
}
.progress-ring { position: relative; display: inline-block; }

/* ── COMPARISON TABLE ── */
.ctbl { width: 100%; border-collapse: collapse; }
.ctbl th { font-size: 10px; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.12em; padding: 8px 12px; border-bottom: 1px solid #12182b; text-align: left; }
.ctbl td { font-size: 12px; color: #64748b; padding: 10px 12px; border-bottom: 1px solid #12182b; }
.ctbl .yes { color: #22c55e; font-weight: 700; }
.ctbl .no  { color: #334155; }
.ctbl .partial { color: #f59e0b; font-weight: 600; }
.ctbl .us  { background: #021a0b !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def ring(score, size=130):
    r = 44; c = 2 * 3.14159 * r
    d = round(score / 100 * c, 1); g = round(c - d, 1)
    col = "#22c55e" if score >= 65 else ("#f59e0b" if score >= 35 else "#f87171")
    return (f'<div class="ring-wrap">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 100 100">'
            f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="#12182b" stroke-width="8"/>'
            f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="{col}" stroke-width="8"'
            f' stroke-dasharray="{d} {g}" stroke-dashoffset="{c*0.25}" stroke-linecap="round"/>'
            f'<text x="50" y="45" text-anchor="middle" font-family="Space Mono,monospace"'
            f' font-size="20" font-weight="700" fill="#f1f5f9">{score:.0f}</text>'
            f'<text x="50" y="60" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif"'
            f' font-size="9" fill="#1e3a5f" letter-spacing="2">SCORE</text>'
            f'</svg></div>')

def bar(pct, color="#22c55e"):
    pct = min(100, max(0, pct))
    return f'<div class="bt"><div class="bf" style="width:{pct}%;background:{color};"></div></div>'

def risk_tag(risk):
    c = {"SAFE": "r-s", "MODERATE": "r-m", "RISKY": "r-r"}
    l = {"SAFE": "Safe", "MODERATE": "Moderate", "RISKY": "High Risk"}
    return f'<span class="tag {c[risk]}">{l[risk]}</span>'

def level_tag(name):
    c = {"Platinum":"l-pl","Gold":"l-go","Silver":"l-si","Bronze":"l-br","Starter":"l-st"}
    return f'<span class="tag {c.get(name,"l-st")}">{name}</span>'

def sec(title, sub=None):
    s = f"<div class='section-sub'>{sub}</div>" if sub else ""
    st.markdown(f"<div class='section-title'>{title}</div>{s}", unsafe_allow_html=True)

def lbl(text):
    st.markdown(f"<span class='lbl'>{text}</span>", unsafe_allow_html=True)

def cmp_row(label, before, after, fmt=None, hb=True):
    b = fmt(before) if fmt else f"{before:.1f}"
    a = fmt(after)  if fmt else f"{after:.1f}"
    d = after - before
    cls = "ce" if abs(d) < 0.05 else ("cu" if (d > 0) == hb else "cd")
    return (f'<div class="cmp"><span class="cl">{label}</span>'
            f'<span class="co">{b}</span><span class="ca">→</span>'
            f'<span class="{cls}">{a}</span></div>')

def plotly_cfg():
    return {
        "paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#475569", "family": "Plus Jakarta Sans", "size": 11},
        "margin": {"l": 10, "r": 10, "t": 28, "b": 10},
        "xaxis": {"gridcolor": "#12182b", "linecolor": "#12182b", "tickfont": {"color":"#334155"}},
        "yaxis": {"gridcolor": "#12182b", "linecolor": "#12182b", "tickfont": {"color":"#334155"}},
    }


# ══════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════
defaults = {
    "page": "landing", "logged_in": False, "username": "",
    "persona_name": "Working Professional",
    "last_result": None, "last_income": 50000.0,
    "last_expenses": 35000.0, "last_savings": 120000.0,
    "challenges_done": set(), "active_tab": "Score",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════
# ──────────────── LANDING PAGE ────────────────
# ══════════════════════════════════════════════
if st.session_state.page == "landing":

    # Top bar
    st.markdown("""
    <div class="topnav">
        <div class="nav-logo">FIN<span>VERSE</span></div>
        <div style="font-size:11px;color:#1e3a5f;">Free · No account · Just your financial truth</div>
    </div>
    """, unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div style="text-align:center;padding:48px 0 40px 0;">
        <div class="hero-badge">India's Financial Safety Platform</div>
        <h1 style="font-size:56px;font-weight:800;color:#f1f5f9;margin:0 0 16px 0;
                   line-height:1.1;letter-spacing:-1.5px;">
            Are you actually<br><span style="color:#22c55e;">financially safe?</span>
        </h1>
        <p style="font-size:18px;color:#475569;max-width:520px;margin:0 auto 12px;line-height:1.75;">
            Most people have no idea. Finverse gives you a clear, honest answer —
            your personal <strong style="color:#94a3b8;">Financial Safety Score</strong> —
            in under 60 seconds.
        </p>
        <p style="font-size:13px;color:#1e3a5f;margin-bottom:32px;">
            Free · No email · No credit card · Works for any income level
        </p>
    </div>
    """, unsafe_allow_html=True)

    h1, h2, h3 = st.columns([1, 2, 1])
    with h2:
        if st.button("GET MY SCORE — FREE", key="hero_cta"):
            st.session_state.page = "onboard"
            st.rerun()

    # Live stats
    stats = get_platform_stats()
    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, val, label in [
        (s1, stats["total_users"], "People Using Finverse"),
        (s2, stats["total_scores"], "Scores Calculated"),
        (s3, f"{stats['avg_score']:.0f}/100", "Average Safety Score"),
        (s4, stats["total_expenses"], "Expenses Tracked"),
    ]:
        with col:
            st.markdown(
                f"<div class='stat-hero'>"
                f"<div style='font-family:Space Mono,monospace;font-size:28px;font-weight:700;"
                f"color:#22c55e;'>{val}</div>"
                f"<div style='font-size:11px;color:#334155;text-transform:uppercase;"
                f"letter-spacing:0.1em;margin-top:4px;'>{label}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # The Problem
    st.markdown("""
    <div style="margin:56px 0 32px 0; text-align:center;">
        <span class="lbl" style="display:block;text-align:center;margin-bottom:12px;">The Problem We're Solving</span>
        <h2 style="font-size:32px;font-weight:800;color:#f1f5f9;margin:0 0 12px 0;letter-spacing:-0.5px;">
            78% of Indians live paycheck to paycheck
        </h2>
        <p style="font-size:15px;color:#475569;max-width:580px;margin:0 auto;line-height:1.8;">
            No one teaches personal finance in school. Banks profit from confusion.
            Most financial apps are built for people who already know finance.
            <strong style="color:#94a3b8;">Finverse is built for everyone else.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    pb1, pb2, pb3 = st.columns(3)
    for col, num, title, desc in [
        (pb1, "01", "You don't know your number", "No app tells you plainly: are you financially safe right now? Finverse does."),
        (pb2, "02", "One bad month can destroy you", "Without an emergency fund, a job loss or medical bill becomes a crisis overnight."),
        (pb3, "03", "Nobody gives you a real plan", "Banks sell products. Apps track numbers. No one tells you exactly what to do next."),
    ]:
        with col:
            st.markdown(
                f"<div class='card card-hover' style='padding:24px;'>"
                f"<div style='font-family:Space Mono,monospace;font-size:12px;color:#22c55e;"
                f"font-weight:700;margin-bottom:12px;'>{num}</div>"
                f"<div style='font-size:15px;font-weight:700;color:#f1f5f9;margin-bottom:8px;'>{title}</div>"
                f"<div style='font-size:13px;color:#475569;line-height:1.65;'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # Our Story
    st.markdown("""
    <div style="margin:48px 0;">
        <div class="card" style="padding:32px 36px;">
            <span class="lbl">Why We Built Finverse</span>
            <h3 style="font-size:22px;font-weight:800;color:#f1f5f9;margin:0 0 14px 0;
                       letter-spacing:-0.3px;">A question no app could answer</h3>
            <p style="font-size:14px;color:#64748b;line-height:1.85;margin:0 0 12px 0;">
                After receiving a salary, paying all the bills, and checking the bank balance —
                the question that kept coming up was:
                <em style="color:#94a3b8;">"Am I actually okay? Or am I just getting by?"</em>
            </p>
            <p style="font-size:14px;color:#64748b;line-height:1.85;margin:0 0 12px 0;">
                We tested every financial app we could find. None of them answered that question directly.
                They showed transactions, charts, categories. But nobody said:
                <em style="color:#94a3b8;">"Here is your safety score. Here is what it means. Here is what to do next."</em>
            </p>
            <p style="font-size:14px;color:#64748b;line-height:1.85;margin:0;">
                That gap is what Finverse fills. One clear score. One honest assessment.
                One personalised action plan. Built for India, by someone who needed it.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features
    st.markdown("""
    <div style="text-align:center;margin:8px 0 28px 0;">
        <h2 style="font-size:28px;font-weight:800;color:#f1f5f9;margin:0 0 8px 0;">Everything in one platform</h2>
        <p style="font-size:13px;color:#334155;">Free. No account needed. Works for students, salaried, freelancers, and business owners.</p>
    </div>
    """, unsafe_allow_html=True)

    fa, fb = st.columns(2)
    features = [
        ("Financial Safety Score", "A single 0–100 score that answers 'Am I safe?' No other Indian app does this."),
        ("Financial Stress Score", "Separate from safety — measures your financial anxiety based on runway and cash flow pressure."),
        ("Daily Expense Tracker", "Log expenses in seconds. Budget alerts. Monthly breakdowns. Streak system."),
        ("Lend / Borrow Manager", "Track who owes you and who you owe. One-tap WhatsApp reminder messages."),
        ("What-If Simulator", "Slide to see how a raise, cut, or bonus changes your score — live, no recalculation."),
        ("Partner Compatibility", "Get a compatibility score and ideal partner income for a stable shared life."),
        ("9 Finance Modules", "Structured learning from Beginner to Advanced with real content and key takeaways."),
        ("Predictions & Insights", "When will you reach FIRE? Emergency fund? Based on your actual data."),
        ("Community Discussions", "Anonymous or named — discuss saving, debt, and investing with real people."),
        ("Gamification", "Levels (Starter → Platinum), badges, XP, challenges, leaderboard."),
    ]
    for i, (t, d) in enumerate(features):
        with (fa if i % 2 == 0 else fb):
            st.markdown(
                f"<div class='card card-hover' style='margin-bottom:10px;'>"
                f"<div style='font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:5px;'>{t}</div>"
                f"<div style='font-size:12px;color:#475569;line-height:1.65;'>{d}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # Competitor comparison
    st.markdown("""
    <div style="text-align:center;margin:48px 0 24px 0;">
        <h2 style="font-size:26px;font-weight:800;color:#f1f5f9;margin:0 0 6px 0;">
            How Finverse compares
        </h2>
        <p style="font-size:13px;color:#334155;">We studied Fi, Jupiter, Walnut, YNAB, Mint, Splitwise, Groww before building this.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="overflow-x:auto;">
    <table class="ctbl">
    <thead>
        <tr>
            <th>Feature</th>
            <th style="color:#22c55e;text-align:center;">Finverse</th>
            <th style="text-align:center;">Fi / Jupiter</th>
            <th style="text-align:center;">Walnut</th>
            <th style="text-align:center;">Splitwise</th>
            <th style="text-align:center;">YNAB</th>
        </tr>
    </thead>
    <tbody>
        <tr class="us"><td>Financial Safety Score (single number)</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td></tr>
        <tr><td>Survival time without income</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td></tr>
        <tr class="us"><td>Financial Stress Score</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td></tr>
        <tr><td>What-If Simulator</td><td class="yes" style="text-align:center;">✓</td><td class="partial" style="text-align:center;">Partial</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="partial" style="text-align:center;">Partial</td></tr>
        <tr class="us"><td>Expense tracking + daily budget</td><td class="yes" style="text-align:center;">✓</td><td class="yes" style="text-align:center;">✓</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">✗</td><td class="yes" style="text-align:center;">✓</td></tr>
        <tr><td>Lend / Borrow with reminders</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">✗</td></tr>
        <tr class="us"><td>Personalised action plan (₹ amounts)</td><td class="yes" style="text-align:center;">✓</td><td class="partial" style="text-align:center;">Partial</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="partial" style="text-align:center;">Partial</td></tr>
        <tr><td>Partner compatibility score</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td></tr>
        <tr class="us"><td>Financial education (structured)</td><td class="yes" style="text-align:center;">✓</td><td class="partial" style="text-align:center;">Partial</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="partial" style="text-align:center;">Partial</td></tr>
        <tr><td>Community discussions</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td><td class="no" style="text-align:center;">✗</td></tr>
        <tr class="us"><td>100% free, no bank link needed</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">✗</td><td class="partial" style="text-align:center;">Partial</td><td class="yes" style="text-align:center;">✓</td><td class="no" style="text-align:center;">Paid</td></tr>
    </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    # Final CTA
    st.markdown("""
    <div style="background:linear-gradient(135deg,#021a0b,#020d1a);border:1px solid #14532d;
                border-radius:20px;padding:48px 36px;text-align:center;margin:40px 0 20px 0;">
        <h2 style="font-size:30px;font-weight:800;color:#f1f5f9;margin:0 0 10px 0;letter-spacing:-0.5px;">
            Your financial truth in 60 seconds
        </h2>
        <p style="font-size:14px;color:#475569;margin:0 0 28px 0;">
            Free. No email. No credit card. No bank link.
        </p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("START NOW — FREE", key="bottom_cta"):
            st.session_state.page = "onboard"
            st.rerun()

    st.markdown(
        "<p style='text-align:center;font-size:11px;color:#1e3a5f;margin-top:16px;'>"
        "Finverse v8.0 · Built in India · Your data stays on this server · Not financial advice</p>",
        unsafe_allow_html=True,
    )
    st.stop()


# ══════════════════════════════════════════════
# ─────────────── ONBOARDING ───────────────────
# ══════════════════════════════════════════════
if st.session_state.page == "onboard":

    st.markdown("""
    <div class="topnav">
        <div class="nav-logo">FIN<span>VERSE</span></div>
    </div>
    """, unsafe_allow_html=True)

    _, oc, _ = st.columns([1, 2, 1])
    with oc:
        st.markdown("""
        <div style="text-align:center;margin-bottom:28px;">
            <div style="font-size:13px;color:#1e3a5f;text-transform:uppercase;
                        letter-spacing:0.16em;font-weight:700;">Step 1 of 2 — About You</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Your Details")
        oa, ob = st.columns(2)
        with oa:
            name_in = st.text_input("Your name", placeholder="e.g. Aashi", key="ob_name")
        with ob:
            age_in  = st.number_input("Age", min_value=16, max_value=80, value=25, step=1)

        city_in = st.text_input("City", placeholder="e.g. Mumbai", key="ob_city")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Your Life Stage")
        st.markdown(
            "<p style='font-size:12px;color:#334155;margin:0 0 14px 0;'>"
            "This sets your personalised targets and tips.</p>",
            unsafe_allow_html=True,
        )
        persona_options = list(PERSONAS.keys())
        selected_persona = st.radio(
            "I am a",
            persona_options,
            format_func=lambda x: f"{PERSONAS[x]['icon']}  {x}",
            index=1,
            label_visibility="collapsed",
        )
        p = PERSONAS[selected_persona]
        st.markdown(
            f"<div style='background:#07080f;border:1px solid #12182b;border-radius:8px;"
            f"padding:12px 14px;margin-top:10px;font-size:12px;color:#475569;'>"
            f"Savings target: <span style='color:#22c55e;font-weight:700;'>{p['savings_rate_target']}%</span>"
            f"  ·  Emergency fund goal: <span style='color:#22c55e;font-weight:700;'>{p['survival_target']} months</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("CONTINUE →", key="onboard_btn"):
            if name_in.strip():
                un = name_in.strip()
                upsert_user_profile(un, un, selected_persona, int(age_in), city_in)
                settings = get_user_settings(un)
                st.session_state.update({
                    "page": "app", "logged_in": True, "username": un,
                    "persona_name": selected_persona,
                    "challenges_done": get_completed_challenges(un),
                })
                st.rerun()
            else:
                st.warning("Please enter your name to continue.")

        st.markdown(
            "<div style='text-align:center;margin-top:14px;'>"
            "<a style='font-size:12px;color:#1e3a5f;cursor:pointer;'>← Back to home</a>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Back", key="back_land", help="Go back to home"):
            st.session_state.page = "landing"
            st.rerun()

    st.stop()


# ══════════════════════════════════════════════
# ────────────────── MAIN APP ──────────────────
# ══════════════════════════════════════════════
if not st.session_state.logged_in:
    st.session_state.page = "landing"
    st.rerun()

un      = st.session_state.username
persona = PERSONAS[st.session_state.persona_name]
profile = get_user_profile(un) or {}
settings_ = get_user_settings(un)
xp_total = get_total_xp(st.session_state.get("challenges_done", set()))

# ── TOP NAVIGATION ───────────────────────────
nav_pages = ["Score", "Dashboard", "Tracker", "Lend/Borrow",
             "Learn", "Community", "Insights", "Me"]

avatar_letter = un[0].upper()
st.markdown(f"""
<div class="topnav">
  <div class="nav-logo">FIN<span>VERSE</span></div>
  <div style="display:flex;align-items:center;gap:6px;overflow-x:auto;">
    {"".join(
        f'<span class="nav-btn {"active" if st.session_state.active_tab == p else ""}" '
        f'onclick="void(0)">{p}</span>'
        for p in nav_pages
    )}
  </div>
  <div class="nav-user">
    <div class="nav-avatar">{avatar_letter}</div>
    <span style="font-size:12px;color:#64748b;font-weight:600;">{un}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Use actual Streamlit tabs (horizontal navigation)
tabs = st.tabs(nav_pages)
(t_score, t_dash, t_track, t_lend,
 t_learn, t_comm, t_insights, t_me) = tabs


# ════════════════════════════════════════════
# SCORE TAB
# ════════════════════════════════════════════
with t_score:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Enter Your Monthly Numbers")
    st.markdown(
        "<p style='font-size:13px;color:#334155;margin:0 0 16px 0;'>"
        "Be honest — the more accurate your numbers, the more useful your score.</p>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        income  = st.number_input(
            persona["income_label"], min_value=0.0, value=50000.0, step=1000.0, key="s_inc",
            help="Your take-home pay after taxes and deductions.",
        )
        savings = st.number_input(
            "Total savings (₹)", min_value=0.0, value=120000.0, step=5000.0, key="s_sav",
            help="All liquid savings — bank accounts, FDs, emergency fund.",
        )
    with c2:
        expenses = st.number_input(
            "Total monthly expenses (₹)", min_value=0.0, value=35000.0, step=1000.0, key="s_exp",
            help="Everything you spend: rent, food, transport, EMIs, subscriptions.",
        )
        st.markdown(
            "<div style='background:#07080f;border:1px solid #12182b;border-radius:8px;"
            "padding:12px 14px;margin-top:6px;font-size:12px;color:#334155;line-height:1.7;'>"
            "<strong style='color:#22c55e;'>Tip:</strong> Include all monthly costs — "
            "rent, groceries, fuel, EMIs, OTT, eating out. Underestimating expenses = "
            "overestimating safety.</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("CALCULATE MY SAFETY SCORE", key="s_calc"):
        if income <= 0:
            st.error("Please enter your monthly income to continue.")
            st.stop()

        result = analyse_finances(income, expenses, savings)
        lv     = get_level(result["composite_score"])
        next_l = get_next_level(result["composite_score"])
        bdgs   = get_badges(result)
        score  = result["composite_score"]
        risk   = result["risk_level"]
        stress = calculate_stress_score(income, expenses, savings, result)

        save_score(un, st.session_state.persona_name, income, expenses, savings, result, stress)
        upsert_leaderboard(un, score, lv["name"], st.session_state.persona_name)
        st.session_state.update({
            "last_result": result, "last_income": income,
            "last_expenses": expenses, "last_savings": savings,
        })

        # Main score card
        st.markdown('<div class="card-grad">', unsafe_allow_html=True)
        rc1, rc2 = st.columns([1, 2])
        with rc1:
            st.markdown(ring(score, 150), unsafe_allow_html=True)
        with rc2:
            nh = (f"<div style='font-size:11px;color:#1e3a5f;margin-top:8px;'>"
                  f"{next_l['points_needed']} more points → {next_l['name']} level</div>"
                  if next_l else
                  "<div style='font-size:11px;color:#22c55e;margin-top:8px;'>Maximum level reached</div>")
            st.markdown(
                f"<div style='padding:8px 0;'>{level_tag(lv['name'])}"
                f"<div style='font-size:26px;font-weight:800;color:#f1f5f9;"
                f"margin:10px 0 6px 0;line-height:1.2;letter-spacing:-0.3px;'>{lv['message']}</div>"
                f"{risk_tag(risk)}"
                f"<div style='font-size:13px;color:#475569;margin-top:8px;line-height:1.6;'>{get_risk_advice(risk)}</div>"
                f"{nh}</div>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Two cards side by side
        col_a, col_b = st.columns(2)

        with col_a:
            s_label, s_color = get_stress_label(stress)
            stress_tips = {
                "High Stress": "Your financial buffers are critically thin. Reducing expenses is priority one.",
                "Moderate Stress": "Some pressure exists. Building savings will bring this down.",
                "Low Stress": "You are in a stable position. Keep improving.",
                "Minimal Stress": "Strong buffers. Healthy cash flow. Excellent.",
            }
            st.markdown(
                f"<div class='card'>"
                f"<span class='lbl'>Stress Score</span>"
                f"<div style='display:flex;align-items:center;gap:16px;'>"
                f"<div style='font-family:Space Mono,monospace;font-size:44px;font-weight:700;"
                f"color:{s_color};line-height:1;'>{stress}</div>"
                f"<div><div style='font-size:14px;font-weight:700;color:{s_color};'>{s_label}</div>"
                f"<div style='font-size:12px;color:#334155;margin-top:4px;line-height:1.5;'>"
                f"{stress_tips.get(s_label,'')}</div>"
                f"<div style='font-size:10px;color:#1e3a5f;margin-top:4px;'>0 = no stress · 100 = severe</div>"
                f"</div></div>{bar(stress, s_color)}</div>",
                unsafe_allow_html=True,
            )

        with col_b:
            surplus = income - expenses
            sr = result["savings_rate"]; sm = result["survival_months"]; er = result["expense_ratio"]
            sc = "#22c55e" if sr >= 20 else ("#f59e0b" if sr >= 10 else "#f87171")
            smc = "#22c55e" if sm >= 6 else ("#f59e0b" if sm >= 3 else "#f87171")
            erc = "#22c55e" if er <= 60 else ("#f59e0b" if er <= 80 else "#f87171")
            st.markdown(
                f"<div class='card'><span class='lbl'>Key Metrics</span>"
                f"<div class='sg'>"
                f"<div class='sb'><div class='sv' style='color:{sc};'>{sr:.1f}%</div>"
                f"<div class='sk'>Savings Rate</div><div class='sn'>{get_savings_rate_message(sr)}</div></div>"
                f"<div class='sb'><div class='sv' style='color:{smc};'>{format_months(sm)}</div>"
                f"<div class='sk'>Survival Time</div><div class='sn'>Without income</div></div>"
                f"<div class='sb'><div class='sv' style='color:{erc};'>{er:.1f}%</div>"
                f"<div class='sk'>Expense Ratio</div><div class='sn'>Of income spent</div></div>"
                f"</div>{bar(min(100,int(sr/30*100)),sc)}{bar(min(100,int(sm/12*100)),smc)}</div>",
                unsafe_allow_html=True,
            )

        # Monthly summary
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Monthly Picture")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Income",   format_currency(income))
        m2.metric("Expenses", format_currency(expenses))
        m3.metric("Surplus" if surplus >= 0 else "Deficit", format_currency(abs(surplus)),
                  delta_color="normal" if surplus >= 0 else "inverse")
        m4.metric("Safety Score", f"{score:.0f} / 100")
        st.markdown('</div>', unsafe_allow_html=True)

        # Badges
        if bdgs:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            lbl("Achievements Unlocked")
            st.markdown(
                "".join(
                    f'<span style="display:inline-block;background:#07080f;border:1px solid #12182b;'
                    f'border-radius:6px;padding:5px 12px;font-size:11px;font-weight:700;'
                    f'color:#475569;margin:3px;letter-spacing:0.04em;">'
                    f'{b["name"].split(" ",1)[-1]}</span>'
                    for b in bdgs
                ),
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # What to do next
        suggs = generate_suggestions(income, expenses, savings, result)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Your Next 3 Actions")
        st.markdown(
            "<p style='font-size:13px;color:#334155;margin:0 0 14px 0;'>Based on your numbers — ranked by impact.</p>",
            unsafe_allow_html=True,
        )
        for s in sorted(suggs, key=lambda x: {"High":0,"Medium":1,"Low":2}.get(x["impact"],3))[:3]:
            cls  = {"High":"sug-h","Medium":"sug-m","Low":"sug-l"}[s["impact"]]
            icls = {"High":"i-h","Medium":"i-m","Low":"i-l"}[s["impact"]]
            st.markdown(
                f'<div class="sug {cls}"><div class="stit">{s["title"]}'
                f'<span class="imp {icls}">{s["impact"]}</span></div>'
                f'<div class="sbod">{s["detail"]}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # What-If inline
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Quick What-If")
        st.markdown(
            "<p style='font-size:12px;color:#334155;margin:0 0 12px 0;'>"
            "Drag to see how changes affect your score instantly.</p>",
            unsafe_allow_html=True,
        )
        wi1, wi2 = st.columns(2)
        with wi1:
            id_ = st.slider("Income change (₹/mo)", -20000, 50000, 0, 1000, key="wi_inc")
        with wi2:
            ed_ = st.slider("Expense change (₹/mo)", -20000, 20000, 0, 500, key="wi_exp")

        nr   = calculate_whatif(income, expenses, savings, {"income_delta": id_, "expenses_delta": ed_, "savings_delta": 0})
        diff = nr["composite_score"] - score
        dc   = "#22c55e" if diff >= 0 else "#f87171"
        arrow = "+" if diff >= 0 else ""
        wc1, wc2, wc3 = st.columns(3)
        wc1.metric("New Score",   f"{nr['composite_score']:.1f}")
        wc2.metric("Change",      f"{arrow}{diff:.1f} pts",
                   delta_color="normal" if diff >= 0 else "inverse")
        wc3.metric("New Status",  nr["risk_level"].capitalize())
        st.markdown('</div>', unsafe_allow_html=True)

        # Challenges
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Active Challenges")
        for ch in get_challenges():
            done = ch["id"] in st.session_state.get("challenges_done", set())
            ca, cb = st.columns([5, 1])
            with ca:
                op = "opacity:0.3;" if done else ""
                td = "text-decoration:line-through;" if done else ""
                st.markdown(
                    f"<div style='{op}background:#07080f;border:1px solid #12182b;"
                    f"border-radius:8px;padding:10px 14px;margin-bottom:5px;'>"
                    f"<div style='font-size:13px;color:#f1f5f9;font-weight:600;{td}'>{ch['name']}</div>"
                    f"<div style='font-size:11px;color:#1e3a5f;margin-top:2px;'>"
                    f"{ch['desc']} · +{ch['reward_xp']} XP</div></div>",
                    unsafe_allow_html=True,
                )
            with cb:
                if not done:
                    if st.button("Done", key=f"ch_{ch['id']}"):
                        save_challenge(un, ch["id"])
                        st.session_state.challenges_done.add(ch["id"])
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Score history
        history = get_score_history(un, 6)
        if len(history) > 1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            lbl("Score History")
            for h in history:
                col = "#22c55e" if h["risk_level"] == "SAFE" else ("#f59e0b" if h["risk_level"] == "MODERATE" else "#f87171")
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:8px 0;border-bottom:1px solid #12182b;'>"
                    f"<span style='font-family:Space Mono,monospace;font-size:11px;color:#1e3a5f;'>{h['created_at'][:10]}</span>"
                    f"<span style='font-size:11px;color:#334155;'>{h['persona']}</span>"
                    f"<span style='font-family:Space Mono,monospace;font-size:16px;color:{col};font-weight:700;'>{h['score']:.1f}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div class="card" style="text-align:center;padding:56px 28px;">
          <div style="font-family:'Space Mono',monospace;font-size:60px;color:#12182b;
                      font-weight:700;letter-spacing:-3px;line-height:1;">--</div>
          <div style="font-size:18px;font-weight:700;color:#1e3a5f;margin-top:16px;">
              Enter your numbers above to get your score
          </div>
          <div style="font-size:13px;color:#12182b;margin-top:6px;line-height:1.7;">
              Safety score · Stress score · Key metrics · Action plan · What-If simulator
          </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# DASHBOARD TAB
# ════════════════════════════════════════════
with t_dash:
    score_hist  = get_score_history(un, 30)
    spend_trend = get_spending_trend(un, 30)
    monthly_exp = get_monthly_expenses(un)
    p_stats     = get_platform_stats()

    # Platform stats
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Platform Stats — All Users")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Total Users",     p_stats["total_users"])
    d2.metric("Avg Safety Score", f"{p_stats['avg_score']:.1f}")
    d3.metric("Safe Users",      p_stats["safe_count"])
    d4.metric("High Risk Users", p_stats["risky_count"])
    st.markdown('</div>', unsafe_allow_html=True)

    if PLOTLY:
        row1, row2 = st.columns(2), st.columns(2)

        # Score trend
        if score_hist and len(score_hist) > 1:
            d = build_score_trend_data(score_hist)
            with row1[0]:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                lbl("Your Safety Score — Over Time")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=d["dates"], y=d["scores"], mode="lines+markers",
                    line={"color":"#22c55e","width":2.5}, marker={"color":"#22c55e","size":7},
                    fill="tozeroy", fillcolor="rgba(34,197,94,0.06)"))
                fig.add_hline(y=65, line_dash="dot", line_color="#1e3a5f",
                              annotation_text="Safe zone", annotation_font_color="#1e3a5f")
                fig.update_layout(**plotly_cfg(), height=240)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

        # Spending trend
        if spend_trend:
            with row1[1]:
                d2_ = build_expense_trend_data(spend_trend)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                lbl("Daily Spending — Last 30 Days")
                fig2 = go.Figure(go.Bar(x=d2_["dates"], y=d2_["amounts"],
                    marker_color="#22c55e", opacity=0.75))
                fig2.update_layout(**plotly_cfg(), height=240)
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

        # Category pie
        if monthly_exp:
            with row2[0]:
                da = build_category_data(monthly_exp)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                lbl("Spending by Category — This Month")
                fig3 = go.Figure(go.Pie(labels=da["categories"], values=da["totals"], hole=0.55,
                    marker={"colors": ["#22c55e","#3b82f6","#f59e0b","#f87171","#8b5cf6","#ec4899","#14b8a6","#f97316"]},
                    textfont={"color":"#64748b","size":10}))
                fig3.update_layout(**plotly_cfg(), height=260, showlegend=True,
                                   legend={"font": {"color":"#475569","size":10}})
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

        # Savings projection
        if st.session_state.last_result:
            surplus_ = st.session_state.last_income - st.session_state.last_expenses
            if surplus_ > 0:
                with row2[1]:
                    dp = build_prediction_data(st.session_state.last_savings, surplus_)
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    lbl("12-Month Savings Projection")
                    fig4 = go.Figure(go.Scatter(x=dp["months"], y=dp["savings"],
                        mode="lines+markers", line={"color":"#3b82f6","width":2,"dash":"dot"},
                        marker={"color":"#3b82f6","size":6},
                        fill="tozeroy", fillcolor="rgba(59,130,246,0.05)"))
                    fig4.update_layout(**plotly_cfg(), height=260)
                    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Install plotly for charts: pip install plotly")

    if not score_hist and not spend_trend:
        st.markdown(
            "<div class='card' style='text-align:center;padding:44px;color:#1e3a5f;'>"
            "Calculate your score and log expenses to populate your dashboard.</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# TRACKER TAB
# ════════════════════════════════════════════
with t_track:
    s_cfg = get_user_settings(un)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Daily Expense Tracker")
    h1, h2, h3 = st.columns(3)
    h1.metric("Tracking Streak",  f"{s_cfg['streak']} days",
              help="Increases every day you log expenses and tap End Day.")
    h2.metric("Today's Budget",   format_currency(s_cfg["daily_budget"]))
    with h3:
        nb = st.number_input("Update daily budget (₹)", min_value=0.0,
                             value=float(s_cfg["daily_budget"]), step=100.0)
        if nb != s_cfg["daily_budget"]:
            save_user_settings(un, nb, s_cfg["streak"], s_cfg["last_tracked"])
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Add expense form
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Add an Expense")
    tc1, tc2, tc3, tc4 = st.columns([2, 2, 2, 3])
    with tc1:
        cat = st.selectbox("Category", ["Food & Dining", "Transport", "Shopping", "Bills & Utilities",
                                         "Entertainment", "Health & Medical", "Education",
                                         "Personal Care", "Investment", "Other"])
    with tc2:
        amt = st.number_input("Amount (₹)", min_value=0.0, value=0.0, step=10.0)
    with tc3:
        exp_date = st.date_input("Date", value=date.today())
    with tc4:
        note = st.text_input("Note (optional)", placeholder="e.g. Lunch at office")
    if st.button("ADD EXPENSE", key="add_exp"):
        if amt > 0:
            save_expense(un, cat, float(amt), note, str(exp_date))
            st.success(f"Added: {cat}  —  {format_currency(amt)}")
            st.rerun()
        else:
            st.warning("Please enter an amount greater than ₹0.")
    st.markdown('</div>', unsafe_allow_html=True)

    today_exps = get_today_expenses(un)
    budget     = s_cfg["daily_budget"]

    if today_exps:
        total = sum(e["amount"] for e in today_exps)
        left  = budget - total
        pct   = min(100, int(total / budget * 100)) if budget > 0 else 100
        bc    = "#22c55e" if pct < 70 else ("#f59e0b" if pct < 90 else "#f87171")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Today's Summary")
        d1, d2, d3 = st.columns(3)
        d1.metric("Spent Today",   format_currency(total))
        d2.metric("Daily Budget",  format_currency(budget))
        d3.metric("Remaining" if left >= 0 else "Over Budget", format_currency(abs(left)),
                  delta_color="normal" if left >= 0 else "inverse")
        st.markdown(
            f"<div style='font-size:11px;color:#1e3a5f;margin-bottom:4px;'>Budget used: {pct}%</div>",
            unsafe_allow_html=True,
        )
        st.markdown(bar(pct, bc), unsafe_allow_html=True)
        if pct >= 90:   st.error("You are at 90%+ of your daily budget.")
        elif pct >= 70: st.warning("More than two-thirds of today's budget used.")
        else:           st.success("Spending is on track today.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Expense Log — tap Delete to remove any entry")
        for exp in reversed(today_exps):
            ec1, ec2, ec3, ec4, ec5 = st.columns([2, 3, 1, 2, 1])
            with ec1:
                st.markdown(f"<span style='font-size:11px;color:#334155;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;'>{exp['category']}</span>", unsafe_allow_html=True)
            with ec2:
                st.markdown(f"<span style='font-size:12px;color:#475569;'>{exp['note'] or '—'}</span>", unsafe_allow_html=True)
            with ec3:
                st.markdown(f"<span style='font-family:Space Mono,monospace;font-size:10px;color:#1e3a5f;'>{exp['created_at'][11:16]}</span>", unsafe_allow_html=True)
            with ec4:
                st.markdown(f"<span style='font-family:Space Mono,monospace;font-size:14px;color:#f1f5f9;font-weight:700;'>{format_currency(exp['amount'])}</span>", unsafe_allow_html=True)
            with ec5:
                if st.button("Del", key=f"del_{exp['id']}"):
                    delete_expense(exp["id"])
                    st.rerun()
        st.markdown("<hr style='border-color:#12182b;margin:14px 0;'>", unsafe_allow_html=True)
        if st.button("END DAY — SAVE STREAK", use_container_width=True):
            new_streak = end_day_update_streak(un)
            st.success(f"Day saved! Streak is now {new_streak} days.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        monthly = get_monthly_expenses(un)
        if monthly:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            lbl("This Month — Total Spending by Category")
            mt = sum(r["total"] for r in monthly)
            for row in monthly:
                p_ = int(row["total"] / mt * 100) if mt > 0 else 0
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;'>"
                    f"<span style='color:#475569;'>{row['category']}"
                    f"<span style='color:#1e3a5f;margin-left:5px;font-size:10px;'>({row['count']} entries)</span></span>"
                    f"<span style='font-family:Space Mono,monospace;color:#f1f5f9;font-weight:700;'>{format_currency(row['total'])}</span></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(bar(p_, "#1e3a5f"), unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-family:Space Mono,monospace;font-size:15px;color:#22c55e;"
                f"margin-top:10px;border-top:1px solid #12182b;padding-top:10px;font-weight:700;'>"
                f"Month Total: {format_currency(mt)}</div>",
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='card' style='text-align:center;padding:40px;color:#1e3a5f;'>"
            "No expenses logged today. Add one above to start your streak.</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# LEND / BORROW TAB
# ════════════════════════════════════════════
with t_lend:
    summary = get_lend_borrow_summary(un)
    net     = summary["net"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Lend / Borrow Tracker")
    st.markdown(
        "<p style='font-size:13px;color:#334155;margin:0 0 14px 0;'>"
        "Track money you've given and money you owe. Never lose track again.</p>",
        unsafe_allow_html=True,
    )
    ls1, ls2, ls3 = st.columns(3)
    ls1.metric("Others Owe You",   format_currency(summary["total_gave"]))
    ls2.metric("You Owe Others",   format_currency(summary["total_owe"]))
    ls3.metric("Net Position",     format_currency(abs(net)),
               "in your favour" if net >= 0 else "you owe net",
               delta_color="normal" if net >= 0 else "inverse")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Add a Transaction")
    la1, la2, la3 = st.columns([2, 2, 2])
    with la1:
        party    = st.text_input("Person's name", placeholder="e.g. Rahul")
    with la2:
        l_amt    = st.number_input("Amount (₹)", min_value=0.0, value=0.0, step=100.0, key="l_amt")
    with la3:
        txn_type = st.selectbox("Type", ["I gave money (they owe me)", "I borrowed money (I owe them)"])
    lb1c, lb2c = st.columns(2)
    with lb1c:
        desc     = st.text_input("What for?", placeholder="e.g. Dinner, travel, emergency")
    with lb2c:
        due_date = st.date_input("Due date (optional)", value=None, key="lb_due")

    if st.button("ADD TRANSACTION", key="add_lb"):
        if party.strip() and l_amt > 0:
            t  = "gave" if "gave" in txn_type else "owe"
            dd = str(due_date) if due_date else None
            add_lend_borrow(un, party.strip(), float(l_amt), t, desc, dd)
            st.success(f"Recorded. {format_currency(l_amt)} {'given to' if t == 'gave' else 'borrowed from'} {party}.")
            st.rerun()
        else:
            st.warning("Enter a name and an amount greater than ₹0.")
    st.markdown('</div>', unsafe_allow_html=True)

    all_txns = get_lend_borrow(un)
    pending  = [t for t in all_txns if t["status"] == "pending"]
    settled  = [t for t in all_txns if t["status"] == "settled"]

    if pending:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl(f"Pending Transactions ({len(pending)})")
        for txn in pending:
            is_gave = txn["txn_type"] == "gave"
            color   = "#22c55e" if is_gave else "#f87171"
            label   = "They owe you" if is_gave else "You owe them"
            due_str = f"  ·  Due: {txn['due_date']}" if txn.get("due_date") else ""

            t1, t2, t3, t4, t5 = st.columns([2, 2, 2, 1, 1])
            with t1:
                st.markdown(
                    f"<div style='font-size:14px;color:#f1f5f9;font-weight:700;'>{txn['party_name']}</div>"
                    f"<div style='font-size:11px;color:#334155;'>{txn.get('description','') or '—'}{due_str}</div>",
                    unsafe_allow_html=True,
                )
            with t2:
                st.markdown(
                    f"<span style='font-family:Space Mono,monospace;font-size:16px;"
                    f"color:{color};font-weight:700;'>{format_currency(txn['amount'])}</span>",
                    unsafe_allow_html=True,
                )
            with t3:
                st.markdown(f"<span style='font-size:12px;color:#475569;'>{label}</span>", unsafe_allow_html=True)
            with t4:
                if st.button("Settle", key=f"set_{txn['id']}"):
                    settle_lend_borrow(txn["id"])
                    st.rerun()
            with t5:
                if st.button("Delete", key=f"dlt_{txn['id']}"):
                    delete_lend_borrow(txn["id"])
                    st.rerun()

            with st.expander(f"Send reminder to {txn['party_name']}"):
                if is_gave:
                    msg = (f"Hi {txn['party_name']}, friendly reminder that you owe me "
                           f"{format_currency(txn['amount'])}"
                           f"{' (due ' + txn['due_date'] + ')' if txn.get('due_date') else ''}. "
                           f"{'For: ' + txn['description'] + '. ' if txn.get('description') else ''}"
                           f"Please pay when you can. Thanks!")
                else:
                    msg = (f"Reminder to self: I owe {txn['party_name']} "
                           f"{format_currency(txn['amount'])}"
                           f"{' by ' + txn['due_date'] if txn.get('due_date') else ''}. "
                           f"{'For: ' + txn['description'] + '.' if txn.get('description') else ''}")
                st.code(msg, language=None)
                st.caption("Copy and send on WhatsApp.")
        st.markdown('</div>', unsafe_allow_html=True)

    if settled:
        with st.expander(f"View {len(settled)} settled transactions"):
            for txn in settled:
                color = "#22c55e" if txn["txn_type"] == "gave" else "#f87171"
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;padding:7px 0;"
                    f"border-bottom:1px solid #12182b;'>"
                    f"<span style='font-size:12px;color:#334155;'>{txn['party_name']} — {txn.get('description','') or '—'}</span>"
                    f"<span style='font-family:Space Mono,monospace;font-size:13px;color:{color};"
                    f"text-decoration:line-through;'>{format_currency(txn['amount'])}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    if not all_txns:
        st.markdown(
            "<div class='card' style='text-align:center;padding:40px;color:#1e3a5f;'>"
            "No transactions yet. Add one above to start tracking.</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# LEARN TAB
# ════════════════════════════════════════════
with t_learn:
    progress = get_education_progress(un)
    done_ids = {mid for mid, done in progress.items() if done}
    total_m  = max(len(LEARNING_MODULES), 1)
    done_ct  = len(done_ids)
    level_colors = {"Beginner": "#22c55e", "Intermediate": "#f59e0b", "Advanced": "#f87171"}

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Financial Education — Beginner to Advanced")
    lp1, lp2, lp3 = st.columns(3)
    lp1.metric("Modules Completed", f"{done_ct} / {total_m}")
    lp2.metric("XP from Learning",  f"{done_ct * 20}")
    lp3.metric("Progress",          f"{int(done_ct / total_m * 100)}%")
    st.markdown(bar(int(done_ct / total_m * 100), "#22c55e"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    modules_by_level = get_modules_by_level()
    for level_name, modules in modules_by_level.items():
        lc = level_colors.get(level_name, "#22c55e")
        st.markdown(
            f"<div style='font-size:16px;font-weight:800;color:{lc};"
            f"margin:22px 0 12px 0;'>{level_name}</div>",
            unsafe_allow_html=True,
        )
        for mod in modules:
            is_done = mod["id"] in done_ids
            status  = "  ✓" if is_done else f"  ·  {mod.get('duration','5 min')}  ·  +{mod.get('xp',20)} XP"
            with st.expander(f"{mod['title']}{status}"):
                st.markdown(
                    f"<div style='font-size:13px;color:#64748b;line-height:1.85;"
                    f"white-space:pre-line;'>{mod['content'].strip()}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='background:#021a0b;border:1px solid #14532d;border-radius:8px;"
                    f"padding:12px 16px;margin-top:12px;'>"
                    f"<div style='font-size:9px;color:#1e3a5f;text-transform:uppercase;"
                    f"letter-spacing:0.14em;margin-bottom:5px;'>Key Takeaway</div>"
                    f"<div style='font-size:13px;color:#22c55e;font-weight:600;line-height:1.5;'>"
                    f"{mod['key_takeaway']}</div></div>",
                    unsafe_allow_html=True,
                )
                book_title  = mod.get("book_title","")
                book_author = mod.get("book_author","")
                free_link   = mod.get("free_link","https://openlibrary.org")
                if book_title:
                    st.markdown(
                        f"<div style='margin-top:10px;font-size:12px;color:#334155;'>"
                        f"Recommended: <strong style='color:#94a3b8;'>{book_title}</strong> by {book_author}"
                        f"  ·  <a href='{free_link}' target='_blank' style='color:#1e3a5f;"
                        f"text-decoration:none;'>Find free →</a></div>",
                        unsafe_allow_html=True,
                    )
                if not is_done:
                    if st.button(f"Mark complete  +{mod.get('xp',20)} XP", key=f"mod_{mod['id']}"):
                        mark_module_complete(un, mod["id"])
                        st.success("Module complete!")
                        st.rerun()

    # Book list
    if BOOK_LIST:
        st.markdown(
            "<div style='font-size:18px;font-weight:800;color:#f1f5f9;margin:28px 0 14px 0;'>Reading List</div>",
            unsafe_allow_html=True,
        )
        for book in BOOK_LIST:
            lc = level_colors.get(book.get("level","Beginner"), "#22c55e")
            buy_link  = book.get("buy_link",  "https://www.amazon.in")
            free_link = book.get("free_link", "https://openlibrary.org")
            st.markdown(
                f"<div class='book'>"
                f"<div style='display:flex;justify-content:space-between;align-items:flex-start;gap:10px;'>"
                f"<div style='font-size:14px;font-weight:700;color:#f1f5f9;'>{book['title']}</div>"
                f"<span style='font-size:9px;color:{lc};text-transform:uppercase;letter-spacing:0.1em;"
                f"font-weight:700;white-space:nowrap;'>{book.get('level','')}</span></div>"
                f"<div style='font-size:11px;color:#334155;margin:2px 0 6px;'>by {book['author']}</div>"
                f"<div style='font-size:12px;color:#475569;line-height:1.6;'>{book.get('why','')}</div>"
                f"<div style='margin-top:8px;display:flex;gap:12px;'>"
                f"<a href='{buy_link}' target='_blank' style='font-size:11px;color:#22c55e;"
                f"text-decoration:none;font-weight:700;'>Buy on Amazon →</a>"
                f"<a href='{free_link}' target='_blank' style='font-size:11px;color:#475569;"
                f"text-decoration:none;'>Find free version →</a>"
                f"</div></div>",
                unsafe_allow_html=True,
            )

    # Free resources
    if FREE_RESOURCES:
        st.markdown(
            "<div style='font-size:16px;font-weight:800;color:#f1f5f9;margin:24px 0 12px 0;'>Free Online Resources</div>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for res in FREE_RESOURCES:
            st.markdown(
                f"<div style='padding:10px 0;border-bottom:1px solid #12182b;'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<div style='font-size:13px;color:#94a3b8;font-weight:700;'>{res['name']}</div>"
                f"<a href='{res['url']}' target='_blank' style='font-size:11px;color:#22c55e;"
                f"text-decoration:none;font-weight:700;white-space:nowrap;'>Visit →</a></div>"
                f"<div style='font-size:11px;color:#334155;margin-top:3px;'>{res['desc']}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# COMMUNITY TAB
# ════════════════════════════════════════════
with t_comm:
    TOPICS = ["All", "Saving Tips", "Investing", "Debt & EMIs",
              "Career & Income", "Students", "Budgeting", "General Finance"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Community Discussions")
    st.markdown(
        "<p style='font-size:13px;color:#334155;margin:0 0 14px 0;'>"
        "Ask questions. Share tips. Help others. Finance topics only. Be respectful.</p>",
        unsafe_allow_html=True,
    )
    topic_filter = st.selectbox("Filter by topic", TOPICS)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Write a New Post"):
        np_topic = st.selectbox("Topic", TOPICS[1:], key="np_topic")
        np_text  = st.text_area("Your post", placeholder="Share a tip, ask a question, describe a situation...", height=100)
        np_anon  = st.checkbox("Post anonymously — your username won't be shown")
        if st.button("PUBLISH", key="post_btn"):
            if len(np_text.strip()) >= 20:
                add_post(un, un, np_topic, np_text.strip(), np_anon)
                st.success("Post published.")
                st.rerun()
            else:
                st.warning("Write at least 20 characters.")

    posts = get_posts(topic_filter if topic_filter != "All" else None, 30)
    if posts:
        for post in posts:
            is_mine = post["username"] == un
            st.markdown(
                f'<div class="post">'
                f'<span class="ptag">{post["topic"]}</span>'
                f'<div class="paut">{post["display_name"]}  ·  {post["created_at"][:10]}</div>'
                f'<div class="ptxt">{post["content"]}</div>'
                f'<div class="pft">{post["upvotes"]} upvotes</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            ub1, ub2 = st.columns([1, 8])
            with ub1:
                if st.button("Upvote", key=f"up_{post['id']}"):
                    upvote_post(un, post["id"])
                    st.rerun()
            if is_mine:
                with ub2:
                    if st.button("Delete my post", key=f"dp_{post['id']}"):
                        delete_post(post["id"], un)
                        st.rerun()
    else:
        st.markdown(
            "<div class='card' style='text-align:center;padding:36px;color:#1e3a5f;'>"
            "No posts here yet. Be the first to write something.</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# INSIGHTS TAB
# ════════════════════════════════════════════
with t_insights:
    score_hist  = get_score_history(un, 30)
    monthly_exp = get_monthly_expenses(un)
    insights    = get_behavioral_insights(score_hist, monthly_exp)

    # Behavioral insights
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Behavioral Insights — What Your Data Says")
    for insight in insights:
        st.markdown(
            f"<div style='padding:12px 16px;border-left:3px solid #22c55e;background:#021a0b;"
            f"border-radius:0 8px 8px 0;margin-bottom:8px;font-size:13px;color:#94a3b8;line-height:1.7;'>"
            f"{insight}</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Predictions
    if st.session_state.last_result:
        surplus_    = st.session_state.last_income - st.session_state.last_expenses
        current_sav = st.session_state.last_savings
        monthly_e   = st.session_state.last_expenses
        annual_e    = monthly_e * 12
        ef_months   = predict_emergency_fund_date(current_sav, surplus_, monthly_e, 6)
        fire_yrs    = predict_fire_date(current_sav, surplus_, annual_e)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Predictions — How Long to Reach Your Targets")
        pr1, pr2 = st.columns(2)
        with pr1:
            if ef_months == 0:
                st.markdown("<div class='card-green'><span class='lbl'>6-Month Emergency Fund</span><div style='font-family:Space Mono,monospace;font-size:26px;color:#22c55e;font-weight:700;'>Achieved</div><div style='font-size:11px;color:#334155;margin-top:4px;'>You have already hit this target.</div></div>", unsafe_allow_html=True)
            elif ef_months:
                st.markdown(f"<div class='card'><span class='lbl'>6-Month Emergency Fund</span><div style='font-family:Space Mono,monospace;font-size:26px;color:#f59e0b;font-weight:700;'>{ef_months} months</div><div style='font-size:11px;color:#334155;margin-top:4px;'>At current savings rate, without investment returns.</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-red'><span class='lbl'>6-Month Emergency Fund</span><div style='font-size:13px;color:#f87171;'>Cannot reach at current rate.</div><div style='font-size:11px;color:#334155;margin-top:4px;'>Create a monthly surplus first.</div></div>", unsafe_allow_html=True)
        with pr2:
            if fire_yrs == 0:
                st.markdown("<div class='card-green'><span class='lbl'>FIRE Number (Financial Independence)</span><div style='font-family:Space Mono,monospace;font-size:26px;color:#22c55e;font-weight:700;'>Achieved</div><div style='font-size:11px;color:#334155;margin-top:4px;'>Financial independence reached.</div></div>", unsafe_allow_html=True)
            elif fire_yrs:
                st.markdown(f"<div class='card'><span class='lbl'>FIRE Number (Financial Independence)</span><div style='font-family:Space Mono,monospace;font-size:26px;color:#3b82f6;font-weight:700;'>{fire_yrs} years</div><div style='font-size:11px;color:#334155;margin-top:4px;'>Without investment growth — actual timeline will be shorter.</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-red'><span class='lbl'>FIRE Number</span><div style='font-size:13px;color:#f87171;'>Cannot calculate.</div><div style='font-size:11px;color:#334155;margin-top:4px;'>Need a positive monthly surplus.</div></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Leaderboard
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Global Safety Leaderboard")
    lb_data = get_leaderboard(20)
    if lb_data:
        for i, e in enumerate(lb_data):
            is_me  = e["username"] == un
            bg     = "#021a0b" if is_me else "#0d1117"
            border = "1px solid #14532d" if is_me else "1px solid #12182b"
            rank   = f"0{i+1}" if i + 1 < 10 else str(i + 1)
            st.markdown(
                f"<div class='lbr' style='background:{bg};border:{border};'>"
                f"<span class='lrk'>{rank}</span>"
                f"<span class='lnm' style='{'color:#22c55e;font-weight:700;' if is_me else ''}'>"
                f"{e['username']}{'  (you)' if is_me else ''}</span>"
                f"<span class='llv'>{e['level_name']}</span>"
                f"<span class='llv'>{e['persona']}</span>"
                f"<span class='lsc'>{e['score']:.1f}</span></div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown("<p style='font-size:12px;color:#1e3a5f;'>No scores yet. Calculate yours in the Score tab.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Survey
    SURVEY_Q    = "What is your biggest financial challenge right now?"
    SURVEY_OPTS = [
        "Not saving enough each month",
        "Too much debt or EMIs",
        "No emergency fund",
        "Irregular or uncertain income",
        "Don't know where to invest",
        "Spending more than I earn",
        "No clear financial plan",
    ]
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Community Survey")
    if not has_answered_survey(un, SURVEY_Q):
        st.markdown(
            f"<div style='font-size:14px;color:#94a3b8;font-weight:700;margin-bottom:14px;'>{SURVEY_Q}</div>",
            unsafe_allow_html=True,
        )
        answer = st.radio("Pick your answer", SURVEY_OPTS, label_visibility="collapsed")
        if st.button("SUBMIT", key="survey_btn"):
            save_survey_response(un, SURVEY_Q, answer)
            st.success("Response saved. Thank you.")
            st.rerun()
    else:
        responses  = get_survey_responses(SURVEY_Q)
        total_r    = max(len(responses), 1)
        counts     = {}
        for r in responses:
            counts[r["answer"]] = counts.get(r["answer"], 0) + 1
        st.markdown(
            f"<div style='font-size:13px;color:#94a3b8;font-weight:700;margin-bottom:12px;'>"
            f"Results — {total_r} responses</div>",
            unsafe_allow_html=True,
        )
        for opt in SURVEY_OPTS:
            cnt = counts.get(opt, 0)
            pct = int(cnt / total_r * 100) if total_r > 0 else 0
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;'>"
                f"<span style='color:#64748b;'>{opt}</span>"
                f"<span style='font-family:Space Mono,monospace;color:#94a3b8;'>{pct}% ({cnt})</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown(bar(pct, "#334155"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# ME / PROFILE TAB
# ════════════════════════════════════════════
with t_me:
    score_hist = get_score_history(un, 30)
    done_ids   = {mid for mid, done in get_education_progress(un).items() if done}
    lv_current = get_level(st.session_state.last_result["composite_score"]) if st.session_state.last_result else get_level(0)

    # Profile header
    st.markdown(
        f"<div class='profile-card'>"
        f"<div style='font-family:Space Mono,monospace;font-size:52px;font-weight:700;"
        f"color:#22c55e;line-height:1;margin-bottom:14px;'>{un[0].upper()}</div>"
        f"<div style='font-size:24px;font-weight:800;color:#f1f5f9;margin-bottom:4px;'>{un}</div>"
        f"<div style='font-size:13px;color:#475569;'>"
        f"{PERSONAS[st.session_state.persona_name]['icon']}  {st.session_state.persona_name}"
        f"{'  ·  ' + profile.get('city','') if profile.get('city') else ''}"
        f"{'  ·  Age ' + str(profile.get('age','')) if profile.get('age') else ''}"
        f"</div>"
        f"<div style='display:flex;gap:8px;margin-top:16px;flex-wrap:wrap;'>"
        f"{level_tag(lv_current['name'])}"
        f"<span style='font-size:10px;color:#1e3a5f;background:#07080f;border:1px solid #12182b;"
        f"border-radius:4px;padding:3px 10px;font-weight:700;'>⚡ {xp_total} XP</span>"
        f"<span style='font-size:10px;color:#1e3a5f;background:#07080f;border:1px solid #12182b;"
        f"border-radius:4px;padding:3px 10px;font-weight:700;'>🔥 {settings_['streak']} day streak</span>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    # Stats overview
    me1, me2, me3, me4 = st.columns(4)
    latest_score = score_hist[0]["score"] if score_hist else 0
    me1.metric("Safety Score",     f"{latest_score:.0f} / 100")
    me2.metric("Scores Logged",    len(score_hist))
    me3.metric("Modules Done",     f"{len(done_ids)} / {max(total_m,1)}")
    me4.metric("XP Earned",        f"{xp_total}")

    # Edit profile
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Edit Your Profile")
    ep1, ep2 = st.columns(2)
    with ep1:
        new_name = st.text_input("Display Name", value=un, key="ep_name")
        new_city = st.text_input("City", value=profile.get("city", ""), key="ep_city")
    with ep2:
        new_age     = st.number_input("Age", min_value=16, max_value=80,
                                       value=int(profile.get("age", 25)), step=1)
        new_persona = st.selectbox(
            "Profile Type",
            list(PERSONAS.keys()),
            index=list(PERSONAS.keys()).index(st.session_state.persona_name),
            format_func=lambda x: f"{PERSONAS[x]['icon']}  {x}",
        )
    if st.button("SAVE PROFILE", key="save_profile"):
        upsert_user_profile(un, new_name, new_persona, int(new_age), new_city)
        st.session_state.persona_name = new_persona
        st.success("Profile updated.")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Score history chart
    if score_hist and PLOTLY:
        d_ = build_score_trend_data(score_hist)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Your Score Over Time")
        if len(d_["dates"]) > 1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=d_["dates"], y=d_["scores"], mode="lines+markers",
                line={"color":"#22c55e","width":2.5}, marker={"color":"#22c55e","size":7},
                fill="tozeroy", fillcolor="rgba(34,197,94,0.06)"))
            fig.add_hline(y=65, line_dash="dot", line_color="#334155",
                          annotation_text="Safe zone (65)")
            fig.update_layout(**plotly_cfg(), height=220)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown("<p style='font-size:12px;color:#334155;'>Calculate your score more than once to see the trend.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Challenges
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Challenges")
    challenges = get_challenges()
    comp_ids   = st.session_state.get("challenges_done", set())
    for ch in challenges:
        done = ch["id"] in comp_ids
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;align-items:center;"
            f"padding:10px 0;border-bottom:1px solid #12182b;'>"
            f"<div><div style='font-size:13px;color:{'#334155' if done else '#f1f5f9'};"
            f"font-weight:600;{'text-decoration:line-through;' if done else ''}'>{ch['name']}</div>"
            f"<div style='font-size:11px;color:#1e3a5f;margin-top:2px;'>{ch['desc']}</div></div>"
            f"<div style='font-family:Space Mono,monospace;font-size:12px;"
            f"color:{'#22c55e' if done else '#334155'};font-weight:700;'>"
            f"{'✓' if done else ''} +{ch['reward_xp']} XP</div></div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Partner compatibility (compact)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Quick Partner Compatibility Check")
    st.markdown(
        "<p style='font-size:12px;color:#334155;margin:0 0 12px 0;'>"
        "Enter your partner's numbers for a quick compatibility score.</p>",
        unsafe_allow_html=True,
    )
    pp1, pp2, pp3 = st.columns(3)
    with pp1:
        p2i = st.number_input("Partner Income (₹)",   min_value=0.0, value=45000.0, step=1000.0, key="me_p2i")
    with pp2:
        p2e = st.number_input("Partner Expenses (₹)", min_value=0.0, value=30000.0, step=1000.0, key="me_p2e")
    with pp3:
        p2s = st.number_input("Partner Savings (₹)",  min_value=0.0, value=80000.0, step=5000.0, key="me_p2s")

    if st.session_state.last_result and st.button("CHECK COMPATIBILITY", key="compat_me"):
        r1     = st.session_state.last_result
        r2     = analyse_finances(p2i, p2e, p2s)
        compat = analyse_compatibility(r1, r2)
        cs     = compat["compatibility_score"]
        if   cs >= 75: lbl_t, col_t = "Excellent Match",   "#22c55e"
        elif cs >= 55: lbl_t, col_t = "Good Match",        "#f59e0b"
        elif cs >= 35: lbl_t, col_t = "Needs Alignment",   "#f59e0b"
        else:          lbl_t, col_t = "Significant Gap",   "#f87171"
        st.markdown(
            f"<div style='text-align:center;padding:16px;background:#07080f;border:1px solid #12182b;"
            f"border-radius:10px;margin-top:8px;'>"
            f"<div style='font-family:Space Mono,monospace;font-size:40px;font-weight:700;"
            f"color:{col_t};'>{cs:.0f}</div>"
            f"<div style='font-size:14px;font-weight:700;color:{col_t};margin-top:4px;'>{lbl_t}</div>"
            f"<div style='font-size:11px;color:#334155;margin-top:3px;'>out of 100</div></div>",
            unsafe_allow_html=True,
        )
    elif not st.session_state.last_result:
        st.info("Calculate your score first, then check compatibility here.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Share + sign out
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Share Your Score")
    if st.session_state.last_result:
        sc_  = st.session_state.last_result["composite_score"]
        msg_ = (f"My Financial Safety Score on Finverse: {sc_:.0f}/100\n"
                f"Do you know yours? It's free — [your Finverse link here]")
        st.code(msg_, language=None)
        st.caption("Copy and share on WhatsApp or Instagram.")
    else:
        st.caption("Calculate your score first to get a shareable message.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("SIGN OUT", key="me_signout"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ── FOOTER ───────────────────────────────────
st.markdown(
    "<div style='text-align:center;padding:24px 0 0;border-top:1px solid #12182b;margin-top:12px;'>"
    "<span style='font-size:14px;font-weight:800;color:#12182b;'>FINVERSE</span>"
    "<span style='font-size:11px;color:#12182b;margin-left:14px;'>v8.0</span>"
    "<span style='font-size:11px;color:#12182b;margin-left:14px;'>Built in India</span>"
    "<span style='font-size:11px;color:#12182b;margin-left:14px;'>Not financial advice</span>"
    "</div>",
    unsafe_allow_html=True,
)
