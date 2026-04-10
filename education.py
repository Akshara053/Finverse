# education.py  —  Finverse v9.0
# All module dicts use consistent keys.
# Every module has: id, level, title, duration, xp,
#   summary, story, content, key_takeaway,
#   book_title, book_author, buy_link, free_link

LEARNING_MODULES = [

    # ══════════════════════════════════════════
    # BEGINNER
    # ══════════════════════════════════════════

    {
        "id": "b1", "level": "Beginner",
        "title": "What is a Budget?",
        "duration": "5 min", "xp": 20,
        "summary": "A budget is a plan for your money. Every rupee gets a job.",
        "story": """
Meera was 26, earning ₹45,000 a month. She had no savings.
Every month she wondered: "Where did the money go?"
Then she tried one thing — she wrote down her income and every expense for 30 days.
The answer shocked her. ₹6,000 on food delivery. ₹3,200 on subscriptions she forgot about.
She hadn't changed her income. She hadn't changed her lifestyle dramatically.
She just started *knowing* where her money went.
Six months later, she had ₹40,000 saved.
The only thing that changed was awareness.
""",
        "content": """
**A budget is the answer to one question: where is your money going?**

Most people don't have a budget. They spend first and wonder later.

The formula is this simple:
**Income − Expenses = Savings**

Positive? You are building a future.
Zero? You are surviving.
Negative? You are borrowing from your future self.

**Why people avoid budgets (and why they're wrong):**
They think a budget means restriction. It actually means freedom.
When you know where every rupee goes, you stop wondering where it went.
You make *conscious* choices instead of automatic ones.

**The Two-Account System:**
1. One account for expenses (bills, rent, food)
2. One account for savings (future you)

On salary day: move savings amount first. Spend from what remains.
This single habit is the foundation of every financially stable person's life.

**How to start in 10 minutes:**
Step 1: Write your take-home income at the top.
Step 2: List every monthly expense (estimate if needed).
Step 3: Subtract. That number is your reality.
Step 4: If negative — find one expense to cut.
Step 5: If positive — automate moving that amount to savings tomorrow.
""",
        "key_takeaway": "A budget is not a cage. It is a map. Start by tracking every rupee for 30 days — just tracking, nothing else.",
        "book_title": "The Total Money Makeover",
        "book_author": "Dave Ramsey",
        "buy_link": "https://www.amazon.in/s?k=total+money+makeover+dave+ramsey",
        "free_link": "https://openlibrary.org/search?q=total+money+makeover",
    },

    {
        "id": "b2", "level": "Beginner",
        "title": "The 50/30/20 Rule",
        "duration": "5 min", "xp": 20,
        "summary": "The simplest budgeting rule that works for most people.",
        "story": """
Arjun had just got his first job. ₹50,000 take-home.
His friends told him to "live a little." His parents said "save everything."
He was stuck.
Then he found a rule: 50/30/20.
Half for needs. A third for wants. A fifth for savings.
At ₹50,000 that meant: ₹25,000 for rent and food.
₹15,000 for fun, dating, and eating out.
₹10,000 straight to savings the moment his salary arrived.
No guilt. No deprivation. No confusion.
By 30, Arjun had ₹12 lakh saved without ever feeling broke.
""",
        "content": """
**The Rule:**
- **50%** → Needs (rent, food, transport, EMIs, electricity)
- **30%** → Wants (dining out, subscriptions, shopping, entertainment)
- **20%** → Savings (emergency fund, investments, goals)

**At ₹50,000/month:**
- ₹25,000 on needs
- ₹15,000 on wants
- ₹10,000 saved and invested

**The critical insight:**
Most people save what is left after spending — which is usually nothing.
The rule says: **save first, then spend what remains**.

**Adapting the rule:**
Expensive city? Your needs might be 60%. That is fine — reduce wants to 10% and protect the 20% savings.
Just starting out? Even 5% saved consistently beats 0%.

**The one number to protect:**
If you could only protect one percentage — protect the 20%.
Cut wants before you cut savings. Always.
""",
        "key_takeaway": "50% needs, 30% wants, 20% savings. Automate the savings transfer on the day your salary arrives.",
        "book_title": "All Your Worth",
        "book_author": "Elizabeth Warren",
        "buy_link": "https://www.amazon.in/s?k=all+your+worth+elizabeth+warren",
        "free_link": "https://openlibrary.org/search?q=all+your+worth+warren",
    },

    {
        "id": "b3", "level": "Beginner",
        "title": "Emergency Fund — Your Safety Net",
        "duration": "6 min", "xp": 25,
        "summary": "3–6 months of expenses liquid. The most important account you will ever build.",
        "story": """
Priya, a software developer, had ₹2 lakh saved. 
Then her company laid off 200 people. She was one of them.
Her colleagues who had no emergency fund panicked within 3 weeks.
Priya? She was calm. She had 6 months of expenses saved — separately.
She used 3 months to find a job she actually loved — not just the first one that called back.
She got an offer with 30% higher salary because she could afford to wait.
Her emergency fund didn't just save her financially. It gave her power.
""",
        "content": """
**What it is:**
Money set aside ONLY for genuine emergencies.
Job loss. Medical crisis. Essential repairs.
NOT for vacations. NOT for a new phone. NOT for "I really want this."

**The targets:**
- 3 months = bare minimum (fragile)
- 6 months = standard (comfortable)
- 9–12 months = freelancers and business owners (necessary)

**Where to keep it:**
A high-interest savings account — liquid, accessible, no market risk.
NOT stocks. NOT mutual funds. NOT crypto.
It must be reachable in 24 hours with no penalty.

**How to build it:**
1. Open a dedicated account. Name it "Emergency Fund."
2. Auto-transfer even ₹2,000 on salary day.
3. NEVER touch it for non-emergencies.
4. After using it, rebuild before resuming investments.

**Why this changes everything:**
Without an emergency fund, every unexpected event is a financial crisis.
With 6 months saved, losing your job is stressful but manageable.
You can wait for the right job. Negotiate from strength. Sleep at night.
This single account is the difference between financial anxiety and financial calm.
""",
        "key_takeaway": "Build 6 months of expenses in a separate dedicated account. This is the most important financial task you have right now.",
        "book_title": "The Psychology of Money",
        "book_author": "Morgan Housel",
        "buy_link": "https://www.amazon.in/s?k=psychology+of+money+morgan+housel",
        "free_link": "https://openlibrary.org/search?q=psychology+of+money+housel",
    },

    {
        "id": "b4", "level": "Beginner",
        "title": "Good Debt vs Bad Debt",
        "duration": "6 min", "xp": 25,
        "summary": "Not all debt is evil. But bad debt is silently destroying millions of people.",
        "story": """
Rahul and Kavya both earned the same salary.
Rahul had a home loan at 8.5%. Kavya had credit card debt at 42%.
Every month, Rahul's loan was slowly building equity in an appreciating asset.
Every month, Kavya's balance grew — even when she paid ₹5,000, her debt barely moved.
After 3 years, Rahul had ₹9 lakh of equity in his home.
Kavya had paid ₹1.8 lakh in interest alone — and still owed more than she originally borrowed.
Same income. Different relationship with debt. Completely different lives.
""",
        "content": """
**Good debt creates value:**
- Home loan: you own an appreciating asset
- Education loan: increases your earning capacity
- Business loan: generates returns above the interest cost

**Bad debt consumes value:**
- Credit card debt: **36–42% annual interest** — the most toxic financial product in existence
- Personal loan for a gadget: paying 18% for something worth 40% less the moment you buy it
- Buy-now-pay-later: normalises spending you cannot afford

**The credit card rule:**
Use it like a debit card. Pay the FULL balance every single month.
If you cannot pay the full balance — do not use the card.
The rewards and cashback are worth nothing compared to 3.5% monthly compound interest.

**Paying off debt — the Avalanche method:**
1. List all debts by interest rate (highest first)
2. Pay the minimum on all debts
3. Put every extra rupee toward the highest-rate debt
4. When it's gone, attack the next one

**The rule:**
If debt interest rate > expected investment return → pay the debt first.
A 36% credit card payoff is better than any investment on earth.
""",
        "key_takeaway": "Eliminate all high-interest debt before investing. A 36% debt repayment beats every mutual fund that has ever existed.",
        "book_title": "I Will Teach You To Be Rich",
        "book_author": "Ramit Sethi",
        "buy_link": "https://www.amazon.in/s?k=i+will+teach+you+to+be+rich+ramit+sethi",
        "free_link": "https://openlibrary.org/search?q=ramit+sethi+rich",
    },

    {
        "id": "b5", "level": "Beginner",
        "title": "Understanding Your Salary Slip",
        "duration": "5 min", "xp": 20,
        "summary": "What CTC, take-home, PF, and gratuity actually mean — explained plainly.",
        "story": """
Ananya got a job offer: "CTC ₹8 LPA." She was thrilled.
Her first salary: ₹52,000.
She expected ₹66,000.
Nobody had explained: CTC is not your salary.
CTC includes your PF contribution (employer + employee), gratuity, insurance.
Understanding her slip saved her from one rude shock every month —
and helped her plan her actual finances instead of imagined ones.
""",
        "content": """
**CTC vs Take-Home:**
CTC (Cost to Company) includes everything the company spends on you.
Take-home (in-hand) is what arrives in your bank account.

**Typical deductions from CTC:**
- Employee PF: 12% of basic salary (YOUR money, your retirement)
- Professional Tax: ₹200/month (state tax)
- TDS: Tax deducted at source (advance income tax)
- Sometimes: health insurance premium

**Components of a salary slip:**
- Basic salary: Usually 40–50% of CTC. PF, gratuity calculated on this.
- HRA: House Rent Allowance. Tax-exempt if you pay rent.
- Special Allowance: The flexible, fully taxable part.
- Employer PF: Company's contribution to your PF — part of CTC but not in-hand.

**PF (Provident Fund) — why you should care:**
12% of basic deducted from you + 12% added by employer.
Earns ~8.15% tax-free interest. Best risk-free return available in India.
Don't withdraw it when you change jobs — let it compound.

**Your effective take-home calculation:**
CTC − (Employee PF + Professional Tax + TDS) = Take-home

**Tax saving tips:**
Submit rent receipts for HRA exemption.
Submit investment proofs (PPF, ELSS, insurance) by January to reduce TDS.
""",
        "key_takeaway": "CTC is not your salary. Know every line of your payslip. Never withdraw PF when changing jobs — let it compound.",
        "book_title": "Let's Talk Money",
        "book_author": "Monika Halan",
        "buy_link": "https://www.amazon.in/s?k=lets+talk+money+monika+halan",
        "free_link": "https://openlibrary.org/search?q=lets+talk+money+monika+halan",
    },

    # ══════════════════════════════════════════
    # INTERMEDIATE
    # ══════════════════════════════════════════

    {
        "id": "i1", "level": "Intermediate",
        "title": "Compound Interest — The 8th Wonder",
        "duration": "7 min", "xp": 30,
        "summary": "Time is the ingredient money cannot buy. Starting later costs more than investing more.",
        "story": """
Two friends graduated together. Riya invested ₹5,000/month from age 22.
She stopped at 32 — only 10 years of investing.
Her friend Dev started at 32 and invested ₹5,000/month until 60. That's 28 years.
At 60, assuming 12% returns:
Riya: ₹3.8 crore.
Dev: ₹2.6 crore.
Riya invested for fewer years, less total money — and ended up richer.
The only difference: she started 10 years earlier.
Time is not just a factor. It is the factor.
""",
        "content": """
**Simple interest vs Compound interest:**
Simple: earn interest only on your principal.
Compound: earn interest on principal AND all previous interest earned.

At ₹1 lakh, 12% returns:
After 10 years simple: ₹2.2 lakh
After 10 years compound: ₹3.1 lakh
After 20 years compound: ₹9.6 lakh
After 30 years compound: ₹29.9 lakh

**The Rule of 72:**
Divide 72 by your return rate = years to double your money.
At 6% (FD): 72 ÷ 6 = 12 years to double
At 12% (equity): 72 ÷ 12 = 6 years to double

**The brutal truth about starting late:**
Starting 5 years earlier is worth more than doubling your monthly investment.
There is no financial decision that beats starting earlier.

**Practical implication:**
Start with ₹500/month if that's all you have.
Increase it with every raise.
Never stop.
The amount matters less than the start date.
""",
        "key_takeaway": "Start investing today. Even ₹500. Time in market matters more than amount. Starting 5 years earlier beats doubling your investment amount.",
        "book_title": "The Little Book of Common Sense Investing",
        "book_author": "John C. Bogle",
        "buy_link": "https://www.amazon.in/s?k=little+book+common+sense+investing+bogle",
        "free_link": "https://openlibrary.org/search?q=bogle+common+sense+investing",
    },

    {
        "id": "i2", "level": "Intermediate",
        "title": "Mutual Funds and SIPs",
        "duration": "8 min", "xp": 30,
        "summary": "The simplest, smartest path to long-term wealth for most Indians.",
        "story": """
Vikram was intimidated by the stock market.
His neighbour lost money in individual stocks. He didn't want that.
Then someone explained mutual funds to him:
"Imagine you and 10,000 other people pool your money.
You hire a professional to invest it. The risk is spread. The returns are shared."
Vikram started a ₹2,000/month SIP in a Nifty 50 index fund.
He didn't need to pick stocks. He didn't need to watch markets.
He just invested every month and forgot about it.
7 years later, ₹1.68 lakh invested had grown to ₹3.2 lakh — with zero stress.
""",
        "content": """
**What is a mutual fund:**
A pool of money from thousands of investors, managed together.
The fund manager invests in stocks, bonds, or a mix.

**Types you need:**
- Equity funds: invest in stocks. Higher long-term returns (10–14% historically over 10+ years). Higher short-term volatility.
- Debt funds: invest in bonds. Stable 6–8% returns. Low risk.
- Index funds: track Nifty 50 or Nifty Next 50. No active manager. Lowest fees. Consistently outperforms 80% of active funds over 10 years.

**SIP — Systematic Investment Plan:**
Fixed amount invested every month automatically.
- Removes emotion (no timing the market)
- Buys more units when prices fall (rupee cost averaging)
- Builds an unstoppable habit

**The case for Nifty 50 index funds:**
Over any 10-year period in India, Nifty 50 index funds beat 80%+ of actively managed funds.
They charge 0.1–0.2% vs 1.5–2% for active funds.
Lower cost + consistent performance = better outcome over decades.

**Where to start:**
Zerodha Coin, Groww, or Kuvera (direct plans — zero commission).
Search for "Nifty 50 index fund." Start a monthly SIP of whatever you can.
Increase it with every salary hike.
""",
        "key_takeaway": "Start a Nifty 50 index fund SIP today. Automate it. Increase it with every raise. Never panic-sell in a crash.",
        "book_title": "Let's Talk Money",
        "book_author": "Monika Halan",
        "buy_link": "https://www.amazon.in/s?k=lets+talk+money+monika+halan",
        "free_link": "https://openlibrary.org/search?q=lets+talk+money+india",
    },

    {
        "id": "i3", "level": "Intermediate",
        "title": "Insurance — The Foundation Everyone Skips",
        "duration": "7 min", "xp": 30,
        "summary": "Insurance is not investment. It is protection. Get the right kind before anything else.",
        "story": """
Suresh, 34, had ₹5 lakh in investments. He felt secure.
Then a drunk driver hit his car. He survived but needed surgery.
Hospital bill: ₹4.2 lakh.
He hadn't taken health insurance because "I'm young and healthy."
In one afternoon, years of savings were gone.
His colleague Rajan had the same accident. His health insurance covered ₹3.8 lakh.
Rajan's portfolio was untouched. Suresh had to start over.
The difference was ₹12,000 a year in premiums.
""",
        "content": """
**The two essential insurance products:**

**1. Term Life Insurance (if anyone depends on your income)**
Pure protection. If you die, your family gets a large lump sum.
- Rule: Cover = 10–15× your annual income
- Buy as young as possible. At 25, ₹1 crore cover costs ~₹8,000/year.
- AVOID: ULIPs, endowment, money-back plans. They are bad insurance AND bad investments.
- Separating insurance from investment always beats combining them.

**2. Health Insurance**
One hospitalisation can wipe out years of savings.
- Rule: ₹5 lakh minimum cover. ₹10–25 lakh if affordable.
- Add a super top-up plan for large coverage at low cost.
- Don't rely only on employer cover — it ends when you resign.
- Buy individually even if your employer provides cover.

**Critical Illness Insurance:**
Pays a lump sum on diagnosis of cancer, heart attack, stroke.
Covers income loss during treatment, not just hospital bills.

**What to avoid:**
- Any plan that combines insurance + investment (ULIPs)
- Endowment / money-back plans
- Buying insurance under pressure from a bank relationship manager

**The golden rule:**
Buy term insurance for life protection.
Buy mutual funds for investment.
NEVER mix the two.
""",
        "key_takeaway": "Get term life insurance and health insurance BEFORE any investment. These two protect everything else you build.",
        "book_title": "Let's Talk Money",
        "book_author": "Monika Halan",
        "buy_link": "https://www.amazon.in/s?k=lets+talk+money+monika+halan",
        "free_link": "https://openlibrary.org/search?q=monika+halan+insurance",
    },

    {
        "id": "i4", "level": "Intermediate",
        "title": "Understanding Taxes in India",
        "duration": "8 min", "xp": 30,
        "summary": "Basic tax knowledge saves real money. Most people overpay because they don't know the rules.",
        "story": """
Nisha got her first ₹10 LPA job. Her TDS was ₹18,000/month.
Her colleague doing the same job submitted investment proofs and paid ₹4,000/month.
Same salary. Different tax knowledge.
Nisha was paying ₹14,000 extra per month — ₹1.68 lakh per year — unnecessarily.
One afternoon learning about 80C, 80D, and HRA saved her more than a salary hike.
""",
        "content": """
**Income Tax Basics:**
India uses a slab system — higher income is taxed at higher rates.
You choose between Old Regime (more deductions) and New Regime (lower rates, fewer deductions).

**Old Regime — Key Deductions:**
- **Section 80C** (₹1.5 lakh limit): PPF, EPF, ELSS mutual funds, life insurance premium, home loan principal, NSC, 5-year FD
- **Section 80D**: Health insurance premium (₹25,000 for self, ₹50,000 for parents senior)
- **HRA exemption**: If you pay rent, significant portion of HRA is tax-free
- **Home loan interest**: Up to ₹2 lakh deduction under Section 24

**New Regime (Default from FY2024-25):**
Lower tax slabs but most deductions are removed.
Standard deduction ₹75,000 still available.
Better for: people with fewer investments and deductions.

**Which regime to choose:**
If your total deductions > ₹3.75 lakh → Old regime usually better.
If your total deductions < ₹3.75 lakh → New regime likely better.
Calculate both every year.

**Simple tax-saving moves:**
1. Invest ₹1.5 lakh in PPF or ELSS every year (80C)
2. Buy ₹25,000 health insurance (80D)
3. Claim HRA if paying rent
4. Submit proofs to employer by January

**File your ITR every year** — even if no tax due.
It builds your financial record and is needed for loans.
""",
        "key_takeaway": "Section 80C (₹1.5L), Section 80D (health insurance), and HRA can save you ₹50,000–₹1.5 lakh in taxes every year. Calculate both regimes annually.",
        "book_title": "Let's Talk Money",
        "book_author": "Monika Halan",
        "buy_link": "https://www.amazon.in/s?k=lets+talk+money+india+tax",
        "free_link": "https://www.incometax.gov.in/iec/foportal",
    },

    {
        "id": "i5", "level": "Intermediate",
        "title": "Real Estate vs Mutual Funds",
        "duration": "8 min", "xp": 30,
        "summary": "The great Indian debate. What actually builds more wealth?",
        "story": """
Two brothers, same income in 2010.
Rohan bought a flat for ₹40 lakh (₹8 lakh down payment + ₹32 lakh loan at 9%).
Kiran invested ₹32,000/month in a Nifty 50 index fund instead.
In 2024:
Rohan's flat: worth ₹80 lakh. He paid ₹74 lakh in total (principal + interest). Net gain: ₹6 lakh.
Kiran's mutual fund: ₹1.8 crore. Total invested: ₹54 lakh. Gain: ₹1.26 crore.
Plus Kiran had full liquidity and zero maintenance headaches.
This is not to say don't buy a home. It's to say: understand the math before deciding.
""",
        "content": """
**Real Estate — The full picture:**

Pros:
- Tangible asset. Leverage (loans let you buy more than you can afford in cash).
- Rental income. Emotional value of ownership.
- Hedge against some inflation.

Cons:
- Highly illiquid (can take 3–6 months to sell)
- High transaction costs (registration, stamp duty, brokerage = 5–8%)
- Maintenance costs, property tax, repairs
- EMI locks your cash flow for 20+ years
- Real price appreciation in India: ~5–7% annually (less than people think)

**Mutual Funds (equity index) — The full picture:**

Pros:
- Fully liquid (sell in 1–2 working days)
- Low cost, professionally managed (index funds)
- Historical returns: 12–14% annually over 10+ years
- No maintenance, no tenants, no registration costs
- Easily diversified across sectors and geographies

Cons:
- No leverage available
- Short-term volatility (but irrelevant if you invest for 10+ years)
- Requires discipline to not sell in market crashes

**The honest answer:**
For wealth creation: mutual funds typically outperform real estate over 15+ years.
For living in: buying makes emotional and sometimes financial sense.
For investment only: run the full calculation including all costs, EMI, opportunity cost.

**REITs — the middle ground:**
Real Estate Investment Trusts let you invest in commercial real estate like a mutual fund.
Liquid, dividend-paying, lower ticket size. Worth exploring.
""",
        "key_takeaway": "Real estate is not automatically a good investment. Calculate total cost including EMI interest and opportunity cost. Mutual funds beat real estate for wealth creation in most honest calculations.",
        "book_title": "Retire Rich Invest ₹40 a Day",
        "book_author": "P.V. Subramanyam",
        "buy_link": "https://www.amazon.in/s?k=retire+rich+invest+40+day+subramanyam",
        "free_link": "https://openlibrary.org/search?q=real+estate+vs+stocks+india",
    },

    # ══════════════════════════════════════════
    # ADVANCED
    # ══════════════════════════════════════════

    {
        "id": "a1", "level": "Advanced",
        "title": "The FIRE Number — Financial Independence",
        "duration": "10 min", "xp": 40,
        "summary": "How much do you need to never work for money again? There is a precise formula.",
        "story": """
Deepa was 32. She looked at her calendar — 28 more years until retirement.
"28 more years of alarm clocks?" she thought.
Then she discovered FIRE.
She calculated her FIRE number: ₹1.8 crore.
She had ₹45 lakh. She was saving ₹40,000/month.
At 12% returns, she'd reach her number in 11 years. Age 43.
Not 60. 43.
The math didn't require her to earn more. Just to know the target.
She didn't retire at 43 — she liked her work. But knowing she *could* leave
changed everything. She stopped tolerating bad managers. Started negotiating.
Financial independence isn't about stopping work. It's about choosing.
""",
        "content": """
**FIRE = Financial Independence, Retire Early**
The goal: accumulate enough that investment returns cover all living expenses — permanently.

**The FIRE Number:**
25 × your annual expenses

From the Trinity Study: at a 4% annual withdrawal rate, a diversified portfolio has lasted 30+ years historically without running out.

Example:
- Monthly expenses: ₹50,000 → Annual: ₹6,00,000
- FIRE Number: ₹6,00,000 × 25 = ₹1,50,00,000 (1.5 crore)

**FIRE Variants:**
- **Lean FIRE**: Minimal lifestyle. Extreme savings rate (50–70%). Very early retirement.
- **Fat FIRE**: Full lifestyle maintained. Larger corpus needed.
- **Coast FIRE**: Stop saving now — existing investments compound to FIRE number by retirement age.
- **Barista FIRE**: Part-time income covers basic expenses. Investments cover the rest.

**The savings rate is everything:**
| Savings Rate | Approx. Years to FIRE |
|---|---|
| 10% | 40+ years |
| 25% | ~32 years |
| 50% | ~17 years |
| 75% | ~7 years |

**The insight:**
Income only matters relative to expenses. A ₹10L/month earner who spends ₹9.8L is worse off
than a ₹60,000/month earner who spends ₹25,000.
Savings rate — not income — determines financial freedom.
""",
        "key_takeaway": "FIRE Number = 25× annual expenses. Savings rate determines your timeline. Every 5% increase in savings rate shaves years off your working life.",
        "book_title": "Your Money or Your Life",
        "book_author": "Vicki Robin",
        "buy_link": "https://www.amazon.in/s?k=your+money+or+your+life+vicki+robin",
        "free_link": "https://openlibrary.org/search?q=your+money+or+your+life+robin",
    },

    {
        "id": "a2", "level": "Advanced",
        "title": "Asset Allocation and Portfolio Design",
        "duration": "10 min", "xp": 40,
        "summary": "How you divide money across assets is the biggest driver of long-term returns.",
        "story": """
During the 2020 COVID crash, the Nifty fell 38% in weeks.
Investor A (100% equity) panicked, sold everything, locked in losses.
Investor B (70% equity, 20% debt, 10% gold) saw his portfolio fall only 18%.
He stayed calm, rebalanced — bought more equity at the bottom.
By year end, Investor A had recovered to 0% gain. Investor B was up 24%.
Same market. Investor B's advantage wasn't better stock picks.
It was asset allocation that let him stay rational when others panicked.
""",
        "content": """
**The core asset classes:**
- **Equity** (stocks/mutual funds): 10–14% long-term return. High short-term volatility. Long-term wealth engine.
- **Debt** (PPF/FDs/bonds): 6–8% return. Stable. Reduces portfolio volatility.
- **Gold**: 8–10% long-term return. Inflation hedge. Crisis protection. Max 10%.
- **Real estate**: Long-term appreciation. Illiquid. REITs are accessible alternative.
- **Cash**: Emergency fund only. Not an investment.

**The 100-Age Rule:**
Equity % = 100 − your age
Age 25: 75% equity, 25% debt
Age 45: 55% equity, 45% debt
Adjust based on risk tolerance.

**A simple Indian portfolio:**
- 60% Nifty 50 index fund (large cap equity)
- 15% Nifty Next 50 index fund (mid-cap equity)
- 15% PPF or debt mutual fund
- 10% Sovereign Gold Bond

**Annual rebalancing:**
Review once a year. If equity has grown to 85%, sell some, buy debt.
This forces you to sell high, buy low — automatically.

**Evidence:**
A simple 3-fund portfolio with annual rebalancing has beaten the majority of actively managed portfolios over 20 years in India.
""",
        "key_takeaway": "Equity % = 100 minus your age. Keep it simple — 2-4 funds maximum. Rebalance once a year. Stay consistent for decades.",
        "book_title": "A Random Walk Down Wall Street",
        "book_author": "Burton Malkiel",
        "buy_link": "https://www.amazon.in/s?k=random+walk+wall+street+malkiel",
        "free_link": "https://openlibrary.org/search?q=random+walk+wall+street",
    },

    {
        "id": "a3", "level": "Advanced",
        "title": "Behavioural Finance — Why Smart People Make Dumb Money Choices",
        "duration": "9 min", "xp": 40,
        "summary": "Your brain is actively working against your wealth. Here is how to fight back.",
        "story": """
When markets crashed in 2008, a finance professor sold all his index funds.
He knew intellectually that markets recover. He had taught this for 20 years.
But the fear was unbearable. He sold at the bottom.
The market recovered. He missed it.
He later wrote: "I knew what to do. I just couldn't do it.
The emotional part of my brain overpowered the rational part."
Intelligence does not protect you from emotional decisions.
Systems do.
""",
        "content": """
**The key biases destroying your returns:**

**1. Loss Aversion**
We feel the pain of losses about 2× more intensely than the pleasure of equal gains.
This makes us sell good investments at a loss and hold bad ones hoping to "break even."
Fix: Set rules in advance. "I will not check my portfolio more than once a month."

**2. Recency Bias**
We assume recent trends will continue.
When markets are rising — we think they'll always rise (buy at the top).
When markets are crashing — we think they'll crash forever (sell at the bottom).
Fix: Automate your SIP so you buy regardless of market conditions.

**3. Overconfidence**
Most people rate themselves as above-average drivers. Most investors think they can beat the market.
98% of professional fund managers underperform a simple index fund over 15 years.
Fix: Index funds. Systematic investing. Remove your judgment from the equation.

**4. Anchoring**
"I can't sell this stock — I bought it at ₹500 and it's at ₹300."
The market doesn't know or care what you paid. The question is only: is this the best use of this money now?
Fix: Evaluate every holding on its merits today, not your purchase price.

**5. Present Bias**
We overvalue today's pleasure vs future benefit.
"I'll start saving next month." (For the 47th consecutive month.)
Fix: Automation. Pre-commit to saving before you touch the money.

**The ultimate fix:**
Automate everything. Decisions are the enemy of financial success.
The less you decide in the moment, the better your outcomes.
""",
        "key_takeaway": "Your emotions are the biggest risk to your wealth. Automate investments to remove real-time decisions. Never check your portfolio daily.",
        "book_title": "The Psychology of Money",
        "book_author": "Morgan Housel",
        "buy_link": "https://www.amazon.in/s?k=psychology+of+money",
        "free_link": "https://openlibrary.org/search?q=psychology+of+money+housel",
    },

    {
        "id": "a4", "level": "Advanced",
        "title": "Building Multiple Income Streams",
        "duration": "10 min", "xp": 50,
        "summary": "One income is fragile. Here is how to build financial resilience through multiple streams.",
        "story": """
When the pandemic hit, Sameer's single income — his job — disappeared overnight.
He had savings. But his neighbour Aditi had three income streams:
Her salary, rental income from a flat, and dividends from a portfolio of REITs and dividend stocks.
When Aditi's salary stopped, 65% of her income continued automatically.
She didn't just survive. She used the time to launch a consulting practice.
Now she has four income streams.
Sameer rebuilt too — but the lesson stayed: one income is fragile. Always.
""",
        "content": """
**The 7 types of income:**
1. **Active Income**: Salary or business income. Requires your time.
2. **Investment Income**: Dividends, interest, capital gains. Grows with portfolio size.
3. **Rental Income**: Real estate. Requires capital and management.
4. **Business Income**: Owning a business that runs without you.
5. **Royalty Income**: From books, music, patents, content.
6. **Freelance/Consulting**: Selling skills part-time.
7. **Platform Income**: YouTube, courses, affiliate income.

**Where to start (in order of effort required):**

**Lowest effort:**
- Dividend-paying stocks or dividend mutual funds
- High-interest savings account or liquid mutual fund for emergency fund
- PPF (tax-free, government-backed, 7.1%)

**Medium effort:**
- Rent out a room, parking space, or storage
- Sell expertise as freelance (writing, coding, design, teaching)
- Create a digital product once (course, ebook, template)

**Higher effort (but high reward):**
- Build a content channel (YouTube, podcast, newsletter)
- Start a side business in your domain of expertise

**The key principle:**
Don't add income streams just to add them.
Add the second stream only after your primary is stable.
Deepen one stream before starting another.
Passive income is never truly passive at the start.
""",
        "key_takeaway": "One income is fragile. Start with dividend investments, then freelancing in your domain. Build the second stream before you need it.",
        "book_title": "Rich Dad Poor Dad",
        "book_author": "Robert Kiyosaki",
        "buy_link": "https://www.amazon.in/s?k=rich+dad+poor+dad",
        "free_link": "https://openlibrary.org/search?q=rich+dad+poor+dad",
    },
]

BOOK_LIST = [
    {
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "level": "Beginner",
        "why": "The best starting point for anyone. Changes how you think about wealth, risk, and time permanently. 19 short stories, no jargon.",
        "buy_link": "https://www.amazon.in/s?k=psychology+of+money",
        "free_link": "https://openlibrary.org/search?q=psychology+of+money+housel",
    },
    {
        "title": "Let's Talk Money",
        "author": "Monika Halan",
        "level": "Beginner",
        "why": "The best Indian personal finance book. Covers insurance, mutual funds, and banking specific to India. Reads like a conversation.",
        "buy_link": "https://www.amazon.in/s?k=lets+talk+money+monika+halan",
        "free_link": "https://openlibrary.org/search?q=lets+talk+money+monika+halan",
    },
    {
        "title": "I Will Teach You To Be Rich",
        "author": "Ramit Sethi",
        "level": "Beginner",
        "why": "Automation-first approach. Set up your financial systems once and barely think about money again. Practical and funny.",
        "buy_link": "https://www.amazon.in/s?k=i+will+teach+you+to+be+rich",
        "free_link": "https://openlibrary.org/search?q=ramit+sethi+rich",
    },
    {
        "title": "Rich Dad Poor Dad",
        "author": "Robert Kiyosaki",
        "level": "Beginner",
        "why": "The mindset shift on assets vs liabilities that millions needed to hear. Read it once — it rewires how you see money.",
        "buy_link": "https://www.amazon.in/s?k=rich+dad+poor+dad",
        "free_link": "https://openlibrary.org/search?q=rich+dad+poor+dad",
    },
    {
        "title": "The Automatic Millionaire",
        "author": "David Bach",
        "level": "Beginner",
        "why": "One simple idea: automate everything. A couple earning average salaries retired millionaires. Proven system for regular people.",
        "buy_link": "https://www.amazon.in/s?k=automatic+millionaire+david+bach",
        "free_link": "https://openlibrary.org/search?q=automatic+millionaire+bach",
    },
    {
        "title": "The Richest Man in Babylon",
        "author": "George S. Clason",
        "level": "Beginner",
        "why": "Ancient money wisdom told through parables. Pay yourself first. The simplest timeless rules of wealth building.",
        "buy_link": "https://www.amazon.in/s?k=richest+man+in+babylon",
        "free_link": "https://openlibrary.org/search?q=richest+man+babylon+clason",
    },
    {
        "title": "The Little Book of Common Sense Investing",
        "author": "John C. Bogle",
        "level": "Intermediate",
        "why": "The definitive case for index fund investing. Written by the inventor of the index fund. Short. Dense. Life-changing.",
        "buy_link": "https://www.amazon.in/s?k=little+book+common+sense+investing",
        "free_link": "https://openlibrary.org/search?q=bogle+common+sense+investing",
    },
    {
        "title": "The Millionaire Next Door",
        "author": "Thomas Stanley",
        "level": "Intermediate",
        "why": "Real research on how genuinely wealthy people actually live, save, and spend. Spoiler: they drive second-hand cars.",
        "buy_link": "https://www.amazon.in/s?k=millionaire+next+door+stanley",
        "free_link": "https://openlibrary.org/search?q=millionaire+next+door",
    },
    {
        "title": "Your Money or Your Life",
        "author": "Vicki Robin",
        "level": "Intermediate",
        "why": "The original FIRE book. Reframes money as life energy. If you trade your time for money, is the exchange worth it?",
        "buy_link": "https://www.amazon.in/s?k=your+money+or+your+life+vicki+robin",
        "free_link": "https://openlibrary.org/search?q=your+money+or+your+life",
    },
    {
        "title": "Retire Rich — Invest ₹40 a Day",
        "author": "P.V. Subramanyam",
        "level": "Intermediate",
        "why": "Indian-specific, practical, math-heavy. Proves that consistent small amounts compound into life-changing wealth.",
        "buy_link": "https://www.amazon.in/s?k=retire+rich+invest+40+day",
        "free_link": "https://openlibrary.org/search?q=retire+rich+subramanyam",
    },
    {
        "title": "The Intelligent Investor",
        "author": "Benjamin Graham",
        "level": "Advanced",
        "why": "Warren Buffett's recommended reading. The bible of value investing. Dense but worth every page.",
        "buy_link": "https://www.amazon.in/s?k=intelligent+investor+benjamin+graham",
        "free_link": "https://openlibrary.org/search?q=intelligent+investor+graham",
    },
    {
        "title": "A Random Walk Down Wall Street",
        "author": "Burton Malkiel",
        "level": "Advanced",
        "why": "The strongest academic argument for passive investing. Markets are efficient. Index funds win long-term. The evidence is overwhelming.",
        "buy_link": "https://www.amazon.in/s?k=random+walk+wall+street",
        "free_link": "https://openlibrary.org/search?q=random+walk+wall+street",
    },
    {
        "title": "Early Retirement Extreme",
        "author": "Jacob Lund Fisker",
        "level": "Advanced",
        "why": "The most rigorous FIRE framework. Systems thinking applied to personal finance. Not for the faint-hearted but extraordinarily thorough.",
        "buy_link": "https://www.amazon.in/s?k=early+retirement+extreme",
        "free_link": "https://openlibrary.org/search?q=early+retirement+extreme+fisker",
    },
    {
        "title": "One Up on Wall Street",
        "author": "Peter Lynch",
        "level": "Advanced",
        "why": "Lynch managed the best mutual fund in history. His insight: regular people have an investing edge over professionals in spotting consumer trends.",
        "buy_link": "https://www.amazon.in/s?k=one+up+on+wall+street+peter+lynch",
        "free_link": "https://openlibrary.org/search?q=one+up+wall+street+lynch",
    },
]

FREE_RESOURCES = [
    {"name": "Zerodha Varsity", "url": "https://zerodha.com/varsity",
     "desc": "The best free course on stock markets and investing in India. 10+ comprehensive modules. Written by practitioners."},
    {"name": "SEBI Investor Education", "url": "https://investor.sebi.gov.in",
     "desc": "India's official investor education portal from the market regulator."},
    {"name": "NISM Free Courses", "url": "https://www.nism.ac.in/e-learning/",
     "desc": "Free certified courses on mutual funds, securities, and financial planning from NISM."},
    {"name": "RBI Financial Education", "url": "https://rbi.org.in/financialeducation",
     "desc": "Official RBI resources on banking, savings, and financial awareness."},
    {"name": "Khan Academy — Personal Finance", "url": "https://www.khanacademy.org/college-careers-more/personal-finance",
     "desc": "Free structured personal finance education from complete basics to advanced topics."},
    {"name": "Freefincal", "url": "https://freefincal.com",
     "desc": "India's most rigorous personal finance research site. M. Pattabiraman's data-driven analysis."},
    {"name": "Open Library", "url": "https://openlibrary.org",
     "desc": "Borrow digital versions of finance books for free with a free account. Legal digital lending."},
    {"name": "Income Tax Portal", "url": "https://www.incometax.gov.in",
     "desc": "Official Indian tax filing, deduction guides, and ITR utilities. File your returns free here."},
]


def get_modules_by_level():
    result = {}
    for m in LEARNING_MODULES:
        result.setdefault(m["level"], []).append(m)
    return result


def get_module_by_id(module_id):
    return next((m for m in LEARNING_MODULES if m["id"] == module_id), None)
