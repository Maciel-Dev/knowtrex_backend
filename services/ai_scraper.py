import os
import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()


async def fetch_page_content(url: str) -> str:
    """Fetch and extract text content from a URL"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, follow_redirects=True, timeout=30.0)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup)

    # Remove script and style elements
    for element in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript']):
        element.decompose()

    # Get text and clean it
    text = soup.get_text(separator=' ', strip=True)
    print(text)
    return text[:18000]  # Limit to avoid token limits


async def ai_search(url: str = "", description: str = ""):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Fetch the page content
    page_content = await fetch_page_content(url)

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a helpful assistant that helps with product search and recommendations. Analyze the provided webpage content and respond based on the user's request."},
        {"role": "user", "content": f"Webpage content:\n{page_content}\n\nUser request: {description}"}
    ]
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content.strip()