# 🐉 LUO GATE — WEB SEARCH
import requests

def search(query, max_results=5):
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Search unavailable: {e}"

print("🔍 Search loaded!")
