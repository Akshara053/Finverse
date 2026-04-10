# app.py  —  Finverse v9.0
# Three themes: Dark / Light / Warm
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

# Safe education import — handles any version of education.py
try:
    from education import (LEARNING_MODULES, BOOK_LIST, get_modules_by_level)
    try:
        from education import FREE_RESOURCES
    except ImportError:
        FREE_RESOURCES = [
            {"name": "Zerodha Varsity", "url": "https://zerodha.com/varsity",
             "desc": "Best free course on stock markets and investing in India."},
            {"name": "SEBI Investor Education", "url": "https://investor.sebi.gov.in",
             "desc": "India's official investor education portal."},
        ]
except Exception:
    LEARNING_MODULES = []; BOOK_LIST = []; FREE_RESOURCES = []
    def get_modules_by_level(): return {}

try:
    import plotly.graph_objects as go
    PLOTLY = True
except ImportError:
    PLOTLY = False

init_db()

st.set_page_config(
    page_title="Finverse — Your Financial Safety Score",
    page_icon="F", layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════
# THEME SYSTEM
# ══════════════════════════════════════════════
THEMES = {
    "Dark": {
        "bg":       "#07080f",
        "surface":  "#0d1117",
        "border":   "#12182b",
        "text":     "#f1f5f9",
        "sub":      "#475569",
        "muted":    "#1e3a5f",
        "accent":   "#22c55e",
        "accent2":  "#16a34a",
        "input_bg": "#07080f",
        "green_bg": "#021a0b",
        "green_br": "#14532d",
        "red_bg":   "#1a0508",
        "red_br":   "#7f1d1d",
        "amber_bg": "#1a0e01",
        "amber_br": "#78350f",
        "grad_start":"#021a0b",
        "grad_end":  "#020d1a",
        "mode_icon": "🌙",
    },
    "Light": {
        "bg":       "#f8fafc",
        "surface":  "#ffffff",
        "border":   "#e2e8f0",
        "text":     "#0f172a",
        "sub":      "#64748b",
        "muted":    "#94a3b8",
        "accent":   "#16a34a",
        "accent2":  "#15803d",
        "input_bg": "#f8fafc",
        "green_bg": "#f0fdf4",
        "green_br": "#bbf7d0",
        "red_bg":   "#fef2f2",
        "red_br":   "#fecaca",
        "amber_bg": "#fffbeb",
        "amber_br": "#fde68a",
        "grad_start":"#f0fdf4",
        "grad_end":  "#eff6ff",
        "mode_icon": "☀️",
    },
    "Warm": {
        "bg":       "#1a1208",
        "surface":  "#221a0e",
        "border":   "#3d2e14",
        "text":     "#fef3c7",
        "sub":      "#92400e",
        "muted":    "#78350f",
        "accent":   "#f59e0b",
        "accent2":  "#d97706",
        "input_bg": "#1a1208",
        "green_bg": "#1a2808",
        "green_br": "#365314",
        "red_bg":   "#2d0a00",
        "red_br":   "#7c2d12",
        "amber_bg": "#1a1208",
        "amber_br": "#92400e",
        "grad_start":"#1a2808",
        "grad_end":  "#1a1208",
        "mode_icon": "🪔",
    },
}

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

T = THEMES[st.session_state.theme]

def get_css(T):
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

*, html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.stApp {{ background: {T['bg']}; }}
.block-container {{ max-width: 1100px !important; padding: 0 1.5rem 5rem !important; }}
[data-testid="stSidebar"] {{ display: none !important; }}

/* CARDS */
.card {{ background:{T['surface']}; border:1px solid {T['border']}; border-radius:14px; padding:20px 22px; margin-bottom:14px; }}
.card-flat {{ background:{T['bg']}; border:1px solid {T['border']}; border-radius:14px; padding:20px 22px; margin-bottom:14px; }}
.card-green {{ background:{T['green_bg']}; border:1px solid {T['green_br']}; border-radius:14px; padding:20px 22px; margin-bottom:14px; }}
.card-red   {{ background:{T['red_bg']}; border:1px solid {T['red_br']}; border-radius:14px; padding:20px 22px; margin-bottom:14px; }}
.card-amber {{ background:{T['amber_bg']}; border:1px solid {T['amber_br']}; border-radius:14px; padding:20px 22px; margin-bottom:14px; }}
.card-grad  {{ background:linear-gradient(135deg,{T['grad_start']},{T['grad_end']}); border:1px solid {T['green_br']}; border-radius:14px; padding:20px 22px; margin-bottom:14px; }}
.card:hover {{ border-color:{T['accent']}; transition:border-color 0.2s; }}

/* LABELS */
.lbl {{ font-size:10px; font-weight:700; letter-spacing:0.16em; text-transform:uppercase; color:{T['muted']}; margin:0 0 12px 0; display:block; }}
.section-title {{ font-size:18px; font-weight:800; color:{T['text']}; margin:0 0 4px 0; letter-spacing:-0.3px; }}
.section-sub {{ font-size:13px; color:{T['sub']}; margin:0 0 16px 0; }}

/* STAT BOXES */
.sg {{ display:flex; gap:10px; flex-wrap:wrap; margin-bottom:6px; }}
.sb {{ flex:1; min-width:120px; background:{T['bg']}; border:1px solid {T['border']}; border-radius:10px; padding:13px 15px; }}
.sv {{ font-family:'Space Mono',monospace; font-size:21px; font-weight:700; color:{T['text']}; line-height:1.1; }}
.sk {{ font-size:10px; color:{T['muted']}; text-transform:uppercase; letter-spacing:0.12em; margin-top:4px; font-weight:700; }}
.sn {{ font-size:11px; color:{T['muted']}; margin-top:3px; line-height:1.4; }}

/* TAGS */
.tag {{ display:inline-block; font-size:10px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; padding:3px 10px; border-radius:4px; }}
.r-s {{ background:{T['green_bg']}; color:{T['accent']}; border:1px solid {T['green_br']}; }}
.r-m {{ background:{T['amber_bg']}; color:#f59e0b; border:1px solid {T['amber_br']}; }}
.r-r {{ background:{T['red_bg']}; color:#f87171; border:1px solid {T['red_br']}; }}
.l-pl {{ background:{T['surface']}; color:#60a5fa; border:1px solid #1d4ed8; }}
.l-go {{ background:{T['amber_bg']}; color:#fbbf24; border:1px solid #d97706; }}
.l-si {{ background:{T['surface']}; color:{T['sub']}; border:1px solid {T['border']}; }}
.l-br {{ background:{T['amber_bg']}; color:#fb923c; border:1px solid #9a3412; }}
.l-st {{ background:{T['green_bg']}; color:#34d399; border:1px solid #065f46; }}

/* BAR */
.bt {{ background:{T['border']}; border-radius:2px; height:4px; margin:5px 0 12px 0; }}
.bf {{ height:4px; border-radius:2px; }}

/* SUGGESTION */
.sug {{ background:{T['surface']}; border:1px solid {T['border']}; border-radius:10px; padding:15px 17px; margin-bottom:8px; }}
.sug-h {{ border-left:3px solid #f87171; }}
.sug-m {{ border-left:3px solid #f59e0b; }}
.sug-l {{ border-left:3px solid {T['accent']}; }}
.stit {{ font-size:14px; font-weight:700; color:{T['text']}; margin:0 0 5px 0; }}
.sbod {{ font-size:12px; color:{T['sub']}; margin:0; line-height:1.7; }}
.imp {{ display:inline-block; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; padding:2px 7px; border-radius:3px; margin-left:8px; vertical-align:middle; }}
.i-h {{ background:{T['red_bg']}; color:#f87171; }}
.i-m {{ background:{T['amber_bg']}; color:#f59e0b; }}
.i-l {{ background:{T['green_bg']}; color:{T['accent']}; }}

/* CMP */
.cmp {{ display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid {T['border']}; }}
.cl {{ font-size:11px; color:{T['muted']}; width:130px; flex-shrink:0; text-transform:uppercase; letter-spacing:0.07em; font-weight:700; }}
.co {{ font-family:'Space Mono',monospace; font-size:13px; color:{T['muted']}; width:75px; }}
.ca {{ font-size:11px; color:{T['border']}; }}
.cu {{ font-family:'Space Mono',monospace; font-size:13px; color:{T['accent']}; font-weight:700; }}
.cd {{ font-family:'Space Mono',monospace; font-size:13px; color:#f87171; font-weight:700; }}
.ce {{ font-family:'Space Mono',monospace; font-size:13px; color:{T['sub']}; font-weight:500; }}

/* LB ROW */
.lbr {{ display:flex; align-items:center; gap:12px; padding:11px 14px; border-radius:10px; margin-bottom:5px; border:1px solid {T['border']}; background:{T['surface']}; }}
.lrk {{ font-family:'Space Mono',monospace; font-size:12px; color:{T['muted']}; width:28px; }}
.lnm {{ flex:1; font-size:13px; color:{T['sub']}; }}
.llv {{ font-size:10px; color:{T['muted']}; margin-right:8px; text-transform:uppercase; letter-spacing:0.07em; }}
.lsc {{ font-family:'Space Mono',monospace; font-size:17px; color:{T['accent']}; font-weight:700; }}

/* STORY BOX */
.story {{ background:{T['grad_start']}; border:1px solid {T['green_br']}; border-radius:10px; padding:16px 18px; margin:0 0 12px 0; font-size:13px; color:{T['sub']}; line-height:1.85; font-style:italic; }}
.story-label {{ font-size:9px; color:{T['accent']}; text-transform:uppercase; letter-spacing:0.16em; font-weight:700; margin-bottom:8px; display:block; font-style:normal; }}

/* POST */
.post {{ background:{T['surface']}; border:1px solid {T['border']}; border-radius:10px; padding:15px 17px; margin-bottom:9px; }}
.ptag {{ font-size:10px; color:{T['sub']}; text-transform:uppercase; letter-spacing:0.1em; font-weight:700; display:inline-block; background:{T['bg']}; border:1px solid {T['border']}; padding:2px 8px; border-radius:3px; margin-bottom:7px; }}
.paut {{ font-size:11px; color:{T['muted']}; margin-bottom:5px; }}
.ptxt {{ font-size:13px; color:{T['sub']}; line-height:1.75; }}
.pft  {{ font-size:11px; color:{T['muted']}; margin-top:7px; }}

/* BOOK */
.book {{ background:{T['surface']}; border:1px solid {T['border']}; border-radius:10px; padding:15px 17px; margin-bottom:8px; }}

/* PROFILE */
.profile-card {{ background:linear-gradient(135deg,{T['grad_start']},{T['grad_end']}); border:1px solid {T['green_br']}; border-radius:18px; padding:26px; margin-bottom:14px; }}

/* HERO BADGE */
.hero-badge {{ display:inline-block; background:{T['green_bg']}; border:1px solid {T['green_br']}; border-radius:20px; padding:5px 16px; font-size:11px; font-weight:700; color:{T['accent']}; letter-spacing:0.14em; text-transform:uppercase; margin-bottom:20px; }}

/* STAT HERO */
.stat-hero {{ text-align:center; padding:18px; background:{T['surface']}; border:1px solid {T['border']}; border-radius:12px; }}

/* COMPARISON TABLE */
.ctbl {{ width:100%; border-collapse:collapse; }}
.ctbl th {{ font-size:10px; color:{T['muted']}; text-transform:uppercase; letter-spacing:0.12em; padding:8px 12px; border-bottom:1px solid {T['border']}; text-align:left; }}
.ctbl td {{ font-size:12px; color:{T['sub']}; padding:9px 12px; border-bottom:1px solid {T['border']}; }}
.ctbl .yes {{ color:{T['accent']}; font-weight:700; }}
.ctbl .no  {{ color:{T['muted']}; }}
.ctbl .partial {{ color:#f59e0b; font-weight:600; }}
.ctbl .us  {{ background:{T['green_bg']} !important; }}

/* TABS */
.stTabs [data-baseweb="tab-list"] {{ background:{T['surface']} !important; border-bottom:1px solid {T['border']} !important; gap:0 !important; padding:0 !important; border-radius:0 !important; overflow-x:auto !important; }}
.stTabs [data-baseweb="tab"] {{ background:transparent !important; color:{T['muted']} !important; font-size:11px !important; font-weight:700 !important; padding:13px 16px !important; border-radius:0 !important; border-bottom:2px solid transparent !important; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap !important; }}
.stTabs [aria-selected="true"] {{ background:transparent !important; color:{T['accent']} !important; border-bottom:2px solid {T['accent']} !important; }}
[data-testid="stTabPanel"] {{ background:transparent !important; padding-top:18px !important; }}

/* INPUTS */
.stNumberInput input, .stTextInput input {{ background:{T['input_bg']} !important; border:1px solid {T['border']} !important; border-radius:9px !important; color:{T['text']} !important; font-family:'Space Mono',monospace !important; font-size:15px !important; padding:10px 13px !important; }}
.stNumberInput input:focus, .stTextInput input:focus {{ border-color:{T['accent']} !important; box-shadow:0 0 0 3px {T['accent']}20 !important; }}
.stTextArea textarea {{ background:{T['input_bg']} !important; border:1px solid {T['border']} !important; border-radius:9px !important; color:{T['text']} !important; font-size:13px !important; }}
[data-baseweb="select"] > div {{ background:{T['input_bg']} !important; border:1px solid {T['border']} !important; border-radius:9px !important; }}
[data-baseweb="select"] span {{ color:{T['text']} !important; }}
label {{ font-size:10px !important; font-weight:700 !important; color:{T['muted']} !important; text-transform:uppercase !important; letter-spacing:0.1em !important; }}
.stDateInput input {{ background:{T['input_bg']} !important; border:1px solid {T['border']} !important; color:{T['text']} !important; border-radius:9px !important; }}

/* BUTTON */
.stButton > button {{ background:linear-gradient(135deg,{T['accent']},{T['accent2']}) !important; color:#fff !important; border:none !important; border-radius:9px !important; font-weight:800 !important; font-size:12px !important; letter-spacing:0.1em !important; text-transform:uppercase !important; padding:12px 20px !important; width:100% !important; box-shadow:0 4px 14px {T['accent']}30 !important; transition:all 0.2s !important; }}
.stButton > button:hover {{ transform:translateY(-2px) !important; box-shadow:0 8px 22px {T['accent']}50 !important; }}

/* METRICS */
[data-testid="metric-container"] {{ background:{T['bg']} !important; border:1px solid {T['border']} !important; border-radius:10px !important; padding:13px 15px !important; }}
[data-testid="stMetricLabel"] {{ font-size:10px !important; color:{T['muted']} !important; text-transform:uppercase !important; letter-spacing:0.1em !important; }}
[data-testid="stMetricValue"] {{ font-family:'Space Mono',monospace !important; font-size:19px !important; color:{T['text']} !important; }}

/* SLIDER */
[data-testid="stSlider"] > div > div > div > div {{ background:{T['accent']} !important; }}
[data-testid="stSlider"] > div > div > div {{ background:{T['border']} !important; }}

/* RADIO / CHECKBOX */
.stRadio label {{ font-size:13px !important; color:{T['sub']} !important; text-transform:none !important; letter-spacing:0 !important; }}
.stCheckbox label {{ font-size:13px !important; color:{T['sub']} !important; text-transform:none !important; letter-spacing:0 !important; }}

/* ALERTS */
[data-testid="stAlert"] {{ background:{T['surface']} !important; border:1px solid {T['border']} !important; border-radius:9px !important; font-size:13px !important; }}

/* EXPANDER */
.streamlit-expanderHeader {{ background:{T['surface']} !important; border:1px solid {T['border']} !important; border-radius:9px !important; color:{T['sub']} !important; font-size:13px !important; font-weight:600 !important; }}

::-webkit-scrollbar {{ width:3px; height:3px; background:transparent; }}
::-webkit-scrollbar-thumb {{ background:{T['border']}; border-radius:3px; }}
hr {{ border-color:{T['border']} !important; }}
</style>
"""

st.markdown(get_css(T), unsafe_allow_html=True)

# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def ring(score, size=130):
    r = 44; c = 2 * 3.14159 * r
    d = round(score / 100 * c, 1); g = round(c - d, 1)
    col = T['accent'] if score >= 65 else ("#f59e0b" if score >= 35 else "#f87171")
    return (f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 100 100">'
            f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="{T["border"]}" stroke-width="8"/>'
            f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="{col}" stroke-width="8"'
            f' stroke-dasharray="{d} {g}" stroke-dashoffset="{c*0.25}" stroke-linecap="round"/>'
            f'<text x="50" y="45" text-anchor="middle" font-family="Space Mono,monospace"'
            f' font-size="20" font-weight="700" fill="{T["text"]}">{score:.0f}</text>'
            f'<text x="50" y="60" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif"'
            f' font-size="9" fill="{T["muted"]}" letter-spacing="2">SCORE</text>'
            f'</svg></div>')

def bar(pct, color=None):
    pct = min(100, max(0, pct))
    color = color or T['accent']
    return f'<div class="bt"><div class="bf" style="width:{pct}%;background:{color};"></div></div>'

def risk_tag(risk):
    c = {"SAFE":"r-s","MODERATE":"r-m","RISKY":"r-r"}
    l = {"SAFE":"Safe","MODERATE":"Moderate","RISKY":"High Risk"}
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
        "paper_bgcolor":"rgba(0,0,0,0)", "plot_bgcolor":"rgba(0,0,0,0)",
        "font":{"color":T['sub'],"family":"Plus Jakarta Sans","size":11},
        "margin":{"l":10,"r":10,"t":28,"b":10},
        "xaxis":{"gridcolor":T['border'],"linecolor":T['border'],"tickfont":{"color":T['muted']}},
        "yaxis":{"gridcolor":T['border'],"linecolor":T['border'],"tickfont":{"color":T['muted']}},
    }


# ══════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════
for k, v in {
    "page":"landing", "logged_in":False, "username":"",
    "persona_name":"Working Professional",
    "last_result":None, "last_income":50000.0,
    "last_expenses":35000.0, "last_savings":120000.0,
    "challenges_done":set(), "active_tab":"Score",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════
# THEME SWITCHER (shown on all pages)
# ══════════════════════════════════════════════
def theme_switcher():
    t1, t2, t3 = st.columns([8, 1, 1])
    with t2:
        if st.button(THEMES["Light"]["mode_icon"], key="th_light",
                     help="Light mode"):
            st.session_state.theme = "Light"
            st.rerun()
    with t3:
        opts = [k for k in THEMES if k != st.session_state.theme]
        icons = {"Dark":"🌙","Warm":"🪔","Light":"☀️"}
        next_t = [k for k in ["Dark","Light","Warm"] if k != st.session_state.theme]
        if st.button(icons.get(next_t[0],"🌙"), key="th_toggle",
                     help=f"Switch to {next_t[0]} mode"):
            st.session_state.theme = next_t[0]
            st.rerun()


# ══════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════
if st.session_state.page == "landing":

    # Top bar with theme toggle
    c_logo, c_space, c_th = st.columns([6, 3, 1])
    with c_logo:
        st.markdown(
            f"<div style='font-size:20px;font-weight:800;color:{T['text']};padding:14px 0;"
            f"border-bottom:1px solid {T['border']};'>FIN<span style='color:{T['accent']};'>VERSE</span></div>",
            unsafe_allow_html=True,
        )
    with c_th:
        theme_opts = list(THEMES.keys())
        theme_icons = {"Dark":"🌙","Light":"☀️","Warm":"🪔"}
        for t_name in theme_opts:
            if t_name != st.session_state.theme:
                if st.button(theme_icons[t_name], key=f"land_th_{t_name}", help=f"{t_name} mode"):
                    st.session_state.theme = t_name
                    st.rerun()
                break

    # Hero
    st.markdown(f"""
    <div style="text-align:center;padding:52px 0 40px 0;">
        <div class="hero-badge">India's Financial Safety Platform</div>
        <h1 style="font-size:54px;font-weight:800;color:{T['text']};margin:0 0 16px 0;
                   line-height:1.1;letter-spacing:-1.5px;">
            Are you actually<br><span style="color:{T['accent']};">financially safe?</span>
        </h1>
        <p style="font-size:17px;color:{T['sub']};max-width:520px;margin:0 auto 12px;line-height:1.75;">
            Most people have no idea. Finverse gives you a clear, honest answer —
            your personal Financial Safety Score — in under 60 seconds.
        </p>
        <p style="font-size:12px;color:{T['muted']};margin-bottom:32px;">
            Free · No email · No credit card · Works for any income level
        </p>
    </div>
    """, unsafe_allow_html=True)

    h1, h2, h3 = st.columns([1, 2, 1])
    with h2:
        if st.button("GET MY SCORE — FREE", key="hero_cta"):
            st.session_state.page = "onboard"
            st.rerun()

    # Stats
    stats = get_platform_stats()
    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, val, label in [
        (s1, stats["total_users"],    "People Using Finverse"),
        (s2, stats["total_scores"],   "Scores Calculated"),
        (s3, f"{stats['avg_score']:.0f}/100", "Average Score"),
        (s4, stats["total_expenses"], "Expenses Tracked"),
    ]:
        with col:
            st.markdown(
                f"<div class='stat-hero'>"
                f"<div style='font-family:Space Mono,monospace;font-size:26px;font-weight:700;"
                f"color:{T['accent']};'>{val}</div>"
                f"<div style='font-size:10px;color:{T['muted']};text-transform:uppercase;"
                f"letter-spacing:0.1em;margin-top:4px;'>{label}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # Problem
    st.markdown(f"""
    <div style="margin:52px 0 28px 0;text-align:center;">
        <h2 style="font-size:30px;font-weight:800;color:{T['text']};margin:0 0 10px 0;">
            78% of Indians live paycheck to paycheck
        </h2>
        <p style="font-size:14px;color:{T['sub']};max-width:560px;margin:0 auto;line-height:1.8;">
            No one teaches personal finance in school. Banks profit from confusion.
            Most apps are built for people who already know finance.
            <strong style="color:{T['text']};">Finverse is built for everyone else.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    pb1, pb2, pb3 = st.columns(3)
    for col, num, title, desc in [
        (pb1, "01", "No one tells you if you're safe", "Finverse gives you one honest number that answers the question directly."),
        (pb2, "02", "One bad month can destroy you", "Without an emergency fund, a job loss or medical bill becomes a crisis overnight."),
        (pb3, "03", "No one gives you a real plan", "Banks sell products. Apps track numbers. Finverse tells you exactly what to do next."),
    ]:
        with col:
            st.markdown(
                f"<div class='card' style='padding:22px;'>"
                f"<div style='font-family:Space Mono,monospace;font-size:12px;color:{T['accent']};"
                f"font-weight:700;margin-bottom:10px;'>{num}</div>"
                f"<div style='font-size:14px;font-weight:700;color:{T['text']};margin-bottom:6px;'>{title}</div>"
                f"<div style='font-size:12px;color:{T['sub']};line-height:1.65;'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # Our Story
    st.markdown(f"""
    <div style="margin:44px 0;">
        <div class="card" style="padding:30px 34px;">
            <span class="lbl">Why We Built This</span>
            <h3 style="font-size:22px;font-weight:800;color:{T['text']};margin:0 0 12px 0;">
                A question no app could answer
            </h3>
            <p style="font-size:14px;color:{T['sub']};line-height:1.85;margin:0 0 10px 0;">
                After getting a salary, paying bills, and checking the bank balance —
                the question that kept coming up: <em style="color:{T['text']};">"Am I actually okay? Or just getting by?"</em>
            </p>
            <p style="font-size:14px;color:{T['sub']};line-height:1.85;margin:0;">
                We tried every app. None answered it directly. They showed charts, categories, numbers.
                But nobody said: <em style="color:{T['text']};">"Here is your score. Here is what it means. Here is what to do."</em>
                That gap is Finverse.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features
    st.markdown(f"""
    <div style="text-align:center;margin:8px 0 24px 0;">
        <h2 style="font-size:26px;font-weight:800;color:{T['text']};margin:0 0 6px 0;">Everything in one platform</h2>
        <p style="font-size:13px;color:{T['muted']};">Free. No account needed. Works for students, salaried, freelancers, and business owners.</p>
    </div>
    """, unsafe_allow_html=True)

    fa, fb = st.columns(2)
    features = [
        ("Financial Safety Score", "One honest 0–100 score. No other Indian app answers 'Am I safe?' directly."),
        ("Financial Stress Score", "Separate metric measuring financial anxiety — runway pressure + cash flow tightness."),
        ("Daily Expense Tracker", "Log expenses in seconds. Budget alerts. Monthly breakdown. Streak system."),
        ("Lend / Borrow Manager", "Track who owes you and who you owe. Auto-generate WhatsApp reminder messages."),
        ("What-If Simulator", "Live sliders: see how a raise, expense cut, or bonus changes your score instantly."),
        ("Partner Compatibility", "Compatibility score + ideal partner income for a stable shared financial life."),
        ("14 Finance Modules + Stories", "Structured learning with real stories. Beginner to Advanced. With XP rewards."),
        ("Predictions and Insights", "Emergency fund date. FIRE number. Behavioral patterns from your real data."),
        ("Community + Surveys", "Anonymous or named discussions. Real-time survey data from all users."),
    ]
    for i, (t, d) in enumerate(features):
        with (fa if i % 2 == 0 else fb):
            st.markdown(
                f"<div class='card' style='margin-bottom:10px;'>"
                f"<div style='font-size:14px;font-weight:700;color:{T['text']};margin-bottom:5px;'>{t}</div>"
                f"<div style='font-size:12px;color:{T['sub']};line-height:1.65;'>{d}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # Comparison
    st.markdown(f"""
    <div style="text-align:center;margin:44px 0 22px 0;">
        <h2 style="font-size:24px;font-weight:800;color:{T['text']};margin:0 0 4px 0;">How Finverse compares</h2>
        <p style="font-size:12px;color:{T['muted']};">Studied: Fi, Jupiter, Walnut, YNAB, Mint, Splitwise, Groww before building this.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="overflow-x:auto;">
    <table class="ctbl">
    <thead>
        <tr>
            <th>Feature</th>
            <th style="color:{T['accent']};text-align:center;">Finverse</th>
            <th style="text-align:center;">Fi / Jupiter</th>
            <th style="text-align:center;">Walnut</th>
            <th style="text-align:center;">Splitwise</th>
            <th style="text-align:center;">YNAB</th>
        </tr>
    </thead>
    <tbody>
        <tr class="us"><td>Financial Safety Score</td><td class="yes" align="center">✓</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td></tr>
        <tr><td>Survival time without income</td><td class="yes" align="center">✓</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td></tr>
        <tr class="us"><td>Financial Stress Score</td><td class="yes" align="center">✓</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td></tr>
        <tr><td>What-If Simulator</td><td class="yes" align="center">✓</td><td class="partial" align="center">Partial</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="partial" align="center">Partial</td></tr>
        <tr class="us"><td>Expense tracking + daily budget</td><td class="yes" align="center">✓</td><td class="yes" align="center">✓</td><td class="yes" align="center">✓</td><td class="no" align="center">✗</td><td class="yes" align="center">✓</td></tr>
        <tr><td>Lend / Borrow with reminders</td><td class="yes" align="center">✓</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="yes" align="center">✓</td><td class="no" align="center">✗</td></tr>
        <tr class="us"><td>Partner compatibility score</td><td class="yes" align="center">✓</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td></tr>
        <tr><td>Story-based finance education</td><td class="yes" align="center">✓</td><td class="partial" align="center">Partial</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="partial" align="center">Partial</td></tr>
        <tr class="us"><td>Community discussions</td><td class="yes" align="center">✓</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td></tr>
        <tr><td>100% free, no bank account link</td><td class="yes" align="center">✓</td><td class="no" align="center">Paid</td><td class="partial" align="center">Partial</td><td class="yes" align="center">✓</td><td class="no" align="center">Paid</td></tr>
        <tr class="us"><td>Three themes (Dark/Light/Warm)</td><td class="yes" align="center">✓</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td><td class="no" align="center">✗</td></tr>
    </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    # Final CTA
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{T['grad_start']},{T['grad_end']});
                border:1px solid {T['green_br']};border-radius:18px;padding:44px 36px;
                text-align:center;margin:36px 0 20px 0;">
        <h2 style="font-size:28px;font-weight:800;color:{T['text']};margin:0 0 8px 0;">
            Your financial truth in 60 seconds
        </h2>
        <p style="font-size:13px;color:{T['sub']};margin:0 0 24px 0;">
            Free. No email. No credit card. No bank link required.
        </p>
    </div>
    """, unsafe_allow_html=True)
    cl, cm, cr = st.columns([1, 2, 1])
    with cm:
        if st.button("START NOW — FREE", key="bottom_cta"):
            st.session_state.page = "onboard"
            st.rerun()

    st.markdown(
        f"<p style='text-align:center;font-size:11px;color:{T['muted']};margin-top:14px;'>"
        f"Finverse v9.0 · Built in India · Not financial advice · {T['mode_icon']} {st.session_state.theme} mode</p>",
        unsafe_allow_html=True,
    )
    st.stop()


# ══════════════════════════════════════════════
# ONBOARDING
# ══════════════════════════════════════════════
if st.session_state.page == "onboard":
    c_logo, _, c_th2 = st.columns([6, 3, 1])
    with c_logo:
        st.markdown(
            f"<div style='font-size:20px;font-weight:800;color:{T['text']};padding:14px 0;"
            f"border-bottom:1px solid {T['border']};'>FIN<span style='color:{T['accent']};'>VERSE</span></div>",
            unsafe_allow_html=True,
        )

    _, oc, _ = st.columns([1, 2, 1])
    with oc:
        st.markdown(f"""
        <div style="text-align:center;margin:28px 0 24px 0;">
            <div style="font-size:12px;color:{T['muted']};text-transform:uppercase;
                        letter-spacing:0.16em;font-weight:700;">Quick Setup — 1 Minute</div>
            <h2 style="font-size:22px;font-weight:800;color:{T['text']};margin:8px 0 0 0;">
                Tell us a little about you
            </h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Step 1 — Your Details")
        oa, ob = st.columns(2)
        with oa:
            name_in = st.text_input("Your name", placeholder="e.g. Aashi", key="ob_name")
        with ob:
            age_in  = st.number_input("Age", min_value=16, max_value=80, value=25, step=1)
        city_in = st.text_input("City (optional)", placeholder="e.g. Mumbai", key="ob_city")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Step 2 — Your Life Stage")
        st.markdown(
            f"<p style='font-size:12px;color:{T['muted']};margin:0 0 12px 0;'>"
            "This sets your personalised financial targets and tips.</p>",
            unsafe_allow_html=True,
        )
        selected_persona = st.radio(
            "I am a",
            list(PERSONAS.keys()),
            format_func=lambda x: f"{PERSONAS[x]['icon']}  {x}",
            index=1,
            label_visibility="collapsed",
        )
        p = PERSONAS[selected_persona]
        st.markdown(
            f"<div style='background:{T['bg']};border:1px solid {T['border']};border-radius:8px;"
            f"padding:11px 14px;margin-top:10px;font-size:12px;color:{T['sub']};'>"
            f"Savings target: <span style='color:{T['accent']};font-weight:700;'>{p['savings_rate_target']}%</span>"
            f"  ·  Emergency fund: <span style='color:{T['accent']};font-weight:700;'>{p['survival_target']} months</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("ENTER FINVERSE →", key="onboard_btn"):
            if name_in.strip():
                un_ = name_in.strip()
                upsert_user_profile(un_, un_, selected_persona, int(age_in), city_in)
                st.session_state.update({
                    "page": "app", "logged_in": True, "username": un_,
                    "persona_name": selected_persona,
                    "challenges_done": get_completed_challenges(un_),
                })
                st.rerun()
            else:
                st.warning("Please enter your name to continue.")

        if st.button("← Back", key="back_land"):
            st.session_state.page = "landing"
            st.rerun()
    st.stop()


# ══════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════
if not st.session_state.logged_in:
    st.session_state.page = "landing"; st.rerun()

un       = st.session_state.username
persona  = PERSONAS[st.session_state.persona_name]
profile  = get_user_profile(un) or {}
settings_= get_user_settings(un)
xp_total = get_total_xp(st.session_state.get("challenges_done", set()))

# ── APP HEADER ──────────────────────────────
h_logo, h_space, h_th1, h_th2, h_th3 = st.columns([4, 4, 1, 1, 1])
with h_logo:
    st.markdown(
        f"<div style='font-size:20px;font-weight:800;color:{T['text']};padding:16px 0 16px 0;"
        f"border-bottom:1px solid {T['border']};'>"
        f"FIN<span style='color:{T['accent']};'>VERSE</span>"
        f"<span style='font-size:11px;color:{T['muted']};font-weight:400;margin-left:12px;'>"
        f"Hello, {un}</span></div>",
        unsafe_allow_html=True,
    )
with h_th1:
    if st.button("🌙", key="ap_dark",  help="Dark mode"):
        st.session_state.theme = "Dark"; st.rerun()
with h_th2:
    if st.button("☀️", key="ap_light", help="Light mode"):
        st.session_state.theme = "Light"; st.rerun()
with h_th3:
    if st.button("🪔", key="ap_warm",  help="Warm mode"):
        st.session_state.theme = "Warm"; st.rerun()

st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────
tab_names = ["Score", "Dashboard", "Tracker", "Lend / Borrow",
             "Learn", "Community", "Insights", "Me"]
tabs = st.tabs(tab_names)
(t_score, t_dash, t_track, t_lend,
 t_learn, t_comm, t_insights, t_me) = tabs


# ════════════════════════════════════════════
# SCORE TAB
# ════════════════════════════════════════════
with t_score:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Monthly Snapshot")
    st.markdown(
        f"<p style='font-size:12px;color:{T['muted']};margin:0 0 14px 0;'>"
        "Enter your honest numbers. The more accurate, the more useful your score.</p>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        income  = st.number_input(persona["income_label"], min_value=0.0, value=50000.0, step=1000.0, key="s_inc",
                                   help="Take-home pay after taxes.")
        savings = st.number_input("Total savings (₹)", min_value=0.0, value=120000.0, step=5000.0, key="s_sav",
                                   help="All liquid savings — bank, FDs, emergency fund.")
    with c2:
        expenses = st.number_input("Monthly expenses (₹)", min_value=0.0, value=35000.0, step=1000.0, key="s_exp",
                                    help="All spending: rent, food, transport, EMIs, subscriptions.")
        st.markdown(
            f"<div style='background:{T['bg']};border:1px solid {T['border']};border-radius:8px;"
            f"padding:11px 13px;margin-top:6px;font-size:12px;color:{T['muted']};line-height:1.65;'>"
            f"<span style='color:{T['accent']};font-weight:700;'>Tip:</span> Include "
            f"rent, groceries, fuel, EMIs, OTT, eating out. Underestimating expenses = overestimating safety.</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("CALCULATE MY SAFETY SCORE", key="s_calc"):
        if income <= 0:
            st.error("Please enter your monthly income.")
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

        # Score card
        st.markdown('<div class="card-grad">', unsafe_allow_html=True)
        rc1, rc2 = st.columns([1, 2])
        with rc1:
            st.markdown(ring(score, 150), unsafe_allow_html=True)
        with rc2:
            nh = (f"<div style='font-size:11px;color:{T['muted']};margin-top:8px;'>"
                  f"{next_l['points_needed']} more pts → {next_l['name']} level</div>"
                  if next_l else
                  f"<div style='font-size:11px;color:{T['accent']};margin-top:8px;'>Max level reached</div>")
            st.markdown(
                f"<div style='padding:6px 0;'>{level_tag(lv['name'])}"
                f"<div style='font-size:24px;font-weight:800;color:{T['text']};"
                f"margin:10px 0 6px 0;line-height:1.2;'>{lv['message']}</div>"
                f"{risk_tag(risk)}"
                f"<div style='font-size:13px;color:{T['sub']};margin-top:8px;line-height:1.6;'>{get_risk_advice(risk)}</div>"
                f"{nh}</div>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Two cards: stress + metrics
        ca, cb = st.columns(2)
        with ca:
            s_label, s_color = get_stress_label(stress)
            stress_tips = {
                "High Stress": "Financial buffers are critically thin. Reduce expenses first.",
                "Moderate Stress": "Some pressure exists. Building savings will reduce this.",
                "Low Stress": "Stable position. Keep improving.",
                "Minimal Stress": "Strong buffers and healthy cash flow.",
            }
            st.markdown(
                f"<div class='card-flat'><span class='lbl'>Stress Score</span>"
                f"<div style='display:flex;align-items:center;gap:14px;'>"
                f"<div style='font-family:Space Mono,monospace;font-size:42px;font-weight:700;"
                f"color:{s_color};line-height:1;'>{stress}</div>"
                f"<div><div style='font-size:14px;font-weight:700;color:{s_color};'>{s_label}</div>"
                f"<div style='font-size:12px;color:{T['muted']};margin-top:4px;line-height:1.5;'>"
                f"{stress_tips.get(s_label,'')}</div>"
                f"<div style='font-size:10px;color:{T['muted']};margin-top:4px;'>0 = no stress · 100 = severe</div>"
                f"</div></div>{bar(stress, s_color)}</div>",
                unsafe_allow_html=True,
            )
        with cb:
            sr  = result["savings_rate"]; sm = result["survival_months"]; er = result["expense_ratio"]
            sc  = T['accent'] if sr >= 20 else ("#f59e0b" if sr >= 10 else "#f87171")
            smc = T['accent'] if sm >= 6  else ("#f59e0b" if sm >= 3  else "#f87171")
            erc = T['accent'] if er <= 60 else ("#f59e0b" if er <= 80 else "#f87171")
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

        # Monthly picture
        surplus = income - expenses
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
                    f'<span style="display:inline-block;background:{T["bg"]};border:1px solid {T["border"]};'
                    f'border-radius:6px;padding:4px 11px;font-size:11px;font-weight:700;'
                    f'color:{T["sub"]};margin:3px;">{b["name"].split(" ",1)[-1]}</span>'
                    for b in bdgs
                ),
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Suggestions + What-If
        suggs = generate_suggestions(income, expenses, savings, result)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Your Top 3 Actions")
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

        # Quick What-If
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Quick What-If Simulator")
        wi1, wi2 = st.columns(2)
        with wi1:
            id_ = st.slider("Income change (₹/mo)", -20000, 50000, 0, 1000, key="wi_inc")
        with wi2:
            ed_ = st.slider("Expense change (₹/mo)", -20000, 20000, 0, 500, key="wi_exp")
        nr   = calculate_whatif(income, expenses, savings, {"income_delta":id_,"expenses_delta":ed_,"savings_delta":0})
        diff = nr["composite_score"] - score
        wc1, wc2, wc3 = st.columns(3)
        wc1.metric("New Score", f"{nr['composite_score']:.1f}")
        wc2.metric("Change",    f"{'+'if diff>=0 else ''}{diff:.1f} pts",
                   delta_color="normal" if diff >= 0 else "inverse")
        wc3.metric("New Status", nr["risk_level"].capitalize())
        st.markdown('</div>', unsafe_allow_html=True)

        # Challenges
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Active Challenges")
        for ch in get_challenges():
            done = ch["id"] in st.session_state.get("challenges_done", set())
            ca_, cb_ = st.columns([5, 1])
            with ca_:
                op = "opacity:0.3;" if done else ""
                td = "text-decoration:line-through;" if done else ""
                st.markdown(
                    f"<div style='{op}background:{T['bg']};border:1px solid {T['border']};"
                    f"border-radius:8px;padding:9px 13px;margin-bottom:4px;'>"
                    f"<div style='font-size:13px;color:{T['text']};font-weight:600;{td}'>{ch['name']}</div>"
                    f"<div style='font-size:11px;color:{T['muted']};margin-top:2px;'>"
                    f"{ch['desc']} · +{ch['reward_xp']} XP</div></div>",
                    unsafe_allow_html=True,
                )
            with cb_:
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
                col = T['accent'] if h["risk_level"]=="SAFE" else ("#f59e0b" if h["risk_level"]=="MODERATE" else "#f87171")
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:7px 0;border-bottom:1px solid {T['border']};'>"
                    f"<span style='font-family:Space Mono,monospace;font-size:11px;color:{T['muted']};'>{h['created_at'][:10]}</span>"
                    f"<span style='font-size:11px;color:{T['sub']};'>{h['persona']}</span>"
                    f"<span style='font-family:Space Mono,monospace;font-size:16px;color:{col};font-weight:700;'>{h['score']:.1f}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown(
            f"<div class='card' style='text-align:center;padding:54px 28px;'>"
            f"<div style='font-family:Space Mono,monospace;font-size:58px;color:{T['border']};"
            f"font-weight:700;letter-spacing:-3px;line-height:1;'>--</div>"
            f"<div style='font-size:18px;font-weight:700;color:{T['muted']};margin-top:14px;'>"
            f"Enter your numbers above to get your score</div>"
            f"<div style='font-size:12px;color:{T['border']};margin-top:6px;line-height:1.7;'>"
            f"Safety score · Stress score · Key metrics · Action plan · Simulator</div>"
            f"</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# DASHBOARD TAB
# ════════════════════════════════════════════
with t_dash:
    score_hist  = get_score_history(un, 30)
    spend_trend = get_spending_trend(un, 30)
    monthly_exp = get_monthly_expenses(un)
    p_stats     = get_platform_stats()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Platform Stats")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Total Users",      p_stats["total_users"])
    d2.metric("Avg Safety Score", f"{p_stats['avg_score']:.1f}")
    d3.metric("Safe Users",       p_stats["safe_count"])
    d4.metric("High Risk Users",  p_stats["risky_count"])
    st.markdown('</div>', unsafe_allow_html=True)

    if PLOTLY:
        if score_hist and len(score_hist) > 1:
            d_ = build_score_trend_data(score_hist)
            r1a, r1b = st.columns(2)
            with r1a:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                lbl("Safety Score Over Time")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=d_["dates"], y=d_["scores"], mode="lines+markers",
                    line={"color":T['accent'],"width":2.5}, marker={"color":T['accent'],"size":7},
                    fill="tozeroy", fillcolor=f"{T['accent']}10"))
                fig.add_hline(y=65, line_dash="dot", line_color=T['muted'],
                              annotation_text="Safe zone", annotation_font_color=T['muted'])
                fig.update_layout(**plotly_cfg(), height=230)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            if spend_trend:
                with r1b:
                    d2_ = build_expense_trend_data(spend_trend)
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    lbl("Daily Spending — Last 30 Days")
                    fig2 = go.Figure(go.Bar(x=d2_["dates"], y=d2_["amounts"],
                        marker_color=T['accent'], opacity=0.75))
                    fig2.update_layout(**plotly_cfg(), height=230)
                    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
                    st.markdown('</div>', unsafe_allow_html=True)

        if monthly_exp:
            r2a, r2b = st.columns(2)
            with r2a:
                da = build_category_data(monthly_exp)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                lbl("Spending by Category — This Month")
                fig3 = go.Figure(go.Pie(labels=da["categories"], values=da["totals"], hole=0.55,
                    marker={"colors":[T['accent'],"#3b82f6","#f59e0b","#f87171","#8b5cf6","#ec4899","#14b8a6","#f97316"]},
                    textfont={"color":T['sub'],"size":10}))
                fig3.update_layout(**plotly_cfg(), height=260, showlegend=True,
                                   legend={"font":{"color":T['sub'],"size":10}})
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state.last_result:
                surplus_ = st.session_state.last_income - st.session_state.last_expenses
                if surplus_ > 0:
                    with r2b:
                        dp = build_prediction_data(st.session_state.last_savings, surplus_)
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        lbl("12-Month Savings Projection")
                        fig4 = go.Figure(go.Scatter(x=dp["months"], y=dp["savings"],
                            mode="lines+markers", line={"color":"#3b82f6","width":2,"dash":"dot"},
                            marker={"color":"#3b82f6","size":5},
                            fill="tozeroy", fillcolor="#3b82f610"))
                        fig4.update_layout(**plotly_cfg(), height=260)
                        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})
                        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Run: pip install plotly  to enable charts.")

    if not score_hist and not spend_trend:
        st.markdown(
            f"<div class='card' style='text-align:center;padding:44px;color:{T['muted']};'>"
            "Calculate your score and log expenses to populate the dashboard.</div>",
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
    h1.metric("Tracking Streak",  f"{s_cfg['streak']} days")
    h2.metric("Today's Budget",   format_currency(s_cfg["daily_budget"]))
    with h3:
        nb = st.number_input("Update daily budget (₹)", min_value=0.0,
                             value=float(s_cfg["daily_budget"]), step=100.0)
        if nb != s_cfg["daily_budget"]:
            save_user_settings(un, nb, s_cfg["streak"], s_cfg["last_tracked"])
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Add an Expense")
    tc1, tc2, tc3, tc4 = st.columns([2, 2, 2, 3])
    with tc1:
        cat = st.selectbox("Category", ["Food & Dining","Transport","Shopping","Bills & Utilities",
                                         "Entertainment","Health & Medical","Education",
                                         "Personal Care","Investment","Other"])
    with tc2:
        amt = st.number_input("Amount (₹)", min_value=0.0, value=0.0, step=10.0)
    with tc3:
        exp_date = st.date_input("Date", value=date.today())
    with tc4:
        note = st.text_input("Note (optional)", placeholder="e.g. Lunch at Café")
    if st.button("ADD EXPENSE", key="add_exp"):
        if amt > 0:
            save_expense(un, cat, float(amt), note, str(exp_date))
            st.success(f"Added: {cat}  —  {format_currency(amt)}")
            st.rerun()
        else:
            st.warning("Enter an amount greater than ₹0.")
    st.markdown('</div>', unsafe_allow_html=True)

    today_exps = get_today_expenses(un)
    budget     = s_cfg["daily_budget"]

    if today_exps:
        total = sum(e["amount"] for e in today_exps)
        left  = budget - total
        pct   = min(100, int(total / budget * 100)) if budget > 0 else 100
        bc    = T['accent'] if pct < 70 else ("#f59e0b" if pct < 90 else "#f87171")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Today")
        d1, d2, d3 = st.columns(3)
        d1.metric("Spent Today",  format_currency(total))
        d2.metric("Daily Budget", format_currency(budget))
        d3.metric("Remaining" if left >= 0 else "Over Budget", format_currency(abs(left)),
                  delta_color="normal" if left >= 0 else "inverse")
        st.markdown(f"<div style='font-size:11px;color:{T['muted']};margin-bottom:4px;'>Used: {pct}%</div>", unsafe_allow_html=True)
        st.markdown(bar(pct, bc), unsafe_allow_html=True)
        if pct >= 90:   st.error("At 90%+ of daily budget.")
        elif pct >= 70: st.warning("Over two-thirds of budget used.")
        else:           st.success("Spending is on track.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Expense Log — click Delete to remove")
        for exp in reversed(today_exps):
            ec1, ec2, ec3, ec4, ec5 = st.columns([2, 3, 1, 2, 1])
            with ec1:
                st.markdown(f"<span style='font-size:11px;color:{T['sub']};font-weight:700;text-transform:uppercase;letter-spacing:0.06em;'>{exp['category']}</span>", unsafe_allow_html=True)
            with ec2:
                st.markdown(f"<span style='font-size:12px;color:{T['sub']};'>{exp['note'] or '—'}</span>", unsafe_allow_html=True)
            with ec3:
                st.markdown(f"<span style='font-family:Space Mono,monospace;font-size:10px;color:{T['muted']};'>{exp['created_at'][11:16]}</span>", unsafe_allow_html=True)
            with ec4:
                st.markdown(f"<span style='font-family:Space Mono,monospace;font-size:14px;color:{T['text']};font-weight:700;'>{format_currency(exp['amount'])}</span>", unsafe_allow_html=True)
            with ec5:
                if st.button("Del", key=f"del_{exp['id']}"):
                    delete_expense(exp["id"]); st.rerun()
        st.markdown(f"<hr style='border-color:{T['border']};margin:12px 0;'>", unsafe_allow_html=True)
        if st.button("END DAY — SAVE STREAK", use_container_width=True):
            new_streak = end_day_update_streak(un)
            st.success(f"Day saved! Streak: {new_streak} days."); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        monthly = get_monthly_expenses(un)
        if monthly:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            lbl("This Month — All Spending")
            mt = sum(r["total"] for r in monthly)
            for row in monthly:
                p_ = int(row["total"] / mt * 100) if mt > 0 else 0
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;'>"
                    f"<span style='color:{T['sub']};'>{row['category']}"
                    f"<span style='color:{T['muted']};margin-left:5px;font-size:10px;'>({row['count']})</span></span>"
                    f"<span style='font-family:Space Mono,monospace;color:{T['text']};font-weight:700;'>{format_currency(row['total'])}</span></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(bar(p_, T['muted']), unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-family:Space Mono,monospace;font-size:15px;color:{T['accent']};"
                f"margin-top:10px;border-top:1px solid {T['border']};padding-top:10px;font-weight:700;'>"
                f"Month Total: {format_currency(mt)}</div>",
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div class='card' style='text-align:center;padding:40px;color:{T['muted']};'>"
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
    st.markdown(f"<p style='font-size:12px;color:{T['muted']};margin:0 0 14px 0;'>Track money you've given and money you owe. One-tap reminder messages.</p>", unsafe_allow_html=True)
    ls1, ls2, ls3 = st.columns(3)
    ls1.metric("Others Owe You", format_currency(summary["total_gave"]))
    ls2.metric("You Owe Others", format_currency(summary["total_owe"]))
    ls3.metric("Net Position",   format_currency(abs(net)),
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
        desc     = st.text_input("What for?", placeholder="e.g. Dinner, travel")
    with lb2c:
        due_date = st.date_input("Due date (optional)", value=None, key="lb_due")
    if st.button("ADD TRANSACTION", key="add_lb"):
        if party.strip() and l_amt > 0:
            t  = "gave" if "gave" in txn_type else "owe"
            dd = str(due_date) if due_date else None
            add_lend_borrow(un, party.strip(), float(l_amt), t, desc, dd)
            st.success(f"Recorded: {format_currency(l_amt)} {'given to' if t=='gave' else 'borrowed from'} {party}.")
            st.rerun()
        else:
            st.warning("Enter a name and amount greater than ₹0.")
    st.markdown('</div>', unsafe_allow_html=True)

    all_txns = get_lend_borrow(un)
    pending  = [t for t in all_txns if t["status"] == "pending"]
    settled  = [t for t in all_txns if t["status"] == "settled"]

    if pending:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl(f"Pending ({len(pending)})")
        for txn in pending:
            is_gave = txn["txn_type"] == "gave"
            color   = T['accent'] if is_gave else "#f87171"
            label   = "They owe you" if is_gave else "You owe them"
            due_str = f"  ·  Due: {txn['due_date']}" if txn.get("due_date") else ""
            t1, t2, t3, t4, t5 = st.columns([2, 2, 2, 1, 1])
            with t1:
                st.markdown(
                    f"<div style='font-size:14px;color:{T['text']};font-weight:700;'>{txn['party_name']}</div>"
                    f"<div style='font-size:11px;color:{T['muted']};'>{txn.get('description','') or '—'}{due_str}</div>",
                    unsafe_allow_html=True,
                )
            with t2:
                st.markdown(
                    f"<span style='font-family:Space Mono,monospace;font-size:16px;"
                    f"color:{color};font-weight:700;'>{format_currency(txn['amount'])}</span>",
                    unsafe_allow_html=True,
                )
            with t3:
                st.markdown(f"<span style='font-size:12px;color:{T['sub']};'>{label}</span>", unsafe_allow_html=True)
            with t4:
                if st.button("Settle", key=f"set_{txn['id']}"):
                    settle_lend_borrow(txn["id"]); st.rerun()
            with t5:
                if st.button("Del", key=f"dlt_{txn['id']}"):
                    delete_lend_borrow(txn["id"]); st.rerun()
            with st.expander(f"Reminder for {txn['party_name']}"):
                if is_gave:
                    msg = (f"Hi {txn['party_name']}, friendly reminder that you owe me "
                           f"{format_currency(txn['amount'])}"
                           f"{' (due ' + txn['due_date'] + ')' if txn.get('due_date') else ''}. "
                           f"{'For: ' + txn['description'] + '. ' if txn.get('description') else ''}"
                           "Please pay when convenient. Thanks!")
                else:
                    msg = (f"Reminder to self: I owe {txn['party_name']} {format_currency(txn['amount'])}"
                           f"{' by ' + txn['due_date'] if txn.get('due_date') else ''}. "
                           f"{'For: ' + txn['description'] + '.' if txn.get('description') else ''}")
                st.code(msg, language=None)
                st.caption("Copy and send on WhatsApp.")
        st.markdown('</div>', unsafe_allow_html=True)

    if settled:
        with st.expander(f"Settled ({len(settled)})"):
            for txn in settled:
                color = T['accent'] if txn["txn_type"]=="gave" else "#f87171"
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;padding:7px 0;"
                    f"border-bottom:1px solid {T['border']};'>"
                    f"<span style='font-size:12px;color:{T['muted']};'>{txn['party_name']} — {txn.get('description','') or '—'}</span>"
                    f"<span style='font-family:Space Mono,monospace;font-size:13px;color:{color};"
                    f"text-decoration:line-through;'>{format_currency(txn['amount'])}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    if not all_txns:
        st.markdown(
            f"<div class='card' style='text-align:center;padding:40px;color:{T['muted']};'>"
            "No transactions yet. Add one above.</div>",
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
    level_colors = {"Beginner": T['accent'], "Intermediate": "#f59e0b", "Advanced": "#f87171"}

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Financial Education — Story-Based Learning")
    st.markdown(
        f"<p style='font-size:13px;color:{T['muted']};margin:0 0 14px 0;'>"
        "Each module starts with a real story about a real person's financial moment. "
        "Then the lesson. Then the key takeaway. 5–10 minutes each.</p>",
        unsafe_allow_html=True,
    )
    lp1, lp2, lp3 = st.columns(3)
    lp1.metric("Completed",  f"{done_ct} / {total_m}")
    lp2.metric("XP Earned",  f"{done_ct * 25}")
    lp3.metric("Progress",   f"{int(done_ct / total_m * 100)}%")
    st.markdown(bar(int(done_ct / total_m * 100)), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    modules_by_level = get_modules_by_level()
    for level_name, modules in modules_by_level.items():
        lc = level_colors.get(level_name, T['accent'])
        st.markdown(
            f"<div style='font-size:16px;font-weight:800;color:{lc};"
            f"margin:22px 0 10px 0;'>{level_name}</div>",
            unsafe_allow_html=True,
        )
        for mod in modules:
            is_done   = mod.get("id","") in done_ids
            title     = mod.get("title", "Module")
            duration  = mod.get("duration", "5 min")
            xp_val    = mod.get("xp", 20)
            content   = mod.get("content", "")
            story     = mod.get("story", "")
            takeaway  = mod.get("key_takeaway", mod.get("takeaway", ""))
            book_t    = mod.get("book_title", "")
            book_a    = mod.get("book_author", "")
            free_link = mod.get("free_link", "https://openlibrary.org")
            buy_link  = mod.get("buy_link", "https://www.amazon.in")

            status = "  ✓" if is_done else f"  ·  {duration}  ·  +{xp_val} XP"

            with st.expander(f"{title}{status}"):
                # Story first
                if story.strip():
                    st.markdown(
                        f"<div class='story'><span class='story-label'>A real story</span>"
                        f"{story.strip()}</div>",
                        unsafe_allow_html=True,
                    )
                # Content
                if content.strip():
                    st.markdown(
                        f"<div style='font-size:13px;color:{T['sub']};line-height:1.85;"
                        f"white-space:pre-line;margin-bottom:12px;'>{content.strip()}</div>",
                        unsafe_allow_html=True,
                    )
                # Takeaway
                if takeaway:
                    st.markdown(
                        f"<div style='background:{T['green_bg']};border:1px solid {T['green_br']};"
                        f"border-radius:8px;padding:12px 16px;margin-bottom:10px;'>"
                        f"<div style='font-size:9px;color:{T['muted']};text-transform:uppercase;"
                        f"letter-spacing:0.14em;margin-bottom:5px;'>Key Takeaway</div>"
                        f"<div style='font-size:13px;color:{T['accent']};font-weight:600;line-height:1.5;'>"
                        f"{takeaway}</div></div>",
                        unsafe_allow_html=True,
                    )
                # Book link
                if book_t:
                    st.markdown(
                        f"<div style='font-size:12px;color:{T['muted']};margin-bottom:10px;'>"
                        f"Recommended: <strong style='color:{T['sub']};'>{book_t}</strong> by {book_a}"
                        f"  ·  <a href='{buy_link}' target='_blank' style='color:{T['accent']};"
                        f"text-decoration:none;font-weight:700;'>Buy →</a>"
                        f"  <a href='{free_link}' target='_blank' style='color:{T['muted']};"
                        f"text-decoration:none;'>Free version →</a></div>",
                        unsafe_allow_html=True,
                    )
                if not is_done:
                    if st.button(f"Mark complete  +{xp_val} XP", key=f"mod_{mod.get('id',title)}"):
                        mark_module_complete(un, mod.get("id", title))
                        st.success("Module complete!")
                        st.rerun()
                else:
                    st.markdown(f"<span style='font-size:11px;color:{T['accent']};'>✓ Completed</span>", unsafe_allow_html=True)

    # Book list
    if BOOK_LIST:
        st.markdown(
            f"<div style='font-size:18px;font-weight:800;color:{T['text']};margin:28px 0 12px 0;'>Reading List — 14 Essential Books</div>",
            unsafe_allow_html=True,
        )
        bl1, bl2 = st.columns(2)
        for i, book in enumerate(BOOK_LIST):
            lc = level_colors.get(book.get("level","Beginner"), T['accent'])
            buy_l  = book.get("buy_link",  "https://www.amazon.in")
            free_l = book.get("free_link", "https://openlibrary.org")
            with (bl1 if i % 2 == 0 else bl2):
                st.markdown(
                    f"<div class='book'>"
                    f"<div style='display:flex;justify-content:space-between;align-items:flex-start;gap:8px;'>"
                    f"<div style='font-size:14px;font-weight:700;color:{T['text']};'>{book['title']}</div>"
                    f"<span style='font-size:9px;color:{lc};text-transform:uppercase;letter-spacing:0.1em;"
                    f"font-weight:700;white-space:nowrap;'>{book.get('level','')}</span></div>"
                    f"<div style='font-size:11px;color:{T['muted']};margin:2px 0 5px;'>by {book['author']}</div>"
                    f"<div style='font-size:12px;color:{T['sub']};line-height:1.6;'>{book.get('why','')}</div>"
                    f"<div style='margin-top:8px;display:flex;gap:12px;'>"
                    f"<a href='{buy_l}' target='_blank' style='font-size:11px;color:{T['accent']};"
                    f"text-decoration:none;font-weight:700;'>Buy on Amazon →</a>"
                    f"<a href='{free_l}' target='_blank' style='font-size:11px;color:{T['muted']};"
                    f"text-decoration:none;'>Free version →</a>"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )

    # Free resources
    if FREE_RESOURCES:
        st.markdown(
            f"<div style='font-size:16px;font-weight:800;color:{T['text']};margin:24px 0 10px 0;'>Free Online Resources</div>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for res in FREE_RESOURCES:
            st.markdown(
                f"<div style='padding:10px 0;border-bottom:1px solid {T['border']};'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<div style='font-size:13px;color:{T['text']};font-weight:700;'>{res['name']}</div>"
                f"<a href='{res['url']}' target='_blank' style='font-size:11px;color:{T['accent']};"
                f"text-decoration:none;font-weight:700;white-space:nowrap;'>Visit →</a></div>"
                f"<div style='font-size:11px;color:{T['muted']};margin-top:3px;'>{res['desc']}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# COMMUNITY TAB
# ════════════════════════════════════════════
with t_comm:
    TOPICS = ["All","Saving Tips","Investing","Debt & EMIs",
              "Career & Income","Students","Budgeting","General Finance"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Community Discussions")
    st.markdown(f"<p style='font-size:12px;color:{T['muted']};margin:0 0 12px 0;'>Finance topics only. Be kind. Be useful.</p>", unsafe_allow_html=True)
    topic_filter = st.selectbox("Filter by topic", TOPICS)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Write a New Post"):
        np_topic = st.selectbox("Topic", TOPICS[1:], key="np_topic")
        np_text  = st.text_area("Your post", placeholder="Share a tip, ask a question...", height=100)
        np_anon  = st.checkbox("Post anonymously")
        if st.button("PUBLISH", key="post_btn"):
            if len(np_text.strip()) >= 20:
                add_post(un, un, np_topic, np_text.strip(), np_anon)
                st.success("Post published."); st.rerun()
            else:
                st.warning("Write at least 20 characters.")

    posts = get_posts(topic_filter if topic_filter != "All" else None, 30)
    if posts:
        for post in posts:
            is_mine = post["username"] == un
            st.markdown(
                f'<div class="post"><span class="ptag">{post["topic"]}</span>'
                f'<div class="paut">{post["display_name"]}  ·  {post["created_at"][:10]}</div>'
                f'<div class="ptxt">{post["content"]}</div>'
                f'<div class="pft">{post["upvotes"]} upvotes</div></div>',
                unsafe_allow_html=True,
            )
            ub1, ub2 = st.columns([1, 8])
            with ub1:
                if st.button("Upvote", key=f"up_{post['id']}"):
                    upvote_post(un, post["id"]); st.rerun()
            if is_mine:
                with ub2:
                    if st.button("Delete", key=f"dp_{post['id']}"):
                        delete_post(post["id"], un); st.rerun()
    else:
        st.markdown(
            f"<div class='card' style='text-align:center;padding:36px;color:{T['muted']};'>"
            "No posts here yet. Be the first.</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════
# INSIGHTS TAB
# ════════════════════════════════════════════
with t_insights:
    score_hist2 = get_score_history(un, 30)
    monthly_exp2= get_monthly_expenses(un)
    insights    = get_behavioral_insights(score_hist2, monthly_exp2)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Behavioral Insights")
    for insight in insights:
        st.markdown(
            f"<div style='padding:12px 16px;border-left:3px solid {T['accent']};background:{T['green_bg']};"
            f"border-radius:0 8px 8px 0;margin-bottom:8px;font-size:13px;color:{T['sub']};line-height:1.7;'>"
            f"{insight}</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.last_result:
        surplus_    = st.session_state.last_income - st.session_state.last_expenses
        current_sav = st.session_state.last_savings
        monthly_e   = st.session_state.last_expenses
        ef_months   = predict_emergency_fund_date(current_sav, surplus_, monthly_e, 6)
        fire_yrs    = predict_fire_date(current_sav, surplus_, monthly_e * 12)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Time to Reach Your Targets")
        pr1, pr2 = st.columns(2)
        with pr1:
            if ef_months == 0:
                st.markdown(f"<div class='card-green'><span class='lbl'>6-Month Emergency Fund</span><div style='font-family:Space Mono,monospace;font-size:26px;color:{T['accent']};font-weight:700;'>Achieved</div><div style='font-size:11px;color:{T['muted']};margin-top:4px;'>You have hit this target.</div></div>", unsafe_allow_html=True)
            elif ef_months:
                st.markdown(f"<div class='card-flat'><span class='lbl'>6-Month Emergency Fund</span><div style='font-family:Space Mono,monospace;font-size:26px;color:#f59e0b;font-weight:700;'>{ef_months} months</div><div style='font-size:11px;color:{T['muted']};margin-top:4px;'>At current savings rate.</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='card-red'><span class='lbl'>6-Month Emergency Fund</span><div style='font-size:13px;color:#f87171;'>Cannot reach at current rate.</div><div style='font-size:11px;color:{T['muted']};margin-top:4px;'>Create a monthly surplus first.</div></div>", unsafe_allow_html=True)
        with pr2:
            if fire_yrs == 0:
                st.markdown(f"<div class='card-green'><span class='lbl'>FIRE Number</span><div style='font-family:Space Mono,monospace;font-size:26px;color:{T['accent']};font-weight:700;'>Achieved</div></div>", unsafe_allow_html=True)
            elif fire_yrs:
                st.markdown(f"<div class='card-flat'><span class='lbl'>FIRE Number</span><div style='font-family:Space Mono,monospace;font-size:26px;color:#3b82f6;font-weight:700;'>{fire_yrs} years</div><div style='font-size:11px;color:{T['muted']};margin-top:4px;'>Without investment returns — actual shorter.</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='card-red'><span class='lbl'>FIRE Number</span><div style='font-size:13px;color:#f87171;'>Need positive surplus first.</div></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Leaderboard
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Global Safety Leaderboard")
    lb_data = get_leaderboard(20)
    if lb_data:
        for i, e in enumerate(lb_data):
            is_me      = e["username"] == un
            bg         = T['green_bg'] if is_me else T['surface']
            border     = f"1px solid {T['green_br']}" if is_me else f"1px solid {T['border']}"
            rank       = f"0{i+1}" if i + 1 < 10 else str(i+1)
            name_style = f"color:{T['accent']};font-weight:700;" if is_me else ""
            st.markdown(
                f"<div class='lbr' style='background:{bg};border:{border};'>"
                f"<span class='lrk'>{rank}</span>"
                f"<span class='lnm' style='{name_style}'>"
                f"{e['username']}{'  (you)' if is_me else ''}</span>"
                f"<span class='llv'>{e['level_name']}</span>"
                f"<span class='llv'>{e['persona']}</span>"
                f"<span class='lsc'>{e['score']:.1f}</span></div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(f"<p style='font-size:12px;color:{T['muted']};'>No scores yet. Calculate yours first.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Survey
    SURVEY_Q    = "What is your biggest financial challenge right now?"
    SURVEY_OPTS = ["Not saving enough each month","Too much debt or EMIs","No emergency fund",
                   "Irregular or uncertain income","Don't know where to invest",
                   "Spending more than I earn","No clear financial plan"]
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Community Survey")
    if not has_answered_survey(un, SURVEY_Q):
        st.markdown(f"<div style='font-size:14px;color:{T['text']};font-weight:700;margin-bottom:12px;'>{SURVEY_Q}</div>", unsafe_allow_html=True)
        answer = st.radio("Pick your answer", SURVEY_OPTS, label_visibility="collapsed")
        if st.button("SUBMIT", key="survey_btn"):
            save_survey_response(un, SURVEY_Q, answer)
            st.success("Thank you. Response recorded."); st.rerun()
    else:
        responses = get_survey_responses(SURVEY_Q)
        total_r   = max(len(responses), 1)
        counts    = {}
        for r in responses:
            counts[r["answer"]] = counts.get(r["answer"], 0) + 1
        st.markdown(f"<div style='font-size:13px;color:{T['sub']};font-weight:700;margin-bottom:12px;'>Results — {len(responses)} responses</div>", unsafe_allow_html=True)
        for opt in SURVEY_OPTS:
            cnt = counts.get(opt, 0)
            pct = int(cnt / total_r * 100) if total_r > 0 else 0
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;'>"
                f"<span style='color:{T['sub']};'>{opt}</span>"
                f"<span style='font-family:Space Mono,monospace;color:{T['text']};'>{pct}% ({cnt})</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown(bar(pct, T['muted']), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# ME / PROFILE TAB
# ════════════════════════════════════════════
with t_me:
    score_hist3 = get_score_history(un, 30)
    done_ids3   = {mid for mid, done in get_education_progress(un).items() if done}
    lv_current  = get_level(st.session_state.last_result["composite_score"]) if st.session_state.last_result else get_level(0)
    latest_sc   = score_hist3[0]["score"] if score_hist3 else 0

    # Profile card
    st.markdown(
        f"<div class='profile-card'>"
        f"<div style='font-family:Space Mono,monospace;font-size:54px;font-weight:700;"
        f"color:{T['accent']};line-height:1;margin-bottom:14px;'>{un[0].upper()}</div>"
        f"<div style='font-size:24px;font-weight:800;color:{T['text']};margin-bottom:4px;'>{un}</div>"
        f"<div style='font-size:13px;color:{T['sub']};'>"
        f"{PERSONAS[st.session_state.persona_name]['icon']}  {st.session_state.persona_name}"
        f"{'  ·  ' + profile.get('city','') if profile.get('city') else ''}"
        f"{'  ·  Age ' + str(profile.get('age','')) if profile.get('age') else ''}"
        f"</div>"
        f"<div style='display:flex;gap:8px;margin-top:14px;flex-wrap:wrap;'>"
        f"{level_tag(lv_current['name'])}"
        f"<span style='font-size:10px;color:{T['muted']};background:{T['bg']};border:1px solid {T['border']};"
        f"border-radius:4px;padding:3px 10px;font-weight:700;'>⚡ {xp_total} XP</span>"
        f"<span style='font-size:10px;color:{T['muted']};background:{T['bg']};border:1px solid {T['border']};"
        f"border-radius:4px;padding:3px 10px;font-weight:700;'>🔥 {settings_['streak']} days</span>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    me1, me2, me3, me4 = st.columns(4)
    me1.metric("Safety Score",  f"{latest_sc:.0f} / 100")
    me2.metric("Scores Logged", len(score_hist3))
    me3.metric("Modules Done",  f"{len(done_ids3)} / {total_m}")
    me4.metric("Total XP",      xp_total)

    # Edit profile
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Edit Profile")
    ep1, ep2 = st.columns(2)
    with ep1:
        new_name = st.text_input("Display Name", value=un, key="ep_name")
        new_city = st.text_input("City", value=profile.get("city",""), key="ep_city")
    with ep2:
        new_age  = st.number_input("Age", min_value=16, max_value=80,
                                    value=int(profile.get("age",25)), step=1)
        new_persona = st.selectbox(
            "Profile Type", list(PERSONAS.keys()),
            index=list(PERSONAS.keys()).index(st.session_state.persona_name),
            format_func=lambda x: f"{PERSONAS[x]['icon']}  {x}",
        )
    if st.button("SAVE PROFILE", key="save_profile"):
        upsert_user_profile(un, new_name, new_persona, int(new_age), new_city)
        st.session_state.persona_name = new_persona
        st.success("Profile saved."); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Score history chart
    if score_hist3 and PLOTLY and len(score_hist3) > 1:
        d3_ = build_score_trend_data(score_hist3)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lbl("Score Over Time")
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=d3_["dates"], y=d3_["scores"], mode="lines+markers",
            line={"color":T['accent'],"width":2.5}, marker={"color":T['accent'],"size":7},
            fill="tozeroy", fillcolor=f"{T['accent']}10"))
        fig5.add_hline(y=65, line_dash="dot", line_color=T['muted'],
                       annotation_text="Safe zone")
        fig5.update_layout(**plotly_cfg(), height=220)
        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Challenges
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("All Challenges")
    for ch in get_challenges():
        done = ch["id"] in st.session_state.get("challenges_done", set())
        ca_, cb_ = st.columns([5, 1])
        with ca_:
            ch_col = T['muted'] if done else T['text']
            ch_td  = "text-decoration:line-through;" if done else ""
            ch_xp_col = T['accent'] if done else T['muted']
            ch_tick = "✓" if done else ""
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;align-items:center;"
                f"padding:9px 0;border-bottom:1px solid {T['border']};'>"
                f"<div><div style='font-size:13px;color:{ch_col};font-weight:600;{ch_td}'>{ch['name']}</div>"
                f"<div style='font-size:11px;color:{T['muted']};margin-top:2px;'>{ch['desc']}</div></div>"
                f"<div style='font-family:Space Mono,monospace;font-size:12px;"
                f"color:{ch_xp_col};font-weight:700;'>"
                f"{ch_tick} +{ch['reward_xp']}</div></div>",
                unsafe_allow_html=True,
            )
        with cb_:
            if not done:
                if st.button("Done", key=f"me_ch_{ch['id']}"):
                    save_challenge(un, ch["id"])
                    st.session_state.challenges_done.add(ch["id"])
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Share
    st.markdown('<div class="card">', unsafe_allow_html=True)
    lbl("Share Your Score")
    if st.session_state.last_result:
        sc_ = st.session_state.last_result["composite_score"]
        risk_ = st.session_state.last_result["risk_level"]
        msg_ = (f"My Financial Safety Score on Finverse: {sc_:.0f}/100 ({risk_})\n"
                f"It tells you if you're actually financially safe — not just whether you have money.\n"
                f"Check yours free: [your Finverse link here]")
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
    f"<div style='text-align:center;padding:24px 0 0;border-top:1px solid {T['border']};margin-top:12px;'>"
    f"<span style='font-size:13px;font-weight:800;color:{T['border']};'>FINVERSE</span>"
    f"<span style='font-size:11px;color:{T['border']};margin-left:12px;'>v9.0</span>"
    f"<span style='font-size:11px;color:{T['border']};margin-left:12px;'>Built in India</span>"
    f"<span style='font-size:11px;color:{T['border']};margin-left:12px;'>{T['mode_icon']} {st.session_state.theme} mode</span>"
    f"</div>",
    unsafe_allow_html=True,
)
