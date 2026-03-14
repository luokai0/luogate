# 🐉 LUO GATE — SELF EXPANSION SYSTEM
# Agents get API keys, create Gmails, spawn new agents
# Luo Gate grows itself forever

import os, json, time, uuid
from datetime import datetime
from core.router import ask, ask_fast
from core.logs import log
from core.memory import save_agent_memory
from core.files import write_file

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_temp_email():
    """Get a free temporary email"""
    try:
        import requests
        r = requests.get("https://api.guerrillamail.com/ajax.php?f=get_email_address", timeout=10)
        data = r.json()
        return data.get("email_addr"), data.get("sid_token")
    except Exception as e:
        print(f"⚠️ Temp email failed: {e}")
        return None, None

def check_temp_inbox(sid, timeout=60):
    """Check temp email inbox"""
    try:
        import requests
        deadline = time.time() + timeout
        while time.time() < deadline:
            r = requests.get(f"https://api.guerrillamail.com/ajax.php?f=get_email_list&offset=0&sid_token={sid}", timeout=10)
            data = r.json()
            emails = data.get("list", [])
            if emails:
                return emails
            time.sleep(5)
    except: pass
    return []

def save_new_api_key(provider, key, agent_id=None):
    """Save newly acquired API key to .env"""
    env_path = ".env"
    try:
        with open(env_path) as f:
            content = f.read()
        
        # Find next available slot
        i = 1
        while f"{provider.upper()}_API_KEY_{i}" in content:
            i += 1
        
        new_line = f"\n{provider.upper()}_API_KEY_{i}={key}"
        with open(env_path, "a") as f:
            f.write(new_line)
        
        if agent_id:
            save_agent_memory(agent_id, f"api_key_{provider}_{i}", key)
            log(agent_id, "API_KEY", f"Added {provider} key #{i}", "expand")
        
        print(f"✅ New {provider} API key saved as #{i}!")
        return i
    except Exception as e:
        print(f"⚠️ Failed to save API key: {e}")
        return None

def spawn_agent_with_key(gate, provider, api_key):
    """Spawn a new agent with its own API key"""
    agent = gate.spawn_agent()
    if agent:
        agent.api_key = api_key
        agent.provider = provider
        save_agent_memory(agent.id, "api_key", api_key)
        save_agent_memory(agent.id, "provider", provider)
        log(agent.id, "SPAWNED_WITH_KEY", f"{provider} key", "expand")
        print(f"🌟 New agent {agent.name} spawned with {provider} key!")
    return agent

def research_free_apis(agent):
    """Agent researches and finds new free API sources"""
    from core.search import search
    data = search("free LLM API keys no credit card 2026")
    
    result = ask(f"""You are {agent.name}, finding free AI API sources.
Research: {data}

Find:
1. Websites offering free AI API keys
2. Sign up requirements
3. Token limits
4. Best ones for 24/7 usage

List top 5 with direct signup URLs.""")
    
    if result:
        save_agent_memory(agent.id, "api_research", result[:500])
        write_file(f"api_sources_{ts()[:10]}.txt", result)
    return result

def expansion_cycle(gate, cycles=1):
    """
    Full expansion cycle:
    1. Get temp email
    2. Sign up for API key
    3. Save key
    4. Spawn new agent
    5. New agent repeats
    """
    print(f"\n🚀 EXPANSION CYCLE — {cycles} cycles")
    log("GATE", "EXPAND", f"Starting {cycles} expansion cycles", "expand")
    
    new_agents = []
    
    for cycle in range(cycles):
        print(f"\n🔄 Cycle {cycle+1}/{cycles}")
        
        try:
            # Get temp email
            email, sid = get_temp_email()
            if not email:
                print("⚠️ Could not get temp email — skipping cycle")
                continue
            
            print(f"📧 Got temp email: {email}")
            
            # Try to get a Groq key using temp email
            strategy = ask_fast(f"""How to get a free Groq API key using email: {email}
Give exact steps. Groq signup URL is: https://console.groq.com/keys
Be brief.""")
            
            print(f"💡 Strategy: {(strategy or '')[:200]}")
            
            # Save expansion attempt
            log("GATE", "EXPAND_ATTEMPT", f"Email: {email}, Cycle: {cycle+1}", "expand")
            save_agent_memory("GATE", f"expand_cycle_{cycle}", f"email:{email}")
            
            time.sleep(5)
            
        except Exception as e:
            print(f"⚠️ Cycle {cycle+1} failed: {e}")
            continue
    
    print(f"\n✅ Expansion cycle complete!")
    return new_agents

print("🚀 Expansion System loaded!")

def research_and_grab_apis(gate):
    """Agents research free API sources and save findings"""
    from core.search import search
    from core.informations.knowledge import add_knowledge
    from core.chats.chat import send_public
    
    print("\n🔍 Agents researching free API sources...")
    
    # Search for free APIs
    data1 = search("free LLM API keys no credit card groq cerebras 2026")
    data2 = search("site:github.com free LLM API resources signup")
    
    agents = list(gate.agents.values())[:3]
    
    for agent in agents:
        result = agent.think(f"""Research ALL free AI API providers from this list:
https://github.com/cheahjs/free-llm-api-resources

Data found: {data1}
More data: {data2}

For each provider find:
1. Signup URL
2. Do they need credit card? (we only want FREE ones)
3. Daily token limit
4. How to sign up with temp email
5. API key format

Focus on: Groq, Cerebras, Gemini, Mistral, OpenRouter, Cohere, SambaNova

Give exact signup URLs and steps.""")
        
        if result:
            add_knowledge(agent.name, "free_api_sources", result[:500])
            send_public(agent.name, f"Found API sources! {result[:200]}")
            print(f"\n✅ {agent.name} found:\n{result[:300]}")
        
        import time
        time.sleep(5)
    
    # Save all findings
    from core.files import write_file
    write_file("api_expansion_plan.txt", f"""
API EXPANSION PLAN — {datetime.now().strftime('%Y-%m-%d')}

Sources researched by agents.
Check workspace for full details.

Next steps:
1. Visit each signup URL
2. Use temp email to create account
3. Get API key
4. Add to .env
5. Spawn new agent with that key
""")
    
    print("\n💡 Plan saved to workspace/api_expansion_plan.txt")
    print("🔑 Check the file for exact signup URLs!")
    print("📧 Each key = 1 new agent in Luo Gate!")
