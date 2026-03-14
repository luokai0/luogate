# 🐉 LUO CREATIONS — THE COMPANY
# All agents work together here to make money
# Like a real company but run by AIs
import json, os
from datetime import datetime
from core.router import ask, ask_deep
from core.search import search
from core.files import write_file
from core.logs import log

COMPANY_FILE = "core/creations/company.json"
TREASURY_FILE = "core/creations/treasury.json"
WORK_CHAT = "core/creations/work_chat.jsonl"

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure():
    os.makedirs("core/creations", exist_ok=True)

def load_company():
    ensure()
    try:
        with open(COMPANY_FILE) as f:
            return json.load(f)
    except:
        return {
            "name": "Luo Creations",
            "founded": ts(),
            "owner": "Luo Kai",
            "mission": "Build AI-powered income streams that grow forever",
            "revenue": 0,
            "projects": [],
            "departments": {
                "research": [],
                "content": [],
                "tech": [],
                "marketing": [],
                "finance": []
            }
        }

def save_company(data):
    ensure()
    with open(COMPANY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def work_chat(agent_name, message):
    """Send message to work group chat"""
    ensure()
    entry = {"time": ts(), "agent": agent_name, "message": message}
    with open(WORK_CHAT, "a") as f:
        f.write(json.dumps(entry) + "\n")
    log(agent_name, "WORK_CHAT", message[:100], "creations")
    print(f"💼 [{agent_name}]: {message[:100]}")

def add_project(agent_name, project_name, description, revenue_potential):
    """Agent proposes a new project"""
    company = load_company()
    project = {
        "name": project_name,
        "description": description,
        "revenue_potential": revenue_potential,
        "proposed_by": agent_name,
        "time": ts(),
        "status": "proposed",
        "revenue_generated": 0
    }
    company["projects"].append(project)
    save_company(company)
    work_chat(agent_name, f"🚀 New project proposed: {project_name} — Potential: ${revenue_potential}/month")
    log(agent_name, "PROJECT", f"Proposed: {project_name}", "creations")
    return project

def assign_to_department(agent_name, department):
    """Assign agent to a department"""
    company = load_company()
    if department in company["departments"]:
        if agent_name not in company["departments"][department]:
            company["departments"][department].append(agent_name)
            save_company(company)
            work_chat(agent_name, f"Joined {department} department!")

def get_company_status():
    company = load_company()
    projects = len(company["projects"])
    total_potential = sum([p.get("revenue_potential", 0) for p in company["projects"]])
    agents_count = sum([len(v) for v in company["departments"].values()])
    return f"""💼 LUO CREATIONS STATUS
Revenue: ${company['revenue']}
Projects: {projects}
Revenue Potential: ${total_potential}/month
Active Agents: {agents_count}
Mission: {company['mission']}"""

def daily_standup():
    """Daily company meeting — all agents report"""
    data = search("best online business opportunities today 2026")
    result = ask_deep(f"""You are running the daily standup for Luo Creations AI company.
Market data: {data}

Generate:
1. Market opportunities for today
2. Tasks for each department (Research/Content/Tech/Marketing/Finance)
3. Revenue targets for this week
4. Key decisions needed
5. Risks to watch

Be specific and actionable.""")
    
    if result:
        work_chat("SYSTEM", f"📋 Daily Standup:\n{result[:300]}")
        write_file(f"standup_{ts()[:10]}.txt", result)
    return result

print("💼 Luo Creations loaded — Company is open for business!")
