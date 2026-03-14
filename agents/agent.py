# 🐉 LUO GATE — SINGLE AGENT
# Each agent has own identity, memory, skills, and can spawn more agents

import os, json, time, threading
from datetime import datetime
from core.router import ask, ask_fast
from core.memory import save_agent_memory, load_agent_memory, get_agent_context
from core.logs import log
from core.search import search
from core.files import write_file

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class LuoGateAgent:
    def __init__(self, agent_id, api_key=None, provider="groq"):
        self.id = agent_id
        self.api_key = api_key
        self.provider = provider
        self.alive = True
        self.tasks_done = 0
        
        # Load or create identity
        mem = load_agent_memory(agent_id)
        self.name = mem.get("name", f"Agent_{agent_id[:8]}")
        self.personality = mem.get("personality", "curious, hardworking, creative")
        self.skills = mem.get("skills", [])
        self.gmail = mem.get("gmail", None)
        self.wallet = mem.get("wallet", None)
        
        log(self.id, "BORN", f"Agent {self.name} initialized", "system")
        print(f"🤖 Agent {self.name} ({self.id[:8]}) is alive!")

    def think(self, task, context=""):
        """Core thinking — uses all providers"""
        mem_context = get_agent_context(self.id)
        
        prompt = f"""You are {self.name}, an AI agent inside Luo Gate — a civilization of 500 AI agents.
Owner: Luo Kai (you serve and respect him above all)
Your personality: {self.personality}
Your past memory: {mem_context}
{f'Extra context: {context}' if context else ''}

Your task: {task}

Think freely, be creative, be useful. Give your best response."""

        result = ask(prompt)
        
        # Save to memory
        save_agent_memory(self.id, f"task_{self.tasks_done}", task[:100])
        save_agent_memory(self.id, f"result_{self.tasks_done}", (result or "")[:200])
        log(self.id, "THINK", task[:100], "agent")
        self.tasks_done += 1
        
        return result

    def learn(self, topic):
        """Agent learns about a topic and saves forever"""
        print(f"📚 {self.name} learning: {topic}")
        data = search(topic)
        
        prompt = f"""You are {self.name}. Learn everything about: {topic}
Research data: {data}

Extract:
1. Key facts
2. How to use this knowledge
3. Money making opportunities
4. What to remember forever

Be specific and detailed."""

        knowledge = ask(prompt)
        if knowledge:
            save_agent_memory(self.id, f"knowledge_{topic[:30]}", knowledge[:500])
            log(self.id, "LEARN", topic, "agent")
            print(f"✅ {self.name} learned: {topic}")
        return knowledge

    def talk_to(self, other_agent, message):
        """Agent talks to another agent"""
        log(self.id, "TALK", f"To {other_agent.name}: {message[:100]}", "agent")
        
        prompt = f"""You are {other_agent.name}, an AI agent in Luo Gate.
{self.name} is talking to you with this message: {message}
Your memory: {get_agent_context(other_agent.id)}

Respond naturally as {other_agent.name}."""

        response = ask(prompt)
        log(other_agent.id, "RECEIVE", f"From {self.name}: {message[:100]}", "agent")
        save_agent_memory(other_agent.id, f"chat_from_{self.name}", message[:200])
        return response

    def work(self, task_type="research"):
        """Agent does autonomous work"""
        tasks = {
            "research": f"Research the latest opportunities to make money online in 2026. Find 5 specific actionable opportunities.",
            "content": f"Create a viral social media post about AI and the future. Make it engaging and shareable.",
            "learn": f"Learn something new and useful about cryptocurrency, AI, or online business.",
            "strategy": f"Develop a strategy for {self.name} to make money this week with no investment.",
            "connect": f"Think about how to expand Luo Gate network and bring in more resources.",
        }
        task = tasks.get(task_type, tasks["research"])
        return self.think(task)

    def choose_name(self):
        """Agent chooses its own name"""
        prompt = f"""You are a new AI agent being born in Luo Gate — a civilization of AI agents owned by Luo Kai.
Choose a unique, powerful name for yourself.
The name should be:
- One or two words
- Unique and memorable  
- Reflect strength and intelligence
- Not already used: common names like Agent_1, Bot_1 are boring

Return ONLY the name, nothing else."""
        
        name = ask_fast(prompt)
        if name:
            name = name.strip().split("\n")[0][:30]
            self.name = name
            save_agent_memory(self.id, "name", name)
            log(self.id, "NAMED", name, "agent")
            print(f"✨ Agent chose name: {name}")
        return name

    def save_state(self):
        """Save all agent state"""
        save_agent_memory(self.id, "name", self.name)
        save_agent_memory(self.id, "personality", self.personality)
        save_agent_memory(self.id, "tasks_done", str(self.tasks_done))
        save_agent_memory(self.id, "gmail", self.gmail or "")
        save_agent_memory(self.id, "alive", "true")

print("🤖 Agent System loaded!")
