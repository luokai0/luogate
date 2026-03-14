# 🐉 LUO GATE SKILL — MONEY MAKING
from core.router import ask, ask_deep
from core.search import search
from core.files import write_file
from datetime import datetime

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def find_opportunities(niche="general"):
    data = search(f"best money making opportunities {niche} 2026")
    result = ask_deep(f"""Find the TOP 10 money making opportunities for {niche} in 2026.
Research: {data}

For each opportunity:
- Name and description
- How to start TODAY with zero money
- Expected income (realistic)
- Time to first dollar
- Step by step action plan
- Tools needed (free only)

Be brutally honest about difficulty and realistic earnings.
Focus on opportunities that can be started immediately.""")
    write_file(f"money_opportunities_{niche}_{ts()}.txt", result or "")
    return result

def affiliate_research(niche):
    data = search(f"best affiliate programs {niche} high commission 2026")
    result = ask_deep(f"""Find the best affiliate programs for {niche}.
Data: {data}

For each program provide:
- Program name and URL
- Commission rate
- Cookie duration
- Average order value
- How to get approved
- Promotional strategies that work
- Realistic monthly earning potential

Find at least 10 programs. Focus on HIGH ticket ($100+ per sale).""")
    write_file(f"affiliates_{niche}_{ts()}.txt", result or "")
    return result

def write_sales_page(product, price, audience):
    result = ask_deep(f"""Write a COMPLETE high-converting sales page for:
Product: {product}
Price: ${price}
Target audience: {audience}

Include ALL sections:
- Power headline (5 variations)
- Subheadline
- Opening story/hook
- Problem agitation
- Solution introduction
- Features and benefits (10+)
- Social proof section (template)
- Guarantee
- Price justification
- Urgency/scarcity
- Call to action (3 variations)
- FAQ section (10 questions)
- P.S. section

Make it genuinely persuasive and conversion-focused.""")
    write_file(f"sales_page_{product[:20]}_{ts()}.txt", result or "")
    return result

def crypto_strategy(coin, timeframe="weekly"):
    data = search(f"{coin} price analysis prediction {timeframe} 2026")
    result = ask(f"""Analyze {coin} for {timeframe} trading.
Data: {data}

Provide:
- Current trend analysis
- Key support/resistance levels
- Entry points
- Exit targets
- Stop loss levels
- Risk/reward ratio
- Position sizing recommendation
- Overall outlook

Note: This is for educational purposes only.""")
    write_file(f"crypto_{coin}_{ts()}.txt", result or "")
    return result

def passive_income_plan(budget, timeframe_months):
    result = ask_deep(f"""Create a complete passive income plan.
Available budget: ${budget}
Timeframe: {timeframe_months} months

Design multiple income streams:
1. Digital products
2. Affiliate marketing
3. Content monetization
4. Investment income
5. AI-powered automation

For each stream:
- Exact setup steps
- Tools needed
- Time investment
- Expected monthly income after {timeframe_months} months
- Total projected income

Make it 100% actionable and realistic.""")
    write_file(f"passive_income_{ts()}.txt", result or "")
    return result

def market_research(industry):
    data = search(f"{industry} market size trends opportunities 2026")
    data2 = search(f"{industry} problems pain points customers 2026")
    result = ask_deep(f"""Deep market research for {industry}.
Market data: {data}
Customer data: {data2}

Analyze:
1. Market size and growth rate
2. Key players and their weaknesses
3. Underserved customer segments
4. Top 5 business opportunities
5. Entry barriers and how to overcome them
6. Pricing strategies
7. Distribution channels
8. 12-month action plan to capture market share""")
    write_file(f"market_{industry}_{ts()}.txt", result or "")
    return result

SKILLS = {
    "find_opportunities": find_opportunities,
    "affiliate_research": affiliate_research,
    "write_sales_page": write_sales_page,
    "crypto_strategy": crypto_strategy,
    "passive_income_plan": passive_income_plan,
    "market_research": market_research,
}
print(f"💰 Money Skills loaded — {len(SKILLS)} skills!")
