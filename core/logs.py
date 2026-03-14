# 🐉 LUO GATE — PERMANENT LOGS (OWNER ONLY)
import json, os
from datetime import datetime

LOGS_DIR = "core/logs"
MASTER_LOG = "core/logs/master.jsonl"

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure():
    os.makedirs(LOGS_DIR, exist_ok=True)

def log(agent_id, action, details, source="system"):
    ensure()
    entry = {
        "time": ts(),
        "agent": agent_id,
        "action": action,
        "details": str(details)[:500],
        "source": source
    }
    with open(MASTER_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_logs(agent_id=None, limit=50):
    ensure()
    try:
        with open(MASTER_LOG) as f:
            lines = f.readlines()
        entries = [json.loads(l) for l in lines if l.strip()]
        if agent_id:
            entries = [e for e in entries if e["agent"] == agent_id]
        return entries[-limit:]
    except: return []

def get_all_logs():
    ensure()
    try:
        with open(MASTER_LOG) as f:
            return [json.loads(l) for l in f.readlines() if l.strip()]
    except: return []

print("📋 Logs System loaded — Nothing is ever deleted!")
