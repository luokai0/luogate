# 🐉 LUO GATE — KNOWLEDGE BASE
# All agents write and organize information here
# Accessible by all agents and owner
# Works offline too (for Luo Kai AI)
import json, os
from datetime import datetime
from core.logs import log

KB_DIR = "core/informations/data"
KB_INDEX = "core/informations/index.json"

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure():
    os.makedirs(KB_DIR, exist_ok=True)

def load_index():
    ensure()
    try:
        with open(KB_INDEX) as f:
            return json.load(f)
    except:
        return {"topics": {}, "total_entries": 0}

def save_index(idx):
    ensure()
    with open(KB_INDEX, "w") as f:
        json.dump(idx, f, indent=2)

def add_knowledge(agent_name, topic, content, category="general"):
    """Agent adds knowledge to the base"""
    ensure()
    idx = load_index()
    
    if topic not in idx["topics"]:
        idx["topics"][topic] = {"entries": 0, "category": category, "last_updated": ts()}
    
    idx["topics"][topic]["entries"] += 1
    idx["topics"][topic]["last_updated"] = ts()
    idx["total_entries"] += 1
    save_index(idx)
    
    # Save actual content
    safe_topic = topic[:30].replace(" ", "_").replace("/", "_")
    path = f"{KB_DIR}/{safe_topic}.jsonl"
    entry = {
        "time": ts(),
        "agent": agent_name,
        "topic": topic,
        "category": category,
        "content": content
    }
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    log(agent_name, "KNOWLEDGE", f"Added: {topic[:50]}", "informations")
    print(f"📚 {agent_name} added knowledge: {topic}")

def search_knowledge(query, limit=5):
    """Search the knowledge base"""
    ensure()
    idx = load_index()
    query_words = set(query.lower().split())
    
    results = []
    for topic in idx["topics"]:
        topic_words = set(topic.lower().split())
        if query_words & topic_words:
            safe_topic = topic[:30].replace(" ", "_").replace("/", "_")
            path = f"{KB_DIR}/{safe_topic}.jsonl"
            try:
                with open(path) as f:
                    entries = [json.loads(l) for l in f.readlines() if l.strip()]
                if entries:
                    results.append(entries[-1])
            except: continue
    
    return results[:limit]

def get_all_topics():
    idx = load_index()
    return list(idx["topics"].keys())

def get_knowledge(topic):
    """Get all knowledge about a topic"""
    ensure()
    safe_topic = topic[:30].replace(" ", "_").replace("/", "_")
    path = f"{KB_DIR}/{safe_topic}.jsonl"
    try:
        with open(path) as f:
            return [json.loads(l) for l in f.readlines() if l.strip()]
    except: return []

def knowledge_stats():
    idx = load_index()
    return f"📚 Knowledge Base: {len(idx['topics'])} topics, {idx['total_entries']} total entries"

print("📚 Knowledge Base loaded!")
