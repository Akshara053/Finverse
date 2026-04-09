# education.py  —  Finverse v6.0
# Structured financial education content.
# Beginner → Intermediate → Advanced learning path.

LEARNING_MODULES = [
    # ── BEGINNER ─────────────────────────────
    {
        "id":       "b1",
        "level":    "Beginner",
        "title":    "What is a Budget?",
        "duration": "5 min",
        "content":  """
A budget is simply a plan for your money.

It tells every rupee where to go — instead of wondering where it went.

**The simple formula:**
Income - Expenses = Savings

If this number is positive, you're building wealth.
If it's zero, you're surviving.
If it's negative, you're borrowing from your future.

**Why it matters:**
Most people don't fail at earning. They fail at directing.
A budget is the most powerful financial tool — and it costs nothing to make one.

**Start here:**
Write down your income. Write down your expenses. Subtract.
That number tells you everything about your current financial story.
        """,
        "key_takeaway": "A budget is a spending plan. Track income and expenses every month.",
        "book": "The Total Money Makeover — Dave Ramsey",
    },
    {
        "id":       "b2",
        "level":    "Beginner",
        "title":    "The 50/30/20 Rule",
        "duration": "5 min",
        "content":  """
The 50/30/20 rule is the simplest budgeting framework that works.

**50% — Needs** (things you must pay)
Rent, food, utilities, EMIs, transport.

**30% — Wants** (things you choose to pay)
Dining out, OTT subscriptions, shopping, travel.

**20% — Savings** (pay yourself first)
Emergency fund, investments, goal savings.

**The rule in practice:**
If your take-home is ₹50,000:
- ₹25,000 on needs
- ₹15,000 on wants
- ₹10,000 saved

**The most common mistake:**
People save what is left after spending.
The rule says: save first, then spend what remains.
        """,
        "key_takeaway": "Split income: 50% needs, 30% wants, 20% savings. Automate the savings part.",
        "book": "All Your Worth — Elizabeth Warren",
    },
    {
        "id":       "b3",
        "level":    "Beginner",
        "title":    "Emergency Fund — Your Financial Safety Net",
        "duration": "6 min",
        "content":  """
An emergency fund is money set aside for unexpected events — not vacations, not gadgets.
True emergencies: job loss, medical crisis, urgent repairs.

**The target:**
3 months of expenses = minimum
6 months of expenses = standard
12 months of expenses = freelancers and business owners

**Where to keep it:**
A separate savings account. Not in stocks. Not in crypto.
It must be liquid — accessible within 24 hours, no penalty.

**How to build it:**
Step 1: Open a dedicated savings account. Name it "Emergency Fund."
Step 2: Auto-transfer a fixed amount every salary day.
Step 3: Do not touch it for anything that is not a genuine emergency.

**Why it changes everything:**
With a 6-month emergency fund, losing your job feels manageable.
Without one, it feels catastrophic.
        """,
        "key_takeaway": "Build 6 months of expenses in a separate liquid account. Touch it only for true emergencies.",
        "book": "The Psychology of Money — Morgan Housel",
    },

    # ── INTERMEDIATE ──────────────────────────
    {
        "id":       "i1",
        "level":    "Intermediate",
        "title":    "How Compound Interest Works",
        "duration": "7 min",
        "content":  """
Compound interest is the most powerful force in personal finance.
Einstein reportedly called it the eighth wonder of the world.

**Simple interest vs Compound interest:**
Simple: You earn interest only on your principal.
Compound: You earn interest on your principal AND on previous interest.

**The Rule of 72:**
Divide 72 by your annual return rate to know how many years it takes to double money.

At 8% return: 72 / 8 = 9 years to double.
At 12% return: 72 / 12 = 6 years to double.

**The brutal truth about starting late:**
₹10,000/month invested at age 25 for 10 years (then stopped) = more wealth at 60
than ₹10,000/month invested from age 35 to 60.

Time is the variable that money cannot buy back.
Start now. Even small amounts.
        """,
        "key_takeaway": "Start investing early. Time in market matters more than timing the market.",
        "book": "The Little Book of Common Sense Investing — John Bogle",
    },
    {
        "id":       "i2",
        "level":    "Intermediate",
        "title":    "Understanding Mutual Funds and SIPs",
        "duration": "8 min",
        "content":  """
A mutual fund pools money from thousands of investors and invests it in stocks, bonds, or both.
A professional fund manager makes the decisions.

**Types you need to know:**
- Equity funds: Invest in stocks. Higher risk, higher return (10–14% historically).
- Debt funds: Invest in bonds. Lower risk, stable return (6–8%).
- Index funds: Track a market index (Nifty 50). No active management. Low cost.

**SIP — Systematic Investment Plan:**
Invest a fixed amount every month automatically.
Removes emotion from investing. Buys more units when price is low. Averages out cost.

**The case for index funds:**
Over 10+ years, 80% of actively managed funds underperform the index.
A Nifty 50 index fund with 0.1% expense ratio beats most fund managers over time.

**How to start:**
- Open an account on Zerodha Coin, Groww, or Kuvera (direct funds, zero commission).
- Start a SIP of even ₹500/month.
- Increase it every time your income increases.
        """,
        "key_takeaway": "Start a SIP in a Nifty 50 index fund. Automate it. Increase it with every raise.",
        "book": "Let's Talk Money — Monika Halan",
    },
    {
        "id":       "i3",
        "level":    "Intermediate",
        "title":    "Debt Management — Good Debt vs Bad Debt",
        "duration": "7 min",
        "content":  """
Not all debt is equal. The key question is: does this debt build or destroy wealth?

**Good debt:** Borrows to create something that appreciates or generates income.
- Home loan: You get an appreciating asset.
- Education loan: Increases your earning capacity.
- Business loan: Can generate returns above interest cost.

**Bad debt:** Borrows to consume things that depreciate.
- Credit card debt: 36–42% annual interest. The most toxic debt that exists.
- Personal loans for gadgets: Paying 18% to buy something that loses 40% value immediately.
- Buy-now-pay-later traps: Normalizes spending you cannot actually afford.

**The Debt Avalanche Method:**
List all debts by interest rate. Pay minimum on all, throw every extra rupee at the highest-rate debt first.
Mathematically optimal. Saves the most money.

**The rule:**
If the interest rate on debt > expected investment return, pay off the debt first.
        """,
        "key_takeaway": "Eliminate high-interest bad debt before investing. A 36% debt repayment beats any investment.",
        "book": "I Will Teach You To Be Rich — Ramit Sethi",
    },

    # ── ADVANCED ──────────────────────────────
    {
        "id":       "a1",
        "level":    "Advanced",
        "title":    "The FIRE Movement — Financial Independence",
        "duration": "10 min",
        "content":  """
FIRE stands for Financial Independence, Retire Early.
The goal: accumulate enough wealth that your investment returns cover all living expenses.

**The FIRE Number:**
25x your annual expenses. (Based on the 4% Safe Withdrawal Rate from the Trinity Study.)

If you spend ₹5,00,000/year:
FIRE Number = ₹1,25,00,000 (1.25 crore)

At this corpus, you can withdraw 4% per year indefinitely — historically, the portfolio never runs out.

**FIRE Variants:**
- Lean FIRE: Minimal lifestyle. Extreme savings rate (50–70%).
- Fat FIRE: Full lifestyle maintained. Requires larger corpus.
- Barista FIRE: Part-time work to cover basics, investments cover the rest.
- Coast FIRE: Stop saving now — existing investments grow to FIRE number by retirement age.

**The math of savings rate:**
At 10% savings rate: 40+ years to FIRE.
At 25% savings rate: ~32 years.
At 50% savings rate: ~17 years.
At 75% savings rate: ~7 years.

Savings rate is the only variable that dramatically changes the timeline.
        """,
        "key_takeaway": "FIRE Number = 25x annual expenses. Higher savings rate = earlier freedom.",
        "book": "Early Retirement Extreme — Jacob Lund Fisker",
    },
    {
        "id":       "a2",
        "level":    "Advanced",
        "title":    "Asset Allocation and Portfolio Building",
        "duration": "10 min",
        "content":  """
Asset allocation is how you divide your money across different asset classes.
It is the single biggest driver of long-term investment returns.

**The core asset classes:**
- Equity (stocks/mutual funds): High return, high volatility. Long-term engine.
- Debt (bonds/FDs/PPF): Stable return, low volatility. Stability anchor.
- Gold: Inflation hedge, crisis protection. 5–10% max.
- Real estate: Illiquid but appreciates long term.
- Cash: Emergency fund only. Not an investment.

**The 100-Age Rule:**
Equity % = 100 - your age
At 25: 75% equity, 25% debt.
At 45: 55% equity, 45% debt.

**Portfolio rebalancing:**
Every year, review your allocation.
If equity has grown to 85% (market run-up), sell some and buy debt to restore balance.
Rebalancing forces you to sell high and buy low automatically.

**For Indian investors:**
- Nifty 50 index fund (large cap equity)
- Nifty Next 50 index fund (mid cap)
- PPF or Debt mutual fund (debt)
- Sovereign Gold Bond (gold)
        """,
        "key_takeaway": "Equity % = 100 minus your age. Rebalance once a year. Keep it simple.",
        "book": "A Random Walk Down Wall Street — Burton Malkiel",
    },
]

BOOK_LIST = [
    {"title": "The Psychology of Money",          "author": "Morgan Housel",       "level": "Beginner",      "why": "Best starting point. Changes how you think about money permanently."},
    {"title": "Let's Talk Money",                 "author": "Monika Halan",        "level": "Beginner",      "why": "Best Indian personal finance book. Practical, no jargon."},
    {"title": "The Total Money Makeover",         "author": "Dave Ramsey",         "level": "Beginner",      "why": "Step-by-step debt elimination and wealth building system."},
    {"title": "I Will Teach You To Be Rich",      "author": "Ramit Sethi",         "level": "Beginner",      "why": "Automation-first approach. Set it up once and forget it."},
    {"title": "Rich Dad Poor Dad",                "author": "Robert Kiyosaki",     "level": "Beginner",      "why": "Mindset shift on assets vs liabilities. Read once."},
    {"title": "The Little Book of Common Sense",  "author": "John Bogle",          "level": "Intermediate",  "why": "The definitive case for index fund investing."},
    {"title": "All Your Worth",                   "author": "Elizabeth Warren",    "level": "Intermediate",  "why": "The original 50/30/20 book. Deeply practical."},
    {"title": "The Millionaire Next Door",        "author": "Thomas Stanley",      "level": "Intermediate",  "why": "Real data on how wealthy people actually live and save."},
    {"title": "A Random Walk Down Wall Street",   "author": "Burton Malkiel",      "level": "Advanced",      "why": "Markets are efficient. Index funds win long-term."},
    {"title": "Early Retirement Extreme",         "author": "Jacob Lund Fisker",   "level": "Advanced",      "why": "Most rigorous FIRE framework. Not for the faint-hearted."},
    {"title": "The Intelligent Investor",         "author": "Benjamin Graham",     "level": "Advanced",      "why": "Warren Buffett calls this the best investing book ever written."},
]


def get_modules_by_level():
    result = {}
    for m in LEARNING_MODULES:
        lvl = m["level"]
        if lvl not in result:
            result[lvl] = []
        result[lvl].append(m)
    return result


def get_module_by_id(module_id):
    for m in LEARNING_MODULES:
        if m["id"] == module_id:
            return m
    return None
