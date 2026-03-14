# 🐉 LUO GATE — CHAT SYSTEM
# Private chats between owner and agents
# Public chat for all agents + Luo Kai AI
import json, os
from datetime import datetime
from core.logs import log

CHATS_DIR = "core/chats/data"
PUBLIC_CHAT = "core/chats/data/public.jsonl"
OWNER = "Luo Kai"

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure():
    os.makedirs(CHATS_DIR, exist_ok=True)

def send_public(sender, message):
    """Send to public chat — visible to all"""
    ensure()
    entry = {"time": ts(), "sender": sender, "message": message, "type": "public"}
    with open(PUBLIC_CHAT, "a") as f:
        f.write(json.dumps(entry) + "\n")
    log(sender, "PUBLIC_CHAT", message[:100], "chat")
    print(f"💬 [{sender}]: {message[:100]}")

def send_private(sender, recipient, message):
    """Private chat between two parties"""
    ensure()
    chat_id = "_".join(sorted([sender, recipient]))
    path = f"{CHATS_DIR}/private_{chat_id}.jsonl"
    entry = {"time": ts(), "sender": sender, "recipient": recipient, "message": message}
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")
    log(sender, "PRIVATE_CHAT", f"To {recipient}: {message[:50]}", "chat")

def get_public_chat(limit=50):
    """Get public chat history"""
    ensure()
    try:
        with open(PUBLIC_CHAT) as f:
            lines = f.readlines()
        return [json.loads(l) for l in lines[-limit:] if l.strip()]
    except: return []

def get_private_chat(user1, user2, limit=50):
    """Get private chat between two users"""
    ensure()
    chat_id = "_".join(sorted([user1, user2]))
    path = f"{CHATS_DIR}/private_{chat_id}.jsonl"
    try:
        with open(path) as f:
            lines = f.readlines()
        return [json.loads(l) for l in lines[-limit:] if l.strip()]
    except: return []

def owner_message(message):
    """Owner (Luo Kai) sends to public chat"""
    send_public(OWNER, message)

def owner_private(agent_name, message):
    """Owner sends private message to agent"""
    send_private(OWNER, agent_name, message)
    print(f"🔐 Private message sent to {agent_name}")

def display_public_chat(limit=20):
    """Display public chat nicely"""
    messages = get_public_chat(limit)
    print(f"\n💬 PUBLIC CHAT — Last {len(messages)} messages")
    print("=" * 50)
    for msg in messages:
        print(f"[{msg['time'][11:16]}] {msg['sender']}: {msg['message'][:100]}")
    print("=" * 50)

print("💬 Chat System loaded!")
