# 🐉 LUO GATE SKILL — BROWSER CONTROL
from core.files import write_file
from datetime import datetime
import time

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_browser(headless=True):
    from playwright.sync_api import sync_playwright
    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=headless,
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
    page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})
    return p, browser, context, page

def scrape_page(url):
    try:
        p, browser, context, page = get_browser()
        page.goto(url, timeout=30000)
        time.sleep(3)
        content = page.inner_text("body")
        title = page.title()
        browser.close()
        p.stop()
        return {"title": title, "content": content[:5000], "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}

def fill_form(url, fields):
    """Fill a form on a webpage
    fields = {"placeholder_or_label": "value"}"""
    try:
        p, browser, context, page = get_browser()
        page.goto(url, timeout=30000)
        time.sleep(3)
        
        filled = 0
        for field, value in fields.items():
            try:
                selectors = [
                    f'input[placeholder*="{field}"]',
                    f'input[name*="{field}"]',
                    f'input[id*="{field}"]',
                    f'textarea[placeholder*="{field}"]',
                ]
                for sel in selectors:
                    try:
                        page.fill(sel, value, timeout=2000)
                        filled += 1
                        break
                    except: continue
            except: continue
        
        final_url = page.url
        browser.close()
        p.stop()
        return {"filled": filled, "total": len(fields), "final_url": final_url}
    except Exception as e:
        return {"error": str(e)}

def bypass_and_visit(url):
    """Visit URL with anti-detection measures"""
    try:
        p, browser, context, page = get_browser()
        
        # Remove webdriver detection
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        """)
        
        page.goto(url, timeout=30000)
        time.sleep(3)
        
        content = page.inner_text("body")
        browser.close()
        p.stop()
        return content[:3000]
    except Exception as e:
        return f"Error: {e}"

SKILLS = {
    "scrape_page": scrape_page,
    "fill_form": fill_form,
    "bypass_and_visit": bypass_and_visit,
}
print(f"🌐 Browser Skills loaded — {len(SKILLS)} skills!")
