import logging
from typing import List, Dict, Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

from utils.constants import (
    UA, HTML_HINTS, CODE_TOKEN_REGEX,
    GITHUB_HEADERS, DEFAULT_GH_PER_PAGE, MAX_GH_PER_PAGE
)
from utils.scraper_utils import (
    assert_valid_url, ensure_per_page, to_raw_url, clean_text
)

logger = logging.getLogger(__name__)


def html_scrape(url: str) -> List[Dict[str, Any]]:
    try:
        resp = requests.get(url, headers=UA, timeout=30)
        resp.raise_for_status()
    except requests.HTTPError as e:
        code = e.response.status_code if e.response is not None else 500
        raise HTTPException(status_code=code, detail=f"Fetch failed ({code}) for URL: {url}")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Network error fetching {url}: {e}")

    soup = BeautifulSoup(resp.text, "html.parser")
    if soup.title and soup.title.text:
        title = soup.title.text.strip()
    else:
        h1 = soup.find("h1")
        title = (h1.get_text().strip() if h1 else "Untitled Architecture")

    text = clean_text(soup.get_text(separator="\n"))
    tokens = [kw for kw in HTML_HINTS if kw in text.lower()]

    logger.info("[scraper] html %s (len=%s, tokens=%s)", url, len(text), len(tokens))
    return [{
        "title": title or "Untitled Architecture",
        "source": url,
        "text": text,
        "tokens": tokens,
    }]


def github_api_scrape(api_url: str) -> List[Dict[str, Any]]:
    api_url = ensure_per_page(api_url)
    try:
        resp = requests.get(api_url, headers=GITHUB_HEADERS, timeout=60)
        if resp.status_code == 401:
            raise HTTPException(status_code=401, detail="GitHub 401 Unauthorized. Set GITHUB_TOKEN.")
        if resp.status_code == 403:
            msg = ""
            try:
                msg = resp.json().get("message", "")
            except Exception:
                pass
            raise HTTPException(status_code=429, detail=f"GitHub rate-limited/forbidden: {msg}")
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"GitHub API error: {e}")

    items = resp.json().get("items", [])
    logger.info("[scraper] GitHub API hits=%d", len(items))

    docs: List[Dict[str, Any]] = []
    for it in items:
        html_url = it.get("html_url")
        name = it.get("name") or "code"
        if not html_url:
            continue

        raw_url = to_raw_url(html_url)
        try:
            response = requests.get(raw_url, headers=GITHUB_HEADERS, timeout=60)
            response.raise_for_status()
        except requests.RequestException:
            continue

        content = response.text
        tokens = sorted(set(m.group(0) for m in CODE_TOKEN_REGEX.finditer(content)))
        docs.append({
            "title": f"Code: {name}",
            "source": html_url,          
            "text": content[:20000],     
            "tokens": tokens,
        })

    return docs


def scrape_url(url: str) -> List[Dict[str, Any]]:
    """
    Scraper:
      - If URL host is 'api.github.com' and path starts with '/search/code' -> GitHub code search
      - Else -> treat as a normal HTML page
    Returns: list of {title, source, text, tokens}
    """
    assert_valid_url(url)
    parsed_url = urlparse(url)
    host = parsed_url.netloc.lower()
    path = parsed_url.path

    if host == "api.github.com" and path.startswith("/search/code"):
        return github_api_scrape(url)

    return html_scrape(url)
