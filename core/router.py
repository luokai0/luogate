# 🐉 LUO GATE — MEGA ROUTER
import os, time, requests
from dotenv import load_dotenv
load_dotenv()

GROQ_KEYS = [os.getenv(f"GROQ_API_KEY_{i}") for i in range(1,51) if os.getenv(f"GROQ_API_KEY_{i}")]
CEREBRAS_KEYS = [os.getenv(f"CEREBRAS_API_KEY_{i}") for i in range(1,20) if os.getenv(f"CEREBRAS_API_KEY_{i}")]
GEMINI_KEYS = [os.getenv(f"GEMINI_API_KEY_{i}") for i in range(1,30) if os.getenv(f"GEMINI_API_KEY_{i}")]
MISTRAL_KEYS = [os.getenv(f"MISTRAL_API_KEY_{i}") for i in range(1,20) if os.getenv(f"MISTRAL_API_KEY_{i}")]
OPENROUTER_KEYS = [os.getenv(f"OPENROUTER_API_KEY_{i}") for i in range(1,20) if os.getenv(f"OPENROUTER_API_KEY_{i}")]

idx = {"groq":0,"cerebras":0,"gemini":0,"mistral":0,"openrouter":0}
cooldowns = {}

def is_ready(key): return cooldowns.get(key,0) <= time.time()
def cooldown(key, secs=61): cooldowns[key] = time.time() + secs
def next_key(keys, p):
    for _ in range(len(keys)):
        i = idx[p] % len(keys)
        idx[p] += 1
        k = keys[i]
        if is_ready(k): return k, i+1
    return None, 0

print(f"🔑 {len(GROQ_KEYS)} Groq | {len(CEREBRAS_KEYS)} Cerebras | {len(GEMINI_KEYS)} Gemini | {len(MISTRAL_KEYS)} Mistral | {len(OPENROUTER_KEYS)} OpenRouter")

def ask_cerebras(prompt, max_tokens=2048):
    if not CEREBRAS_KEYS: return None
    key, num = next_key(CEREBRAS_KEYS, "cerebras")
    if not key: return None
    try:
        from cerebras.cloud.sdk import Cerebras
        client = Cerebras(api_key=key)
        r = client.chat.completions.create(
            model="llama-3.3-70b",
            messages=[{"role":"user","content":prompt}],
            max_tokens=max_tokens
        )
        print(f"⚡ Cerebras {num} responded!")
        return r.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "429" in err or "rate" in err.lower(): cooldown(key)
        return None

def ask_groq(prompt, max_tokens=2048, temperature=0.8):
    if not GROQ_KEYS: return None
    key, num = next_key(GROQ_KEYS, "groq")
    if not key: return None
    try:
        from groq import Groq
        client = Groq(api_key=key)
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        print(f"✅ Groq {num} responded!")
        return r.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "429" in err or "rate" in err.lower(): cooldown(key)
        return None

def ask_gemini(prompt, max_tokens=2048):
    if not GEMINI_KEYS: return None
    key, num = next_key(GEMINI_KEYS, "gemini")
    if not key: return None
    try:
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
            json={"contents":[{"parts":[{"text":prompt}]}]},
            timeout=30
        )
        data = r.json()
        if "candidates" in data:
            print(f"🔵 Gemini {num} responded!")
            return data["candidates"][0]["content"]["parts"][0]["text"]
        cooldown(key)
        return None
    except Exception as e:
        return None

def ask_mistral(prompt, max_tokens=2048):
    if not MISTRAL_KEYS: return None
    key, num = next_key(MISTRAL_KEYS, "mistral")
    if not key: return None
    try:
        from mistralai import Mistral
        client = Mistral(api_key=key)
        r = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role":"user","content":prompt}],
            max_tokens=max_tokens
        )
        print(f"🟡 Mistral {num} responded!")
        return r.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "429" in err or "rate" in err.lower(): cooldown(key)
        return None

def ask_openrouter(prompt, max_tokens=2048):
    if not OPENROUTER_KEYS: return None
    key, num = next_key(OPENROUTER_KEYS, "openrouter")
    if not key: return None
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},
            json={"model":"meta-llama/llama-3.3-70b-instruct:free","messages":[{"role":"user","content":prompt}],"max_tokens":max_tokens},
            timeout=30
        )
        data = r.json()
        if "choices" in data:
            print(f"🟢 OpenRouter {num} responded!")
            return data["choices"][0]["message"]["content"]
        cooldown(key)
        return None
    except: return None

def ask(prompt, max_tokens=2048, temperature=0.8):
    for fn in [ask_cerebras, ask_groq, ask_gemini, ask_mistral, ask_openrouter]:
        try:
            result = fn(prompt, max_tokens) if fn != ask_groq else fn(prompt, max_tokens, temperature)
            if result: return result
        except: continue
    return "❌ All providers exhausted."

def ask_fast(prompt): return ask(prompt, max_tokens=512)
def ask_deep(prompt): return ask(prompt, max_tokens=4096)

print("🚀 Mega Router ready — 5 providers!")
