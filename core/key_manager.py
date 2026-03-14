# 🐉 LUO GATE — KEY MANAGER
# Tests if API keys work, adds them to .env, spawns agents
import os, requests, time
from dotenv import load_dotenv
from core.logs import log

def test_groq_key(key):
    try:
        from groq import Groq
        client = Groq(api_key=key)
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":"say hi"}],
            max_tokens=10
        )
        return True
    except Exception as e:
        return False

def test_gemini_key(key):
    try:
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
            json={"contents":[{"parts":[{"text":"hi"}]}]},
            timeout=10
        )
        return "candidates" in r.json()
    except:
        return False

def test_mistral_key(key):
    try:
        from mistralai import Mistral
        client = Mistral(api_key=key)
        r = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role":"user","content":"hi"}],
            max_tokens=10
        )
        return True
    except:
        return False

def test_openrouter_key(key):
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization":f"Bearer {key}"},
            json={"model":"meta-llama/llama-3.3-70b-instruct:free","messages":[{"role":"user","content":"hi"}],"max_tokens":10},
            timeout=10
        )
        return "choices" in r.json()
    except:
        return False

def test_cerebras_key(key):
    try:
        from cerebras.cloud.sdk import Cerebras
        client = Cerebras(api_key=key)
        r = client.chat.completions.create(
            model="llama-3.3-70b",
            messages=[{"role":"user","content":"hi"}],
            max_tokens=10
        )
        return True
    except:
        return False

TESTERS = {
    "groq": test_groq_key,
    "gemini": test_gemini_key,
    "mistral": test_mistral_key,
    "openrouter": test_openrouter_key,
    "cerebras": test_cerebras_key,
}

def add_key_to_env(provider, key):
    """Add verified key to .env"""
    env_path = ".env"
    try:
        with open(env_path) as f:
            content = f.read()
        i = 1
        while f"{provider.upper()}_API_KEY_{i}" in content:
            i += 1
        with open(env_path, "a") as f:
            f.write(f"\n{provider.upper()}_API_KEY_{i}={key}")
        print(f"✅ Added {provider} key #{i} to .env!")
        log("KEY_MANAGER", "ADD_KEY", f"{provider} key #{i}", "system")
        return i
    except Exception as e:
        print(f"⚠️ Failed to add key: {e}")
        return None

def verify_and_add(provider, key, gate=None):
    """Test key, add if works, spawn agent"""
    print(f"🔍 Testing {provider} key: {key[:20]}...")
    
    tester = TESTERS.get(provider.lower())
    if not tester:
        print(f"⚠️ Unknown provider: {provider}")
        return False
    
    if tester(key):
        print(f"✅ Key works!")
        slot = add_key_to_env(provider, key)
        
        # Spawn new agent with this key
        if gate and slot:
            agent = gate.spawn_agent()
            if agent:
                from core.memory import save_agent_memory
                save_agent_memory(agent.id, "api_key", key)
                save_agent_memory(agent.id, "provider", provider)
                print(f"🌟 New agent {agent.name} spawned with {provider} key!")
        return True
    else:
        print(f"❌ Key failed — not added")
        return False

def verify_all_existing_keys():
    """Test ALL keys already in .env"""
    load_dotenv()
    print("\n🔍 Verifying all existing keys...")
    results = {"working": [], "failed": []}
    
    for provider, tester in TESTERS.items():
        i = 1
        while True:
            key = os.getenv(f"{provider.upper()}_API_KEY_{i}")
            if not key:
                break
            print(f"Testing {provider} key {i}...", end=" ")
            if tester(key):
                print("✅ Works!")
                results["working"].append(f"{provider}_{i}")
            else:
                print("❌ Failed")
                results["failed"].append(f"{provider}_{i}")
            i += 1
            time.sleep(1)
    
    print(f"\n📊 Results:")
    print(f"  ✅ Working: {len(results['working'])} keys")
    print(f"  ❌ Failed: {len(results['failed'])} keys")
    print(f"  Working: {', '.join(results['working'])}")
    return results

print("🔑 Key Manager loaded!")
