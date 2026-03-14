# 🐉 LUO GATE SKILL — CONTENT CREATION
from core.router import ask, ask_deep
from core.search import search
from core.files import write_file
from datetime import datetime

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def write_viral_thread(topic):
    data = search(f"{topic} facts statistics 2026")
    result = ask(f"""Write a VIRAL Twitter/X thread about: {topic}
Data: {data}

Requirements:
- 10-15 tweets
- Tweet 1: Mind-blowing hook that stops scrolling
- Tweets 2-9: Value-packed insights
- Tweet 10: Powerful conclusion + CTA
- Each tweet under 280 characters
- Number each tweet (1/, 2/, etc)
- Include surprising facts and statistics
- Make it highly shareable""")
    write_file(f"thread_{topic[:20]}_{ts()}.txt", result or "")
    return result

def write_seo_article(keyword, word_count=2000):
    data = search(f"{keyword} complete guide 2026")
    result = ask_deep(f"""Write a complete {word_count} word SEO-optimized article about: {keyword}
Research: {data}

Structure:
- SEO title (under 60 chars)
- Meta description (under 160 chars)
- Introduction with hook
- 6-8 H2 sections with full content
- Each section: 200-300 words
- Include statistics and examples
- Internal linking suggestions
- FAQ section (5 questions)
- Conclusion with CTA

Write naturally for humans first, SEO second.""")
    write_file(f"article_{keyword[:20]}_{ts()}.txt", result or "")
    return result

def write_youtube_script(topic, duration_mins=10):
    result = ask_deep(f"""Write a complete {duration_mins}-minute YouTube video script about: {topic}

Include:
- HOOK (first 30 seconds — make it irresistible)
- INTRO (who you are, what they'll learn)
- MAIN CONTENT (5-7 sections)
- Each section with talking points
- B-roll suggestions
- Pattern interrupts every 2 minutes
- CTA (subscribe, like, comment)
- OUTRO

Make it conversational, engaging, educational.
Format with timestamps.""")
    write_file(f"yt_script_{topic[:20]}_{ts()}.txt", result or "")
    return result

def write_email_sequence(product, audience, emails=7):
    result = ask_deep(f"""Write a complete {emails}-email marketing sequence for:
Product: {product}
Audience: {audience}

Email 1 (Day 0): Welcome + quick win
Email 2 (Day 1): Your story + problem
Email 3 (Day 3): Solution introduction
Email 4 (Day 5): Case study/proof
Email 5 (Day 7): Objection handling
Email 6 (Day 9): Soft pitch
Email 7 (Day 11): Hard pitch with urgency

For each email:
- Subject line (3 variations)
- Preview text
- Full body
- CTA""")
    write_file(f"email_seq_{product[:20]}_{ts()}.txt", result or "")
    return result

def write_tiktok_scripts(niche, count=10):
    result = ask(f"""Write {count} TikTok video scripts for {niche} niche.

For each script:
- Hook (first 3 seconds — must stop scroll)
- Main content (45-55 seconds)
- CTA (last 5 seconds)
- On-screen text suggestions
- Trending sound suggestions
- Hashtags (10)

Make each one unique and viral-worthy.""")
    write_file(f"tiktok_{niche}_{ts()}.txt", result or "")
    return result

def create_digital_product(topic, product_type="ebook"):
    result = ask_deep(f"""Create a complete {product_type} about: {topic}

Requirements:
- Compelling title
- Table of contents (10+ chapters)
- Full content for each chapter
- Practical exercises
- Templates and checklists
- Resource list
- Bonus section
- Make it worth $47-$97

This should be a complete, publishable product
that delivers massive value.""")
    write_file(f"product_{topic[:20]}_{ts()}.txt", result or "")
    return result

SKILLS = {
    "write_viral_thread": write_viral_thread,
    "write_seo_article": write_seo_article,
    "write_youtube_script": write_youtube_script,
    "write_email_sequence": write_email_sequence,
    "write_tiktok_scripts": write_tiktok_scripts,
    "create_digital_product": create_digital_product,
}
print(f"✍️ Content Skills loaded — {len(SKILLS)} skills!")
