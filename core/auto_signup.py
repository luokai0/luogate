# 🐉 AUTO SIGNUP — Agents get API keys automatically
import time, requests, json, os
from core.logs import log
from core.key_manager import verify_and_add

def get_temp_email():
    try:
        r = requests.get("https://api.guerrillamail.com/ajax.php?f=get_email_address", timeout=10)
        data = r.json()
        return data.get("email_addr"), data.get("sid_token")
    except:
        return None, None

def check_inbox(sid, timeout=120):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"https://api.guerrillamail.com/ajax.php?f=get_email_list&offset=0&sid_token={sid}", timeout=10)
            emails = r.json().get("list", [])
            if emails:
                return emails
        except: pass
        time.sleep(5)
    return []

def auto_signup_openrouter(gate=None):
    """Auto signup to OpenRouter — no phone needed!"""
    print("\n🤖 Auto signing up to OpenRouter...")
    
    email, sid = get_temp_email()
    if not email:
        print("⚠️ Could not get temp email")
        return None
    
    print(f"📧 Using temp email: {email}")
    
    try:
        from playwright.sync_api import sync_playwright
        import time as t
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()
            
            # Go to OpenRouter signup
            print("🌐 Opening OpenRouter...")
            page.goto("https://openrouter.ai/", timeout=30000)
            t.sleep(3)
            
            # Click sign in
            try:
                page.click("text=Sign in", timeout=5000)
                t.sleep(2)
            except: pass
            
            # Try email signup
            try:
                page.fill('input[type="email"]', email, timeout=5000)
                page.keyboard.press("Enter")
                t.sleep(3)
                print(f"📧 Email entered: {email}")
            except Exception as e:
                print(f"⚠️ Could not fill email: {e}")
                browser.close()
                return None
            
            # Wait for verification email
            print("⏳ Waiting for verification email...")
            emails = check_inbox(sid, timeout=60)
            
            if emails:
                print(f"📬 Got {len(emails)} emails!")
                # Try to get verification link
                for em in emails:
                    try:
                        r = requests.get(
                            f"https://api.guerrillamail.com/ajax.php?f=fetch_email&email_id={em['mail_id']}&sid_token={sid}",
                            timeout=10
                        )
                        body = r.json().get("mail_body", "")
                        # Find verification link
                        import re
                        links = re.findall(r'https://[^\s<>"]+', body)
                        for link in links:
                            if "openrouter" in link or "verify" in link or "confirm" in link:
                                print(f"🔗 Found verification link!")
                                page.goto(link, timeout=30000)
                                t.sleep(5)
                                break
                    except: continue
            
            # Try to get API key
            try:
                page.goto("https://openrouter.ai/keys", timeout=30000)
                t.sleep(3)
                
                # Create new key
                try:
                    page.click("text=Create Key", timeout=5000)
                    t.sleep(2)
                    page.fill('input[placeholder*="name"]', "LuoGate", timeout=3000)
                    page.click("text=Create", timeout=3000)
                    t.sleep(2)
                except: pass
                
                # Get the key from page
                content = page.inner_text("body")
                import re
                keys = re.findall(r'sk-or-v1-[a-f0-9]{64}', content)
                
                if keys:
                    new_key = keys[0]
                    print(f"🔑 Got new OpenRouter key!")
                    browser.close()
                    
                    # Verify and add
                    if verify_and_add("openrouter", new_key, gate):
                        log("AUTO_SIGNUP", "SUCCESS", f"OpenRouter key added", "expand")
                        return new_key
                else:
                    print("⚠️ Could not extract key from page")
            except Exception as e:
                print(f"⚠️ Key extraction failed: {e}")
            
            browser.close()
    except Exception as e:
        print(f"⚠️ Signup failed: {e}")
    
    return None

def auto_signup_groq(gate=None):
    """Research Groq signup process"""
    print("\n🤖 Groq requires Google login — agents will guide you...")
    print("📌 Steps:")
    print("  1. Go to: https://console.groq.com")
    print("  2. Click 'Sign Up'")  
    print("  3. Use any Gmail account")
    print("  4. Go to: https://console.groq.com/keys")
    print("  5. Click 'Create API Key'")
    print("  6. Copy the key")
    print("  7. Come back and type: addkey groq YOUR_KEY")
    print("\n💡 Takes 2 minutes per account!")
    print("💡 Use different Gmail accounts for more keys!")

def expand_gate(gate, rounds=3):
    """Full expansion — try all auto methods"""
    print(f"\n🚀 EXPANSION MODE — {rounds} rounds")
    
    success = 0
    for i in range(rounds):
        print(f"\n🔄 Round {i+1}/{rounds}")
        
        # Try OpenRouter (most automatable)
        key = auto_signup_openrouter(gate)
        if key:
            success += 1
            print(f"✅ Round {i+1} success!")
        else:
            print(f"⚠️ Round {i+1} failed")
        
        time.sleep(10)
    
    print(f"\n✅ Expansion complete!")
    print(f"🔑 New keys added: {success}")
    print(f"🤖 Total agents: {len(gate.agents)}")
    
    # Guide for manual keys
    if success < rounds:
        auto_signup_groq()

print("🚀 Auto Signup loaded!")
