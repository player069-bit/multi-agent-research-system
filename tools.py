import sys
import os
from wsgiref import headers

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from tavily import TavilyClient
from langchain.tools import tool

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from rich import print


# Load environment variables
load_dotenv()


# Get Tavily API key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not set in the .env file.")


# Create Tavily client
tavily = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information.
    Returns the title, URL, and content snippet for each result.
    """

    if not query.strip():
        return "Error: Search query cannot be empty."

    try:
        results = tavily.search(
            query=query,
            max_results=2
        )

        if not results.get("results"):
            return "No search results found."

        formatted_results = []

        for result in results["results"]:
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            content = result.get("content", "No content")

            formatted_results.append(
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Snippet: {content}\n"
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Web search failed: {str(e)}"


# Test the tool
if __name__ == "__main__":
    result = web_search.invoke(
        {"query": "recent news about wars"}
    )

    print(result)
    
import requests
from bs4 import BeautifulSoup
from langchain.tools import tool


@tool
def scrape_url(url: str) -> str:
    """
    Scrape a webpage and return clean text content
    for deeper research and analysis.
    """
    if not url.strip():
        return "Error: URL cannot be empty."

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary webpage elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        # Extract clean text
        text = soup.get_text(separator=" ", strip=True)

# Remove excessive whitespace and invisible characters
        text = " ".join(text.split())
        text = text.replace("\u200b", "")

        # Limit output for the LLM
        return text[:5000]

    except requests.exceptions.Timeout:
        return "Could not scrape URL: Request timed out."

    except requests.exceptions.RequestException as e:
        return f"Could not scrape URL: Request failed - {str(e)}"

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"