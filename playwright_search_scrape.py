import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from langchain.tools import Tool

# ✅ Moved here from tools.py
from urllib.parse import urlparse

allowed_domains = [
    "wikipedia.org", "medium.com", "arxiv.org", "nature.com",
    "sciencedirect.com", "springer.com", "ieee.org", "npr.org",
    "bbc.com", "nytimes.com", "theguardian.com", "scholar.google.com",
    "huggingface.co", "stanford.edu", "mit.edu", "deepmind.com",
    "openai.com", "ox.ac.uk", "harvard.edu"
]

def is_allowed(url: str) -> bool:
    domain = urlparse(url).netloc
    return any(allowed in domain for allowed in allowed_domains)

HEADLESS = True
SCRAPE_CHAR_LIMIT = 6000


async def scrape_page(url: str) -> str:
    print("Scraping page:", url)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=15000)
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            paragraphs = soup.find_all("p")
            text = "\n".join(p.get_text() for p in paragraphs)
            return text.strip()[:SCRAPE_CHAR_LIMIT]
        except Exception as e:
            return f"[Scrape Error: {e}]"
        finally:
            await browser.close()

async def search_and_scrape(query: str) -> str:
    print("Searching for:", query)
    search_url = f"https://www.google.com/search?q={query}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        page = await browser.new_page()

        try:
            # Set user-agent to avoid bot detection
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                              " (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            })

            await page.goto(search_url, timeout=15000)
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")

            for a in soup.find_all("a"):
                href = a.get("href", "")
                if "url?q=" in href and not href.startswith("/search"):
                    url = href.split("url?q=")[-1].split("&")[0]
                    if is_allowed(url):
                        print("Found allowed URL:", url)
                        return await scrape_page(url)
            return "[No suitable or allowed result found]"
        except Exception as e:
            return f"[Search Error: {e}]"
        finally:
            await browser.close()

def sync_search_and_scrape(query: str) -> str:
    try:
        return asyncio.run(search_and_scrape(query))
    except RuntimeError:
        return asyncio.get_event_loop().run_until_complete(search_and_scrape(query))

search_scrape_tool = Tool.from_function(
    name="SearchScrape",
    description="Useful for searching the web for factual questions. Input should be a search query.",
    func=sync_search_and_scrape,
)
