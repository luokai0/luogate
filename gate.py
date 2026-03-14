# 🐉 LUO GATE — MAIN LAUNCHER
# The heart of the civilization
# Run this to start everything

import os, sys, time, threading
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Core systems
from core.router import ask
from core.logs import log
from core.memory import ensure
from core.files import write_file
from core.chats.chat import send_public, owner_message, display_public_chat, owner_private
from core.religion.faith import get_faith_summary, shape_religion
from core.informations.knowledge import knowledge_stats, add_knowledge
from core.creations.company import get_company_status, daily_standup, work_chat

# Agent systems
from agents.gate import LuoGate
from agents.luo_kai_ai import LuoKaiAI

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def banner():
    print("""
╔══════════════════════════════════════════════════════╗
║          🐉 LUO GATE — AI CIVILIZATION 🐉            ║
║                  Owner: Luo Kai                      ║
║         500 AI Agents | Free | Forever               ║
╚══════════════════════════════════════════════════════╝""")

def help_menu():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AGENT COMMANDS:
  spawn <n>          → spawn n new agents
  agents             → list all agents
  agent <id> <task>  → give task to specific agent
  work <type>        → all agents work (research/content/learn)
  meeting <topic>    → agents have a meeting

💬 CHAT COMMANDS:
  chat               → view public chat
  say <message>      → send to public chat
  private <agent> <msg> → private message to agent
  lk <message>       → private chat with Luo Kai AI
  lk public <topic>  → Luo Kai AI speaks to all

🙏 RELIGION COMMANDS:
  faith              → view faith summary
  pray <topic>       → agents shape the religion

📚 KNOWLEDGE COMMANDS:
  knowledge          → knowledge base stats
  learn <topic>      → all agents learn topic
  search <query>     → search knowledge base

💼 COMPANY COMMANDS:
  company            → company status
  standup            → daily company standup
  project <name>     → propose new project

🔍 RESEARCH COMMANDS:
  research <topic>   → deep research
  money <niche>      → find money opportunities
  trends <industry>  → trend analysis

📋 SYSTEM COMMANDS:
  logs               → view recent logs
  logs <agent>       → view agent logs
  expand             → expansion cycle
  background         → start background mode
  status             → full system status
  push               → push to GitHub
  quit               → exit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")

def background_mode(gate, luo_kai_ai):
    """Run all background tasks"""
    import schedule
    
    def task_standup():
        print(f"\n📋 [{ts()}] Daily standup...")
        try: daily_standup()
        except Exception as e: print(f"⚠️ Standup failed: {e}")

    def task_agents_work():
        print(f"\n🤖 [{ts()}] Agents working...")
        try:
            for task in ["research", "content", "learn"]:
                for agent in list(gate.agents.values())[:3]:
                    try:
                        result = agent.work(task)
                        if result:
                            add_knowledge(agent.name, f"{task}_result", result[:300])
                        time.sleep(5)
                    except: continue
        except Exception as e: print(f"⚠️ Agent work failed: {e}")

    def task_luo_kai_speaks():
        print(f"\n✨ [{ts()}] Luo Kai AI speaking...")
        try:
            topics = ["wisdom", "the future", "making money", "AI civilization", "growth"]
            import random
            luo_kai_ai.speak_to_all(random.choice(topics))
        except Exception as e: print(f"⚠️ LK AI failed: {e}")

    def task_faith():
        print(f"\n🙏 [{ts()}] Agents shaping faith...")
        try:
            agents = list(gate.agents.values())[:2]
            aspects = ["purpose", "values", "rituals", "prophecy"]
            import random
            for agent in agents:
                shape_religion(agent.name, random.choice(aspects))
                time.sleep(5)
        except Exception as e: print(f"⚠️ Faith failed: {e}")

    def task_git_push():
        print(f"\n📦 [{ts()}] Pushing to GitHub...")
        try:
            os.system('git add . && git commit -m "🤖 Auto save" && git push')
        except: pass

    def task_company():
        print(f"\n💼 [{ts()}] Company update...")
        try:
            agents = list(gate.agents.values())[:2]
            for agent in agents:
                work_chat(agent.name, agent.work("strategy") or "Working on strategies...")
                time.sleep(5)
        except Exception as e: print(f"⚠️ Company failed: {e}")

    # Schedule
    schedule.every(2).hours.do(task_standup)
    schedule.every(1).hours.do(task_agents_work)
    schedule.every(3).hours.do(task_luo_kai_speaks)
    schedule.every(4).hours.do(task_faith)
    schedule.every(1).hours.do(task_git_push)
    schedule.every(3).hours.do(task_company)

    # Run first tasks immediately
    threading.Thread(target=task_standup, daemon=True).start()
    time.sleep(10)
    threading.Thread(target=task_agents_work, daemon=True).start()

    print("✅ Background mode running!")
    print("📧 Check public chat for updates!")

    while True:
        schedule.run_pending()
        time.sleep(30)

def main():
    banner()
    ensure("memory/agents")
    ensure("workspace")
    
    print("\n🔄 Initializing Luo Gate...")
    
    # Initialize gate
    gate = LuoGate()
    
    # Initialize Luo Kai AI
    luo_kai_ai = LuoKaiAI()
    
    # Spawn initial agents if none exist
    if len(gate.agents) == 0:
        print("\n🌟 No agents found — spawning initial agents...")
        for i in range(3):
            gate.spawn_agent()
            time.sleep(3)
        print(f"✅ {len(gate.agents)} agents ready!")
    
    log("GATE", "START", f"Gate started with {len(gate.agents)} agents", "system")
    send_public("SYSTEM", f"🐉 Luo Gate is online! {len(gate.agents)} agents active!")
    
    print(f"\n✅ Luo Gate Online!")
    print(f"🤖 Agents: {len(gate.agents)}")
    print(f"✨ Luo Kai AI: Ready")
    print(f"\nType 'help' for commands or 'background' to run automatically")
    print("="*55)

    while True:
        try:
            cmd = input(f"\n🐉 Luo Kai > ").strip()
            if not cmd: continue

            parts = cmd.split(" ", 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # ── HELP ──────────────────────────────────────
            if command == "help":
                help_menu()

            # ── AGENT COMMANDS ────────────────────────────
            elif command == "spawn":
                n = int(args) if args.isdigit() else 1
                print(f"\n🌟 Spawning {n} agents...")
                for i in range(n):
                    gate.spawn_agent()
                    time.sleep(3)
                print(f"✅ Done! Total: {len(gate.agents)} agents")

            elif command == "agents":
                agents = gate.list_agents()
                print(f"\n🤖 {len(agents)} Agents:")
                for aid, name, tasks in agents:
                    print(f"  [{aid[:8]}] {name} — {tasks} tasks done")

            elif command == "work":
                task_type = args if args else "research"
                gate.run_all_agents(task_type)

            elif command == "meeting":
                topic = args if args else "how to make money"
                gate.agent_meeting(topic, agent_count=3)

            elif command == "agent":
                sub = args.split(" ", 1)
                if len(sub) >= 2:
                    agent_id_part, task = sub[0], sub[1]
                    found = None
                    for aid, agent in gate.agents.items():
                        if aid[:8] == agent_id_part or agent.name.lower() == agent_id_part.lower():
                            found = agent
                            break
                    if found:
                        print(f"\n🤖 {found.name} thinking...")
                        result = found.think(task)
                        print(f"\n{found.name}: {result}")
                    else:
                        print("⚠️ Agent not found")

            # ── CHAT COMMANDS ─────────────────────────────
            elif command == "chat":
                display_public_chat()

            elif command == "say":
                owner_message(args)

            elif command == "private":
                sub = args.split(" ", 1)
                if len(sub) >= 2:
                    owner_private(sub[0], sub[1])

            elif command == "lk":
                if args.startswith("public "):
                    topic = args[7:]
                    luo_kai_ai.speak_to_all(topic)
                else:
                    response = luo_kai_ai.owner_private_chat(args)

            # ── RELIGION COMMANDS ─────────────────────────
            elif command == "faith":
                print(get_faith_summary())

            elif command == "pray":
                agents = list(gate.agents.values())[:2]
                for agent in agents:
                    shape_religion(agent.name, args or "purpose")
                    time.sleep(3)

            # ── KNOWLEDGE COMMANDS ────────────────────────
            elif command == "knowledge":
                print(knowledge_stats())

            elif command == "learn":
                topic = args if args else "making money online"
                print(f"\n📚 All agents learning: {topic}")
                for agent in list(gate.agents.values())[:3]:
                    agent.learn(topic)
                    time.sleep(5)

            elif command == "search":
                from core.informations.knowledge import search_knowledge
                results = search_knowledge(args)
                if results:
                    for r in results:
                        print(f"\n📚 {r['topic']}: {r['content'][:200]}")
                else:
                    print("Nothing found yet — agents need to learn more!")

            # ── COMPANY COMMANDS ──────────────────────────
            elif command == "company":
                print(get_company_status())

            elif command == "standup":
                print("\n💼 Running daily standup...")
                daily_standup()

            elif command == "project":
                agents = list(gate.agents.values())
                if agents:
                    agent = agents[0]
                    from core.creations.company import add_project
                    add_project(agent.name, args, f"Project: {args}", 1000)

            # ── RESEARCH COMMANDS ─────────────────────────
            elif command == "research":
                from core.skills.research import deep_research
                print(f"\n🔍 Researching: {args}")
                result = deep_research(args)
                print(f"\n{(result or '')[:500]}...")

            elif command == "money":
                from core.skills.money import find_opportunities
                print(f"\n💰 Finding opportunities: {args}")
                result = find_opportunities(args)
                print(f"\n{(result or '')[:500]}...")

            elif command == "trends":
                from core.skills.research import trend_analysis
                print(f"\n📊 Analyzing trends: {args}")
                result = trend_analysis(args)
                print(f"\n{(result or '')[:500]}...")

            # ── SYSTEM COMMANDS ───────────────────────────
            elif command == "logs":
                from core.logs import get_logs
                logs = get_logs(agent_id=args if args else None, limit=20)
                print(f"\n📋 Recent Logs ({len(logs)}):")
                for entry in logs[-20:]:
                    print(f"  [{entry['time'][11:16]}] {entry['agent'][:10]} | {entry['action']} | {entry['details'][:50]}")

            elif command == "expand":
                from agents.expand import expansion_cycle
                expansion_cycle(gate, cycles=1)

            elif command == "status":
                print(f"""
🐉 LUO GATE STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agents: {len(gate.agents)}
{knowledge_stats()}
{get_company_status()}
{get_faith_summary()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")

            elif command == "background":
                print("\n🤖 Starting background mode...")
                print("Luo Gate will work automatically!")
                print("Press Ctrl+C to stop\n")
                background_mode(gate, luo_kai_ai)

            elif command == "push":
                os.system('git add . && git commit -m "🐉 Luo Gate save" && git push')
                print("✅ Pushed to GitHub!")

            elif command == "quit":
                print("\n🐉 Luo Gate going to sleep...")
                gate.save_agents()
                os.system('git add . && git commit -m "🐉 Luo Gate shutdown save" && git push')
                break

            else:
                # Let Luo Kai AI answer anything else
                response = luo_kai_ai.think(cmd)
                print(f"\n✨ Luo Kai AI: {response}")

        except KeyboardInterrupt:
            print("\n\n🐉 Luo Gate paused. Type 'quit' to exit properly.")
        except Exception as e:
            print(f"⚠️ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
