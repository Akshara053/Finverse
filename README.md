# 💰 Finverse – Financial Stability Platform v2.0

> "Do you really know if you're financially safe?"

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
finverse/
├── app.py            → All UI (5 tabs). No logic here.
├── logic.py          → All financial calculations
├── gamification.py   → Levels, badges, challenges, XP
├── config.py         → Thresholds, weights, persona configs
├── utils.py          → Formatting helpers
└── requirements.txt
```

**Rule:** Change how it *looks* → `app.py`. Change how it's *calculated* → `logic.py`. Change a *threshold or constant* → `config.py`.

---

## 🎮 Features

### Tab 1 — My Score
- Persona selector (Student, Professional, Freelancer, Business Owner)
- Weighted composite financial health score (0–100)
- Level system: Starter → Bronze → Silver → Gold → Platinum
- Badges for savings rate, survival months, and expense ratio
- Active challenges with XP rewards

### Tab 2 — Daily Tracker
- Add daily expenses by category
- Budget progress bar with alerts
- Spending breakdown by category
- Daily tracking streak counter

### Tab 3 — Partner Test
- Individual scores for both partners
- Combined financial health
- Alignment score (how similar your financial behaviors are)
- "What should my partner earn?" calculator
- Sliders for target savings rate and emergency fund

### Tab 4 — Leaderboard
- Join the leaderboard with your name and score
- Pre-populated mock users for context
- Challenge-a-friend shareable text

### Tab 5 — Money Rules
- 50/30/20 rule personalized to your income
- Emergency fund progress and time-to-target
- FIRE number and progress percentage
- 100-Age investment allocation rule

---

## 🧠 How the Score Works

| Signal | Weight | Measures |
|---|---|---|
| Savings Rate | 40% | Monthly surplus as % of income |
| Survival Months | 35% | How long savings last without income |
| Expense Ratio | 25% | Expenses as % of income |

**Levels:** Starter (0) → Bronze (25) → Silver (50) → Gold (70) → Platinum (85)

**Risk:** SAFE (≥65) · MODERATE (35–64) · RISKY (<35)

---

## 🗺️ Roadmap

- [x] Phase 1: Core financial calculator
- [x] Phase 2: Gamification, personas, partner test, tracker
- [ ] Phase 3: SQLite database + user login
- [ ] Phase 4: Charts, dashboards, trends over time
- [ ] Phase 5: Social features, real-time leaderboard, community
