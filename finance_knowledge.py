# finance_knowledge.py  —  Finverse v10.0
# Finance Q&A inspired by top Indian finance YouTube creators.
# All content is original writing — sources are attributed as inspiration.
# Topics extracted from: Nitish Rajput, Finance with Sharan, CA Rachana Phadke Ranade,
# Labour Law Advisor, Pranjal Kamra, Akshat Shrivastava, Warikoo, Asset Yogi.

FINANCE_QA = [

    # ══════════════════════════════════════════
    # MONEY BASICS
    # ══════════════════════════════════════════
    {
        "id": "q1",
        "category": "Money Basics",
        "question": "What actually is money? Why does a piece of paper have value?",
        "answer": """
Money is a shared agreement. Nothing more.

A ₹500 note is just printed paper. It has value because the Government of India promises to honour it, and because every person in the country agrees to accept it as payment. The moment that trust breaks — as happened in Zimbabwe or Venezuela — the paper becomes worthless.

**The three functions of money:**
1. **Medium of exchange** — eliminates the need for barter (imagine trying to buy a car by paying in wheat)
2. **Store of value** — you can earn today and spend tomorrow
3. **Unit of account** — a common measure to compare the price of different things

**Why does the value of money change?**
Because more money chasing the same goods = each rupee buys less (inflation).
When RBI prints more rupees, each existing rupee dilutes slightly.

**The key insight:**
Money is a tool, not a goal. Holding too much cash is actually losing money slowly — inflation erodes its purchasing power every year. Investing is not gambling — it is refusing to let inflation eat your savings quietly.
        """,
        "source": "Inspired by: Nitish Rajput — 'What is Money?' series",
        "source_url": "https://www.youtube.com/@NitishRajput",
        "tags": ["basics", "money", "inflation"],
    },
    {
        "id": "q2",
        "category": "Money Basics",
        "question": "Why is the US Dollar so powerful? What is the Petrodollar?",
        "answer": """
After World War II, the world needed a stable reserve currency. The US economy was the largest and its currency was backed by gold. In 1944, 44 nations agreed at Bretton Woods: all currencies would be pegged to the dollar, and the dollar would be redeemable for gold at $35/ounce.

**The Petrodollar — why oil runs on dollars:**
In 1971, Nixon ended dollar-gold convertibility. To maintain dollar dominance, the US struck a deal with Saudi Arabia: oil would always be priced and traded in US dollars, in exchange for US military protection. Since every country needs oil, every country needs dollars. Demand for dollars = dollar stays strong.

**Why this matters for India:**
- India imports ~85% of its oil
- We pay in dollars, which weakens the rupee over time
- When the rupee falls, imports get costlier — petrol, electronics, medicines

**Is the dollar's dominance permanent?**
Countries like Russia, China, and BRICS are slowly building alternatives. But dethroning the dollar requires the world to trust another currency equally. That trust takes decades to build.
        """,
        "source": "Inspired by: Nitish Rajput — 'Dollar Dominance' & 'Petrodollar Explained'",
        "source_url": "https://www.youtube.com/@NitishRajput",
        "tags": ["dollar", "global", "currency", "oil"],
    },
    {
        "id": "q3",
        "category": "Money Basics",
        "question": "What is inflation and why does the government allow it?",
        "answer": """
Inflation means prices rise over time — the same ₹100 buys less than it did 5 years ago.

**Why does it happen?**
- Too much money chasing too few goods
- Supply chain disruptions (like COVID shortages)
- Rising input costs (oil prices, raw materials)
- Government printing money to fund spending

**Why does the government WANT some inflation?**
Because deflation (falling prices) is actually more dangerous. If people expect prices to fall tomorrow, they stop buying today. Factories shut. Workers get laid off. Economies collapse. Japan suffered a decade of deflation in the 1990s and still hasn't fully recovered.

The ideal inflation target in India: **4% ±2%** (set by RBI's Monetary Policy Committee).

**How inflation silently destroys savings:**
₹1,00,000 in a savings account at 3.5% interest, with 6% inflation:
Your money "grows" to ₹1,03,500 — but what it can buy has shrunk by ₹2,500.
You are actually ₹2,500 poorer in real terms, even as the number grows.

**The solution:**
Invest in assets that grow faster than inflation — equity, real estate, gold, index funds.
Not in savings accounts or FDs alone.
        """,
        "source": "Inspired by: Finance with Sharan — 'Inflation Explained Simply'",
        "source_url": "https://www.youtube.com/@financewithsharan",
        "tags": ["inflation", "RBI", "savings", "basics"],
    },

    # ══════════════════════════════════════════
    # STOCK MARKET
    # ══════════════════════════════════════════
    {
        "id": "q4",
        "category": "Stock Market",
        "question": "What is the stock market? How does it work in simple terms?",
        "answer": """
Imagine you own a chai stall. Business is good and you want to open 10 more stalls — but you don't have enough money.

You could: borrow from a bank (loan), or sell a part of your business to people who believe in it (equity).

If you sell 40% of your business to 4 friends for ₹1 lakh each, they become part-owners. If your business doubles, their investment doubles. If it fails, they lose money.

**The stock market does this at scale:**
A company lists on NSE or BSE by offering shares to the public (IPO). Investors buy shares and become part-owners. As the company grows and profits, share prices rise. If the company does poorly, prices fall.

**BSE and NSE:**
- BSE (Bombay Stock Exchange): Asia's oldest, est. 1875. Sensex tracks top 30 companies.
- NSE (National Stock Exchange): est. 1992. Nifty 50 tracks top 50 companies.

**SEBI (Securities and Exchange Board of India):**
The regulator. Like RBI for banks, SEBI regulates stock markets — prevents fraud, ensures transparency, protects investors.

**Key truth:**
The stock market is not a casino. Over the long term (10+ years), the Nifty 50 has given ~12% CAGR returns, turning every ₹1 lakh into ~₹3.1 lakh. Short-term: volatile. Long-term: wealth-building machine.
        """,
        "source": "Inspired by: CA Rachana Phadke Ranade — 'Stock Market for Beginners'",
        "source_url": "https://www.youtube.com/@CARachanaRanade",
        "tags": ["stocks", "NSE", "BSE", "basics", "Nifty"],
    },
    {
        "id": "q5",
        "category": "Stock Market",
        "question": "What is the difference between Sensex and Nifty?",
        "answer": """
Both are indices — benchmarks that track the overall health of the Indian stock market.

**Sensex (BSE Sensitive Index):**
- Tracks the 30 largest and most actively traded companies on BSE
- Started in 1979 at 100 points
- Has grown to 70,000+ points today
- Includes: Reliance, TCS, HDFC Bank, Infosys, HUL, etc.

**Nifty 50 (NSE):**
- Tracks the 50 largest companies on NSE
- Broader representation than Sensex
- More commonly used by fund managers and for index funds

**What does a rise in Sensex/Nifty mean?**
On average, the combined value of those top companies has increased.
It does NOT mean every stock went up — individual stocks can fall even on a good day.

**For investors:**
When you invest in a Nifty 50 index fund, you are effectively buying a tiny slice of India's 50 largest companies at once — instant diversification.

**Historical data:**
Nifty 50 in 2000: ~1,500 points
Nifty 50 in 2024: ~22,000 points
CAGR: ~12.5% per year over 24 years.
₹1 lakh invested in 2000 would be ~₹17.5 lakh today.
        """,
        "source": "Inspired by: Pranjal Kamra — 'Nifty vs Sensex' videos",
        "source_url": "https://www.youtube.com/@PranjalKamra",
        "tags": ["Nifty", "Sensex", "index", "BSE", "NSE"],
    },
    {
        "id": "q6",
        "category": "Stock Market",
        "question": "What is an IPO and should you invest in one?",
        "answer": """
IPO = Initial Public Offering. It is the first time a private company sells its shares to the public.

**Why companies do IPOs:**
To raise capital for expansion, pay off debt, or let early investors (founders, VCs) exit.

**The IPO process:**
1. Company hires investment banks (SEBI-registered)
2. Files DRHP (Draft Red Herring Prospectus) — a detailed document about the business
3. Sets a price band (e.g., ₹400–₹420 per share)
4. Public applies for shares (3-day window)
5. Allotment: if oversubscribed, shares are allotted by lottery
6. Company lists on exchange; trading begins

**Should you invest in an IPO?**

**The honest answer:** It depends.

IPOs of profitable, established companies at reasonable valuations: can be good.
IPOs of loss-making startups at high valuations: often drop 30–50% post-listing.

**Red flags to avoid:**
- No profits for 3+ years
- Promoters selling (Offer for Sale) — they are exiting, not growing
- Very high P/E ratio vs peers
- IPO proceeds mainly repay debt

**Better alternative:**
Wait 6–12 months post-IPO. If the company is genuinely good, the share will still be available — often at a lower price after the hype fades.
        """,
        "source": "Inspired by: Akshat Shrivastava — 'IPO Investing Strategy'",
        "source_url": "https://www.youtube.com/@AkshatShrivastava",
        "tags": ["IPO", "stocks", "investing", "beginners"],
    },

    # ══════════════════════════════════════════
    # MUTUAL FUNDS
    # ══════════════════════════════════════════
    {
        "id": "q7",
        "category": "Mutual Funds",
        "question": "Direct vs Regular mutual funds — what is the difference and which is better?",
        "answer": """
This single choice can cost or save you lakhs of rupees over 20 years.

**Regular Plan:**
You invest through a broker/distributor/bank.
The broker earns a commission from the fund house (1–1.5% per year from your returns).
The fund house deducts this from the NAV (Net Asset Value) every day — silently.

**Direct Plan:**
You invest directly with the fund house (or via platforms like Kuvera, Coin, Groww — direct plans).
No distributor. No commission. Lower expense ratio by ~1%.

**Why does 1% matter?**
At ₹10,000/month SIP, 12% returns, over 20 years:
- Regular plan (1.5% expense ratio): ₹81 lakh
- Direct plan (0.5% expense ratio): ₹96 lakh

That is ₹15 lakh difference — just from choosing Direct.

**Which platforms offer Direct plans:**
- Kuvera.in (free, clean interface)
- Coin by Zerodha (₹50/month, advanced features)
- Groww (direct plans available, verify before investing)
- MFCentral / AMC websites directly

**The rule:**
Always invest in Direct plans unless you genuinely need advice, in which case pay a fee-only SEBI-registered financial advisor — do not pay through hidden commissions.
        """,
        "source": "Inspired by: Finance with Sharan — 'Direct vs Regular Mutual Funds'",
        "source_url": "https://www.youtube.com/@financewithsharan",
        "tags": ["mutual funds", "direct", "regular", "SIP", "expense ratio"],
    },
    {
        "id": "q8",
        "category": "Mutual Funds",
        "question": "What is NAV and how is it calculated?",
        "answer": """
NAV = Net Asset Value. It is the per-unit price of a mutual fund.

**Formula:**
NAV = (Total Assets − Liabilities) ÷ Number of Units Outstanding

If a fund manages ₹1,000 crore across 10 crore units, NAV = ₹100.

**Common myth: Low NAV = cheap fund, High NAV = expensive fund**

This is completely wrong. 

A fund with NAV ₹10 and a fund with NAV ₹500 are equally "cheap" if they represent the same quality of underlying assets.

What matters: the future growth of the underlying portfolio — not the current NAV number.

**NAV changes daily:**
Because the underlying stocks/bonds change in value every trading day. Your returns = (Exit NAV − Entry NAV) ÷ Entry NAV × 100.

**IDCW vs Growth option:**
Growth: NAV keeps growing. All returns are reinvested.
IDCW (formerly Dividend): Fund periodically pays out from NAV. NAV drops after each payment.
For long-term wealth building: **always choose Growth.**

**When to check NAV:**
For SIP investors: never obsess over daily NAV. Check performance annually vs benchmark.
        """,
        "source": "Inspired by: Asset Yogi — 'NAV Explained'",
        "source_url": "https://www.youtube.com/@AssetYogi",
        "tags": ["NAV", "mutual funds", "SIP", "investing"],
    },

    # ══════════════════════════════════════════
    # BANKING & RBI
    # ══════════════════════════════════════════
    {
        "id": "q9",
        "category": "Banking & RBI",
        "question": "What does RBI actually do? Why does it matter to your money?",
        "answer": """
RBI = Reserve Bank of India. It is the central bank — the bank of all banks.

**What RBI does:**

1. **Issues currency:** Only RBI can print rupees. ₹1 coins are issued by the Government.

2. **Controls money supply:** Raises or lowers interest rates to control inflation.
   - Rate hike → loans get expensive → people borrow less → economy cools → inflation falls
   - Rate cut → loans get cheaper → people borrow more → economy heats up

3. **Regulates banks:** Sets rules, monitors health, acts as lender of last resort.
   When YES Bank and PMC Bank nearly collapsed, RBI stepped in.

4. **Manages forex reserves:** India's foreign exchange reserves (~$600 billion) are managed by RBI. Used to stabilise the rupee.

5. **Repo Rate:** The rate at which RBI lends to commercial banks overnight. When this rises, all EMIs across India go up. When it falls, EMIs fall.

**How RBI decisions hit your life directly:**
- Repo rate up → your home loan EMI rises within months
- Repo rate down → FD rates fall within weeks
- RBI tightens rules → banks lend more carefully → fewer bad loans

**The key number to track:**
Repo Rate (currently watch RBI's Monetary Policy Committee meetings — 6 times a year).
        """,
        "source": "Inspired by: Nitish Rajput — 'RBI Explained' series",
        "source_url": "https://www.youtube.com/@NitishRajput",
        "tags": ["RBI", "banking", "repo rate", "inflation", "EMI"],
    },
    {
        "id": "q10",
        "category": "Banking & RBI",
        "question": "What is DICGC? Is your bank deposit safe?",
        "answer": """
DICGC = Deposit Insurance and Credit Guarantee Corporation. A fully-owned subsidiary of RBI.

**What it does:**
Insures your bank deposits up to **₹5 lakh** per depositor per bank.

If your bank goes bankrupt (like PMC Bank, Yes Bank crisis), DICGC guarantees you get back up to ₹5 lakh.

**Key points:**
- ₹5 lakh limit includes both principal AND interest
- Covers: savings, current, FD, RD accounts
- Covers: scheduled commercial banks, small finance banks, cooperative banks
- Does NOT cover: NBFCs, mutual funds, stock market investments

**What if you have more than ₹5 lakh?**

Strategy: Spread deposits across multiple banks.
₹5 lakh in Bank A, ₹5 lakh in Bank B = both are fully insured.

**Real events where this mattered:**
- PMC Bank (2019): Depositors couldn't withdraw their money for over a year
- Lakshmi Vilas Bank (2020): Merged forcibly by RBI
- In both cases, deposits up to ₹5 lakh were eventually safe

**Practical advice:**
Don't keep more than ₹5 lakh in any single bank if you're worried about risk.
Use strong banks (SBI, HDFC, ICICI) as primary accounts.
        """,
        "source": "Inspired by: Labour Law Advisor — 'Is your bank deposit safe?'",
        "source_url": "https://www.youtube.com/@LabourLawAdvisor",
        "tags": ["DICGC", "banking", "safety", "deposits", "RBI"],
    },

    # ══════════════════════════════════════════
    # CREDIT & LOANS
    # ══════════════════════════════════════════
    {
        "id": "q11",
        "category": "Credit & Loans",
        "question": "What is a CIBIL score and how do you improve it?",
        "answer": """
CIBIL score (now TransUnion CIBIL) is a 3-digit number (300–900) that represents your creditworthiness — how reliably you repay loans and credit cards.

**Score ranges:**
- 750–900: Excellent. Best loan rates. Easy approvals.
- 700–749: Good. Most loans approved at competitive rates.
- 650–699: Fair. Loans may be approved at higher rates.
- Below 650: Poor. Loan rejections likely. Work on improvement first.

**What affects your CIBIL score:**
1. Payment history (35%): Do you pay EMIs and credit card bills on time?
2. Credit utilisation (30%): How much of your credit limit are you using? Keep below 30%.
3. Credit history length (15%): Longer history = better. Don't close old accounts.
4. Credit mix (10%): Having both secured (home loan) and unsecured (credit card) is better.
5. New credit (10%): Each loan application triggers a "hard inquiry" which briefly lowers your score.

**How to improve your score:**
- Pay ALL dues on time — even minimum payment counts negatively if missed
- Keep credit card usage below 30% of limit
- Don't apply for multiple loans simultaneously
- Check your CIBIL report free at cibil.com annually (you get one free report per year)
- Dispute errors — they do exist and drag scores down unfairly

**The hidden trap:**
Co-signing someone else's loan makes you equally responsible. Their default hits YOUR CIBIL score.
        """,
        "source": "Inspired by: Finance with Sharan — 'CIBIL Score Guide'",
        "source_url": "https://www.youtube.com/@financewithsharan",
        "tags": ["CIBIL", "credit score", "loans", "credit card"],
    },
    {
        "id": "q12",
        "category": "Credit & Loans",
        "question": "How do home loans actually work? What is the real cost?",
        "answer": """
A home loan is the largest financial commitment most Indians will ever make. Most people focus on the monthly EMI — and completely miss the total cost.

**A real example:**
Loan amount: ₹60 lakh
Interest rate: 8.5% p.a.
Tenure: 20 years

EMI: ~₹52,000/month
Total paid over 20 years: ₹1.25 crore
Interest paid: ₹65 lakh (you paid MORE in interest than the loan itself)

**How amortisation works:**
In the first year, ~80% of your EMI goes toward interest and only ~20% reduces principal.
In the last year, ~80% reduces principal and ~20% is interest.
This is why prepaying in the early years saves enormous interest.

**The prepayment strategy:**
Making even one extra EMI per year can reduce a 20-year loan to 17 years, saving ₹10–15 lakh in interest.
Invest your bonus in prepayment if your home loan rate > your investment return rate.

**Floating vs Fixed rate:**
Floating rate: changes with RBI repo rate. Currently standard.
Fixed rate: fixed for 2–5 years, then floating. Rarely truly fixed for full tenure.

**Key hidden costs:**
Processing fees (0.5–1%), legal charges, technical valuation, insurance (sometimes forced bundled).
Always read the complete sanction letter before signing.
        """,
        "source": "Inspired by: CA Rachana Phadke Ranade — 'Home Loan Guide'",
        "source_url": "https://www.youtube.com/@CARachanaRanade",
        "tags": ["home loan", "EMI", "credit", "real estate", "interest"],
    },

    # ══════════════════════════════════════════
    # CAREER & INCOME
    # ══════════════════════════════════════════
    {
        "id": "q13",
        "category": "Career & Income",
        "question": "How do you negotiate a salary? What most people get wrong.",
        "answer": """
Most people accept the first number. That is the single most expensive mistake of your career.

**Why negotiation matters:**
A ₹5,000 higher starting salary compounds through every raise and every future job offer.
Over 10 years, that ₹5,000 could mean ₹10–20 lakh difference in total earnings.

**The negotiation framework:**

1. **Know your market value.** Check: LinkedIn Salary, Glassdoor, AmbitionBox, industry surveys. Know the range for your role, city, and experience.

2. **Never give the first number.** When asked "what are your salary expectations?", say: "I'm open to a competitive offer based on the role and responsibilities. What is the budgeted range?" Make them anchor first.

3. **Anchor high with justification.** If forced to name a number, ask for 20–30% more than you expect, with reasoning (your skills, market rate, competing offer).

4. **Competing offer = the most powerful leverage.** A real competing offer changes the entire negotiation. Get it before you need it.

5. **Negotiate beyond salary:** joining bonus, work from home flexibility, learning budget, stock options, performance review timeline.

6. **Stay silent after stating your number.** Silence is leverage. The person who speaks first after a number is stated usually concedes.

**The final key:**
Negotiation is expected. Hiring managers budget for it. The offer you receive is almost never the final offer. Always ask once.
        """,
        "source": "Inspired by: Ankur Warikoo — 'Salary Negotiation' content",
        "source_url": "https://www.youtube.com/@warikoo",
        "tags": ["salary", "career", "negotiation", "income"],
    },
    {
        "id": "q14",
        "category": "Career & Income",
        "question": "What is the difference between a job, freelancing, and a business?",
        "answer": """
Three ways to earn. Each has a fundamentally different risk-reward profile.

**Job (Service):**
You trade time for a fixed salary. The employer takes the risk; you take the certainty.
- Stability: High
- Upside: Capped (raises, promotions are incremental)
- Downside: Limited (layoffs happen, but rare for skilled workers)
- Best for: Building skills, accumulating savings, early career

**Freelancing:**
You sell a skill directly to multiple clients. More control, more risk.
- Stability: Variable (feast and famine cycles)
- Upside: 2–3× more per hour than equivalent job salary (no employer overhead)
- Downside: No benefits, no guaranteed monthly income, you handle taxes
- Best for: High-skill individuals willing to market themselves

**Business:**
You build systems that generate revenue with or without your direct time.
- Stability: Low initially, can become very high
- Upside: Unlimited in theory
- Downside: High initial risk, capital required, most fail in 3–5 years
- Best for: People with deep domain knowledge, risk tolerance, and capital buffer

**The progression most wealth-builders follow:**
Job → Freelancing on the side → Business from freelancing client base.
Or: Job → Investing aggressively → Financial independence → Entrepreneurship from a position of strength.

**The mistake to avoid:**
Quitting a job to start a business without 12 months of savings as runway.
        """,
        "source": "Inspired by: Ankur Warikoo — 'Job vs Business' content",
        "source_url": "https://www.youtube.com/@warikoo",
        "tags": ["career", "business", "freelance", "income", "entrepreneurship"],
    },

    # ══════════════════════════════════════════
    # INSURANCE & PROTECTION
    # ══════════════════════════════════════════
    {
        "id": "q15",
        "category": "Insurance & Protection",
        "question": "What is the difference between term insurance and ULIP? Why does it matter?",
        "answer": """
This is perhaps the most financially consequential product choice most Indians make — and most get it wrong.

**Term Insurance:**
Pure life cover. You pay a premium. If you die during the term, nominee gets the sum assured. If you survive, nothing is returned.
- ₹1 crore cover at age 25: ~₹8,000–12,000/year
- Purpose: Replace your income for your family if you die early.
- Verdict: The ONLY life insurance product most people need.

**ULIP (Unit Linked Insurance Plan):**
Combines insurance + investment. Part of your premium buys life cover; the rest is invested in market-linked funds.
- Premium: ₹50,000–₹1,00,000/year for similar coverage
- Returns: Often 6–8% after charges vs 12% from a pure index fund
- Lock-in: 5 years minimum
- Charges: Premium allocation charge, fund management charge, policy administration charge, mortality charge — all eat returns

**The mathematical reality:**
₹1,00,000 ULIP premium:
- Insurance cost: ₹15,000 (you could get same cover with term at ₹8,000)
- Remaining ₹85,000 minus charges (~₹20,000): ₹65,000 actually invested

vs. 
₹8,000 term insurance + ₹92,000 in Nifty 50 index fund:
At 12% returns over 20 years, the index fund strategy builds ₹3.2 crore more.

**ULIP is not always scam — but it is almost never optimal.**
Buy protection and investment separately. Always.
        """,
        "source": "Inspired by: Finance with Sharan & CA Rachana Ranade — Insurance series",
        "source_url": "https://www.youtube.com/@financewithsharan",
        "tags": ["insurance", "ULIP", "term insurance", "LIC", "protection"],
    },

    # ══════════════════════════════════════════
    # ADVANCED CONCEPTS
    # ══════════════════════════════════════════
    {
        "id": "q16",
        "category": "Advanced Concepts",
        "question": "What is the difference between XIRR and CAGR? Which should you use?",
        "answer": """
Both measure investment returns — but they apply to different situations.

**CAGR (Compound Annual Growth Rate):**
Used when you make a single lump-sum investment.
Formula: (Final Value / Initial Value)^(1/years) − 1
Example: ₹1 lakh grows to ₹2 lakh in 6 years. CAGR = (2/1)^(1/6) − 1 = 12.2%

**XIRR (Extended Internal Rate of Return):**
Used when you make multiple investments at different times (like SIPs).
It accounts for the exact timing of each cash flow.

**Why XIRR matters for SIP investors:**
Your ₹10,000 invested in Month 1 has been growing for 60 months.
Your ₹10,000 invested in Month 60 has only been growing for 1 month.
Simple annualised return would give a misleading number. XIRR adjusts for this.

**How to calculate XIRR:**
In Excel/Sheets: =XIRR(cash_flows, dates)
Make all SIP investments negative (outflows), final portfolio value positive (inflow).

**What a "good" XIRR looks like:**
Over 5+ years: 10–14% XIRR for a Nifty 50 index fund is strong.
Below 7%: You may have been better off in PPF.

**The trap:**
Many apps show "returns" using simple methods that look higher than actual XIRR.
Always verify with XIRR on your actual investment dates and amounts.
        """,
        "source": "Inspired by: Pranjal Kamra — 'XIRR vs CAGR' explainer",
        "source_url": "https://www.youtube.com/@PranjalKamra",
        "tags": ["XIRR", "CAGR", "returns", "SIP", "advanced"],
    },
    {
        "id": "q17",
        "category": "Advanced Concepts",
        "question": "What is Asset Allocation and why does it beat stock picking?",
        "answer": """
Asset allocation is deciding what percentage of your money goes into different asset classes — stocks, bonds, gold, real estate, cash.

**The research finding that changed investing:**
A landmark 1986 study (Brinson, Hood, Beebower) found that 91.5% of portfolio returns are explained by asset allocation — not by stock selection or market timing.

In plain English: HOW you divide your money matters far more than WHICH stocks you pick.

**Why this is true:**
Different assets respond differently to the same economic conditions:
- Rising inflation → gold rises, bonds fall
- Economic recession → bonds rise, stocks fall
- Strong economic growth → stocks rise, gold flat
- By holding all three, your portfolio is always partly in the "right" place.

**The rebalancing advantage:**
Say you want 70% equity, 20% debt, 10% gold.
After a bull market, equity is now 85%. You sell equity (high) and buy debt/gold (low).
After a crash, equity is 50%. You sell debt/gold (high relative) and buy equity (low).
Rebalancing mechanically forces you to buy low and sell high — without any forecasting.

**Simple 3-fund Indian portfolio:**
- Nifty 50 index fund: 50%
- Nifty Next 50 index fund: 20%
- Short-duration debt fund or PPF: 20%
- Sovereign Gold Bond: 10%

Rebalance once a year. No stock picking needed. Beat 90% of active fund managers over 15 years.
        """,
        "source": "Inspired by: Akshat Shrivastava — 'Asset Allocation Strategy'",
        "source_url": "https://www.youtube.com/@AkshatShrivastava",
        "tags": ["asset allocation", "portfolio", "advanced", "rebalancing"],
    },
]

# ══════════════════════════════════════════════
# CURRENT AFFAIRS IN FINANCE
# ══════════════════════════════════════════════
# Note: These are evergreen topics that remain relevant.
# For truly real-time news, users should check linked sources.

CURRENT_AFFAIRS = [
    {
        "id": "ca1",
        "title": "India's GDP Growth and What It Means for Your Investments",
        "category": "Economy",
        "summary": """
India is one of the world's fastest-growing major economies at 6–7% GDP growth annually.

**What this means practically:**
GDP growth → corporate earnings growth → stock market returns.
Companies in a fast-growing economy have more customers, more revenue, more profit.
This is a major reason why Indian equities have outperformed global peers over 15+ years.

**Sectors benefiting most from India's growth:**
Banking & Finance, Consumer goods, Infrastructure, IT/Digital, Healthcare.

**Risk:** Political instability, global recession, high oil prices can disrupt growth.

**For your portfolio:** India's growth story makes a strong case for staying invested in Indian equities for the long term, even through short-term volatility.
        """,
        "source": "RBI Annual Report, MOSPI (Ministry of Statistics)",
        "source_url": "https://www.rbi.org.in",
        "relevance": "High",
    },
    {
        "id": "ca2",
        "title": "RBI's Interest Rate Cycle — What It Means for Your EMI and FDs",
        "category": "Banking",
        "summary": """
The RBI's Monetary Policy Committee meets 6 times a year to decide the Repo Rate.

**The rate cycle and your finances:**

When rates RISE:
- Home loan, car loan, personal loan EMIs increase
- New FD rates improve
- Equity markets often dip short-term

When rates FALL:
- Existing borrowers benefit (floating rate loans)
- FD rates fall — time to lock in long-term FDs before they drop further
- Equity markets often rally

**What to do in a rising rate environment:**
- Lock FDs for longer tenure now (rates may fall later)
- Avoid taking new discretionary loans
- Invest in short-duration debt funds (less interest rate risk)

**What to do in a falling rate environment:**
- Prepay your home loan (rate benefits pass through)
- Consider FDs before rates drop further
- Equity tends to do well — stay invested
        """,
        "source": "RBI Monetary Policy Committee statements",
        "source_url": "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx",
        "relevance": "High",
    },
    {
        "id": "ca3",
        "title": "UPI and India's Digital Payment Revolution",
        "category": "Fintech",
        "summary": """
India processes more than 10 billion UPI transactions per month — more than the US, EU, and UK combined.

**What UPI changed:**
- Eliminated cash dependency for daily transactions
- Enabled instant P2P transfers 24/7 (even bank holidays)
- Created massive financial data trails that banks and fintechs use for credit scoring

**ONDC and the next wave:**
Open Network for Digital Commerce is attempting to do for commerce what UPI did for payments — create an interoperable open network where any app can list products from any seller.

**What this means for you:**
- Your UPI transaction history is increasingly used to assess creditworthiness (NBFC credit)
- Fintech lenders can now offer loans in minutes based on transaction history
- Better credit access for those with no traditional credit history

**Risk to watch:**
UPI fraud has risen sharply. Never share UPI PIN, never call back unknown numbers claiming to be bank officials, never scan QR codes to "receive" money (you only scan to PAY).
        """,
        "source": "NPCI (National Payments Corporation of India) data",
        "source_url": "https://www.npci.org.in/what-we-do/upi/product-statistics",
        "relevance": "Medium",
    },
    {
        "id": "ca4",
        "title": "The Budget 2024–25 — Key Changes That Affect Personal Finance",
        "category": "Taxation",
        "summary": """
Key personal finance changes from recent Union Budgets:

**New Tax Regime (Default from FY2024-25):**
- Standard deduction raised to ₹75,000 (from ₹50,000)
- New regime is now default — you must opt out to use old regime
- New slabs: ₹3–7 lakh: 5%, ₹7–10 lakh: 10%, ₹10–12 lakh: 15%, ₹12–15 lakh: 20%, above ₹15 lakh: 30%
- Tax rebate under 87A: zero tax up to ₹7 lakh income

**Long-Term Capital Gains (LTCG) on equities:**
- Increased from 10% to 12.5% on gains above ₹1.25 lakh
- Holding period remains 1 year for equity funds

**Short-Term Capital Gains (STCG):**
- Increased from 15% to 20%

**What you should do:**
- Calculate if new regime saves you more than old regime
- For most salaried people without large 80C investments: new regime is better
- Harvest LTCG below ₹1.25 lakh annually (tax free) — this is called tax loss/gain harvesting
        """,
        "source": "Union Budget 2024-25, Income Tax Department",
        "source_url": "https://www.indiabudget.gov.in",
        "relevance": "High",
    },
    {
        "id": "ca5",
        "title": "Gold — Why Indians Love It and What the Data Actually Says",
        "category": "Investments",
        "summary": """
India is the world's second-largest gold consumer. Indians collectively hold an estimated 25,000 tonnes of gold — more than the official reserves of most countries.

**Gold's actual returns:**
1979–2024: Gold has given ~10% CAGR in rupee terms.
This beats FDs but trails equity (12–14% CAGR for Nifty 50).

**Why gold still belongs in your portfolio:**
- Crisis hedge: Gold rises when markets fall (2008 crash: gold +25%)
- Rupee depreciation protection: As ₹ weakens vs $, gold in ₹ rises
- Inflation protection over very long periods (50+ years)

**Best ways to invest in gold:**
1. **Sovereign Gold Bond (SGB):** Best option. 2.5% additional annual interest + capital gains. Issued by government, zero making charges.
2. **Gold ETF:** Tracks gold price, stored digitally. Expense ratio ~0.5%. No lock-in.
3. **Physical gold:** Worst for investment. Making charges (10–20%), purity risk, storage risk, locker charges.

**The allocation rule:**
Gold: 10% maximum in a long-term portfolio. It is insurance, not primary wealth-builder.

**Watch for:** SGBs are currently not being issued regularly by the government.
        """,
        "source": "World Gold Council, RBI SGB notifications",
        "source_url": "https://www.gold.org/goldhub/research/gold-demand-trends",
        "relevance": "Medium",
    },
]

# ══════════════════════════════════════════════
# YOUTUBE CHANNELS
# ══════════════════════════════════════════════
YOUTUBE_CHANNELS = [
    {
        "name": "Nitish Rajput",
        "handle": "@NitishRajput",
        "url": "https://www.youtube.com/@NitishRajput",
        "specialty": "Macroeconomics, Geopolitics, India's economy explained in simple Hindi/English",
        "best_for": "Understanding global and Indian economic events",
        "subscribers": "5M+",
    },
    {
        "name": "Finance with Sharan",
        "handle": "@financewithsharan",
        "url": "https://www.youtube.com/@financewithsharan",
        "specialty": "Personal finance, mutual funds, tax planning for salaried Indians",
        "best_for": "Practical money management for working professionals",
        "subscribers": "2M+",
    },
    {
        "name": "CA Rachana Phadke Ranade",
        "handle": "@CARachanaRanade",
        "url": "https://www.youtube.com/@CARachanaRanade",
        "specialty": "Stock market, technical analysis, investing fundamentals",
        "best_for": "Stock market education, beginner to advanced",
        "subscribers": "4M+",
    },
    {
        "name": "Labour Law Advisor",
        "handle": "@LabourLawAdvisor",
        "url": "https://www.youtube.com/@LabourLawAdvisor",
        "specialty": "Tax filing, ITR, labour laws, PF, ESI, salary compliance",
        "best_for": "Tax filing, understanding your salary structure, employee rights",
        "subscribers": "15M+",
    },
    {
        "name": "Pranjal Kamra",
        "handle": "@PranjalKamra",
        "url": "https://www.youtube.com/@PranjalKamra",
        "specialty": "Value investing, fundamental analysis, long-term wealth creation",
        "best_for": "Learning value investing and stock analysis",
        "subscribers": "3M+",
    },
    {
        "name": "Akshat Shrivastava",
        "handle": "@AkshatShrivastava",
        "url": "https://www.youtube.com/@AkshatShrivastava",
        "specialty": "Global investing, US stocks, portfolio building, business finance",
        "best_for": "Advanced investors, global portfolio diversification",
        "subscribers": "2M+",
    },
    {
        "name": "Asset Yogi",
        "handle": "@AssetYogi",
        "url": "https://www.youtube.com/@AssetYogi",
        "specialty": "Financial products, insurance comparison, loan explainers",
        "best_for": "Understanding financial products before buying them",
        "subscribers": "4M+",
    },
    {
        "name": "Ankur Warikoo",
        "handle": "@warikoo",
        "url": "https://www.youtube.com/@warikoo",
        "specialty": "Personal development, money mindset, career and entrepreneurship",
        "best_for": "Career decisions, money habits, entrepreneurship mindset",
        "subscribers": "4M+",
    },
    {
        "name": "Groww",
        "handle": "@GrowwApp",
        "url": "https://www.youtube.com/@GrowwApp",
        "specialty": "Mutual fund and stock explainers, how-to investing guides",
        "best_for": "Beginners starting their investment journey",
        "subscribers": "2M+",
    },
]


def get_qa_by_category():
    result = {}
    for q in FINANCE_QA:
        result.setdefault(q["category"], []).append(q)
    return result


def get_qa_by_id(qid):
    return next((q for q in FINANCE_QA if q["id"] == qid), None)


def search_qa(query: str):
    query = query.lower()
    results = []
    for q in FINANCE_QA:
        score = 0
        if query in q["question"].lower():
            score += 3
        if query in q["answer"].lower():
            score += 1
        if any(query in tag for tag in q.get("tags", [])):
            score += 2
        if score > 0:
            results.append({**q, "_score": score})
    return sorted(results, key=lambda x: -x["_score"])


ALL_QA_CATEGORIES = sorted(set(q["category"] for q in FINANCE_QA))
ALL_CA_CATEGORIES = sorted(set(c["category"] for c in CURRENT_AFFAIRS))
