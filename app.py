# app.py  —  Finverse v6.0
# Full-featured financial platform.
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
from education    import LEARNING_MODULES, BOOK_LIST, get_modules_by_level, get_module_by_id
from database     import (
    init_db, upsert_user_profile, get_user_profile, get_all_users,
    save_score, get_score_history, get_all_score_history, get_platform_stats,
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
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY = True
except ImportError:
    PLOTLY = False

# ── INIT ─────────────────────────────────────
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
# CSS
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Mono:wght@400;500&family=Mulish:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Mulish', sans-serif !important; }
#MainMenu, footer, header   { visibility: hidden; }
.stApp                      { background: #050a14; }
.block-container            { max-width: 1000px !important; padding: 0 1.5rem 4rem !important; }

[data-testid="stSidebar"]         { background: #080f1e !important; border-right: 1px solid #0d1a2e !important; }
[data-testid="stSidebar"] section { padding-top: 1rem !important; }

/* CARDS */
.card  { background:#080f1e; border:1px solid #0d1a2e; border-radius:10px; padding:20px 22px; margin-bottom:14px; }
.card2 { background:#050a14; border:1px solid #0d1a2e; border-radius:10px; padding:20px 22px; margin-bottom:14px; }
.card-g{ background:#041810; border:1px solid #064e35; border-radius:10px; padding:20px 22px; margin-bottom:14px; }
.card-r{ background:#1a0505; border:1px solid #7f1d1d; border-radius:10px; padding:20px 22px; margin-bottom:14px; }
.card-y{ background:#1c1000; border:1px solid #78350f; border-radius:10px; padding:20px 22px; margin-bottom:14px; }

/* LABEL */
.lbl { font-size:10px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#1e3a5f; margin:0 0 12px 0; display:block; }

/* STATS */
.sg  { display:flex; gap:10px; flex-wrap:wrap; }
.sb  { flex:1; min-width:120px; background:#050a14; border:1px solid #0d1a2e; border-radius:8px; padding:13px 15px; }
.sv  { font-family:'DM Mono',monospace; font-size:21px; font-weight:500; color:#e2e8f0; line-height:1.1; }
.sk  { font-size:10px; color:#1e3a5f; text-transform:uppercase; letter-spacing:0.12em; margin-top:4px; font-weight:700; }
.sn  { font-size:11px; color:#1e3a5f; margin-top:3px; line-height:1.4; }

/* RISK / LEVEL TAGS */
.tag  { display:inline-block; font-size:10px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; padding:3px 10px; border-radius:3px; }
.r-s  { background:#041810; color:#10b981; border:1px solid #064e35; }
.r-m  { background:#1c1000; color:#f59e0b; border:1px solid #78350f; }
.r-r  { background:#1a0505; color:#ef4444; border:1px solid #7f1d1d; }
.l-pl { background:#0c1f3d; color:#60a5fa; border:1px solid #1d4ed8; }
.l-go { background:#1c1000; color:#fbbf24; border:1px solid #d97706; }
.l-si { background:#0d1a2e; color:#94a3b8; border:1px solid #334155; }
.l-br { background:#1a0a00; color:#fb923c; border:1px solid #9a3412; }
.l-st { background:#041810; color:#34d399; border:1px solid #065f46; }

/* BAR */
.bt { background:#0d1a2e; border-radius:2px; height:3px; margin:5px 0 12px 0; }
.bf { height:3px; border-radius:2px; }

/* SUGGESTION */
.sug  { background:#080f1e; border:1px solid #0d1a2e; border-radius:8px; padding:15px 17px; margin-bottom:8px; }
.sug-h{ border-left:3px solid #ef4444; }
.sug-m{ border-left:3px solid #f59e0b; }
.sug-l{ border-left:3px solid #10b981; }
.stit { font-family:'Syne',sans-serif; font-size:14px; font-weight:700; color:#e2e8f0; margin:0 0 4px 0; }
.sbod { font-size:12px; color:#334155; margin:0; line-height:1.65; }
.imp  { display:inline-block; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; padding:2px 7px; border-radius:2px; margin-left:8px; vertical-align:middle; }
.i-h  { background:#1a0505; color:#ef4444; }
.i-m  { background:#1c1000; color:#f59e0b; }
.i-l  { background:#041810; color:#10b981; }

/* CMP */
.cmp  { display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid #0d1a2e; }
.cl   { font-size:11px; color:#1e3a5f; width:130px; flex-shrink:0; text-transform:uppercase; letter-spacing:0.07em; font-weight:700; }
.co   { font-family:'DM Mono',monospace; font-size:13px; color:#1e3a5f; width:75px; }
.ca   { font-size:11px; color:#334155; }
.cu   { font-family:'DM Mono',monospace; font-size:13px; color:#10b981; font-weight:500; }
.cd   { font-family:'DM Mono',monospace; font-size:13px; color:#ef4444; font-weight:500; }
.ce   { font-family:'DM Mono',monospace; font-size:13px; color:#475569; font-weight:500; }

/* LB ROW */
.lb   { display:flex; align-items:center; gap:12px; padding:11px 14px; border-radius:8px; margin-bottom:5px; border:1px solid #0d1a2e; background:#080f1e; }
.lr   { font-family:'DM Mono',monospace; font-size:12px; color:#1e3a5f; width:26px; }
.ln   { flex:1; font-size:13px; color:#94a3b8; }
.ll   { font-size:10px; color:#1e3a5f; margin-right:8px; text-transform:uppercase; letter-spacing:0.07em; }
.ls   { font-family:'DM Mono',monospace; font-size:17px; color:#10b981; font-weight:500; }

/* LEND/BORROW ROW */
.txn  { display:flex; align-items:center; gap:10px; padding:11px 14px; border-radius:7px; margin-bottom:5px; background:#050a14; border:1px solid #0d1a2e; }
.tg   { border-left:3px solid #10b981; }
.to   { border-left:3px solid #ef4444; }

/* COMMUNITY POST */
.post { background:#080f1e; border:1px solid #0d1a2e; border-radius:8px; padding:15px 18px; margin-bottom:10px; }
.ptop { font-size:10px; color:#334155; text-transform:uppercase; letter-spacing:0.1em; font-weight:700; display:inline-block; background:#050a14; border:1px solid #0d1a2e; padding:2px 8px; border-radius:3px; margin-bottom:8px; }
.paut { font-size:12px; color:#475569; margin-bottom:6px; }
.ptxt { font-size:13px; color:#94a3b8; line-height:1.65; }
.pft  { font-size:11px; color:#1e3a5f; margin-top:8px; }

/* MODULE */
.mod  { background:#080f1e; border:1px solid #0d1a2e; border-radius:8px; padding:15px 18px; margin-bottom:8px; cursor:pointer; }
.mod-done { border-color:#064e35 !important; background:#041810 !important; }
.mtit { font-family:'Syne',sans-serif; font-size:14px; font-weight:700; color:#e2e8f0; margin:0 0 4px 0; }
.mmeta{ font-size:11px; color:#334155; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background:#080f1e !important; border-bottom:1px solid #0d1a2e !important; gap:0 !important; padding:0 !important; border-radius:0 !important; }
.stTabs [data-baseweb="tab"]      { background:transparent !important; color:#1e3a5f !important; font-size:11px !important; font-weight:700 !important; padding:13px 16px !important; border-radius:0 !important; border-bottom:2px solid transparent !important; letter-spacing:0.1em; text-transform:uppercase; font-family:'Mulish',sans-serif !important; }
.stTabs [aria-selected="true"]    { background:transparent !important; color:#10b981 !important; border-bottom:2px solid #10b981 !important; }
[data-testid="stTabPanel"]        { background:transparent !important; padding-top:18px !important; }

/* INPUTS */
.stNumberInput input, .stTextInput input { background:#050a14 !important; border:1px solid #0d1a2e !important; border-radius:7px !important; color:#e2e8f0 !important; font-family:'DM Mono',monospace !important; }
.stNumberInput input:focus, .stTextInput input:focus { border-color:#10b981 !important; }
[data-baseweb="select"] > div { background:#050a14 !important; border:1px solid #0d1a2e !important; border-radius:7px !important; }
[data-baseweb="select"] span  { color:#e2e8f0 !important; }
label { font-size:10px !important; font-weight:700 !important; color:#1e3a5f !important; text-transform:uppercase !important; letter-spacing:0.1em !important; }
.stTextArea textarea { background:#050a14 !important; border:1px solid #0d1a2e !important; border-radius:7px !important; color:#e2e8f0 !important; font-size:13px !important; }

/* BUTTON */
.stButton > button { background:#10b981 !important; color:#020c07 !important; border:none !important; border-radius:7px !important; font-weight:800 !important; font-size:11px !important; letter-spacing:0.1em !important; text-transform:uppercase !important; padding:11px 18px !important; font-family:'Mulish',sans-serif !important; width:100% !important; transition:all 0.15s !important; }
.stButton > button:hover { background:#059669 !important; box-shadow:0 0 16px rgba(16,185,129,0.2) !important; transform:translateY(-1px) !important; }

/* METRICS */
[data-testid="metric-container"]          { background:#050a14 !important; border:1px solid #0d1a2e !important; border-radius:8px !important; padding:13px 15px !important; }
[data-testid="stMetricLabel"]             { font-size:10px !important; color:#1e3a5f !important; text-transform:uppercase !important; letter-spacing:0.1em !important; }
[data-testid="stMetricValue"]             { font-family:'DM Mono',monospace !important; font-size:19px !important; color:#e2e8f0 !important; }

/* SLIDER */
[data-testid="stSlider"] > div > div > div > div { background:#10b981 !important; }
[data-testid="stSlider"] > div > div > div        { background:#0d1a2e !important; }

/* CHECKBOX */
.stCheckbox > label > div { border-color:#0d1a2e !important; background:#050a14 !important; }

/* PLOTLY */
.js-plotly-plot .plotly { background:transparent !important; }

::-webkit-scrollbar { width:3px; background:#050a14; }
::-webkit-scrollbar-thumb { background:#0d1a2e; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════
def ring(score, size=130):
    r   = 44
    c   = 2 * 3.14159 * r
    d   = round(score / 100 * c, 1)
    g   = round(c - d, 1)
    col = "#10b981" if score >= 65 else ("#f59e0b" if score >= 35 else "#ef4444")
    return (f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 100 100">'
            f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="#0d1a2e" stroke-width="7"/>'
            f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="{col}" stroke-width="7"'
            f' stroke-dasharray="{d} {g}" stroke-dashoffset="{c*0.25}" stroke-linecap="round"/>'
            f'<text x="50" y="46" text-anchor="middle" font-family="DM Mono,monospace"'
            f' font-size="20" font-weight="500" fill="#e2e8f0">{score:.0f}</text>'
            f'<text x="50" y="61" text-anchor="middle" font-family="Mulish,sans-serif"'
            f' font-size="9" fill="#1e3a5f" letter-spacing="1">SCORE</text>'
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

def sec(title):
    st.markdown(f'<span class="lbl">{title}</span>', unsafe_allow_html=True)

def cmp_row(label, before, after, fmt=None, hb=True):
    b = fmt(before) if fmt else f"{before:.1f}"
    a = fmt(after)  if fmt else f"{after:.1f}"
    d = after - before
    if   abs(d) < 0.05:        cls = "ce"
    elif (d > 0) == hb:        cls = "cu"
    else:                       cls = "cd"
    return (f'<div class="cmp"><span class="cl">{label}</span>'
            f'<span class="co">{b}</span><span class="ca">&#8594;</span>'
            f'<span class="{cls}">{a}</span></div>')

def plotly_cfg():
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor":  "rgba(0,0,0,0)",
        "font":          {"color": "#475569", "family": "Mulish", "size": 11},
        "margin":        {"l": 10, "r": 10, "t": 30, "b": 10},
        "xaxis":         {"gridcolor": "#0d1a2e", "linecolor": "#0d1a2e", "tickfont": {"color":"#334155"}},
        "yaxis":         {"gridcolor": "#0d1a2e", "linecolor": "#0d1a2e", "tickfont": {"color":"#334155"}},
    }

# ══════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════
for k, v in {
    "logged_in": False, "username": "", "persona_name": "💼 Working Professional",
    "last_result": None, "last_income": 50000.0,
    "last_expenses": 35000.0, "last_savings": 120000.0,
    "challenges_done": set(), "daily_budget": 1000.0, "streak": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════
# LOGIN SCREEN
# ══════════════════════════════════════════════
if not st.session_state.logged_in:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:28px;">
          <div style="font-family:Syne,sans-serif;font-size:36px;font-weight:800;
                      color:#e2e8f0;letter-spacing:-1px;">
            FIN<span style="color:#10b981;">VERSE</span></div>
          <div style="font-size:11px;color:#1e3a5f;letter-spacing:0.22em;
                      text-transform:uppercase;margin-top:4px;">Financial Safety Platform</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Your Name")
        name_in = st.text_input("name", placeholder="e.g. Aashi", label_visibility="collapsed")

        sec("Profile Type")
        persona_in = st.selectbox("persona", list(PERSONAS.keys()), index=1, label_visibility="collapsed")

        col_a, col_b = st.columns(2)
        with col_a:
            age_in  = st.number_input("Age", min_value=16, max_value=70, value=25, step=1)
        with col_b:
            city_in = st.text_input("City", placeholder="e.g. Delhi")

        if st.button("ENTER FINVERSE"):
            if name_in.strip():
                un = name_in.strip()
                upsert_user_profile(un, un, persona_in, int(age_in), city_in)
                settings = get_user_settings(un)
                st.session_state.update({
                    "logged_in":      True,
                    "username":       un,
                    "persona_name":   persona_in,
                    "daily_budget":   settings["daily_budget"],
                    "streak":         settings["streak"],
                    "challenges_done": get_completed_challenges(un),
                })
                st.rerun()
            else:
                st.warning("Enter your name to continue.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Platform stats
        stats = get_platform_stats()
        if stats["total_users"] > 0:
            st.markdown(
                f"<div style='text-align:center;margin-top:16px;'>"
                f"<span style='font-size:12px;color:#1e3a5f;'>"
                f"{stats['total_users']} users · "
                f"avg score {stats['avg_score']:.0f} · "
                f"{stats['total_scores']} calculations done"
                f"</span></div>",
                unsafe_allow_html=True,
            )
    st.stop()

# ══════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════
un      = st.session_state.username
persona = PERSONAS[st.session_state.persona_name]

# ── SIDEBAR ──────────────────────────────────
with st.sidebar:
    st.markdown(
        f"<div style='background:#050a14;border:1px solid #0d1a2e;border-radius:8px;"
        f"padding:12px 14px;margin-bottom:16px;'>"
        f"<div style='font-size:9px;color:#1e3a5f;text-transform:uppercase;"
        f"letter-spacing:0.14em;'>Signed in as</div>"
        f"<div style='font-family:Syne,sans-serif;font-size:17px;font-weight:700;"
        f"color:#10b981;margin-top:2px;'>{un}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    new_persona = st.selectbox(
        "Profile", list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.persona_name),
        label_visibility="collapsed",
    )
    if new_persona != st.session_state.persona_name:
        st.session_state.persona_name = new_persona
        persona = PERSONAS[new_persona]
        upsert_user_profile(un, persona=new_persona)

    p = PERSONAS[st.session_state.persona_name]
    st.markdown(
        f"<div style='background:#050a14;border:1px solid #0d1a2e;border-radius:8px;"
        f"padding:13px 15px;margin:12px 0;'>"
        f"<div style='font-size:9px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;'>Savings Target</div>"
        f"<div style='font-family:DM Mono,monospace;font-size:19px;color:#e2e8f0;margin:2px 0 10px 0;'>{p['savings_rate_target']}%</div>"
        f"<div style='font-size:9px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;'>Emergency Goal</div>"
        f"<div style='font-family:DM Mono,monospace;font-size:19px;color:#e2e8f0;margin-top:2px;'>{p['survival_target']} months</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    for tip in p["tips"]:
        st.markdown(
            f"<p style='font-size:11px;color:#334155;margin:0 0 7px 0;line-height:1.5;"
            f"padding-left:8px;border-left:2px solid #0d1a2e;'>{tip}</p>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border-color:#0d1a2e;margin:14px 0;'>", unsafe_allow_html=True)

    xp = get_total_xp(st.session_state.get("challenges_done", set()))
    settings = get_user_settings(un)
    st.markdown(
        f"<div style='background:#050a14;border:1px solid #0d1a2e;border-radius:8px;"
        f"padding:13px;text-align:center;'>"
        f"<div style='font-family:DM Mono,monospace;font-size:30px;font-weight:500;color:#10b981;'>{xp}</div>"
        f"<div style='font-size:9px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.12em;margin-top:2px;'>XP Earned</div>"
        f"<div style='font-size:10px;color:#1e3a5f;margin-top:6px;'>Streak: {settings['streak']} days</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border-color:#0d1a2e;margin:14px 0;'>", unsafe_allow_html=True)
    if st.button("SIGN OUT"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.markdown(
        "<p style='font-size:10px;color:#0d1a2e;text-align:center;margin-top:12px;'>"
        "Finverse v6.0 · Not financial advice</p>",
        unsafe_allow_html=True,
    )

# ── HEADER ───────────────────────────────────
st.markdown("""
<div style="padding:18px 0 18px 0;border-bottom:1px solid #0d1a2e;margin-bottom:22px;">
  <div style="font-family:Syne,sans-serif;font-size:20px;font-weight:800;
              color:#e2e8f0;letter-spacing:-0.3px;">
    FIN<span style="color:#10b981;">VERSE</span></div>
  <div style="font-size:10px;color:#1e3a5f;letter-spacing:0.18em;text-transform:uppercase;margin-top:1px;">
    Financial Safety Platform</div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
(tab_score, tab_dash, tab_wi, tab_sug, tab_track,
 tab_lb_, tab_part, tab_learn, tab_comm, tab_ins) = st.tabs([
    "Score", "Dashboard", "What-If", "Suggestions",
    "Tracker", "Lend/Borrow", "Partner",
    "Learn", "Community", "Insights",
])


# ════════════════════════════════════════════
# TAB — SCORE
# ════════════════════════════════════════════
with tab_score:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Monthly Snapshot")
    c1, c2 = st.columns(2)
    with c1:
        income   = st.number_input(persona["income_label"], min_value=0.0, value=50000.0, step=1000.0, key="s_inc")
        savings  = st.number_input("Total Savings (INR)",   min_value=0.0, value=120000.0, step=5000.0, key="s_sav")
    with c2:
        expenses = st.number_input("Monthly Expenses (INR)", min_value=0.0, value=35000.0, step=1000.0, key="s_exp")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("CALCULATE SAFETY SCORE", key="s_calc"):
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

        # Score card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        r1, r2 = st.columns([1, 2])
        with r1:
            st.markdown(ring(score), unsafe_allow_html=True)
        with r2:
            if next_l:
                nh = (f"<div style='font-size:11px;color:#1e3a5f;margin-top:6px;'>"
                      f"{next_l['points_needed']} pts to {next_l['name']}</div>")
            else:
                nh = ""
            st.markdown(
                f"<div style='padding:4px 0;'>{level_tag(lv['name'])}"
                f"<div style='font-family:Syne,sans-serif;font-size:22px;font-weight:700;"
                f"color:#e2e8f0;margin:8px 0 5px 0;line-height:1.2;'>{lv['message']}</div>"
                f"{risk_tag(risk)}"
                f"<div style='font-size:12px;color:#334155;margin-top:7px;'>{get_risk_advice(risk)}</div>"
                f"{nh}</div>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Stress score
        s_label, s_color = get_stress_label(stress)
        st.markdown(
            f"<div class='card2'>"
            f"<span class='lbl'>Financial Stress Score</span>"
            f"<div style='display:flex;align-items:center;gap:16px;'>"
            f"<div style='font-family:DM Mono,monospace;font-size:38px;font-weight:500;color:{s_color};'>{stress}</div>"
            f"<div><div style='font-size:13px;font-weight:700;color:{s_color};'>{s_label}</div>"
            f"<div style='font-size:11px;color:#334155;margin-top:3px;'>Lower is better. 0 = no stress.</div></div>"
            f"</div>"
            f"<div style='margin-top:10px;'>{bar(stress, s_color)}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Key metrics
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
            f"<div class='sk'>Survival Time</div><div class='sn'>{get_survival_message(sm)}</div></div>"
            f"<div class='sb'><div class='sv' style='color:{erc};'>{er:.1f}%</div>"
            f"<div class='sk'>Expense Ratio</div><div class='sn'>of income on expenses</div></div>"
            f"</div>"
            f"{bar(min(100,int(sr/30*100)),sc)}"
            f"{bar(min(100,int(sm/12*100)),smc)}"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Monthly picture
        surplus = income - expenses
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Monthly Picture")
        m1, m2, m3 = st.columns(3)
        m1.metric("Income",   format_currency(income))
        m2.metric("Expenses", format_currency(expenses))
        m3.metric("Surplus" if surplus >= 0 else "Deficit", format_currency(abs(surplus)),
                  delta_color="normal" if surplus >= 0 else "inverse")
        st.markdown('</div>', unsafe_allow_html=True)

        # Badges
        if bdgs:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("Achievements")
            st.markdown(
                "".join(f'<span style="display:inline-block;background:#080f1e;border:1px solid #0d1a2e;'
                        f'border-radius:4px;padding:4px 10px;font-size:11px;font-weight:700;'
                        f'color:#475569;margin:3px;letter-spacing:0.04em;text-transform:uppercase;">'
                        f'{b["name"].split(" ",1)[-1]}</span>' for b in bdgs),
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Score history
        history = get_score_history(un, 5)
        if len(history) > 1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("Score History")
            for h in history:
                col = "#10b981" if h["risk_level"]=="SAFE" else ("#f59e0b" if h["risk_level"]=="MODERATE" else "#ef4444")
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:7px 0;border-bottom:1px solid #0d1a2e;'>"
                    f"<span style='font-size:11px;color:#1e3a5f;font-family:DM Mono,monospace;'>{h['created_at'][:10]}</span>"
                    f"<span style='font-size:11px;color:#334155;'>{h['persona'].split()[-1]}</span>"
                    f"<span style='font-family:DM Mono,monospace;font-size:16px;color:{col};'>{h['score']:.1f}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        # Challenges
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Active Challenges")
        for ch in get_challenges():
            done = ch["id"] in st.session_state.get("challenges_done", set())
            ca, cb = st.columns([5, 1])
            op = "opacity:0.35;" if done else ""
            with ca:
                st.markdown(
                    f"<div style='{op}background:#050a14;border:1px solid #0d1a2e;"
                    f"border-radius:7px;padding:10px 13px;margin-bottom:4px;'>"
                    f"<div style='font-size:13px;color:#94a3b8;font-weight:600;"
                    f"{'text-decoration:line-through;' if done else ''}'>{ch['name']}</div>"
                    f"<div style='font-size:11px;color:#1e3a5f;margin-top:2px;'>"
                    f"{ch['desc']} &nbsp;+{ch['reward_xp']} XP</div></div>",
                    unsafe_allow_html=True,
                )
            with cb:
                if not done:
                    if st.button("Done", key=f"ch_{ch['id']}"):
                        save_challenge(un, ch["id"])
                        st.session_state.challenges_done.add(ch["id"])
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:52px 28px;">
          <div style="font-family:DM Mono,monospace;font-size:50px;color:#0d1a2e;
                      font-weight:500;letter-spacing:-2px;line-height:1;">--</div>
          <div style="font-family:Syne,sans-serif;font-size:17px;font-weight:700;
                      color:#1e3a5f;margin-top:12px;">Enter your numbers above</div>
          <div style="font-size:12px;color:#0d1a2e;margin-top:4px;">
              Financial safety score, stress score, and achievements appear here</div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB — DASHBOARD
# ════════════════════════════════════════════
with tab_dash:
    score_hist = get_score_history(un, 30)
    spend_trend = get_spending_trend(un, 30)
    monthly_exp = get_monthly_expenses(un)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Financial Dashboard")
    p_stats = get_platform_stats()
    ds1, ds2, ds3, ds4 = st.columns(4)
    ds1.metric("Platform Users",  p_stats["total_users"])
    ds2.metric("Avg Score",       f"{p_stats['avg_score']:.1f}")
    ds3.metric("Safe Users",      p_stats["safe_count"])
    ds4.metric("High Risk Users", p_stats["risky_count"])
    st.markdown('</div>', unsafe_allow_html=True)

    if not PLOTLY:
        st.warning("Install plotly for charts: pip install plotly")
    elif score_hist:
        # Score trend
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Your Score Trend")
        d = build_score_trend_data(score_hist)
        if len(d["dates"]) > 1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=d["dates"], y=d["scores"],
                mode="lines+markers",
                line={"color":"#10b981","width":2},
                marker={"color":"#10b981","size":6},
                fill="tozeroy",
                fillcolor="rgba(16,185,129,0.06)",
            ))
            fig.update_layout(**plotly_cfg(), height=220)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            st.markdown("<p style='font-size:12px;color:#334155;'>Calculate your score more than once to see the trend.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Stress trend
        stress_vals = [h.get("stress_score", 0) for h in score_hist]
        if any(v > 0 for v in stress_vals):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("Financial Stress Trend")
            dates = [h["created_at"][:10] for h in reversed(score_hist)]
            svals = list(reversed(stress_vals))
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=dates, y=svals,
                mode="lines+markers",
                line={"color":"#ef4444","width":2},
                marker={"color":"#ef4444","size":6},
                fill="tozeroy",
                fillcolor="rgba(239,68,68,0.06)",
            ))
            fig2.update_layout(**plotly_cfg(), height=200)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

    if PLOTLY and spend_trend:
        # Spending trend
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Daily Spending — Last 30 Days")
        d = build_expense_trend_data(spend_trend)
        fig3 = go.Figure(go.Bar(
            x=d["dates"], y=d["amounts"],
            marker_color="#10b981",
            opacity=0.8,
        ))
        fig3.update_layout(**plotly_cfg(), height=220)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    if PLOTLY and monthly_exp:
        # Category pie
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Spending by Category — This Month")
        d = build_category_data(monthly_exp)
        fig4 = go.Figure(go.Pie(
            labels=d["categories"], values=d["totals"],
            hole=0.55,
            marker={"colors":["#10b981","#3b82f6","#f59e0b","#ef4444","#8b5cf6","#ec4899","#14b8a6","#f97316"]},
            textfont={"color":"#94a3b8","size":11},
        ))
        fig4.update_layout(**plotly_cfg(), height=280, showlegend=True,
                           legend={"font":{"color":"#475569"}})
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Savings prediction chart
    if st.session_state.last_result and PLOTLY:
        surplus = st.session_state.last_income - st.session_state.last_expenses
        if surplus > 0:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("12-Month Savings Projection")
            d = build_prediction_data(st.session_state.last_savings, surplus)
            fig5 = go.Figure()
            fig5.add_trace(go.Scatter(
                x=d["months"], y=d["savings"],
                mode="lines+markers",
                line={"color":"#3b82f6","width":2,"dash":"dot"},
                marker={"color":"#3b82f6","size":5},
                fill="tozeroy",
                fillcolor="rgba(59,130,246,0.06)",
            ))
            fig5.update_layout(**plotly_cfg(), height=200)
            st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

    if not score_hist and not spend_trend:
        st.markdown(
            "<div class='card' style='text-align:center;padding:40px;color:#1e3a5f;'>"
            "Calculate your score and log expenses to populate the dashboard.</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# TAB — WHAT-IF
# ════════════════════════════════════════════
with tab_wi:
    if not st.session_state.last_result:
        st.markdown('<div class="card" style="text-align:center;padding:40px;color:#1e3a5f;">Calculate your score in the Score tab first.</div>', unsafe_allow_html=True)
    else:
        base = st.session_state.last_result
        bi   = st.session_state.last_income
        be   = st.session_state.last_expenses
        bs   = st.session_state.last_savings

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Adjust Scenario")
        st.markdown('<p style="font-size:12px;color:#334155;margin:0 0 14px 0;">Move sliders to see instant impact — no recalculation needed.</p>', unsafe_allow_html=True)
        id_ = st.slider("Income change per month (INR)",  -20000, 50000,  0, 1000)
        ed_ = st.slider("Expense change per month (INR)", -20000, 20000,  0,  500)
        sd_ = st.slider("Extra savings added (INR)",           0, 500000, 0, 5000)
        st.markdown('</div>', unsafe_allow_html=True)

        nr   = calculate_whatif(bi, be, bs, {"income_delta":id_,"expenses_delta":ed_,"savings_delta":sd_})
        ns   = nr["composite_score"];  os_ = base["composite_score"];  diff = ns - os_
        dc   = "#10b981" if diff >= 0 else "#ef4444"

        ra, rb = st.columns(2)
        with ra:
            st.markdown(f'<div class="card" style="text-align:center;"><span class="lbl" style="display:block;text-align:center;">Current</span>{ring(os_,118)}<div style="margin-top:10px;">{risk_tag(base["risk_level"])}</div></div>', unsafe_allow_html=True)
        with rb:
            arrow = "+" if diff >= 0 else ""
            st.markdown(f'<div class="card" style="text-align:center;"><span class="lbl" style="display:block;text-align:center;">New Scenario</span>{ring(ns,118)}<div style="margin-top:10px;">{risk_tag(nr["risk_level"])}</div><div style="font-family:DM Mono,monospace;font-size:15px;color:{dc};margin-top:8px;font-weight:500;">{arrow}{diff:.1f} pts</div></div>', unsafe_allow_html=True)

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

        if   diff > 10: st.success(f"+{diff:.1f} points — moves to {nr['risk_level']}.")
        elif diff > 0:  st.info(f"Small improvement of {diff:.1f} points.")
        elif diff < -10:st.error(f"{diff:.1f} points — drops to {nr['risk_level']}.")
        elif diff < 0:  st.warning(f"Small decline of {abs(diff):.1f} points.")
        else:           st.info("No meaningful change.")


# ════════════════════════════════════════════
# TAB — SUGGESTIONS
# ════════════════════════════════════════════
with tab_sug:
    if not st.session_state.last_result:
        st.markdown('<div class="card" style="text-align:center;padding:40px;color:#1e3a5f;">Calculate your score in the Score tab first.</div>', unsafe_allow_html=True)
    else:
        suggs = generate_suggestions(
            st.session_state.last_income,
            st.session_state.last_expenses,
            st.session_state.last_savings,
            st.session_state.last_result,
        )
        st.markdown(
            "<div style='margin-bottom:18px;'>"
            "<div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#e2e8f0;'>Action Plan</div>"
            "<div style='font-size:12px;color:#334155;margin-top:3px;'>Ranked by impact. Work top to bottom.</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        order = {"High":0,"Medium":1,"Low":2}
        for s in sorted(suggs, key=lambda x: order.get(x["impact"],3)):
            cls  = {"High":"sug-h","Medium":"sug-m","Low":"sug-l"}[s["impact"]]
            icls = {"High":"i-h","Medium":"i-m","Low":"i-l"}[s["impact"]]
            st.markdown(
                f'<div class="sug {cls}"><div class="stit">{s["title"]}'
                f'<span class="imp {icls}">{s["impact"]}</span></div>'
                f'<div class="sbod">{s["detail"]}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            "<div style='border-left:3px solid #10b981;padding:14px 18px;background:#041810;"
            "border-radius:0 8px 8px 0;margin-top:14px;'>"
            "<div style='font-family:Syne,sans-serif;font-size:15px;font-weight:700;"
            "color:#e2e8f0;margin-bottom:6px;'>Save first. Spend what remains.</div>"
            "<div style='font-size:12px;color:#334155;line-height:1.65;'>"
            "Most people spend first. Whatever is left — usually nothing — becomes savings. "
            "Flip it. Automate savings on salary day. Your spending adjusts automatically.</div>"
            "</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# TAB — TRACKER
# ════════════════════════════════════════════
with tab_track:
    s = get_user_settings(un)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Daily Tracker")
    h1, h2, h3 = st.columns(3)
    h1.metric("Streak",         f"{s['streak']} days")
    h2.metric("Today's Budget", format_currency(s["daily_budget"]))
    with h3:
        nb = st.number_input("Update Daily Budget", min_value=0.0, value=float(s["daily_budget"]), step=100.0)
        if nb != s["daily_budget"]:
            save_user_settings(un, nb, s["streak"], s["last_tracked"])
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Add expense
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Add Expense")
    tc1, tc2, tc3, tc4 = st.columns([2, 2, 2, 3])
    with tc1:
        cat = st.selectbox("Category", ["Food","Transport","Shopping","Bills","Entertainment","Health","Education","Other"])
    with tc2:
        amt = st.number_input("Amount (INR)", min_value=0.0, value=0.0, step=10.0)
    with tc3:
        exp_date = st.date_input("Date", value=date.today())
    with tc4:
        note = st.text_input("Note", placeholder="e.g. Lunch at office")
    if st.button("ADD EXPENSE", key="add_exp"):
        if amt > 0:
            save_expense(un, cat, float(amt), note, str(exp_date))
            st.success(f"Added: {cat} — {format_currency(amt)}")
            st.rerun()
        else:
            st.warning("Enter an amount greater than zero.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Today's list
    today_exps = get_today_expenses(un)
    budget     = s["daily_budget"]

    if today_exps:
        total  = sum(e["amount"] for e in today_exps)
        left   = budget - total
        pct    = min(100, int(total / budget * 100)) if budget > 0 else 100
        bc     = "#10b981" if pct < 70 else ("#f59e0b" if pct < 90 else "#ef4444")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Today")
        d1, d2, d3 = st.columns(3)
        d1.metric("Spent",      format_currency(total))
        d2.metric("Budget",     format_currency(budget))
        d3.metric("Remaining" if left >= 0 else "Over Budget", format_currency(abs(left)),
                  delta_color="normal" if left >= 0 else "inverse")
        st.markdown(bar(pct, bc), unsafe_allow_html=True)
        if pct >= 90: st.error("Approaching daily limit.")
        elif pct >= 70: st.warning("High spending today.")
        else: st.success("On track.")

        st.markdown("<hr style='border-color:#0d1a2e;margin:12px 0;'>", unsafe_allow_html=True)
        sec("Expense Log — click Delete to remove")

        for exp in reversed(today_exps):
            ec1, ec2, ec3, ec4, ec5 = st.columns([2, 3, 2, 2, 1])
            with ec1:
                st.markdown(f"<span style='font-size:11px;color:#334155;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;'>{exp['category']}</span>", unsafe_allow_html=True)
            with ec2:
                st.markdown(f"<span style='font-size:12px;color:#475569;'>{exp['note']}</span>", unsafe_allow_html=True)
            with ec3:
                st.markdown(f"<span style='font-family:DM Mono,monospace;font-size:11px;color:#1e3a5f;'>{exp['created_at'][11:16]}</span>", unsafe_allow_html=True)
            with ec4:
                st.markdown(f"<span style='font-family:DM Mono,monospace;font-size:14px;color:#e2e8f0;'>{format_currency(exp['amount'])}</span>", unsafe_allow_html=True)
            with ec5:
                if st.button("Delete", key=f"del_{exp['id']}"):
                    delete_expense(exp["id"])
                    st.rerun()

        st.markdown("<hr style='border-color:#0d1a2e;margin:12px 0;'>", unsafe_allow_html=True)
        if st.button("END DAY — SAVE STREAK", use_container_width=True):
            new_streak = end_day_update_streak(un)
            st.success(f"Day saved. Streak: {new_streak} days.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Monthly breakdown
        monthly = get_monthly_expenses(un)
        if monthly:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sec("This Month")
            mt = sum(r["total"] for r in monthly)
            for row in monthly:
                p = int(row["total"] / mt * 100) if mt > 0 else 0
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;'>"
                    f"<span style='color:#475569;text-transform:uppercase;letter-spacing:0.06em;font-size:10px;'>"
                    f"{row['category']}<span style='color:#1e3a5f;margin-left:5px;'>({row['count']})</span></span>"
                    f"<span style='font-family:DM Mono,monospace;color:#94a3b8;'>{format_currency(row['total'])}</span></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(bar(p, "#0d1a2e"), unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-family:DM Mono,monospace;font-size:15px;color:#e2e8f0;"
                f"margin-top:10px;border-top:1px solid #0d1a2e;padding-top:10px;'>"
                f"Total this month: {format_currency(mt)}</div>",
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card" style="text-align:center;padding:36px;color:#1e3a5f;">No expenses logged today. Add one above.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB — LEND / BORROW
# ════════════════════════════════════════════
with tab_lb_:
    summary = get_lend_borrow_summary(un)

    # Summary strip
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Lend / Borrow Tracker")
    ls1, ls2, ls3 = st.columns(3)
    ls1.metric("You Are Owed",    format_currency(summary["total_gave"]), "you gave")
    ls2.metric("You Owe Others",  format_currency(summary["total_owe"]),  "you borrowed")
    ls3.metric("Net Position",    format_currency(abs(summary["net"])),
               "in your favour" if summary["net"] >= 0 else "you owe net")
    st.markdown('</div>', unsafe_allow_html=True)

    # Add transaction
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Add Transaction")
    la1, la2, la3 = st.columns([2, 2, 2])
    with la1:
        party   = st.text_input("Person's Name", placeholder="e.g. Rahul")
    with la2:
        l_amt   = st.number_input("Amount (INR)", min_value=0.0, value=0.0, step=100.0, key="l_amt")
    with la3:
        txn_type = st.selectbox("Type", ["I Gave (they owe me)", "I Owe (I borrowed)"])

    lb1_c, lb2_c = st.columns(2)
    with lb1_c:
        desc     = st.text_input("Description", placeholder="e.g. Dinner split")
    with lb2_c:
        due_date = st.date_input("Due Date (optional)", value=None)

    if st.button("ADD TRANSACTION", key="add_lb"):
        if party.strip() and l_amt > 0:
            t = "gave" if "Gave" in txn_type else "owe"
            dd = str(due_date) if due_date else None
            add_lend_borrow(un, party.strip(), float(l_amt), t, desc, dd)
            st.success(f"Recorded: {txn_type} {format_currency(l_amt)} with {party}")
            st.rerun()
        else:
            st.warning("Enter a name and amount.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Transaction list
    all_txns = get_lend_borrow(un)
    pending  = [t for t in all_txns if t["status"] == "pending"]
    settled  = [t for t in all_txns if t["status"] == "settled"]

    if pending:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Pending Transactions")
        for txn in pending:
            is_gave = txn["txn_type"] == "gave"
            color   = "#10b981" if is_gave else "#ef4444"
            label   = "They owe you" if is_gave else "You owe them"
            due_str = f" · Due: {txn['due_date']}" if txn["due_date"] else ""

            t1, t2, t3, t4 = st.columns([3, 2, 2, 1])
            with t1:
                st.markdown(
                    f"<div style='font-size:13px;color:#94a3b8;font-weight:600;'>{txn['party_name']}</div>"
                    f"<div style='font-size:11px;color:#334155;'>{txn['description']}{due_str}</div>",
                    unsafe_allow_html=True,
                )
            with t2:
                st.markdown(
                    f"<span style='font-family:DM Mono,monospace;font-size:15px;color:{color};'>"
                    f"{format_currency(txn['amount'])}</span>",
                    unsafe_allow_html=True,
                )
            with t3:
                st.markdown(f"<span style='font-size:11px;color:#475569;'>{label}</span>", unsafe_allow_html=True)
            with t4:
                if st.button("Settle", key=f"set_{txn['id']}"):
                    settle_lend_borrow(txn["id"])
                    st.rerun()

            # Reminder message
            with st.expander(f"Send Reminder to {txn['party_name']}"):
                if is_gave:
                    msg = (f"Hi {txn['party_name']}, just a friendly reminder that "
                           f"you owe me {format_currency(txn['amount'])}."
                           f"{' It was due on ' + txn['due_date'] + '.' if txn['due_date'] else ''} "
                           f"Please settle when convenient. Thanks!")
                else:
                    msg = (f"Hi {txn['party_name']}, reminding myself that I owe you "
                           f"{format_currency(txn['amount'])}."
                           f"{' Due: ' + txn['due_date'] + '.' if txn['due_date'] else ''} "
                           f"Will pay you soon.")
                st.code(msg, language=None)
                st.caption("Copy and send on WhatsApp.")
        st.markdown('</div>', unsafe_allow_html=True)

    if settled:
        with st.expander(f"Settled Transactions ({len(settled)})"):
            for txn in settled:
                color = "#10b981" if txn["txn_type"]=="gave" else "#ef4444"
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;padding:7px 0;"
                    f"border-bottom:1px solid #0d1a2e;'>"
                    f"<span style='font-size:12px;color:#334155;'>{txn['party_name']} — {txn['description']}</span>"
                    f"<span style='font-family:DM Mono,monospace;font-size:13px;color:{color};"
                    f"text-decoration:line-through;'>{format_currency(txn['amount'])}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    if not all_txns:
        st.markdown('<div class="card" style="text-align:center;padding:36px;color:#1e3a5f;">No transactions yet. Add one above to start tracking who owes whom.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB — PARTNER
# ════════════════════════════════════════════
with tab_part:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Financial Compatibility")
    st.markdown('<p style="font-size:12px;color:#334155;margin:0 0 16px 0;">Compare two financial profiles for combined health, alignment, and ideal partner income.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;color:#1e3a5f;text-transform:uppercase;margin-bottom:8px;'>You</div>", unsafe_allow_html=True)
        p1i = st.number_input("Income",   min_value=0.0, value=50000.0, step=1000.0, key="p1i")
        p1e = st.number_input("Expenses", min_value=0.0, value=35000.0, step=1000.0, key="p1e")
        p1s = st.number_input("Savings",  min_value=0.0, value=120000.0,step=5000.0, key="p1s")
    with pc2:
        st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;color:#1e3a5f;text-transform:uppercase;margin-bottom:8px;'>Partner</div>", unsafe_allow_html=True)
        p2i = st.number_input("Income",   min_value=0.0, value=45000.0, step=1000.0, key="p2i")
        p2e = st.number_input("Expenses", min_value=0.0, value=30000.0, step=1000.0, key="p2e")
        p2s = st.number_input("Savings",  min_value=0.0, value=80000.0, step=5000.0, key="p2s")

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
            f"<div class='card' style='text-align:center;padding:30px;'>"
            f"<div style='font-family:DM Mono,monospace;font-size:58px;font-weight:500;color:{col};letter-spacing:-3px;line-height:1;'>{cs:.0f}</div>"
            f"<div style='font-family:Syne,sans-serif;font-size:17px;font-weight:700;color:#e2e8f0;margin-top:6px;'>{lbl}</div>"
            f"<div style='font-size:11px;color:#1e3a5f;margin-top:3px;'>out of 100</div></div>",
            unsafe_allow_html=True,
        )
        ia, ib, ic = st.columns(3)
        ia.metric("Your Score",    f"{r1['composite_score']} / 100")
        ib.metric("Partner Score", f"{r2['composite_score']} / 100")
        ic.metric("Alignment",     f"{compat['alignment_score']} / 100")
        combined = compat["combined"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Combined Picture")
        cf1, cf2, cf3, cf4 = st.columns(4)
        cf1.metric("Combined Income",  format_currency(combined["income"]))
        cf2.metric("Combined Savings", format_currency(combined["savings"]))
        cf3.metric("Survive Together", format_months(combined["survival_months"]))
        cf4.metric("Combined Score",   f"{combined['composite_score']} / 100")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Ideal Partner Income Calculator")
        t_sr = st.slider("Target Combined Savings Rate (%)", 10, 40, 20, key="tsr")
        rec  = recommended_partner_income(p1i, p1e, p1s, t_sr)
        ri1, ri2, ri3 = st.columns(3)
        ri1.metric("Min. Partner Income",     format_currency(rec["min_partner_income"]), "per month")
        ri2.metric("Emergency Fund Target",   format_currency(rec["target_combined_savings"]))
        ri3.metric("Partner Monthly Savings", format_currency(rec["partner_monthly_savings_target"]))
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB — LEARN
# ════════════════════════════════════════════
with tab_learn:
    progress = get_education_progress(un)
    done_ids = {mid for mid, done in progress.items() if done}
    total    = len(LEARNING_MODULES)
    done_ct  = len(done_ids)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Financial Education")
    lp1, lp2, lp3 = st.columns(3)
    lp1.metric("Modules Completed", f"{done_ct} / {total}")
    lp2.metric("XP from Learning",  f"{done_ct * 20} XP")
    lp3.metric("Progress",          f"{int(done_ct/total*100)}%")
    st.markdown(bar(int(done_ct/total*100), "#10b981"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    modules_by_level = get_modules_by_level()
    for level_name, modules in modules_by_level.items():
        level_color = {"Beginner":"#10b981","Intermediate":"#f59e0b","Advanced":"#ef4444"}.get(level_name,"#10b981")
        st.markdown(
            f"<div style='font-family:Syne,sans-serif;font-size:15px;font-weight:700;"
            f"color:{level_color};margin:18px 0 10px 0;letter-spacing:0.02em;'>{level_name}</div>",
            unsafe_allow_html=True,
        )
        for mod in modules:
            is_done  = mod["id"] in done_ids
            done_cls = "mod-done" if is_done else ""
            with st.expander(
                f"{'[Done] ' if is_done else ''}{mod['title']}  ·  {mod['duration']}",
                expanded=False,
            ):
                st.markdown(
                    f"<div style='font-size:13px;color:#64748b;line-height:1.75;'>{mod['content']}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='background:#041810;border:1px solid #064e35;border-radius:7px;"
                    f"padding:11px 14px;margin-top:12px;'>"
                    f"<div style='font-size:10px;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.1em;'>Key Takeaway</div>"
                    f"<div style='font-size:13px;color:#34d399;margin-top:4px;line-height:1.5;'>{mod['key_takeaway']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='margin-top:10px;font-size:12px;color:#334155;'>"
                    f"Recommended book: <span style='color:#94a3b8;font-weight:600;'>{mod['book']}</span></div>",
                    unsafe_allow_html=True,
                )
                if not is_done:
                    if st.button(f"Mark as Complete  +20 XP", key=f"mod_{mod['id']}"):
                        mark_module_complete(un, mod["id"])
                        st.success("Module complete! +20 XP earned.")
                        st.rerun()
                else:
                    st.markdown("<span style='font-size:11px;color:#10b981;'>Completed</span>", unsafe_allow_html=True)

    # Book list
    st.markdown(
        "<div style='font-family:Syne,sans-serif;font-size:15px;font-weight:700;"
        "color:#e2e8f0;margin:22px 0 12px 0;'>Reading List</div>",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="card">', unsafe_allow_html=True)
    for book in BOOK_LIST:
        level_color = {"Beginner":"#10b981","Intermediate":"#f59e0b","Advanced":"#ef4444"}.get(book["level"],"#10b981")
        st.markdown(
            f"<div style='padding:10px 0;border-bottom:1px solid #0d1a2e;'>"
            f"<div style='display:flex;justify-content:space-between;align-items:flex-start;'>"
            f"<div style='font-size:13px;color:#94a3b8;font-weight:600;'>{book['title']}</div>"
            f"<span style='font-size:9px;color:{level_color};text-transform:uppercase;letter-spacing:0.1em;"
            f"font-weight:700;white-space:nowrap;margin-left:10px;'>{book['level']}</span></div>"
            f"<div style='font-size:11px;color:#334155;margin-top:2px;'>by {book['author']}</div>"
            f"<div style='font-size:11px;color:#1e3a5f;margin-top:4px;line-height:1.5;'>{book['why']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB — COMMUNITY
# ════════════════════════════════════════════
with tab_comm:
    TOPICS = ["All", "Saving Tips", "Investing", "Debt", "Career & Income",
              "Students", "Budgeting", "General Finance"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Community — Finance Discussions")
    st.markdown(
        "<p style='font-size:12px;color:#334155;margin:0 0 12px 0;'>"
        "Ask questions, share tips, discuss finance. Be respectful. Stay on topic.</p>",
        unsafe_allow_html=True,
    )
    topic_filter = st.selectbox("Filter by topic", TOPICS)
    st.markdown('</div>', unsafe_allow_html=True)

    # New post
    with st.expander("Write a Post"):
        np_topic = st.selectbox("Topic", TOPICS[1:], key="np_topic")
        np_text  = st.text_area("Your post", placeholder="Share a tip, ask a question...", height=100)
        np_anon  = st.checkbox("Post anonymously")
        if st.button("POST", key="post_btn"):
            if np_text.strip():
                add_post(un, un, np_topic, np_text.strip(), np_anon)
                st.success("Posted.")
                st.rerun()
            else:
                st.warning("Write something before posting.")

    # Post list
    posts = get_posts(topic_filter if topic_filter != "All" else None, 30)
    if posts:
        for post in posts:
            is_mine = post["username"] == un
            st.markdown('<div class="post">', unsafe_allow_html=True)
            st.markdown(
                f'<span class="ptop">{post["topic"]}</span>'
                f'<div class="paut">{post["display_name"]} &nbsp;·&nbsp; {post["created_at"][:10]}</div>'
                f'<div class="ptxt">{post["content"]}</div>'
                f'<div class="pft">{post["upvotes"]} upvotes</div>',
                unsafe_allow_html=True,
            )
            ub1, ub2 = st.columns([1, 5])
            with ub1:
                if st.button("Upvote", key=f"up_{post['id']}"):
                    upvote_post(un, post["id"])
                    st.rerun()
            with ub2:
                if is_mine:
                    if st.button("Delete", key=f"dp_{post['id']}"):
                        delete_post(post["id"], un)
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='card' style='text-align:center;padding:36px;color:#1e3a5f;'>"
            "No posts yet in this topic. Be the first to write.</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# TAB — INSIGHTS
# ════════════════════════════════════════════
with tab_ins:
    score_hist = get_score_history(un, 30)
    monthly_exp = get_monthly_expenses(un)
    insights    = get_behavioral_insights(score_hist, monthly_exp)

    # Behavioral insights
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Behavioral Insights")
    for insight in insights:
        st.markdown(
            f"<div style='padding:10px 14px;border-left:3px solid #10b981;background:#041810;"
            f"border-radius:0 7px 7px 0;margin-bottom:8px;font-size:13px;color:#94a3b8;"
            f"line-height:1.6;'>{insight}</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Predictions
    if st.session_state.last_result:
        surplus       = st.session_state.last_income - st.session_state.last_expenses
        current_sav   = st.session_state.last_savings
        monthly_exp_v = st.session_state.last_expenses
        annual_exp    = monthly_exp_v * 12

        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Predictive Targets")
        ef_months = predict_emergency_fund_date(current_sav, surplus, monthly_exp_v, 6)
        fire_yrs  = predict_fire_date(current_sav, surplus, annual_exp)

        pr1, pr2 = st.columns(2)
        with pr1:
            if ef_months == 0:
                st.markdown(
                    "<div class='card-g'><div class='lbl'>6-Month Emergency Fund</div>"
                    "<div style='font-family:DM Mono,monospace;font-size:28px;color:#10b981;'>Done</div>"
                    "<div style='font-size:11px;color:#334155;margin-top:4px;'>You have already reached this target.</div></div>",
                    unsafe_allow_html=True,
                )
            elif ef_months:
                st.markdown(
                    f"<div class='card2'><div class='lbl'>6-Month Emergency Fund</div>"
                    f"<div style='font-family:DM Mono,monospace;font-size:28px;color:#f59e0b;'>{ef_months} months</div>"
                    f"<div style='font-size:11px;color:#334155;margin-top:4px;'>At current savings rate.</div></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='card-r'><div class='lbl'>6-Month Emergency Fund</div>"
                    "<div style='font-size:13px;color:#ef4444;'>Cannot reach at current rate.</div>"
                    "<div style='font-size:11px;color:#334155;margin-top:4px;'>Create a monthly surplus first.</div></div>",
                    unsafe_allow_html=True,
                )
        with pr2:
            if fire_yrs == 0:
                st.markdown(
                    "<div class='card-g'><div class='lbl'>FIRE Number</div>"
                    "<div style='font-family:DM Mono,monospace;font-size:28px;color:#10b981;'>Reached</div>"
                    "<div style='font-size:11px;color:#334155;margin-top:4px;'>Financial independence achieved.</div></div>",
                    unsafe_allow_html=True,
                )
            elif fire_yrs:
                st.markdown(
                    f"<div class='card2'><div class='lbl'>FIRE Number</div>"
                    f"<div style='font-family:DM Mono,monospace;font-size:28px;color:#3b82f6;'>{fire_yrs} years</div>"
                    f"<div style='font-size:11px;color:#334155;margin-top:4px;'>Before investment growth — actual timeline will be shorter.</div></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='card-r'><div class='lbl'>FIRE Number</div>"
                    "<div style='font-size:13px;color:#ef4444;'>Cannot calculate.</div>"
                    "<div style='font-size:11px;color:#334155;margin-top:4px;'>Need a positive monthly surplus.</div></div>",
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)

    # Leaderboard
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Global Leaderboard")
    lb_data = get_leaderboard(20)
    if lb_data:
        for i, e in enumerate(lb_data):
            is_me  = e["username"] == un
            bg     = "#041810" if is_me else "#080f1e"
            border = "1px solid #064e35" if is_me else "1px solid #0d1a2e"
            rank   = f"0{i+1}" if i + 1 < 10 else str(i+1)
            st.markdown(
                f"<div class='lb' style='background:{bg};border:{border};'>"
                f"<span class='lr'>{rank}</span>"
                f"<span class='ln' style='{'color:#10b981;font-weight:700;' if is_me else ''}'>"
                f"{e['username']}{'  (you)' if is_me else ''}</span>"
                f"<span class='ll'>{e['level_name']}</span>"
                f"<span class='ll'>{e['persona'].split()[-1]}</span>"
                f"<span class='ls'>{e['score']:.1f}</span></div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown("<p style='font-size:12px;color:#1e3a5f;'>No scores yet. Calculate yours in the Score tab.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Survey
    SURVEY_Q = "What is your biggest financial challenge right now?"
    SURVEY_OPTS = [
        "Not enough savings",
        "High monthly expenses",
        "Debt / EMIs",
        "Irregular income",
        "Don't know where to invest",
        "No financial plan",
    ]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sec("Community Survey")
    if not has_answered_survey(un, SURVEY_Q):
        st.markdown(
            f"<div style='font-size:13px;color:#94a3b8;font-weight:600;margin-bottom:12px;'>{SURVEY_Q}</div>",
            unsafe_allow_html=True,
        )
        answer = st.radio("Select one", SURVEY_OPTS, label_visibility="collapsed")
        if st.button("SUBMIT ANSWER", key="survey_btn"):
            save_survey_response(un, SURVEY_Q, answer)
            st.success("Response saved. Thank you.")
            st.rerun()
    else:
        # Show results
        responses = get_survey_responses(SURVEY_Q)
        st.markdown(
            f"<div style='font-size:13px;color:#94a3b8;font-weight:600;margin-bottom:12px;'>"
            f"Survey Results — {SURVEY_Q}</div>",
            unsafe_allow_html=True,
        )
        counts = {}
        for r in responses:
            counts[r["answer"]] = counts.get(r["answer"], 0) + 1
        total_r = len(responses)
        for opt in SURVEY_OPTS:
            cnt = counts.get(opt, 0)
            pct = int(cnt / total_r * 100) if total_r > 0 else 0
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;'>"
                f"<span style='color:#64748b;'>{opt}</span>"
                f"<span style='font-family:DM Mono,monospace;color:#94a3b8;'>{pct}% ({cnt})</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown(bar(pct, "#334155"), unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:11px;color:#1e3a5f;margin-top:6px;'>{total_r} total responses</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Share
    if st.session_state.last_result:
        sc_ = st.session_state.last_result["composite_score"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sec("Share Your Score")
        msg = (f"My Finverse Financial Safety Score: {sc_:.1f}/100. "
               f"Know yours? — [your Streamlit link here]")
        st.code(msg, language=None)
        st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────
st.markdown(
    "<div style='text-align:center;padding:24px 0 0;border-top:1px solid #0d1a2e;margin-top:14px;'>"
    "<span style='font-family:Syne,sans-serif;font-size:13px;font-weight:800;color:#0d1a2e;'>FINVERSE</span>"
    "<span style='font-size:11px;color:#0d1a2e;margin-left:12px;'>v6.0</span>"
    "<span style='font-size:11px;color:#0d1a2e;margin-left:12px;'>All data stored locally</span>"
    "<span style='font-size:11px;color:#0d1a2e;margin-left:12px;'>Not financial advice</span>"
    "</div>",
    unsafe_allow_html=True,
)
