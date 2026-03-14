# 🐉 LUO GATE — AUTO KEY COLLECTOR
# Uses Gmail+ trick to get unlimited free API keys
# Supports ALL providers from free-llm-api-resources

import time, re, os, json
from datetime import datetime
from playwright.sync_api import sync_playwright
from core.logs import log
from core.key_manager import verify_and_add

BASE_EMAIL = "creationslous@gmail.com"
GMAIL_PASS = "luorosie25"
KEYS_LOG = "memory/collected_keys.json"

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def make_email(provider, index):
    """Generate unique Gmail+ address"""
    base = BASE_EMAIL.replace("@gmail.com", "")
    return f"{base}+{provider}{index}@gmail.com"

def load_keys_log():
    try:
        with open(KEYS_LOG) as f:
            return json.load(f)
    except:
        return {"collected": [], "failed": [], "total": 0}

def save_keys_log(data):
    os.makedirs("memory", exist_ok=True)
    with open(KEYS_LOG, "w") as f:
        json.dump(data, f, indent=2)

def get_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
        ]
    )
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720}
    )
    page = context.new_page()
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        window.chrome = {runtime: {}};
    """)
    return p, browser, context, page

def login_google(page):
    """Login to Google account"""
    try:
        print("🔐 Logging into Google...")
        page.goto("https://accounts.google.com/signin", timeout=30000)
        time.sleep(2)
        
        # Enter email
        page.fill('input[type="email"]', BASE_EMAIL, timeout=10000)
        page.keyboard.press("Enter")
        time.sleep(3)
        
        # Enter password
        page.fill('input[type="password"]', GMAIL_PASS, timeout=10000)
        page.keyboard.press("Enter")
        time.sleep(5)
        
        # Check if logged in
        if "myaccount.google.com" in page.url or "google.com" in page.url:
            print("✅ Google login successful!")
            return True
        print("⚠️ Google login may have failed")
        return True  # Try anyway
    except Exception as e:
        print(f"⚠️ Google login error: {e}")
        return False

def get_groq_key(page, index):
    """Get Groq API key"""
    email = make_email("groq", index)
    print(f"\n🔑 Getting Groq key #{index} with {email}")
    try:
        # Sign up to Groq
        page.goto("https://console.groq.com/login", timeout=30000)
        time.sleep(3)
        
        # Try Google OAuth
        try:
            page.click("text=Continue with Google", timeout=5000)
            time.sleep(3)
            
            # Select account or enter email
            try:
                page.click(f"text={BASE_EMAIL}", timeout=3000)
            except:
                try:
                    page.fill('input[type="email"]', email, timeout=3000)
                    page.keyboard.press("Enter")
                    time.sleep(2)
                    page.fill('input[type="password"]', GMAIL_PASS, timeout=3000)
                    page.keyboard.press("Enter")
                except: pass
            time.sleep(5)
        except:
            pass
        
        # Go to keys page
        page.goto("https://console.groq.com/keys", timeout=30000)
        time.sleep(3)
        
        # Create new key
        try:
            page.click("text=Create API Key", timeout=5000)
            time.sleep(2)
            page.fill('input[placeholder*="name"]', f"LuoGate_{index}", timeout=3000)
            time.sleep(1)
            
            # Click create/submit
            for btn_text in ["Create", "Submit", "Generate", "Add"]:
                try:
                    page.click(f"text={btn_text}", timeout=2000)
                    break
                except: continue
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ Key creation: {e}")
        
        # Extract key
        content = page.inner_text("body")
        keys = re.findall(r'gsk_[a-zA-Z0-9]{52}', content)
        if keys:
            print(f"✅ Got Groq key!")
            return keys[0]
            
    except Exception as e:
        print(f"⚠️ Groq failed: {e}")
    return None

def get_gemini_key(page, index):
    """Get Gemini API key"""
    email = make_email("gemini", index)
    print(f"\n🔑 Getting Gemini key #{index}")
    try:
        page.goto("https://aistudio.google.com/apikey", timeout=30000)
        time.sleep(4)
        
        # Click create key
        for btn in ["Create API key", "Create API Key", "New API key"]:
            try:
                page.click(f"text={btn}", timeout=3000)
                time.sleep(3)
                break
            except: continue
        
        # Click create in dialog
        try:
            page.click("text=Create API key in new project", timeout=3000)
            time.sleep(5)
        except:
            try:
                page.click("button:has-text('Create')", timeout=3000)
                time.sleep(5)
            except: pass
        
        # Extract key
        content = page.inner_text("body")
        keys = re.findall(r'AIzaSy[a-zA-Z0-9_-]{33}', content)
        if keys:
            print(f"✅ Got Gemini key!")
            return keys[0]
            
    except Exception as e:
        print(f"⚠️ Gemini failed: {e}")
    return None

def get_openrouter_key(page, index):
    """Get OpenRouter API key"""
    email = make_email("openrouter", index)
    print(f"\n🔑 Getting OpenRouter key #{index} with {email}")
    try:
        # Sign up with email
        page.goto("https://openrouter.ai/", timeout=30000)
        time.sleep(3)
        
        # Click sign in
        for btn in ["Sign in", "Sign Up", "Get Started"]:
            try:
                page.click(f"text={btn}", timeout=3000)
                time.sleep(2)
                break
            except: continue
        
        # Try Google login
        try:
            page.click("text=Continue with Google", timeout=3000)
            time.sleep(3)
            try:
                page.click(f"text={BASE_EMAIL}", timeout=3000)
            except:
                page.fill('input[type="email"]', email, timeout=3000)
                page.keyboard.press("Enter")
            time.sleep(5)
        except:
            # Try email signup
            try:
                page.fill('input[type="email"]', email, timeout=3000)
                page.keyboard.press("Enter")
                time.sleep(3)
            except: pass
        
        # Go to keys
        page.goto("https://openrouter.ai/settings/keys", timeout=30000)
        time.sleep(3)
        
        # Create key
        try:
            page.click("text=Create Key", timeout=5000)
            time.sleep(2)
            try:
                page.fill('input', f"LuoGate_{index}", timeout=2000)
            except: pass
            for btn in ["Create", "Add", "Generate"]:
                try:
                    page.click(f"text={btn}", timeout=2000)
                    break
                except: continue
            time.sleep(3)
        except: pass
        
        # Extract key
        content = page.inner_text("body")
        keys = re.findall(r'sk-or-v1-[a-f0-9]{64}', content)
        if keys:
            print(f"✅ Got OpenRouter key!")
            return keys[0]
            
    except Exception as e:
        print(f"⚠️ OpenRouter failed: {e}")
    return None

def get_mistral_key(page, index):
    """Get Mistral API key"""
    email = make_email("mistral", index)
    print(f"\n🔑 Getting Mistral key #{index} with {email}")
    try:
        page.goto("https://console.mistral.ai/", timeout=30000)
        time.sleep(3)
        
        # Try Google login
        try:
            page.click("text=Continue with Google", timeout=3000)
            time.sleep(3)
            try:
                page.click(f"text={BASE_EMAIL}", timeout=3000)
            except: pass
            time.sleep(5)
        except:
            try:
                page.fill('input[type="email"]', email, timeout=3000)
                page.keyboard.press("Enter")
                time.sleep(3)
                page.fill('input[type="password"]', GMAIL_PASS, timeout=3000)
                page.keyboard.press("Enter")
                time.sleep(5)
            except: pass
        
        # Go to API keys
        page.goto("https://console.mistral.ai/home?profile_dialog=api-keys", timeout=30000)
        time.sleep(3)
        
        # Create key
        try:
            page.click("text=Create new key", timeout=5000)
            time.sleep(2)
            try:
                page.fill('input[placeholder*="name"]', f"LuoGate_{index}", timeout=2000)
            except: pass
            for btn in ["Create", "Generate", "Add"]:
                try:
                    page.click(f"text={btn}", timeout=2000)
                    break
                except: continue
            time.sleep(3)
        except: pass
        
        # Extract key
        content = page.inner_text("body")
        keys = re.findall(r'[a-zA-Z0-9]{32}', content)
        # Mistral keys are 32 chars
        for key in keys:
            if len(key) == 32:
                print(f"✅ Got Mistral key!")
                return key
                
    except Exception as e:
        print(f"⚠️ Mistral failed: {e}")
    return None

def get_cerebras_key(page, index):
    """Get Cerebras API key"""
    email = make_email("cerebras", index)
    print(f"\n🔑 Getting Cerebras key #{index} with {email}")
    try:
        page.goto("https://cloud.cerebras.ai/", timeout=30000)
        time.sleep(3)
        
        # Try Google login
        try:
            page.click("text=Continue with Google", timeout=3000)
            time.sleep(3)
            try:
                page.click(f"text={BASE_EMAIL}", timeout=3000)
            except: pass
            time.sleep(5)
        except:
            try:
                page.fill('input[type="email"]', email, timeout=3000)
                page.keyboard.press("Enter")
                time.sleep(3)
            except: pass
        
        # Go to API keys
        try:
            page.goto("https://cloud.cerebras.ai/platform?tab=apikeys", timeout=30000)
            time.sleep(3)
        except: pass
        
        # Create key
        try:
            page.click("text=Create API Key", timeout=5000)
            time.sleep(2)
            try:
                page.fill('input', f"LuoGate_{index}", timeout=2000)
            except: pass
            for btn in ["Create", "Generate", "Add"]:
                try:
                    page.click(f"text={btn}", timeout=2000)
                    break
                except: continue
            time.sleep(3)
        except: pass
        
        # Extract key
        content = page.inner_text("body")
        keys = re.findall(r'csk-[a-zA-Z0-9]{48}', content)
        if keys:
            print(f"✅ Got Cerebras key!")
            return keys[0]
            
    except Exception as e:
        print(f"⚠️ Cerebras failed: {e}")
    return None

# All providers
PROVIDERS = {
    "groq": get_groq_key,
    "gemini": get_gemini_key,
    "openrouter": get_openrouter_key,
    "mistral": get_mistral_key,
    "cerebras": get_cerebras_key,
}

def collect_keys(gate=None, providers=None, keys_per_provider=3):
    """Main key collection — runs all providers"""
    if providers is None:
        providers = list(PROVIDERS.keys())
    
    keys_log = load_keys_log()
    total_new = 0
    
    print(f"\n🚀 KEY COLLECTION STARTED")
    print(f"Providers: {providers}")
    print(f"Keys per provider: {keys_per_provider}")
    print("="*50)
    
    p, browser, context, page = get_browser()
    
    try:
        # Login to Google first
        login_google(page)
        time.sleep(3)
        
        # Collect from each provider
        for provider in providers:
            getter = PROVIDERS.get(provider)
            if not getter:
                continue
            
            print(f"\n📦 Collecting {keys_per_provider} {provider} keys...")
            
            for i in range(1, keys_per_provider + 1):
                try:
                    key = getter(page, i)
                    
                    if key:
                        # Verify and add
                        if verify_and_add(provider, key, gate):
                            keys_log["collected"].append({
                                "provider": provider,
                                "key": key[:20] + "...",
                                "time": ts()
                            })
                            keys_log["total"] += 1
                            total_new += 1
                            print(f"🎉 {provider} key #{i} collected and verified!")
                        else:
                            keys_log["failed"].append(f"{provider}_{i}")
                    else:
                        print(f"⚠️ {provider} key #{i} not obtained")
                        keys_log["failed"].append(f"{provider}_{i}")
                    
                    save_keys_log(keys_log)
                    time.sleep(5)
                    
                except Exception as e:
                    print(f"⚠️ {provider} #{i} error: {e}")
                    continue
    
    finally:
        browser.close()
        p.stop()
    
    print(f"\n{'='*50}")
    print(f"🎉 COLLECTION COMPLETE!")
    print(f"✅ New keys: {total_new}")
    print(f"🤖 Total agents: {len(gate.agents) if gate else 'N/A'}")
    print(f"💾 Log saved to memory/collected_keys.json")
    
    return total_new

print("🔑 Auto Key Collector loaded!")
