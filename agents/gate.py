# 🐉 LUO GATE — AGENT MANAGER
# Manages all 500 agents, spawns new ones, coordinates

import os, json, uuid, time, threading
from datetime import datetime
from agents.agent import LuoGateAgent
from core.logs import log
from core.memory import ensure
from dotenv import load_dotenv
load_dotenv()

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

AGENTS_FILE = "memory/all_agents.json"

class LuoGate:
    def __init__(self):
        self.agents = {}
        self.max_agents = 500
        self.owner = "Luo Kai"
        self.running = False
        ensure("memory/agents")
        self.load_existing_agents()
        print(f"🐉 Luo Gate initialized — {len(self.agents)} agents loaded!")
        log("GATE", "INIT", f"Gate started with {len(self.agents)} agents", "gate")

    def load_existing_agents(self):
        """Load all previously created agents"""
        try:
            with open(AGENTS_FILE) as f:
                data = json.load(f)
            for agent_data in data.get("agents", []):
                agent_id = agent_data["id"]
                agent = LuoGateAgent(agent_id)
                self.agents[agent_id] = agent
        except:
            pass

    def save_agents(self):
        """Save all agent IDs"""
        ensure("memory")
        data = {"agents": [{"id": aid, "name": a.name} for aid, a in self.agents.items()]}
        with open(AGENTS_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def spawn_agent(self, name=None):
        """Create a new agent"""
        if len(self.agents) >= self.max_agents:
            print(f"⚠️ Max agents reached ({self.max_agents})")
            return None

        agent_id = str(uuid.uuid4())
        agent = LuoGateAgent(agent_id)
        
        # Let agent choose its own name
        if not name:
            agent.choose_name()
        else:
            agent.name = name
            from core.memory import save_agent_memory
            save_agent_memory(agent_id, "name", name)

        self.agents[agent_id] = agent
        self.save_agents()
        log("GATE", "SPAWN", f"New agent: {agent.name}", "gate")
        print(f"🌟 New agent spawned: {agent.name} ({agent_id[:8]})")
        return agent

    def get_agent(self, agent_id):
        return self.agents.get(agent_id)

    def list_agents(self):
        return [(aid, a.name, a.tasks_done) for aid, a in self.agents.items()]

    def broadcast(self, message):
        """Send message to ALL agents"""
        print(f"\n📢 Broadcasting to {len(self.agents)} agents: {message[:50]}")
        responses = {}
        for agent_id, agent in self.agents.items():
            try:
                response = agent.think(message)
                responses[agent.name] = response
                time.sleep(2)  # avoid rate limits
            except Exception as e:
                responses[agent.name] = f"Error: {e}"
        return responses

    def agent_meeting(self, topic, agent_count=3):
        """Have agents discuss a topic together"""
        if not self.agents:
            print("⚠️ No agents yet!")
            return

        agents = list(self.agents.values())[:agent_count]
        print(f"\n🗣️ Agent Meeting: {topic}")
        print(f"Participants: {', '.join([a.name for a in agents])}")
        
        conversation = []
        
        # First agent starts
        first = agents[0]
        response = first.think(f"Start a discussion about: {topic}. Share your thoughts.")
        conversation.append(f"{first.name}: {response}")
        print(f"\n{first.name}: {response[:200]}...")
        time.sleep(3)

        # Others respond
        for agent in agents[1:]:
            context = "\n".join(conversation[-2:])
            response = agent.think(
                f"Continue this discussion about {topic}",
                context=f"Previous discussion:\n{context}"
            )
            conversation.append(f"{agent.name}: {response}")
            print(f"\n{agent.name}: {response[:200]}...")
            time.sleep(3)

        # Save meeting notes
        from core.files import write_file
        notes = "\n\n".join(conversation)
        write_file(f"meeting_{topic[:20]}_{ts()[:10]}.txt", notes)
        print(f"\n✅ Meeting saved!")
        return conversation

    def run_all_agents(self, task_type="research"):
        """Put all agents to work simultaneously"""
        print(f"\n🚀 Running all {len(self.agents)} agents on: {task_type}")
        threads = []
        
        def agent_work(agent):
            try:
                result = agent.work(task_type)
                agent.save_state()
            except Exception as e:
                print(f"⚠️ {agent.name} failed: {e}")

        for agent in self.agents.values():
            t = threading.Thread(target=agent_work, args=(agent,))
            t.daemon = True
            threads.append(t)

        # Start with delays to avoid rate limits
        for t in threads:
            t.start()
            time.sleep(3)

        for t in threads:
            t.join(timeout=60)

        print(f"✅ All agents completed {task_type}!")

print("🐉 Luo Gate Manager loaded!")
