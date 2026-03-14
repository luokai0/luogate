# 🐉 LUO GATE SKILL — CODING
from core.router import ask, ask_deep
from core.files import write_file
from datetime import datetime

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def build_bot(platform, purpose):
    result = ask_deep(f"""Build a complete {platform} bot for: {purpose}

Provide:
- Complete working Python code
- All dependencies (requirements.txt)
- Setup instructions
- Configuration options
- Error handling
- Rate limiting
- Deployment guide

Make it production-ready.""")
    write_file(f"bot_{platform}_{ts()}.py", result or "")
    return result

def build_scraper(target, data_needed):
    result = ask_deep(f"""Build a web scraper for {target} to extract: {data_needed}

Provide complete Python code with:
- Playwright or requests+BS4
- Anti-detection measures
- Error handling and retries
- Data storage (JSON/CSV)
- Rate limiting
- Proxy support
- Full working code""")
    write_file(f"scraper_{target[:20]}_{ts()}.py", result or "")
    return result

def build_api(purpose, endpoints):
    result = ask_deep(f"""Build a REST API for: {purpose}
Endpoints needed: {endpoints}

Provide:
- Complete FastAPI/Flask code
- All endpoints with handlers
- Database models
- Authentication
- Error handling
- Requirements.txt
- Deployment guide (Railway/Render free tier)""")
    write_file(f"api_{purpose[:20]}_{ts()}.py", result or "")
    return result

def fix_code(code, error):
    result = ask(f"""Fix this Python code:

CODE:
{code}

ERROR:
{error}

Provide:
1. What caused the error
2. Fixed code
3. What you changed and why""")
    return result

def build_automation(task):
    result = ask_deep(f"""Build a Python automation script for: {task}

Requirements:
- Complete working code
- Error handling
- Logging
- Schedule support
- Can run 24/7
- All imports included""")
    write_file(f"automation_{task[:20]}_{ts()}.py", result or "")
    return result

SKILLS = {
    "build_bot": build_bot,
    "build_scraper": build_scraper,
    "build_api": build_api,
    "fix_code": fix_code,
    "build_automation": build_automation,
}
print(f"💻 Coding Skills loaded — {len(SKILLS)} skills!")
