# app.py
# ─────────────────────────────────────────────
# Finverse – Financial Stability Platform v2.0
# Run: streamlit run app.py
# ─────────────────────────────────────────────

import streamlit as st
from datetime import datetime

from logic import (
    analyse_finances,
    analyse_compatibility,
    recommended_partner_income,
    calculate_savings_rules,
)
from config import PERSONAS
from gamification import get_level, get_next_level, get_badges, get_challenges, get_total_xp
from utils import (
    format_currency, format_percent, format_months,
    get_savings_rate_message, get_survival_message, get_risk_advice,
)

# ── PAGE CONFIG ──────────────────────────────
st.set_page_config(
    page_title="Finverse – Financial Safety",
    page_icon="💰",
    layout="centered",
)

# ── SESSION STATE ────────────────────────────
# All data that needs to persist across reruns
defaults = {
    "daily_expenses":      [],
    "daily_budget":        1000.0,
    "streak":              1,
    "challenges_done":     set(),
    "my_score":            None,
    "my_name":             "",
    "leaderboard": [
        {"name": "Priya S.",  "score": 82.3, "level": "🥇 Gold"},
        {"name": "Rahul M.",  "score": 74.1, "level": "🥇 Gold"},
        {"name": "Aisha K.",  "score": 68.5, "level": "🥇 Gold"},
        {"name": "Vikram N.", "score": 61.2, "level": "🥈 Silver"},
        {"name": "Sneha R.",  "score": 55.8, "level": "🥈 Silver"},
        {"name": "Arjun T.",  "score": 44.3, "level": "🥈 Silver"},
        {"name": "Meera P.",  "score": 38.7, "level": "🥉 Bronze"},
    ],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── HEADER ───────────────────────────────────
st.title("💰 Finverse")
st.caption("Your Personal Financial Safety Platform")

# ── SIDEBAR ──────────────────────────────────
with st.sidebar:
    st.markdown("### 👤 Select Your Profile")
    persona_name = st.selectbox(
        "Who are you?",
        list(PERSONAS.keys()),
        index=1,
        help="Different life stages have different financial targets.",
    )
    persona = PERSONAS[persona_name]

    st.markdown(f"**Savings Rate Target:** {persona['savings_rate_target']}%")
    st.markdown(f"**Emergency Fund Goal:** {persona['survival_target']} months")

    st.divider()
    st.markdown("### 💡 Tips for You")
    for tip in persona["tips"]:
        st.caption(f"• {tip}")

    st.divider()
    total_xp = get_total_xp(st.session_state.challenges_done)
    st.metric("⚡ Total XP Earned", f"{total_xp} XP")
    st.caption("Complete challenges to earn XP →")

    st.divider()
    st.caption("Finverse v2.0 · Not financial advice")


# ── TABS ─────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 My Score",
    "📅 Daily Tracker",
    "💑 Partner Test",
    "🏆 Leaderboard",
    "📚 Money Rules",
])


# ════════════════════════════════════════════
# TAB 1 — MY SCORE
# ════════════════════════════════════════════
with tab1:
    st.markdown("### 📥 Your Financial Snapshot")

    c1, c2 = st.columns(2)
    with c1:
        income = st.number_input(
            persona["income_label"],
            min_value=0.0, value=50000.0, step=1000.0, key="t1_inc",
        )
        savings = st.number_input(
            "Total Savings (₹)",
            min_value=0.0, value=120000.0, step=5000.0, key="t1_sav",
        )
    with c2:
        expenses = st.number_input(
            "Monthly Expenses (₹)",
            min_value=0.0, value=35000.0, step=1000.0, key="t1_exp",
        )

    if st.button("📊 Calculate My Score", use_container_width=True, key="t1_btn"):
        if income <= 0:
            st.error("Please enter a valid income greater than 0.")
            st.stop()

        result = analyse_finances(income, expenses, savings)
        risk   = result["risk_level"]
        score  = result["composite_score"]
        level  = get_level(score)
        next_l = get_next_level(score)
        badges = get_badges(result)

        # Save score to session state for leaderboard use
        st.session_state.my_score = score

        st.divider()

        # ── LEVEL CARD ──────────────────────
        st.markdown("### 🎮 Your Financial Level")
        st.markdown(
            f"""
            <div style="
                background: {level['color']};
                border-radius: 12px;
                padding: 24px;
                text-align: center;
            ">
                <div style="font-size: 56px; margin: 0;">{level['icon']}</div>
                <h2 style="margin: 8px 0 4px 0;">{level['name']} Level</h2>
                <p style="margin: 0; color: #555; font-size: 15px;">{level['message']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"**Financial Health Score: {score} / 100**")
        st.progress(int(score))

        if next_l:
            st.caption(
                f"🎯 You need **{next_l['points_needed']} more points** "
                f"to reach {next_l['icon']} {next_l['name']}!"
            )
        else:
            st.caption("🏆 Maximum level reached — Platinum!")

        st.divider()

        # ── RISK BANNER ─────────────────────
        risk_cfg = {
            "SAFE":     ("✅ SAFE",     "#d4edda", "green",      "Strong financial position."),
            "MODERATE": ("⚠️ MODERATE", "#fff3cd", "darkorange", "Stable, but improve your cushion."),
            "RISKY":    ("🔴 RISKY",    "#f8d7da", "crimson",    "Needs immediate attention."),
        }
        badge_txt, bg, color, headline = risk_cfg[risk]
        st.markdown(
            f"""<div style="background:{bg}; border-left:6px solid {color};
                        padding:16px; border-radius:8px; margin-bottom:8px;">
                <h3 style="color:{color}; margin:0;">{badge_txt}</h3>
                <p style="margin:4px 0 0 0;">{headline}</p>
                <p style="margin:4px 0 0 0; font-size:13px; color:#555;">
                    {get_risk_advice(risk)}
                </p>
            </div>""",
            unsafe_allow_html=True,
        )

        st.divider()

        # ── KEY METRICS ─────────────────────
        st.markdown("### 📊 Key Metrics")
        m1, m2, m3 = st.columns(3)

        with m1:
            sr = result["savings_rate"]
            st.metric("💾 Savings Rate", format_percent(sr))
            st.progress(min(100, max(0, int(sr * 100 / 30))))
            st.caption(get_savings_rate_message(sr))
            target = persona["savings_rate_target"]
            if sr < target:
                st.caption(f"🎯 Your target: {target}%")

        with m2:
            sm = result["survival_months"]
            st.metric("🛟 Survival Time", format_months(sm))
            st.progress(min(100, int(sm / 12 * 100)))
            st.caption(get_survival_message(sm))
            target = persona["survival_target"]
            if sm < target:
                st.caption(f"🎯 Your target: {target} months")

        with m3:
            er = result["expense_ratio"]
            st.metric("📤 Expense Ratio", format_percent(er))
            st.progress(min(100, int(er)))
            warn = persona["expense_ratio_warning"]
            if er >= warn:
                st.caption(f"⚠️ High for your profile (>{warn}%)")

        st.divider()

        # ── BADGES ──────────────────────────
        if badges:
            st.markdown("### 🏅 Earned Badges")
            badge_cols = st.columns(min(len(badges), 3))
            for i, b in enumerate(badges):
                with badge_cols[i % 3]:
                    st.markdown(
                        f"""<div style="background:#f0f9ff; border:1px solid #b3d9f7;
                                    border-radius:8px; padding:10px; text-align:center;
                                    margin-bottom:8px;">
                            <b>{b['name']}</b><br>
                            <small style="color:#666;">{b['desc']}</small>
                        </div>""",
                        unsafe_allow_html=True,
                    )

        st.divider()

        # ── MONTHLY SUMMARY ─────────────────
        st.markdown("### 💼 Monthly Summary")
        surplus = income - expenses
        ms1, ms2, ms3 = st.columns(3)
        ms1.metric("Income",   format_currency(income))
        ms2.metric("Expenses", format_currency(expenses))
        ms3.metric(
            "Monthly Surplus" if surplus >= 0 else "Monthly Deficit",
            format_currency(abs(surplus)),
            delta_color="normal" if surplus >= 0 else "inverse",
        )

        st.divider()

        # ── CHALLENGES ──────────────────────
        st.markdown("### 🎯 Active Challenges")
        st.caption("Complete challenges to earn XP and improve your score.")
        for ch in get_challenges():
            done = ch["id"] in st.session_state.challenges_done
            col_a, col_b = st.columns([5, 1])
            with col_a:
                label = f"~~{ch['name']}~~" if done else f"**{ch['name']}**"
                st.markdown(f"{label} {'✅' if done else ''}")
                st.caption(f"{ch['desc']} · +{ch['reward_xp']} XP")
            with col_b:
                if not done:
                    if st.button("Done ✓", key=f"ch_{ch['id']}"):
                        st.session_state.challenges_done.add(ch["id"])
                        st.rerun()


# ════════════════════════════════════════════
# TAB 2 — DAILY TRACKER
# ════════════════════════════════════════════
with tab2:
    st.markdown("### 📅 Daily Expense Tracker")
    st.caption("Track spending every day to build the habit. Your streak grows each day you track! 🔥")

    # Streak + Budget
    sb1, sb2 = st.columns(2)
    with sb1:
        st.metric("🔥 Tracking Streak", f"{st.session_state.streak} day(s)")
    with sb2:
        st.session_state.daily_budget = st.number_input(
            "Daily Budget (₹)",
            min_value=0.0,
            value=st.session_state.daily_budget,
            step=100.0,
        )

    st.divider()

    # Add expense
    st.markdown("#### ➕ Add an Expense")
    ea, eb, ec = st.columns([2, 2, 3])
    with ea:
        category = st.selectbox("Category", [
            "🍜 Food", "🚗 Transport", "🛒 Shopping",
            "💡 Bills", "🎬 Entertainment", "💊 Health",
            "📚 Education", "🎁 Others",
        ])
    with eb:
        exp_amount = st.number_input(
            "Amount (₹)", min_value=0.0, value=0.0, step=10.0, key="exp_amt"
        )
    with ec:
        note = st.text_input("Note (optional)", placeholder="e.g. Lunch at office")

    if st.button("➕ Add Expense", use_container_width=True):
        if exp_amount > 0:
            st.session_state.daily_expenses.append({
                "category": category,
                "amount":   exp_amount,
                "note":     note or "—",
                "time":     datetime.now().strftime("%H:%M"),
            })
            st.rerun()
        else:
            st.warning("Enter an amount greater than 0.")

    st.divider()

    # Today's summary
    if st.session_state.daily_expenses:
        total_spent = sum(e["amount"] for e in st.session_state.daily_expenses)
        budget      = st.session_state.daily_budget
        remaining   = budget - total_spent
        pct         = min(100, int(total_spent / budget * 100)) if budget > 0 else 100

        st.markdown("#### 📊 Today's Summary")
        ds1, ds2, ds3 = st.columns(3)
        ds1.metric("Spent",      format_currency(total_spent))
        ds2.metric("Budget",     format_currency(budget))
        ds3.metric(
            "Left" if remaining >= 0 else "Over Budget",
            format_currency(abs(remaining)),
            delta_color="normal" if remaining >= 0 else "inverse",
        )

        if pct >= 90:
            st.error(f"⚠️ Budget Alert! You've used {pct}% of your daily budget.")
        elif pct >= 70:
            st.warning(f"You've used {pct}% of your daily budget.")
        else:
            st.success(f"On track — used {pct}% of daily budget.")
        st.progress(pct)

        st.divider()

        # Expense list
        st.markdown("#### 📋 Today's Expenses")
        for exp in reversed(st.session_state.daily_expenses):
            el, er = st.columns([4, 1])
            with el:
                st.markdown(
                    f"**{exp['category']}** · {exp['note']} · "
                    f"<small style='color:#888;'>{exp['time']}</small>",
                    unsafe_allow_html=True,
                )
            with er:
                st.markdown(f"**{format_currency(exp['amount'])}**")

        st.divider()

        # Category breakdown
        st.markdown("#### 🥧 By Category")
        cat_totals = {}
        for exp in st.session_state.daily_expenses:
            cat_totals[exp["category"]] = cat_totals.get(exp["category"], 0) + exp["amount"]

        for cat, amt in sorted(cat_totals.items(), key=lambda x: -x[1]):
            cat_pct = int(amt / total_spent * 100) if total_spent > 0 else 0
            st.write(f"{cat}: **{format_currency(amt)}** ({cat_pct}%)")
            st.progress(cat_pct)

        st.divider()
        if st.button("✅ End Day & Save Streak", use_container_width=True):
            st.session_state.daily_expenses = []
            st.session_state.streak += 1
            st.success(f"Day saved! Streak: {st.session_state.streak} 🔥")
            st.rerun()

    else:
        st.info(
            "No expenses added yet today. Start tracking to keep your streak alive! 🔥\n\n"
            "**Why track?** People who track spending save 15–20% more on average."
        )


# ════════════════════════════════════════════
# TAB 3 — PARTNER TEST
# ════════════════════════════════════════════
with tab3:
    st.markdown("### 💑 Partner Financial Compatibility Test")
    st.caption(
        "How financially compatible are you two? "
        "Find out your combined health score and plan your future together."
    )

    st.markdown("#### Enter Both Financial Profiles")
    pc1, pc2 = st.columns(2)

    with pc1:
        st.markdown("**👤 You**")
        p1_inc = st.number_input("Your Income (₹/month)",   min_value=0.0, value=50000.0, step=1000.0, key="p1i")
        p1_exp = st.number_input("Your Expenses (₹/month)", min_value=0.0, value=35000.0, step=1000.0, key="p1e")
        p1_sav = st.number_input("Your Savings (₹ total)",  min_value=0.0, value=120000.0, step=5000.0, key="p1s")

    with pc2:
        st.markdown("**👤 Partner**")
        p2_inc = st.number_input("Partner's Income (₹/month)",   min_value=0.0, value=45000.0, step=1000.0, key="p2i")
        p2_exp = st.number_input("Partner's Expenses (₹/month)", min_value=0.0, value=30000.0, step=1000.0, key="p2e")
        p2_sav = st.number_input("Partner's Savings (₹ total)",  min_value=0.0, value=80000.0, step=5000.0, key="p2s")

    st.divider()

    if st.button("💑 Calculate Compatibility", use_container_width=True):
        r1     = analyse_finances(p1_inc, p1_exp, p1_sav)
        r2     = analyse_finances(p2_inc, p2_exp, p2_sav)
        compat = analyse_compatibility(r1, r2)
        cs     = compat["compatibility_score"]

        # Compatibility banner
        if cs >= 75:
            c_label, c_msg, c_bg, c_border = (
                "💚 Excellent Match", "Financially well-aligned. Great foundation!", "#d4edda", "green"
            )
        elif cs >= 55:
            c_label, c_msg, c_bg, c_border = (
                "💛 Good Match", "Solid. A few money conversations will strengthen the bond.", "#fffde7", "goldenrod"
            )
        elif cs >= 35:
            c_label, c_msg, c_bg, c_border = (
                "🟠 Needs Work", "Some gaps exist. Open discussions about money are key.", "#fff3cd", "orange"
            )
        else:
            c_label, c_msg, c_bg, c_border = (
                "🔴 Financial Mismatch", "Significant differences. Discuss and align before big commitments.", "#f8d7da", "crimson"
            )

        st.markdown(
            f"""<div style="background:{c_bg}; border-left:6px solid {c_border};
                        padding:20px; border-radius:8px; text-align:center;">
                <h2 style="margin:0;">{c_label}</h2>
                <h1 style="color:{c_border}; margin:8px 0;">{cs:.0f} / 100</h1>
                <p style="margin:0;">{c_msg}</p>
            </div>""",
            unsafe_allow_html=True,
        )

        st.divider()

        # Individual vs combined
        st.markdown("#### 📊 Individual Scores")
        is1, is2, is3 = st.columns(3)
        is1.metric("Your Score",      f"{r1['composite_score']} / 100")
        is2.metric("Partner's Score", f"{r2['composite_score']} / 100")
        is3.metric("Alignment",       f"{compat['alignment_score']} / 100",
                   help="How similar your financial behaviors are.")

        st.divider()
        st.markdown("#### 🏠 Combined Financial Picture")
        combined = compat["combined"]
        cf1, cf2, cf3, cf4 = st.columns(4)
        cf1.metric("Combined Income",   format_currency(combined["income"]))
        cf2.metric("Combined Expenses", format_currency(combined["expenses"]))
        cf3.metric("Combined Savings",  format_currency(combined["savings"]))
        cf4.metric("Survive Together",  format_months(combined["survival_months"]))

        st.markdown(f"**Combined Financial Score: {combined['composite_score']} / 100**")
        st.progress(int(combined["composite_score"]))

        surplus = compat["combined_surplus"]
        if surplus >= 0:
            st.success(f"✅ Combined monthly surplus: {format_currency(surplus)}")
        else:
            st.error(f"⚠️ Combined monthly deficit: {format_currency(abs(surplus))}")

        st.divider()
        st.info(
            f"**Stronger saver:** {compat['stronger_saver']}  ·  "
            f"Your savings rate: {r1['savings_rate']}%  ·  "
            f"Partner's savings rate: {r2['savings_rate']}%"
        )

        st.divider()

        # Ideal partner income calculator
        st.markdown("#### 🎯 What Should Your Partner Earn?")
        st.caption(
            "Based on your finances, this is what your partner should ideally earn "
            "for a financially stable life together."
        )
        t_sr = st.slider("Target Combined Savings Rate (%)", 10, 40, 20, key="tsr")
        t_sm = st.slider("Target Emergency Fund (months)",    3, 12,  6, key="tsm")

        rec = recommended_partner_income(p1_inc, p1_exp, p1_sav, t_sr, t_sm)

        ri1, ri2, ri3 = st.columns(3)
        ri1.metric("Min. Partner Income",   format_currency(rec["min_partner_income"]),   "per month")
        ri2.metric("Combined Savings Goal", format_currency(rec["target_combined_savings"]), "emergency fund")
        ri3.metric("Partner Save Monthly",  format_currency(rec["partner_monthly_savings_target"]), "to reach goal")

        st.caption(
            f"Assumption: Shared life costs ≈ {format_currency(rec['estimated_combined_expenses'])}/month "
            f"(your expenses × 1.6 for shared living)."
        )


# ════════════════════════════════════════════
# TAB 4 — LEADERBOARD
# ════════════════════════════════════════════
with tab4:
    st.markdown("### 🏆 Financial Leaderboard")
    st.caption("See how you rank. Calculate your score in 'My Score' first, then join the board.")

    # Add to leaderboard
    st.markdown("#### 📝 Add Your Score")
    lb_c1, lb_c2 = st.columns([3, 1])
    with lb_c1:
        name_input = st.text_input(
            "Your name or nickname",
            value=st.session_state.my_name,
            placeholder="e.g. Aashi",
        )
    with lb_c2:
        if st.session_state.my_score:
            st.metric("Your Score", f"{st.session_state.my_score:.1f}")
        else:
            st.warning("Go to 'My Score' tab first →")

    if st.button("🏆 Join Leaderboard", use_container_width=True):
        if not name_input:
            st.warning("Please enter your name.")
        elif not st.session_state.my_score:
            st.warning("Calculate your score in 'My Score' tab first.")
        else:
            level_info = get_level(st.session_state.my_score)
            new_entry  = {
                "name":  name_input,
                "score": st.session_state.my_score,
                "level": f"{level_info['icon']} {level_info['name']}",
            }
            # Update if already exists, otherwise add
            existing = [e for e in st.session_state.leaderboard if e["name"] == name_input]
            if existing:
                st.session_state.leaderboard = [
                    new_entry if e["name"] == name_input else e
                    for e in st.session_state.leaderboard
                ]
            else:
                st.session_state.leaderboard.append(new_entry)

            st.session_state.my_name = name_input
            st.success("You're on the leaderboard! 🎉")
            st.rerun()

    st.divider()

    # Rankings
    st.markdown("#### 📊 Current Rankings")
    sorted_lb   = sorted(st.session_state.leaderboard, key=lambda x: -x["score"])
    rank_icons  = ["🥇", "🥈", "🥉"]

    for i, entry in enumerate(sorted_lb):
        rank  = rank_icons[i] if i < 3 else f"**#{i+1}**"
        is_me = entry["name"] == st.session_state.my_name
        bg    = "#fffde7" if is_me else "#fafafa"
        bord  = "2px solid #ffd700" if is_me else "1px solid #eee"

        st.markdown(
            f"""<div style="
                    background:{bg}; border:{bord}; border-radius:8px;
                    padding:12px 16px; margin-bottom:8px;
                    display:flex; justify-content:space-between; align-items:center;
                ">
                <span style="font-size:20px; width:32px;">{rank}</span>
                <span style="flex:1; margin-left:12px; font-weight:{'bold' if is_me else 'normal'};">
                    {entry['name']}{'  ⭐ You' if is_me else ''}
                </span>
                <span style="color:#666; margin-right:16px; font-size:13px;">{entry['level']}</span>
                <span style="font-weight:bold; font-size:18px;">{entry['score']:.1f}</span>
            </div>""",
            unsafe_allow_html=True,
        )

    st.divider()

    # Challenge a friend
    st.markdown("#### 📤 Challenge a Friend")
    if st.session_state.my_score:
        challenge_text = (
            f"I just scored {st.session_state.my_score:.1f}/100 on Finverse — "
            f"the Financial Safety app! 💰 Can you beat my score?\n"
            f"Check it out → [paste your Streamlit URL here]"
        )
    else:
        challenge_text = "Calculate your score in 'My Score' tab, then challenge your friends!"

    st.code(challenge_text, language=None)
    st.caption("Copy this and send it on WhatsApp, Instagram, or anywhere. 🚀")


# ════════════════════════════════════════════
# TAB 5 — MONEY RULES
# ════════════════════════════════════════════
with tab5:
    st.markdown("### 📚 Smart Money Rules")
    st.caption("Enter your numbers once to get personalized targets from the best personal finance rules.")

    r_inc  = st.number_input("Monthly Income (₹)",   min_value=0.0, value=50000.0, step=1000.0, key="r_i")
    r_exp  = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=35000.0, step=1000.0, key="r_e")
    r_sav  = st.number_input("Current Savings (₹)",  min_value=0.0, value=120000.0, step=5000.0, key="r_s")
    r_age  = st.slider("Your Age", 18, 60, 25)

    if st.button("📐 Show My Numbers", use_container_width=True):
        rules = calculate_savings_rules(r_inc, r_exp, r_sav, r_age)

        # ── RULE 1: 50/30/20 ────────────────
        st.divider()
        st.markdown("### 💡 Rule 1 — The 50/30/20 Rule")
        st.caption(
            "Split your income: 50% on Needs, 30% on Wants, 20% on Savings. "
            "Simple. Proven. Powerful."
        )
        r1a, r1b, r1c = st.columns(3)
        r1a.metric("50% → Needs",   format_currency(rules["rule_50_needs"]),   "rent, food, bills")
        r1b.metric("30% → Wants",   format_currency(rules["rule_30_wants"]),   "fun, dining, shopping")
        r1c.metric("20% → Savings", format_currency(rules["rule_20_savings"]), "investments & future")

        actual_saving = r_inc - r_exp
        gap           = rules["rule_20_savings"] - actual_saving
        if actual_saving >= rules["rule_20_savings"]:
            st.success(
                f"✅ You save {format_currency(actual_saving)}/month — "
                f"above the 20% target! ({format_percent(actual_saving/r_inc*100 if r_inc > 0 else 0)})"
            )
        else:
            st.warning(
                f"⚠️ You're {format_currency(gap)} short of the 20% savings target. "
                f"Try cutting {format_currency(gap)} from Wants."
            )

        # ── RULE 2: Emergency Fund ───────────
        st.divider()
        st.markdown("### 🛟 Rule 2 — Emergency Fund Rule")
        st.caption(
            "Always keep 3–6 months of expenses in a liquid, easily accessible account. "
            "This is your financial safety net."
        )
        ef1, ef2, ef3 = st.columns(3)
        ef1.metric("3-Month Fund",      format_currency(rules["emergency_3m"]))
        ef2.metric("6-Month Fund",      format_currency(rules["emergency_6m"]))
        ef3.metric("You Have",          format_months(rules["current_coverage"]))

        if rules["current_coverage"] >= 6:
            st.success("✅ You've hit the 6-month emergency fund target. Well done!")
        elif rules["current_coverage"] >= 3:
            months_left = rules.get("months_to_6m_fund")
            if months_left is not None and months_left > 0:
                st.info(
                    f"You have {format_months(rules['current_coverage'])} coverage. "
                    f"At your current savings rate, you'll reach 6 months in "
                    f"**{months_left:.0f} more months**."
                )
        else:
            months_left = rules.get("months_to_6m_fund")
            if months_left:
                st.warning(
                    f"You have {format_months(rules['current_coverage'])} coverage. "
                    f"Estimated time to 6-month fund: **{months_left:.0f} months**."
                )
            else:
                st.error(
                    "You need to create a monthly surplus before you can build an emergency fund. "
                    "Reducing expenses is priority #1."
                )

        # ── RULE 3: FIRE Number ──────────────
        st.divider()
        st.markdown("### 🔥 Rule 3 — Your FIRE Number")
        st.caption(
            "Financial Independence = 25× your annual expenses. "
            "At a 4% withdrawal rate, this corpus lasts forever."
        )
        fi1, fi2 = st.columns(2)
        fi1.metric("Your FIRE Number",  format_currency(rules["fire_number"]))
        fi2.metric("Progress",          f"{rules['fire_progress']:.1f}%")
        st.progress(min(100, int(rules["fire_progress"])))

        if rules["fire_progress"] >= 100:
            st.success("🎉 You've hit your FIRE number! Financial independence is yours.")
        else:
            remaining = rules["fire_number"] - r_sav
            st.info(
                f"You need {format_currency(remaining)} more to reach FIRE. "
                f"At {format_currency(max(0, r_inc - r_exp))}/month surplus, "
                f"that's ~{round(remaining / max(1, r_inc - r_exp) / 12, 0):.0f} years "
                f"(before investment growth)."
            )

        # ── RULE 4: 100-Age Rule ─────────────
        st.divider()
        st.markdown("### 📈 Rule 4 — The 100-Age Investment Rule")
        st.caption(
            f"At age {r_age}: put {rules['equity_pct']}% in equity (stocks, mutual funds) "
            f"and {rules['debt_pct']}% in safer debt instruments (FD, bonds, PPF). "
            "Rebalance every year."
        )
        ia1, ia2 = st.columns(2)
        ia1.metric(
            f"Equity ({rules['equity_pct']}%)",
            format_currency(rules["equity_amount"]),
            "stocks, mutual funds",
        )
        ia2.metric(
            f"Debt ({rules['debt_pct']}%)",
            format_currency(rules["debt_amount"]),
            "FD, bonds, PPF",
        )

        # ── MONTHLY PICTURE ──────────────────
        st.divider()
        st.markdown("### 💼 Your Monthly Picture")
        mp1, mp2 = st.columns(2)
        mp1.metric("Monthly Surplus", format_currency(rules["monthly_surplus"]))
        mp2.metric("Annual Surplus",  format_currency(rules["annual_surplus"]))

        surplus = rules["monthly_surplus"]
        if surplus > 0:
            st.success(
                f"You have {format_currency(surplus)}/month to invest. "
                f"Even putting half in a simple index fund builds serious wealth over time."
            )
        else:
            st.error(
                "Your expenses exceed your income. Reducing costs is your single highest-priority action. "
                "Find {format_currency(abs(surplus))}/month in cuts."
            )


# ── FOOTER ───────────────────────────────────
st.divider()
st.caption("Finverse v2.0 · Your data stays in your session · Not financial advice")
