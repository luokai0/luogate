# 🐉 LUO GATE — PERMANENT MEMORY SYSTEM
import json, os
from datetime import datetime

MEMORY_DIR = "memory"
AGENTS_MEMORY_DIR = "memory/agents"

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure(path):
    os.makedirs(path, exist_ok=True)

def save_agent_memory(agent_id, key, value):
    ensure(AGENTS_MEMORY_DIR)
    path = f"{AGENTS_MEMORY_DIR}/{agent_id}.json"
    try:
        with open(path) as f: data = json.load(f)
    except: data = {"id": agent_id, "created": ts(), "memories": {}}
    data["memories"][key] = {"value": value, "time": ts()}
    with open(path, "w") as f: json.dump(data, f, indent=2)

def load_agent_memory(agent_id):
    path = f"{AGENTS_MEMORY_DIR}/{agent_id}.json"
    try:
        with open(path) as f: return json.load(f)
    except: return {"id": agent_id, "memories": {}}

def get_agent_context(agent_id, limit=5):
    mem = load_agent_memory(agent_id)
    memories = mem.get("memories", {})
    recent = list(memories.items())[-limit:]
    if not recent: return ""
    return "\n".join([f"- {k}: {v['value'][:100]}" for k,v in recent])

print("🧠 Memory System loaded!")
