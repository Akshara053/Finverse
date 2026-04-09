# app.py  —  Finverse v7.0
# "India's Financial Safety Platform"
# Run: streamlit run app.py

import streamlit as st
from datetime import datetime, date

from logic        import (analyse_finances, calculate_savings_rules,
                           analyse_compatibility, recommended_partner_income)
from config       import PERSONAS
from gamification import get_level, get_next_level, get_badges, get_challenges, get_total_xp
from suggestions  import generate_suggestions, calculate_whatif
from analytics    import (calculate_stress_score, get_stress_label,
                           predict_savings, predict_emergency_fund_date,
                           predict_fire_date, get_behavioral_insights,
                           build_score_trend_data, build_expense_trend_data,
                           build_category_data, build_prediction_data)
from education    import (LEARNING_MODULES, BOOK_LIST, FREE_RESOURCES,
                           get_modules_by_level, get_module_by_id)
from database     import (
    init_db, upsert_user_profile, get_user_profile, get_platform_stats,
    save_score, get_score_history, get_all_score_history,
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

try:
    import plotly.graph_objects as go
    PLOTLY = True
except ImportError:
    PLOTLY = False

# ─────────────────────────────────────────────
init_db()

st.set_page_config(
    page_title="Finverse — Know If You're Financially Safe",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
# DESIGN SYSTEM
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #060b17; }
.block-container { max-width: 1060px !important; padding: 0 1.5rem 5rem !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] { background: #080e1c !important; border-right: 1px solid #0f1e38 !important; }
[data-testid="stSidebar"] * { color: #94a3b8; }

/* ── UNIVERSAL CARD ── */
.card {
    background: #0a1628;
    border: 1px solid #0f1e38;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 14px;
    transition: border-color 0.2s;
}
.card:hover { border-color: #1a3560; }
.card-flat { background: #060b17; border: 1px solid #0f1e38; border-radius: 14px; padding: 22px 24px; margin-bottom: 14px; }
.card-green { background: #031a0f; border: 1px solid #064e35; border-radius: 14px; padding: 22px 24px; margin-bottom: 14px; }
.card-amber { background: #1a0f00; border: 1px solid #78350f; border-radius: 14px; padding: 22px 24px; margin-bottom: 14px; }
.card-red   { background: #1a0505; border: 1px solid #7f1d1d; border-radius: 14px; padding: 22px 24px; margin-bottom: 14px; }
.card-blue  { background: #030d1a; border: 1px solid #1e3a5f; border-radius: 14px; padding: 22px 24px; margin-bottom: 14px; }

/* ── LABEL ── */
.lbl {
    font-size: 10px; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: #1e3a5f;
    margin: 0 0 14px 0; display: block;
}

/* ── STAT GRID ── */
.sg { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 6px; }
.sb {
    flex: 1; min-width: 120px;
    background: #060b17; border: 1px solid #0f1e38;
    border-radius: 10px; padding: 14px 16px;
}
.sv { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: 500; color: #e2e8f0; line-height: 1.1; letter-spacing: -0.3px; }
.sk { font-size: 10px; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 4px; font-weight: 700; }
.sn { font-size: 11px; color: #1e3a5f; margin-top: 3px; line-height: 1.4; }

/* ── TAGS ── */
.tag { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 3px 10px; border-radius: 4px; }
.r-s { background: #031a0f; color: #10b981; border: 1px solid #064e35; }
.r-m { background: #1a0f00; color: #f59e0b; border: 1px solid #78350f; }
.r-r { background: #1a0505; color: #ef4444; border: 1px solid #7f1d1d; }
.l-pl { background: #0a1f3d; color: #60a5fa; border: 1px solid #1d4ed8; }
.l-go { background: #1a0f00; color: #fbbf24; border: 1px solid #d97706; }
.l-si { background: #0d1a2e; color: #94a3b8; border: 1px solid #334155; }
.l-br { background: #1a0800; color: #fb923c; border: 1px solid #9a3412; }
.l-st { background: #031a0f; color: #34d399; border: 1px solid #065f46; }

/* ── BAR ── */
.bt { background: #0f1e38; border-radius: 2px; height: 4px; margin: 6px 0 14px 0; }
.bf { height: 4px; border-radius: 2px; }

/* ── SUGGESTION ── */
.sug { background: #0a1628; border: 1px solid #0f1e38; border-radius: 10px; padding: 16px 18px; margin-bottom: 8px; }
.sug-h { border-left: 3px solid #ef4444; }
.sug-m { border-left: 3px solid #f59e0b; }
.sug-l { border-left: 3px solid #10b981; }
.stit { font-size: 14px; font-weight: 700; color: #e2e8f0; margin: 0 0 5px 0; }
.sbod { font-size: 12px; color: #334155; margin: 0; line-height: 1.7; }
.imp { display: inline-block; font-size: 9px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 2px 7px; border-radius: 3px; margin-left: 8px; vertical-align: middle; }
.i-h { background: #1a0505; color: #ef4444; }
.i-m { background: #1a0f00; color: #f59e0b; }
.i-l { background: #031a0f; color: #10b981; }

/* ── CMP ── */
.cmp { display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid #0f1e38; }
.cl { font-size:11px; color:#1e3a5f; width:130px; flex-shrink:0; text-transform:uppercase; letter-spacing:0.07em; font-weight:700; }
.co { font-family:'JetBrains Mono',monospace; font-size:13px; color:#1e3a5f; width:75px; }
.ca { font-size:11px; color:#0f1e38; }
.cu { font-family:'JetBrains Mono',monospace; font-size:13px; color:#10b981; font-weight:500; }
.cd { font-family:'JetBrains Mono',monospace; font-size:13px; color:#ef4444; font-weight:500; }
.ce { font-family:'JetBrains Mono',monospace; font-size:13px; color:#475569; font-weight:500; }

/* ── LB ── */
.lbr { display:flex; align-items:center; gap:12px; padding:11px 14px; border-radius:10px; margin-bottom:5px; border:1px solid #0f1e38; background:#0a1628; }
.lrk { font-family:'JetBrains Mono',monospace; font-size:12px; color:#1e3a5f; width:26px; }
.lnm { flex:1; font-size:13px; color:#94a3b8; }
.llv { font-size:10px; color:#1e3a5f; margin-right:8px; text-transform:uppercase; letter-spacing:0.07em; }
.lsc { font-family:'JetBrains Mono',monospace; font-size:17px; color:#10b981; font-weight:500; }

/* ── COMMUNITY POST ── */
.post { background:#0a1628; border:1px solid #0f1e38; border-radius:10px; padding:16px 18px; margin-bottom:10px; }
.ptag { font-size:10px; color:#334155; text-transform:uppercase; letter-spacing:0.1em; font-weight:700; display:inline-block; background:#060b17; border:1px solid #0f1e38; padding:2px 8px; border-radius:3px; margin-bottom:8px; }
.paut { font-size:11px; color:#334155; margin-bottom:6px; }
.ptxt { font-size:13px; color:#64748b; line-height:1.7; }
.pft { font-size:11px; color:#1e3a5f; margin-top:8px; }

/* ── BOOK CARD ── */
.book { background:#0a1628; border:1px solid #0f1e38; border-radius:10px; padding:16px 18px; margin-bottom:8px; }
.btit { font-size:14px; font-weight:700; color:#e2e8f0; margin:0 0 3px 0; }
.baut { font-size:11px; color:#334155; margin-bottom:6px; }
.bwhy { font-size:12px; color:#475569; line-height:1.6; }

/* ── ONBOARDING STEP ── */
.step { background:#0a1628; border:1px solid #0f1e38; border-radius:14px; padding:20px 22px; margin-bottom:10px; cursor:pointer; transition:all 0.2s; }
.step:hover { border-color:#10b981; }
.step-done { border-color:#064e35 !important; background:#031a0f !important; }
.step-num { font-family:'JetBrains Mono',monospace; font-size:11px; color:#1e3a5f; font-weight:700; }
.step-title { font-size:15px; font-weight:700; color:#e2e8f0; margin:4px 0 2px 0; }
.step-desc { font-size:12px; color:#334155; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { background:#080e1c !important; border-bottom:1px solid #0f1e38 !important; gap:0 !important; padding:0 !important; border-radius:0 !important; overflow-x:auto !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important; color:#1e3a5f !important; font-size:11px !important; font-weight:700 !important; padding:14px 16px !important; border-radius:0 !important; border-bottom:2px solid transparent !important; letter-spacing:0.1em; text-transform:uppercase; white-space:nowrap !important; }
.stTabs [aria-selected="true"] { background:transparent !important; color:#10b981 !important; border-bottom:2px solid #10b981 !important; }
[data-testid="stTabPanel"] { background:transparent !important; padding-top:20px !important; }

/* ── INPUTS ── */
.stNumberInput input, .stTextInput input {
    background: #060b17 !important; border: 1px solid #0f1e38 !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 15px !important;
    padding: 10px 12px !important;
}
.stNumberInput input:focus, .stTextInput input:focus { border-color: #10b981 !important; box-shadow: 0 0 0 2px rgba(16,185,129,0.1) !important; }
.stTextArea textarea { background:#060b17 !important; border:1px solid #0f1e38 !important; border-radius:8px !important; color:#e2e8f0 !important; font-size:13px !important; line-height:1.6 !important; }
.stTextArea textarea:focus { border-color:#10b981 !important; }
[data-baseweb="select"] > div { background:#060b17 !important; border:1px solid #0f1e38 !important; border-radius:8px !important; }
[data-baseweb="select"] span, [data-baseweb="select"] div { color:#e2e8f0 !important; }
label { font-size:10px !important; font-weight:700 !important; color:#1e3a5f !important; text-transform:uppercase !important; letter-spacing:0.1em !important; font-family:'Outfit',sans-serif !important; }
.stDateInput input { background:#060b17 !important; border:1px solid #0f1e38 !important; color:#e2e8f0 !important; border-radius:8px !important; }

/* ── BUTTON — PRIMARY ── */
.stButton > button {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    font-weight: 700 !important; font-size: 12px !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    padding: 12px 20px !important; width: 100% !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(16,185,129,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(16,185,129,0.35) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── METRICS ── */
[data-testid="metric-container"] { background:#060b17 !important; border:1px solid #0f1e38 !important; border-radius:10px !important; padding:14px 16px !important; }
[data-testid="stMetricLabel"] { font-size:10px !important; color:#1e3a5f !important; text-transform:uppercase !important; letter-spacing:0.1em !important; font-family:'Outfit',sans-serif !important; }
[data-testid="stMetricValue"] { font-family:'JetBrains Mono',monospace !important; font-size:20px !important; color:#e2e8f0 !important; }
[data-testid="stMetricDelta"] { font-size:11px !important; }

/* ── SLIDER ── */
[data-testid="stSlider"] > div > div > div > div { background:#10b981 !important; }
[data-testid="stSlider"] > div > div > div { background:#0f1e38 !important; }

/* ── CHECKBOX ── */
.stCheckbox label { font-size:13px !important; color:#64748b !important; text-transform:none !important; letter-spacing:0 !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader { background:#0a1628 !important; border:1px solid #0f1e38 !important; border-radius:8px !important; color:#94a3b8 !important; font-size:13px !important; font-weight:600 !important; }
.streamlit-expanderContent { background:#060b17 !important; border:1px solid #0f1e38 !important; border-radius:0 0 8px 8px !important; }

/* ── RADIO ── */
.stRadio label { font-size:13px !important; color:#64748b !important; text-transform:none !important; letter-spacing:0 !important; }

/* ── SUCCESS / INFO / ERROR / WARNING ── */
[data-testid="stAlert"] { background:#0a1628 !important; border:1px solid #0f1e38 !important; border-radius:8px !important; font-size:13px !important; }

/* ── DIVIDER ── */
hr { border-color:#0f1e38 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:3px; background:transparent; }
::-webkit-scrollbar-thumb { background:#0f1e38; border-radius:3px; }

/* ── TOOLTIP HELPER ── */
.hint { font-size:11px; color:#1e3a5f; margin-top:4px; line-height:1.5; }

/* ── FEATURE COMPARE ROW ── */
.fcmp { display:flex; align-items:center; padding:10px 0; border-bottom:1px solid #0f1e38; gap:10px; }
.fcmp-feat { font-size:13px; color:#64748b; flex:1; }
.fcmp-us   { font-size:12px; color:#10b981; font-weight:700; width:80px; text-align:center; }
.fcmp-comp { font-size:12px; color:#334155; width:70px; text-align:center; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def ring(score, size=130):
    r = 44; c = 2 * 3.14159 * r
    d = round(score / 100 * c, 1); g = round(c - d, 1)
    col = "#10b981" if score >= 65 else ("#f59e0b" if score >= 35 else "#ef4444")
    return (f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 100 100">'
            f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="#0f1e38" stroke-width="8"/>'
            f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="{col}" stroke-width="8"'
            f' stroke-dasharray="{d} {g}" stroke-dashoffset="{c*0.25}" stroke-linecap="round"/>'
            f'<text x="50" y="45" text-anchor="middle" font-family="JetBrains Mono,monospace"'
            f' font-size="20" font-weight="500" fill="#e2e8f0">{score:.0f}</text>'
            f'<text x="50" y="60" text-anchor="middle" font-family="Outfit,sans-serif"'
            f' font-size="9" fill="#1e3a5f" letter-spacing="2">SCORE</text>'
            f'</svg></div>')

def bar(pct, color="#10b981"):
    pct = min(100, max(0, pct))
    return f'<div class="bt"><div class="bf" style="width:{pct}%;background:{color};"></div></div>'

def risk_tag(risk):
    c = {"SAFE":"r-s","MODERATE":"r-m","RISKY":"r-r"}
    l = {"SAFE":"Safe","MODERATE":"Moderate","RISKY":"High Risk"}
    return f'<span class="tag {c[risk]}">{l[risk]}</span>'

def level_tag(name):
    c = {"Platinum":"l-pl","Gold":"l-go","Silver":"l-si","Bronze":"l-br","Starter":"l-st"}
    return f'<span class="tag {c.get(name,"l-st")}">{name}</span>'

def sec(title, subtitle=None):
    sub = f"<div style='font-size:12px;color:#334155;margin-top:3px;'>{subtitle}</div>" if subtitle else ""
    st.markdown(f'<span class="lbl">{title}</span>{sub}', unsafe_allow_html=True)

def cmp_row(label, before, after, fmt=None, hb=True):
    b = fmt(before) if fmt else f"{before:.1f}"
    a = fmt(after)  if fmt else f"{after:.1f}"
    d = after - before
    cls = "ce" if abs(d) < 0.05 else ("cu" if (d > 0) == hb else "cd")
    return (f'<div class="cmp"><span class="cl">{label}</span>'
            f'<span class="co">{b}</span><span class="ca">→</span>'
            f'<span class="{cls}">{a}</span></div>')

def plotly_dark():
    return {
        "paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#475569", "family": "Outfit", "size": 11},
        "margin": {"l": 10, "r": 10, "t": 30, "b": 10},
        "xaxis": {"gridcolor": "#0f1e38", "linecolor": "#0f1e38", "tickfont": {"color":"#334155"}},
        "yaxis": {"gridcolor": "#0f1e38", "linecolor": "#0f1e38", "tickfont": {"color":"#334155"}},
    }

def divider():
    st.markdown("<hr style='border-color:#0f1e38;margin:16px 0;'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════
for k, v in {
    "page": "landing", "logged_in": False, "username": "",
    "persona_name": "Working Professional",
    "last_result": None, "last_income": 50000.0,
    "last_expenses": 35000.0, "last_savings": 120000.0,
    "challenges_done": set(), "daily_budget": 1000.0, "streak": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <style>
    .stApp { background: #060b17 !important; }
    .block-container { max-width: 900px !important; padding: 3rem 2rem 5rem !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── HERO ─────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 48px 0 36px 0;">
        <div style="display:inline-block; background:#031a0f; border:1px solid #064e35;
                    border-radius:20px; padding:4px 16px; font-size:11px; font-weight:700;
                    color:#10b981; letter-spacing:0.16em; text-transform:uppercase;
                    margin-bottom:20px;">
            India's Financial Safety Platform
        </div>
        <h1 style="font-family:'Outfit',sans-serif; font-size:52px; font-weight:900;
                   color:#f1f5f9; margin:0 0 16px 0; line-height:1.1; letter-spacing:-1px;">
            Do you know if<br><span style="color:#10b981;">you're financially safe?</span>
        </h1>
        <p style="font-size:18px; color:#475569; max-width:560px; margin:0 auto 32px auto;
                  line-height:1.7; font-weight:400;">
            Most people have no idea. Finverse gives you a clear, honest answer —
            your personal Financial Safety Score — in under 60 seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("GET MY SAFETY SCORE — FREE", key="hero_cta"):
            st.session_state.page = "onboard"
            st.rerun()

    # ── PROBLEM STATEMENT ────────────────────
    st.markdown("""
    <div style="text-align:center; margin: 48px 0 32px 0;">
        <div style="font-size:11px; color:#1e3a5f; text-transform:uppercase;
                    letter-spacing:0.16em; font-weight:700; margin-bottom:12px;">
            The Problem We're Solving
        </div>
        <h2 style="font-family:'Outfit',sans-serif; font-size:30px; font-weight:800;
                   color:#e2e8f0; margin:0 0 14px 0;">
            78% of Indians live paycheck to paycheck
        </h2>
        <p style="font-size:15px; color:#475569; max-width:600px; margin:0 auto;
                  line-height:1.75;">
            No one teaches us this in school. Banks profit from your confusion.
            Financial apps are designed for people who already understand finance.
            Finverse is built for everyone else.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Pain points
    p1, p2, p3 = st.columns(3)
    for col, icon, title, desc in [
        (p1, "?", "You don't know your number", "What is your financial safety score? If you can't answer in 5 seconds, you need Finverse."),
        (p2, "!", "One bad month can ruin you", "Without an emergency fund, a job loss or medical bill becomes a financial crisis overnight."),
        (p3, "→", "No one gives you a plan", "Banks sell products. Apps track numbers. Nobody tells you exactly what to do next."),
    ]:
        with col:
            st.markdown(
                f"<div class='card' style='text-align:center;padding:24px 20px;'>"
                f"<div style='font-family:JetBrains Mono,monospace;font-size:28px;font-weight:500;"
                f"color:#10b981;margin-bottom:12px;'>{icon}</div>"
                f"<div style='font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:8px;'>{title}</div>"
                f"<div style='font-size:12px;color:#475569;line-height:1.6;'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── OUR STORY ────────────────────────────
    st.markdown("""
    <div style="background:#0a1628; border:1px solid #0f1e38; border-radius:16px;
                padding:32px 36px; margin:32px 0;">
        <div style="font-size:10px; color:#1e3a5f; text-transform:uppercase;
                    letter-spacing:0.16em; font-weight:700; margin-bottom:14px;">
            Why We Built Finverse
        </div>
        <h3 style="font-family:'Outfit',sans-serif; font-size:22px; font-weight:800;
                   color:#e2e8f0; margin:0 0 14px 0; line-height:1.3;">
            A simple question that no app could answer
        </h3>
        <p style="font-size:14px; color:#64748b; line-height:1.85; margin:0 0 14px 0;">
            The idea came from a real moment. After getting a salary, paying bills, and checking the bank balance —
            the question that came to mind was: <em style="color:#94a3b8;">"Am I actually okay financially? Or am I just getting by?"</em>
        </p>
        <p style="font-size:14px; color:#64748b; line-height:1.85; margin:0 0 14px 0;">
            We opened every app we could find. None of them answered that question directly. They showed
            numbers, charts, categories. But nobody said: <em style="color:#94a3b8;">"Here is your financial safety
            score. Here is what it means. Here is exactly what to do."</em>
        </p>
        <p style="font-size:14px; color:#64748b; line-height:1.85; margin:0;">
            That is the gap Finverse fills. One clear score. One honest assessment.
            One personalised action plan. Built for India, by someone who needed it.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── FEATURES ─────────────────────────────
    st.markdown("""
    <div style="text-align:center; margin:32px 0 24px 0;">
        <div style="font-size:11px; color:#1e3a5f; text-transform:uppercase;
                    letter-spacing:0.16em; font-weight:700; margin-bottom:10px;">Everything in one place</div>
        <h2 style="font-family:'Outfit',sans-serif; font-size:28px; font-weight:800;
                   color:#e2e8f0; margin:0;">What Finverse Does</h2>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("Financial Safety Score", "A weighted composite score (0–100) that answers 'Am I safe?' in one number. No existing Indian app does this."),
        ("Stress Score", "Separate from your safety score — measures your financial anxiety level based on runway and cash flow."),
        ("Daily Expense Tracker", "Log expenses in seconds. Track against a daily budget. Build a streak. See monthly breakdowns."),
        ("Lend / Borrow Manager", "Track who owes you and who you owe. One-click reminder messages for WhatsApp."),
        ("What-If Simulator", "Drag sliders to see how a raise, expense cut, or bonus changes your safety score — instantly."),
        ("Partner Compatibility", "Enter both profiles. Get a compatibility score and the minimum partner income for a stable shared life."),
        ("Financial Education", "9 structured modules from Beginner to Advanced with real content, key takeaways, and book recommendations."),
        ("Behavioral Insights + Predictions", "Your FIRE date, emergency fund timeline, and pattern analysis from your own historical data."),
        ("Community", "Discuss saving, investing, and debt with other users anonymously. Finance-focused. Moderated."),
    ]

    f1, f2 = st.columns(2)
    for i, (title, desc) in enumerate(features):
        with (f1 if i % 2 == 0 else f2):
            st.markdown(
                f"<div class='card' style='margin-bottom:10px;'>"
                f"<div style='font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:5px;'>{title}</div>"
                f"<div style='font-size:12px;color:#475569;line-height:1.6;'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── COMPETITOR COMPARISON ────────────────
    st.markdown("""
    <div style="text-align:center; margin:36px 0 24px 0;">
        <div style="font-size:11px; color:#1e3a5f; text-transform:uppercase;
                    letter-spacing:0.16em; font-weight:700; margin-bottom:10px;">How We Compare</div>
        <h2 style="font-family:'Outfit',sans-serif; font-size:26px; font-weight:800;
                   color:#e2e8f0; margin:0 0 6px 0;">Finverse vs Every Other App</h2>
        <p style="font-size:13px; color:#334155; margin:0;">
            We studied Walnut, Fi, Jupiter, YNAB, Mint, and Splitwise before building Finverse.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        "<div style='display:flex;gap:10px;padding:8px 0 12px 0;border-bottom:1px solid #0f1e38;'>"
        "<div style='flex:1;font-size:11px;color:#1e3a5f;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;'>Feature</div>"
        "<div style='width:80px;text-align:center;font-size:11px;color:#10b981;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;'>Finverse</div>"
        "<div style='width:70px;text-align:center;font-size:11px;color:#334155;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;'>Others</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    comparisons = [
        ("Financial Safety Score (single honest number)", "✓", "✗"),
        ("Survival time without income", "✓", "✗"),
        ("Financial Stress Score", "✓", "✗"),
        ("What-If simulator (live)", "✓", "Partial"),
        ("Partner financial compatibility", "✓", "✗"),
        ("Expense tracking + daily budget", "✓", "✓"),
        ("Lend / Borrow with reminder messages", "✓", "Splitwise only"),
        ("Personalised action plan with amounts", "✓", "✗"),
        ("Financial education (structured modules)", "✓", "Partial"),
        ("Community discussions", "✓", "✗"),
        ("Gamification (levels, badges, XP)", "✓", "✗"),
        ("India-specific (₹, Indian finance rules)", "✓", "Partial"),
        ("Free, no account required", "✓", "Varies"),
    ]
    for feat, us, comp in comparisons:
        us_col   = "#10b981" if us == "✓" else "#f59e0b"
        comp_col = "#334155" if comp in ("✗","Varies") else ("#f59e0b" if comp == "Partial" else "#10b981")
        st.markdown(
            f"<div class='fcmp'>"
            f"<span class='fcmp-feat'>{feat}</span>"
            f"<span class='fcmp-us' style='color:{us_col};'>{us}</span>"
            f"<span class='fcmp-comp' style='color:{comp_col};'>{comp}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── STATS ────────────────────────────────
    stats = get_platform_stats()
    st.markdown(
        f"<div style='display:flex;gap:10px;flex-wrap:wrap;margin:32px 0;'>"
        f"<div class='card' style='flex:1;min-width:140px;text-align:center;padding:20px;'>"
        f"<div style='font-family:JetBrains Mono,monospace;font-size:32px;font-weight:500;color:#10b981;'>{max(stats['total_users'],0)}</div>"
        f"<div style='font-size:10px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;margin-top:4px;'>Users</div></div>"
        f"<div class='card' style='flex:1;min-width:140px;text-align:center;padding:20px;'>"
        f"<div style='font-family:JetBrains Mono,monospace;font-size:32px;font-weight:500;color:#10b981;'>{max(stats['total_scores'],0)}</div>"
        f"<div style='font-size:10px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;margin-top:4px;'>Scores Calculated</div></div>"
        f"<div class='card' style='flex:1;min-width:140px;text-align:center;padding:20px;'>"
        f"<div style='font-family:JetBrains Mono,monospace;font-size:32px;font-weight:500;color:#10b981;'>{stats['avg_score']:.0f}</div>"
        f"<div style='font-size:10px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;margin-top:4px;'>Avg Safety Score</div></div>"
        f"<div class='card' style='flex:1;min-width:140px;text-align:center;padding:20px;'>"
        f"<div style='font-family:JetBrains Mono,monospace;font-size:32px;font-weight:500;color:#10b981;'>{max(stats['total_expenses'],0)}</div>"
        f"<div style='font-size:10px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;margin-top:4px;'>Expenses Tracked</div></div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── FINAL CTA ────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#031a0f,#042e1a); border:1px solid #064e35;
                border-radius:16px; padding:40px 36px; text-align:center; margin:16px 0 32px 0;">
        <h2 style="font-family:'Outfit',sans-serif; font-size:28px; font-weight:900;
                   color:#f1f5f9; margin:0 0 12px 0;">
            Ready to know your number?
        </h2>
        <p style="font-size:14px; color:#475569; margin:0 0 24px 0;">
            Free. No email. No credit card. Just your financial truth in 60 seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_l, c_m, c_r = st.columns([1, 2, 1])
    with c_m:
        if st.button("START NOW — IT'S FREE", key="bottom_cta"):
            st.session_state.page = "onboard"
            st.rerun()

    st.markdown(
        "<p style='text-align:center;font-size:11px;color:#1e3a5f;margin-top:16px;'>"
        "Finverse v7.0 · Built in India · Not financial advice · Your data stays on this server</p>",
        unsafe_allow_html=True,
    )
    st.stop()


# ══════════════════════════════════════════════
# ONBOARDING
# ══════════════════════════════════════════════
if st.session_state.page == "onboard":
    st.markdown("""
    <style>
    .block-container { max-width: 600px !important; padding: 3rem 2rem 5rem !important; }
    </style>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom:32px;">
        <div style="font-family:'Outfit',sans-serif; font-size:28px; font-weight:900;
                    color:#f1f5f9; letter-spacing:-0.5px;">
            FIN<span style="color:#10b981;">VERSE</span>
        </div>
        <div style="font-size:12px; color:#1e3a5f; margin-top:4px; letter-spacing:0.14em;
                    text-transform:uppercase;">Tell us about yourself</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Step 1 — Your Identity", "This personalises your targets and tips.")

    oc1, oc2 = st.columns(2)
    with oc1:
        name_in = st.text_input("Your name", placeholder="e.g. Aashi")
    with oc2:
        age_in  = st.number_input("Your age", min_value=16, max_value=80, value=25, step=1)

    city_in = st.text_input("Your city", placeholder="e.g. Mumbai")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Step 2 — Your Life Stage", "Different stages need different financial targets.")

    persona_options = {k: f"{v['icon']}  {k}" for k, v in PERSONAS.items()}
    selected_persona = st.radio(
        "I am a",
        list(persona_options.keys()),
        format_func=lambda x: persona_options[x],
        index=1,
        label_visibility="collapsed",
        horizontal=True,
    )
    p = PERSONAS[selected_persona]
    st.markdown(
        f"<div style='background:#060b17;border:1px solid #0f1e38;border-radius:8px;"
        f"padding:12px 14px;margin-top:10px;font-size:12px;color:#475569;line-height:1.8;'>"
        f"Savings target: <span style='color:#10b981;font-weight:700;'>{p['savings_rate_target']}%</span> &nbsp;·&nbsp; "
        f"Emergency fund goal: <span style='color:#10b981;font-weight:700;'>{p['survival_target']} months</span>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    ob_l, ob_m, ob_r = st.columns([1, 2, 1])
    with ob_m:
        if st.button("ENTER FINVERSE", key="onboard_btn"):
            if name_in.strip():
                un = name_in.strip()
                upsert_user_profile(un, un, selected_persona, int(age_in), city_in)
                settings = get_user_settings(un)
                st.session_state.update({
                    "page": "app", "logged_in": True, "username": un,
                    "persona_name": selected_persona,
                    "daily_budget": settings["daily_budget"],
                    "streak": settings["streak"],
                    "challenges_done": get_completed_challenges(un),
                })
                st.rerun()
            else:
                st.warning("Enter your name to continue.")

    if st.button("← Back to home", key="back_land"):
        st.session_state.page = "landing"
        st.rerun()
    st.stop()


# ══════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════
if not st.session_state.logged_in:
    st.session_state.page = "landing"
    st.rerun()

un      = st.session_state.username
persona = PERSONAS[st.session_state.persona_name]

# ── SIDEBAR ──────────────────────────────────
with st.sidebar:
    st.markdown(
        f"<div style='background:#060b17;border:1px solid #0f1e38;border-radius:10px;"
        f"padding:14px 16px;margin-bottom:18px;'>"
        f"<div style='font-size:9px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.14em;'>Signed in as</div>"
        f"<div style='font-family:Outfit,sans-serif;font-size:18px;font-weight:800;"
        f"color:#10b981;margin-top:3px;'>{un}</div>"
        f"<div style='font-size:10px;color:#334155;margin-top:2px;'>{PERSONAS[st.session_state.persona_name]['icon']} {st.session_state.persona_name}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    new_p = st.selectbox(
        "Switch profile", list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.persona_name),
        label_visibility="collapsed",
    )
    if new_p != st.session_state.persona_name:
        st.session_state.persona_name = new_p
        persona = PERSONAS[new_p]
        upsert_user_profile(un, persona=new_p)
        st.rerun()

    p = PERSONAS[st.session_state.persona_name]
    st.markdown(
        f"<div style='background:#060b17;border:1px solid #0f1e38;border-radius:8px;"
        f"padding:13px 14px;margin:12px 0;'>"
        f"<div style='display:flex;justify-content:space-between;margin-bottom:8px;'>"
        f"<span style='font-size:9px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;'>Savings Target</span>"
        f"<span style='font-family:JetBrains Mono,monospace;font-size:15px;color:#10b981;'>{p['savings_rate_target']}%</span></div>"
        f"<div style='display:flex;justify-content:space-between;'>"
        f"<span style='font-size:9px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;'>Emergency Fund</span>"
        f"<span style='font-family:JetBrains Mono,monospace;font-size:15px;color:#10b981;'>{p['survival_target']}mo</span></div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='font-size:9px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.14em;"
        "margin:14px 0 8px 0;'>Tips for your profile</div>",
        unsafe_allow_html=True,
    )
    for tip in p["tips"]:
        st.markdown(
            f"<p style='font-size:11px;color:#334155;margin:0 0 8px 0;line-height:1.55;"
            f"padding-left:8px;border-left:2px solid #0f1e38;'>{tip}</p>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border-color:#0f1e38;margin:14px 0;'>", unsafe_allow_html=True)

    xp = get_total_xp(st.session_state.get("challenges_done", set()))
    settings = get_user_settings(un)
    st.markdown(
        f"<div style='background:#060b17;border:1px solid #0f1e38;border-radius:8px;"
        f"padding:13px;text-align:center;'>"
        f"<div style='font-family:JetBrains Mono,monospace;font-size:28px;font-weight:500;"
        f"color:#10b981;'>{xp}</div>"
        f"<div style='font-size:9px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;margin-top:2px;'>XP Earned</div>"
        f"<div style='font-size:10px;color:#1e3a5f;margin-top:6px;'>Streak: {settings['streak']} days</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border-color:#0f1e38;margin:14px 0;'>", unsafe_allow_html=True)

    if st.button("SIGN OUT", key="signout"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.markdown(
        "<p style='font-size:10px;color:#0f1e38;text-align:center;margin-top:10px;'>"
        "v7.0 · Not financial advice</p>",
        unsafe_allow_html=True,
    )

# ── HEADER ───────────────────────────────────
st.markdown("""
<div style="padding:18px 0 18px 0; border-bottom:1px solid #0f1e38; margin-bottom:22px;
            display:flex; justify-content:space-between; align-items:center;">
  <div>
    <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:900;
                color:#f1f5f9;letter-spacing:-0.3px;">
      FIN<span style="color:#10b981;">VERSE</span>
    </div>
    <div style="font-size:10px;color:#1e3a5f;letter-spacing:0.18em;text-transform:uppercase;margin-top:1px;">
      Financial Safety Platform
    </div>
  </div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
(t_score, t_dash, t_wi, t_sug, t_track,
 t_lend, t_part, t_rules, t_learn, t_comm, t_insights) = st.tabs([
    "Score", "Dashboard", "What-If", "Suggestions",
    "Tracker", "Lend / Borrow", "Partner",
    "Money Rules", "Learn", "Community", "Insights",
])


# ════════════════════════════════════════════
# SCORE TAB
# ════════════════════════════════════════════
with t_score:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Your Monthly Numbers", "Enter your current financial snapshot to get your safety score.")
    c1, c2 = st.columns(2)
    with c1:
        income  = st.number_input(persona["income_label"],  min_value=0.0, value=50000.0, step=1000.0, key="s_inc")
        savings = st.number_input("Total savings (₹)",      min_value=0.0, value=120000.0, step=5000.0, key="s_sav",
                                  help="All money you currently have saved — bank accounts, FDs, etc.")
    with c2:
        expenses = st.number_input("Monthly expenses (₹)", min_value=0.0, value=35000.0, step=1000.0, key="s_exp",
                                   help="Everything you spend: rent, food, EMIs, subscriptions, transport.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("CALCULATE MY SAFETY SCORE", key="s_calc"):
        if income <= 0:
            st.error("Income must be greater than zero.")
            st.stop()

        result  = analyse_finances(income, expenses, savings)
        lv      = get_level(result["composite_score"])
        next_l  = get_next_level(result["composite_score"])
        bdgs    = get_badges(result)
        score   = result["composite_score"]
        risk    = result["risk_level"]
        stress  = calculate_stress_score(income, expenses, savings, result)

        save_score(un, st.session_state.persona_name, income, expenses, savings, result, stress)
        upsert_leaderboard(un, score, lv["name"], st.session_state.persona_name)
        st.session_state.update({
            "last_result": result, "last_income": income,
            "last_expenses": expenses, "last_savings": savings,
        })

        # ── SCORE CARD ──────────────────────
        st.markdown('<div class="card">', unsafe_allow_html=True)
        rc1, rc2 = st.columns([1, 2])
        with rc1:
            st.markdown(ring(score, 140), unsafe_allow_html=True)
        with rc2:
            nh = (f"<div class='hint'>{next_l['points_needed']} more points to reach {next_l['name']}</div>"
                  if next_l else "<div class='hint' style='color:#10b981;'>Maximum level reached.</div>")
            st.markdown(
                f"<div style='padding:6px 0;'>{level_tag(lv['name'])}"
                f"<div style='font-family:Outfit,sans-serif;font-size:24px;font-weight:800;"
                f"color:#e2e8f0;margin:10px 0 6px 0;line-height:1.2;'>{lv['message']}</div>"
                f"{risk_tag(risk)}"
                f"<div class='hint' style='margin-top:8px;color:#475569;'>{get_risk_advice(risk)}</div>"
                f"{nh}</div>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # ── STRESS SCORE ────────────────────
        s_label, s_color = get_stress_label(stress)
        stress_tip = {
            "High Stress": "Your finances are under significant pressure. Focus on reducing expenses and building runway.",
            "Moderate Stress": "You have some financial cushion but it's thin. Building savings will reduce this score.",
            "Low Stress": "Your financial position is stable. Minor improvements can bring this to minimal.",
            "Minimal Stress": "Excellent. You have strong financial buffers and healthy cash flow.",
        }.get(s_label, "")
        st.markdown(
            f"<div class='card-flat'>"
            f"<span class='lbl'>Financial Stress Score</span>"
            f"<div style='display:flex;align-items:center;gap:20px;'>"
            f"<div style='font-family:JetBrains Mono,monospace;font-size:42px;font-weight:500;color:{s_color};'>{stress}</div>"
            f"<div><div style='font-size:14px;font-weight:700;color:{s_color};margin-bottom:3px;'>{s_label}</div>"
            f"<div style='font-size:12px;color:#475569;line-height:1.5;'>{stress_tip}</div>"
            f"<div style='font-size:11px;color:#1e3a5f;margin-top:4px;'>0 = no stress · 100 = severe</div></div>"
            f"</div>{bar(stress, s_color)}</div>",
            unsafe_allow_html=True,
        )

        # ── 3 METRICS ───────────────────────
        sr  = result["savings_rate"];  sm = result["survival_months"];  er = result["expense_ratio"]
        sc  = "#10b981" if sr >= 20 else ("#f59e0b" if sr >= 10 else "#ef4444")
        smc = "#10b981" if sm >= 6  else ("#f59e0b" if sm >= 3  else "#ef4444")
        erc = "#10b981" if er <= 60 else ("#f59e0b" if er <= 80 else "#ef4444")

        st.markdown(
            f"<div class='card'><span class='lbl'>Key Metrics</span>"
            f"<div class='sg'>"
            f"<div class='sb'><div class='sv' style='color:{sc};'>{sr:.1f}%</div>"
            f"<div class='sk'>Savings Rate</div><div class='sn'>{get_savings_rate_message(sr)}</div></div>"
            f"<div class='sb'><div class='sv' style='color:{smc};'>{format_months(sm)}</div>"
            f"<div class='sk'>Survival Time</div><div class='sn'>Without income</div></div>"
            f"<div class='sb'><div class='sv' style='color:{erc};'>{er:.1f}%</div>"
            f"<div class='sk'>Expense Ratio</div><div class='sn'>Of income spent</div></div>"
            f"</div>"
            f"<div style='margin-top:8px;'>{bar(min(100,int(sr/30*100)),sc)}{bar(min(100,int(sm/12*100)),smc)}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # ── MONTHLY ─────────────────────────
        surplus = income - expenses
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Monthly Picture")
        m1, m2, m3 = st.columns(3)
        m1.metric("Take-home Income", format_currency(income))
        m2.metric("Total Expenses",   format_currency(expenses))
        m3.metric("Surplus" if surplus >= 0 else "Deficit",
                  format_currency(abs(surplus)),
                  delta_color="normal" if surplus >= 0 else "inverse")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── BADGES ──────────────────────────
        if bdgs:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("Achievements Unlocked")
            st.markdown(
                "".join(
                    f'<span style="display:inline-block;background:#060b17;border:1px solid #0f1e38;'
                    f'border-radius:6px;padding:5px 12px;font-size:11px;font-weight:700;'
                    f'color:#475569;margin:3px;letter-spacing:0.06em;">'
                    f'{b["name"].split(" ",1)[-1]}</span>'
                    for b in bdgs
                ),
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # ── SCORE HISTORY ───────────────────
        history = get_score_history(un, 6)
        if len(history) > 1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("Your Score History")
            for h in history:
                col = "#10b981" if h["risk_level"]=="SAFE" else ("#f59e0b" if h["risk_level"]=="MODERATE" else "#ef4444")
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:8px 0;border-bottom:1px solid #0f1e38;'>"
                    f"<span style='font-family:JetBrains Mono,monospace;font-size:11px;color:#1e3a5f;'>{h['created_at'][:10]}</span>"
                    f"<span style='font-size:11px;color:#334155;'>{h['persona']}</span>"
                    f"<span style='font-family:JetBrains Mono,monospace;font-size:16px;color:{col};font-weight:500;'>{h['score']:.1f}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        # ── CHALLENGES ──────────────────────
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Active Challenges", "Complete these to earn XP and improve your score.")
        for ch in get_challenges():
            done = ch["id"] in st.session_state.get("challenges_done", set())
            ca, cb = st.columns([5, 1])
            with ca:
                op = "opacity:0.3;" if done else ""
                td = "text-decoration:line-through;" if done else ""
                st.markdown(
                    f"<div style='{op}background:#060b17;border:1px solid #0f1e38;"
                    f"border-radius:8px;padding:10px 14px;margin-bottom:5px;'>"
                    f"<div style='font-size:13px;color:#e2e8f0;font-weight:600;{td}'>{ch['name']}</div>"
                    f"<div style='font-size:11px;color:#1e3a5f;margin-top:2px;'>"
                    f"{ch['desc']} · +{ch['reward_xp']} XP</div></div>",
                    unsafe_allow_html=True,
                )
            with cb:
                if not done:
                    if st.button("Done", key=f"ch_{ch['id']}"):
                        save_challenge(un, ch["id"])
                        st.session_state.challenges_done.add(ch["id"])
                        st.success(f"+{ch['reward_xp']} XP!")
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding:56px 28px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:56px;color:#0f1e38;
                      font-weight:500;letter-spacing:-3px;line-height:1;">--</div>
          <div style="font-size:18px;font-weight:700;color:#1e3a5f;margin-top:14px;">
              Enter your numbers above
          </div>
          <div style="font-size:13px;color:#0f1e38;margin-top:6px;line-height:1.6;">
              Your safety score, stress score, and action plan<br>appear here after you calculate
          </div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# DASHBOARD TAB
# ════════════════════════════════════════════
with t_dash:
    score_hist  = get_score_history(un, 30)
    spend_trend = get_spending_trend(un, 30)
    monthly_exp = get_monthly_expenses(un)
    p_stats     = get_platform_stats()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Platform Overview")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Total Users",    p_stats["total_users"])
    d2.metric("Avg Safety Score", f"{p_stats['avg_score']:.1f}")
    d3.metric("Safe Users",     p_stats["safe_count"])
    d4.metric("High Risk Users",p_stats["risky_count"])
    st.markdown('</div>', unsafe_allow_html=True)

    if not PLOTLY:
        st.warning("Install plotly for charts: pip install plotly")
    else:
        if score_hist and len(score_hist) > 1:
            d = build_score_trend_data(score_hist)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("Your Safety Score — Trend Over Time")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=d["dates"], y=d["scores"],
                mode="lines+markers", line={"color":"#10b981","width":2},
                marker={"color":"#10b981","size":6},
                fill="tozeroy", fillcolor="rgba(16,185,129,0.05)"))
            fig.add_hline(y=65, line_dash="dot", line_color="#334155", annotation_text="Safe zone (65)")
            fig.update_layout(**plotly_dark(), height=230)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        if spend_trend:
            d2_ = build_expense_trend_data(spend_trend)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("Daily Spending — Last 30 Days")
            fig2 = go.Figure(go.Bar(x=d2_["dates"], y=d2_["amounts"],
                marker_color="#10b981", opacity=0.7))
            fig2.update_layout(**plotly_dark(), height=220)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        if monthly_exp:
            da = build_category_data(monthly_exp)
            c_dash1, c_dash2 = st.columns(2)
            with c_dash1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                sec("Spending by Category — This Month")
                fig3 = go.Figure(go.Pie(labels=da["categories"], values=da["totals"],
                    hole=0.55,
                    marker={"colors":["#10b981","#3b82f6","#f59e0b","#ef4444","#8b5cf6","#ec4899","#14b8a6","#f97316"]},
                    textfont={"color":"#64748b","size":10}))
                fig3.update_layout(**plotly_dark(), height=260, showlegend=True,
                                   legend={"font":{"color":"#475569","size":10}})
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            with c_dash2:
                if st.session_state.last_result:
                    surplus = st.session_state.last_income - st.session_state.last_expenses
                    if surplus > 0:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        sec("12-Month Savings Projection")
                        dp = build_prediction_data(st.session_state.last_savings, surplus)
                        fig4 = go.Figure(go.Scatter(x=dp["months"], y=dp["savings"],
                            mode="lines+markers", line={"color":"#3b82f6","width":2,"dash":"dot"},
                            marker={"color":"#3b82f6","size":5},
                            fill="tozeroy", fillcolor="rgba(59,130,246,0.05)"))
                        fig4.update_layout(**plotly_dark(), height=260)
                        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})
                        st.markdown('</div>', unsafe_allow_html=True)

    if not score_hist and not spend_trend:
        st.markdown(
            "<div class='card' style='text-align:center;padding:44px;color:#1e3a5f;'>"
            "Calculate your score and log some expenses to populate the dashboard.</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# WHAT-IF TAB
# ════════════════════════════════════════════
with t_wi:
    if not st.session_state.last_result:
        st.markdown('<div class="card" style="text-align:center;padding:40px;color:#1e3a5f;">Calculate your score in the Score tab first, then come back here.</div>', unsafe_allow_html=True)
    else:
        base = st.session_state.last_result
        bi   = st.session_state.last_income
        be   = st.session_state.last_expenses
        bs   = st.session_state.last_savings

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("What-If Simulator", "Drag the sliders to see how changes affect your safety score — instantly, no recalculation needed.")
        id_ = st.slider("💰 If my income changed by (₹/month)",   -20000, 50000,  0, 1000,
                        help="Positive = raise or side income. Negative = income drop.")
        ed_ = st.slider("✂️ If my expenses changed by (₹/month)", -20000, 20000,  0,  500,
                        help="Negative = cutting costs. Positive = more spending.")
        sd_ = st.slider("🏦 If I added to savings (₹)",                0, 500000, 0, 5000,
                        help="Bonus, gift, or asset sale proceeds.")
        st.markdown('</div>', unsafe_allow_html=True)

        nr   = calculate_whatif(bi, be, bs, {"income_delta":id_,"expenses_delta":ed_,"savings_delta":sd_})
        diff = nr["composite_score"] - base["composite_score"]
        dc   = "#10b981" if diff >= 0 else "#ef4444"

        ra, rb = st.columns(2)
        with ra:
            st.markdown(f'<div class="card" style="text-align:center;"><span class="lbl" style="display:block;text-align:center;">Current</span>{ring(base["composite_score"],120)}<div style="margin-top:10px;">{risk_tag(base["risk_level"])}</div></div>', unsafe_allow_html=True)
        with rb:
            arrow = "+" if diff >= 0 else ""
            st.markdown(f'<div class="card" style="text-align:center;"><span class="lbl" style="display:block;text-align:center;">New Scenario</span>{ring(nr["composite_score"],120)}<div style="margin-top:10px;">{risk_tag(nr["risk_level"])}</div><div style="font-family:JetBrains Mono,monospace;font-size:16px;color:{dc};margin-top:8px;font-weight:500;">{arrow}{diff:.1f} pts</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Metric Comparison")
        st.markdown(
            cmp_row("Savings Rate",    base["savings_rate"],    nr["savings_rate"],    fmt=lambda v:f"{v:.1f}%") +
            cmp_row("Survival Time",   base["survival_months"], nr["survival_months"], fmt=lambda v:format_months(v)) +
            cmp_row("Expense Ratio",   base["expense_ratio"],   nr["expense_ratio"],   fmt=lambda v:f"{v:.1f}%", hb=False) +
            cmp_row("Monthly Surplus", bi-be, (bi+id_)-(be+ed_), fmt=lambda v:format_currency(v)),
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if   diff > 10: st.success(f"+{diff:.1f} pts — moves you to {nr['risk_level']}.")
        elif diff > 0:  st.info(f"Small improvement of {diff:.1f} points.")
        elif diff < -10:st.error(f"{diff:.1f} pts — drops you to {nr['risk_level']}.")
        elif diff < 0:  st.warning(f"Small decline of {abs(diff):.1f} points.")
        else:           st.info("No meaningful change in this scenario.")


# ════════════════════════════════════════════
# SUGGESTIONS TAB
# ════════════════════════════════════════════
with t_sug:
    if not st.session_state.last_result:
        st.markdown('<div class="card" style="text-align:center;padding:40px;color:#1e3a5f;">Calculate your score first to get your personalised action plan.</div>', unsafe_allow_html=True)
    else:
        suggs = generate_suggestions(
            st.session_state.last_income,
            st.session_state.last_expenses,
            st.session_state.last_savings,
            st.session_state.last_result,
        )
        st.markdown(
            "<div style='margin-bottom:18px;'>"
            "<div style='font-size:20px;font-weight:800;color:#e2e8f0;'>Your Action Plan</div>"
            "<div style='font-size:13px;color:#334155;margin-top:3px;'>"
            "Personalised to your exact numbers. Ranked by financial impact. Work top to bottom.</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        for s in sorted(suggs, key=lambda x: {"High":0,"Medium":1,"Low":2}.get(x["impact"],3)):
            cls  = {"High":"sug-h","Medium":"sug-m","Low":"sug-l"}[s["impact"]]
            icls = {"High":"i-h","Medium":"i-m","Low":"i-l"}[s["impact"]]
            st.markdown(
                f'<div class="sug {cls}"><div class="stit">{s["title"]}'
                f'<span class="imp {icls}">{s["impact"]} Impact</span></div>'
                f'<div class="sbod">{s["detail"]}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            "<div style='border-left:3px solid #10b981;padding:16px 20px;background:#031a0f;"
            "border-radius:0 10px 10px 0;margin-top:16px;'>"
            "<div style='font-size:16px;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>"
            "The Rule That Beats All Others</div>"
            "<div style='font-size:13px;color:#475569;line-height:1.75;'>"
            "Save first. Spend what remains. Set up an automatic transfer on salary day "
            "before you spend a single rupee. Your lifestyle adjusts to what is left. "
            "This one habit, sustained for a decade, creates more wealth than any investment strategy.</div>"
            "</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# TRACKER TAB
# ════════════════════════════════════════════
with t_track:
    s = get_user_settings(un)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Daily Expense Tracker", "Log every expense to build the habit. Your streak grows each day you track.")
    h1, h2 = st.columns(2)
    h1.metric("Tracking Streak", f"{s['streak']} days",
              help="Increases every day you log at least one expense and click End Day.")
    with h2:
        nb = st.number_input("Daily budget (₹)", min_value=0.0, value=float(s["daily_budget"]), step=100.0,
                             help="How much you plan to spend today. You'll get an alert if you go over.")
        if nb != s["daily_budget"]:
            save_user_settings(un, nb, s["streak"], s["last_tracked"])
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Add an Expense")
    tc1, tc2, tc3, tc4 = st.columns([2, 2, 2, 3])
    with tc1:
        cat = st.selectbox("Category", ["Food & Dining","Transport","Shopping","Bills & Utilities",
                                         "Entertainment","Health","Education","Personal Care","Other"])
    with tc2:
        amt = st.number_input("Amount (₹)", min_value=0.0, value=0.0, step=10.0)
    with tc3:
        exp_date = st.date_input("Date", value=date.today())
    with tc4:
        note = st.text_input("Note (optional)", placeholder="e.g. Lunch at Café Coffee Day")
    if st.button("ADD EXPENSE", key="add_exp"):
        if amt > 0:
            save_expense(un, cat, float(amt), note, str(exp_date))
            st.success(f"Added: {cat} — {format_currency(amt)}")
            st.rerun()
        else:
            st.warning("Enter an amount greater than ₹0.")
    st.markdown('</div>', unsafe_allow_html=True)

    today_exps = get_today_expenses(un)
    budget     = s["daily_budget"]

    if today_exps:
        total  = sum(e["amount"] for e in today_exps)
        left   = budget - total
        pct    = min(100, int(total / budget * 100)) if budget > 0 else 100
        bc     = "#10b981" if pct < 70 else ("#f59e0b" if pct < 90 else "#ef4444")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Today's Summary")
        d1, d2, d3 = st.columns(3)
        d1.metric("Spent Today",    format_currency(total))
        d2.metric("Daily Budget",   format_currency(budget))
        d3.metric("Remaining" if left >= 0 else "Over Budget", format_currency(abs(left)),
                  delta_color="normal" if left >= 0 else "inverse")
        st.markdown(f"<div style='font-size:11px;color:#1e3a5f;margin-bottom:4px;'>Budget used: {pct}%</div>", unsafe_allow_html=True)
        st.markdown(bar(pct, bc), unsafe_allow_html=True)
        if pct >= 90: st.error("You are at 90%+ of your daily budget.")
        elif pct >= 70: st.warning("Over two-thirds of daily budget used.")
        else: st.success("Spending is on track today.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Expense Log — click Delete to remove any entry")
        for exp in reversed(today_exps):
            ec1, ec2, ec3, ec4, ec5 = st.columns([2, 3, 2, 2, 1])
            with ec1:
                st.markdown(f"<span style='font-size:11px;color:#334155;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;'>{exp['category']}</span>", unsafe_allow_html=True)
            with ec2:
                st.markdown(f"<span style='font-size:12px;color:#475569;'>{exp['note'] or '—'}</span>", unsafe_allow_html=True)
            with ec3:
                st.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:11px;color:#1e3a5f;'>{exp['created_at'][11:16]}</span>", unsafe_allow_html=True)
            with ec4:
                st.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:14px;color:#e2e8f0;'>{format_currency(exp['amount'])}</span>", unsafe_allow_html=True)
            with ec5:
                if st.button("Del", key=f"del_{exp['id']}"):
                    delete_expense(exp["id"])
                    st.rerun()
        divider()
        if st.button("END DAY — SAVE STREAK", use_container_width=True):
            new_streak = end_day_update_streak(un)
            st.success(f"Day saved! Streak: {new_streak} days.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        monthly = get_monthly_expenses(un)
        if monthly:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("This Month — All Spending")
            mt = sum(r["total"] for r in monthly)
            for row in monthly:
                p_ = int(row["total"] / mt * 100) if mt > 0 else 0
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;'>"
                    f"<span style='color:#475569;'>{row['category']}"
                    f"<span style='color:#1e3a5f;margin-left:5px;font-size:10px;'>({row['count']} entries)</span></span>"
                    f"<span style='font-family:JetBrains Mono,monospace;color:#e2e8f0;'>{format_currency(row['total'])}</span></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(bar(p_, "#1e3a5f"), unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-family:JetBrains Mono,monospace;font-size:16px;color:#e2e8f0;"
                f"margin-top:10px;border-top:1px solid #0f1e38;padding-top:10px;'>"
                f"Month total: {format_currency(mt)}</div>",
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card" style="text-align:center;padding:40px;color:#1e3a5f;">No expenses logged today. Add one above to start your tracking streak.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# LEND / BORROW TAB
# ════════════════════════════════════════════
with t_lend:
    summary = get_lend_borrow_summary(un)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Lend / Borrow Tracker", "Never lose track of who owes you — and who you owe.")
    ls1, ls2, ls3 = st.columns(3)
    ls1.metric("Others Owe You",  format_currency(summary["total_gave"]))
    ls2.metric("You Owe Others",  format_currency(summary["total_owe"]))
    net = summary["net"]
    ls3.metric("Your Net Position", format_currency(abs(net)),
               "in your favour" if net >= 0 else "you owe net",
               delta_color="normal" if net >= 0 else "inverse")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Add a Transaction")
    la1, la2, la3 = st.columns([2, 2, 2])
    with la1:
        party = st.text_input("Person's name", placeholder="e.g. Rahul")
    with la2:
        l_amt = st.number_input("Amount (₹)", min_value=0.0, value=0.0, step=100.0, key="l_amt")
    with la3:
        txn_type = st.selectbox("Transaction type", ["I gave them money (they owe me)", "I borrowed from them (I owe them)"])

    lb1c, lb2c = st.columns(2)
    with lb1c:
        desc     = st.text_input("What for?", placeholder="e.g. Dinner split, travel expense")
    with lb2c:
        due_date = st.date_input("Due date (optional)", value=None, key="lb_due")

    if st.button("ADD TRANSACTION", key="add_lb"):
        if party.strip() and l_amt > 0:
            t  = "gave" if "gave" in txn_type else "owe"
            dd = str(due_date) if due_date else None
            add_lend_borrow(un, party.strip(), float(l_amt), t, desc, dd)
            st.success(f"Recorded: {txn_type.split('(')[0].strip()} {format_currency(l_amt)} with {party}")
            st.rerun()
        else:
            st.warning("Enter a name and amount greater than ₹0.")
    st.markdown('</div>', unsafe_allow_html=True)

    all_txns = get_lend_borrow(un)
    pending  = [t for t in all_txns if t["status"] == "pending"]
    settled  = [t for t in all_txns if t["status"] == "settled"]

    if pending:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec(f"Pending Transactions ({len(pending)})")
        for txn in pending:
            is_gave = txn["txn_type"] == "gave"
            color   = "#10b981" if is_gave else "#ef4444"
            label   = "They owe you" if is_gave else "You owe them"
            due_str = f"  ·  Due: {txn['due_date']}" if txn.get("due_date") else ""

            t1, t2, t3, t4, t5 = st.columns([2, 2, 2, 1, 1])
            with t1:
                st.markdown(f"<div style='font-size:13px;color:#94a3b8;font-weight:700;'>{txn['party_name']}</div><div style='font-size:11px;color:#334155;'>{txn.get('description','') or '—'}{due_str}</div>", unsafe_allow_html=True)
            with t2:
                st.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:16px;color:{color};font-weight:500;'>{format_currency(txn['amount'])}</span>", unsafe_allow_html=True)
            with t3:
                st.markdown(f"<span style='font-size:11px;color:#475569;'>{label}</span>", unsafe_allow_html=True)
            with t4:
                if st.button("Settle", key=f"set_{txn['id']}"):
                    settle_lend_borrow(txn["id"])
                    st.success(f"Settled with {txn['party_name']}.")
                    st.rerun()
            with t5:
                if st.button("Delete", key=f"dlt_{txn['id']}"):
                    delete_lend_borrow(txn["id"])
                    st.rerun()

            # Reminder generator
            with st.expander(f"Generate reminder message for {txn['party_name']}"):
                if is_gave:
                    msg = (f"Hi {txn['party_name']}! Just a friendly reminder that you owe me "
                           f"{format_currency(txn['amount'])}"
                           f"{' (due ' + txn['due_date'] + ')' if txn.get('due_date') else ''}. "
                           f"{'For: ' + txn['description'] + '. ' if txn.get('description') else ''}"
                           f"Please pay when convenient. Thanks!")
                else:
                    msg = (f"Reminding myself: I owe {txn['party_name']} {format_currency(txn['amount'])}"
                           f"{' by ' + txn['due_date'] if txn.get('due_date') else ''}. "
                           f"{'For: ' + txn['description'] + '.' if txn.get('description') else ''} "
                           f"I will pay soon.")
                st.code(msg, language=None)
                st.caption("Copy this and send on WhatsApp.")
        st.markdown('</div>', unsafe_allow_html=True)

    if settled:
        with st.expander(f"Settled Transactions ({len(settled)})"):
            for txn in settled:
                color = "#10b981" if txn["txn_type"]=="gave" else "#ef4444"
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #0f1e38;'>"
                    f"<span style='font-size:12px;color:#334155;'>{txn['party_name']} — {txn.get('description','') or 'no description'}</span>"
                    f"<span style='font-family:JetBrains Mono,monospace;font-size:13px;color:{color};text-decoration:line-through;'>{format_currency(txn['amount'])}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    if not all_txns:
        st.markdown('<div class="card" style="text-align:center;padding:40px;color:#1e3a5f;">No transactions yet. Add one above to start tracking.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# PARTNER TAB
# ════════════════════════════════════════════
with t_part:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Financial Compatibility Test", "How financially compatible are you? Enter both profiles to find out.")
    st.markdown('</div>', unsafe_allow_html=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;color:#1e3a5f;text-transform:uppercase;margin-bottom:8px;'>Your Profile</div>", unsafe_allow_html=True)
        p1i = st.number_input("Your income (₹/month)",   min_value=0.0, value=50000.0, step=1000.0, key="p1i")
        p1e = st.number_input("Your expenses (₹/month)", min_value=0.0, value=35000.0, step=1000.0, key="p1e")
        p1s = st.number_input("Your savings (₹ total)",  min_value=0.0, value=120000.0,step=5000.0, key="p1s")
    with pc2:
        st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;color:#1e3a5f;text-transform:uppercase;margin-bottom:8px;'>Partner's Profile</div>", unsafe_allow_html=True)
        p2i = st.number_input("Partner's income (₹/month)",   min_value=0.0, value=45000.0, step=1000.0, key="p2i")
        p2e = st.number_input("Partner's expenses (₹/month)", min_value=0.0, value=30000.0, step=1000.0, key="p2e")
        p2s = st.number_input("Partner's savings (₹ total)",  min_value=0.0, value=80000.0, step=5000.0, key="p2s")

    if st.button("CALCULATE COMPATIBILITY", use_container_width=True):
        r1     = analyse_finances(p1i, p1e, p1s)
        r2     = analyse_finances(p2i, p2e, p2s)
        compat = analyse_compatibility(r1, r2)
        cs     = compat["compatibility_score"]

        if   cs >= 75: lbl, col, tip = "Excellent Match",   "#10b981", "Financially well-aligned. Strong foundation for a shared life."
        elif cs >= 55: lbl, col, tip = "Good Match",        "#f59e0b", "Solid. Have regular money conversations to strengthen alignment."
        elif cs >= 35: lbl, col, tip = "Needs Alignment",   "#f59e0b", "Significant differences exist. Open, honest financial discussions are essential."
        else:          lbl, col, tip = "Significant Gap",   "#ef4444", "Major financial misalignment. Address this before any major shared commitments."

        st.markdown(
            f"<div class='card' style='text-align:center;padding:32px;'>"
            f"<div style='font-family:JetBrains Mono,monospace;font-size:60px;font-weight:500;"
            f"color:{col};letter-spacing:-3px;line-height:1;'>{cs:.0f}</div>"
            f"<div style='font-size:18px;font-weight:800;color:#e2e8f0;margin-top:6px;'>{lbl}</div>"
            f"<div style='font-size:12px;color:#475569;margin-top:6px;line-height:1.6;max-width:400px;margin-left:auto;margin-right:auto;'>{tip}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        ia, ib, ic = st.columns(3)
        ia.metric("Your Score",    f"{r1['composite_score']} / 100")
        ib.metric("Partner Score", f"{r2['composite_score']} / 100")
        ic.metric("Alignment",     f"{compat['alignment_score']} / 100",
                  help="How similar your financial behaviours are. Higher = more aligned.")

        combined = compat["combined"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Combined Financial Picture")
        cf1, cf2, cf3, cf4 = st.columns(4)
        cf1.metric("Combined Income",  format_currency(combined["income"]))
        cf2.metric("Combined Savings", format_currency(combined["savings"]))
        cf3.metric("Survive Together", format_months(combined["survival_months"]))
        cf4.metric("Combined Score",   f"{combined['composite_score']} / 100")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Ideal Partner Income Calculator", "How much should your partner earn for a financially stable shared life?")
        t_sr = st.slider("Target combined savings rate (%)", 10, 40, 20, key="tsr",
                         help="The percentage of combined income you want to save each month.")
        rec  = recommended_partner_income(p1i, p1e, p1s, t_sr)
        ri1, ri2, ri3 = st.columns(3)
        ri1.metric("Min. Partner Income",       format_currency(rec["min_partner_income"]), "per month")
        ri2.metric("Emergency Fund Target",     format_currency(rec["target_combined_savings"]))
        ri3.metric("Partner Monthly Savings",   format_currency(rec["partner_monthly_savings_target"]))
        st.markdown(
            f"<div class='hint'>Assumes combined living costs ≈ {format_currency(rec['estimated_combined_expenses'])}/month "
            f"(your expenses × 1.6 for shared living).</div>",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# MONEY RULES TAB
# ════════════════════════════════════════════
with t_rules:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Personal Finance Rules Calculator", "Enter your numbers once to see all major financial rules applied to your exact situation.")
    rc1, rc2 = st.columns(2)
    with rc1:
        r_inc = st.number_input("Monthly income (₹)",  min_value=0.0, value=50000.0, step=1000.0, key="r_i")
        r_sav = st.number_input("Current savings (₹)", min_value=0.0, value=120000.0, step=5000.0, key="r_s")
    with rc2:
        r_exp = st.number_input("Monthly expenses (₹)",min_value=0.0, value=35000.0, step=1000.0, key="r_e")
        r_age = st.slider("Your age", 18, 65, 25)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("SHOW MY NUMBERS", key="rules_btn"):
        rules = calculate_savings_rules(r_inc, r_exp, r_sav, r_age)

        for rule_num, (title, subtitle, content) in enumerate([
            (
                "Rule 1 — The 50 / 30 / 20 Rule",
                "Split your income: 50% needs, 30% wants, 20% savings.",
                lambda: (
                    st.columns(3),
                    st.success(f"You save {format_currency(r_inc - r_exp)}/month — above the 20% target.") if (r_inc - r_exp) >= rules["rule_20_savings"]
                    else st.warning(f"You are {format_currency(rules['rule_20_savings'] - (r_inc - r_exp))} short of the 20% savings target. Try cutting discretionary spending."),
                )
            ),
        ]):
            pass

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Rule 1 — The 50 / 30 / 20 Rule", "Split your income: 50% needs, 30% wants, 20% savings.")
        r1a, r1b, r1c = st.columns(3)
        r1a.metric("50% — Needs",   format_currency(rules["rule_50_needs"]),   "rent, food, bills")
        r1b.metric("30% — Wants",   format_currency(rules["rule_30_wants"]),   "fun, dining, shopping")
        r1c.metric("20% — Savings", format_currency(rules["rule_20_savings"]), "investments & future")
        actual = r_inc - r_exp
        if actual >= rules["rule_20_savings"]:
            st.success(f"You save {format_currency(actual)}/month — above the 20% target. Well done.")
        else:
            gap = rules["rule_20_savings"] - actual
            st.warning(f"You are {format_currency(gap)}/month short of the 20% target. Cut wants, not needs.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Rule 2 — Emergency Fund Rule", "Keep 3–6 months of expenses in a liquid, easily accessible account.")
        ef1, ef2, ef3 = st.columns(3)
        ef1.metric("3-Month Target",  format_currency(rules["emergency_3m"]))
        ef2.metric("6-Month Target",  format_currency(rules["emergency_6m"]))
        ef3.metric("You Currently Have", format_months(rules["current_coverage"]), "of coverage")
        m = rules.get("months_to_6m_fund")
        if rules["current_coverage"] >= 6:
            st.success("You have reached the 6-month emergency fund target.")
        elif rules["current_coverage"] >= 3 and m:
            st.info(f"At current savings rate, you reach 6 months in {m:.0f} more months.")
        elif m:
            st.warning(f"Time to 6-month emergency fund: {m:.0f} months at current rate.")
        else:
            st.error("You need a monthly surplus before you can build an emergency fund. Reduce expenses first.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Rule 3 — Your FIRE Number", "25× your annual expenses. At a 4% withdrawal rate, this corpus lasts indefinitely.")
        fi1, fi2 = st.columns(2)
        fi1.metric("Your FIRE Number", format_currency(rules["fire_number"]))
        fi2.metric("Progress",         f"{rules['fire_progress']:.1f}%")
        st.markdown(bar(min(100, int(rules["fire_progress"])), "#10b981"), unsafe_allow_html=True)
        remaining = rules["fire_number"] - r_sav
        surplus_  = r_inc - r_exp
        if remaining > 0 and surplus_ > 0:
            yrs = round(remaining / surplus_ / 12, 1)
            st.info(f"{format_currency(remaining)} remaining to FIRE. At current surplus: ~{yrs} years (without investment growth — actual will be shorter).")
        elif rules["fire_progress"] >= 100:
            st.success("You have reached your FIRE number. Financial independence is yours.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec(f"Rule 4 — 100-Age Investment Rule (Age {r_age})", f"Put {rules['equity_pct']}% in equity and {rules['debt_pct']}% in safer debt instruments. Rebalance once a year.")
        ia1, ia2 = st.columns(2)
        ia1.metric(f"Equity ({rules['equity_pct']}%)", format_currency(rules["equity_amount"]), "stocks, index funds")
        ia2.metric(f"Debt ({rules['debt_pct']}%)",     format_currency(rules["debt_amount"]),   "FD, PPF, bonds")
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# LEARN TAB
# ════════════════════════════════════════════
with t_learn:
    progress = get_education_progress(un)
    done_ids = {mid for mid, done in progress.items() if done}
    total_m  = len(LEARNING_MODULES)
    done_ct  = len(done_ids)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Financial Education — Structured Learning Path", "9 modules from Beginner to Advanced. Each takes 5–10 minutes.")
    lp1, lp2, lp3 = st.columns(3)
    lp1.metric("Completed",   f"{done_ct} / {total_m}")
    lp2.metric("XP Earned",   f"{done_ct * 20}")
    lp3.metric("Progress",    f"{int(done_ct / total_m * 100)}%")
    st.markdown(bar(int(done_ct / total_m * 100), "#10b981"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    modules_by_level = get_modules_by_level()
    level_colors = {"Beginner":"#10b981","Intermediate":"#f59e0b","Advanced":"#ef4444"}

    for level_name, modules in modules_by_level.items():
        lc = level_colors.get(level_name, "#10b981")
        st.markdown(
            f"<div style='font-size:16px;font-weight:800;color:{lc};"
            f"margin:20px 0 10px 0;'>{level_name}</div>",
            unsafe_allow_html=True,
        )
        for mod in modules:
            is_done = mod["id"] in done_ids
            done_label = "  ✓  Completed" if is_done else f"  ·  {mod['duration']}  ·  +{mod['xp']} XP"
            with st.expander(f"{mod['title']}{done_label}", expanded=False):
                st.markdown(
                    f"<div style='font-size:13px;color:#94a3b8;margin-bottom:8px;"
                    f"font-style:italic;'>{mod['summary']}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='font-size:13px;color:#64748b;line-height:1.8;"
                    f"white-space:pre-line;'>{mod['content'].strip()}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='background:#031a0f;border:1px solid #064e35;border-radius:8px;"
                    f"padding:12px 16px;margin-top:14px;'>"
                    f"<div style='font-size:9px;color:#1e3a5f;text-transform:uppercase;"
                    f"letter-spacing:0.14em;margin-bottom:4px;'>Key Takeaway</div>"
                    f"<div style='font-size:13px;color:#34d399;font-weight:600;line-height:1.5;'>"
                    f"{mod['key_takeaway']}</div></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='margin-top:10px;font-size:12px;color:#334155;'>"
                    f"Recommended: <span style='color:#94a3b8;font-weight:700;'>"
                    f"{mod['book_title']}</span> by {mod['book_author']}"
                    f"  ·  <a href='{mod['free_link']}' target='_blank' "
                    f"style='color:#1e3a5f;text-decoration:none;'>Find on Open Library</a></div>",
                    unsafe_allow_html=True,
                )
                if not is_done:
                    if st.button(f"Mark complete  +{mod['xp']} XP", key=f"mod_{mod['id']}"):
                        mark_module_complete(un, mod["id"])
                        st.success(f"Module completed! +{mod['xp']} XP added.")
                        st.rerun()

    # Books
    st.markdown(
        "<div style='font-size:18px;font-weight:800;color:#e2e8f0;"
        "margin:28px 0 14px 0;'>Reading List</div>",
        unsafe_allow_html=True,
    )
    for book in BOOK_LIST:
        lc = level_colors.get(book["level"], "#10b981")
        st.markdown(
            f"<div class='book'>"
            f"<div style='display:flex;justify-content:space-between;align-items:flex-start;gap:10px;'>"
            f"<div class='btit'>{book['title']}</div>"
            f"<span style='font-size:9px;color:{lc};text-transform:uppercase;letter-spacing:0.1em;"
            f"font-weight:700;white-space:nowrap;'>{book['level']}</span></div>"
            f"<div class='baut'>by {book['author']}</div>"
            f"<div class='bwhy'>{book['why']}</div>"
            f"<div style='margin-top:8px;display:flex;gap:12px;'>"
            f"<a href='{book['buy_link']}' target='_blank' style='font-size:11px;color:#10b981;"
            f"text-decoration:none;font-weight:700;'>Buy on Amazon</a>"
            f"<a href='{book['free_link']}' target='_blank' style='font-size:11px;color:#475569;"
            f"text-decoration:none;'>Find free version</a>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    # Free resources
    st.markdown(
        "<div style='font-size:16px;font-weight:800;color:#e2e8f0;"
        "margin:24px 0 12px 0;'>Free Online Resources</div>",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="card">', unsafe_allow_html=True)
    for res in FREE_RESOURCES:
        st.markdown(
            f"<div style='padding:10px 0;border-bottom:1px solid #0f1e38;'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center;gap:10px;'>"
            f"<div style='font-size:13px;color:#94a3b8;font-weight:600;'>{res['name']}</div>"
            f"<a href='{res['url']}' target='_blank' style='font-size:11px;color:#10b981;"
            f"text-decoration:none;font-weight:700;white-space:nowrap;'>Visit →</a></div>"
            f"<div style='font-size:11px;color:#334155;margin-top:3px;line-height:1.5;'>{res['desc']}</div>"
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
    sec("Community Discussions", "Ask questions, share what works, help others. Finance-only. Be respectful.")
    topic_filter = st.selectbox("Filter topic", TOPICS)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Write a New Post"):
        np_topic = st.selectbox("Topic", TOPICS[1:], key="np_topic")
        np_text  = st.text_area("Your post", placeholder="Share a tip, ask a question, describe a situation...", height=100)
        np_anon  = st.checkbox("Post anonymously (your name won't be shown)")
        if st.button("PUBLISH POST", key="post_btn"):
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
            "No posts in this topic yet. Be the first to start the conversation.</div>",
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
    sec("Behavioral Insights", "Patterns from your historical data — what your numbers are telling you.")
    for insight in insights:
        st.markdown(
            f"<div style='padding:12px 16px;border-left:3px solid #10b981;background:#031a0f;"
            f"border-radius:0 8px 8px 0;margin-bottom:8px;font-size:13px;color:#94a3b8;"
            f"line-height:1.7;'>{insight}</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Predictions
    if st.session_state.last_result:
        surplus_     = st.session_state.last_income - st.session_state.last_expenses
        current_sav  = st.session_state.last_savings
        monthly_exp_ = st.session_state.last_expenses
        annual_exp_  = monthly_exp_ * 12

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Financial Targets — Time to Reach")
        ef_months = predict_emergency_fund_date(current_sav, surplus_, monthly_exp_, 6)
        fire_yrs  = predict_fire_date(current_sav, surplus_, annual_exp_)

        pr1, pr2 = st.columns(2)
        with pr1:
            if ef_months == 0:
                st.markdown("<div class='card-green'><span class='lbl'>6-Month Emergency Fund</span><div style='font-family:JetBrains Mono,monospace;font-size:26px;color:#10b981;'>Achieved</div><div class='hint' style='color:#334155;'>You have already hit this target.</div></div>", unsafe_allow_html=True)
            elif ef_months:
                st.markdown(f"<div class='card-flat'><span class='lbl'>6-Month Emergency Fund</span><div style='font-family:JetBrains Mono,monospace;font-size:26px;color:#f59e0b;'>{ef_months} months</div><div class='hint'>At current savings rate, without any investment growth.</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-red'><span class='lbl'>6-Month Emergency Fund</span><div style='font-size:13px;color:#ef4444;'>Cannot reach at current rate.</div><div class='hint'>Create a monthly surplus by reducing expenses first.</div></div>", unsafe_allow_html=True)
        with pr2:
            if fire_yrs == 0:
                st.markdown("<div class='card-green'><span class='lbl'>FIRE Number</span><div style='font-family:JetBrains Mono,monospace;font-size:26px;color:#10b981;'>Achieved</div><div class='hint' style='color:#334155;'>Financial independence reached.</div></div>", unsafe_allow_html=True)
            elif fire_yrs:
                st.markdown(f"<div class='card-flat'><span class='lbl'>FIRE Number</span><div style='font-family:JetBrains Mono,monospace;font-size:26px;color:#3b82f6;'>{fire_yrs} years</div><div class='hint'>Without investment returns — actual timeline will be shorter.</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-red'><span class='lbl'>FIRE Number</span><div style='font-size:13px;color:#ef4444;'>Cannot calculate.</div><div class='hint'>Need a positive monthly surplus first.</div></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Global Leaderboard
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Global Safety Leaderboard")
    lb_data = get_leaderboard(20)
    if lb_data:
        for i, e in enumerate(lb_data):
            is_me  = e["username"] == un
            bg     = "#031a0f" if is_me else "#0a1628"
            border = "1px solid #064e35" if is_me else "1px solid #0f1e38"
            rank   = f"0{i+1}" if i + 1 < 10 else str(i+1)
            st.markdown(
                f"<div class='lbr' style='background:{bg};border:{border};'>"
                f"<span class='lrk'>{rank}</span>"
                f"<span class='lnm' style='{'color:#10b981;font-weight:700;' if is_me else ''}'>"
                f"{e['username']}{'  (you)' if is_me else ''}</span>"
                f"<span class='llv'>{e['level_name']}</span>"
                f"<span class='llv'>{e['persona']}</span>"
                f"<span class='lsc'>{e['score']:.1f}</span></div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown("<p style='font-size:12px;color:#1e3a5f;'>No scores yet. Calculate yours in the Score tab to appear here.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Survey
    SURVEY_Q    = "What is your biggest financial challenge right now?"
    SURVEY_OPTS = [
        "Not saving enough each month",
        "Too much debt or EMIs",
        "No emergency fund",
        "Irregular or uncertain income",
        "Don't know how or where to invest",
        "Spending more than I earn",
        "No clear financial plan",
    ]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Community Survey")
    if not has_answered_survey(un, SURVEY_Q):
        st.markdown(
            f"<div style='font-size:14px;color:#94a3b8;font-weight:600;margin-bottom:14px;'>"
            f"{SURVEY_Q}</div>",
            unsafe_allow_html=True,
        )
        answer = st.radio("Select your answer", SURVEY_OPTS, label_visibility="collapsed")
        if st.button("SUBMIT ANSWER", key="survey_btn"):
            save_survey_response(un, SURVEY_Q, answer)
            st.success("Thank you. Your response has been recorded.")
            st.rerun()
    else:
        responses  = get_survey_responses(SURVEY_Q)
        total_r    = len(responses)
        counts     = {}
        for r in responses:
            counts[r["answer"]] = counts.get(r["answer"], 0) + 1

        st.markdown(
            f"<div style='font-size:13px;color:#94a3b8;font-weight:600;margin-bottom:14px;'>"
            f"Survey Results — {SURVEY_Q} ({total_r} responses)</div>",
            unsafe_allow_html=True,
        )
        for opt in SURVEY_OPTS:
            cnt = counts.get(opt, 0)
            pct = int(cnt / total_r * 100) if total_r > 0 else 0
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;'>"
                f"<span style='color:#64748b;'>{opt}</span>"
                f"<span style='font-family:JetBrains Mono,monospace;color:#94a3b8;'>{pct}% ({cnt})</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown(bar(pct, "#334155"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Share
    if st.session_state.last_result:
        sc_ = st.session_state.last_result["composite_score"]
        risk_ = st.session_state.last_result["risk_level"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Share Your Score")
        msg = (f"I just checked my Financial Safety Score on Finverse: {sc_:.0f}/100 ({risk_})\n"
               f"It tells you if you're actually financially safe — not just whether you have money.\n"
               f"Check yours free: [your Finverse link here]")
        st.code(msg, language=None)
        st.caption("Copy and send on WhatsApp, Instagram, or LinkedIn.")
        st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────
st.markdown(
    "<div style='text-align:center;padding:28px 0 0;border-top:1px solid #0f1e38;margin-top:16px;'>"
    "<span style='font-family:Outfit,sans-serif;font-size:14px;font-weight:900;"
    "color:#0f1e38;'>FINVERSE</span>"
    "<span style='font-size:11px;color:#0f1e38;margin-left:14px;'>v7.0</span>"
    "<span style='font-size:11px;color:#0f1e38;margin-left:14px;'>Built in India</span>"
    "<span style='font-size:11px;color:#0f1e38;margin-left:14px;'>Not financial advice</span>"
    "<span style='font-size:11px;color:#0f1e38;margin-left:14px;'>Data stored on this server</span>"
    "</div>",
    unsafe_allow_html=True,
)
