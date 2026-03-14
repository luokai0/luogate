# 🐉 LUO GATE SKILL — RESEARCH
from core.router import ask, ask_deep
from core.search import search
from core.files import write_file
from datetime import datetime

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def deep_research(topic):
    data1 = search(f"{topic} latest research 2026")
    data2 = search(f"{topic} expert analysis")
    data3 = search(f"{topic} statistics data")
    result = ask_deep(f"""Deep research report on: {topic}

Data 1: {data1}
Data 2: {data2}
Data 3: {data3}

Write a comprehensive report:
1. Executive Summary
2. Background and Context
3. Current State (2026)
4. Key Findings
5. Data and Statistics
6. Expert Opinions
7. Trends and Predictions
8. Opportunities and Threats
9. Recommendations
10. Conclusion

Make it detailed and actionable.""")
    write_file(f"research_{topic[:20]}_{ts()}.txt", result or "")
    return result

def competitor_analysis(company):
    data = search(f"{company} business model revenue strategy 2026")
    result = ask_deep(f"""Complete competitor analysis for: {company}
Data: {data}

Analyze:
1. Business model
2. Revenue streams
3. Target market
4. Strengths
5. Weaknesses
6. Opportunities to compete
7. Threats they face
8. How to beat them
9. What to copy
10. What to avoid""")
    write_file(f"competitor_{company[:20]}_{ts()}.txt", result or "")
    return result

def trend_analysis(industry):
    data = search(f"{industry} trends predictions 2026 2027")
    result = ask_deep(f"""Trend analysis for {industry}:
Data: {data}

Identify:
1. Top 10 emerging trends
2. Dying trends to avoid
3. Technologies changing the industry
4. New business models emerging
5. Consumer behavior shifts
6. Investment opportunities
7. Risks and disruptions
8. 2-year prediction""")
    write_file(f"trends_{industry[:20]}_{ts()}.txt", result or "")
    return result

def niche_finder(interests, budget):
    data = search("most profitable niches online business 2026")
    result = ask_deep(f"""Find the perfect niche for:
Interests: {interests}
Budget: ${budget}
Data: {data}

Analyze 10 potential niches:
- Market size
- Competition level
- Profitability
- Entry barrier
- Growth potential
- Best monetization method
- Time to profit

Rank them and recommend the best one with full action plan.""")
    write_file(f"niche_research_{ts()}.txt", result or "")
    return result

SKILLS = {
    "deep_research": deep_research,
    "competitor_analysis": competitor_analysis,
    "trend_analysis": trend_analysis,
    "niche_finder": niche_finder,
}
print(f"🔍 Research Skills loaded — {len(SKILLS)} skills!")
